# FILENAME: todo_audit.md
# COMPLETE PATH: audit/todo_audit.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## P0
- [ ] Normaliser les chemins via variables d’environnement (CHROMA_DIR, SQLITE_DB, BASE_DIR). Dépendances: aucune. Validation: app démarre avec chemins custom.
- [ ] Résoudre la collision /api/monitor/health. Dépendances: aucune. Validation: routes uniques dans /docs.

## P1
- [ ] Documenter précisément l’installation (Ollama, modèles, Chroma). Dépendances: P0 chemins. Validation: un nouveau dev peut installer sans erreur.
- [ ] Remplacer les certificats TLS versionnés par génération locale. Dépendances: P0 chemins. Validation: certs générés via script.
- [ ] Nettoyer fichiers legacy (status.ORI.py, fastapi_full_monitor.py si non utilisé). Dépendances: P0 routes. Validation: aucun import orphelin.

## P2
- [ ] Ajouter tests automatisés (pytest) pour endpoints /generate, /upload, /status. Dépendances: P0. Validation: tests passent en CI.
- [ ] Ajouter validation d’upload (taille, type). Dépendances: P0. Validation: erreurs gérées pour formats non supportés.
- [ ] Ajouter journalisation structurée. Dépendances: P1 docs. Validation: logs JSON ou format standardisé.
