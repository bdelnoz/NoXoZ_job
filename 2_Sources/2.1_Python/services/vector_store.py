#!/usr/bin/env python3
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/services/vector_store.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Gestion du stockage vectoriel (Chroma) + métadonnées (SQLite) pour NoXoZ_job
# Version: v1.2.0 – Date: 2026-02-08
#
# CHANGELOG (historique complet, ne rien omettre) :
# - v1.2.0 – 2026-02-08 :
#   * FIX: suppression du paramètre invalide `embedding_function` dans `collection.add()` et `collection.query()`
#   * Ajout explicite du calcul des embeddings côté Python via HuggingFaceEmbeddings (LangChain Community)
#   * Utilisation de `embeddings=` pour add() et `query_embeddings=` pour query()
#   * Persist Chroma rendu robuste (compat versions) : client.persist() si disponible, sinon no-op
#   * Commentaires renforcés pour expliquer la logique et éviter les regressions
# - v1.1 – 2026-02-06 :
#   * Version précédente fournie par l’utilisateur (stockage Chroma + SQLite, loaders PDF/DOCX/MD/TXT/JSON/XML)
################################################################################

import sqlite3
from pathlib import Path
from typing import List, Dict

import chromadb

# LangChain embeddings (Community) : API stable pour HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Loaders simples pour extraire du texte (pas d’OCR ici)
from pypdf import PdfReader
import docx


# ==============================================================================
# 1) RESOLUTION DES CHEMINS (compat legacy)
# ==============================================================================
# Objectif :
# - Retrouver le dossier du projet et les emplacements des liens symboliques (chroma_link)
# - Gérer les variations "legacy" (folders renvoyés dans l’historique)
# - Toujours garantir que les dossiers existent
# ==============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "3_Data"

# Dossier Chroma (vector store) : structure récente "3.1_Vectors/chroma_link"
VECTORS_DIR = DATA_DIR / "3.1_Vectors" / "chroma_link"
if not VECTORS_DIR.exists():
    # Compat legacy : "Vectors/chroma_link"
    legacy_vectors_dir = DATA_DIR / "Vectors" / "chroma_link"
    if legacy_vectors_dir.exists():
        VECTORS_DIR = legacy_vectors_dir

# Dossier SQLite metadata : tentative structure "Metadata" puis fallback "3.2_Metadata"
metadata_dir = DATA_DIR / "Metadata"
if not metadata_dir.exists():
    legacy_metadata_dir = DATA_DIR / "3.2_Metadata"
    if legacy_metadata_dir.exists():
        metadata_dir = legacy_metadata_dir

METADATA_DB = metadata_dir / "metadata.db"

# Création défensive (au cas où la structure n’est pas encore en place)
VECTORS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DB.parent.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 2) INIT CHROMA
# ==============================================================================
# NOTE CRITIQUE (bug corrigé) :
# - Dans l’API Chroma "native" (chromadb), `collection.add()` N’accepte PAS `embedding_function=...`
# - Donc : soit on passe un embedding_function AU MOMENT de la création de collection (selon version),
#   soit on calcule les embeddings nous-mêmes et on les passe via `embeddings=...`
#
# Ici : choix robuste et explicite => calcul des embeddings côté Python
# ==============================================================================
def init_chroma():
    # PersistentClient stocke sur disque (via path) et permet de relire les collections existantes
    client = chromadb.PersistentClient(path=str(VECTORS_DIR))

    # Pas d'embedding_function ici pour rester compatible; on calcule embeddings nous-mêmes.
    collection = client.get_or_create_collection("noxoz_documents")
    return client, collection


