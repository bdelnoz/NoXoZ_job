from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:8443"],  # HTTPS correct
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure le router principal avec préfixe /api
app.include_router(api_router, prefix="/api")
