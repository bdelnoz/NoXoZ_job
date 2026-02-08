#!/usr/bin/env python3
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/services/vector_store.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Gestion du stockage vectoriel (Chroma) + métadonnées (SQLite) + ingestion/search pour NoXoZ_job
# Version: v1.2.1 – Date: 2026-02-08
#
# CHANGELOG:
# v1.2.1 - 2026-02-08:
#   - Fix: export DEFAULT_COLLECTION (évite ImportError dans api/monitor.py)
#   - Fix: migrations SQLite robustes (ALTER + fallback rebuild table si table legacy)
#   - Fix: sélection METADATA_DB avec fallback vers DB existante (metadata.db vs noxoz_metadata.db, etc.)
#   - Ajout: ensure_sqlite_schema() helper (à appeler côté endpoints si besoin)
# v1.2.0 - 2026-02-08:
#   - Ajout migrations SQLite automatiques (PRAGMA table_info + ALTER TABLE)
#   - Ajout tables "files" + "documents" (chunk-level) + index
#   - Correction compat: base existante sans colonne file_id (fix "no such column: file_id")
#   - Ajout fonctions utilitaires: compute_file_id, upsert_file_record, delete_file_records
#   - Ajout commentaires détaillés et helpers pour gestion future (re-ingestion/purge/rebuild)
# v1.1.0 - 2026-02-06:
#   - Version initiale (chemins projet, init chroma/sqlite, ingest_file, search_similar)
################################################################################

import os
import json
import hashlib
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timezone

import chromadb

# Embeddings (LangChain community)
from langchain_community.embeddings import HuggingFaceEmbeddings

# Parsers basiques (déjà utilisés chez toi)
from pypdf import PdfReader
import docx


# ==============================================================================
# 0) CONSTANTES EXPORTÉES (utilisées ailleurs)
# ==============================================================================

DEFAULT_COLLECTION = "noxoz_documents"


# ==============================================================================
# 1) PATHS PROJET (compat ancienne arborescence)
# ==============================================================================

# NOTE:
# - Ce fichier est dans: .../2_Sources/2.1_Python/services/vector_store.py
# - parents[3] remonte à la racine projet: .../NoXoZ_job
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "3_Data"

# Chroma (nouveau layout)
VECTORS_DIR = DATA_DIR / "3.1_Vectors" / "chroma_link"
if not VECTORS_DIR.exists():
    # Compat legacy
    legacy_vectors_dir = DATA_DIR / "Vectors" / "chroma_link"
    if legacy_vectors_dir.exists():
        VECTORS_DIR = legacy_vectors_dir

# SQLite metadata (nouveau layout)
metadata_dir = DATA_DIR / "Metadata"
if not metadata_dir.exists():
    # Compat legacy
    legacy_metadata_dir = DATA_DIR / "3.2_Metadata"
    if legacy_metadata_dir.exists():
        metadata_dir = legacy_metadata_dir

# Choix DB par défaut
_default_db = metadata_dir / "metadata.db"

# Fallback: si metadata.db n'existe pas mais qu'une autre DB existe déjà, on la prend
# (évite “deux DB différentes” selon les scripts)
if not _default_db.exists():
    candidates = sorted(metadata_dir.glob("*.db"))
    if candidates:
        _default_db = candidates[0]

METADATA_DB = _default_db

# Uploads (utilisé par ingestion.py pour stocker les fichiers reçus)
UPLOADS_DIR = DATA_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Ensure dirs exist
VECTORS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DB.parent.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 2) CHROMA INIT
# ==============================================================================

def init_chroma() -> Tuple[chromadb.PersistentClient, any]:
    """
    Initialise Chroma en mode persistant.
    On récupère (ou crée) la collection standard DEFAULT_COLLECTION.
    """
    client = chromadb.PersistentClient(path=str(VECTORS_DIR))
    collection = client.get_or_create_collection(DEFAULT_COLLECTION)
    return client, collection


# ==============================================================================
# 3) SQLITE HELPERS + MIGRATIONS
# ==============================================================================

def _sqlite_table_exists(cursor: sqlite3.Cursor, table: str) -> bool:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    return cursor.fetchone() is not None


def _sqlite_table_columns(cursor: sqlite3.Cursor, table: str) -> set[str]:
    """
    Retourne l'ensemble des colonnes existantes pour une table donnée.
    """
    cursor.execute(f"PRAGMA table_info({table});")
    return {row[1] for row in cursor.fetchall()}  # row[1] = column name


def _sqlite_add_column(cursor: sqlite3.Cursor, table: str, col: str, ddl_fragment: str) -> bool:
    """
    Ajoute une colonne si absente.
    - ddl_fragment est la définition SQL complète SANS le nom de table
      ex: "file_id TEXT" ou "updated_at TEXT NOT NULL DEFAULT '...'"
    Retourne True si ajouté, False sinon.
    """
    cols = _sqlite_table_columns(cursor, table)
    if col not in cols:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {ddl_fragment};")
        return True
    return False


