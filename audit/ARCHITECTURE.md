FILENAME: ARCHITECTURE.md
COMPLETE PATH: ./audit/ARCHITECTURE.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:21

---

# Architecture (Audit View)

## High-level overview
The project implements a local document ingestion and generation pipeline with a FastAPI backend, a vector store (ChromaDB), a SQLite metadata store, and an external local LLM runtime (Ollama). It is designed to run fully offline with local storage paths specified in `.env` and in documentation.

## Components and responsibilities
- **FastAPI API server** (`2_Sources/2.1_Python/main_agent.py`)
  - Sets up CORS and mounts the main API router at `/api`.
- **API router and endpoints** (`2_Sources/2.1_Python/api/`)
  - `/generate`: document generation from a prompt using vector search and Ollama.
  - `/upload`: file upload + ingestion to Chroma + SQLite.
  - `/status`: status for database contents.
  - `/monitor`: monitoring endpoints for API, Chroma, SQLite, Ollama, logs.
- **Vector store** (`2_Sources/2.1_Python/services/vector_store.py`)
  - Persistent Chroma store + SQLite metadata.
  - Uses HuggingFace sentence-transformer embeddings.
- **Document ingestion** (`2_Sources/2.1_Python/services/ingestion.py`)
  - Saves uploads, parses documents, and ingests into Chroma + SQLite.
- **Document generation** (`2_Sources/2.1_Python/services/generation.py`)
  - Queries similar documents, calls `ollama run` for LLM output, writes DOCX.
- **External services**
  - Ollama: local LLM runtime.
  - Chroma: vector DB (containerized in `docker-compose.yml`).

## Data flow (observed)
1. User uploads documents (FastAPI `/api/upload/`).
2. Files are parsed and ingested into Chroma with embeddings; metadata stored in SQLite.
3. User submits a prompt (FastAPI `/api/generate/`).
4. Similar documents retrieved from Chroma, context compiled.
5. Ollama generates output text; output stored in `5_Outputs/DOCX`.

## Deployment view
- `docker-compose.yml` contains only Ollama and Chroma containers.
- FastAPI application must be started separately (not defined in Compose).
- Local filesystem paths for models and vectors are hard-coded in `.env` and documentation.

## Unknowns / gaps
- No explicit UI code found in this repository for the local web interface described in documentation.
- CI/CD configuration is referenced but not present.
- Production hardening (auth, RBAC, secrets management) is not implemented in the code base.

## Conclusion
STATUS: SUCCESS
