FILENAME: preflight.md
COMPLETE PATH: ./audit/preflight.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:24:49

---

# Preflight & Baseline Hygiene

## Repository tree (summary)
- Top-level directories: `1_Documentation/`, `2_Sources/`, `3_Data/`, `4_Logs/`, `5_Outputs/`, `6_Results/`, `7_Infos/`, `8_Scripts/`, `9_Templates/`, `10_Runs/`, `audit/`, `certs/`.
- Top-level files: `README.md`, `Pipfile`, `Pipfile.lock`, `requirements.txt`, `docker-compose.yml`, `.env`, `check_all_web_python.sh`, `temp.py`, `fastapi.pid`.
- Full tree captured in `./audit/tree.txt`.

## Detected languages
- Python (`.py`)
- Shell (`.sh`)
- Markdown (`.md`)
- CSV (`.csv`)
- YAML (`docker-compose.yml`)
- TOML (`Pipfile`)
- DOCX (`.docx`)

## Detected frameworks / platforms (from code and declared dependencies)
- FastAPI (API server)
- Uvicorn (ASGI server)
- LangChain (agent and embeddings helpers)
- ChromaDB (vector store)
- Sentence-Transformers / HuggingFace embeddings
- Ollama (local LLM runtime)
- Docker Compose (deployment)

## README / LICENSE / Tests / CI
- README: present (`README.md`).
- LICENSE: not found.
- Tests: present (`2_Sources/2.1_Python/test_db_huffing.py`, `2_Sources/2.1_Python/test_sentence_transformers.py`).
- CI: no workflow files found in the repository (no `.github/workflows/`).

## Sensitive or security-relevant files (paths only)
- `.env`
- `certs/key.pem`
- `certs/cert.pem`

## Major inconsistencies or anomalies
- Documentation tree in `1_Documentation/1.2_Technical/structure.md` does not match the current repository structure (mentions `.github/`, `src/`, `scripts/`, etc. that are not present).
- `docker-compose.yml` declares only Ollama and Chroma services; the FastAPI service is not defined in the Compose file.
- Absolute paths in `.env` and documentation point to local mounts not present in this repository.

## Conclusion
STATUS: SUCCESS
