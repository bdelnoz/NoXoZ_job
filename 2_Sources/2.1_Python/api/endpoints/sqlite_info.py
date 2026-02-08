from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import sqlite3
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from services.vector_store import METADATA_DB, UPLOADS_DIR, ensure_sqlite_schema

router = APIRouter()


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="SQL query (SELECT/PRAGMA only)")
    limit: int = Field(200, ge=1, le=1000)


@dataclass
class SqliteQueryResult:
    columns: list[str]
    rows: list[list[Any]]
    row_count: int


def _sanitize_query(raw_query: str) -> str:
    query = raw_query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query vide.")

    trimmed = query.rstrip(";")
    if ";" in trimmed:
        raise HTTPException(status_code=400, detail="Une seule requête SELECT/PRAGMA est autorisée.")

    lower = trimmed.lstrip().lower()
    if not (lower.startswith("select") or lower.startswith("pragma")):
        raise HTTPException(status_code=400, detail="Seules les requêtes SELECT/PRAGMA sont autorisées.")

    return trimmed


def _run_query(query: str, limit: int) -> SqliteQueryResult:
    ensure_sqlite_schema()
    conn = sqlite3.connect(METADATA_DB)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in (cursor.description or [])]
        rows = cursor.fetchmany(limit)
        return SqliteQueryResult(columns=columns, rows=[list(row) for row in rows], row_count=len(rows))
    finally:
        conn.close()


def _safe_table_count(cursor: sqlite3.Cursor, table: str) -> int | None:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        return int(cursor.fetchone()[0])
    except sqlite3.Error:
        return None


@router.get("/tables")
async def list_tables() -> JSONResponse:
    ensure_sqlite_schema()
    conn = sqlite3.connect(METADATA_DB)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]
        payload = []
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default": col[4],
                    "pk": bool(col[5]),
                }
                for col in cursor.fetchall()
            ]
            payload.append({
                "name": table,
                "columns": columns,
                "row_count": _safe_table_count(cursor, table),
            })

        return JSONResponse({
            "status": "ok",
            "db_path": str(METADATA_DB),
            "tables": payload,
        })
    finally:
        conn.close()


@router.post("/query")
async def execute_query(payload: QueryRequest) -> JSONResponse:
    sanitized = _sanitize_query(payload.query)
    result = _run_query(sanitized, payload.limit)
    return JSONResponse({
        "status": "ok",
        "query": sanitized,
        "columns": result.columns,
        "rows": result.rows,
        "row_count": result.row_count,
        "limit": payload.limit,
    })


def _fetch_table_rows(table: str, limit: int) -> SqliteQueryResult:
    query = f"SELECT * FROM {table} ORDER BY rowid DESC"
    return _run_query(query, limit)


@router.get("/files")
async def list_files(limit: int = 200) -> JSONResponse:
    ensure_sqlite_schema()
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="Limit doit être entre 1 et 1000.")
    try:
        result = _fetch_table_rows("files", limit)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=404, detail=f"Table files introuvable: {exc}") from exc
    return JSONResponse({
        "status": "ok",
        "table": "files",
        "columns": result.columns,
        "rows": result.rows,
        "row_count": result.row_count,
        "limit": limit,
    })


@router.get("/documents")
async def list_documents(limit: int = 200) -> JSONResponse:
    ensure_sqlite_schema()
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="Limit doit être entre 1 et 1000.")
    try:
        result = _fetch_table_rows("documents", limit)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=404, detail=f"Table documents introuvable: {exc}") from exc
    return JSONResponse({
        "status": "ok",
        "table": "documents",
        "columns": result.columns,
        "rows": result.rows,
        "row_count": result.row_count,
        "limit": limit,
    })


@router.get("/uploads")
async def list_uploads() -> JSONResponse:
    items: list[dict[str, Any]] = []
    if UPLOADS_DIR.exists():
        for file_path in sorted(UPLOADS_DIR.rglob("*")):
            if file_path.is_file():
                stat = file_path.stat()
                items.append({
                    "name": file_path.name,
                    "relative_path": str(file_path.relative_to(UPLOADS_DIR)),
                    "size_bytes": stat.st_size,
                    "modified_at": datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z",
                })

    return JSONResponse({
        "status": "ok",
        "uploads_dir": str(UPLOADS_DIR),
        "count": len(items),
        "files": items,
    })
