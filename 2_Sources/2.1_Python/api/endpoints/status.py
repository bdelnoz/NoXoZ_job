# api/endpoints/status.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_status():
    """Statut en temps réel des composants"""
    # TODO : récupérer statut Ollama, Chroma, API
    status = {
        "api": "online",
        "llm": "running",
        "chroma": "available"
    }
    return status
