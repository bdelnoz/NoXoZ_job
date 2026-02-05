#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/test_fastapi.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Test automatisé et contrôlé de l'API FastAPI (NoXoZ_job)
# Version: v1.2.0 – Date: 2026-02-06
#
# Changelog:
# - v1.0.0 (2026-02-05): Version initiale
# - v1.1.0 (2026-02-06): Correction PYTHONPATH, logs projet, simulate strict
# - v1.2.0 (2026-02-06): Logs déplacés vers ./4_Logs (architecture projet)
################################################################################

# ==============================================================================
# VARIABLES GLOBALES
# ==============================================================================
BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
API_URL="http://127.0.0.1:11111"

SCRIPT_NAME="test_fastapi"
SCRIPT_VERSION="v1.2.0"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

LOG_DIR="$BASE_DIR/4_Logs"
LOG_FILE="$LOG_DIR/log.${SCRIPT_NAME}.${TIMESTAMP}.${SCRIPT_VERSION}.log"

EXEC=false
SIMULATE=false
PREREQUIS=false
INSTALL=false
FORCE=false
KEEP=false


TEST_RESULTS_OK=()
TEST_RESULTS_FAIL=()

PID_FILE="$LOG_DIR/${SCRIPT_NAME}.pid"


# ==============================================================================
# HELP
# ==============================================================================
show_help() {
cat <<EOF
Usage: $0 [OPTIONS]

OPTIONS:
  --help, -h        Affiche cette aide
  --exec, -exe      Lance réellement les tests FastAPI
  --simulate, -s    Simulation uniquement (aucune action, aucun fichier touché)
  --prerequis, -pr  Vérifie les prérequis système
  --install, -i     Installe les prérequis manquants
  --force, -f       Force l'arrêt d'un PID existant (PID zombie ou actif)
  --keep, -k        Garde le serveur FastAPI démarré après les tests
Exemples:
  $0 --simulate
  $0 --prerequis
  $0 --exec
EOF
}

# ==============================================================================
# PARSING ARGUMENTS
# ==============================================================================
if [ "$#" -eq 0 ]; then
    show_help
    exit 0
fi

for arg in "$@"; do
    case "$arg" in
        --help|-h) show_help; exit 0 ;;
        --exec|-exe) EXEC=true ;;
        --simulate|-s) SIMULATE=true ;;
        --prerequis|-pr) PREREQUIS=true ;;
        --install|-i) INSTALL=true ;;
        --force|-f) FORCE=true ;;
        --keep|-k) KEEP=true ;;
        *) echo "[ERROR] Argument inconnu: $arg"; exit 1 ;;
    esac
done

# ==============================================================================
# PREREQUIS
# ==============================================================================
if [ "$PREREQUIS" = true ]; then
    echo "[CHECK] Vérification des prérequis"
    command -v python3 >/dev/null || echo "[WARN] python3 manquant"
    command -v pipenv >/dev/null || echo "[WARN] pipenv manquant"
    command -v curl >/dev/null || echo "[WARN] curl manquant"
    exit 0
fi

# ==============================================================================
# INSTALL
# ==============================================================================
if [ "$INSTALL" = true ]; then
    echo "[INSTALL] Installation des prérequis"
    sudo apt update
    sudo apt install -y python3 python3-pip curl
    pip install pipenv
    exit 0
fi

# ==============================================================================
# SIMULATE
# ==============================================================================
if [ "$SIMULATE" = true ]; then
    echo "[SIMULATE] Actions prévues :"
    echo "  - cd $BASE_DIR"
    echo "  - activation pipenv"
    echo "  - export PYTHONPATH=2_Sources/2.1_Python"
    echo "  - lancement FastAPI (uvicorn)"
    echo "  - tests endpoints: /status /generate /upload"
    echo "  - logs dans $LOG_DIR"
    exit 0
fi

