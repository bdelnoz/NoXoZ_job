#!/bin/bash
################################################################################
# Désinstallation service systemd Ollama NoXoZ_job
# Auteur: Bruno DELNOZ
# Date: 2026-02-07
################################################################################
set -euo pipefail

SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="noxoz_job.ollama.service"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
RUN_DIR="$BASE_DIR/10_Runs"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

check_root() {
  if [[ $EUID -ne 0 ]]; then
    error "Ce script doit être exécuté avec sudo"
    exit 1
  fi
}

main() {
  info "=== Désinstallation service Ollama NoXoZ_job ==="
  check_root

  if [[ ! -f "$SYSTEMD_DIR/$SERVICE_NAME" ]]; then
    warn "Service $SERVICE_NAME non installé"
    exit 0
  fi

  info "Arrêt du service..."
  sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true

  info "Désactivation démarrage automatique..."
  sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true

  info "Suppression fichier service..."
  sudo rm -f "$SYSTEMD_DIR/$SERVICE_NAME"

  info "Reload systemd..."
  sudo systemctl daemon-reload

  info "Nettoyage PID..."
  rm -f "$RUN_DIR/service.noxoz_job.ollama.pid" "$RUN_DIR/ollama.pid"

  info "=== Désinstallation terminée ==="
  echo "Les logs et scripts restent en place:"
  echo "  Logs: $BASE_DIR/4_Logs/"
  echo "  Scripts: $BASE_DIR/8_Scripts/8.1_Init/service.ollama/"
}

main "$@"
