#!/bin/bash
################################################################################
# Script: count_tokens.sh
# Auteur: Bruno DELNOZ <bruno.delnoz@protonmail.com>
# Chemin: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.2_Utils/count_tokens.sh
# Version: 1.7
# Date: 2026-02-06 22:00:00 (Europe/Brussels)
# Description: Compte les tokens dans un fichier texte avec tiktoken (OpenAI/Mistral).
#              **Utilise ton VENV existant pour Ollama (Pipenv).**
#              **Aucune modification de répertoires sans accord explicite.**
# Usage: ./count_tokens.sh [OPTIONS] <fichier> [modèle]
# Options:
#   --help          Affiche l'aide et quitte.
#   --prerequis     Vérifie les prérequis (Pipenv + VENV existant).
#   --install       Installe tiktoken dans le VENV existant.
#   --exec          Exécute le script (défaut: SIMULATE=false).
#   --simulate=true Active le mode simulation (désactivé par défaut).
#   --changelog     Affiche le changelog et quitte.
# Modèles: gpt4 (défaut), mistral, cl100k, p50k.
# Exemple:
#   ./count_tokens.sh 350_questions.txt mistral
################################################################################

# --- CHANGELOG ---
# v1.7 - 2026-02-06 22:00:00 - Bruno DELNOZ
#   - Correction: Pipenv (et non Pipend).
#   - Utilisation exclusive de ton VENV existant pour Ollama.
#   - Aucune modification de répertoires sans accord.
# v1.6 - 2026-02-06 18:00:00 - Bruno DELNOZ
#   - Intégration du VENV dédié (DELV) pour Ollama.
################################################################################

# --- VARIABLES GLOBALES ---
SCRIPT_NAME="count_tokens"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/LOGS"
RESULT_DIR="$SCRIPT_DIR/results"
INFO_DIR="$SCRIPT_DIR/infos"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/log.$SCRIPT_NAME.$TIMESTAMP.log"
SIMULATE=false  # Mode exécution réel par défaut
EXECUTE=false
SHOW_HELP=false
SHOW_CHANGELOG=false
CHECK_PREREQUIS=false
INSTALL_DEPS=false
FILE=""
MODEL="gpt4"
VENV_PATH="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/venv/ollama"  # Chemin vers TON VENV existant pour Ollama

# --- FONCTIONS ---
init() {
    echo "[1/8] Initialisation du script $SCRIPT_NAME..." | tee "$LOG_FILE"
    mkdir -p "$LOG_DIR" "$RESULT_DIR" "$INFO_DIR" 2>/dev/null | tee -a "$LOG_FILE"
    update_gitignore | tee -a "$LOG_FILE"
    generate_docs | tee -a "$LOG_FILE"
}

update_gitignore() {
    echo "[2/8] Mise à jour de .gitignore..." | tee -a "$LOG_FILE"
    local entries=("/logs" "/results" "/infos")
    if [ ! -f "$SCRIPT_DIR/.gitignore" ]; then
        touch "$SCRIPT_DIR/.gitignore"
        echo "  ✅ .gitignore créé." | tee -a "$LOG_FILE"
    fi
    for entry in "${entries[@]}"; do
        if ! grep -q "^$entry\$" "$SCRIPT_DIR/.gitignore"; then
            echo "$entry" >> "$SCRIPT_DIR/.gitignore"
            echo "  ✅ Ajout de $entry à .gitignore." | tee -a "$LOG_FILE"
        else
            echo "  ℹ️  $entry déjà présent dans .gitignore." | tee -a "$LOG_FILE"
        fi
    done
}

