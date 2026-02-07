# Audit complet du dépôt NoXoZ_job

## 1) Inventaire des fichiers par domaine/fonction

### Backend (API + services Python)
- `2_Sources/2.1_Python/main_agent.py`
- `2_Sources/2.1_Python/api/__init__.py`
- `2_Sources/2.1_Python/api/dependencies.py`
- `2_Sources/2.1_Python/api/router.py`
- `2_Sources/2.1_Python/api/monitor.py`
- `2_Sources/2.1_Python/api/endpoints/generate.py`
- `2_Sources/2.1_Python/api/endpoints/upload.py`
- `2_Sources/2.1_Python/api/endpoints/status.py`
- `2_Sources/2.1_Python/api/endpoints/status_web.py`
- `2_Sources/2.1_Python/api/endpoints/status.ORI.py`
- `2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py`
- `2_Sources/2.1_Python/services/generation.py`
- `2_Sources/2.1_Python/services/ingestion.py`
- `2_Sources/2.1_Python/services/vector_store.py`
- `2_Sources/2.1_Python/chroma_integration.py`
- `2_Sources/2.1_Python/temp.py`
- `temp.py`

### Frontend
- Pas de frontend dédié. `status_web.py` génère une page HTML de statut (monitoring).

### Data / Storage
- `3_Data/3.1_Vectors/chroma_link` (symlink)
- `3_Data/3.1_Vectors/models_link` (symlink)
- `3_Data/Metadata/noxoz_metadata.db` (symlink)
- `3_Data/models/huggingface_embeddings/all-MiniLM-L6-v2` (symlink)

### Scripts (bash + utilitaires)
- `8_Scripts/8.1_Init/*.sh` (init, tests, services systemd)
- `8_Scripts/8.2_Utils/count_tokens.sh`
- `8_Scripts/8.2_Utils/md_compressor.py`
- `2_Sources/2.2_Bash/create_structure.sh`
- `check_all_web_python.sh`

### Documentation
- `README.md`
- `1_Documentation/**` (docs générales/techniques)
- `7_Infos/PERMANENT_MEMORY.md`
- `7_Infos/tree.txt`
- `audit/*.md` (audit généré)

### Config / Dépendances
- `.env`
- `.gitignore`
- `Pipfile`, `Pipfile.lock`, `requirements.txt`
- `certs/cert.pem`, `certs/key.pem`

### Infra / DevOps
- `docker-compose.yml`
- `8_Scripts/8.1_Init/service.fastapi/*`
- `8_Scripts/8.1_Init/service.ollama/*`

### Tests
- `2_Sources/2.1_Python/test_sentence_transfomers.py`
- `2_Sources/2.1_Python/test_db_huffing.py`
- `8_Scripts/8.1_Init/test_fastapi.sh`
- `8_Scripts/8.1_Init/test_sqlite.sh`

### Logs / Outputs / Results
- `4_Logs/*`, `5_Outputs/*`, `6_Results/*`, `10_Runs/*.pid`

---

## 2) Fichiers clés par domaine (usage)

### Backend
- **`main_agent.py`** : crée l’app FastAPI et monte les routes sous `/api`.
- **`api/router.py`** : routeur principal (generate, upload, status, monitor).
- **`api/endpoints/*`** : endpoints REST.
- **`services/vector_store.py`** : ingestion, embeddings, SQLite, recherche.
- **`services/generation.py`** : génération de DOCX via Ollama.
- **`services/ingestion.py`** : sauvegarde et ingestion des uploads.
- **`chroma_integration.py`** : intégration Chroma persistante (script standalone).

### Frontend
- **`status_web.py`** : page HTML de monitoring + lecture de fichiers Python.

### Data
- **`3_Data/3.1_Vectors/*`** : symlinks vers Chroma et modèles.
- **`3_Data/Metadata/noxoz_metadata.db`** : base SQLite (symlink).

### Scripts
- **Init** : `init_project.sh`, `init_python.sh`, `init_fastapi.sh`, `init_sqlite.sh`.
- **Services** : `service.fastapi/*`, `service.ollama/*`.
- **Tests** : `test_fastapi.sh`, `test_sqlite.sh`.
- **Utilitaires** : `count_tokens.sh`, `md_compressor.py`.

