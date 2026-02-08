# FILENAME: repo_audit.md
# COMPLETE PATH: audit/repo_audit.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## 4.2.1 Inventaire exhaustif (tous les fichiers)

### Backend (Python/FastAPI)
- 2_Sources/2.1_Python/api/__init__.py
- 2_Sources/2.1_Python/api/dependencies.py
- 2_Sources/2.1_Python/api/monitor.py
- 2_Sources/2.1_Python/api/router.py
- 2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py
- 2_Sources/2.1_Python/api/endpoints/generate.py
- 2_Sources/2.1_Python/api/endpoints/status.py
- 2_Sources/2.1_Python/api/endpoints/status.ORI.py
- 2_Sources/2.1_Python/api/endpoints/status_web.py
- 2_Sources/2.1_Python/api/endpoints/upload.py
- 2_Sources/2.1_Python/chroma_integration.py
- 2_Sources/2.1_Python/main_agent.py
- 2_Sources/2.1_Python/services/generation.py
- 2_Sources/2.1_Python/services/ingestion.py
- 2_Sources/2.1_Python/services/vector_store.py
- 2_Sources/2.1_Python/temp.py

### Frontend
- UNKNOWN (aucun fichier frontend détecté dans le repository)

### Data
- 4_Logs/init.txt
- 5_Outputs/init.txt
- 5_Outputs/out.txt
- 5_Outputs/outputs.md
- 6_Results/init.txt
- 7_Infos/PERMANENT_MEMORY.md
- 7_Infos/tree.txt
- 8_Scripts/out.txt
- 9_Templates/init.txt
- 10_Runs/ollama.pid
- 10_Runs/service.noxoz_job.ollama.pid
- fastapi.pid

### Scripts
- 2_Sources/2.2_Bash/create_structure.sh
- 8_Scripts/8.1_Init/config_paths.sh
- 8_Scripts/8.1_Init/create-repo.sh
- 8_Scripts/8.1_Init/fix_ollama_group_permissions.sh
- 8_Scripts/8.1_Init/init_fastapi.sh
- 8_Scripts/8.1_Init/init_project.sh
- 8_Scripts/8.1_Init/init_python.sh
- 8_Scripts/8.1_Init/init_sqlite.sh
- 8_Scripts/8.1_Init/ollama-batch-download.sh
- 8_Scripts/8.1_Init/reset_ollama_service.sh
- 8_Scripts/8.1_Init/test_fastapi.sh
- 8_Scripts/8.1_Init/test_sqlite.sh
- 8_Scripts/8.1_Init/service.fastapi/install_service.sh
- 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh
- 8_Scripts/8.1_Init/service.fastapi/uninstall_service.sh
- 8_Scripts/8.1_Init/service.ollama/install_service.sh
- 8_Scripts/8.1_Init/service.ollama/start_ollama.sh
- 8_Scripts/8.1_Init/service.ollama/uninstall_service.sh
- 8_Scripts/8.2_Utils/count_tokens.sh
- check_all_web_python.sh

### Docs
- 1_Documentation/fastapi_audit.md
- 1_Documentation/out.txt
- 1_Documentation/1.1_General/ARCHITECTURE.md
- 1_Documentation/1.1_General/INSTALL.docx
- 1_Documentation/1.1_General/WHY.docx
- 1_Documentation/1.1_General/ollama-models-guide.md
- 1_Documentation/1.2_Technical/API_SPECIFICATIONS.docx
- 1_Documentation/1.2_Technical/COMPOSANTS.csv
- 1_Documentation/1.2_Technical/OLLAMA_all_models_with_token_limits.md
- 1_Documentation/1.2_Technical/OLLAMA_commandes.md
- 1_Documentation/1.2_Technical/pipenv_guide.md
- 1_Documentation/1.2_Technical/structure.md
- 1_Documentation/1.2_Technical/table.csv
- 1_Documentation/1.3_Status/COMPOSANTS_mis_a_jour.csv
- 1_Documentation/1.3_Status/plan_detaille.md
- README.md
- audit/ARCHITECTURE.md
- audit/CHANGELOG.md
- audit/DEBUG.md
- audit/INSTALL.md
- audit/README.md
- audit/TESTING.md
- audit/USAGE.md
- audit/correction_audit.md
- audit/file_table.md
- audit/repo_audit.md
- audit/test_audit.md
- audit/todo_audit.md
- correction_audit.md
- correction_audit.pdf
- repo_audit.md
- repo_audit.pdf
- todo_audit.md
- todo_audit.pdf

