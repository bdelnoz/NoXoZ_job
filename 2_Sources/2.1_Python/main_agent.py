# main_agent.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

# CORS pour localhost uniquement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:11111"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajout des routes
app.include_router(api_router)

# Lancement : uvicorn main_agent:app --reload --port 11111
