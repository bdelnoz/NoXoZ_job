from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sqlite3
from datetime import datetime
from services.vector_store import METADATA_DB

router = APIRouter()

@router.get("/")
def status():
    try:
        conn = sqlite3.connect(METADATA_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        count = cursor.fetchone()[0]
        conn.close()
        return JSONResponse({
            "status": "success",
            "documents_ingested": count,
            "last_checked": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
# Endpoint health
@router.get("/health")
async def health_status():
    return JSONResponse({"status": "ok", "endpoint": "status"})
