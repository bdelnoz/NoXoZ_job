#!/usr/bin/env python3
# PATH: services/ingestion.py
# Auteur: Bruno DELNOZ
# Version: v2.0.1 – Date: 2026-02-08
# Target usage: Ingestion fichiers uploadés et fichiers serveur (path relatif)
#
# Fix v2.0.1:
# - Compatible avec vector_store.ingest_file(file_path, reingest=False, bump_version=False)
# - Ajout ensure_sqlite_schema() avant ingestion (évite schéma legacy)
# - parse_and_store_local_file sécurisé + async cohérent

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import shutil

from fastapi import UploadFile

from services.vector_store import ingest_file, sha256_file, ensure_sqlite_schema

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_ROOT = PROJECT_ROOT / "3_Data" / "uploads"
TMP_DIR = UPLOAD_ROOT / "tmp"
BY_SHA = UPLOAD_ROOT / "by_sha256"
BY_NAME = UPLOAD_ROOT / "by_name"


def _ensure_dirs():
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    BY_SHA.mkdir(parents=True, exist_ok=True)
    BY_NAME.mkdir(parents=True, exist_ok=True)


async def parse_and_store_file(file: UploadFile) -> dict:
    """
    - écrit en tmp
    - calcule sha256 (file_id)
    - move vers by_sha256/<2chars>/<sha256>.<ext>
    - copie vers by_name/<stem>/<timestamp>__<sha12>.<ext>
    - lance ingest_file() (idempotent via file_id côté vector_store)
    """
    _ensure_dirs()
    ensure_sqlite_schema()

    steps = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    original_name = file.filename or "uploaded_file"
    ext = Path(original_name).suffix.lower()

    steps.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Upload reçu, préparation du répertoire",
        "status": "ok",
    })

    # 1) tmp write (ok pour fichiers raisonnables; si énorme -> streaming)
    tmp_path = TMP_DIR / f"{ts}__{original_name}"
    content = await file.read()
    tmp_path.write_bytes(content)

    steps.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": f"Écriture du fichier sur disque: {tmp_path}",
        "status": "ok",
    })

    # 2) hash
    file_id = sha256_file(str(tmp_path))

    # 3) target paths
    sha_sub = file_id[:2]
    target_sha_dir = BY_SHA / sha_sub
    target_sha_dir.mkdir(parents=True, exist_ok=True)
    target_sha_path = target_sha_dir / f"{file_id}{ext}"

    stem = Path(original_name).stem
    target_name_dir = BY_NAME / stem
    target_name_dir.mkdir(parents=True, exist_ok=True)
    target_name_path = target_name_dir / f"{ts}__{file_id[:12]}{ext}"

    # 4) dedup disk + store
    if target_sha_path.exists():
        tmp_path.unlink(missing_ok=True)
        stored_path = target_sha_path
        steps.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Dédup disque: contenu déjà présent => {stored_path}",
            "status": "ok",
        })
    else:
        shutil.move(str(tmp_path), str(target_sha_path))
        stored_path = target_sha_path
        steps.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Move vers stockage content-addressed: {stored_path}",
            "status": "ok",
        })

    # copie lisible (historique)
    if not target_name_path.exists():
        try:
            shutil.copy2(str(stored_path), str(target_name_path))
        except Exception:
            pass  # pas bloquant

    # 5) ingestion
    steps.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Début ingestion Chroma + SQLite",
        "status": "ok",
    })

    # IMPORTANT: compatible avec TON vector_store.py (pas de original_name=)
    res = ingest_file(str(stored_path), reingest=False, bump_version=False)

    steps.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Ingestion terminée",
        "status": "ok",
    })

    return {
        "status": "success" if res.get("status") == "ok" else res.get("status", "unknown"),
        "message": (
            f"Fichier {original_name} ingéré avec succès"
            if res.get("status") != "already_ingested"
            else f"Fichier {original_name} déjà ingéré (skip)"
        ),
        "file_path": str(stored_path),
        "file_id": res.get("file_id", file_id),
        "ingestion": res,
        "steps": steps,
    }


async def parse_and_store_local_file(relative_path: str) -> dict:
    """
    Ingestion d'un fichier déjà présent sur le serveur.
    Sécurisé: interdit absolu + '..'
    """
    ensure_sqlite_schema()

    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Chemin relatif invalide (interdit: absolu ou '..').")

    abs_path = (PROJECT_ROOT / rel).resolve()

    if not abs_path.exists() or not abs_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable: {abs_path}")

    res = ingest_file(str(abs_path), reingest=False, bump_version=False)

    return {
        "status": "success" if res.get("status") == "ok" else res.get("status", "unknown"),
        "message": f"Fichier serveur ingéré: {abs_path.name}",
        "file_path": str(abs_path),
        "file_id": res.get("file_id"),
        "ingestion": res,
        "steps": [{
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "Ingestion server-file terminée",
            "status": "ok",
        }],
    }
