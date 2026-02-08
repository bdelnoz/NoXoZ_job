#!/usr/bin/env python3
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/2_Sources/2.1_Python/services/ingestion.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Deterministic ingestion pipeline for NoXoZ_job:
#              - UploadFile -> canonical disk storage (SHA256-based)
#              - SQLite registry for audit/deduplication
#              - Chroma ingestion via services.vector_store.ingest_file()
#              - Utilities for re-ingestion, purge, and rebuild of Chroma from disk
# Version: v1.1.0 – Date: 2026-02-08
#
# CHANGELOG (full history; do not omit older entries):
# - v1.1.0 – 2026-02-08:
#   * FIX: restore missing export `parse_and_store_local_file` required by api/endpoints/upload.py
#   * Add deterministic disk storage using SHA256 and a stable filename suffix (sha12)
#   * Add SQLite schema management:
#       - new table `files` (sha256 primary key) for canonical file registry
#       - extend table `documents` with extra columns (file_sha256, chunk_index, stored_path, content_sha256)
#   * Dedup logic:
#       - re-upload of same bytes => update last_seen_at and skip ingestion (no Chroma/SQLite duplication)
#   * Add management primitives:
#       - reingest_file_sha(sha256)
#       - purge_file_sha(sha256)  (best-effort for Chroma delete; always cleans SQLite)
#       - rebuild_chroma_from_disk(limit=None)
#   * Add verbose step-by-step tracing payload (timestamps, messages, status) for API responses
# - v1.0.0 – 2026-02-08:
#   * Initial ingestion module skeleton for NoXoZ_job (upload parsing + ingestion hook)
################################################################################

from __future__ import annotations

import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import UploadFile


# ==============================================================================
# IMPORTANT: Imports from vector_store
# ------------------------------------------------------------------------------
# This module must provide two async functions used by FastAPI endpoints:
#   - parse_and_store_file(file: UploadFile) -> dict
#   - parse_and_store_local_file(relative_path: str) -> dict
#
# It also provides management functions for future operations:
#   - reingest_file_sha(sha256: str)
#   - purge_file_sha(sha256: str)
#   - rebuild_chroma_from_disk(limit: Optional[int] = None)
#
# NOTE:
# We ingest into Chroma+SQLite by calling `ingest_file()` from services.vector_store.
# That function currently writes to the `documents` table itself.
# We enrich the schema and provide dedupe/registry without breaking existing behavior.
# ==============================================================================
from services.vector_store import METADATA_DB, ingest_file, VECTORS_DIR  # type: ignore


# ==============================================================================
# 1) DISK STRUCTURE (canonical uploads)
# ------------------------------------------------------------------------------
# Canonical disk storage location (inside project):
#   3_Data/uploads/YYYY/MM/<safe_stem>__<sha12><ext>
#
# Why:
# - Avoid silent overwrite when same original filename is uploaded again.
# - Guarantee traceability and enable rebuild of Chroma from disk.
#
# Example:
#   3_Data/uploads/2026/02/CV-Bruno-DELNOZ-clean__9f3a1c2d4e5f.md
# ==============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "3_Data"
UPLOADS_DIR = DATA_DIR / "uploads"


# ==============================================================================
# 2) SMALL UTILS
# ==============================================================================
def _utc_now_iso() -> str:
    """UTC timestamp in ISO format, always timezone-aware."""
    return datetime.now(timezone.utc).isoformat()


def _sha256_bytes(data: bytes) -> str:
    """SHA256 hex digest for raw bytes."""
    return hashlib.sha256(data).hexdigest()


def _safe_stem(filename: str) -> str:
    """
    Build a filesystem-safe stem:
    - keep [a-zA-Z0-9._-]
    - replace anything else by '_'
    - avoid empty name
    """
    stem = Path(filename).stem
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "_", stem).strip("_")
    return stem or "uploaded_file"


def _build_storage_path(original_filename: str, sha256: str) -> Path:
    """
    Create canonical target path:
      uploads/YYYY/MM/<stem>__<sha12><ext>
    """
    now = datetime.now(timezone.utc)
    y = f"{now.year:04d}"
    m = f"{now.month:02d}"
    ext = Path(original_filename).suffix.lower() or ""
    stem = _safe_stem(original_filename)
    sha12 = sha256[:12]
    target_dir = UPLOADS_DIR / y / m
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{stem}__{sha12}{ext}"


