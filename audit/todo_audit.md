# TODO – Audit NoXoZ_job

## Court terme
- [ ] Aligner la base SQLite (`metadata.db` vs `noxoz_metadata.db`).
- [ ] Supprimer/archiver `status.ORI.py` et `fastapi_full_monitor.py` si non utilisés.
- [ ] Nettoyer `temp.py` et `check_all_web_python.sh`.
- [ ] Ajouter les PID/logs manquants dans `.gitignore`.
- [ ] Uniformiser les chemins via `.env` (remplacer les chemins hardcodés).

## Moyen terme
- [ ] Normaliser les embeddings (local uniquement) et retirer `OpenAIEmbeddingFunction`.
- [ ] Isoler les tests (logs, ports dédiés).
- [ ] Ajouter un vrai framework de tests (pytest) + mocks Ollama/Chroma.

## Long terme
- [ ] Ajouter une UI frontend dédiée (actuellement uniquement HTML minimal dans `status_web.py`).
- [ ] Mettre en place CI (lint + tests) avec GitHub Actions.