def _sqlite_rebuild_documents_table_if_needed(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Rebuild ultra-robuste pour le cas où la table documents est legacy
    et que les ALTER ne suffisent pas / schéma trop différent.
    - On conserve ce qu'on peut (source_path, ingestion_date, etc.)
    - On garantit un schéma final compatible avec le code actuel.
    """
    if not _sqlite_table_exists(cursor, "documents"):
        return

    cols = _sqlite_table_columns(cursor, "documents")
    # Si on a déjà au moins chunk_id et file_id, on ne touche pas
    if "file_id" in cols and "chunk_id" in cols and "chunk_index" in cols:
        return

    # Crée une nouvelle table clean
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents_new (
            chunk_id TEXT PRIMARY KEY,
            file_id TEXT,
            chunk_index INTEGER,
            source_path TEXT,
            ingestion_date TEXT
        )
    """)

    # Heuristique: map anciennes colonnes possibles -> nouvelles
    # cas vu dans tes anciens snippets: documents(id, filename, source, ingestion_date)
    # On essaye de récupérer un "source_path"
    source_col = None
    for c in ("source_path", "source", "path", "filepath", "file_path"):
        if c in cols:
            source_col = c
            break

    ingestion_col = "ingestion_date" if "ingestion_date" in cols else None

    # On copie ce qu'on peut (sans chunk_id/file_id, on crée des placeholder uniques)
    # chunk_id doit être unique: on utilise rowid
    if source_col or ingestion_col:
        select_parts = []
        if source_col:
            select_parts.append(f"{source_col}")
        else:
            select_parts.append("NULL")
        if ingestion_col:
            select_parts.append(f"{ingestion_col}")
        else:
            select_parts.append("NULL")

        cursor.execute(f"SELECT rowid, {', '.join(select_parts)} FROM documents;")
        rows = cursor.fetchall()
        now = datetime.now(timezone.utc).isoformat()

        for row in rows:
            rowid = row[0]
            src = row[1]
            ing = row[2] if len(row) > 2 else None
            # chunk_id placeholder: legacy_<rowid>
            chunk_id = f"legacy_{rowid}"
            cursor.execute("""
                INSERT OR IGNORE INTO documents_new (chunk_id, file_id, chunk_index, source_path, ingestion_date)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, None, None, src, ing or now))

    # Swap
    cursor.execute("DROP TABLE documents;")
    cursor.execute("ALTER TABLE documents_new RENAME TO documents;")
    conn.commit()
def init_sqlite() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Initialise SQLite et applique des migrations AUTOMATIQUES si l'ancienne base
    existe avec un schéma incomplet (ex: pas de colonne updated_at).
    """
    conn = sqlite3.connect(METADATA_DB)
    cursor = conn.cursor()

    # --------------------------------------------------------------------------
    # Table FILES (création si absente)
    # --------------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            original_name TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            ext TEXT,
            size_bytes INTEGER,
            sha256 TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'ingested'
        )
    """)

    # --------------------------------------------------------------------------
    # Table DOCUMENTS (création si absente)
    # --------------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            chunk_id TEXT PRIMARY KEY,
            file_id TEXT,
            chunk_index INTEGER,
            source_path TEXT,
            ingestion_date TEXT
        )
    """)

    # --------------------------------------------------------------------------
    # MIGRATIONS: FILES (si table existante ancienne / incomplète)
    # --------------------------------------------------------------------------
    if _sqlite_table_exists(cursor, "files"):
        # Ajoute les colonnes manquantes (sinon: "no such column: updated_at", etc.)
        _sqlite_add_column(cursor, "files", "original_name", "original_name TEXT")
        _sqlite_add_column(cursor, "files", "stored_path", "stored_path TEXT")
        _sqlite_add_column(cursor, "files", "ext", "ext TEXT")
        _sqlite_add_column(cursor, "files", "size_bytes", "size_bytes INTEGER")
        _sqlite_add_column(cursor, "files", "sha256", "sha256 TEXT")

        _sqlite_add_column(cursor, "files", "created_at", "created_at TEXT")
        _sqlite_add_column(cursor, "files", "updated_at", "updated_at TEXT")

        _sqlite_add_column(cursor, "files", "version", "version INTEGER NOT NULL DEFAULT 1")
        _sqlite_add_column(cursor, "files", "status", "status TEXT NOT NULL DEFAULT 'ingested'")

        # Si created_at/updated_at viennent d’être ajoutés, on les backfill (sinon NULL partout)
        cols = _sqlite_table_columns(cursor, "files")
        now = datetime.now(timezone.utc).isoformat()

        if "created_at" in cols:
            cursor.execute("UPDATE files SET created_at = COALESCE(created_at, ?) WHERE created_at IS NULL OR created_at = '';", (now,))
        if "updated_at" in cols:
            cursor.execute("UPDATE files SET updated_at = COALESCE(updated_at, ?) WHERE updated_at IS NULL OR updated_at = '';", (now,))

    # --------------------------------------------------------------------------
    # MIGRATIONS: DOCUMENTS (si table existante ancienne / incomplète)
    # --------------------------------------------------------------------------
    if _sqlite_table_exists(cursor, "documents"):
        _sqlite_add_column(cursor, "documents", "file_id", "file_id TEXT")
        _sqlite_add_column(cursor, "documents", "chunk_id", "chunk_id TEXT")
        _sqlite_add_column(cursor, "documents", "chunk_index", "chunk_index INTEGER")
        _sqlite_add_column(cursor, "documents", "source_path", "source_path TEXT")
        _sqlite_add_column(cursor, "documents", "ingestion_date", "ingestion_date TEXT")

    # Index (safe)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_file_id ON documents(file_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_chunk_id ON documents(chunk_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_files_updated_at ON files(updated_at)")

    conn.commit()
    return conn, cursor

