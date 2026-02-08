# PATH: 2_Sources/2.1_Python/api/monitor.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v2.0.1 - Date: 2026-02-08
# Target usage: Monitoring complet des composants NoXoZ_job (FastAPI, Chroma, SQLite, Ollama)

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import chromadb
import sqlite3
import os
import subprocess
from pathlib import Path

from services.vector_store import METADATA_DB, VECTORS_DIR, DEFAULT_COLLECTION

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_DIR = str(VECTORS_DIR)
SQLITE_DB = str(METADATA_DB)
LOG_DIR = str(PROJECT_ROOT / "4_Logs")
LAST_PROMPT_FILE = str(PROJECT_ROOT / "7_Infos" / "PERMANENT_MEMORY.md")


def check_chroma():
    try:
        if not os.path.exists(CHROMA_DIR):
            return {"status": "error", "error": f"Chroma directory not found: {CHROMA_DIR}"}

        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        collections = chroma_client.list_collections()
        names = [c.name for c in collections]

        count_default = None
        if DEFAULT_COLLECTION in names:
            col = chroma_client.get_collection(DEFAULT_COLLECTION)
            try:
                count_default = col.count()
            except Exception:
                count_default = "N/A"

        return {
            "status": "ok",
            "collections": names,
            "collections_count": len(names),
            "default_collection": DEFAULT_COLLECTION,
            "default_count": count_default,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_sqlite():
    try:
        if not os.path.exists(SQLITE_DB):
            return {"status": "error", "error": f"Database file not found: {SQLITE_DB}"}

        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

        counts = {}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                counts[table] = cursor.fetchone()[0]
            except Exception:
                counts[table] = "N/A"

        conn.close()

        return {"status": "ok", "database": SQLITE_DB, "tables": tables, "counts": counts}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_ollama():
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=3,
        )

        if result.returncode != 0:
            return {"status": "error", "error": "Ollama service not responding"}

        import json
        try:
            data = json.loads(result.stdout or "{}")
            models = [m.get("name", "unknown") for m in data.get("models", [])]
            return {"status": "ok", "endpoint": "http://localhost:11434", "models": models, "models_count": len(models)}
        except json.JSONDecodeError:
            return {"status": "ok", "endpoint": "http://localhost:11434", "note": "Service running but response not JSON"}

    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Ollama ping timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_recent_logs():
    try:
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

        logs = {}
        log_files = sorted(Path(LOG_DIR).glob("*.log"), key=os.path.getmtime, reverse=True)

        for lf in log_files[:5]:
            try:
                with open(lf, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
                logs[lf.name] = lines[-10:] if len(lines) >= 10 else lines
            except Exception as e:
                logs[lf.name] = [f"Error reading: {e}"]

        total = len(list(Path(LOG_DIR).glob("*.log")))
        return {"status": "ok", "logs": logs, "total_log_files": total}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_last_prompt():
    try:
        p = Path(LAST_PROMPT_FILE)
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text("", encoding="utf-8")

        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        last_lines = lines[-20:] if len(lines) >= 20 else lines
        return {"status": "ok", "last_lines": last_lines, "total_lines": len(lines)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.get("/full")
async def full_monitor():
    response = {
        "fastapi": {"status": "ok"},
        "chroma": check_chroma(),
        "sqlite": check_sqlite(),
        "ollama": check_ollama(),
        "logs": get_recent_logs(),
        "last_prompt": get_last_prompt(),
    }
    return JSONResponse(content=response)


@router.get("/status")
async def status_monitor():
    return JSONResponse({"status": "ok", "endpoint": "monitor"})


@router.get("/health")
async def health_monitor():
    return JSONResponse({"status": "ok", "endpoint": "monitor"})
