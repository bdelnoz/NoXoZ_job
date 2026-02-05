# GUIDE RAPIDE MODÈLES OLLAMA

## MISTRAL (4.1GB chacun)
**mistral:latest** | **mistral:7b**
- Usage: Général français/anglais, conversations, rédaction
- Fort: Excellent en français, raisonnement solide
- Commande: `ollama run mistral "ta question"`

## LLAMA 3.2 (2GB chacun)
**llama3.2:latest** | **llama3.2:3b**
- Usage: Conversations rapides, tâches légères
- Fort: Rapide, peu gourmand, bon généraliste
- Commande: `ollama run llama3.2 "ta question"`

## CODELLAMA (3.8GB)
**codellama:7b**
- Usage: Génération code, debug, explications techniques
- Fort: Python, JavaScript, bash, SQL
- Commande: `ollama run codellama "écris fonction python pour..."`

## GEMMA2 (1.6GB)
**gemma2:2b**
- Usage: Petit, rapide, multitâche basique
- Fort: Efficacité/taille, conversations courtes
- Commande: `ollama run gemma2:2b "question simple"`

## QWEN 2.5 (1.9GB)
**qwen2.5:3b**
- Usage: Multilingue, maths, raisonnement
- Fort: Chinois/anglais, calculs, logique
- Commande: `ollama run qwen2.5:3b "problème maths"`

## DEEPSEEK-R1 (4.4GB et 4.7GB)
**deepseek-r1:7b** | **deepseek-r1:8b**
- Usage: Raisonnement complexe, résolution problèmes
- Fort: Analyse étape par étape, logique avancée
- Commande: `ollama run deepseek-r1:7b "raisonne sur..."`

## PHI3 (2.3GB et 7.9GB)
**phi3:mini** | **phi3:medium**
- Usage: Efficace qualité/taille, tâches variées
- Fort: Mini=rapide, Medium=précis
- Commande: `ollama run phi3:mini "question"`

## ORCA-MINI (1.9GB)
**orca-mini:3b**
- Usage: Conversations naturelles compactes
- Fort: Dialogues fluides, peu de ressources
- Commande: `ollama run orca-mini "discutons de..."`

## NEURAL-CHAT (4.1GB)
**neural-chat:7b**
- Usage: Chat optimisé, assistant conversationnel
- Fort: Réponses structurées, tonalité adaptée
- Commande: `ollama run neural-chat "aide-moi à..."`

## STARLING-LM (4.1GB)
**starling-lm:7b**
- Usage: Chat haute qualité, instructions précises
- Fort: Suivi instructions, réponses détaillées
- Commande: `ollama run starling-lm "explique..."`

## SOLAR (6.1GB)
**solar:10.7b**
- Usage: Raisonnement avancé, tâches complexes
- Fort: Plus gros modèle, meilleures performances
- Commande: `ollama run solar "analyse complexe..."`

---

## CONSEILS UTILISATION

**Pour coder**: codellama, deepseek-r1
**Pour français**: mistral
**Pour rapidité**: gemma2, llama3.2, phi3:mini
**Pour qualité**: solar, phi3:medium, starling-lm
**Pour raisonnement**: deepseek-r1, solar, qwen2.5
**Pour conversations**: neural-chat, orca-mini, mistral

**Commande générique**:
```bash
ollama run <modele> "ta question ou prompt"
```

**Lister modèles installés**:
```bash
ollama list
```