### Config
- .env
- .gitignore
- Pipfile
- Pipfile.lock
- requirements.txt

### Infra
- certs/cert.pem
- certs/key.pem
- docker-compose.yml
- 8_Scripts/8.1_Init/service.fastapi/noxoz_job.fastapi.service
- 8_Scripts/8.1_Init/service.ollama/noxoz_job.ollama.service

### Tests
- 2_Sources/2.1_Python/test_db_huffing.py
- 2_Sources/2.1_Python/test_sentence_transfomers.py

### Autres
- temp.py
- .git/HEAD
- .git/FETCH_HEAD
- .git/config
- .git/description
- .git/index
- .git/info/exclude
- .git/logs/HEAD
- .git/logs/refs/heads/work
- .git/objects/05/ff6a0418235b0f8e173b7d6135850d8dccb446
- .git/objects/07/2bc127fc1e65f23402b9b2cb9de6ba9466cbf6
- .git/objects/0d/293efa8f48870000158ef3d55e97d99a117683
- .git/objects/17/44ac46e9e43d3bf057803cdb17ec0e9a6c2dce
- .git/objects/1f/90adf359cbc92476e8ae3583e262ea6634d260
- .git/objects/26/b01db3695b83e312959d3801d951eec706636b
- .git/objects/2c/311b9e9c65de23cce29e68a4903c5b250d536d
- .git/objects/2c/88698a1007172832d63bc9769817d7388e3938
- .git/objects/30/4d21dcf567124624a952e6f5bdfd1e79d1b107
- .git/objects/35/79755feb03ca40f15c0b05380b43072999411d
- .git/objects/3a/deb82b110ecdd3c5a54a14f1c24e579b85ec38
- .git/objects/43/8190f9e57329539857a162f4234425511f21b0
- .git/objects/45/e57c7eb52ceed4abbadb8dbf9969f56422274a
- .git/objects/53/af348cef9c198012afbfd4e109c18c5454a57f
- .git/objects/54/f9a96a33c8226ba02c13fd3dce968b068f2860
- .git/objects/5f/bd4eb0b3da1a470485d8e6bfeab1ceff9f6231
- .git/objects/60/cac26a9e9f3cf7275f0335e4b728acd7a5ecb1
- .git/objects/61/e2644b2b38adc8f3c0ecf22c157f4eeba7543e
- .git/objects/65/28fc4a2d3a60285527b12f29d6c8590e851eab
- .git/objects/68/ed38efccdb36943c76dd916ed26cdc39655c32
- .git/objects/6c/9d0db60c75ce94d10968a084b4841451a44cde
- .git/objects/70/098f186ff1fa1b13fb918549032108c9103599
- .git/objects/71/002ad43ee65f98997afd36211782aefd52966d
- .git/objects/81/c67e733a1264c3db5f6580a21e584c52702313
- .git/objects/85/a780e56eac6a974da871ffe5370e9cae0f576c
- .git/objects/87/f7b86e8a3e9b09936c343846160f525458d49f
- .git/objects/99/767d5cb136755cb75339a4396c2c3af9a9224d
- .git/objects/9d/8066e06a9eb1a8f4fc08d70dfe5f9d407c7bdf
- .git/objects/ab/eb309bae34245670055e2c7ab3ac480ab8ff2d
- .git/objects/b6/a6fde242290f54e8f1c47d7678bf8c3880892f
- .git/objects/c2/b58c1459cafcb02a16ff7a6b4ea29cc55ec9ca
- .git/objects/c3/bad4fef166a6b6a7ae7c58d7364d349a3a7c31
- .git/objects/da/c943ef925864496989f7b21400ac5cb1b2bd05
- .git/objects/d6/c4968bc2e36a0db902cd708a9579136bb44a70
- .git/objects/e2/3e913f254a0e477954723fad4f566cef15961b
- .git/objects/e2/81340245bad0cb469eae1a7bb52e98d45e96c6
- .git/objects/e7/f293f238cf6cda7c0438bd036ec1bf8b2ee7ef
- .git/objects/e9/0b94204c54a8e3f4356adfabbb3b4634337096
- .git/objects/eb/ab4145dec18e015a574dcf32dbe82ee05c40f2
- .git/objects/f8/e32f0c580217de2b74b33ff99f2c7dd6f599d9
- .git/objects/fb/1d94dfeb717727d540b7ff664be86a0389d632
- .git/objects/pack/pack-0d65f90cd3b9ab84c01be639dc3d6d1303e7d71d.idx
- .git/objects/pack/pack-0d65f90cd3b9ab84c01be639dc3d6d1303e7d71d.pack
- .git/objects/pack/pack-0d65f90cd3b9ab84c01be639dc3d6d1303e7d71d.rev
- .git/packed-refs
- .git/refs/heads/work
- .git/hooks/applypatch-msg.sample
- .git/hooks/commit-msg.sample
- .git/hooks/fsmonitor-watchman.sample
- .git/hooks/post-update.sample
- .git/hooks/pre-applypatch.sample
- .git/hooks/pre-commit.sample
- .git/hooks/pre-merge-commit.sample
- .git/hooks/pre-push.sample
- .git/hooks/pre-rebase.sample
- .git/hooks/pre-receive.sample
- .git/hooks/prepare-commit-msg.sample
- .git/hooks/push-to-checkout.sample
- .git/hooks/sendemail-validate.sample
- .git/hooks/update.sample