### Config
- **`requirements.txt` / `Pipfile`** : dépendances.
- **`.env`** : chemins Ollama/Chroma/Models.
- **`docker-compose.yml`** : services Ollama + Chroma.

---

## 3) Structure globale du projet

### Points d’entrée
- `main_agent.py` : application FastAPI.
- `api/router.py` : routeur principal.

### Modules principaux
- **API** : `api/endpoints/*`, `api/monitor.py`.
- **Services** : ingestion, génération, vector store.

### Flux de données
1. **Upload** (`/api/upload`) → sauvegarde fichier → ingestion Chroma + SQLite.
2. **Recherche** (services) → `search_similar()` sur Chroma.
3. **Génération** (`/api/generate`) → prompt enrichi → Ollama → DOCX.

### Dépendances majeures
- FastAPI, Uvicorn, ChromaDB, SQLite, LangChain, SentenceTransformers, Ollama.

---

## 4) API – Endpoints

| Méthode | Chemin | Description | Fichier source |
| --- | --- | --- | --- |
| POST | `/api/generate/` | Génère un document à partir d’un prompt | `api/endpoints/generate.py` |
| GET | `/api/generate/health` | Health check generate | `api/endpoints/generate.py` |
| POST | `/api/upload/` | Upload + ingestion d’un fichier | `api/endpoints/upload.py` |
| GET | `/api/upload/health` | Health check upload | `api/endpoints/upload.py` |
| GET | `/api/status/` | Statut (nombre de documents) | `api/endpoints/status.py` |
| GET | `/api/status/health` | Health check status | `api/endpoints/status.py` |
| GET | `/api/monitor/full` | Monitoring complet (Chroma/SQLite/Ollama/logs) | `api/monitor.py` |
| GET | `/api/monitor/health` | Health check monitor | `api/monitor.py` |
| GET | `/api/monitor/web_status` | Page HTML de status + endpoints | `api/endpoints/status_web.py` |
| GET | `/api/monitor/read_file` | Lire un fichier Python (affichage HTML) | `api/endpoints/status_web.py` |
| GET | `/api/monitor/health` | Health check status_web | `api/endpoints/status_web.py` |

---

## 5) Scripts `.sh` (usage)

- `8_Scripts/8.1_Init/init_project.sh` : création complète de la structure projet + fichiers init.
- `8_Scripts/8.1_Init/init_python.sh` : génère `requirements.txt` et installe les dépendances.
- `8_Scripts/8.1_Init/init_fastapi.sh` : init FastAPI (ports, certs, etc.).
- `8_Scripts/8.1_Init/init_sqlite.sh` : init SQLite + schémas.
- `8_Scripts/8.1_Init/test_fastapi.sh` : tests API (status, generate, upload).
- `8_Scripts/8.1_Init/test_sqlite.sh` : tests SQLite + perf.
- `8_Scripts/8.1_Init/reset_ollama_service.sh` : reset service Ollama (systemd).
- `8_Scripts/8.1_Init/fix_ollama_group_permissions.sh` : fix permissions Ollama.
- `8_Scripts/8.1_Init/ollama-batch-download.sh` : téléchargement batch de modèles.
- `8_Scripts/8.1_Init/config_paths.sh` : symlinks + config `.env`.
- `8_Scripts/8.1_Init/service.fastapi/*` : installation/désinstallation/launch systemd FastAPI.
- `8_Scripts/8.1_Init/service.ollama/*` : installation/désinstallation/launch systemd Ollama.
- `8_Scripts/8.2_Utils/count_tokens.sh` : compte tokens d’un fichier avec tiktoken.
- `2_Sources/2.2_Bash/create_structure.sh` : placeholder vide.
- `check_all_web_python.sh` : note/text snippet (non exécutable).

---

## 6) Scripts `.py` (usage + packages)

