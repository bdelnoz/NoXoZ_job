---
# **Commandes Ollama Complètes (Bruno Delnoz - Kali Linux)**
**Date** : 2026-02-05
**Format** : Markdown (`.md`)
**Emplacement** : `/mnt/data2_78g/Security/scripts/Projects_system/Docs/commandes_ollama.md`
**Usage** : Copier-coller directement ce bloc dans un fichier `.md`.

---

```bash
################################################################################
# 📌 COMMANDES OLLAMA (Toutes catégories confondues)
################################################################################

# ===============================================================================
# 1️⃣ GESTION DES MODÈLES
# ===============================================================================

# --- Téléchargement/Mise à jour ---
ollama pull <modèle>                     # Ex: ollama pull phi3:3.8b
ollama pull --help                        # Affiche l'aide complète
ollama pull <modèle> --show-progress     # Affiche la progression
ollama pull --update <modèle>             # Met à jour un modèle

# --- Liste/Suppression ---
ollama list                              # Liste TOUS les modèles locaux
ollama rm <modèle>                       # Supprime un modèle (ex: ollama rm mistral:7b)
ollama rm --all                          # ⚠️ Supprime TOUS les modèles locaux

# ===============================================================================
# 2️⃣ EXÉCUTION ET INTERACTION
# ===============================================================================

# --- Mode Interactif ---
ollama run <modèle>                      # Ex: ollama run llama3:8b
ollama run <modèle> "<prompt>"           # Ex: ollama run phi3:3.8b "Explique Docker"

# --- Options Avancées ---
ollama run <modèle> --verbose            # Mode verbeux (logs détaillés)
ollama run <modèle> --temperature 0.8    # Équilibre créativité/précision
ollama run <modèle> --num-gpu 1          # Utilise 1 GPU
ollama run <modèle> --num-threads 8      # Limite à 8 threads CPU
ollama run <modèle> --mirostat 2         # Meilleure cohérence des réponses
ollama run <modèle> --repeat_penalty 1.2 # Réduit les répétitions

# ===============================================================================
# 3️⃣ GESTION DU SERVEUR OLLAMA
# ===============================================================================

# --- Démarrage/Arrêt ---
ollama serve                             # Démarre le serveur (port 11434)
ollama serve --host 0.0.0.0              # ⚠️ Accès réseau (sécurité !)
ollama serve --port 11435                # Change le port
pkill -f ollama                          # Arrête le serveur (Kali Linux)

# --- Configuration ---
export OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models  # Chemin personnalisé
export OLLAMA_HOST=0.0.0.0:11434         # Hôte/port
ollama serve --debug                     # Mode debug (logs étendus)

# ===============================================================================
# 4️⃣ MODELFILES (Personnalisation)
# ===============================================================================

# --- Exemple de Modelfile ---
# FROM llama2:7b
# PARAMETER temperature 0.8
# SYSTEM "Tu es un assistant technique spécialisé en Kali Linux."

ollama create mon_modèle -f Modelfile   # Crée un modèle personnalisé

# ===============================================================================
# 5️⃣ API ET RÉSEAU
# ===============================================================================

# --- Requêtes API ---
curl http://localhost:11434/api/tags     # Liste les modèles via API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3:8b", "prompt": "Bonjour"}'

# --- Sécurité Réseau ---
ollama serve --tls-key key.pem --tls-cert cert.pem  # Chiffrement TLS

# ===============================================================================
# 6️⃣ PERFORMANCES ET DÉBOGAGE
# ===============================================================================

# --- Optimisation ---
ollama run <modèle> --mirostat 2         # Cohérence améliorée
ollama run <modèle> --repeat_penalty 1.2 # Moins de répétitions

# --- Débogage ---
journalctl -u ollama -f                 # Logs temps réel (systemd)
ollama run <modèle> --verbose            # Sortie détaillée

# ===============================================================================
# 7️⃣ SCRIPTS PRÊTS À L'EMPLOI
# ===============================================================================

# --- Analyser un Fichier Texte ---
#!/bin/bash
# Script: analyse_doc.sh
# Usage: ./analyse_doc.sh mon_fichier.txt "Ta question"
ollama run phi3:3.8b "Analyse ce fichier : \$(cat \$1) et réponds à : \$2" > "analyse_\$(date +%Y%m%d).md"

# --- Générer une Synthèse ---
#!/bin/bash
# Script: synthese_doc.sh
# Usage: ./synthese_doc.sh mon_fichier.txt
ollama run llama3:8b "Résume ce document en 5 points clés : \$(cat \$1)" > "synthese_\$(date +%Y%m%d).md"

# --- Lister les Modèles (Filtré) ---
ollama list | grep -E "NAME|<modèle>"    # Filtre un modèle spécifique

# ===============================================================================
# 8️⃣ MODÈLES RECOMMANDÉS (Pour Bruno Delnoz)
# ===============================================================================

| Modèle               | Taille (Go) | Tokens Max | Usage Recommandé                          | Commande                     |
|----------------------|-------------|------------|-------------------------------------------|------------------------------|
| phi3:3.8b            | 2.3          | 128,000    | Documents très longs (350 questions)      | ollama pull phi3:3.8b        |
| mistral:7b           | 4.1          | 8,192      | Rapidité, scripts Kali Linux             | ollama pull mistral:7b        |
| llama3:8b            | 4.7          | 8,192      | Usage général                            | ollama pull llama3:8b        |
| codellama:34b         | 20           | 32,000     | Analyse de code                          | ollama pull codellama:34b    |
| dbrx:132b             | 240          | 128,000    | Analyse de très longs documents          | ollama pull dbrx:132b        |

# ===============================================================================
# 9️⃣ RÉSUMÉ DES BONNES PRATIQUES
# ===============================================================================

# 1. Téléchargement : ollama pull <modèle>
# 2. Exécution : ollama run <modèle>
# 3. Gestion : ollama list / ollama rm
# 4. Scripts : Intégration avec redirections (<<<, |)
# 5. Débogage : ollama serve --debug + journalctl

# ===============================================================================
# 📄 EXEMPLE DE SCRIPT COMPLET
# ===============================================================================

#!/bin/bash
# Script: ollama_tools.sh
# Auteur: Bruno Delnoz
# Description: Outils pour Ollama

download_model() {
    ollama pull "\$1"
}

analyze_file() {
    ollama run phi3:3.8b "Analyse ce fichier : \$(cat \$1)" > "analyse_\$(date +%Y%m%d).md"
}

list_models() {
    ollama list
}

case "\$1" in
    download) download_model "\$2" ;;
    analyze) analyze_file "\$2" ;;
    list) list_models ;;
    *) echo "Usage: \$0 {download|analyze|list} [args]"; exit 1 ;;
esac
################################################################################
