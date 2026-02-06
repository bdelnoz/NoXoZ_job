#!/bin/bash
################################################################################
# PATH: start_fastapi.sh
# Auteur: Bruno DELNOZ
# Objectif: Gestion FastAPI (start/stop/restart/status) fiable
# Version: v3.1.0 – corrigé
################################################################################
set -euo pipefail

### CONFIG ###
APP_MODULE="main_agent:app"       # <-- corrigé
HOST="127.0.0.1"
PORT="8443"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
SRC_DIR="$BASE_DIR/2_Sources/2.1_Python"   # <-- répertoire du main_agent.py
LOG_DIR="$BASE_DIR/4_Logs"
PID_FILE="$BASE_DIR/fastapi.pid"

CERT_FILE="$BASE_DIR/certs/cert.pem"
KEY_FILE="$BASE_DIR/certs/key.pem"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/log.start_fastapi.$TIMESTAMP.log"

### UTILS ###
is_running() {
  [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

### ACTIONS ###
start() {
  if is_running; then
    echo "[ERROR] FastAPI déjà actif (PID $(cat "$PID_FILE"))"
    exit 1
  fi

  echo "[INFO] Démarrage FastAPI (HTTPS uniquement)"
  echo "[INFO] Log : $LOG_FILE"

  # Aller dans le répertoire où se trouve main_agent.py
  cd "$SRC_DIR"

  # Active pipenv si présent
  if command -v pipenv >/dev/null 2>&1; then
    exec_cmd="pipenv run uvicorn  --reload"
  else
    exec_cmd="uvicorn  --reload "
  fi

  nohup $exec_cmd "$APP_MODULE" \
    --host "$HOST" \
    --port "$PORT" \
    --ssl-certfile "$CERT_FILE" \
    --ssl-keyfile "$KEY_FILE" \
    > "$LOG_FILE" 2>&1 &

  echo $! > "$PID_FILE"

  sleep 1
  if is_running; then
    echo "[INFO] FastAPI démarré avec PID $(cat "$PID_FILE")"
    echo "URL: https://$HOST:$PORT"
  else
    echo "[ERROR] Échec du démarrage"
    rm -f "$PID_FILE"
    exit 1
  fi
}

stop() {
  if ! is_running; then
    echo "[INFO] Aucun FastAPI actif"
    rm -f "$PID_FILE"
    exit 0
  fi

  PID="$(cat "$PID_FILE")"
  echo "[INFO] Arrêt FastAPI PID $PID"
  kill "$PID"
  sleep 1

  if kill -0 "$PID" 2>/dev/null; then
    echo "[WARN] Process encore actif, kill -9"
    kill -9 "$PID"
  fi

  rm -f "$PID_FILE"
  echo "[INFO] FastAPI arrêté"
}

status() {
  if is_running; then
    echo "[STATUS] FastAPI actif, PID $(cat "$PID_FILE")"
  else
    echo "[STATUS] FastAPI non lancé"
  fi
}

### MAIN ###
case "${1:-}" in
  start)  start ;;
  stop)   stop ;;
  status) status ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
    ;;
esac
