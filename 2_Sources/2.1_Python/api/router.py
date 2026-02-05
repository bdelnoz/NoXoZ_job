# api/router.py
from fastapi import APIRouter
from .endpoints import upload, generate, status

router = APIRouter()
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(generate.router, prefix="/generate", tags=["Génération"])
router.include_router(status.router, prefix="/status", tags=["Statut"])
