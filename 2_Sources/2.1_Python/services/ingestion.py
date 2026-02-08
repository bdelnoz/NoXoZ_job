from datetime import datetime, timezone
import shutil
from fastapi import UploadFile
from .vector_store import ingest_file, DATA_DIR

def _step(message: str, status: str = "ok") -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "status": status,
    }

async def parse_and_store_file(file: UploadFile):
    """
    Sauvegarde le fichier uploadé et l'ingère dans Chroma + SQLite
    """
    steps = []
    steps.append(_step("Upload reçu, préparation du répertoire"))
    # Dossier temporaire pour les uploads
    upload_dir = DATA_DIR / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    # Sauvegarde du fichier uploadé
    steps.append(_step(f"Écriture du fichier sur disque: {file_path}"))
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Ingestion dans Chroma + SQLite
    steps.append(_step("Début ingestion Chroma + SQLite"))
    ingest_file(str(file_path))
    steps.append(_step("Ingestion terminée"))

    return {
        "message": f"Fichier {file.filename} ingéré avec succès",
        "file_path": str(file_path),
        "steps": steps,
    }
