# TODO Audit – NoXoZ_job

PDF companion: `todo_audit.pdf`.

## P0 – Critiques (fiabilité & runtime)
- [ ] **Unifier les chemins SQLite** (choisir `noxoz_metadata.db` ou `metadata.db`, aligner code + scripts).
- [ ] **Corriger le conflit de route `/api/monitor/health`** (renommage ou fusion).
- [ ] **Harmoniser le chemin Chroma** (code + scripts + monitoring).

## P1 – Qualité & maintenance
- [ ] Supprimer/archiver `status.ORI.py` et `fastapi_full_monitor.py` si non utilisés.
- [ ] Nettoyer les `temp.py` si ce sont des scripts de test locaux.
- [ ] Renommer `check_all_web_python.sh` en `.md` ou `.txt` (ou ajouter un shebang + exécution réelle).
- [ ] Documenter l’usage réel de `init_fastapi.sh` vs `config_paths.sh`.

## P2 – Hygiène repo & clarté
- [ ] Ajouter `.gitignore` pour `4_Logs/`, `10_Runs/`, `5_Outputs/`, `6_Results/`.
- [ ] Déplacer les fichiers PS (`8_Scripts/8.2_Utils/*`) dans `docs/assets/` ou supprimer.
- [ ] Clarifier les scripts vides (supprimer `create-repo.sh`, `create_structure.sh` ou ajouter README).
- [ ] Mettre à jour la section arborescence du README.

## P3 – Améliorations futures
- [ ] Ajouter un vrai dossier `tests/` avec pytest + fixtures.
- [ ] Ajouter un healthcheck unique exposant tous les composants.
- [ ] Écrire un `Makefile` ou `taskfile` pour les commandes standard.

---

*Ce fichier fournit la liste d’actions issues de l’audit.*
