#!/bin/bash

# =============================================================================
# Script: init_project.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Chemin: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/scripts/init_project.sh
# Version: 1.0
# Date: 2026-02-04
# Description: Initialise le projet NoXoZ_job avec une structure hiérarchisée,
#              des fichiers .docx pour la documentation, et des logs automatisés.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Variables globales
# -----------------------------------------------------------------------------
BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
LOG_DIR="$BASE_DIR/logs/INIT"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/init_project_$TIMESTAMP.log"
SIMULATE="${SIMULATE:-false}"  # Mode simulation désactivé par défaut

# -----------------------------------------------------------------------------
# 2. Fonction: Afficher l'aide
# -----------------------------------------------------------------------------
display_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --help      Affiche cette aide"
    echo "  --exec      Exécute l'initialisation du projet (défaut)"
    echo "  --simulate  Mode simulation (affiche les actions sans les exécuter)"
    echo "Exemple:"
    echo "  $0 --exec"
}

# -----------------------------------------------------------------------------
# 3. Fonction: Créer un répertoire avec vérification
# -----------------------------------------------------------------------------
create_directory() {
    local dir_path="$1"
    local step="$2"
    echo "[Étape $step] Création du répertoire: $dir_path"
    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Répertoire: $dir_path" >> "$LOG_FILE"
    else
        if [ ! -d "$dir_path" ]; then
            mkdir -p "$dir_path"
            echo "[SUCCESS] Répertoire créé: $dir_path" >> "$LOG_FILE"
        else
            echo "[INFO] Répertoire existant: $dir_path" >> "$LOG_FILE"
        fi
    fi
}

# -----------------------------------------------------------------------------
# 4. Fonction: Créer un fichier .docx vide
# -----------------------------------------------------------------------------
create_docx() {
    local file_path="$1"
    local step="$2"
    echo "[Étape $step] Création du fichier .docx: $file_path"
    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Fichier .docx: $file_path" >> "$LOG_FILE"
    else
        if [ ! -f "$file_path" ]; then
            python3 - <<END > /dev/null 2>&1
from docx import Document
doc = Document()
doc.save("$file_path")
END
            echo "[SUCCESS] Fichier .docx créé: $file_path" >> "$LOG_FILE"
        else
            echo "[INFO] Fichier .docx existant: $file_path" >> "$LOG_FILE"
        fi
    fi
}

# -----------------------------------------------------------------------------
# 5. Fonction: Créer un fichier vide (autres formats)
# -----------------------------------------------------------------------------
create_file() {
    local file_path="$1"
    local step="$2"
    echo "[Étape $step] Création du fichier: $file_path"
    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Fichier: $file_path" >> "$LOG_FILE"
    else
        if [ ! -f "$file_path" ]; then
            touch "$file_path"
            echo "[SUCCESS] Fichier créé: $file_path" >> "$LOG_FILE"
        else
            echo "[INFO] Fichier existant: $file_path" >> "$LOG_FILE"
        fi
    fi
}

# -----------------------------------------------------------------------------
# 6. Fonction: Initialiser les répertoires de logs
# -----------------------------------------------------------------------------
init_logs() {
    echo "[Étape 6] Initialisation des répertoires de logs"
    create_directory "$BASE_DIR/logs" "6.1"
    create_directory "$LOG_DIR" "6.2"
}

