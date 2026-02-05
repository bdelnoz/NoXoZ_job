#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/test_sqlite.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v3.2.0 – 2026-02-05
# Target usage: Test SQLite complet pour NoXoZ_job
# Changelog:
#   v3.0.0 – Version ultime avec --exec, --simulate, --remove, --perf
#   v3.1.0 – --remove supprime aussi les entrées de perf
#   v3.2.0 – Version finale, commentaires détaillés et respect intégral des règles de scripting

# ----------------------------------------------------------------------
# 1. HELP
# ----------------------------------------------------------------------
function show_help() {
    echo "Usage: $0 [--simulate] [--exec] [--remove] [--perf]"
    echo
    echo "Ce script teste la base SQLite NoXoZ_job avec plusieurs modes :"
    echo "- --exec (-e) : insertion et lecture test standard"
    echo "- --simulate (-s) : dry-run, affiche toutes les actions sans exécuter"
    echo "- --remove (-r) : supprime toutes les entrées créées par le test (standard + perf)"
    echo "- --perf (-p) : test rapide de performance avec insert massifs dans cv"
    echo "- --help (-h) : affiche cette aide"
    exit 0
}

# ----------------------------------------------------------------------
# 2. PARSING DES ARGUMENTS
# ----------------------------------------------------------------------
SIMULATE=false
EXEC=false
REMOVE=false
PERF=false
for arg in "$@"; do
    case $arg in
        --help|-h) show_help ;;
        --simulate|-s) SIMULATE=true ;;
        --exec|-e) EXEC=true ;;
        --remove|-r) REMOVE=true ;;
        --perf|-p) PERF=true ;;
        *)
            echo "[ERROR] Option inconnue: $arg"
            show_help
            ;;
    esac
done

# ----------------------------------------------------------------------
# 3. CHEMIN DE LA DB
# ----------------------------------------------------------------------
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
DB_PATH="${PROJECT_ROOT}/3_Data/Metadata/noxoz_metadata.db"

# Vérification de l’existence de la DB
if [ ! -f "$DB_PATH" ]; then
    echo "[TestSQLite] ERREUR : DB non trouvée à $DB_PATH"
    exit 1
fi
echo "[TestSQLite] DB trouvée : $DB_PATH"

# ----------------------------------------------------------------------
# 4. COMMANDES SQL
# ----------------------------------------------------------------------
# 4a. Insertions test standard
SQL_INSERT_TEST=$(cat <<'EOF'
-- Insertion d'un CV test
INSERT INTO cv (filename, format, size, hash) VALUES ('test_cv.docx', 'docx', 12345, 'sha256:testhash');

-- Insertion d'un chat test
INSERT INTO chat_history (platform, content) VALUES ('TestPlatform', 'Ceci est un test chat.');

-- Insertion d'un document généré test
INSERT INTO generated_docs (type, filename, format) VALUES ('lettre_motivation', 'lettre_test.docx', 'docx');

-- Insertion d'un embedding lié au dernier CV
INSERT INTO embeddings_index (document_id, vector_id)
SELECT id, 'vector_test_001' FROM cv ORDER BY id DESC LIMIT 1;
EOF
)

# 4b. Sélection des dernières entrées
SQL_SELECT_TEST=$(cat <<'EOF'
SELECT 'CV Table:' AS TableName, * FROM cv ORDER BY id DESC LIMIT 1;
SELECT 'Chat Table:' AS TableName, * FROM chat_history ORDER BY id DESC LIMIT 1;
SELECT 'Generated Docs Table:' AS TableName, * FROM generated_docs ORDER BY id DESC LIMIT 1;
SELECT 'Embeddings Table:' AS TableName, * FROM embeddings_index ORDER BY id DESC LIMIT 1;
EOF
)

# 4c. Suppression des entrées test (standard + perf)
SQL_REMOVE_TEST=$(cat <<'EOF'
-- Suppression embeddings test
DELETE FROM embeddings_index WHERE vector_id='vector_test_001';
-- Suppression CV test
DELETE FROM cv WHERE filename='test_cv.docx';
-- Suppression chat test
DELETE FROM chat_history WHERE platform='TestPlatform';
-- Suppression document généré test
DELETE FROM generated_docs WHERE filename='lettre_test.docx';
-- Suppression des inserts perf (filtre par préfixe)
DELETE FROM cv WHERE filename LIKE 'perf_cv%';
EOF
)

# 4d. Test performance rapide (insert 100 CV)
SQL_PERF_TEST=$(cat <<'EOF'
-- Test de performance : insert massifs
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

# ----------------------------------------------------------------------
# 5. EXECUTION DES TESTS
# ----------------------------------------------------------------------
# 5a. Test standard (--exec)
if [ "$EXEC" = true ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] Insertion données test standard"
        echo "$SQL_INSERT_TEST"
        echo "[SIMULATE] Lecture dernières entrées"
        echo "$SQL_SELECT_TEST"
    else
        echo "[TestSQLite] Insertion des données test standard..."
        echo "$SQL_INSERT_TEST" | sqlite3 "$DB_PATH"
        echo "[TestSQLite] Lecture des dernières entrées..."
        echo "$SQL_SELECT_TEST" | sqlite3 "$DB_PATH"

        # Vérification FK embeddings_index -> cv
        echo "[TestSQLite] Vérification FK embeddings_index -> cv..."
        FK_CHECK=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM embeddings_index WHERE document_id NOT IN (SELECT id FROM cv);")
        if [ "$FK_CHECK" -eq 0 ]; then
            echo "[TestSQLite] OK : Tous les embeddings ont une CV existante."
        else
            echo "[TestSQLite] ERREUR : $FK_CHECK embeddings pointent sur des CV inexistantes !"
        fi
    fi
fi

# 5b. Test performance (--perf)
if [ "$PERF" = true ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] Test rapide de performance activé"
        echo "$SQL_PERF_TEST"
    else
        echo "[TestSQLite] Test rapide de performance : insertion massives dans CV"
        echo "$SQL_PERF_TEST" | sqlite3 "$DB_PATH"
    fi
fi

# 5c. Suppression des entrées (--remove)
if [ "$REMOVE" = true ]; then
    if [ "$SIMULATE" = true ]; then
        echo "[SIMULATE] Suppression des entrées test standard + perf"
        echo "$SQL_REMOVE_TEST"
    else
        echo "[TestSQLite] Suppression des entrées test standard + perf..."
        echo "$SQL_REMOVE_TEST" | sqlite3 "$DB_PATH"
        echo "[TestSQLite] Toutes les entrées test supprimées."
    fi
fi

# ----------------------------------------------------------------------
# 6. FIN
# ----------------------------------------------------------------------
echo "[TestSQLite] Test SQLite terminé."
