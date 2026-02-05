#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/test_sqlite.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v2.0.0 – 2026-02-05
# Target usage: Test complet SQLite NoXoZ_job avec FK, embeddings et perf
# Changelog:
#   v2.0.0 – Création ultime avec --exec, --simulate, --remove, --perf, test embeddings_index et relation FK

DB_PATH="./3_Data/Metadata/noxoz_metadata.db"

# --- Arguments ---
SIMULATE=false
REMOVE=false
EXEC=false
PERF=false
for arg in "$@"; do
    case $arg in
        --help|-h)
            echo "Usage: $0 [--simulate] [--exec] [--remove] [--perf]"
            echo
            echo "Options:"
            echo "  --help, -h       Affiche cette aide"
            echo "  --simulate, -s   Dry-run, affiche les actions sans exécution"
            echo "  --exec, -e       Exécute le test complet"
            echo "  --remove, -r     Supprime les entrées test après exécution"
            echo "  --perf, -p       Test rapide de performance (insert/lecture massifs)"
            exit 0
            ;;
        --simulate|-s)
            SIMULATE=true
            ;;
        --exec|-e)
            EXEC=true
            ;;
        --remove|-r)
            REMOVE=true
            ;;
        --perf|-p)
            PERF=true
            ;;
        *)
            echo "[ERROR] Option inconnue: $arg"
            exit 1
            ;;
    esac
done

# --- Vérification DB ---
if [ ! -f "$DB_PATH" ]; then
    echo "[TestSQLite] ERREUR: DB non trouvée à $DB_PATH"
    exit 1
fi
echo "[TestSQLite] DB trouvée : $DB_PATH"

if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] Mode dry-run activé, aucune action réelle"
fi

# --- SQL Tests ---
SQL_INSERT_TEST=$(cat <<'EOF'
-- Insert test CV
INSERT INTO cv (filename, format, size, hash) VALUES ('test_cv.docx', 'docx', 12345, 'sha256:testhash');
-- Insert test Chat
INSERT INTO chat_history (platform, content) VALUES ('TestPlatform', 'Ceci est un test chat.');
-- Insert test Doc généré
INSERT INTO generated_docs (type, filename, format) VALUES ('lettre_motivation', 'lettre_test.docx', 'docx');
-- Insert test Embeddings (FK vers cv.id = dernier insert)
INSERT INTO embeddings_index (document_id, vector_id)
    SELECT id, 'vector_test_001' FROM cv ORDER BY id DESC LIMIT 1;
EOF
)

SQL_SELECT_TEST=$(cat <<'EOF'
-- Lecture dernières entrées
SELECT 'CV Table:' AS TableName, * FROM cv ORDER BY id DESC LIMIT 1;
SELECT 'Chat Table:' AS TableName, * FROM chat_history ORDER BY id DESC LIMIT 1;
SELECT 'Generated Docs Table:' AS TableName, * FROM generated_docs ORDER BY id DESC LIMIT 1;
SELECT 'Embeddings Table:' AS TableName, * FROM embeddings_index ORDER BY id DESC LIMIT 1;
EOF
)

SQL_REMOVE_TEST=$(cat <<'EOF'
-- Supprime les entrées de test
DELETE FROM embeddings_index WHERE vector_id='vector_test_001';
DELETE FROM cv WHERE filename='test_cv.docx';
DELETE FROM chat_history WHERE platform='TestPlatform';
DELETE FROM generated_docs WHERE filename='lettre_test.docx';
EOF
)

SQL_PERF_TEST=$(cat <<'EOF'
-- Test rapide perf : 100 inserts dans CV et lecture
BEGIN TRANSACTION;
INSERT INTO cv (filename, format, size, hash) SELECT 'perf_cv'||i||'.docx', 'docx', 1234, 'sha256:perf'||i FROM (SELECT 1 AS i UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) CROSS JOIN (SELECT 1 AS j UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10);
COMMIT;
SELECT COUNT(*) FROM cv WHERE filename LIKE 'perf_cv%';
EOF
)

# --- Execution ---
if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] sqlite3 $DB_PATH <<EOF"
    echo "$SQL_INSERT_TEST"
    echo "$SQL_SELECT_TEST"
    if [ "$REMOVE" = true ]; then
        echo "[SIMULATE] Suppression des entrées test"
        echo "$SQL_REMOVE_TEST"
    fi
    if [ "$PERF" = true ]; then
        echo "[SIMULATE] Test perf"
        echo "$SQL_PERF_TEST"
    fi
    echo "EOF"
fi

if [ "$EXEC" = true ] && [ "$SIMULATE" = false ]; then
    echo "[TestSQLite] Insertion des données test..."
    echo "$SQL_INSERT_TEST" | sqlite3 "$DB_PATH"

    echo "[TestSQLite] Lecture des dernières entrées..."
    echo "$SQL_SELECT_TEST" | sqlite3 "$DB_PATH"

    # Vérification FK : chaque embeddings doit pointer sur un cv existant
    echo "[TestSQLite] Vérification FK embeddings_index -> cv..."
    FK_CHECK=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM embeddings_index WHERE document_id NOT IN (SELECT id FROM cv);")
    if [ "$FK_CHECK" -eq 0 ]; then
        echo "[TestSQLite] OK : Tous les embeddings ont une CV existante."
    else
        echo "[TestSQLite] ERREUR : $FK_CHECK embeddings pointent sur des CV inexistantes !"
    fi

    # Test perf si demandé
    if [ "$PERF" = true ]; then
        echo "[TestSQLite] Test rapide de performance : inserts massifs"
        echo "$SQL_PERF_TEST" | sqlite3 "$DB_PATH"
    fi

    # Suppression si demandé
    if [ "$REMOVE" = true ]; then
        echo "[TestSQLite] Suppression des entrées test..."
        echo "$SQL_REMOVE_TEST" | sqlite3 "$DB_PATH"
        echo "[TestSQLite] Entrées test supprimées."
    fi
fi

echo "[TestSQLite] Test SQLite terminé."
