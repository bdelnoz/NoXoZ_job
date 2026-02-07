# NoXoZ_job – README

**Agent LLM local pour la gestion complète de documents professionnels, 100 % offline**

---

## Présentation générale

NoXoZ_job est un projet open-source visant à créer un **agent intelligent entièrement local**, capable d'ingérer, analyser et générer des documents professionnels à partir de diverses sources : CV, historiques de chat, fichiers Markdown, DOCX, PDF, JSON, XML, etc.

Ce système a été conçu pour être :

* **100 % hors cloud** : aucune donnée n’est envoyée à des serveurs externes.
* **Robuste et réutilisable** : architecture modulaire, scripts de configuration et conteneurisation via Docker pour déploiement local ou sur VirtualBox.
* **Extensible et évolutif** : pipelines et API conçus pour intégrer de nouveaux modèles LLM et fonctionnalités.
* **Sécurisé** : données sous contrôle complet de l’utilisateur, isolation des composants, logging complet.

Ce README est une ressource complète pour comprendre le projet, le déployer et l’utiliser.

---

## Objectifs du projet

* Fournir un **agent intelligent local** pour la génération de documents professionnels.
* Permettre l’**ingestion de données personnelles** depuis différentes sources.
* Fournir une **interface web locale simple et évolutive** pour interagir avec l’agent.
* Assurer une **réutilisabilité totale** via scripts, Docker, et VirtualBox.
* Faciliter la **modularité** et l’évolution future des pipelines et modèles.

---

## Fonctionnalités clés

* **Ingestion de fichiers** : CV, historiques de chat, documents personnels.
* **Formats supportés** : .md, .docx, .pdf, .json, .xml.
* **Analyse intelligente** : extraction des compétences, expériences et métadonnées.
* **Génération de documents** : lettres de motivation, CV personnalisés, emails.
* **Stockage vectoriel et sémantique** : Chroma + SQLite.
* **API RESTful** : endpoints FastAPI pour upload, génération, requêtes.
* **Interface web locale** : accessible uniquement sur `https://127.0.0.1:8443`.
* **Pipeline CI/CD** : automatisation avec GitHub Actions.
* **Déploiement conteneurisé** : Docker Compose pour isoler et réutiliser les composants.
* **Sécurité et contrôle** : isolation des agents, accès utilisateur/role, logging complet.

---

## Interface web locale

L’interface web est le point central de l’interaction avec l’agent.

### Version MVP

* Champ input pour prompt
* Bouton **Send** pour envoyer la requête
* Affichage du résultat généré par le LLM
* Fonctionne uniquement sur `https://127.0.0.1:8443`

### Évolutions prévues

* Sélection dynamique du modèle LLM
* Upload multiple de fichiers
* Boutons de contrôle : restart Ollama, API, reload de la base vectorielle
* Historique des prompts et réponses
* Statut des composants en temps réel
* Interface enrichie avec dashboard de monitoring

---

## Architecture détaillée

### Composants Clés

| Composant                 | Technologie                                             | Rôle                                                               |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
| **LLM Engine**            | Ollama (Mistral-7B, Mixtral)                            | Inférence locale du modèle de langage (gratuit, téléchargeable)    |
| **Document Ingestion**    | LangChain Loaders                                       | Parsing et ingestion de fichiers (PDF, DOCX, MD, JSON, XML)        |
| **Vector Store**          | Chroma                                                  | Stockage persistant des embeddings sur disque                      |
| **Agent Logic**           | LangChain (ReAct)                                       | Raisonnement, actions et génération de documents basés sur données |
| **API Layer**             | FastAPI                                                 | Endpoints pour upload, requêtes et génération de documents         |
| **DB**                    | SQLite + Chroma                                         | Métadonnées utilisateur et stockage vectoriel                      |
| **Output Generation**     | Pandoc, python-docx                                     | Conversion et génération de fichiers (MD → PDF/DOCX)               |
| **Deployment**            | Docker Compose                                          | Conteneurisation pour réutilisation et isolation des composants    |
| **Storage big files**     | `/mnt/data1_100g/agent_llm_local/`                      | Stockage centralisé des gros volumes                               |
| **Storage project files** | `/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job` | Stockage centralisé des fichiers projet GitHub                     |

### Architecture Diagramme (Text-Based)

```text
+-------------+     +-------------+
| User Input  |     | GitHub Repo |
| (CLI/Web)  |<--->| NoXoZ_job   |
+-------------+     +-------------+
         |                  ^
         v                  |
 +----------------+     +----------+
 | FastAPI Server |<--->| Pipelines|
 +----------------+     | (CI/CD)  |
         |              +----------+
         v
 +-----------------+
 | LangChain Agent |
 | (ReAct + Tools) |
 +-----------------+
         |
         v
 +-----------------+     +-----------------+
 | Ollama LLM      |<--->| Chroma Vector DB|
 | (Mistral-7B)    |     | + SQLite Meta   |
 +-----------------+     +-----------------+
         |                        |
         v                        v
 +-----------------+     +-----------------+
 | Doc Loaders     |     | Persistent Storage|
 | (.md/.docx/etc) |     | /mnt/data1_100g/ |
 +-----------------+     +-----------------+
         |
         v
 +-----------------+
 | Output Generators|
 | (Pandoc/Docx)   |
 +-----------------+
```

