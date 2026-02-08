#!/usr/bin/env python3
# PATH: api/endpoints/upload.py
# Auteur: Bruno DELNOZ
# Version: v2.0.1 – Date: 2026-02-08
# Target usage: Upload + ingestion + journaux en mémoire (ring buffer)
#
# Fix v2.0.1:
# - IDs de logs stables (NEXT_LOG_ID) même quand on pop(0)
# - steps toujours une liste
# - expose file_id/file_path au top-level en succès
# - logs: copie défensive pour éviter effets de bord

from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from services.ingestion import parse_and_store_file, parse_and_store_local_file

router = APIRouter()

UPLOAD_LOGS: list[dict] = []
MAX_LOGS = 200
NEXT_LOG_ID = 1


class ServerFileRequest(BaseModel):
    relative_path: str


def _push_log(entry: dict):
    """
    Ring buffer simple en mémoire (non persistant).
    """
    UPLOAD_LOGS.append(entry)
    if len(UPLOAD_LOGS) > MAX_LOGS:
        UPLOAD_LOGS.pop(0)


def _new_log_entry(filename: str) -> dict:
    global NEXT_LOG_ID
    entry = {
        "id": NEXT_LOG_ID,
        "filename": filename,
        "status": "pending",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "steps": [],
    }
    NEXT_LOG_ID += 1
    return entry


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    log_entry = _new_log_entry(file.filename or "uploaded_file")

    try:
        result = await parse_and_store_file(file)

        steps = result.get("steps") or []
        if not isinstance(steps, list):
            steps = [steps]

        log_entry["status"] = "success"
        log_entry["steps"] = steps
        log_entry["result"] = result.get("message")
        log_entry["file_path"] = result.get("file_path")
        log_entry["file_id"] = result.get("file_id")
        log_entry["finished_at"] = datetime.now(timezone.utc).isoformat()
        _push_log(dict(log_entry))  # copie défensive

        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "file_id": result.get("file_id"),
            "file_path": result.get("file_path"),
            "result": result,
            "log_id": log_entry["id"],
        })

    except Exception as e:
        log_entry["status"] = "error"
        log_entry["error"] = str(e)
        log_entry["steps"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Erreur upload: {e}",
            "status": "error",
        })
        log_entry["finished_at"] = datetime.now(timezone.utc).isoformat()
        _push_log(dict(log_entry))  # copie défensive

        return JSONResponse({
            "status": "error",
            "message": str(e),
            "steps": log_entry["steps"],
            "log_id": log_entry["id"],
        }, status_code=500)


@router.post("/server-file")
async def upload_server_file(payload: ServerFileRequest):
    log_entry = _new_log_entry(payload.relative_path)

    try:
        result = await parse_and_store_local_file(payload.relative_path)

        steps = result.get("steps") or []
        if not isinstance(steps, list):
            steps = [steps]

        log_entry["status"] = "success"
        log_entry["steps"] = steps
        log_entry["result"] = result.get("message")
        log_entry["file_path"] = result.get("file_path")
        log_entry["file_id"] = result.get("file_id")
        log_entry["finished_at"] = datetime.now(timezone.utc).isoformat()
        _push_log(dict(log_entry))  # copie défensive

        return JSONResponse({
            "status": "success",
            "filename": payload.relative_path,
            "file_id": result.get("file_id"),
            "file_path": result.get("file_path"),
            "result": result,
            "log_id": log_entry["id"],
        })

    except Exception as e:
        log_entry["status"] = "error"
        log_entry["error"] = str(e)
        log_entry["steps"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Erreur upload serveur: {e}",
            "status": "error",
        })
        log_entry["finished_at"] = datetime.now(timezone.utc).isoformat()
        _push_log(dict(log_entry))  # copie défensive

        return JSONResponse({
            "status": "error",
            "message": str(e),
            "steps": log_entry["steps"],
            "log_id": log_entry["id"],
        }, status_code=500)


@router.get("/status")
async def status_upload():
    return JSONResponse({"status": "ok", "endpoint": "upload"})


@router.get("/logs")
async def upload_logs(limit: int = 50):
    limit = max(1, min(limit, MAX_LOGS))
    # copie pour éviter qu’un client voie des refs mutables
    return JSONResponse({"status": "ok", "logs": [dict(x) for x in UPLOAD_LOGS[-limit:]]})


@router.get("/health")
async def health_upload():
    return JSONResponse({"status": "ok", "endpoint": "upload"})
