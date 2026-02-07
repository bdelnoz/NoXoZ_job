# NoXoZ_job – Testing (audit)

## Tests unitaires disponibles
- `2_Sources/2.1_Python/test_sentence_transfomers.py`
- `2_Sources/2.1_Python/test_db_huffing.py`

## Tests d’intégration
- `8_Scripts/8.1_Init/test_fastapi.sh` (démarre FastAPI, teste /status, /generate, /upload).
- `8_Scripts/8.1_Init/test_sqlite.sh` (tests SQLite + perf).

## Commandes type
```bash
python 2_Sources/2.1_Python/test_sentence_transfomers.py
python 2_Sources/2.1_Python/test_db_huffing.py

bash 8_Scripts/8.1_Init/test_fastapi.sh --exec
bash 8_Scripts/8.1_Init/test_sqlite.sh --exec
```
