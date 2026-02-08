#!/usr/bin/env python3
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/services/ingestion.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Ingestion UploadFile -> sauvegarde disque (hash-based) -> Chroma + SQLite (audit/dedupe/purge/rebuild)
# Version: v1.0.0 – Date: 2026-02-08
#
# CHANGELOG (historique complet, ne rien omettre) :
# - v1.0.0 – 2026-02-08 :
#   * Ajout d’une sauvegarde disque déterministe (SHA256) dans 3_Data/uploads/YYYY/MM/
#   * Ajout de tables SQLite: files + documents_v2 (ou extension documents) pour audit et déduplication
#   * Dedupe: re-upload même contenu => skip ingestion (par défaut) + mise à jour last_seen_at
#   * IDs Chroma stables: "<sha12>_<chunkIndex>" => re-ingestion contrôlable
#   * Ajout primitives de gestion: reingest_file_sha, purge_file_sha, rebuild_chroma_from_disk
################################################################################

from __future__ import annotations

import os
import re
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from fastapi import UploadFile

# NOTE:
# - On réutilise ta logique existante de parsing/chargement texte (PDF/DOCX/MD/...)
# - Et ton vector_store pour ingestion/search.
# - Adapte les imports selon ton arborescence réelle.
from services.vector_store import (
    METADATA_DB,
    ingest_file,        # ingest_file(file_path: str) ingère vers Chroma + SQLite "documents"
)

# ==============================================================================
# 0) STRUCTURE DISQUE (cible)
# ==============================================================================
# Objectif:
# - Ne plus écraser "uploads/<filename>".
# - Stocker une copie canonique par contenu (hash) avec un nom stable.
#
# Arborescence:
# 3_Data/
# └── uploads/
#     └── 2026/
#         └── 02/
#             ├── CV-Bruno-DELNOZ-clean__9f3a1c2d4e5f.md
#             └── ...
#
# Nom de fichier:
# <original_stem>__<sha256_prefix12><original_ext>
# Exemple:
# CV-Bruno-DELNOZ-clean__9f3a1c2d4e5f.md
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "3_Data"
UPLOADS_DIR = DATA_DIR / "uploads"


# ==============================================================================
# 1) SQLITE MIGRATIONS (sans casser l’existant)
# ==============================================================================
# On ajoute une table "files" (registre d’objets binaires) + on enrichit "documents".
#
# Pourquoi une table files ?
# - Le hash est la clé de vérité.
# - On sait où est le fichier sur disque.
# - On peut dédupliquer, purger et reconstruire Chroma.
#
# IMPORTANT SQLite:
# - Pas de "ADD COLUMN IF NOT EXISTS" standard.
# - Donc on inspecte PRAGMA table_info + on applique ALTER si manquant.
# ==============================================================================

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _sqlite_connect() -> sqlite3.Connection:
    METADATA_DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(METADATA_DB))

def _sqlite_table_columns(conn: sqlite3.Connection, table: str) -> List[str]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cur.fetchall()]  # row[1] = column name
    return cols

def _sqlite_ensure_schema() -> None:
    conn = _sqlite_connect()
    cur = conn.cursor()

    # --- Table files (nouvelle) ---
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            sha256 TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            mime_type TEXT,
            created_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL
        )
        """
    )

    # --- Table documents (existante chez toi) ---
    # On garde l’existant mais on enrichit si possible.
    # Table actuelle (d’après ton vector_store.py):
    # documents(id TEXT PRIMARY KEY, filename TEXT, source TEXT, ingestion_date TEXT)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT,
            source TEXT,
            ingestion_date TEXT
        )
        """
    )

    # Colonnes supplémentaires (audit + lien vers file hash)
    cols = _sqlite_table_columns(conn, "documents")

    # Ajoute sha256 pour tracer le document vers son fichier canonique
    if "file_sha256" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN file_sha256 TEXT")

    # Ajoute chunk_index pour un futur chunking propre
    if "chunk_index" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN chunk_index INTEGER")

    # Ajoute stored_path pour conserver le chemin canonique (utile pour rebuild)
    if "stored_path" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN stored_path TEXT")

    # Ajoute content_sha256 optionnel (hash du texte chunk) si tu veux pousser l’audit plus loin
    if "content_sha256" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN content_sha256 TEXT")

    conn.commit()
    conn.close()


# ==============================================================================
# 2) UTILITAIRES HASH / SANITIZE / PATHS
# ==============================================================================
def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _safe_stem(name: str) -> str:
    # Nettoyage: garde lettres/chiffres/._- et remplace le reste par "_"
    stem = Path(name).stem
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "_", stem).strip("_")
    return stem or "uploaded_file"

