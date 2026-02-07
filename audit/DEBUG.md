# NoXoZ_job – Debug (audit)

## Problèmes courants
1. **Chroma indisponible** : vérifier le chemin `/mnt/data1_100g/agent_llm_local/vectors` et les permissions.
2. **Ollama non accessible** : tester `curl http://localhost:11434/api/tags`.
3. **FastAPI HTTPS** : vérifier `certs/cert.pem` et `certs/key.pem`.
4. **SQLite** : cohérence des fichiers `metadata.db` vs `noxoz_metadata.db`.

## Logs
- `4_Logs/log.start_fastapi.*.log` (démarrage FastAPI).
- `4_Logs/log.start_ollama.*.log` (Ollama).

## Monitoring
- `GET /api/monitor/full` : état global.
- `GET /api/monitor/web_status` : page HTML.