---

## Pipelines et workflow

1. **Ingestion** : upload des fichiers → parsing → stockage vectoriel et métadonnées
2. **Analyse** : extraction NLP des informations clés (compétences, expériences, dates, etc.)
3. **Génération** : création de documents via templates
4. **Export** : sortie des fichiers générés (.docx, .md, .pdf)
5. **Interface** : interaction via CLI ou interface web locale

### Sécurité et contrôle

* Contrôle d’accès par utilisateur et rôle
* Isolation des agents pour éviter les fuites de contexte
* Logging complet des interactions et des modèles utilisés
* Gestion des permissions pour accès aux modèles et aux fichiers

### Base de données et stockage

* **Type** : SQLite + Chroma pour embeddings
* **Schémas** :

  * `cv` : id, contenu, format, date_creation
  * `chat_history` : id, plateforme, contenu, date
  * `generated_docs` : id, type, contenu, date_generation
* Stockage sécurisé des fichiers et vecteurs dans `/mnt/data1_100g/agent_llm_local/`

### Composants techniques

| Composant         | Technologie/Outils                                              |
| ----------------- | --------------------------------------------------------------- |
| Base de données   | SQLite + Chroma                                                 |
| Moteur d'AI       | Ollama (Mistral, Mixtral), Llama 2, `transformers`, `llama.cpp` |
| Backend           | FastAPI                                                         |
| Pipelines         | Python, Pandas, NLTK, spaCy                                     |
| Virtualisation    | VirtualBox                                                      |
| Versioning        | Git, GitHub                                                     |
| Formats supportés | .md, .docx, .pdf, .json, .xml                                   |

---

## Arborescence complète du projet

```
NoXoZ_job/
├── 1_Documentation/
│   ├── General/
│   │   ├── INSTALL.docx
│   │   ├── WHY.docx
│   │   └── ollama-models-guide.md
│   └── Technical/
│       ├── API_SPECIFICATIONS.docx
│       ├── ARCHITECTURE.md
│       ├── LECHAT-architecture_agent_llm_local.md
│       ├── OLLAMA_all_models_with_token_limits.md
│       ├── OLLAMA_commandes.md
│       ├── structure.md
│       └── table.csv
├── 2_Sources/
│   ├── 2.1_Python/
│   │   └── main_agent.py
│   └── 2.2_Bash/
│       └── create_structure.sh
├── 3_Data/
│   ├── 3.1_Vectors/
│   │   ├── chroma_link -> /mnt/data1_100g/agent_llm_local/vectors
│   │   └── models_link -> /mnt/data1_100g/agent_llm_local/models
│   └── Metadata/
├── 4_Logs/
├── 5_Outputs/
│   ├── DOCX/
│   └── PDF/
├── 6_Results/
│   ├── Bugs/
│   └── Innovations/
├── 7_Infos/
│   └── PERMANENT_MEMORY.md
├── 8_Scripts/
│   ├── Init/
│   │   ├── config_paths.sh
│   │   ├── fix_ollama_group_permissions.sh
│   │   ├── logs/
│   │   ├── ollama-batch-download.sh
│   │   ├── reset_ollama_service.sh
│   │   └── results/
│   └── Utils/
│       └── count_tokens.sh
├── 9_Templates/
├── README.md
├── ARCHITECTURE.md
├── docker-compose.yml
├── Pipfile
├── Pipfile.lock
├── requirements.txt
└── start_ollama.sh
```

---

## Déploiement complet

1. Installer Linux (VM ou machine dédiée, Debian/Kali recommandé)
2. Installer Python et dépendances (Pipenv ou venv)
3. Installer Ollama et télécharger les modèles dans le dossier configuré
4. Configurer la base de données SQLite + Chroma
5. Lancer les scripts d'initialisation pour créer la structure et logs
6. Démarrer l’API FastAPI : `uvicorn main:app --reload --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem`
7. Accéder à l’interface web sur `https://127.0.0.1:8443`
8. Upload des fichiers, génération des documents, suivi du statut des composants

---

## Exemples de code

### Ingestion d’un CV

```python
import pandas as pd
from sqlalchemy import create_engine

def ingest_cv(file_path, db_uri):
    data = pd.read_csv(file_path)
    engine = create_engine(db_uri)
    data.to_sql('cv', engine, if_exists='append', index=False)
```

### Endpoint FastAPI

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Logic to parse and store the file
    return {"filename": file.filename}
```

---

## Perspectives et évolutions

* Interface web avancée avec dashboard et multi-modèles
* Contrôle et redémarrage des composants directement depuis le web
* Matching automatique CV / offres
* Mémoire long terme enrichie et multi-agents spécialisés
* Tests automatisés et pipelines CI/CD enrichis
* Support multi-OS et installation simplifiée via scripts et Docker

---

**Auteur** : Bruno Delnoz
**Date** : 04/02/2026
**Version** : 1.0
