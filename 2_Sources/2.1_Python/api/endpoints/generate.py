# api/endpoints/generate.py
from fastapi import APIRouter, Form
from services.generation import generate_document

router = APIRouter()

@router.post("/")
def generate_doc(prompt: str = Form(...), template: str = Form("default")):
    """Génération de document depuis prompt et template"""
    doc_path = generate_document(prompt, template)
    return {"status": "success", "file_path": doc_path}
