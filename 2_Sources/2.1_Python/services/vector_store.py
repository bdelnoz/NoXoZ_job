#!/usr/bin/env python3
# PATH: services/vector_store.py
# Auteur: Bruno DELNOZ
# Target usage: Gestion du stockage vectoriel et métadonnées pour NoXoZ_job
# Version: v1.1 – Date: 2026-02-06

import sqlite3
from pathlib import Path
from typing import List, Dict
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import docx

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "3_Data"
VECTORS_DIR = DATA_DIR / "3.1_Vectors" / "chroma_link"
METADATA_DB = DATA_DIR / "3.2_Metadata" / "metadata.db"
VECTORS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DB.parent.mkdir(parents=True, exist_ok=True)

def init_chroma():
    client = chromadb.PersistentClient(path=str(VECTORS_DIR))
    collection = client.get_or_create_collection("noxoz_documents")
    return client, collection

def init_sqlite():
    conn = sqlite3.connect(METADATA_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT,
            source TEXT,
            ingestion_date TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def load_file_text(file_path: str) -> List[str]:
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

def ingest_file(file_path: str):
    client, collection = init_chroma()
    conn, cursor = init_sqlite()

    texts = load_file_text(file_path)
    ids = [f"{Path(file_path).stem}_{i}" for i in range(len(texts))]
    metadatas = [{"source": str(file_path)} for _ in texts]

    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embedding_function=embeddings_model.embed_documents
    )
    collection.client.persist()

    from datetime import datetime
    now = datetime.utcnow().isoformat()
    for doc_id in ids:
        cursor.execute("""
            INSERT OR REPLACE INTO documents (id, filename, source, ingestion_date)
            VALUES (?, ?, ?, ?)
        """, (doc_id, Path(file_path).name, str(file_path), now))
    conn.commit()
    conn.close()

def search_similar(query: str, k: int = 5) -> List[Dict]:
    client, collection = init_chroma()
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["metadatas", "documents"],
        embedding_function=embeddings_model.embed_query
    )

    docs = []
    for doc_text, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append({"text": doc_text, "source": meta["source"]})
    return docs
