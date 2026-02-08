# FILENAME: USAGE.md
# COMPLETE PATH: audit/USAGE.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Lancement du projet
```
bash 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh start
```

## Usage des scripts .sh
- FastAPI service: `bash 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh {start|stop|restart|status|update-pid}`.
- Ollama service: `bash 8_Scripts/8.1_Init/service.ollama/start_ollama.sh {start|stop|restart|status}`.
- Init projet: `bash 8_Scripts/8.1_Init/init_project.sh --exec`.

## Usage des scripts .py
- Tests manuels: `python 2_Sources/2.1_Python/test_sentence_transfomers.py`.
- Test Chroma: `python 2_Sources/2.1_Python/test_db_huffing.py`.

## Usage API
- Upload fichier:
```
curl -k -F "file=@/path/to/file.pdf" https://127.0.0.1:8443/api/upload/
```
- Génération:
```
curl -k -F "prompt=Génère un CV" -F "template=default" https://127.0.0.1:8443/api/generate/
```
- Status:
```
curl -k https://127.0.0.1:8443/api/status/
```
- Monitoring:
```
curl -k https://127.0.0.1:8443/api/monitor/full
```

## Paramètres configurables
- Fichiers de certs: `certs/cert.pem`, `certs/key.pem`.
- Chemins data/outputs: hardcodés dans scripts et services (voir correction_audit.md).

## Erreurs fréquentes
- Erreur TLS: vérifier certs et usage -k avec curl.
- Ollama indisponible: vérifier service et port 11434.
