FILENAME: INSTALL.md
COMPLETE PATH: ./audit/INSTALL.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:37

---

# Installation (Audit View)

## Prerequisites (observed or implied)
- Python 3.10+ (repository includes `Pipfile` with Python 3.13 requirement).
- Local filesystem paths for models and vectors (see `.env`).
- Ollama installed locally or running via Docker.
- ChromaDB running (Docker Compose provides a container for Chroma).

## Installation steps (documented and inferred)
1. Create or update `.env` to match local storage paths.
2. Install Python dependencies:
   - Option A: `pip install -r requirements.txt`
   - Option B: `pipenv install` (uses `Pipfile`)
3. Start external services:
   - `docker-compose up -d` (starts Ollama + Chroma containers only)
4. Start FastAPI application (manual):
   - `uvicorn main_agent:app --app-dir 2_Sources/2.1_Python --host 0.0.0.0 --port <PORT>`

## Known gaps / UNKNOWN
- The repository does not provide a single, validated installation script.
- The FastAPI service is not defined in `docker-compose.yml`.
- The required LLM models (Ollama) are not downloaded by any script in this repository.
- UI installation instructions are not present.

## Conclusion
STATUS: SUCCESS
