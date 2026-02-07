peut tu verifier :

# main_agent.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:8443"],  # HTTPS correct
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure le router principal avec préfixe /api
app.include_router(api_router, prefix="/api")

----------------------------

# router.py
from fastapi import APIRouter
from api.endpoints import generate, status, upload, status_web

router = APIRouter()
router.include_router(generate.router, prefix="/generate", tags=["Generate"])
router.include_router(status.router, prefix="/status", tags=["Status"])
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(status_web.router, prefix="/monitor", tags=["Monitor"])


----------------------------

# monitor.py

# PATH: 2_Sources/Python/routers/monitor.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import sqlite3
import os
import subprocess

router = APIRouter()

# --- Configs ---
CHROMA_DIR = "/mnt/data1_100g/agent_llm_local/vectors"
SQLITE_DB = "/mnt/data1_100g/agent_llm_local/metadata.db"
LOG_DIR = "./4_Logs"
LAST_PROMPT_FILE = "./7_Infos/PERMANENT_MEMORY.md"

# Chroma client
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=CHROMA_DIR
))
emb_func = embedding_functions.HuggingFaceEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- Helpers (mêmes que dans full_monitor.py) ---
# check_chroma(), check_sqlite(), check_ollama(), get_recent_logs(), get_last_prompt()
# [Tu peux copier les fonctions directement ici]
# -------------------------------

@router.get("/monitor/full")
async def full_monitor():
    response = {
        "fastapi": {"status": "ok"},
        "chroma": check_chroma(),
        "sqlite": check_sqlite(),
        "ollama": check_ollama(),
        "logs": get_recent_logs(),
        "last_prompt": get_last_prompt()
    }
    return JSONResponse(content=response)




-----------------------------

# dependencies.py
# actuellement vide


-----------------------------

# chroma_integration.py

#!/usr/bin/env python3
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/chroma_integration.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Intégration et gestion de Chroma Vector Store pour NoXoZ_job
# Version: v2.0 – Date: 2026-02-06
# Changelog:
#   v2.0 – 2026-02-06 – Migration vers le nouveau client PersistentClient de Chroma

"""
ChromaDB Integration – NoXoZ_job (nouvelle API)

Fonctions:
- Initialisation d’un ChromaDB persistant avec PersistentClient
- Ingestion de documents multi-format
- Recherche vectorielle de documents similaires
"""

import os
from pathlib import Path
from typing import List
import chromadb
from chromadb.utils import embedding_functions

# =========================
# CONFIGURATION DES PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "3_Data"
VECTORS_DIR = DATA_DIR / "3.1_Vectors" / "chroma_link"
VECTORS_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# INITIALISATION DU CLIENT CHROMA
# =========================
def init_chroma_client(persist_directory: Path = VECTORS_DIR):
    """
    Initialise le client ChromaDB persistant avec la nouvelle API
    """
    print(f"[Chroma] Initialisation du PersistentClient dans {persist_directory}")
    client = chromadb.PersistentClient(path=str(persist_directory))
    collection = client.get_or_create_collection("noxoz_documents")
    return client, collection

# =========================
# CHARGEMENT DE DOCUMENTS
# =========================
def load_document(file_path: str) -> List[str]:
    """
    Charge le contenu d’un document en texte brut
    """
    from PyPDF2 import PdfReader
    import docx

    ext = Path(file_path).suffix.lower()
    print(f"[Chroma] Chargement du fichier {file_path} (extension: {ext})")

    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return [text]
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return [text]
    elif ext in [".md", ".txt", ".json", ".xml"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]
    else:
        raise ValueError(f"Format non supporté: {ext}")

# =========================
# INGESTION DE DOCUMENTS
# =========================
def ingest_documents(file_paths: List[str], collection):
    """
    Ajoute les documents dans la collection ChromaDB avec embeddings
    """
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key="")  # remplacer par modèle local si besoin

    for idx, file_path in enumerate(file_paths, start=1):
        try:
            texts = load_document(file_path)
            ids = [f"{Path(file_path).stem}_{i}" for i in range(len(texts))]
            metadatas = [{"source": file_path} for _ in texts]
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids,
                embedding_function=embedding_fn
            )
            print(f"[Chroma] Ingesté {len(texts)} documents depuis {file_path}")
        except Exception as e:
            print(f"[Chroma] Erreur ingestion {file_path}: {e}")

    print("[Chroma] Persistance du store terminée")
    collection.client.persist()

# =========================
# RECHERCHE VECTORIELLE
# =========================
def search_similar(query: str, collection, k: int = 5):
    """
    Recherche k documents les plus similaires à la query
    """
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key="")  # remplacer par modèle local
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["metadatas", "documents"],
        embedding_function=embedding_fn
    )
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        print(f"Result {idx} – source: {meta['source']}\n{doc[:200]}...\n")
    return documents

# =========================
# MAIN / EXEMPLE D’UTILISATION
# =========================
if __name__ == "__main__":
    client, collection = init_chroma_client()

    # Exemple d’ingestion
    example_files = [
        str(BASE_DIR / "2.1_Python" / "examples" / "cv_example.pdf"),
        str(BASE_DIR / "2.1_Python" / "examples" / "doc_example.docx")
    ]
    ingest_documents(example_files, collection)

    # Exemple de recherche
    query = "Expérience en Python et IA"
    search_similar(query, collection, k=3)



--------------------------------------

#fastapi_full_monitor.py
