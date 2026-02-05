#!/bin/bash
# =============================================================================
# Script: config_paths.sh
# Auteur: Bruno DELNOZ - bruno.delnoz@protonmail.com
# Chemin: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/config_paths.sh
# Version: 1.7
# Date: 2026-02-04
# Description: Configure paths vers /mnt/data1_100g/agent_llm_local/ (lecture seule)
#              Crée symlinks et .env dans projet. Support pipenv pour dépendances.
# =============================================================================
# Changelog:
# v1.6: SIMULATE=false par défaut, pas de mkdir dans VOL_DIR, vérif existence
# v1.7: Adaptation pipenv : --install crée venv + installe deps via pipenv
# -----------------------------------------------------------------------------
# Couleurs
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
PROJECT_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
VOL_DIR="/mnt/data1_100g/agent_llm_local"
MODELS_DIR="$VOL_DIR/models"
VECTORS_DIR="$VOL_DIR/vectors"
LOG_DIR="$PROJECT_DIR/logs/CONFIG_PATHS"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/config_paths_${TIMESTAMP}.log"
SIMULATE="${SIMULATE:-false}"  # Réel par défaut

# -----------------------------------------------------------------------------
# Afficher aide
# -----------------------------------------------------------------------------
display_help() {
    cat <<'HELP'
Usage: ./config_paths.sh [options]
Options:
  --help          Cette aide
  --exec          Configure (réel par défaut)
  --prerequis     Vérifie prérequis
  --install       Initialise pipenv + installe deps (langchain, chromadb...)
  --simulate      Force dry-run
  --changelog     Historique
  --delete        Supprime config + backup
  --undelete      Restaure backup

Exemples:
  ./config_paths.sh --exec           # Réel
  ./config_paths.sh --simulate --exec # Dry-run
  ./config_paths.sh --install        # pipenv + deps
HELP
}

# -----------------------------------------------------------------------------
# Log + écran
# -----------------------------------------------------------------------------
log_screen() {
    local level="$1" msg="$2"
    echo "$msg" >> "$LOG_FILE"
    case "$level" in
        success) echo -e "${GREEN}[SUCCESS] $msg${NC}" ;;
        info)    echo -e "${YELLOW}[INFO] $msg${NC}" ;;
        error)   echo -e "${RED}[ERROR] $msg${NC}" ;;
        *)       echo "$msg" ;;
    esac
}

# -----------------------------------------------------------------------------
# Symlink
# -----------------------------------------------------------------------------
create_symlink() {
    local src="$1" dest="$2" step="$3"
    log_screen info "[Étape $step] Symlink $dest → $src"
    if [ "$SIMULATE" = "true" ]; then
        log_screen info "[DRY-RUN] ln -s $src $dest"
    else
        [ ! -e "$dest" ] && ln -s "$src" "$dest" && log_screen success "Symlink créé" || \
            log_screen info "Symlink existe déjà"
    fi
}

# -----------------------------------------------------------------------------
# Mise à jour .env
# -----------------------------------------------------------------------------
update_env() {
    local env_path="$PROJECT_DIR/.env"
    log_screen info "[Étape 5] Mise à jour $env_path"
    if [ "$SIMULATE" = "true" ]; then
        log_screen info "[DRY-RUN] Ajout dans .env"
        return
    fi

    cat <<'ENV' >> "$env_path"
# Config NoXoZ_job - $(date)
OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models
CHROMA_PERSIST_DIR=/mnt/data1_100g/agent_llm_local/vectors
BASE_DIR=/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job
ENV

    log_screen success ".env mis à jour"
}

# -----------------------------------------------------------------------------
# Vérif prérequis
# -----------------------------------------------------------------------------
check_prereqs() {
    log_screen info "[Étape 6] Vérification prérequis"
    local errors=0

    command -v ollama >/dev/null || { log_screen error "Ollama absent"; ((errors++)); }
    [ -d "$MODELS_DIR" ] || { log_screen error "models absent : $MODELS_DIR"; ((errors++)); }
    [ -d "$VECTORS_DIR" ] || { log_screen error "vectors absent : $VECTORS_DIR"; ((errors++)); }
    command -v pipenv >/dev/null || { log_screen error "pipenv absent"; ((errors++)); }
    [ -d "$PROJECT_DIR" ] || { log_screen error "Projet absent"; ((errors++)); }

    [ "$errors" -eq 0 ] && log_screen success "Prérequis OK" || \
        log_screen error "$errors problème(s) - corrige avant --exec"
}

