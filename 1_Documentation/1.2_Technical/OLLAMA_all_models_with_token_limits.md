# **Liste Exhaustive des Modèles Ollama**
*Dernière mise à jour : 2026-02-05*
*Format : Markdown (pour intégration directe dans la documentation technique de Bruno Delnoz)*

---

## **1. Modèles Généraux (Text Generation)**

| **Modèle**               | **Taille (Go)** | **Commande `ollama pull`**       | **Tokens Max** | **Usage Recommandé**                     |
|--------------------------|-----------------|-----------------------------------|----------------|------------------------------------------|
| **phi3:3.8b**            | 2.3             | `ollama pull phi3:3.8b`          | 128,000         | Documents très longs, contexte étendu    |
| **phi3:mini**            | 1.8             | `ollama pull phi3:mini`          | 128,000         | Léger et efficace                        |
| **llama3:8b**            | 4.7             | `ollama pull llama3:8b`          | 8,192           | Usage général, raisonnement              |
| **llama3:70b**           | 42              | `ollama pull llama3:70b`         | 32,000          | Raisonnement profond, tâches complexes    |
| **llama2:7b**            | 3.8             | `ollama pull llama2:7b`          | 4,096           | Usage général                            |
| **llama2:13b**           | 7.5             | `ollama pull llama2:13b`         | 4,096           | Tâches plus complexes                    |
| **llama2:70b**           | 42              | `ollama pull llama2:70b`         | 4,096           | Usage avancé                             |
| **mistral:7b**           | 4.1             | `ollama pull mistral:7b`          | 8,192           | Rapidité, documents techniques            |
| **mixtral:8x7b**         | 26              | `ollama pull mixtral:8x7b`        | 32,000          | Équilibre performance/ressources          |
| **mixtral:8x22b**        | 64              | `ollama pull mixtral:8x22b`       | 64,000          | Analyse complexe, multilingue            |
| **gemma:2b**             | 1.4             | `ollama pull gemma:2b`            | 8,192           | Léger et efficace                        |
| **gemma:7b**             | 4.8             | `ollama pull gemma:7b`            | 8,192           | Usage général léger                      |
| **gemma2:9b**            | 5.4             | `ollama pull gemma2:9b`          | 8,192           | Amélioration de gemma:7b                  |
| **dbrx:132b**            | 240             | `ollama pull dbrx:132b`          | 128,000         | Analyse de très longs documents           |
| **tinyllama:1.1b**       | 0.6             | `ollama pull tinyllama:1.1b`      | 2,048           | Tests rapides, environnements limités     |

---

## **2. Modèles Spécialisés (Code, Multilingue, etc.)**

