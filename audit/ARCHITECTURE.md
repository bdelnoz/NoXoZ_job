# FILENAME: ARCHITECTURE.md
# COMPLETE PATH: audit/ARCHITECTURE.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Vue d’ensemble logique
- FastAPI expose l’API REST.
- Services Python assurent ingestion, stockage vectoriel, génération de documents.
- Scripts shell gèrent l’initialisation et les services systemd.

## Découpage par couches
1. API: `2_Sources/2.1_Python/api/*`.
2. Services: `2_Sources/2.1_Python/services/*`.
3. Data/Storage: `3_Data` (Chroma, SQLite), `5_Outputs` (DOCX), `4_Logs`.
4. Runtime/Infra: `8_Scripts/8.1_Init` + `certs/` + systemd services.

## Points d’entrée
- ASGI: `2_Sources/2.1_Python/main_agent.py` via Uvicorn.
- CLI scripts: `8_Scripts/8.1_Init/service.fastapi/start_fastapi.sh`, `service.ollama/*`.

## Flux de données détaillés
- Upload (API) → sauvegarde fichier → ingestion vectorielle → metadata SQLite.
- Génération (API) → query embeddings → contexte → appel Ollama → DOCX.
- Monitoring (API) → statut Chroma/SQLite/Ollama → rendu JSON/HTML.

## Dépendances internes
- API ↔ services.*
- services.vector_store ↔ Chroma/SQLite.

## Dépendances externes
- Ollama CLI
- ChromaDB
- sentence-transformers
- python-docx

## Contraintes techniques
- Chemins absolus /mnt/data1_100g et /mnt/data2_78g.
- Scripts systemd supposent un OS Linux avec systemd.

## Limitations
- Collision d’endpoint /api/monitor/health.
- Tests automatiques absents.

## Axes d’évolution
- Ajouter tests automatisés.
- Rendre la config portable (env vars).
- Sécuriser upload et lecture de fichiers.
