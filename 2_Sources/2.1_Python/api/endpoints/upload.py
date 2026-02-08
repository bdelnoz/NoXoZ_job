from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.ingestion import parse_and_store_file

router = APIRouter()
UPLOAD_LOGS = []
MAX_LOGS = 200

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    log_entry = {
        "id": len(UPLOAD_LOGS) + 1,
        "filename": file.filename,
        "status": "pending",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "steps": [],
    }
    try:
        result = await parse_and_store_file(file)
        log_entry["status"] = "success"
        log_entry["steps"] = result.get("steps", [])
        log_entry["result"] = result.get("message")
        log_entry["file_path"] = result.get("file_path")
        log_entry["finished_at"] = datetime.now(timezone.utc).isoformat()
        UPLOAD_LOGS.append(log_entry)
        if len(UPLOAD_LOGS) > MAX_LOGS:
            UPLOAD_LOGS.pop(0)
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
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
        UPLOAD_LOGS.append(log_entry)
        if len(UPLOAD_LOGS) > MAX_LOGS:
            UPLOAD_LOGS.pop(0)
        return JSONResponse({
            "status": "error",
            "message": str(e),
            "steps": log_entry["steps"],
            "log_id": log_entry["id"],
        }, status_code=500)

@router.get("/status")
async def status_upload():
    return JSONResponse({"status": "ok", "endpoint": "upload"})

# Logs des uploads
@router.get("/logs")
async def upload_logs(limit: int = 50):
    limit = max(1, min(limit, MAX_LOGS))
    return JSONResponse({"status": "ok", "logs": UPLOAD_LOGS[-limit:]})

# Endpoint health
@router.get("/health")
async def health_upload():
    return JSONResponse({"status": "ok", "endpoint": "upload"})
