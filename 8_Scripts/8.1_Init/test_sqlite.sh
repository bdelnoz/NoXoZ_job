#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/test_sqlite.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v3.0.0 – 2026-02-05
# Target usage: Test complet SQLite avec perf, perfbig, suppression totale et logging automatique
# Changelog:
#   v3.0.0 – Version finale avec log, messages explicites, compteurs, perfbig et suppression complète

# ----------------------------------------------------------------------
# 1. HELP
# ----------------------------------------------------------------------
function show_help() {
    echo "Usage: $0 [--simulate] [--exec] [--remove] [--perf] [--perfbig]"
    echo
    echo "Options:"
    echo "  --help, -h       Affiche cette aide"
    echo "  --simulate, -s   Dry-run complet"
    echo "  --exec, -e       Test standard (CV, chat, doc, embeddings)"
    echo "  --remove, -r     Supprime toutes les entrées test (standard + perf + perfbig)"
    echo "  --perf, -p       Test rapide perf (100 inserts)"
    echo "  --perfbig        Test perf massif (~10 000+ inserts)"
    exit 0
}

# ----------------------------------------------------------------------
# 2. PARSING ARGUMENTS
# ----------------------------------------------------------------------
SIMULATE=false
EXEC=false
REMOVE=false
PERF=false
PERFBIG=false
for arg in "$@"; do
    case $arg in
        --help|-h) show_help ;;
        --simulate|-s) SIMULATE=true ;;
        --exec|-e) EXEC=true ;;
        --remove|-r) REMOVE=true ;;
        --perf|-p) PERF=true ;;
        --perfbig) PERFBIG=true ;;
        *) echo "[ERROR] Option inconnue: $arg"; show_help ;;
    esac
done

# ----------------------------------------------------------------------
# 3. CHEMIN DB ABSOLU
# ----------------------------------------------------------------------
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
DB_PATH="${PROJECT_ROOT}/3_Data/Metadata/noxoz_metadata.db"

if [ ! -f "$DB_PATH" ]; then
    echo "[TestSQLite] ERREUR : DB non trouvée à $DB_PATH"
    exit 1
fi
echo "[TestSQLite] DB trouvée : $DB_PATH"

# ----------------------------------------------------------------------
# 4. LOGGING
# ----------------------------------------------------------------------
LOG_DIR="${PROJECT_ROOT}/4_Logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/log.test_sqlite.${TIMESTAMP}.v3.0.0.log"

# Redirection stdout/stderr vers le log
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[LogSQLite] Début du test SQLite, log enregistré dans : $LOG_FILE"

# ----------------------------------------------------------------------
# 5. SQL COMMANDES
# ----------------------------------------------------------------------
SQL_INSERT_TEST=$(cat <<'EOF'
INSERT INTO cv (filename, format, size, hash) VALUES ('test_cv.docx', 'docx', 12345, 'sha256:testhash');
INSERT INTO chat_history (platform, content) VALUES ('TestPlatform', 'Ceci est un test chat.');
INSERT INTO generated_docs (type, filename, format) VALUES ('lettre_motivation', 'lettre_test.docx', 'docx');
INSERT INTO embeddings_index (document_id, vector_id)
SELECT id, 'vector_test_001' FROM cv ORDER BY id DESC LIMIT 1;
EOF
)

SQL_SELECT_TEST=$(cat <<'EOF'
SELECT 'CV Table:' AS TableName, * FROM cv ORDER BY id DESC LIMIT 1;
SELECT 'Chat Table:' AS TableName, * FROM chat_history ORDER BY id DESC LIMIT 1;
SELECT 'Generated Docs Table:' AS TableName, * FROM generated_docs ORDER BY id DESC LIMIT 1;
SELECT 'Embeddings Table:' AS TableName, * FROM embeddings_index ORDER BY id DESC LIMIT 1;
EOF
)

