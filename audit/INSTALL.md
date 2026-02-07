# NoXoZ_job – Installation (audit)

## Prérequis
- Python 3.13 (Pipenv recommandé).
- Ollama installé localement.
- Accès aux répertoires `/mnt/data1_100g/agent_llm_local/*`.
- (Optionnel) Docker + Docker Compose.

## Installation Python (Pipenv)
```bash
pip install pipenv
pipenv install --python 3.13
pipenv install -r requirements.txt
```

## Installation via requirements.txt
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration des chemins
```bash
8_Scripts/8.1_Init/config_paths.sh --exec
```

## Déploiement Docker (optionnel)
```bash
docker compose up -d
```

## Génération des certificats TLS
Les certificats sont présents dans `certs/` (utilisés par FastAPI en HTTPS local).
