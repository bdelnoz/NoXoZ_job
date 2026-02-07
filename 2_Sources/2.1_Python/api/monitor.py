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
