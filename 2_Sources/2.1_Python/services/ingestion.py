from datetime import datetime, timezone
from pathlib import Path
import shutil
from fastapi import UploadFile
from .vector_store import ingest_file, DATA_DIR, PROJECT_ROOT

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

async def parse_and_store_local_file(relative_path: str):
    """
    Ingestion d'un fichier déjà présent sur le serveur.
    """
    steps = []
    steps.append(_step("Validation du chemin serveur"))
    base_dir = PROJECT_ROOT.resolve()
    target_path = (base_dir / relative_path).resolve()
    try:
        target_path.relative_to(base_dir)
    except ValueError as exc:
        raise ValueError("Chemin serveur non autorisé.") from exc
    if not target_path.exists() or not target_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable: {relative_path}")

    steps.append(_step(f"Fichier trouvé: {target_path}"))
    steps.append(_step("Début ingestion Chroma + SQLite"))
    ingest_file(str(target_path))
    steps.append(_step("Ingestion terminée"))

    return {
        "message": f"Fichier {target_path.name} ingéré avec succès",
        "file_path": str(target_path),
        "steps": steps,
    }
