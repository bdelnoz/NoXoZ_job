# PATH: 2_Sources/2.1_Python/api/monitor.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v2.0.0 - Date: 2026-02-07
# Target usage: Monitoring complet des composants NoXoZ_job (FastAPI, Chroma, SQLite, Ollama)
# Changelog:
#   v1.0.0 - 2026-02-06: Création initiale avec structure de base
#   v2.0.0 - 2026-02-07: Implémentation complète des fonctions helper

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import sqlite3
import os
import subprocess
from pathlib import Path
from services.vector_store import METADATA_DB, VECTORS_DIR

router = APIRouter()

# =========================
# CONFIGURATION PATHS
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = str(VECTORS_DIR)
SQLITE_DB = str(METADATA_DB)
LOG_DIR = str(PROJECT_ROOT / "4_Logs")
LAST_PROMPT_FILE = str(PROJECT_ROOT / "7_Infos" / "PERMANENT_MEMORY.md")

# =========================
# INITIALISATION CHROMA CLIENT
# =========================
try:
    chroma_client = chromadb.Client(Settings(
        persist_directory=CHROMA_DIR,
        anonymized_telemetry=False
    ))
    emb_func = embedding_functions.HuggingFaceEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    CHROMA_AVAILABLE = True
except Exception as e:
    CHROMA_AVAILABLE = False
    CHROMA_ERROR = str(e)

# =========================
# HELPER FUNCTIONS
# =========================

def check_chroma():
    """
    Vérifie l'état de Chroma Vector Store
    """
    if not CHROMA_AVAILABLE:
        return {
            "status": "error",
            "error": f"Chroma client unavailable: {CHROMA_ERROR}"
        }

    try:
        # Liste des collections
        collections = chroma_client.list_collections()
        collection_names = [col.name for col in collections]

        # Test query sur collection par défaut si existe
        test_result = None
        if "noxoz_documents" in collection_names:
            collection = chroma_client.get_collection("noxoz_documents")
            test_result = collection.count()

        return {
            "status": "ok",
            "collections": collection_names,
            "collections_count": len(collections),
            "noxoz_documents_count": test_result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def check_sqlite():
    """
    Vérifie l'état de la base SQLite
    """
    try:
        if not os.path.exists(SQLITE_DB):
            return {
                "status": "error",
                "error": f"Database file not found: {SQLITE_DB}"
            }

        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()

        # Liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

        # Comptage documents par table
        counts = {}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                counts[table] = cursor.fetchone()[0]
            except Exception:
                counts[table] = "N/A"

        conn.close()

        return {
            "status": "ok",
            "database": SQLITE_DB,
            "tables": tables,
            "counts": counts
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def check_ollama():
    """
    Vérifie l'état du service Ollama
    """
    try:
        # Test ping vers API Ollama
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=3
        )

        if result.returncode == 0:
            import json
            try:
                data = json.loads(result.stdout)
                models = [m.get("name", "unknown") for m in data.get("models", [])]
                return {
                    "status": "ok",
                    "endpoint": "http://localhost:11434",
                    "models": models,
                    "models_count": len(models)
                }
            except json.JSONDecodeError:
                return {
                    "status": "ok",
                    "endpoint": "http://localhost:11434",
                    "note": "Service running but response not JSON"
                }
        else:
            return {
                "status": "error",
                "error": "Ollama service not responding"
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "Ollama ping timeout"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def get_recent_logs():
    """
    Récupère les dernières lignes des fichiers logs
    """
    try:
        if not os.path.exists(LOG_DIR):
            return {
                "status": "warning",
                "message": f"Log directory not found: {LOG_DIR}"
            }

        logs = {}
        log_files = sorted(Path(LOG_DIR).glob("*.log"), key=os.path.getmtime, reverse=True)

        # Prendre les 5 fichiers logs les plus récents
        for log_file in log_files[:5]:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # Dernières 10 lignes
                    logs[log_file.name] = lines[-10:] if len(lines) >= 10 else lines
            except Exception as e:
                logs[log_file.name] = [f"Error reading: {str(e)}"]

        return {
            "status": "ok",
            "logs": logs,
            "total_log_files": len(list(Path(LOG_DIR).glob("*.log")))
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def get_last_prompt():
    """
    Récupère les dernières lignes du fichier PERMANENT_MEMORY
    """
    try:
        if not os.path.exists(LAST_PROMPT_FILE):
            return {
                "status": "warning",
                "message": f"Memory file not found: {LAST_PROMPT_FILE}"
            }

        with open(LAST_PROMPT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Dernières 20 lignes
            last_lines = lines[-20:] if len(lines) >= 20 else lines

        return {
            "status": "ok",
            "last_lines": last_lines,
            "total_lines": len(lines)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =========================
# ENDPOINT PRINCIPAL
# =========================

@router.get("/full")
async def full_monitor():
    """
    Endpoint de monitoring complet de tous les composants
    """
    response = {
        "fastapi": {"status": "ok"},
        "chroma": check_chroma(),
        "sqlite": check_sqlite(),
        "ollama": check_ollama(),
        "logs": get_recent_logs(),
        "last_prompt": get_last_prompt()
    }
    return JSONResponse(content=response)

@router.get("/status")
async def status_monitor():
    """
    Endpoint status check simple
    """
    return JSONResponse({"status": "ok", "endpoint": "monitor"})

@router.get("/health")
async def health_monitor():
    """
    Endpoint health check simple
    """
    return JSONResponse({"status": "ok", "endpoint": "monitor"})
