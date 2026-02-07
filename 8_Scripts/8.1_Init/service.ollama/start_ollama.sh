#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/start_ollama.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Gestion Ollama avec PID réel et intégration systemd NoXoZ
# Version: v1.0.0 – Date: 2026-02-07
#
# CHANGELOG:
# v1.0.0 - 2026-02-07: Création start_ollama.sh avec PID réel, stop fiable, status
################################################################################
set -euo pipefail

### CONFIG ###
OLLAMA_BIN="/usr/local/bin/ollama"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
LOG_DIR="$BASE_DIR/4_Logs"
RUN_DIR="$BASE_DIR/10_Runs"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

PID_FILE="$RUN_DIR/ollama.pid"
SYSTEMD_PID_FILE="$RUN_DIR/service.noxoz_job.ollama.pid"
LOG_FILE="$LOG_DIR/log.start_ollama.$TIMESTAMP.log"

### UTILS ###

is_running() {
  if [[ -f "$SYSTEMD_PID_FILE" ]]; then
    local pid
    pid="$(cat "$SYSTEMD_PID_FILE" 2>/dev/null || true)"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

get_pid() {
  if [[ -f "$SYSTEMD_PID_FILE" ]]; then
    cat "$SYSTEMD_PID_FILE" 2>/dev/null || true
  fi
}

### ACTIONS ###

start() {
  if is_running; then
    local pid
    pid="$(get_pid)"
    echo "[ERROR] Ollama déjà actif (PID $pid)"
    exit 1
  fi

  echo "[INFO] Démarrage Ollama"
  echo "[INFO] Log: $LOG_FILE"

  nohup "$OLLAMA_BIN" serve \
    > "$LOG_FILE" 2>&1 &

  local launch_pid=$!
  echo "$launch_pid" > "$PID_FILE"
  echo "$launch_pid" > "$SYSTEMD_PID_FILE"

  sleep 2

  if kill -0 "$launch_pid" 2>/dev/null; then
    echo "[INFO] Ollama démarré"
    echo "[INFO] PID: $launch_pid"
  else
    echo "[ERROR] Échec démarrage Ollama"
    rm -f "$PID_FILE" "$SYSTEMD_PID_FILE"
    exit 1
  fi
}

stop() {
  if ! is_running; then
    echo "[INFO] Ollama non actif"
    rm -f "$PID_FILE" "$SYSTEMD_PID_FILE"
    exit 0
  fi

  local pid
  pid="$(get_pid)"

  echo "[INFO] Arrêt Ollama PID $pid"

  kill "$pid" 2>/dev/null || true
  sleep 2

  if kill -0 "$pid" 2>/dev/null; then
    echo "[WARN] Process encore actif, kill -9"
    kill -9 "$pid" 2>/dev/null || true
    sleep 1
  fi

  rm -f "$PID_FILE" "$SYSTEMD_PID_FILE"

  if is_running; then
    echo "[ERROR] Impossible d'arrêter Ollama"
    exit 1
  else
    echo "[INFO] Ollama arrêté"
  fi
}

restart() {
  echo "[INFO] Restart Ollama"
  stop
  sleep 2
  start
}

status() {
  if is_running; then
    local pid
    pid="$(get_pid)"
    echo "[STATUS] Ollama actif"
    echo "[STATUS] PID: $pid"
    echo ""
    ps -fp "$pid" 2>/dev/null || true
  else
    echo "[STATUS] Ollama non lancé"
  fi
}

update_pid() {
  # Pour compatibilité systemd (ExecStartPost)
  if is_running; then
    echo "[INFO] PID déjà présent: $(get_pid)"
    exit 0
  fi

  local pid
  pid="$(pgrep -f 'ollama serve' | head -n1 || true)"

  if [[ -n "$pid" ]]; then
    echo "$pid" > "$SYSTEMD_PID_FILE"
    echo "[INFO] PID systemd mis à jour: $pid"
  else
    echo "[WARN] Impossible de détecter PID Ollama"
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
    echo "  - Démarrage Ollama avec PID réel"
    echo "  - PID visible et exploitable par systemd"
    echo "  - Stop/restart fiables"
    exit 1
    ;;
esac
