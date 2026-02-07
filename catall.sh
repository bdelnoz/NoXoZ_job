#!/bin/bash

########################################################################################################################
# Auteur: Bruno DELNOZ                                                                                                   #
# Email: bruno.delnoz@protonmail.com                                                                                     #
# Chemin complet du script: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/service.ollama/cat_files.sh #
# Version: 1.8                                                                                                           #
# Date: 2026-02-07                                                                                                        #
#                                                                                                                        #
# Changelog:                                                                                                              #
#   1.0 - 2026-02-07 - Création initiale avec flags -r, -f, check "cat'able", header personnalisé.                        #
#   1.8 - 2026-02-07 - Correction : chemin complet absolu dans le header, gestion stricte de -f, récursif fonctionnel.     #
########################################################################################################################

# --- Variables globales ---
OUTPUT_FILE=""
RECURSIVE=false
EXCLUDE_DIRS=()
OPEN_WITH_KATE=false

# --- Gestion des arguments ---
while getopts "rf:x:" opt; do
    case "$opt" in
        r) RECURSIVE=true ;;
        f)
            OUTPUT_FILE="${OPTARG:-output.txt}"
            OPEN_WITH_KATE=true
            ;;
        x) IFS='|' read -ra EXCLUDE_DIRS <<< "$OPTARG" ;;
        \?)
            echo "Usage: $0 [-r] [-f [fichier]] [-x <dossiers_exclus>]"
            echo "  -r : Traite les fichiers de manière récursive."
            echo "  -f [fichier] : Redirige la sortie vers le fichier spécifié (défaut: output.txt)."
            echo "  -x <dossiers_exclus> : Exclut les dossiers spécifiés (séparés par |)."
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

# --- Fonction pour vérifier si un fichier est "cat'able" ---
is_catable() {
    local file="$1"
    file "$file" | grep -q "text"
}

# --- Fonction pour traiter un fichier ---
process_file() {
    local file="$1"
    local full_path
    full_path="$(realpath "$file")"
    echo "[INFO] Traitement du fichier : $full_path"
    if is_catable "$file"; then
        {
            echo "######################################################################"
            echo "# FULLPATH $full_path"
            echo "######################################################################"
            cat "$file"
            echo
        } >> "${OUTPUT_FILE:-/dev/stdout}"
    else
        echo "[WARNING] Le fichier $full_path n'est pas un fichier texte. Ignoré." >&2
    fi
}

# --- Fonction pour parcourir les fichiers (non récursif) ---
traverse_files() {
    local dir="."
    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(find "$dir" -maxdepth 1 -type f -print0)
}

# --- Fonction pour parcourir les fichiers de manière récursive ---
traverse_files_recursive() {
    local dir="."
    local exclude_args=()
    for exclude in "${EXCLUDE_DIRS[@]}"; do
        exclude_args+=(-not -path "*/$exclude/*")
    done
    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(find "$dir" -type f "${exclude_args[@]}" -print0)
}

# --- Point d'entrée ---
main() {
    echo "[INFO] Début de l'exécution du script $(basename "$0") (version 1.8)."
    if [[ "$RECURSIVE" = true ]]; then
        echo "[INFO] Mode récursif activé."
        traverse_files_recursive
    else
        echo "[INFO] Mode non récursif."
        traverse_files
    fi
    echo "[INFO] Fin de l'exécution. Résultats disponibles dans ${OUTPUT_FILE:-console}."
    if [[ "$OPEN_WITH_KATE" = true ]]; then
        kate "$OUTPUT_FILE" &
    fi
}

# --- Exécution ---
main
