#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/service.fastapi/uninstall_service.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Désinstallation service systemd noxoz_job.fastapi
# Version: v1.0.0 – Date: 2026-02-07
#
# CHANGELOG:
# v1.0.0 - 2026-02-07: Création script désinstallation service
################################################################################
set -euo pipefail

### CONFIG ###
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="noxoz_job.fastapi.service"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
RUN_DIR="$BASE_DIR/10_Runs"

### COLORS ###
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

### UTILS ###
info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

check_root() {
  if [[ $EUID -ne 0 ]]; then
    error "Ce script doit être exécuté avec sudo"
    exit 1
  fi
}

### MAIN ###

main() {
  info "=== Désinstallation service FastAPI NoXoZ_job ==="
  echo ""

  check_root

  if [[ ! -f "$SYSTEMD_DIR/$SERVICE_NAME" ]]; then
    warn "Service $SERVICE_NAME non installé"
    exit 0
  fi

  info "Arrêt service..."
  systemctl stop "$SERVICE_NAME" 2>/dev/null || true

  info "Désactivation démarrage auto..."
  systemctl disable "$SERVICE_NAME" 2>/dev/null || true

  info "Suppression fichier service..."
  rm -f "$SYSTEMD_DIR/$SERVICE_NAME"

  info "Reload systemd..."
  systemctl daemon-reload

  info "Nettoyage PID files..."
  rm -f "$RUN_DIR/service.noxoz_job.fastapi.pid"
  rm -f "$RUN_DIR/fastapi.pid"

  echo ""
  info "=== Désinstallation terminée ==="
  echo ""

  info "Les logs et scripts restent en place:"
  echo "  Logs: $BASE_DIR/4_Logs/"
  echo "  Scripts: $BASE_DIR/8_Scripts/8.1_Init/"
}

main "$@"
