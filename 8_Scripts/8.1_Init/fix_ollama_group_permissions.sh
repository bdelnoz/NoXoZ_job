#!/bin/bash
# -------------------------------------------------------------------
# Script: fix_ollama_group_permissions.sh
# Auteur: Bruno DELNOZ <bruno.delnoz@protonmail.com>
# Chemin: /mnt/data2_78g/Security/scripts/Projects_system/ollama/fix_ollama_group_permissions.sh
# Version: 1.0
# Date: 2026-02-05
# Description: Ajoute l'utilisateur 'ollama' au groupe 'nox' et corrige les permissions.
# -------------------------------------------------------------------

# 1. Ajouter 'ollama' au groupe 'nox'
echo "[1/5] Ajout de 'ollama' au groupe 'nox'..."
sudo usermod -aG nox ollama

# 2. Vérifier que 'ollama' est dans le groupe 'nox'
echo "[2/5] Vérification des groupes de 'ollama'..."
id ollama

# 3. Changer le groupe des dossiers concernés
echo "[3/5] Correction des permissions des dossiers..."
sudo chown -R nox:nox /mnt/data1_100g/agent_llm_local/models/
sudo chmod -R 770 /mnt/data1_100g/agent_llm_local/models/

# 4. Corriger les permissions du chemin complet
echo "[4/5] Correction des permissions du chemin complet..."
sudo chmod 750 /mnt/
sudo chmod 750 /mnt/data1_100g/
sudo chmod 750 /mnt/data1_100g/agent_llm_local/

# 5. Redémarrer le service Ollama
echo "[5/5] Redémarrage du service Ollama..."
sudo systemctl restart ollama.service

# Vérification finale
echo ""
echo "=== Vérification des permissions ==="
sudo -u ollama ls -l /mnt/data1_100g/agent_llm_local/models/

echo ""
echo "=== Statut du service Ollama ==="
systemctl status ollama.service --no-pager
