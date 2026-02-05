# NoXoZ_job

Agent LLM local pour l’ingestion, l’analyse et la génération de documents professionnels, **100 % hors cloud**, sécurisé et modulaire.

---

## Objectif du projet

NoXoZ_job est conçu pour fournir un **agent intelligent local**, capable de :

* Ingérer et analyser des données personnelles (CV, conversations, documents, exports de chats).
* Raisonner sur ces données via un LLM local puissant.
* Générer des documents professionnels personnalisés (.docx, .md, .pdf).
* Fonctionner entièrement hors ligne, sous contrôle total de l’utilisateur.
* Être réutilisable dans différents environnements, y compris VirtualBox.

Le projet met l’accent sur **robustesse, modularité et durabilité**, adapté à un usage personnel ou professionnel sensible.

---

## Principes clés

* Exécution 100 % locale
* Pas de dépendances cloud
* Contrôle complet des données par l’utilisateur
* Architecture modulaire et évolutive
* Installation et configuration entièrement scriptées pour réutilisation

---

## Interface Web Locale

Le projet inclut une **interface web locale**, accessible uniquement sur la machine hôte.

### Accès

* Adresse fixe : `http://127.0.0.1:11111`
* Accessible uniquement depuis la machine locale

### Fonctionnalités – Version initiale (MVP)

* Page web minimaliste avec :

  * Champ de saisie pour le prompt utilisateur
  * Bouton **Send** pour envoyer le prompt à l’API FastAPI
  * Affichage dynamique de la réponse générée par le LLM

### Évolutions prévues

* Sélection dynamique des modèles Ollama disponibles
* Upload multi-fichiers pour CV, historiques de chat, documents
* Boutons de contrôle des composants :

  * Redémarrage Ollama
  * Redémarrage API
  * Rechargement de la base vectorielle
* Statut en temps réel des composants : API, Ollama, Chroma
* Historique des interactions pour suivi et audit
* Interface web locale sécurisée, **aucune exposition publique**

---

## Objectifs & Fonctionnalités clés

* **GitHub** : [https://github.com/bdelnoz/NoXoZ_job.git](https://github.com/bdelnoz/NoXoZ_job.git)
* **Local repo** : `/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job`
* **OLLAMA_MODELS** : `/mnt/data1_100g/agent_llm_local/models`
* 100 % local et offline après installation
* Ingestion de données : CV, exports de chats (Le Chat, ChatGPT, Grok, Claude)
* Fichiers supportés : `.md`, `.docx`, `.pdf`, `.json`, `.xml`
* Génération documentaire : lettres de motivation, CV personnalisés, emails
* Formats de sortie : `.docx`, `.md`, `.pdf`
* API RESTful FastAPI
* Base de données : SQLite + Chroma pour les embeddings
* Déploiement : local natif, VirtualBox, Docker Compose
* Pipeline CI/CD : GitHub Actions
* Installation et configuration entièrement scriptées pour réutilisation
* OS cible : Linux Kali / Debian

---

## Composants Clés

| Composant                 | Technologie                                             | Rôle                                            |
| ------------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| **LLM Engine**            | Ollama (Mistral-7B, Mixtral)                            | Inférence locale du modèle de langage           |
| **Document Ingestion**    | LangChain Loaders                                       | Parsing des fichiers (PDF, DOCX, MD, JSON, XML) |
| **Vector Store**          | Chroma                                                  | Stockage persistant des embeddings sur disque   |
| **Agent Logic**           | LangChain (ReAct)                                       | Raisonnement et actions basées sur les données  |
| **API Layer**             | FastAPI                                                 | Endpoints upload, requêtes et génération        |
| **DB**                    | SQLite + Chroma                                         | Métadonnées utilisateur et stockage vectoriel   |
| **Output Generation**     | Pandoc, python-docx                                     | Conversion et génération de fichiers            |
| **Deployment**            | Docker Compose                                          | Conteneurisation pour local / VirtualBox        |
| **Storage big files**     | `/mnt/data1_100g/agent_llm_local/`                      | Stockage centralisé des gros volumes            |
| **Storage project files** | `/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job` | Stockage centralisé des fichiers du projet      |

---

## Architecture – Diagramme (Text-Based)

```text
+-------------+     +-------------+
| User Input  |     | GitHub Repo |
| (CLI / UI)  |<--->| NoXoZ_job   |
+-------------+     +-------------+
         |
         v
 +----------------+        +-------------+
 | FastAPI Server |<------>| CI/CD       |
 +----------------+        | Pipelines   |
         |                 +-------------+
         v
 +-----------------+
 | LangChain Agent |
 | (ReAct + Tools) |
 +-----------------+
         |
         v
 +-----------------+     +----------------------+
 | Ollama LLM      |<--->| Chroma Vector Store  |
 | (Mistral-7B)    |     | + SQLite Metadata   |
 +-----------------+     +----------------------+
         |
         v
 +-----------------+
 | Document Loaders|
 | (.md/.docx/etc) |
 +-----------------+
         |
         v
 +-----------------+
 | Output Generators|
 | (Pandoc / Docx) |
 +-----------------+

Persistent Storage:
- /mnt/data1_100g/agent_llm_local/
- /mnt/data2_78g/.../NoXoZ_job
```

---

## Arborescence du projet

```
NoXoZ_job/
├── 1_Documentation/
│   ├── 1.1_General/
│   └── 1.2_Technical/
├── 2_Sources/
│   ├── 2.1_Python/
│   └── 2.2_Bash/
├── 3_Data/
│   ├── 3.1_Vectors/
│   └── 3.2_Metadata/
├── 4_Logs/
├── 5_Outputs/
│   ├── 5.1_DOCX/
│   └── 5.2_PDF/
├── 6_Results/
│   ├── 6.1_Bugs/
│   └── 6.2_Innovations/
├── 7_Infos/
├── 8_Scripts/
│   ├── 8.1_Init/
│   └── 8.2_Utils/
├── 9_Templates/
├── README.md
└── ARCHITECTURE.md
```

---

## Pipeline Fonctionnel

1. **Ingestion** : Upload et parsing des fichiers (CV, chats, docs) via API ou interface web.
2. **Analyse** : Extraction des informations clés avec NLP (compétences, expériences).
3. **Génération** : Templates et logique LLM pour créer documents (CV, lettres, emails).
4. **Export** : Formats `.docx`, `.md`, `.pdf`.

---

## Sécurité et Contrôle

* Contrôle d’accès utilisateur et rôle
* Isolation logique des agents pour éviter fuites de contexte
* Logging complet : prompts, réponses, modèles utilisés, actions
* Aucune exposition réseau externe par défaut

---

## Déploiement rapide (résumé)

1. Installer un Linux propre (VM ou machine dédiée)
2. Installer Python, Ollama, dépendances
3. Lancer Ollama et charger les modèles
4. Démarrer l’API FastAPI
5. Accéder à l’interface web sur `127.0.0.1:11111`

---

## Évolutions prévues

* Interface web avancée avec multi-modèles
* Upload multi-fichiers et batch processing
* Multi-agents spécialisés et orchestration avancée
* Matching automatique CV / offres
* Mémoire long terme enrichie pour suivi historique
* Tableau de bord avec statut en temps réel des composants

---

**Auteur** : Bruno Delnoz
**Date** : 04/02/2026
