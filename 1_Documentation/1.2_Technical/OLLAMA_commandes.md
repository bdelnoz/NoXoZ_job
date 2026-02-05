---
# **📜 Commandes Ollama Complètes (Bruno Delnoz - Kali Linux)**
**Auteur** : Bruno Delnoz (nox@casablanca)
**Date** : 2026-02-05
**Version** : 1.0
**Format** : Markdown (`.md`)
**Emplacement** : `/mnt/data2_78g/Security/scripts/Projects_system/Docs/commandes_ollama.md`
**Contexte** : Scripts pour Kali Linux, format Markdown strict, sans numéros de version dans les noms de fichiers.
---

```bash
################################################################################
# 1️⃣ GESTION DES MODÈLES #######################################################
################################################################################

# Téléchargement/Mise à jour
ollama pull <modèle>                     # Ex: ollama pull phi3:3.8b (128K tokens, idéal pour 350 questions)
ollama pull --help                        # Affiche l'aide complète
ollama pull <modèle> --show-progress      # Affiche la progression du téléchargement
ollama pull --update <modèle>             # Met à jour un modèle existant

# Liste/Suppression
ollama list                              # Liste tous les modèles locaux
ollama rm <modèle>                       # Supprime un modèle spécifique (ex: ollama rm mistral:7b)
ollama rm --all                          # ⚠️ Supprime TOUS les modèles locaux (à utiliser avec prudence)

################################################################################
# 2️⃣ EXÉCUTION ET INTERACTION ###################################################
################################################################################

# Mode Interactif
ollama run <modèle>                      # Lance un modèle en mode conversationnel (ex: ollama run llama3:8b)
ollama run <modèle> "<prompt>"           # Exécute une requête unique (ex: ollama run phi3:3.8b "Explique Docker")

# Options Avancées
ollama run <modèle> --verbose             # Active le mode verbeux (logs détaillés)
ollama run <modèle> --temperature 0.8    # Contrôle la créativité (0=précis, 1=créatif)
ollama run <modèle> --num-gpu 1           # Utilise 1 GPU pour l'inférence
ollama run <modèle> --num-threads 8       # Limite à 8 threads CPU
ollama run <modèle> --mirostat 2          # Améliore la cohérence des réponses
ollama run <modèle> --repeat_penalty 1.2  # Réduit les répétitions dans les réponses

################################################################################
# 3️⃣ SERVEUR OLLAMA ###########################################################
################################################################################

# Démarrage/Arrêt
ollama serve                             # Démarre le serveur Ollama (port 11434 par défaut)
ollama serve --host 0.0.0.0              # ⚠️ Autorise les connexions externes (attention sécurité)
ollama serve --port 11435                # Change le port par défaut
pkill -f ollama                          # Arrête le serveur (Kali Linux)

# Configuration
export OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models  # Chemin personnalisé pour les modèles
export OLLAMA_HOST=0.0.0.0:11434         # Définit l'hôte et le port
ollama serve --debug                     # Active le mode debug (logs étendus)

################################################################################
# 4️⃣ MODELFILES (Personnalisation) #############################################
################################################################################

# Exemple de Modelfile pour un assistant Kali Linux (à enregistrer sous kali_assistant.modelfile)
# FROM llama2:7b
# PARAMETER temperature 0.8
# SYSTEM "Expert en Kali Linux, spécialisé en sécurité et scripts shell. Réponds de manière concise et technique."

# Création du modèle personnalisé
ollama create kali_assistant -f kali_assistant.modelfile

################################################################################
# 5️⃣ API ET RÉSEAU #############################################################
################################################################################

# Requêtes API
curl http://localhost:11434/api/tags      # Liste les modèles disponibles via l'API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3:8b", "prompt": "Bonjour, explique-moi comment configurer un pare-feu sous Kali Linux"}'

# Sécurité Réseau
ollama serve --tls-key key.pem --tls-cert cert.pem  # Active le chiffrement TLS

################################################################################
# 6️⃣ PERFORMANCES ET DÉBOGAGE ##################################################
################################################################################

# Optimisation des performances
ollama run <modèle> --mirostat 2          # Meilleure cohérence des réponses
ollama run <modèle> --repeat_penalty 1.2  # Réduit les répétitions

# Débogage
journalctl -u ollama -f                  # Affiche les logs en temps réel (systemd)
ollama run <modèle> --verbose             # Active le mode verbeux pour un modèle spécifique

################################################################################
# 7️⃣ SCRIPTS PRÊTS À L'EMPLOI ###################################################
################################################################################

# Script 1: Analyser un fichier texte (ex: 350 questions)
#!/bin/bash
# Usage: ./analyse_doc.sh mon_fichier.txt "Ta question"
ollama run phi3:3.8b "Analyse ce fichier : \$(cat \$1) et réponds à : \$2" > "analyse_\$(date +%Y%m%d).md"

# Script 2: Générer une synthèse
#!/bin/bash
# Usage: ./synthese_doc.sh mon_fichier.txt
ollama run llama3:8b "Résume ce document en 5 points clés : \$(cat \$1)" > "synthese_\$(date +%Y%m%d).md"

# Script 3: Lister les modèles (filtré)
ollama list | grep -E "NAME|phi3:3.8b"     # Filtre un modèle spécifique

################################################################################
# 8️⃣ MODÈLES RECOMMANDÉS (Bruno Delnoz) ########################################
################################################################################

# | Modèle          | Taille (Go) | Tokens Max | Usage Recommandé                          | Commande               |
# |-----------------|-------------|------------|-------------------------------------------|-------------------------|
# | phi3:3.8b       | 2.3          | 128,000    | Documents très longs (350 questions)       | ollama pull phi3:3.8b   |
# | mistral:7b      | 4.1          | 8,192      | Scripts Kali Linux                       | ollama pull mistral:7b  |
# | codellama:34b   | 20           | 32,000     | Analyse de code                          | ollama pull codellama:34b|
# | dbrx:132b       | 240          | 128,000    | Analyse de très longs documents          | ollama pull dbrx:132b   |

################################################################################
# 9️⃣ ERREURS COURANTES ET SOLUTIONS #############################################
################################################################################

# Permission denied sur /mnt/data1_100g/
sudo chown -R nox\:nox /mnt/data1_100g/agent_llm_local/models/

# Port 11434 déjà utilisé
sudo fuser -k 11434/tcp                  # Libère le port
ollama serve --port 11435                # Change de port

# Modèle corrompu
ollama rm <modèle>                       # Supprime le modèle corrompu
ollama pull <modèle>                      # Réinstalle le modèle

################################################################################
# 🔄 SCRIPT COMPLET (Bruno Delnoz) ###############################################
################################################################################

#!/bin/bash
# Script: ollama_tools.sh
# Auteur: Bruno Delnoz (nox@casablanca)
# Usage: ./ollama_tools.sh {download|analyze|list|server} [args]

# Fonctions
download_model() { ollama pull "\$1"; }
analyze_file() { ollama run phi3:3.8b "Analyse \$(cat \$1)" > "analyse_\$(date +%Y%m%d).md"; }
list_models() { ollama list; }
start_server() {
  export OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models
  ollama serve --host 0.0.0.0 --port 11434
}

# Gestion des arguments
case "\$1" in
  download) download_model "\$2" ;;
  analyze) analyze_file "\$2" ;;
  list) list_models ;;
  server) start_server ;;
  *) echo "Usage: \$0 {download|analyze|list|server} [args]"; exit 1 ;;
esac