# ==============================================================================
# 3) SQLITE: connection + schema management (migrations)
# ------------------------------------------------------------------------------
# Existing table (from vector_store.py):
#   documents(id TEXT PRIMARY KEY, filename TEXT, source TEXT, ingestion_date TEXT)
#
# We add:
# - `files` registry table:
#     sha256 (PK), original_filename, stored_path, size_bytes, mime_type, created_at, last_seen_at
#
# We also extend documents with additional columns (best-effort, non-breaking):
#   file_sha256, chunk_index, stored_path, content_sha256
#
# Why:
# - Dedup by sha256
# - Audit trail
# - Enable rebuild/purge reliably
# ==============================================================================
def _sqlite_connect() -> sqlite3.Connection:
    METADATA_DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(METADATA_DB))


def _sqlite_table_columns(conn: sqlite3.Connection, table: str) -> List[str]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]


def _sqlite_ensure_schema() -> None:
    conn = _sqlite_connect()
    cur = conn.cursor()

    # --- Canonical file registry table ---
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            sha256 TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            mime_type TEXT,
            created_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL
        )
        """
    )

    # --- Ensure the existing documents table exists (compat) ---
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT,
            source TEXT,
            ingestion_date TEXT
        )
        """
    )

    # --- Extend documents table with extra columns (best effort) ---
    cols = _sqlite_table_columns(conn, "documents")

    if "file_sha256" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN file_sha256 TEXT")
    if "chunk_index" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN chunk_index INTEGER")
    if "stored_path" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN stored_path TEXT")
    if "content_sha256" not in cols:
        cur.execute("ALTER TABLE documents ADD COLUMN content_sha256 TEXT")

    conn.commit()
    conn.close()


