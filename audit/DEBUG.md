# FILENAME: DEBUG.md
# COMPLETE PATH: audit/DEBUG.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Erreurs d’installation
### Symptômes
- ImportError sur chromadb, sentence-transformers, docx.
### Causes possibles
- Dépendances Python non installées.
### Diagnostic
- `pip show chromadb sentence-transformers python-docx`
### Logs
- Logs pip/pipenv.
### Solutions
- `pip install -r requirements.txt`

## Erreurs d’exécution
### Symptômes
- API ne démarre pas sur 8443.
### Causes possibles
- Certificats TLS invalides, port occupé.
### Diagnostic
- `ss -tlpn | grep 8443`
- `tail -n 200 4_Logs/log.start_fastapi.*.log`
### Solutions
- Libérer le port ou changer PORT dans start_fastapi.sh.

## Erreurs API / réseau
### Symptômes
- 500 lors de /api/generate.
### Causes possibles
- Ollama non disponible.
### Diagnostic
- `curl http://localhost:11434/api/tags`
### Solutions
- Démarrer Ollama via service.ollama/start_ollama.sh.

## Erreurs de dépendances
### Symptômes
- ImportError pypdf / docx.
### Causes possibles
- Paquets manquants.
### Diagnostic
- `python -c "import pypdf, docx"`
### Solutions
- Installer requirements.txt.

## Erreurs de configuration
### Symptômes
- Erreurs chemins /mnt/data1_100g.
### Causes possibles
- Dossiers inexistants.
### Diagnostic
- `ls /mnt/data1_100g`
### Solutions
- Créer les dossiers ou rendre les chemins configurables.
