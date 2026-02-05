#!/bin/bash
# Nom: setup_agent_llm.sh
# Auteur: Bruno DELNOZ - bruno.delnoz@protonmail.com
# Version: 1.0
# Date: 2026-02-04
# Changelog:
# v1.0: Initial setup with Ollama, LangChain, Docker. Added prerequisites check.

# HELP Bloc
if [ "\$1" == "--help" ]; then
    echo "Usage: ./setup_agent_llm.sh [options]"
    echo "Options:"
    echo "  --help: Affiche cette aide"
    echo "  --exec: Exécute le setup principal"
    echo "  --prerequis: Vérifie les prérequis"
    echo "  --install: Installe les prérequis manquants"
    echo "  --simulate: Dry-run (default: true)"
    echo "  --changelog: Affiche changelog complet"
    echo "  --delete: Supprime tout (avec backup)"
    echo "  --undelete: Restaure depuis backup"
    exit 0
fi

# Variables (réutilisables pour VBox)
BASE_DIR="${BASE_DIR:-/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job}"
REPO_NAME="NoXoZ_job"
SIMULATE="\${SIMULATE:-true}"

# Logs
LOG_FILE="log.setup_agent_llm.v1.0.log"
echo "[\$(date)] Démarrage" >> \$LOG_FILE

# Vérif Prérequis (--prerequis)
check_prereqs() {
    echo "Vérif: Python 3.10+, Docker, Git..."
    command -v python3 >/dev/null || echo "Python manquant"
    command -v docker >/dev/null || echo "Docker manquant"
    command -v git >/dev/null || echo "Git manquant"
}

# Install Prérequis (--install)
install_prereqs() {
    if [ "\$SIMULATE" == "true" ]; then echo "Dry-run: sudo apt update..."; return; fi
    sudo apt update -y
    sudo apt install -y python3 python3-pip docker.io git
    pip install langchain ollama fastapi uvicorn chromadb pandas pandoc python-docx pypdf2
}

# Exec Principal (--exec)
exec_setup() {
    mkdir -p \$BASE_DIR
    cd \$BASE_DIR
    git init
    git remote add origin https://github.com/<ton_user>/\$REPO_NAME.git

    # Install Ollama
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull mistral:7b-instruct-v0.2

    # Docker Compose
    cat > docker-compose.yml << EOL
version: '3'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
  chroma:
    image: chromadb/chroma
    volumes:
      - \$BASE_DIR/vectors:/chroma
EOL

    git add .
    git commit -m "Initial setup v1.0"
    git push origin main
}

# Delete (--delete)
delete_all() {
    BACKUP_DIR="\$BASE_DIR/backup_\$(date +%Y%m%d_%H%M%S)"
    mkdir -p \$BACKUP_DIR
    mv \$BASE_DIR/* \$BACKUP_DIR
    rm -rf \$BASE_DIR/*
    echo "Supprimé avec backup en \$BACKUP_DIR"
}

# Undelete (--undelete)
undelete() {
    LATEST_BACKUP=\$(ls -d \$BASE_DIR/backup_* | tail -1)
    mv \$LATEST_BACKUP/* \$BASE_DIR/
    rm -rf \$LATEST_BACKUP
}

# Traitement args
case "$1" in
    --prerequis) check_prereqs ;;
    --install) install_prereqs ;;
    --exec) exec_setup ;;
    --delete) delete_all ;;
    --undelete) undelete ;;
    *) echo "Utilise --help" ;;
esac

echo "[$(date)] Fin" >> \$LOG_FILE
