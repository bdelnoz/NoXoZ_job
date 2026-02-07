from fastapi import APIRouter
from api.endpoints import generate, status, upload, status_web
from api import monitor

router = APIRouter()
router.include_router(generate.router, prefix="/generate", tags=["Generate"])
router.include_router(status.router, prefix="/status", tags=["Status"])
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(status_web.router, prefix="/monitor", tags=["Monitor"])
router.include_router(monitor.router, prefix="/monitor", tags=["MonitorFull"])
