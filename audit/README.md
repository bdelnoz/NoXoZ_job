# FILENAME: README.md
# COMPLETE PATH: audit/README.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Description du projet
NoXoZ_job est un agent LLM local orienté génération et gestion de documents professionnels (CV, lettres, emails), avec ingestion multi-format et API FastAPI. Objectif: fonctionnement 100% offline avec stockage local (Chroma + SQLite) et génération via Ollama.

## Périmètre fonctionnel
- Ingestion de documents (PDF/DOCX/MD/TXT/JSON/XML).
- Recherche vectorielle via ChromaDB.
- Génération de documents via Ollama CLI.
- API REST FastAPI (upload, generate, status, monitor).

## Stack technique complète
- Backend: Python 3, FastAPI, Uvicorn.
- Vector store: ChromaDB.
- Embeddings: sentence-transformers, langchain_community.
- Stockage: SQLite.
- Génération: Ollama CLI + python-docx.
- Scripts: Bash (init, services systemd).
- Conteneurisation: Docker Compose.

## Architecture (résumé)
- FastAPI expose /api/*.
- services/* gère ingestion, vector store, génération.
- Scripts shell démarrent/arrêtent services et init projet.
Voir ARCHITECTURE.md.

## Prérequis système
- Linux avec systemd (scripts de service).
- Python 3.x + pip/pipenv.
- Ollama installé localement.
- Accès fichiers /mnt/data1_100g et /mnt/data2_78g (actuellement hardcodé).

## Installation rapide (TL;DR)
1. Installer dépendances Python: `pip install -r requirements.txt`.
2. Installer Ollama et modèles.
3. Démarrer FastAPI: `bash 8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh start`.

## Lancement rapide
- API: `https://127.0.0.1:8443/api`.
- Status web: `https://127.0.0.1:8443/api/monitor/web_status`.

## Liens documentation
- INSTALL.md
- USAGE.md
- TESTING.md
- DEBUG.md
- ARCHITECTURE.md

## État du projet
UNKNOWN (aucun indicateur stable/POC explicite dans le repository).

## Licence
UNKNOWN
