FILENAME: USAGE.md
COMPLETE PATH: ./audit/USAGE.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:44

---

# Usage (Audit View)

## API usage (observed)
All API routes are mounted under `/api` via the FastAPI application.

### Upload documents
- Endpoint: `POST /api/upload/`
- Payload: multipart file upload (`file`)
- Behavior: saves file to `3_Data/uploads/`, then ingests into Chroma + SQLite.

### Generate documents
- Endpoint: `POST /api/generate/`
- Payload: JSON with prompt and optional template (implementation in `generate.py`).
- Behavior: searches similar documents, calls `ollama run`, writes DOCX in `5_Outputs/DOCX`.

### Status
- Endpoint: `GET /api/status/`
- Behavior: returns the number of records in SQLite metadata.

### Monitoring
- Endpoint: `GET /api/monitor/full`
- Endpoint: `GET /api/monitor/web_status`
- Behavior: returns status of FastAPI, Chroma, SQLite, Ollama, logs, and last prompt.

## Local UI
- Documentation references a local web interface, but no UI source code is present in this repository.

## Output locations
- Generated DOCX: `5_Outputs/DOCX/`.
- Uploaded files: `3_Data/uploads/` (created on demand).

## UNKNOWN
- Authentication/authorization behavior.
- API schema or OpenAPI documentation beyond default FastAPI output.

## Conclusion
STATUS: SUCCESS
