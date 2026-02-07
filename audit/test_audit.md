# Test Audit – NoXoZ_job

## Résumé
- Les tests unitaires Python échouent localement faute de dépendances installées.
- Le test SQLite échoue car la base `noxoz_metadata.db` n’existe pas dans cet environnement.
- Le test global FastAPI a été exécuté en **mode simulation** (prévu pour un environnement avec pipenv + services actifs).

## Détail des commandes exécutées

### 1) Test SentenceTransformers
**Commande**
```bash
python 2_Sources/2.1_Python/test_sentence_transfomers.py
```
**Résultat**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

### 2) Test ChromaDB + embeddings (huffing)
**Commande**
```bash
python 2_Sources/2.1_Python/test_db_huffing.py
```
**Résultat**
```
ModuleNotFoundError: No module named 'chromadb'
```

### 3) Test SQLite
**Commande**
```bash
bash 8_Scripts/8.1_Init/test_sqlite.sh --exec
```
**Résultat**
```
[TestSQLite] ERREUR : DB non trouvée à /workspace/3_Data/Metadata/noxoz_metadata.db
```

### 4) Test global FastAPI (simulation)
**Commande**
```bash
bash 8_Scripts/8.1_Init/test_fastapi.sh --simulate
```
**Résultat**
```
[SIMULATE] Actions prévues :
  - cd /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job
  - activation pipenv
  - export PYTHONPATH=2_Sources/2.1_Python
  - lancement FastAPI (uvicorn)
  - tests endpoints: /status /generate /upload
  - logs dans /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/4_Logs
```

## Recommandations
- Installer les dépendances (`pipenv install` ou `pip install -r requirements.txt`).
- Vérifier la présence de la base SQLite et des symlinks sous `3_Data/`.
- Lancer Ollama et Chroma avant les tests d’intégration.
