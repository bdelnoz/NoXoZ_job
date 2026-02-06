from fastapi import UploadFile
from pathlib import Path
import shutil
from .vector_store import ingest_file, DATA_DIR

async def parse_and_store_file(file: UploadFile):
    """
    Sauvegarde le fichier uploadé et l'ingère dans Chroma + SQLite
    """
    # Dossier temporaire pour les uploads
    upload_dir = DATA_DIR / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    # Sauvegarde du fichier uploadé
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Ingestion dans Chroma + SQLite
    ingest_file(str(file_path))

    return f"Fichier {file.filename} ingéré avec succès"
