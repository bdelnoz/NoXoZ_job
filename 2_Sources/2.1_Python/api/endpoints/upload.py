from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.ingestion import parse_and_store_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = await parse_and_store_file(file)
        return JSONResponse({"status": "success", "filename": file.filename, "result": result})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
# Endpoint health
@router.get("/health")
async def health_upload():
    return JSONResponse({"status": "ok", "endpoint": "upload"})
