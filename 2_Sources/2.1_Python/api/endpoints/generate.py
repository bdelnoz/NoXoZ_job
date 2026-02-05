from fastapi import APIRouter, Form
from services.generation import generate_document

router = APIRouter()

@router.post("/")
def generate_doc(prompt: str = Form(...), template: str = Form("default")):
    doc_path = generate_document(prompt, template)
    return {"status": "success", "file_path": doc_path}
