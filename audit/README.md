FILENAME: README.md
COMPLETE PATH: ./audit/README.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:08

---

# NoXoZ_job — Audit README

## Purpose
NoXoZ_job is a local, offline-focused LLM agent designed to ingest personal documents, perform analysis, and generate professional documents (DOCX/MD/PDF) via a FastAPI backend and local LLM tooling. The repository includes source code, documentation, data directories, logs, templates, and scripts.

## Repository layout (actual)
- `1_Documentation/`: General and technical documentation (Markdown, DOCX, CSV).
- `2_Sources/`: Python and Bash sources.
- `3_Data/`: Data directories for vectors and metadata (with symlink-like folders).
- `4_Logs/`, `5_Outputs/`, `6_Results/`, `7_Infos/`: Runtime outputs, logs, and information files.
- `8_Scripts/`, `9_Templates/`, `10_Runs/`: Utility scripts, templates, run artifacts.
- `certs/`: TLS certificate and key files.

## Core runtime components (observed)
- FastAPI application entrypoint: `2_Sources/2.1_Python/main_agent.py`.
- API routing: `2_Sources/2.1_Python/api/router.py`.
- Services: ingestion, vector store (Chroma + SQLite), document generation (Ollama + DOCX).
- Docker Compose: `docker-compose.yml` (Ollama + Chroma only).

## External dependencies (high level)
- FastAPI + Uvicorn
- ChromaDB
- LangChain + sentence-transformers
- Ollama runtime (external service)

## Notes
- CI workflows are referenced in documentation but not present in the repository.
- Documentation contains paths and structure that differ from the current repository layout.

## License
- No LICENSE file present in the repository.

## Conclusion
STATUS: SUCCESS