# ==============================================================================
# 3) INIT SQLITE
# ==============================================================================
# Stockage minimal de métadonnées d’ingestion :
# - id : id unique du chunk
# - filename : fichier d’origine
# - source : chemin (ou autre identifiant)
# - ingestion_date : timestamp UTC
# ==============================================================================
def init_sqlite():
    conn = sqlite3.connect(METADATA_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT,
            source TEXT,
            ingestion_date TEXT
        )
        """
    )
    conn.commit()
    return conn, cursor


# ==============================================================================
# 4) EXTRACTION TEXTE (simple, 1 "document" par fichier)
# ==============================================================================
# Retourne une LISTE[str] pour garder l’interface compatible si on chunk plus tard.
# Actuellement :
# - PDF => concat pages
# - DOCX => concat paragraphs
# - MD/TXT/JSON/XML => read brut
# ==============================================================================
def load_file_text(file_path: str) -> List[str]:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        # Extraction brute : pypdf peut retourner None sur certaines pages
        return ["\n".join([(page.extract_text() or "") for page in reader.pages])]

    if ext == ".docx":
        doc = docx.Document(file_path)
        return ["\n".join([p.text for p in doc.paragraphs])]

    if ext in [".md", ".txt", ".json", ".xml"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]

    raise ValueError(f"Format non supporté: {ext}")


# ==============================================================================
# 5) INGESTION FICHIER
# ==============================================================================
# Pipeline :
# - init chroma + sqlite
# - load texte (liste de chunks)
# - produire ids + metadatas
# - calculer embeddings (HuggingFaceEmbeddings)
# - collection.add(..., embeddings=...)  <-- CORRECTION PRINCIPALE
# - persist chroma si l’API le supporte
# - enregistrer ids en SQLite
# ==============================================================================
def ingest_file(file_path: str):
    client, collection = init_chroma()
    conn, cursor = init_sqlite()

    # 1) Chargement du contenu
    texts = load_file_text(file_path)

    # 2) Identifiants stables : stem + index chunk
    ids = [f"{Path(file_path).stem}_{i}" for i in range(len(texts))]

    # 3) Métadonnées : garder la source (chemin)
    metadatas = [{"source": str(file_path)} for _ in texts]

    # 4) Embeddings : modèle sentence-transformers (embeddings dimension fixe)
    #    NOTE: HuggingFaceEmbeddings expose:
    #    - embed_documents(list[str]) -> list[list[float]]
    #    - embed_query(str) -> list[float]
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 5) CALCUL embeddings côté Python (au lieu de les "donner" à add via embedding_function)
    embeddings = embeddings_model.embed_documents(texts)

    # 6) Ajout à Chroma (API correcte)
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings,
    )

    # 7) Persist (compat versions)
    #    - Certaines versions de chromadb ont client.persist()
    #    - D’autres persistent automatiquement en mode PersistentClient
    if hasattr(client, "persist"):
        try:
            client.persist()
        except Exception:
            # No-op volontaire : on ne casse pas l’ingestion si persist change selon version
            pass

    # 8) Écriture SQLite (métadonnées)
    from datetime import datetime

    now = datetime.utcnow().isoformat()
    for doc_id in ids:
        cursor.execute(
            """
            INSERT OR REPLACE INTO documents (id, filename, source, ingestion_date)
            VALUES (?, ?, ?, ?)
            """,
            (doc_id, Path(file_path).name, str(file_path), now),
        )

    conn.commit()
    conn.close()


# ==============================================================================
# 6) RECHERCHE SIMILAIRE
# ==============================================================================
# Bug corrigé :
# - `collection.query()` N’accepte PAS `embedding_function=...`
# - Il faut passer `query_texts=...` si la collection a un embedding_function interne
#   OU passer `query_embeddings=...` si on calcule nous-mêmes.
#
# Ici : même stratégie que ingestion => calcul embeddings en Python.
# ==============================================================================
def search_similar(query: str, k: int = 5) -> List[Dict]:
    client, collection = init_chroma()

    # Même modèle que l’ingestion pour cohérence du space vectoriel
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Embedding du prompt utilisateur (1 vecteur)
    q_emb = embeddings_model.embed_query(query)

    # Requête par embeddings (API correcte)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["metadatas", "documents"],
    )

    # Mise en forme simple
    docs: List[Dict] = []
    # results["documents"] et results["metadatas"] sont des listes de listes (batch)
    for doc_text, meta in zip(results.get("documents", [[]])[0], results.get("metadatas", [[]])[0]):
        docs.append(
            {
                "text": doc_text,
                "source": meta.get("source"),
            }
        )

    return docs