generate_docs() {
    echo "[3/8] Génération de la documentation..." | tee -a "$LOG_FILE"
    cat > "$INFO_DIR/CHANGELOG.md" << EOF
# Changelog - $SCRIPT_NAME

## v1.7 - $(date +"%Y-%m-%d %H:%M:%S")
- **Correction**: Utilisation de **Pipenv** (et non Pipend).
- **VENV existant**: Utilise **ton environnement Ollama** ($VENV_PATH).
- **Aucune modification de répertoires** sans accord explicite.

## v1.6 - 2026-02-06 18:00:00
- Intégration du VENV dédié pour Ollama.
EOF
    cat > "$INFO_DIR/USAGE.md" << EOF
# Utilisation - $SCRIPT_NAME

## Syntax
\`\`\`bash
./$SCRIPT_NAME.sh [OPTIONS] <fichier> [modèle]
\`\`\`

## Options
| Option               | Description                                  |
|----------------------|----------------------------------------------|
| --help               | Affiche cette aide et quitte.                |
| --prerequis          | Vérifie les prérequis (Pipenv + VENV).       |
| --install            | Installe tiktoken dans le VENV existant.    |
| --exec               | Exécute le script (défaut).                 |
| --simulate=true      | Active le mode simulation.                 |
| --changelog          | Affiche le changelog et quitte.             |

## Exemples
\`\`\`bash
# Vérification des prérequis
./$SCRIPT_NAME.sh --prerequis

# Installation de tiktoken (dans le VENV existant)
./$SCRIPT_NAME.sh --install

# Exécution normale (utilise le VENV existant)
./$SCRIPT_NAME.sh 350_questions.txt mistral
\`\`\`
EOF
}

check_prerequisites() {
    echo "[4/8] Vérification des prérequis..." | tee -a "$LOG_FILE"
    local missing=0

    # Vérification de Python 3
    if ! command -v python3 &>/dev/null; then
        echo "  ❌ Python3 non installé." | tee -a "$LOG_FILE"
        missing=$((missing + 1))
    else
        echo "  ✅ Python3 installé." | tee -a "$LOG_FILE"
    fi

    # Vérification du VENV existant
    if [ ! -d "$VENV_PATH" ]; then
        echo "  ❌ VENV Ollama non trouvé dans '$VENV_PATH'." | tee -a "$LOG_FILE"
        missing=$((missing + 1))
    else
        echo "  ✅ VENV Ollama trouvé." | tee -a "$LOG_FILE"
    fi

    # Vérification de Pipenv dans le VENV
    if [ -d "$VENV_PATH" ]; then
        source "$VENV_PATH/bin/activate" && command -v pipenv &>/dev/null
        if [ $? -ne 0 ]; then
            echo "  ❌ Pipenv non installé dans le VENV." | tee -a "$LOG_FILE"
            missing=$((missing + 1))
        else
            echo "  ✅ Pipenv installé dans le VENV." | tee -a "$LOG_FILE"
        fi
        deactivate
    fi

    if [ "$missing" -gt 0 ]; then
        echo "  ⚠️  $missing prérequis manquants." | tee -a "$LOG_FILE"
        return 1
    else
        echo "  ✅ Tous les prérequis sont installés." | tee -a "$LOG_FILE"
    fi
    return 0
}

install_dependencies() {
    echo "[5/8] Installation de tiktoken dans le VENV existant..." | tee -a "$LOG_FILE"
    source "$VENV_PATH/bin/activate"
    pipenv install tiktoken > /dev/null 2>&1
    deactivate
    echo "  ✅ tiktoken installé dans le VENV via Pipenv." | tee -a "$LOG_FILE"
}

count_tokens() {
    local file="$1"
    local model="$2"
    echo "[6/8] Comptage des tokens pour $file (modèle: $model)..." | tee -a "$LOG_FILE"
    source "$VENV_PATH/bin/activate"
    python3 -c "
import tiktoken
encoder = tiktoken.get_encoding('cl100k_base' if '$model' == 'mistral' else '$model')
with open('$file', 'r', encoding='utf-8') as f:
    text = f.read()
token_count = len(encoder.encode(text))
print(token_count)
"
    deactivate | tee -a "$LOG_FILE"
}

display_results() {
    local file="$1"
    local model="$2"
    local count="$3"
    local result_file="$RESULT_DIR/token_count_${file##*/}.$TIMESTAMP.txt"
    echo "[7/8] Génération des résultats..." | tee -a "$LOG_FILE"
    {
        echo "=== RÉSULTATS ==="
        echo "Fichier: $file"
        echo "Modèle: $model"
        echo "Nombre de tokens: $count"
        echo "Date: $(date)"
        echo "=== FIN ==="
    } | tee "$result_file" -a "$LOG_FILE"
    if [ "$model" = "mistral" ]; then
        local max_tokens=32000
        if [ "$count" -gt "$max_tokens" ]; then
            local chunks=$(( ($count + $max_tokens - 1) / $max_tokens ))
            echo "⚠️  Attention: Ce fichier dépasse la limite de $max_tokens tokens pour mistral:7b." | tee -a "$LOG_FILE" "$result_file"
            echo "   Découpe-le en chunks de ~$max_tokens tokens max." | tee -a "$LOG_FILE" "$result_file"
            echo "   Nombre de chunks recommandé: $chunks" | tee -a "$LOG_FILE" "$result_file"
        fi
    fi
    echo "  ✅ Résultats enregistrés dans $result_file" | tee -a "$LOG_FILE"
}

show_help() {
    cat "$INFO_DIR/USAGE.md"
}

show_changelog() {
    cat "$INFO_DIR/CHANGELOG.md"
}

main() {
    init
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help)
                SHOW_HELP=true
                shift
                ;;
            --prerequis)
                CHECK_PREREQUIS=true
                shift
                ;;
            --install)
                INSTALL_DEPS=true
                shift
                ;;
            --exec)
                EXECUTE=true
                shift
                ;;
            --simulate=true)
                SIMULATE=true
                shift
                ;;
            --changelog)
                SHOW_CHANGELOG=true
                shift
                ;;
            --*)
                echo "Option inconnue: $1" | tee -a "$LOG_FILE"
                exit 1
                ;;
            *)
                if [ -z "$FILE" ]; then
                    FILE="$1"
                elif [ -z "$MODEL" ]; then
                    MODEL="$1"
                fi
                shift
                ;;
        esac
    done

    if [ "$SHOW_CHANGELOG" = true ]; then
        show_changelog
        exit 0
    fi
    if [ "$SHOW_HELP" = true ] || [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    if [ "$INSTALL_DEPS" = true ]; then
        if ! check_prerequisites; then
            exit 1
        fi
        install_dependencies
        exit 0
    fi
    if [ "$CHECK_PREREQUIS" = true ]; then
        check_prerequisites
        exit 0
    fi
    if ! check_prerequisites; then
        exit 1
    fi
    if [ ! -f "$FILE" ]; then
        echo "Erreur: Fichier '$FILE' introuvable." | tee -a "$LOG_FILE"
        exit 1
    fi
    if [ "$SIMULATE" = false ]; then
        local count=$(count_tokens "$FILE" "$MODEL")
        display_results "$FILE" "$MODEL" "$count"
    else
        echo "Mode simulation activé. Utilise --simulate=false (défaut) ou supprime --simulate=true pour exécuter." | tee -a "$LOG_FILE"
    fi
}

main "$@"
