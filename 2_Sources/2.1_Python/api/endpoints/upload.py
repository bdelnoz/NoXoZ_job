# api/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File
from services.ingestion import parse_and_store_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload et ingestion d'un fichier (CV, DOCX, PDF, MD)"""
    result = await parse_and_store_file(file)
    return {"status": "success", "filename": file.filename, "result": result}
