# Corrections à appliquer – Audit NoXoZ_job

## Corrections prioritaires (fonctionnelles)
1. **Unifier le chemin SQLite** : `services/vector_store.py` écrit `3_Data/Metadata/metadata.db` alors que `test_sqlite.sh` cible `3_Data/Metadata/noxoz_metadata.db`. Choisir un seul fichier et aligner tous les scripts/endpoints.
2. **Rendre cohérents les embeddings** : `chroma_integration.py` utilise `OpenAIEmbeddingFunction` alors que `vector_store.py` utilise `HuggingFaceEmbeddings` local. Basculer vers un modèle local partout.
3. **Normaliser les chemins absolus** : de nombreux scripts hardcodent `/mnt/data1_100g/...` et `/mnt/data2_78g/...`. Remplacer par `.env` + variables pour faciliter le déploiement.
4. **Nettoyer la duplication d’endpoints** : `api/endpoints/status.ORI.py` et `api/endpoints/fastapi_full_monitor.py` semblent obsolètes/non branchés (risque de confusion). Supprimer ou documenter.

## Corrections qualité & maintenance
5. **Nettoyer les fichiers temporaires** : `temp.py` (racine + 2_Sources) et `check_all_web_python.sh` sont des brouillons. Les déplacer dans un dossier `misc/` ou supprimer.
6. **`.gitignore`** : ajouter `fastapi.pid`, `10_Runs/*.pid`, logs spécifiques, `4_Logs/*.log` pour éviter la pollution Git.
7. **Séparer test vs prod** : les scripts de test démarrent FastAPI en mode `--reload` et écrivent dans les logs de prod. Prévoir un dossier de logs/test.
8. **Modulariser le monitoring** : `status_web.py` lit des fichiers directement; valider et sécuriser le chemin pour éviter la lecture non autorisée.
9. **Répertoires utilitaires volumineux** : `8_Scripts/8.2_Utils/argparse/json/requests/sys/datetime` semblent être des copies de docs/modules; évaluer s’il faut les versionner.

## Corrections documentation
10. **Compléter docs d’installation** : clarifier la création des certificats TLS, et le rôle exact de Docker Compose (ollama/chromadb uniquement).
