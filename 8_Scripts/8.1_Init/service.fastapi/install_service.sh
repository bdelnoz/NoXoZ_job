#!/bin/bash
################################################################################
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/service.fastapi/install_service.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Installation service systemd noxoz_job.fastapi
# Version: v1.0.0 – Date: 2026-02-07
#
# CHANGELOG:
# v1.0.0 - 2026-02-07: Création script installation service
################################################################################
set -euo pipefail

### CONFIG ###
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/noxoz_job.fastapi.service"
START_SCRIPT="$SCRIPT_DIR/../start_fastapi.sh"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="noxoz_job.fastapi.service"

OLD_SERVICES=(
  "fastapi_noxoz.service"
  "NoXoZ_job.DEV.fastAPI.service"
  "NoXoZ_job.PROD.fastAPI.service"
)

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
RUN_DIR="$BASE_DIR/10_Runs"
LOG_DIR="$BASE_DIR/4_Logs"

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

### ACTIONS ###

cleanup_old_services() {
  info "Nettoyage anciens services..."

  for old_service in "${OLD_SERVICES[@]}"; do
    if systemctl list-unit-files | grep -q "$old_service"; then
      info "Suppression service: $old_service"
      systemctl stop "$old_service" 2>/dev/null || true
      systemctl disable "$old_service" 2>/dev/null || true
      rm -f "$SYSTEMD_DIR/$old_service"
    fi
  done

  # Cleanup anciens PID files
  rm -f "$RUN_DIR/service.fastapi_noxoz.pid" 2>/dev/null || true

  info "Nettoyage terminé"
}

verify_files() {
  info "Vérification fichiers requis..."

  if [[ ! -f "$SERVICE_FILE" ]]; then
    error "Fichier service introuvable: $SERVICE_FILE"
    exit 1
  fi

  if [[ ! -f "$START_SCRIPT" ]]; then
    error "Script start_fastapi.sh introuvable: $START_SCRIPT"
    exit 1
  fi

  if [[ ! -x "$START_SCRIPT" ]]; then
    warn "Script start_fastapi.sh non exécutable, correction..."
    chmod +x "$START_SCRIPT"
  fi

  info "Fichiers OK"
}

create_directories() {
  info "Création répertoires nécessaires..."

  mkdir -p "$RUN_DIR"
  mkdir -p "$LOG_DIR"

  chown nox:nox "$RUN_DIR"
  chown nox:nox "$LOG_DIR"

  info "Répertoires créés"
}

install_service() {
  info "Installation service $SERVICE_NAME..."

  cp "$SERVICE_FILE" "$SYSTEMD_DIR/$SERVICE_NAME"
  chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME"

  systemctl daemon-reload

  info "Service installé"
}

display_status() {
  info "Configuration finale:"
  echo ""
  echo "  Service:        $SERVICE_NAME"
  echo "  Emplacement:    $SYSTEMD_DIR/$SERVICE_NAME"
  echo "  Script start:   $START_SCRIPT"
  echo "  PID file:       $RUN_DIR/service.noxoz_job.fastapi.pid"
  echo "  Logs:           $LOG_DIR/log.start_fastapi.*.log"
  echo ""
  info "Commandes disponibles:"
  echo "  sudo systemctl start $SERVICE_NAME"
  echo "  sudo systemctl stop $SERVICE_NAME"
  echo "  sudo systemctl restart $SERVICE_NAME"
  echo "  sudo systemctl status $SERVICE_NAME"
  echo "  sudo systemctl enable $SERVICE_NAME    (démarrage auto)"
  echo ""
}

### MAIN ###

main() {
  info "=== Installation service FastAPI NoXoZ_job ==="
  echo ""

  check_root
  cleanup_old_services
  verify_files
  create_directories
  install_service

  echo ""
  info "=== Installation terminée avec succès ==="
  echo ""

  display_status

  read -p "Voulez-vous activer le démarrage automatique au boot ? (o/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[OoYy]$ ]]; then
    systemctl enable "$SERVICE_NAME"
    info "Démarrage automatique activé"
  fi

  echo ""
  read -p "Voulez-vous démarrer le service maintenant ? (o/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[OoYy]$ ]]; then
    systemctl start "$SERVICE_NAME"
    sleep 2
    systemctl status "$SERVICE_NAME" --no-pager
  fi
}

main "$@"