def _files_get(conn: sqlite3.Connection, sha256: str) -> Optional[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sha256, original_filename, stored_path, size_bytes, mime_type, created_at, last_seen_at
        FROM files
        WHERE sha256=?
        """,
        (sha256,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "sha256": row[0],
        "original_filename": row[1],
        "stored_path": row[2],
        "size_bytes": row[3],
        "mime_type": row[4],
        "created_at": row[5],
        "last_seen_at": row[6],
    }


def _files_upsert_seen(conn: sqlite3.Connection, sha256: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE files SET last_seen_at=? WHERE sha256=?", (_utc_now_iso(), sha256))


def _files_insert(
    conn: sqlite3.Connection,
    sha256: str,
    original_filename: str,
    stored_path: str,
    size_bytes: int,
    mime_type: Optional[str],
) -> None:
    cur = conn.cursor()
    now = _utc_now_iso()
    cur.execute(
        """
        INSERT INTO files (sha256, original_filename, stored_path, size_bytes, mime_type, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (sha256, original_filename, stored_path, size_bytes, mime_type, now, now),
    )


# ==============================================================================
# 4) API-FACING: parse_and_store_file (UploadFile)
# ------------------------------------------------------------------------------
# Behavior:
# - Read the uploaded bytes once
# - Compute SHA256
# - If known: update last_seen_at and return dedupe=True (skip ingestion)
# - Else: write canonical file to disk and register it, then ingest into Chroma+SQLite
#
# Return payload includes:
# - message, file_path, sha256, dedupe
# - steps[] tracing list (timestamp/message/status)
# ==============================================================================
async def parse_and_store_file(file: UploadFile) -> Dict[str, Any]:
    steps: List[Dict[str, Any]] = []

    def step(msg: str, status: str = "ok") -> None:
        steps.append({"timestamp": _utc_now_iso(), "message": msg, "status": status})

    _sqlite_ensure_schema()

    step("Upload received; reading bytes from UploadFile")
    data = await file.read()

    if not data:
        step("Empty file received", "error")
        return {"message": "Empty file", "steps": steps}

    sha256 = _sha256_bytes(data)
    size_bytes = len(data)
    step(f"SHA256 computed: {sha256}")

    # --- SQLite dedupe check + registry update ---
    conn = _sqlite_connect()
    try:
        existing = _files_get(conn, sha256)
        if existing:
            _files_upsert_seen(conn, sha256)
            conn.commit()
            step("File already known (dedupe): last_seen_at updated")
            step("Ingestion skipped (identical content)")
            return {
                "message": f"File already ingested (dedupe): {file.filename}",
                "file_path": existing["stored_path"],
                "sha256": sha256,
                "dedupe": True,
                "steps": steps,
            }

        # --- New file: write canonical copy to disk ---
        step("Preparing uploads directory")
        stored_path = _build_storage_path(file.filename, sha256)

        step(f"Writing file to disk: {stored_path}")
        stored_path.parent.mkdir(parents=True, exist_ok=True)
        stored_path.write_bytes(data)

        # Register in files table
        _files_insert(
            conn=conn,
            sha256=sha256,
            original_filename=file.filename,
            stored_path=str(stored_path),
            size_bytes=size_bytes,
            mime_type=getattr(file, "content_type", None),
        )
        conn.commit()

    finally:
        conn.close()

    # --- Ingest into Chroma+SQLite (documents) ---
    step("Starting ingestion into Chroma + SQLite")
    ingest_file(str(stored_path))
    step("Ingestion completed")

    # Optional: best-effort enrichment of documents table with file_sha256/stored_path.
    # Because `ingest_file()` currently writes its own rows (id-based) we do not know
    # the ids precisely without re-implementing chunking here.
    # However, for a single-chunk file, the common id pattern is "<stem>_0".
    # We do a *best-effort* update to attach sha/path to matching source/stored_path.
    try:
        conn2 = _sqlite_connect()
        cur2 = conn2.cursor()
        # vector_store currently sets metadatas source = file_path (string)
        # and documents table has column 'source' = file_path (string).
        cur2.execute(
            """
            UPDATE documents
            SET file_sha256=?, stored_path=?
            WHERE source=?
            """,
            (sha256, str(stored_path), str(stored_path)),
        )
        conn2.commit()
        conn2.close()
        step("SQLite enrichment: linked documents rows to file_sha256/stored_path (best-effort)")
    except Exception as e:
        step(f"SQLite enrichment skipped (non-fatal): {e}", "warn")

    return {
        "message": f"File {file.filename} ingested successfully",
        "file_path": str(stored_path),
        "sha256": sha256,
        "dedupe": False,
        "steps": steps,
    }


# ==============================================================================
# 5) API-FACING: parse_and_store_local_file (server-side path)
# ------------------------------------------------------------------------------
# Used by POST /api/upload/server-file with payload {"relative_path": "..."}
#
# Behavior:
# - Resolve path (absolute allowed; relative resolved against PROJECT_ROOT)
# - Read bytes, compute SHA256
# - Dedup: if already known => update last_seen_at, skip ingestion
# - Else: copy into canonical uploads path, register, ingest
# ==============================================================================
async def parse_and_store_local_file(relative_path: str) -> Dict[str, Any]:
    steps: List[Dict[str, Any]] = []

    def step(msg: str, status: str = "ok") -> None:
        steps.append({"timestamp": _utc_now_iso(), "message": msg, "status": status})

    _sqlite_ensure_schema()

    # Resolve local path
    p = Path(relative_path).expanduser()
    if not p.is_absolute():
        p = (PROJECT_ROOT / relative_path).resolve()

    if not p.exists() or not p.is_file():
        step(f"Local file not found: {p}", "error")
        return {"message": f"File not found: {p}", "steps": steps}

    step(f"Reading local file: {p}")
    data = p.read_bytes()
    if not data:
        step("Local file is empty", "error")
        return {"message": "Empty file", "steps": steps}

    sha256 = _sha256_bytes(data)
    step(f"SHA256 computed: {sha256}")

    conn = _sqlite_connect()
    try:
        existing = _files_get(conn, sha256)
        if existing:
            _files_upsert_seen(conn, sha256)
            conn.commit()
            step("File already known (dedupe): last_seen_at updated")
            step("Ingestion skipped (identical content)")
            return {
                "message": f"File already ingested (dedupe): {p.name}",
                "file_path": existing["stored_path"],
                "sha256": sha256,
                "dedupe": True,
                "steps": steps,
            }

        stored_path = _build_storage_path(p.name, sha256)
        step(f"Copying file into uploads: {stored_path}")
        stored_path.parent.mkdir(parents=True, exist_ok=True)
        stored_path.write_bytes(data)

        _files_insert(
            conn=conn,
            sha256=sha256,
            original_filename=p.name,
            stored_path=str(stored_path),
            size_bytes=len(data),
            mime_type=None,
        )
        conn.commit()

    finally:
        conn.close()

    step("Starting ingestion into Chroma + SQLite")
    ingest_file(str(stored_path))
    step("Ingestion completed")

    # Best-effort enrichment of documents table to link sha/path
    try:
        conn2 = _sqlite_connect()
        cur2 = conn2.cursor()
        cur2.execute(
            """
            UPDATE documents
            SET file_sha256=?, stored_path=?
            WHERE source=?
            """,
            (sha256, str(stored_path), str(stored_path)),
        )
        conn2.commit()
        conn2.close()
        step("SQLite enrichment: linked documents rows to file_sha256/stored_path (best-effort)")
    except Exception as e:
        step(f"SQLite enrichment skipped (non-fatal): {e}", "warn")

    return {
        "message": f"Local file {p.name} ingested successfully",
        "file_path": str(stored_path),
        "sha256": sha256,
        "dedupe": False,
        "steps": steps,
    }


# ==============================================================================
# 6) MANAGEMENT: re-ingestion / purge / rebuild
# ------------------------------------------------------------------------------
# These are utilities to support the future lifecycle:
# - Re-ingestion (e.g., embeddings model changes or chunking strategy changes)
# - Purge (remove a file from registry and attempt to delete its vectors)
# - Rebuild (recreate vector store by reading the canonical disk copies)
#
# NOTES:
# - Purge from Chroma is best-effort because Chroma API varies by version.
# - Rebuild assumes your ingest_file() is stable. If ingest_file() uses filename-based IDs,
#   you should patch it to use sha-based IDs to avoid collisions.
# ==============================================================================
def reingest_file_sha(sha256: str) -> Dict[str, Any]:
    _sqlite_ensure_schema()
    conn = _sqlite_connect()
    try:
        f = _files_get(conn, sha256)
        if not f:
            return {"ok": False, "message": f"Unknown sha256: {sha256}"}

        stored_path = Path(f["stored_path"])
        if not stored_path.exists():
            return {"ok": False, "message": f"Missing file on disk: {stored_path}", "sha256": sha256}

        # If you want guaranteed clean re-ingestion, purge first:
        # purge_file_sha(sha256)

        ingest_file(str(stored_path))
        _files_upsert_seen(conn, sha256)
        conn.commit()

        return {"ok": True, "message": f"Re-ingestion done: {stored_path}", "sha256": sha256, "file_path": str(stored_path)}
    finally:
        conn.close()


def purge_file_sha(sha256: str) -> Dict[str, Any]:
    """
    Purge strategy:
    1) SQLite:
       - remove documents rows linked to file_sha256 OR stored_path
       - remove files registry row
    2) Chroma (best-effort):
       - try collection.delete(where={"source": "<stored_path>"})
       - if not supported, recommend rebuild
    """
    _sqlite_ensure_schema()

    # Get stored_path first
    conn = _sqlite_connect()
    f: Optional[Dict[str, Any]] = None
    try:
        f = _files_get(conn, sha256)
        if not f:
            return {"ok": False, "message": f"Unknown sha256: {sha256}"}
        stored_path = f["stored_path"]

        cur = conn.cursor()
        cur.execute("DELETE FROM documents WHERE file_sha256=? OR stored_path=? OR source=?", (sha256, stored_path, stored_path))
        cur.execute("DELETE FROM files WHERE sha256=?", (sha256,))
        conn.commit()
    finally:
        conn.close()

    # Chroma best-effort delete
    try:
        import chromadb  # local import to avoid import-time failures if chromadb changes

        client = chromadb.PersistentClient(path=str(VECTORS_DIR))
        col = client.get_or_create_collection("noxoz_documents")

        # Most chroma versions support delete(where=...)
        col.delete(where={"source": f["stored_path"]})

        if hasattr(client, "persist"):
            try:
                client.persist()
            except Exception:
                pass

        return {
            "ok": True,
            "message": "Purged from SQLite and best-effort deleted from Chroma",
            "sha256": sha256,
            "stored_path": f["stored_path"],
        }
    except Exception as e:
        return {
            "ok": True,
            "message": f"SQLite purge done. Chroma delete not guaranteed; rebuild recommended. Error: {e}",
            "sha256": sha256,
            "stored_path": f["stored_path"] if f else None,
        }


def rebuild_chroma_from_disk(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Rebuild Chroma by re-ingesting files registered in SQLite 'files' table.

    WARNING:
    - This does NOT automatically wipe Chroma before rebuilding.
      If you want a true rebuild, you should delete the Chroma persistence directory
      or create a new collection name, then ingest.
    - If ingest_file() uses filename-based IDs, collisions may happen if stems repeat.
      Best practice: patch ingest_file() to use sha-based IDs.
    """
    _sqlite_ensure_schema()

    conn = _sqlite_connect()
    cur = conn.cursor()
    cur.execute("SELECT sha256, stored_path FROM files ORDER BY created_at ASC")
    rows = cur.fetchall()
    conn.close()

    total = 0
    ingested_ok = 0
    missing_files = 0
    errors: List[str] = []

    for sha, stored_path in rows:
        if limit is not None and total >= limit:
            break
        total += 1

        p = Path(stored_path)
        if not p.exists():
            missing_files += 1
            continue

        try:
            ingest_file(str(p))
            ingested_ok += 1
        except Exception as e:
            errors.append(f"{sha}: {e}")

    return {
        "ok": True,
        "message": "Rebuild completed",
        "total": total,
        "ingested_ok": ingested_ok,
        "missing_files": missing_files,
        "errors": errors[:20],
    }
