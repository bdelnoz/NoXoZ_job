# NoXoZ_job – Usage (audit)

## Démarrage FastAPI
```bash
# Via script
8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh start

# Directement via uvicorn
cd 2_Sources/2.1_Python
uvicorn main_agent:app --host 127.0.0.1 --port 8443 --reload \
  --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem
```

## Endpoints API (exemples)
```bash
# Status
curl -k https://127.0.0.1:8443/api/status/

# Upload fichier
curl -k -F "file=@/path/to/doc.pdf" https://127.0.0.1:8443/api/upload/

# Génération
curl -k -F "prompt=Ecris une lettre" https://127.0.0.1:8443/api/generate/

# Monitoring complet
curl -k https://127.0.0.1:8443/api/monitor/full
```

## Utilitaires
```bash
# Compression Markdown via Ollama
python 8_Scripts/8.2_Utils/md_compressor.py --exec --file /path/doc.md

# Comptage tokens
8_Scripts/8.2_Utils/count_tokens.sh --exec /path/doc.txt mistral
```