def ensure_sqlite_schema() -> None:
    """
    Helper safe: juste “assure que le schéma existe”.
    Utile si un endpoint ouvre SQLite ailleurs : il doit appeler ça une fois.
    """
    conn, _ = init_sqlite()
    conn.close()


# ==============================================================================
# 4) FILE UTILITIES: hash, ids, metadata
# ==============================================================================

def sha256_file(path: str, buf_size: int = 1024 * 1024) -> str:
    """
    Calcule sha256 d'un fichier.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(buf_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def compute_file_id(file_path: str) -> str:
    """
    file_id = sha256(file_content)
    => stable: reupload du même contenu = même file_id
    """
    return sha256_file(file_path)


def upsert_file_record(
    cursor: sqlite3.Cursor,
    file_id: str,
    original_name: str,
    stored_path: str,
    ext: str,
    size_bytes: int,
    sha256: str,
    status: str = "ingested",
    bump_version: bool = False,
):
    """
    Upsert d'une ligne dans files.
    - bump_version=True => version = version+1 si déjà présent
    """
    now = datetime.now(timezone.utc).isoformat()

    cursor.execute("SELECT version FROM files WHERE file_id = ?;", (file_id,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO files (file_id, original_name, stored_path, ext, size_bytes, sha256, created_at, updated_at, version, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (file_id, original_name, stored_path, ext, size_bytes, sha256, now, now, 1, status))
    else:
        current_version = int(row[0]) if row[0] is not None else 1
        new_version = (current_version + 1) if bump_version else current_version
        cursor.execute("""
            UPDATE files
            SET original_name = ?, stored_path = ?, ext = ?, size_bytes = ?, sha256 = ?, updated_at = ?, version = ?, status = ?
            WHERE file_id = ?
        """, (original_name, stored_path, ext, size_bytes, sha256, now, new_version, status, file_id))


def delete_file_records(cursor: sqlite3.Cursor, file_id: str):
    """
    Supprime les métadonnées SQLite liées à un file_id.
    (La purge Chroma doit être faite séparément.)
    """
    cursor.execute("DELETE FROM documents WHERE file_id = ?;", (file_id,))
    cursor.execute("DELETE FROM files WHERE file_id = ?;", (file_id,))


# ==============================================================================
# 5) LOADERS: extraction texte (simple, 1 chunk par fichier)
# ==============================================================================

def load_file_text(file_path: str) -> List[str]:
    """
    Charge le contenu texte d'un fichier.
    Retourne une liste de chunks (ici: 1 chunk = 1 doc complet).
    Tu pourras améliorer plus tard (splitters).
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(file_path)
        return ["\n".join([page.extract_text() or "" for page in reader.pages])]
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return ["\n".join([p.text for p in doc.paragraphs])]
    elif ext in [".md", ".txt", ".json", ".xml"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]
    else:
        raise ValueError(f"Format non supporté: {ext}")


# ==============================================================================
# 6) INGESTION: Chroma + SQLite (avec file_id stable)
# ==============================================================================

