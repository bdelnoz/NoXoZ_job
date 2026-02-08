#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/start_fastapi.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Gestion FastAPI avec --reload et PID réel visible dans systemd
# Version: v3.7.0 – Date: 2026-02-07
#
# CHANGELOG:
# v3.7.0 - 2026-02-07: Renommage service noxoz_job.fastapi, fix PID file path
# v3.6.0 - 2026-02-07: Ajout update-pid pour systemd, PID réel visible
# v3.5.0 - 2026-02-07: Version unique --reload, capture PID réel ss -tlpn
################################################################################
set -euo pipefail

### CONFIG ###
APP_MODULE="main_agent:app"
HOST="127.0.0.1"
PORT="8443"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
SRC_DIR="$BASE_DIR/2_Sources/2.1_Python"
LOG_DIR="$BASE_DIR/4_Logs"
RUN_DIR="$BASE_DIR/10_Runs"

CERT_FILE="$BASE_DIR/certs/cert.pem"
KEY_FILE="$BASE_DIR/certs/key.pem"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

PID_FILE="$RUN_DIR/fastapi.pid"
SYSTEMD_PID_FILE="$RUN_DIR/service.noxoz_job.fastapi.pid"
LOG_FILE="$LOG_DIR/log.start_fastapi.$TIMESTAMP.log"


### UTILS ###

# Capture PID réel depuis ss -tlpn
get_real_pid() {
  ss -tlpn 2>/dev/null | grep ":${PORT}" | awk -F'pid=' '{print $2}' | awk -F',' '{print $1}' | head -n1
}

# Fallback PID lookup when ss cannot see the listener (permissions or startup delay)
get_uvicorn_pid() {
  pgrep -f "uvicorn.*${APP_MODULE}.*--port ${PORT}.*--reload" | head -n1
}

# Resolve PID via listener first, then fallback process lookup
resolve_pid() {
  local real_pid
  real_pid="$(get_real_pid)"
  if [[ -n "$real_pid" ]]; then
    echo "$real_pid"
    return 0
  fi
  get_uvicorn_pid
}

# Vérifie si FastAPI écoute sur le port
is_running() {
  local real_pid
  real_pid="$(resolve_pid)"
  if [[ -n "$real_pid" ]] && kill -0 "$real_pid" 2>/dev/null; then
    return 0
  fi
  return 1
}

### ACTIONS ###

start() {
  if is_running; then
    local current_pid=$(get_real_pid)
    echo "[ERROR] FastAPI déjà actif (PID réel $current_pid sur port $PORT)"
    exit 1
  fi

  echo "[INFO] Démarrage FastAPI avec --reload"
  echo "[INFO] Log: $LOG_FILE"

  cd "$SRC_DIR"

  if command -v pipenv >/dev/null 2>&1; then
    exec_cmd="pipenv run uvicorn"
  else
    exec_cmd="uvicorn"
  fi

  nohup $exec_cmd "$APP_MODULE" \
    --host "$HOST" \
    --port "$PORT" \
    --ssl-certfile "$CERT_FILE" \
    --ssl-keyfile "$KEY_FILE" \
    --reload \
    --reload-dir "$SRC_DIR/api" \
    --reload-dir "$SRC_DIR/services" \
    > "$LOG_FILE" 2>&1 &
  local launch_pid=$!
  echo $launch_pid > "$PID_FILE"

  local real_pid=""
  local waited=0
  local max_wait=15
  while [[ $waited -lt $max_wait ]]; do
    sleep 1
    real_pid="$(resolve_pid)"
    if [[ -n "$real_pid" ]] && is_running; then
      break
    fi
    waited=$((waited + 1))
  done

  if [[ -n "$real_pid" ]] && is_running; then
    echo "[INFO] FastAPI démarré avec --reload"
    echo "[INFO] PID initial: $launch_pid"
    echo "[INFO] PID réel (port $PORT): $real_pid"
    echo "URL: https://$HOST:$PORT"

    # Mise à jour PID files
    echo "$real_pid" > "$PID_FILE"
    echo "$real_pid" > "$SYSTEMD_PID_FILE"
  else
    echo "[ERROR] Échec du démarrage"
    echo "[ERROR] Aucun processus détecté sur port $PORT"
    echo "[ERROR] Dernières lignes du log:"
    tail -n 50 "$LOG_FILE" || true
    rm -f "$PID_FILE"
    rm -f "$SYSTEMD_PID_FILE"
    exit 1
  fi
}

stop() {
  local real_pid
  real_pid="$(resolve_pid)"

  if [[ -z "$real_pid" ]]; then
    echo "[INFO] Aucun FastAPI actif sur port $PORT"
    rm -f "$PID_FILE"
    rm -f "$SYSTEMD_PID_FILE"
    exit 0
  fi

  echo "[INFO] Arrêt FastAPI PID réel $real_pid"

  # Kill process group complet (gère --reload watchdog)
  pkill -P "$real_pid" 2>/dev/null || true
  kill "$real_pid" 2>/dev/null || true

  sleep 2

  # Vérification avec ss -tlpn
  if is_running; then
    echo "[WARN] Process encore actif, kill -9"
    local stubborn_pid
    stubborn_pid="$(resolve_pid)"
    pkill -9 -P "$stubborn_pid" 2>/dev/null || true
    kill -9 "$stubborn_pid" 2>/dev/null || true
    sleep 1
  fi

  # Cleanup final
  pkill -9 -f "uvicorn.*${APP_MODULE}.*--reload" 2>/dev/null || true

  rm -f "$PID_FILE"
  rm -f "$SYSTEMD_PID_FILE"

  if is_running; then
    echo "[ERROR] Impossible d'arrêter FastAPI complètement"
    exit 1
  else
    echo "[INFO] FastAPI arrêté"
  fi
}

restart() {
  echo "[INFO] Restart FastAPI"
  stop
  sleep 2
  start
}

status() {
  local real_pid
  real_pid="$(resolve_pid)"

  if [[ -n "$real_pid" ]] && is_running; then
    echo "[STATUS] FastAPI actif avec --reload"
    echo "[STATUS] PID réel (port $PORT): $real_pid"
    echo "[STATUS] Écoute: $HOST:$PORT"
    echo ""
    echo "Détails processus:"
    ps -fp "$real_pid" 2>/dev/null || echo "Impossible d'afficher détails"
    echo ""
    echo "Connexions réseau:"
    ss -tlpn 2>/dev/null | grep ":${PORT}" || echo "Aucune connexion détectée"
  else
    echo "[STATUS] FastAPI non lancé"
    echo "[STATUS] Port $PORT libre"
  fi
}

# Mise à jour PID systemd après démarrage (appelé par ExecStartPost)
update_pid() {
  sleep 3
  local real_pid
  real_pid="$(resolve_pid)"

  if [[ -n "$real_pid" ]]; then
    echo "$real_pid" > "$SYSTEMD_PID_FILE"
    echo "[INFO] PID systemd mis à jour: $real_pid"
  else
    echo "[WARN] Impossible de capturer PID réel"
  fi
}

### MAIN ###
case "${1:-}" in
  start)      start ;;
  stop)       stop ;;
  restart)    restart ;;
  status)     status ;;
  update-pid) update_pid ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|update-pid}"
    echo ""
    echo "Fonctionnalités:"
    echo "  - Démarrage avec --reload (auto-restart sur modif .py)"
    echo "  - Capture PID réel via ss -tlpn"
    echo "  - PID réel visible dans systemctl status"
    echo "  - Stop/restart fiables"
    exit 1
    ;;
esac
