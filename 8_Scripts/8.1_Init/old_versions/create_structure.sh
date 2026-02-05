#!/bin/bash

# =============================================================================
# Script: create_structure.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Chemin: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/scripts/create_structure.sh
# Version: 1.1
# Date: 2026-02-04
# Description: Crée la structure de répertoires et fichiers vides pour NoXoZ_job.
# =============================================================================

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
SCRIPT_NAME="create_structure.sh"
LOG_DIR="$BASE_DIR/logs/LOGS"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/log.$SCRIPT_NAME.$TIMESTAMP.log"
SIMULATE="${SIMULATE:-true}"
AUTHOR="Bruno DELNOZ"
EMAIL="bruno.delnoz@protonmail.com"

# -----------------------------------------------------------------------------
# Étape 1/10 : Afficher l'aide
# -----------------------------------------------------------------------------
display_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --help       Affiche cette aide"
    echo "  --exec       Exécute la création de la structure"
    echo "  --simulate   Mode simulation (défaut: activé)"
    echo "Exemple:"
    echo "  $0 --exec"
}

# -----------------------------------------------------------------------------
# Étape 2/10 : Créer un répertoire
# -----------------------------------------------------------------------------
create_directory() {
    local dir_path="$1"
    local step="$2"
    echo "[Étape $step/10] Création du répertoire: $dir_path"
    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Répertoire: $dir_path" >> "$LOG_FILE"
    else
        if [ ! -d "$dir_path" ]; then
            mkdir -p "$dir_path"
            echo "Répertoire créé: $dir_path" >> "$LOG_FILE"
        else
            echo "Répertoire existant: $dir_path" >> "$LOG_FILE"
        fi
    fi
}

# -----------------------------------------------------------------------------
# Étape 3/10 : Créer un fichier vide
# -----------------------------------------------------------------------------
create_file() {
    local file_path="$1"
    local step="$2"
    echo "[Étape $step/10] Création du fichier: $file_path"
    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Fichier: $file_path" >> "$LOG_FILE"
    else
        if [ ! -f "$file_path" ]; then
            touch "$file_path"
            echo "Fichier créé: $file_path" >> "$LOG_FILE"
        else
            echo "Fichier existant: $file_path" >> "$LOG_FILE"
        fi
    fi
}

# -----------------------------------------------------------------------------
# Étape 4/10 : Mettre à jour .gitignore
# -----------------------------------------------------------------------------
update_gitignore() {
    local step="4/10"
    echo "[Étape $step] Mise à jour de .gitignore"
    local gitignore_path="$BASE_DIR/.gitignore"
    local entries=("# Logs\nlogs/\n\n# Outputs\noutputs/\n\n# Results\nresults/\n\n# Infos\ninfos/")

    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Mise à jour de $gitignore_path" >> "$LOG_FILE"
    else
        if [ ! -f "$gitignore_path" ]; then
            echo "$entries" > "$gitignore_path"
            echo "Fichier .gitignore créé avec les entrées standard." >> "$LOG_FILE"
        else
            if ! grep -q "logs/" "$gitignore_path"; then
                echo -e "\n$entries" >> "$gitignore_path"
                echo "Entrées ajoutées à .gitignore." >> "$LOG_FILE"
            else
                echo ".gitignore déjà à jour." >> "$LOG_FILE"
            fi
        fi
    fi
}

# -----------------------------------------------------------------------------
# Étape 5/10 : Initialiser les répertoires de logs
# -----------------------------------------------------------------------------
init_logs() {
    local step="5/10"
    echo "[Étape $step] Initialisation des répertoires de logs"
    create_directory "$BASE_DIR/logs" "$step"
    create_directory "$LOG_DIR" "$step"
}

# -----------------------------------------------------------------------------
# Étape 6/10 : Créer la structure complète
# -----------------------------------------------------------------------------
create_structure() {
    echo "[$(date)] Début de la création de la structure pour NoXoZ_job" >> "$LOG_FILE"

    # Répertoires principaux
    local directories=(
        "$BASE_DIR"
        "$BASE_DIR/.github/workflows"
        "$BASE_DIR/scripts"
        "$BASE_DIR/scripts/old_versions"
        "$BASE_DIR/src"
        "$BASE_DIR/data"
        "$BASE_DIR/data/vectors"
        "$BASE_DIR/results"
        "$BASE_DIR/infos"
    )

    # Fichiers principaux
    local files=(
        "$BASE_DIR/README.md"
        "$BASE_DIR/WHY.MD"
        "$BASE_DIR/CHANGELOG.md"
        "$BASE_DIR/INSTALL.MD"
        "$BASE_DIR/src/main_agent.py"
        "$BASE_DIR/docker-compose.yml"
        "$BASE_DIR/requirements.txt"
        "$BASE_DIR/scripts/create-repo.sh"
        "$BASE_DIR/scripts/old_versions/all_my_scripts.old_versions.txt"
        "$BASE_DIR/.github/workflows/deploy.yml"
    )

    # Création des répertoires
    for i in {1..6}; do
        local dir="${directories[$((i-1))]}"
        create_directory "$dir" "$((i+5))"
    done

    # Création des fichiers
    for i in {1..7}; do
        local file="${files[$((i-1))]}"
        create_file "$file" "$((i+11))"
    done

    # Mise à jour de .gitignore
    update_gitignore

    echo "[$(date)] Fin de la création de la structure" >> "$LOG_FILE"
}

# -----------------------------------------------------------------------------
# Étape 7/10 : Afficher le changelog
# -----------------------------------------------------------------------------
display_changelog() {
    echo "Changelog pour $SCRIPT_NAME:"
    echo "v1.1 (2026-02-04):"
    echo "  - Correction de la création des répertoires de logs avant écriture."
    echo "  - Ajout de l'affichage des étapes d'avancement."
    echo "v1.0 (2026-02-04):"
    echo "  - Création initiale du script pour générer la structure du projet NoXoZ_job."
}

# -----------------------------------------------------------------------------
# Étape 8/10 : Vérifier les prérequis
# -----------------------------------------------------------------------------
check_prerequisites() {
    echo "[Étape 8/10] Vérification des prérequis"
    if [ ! -d "$BASE_DIR" ]; then
        echo "Erreur: Le répertoire de base n'existe pas: $BASE_DIR" >> "$LOG_FILE"
        exit 1
    fi
}

# -----------------------------------------------------------------------------
# Étape 9/10 : Exécuter la création de la structure
# -----------------------------------------------------------------------------
execute() {
    init_logs
    check_prerequisites
    create_structure
}

# -----------------------------------------------------------------------------
# Étape 10/10 : Traitement des arguments
# -----------------------------------------------------------------------------
case "$1" in
    --help)
        display_help
        ;;
    --exec)
        SIMULATE="false"
        execute
        ;;
    --simulate)
        SIMULATE="true"
        execute
        ;;
    *)
        display_help
        ;;
esac

# -----------------------------------------------------------------------------
# Affichage final
# -----------------------------------------------------------------------------
display_changelog
echo "Script exécuté avec succès. Consultez $LOG_FILE pour plus de détails."