- `main_agent.py` : FastAPI, CORS → `fastapi`, `fastapi.middleware.cors`.
- `api/router.py` : routing → `fastapi`.
- `api/monitor.py` : monitoring Chroma/SQLite/Ollama → `chromadb`, `sqlite3`, `subprocess`.
- `api/endpoints/*` : handlers API → `fastapi`, `httpx`.
- `services/vector_store.py` : embeddings + Chroma + SQLite → `chromadb`, `langchain_community`, `pypdf`, `docx`.
- `services/ingestion.py` : upload + ingestion → `fastapi`, `shutil`.
- `services/generation.py` : Ollama CLI + docx → `subprocess`, `docx`.
- `chroma_integration.py` : ingestion Chroma → `chromadb`, `pypdf`, `docx`.
- `test_sentence_transfomers.py` : tests embeddings → `sentence_transformers`.
- `test_db_huffing.py` : tests Chroma → `chromadb`, `sentence_transformers`.
- `md_compressor.py` : compression MD via Ollama → `argparse`, `requests`.
- `temp.py` : tests torch → `torch`.

---

## 7) Duplications / conflits / obsolètes

- `api/endpoints/status.ORI.py` : doublon probable de `status.py`.
- `api/endpoints/fastapi_full_monitor.py` : app FastAPI séparée non branchée.
- `status_web.py` + `monitor.py` définissent tous deux `/api/monitor/health`.
- `temp.py` à la racine et dans `2_Sources/2.1_Python` : fichiers de test.
- `create_structure.sh` vide.
- `check_all_web_python.sh` : fichier de notes avec snippets.
- Chemins absolus `/mnt/data1_100g/...` et `/mnt/data2_78g/...` très couplés à l’environnement.

---

## 8) Tableau synthétique des fichiers

