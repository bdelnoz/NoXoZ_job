#!/bin/bash
# -------------------------------------------------------------------
# Script: reset_ollama_service.sh
# Auteur: Bruno DELNOZ <bruno.delnoz@protonmail.com>
# Chemin: /mnt/data2_78g/Security/scripts/Projects_system/ollama/reset_ollama_service.sh
# Version: 1.0
# Date: 2026-02-05
# Description: Réinitialise le service Ollama avec les bonnes configurations.
# -------------------------------------------------------------------

# 1. Supprimer le service existant
echo "[1/6] Suppression du service Ollama existant..."
sudo systemctl stop ollama.service 2>/dev/null
sudo systemctl disable ollama.service 2>/dev/null
sudo rm -f /etc/systemd/system/ollama.service
sudo rm -rf /etc/systemd/system/ollama.service.d/

# 2. Créer un nouveau fichier de service
echo "[2/6] Création du nouveau fichier de service..."
sudo tee /etc/systemd/system/ollama.service > /dev/null << 'EOL'
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
Type=simple
User=nox
Group=nox
Environment="OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models"
Environment="PATH=/home/nox/.opencode/bin:/home/nox/.local/bin:/home/nox/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/nox/.dotnet/tools:/mnt/data2_78g/Security/scripts/"
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3
WorkingDirectory=/home/nox
UMask=0002

[Install]
WantedBy=multi-user.target
EOL

# 3. Corriger les permissions des dossiers
echo "[3/6] Correction des permissions des dossiers..."
sudo chown -R nox:nox /mnt/data1_100g/agent_llm_local/models/
sudo chmod -R 770 /mnt/data1_100g/agent_llm_local/models/
sudo chmod 750 /mnt/data1_100g/agent_llm_local/
sudo chmod 750 /mnt/data1_100g/
sudo chmod 750 /mnt/

# 4. Recharger et activer le service
echo "[4/6] Rechargement et activation du service..."
sudo systemctl daemon-reload
sudo systemctl enable ollama.service
sudo systemctl start ollama.service

# 5. Vérifier l'environnement du service
echo "[5/6] Vérification de l'environnement du service..."
systemctl show ollama.service --property=Environment

# 6. Vérifier le statut du service
echo "[6/6] Vérification du statut du service..."
systemctl status ollama.service
journalctl -u ollama.service -n 20 --no-pager