SQL_REMOVE_TEST=$(cat <<'EOF'
DELETE FROM embeddings_index WHERE vector_id='vector_test_001';
DELETE FROM cv WHERE filename='test_cv.docx';
DELETE FROM chat_history WHERE platform='TestPlatform';
DELETE FROM generated_docs WHERE filename='lettre_test.docx';
DELETE FROM cv WHERE filename LIKE 'perf_cv%';
DELETE FROM cv WHERE filename LIKE 'perfbig_cv%';
EOF
)

SQL_PERF_TEST=$(cat <<'EOF'
BEGIN TRANSACTION;
INSERT INTO cv (filename, format, size, hash)
SELECT 'perf_cv'||i||'.docx', 'docx', 1234, 'sha256:perf'||i
FROM (SELECT 1 AS i UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10)
CROSS JOIN (SELECT 1 AS j UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10);
COMMIT;
SELECT COUNT(*) FROM cv WHERE filename LIKE 'perf_cv%';
EOF
)

SQL_PERFBIG_TEST=$(cat <<'EOF'
BEGIN TRANSACTION;
INSERT INTO cv (filename, format, size, hash)
SELECT 'perfbig_cv'||i||'.docx', 'docx', 1234, 'sha256:perfbig'||i
FROM (SELECT 1 AS i UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10)
CROSS JOIN (SELECT 1 AS j UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10)
CROSS JOIN (SELECT 1 AS k UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10);
COMMIT;
SELECT COUNT(*) FROM cv WHERE filename LIKE 'perfbig_cv%';
EOF
)

# ----------------------------------------------------------------------
# 6. EXECUTION
# ----------------------------------------------------------------------
# 6a. Test standard
if [ "$EXEC" = true ]; then
    echo "[TestSQLite] Début insertion test standard..."
    COUNT_BEFORE=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "$SQL_INSERT_TEST" | sqlite3 "$DB_PATH"
    COUNT_AFTER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "[TestSQLite] CV insérés : $((COUNT_AFTER - COUNT_BEFORE))"
    echo "[TestSQLite] Lecture dernières entrées..."
    echo "$SQL_SELECT_TEST" | sqlite3 "$DB_PATH"
    FK_CHECK=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM embeddings_index WHERE document_id NOT IN (SELECT id FROM cv);")
    echo "[TestSQLite] Vérification FK embeddings_index -> cv : $FK_CHECK anomalies"
    [ "$FK_CHECK" -eq 0 ] && echo "[TestSQLite] OK : tous les embeddings liés à un CV existant"
fi

# 6b. Test perf
if [ "$PERF" = true ]; then
    echo "[TestSQLite] Début test perf rapide (100 inserts)..."
    COUNT_BEFORE=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "$SQL_PERF_TEST" | sqlite3 "$DB_PATH"
    COUNT_AFTER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "[TestSQLite] CV insérés (perf) : $((COUNT_AFTER - COUNT_BEFORE))"
fi

# 6c. Test perfbig
if [ "$PERFBIG" = true ]; then
    echo "[TestSQLite] Début test perf BIG (~10 000 inserts)..."
    COUNT_BEFORE=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "$SQL_PERFBIG_TEST" | sqlite3 "$DB_PATH"
    COUNT_AFTER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cv;")
    echo "[TestSQLite] CV insérés (perf BIG) : $((COUNT_AFTER - COUNT_BEFORE))"
fi

# 6d. Suppression
if [ "$REMOVE" = true ]; then
    echo "[TestSQLite] Suppression de toutes les entrées tests standard + perf + perfbig..."
    echo "$SQL_REMOVE_TEST" | sqlite3 "$DB_PATH"
    echo "[TestSQLite] Suppression terminée, DB propre"
fi

# ----------------------------------------------------------------------
# 7. FIN
# ----------------------------------------------------------------------
echo "[TestSQLite] Test SQLite terminé."
echo "[LogSQLite] Log complet disponible ici : $LOG_FILE"