# -----------------------------------------------------------------------------
# 7. Fonction: Mettre à jour .gitignore
# -----------------------------------------------------------------------------
update_gitignore() {
    echo "[Étape 7] Mise à jour de .gitignore"
    local gitignore_path="$BASE_DIR/.gitignore"
    local entries=("# Logs
logs/

# Outputs
outputs/

# Results
results/

# Infos
infos/

# Fichiers temporaires
*.tmp
*.log
*.bak
")

    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Mise à jour de $gitignore_path" >> "$LOG_FILE"
    else
        if [ ! -f "$gitignore_path" ]; then
            echo "$entries" > "$gitignore_path"
            echo "[SUCCESS] Fichier .gitignore créé" >> "$LOG_FILE"
        else
            if ! grep -q "logs/" "$gitignore_path"; then
                echo -e "\n$entries" >> "$gitignore_path"
                echo "[SUCCESS] Entrées ajoutées à .gitignore" >> "$LOG_FILE"
            else
                echo "[INFO] .gitignore déjà à jour" >> "$LOG_FILE"
            fi
        fi
    fi
}

# -----------------------------------------------------------------------------
# 8. Fonction: Créer la structure hiérarchisée du projet
# -----------------------------------------------------------------------------
create_project_structure() {
    echo "[Étape 8] Création de la structure hiérarchisée du projet"

    # 8.1 Répertoires principaux (numérotation 1.N)
    local main_dirs=(
        "$BASE_DIR/1_Documentation"
        "$BASE_DIR/2_Sources"
        "$BASE_DIR/3_Data"
        "$BASE_DIR/4_Logs"
        "$BASE_DIR/5_Outputs"
        "$BASE_DIR/6_Results"
        "$BASE_DIR/7_Infos"
        "$BASE_DIR/8_Scripts"
        "$BASE_DIR/9_Templates"
    )

    # 8.2 Sous-répertoires (numérotation 1.N.M)
    local sub_dirs=(
        "$BASE_DIR/1_Documentation/1.1_General"
        "$BASE_DIR/1_Documentation/1.2_Technical"
        "$BASE_DIR/2_Sources/2.1_Python"
        "$BASE_DIR/2_Sources/2.2_Bash"
        "$BASE_DIR/3_Data/3.1_Vectors"
        "$BASE_DIR/3_Data/3.2_Metadata"
        "$BASE_DIR/5_Outputs/5.1_DOCX"
        "$BASE_DIR/5_Outputs/5.2_PDF"
        "$BASE_DIR/6_Results/6.1_Bugs"
        "$BASE_DIR/6_Results/6.2_Innovations"
        "$BASE_DIR/8_Scripts/8.1_Init"
        "$BASE_DIR/8_Scripts/8.2_Utils"
    )

    # 8.3 Fichiers .docx (numérotation 1.N.M.P)
    local docx_files=(
        "$BASE_DIR/1_Documentation/1.1_General/WHY.docx"
        "$BASE_DIR/1_Documentation/1.1_General/INSTALL.docx"
        "$BASE_DIR/1_Documentation/1.2_Technical/ARCHITECTURE.docx"
        "$BASE_DIR/1_Documentation/1.2_Technical/API_SPECIFICATIONS.docx"
    )

    # 8.4 Fichiers divers (numérotation 1.N.M.P)
    local other_files=(
        "$BASE_DIR/2_Sources/2.1_Python/main_agent.py"
        "$BASE_DIR/2_Sources/2.2_Bash/create_structure.sh"
        "$BASE_DIR/docker-compose.yml"
        "$BASE_DIR/requirements.txt"
        "$BASE_DIR/.env"
    )

    # Création des répertoires principaux (1.N)
    for i in {1..9}; do
        create_directory "${main_dirs[$((i-1))]}" "8.1.$i"
    done

    # Création des sous-répertoires (1.N.M)
    for i in {1..12}; do
        create_directory "${sub_dirs[$((i-1))]}" "8.2.$i"
    done

    # Création des fichiers .docx (1.N.M.P)
    for i in {1..4}; do
        create_docx "${docx_files[$((i-1))]}" "8.3.$i"
    done

    # Création des autres fichiers (1.N.M.P)
    for i in {1..5}; do
        create_file "${other_files[$((i-1))]}" "8.4.$i"
    done
}

# -----------------------------------------------------------------------------
# 9. Fonction: Initialiser le fichier de mémoire pérenne
# -----------------------------------------------------------------------------
init_permanent_memory() {
    echo "[Étape 9] Initialisation du fichier de mémoire pérenne"
    local memory_file="$BASE_DIR/7_Infos/PERMANENT_MEMORY.md"
    local content="# Mémoire Pérenne NoXoZ_job\n\n"
    content+="## 1. Sujets Abordés (Hiérarchie Numérotée)\n"
    content+="### 1.1. Projet NoXoZ_job\n"
    content+="#### 1.1.1. Initialisation du projet (2026-02-04)\n"
    content+="#### 1.1.2. Structure hiérarchisée des répertoires\n"
    content+="### 1.2. Innovations\n"
    content+="#### 1.2.1. Format .docx pour la documentation\n"
    content+="#### 1.2.2. Numérotation hiérarchique (1.N.M.P)\n"
    content+="### 1.3. Bugs Identifiés\n"
    content+="#### 1.3.1. Aucun bug signalé à ce jour\n"
    content+="\n---\n"
    content+="## 2. Règles Personnalisées\n"
    content+="### 2.1. Commande *« chat terminé »*\n"
    content+="- **Seuil**: 30 000 tokens → Fichier Markdown téléchargeable\n"
    content+="- **Seuil**: ≤ 29 000 tokens → Affichage direct dans le chat\n"
    content+="### 2.2. Format des Documents\n"
    content+="- Privilégier **.docx** pour les présentations structurées\n"
    content+="- Réserver **.md** aux fichiers techniques (ex: README.md)\n"
    content+="\n---\n"
    content+="## 3. Collaboratifs pour Bugs & Innovations\n"
    content+="- **Bugs**: Section dédiée avec rapport automatisé\n"
    content+="- **Innovations**: Section dédiée pour les idées d'amélioration\n"

    if [ "$SIMULATE" = "true" ]; then
        echo "[SIMULATION] Création de $memory_file" >> "$LOG_FILE"
    else
        echo -e "$content" > "$memory_file"
        echo "[SUCCESS] Fichier de mémoire pérenne initialisé: $memory_file" >> "$LOG_FILE"
    fi
}

# -----------------------------------------------------------------------------
# 10. Fonction: Exécuter l'initialisation complète
# -----------------------------------------------------------------------------
execute() {
    init_logs
    update_gitignore
    create_project_structure
    init_permanent_memory
    echo "[SUCCESS] Projet NoXoZ_job initialisé avec succès." >> "$LOG_FILE"
    echo "Consultez $LOG_FILE pour les détails."
}

# -----------------------------------------------------------------------------
# 11. Traitement des arguments
# -----------------------------------------------------------------------------
case "$1" in
    --help)
        display_help
        ;;
    --simulate)
        SIMULATE="true"
        execute
        ;;
    --exec|*)
        SIMULATE="false"
        execute
        ;;
esac