# -----------------------------------------------------------------------------
# Installation avec pipenv
# -----------------------------------------------------------------------------
install_prereqs() {
    log_screen info "[Étape 7] Installation via pipenv"
    cd "$PROJECT_DIR" || { log_screen error "Impossible cd $PROJECT_DIR"; exit 1; }

    if [ "$SIMULATE" = "true" ]; then
        log_screen info "[DRY-RUN] pipenv install langchain chromadb python-dotenv fastapi uvicorn"
        return
    fi

    # Si pas de Pipfile → init
    [ ! -f Pipfile ] && pipenv --python 3 install && log_screen info "Pipenv initialisé"

    # Installation deps
    pipenv install langchain chromadb python-dotenv fastapi uvicorn || {
        log_screen error "Échec pipenv install"
        return 1
    }

    log_screen success "Dépendances installées via pipenv"
    log_screen info "Pour exécuter : pipenv run python 2_Sources/2.1_Python/main_agent.py"
}

# -----------------------------------------------------------------------------
# Config principale
# -----------------------------------------------------------------------------
config_paths() {
    log_screen info "[Étape 8] Configuration paths"
    create_symlink "$MODELS_DIR"  "$PROJECT_DIR/3_Data/3.1_Vectors/models_link"  "8.3"
    create_symlink "$VECTORS_DIR" "$PROJECT_DIR/3_Data/3.1_Vectors/chroma_link" "8.4"
    update_env

    local pyfile="$PROJECT_DIR/2_Sources/2.1_Python/main_agent.py"
    if [ -f "$pyfile" ]; then
        if grep -q "load_dotenv" "$pyfile"; then
            log_screen info "main_agent.py déjà patché"
        else
            if [ "$SIMULATE" = "true" ]; then
                log_screen info "[DRY-RUN] Patch main_agent.py"
            else
                sed -i '1i import os\nfrom dotenv import load_dotenv\nload_dotenv()\nBASE_DIR = os.getenv("BASE_DIR", "'"$PROJECT_DIR"'")' "$pyfile"
                log_screen success "main_agent.py patché"
            fi
        fi
    else
        log_screen error "main_agent.py introuvable"
    fi
}

# -----------------------------------------------------------------------------
# Delete / Undelete (inchangé pour l'instant)
# -----------------------------------------------------------------------------
delete_config() {
    local backup_dir="$PROJECT_DIR/backup_config_${TIMESTAMP}"
    log_screen info "[Étape 9] Suppression + backup → $backup_dir"
    if [ "$SIMULATE" = "true" ]; then log_screen info "[DRY-RUN]"; return; fi
    mkdir -p "$backup_dir"
    cp -p "$PROJECT_DIR/.env" "$backup_dir/" 2>/dev/null || true
    rm -f "$PROJECT_DIR/3_Data/3.1_Vectors/models_link" "$PROJECT_DIR/3_Data/3.1_Vectors/chroma_link" 2>/dev/null
    log_screen success "Config supprimée"
}

undelete_config() {
    log_screen info "[Étape 10] Recherche backup"
    local latest
    latest=$(find "$PROJECT_DIR" -maxdepth 1 -type d -name "backup_config_*" -print | sort | tail -n1)
    [ -z "$latest" ] && { log_screen error "Aucun backup"; return 1; }
    log_screen info "Restauration depuis $latest"
    if [ "$SIMULATE" = "true" ]; then log_screen info "[DRY-RUN]"; return; fi
    cp -p "$latest/.env" "$PROJECT_DIR/" 2>/dev/null && log_screen success "Restauration OK"
}

# -----------------------------------------------------------------------------
# Init logs
# -----------------------------------------------------------------------------
init_logs() {
    mkdir -p "$LOG_DIR"
    echo "[START] $(date)" > "$LOG_FILE"
    log_screen info "Logs → $LOG_FILE"
}

# -----------------------------------------------------------------------------
# Exécution
# -----------------------------------------------------------------------------
execute() {
    init_logs
    log_screen info "Mode : $( [ "$SIMULATE" = "true" ] && echo "DRY-RUN" || echo "RÉEL" )"
    check_prereqs
    config_paths
    echo -e "\n${GREEN}=== RÉSUMÉ ===${NC}"
    echo "Mode : $( [ "$SIMULATE" = "true" ] && echo DRY-RUN || echo RÉEL )"
    echo "Log : $LOG_FILE"
    echo -e "${GREEN}Terminé${NC}"
}

# -----------------------------------------------------------------------------
# Arguments
# -----------------------------------------------------------------------------
[ $# -eq 0 ] && { display_help; exit 0; }

case "$1" in
    --help)      display_help ;;
    --prerequis) init_logs; check_prereqs ;;
    --install)   init_logs; install_prereqs ;;
    --simulate)  SIMULATE="true"; shift; execute ;;
    --exec)      execute ;;
    --changelog) cat <<'CHANGELOG'
v1.7 - Support pipenv pour --install
v1.6 - SIMULATE=false par défaut
... (versions précédentes)
CHANGELOG
    ;;
    --delete)    init_logs; delete_config ;;
    --undelete)  init_logs; undelete_config ;;
    *)           echo "Option inconnue."; display_help ;;
esac