# ==============================================================================
# GESTION PID EXISTANT
# ==============================================================================
if [ -f "$PID_FILE" ]; then
    EXISTING_PID="$(cat "$PID_FILE")"

    if ps -p "$EXISTING_PID" >/dev/null 2>&1; then
        if [ "$FORCE" = true ]; then
            echo "[FORCE] PID actif détecté ($EXISTING_PID), arrêt forcé"
            kill "$EXISTING_PID"
            sleep 1
            rm -f "$PID_FILE"
        else
            echo "[ERROR] FastAPI déjà en cours d'exécution (PID=$EXISTING_PID)"
            echo "Utilise --force pour forcer l'arrêt"
            exit 1
        fi
    else
        if [ "$FORCE" = true ]; then
            echo "[FORCE] PID zombie détecté ($EXISTING_PID), nettoyage"
            rm -f "$PID_FILE"
        else
            echo "[ERROR] PID zombie détecté ($EXISTING_PID)"
            echo "Utilise --force pour nettoyer le PID"
            exit 1
        fi
    fi
fi

# ==============================================================================
# EXECUTION RÉELLE
# ==============================================================================
mkdir -p "$LOG_DIR"

cd "$BASE_DIR" || { echo "[ERROR] cd impossible"; exit 1; }

echo "[INFO] Activation pipenv"
pipenv shell

export PYTHONPATH="$BASE_DIR/2_Sources/2.1_Python:$PYTHONPATH"

echo "[INFO] Lancement FastAPI"
echo "[INFO] Log: $LOG_FILE"

uvicorn main_agent:app \
    --host 127.0.0.1 \
    --port 11111 \
    --reload \
    > "$LOG_FILE" 2>&1 &

API_PID=$!
echo "$API_PID" > "$PID_FILE"
sleep 3

if ! ps -p "$API_PID" >/dev/null; then
    echo "[ERROR] FastAPI ne s'est pas lancé"
    echo "Voir log: $LOG_FILE"
    exit 1
fi

# ==============================================================================
# TESTS ENDPOINTS
# ==============================================================================
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/status/")
[ "$STATUS_CODE" = "200" ] \
    && TEST_RESULTS_OK+=("/status OK") \
    || TEST_RESULTS_FAIL+=("/status FAIL ($STATUS_CODE)")

GEN_RESPONSE=$(curl -s -X POST "$API_URL/generate/" -F "prompt=Test FastAPI")
[[ "$GEN_RESPONSE" == *"Document"* ]] \
    && TEST_RESULTS_OK+=("/generate OK") \
    || TEST_RESULTS_FAIL+=("/generate FAIL")

TMP_FILE="$BASE_DIR/4_Logs/test_upload_fastapi.txt"
echo "Test upload FastAPI" > "$TMP_FILE"

UPLOAD_RESPONSE=$(curl -s -X POST -F "file=@$TMP_FILE" "$API_URL/upload/")
[[ "$UPLOAD_RESPONSE" == *"success"* ]] \
    && TEST_RESULTS_OK+=("/upload OK") \
    || TEST_RESULTS_FAIL+=("/upload FAIL")

rm -f "$TMP_FILE"

# ==============================================================================
# ARRÊT SERVEUR (ou maintien)
# ==============================================================================
if [ "$KEEP" = true ]; then
    echo "[KEEP] Serveur FastAPI laissé actif"
    echo "[KEEP] PID: $(cat "$PID_FILE")"
    echo "[KEEP] Pour arrêter manuellement : kill \$(cat $PID_FILE)"
else
    if [ -f "$PID_FILE" ]; then
        API_PID="$(cat "$PID_FILE")"
        kill "$API_PID"
        rm -f "$PID_FILE"
        echo "[INFO] Serveur FastAPI arrêté, PID supprimé"
    fi
fi
sleep 3
# ==============================================================================
# RÉSUMÉ FINAL
# ==============================================================================
echo "================================================="
echo "Résumé des tests FastAPI"
echo "-------------------------------------------------"
for r in "${TEST_RESULTS_OK[@]}"; do echo "[ OK ] $r"; done
for r in "${TEST_RESULTS_FAIL[@]}"; do echo "[FAIL] $r"; done
echo "-------------------------------------------------"
echo "Log complet : $LOG_FILE"
echo "================================================="
