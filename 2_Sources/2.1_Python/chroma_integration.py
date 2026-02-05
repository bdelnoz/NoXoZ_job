#!/usr/bin/env python3
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/chroma_integration.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Intégration et gestion de Chroma Vector Store pour NoXoZ_job
# Version: v1.0 – Date: 2026-02-06
# Changelog:
#   v1.0 – 2026-02-06 – Implémentation initiale de Chroma pour ingestion, stockage et recherche vectorielle

"""
Chroma Integration Module – NoXoZ_job

Ce module permet :
- Initialisation d’un Chroma Vector Store persistant (avec SQLite pour métadonnées)
- Ingestion de documents (PDF, DOCX, MD, JSON, TXT)
- Génération et stockage d’embeddings via OpenAIEmbeddings / modèles locaux
- Recherche vectorielle et récupération de documents similaires
"""

import os
from pathlib import Path
from typing import List, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import (
    PyPDFLoader,
    DocxLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document

# =========================
# CONFIGURATION DES PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /2_Sources
DATA_DIR = BASE_DIR / "3_Data"
VECTORS_DIR = DATA_DIR / "3.1_Vectors" / "chroma_link"
METADATA_DIR = DATA_DIR / "3.2_Metadata"
PERSIST_DIR = VECTORS_DIR  # Chroma persistant ici

# Création des dossiers si inexistants
VECTORS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# INITIALISATION DU VECTOR STORE
# =========================
def init_chroma_store(persist_directory: Path = PERSIST_DIR) -> Chroma:
    """
    Initialise ou charge un Chroma Vector Store existant
    """
    print(f"[Chroma] Initialisation du Vector Store dans {persist_directory}")
    embeddings = OpenAIEmbeddings()
    store = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
        collection_name="noxoz_documents"
    )
    return store

# =========================
# FONCTIONS D’INGESTION DE DOCUMENTS
# =========================
def load_document(file_path: str) -> List[Document]:
    """
    Charge un document selon son type et retourne une liste de Documents LangChain
    """
    ext = Path(file_path).suffix.lower()
    print(f"[Chroma] Chargement du fichier {file_path} (extension: {ext})")
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = DocxLoader(file_path)
    elif ext == ".md":
        loader = UnstructuredMarkdownLoader(file_path)
    elif ext in [".txt", ".json", ".xml"]:
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Format non supporté: {ext}")
    return loader.load()

def ingest_documents(file_paths: List[str], store: Chroma) -> None:
    """
    Ingestion de plusieurs fichiers dans le Chroma Vector Store
    """
    for file_path in file_paths:
        try:
            documents = load_document(file_path)
            store.add_documents(documents)
            print(f"[Chroma] {len(documents)} documents ingérés depuis {file_path}")
        except Exception as e:
            print(f"[Chroma] Erreur lors de l’ingestion de {file_path} : {e}")
    store.persist()
    print("[Chroma] Persistance du store terminée.")

# =========================
# FONCTION DE RECHERCHE VECTORIELLE
# =========================
def search_similar(query: str, store: Chroma, k: int = 5) -> List[Document]:
    """
    Recherche vectorielle dans le store Chroma
    """
    print(f"[Chroma] Recherche de {k} documents similaires pour la requête : {query}")
    results = store.similarity_search(query, k=k)
    print(f"[Chroma] {len(results)} résultats trouvés")
    return results

# =========================
# EXEMPLE D’UTILISATION
# =========================
if __name__ == "__main__":
    # Initialisation du store
    store = init_chroma_store()

    # Ingestion d’exemples
    example_files = [
        str(BASE_DIR / "2.1_Python" / "examples" / "cv_example.pdf"),
        str(BASE_DIR / "2.1_Python" / "examples" / "doc_example.docx")
    ]
    ingest_documents(example_files, store)

    # Recherche
    query = "Expérience en Python et IA"
    results = search_similar(query, store, k=3)
    for idx, doc in enumerate(results, start=1):
        print(f"Result {idx}: {doc.page_content[:200]}...\n")
