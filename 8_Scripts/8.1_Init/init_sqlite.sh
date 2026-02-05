#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/init_sqlite.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.4.0 – 2026-02-05
# Target usage: Initialisation complète de SQLite pour NoXoZ_job avec lien absolu et permissions groupe nox
# Changelog:
#   v1.0.0 – Création initiale
#   v1.1.0 – Installation sqlite3
#   v1.2.0 – Permissions 770 et groupe nox
#   v1.3.0 – Lien symbolique absolu
#   v1.4.0 – Respect strict des règles de scripting et commentaires détaillés

# ----------------------------------------------------------------------
# FONCTION HELP
# ----------------------------------------------------------------------
function show_help() {
    echo "Usage: $0 [--simulate]"
    echo
    echo "Ce script initialise la base SQLite du projet NoXoZ_job."
    echo "Il crée le dossier de stockage bigfiles, la DB, les tables,"
    echo "et un lien symbolique absolu dans le projet."
    echo
    echo "Options:"
    echo "  --help, -h       Affiche cette aide et les options"
    echo "  --simulate, -s   Dry-run, affiche toutes les actions sans les exécuter"
    exit 0
}

# ----------------------------------------------------------------------
# PARSING DES ARGUMENTS
# ----------------------------------------------------------------------
SIMULATE=false
for arg in "$@"; do
    case $arg in
        --help|-h)
            show_help
            ;;
        --simulate|-s)
            SIMULATE=true
            ;;
        *)
            echo "[ERROR] Option inconnue: $arg"
            show_help
            ;;
    esac
done

# ----------------------------------------------------------------------
# 0. VARIABLES UTILISATEUR/GROUPE
# ----------------------------------------------------------------------
# On récupère l'utilisateur nox et son groupe nox
USER_NOX=$(id -un nox 2>/dev/null)
GROUP_NOX=$(getent group nox | cut -d: -f1)

if [ -z "$USER_NOX" ] || [ -z "$GROUP_NOX" ]; then
    echo "[ERROR] L'utilisateur ou le groupe 'nox' n'existe pas. Veuillez créer l'utilisateur et le groupe nox."
    exit 1
fi

echo "[InitSQLite] Utilisateur nox: $USER_NOX, Groupe nox: $GROUP_NOX"

# ----------------------------------------------------------------------
# 0a. Vérification et installation de sqlite3
# ----------------------------------------------------------------------
if ! command -v sqlite3 &> /dev/null; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] sudo apt update && sudo apt install -y sqlite3"
    else
        echo "[InitSQLite] SQLite3 non trouvé, installation en cours..."
        sudo apt update
        sudo apt install -y sqlite3
        echo "[InitSQLite] SQLite3 installé."
    fi
else
    echo "[InitSQLite] SQLite3 déjà installé."
fi

# ----------------------------------------------------------------------
# 1. CHEMINS ABSOLUS ET STRUCTURE
# ----------------------------------------------------------------------
# Répertoire racine projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
# Dossier SQLite sur bigfiles
BIGFILES_SQLITE_DIR="/mnt/data1_100g/agent_llm_local/sqlite"
# Nom du fichier DB
DB_FILE="noxoz_metadata.db"
# Chemin réel DB
DB_PATH_REAL="${BIGFILES_SQLITE_DIR}/${DB_FILE}"
# Dossier Metadata projet
PROJECT_META_DIR="${PROJECT_ROOT}/3_Data/Metadata"
# Chemin du lien symbolique absolu
PROJECT_META_LINK="${PROJECT_META_DIR}/${DB_FILE}"

echo "[InitSQLite] Chemin réel DB: $DB_PATH_REAL"
echo "[InitSQLite] Lien symbolique projet (absolu): $PROJECT_META_LINK"

# ----------------------------------------------------------------------
# 2. CREATION DU DOSSIER BIGFILES/SQLITE
# ----------------------------------------------------------------------
if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] mkdir -p $BIGFILES_SQLITE_DIR"
else
    mkdir -p "$BIGFILES_SQLITE_DIR"
    sudo chown "$USER_NOX:$GROUP_NOX" "$BIGFILES_SQLITE_DIR"
    sudo chmod 770 "$BIGFILES_SQLITE_DIR"
    echo "[InitSQLite] Dossier bigfiles créé et permissions appliquées: $BIGFILES_SQLITE_DIR"
fi

# ----------------------------------------------------------------------
# 3. CREATION DE LA DB SQLITE SI INEXISTANTE
# ----------------------------------------------------------------------
if [ ! -f "$DB_PATH_REAL" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] touch $DB_PATH_REAL"
    else
        touch "$DB_PATH_REAL"
        sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
        sudo chmod 770 "$DB_PATH_REAL"
        echo "[InitSQLite] DB SQLite créée et permissions appliquées: $DB_PATH_REAL"
    fi
else
    echo "[InitSQLite] DB existe déjà: $DB_PATH_REAL"
    if [ "$SIMULATE" = false ]; then
        sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
        sudo chmod 770 "$DB_PATH_REAL"
        echo "[InitSQLite] Permissions ajustées pour la DB existante"
    fi
fi

# ----------------------------------------------------------------------
# 4. CREATION DU DOSSIER METADATA PROJET
# ----------------------------------------------------------------------
if [ ! -d "$PROJECT_META_DIR" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] mkdir -p $PROJECT_META_DIR"
    else
        mkdir -p "$PROJECT_META_DIR"
        sudo chown "$USER_NOX:$GROUP_NOX" "$PROJECT_META_DIR"
        sudo chmod 770 "$PROJECT_META_DIR"
        echo "[InitSQLite] Dossier Metadata projet créé et permissions appliquées: $PROJECT_META_DIR"
    fi
fi

# ----------------------------------------------------------------------
# 5. CREATION DU LIEN SYMBOLIQUE ABSOLU
# ----------------------------------------------------------------------
if [ ! -L "$PROJECT_META_LINK" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] ln -s $DB_PATH_REAL $PROJECT_META_LINK"
    else
        ln -s "$DB_PATH_REAL" "$PROJECT_META_LINK"
        echo "[InitSQLite] Lien symbolique absolu créé: $PROJECT_META_LINK -> $DB_PATH_REAL"
    fi
else
    echo "[InitSQLite] Lien symbolique déjà existant: $PROJECT_META_LINK"
fi

# ----------------------------------------------------------------------
# 6. INITIALISATION DES TABLES SQLITE
# ----------------------------------------------------------------------
SQL_COMMANDS=$(cat <<'EOF'
CREATE TABLE IF NOT EXISTS cv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    format TEXT,
    size INTEGER,
    hash TEXT,
    ingestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT,
    content TEXT,
    ingestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS generated_docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    filename TEXT,
    format TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS embeddings_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    vector_id TEXT,
    FOREIGN KEY(document_id) REFERENCES cv(id)
);
EOF
)

if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] sqlite3 $DB_PATH_REAL <<EOF"
    echo "$SQL_COMMANDS"
    echo "EOF"
else
    echo "$SQL_COMMANDS" | sqlite3 "$DB_PATH_REAL"
    echo "[InitSQLite] Tables SQLite créées ou déjà existantes"
fi

# ----------------------------------------------------------------------
# 7. PERMISSIONS FINALES
# ----------------------------------------------------------------------
if [ "$SIMULATE" = false ]; then
    sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
    sudo chmod 770 "$DB_PATH_REAL"
    echo "[InitSQLite] Permissions finales appliquées (770) sur DB"
fi

# ----------------------------------------------------------------------
# FIN
# ----------------------------------------------------------------------
echo "[InitSQLite] Initialisation SQLite terminée."
