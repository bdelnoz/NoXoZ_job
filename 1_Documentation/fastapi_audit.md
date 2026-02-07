# Audit FastAPI – NoXoZ_job

## Objectif
Ce document recense la configuration FastAPI, les endpoints, et les fichiers Python associés au périmètre API afin de servir de référence pour des audits similaires.

## Configuration FastAPI (résumé)
- L’application FastAPI est créée dans `2_Sources/2.1_Python/main_agent.py` avec un titre/version et un middleware CORS autorisant `https://127.0.0.1:8443`, puis le routeur principal est inclus avec le préfixe `/api`.【F:2_Sources/2.1_Python/main_agent.py†L1-L14】
- La dépendance FastAPI est fixée à `fastapi==0.128.4` dans `requirements.txt`.【F:requirements.txt†L1-L33】

## Table des fichiers FastAPI et usages

| Fichier | Usage | Notes |
|---|---|---|
| `2_Sources/2.1_Python/main_agent.py` | Point d’entrée FastAPI : création de l’app, CORS, inclusion du routeur `/api`. | Application principale. 【F:2_Sources/2.1_Python/main_agent.py†L1-L14】 |
| `2_Sources/2.1_Python/api/router.py` | Routeur central : montage des routers `generate`, `status`, `upload`, `status_web`, `monitor`. | Définition des préfixes. 【F:2_Sources/2.1_Python/api/router.py†L1-L9】 |
| `2_Sources/2.1_Python/api/dependencies.py` | Placeholder pour dépendances FastAPI. | Vide pour l’instant. 【F:2_Sources/2.1_Python/api/dependencies.py†L1】 |
| `2_Sources/2.1_Python/api/endpoints/generate.py` | Endpoint `/generate` (POST) + health check. | Appelle `services.generation.generate_document`. 【F:2_Sources/2.1_Python/api/endpoints/generate.py†L1-L20】 |
| `2_Sources/2.1_Python/api/endpoints/upload.py` | Endpoint `/upload` (POST) + health check. | Appelle `services.ingestion.parse_and_store_file`. 【F:2_Sources/2.1_Python/api/endpoints/upload.py†L1-L20】 |
| `2_Sources/2.1_Python/api/endpoints/status.py` | Endpoint `/status` (GET) + health check. | Lit SQLite via `services.vector_store.METADATA_DB`. 【F:2_Sources/2.1_Python/api/endpoints/status.py†L1-L27】 |
| `2_Sources/2.1_Python/api/endpoints/status.ORI.py` | Copie de `status.py`. | Non référencé dans le routeur. 【F:2_Sources/2.1_Python/api/endpoints/status.ORI.py†L1-L23】 |
| `2_Sources/2.1_Python/api/endpoints/status_web.py` | Page HTML `/monitor/web_status`, lecture de fichiers `.py`, health check. | Inclut `read_file`. 【F:2_Sources/2.1_Python/api/endpoints/status_web.py†L1-L109】 |
| `2_Sources/2.1_Python/api/monitor.py` | Monitoring complet `/monitor/full` + health check. | Vérifie Chroma, SQLite, Ollama, logs, mémoire. 【F:2_Sources/2.1_Python/api/monitor.py†L1-L203】 |
| `2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py` | App FastAPI autonome (non intégrée au routeur principal). | Ancienne version de monitoring. 【F:2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py†L1-L121】 |
| `2_Sources/2.1_Python/services/generation.py` | Génération de document (Ollama + Chroma) pour `/generate`. | Génère un DOCX dans `5_Outputs`. 【F:2_Sources/2.1_Python/services/generation.py†L1-L41】 |
| `2_Sources/2.1_Python/services/ingestion.py` | Ingestion d’un fichier uploadé pour `/upload`. | Sauvegarde puis appelle `ingest_file`. 【F:2_Sources/2.1_Python/services/ingestion.py†L1-L21】 |
| `2_Sources/2.1_Python/services/vector_store.py` | Chroma + SQLite (ingestion, recherche similaire). | Utilisé par `generate` et `status`. 【F:2_Sources/2.1_Python/services/vector_store.py†L1-L120】 |
| `2_Sources/2.1_Python/chroma_integration.py` | Utilitaires Chroma (script autonome). | Non monté dans l’API. 【F:2_Sources/2.1_Python/chroma_integration.py†L1-L159】 |

## Endpoints FastAPI (chemins complets)

> Tous les endpoints sont préfixés par `/api` via `main_agent.py`.【F:2_Sources/2.1_Python/main_agent.py†L1-L14】

| Méthode | Chemin | Fichier | Description |
|---|---|---|---|
| POST | `/api/generate/` | `api/endpoints/generate.py` | Génération d’un document à partir d’un prompt et d’un template. 【F:2_Sources/2.1_Python/api/endpoints/generate.py†L1-L16】 |
| GET | `/api/generate/health` | `api/endpoints/generate.py` | Health check `generate`. 【F:2_Sources/2.1_Python/api/endpoints/generate.py†L17-L20】 |
| POST | `/api/upload/` | `api/endpoints/upload.py` | Upload et ingestion d’un fichier. 【F:2_Sources/2.1_Python/api/endpoints/upload.py†L1-L16】 |
| GET | `/api/upload/health` | `api/endpoints/upload.py` | Health check `upload`. 【F:2_Sources/2.1_Python/api/endpoints/upload.py†L17-L20】 |
| GET | `/api/status/` | `api/endpoints/status.py` | Statut basé sur le nombre de documents en SQLite. 【F:2_Sources/2.1_Python/api/endpoints/status.py†L1-L23】 |
| GET | `/api/status/health` | `api/endpoints/status.py` | Health check `status`. 【F:2_Sources/2.1_Python/api/endpoints/status.py†L24-L27】 |
| GET | `/api/monitor/web_status` | `api/endpoints/status_web.py` | Page HTML de statut des endpoints et des fichiers Python. 【F:2_Sources/2.1_Python/api/endpoints/status_web.py†L1-L84】 |
| GET | `/api/monitor/read_file?file_path=...` | `api/endpoints/status_web.py` | Lecture d’un fichier `.py` depuis l’interface. 【F:2_Sources/2.1_Python/api/endpoints/status_web.py†L86-L99】 |
| GET | `/api/monitor/health` | `api/endpoints/status_web.py` | Health check de la page `monitor`. 【F:2_Sources/2.1_Python/api/endpoints/status_web.py†L101-L109】 |
| GET | `/api/monitor/full` | `api/monitor.py` | Monitoring complet (FastAPI/Chroma/SQLite/Ollama/logs/mémoire). 【F:2_Sources/2.1_Python/api/monitor.py†L164-L193】 |
| GET | `/api/monitor/health` | `api/monitor.py` | Health check du monitor complet. 【F:2_Sources/2.1_Python/api/monitor.py†L196-L203】 |

## Points d’attention
- **Conflit de route** : le chemin `/api/monitor/health` est déclaré deux fois (dans `status_web.py` et `monitor.py`). L’ordre d’inclusion dans `api/router.py` peut rendre un des deux endpoints inactif ou provoquer un comportement ambigu.【F:2_Sources/2.1_Python/api/router.py†L1-L9】【F:2_Sources/2.1_Python/api/endpoints/status_web.py†L101-L109】【F:2_Sources/2.1_Python/api/monitor.py†L196-L203】
- **`fastapi_full_monitor.py`** contient sa propre app FastAPI, mais n’est pas montée dans `main_agent.py`. Il s’agit d’un script autonome historique plutôt qu’un endpoint actif dans l’API principale.【F:2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py†L1-L121】
