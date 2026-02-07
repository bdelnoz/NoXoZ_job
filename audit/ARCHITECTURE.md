# NoXoZ_job – Architecture (audit)

## Vue d’ensemble
Le projet est un **pipeline local** d’ingestion et de génération :
1. **Upload** de fichiers via FastAPI.
2. **Ingestion** : extraction de texte + embeddings + stockage (Chroma + SQLite).
3. **Recherche sémantique** : requête de documents similaires.
4. **Génération** : prompt enrichi + Ollama -> DOCX.

## Schéma logique
```
Client (Web/CLI)
  -> FastAPI (/api/...)
      -> services/ingestion.py -> vector_store.py (Chroma + SQLite)
      -> services/generation.py -> Ollama (ollama run ...)
```

## Modules principaux
- `main_agent.py` : création de l’app FastAPI et montage des routes.
- `api/router.py` : routeur principal.
- `api/endpoints/*` : endpoints HTTP.
- `services/vector_store.py` : ingestion + recherche + SQLite.
- `services/ingestion.py` : upload + appel ingestion.
- `services/generation.py` : génération DOCX via Ollama.

## Données et stockage
- **Chroma** : `/mnt/data1_100g/agent_llm_local/vectors` (symlink dans `3_Data/3.1_Vectors/`).
- **SQLite** : `3_Data/Metadata/metadata.db` (attention à la cohérence avec `noxoz_metadata.db`).
- **Models** : `/mnt/data1_100g/agent_llm_local/models`.

## Monitoring
- `api/monitor.py` : endpoint `/api/monitor/full` pour état global (Chroma/SQLite/Ollama/logs).
- `api/endpoints/status_web.py` : page HTML de status + lecture fichier.

## Déploiement
- **Docker Compose** : services `ollama` et `chromadb`.
- **systemd** : scripts d’installation service FastAPI + Ollama.

## Dépendances majeures
- FastAPI / Uvicorn, ChromaDB, SQLite, SentenceTransformers, LangChain, Ollama.