def ingest_file(
    file_path: str,
    reingest: bool = False,
    bump_version: bool = False,
) -> Dict:
    """
    Ingestion d'un fichier sur disque:
    - Calcule file_id (sha256)
    - Upsert dans table files
    - (Optionnel) purge des anciens chunks (si reingest=True)
    - Ajout des chunks dans Chroma
    - Enregistre chunks dans SQLite (documents)

    reingest=True:
      - supprime d'abord les vecteurs et rows SQLite pour ce file_id
      - puis re-crée proprement

    bump_version=True:
      - si même file_id reingesté / reuploadé => version++ dans files
    """
    client, collection = init_chroma()
    conn, cursor = init_sqlite()

    # --- identification fichier ---
    p = Path(file_path)
    ext = p.suffix.lower()
    size_bytes = p.stat().st_size if p.exists() else 0
    file_sha = sha256_file(str(p))
    file_id = file_sha  # stable

    # --- upsert metadata file ---
    upsert_file_record(
        cursor=cursor,
        file_id=file_id,
        original_name=p.name,
        stored_path=str(p),
        ext=ext,
        size_bytes=size_bytes,
        sha256=file_sha,
        status="ingesting",
        bump_version=bump_version,
    )
    conn.commit()

    # --- (optionnel) purge avant reingest ---
    if reingest:
        try:
            cursor.execute("SELECT chunk_id FROM documents WHERE file_id = ? AND chunk_id IS NOT NULL;", (file_id,))
            existing = [r[0] for r in cursor.fetchall() if r and r[0]]
            if existing:
                collection.delete(ids=existing)
        except Exception:
            pass

        cursor.execute("DELETE FROM documents WHERE file_id = ?;", (file_id,))
        conn.commit()

    # --- extraction texte ---
    texts = load_file_text(str(p))
    chunk_ids = [f"{file_id}_{i}" for i in range(len(texts))]
    metadatas = [{
        "file_id": file_id,
        "source": str(p),
        "chunk_index": i,
        "original_name": p.name,
    } for i in range(len(texts))]

    # --- embeddings ---
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embeddings_model.embed_documents(texts)

    # --- add Chroma ---
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=chunk_ids,
        embeddings=embeddings,
    )

    # --- persist ---
    try:
        client.persist()
    except Exception:
        pass

    # --- write SQLite documents ---
    now = datetime.now(timezone.utc).isoformat()
    for i, chunk_id in enumerate(chunk_ids):
        cursor.execute("""
            INSERT OR REPLACE INTO documents (chunk_id, file_id, chunk_index, source_path, ingestion_date)
            VALUES (?, ?, ?, ?, ?)
        """, (chunk_id, file_id, i, str(p), now))

    # --- finalize status ---
    cursor.execute(
        "UPDATE files SET status = ?, updated_at = ? WHERE file_id = ?;",
        ("ingested", now, file_id),
    )

    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "file_id": file_id,
        "file_path": str(p),
        "chunks": len(texts),
        "chunk_ids": chunk_ids,
    }


# ==============================================================================
# 7) SEARCH: similarité Chroma (embeddings calculés côté client)
# ==============================================================================

def search_similar(query: str, k: int = 5) -> List[Dict]:
    """
    Recherche sémantique:
    - calcule embedding de query
    - query Chroma via query_embeddings
    """
    _, collection = init_chroma()

    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    q_emb = embeddings_model.embed_query(query)

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["metadatas", "documents", "ids"],
    )

    docs: List[Dict] = []
    if results and results.get("documents") and results["documents"]:
        for doc_text, meta, _id in zip(results["documents"][0], results["metadatas"][0], results["ids"][0]):
            docs.append({
                "id": _id,
                "text": doc_text,
                "source": (meta or {}).get("source"),
                "file_id": (meta or {}).get("file_id"),
                "chunk_index": (meta or {}).get("chunk_index"),
            })
    return docs


# ==============================================================================
# 8) MAINTENANCE FUTURE (stubs utiles)
# ==============================================================================

def purge_file(file_id: str) -> Dict:
    """
    Purge complète d'un fichier (Chroma + SQLite).
    - Retire les vecteurs via ids connus dans SQLite
    - Supprime les rows dans SQLite
    """
    client, collection = init_chroma()
    conn, cursor = init_sqlite()

    cursor.execute("SELECT chunk_id FROM documents WHERE file_id = ? AND chunk_id IS NOT NULL;", (file_id,))
    chunk_ids = [r[0] for r in cursor.fetchall() if r and r[0]]

    if chunk_ids:
        try:
            collection.delete(ids=chunk_ids)
        except Exception:
            pass

    delete_file_records(cursor, file_id)
    conn.commit()
    conn.close()

    try:
        client.persist()
    except Exception:
        pass

    return {"status": "ok", "purged_file_id": file_id, "deleted_chunks": len(chunk_ids)}


def rebuild_chroma_from_sqlite() -> Dict:
    """
    Rebuild (concept) :
    - Lis table files
    - Recalcule embeddings pour chaque fichier (depuis stored_path)
    - Réécrit collection Chroma

    NOTE: ici c'est une ébauche. Un vrai rebuild:
    - drop collection
    - recreate
    - bulk add
    """
    return {"status": "todo", "message": "rebuild_chroma_from_sqlite() non implémenté (stub)"}  # pragma: no cover