| **Modèle**               | **Taille (Go)** | **Commande `ollama pull`**       | **Tokens Max** | **Usage Recommandé**                     |
|--------------------------|-----------------|-----------------------------------|----------------|------------------------------------------|
| **codellama:7b**         | 3.8             | `ollama pull codellama:7b`        | 8,192           | Analyse de code                          |
| **codellama:13b**        | 7.5             | `ollama pull codellama:13b`       | 8,192           | Code plus complexe                       |
| **codellama:34b**        | 20              | `ollama pull codellama:34b`       | 32,000          | Code complexe, raisonnement technique    |
| **deepseek-coder:1.3b**   | 0.8             | `ollama pull deepseek-coder:1.3b`  | 4,096           | Code léger                              |
| **deepseek-coder:6.7b**   | 4.0             | `ollama pull deepseek-coder:6.7b`  | 32,000          | Spécialisé pour le code                  |
| **deepseek-coder:33b**    | 19              | `ollama pull deepseek-coder:33b`   | 32,000          | Code avancé                              |
| **qwen:0.5b**            | 0.3             | `ollama pull qwen:0.5b`           | 2,048           | Multilingue léger                       |
| **qwen:1.8b**            | 1.1             | `ollama pull qwen:1.8b`           | 2,048           | Multilingue léger                       |
| **qwen:7b**              | 4.2             | `ollama pull qwen:7b`             | 32,000          | Multilingue (chinois, anglais, français) |
| **qwen:14b**             | 8.4             | `ollama pull qwen:14b`            | 32,000          | Multilingue avancé                      |
| **qwen:72b**             | 135             | `ollama pull qwen:72b`            | 32,000          | Multilingue avancé                      |
| **yi:6b**                | 3.5             | `ollama pull yi:6b`               | 32,000          | Documents techniques                     |
| **yi:34b**               | 20              | `ollama pull yi:34b`              | 32,000          | Analyse approfondie                      |
| **sqlcoder:7b**          | 3.8             | `ollama pull sqlcoder:7b`          | 8,192           | Spécialisé pour SQL                      |
| **starcoder:3b**         | 1.8             | `ollama pull starcoder:3b`         | 8,192           | Code et développement                    |
| **starcoder:7b**         | 4.2             | `ollama pull starcoder:7b`         | 8,192           | Code et développement                    |
| **starcoder2:3b**        | 1.8             | `ollama pull starcoder2:3b`        | 8,192           | Code et développement                    |
| **starcoder2:7b**        | 4.2             | `ollama pull starcoder2:7b`        | 16,384          | Code et développement                    |
| **starcoder2:15b**       | 8.5             | `ollama pull starcoder2:15b`       | 16,384          | Code et développement                    |
| **phind-codellama:34b**  | 20              | `ollama pull phind-codellama:34b`  | 32,000          | Code avancé                              |

---

## **3. Modèles Non Censurés (Dolphin)**

| **Modèle**               | **Taille (Go)** | **Commande `ollama pull`**       | **Tokens Max** | **Usage Recommandé**                     |
|--------------------------|-----------------|-----------------------------------|----------------|------------------------------------------|
| **dolphin-llama3:8b**    | 4.7             | `ollama pull dolphin-llama3:8b`   | 8,192           | Conversations libres, non censurées     |
| **dolphin-mistral:7b**   | 4.1             | `ollama pull dolphin-mistral:7b`  | 8,192           | Usage général non censuré               |
| **dolphin-mixtral:8x7b** | 26              | `ollama pull dolphin-mixtral:8x7b`| 32,000          | Analyse complexe non censurée           |

---

## **4. Modèles Légers (Faible Consommation)**

| **Modèle**               | **Taille (Go)** | **Commande `ollama pull`**       | **Tokens Max** | **Usage Recommandé**                     |
|--------------------------|-----------------|-----------------------------------|----------------|------------------------------------------|
| **tinyllama:1.1b**       | 0.6             | `ollama pull tinyllama:1.1b`      | 2,048           | Tests rapides, environnements limités  |
| **phi:2.7b**             | 1.6             | `ollama pull phi:2.7b`            | 2,048           | Petits projets, rapidité                |

---

## **5. Modèles Expérimentaux et MoE (Mixture of Experts)**

| **Modèle**               | **Taille (Go)** | **Commande `ollama pull`**       | **Tokens Max** | **Usage Recommandé**                     |
|--------------------------|-----------------|-----------------------------------|----------------|------------------------------------------|
| **mixtral:8x7b**         | 26              | `ollama pull mixtral:8x7b`        | 32,000          | Équilibre performance/ressources          |
| **mixtral:8x22b**        | 64              | `ollama pull mixtral:8x22b`       | 64,000          | Analyse complexe, multilingue            |

---

## **6. Notes et Recommandations**
### **6.1. Choix du Modèle**
- **Pour des documents très longs** (ex: 350 questions) : **`phi3:3.8b`** (128K tokens) ou **`dbrx:132b`** (128K tokens).
- **Pour du code** : **`deepseek-coder:6.7b`** ou **`codellama:34b`** (32K tokens).
- **Pour un usage léger** : **`tinyllama:1.1b`** ou **`phi:2.7b`**.

### **6.2. Commandes Utiles**
- **Lister les modèles téléchargés** :
  ```bash
  ollama list
