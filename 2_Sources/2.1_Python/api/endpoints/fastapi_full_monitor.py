# PATH: 2_Sources/Python/fastapi_full_monitor.py
# Auteur: Bruno Delnoz
# Email: bruno.delnoz@protonmail.com
# Version: v1.0 - 2026-02-07
# Target: Full health check monitor pour NoXoZ_job affichable sur interface web
#

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import sqlite3
import os
import subprocess
import json
from pathlib import Path

app = FastAPI()

# -------------------------------
# CONFIG PATHS
# -------------------------------
CHROMA_DIR = "/mnt/data1_100g/agent_llm_local/vectors"
SQLITE_DB = "/mnt/data1_100g/agent_llm_local/metadata.db"
PROJECT_ROOT = Path(__file__).resolve().parents[4]
LOG_DIR = str(PROJECT_ROOT / "4_Logs")
LAST_PROMPT_FILE = str(PROJECT_ROOT / "7_Infos" / "PERMANENT_MEMORY.md")

# -------------------------------
# INIT CHROMA
# -------------------------------
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=CHROMA_DIR
))
emb_func = embedding_functions.HuggingFaceEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------------
# HELPERS
# -------------------------------
def check_chroma():
    try:
        collection = chroma_client.get_or_create_collection(name="health_check_collection")
        test_query = collection.query(
            query_texts=["health check"], n_results=1, embedding_function=emb_func
        )
        return {"status": "ok", "collections_count": len(chroma_client.list_collections()), "test_query": test_query}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def check_sqlite():
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        return {"status": "ok", "tables": tables}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def check_ollama():
    try:
        # Petit ping vers Ollama local
        # À adapter selon ton endpoint local Ollama si disponible
        result = subprocess.run(["./8_Scripts/Init/check_ollama.sh"], capture_output=True, text=True)
        status = "ok" if result.returncode == 0 else "error"
        return {"status": status, "output": result.stdout.strip()}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_recent_logs():
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR, exist_ok=True)
            return {"status": "ok", "logs": {}, "message": f"Log directory created: {LOG_DIR}"}
        logs = {}
        for f in os.listdir(LOG_DIR):
            if f.endswith(".log"):
                path = os.path.join(LOG_DIR, f)
                with open(path, "r") as file:
                    logs[f] = file.readlines()[-10:]  # Dernières 10 lignes
        return {"status": "ok", "logs": logs}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_last_prompt():
    try:
        if not os.path.exists(LAST_PROMPT_FILE):
            os.makedirs(os.path.dirname(LAST_PROMPT_FILE), exist_ok=True)
            with open(LAST_PROMPT_FILE, "w", encoding="utf-8") as f:
                f.write("")
            return {"status": "ok", "last_lines": [], "message": f"Memory file created: {LAST_PROMPT_FILE}"}
        with open(LAST_PROMPT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return {"status": "ok", "last_lines": lines[-10:]}  # Dernières 10 lignes
    except Exception as e:
        return {"status": "error", "error": str(e)}

# -------------------------------
# ENDPOINT MONITOR
# -------------------------------
@app.get("/monitor/full")
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
