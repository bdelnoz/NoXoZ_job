# FILENAME: INSTALL.md
# COMPLETE PATH: audit/INSTALL.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Prérequis système détaillés
- Linux avec systemd (scripts de service).
- Python 3.x.
- Ollama installé localement.
- Accès aux chemins /mnt/data1_100g et /mnt/data2_78g (actuellement hardcodés).

## Dépendances OS
- curl, sqlite3, ss, pkill, systemctl.
- Bibliothèques pour python-docx (zip/unzip). (UNKNOWN si déjà installées.)

## Installation des langages
- Python 3.x via package OS ou pyenv.

## Installation des dépendances projet
```
pip install -r requirements.txt
```

## Variables d’environnement
- CHROMA_PERSIST_DIR (utilisé dans test_db_huffing.py).
- SENTENCE_TRANSFORMERS_HOME (utilisé dans test_db_huffing.py).
- Autres variables: UNKNOWN (paths hardcodés dans scripts et services).

## Scripts d’installation existants
- `8_Scripts/8.1_Init/init_project.sh`
- `8_Scripts/8.1_Init/init_python.sh`
- `8_Scripts/8.1_Init/init_fastapi.sh`
- `8_Scripts/8.1_Init/init_sqlite.sh`

## Vérifications post-install
- Démarrer FastAPI: `bash 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh start`.
- Vérifier l’API: `curl -k https://127.0.0.1:8443/api/status/health`.
- Vérifier monitoring: `curl -k https://127.0.0.1:8443/api/monitor/full`.

## Problèmes fréquents + solutions
- Erreur chemin /mnt/data1_100g manquant → créer le répertoire ou rendre les chemins configurables.
- Ollama non installé → installer Ollama et vérifier `ollama run`.
- Erreurs TLS → régénérer certs ou utiliser HTTP local.
