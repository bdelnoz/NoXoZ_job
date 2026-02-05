#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/init_sqlite.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.2.0 – 2026-02-05
# Target usage: Initialisation complète de SQLite pour NoXoZ_job avec contrôle groupe et permissions
# execution 10.0
# Changelog:
#   v1.0.0 – Création initiale
#   v1.1.0 – Installation sqlite3
#   v1.2.0 – Gestion des utilisateurs/groupe et permissions 770

# --- HELP / Usage ---
function show_help() {
    echo "Usage: $0 [--simulate]"
    echo
    echo "Options:"
    echo "  --help, -h       Affiche cette aide"
    echo "  --simulate, -s   Dry-run, affiche les actions sans les exécuter"
    echo
    echo "Ce script:"
    echo "  - Installe sqlite3 si absent"
    echo "  - Crée le dossier pour SQLite dans /mnt/data1_100g/agent_llm_local/sqlite"
    echo "  - Crée la base noxoz_metadata.db si inexistante"
    echo "  - Crée le lien symbolique dans 3_Data/Metadata/"
    echo "  - Initialise les tables SQLite pour CV, chat, documents générés, embeddings"
    echo "  - Assigne propriétaire et groupe 'nox', permissions 770"
    exit 0
}

# --- Arguments ---
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

# --- 0. Variables utilisateurs / groupe ---
USER_NOX=$(id -un nox 2>/dev/null)
GROUP_NOX=$(getent group nox | cut -d: -f1)

if [ -z "$USER_NOX" ] || [ -z "$GROUP_NOX" ]; then
    echo "[ERROR] L'utilisateur ou le groupe 'nox' n'existe pas. Veuillez créer l'utilisateur et le groupe nox."
    exit 1
fi
echo "[InitSQLite] Utilisateur nox: $USER_NOX, Groupe nox: $GROUP_NOX"

# --- 0a. Vérification et installation SQLite3 ---
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

# --- 1. Chemins ---
BIGFILES_SQLITE_DIR="/mnt/data1_100g/agent_llm_local/sqlite"
PROJECT_META_LINK="./3_Data/Metadata/noxoz_metadata.db"
DB_FILE="noxoz_metadata.db"
DB_PATH_REAL="${BIGFILES_SQLITE_DIR}/${DB_FILE}"

echo "[InitSQLite] Chemin réel DB: $DB_PATH_REAL"
echo "[InitSQLite] Lien symbolique projet: $PROJECT_META_LINK"

# --- 2. Création du dossier bigfiles/sqlite ---
if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] mkdir -p $BIGFILES_SQLITE_DIR"
else
    mkdir -p "$BIGFILES_SQLITE_DIR"
    sudo chown "$USER_NOX:$GROUP_NOX" "$BIGFILES_SQLITE_DIR"
    sudo chmod 770 "$BIGFILES_SQLITE_DIR"
    echo "[InitSQLite] Dossier créé et permissions appliquées: $BIGFILES_SQLITE_DIR"
fi

# --- 3. Création de la DB si inexistante ---
if [ ! -f "$DB_PATH_REAL" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] touch $DB_PATH_REAL"
    else
        touch "$DB_PATH_REAL"
        sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
        sudo chmod 770 "$DB_PATH_REAL"
        echo "[InitSQLite] DB créée et permissions appliquées: $DB_PATH_REAL"
    fi
else
    echo "[InitSQLite] DB existe déjà: $DB_PATH_REAL"
    if [ "$SIMULATE" = false ]; then
        sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
        sudo chmod 770 "$DB_PATH_REAL"
        echo "[InitSQLite] Permissions ajustées pour la DB existante"
    fi
fi

# --- 4. Création du lien symbolique ---
PROJECT_META_DIR=$(dirname "$PROJECT_META_LINK")
if [ ! -d "$PROJECT_META_DIR" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] mkdir -p $PROJECT_META_DIR"
    else
        mkdir -p "$PROJECT_META_DIR"
        sudo chown "$USER_NOX:$GROUP_NOX" "$PROJECT_META_DIR"
        sudo chmod 770 "$PROJECT_META_DIR"
        echo "[InitSQLite] Dossier projet Metadata créé et permissions appliquées: $PROJECT_META_DIR"
    fi
fi

if [ ! -L "$PROJECT_META_LINK" ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] ln -s $DB_PATH_REAL $PROJECT_META_LINK"
    else
        ln -s "$DB_PATH_REAL" "$PROJECT_META_LINK"
        echo "[InitSQLite] Lien symbolique créé: $PROJECT_META_LINK -> $DB_PATH_REAL"
    fi
else
    echo "[InitSQLite] Lien symbolique déjà existant: $PROJECT_META_LINK"
fi

# --- 5. Initialisation des tables SQLite ---
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

# --- 6. Vérification finale permissions ---
if [ "$SIMULATE" = false ]; then
    sudo chown "$USER_NOX:$GROUP_NOX" "$DB_PATH_REAL"
    sudo chmod 770 "$DB_PATH_REAL"
    echo "[InitSQLite] Permissions finales appliquées (770) sur DB"
fi

echo "[InitSQLite] Initialisation SQLite terminée."
