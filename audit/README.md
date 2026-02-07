# NoXoZ_job – README (audit)

## Résumé
NoXoZ_job est un agent LLM local (FastAPI + Chroma + SQLite + Ollama) pour ingérer des documents, stocker des embeddings et générer des documents (DOCX) hors ligne.

## Composants principaux
- **API FastAPI** : point d’entrée HTTP (upload, génération, status, monitoring).
- **Ingestion** : stockage fichiers + embeddings (Chroma) + métadonnées (SQLite).
- **Génération** : récupération de contexte et génération via Ollama.
- **Stockage** : répertoires locaux sous `/mnt/data1_100g/agent_llm_local`.

## Arborescence (haut niveau)
- `1_Documentation/` : documentation générale et technique.
- `2_Sources/` : code Python (API, services), scripts Bash.
- `3_Data/` : liens vers modèles et vecteurs.
- `4_Logs/` : logs d’exécution.
- `5_Outputs/` : sorties générées.
- `8_Scripts/` : init, tests, services, utilitaires.

## Points d’entrée
- `2_Sources/2.1_Python/main_agent.py` (FastAPI app).
- `2_Sources/2.1_Python/api/router.py` (routes).

## Dépendances majeures
- **FastAPI / Uvicorn** (API).
- **ChromaDB** (vector store).
- **SQLite** (métadonnées).
- **LangChain + SentenceTransformers** (embeddings).
- **Ollama** (LLM local).

## Commandes rapides
```bash
# Lancer l’API (via script systemd)
8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh start

# Lancer l’API en local (uvicorn direct)
cd 2_Sources/2.1_Python
uvicorn main_agent:app --host 127.0.0.1 --port 8443 --reload --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem
```

## Voir l’audit complet
Consulter `repo_audit.md`, `correction_audit.md`, `todo_audit.md` et `test_audit.md` dans ce dossier.
