#!/usr/bin/env python3
# PATH: api/router.py

from fastapi import APIRouter

from api.endpoints import generate, status, upload, status_web, sqlite_info
from api import monitor

router = APIRouter()

router.include_router(generate.router, prefix="/generate")
router.include_router(upload.router, prefix="/upload")
router.include_router(status.router, prefix="/status")
router.include_router(monitor.router, prefix="/monitor")
router.include_router(status_web.router, prefix="/monitor")  # si ton status_web est sous /api/monitor/...
router.include_router(sqlite_info.router, prefix="/sqlite_info")
