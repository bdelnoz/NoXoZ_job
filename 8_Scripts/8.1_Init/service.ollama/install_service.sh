#!/bin/bash
################################################################################
# Installation service systemd Ollama NoXoZ_job
# Auteur: Bruno DELNOZ
# Date: 2026-02-07
################################################################################
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/noxoz_job.ollama.service"
START_SCRIPT="$SCRIPT_DIR/start_ollama.sh"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="noxoz_job.ollama.service"

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
RUN_DIR="$BASE_DIR/10_Runs"
LOG_DIR="$BASE_DIR/4_Logs"

# Couleurs pour affichage
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

verify_files() {
  [[ -f "$SERVICE_FILE" ]] || { error "Fichier service introuvable: $SERVICE_FILE"; exit 1; }
  [[ -f "$START_SCRIPT" ]] || { error "Script start_ollama.sh introuvable: $START_SCRIPT"; exit 1; }
  [[ -x "$START_SCRIPT" ]] || chmod +x "$START_SCRIPT"
  info "Fichiers OK"
}

create_directories() {
  mkdir -p "$RUN_DIR" "$LOG_DIR"
  chown nox:nox "$RUN_DIR" "$LOG_DIR"
  info "Répertoires de run et logs créés"
}

install_service() {
  info "Installation service $SERVICE_NAME..."
  sudo cp "$SERVICE_FILE" "$SYSTEMD_DIR/$SERVICE_NAME"
  sudo chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME"
  sudo systemctl daemon-reload
  sudo systemctl enable "$SERVICE_NAME"
  info "Service installé et activé au boot"
}

start_service() {
  read -p "Voulez-vous démarrer le service maintenant ? (o/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[OoYy]$ ]]; then
    sudo systemctl start "$SERVICE_NAME"
    sleep 2
    sudo systemctl status "$SERVICE_NAME" --no-pager
  fi
}

main() {
  info "=== Installation service Ollama NoXoZ_job ==="
  check_root
  verify_files
  create_directories
  install_service
  start_service
  info "=== Installation terminée ==="
}

main "$@"
