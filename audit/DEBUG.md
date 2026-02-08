FILENAME: DEBUG.md
COMPLETE PATH: ./audit/DEBUG.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:58

---

# Debugging Guide (Audit View)

## Common checkpoints
1. Verify `.env` paths exist on the host machine (models, vectors, base directory).
2. Ensure Ollama is running and accessible via CLI (`ollama run ...`).
3. Ensure ChromaDB is running (container or local process).
4. Verify SQLite database exists in `3_Data/Metadata/metadata.db` (created on ingestion).
5. Check output directories (`5_Outputs/DOCX`).

## Logs and monitoring
- Log directory: `4_Logs/` (used by monitoring endpoints).
- Monitoring endpoint: `GET /api/monitor/full` (reports status of components).

## Typical error causes
- Missing dependencies in the Python environment.
- Missing external services (Ollama, Chroma).
- Incompatible absolute paths in `.env`.

## Conclusion
STATUS: SUCCESS