| Chemin | Usage |
| --- | --- |
| .env | Variables d'environnement |
| .gitignore | Règles gitignore |
| 10_Runs/ollama.pid | PID files / état runtime |
| 10_Runs/service.noxoz_job.ollama.pid | PID files / état runtime |
| 1_Documentation/1.1_General/ARCHITECTURE.md | Documentation et spécifications |
| 1_Documentation/1.1_General/INSTALL.docx | Documentation et spécifications |
| 1_Documentation/1.1_General/WHY.docx | Documentation et spécifications |
| 1_Documentation/1.1_General/ollama-models-guide.md | Documentation et spécifications |
| 1_Documentation/1.2_Technical/API_SPECIFICATIONS.docx | Documentation et spécifications |
| 1_Documentation/1.2_Technical/COMPOSANTS.csv | Documentation et spécifications |
| 1_Documentation/1.2_Technical/OLLAMA_all_models_with_token_limits.md | Documentation et spécifications |
| 1_Documentation/1.2_Technical/OLLAMA_commandes.md | Documentation et spécifications |
| 1_Documentation/1.2_Technical/pipenv_guide.md | Documentation et spécifications |
| 1_Documentation/1.2_Technical/structure.md | Documentation et spécifications |
| 1_Documentation/1.2_Technical/table.csv | Documentation et spécifications |
| 1_Documentation/1.3_Status/COMPOSANTS_mis_a_jour.csv | Documentation et spécifications |
| 1_Documentation/1.3_Status/plan_detaille.md | Documentation et spécifications |
| 1_Documentation/fastapi_audit.md | Documentation et spécifications |
| 1_Documentation/out.txt | Documentation et spécifications |
| 2_Sources/2.1_Python/api/__init__.py | Infrastructure FastAPI |
| 2_Sources/2.1_Python/api/dependencies.py | Infrastructure FastAPI |
| 2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/endpoints/generate.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/endpoints/status.ORI.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/endpoints/status.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/endpoints/status_web.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/endpoints/upload.py | Endpoint FastAPI |
| 2_Sources/2.1_Python/api/monitor.py | Infrastructure FastAPI |
| 2_Sources/2.1_Python/api/router.py | Infrastructure FastAPI |
| 2_Sources/2.1_Python/chroma_integration.py | Code Python principal ou scripts de test |
| 2_Sources/2.1_Python/main_agent.py | Code Python principal ou scripts de test |
| 2_Sources/2.1_Python/services/generation.py | Services métier (ingestion/génération/vector store) |
| 2_Sources/2.1_Python/services/ingestion.py | Services métier (ingestion/génération/vector store) |
| 2_Sources/2.1_Python/services/vector_store.py | Services métier (ingestion/génération/vector store) |
| 2_Sources/2.1_Python/temp.py | Code Python principal ou scripts de test |
| 2_Sources/2.1_Python/test_db_huffing.py | Code Python principal ou scripts de test |
| 2_Sources/2.1_Python/test_sentence_transfomers.py | Code Python principal ou scripts de test |
| 2_Sources/2.2_Bash/create_structure.sh | Script Bash (structure projet) |
| 2_Sources/out.txt | Fichier projet |
| 4_Logs/init.txt | Emplacement logs (placeholder ou logs) |
| 5_Outputs/init.txt | Sorties générées (placeholder) |
| 5_Outputs/out.txt | Sorties générées (placeholder) |
| 5_Outputs/outputs.md | Sorties générées (placeholder) |
| 6_Results/init.txt | Résultats (placeholder) |
| 7_Infos/PERMANENT_MEMORY.md | Notes/informations projet |
| 7_Infos/tree.txt | Notes/informations projet |
| 8_Scripts/8.1_Init/config_paths.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/create-repo.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/fix_ollama_group_permissions.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/init_fastapi.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/init_project.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/init_python.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/init_sqlite.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/old_versions/all_my_scripts.old_versions.txt | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/ollama-batch-download.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/reset_ollama_service.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.fastapi/install_service.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.fastapi/noxoz_job.fastapi.service | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.fastapi/uninstall_service.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.ollama/install_service.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.ollama/noxoz_job.ollama.service | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.ollama/start_ollama.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/service.ollama/uninstall_service.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/test_fastapi.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.1_Init/test_sqlite.sh | Scripts d'initialisation/test/service |
| 8_Scripts/8.2_Utils/argparse | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/count_tokens.sh | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/datetime | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/json | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/md_compressor.py | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/requests | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/8.2_Utils/sys | Outils utilitaires (scripts/artefacts) |
| 8_Scripts/out.txt | Scripts projet |
| 9_Templates/init.txt | Templates (placeholder) |
| Pipfile | Dépendances Python |
| Pipfile.lock | Dépendances Python |
| README.md | Documentation principale |
| audit/ARCHITECTURE.md | Audit généré |
| audit/CHANGELOG.md | Audit généré |
| audit/DEBUG.md | Audit généré |
| audit/INSTALL.md | Audit généré |
| audit/README.md | Audit généré |
| audit/TESTING.md | Audit généré |
| audit/USAGE.md | Audit généré |
| audit/correction_audit.md | Audit généré |
| audit/correction_audit.pdf | Audit généré |
| audit/file_table.md | Audit généré |
| audit/repo_audit.md | Audit généré |
| audit/repo_audit.pdf | Audit généré |
| audit/test_audit.md | Audit généré |
| audit/test_audit.pdf | Audit généré |
| audit/todo_audit.md | Audit généré |
| audit/todo_audit.pdf | Audit généré |
| certs/cert.pem | Certificats TLS |
| certs/key.pem | Certificats TLS |
| check_all_web_python.sh | Fichier projet |
| correction_audit.md | Documentation |
| correction_audit.pdf | Document PDF |
| docker-compose.yml | Infrastructure Docker Compose |
| fastapi.pid | Fichier projet |
| repo_audit.md | Documentation |
| repo_audit.pdf | Document PDF |
| requirements.txt | Dépendances Python |
| temp.py | Fichier projet |
| todo_audit.md | Documentation |
| todo_audit.pdf | Document PDF |
---

## 9) Tableau des endpoints

| Méthode | Chemin | Description | Fichier |
| --- | --- | --- | --- |
| POST | `/api/generate/` | Génération de document | `api/endpoints/generate.py` |
| GET | `/api/generate/health` | Health check | `api/endpoints/generate.py` |
| POST | `/api/upload/` | Upload et ingestion | `api/endpoints/upload.py` |
| GET | `/api/upload/health` | Health check | `api/endpoints/upload.py` |
| GET | `/api/status/` | Statut documents | `api/endpoints/status.py` |
| GET | `/api/status/health` | Health check | `api/endpoints/status.py` |
| GET | `/api/monitor/full` | Monitoring complet | `api/monitor.py` |
| GET | `/api/monitor/health` | Health check monitor | `api/monitor.py` |
| GET | `/api/monitor/web_status` | Page HTML monitoring | `api/endpoints/status_web.py` |
| GET | `/api/monitor/read_file` | Lecture fichier Python | `api/endpoints/status_web.py` |
| GET | `/api/monitor/health` | Health check status_web | `api/endpoints/status_web.py` |