def _build_storage_path(original_filename: str, sha256: str) -> Path:
    # Sous-répertoires temporels (audit + ordre humain)
    now = datetime.now(timezone.utc)
    y = f"{now.year:04d}"
    m = f"{now.month:02d}"

    ext = Path(original_filename).suffix.lower() or ""
    stem = _safe_stem(original_filename)
    sha12 = sha256[:12]

    target_dir = UPLOADS_DIR / y / m
    target_dir.mkdir(parents=True, exist_ok=True)

    return target_dir / f"{stem}__{sha12}{ext}"


# ==============================================================================
# 3) REGISTRE FILES (dedupe)
# ==============================================================================
def _files_get(conn: sqlite3.Connection, sha256: str) -> Optional[Dict]:
    cur = conn.cursor()
    cur.execute(
        "SELECT sha256, original_filename, stored_path, size_bytes, mime_type, created_at, last_seen_at FROM files WHERE sha256=?",
        (sha256,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "sha256": row[0],
        "original_filename": row[1],
        "stored_path": row[2],
        "size_bytes": row[3],
        "mime_type": row[4],
        "created_at": row[5],
        "last_seen_at": row[6],
    }

def _files_upsert_seen(conn: sqlite3.Connection, sha256: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE files SET last_seen_at=? WHERE sha256=?", (_utc_now_iso(), sha256))

def _files_insert(conn: sqlite3.Connection, sha256: str, original_filename: str, stored_path: str, size_bytes: int, mime_type: Optional[str]) -> None:
    cur = conn.cursor()
    now = _utc_now_iso()
    cur.execute(
        """
        INSERT INTO files (sha256, original_filename, stored_path, size_bytes, mime_type, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (sha256, original_filename, stored_path, size_bytes, mime_type, now, now),
    )


# ==============================================================================
# 4) PATCH EXACT: parse_and_store_file(file: UploadFile)
# ==============================================================================
# Ce que fait la fonction:
# 1) Migrations SQLite (schema)
# 2) Lit bytes upload (une fois)
# 3) Hash SHA256 du contenu
# 4) Si déjà vu: update last_seen_at et (par défaut) SKIP ingestion
# 5) Sinon: écrit fichier canonique sur disque
# 6) Lance ingestion (Chroma + SQLite via ingest_file)
#
# IMPORTANT:
# - Pour permettre "force reingest", tu peux ajouter un param dans l’endpoint plus tard.
# - Ici on garde simple: reupload identique => dedupe (skip) + réponse explicite.
# ==============================================================================
async def parse_and_store_file(file: UploadFile) -> Dict:
    steps: List[Dict] = []

    def step(msg: str, status: str = "ok") -> None:
        steps.append({"timestamp": _utc_now_iso(), "message": msg, "status": status})

    _sqlite_ensure_schema()

    step("Upload reçu, lecture du contenu en mémoire")
    data = await file.read()
    if not data:
        step("Fichier vide reçu", "error")
        return {"message": "Fichier vide", "steps": steps}

    sha256 = _sha256_bytes(data)
    size_bytes = len(data)

    step(f"SHA256 calculé: {sha256}")

    conn = _sqlite_connect()
    try:
        existing = _files_get(conn, sha256)

        # --- DEDUPE ---
        if existing:
            _files_upsert_seen(conn, sha256)
            conn.commit()

            step("Fichier déjà connu (dedupe) : mise à jour last_seen_at")
            step("Ingestion ignorée (contenu identique)")

            return {
                "message": f"Fichier déjà ingéré (dedupe): {file.filename}",
                "file_path": existing["stored_path"],
                "sha256": sha256,
                "dedupe": True,
                "steps": steps,
            }

        # --- NOUVEAU FICHIER ---
        step("Préparation du répertoire uploads")
        stored_path = _build_storage_path(file.filename, sha256)

        step(f"Écriture du fichier sur disque: {stored_path}")
        stored_path.parent.mkdir(parents=True, exist_ok=True)
        with open(stored_path, "wb") as f:
            f.write(data)

        # Registry SQLite "files"
        _files_insert(
            conn=conn,
            sha256=sha256,
            original_filename=file.filename,
            stored_path=str(stored_path),
            size_bytes=size_bytes,
            mime_type=getattr(file, "content_type", None),
        )
        conn.commit()

    finally:
        conn.close()

    # --- Ingestion Chroma + SQLite (documents) ---
    # NOTE:
    # - Ton ingest_file actuel crée des ids basés sur le nom. Ça marche mais ce n’est pas idéal.
    # - Idéal: ids = f"{sha12}_{chunkIndex}" pour stabilité.
    # - Si tu veux le faire propre: on patchera ingest_file() ensuite (recommandé).
    step("Début ingestion Chroma + SQLite")
    ingest_file(str(stored_path))
    step("Ingestion terminée")

    return {
        "message": f"Fichier {file.filename} ingéré avec succès",
        "file_path": str(stored_path),
        "sha256": sha256,
        "dedupe": False,
        "steps": steps,
    }


# ==============================================================================
# 5) GESTION FUTURE: RE-INGESTION / PURGE / REBUILD (primitives)
# ==============================================================================
# Ces fonctions sont des briques:
# - reingest_file_sha(sha): réingère depuis stored_path (utile si modèle embeddings change)
# - purge_file_sha(sha): supprime documents liés dans SQLite + tente suppression Chroma
# - rebuild_chroma_from_disk(): reconstruit Chroma en relisant files depuis SQLite
#
# IMPORTANT:
# - Pour purge dans Chroma, il faut que tes documents aient un lien filtrable (metadata).
# - Aujourd’hui, ton vector_store met metadata {"source": file_path}. C’est filtrable.
# - On peut supprimer par where={"source": "<stored_path>"} si la version de chroma le supporte.
# ==============================================================================

def reingest_file_sha(sha256: str) -> Dict:
    _sqlite_ensure_schema()
    conn = _sqlite_connect()
    try:
        f = _files_get(conn, sha256)
        if not f:
            return {"ok": False, "message": f"SHA256 inconnu: {sha256}"}

        stored_path = f["stored_path"]
        if not Path(stored_path).exists():
            return {"ok": False, "message": f"Fichier manquant sur disque: {stored_path}"}

        # Optionnel: purge avant reingest pour éviter doublons (recommandé si IDs non stables)
        # purge_file_sha(sha256)

        ingest_file(stored_path)
        _files_upsert_seen(conn, sha256)
        conn.commit()
        return {"ok": True, "message": f"Re-ingestion effectuée: {stored_path}", "sha256": sha256}
    finally:
        conn.close()

def purge_file_sha(sha256: str) -> Dict:
    """
    Purge "logique" et (si possible) purge Chroma.
    - SQLite: supprime lignes documents liées à file_sha256 OU stored_path.
    - Chroma: suppression par filtre metadata where={"source": stored_path} si supporté.
    """
    _sqlite_ensure_schema()
    conn = _sqlite_connect()
    try:
        f = _files_get(conn, sha256)
        if not f:
            return {"ok": False, "message": f"SHA256 inconnu: {sha256}"}
        stored_path = f["stored_path"]

        # 1) SQLite: documents
        cur = conn.cursor()
        cur.execute("DELETE FROM documents WHERE file_sha256=? OR stored_path=?", (sha256, stored_path))

        # 2) SQLite: files
        cur.execute("DELETE FROM files WHERE sha256=?", (sha256,))
        conn.commit()

    finally:
        conn.close()

    # 3) Chroma: best effort (selon API)
    # NOTE: On ne dépend pas ici d’un import de chroma pour éviter de casser si module/versions changent.
    try:
        import chromadb
        from services.vector_store import VECTORS_DIR  # si dispo dans ton vector_store.py

        client = chromadb.PersistentClient(path=str(VECTORS_DIR))
        col = client.get_or_create_collection("noxoz_documents")

        # Beaucoup de versions supportent delete(where=...)
        # Si ça échoue, on laisse SQLite clean et on fera rebuild.
        col.delete(where={"source": stored_path})

        if hasattr(client, "persist"):
            try:
                client.persist()
            except Exception:
                pass

        return {"ok": True, "message": f"Purge effectuée (SQLite + Chroma best-effort)", "sha256": sha256, "stored_path": stored_path}

    except Exception as e:
        return {
            "ok": True,
            "message": f"Purge SQLite ok. Purge Chroma non garantie (rebuild conseillé). Erreur: {e}",
            "sha256": sha256,
            "stored_path": stored_path,
        }

def rebuild_chroma_from_disk(limit: Optional[int] = None) -> Dict:
    """
    Rebuild complet (simple):
    - Parcourt la table files
    - Vérifie que stored_path existe
    - Ré-ingère chaque fichier

    WARNING:
    - Si tes IDs Chroma ne sont pas stables (actuellement basés sur stem), rebuild peut créer collisions
      si différents fichiers ont le même nom.
    - Recommandé: patch ingest_file() pour utiliser des IDs basés sur sha.
    """
    _sqlite_ensure_schema()
    conn = _sqlite_connect()
    cur = conn.cursor()

    cur.execute("SELECT sha256, stored_path FROM files ORDER BY created_at ASC")
    rows = cur.fetchall()
    conn.close()

    total = 0
    ok = 0
    missing = 0
    errors: List[str] = []

    for sha, stored_path in rows:
        if limit is not None and total >= limit:
            break
        total += 1
        p = Path(stored_path)
        if not p.exists():
            missing += 1
            continue
        try:
            ingest_file(str(p))
            ok += 1
        except Exception as e:
            errors.append(f"{sha}: {e}")

    return {
        "ok": True,
        "message": "Rebuild terminé",
        "total": total,
        "ingested_ok": ok,
        "missing_files": missing,
        "errors": errors[:20],  # limite affichage
    }
