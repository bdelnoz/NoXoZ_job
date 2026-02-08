from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from services.generation import generate_document

router = APIRouter()

@router.post("/")
def generate_doc(prompt: str = Form(...), template: str = Form("default")):
    try:
        doc_path = generate_document(prompt, template)
        return JSONResponse({"status": "success", "file_path": doc_path})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@router.get("/status")
async def status_generate():
    return JSONResponse({"status": "ok", "endpoint": "generate"})

# Endpoint health
@router.get("/health")
async def health_generate():
    return JSONResponse({"status": "ok", "endpoint": "generate"})