## 4.2.2 Analyse par domaine

### Backend
- Rôle fonctionnel: API FastAPI, ingestion de documents, stockage vectoriel Chroma, génération de documents via Ollama.
- Fichiers clés: main_agent.py (app FastAPI), api/router.py (routes), services/* (ingestion, generation, vector_store).
- Points d’entrée: main_agent:app pour Uvicorn, api/router.py.
- Dépendances internes: services.vector_store utilisé par ingestion/status/generation; api.monitor pour health complet.

### Frontend
- Rôle fonctionnel: UNKNOWN (aucun code frontend détecté).

### Data
- Rôle fonctionnel: logs init, outputs, résultats, mémoire permanente et PID runtime.
- Fichiers clés: 7_Infos/PERMANENT_MEMORY.md (mémoire), 5_Outputs/outputs.md, PID dans 10_Runs/.
- Points d’entrée: scripts shell et services FastAPI (écritures sur disque).
- Dépendances internes: scripts FastAPI/Ollama et services Python.

### Scripts
- Rôle fonctionnel: bootstrap projet, init Python/FastAPI/SQLite, gestion services systemd, scripts utilitaires.
- Fichiers clés: start_fastapi.sh, install_service.sh (fastapi/ollama), reset_ollama_service.sh.
- Points d’entrée: exécution directe en CLI.
- Dépendances internes: chemins absolus vers /mnt/data2_78g/... et /mnt/data1_100g/..., systemd, uvicorn, ollama.

### Docs
- Rôle fonctionnel: documentation fonctionnelle/technique, audits existants, architecture et templates.
- Fichiers clés: README.md, 1_Documentation/1.1_General/ARCHITECTURE.md, 1_Documentation/1.2_Technical/*.

### Config
- Rôle fonctionnel: dépendances Python et configuration de services.
- Fichiers clés: requirements.txt, Pipfile, docker-compose.yml.

### Infra
- Rôle fonctionnel: certificats TLS et définitions systemd.
- Fichiers clés: certs/*.pem, *.service.

### Tests
- Rôle fonctionnel: scripts de test manuels pour embeddings et Chroma.
- Fichiers clés: test_db_huffing.py, test_sentence_transfomers.py.

## 4.2.3 Structure globale

### Architecture logique
- API FastAPI (2_Sources/2.1_Python) exposant routes /api.
- Services Python pour ingestion, vector store (Chroma + SQLite), génération (Ollama + docx).
- Scripts shell pour init, déploiement systemd, démarrage local.
- Documentation et artefacts d’audit.

### Modules principaux
- API: api/router.py, api/endpoints/*.py.
- Services: services/vector_store.py, services/ingestion.py, services/generation.py.
- Monitoring: api/monitor.py, api/endpoints/status_web.py.
- Chroma utilitaire: chroma_integration.py (exemple/outil séparé).

### Flux de données détaillés
1. Upload → /api/upload → services.ingestion.parse_and_store_file → services.vector_store.ingest_file → Chroma + SQLite.
2. Génération → /api/generate → services.generation.generate_document → services.vector_store.search_similar → Ollama CLI → DOCX dans 5_Outputs/DOCX.
3. Status → /api/status → SQLite metadata.db comptage documents.
4. Monitoring → /api/monitor/full → vérifs Chroma/SQLite/Ollama/logs/memory.

### Dépendances majeures
- FastAPI/Starlette/Uvicorn.
- ChromaDB, sentence-transformers, langchain_community.
- Ollama (CLI externe), sqlite3, python-docx, pypdf.

## 4.2.4 API (si existante)

Framework: FastAPI
Point d’entrée principal: 2_Sources/2.1_Python/main_agent.py (app FastAPI)
Organisation des routes: 2_Sources/2.1_Python/api/router.py (prefix /api)

| Method | Path | Description | Source file | Handler |
| --- | --- | --- | --- | --- |
| POST | /api/generate/ | Génération de document depuis prompt | 2_Sources/2.1_Python/api/endpoints/generate.py | generate_doc |
| GET | /api/generate/health | Health check generate | 2_Sources/2.1_Python/api/endpoints/generate.py | health_generate |
| POST | /api/upload/ | Upload + ingestion fichier | 2_Sources/2.1_Python/api/endpoints/upload.py | upload_file |
| GET | /api/upload/health | Health check upload | 2_Sources/2.1_Python/api/endpoints/upload.py | health_upload |
| GET | /api/status/ | Statut SQLite documents | 2_Sources/2.1_Python/api/endpoints/status.py | status |
| GET | /api/status/health | Health check status | 2_Sources/2.1_Python/api/endpoints/status.py | health_status |
| GET | /api/monitor/full | Monitoring complet | 2_Sources/2.1_Python/api/monitor.py | full_monitor |
| GET | /api/monitor/health | Health check monitor | 2_Sources/2.1_Python/api/monitor.py | health_monitor |
| GET | /api/monitor/web_status | Page HTML status endpoints/fichiers | 2_Sources/2.1_Python/api/endpoints/status_web.py | web_status |
| GET | /api/monitor/read_file | Lecture d’un fichier .py local | 2_Sources/2.1_Python/api/endpoints/status_web.py | read_file |
| GET | /api/monitor/health | Health check status_web (collision avec monitor.py) | 2_Sources/2.1_Python/api/endpoints/status_web.py | health_statusweb |

## 4.2.5 Scripts shell (.sh)

| Script | Path | Usage | Arguments | Side effects | Dependencies |
| --- | --- | --- | --- | --- | --- |
| create_structure.sh | 2_Sources/2.2_Bash/create_structure.sh | UNKNOWN (fichier vide) | UNKNOWN | None | None |
| check_all_web_python.sh | check_all_web_python.sh | Audit/check web Python (UNKNOWN exact) | UNKNOWN | FS read | bash, python (UNKNOWN) |
| count_tokens.sh | 8_Scripts/8.2_Utils/count_tokens.sh | Compte tokens (UNKNOWN) | UNKNOWN | FS read | bash |
| init_project.sh | 8_Scripts/8.1_Init/init_project.sh | Init structure projet + .docx + logs | --exec/--simulate/--help | Crée dossiers/fichiers, modifie .gitignore | python3, docx |
| init_python.sh | 8_Scripts/8.1_Init/init_python.sh | Init environnement Python (UNKNOWN) | UNKNOWN | FS + venv/pip | python3/pip (UNKNOWN) |
| init_fastapi.sh | 8_Scripts/8.1_Init/init_fastapi.sh | Init FastAPI (UNKNOWN) | UNKNOWN | FS, venv | python3/uvicorn (UNKNOWN) |
| init_sqlite.sh | 8_Scripts/8.1_Init/init_sqlite.sh | Init SQLite (UNKNOWN) | UNKNOWN | FS, db create | sqlite3 (UNKNOWN) |
| test_fastapi.sh | 8_Scripts/8.1_Init/test_fastapi.sh | Test API (UNKNOWN) | UNKNOWN | Network to localhost | curl (UNKNOWN) |
| test_sqlite.sh | 8_Scripts/8.1_Init/test_sqlite.sh | Test SQLite (UNKNOWN) | UNKNOWN | DB access | sqlite3 |
| config_paths.sh | 8_Scripts/8.1_Init/config_paths.sh | Configure paths (UNKNOWN) | UNKNOWN | FS modifications | bash |
| create-repo.sh | 8_Scripts/8.1_Init/create-repo.sh | Création dépôt (UNKNOWN) | UNKNOWN | FS + git | git (UNKNOWN) |
| ollama-batch-download.sh | 8_Scripts/8.1_Init/ollama-batch-download.sh | Téléchargement modèles Ollama | UNKNOWN | Network + storage | ollama, curl (UNKNOWN) |
| reset_ollama_service.sh | 8_Scripts/8.1_Init/reset_ollama_service.sh | Reset service Ollama | UNKNOWN | systemctl, FS | systemd, sudo |
| fix_ollama_group_permissions.sh | 8_Scripts/8.1_Init/fix_ollama_group_permissions.sh | Fix permissions Ollama | UNKNOWN | systemctl restart | systemd, sudo |
| start_fastapi.sh | 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh | start|stop|restart|status|update-pid | start/stop/restart/status/update-pid | Démarre uvicorn, écrit PID/logs, kill processus | uvicorn, pipenv, ss, pkill |
| install_service.sh (fastapi) | 8_Scripts/8.1_Init/service.fastapi/install_service.sh | Installe service systemd FastAPI | UNKNOWN | Écrit service, systemctl enable/start | systemd, sudo |
| uninstall_service.sh (fastapi) | 8_Scripts/8.1_Init/service.fastapi/uninstall_service.sh | Désinstalle service systemd FastAPI | UNKNOWN | systemctl stop/disable, supprime service | systemd, sudo |
| start_ollama.sh | 8_Scripts/8.1_Init/service.ollama/start_ollama.sh | start|stop|restart|status | start/stop/restart/status | Démarre/arrête Ollama, PID/logs | ollama, systemd (UNKNOWN) |
| install_service.sh (ollama) | 8_Scripts/8.1_Init/service.ollama/install_service.sh | Installe service systemd Ollama | UNKNOWN | systemctl enable/start | systemd, sudo |
| uninstall_service.sh (ollama) | 8_Scripts/8.1_Init/service.ollama/uninstall_service.sh | Désinstalle service systemd Ollama | UNKNOWN | systemctl stop/disable | systemd, sudo |

## 4.2.6 Scripts Python (.py)

| Module | Path | Role | Main imports | External deps | Execution type |
| --- | --- | --- | --- | --- | --- |
| main_agent | 2_Sources/2.1_Python/main_agent.py | ASGI app FastAPI + CORS + routes | fastapi, CORSMiddleware | fastapi, starlette | Module (Uvicorn) |
| api.router | 2_Sources/2.1_Python/api/router.py | Déclare routes API | fastapi.APIRouter | fastapi | Module |
| api.monitor | 2_Sources/2.1_Python/api/monitor.py | Monitoring Chroma/SQLite/Ollama/logs | chromadb, sqlite3, subprocess | chromadb, sentence-transformers, curl | Module |
| api.dependencies | 2_Sources/2.1_Python/api/dependencies.py | Placeholder | None | None | Module |
| endpoints.generate | 2_Sources/2.1_Python/api/endpoints/generate.py | Génération doc | fastapi, JSONResponse | fastapi | Module |
| endpoints.upload | 2_Sources/2.1_Python/api/endpoints/upload.py | Upload + ingestion | fastapi, JSONResponse | fastapi | Module |
| endpoints.status | 2_Sources/2.1_Python/api/endpoints/status.py | Status SQLite | sqlite3, datetime | sqlite3 | Module |
| endpoints.status_web | 2_Sources/2.1_Python/api/endpoints/status_web.py | Page HTML status + lecture fichiers | httpx, pathlib | httpx | Module |
| endpoints.status.ORI | 2_Sources/2.1_Python/api/endpoints/status.ORI.py | Copie de status.py | sqlite3, datetime | sqlite3 | Module (legacy) |
| endpoints.fastapi_full_monitor | 2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py | App FastAPI monitor (standalone) | fastapi, chromadb | chromadb, sentence-transformers | Script (app) |
| services.vector_store | 2_Sources/2.1_Python/services/vector_store.py | Chroma + SQLite store | chromadb, sqlite3, HuggingFaceEmbeddings | chromadb, langchain_community, pypdf, docx | Module |
| services.ingestion | 2_Sources/2.1_Python/services/ingestion.py | Sauvegarde + ingestion | fastapi.UploadFile, shutil | fastapi | Module |
| services.generation | 2_Sources/2.1_Python/services/generation.py | Génération doc via Ollama | subprocess, docx | python-docx, ollama CLI | Module |
| chroma_integration | 2_Sources/2.1_Python/chroma_integration.py | Script d’intégration Chroma | chromadb, embedding_functions | chromadb | Script (__main__) |
| test_sentence_transfomers | 2_Sources/2.1_Python/test_sentence_transfomers.py | Test embeddings | sentence_transformers | sentence-transformers | Script |
| test_db_huffing | 2_Sources/2.1_Python/test_db_huffing.py | Test Chroma + embeddings | chromadb, sentence_transformers | chromadb, sentence-transformers | Script |
| temp | 2_Sources/2.1_Python/temp.py | UNKNOWN | UNKNOWN | UNKNOWN | Script |
| md_compressor | 8_Scripts/8.2_Utils/md_compressor.py | Utilitaire compression MD | UNKNOWN | UNKNOWN | Script |
| temp | temp.py | UNKNOWN | UNKNOWN | UNKNOWN | Script |

## 4.2.7 Problèmes détectés
- Collision d’endpoint /api/monitor/health défini dans monitor.py et status_web.py.
- Fichiers legacy/redondants: status.ORI.py dupliqué de status.py; chroma_integration.py fournit une API alternative (non branchée).
- Chemins absolus /mnt/data2_78g et /mnt/data1_100g hardcodés dans scripts et services.
- Présence d’artefacts d’audit au root (repo_audit.md, correction_audit.md) en plus de ./audit/.

## 4.2.8 Tableau synthétique global

| Path | Domain | Usage | Priority (High/Med/Low) |
| --- | --- | --- | --- |
| 2_Sources/2.1_Python/main_agent.py | backend | Point d’entrée FastAPI | High |
| 2_Sources/2.1_Python/api/router.py | backend | Routes API | High |
| 2_Sources/2.1_Python/services/vector_store.py | backend | Stockage Chroma/SQLite | High |
| 2_Sources/2.1_Python/services/ingestion.py | backend | Ingestion upload | High |
| 2_Sources/2.1_Python/services/generation.py | backend | Génération doc | High |
| 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh | scripts | Démarrage FastAPI | High |
| 8_Scripts/8.1_Init/service.ollama/install_service.sh | scripts | Service Ollama | Med |
| requirements.txt | config | Dépendances Python | High |
| docker-compose.yml | infra | Conteneurisation | Med |
| certs/*.pem | infra | TLS local | Med |
| 2_Sources/2.1_Python/api/monitor.py | backend | Monitoring | Med |
| 2_Sources/2.1_Python/api/endpoints/status_web.py | backend | Monitoring HTML | Med |
| 2_Sources/2.1_Python/api/endpoints/status.ORI.py | backend | Legacy duplicat | Low |
| 2_Sources/2.1_Python/chroma_integration.py | backend | Script utilitaire | Low |
