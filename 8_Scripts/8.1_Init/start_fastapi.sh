#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/start_fastapi.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Démarrage / arrêt / statut FastAPI NoXoZ_job avec gestion de port et --force
# Version: v1.3.0 – 2026-02-06
################################################################################

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
LOG_DIR="$BASE_DIR/4_Logs"
SCRIPT_NAME="start_fastapi"
SCRIPT_VERSION="v1.3.0"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/log.${SCRIPT_NAME}.${TIMESTAMP}.${SCRIPT_VERSION}.log"

EXEC=false
STOP=false
FORCE=false
STATUS=false

show_help() {
cat <<EOF
Usage: $0 [OPTIONS]

OPTIONS:
  --help, -h      Affiche cette aide
  --exec, -exe    Démarre FastAPI
  --stop, -s      Arrête FastAPI
  --force, -f     Force kill PID bloquant le port
  --status, -st   Affiche le statut actuel de FastAPI
Exemples:
  $0 --exec
  $0 --exec --force
  $0 --stop
  $0 --status
EOF
}

# ----------------------------
# Parsing arguments
# ----------------------------
for arg in "$@"; do
    case "$arg" in
        --help|-h) show_help; exit 0 ;;
        --exec|-exe) EXEC=true ;;
        --stop|-s) STOP=true ;;
        --force|-f) FORCE=true ;;
        --status|-st) STATUS=true ;;
        *) echo "[ERROR] Argument inconnu: $arg"; exit 1 ;;
    esac
done

mkdir -p "$LOG_DIR"
cd "$BASE_DIR" || { echo "[ERROR] Impossible de cd"; exit 1; }

# ----------------------------
# Status check
# ----------------------------
if [ "$STATUS" = true ]; then
    PORT_PID=$(lsof -ti:11111)
    if [ -n "$PORT_PID" ]; then
        echo "[STATUS] FastAPI actif sur le port 11111, PID(s) : $PORT_PID"
    else
        echo "[STATUS] FastAPI non lancé"
    fi
    exit 0
fi

# ----------------------------
# Stop server
# ----------------------------
if [ "$STOP" = true ]; then
    PORT_PID=$(lsof -ti:11111)
    if [ -n "$PORT_PID" ]; then
        echo "[STOP] Kill PID(s) sur port 11111 : $PORT_PID"
        kill -9 $PORT_PID
        sleep 1
        echo "[INFO] Serveur FastAPI arrêté"
    else
        echo "[INFO] Aucun FastAPI actif"
    fi
    exit 0
fi

# ----------------------------
# Force kill si demandé
# ----------------------------
if [ "$FORCE" = true ]; then
    PORT_PID=$(lsof -ti:11111)
    if [ -n "$PORT_PID" ]; then
        echo "[FORCE] Kill PID(s) sur port 11111 : $PORT_PID"
        kill -9 $PORT_PID
        sleep 1
    fi
fi

# ----------------------------
# Start server
# ----------------------------
if [ "$EXEC" = true ]; then
    export PYTHONPATH="$BASE_DIR/2_Sources/2.1_Python:$PYTHONPATH"
    echo "[INFO] Démarrage FastAPI, log : $LOG_FILE"
    uvicorn main_agent:app --host 127.0.0.1 --port 11111 --reload > "$LOG_FILE" 2>&1 &
    API_PID=$!
    sleep 3
    if ps -p $API_PID >/dev/null; then
        echo "[INFO] FastAPI démarré (PID=$API_PID)"
        echo "URL: http://127.0.0.1:11111"
    else
        echo "[ERROR] FastAPI n'a pas pu démarrer"
        echo "Voir log : $LOG_FILE"
        exit 1
    fi
fi
