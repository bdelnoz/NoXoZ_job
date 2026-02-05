# NoXoZ_job: Architecture Complète pour Agent LLM Local Gratuit

**Auteur**: Bruno Delnoz
**Date**: 2026-02-04
**Version**: 1.0
**Repo GitHub**: [NoXoZ_job](https://github.com/<ton_user>/NoXoZ_job)
**Dossier Local**: `/mnt/data1_100g/agent_llm_local/`

---

## Aperçu Général

Ce projet propose une **architecture 100% locale et gratuite** pour un agent LLM capable d’ingérer tes CV, exports de chats (Le Chat, ChatGPT, Grok, Claude), et générer des documents personnalisés (lettres de motivation, CV, mails de réponse aux offres d’emploi). L’objectif est de déployer ce système via des pipelines CI/CD (GitHub Actions) et de le rendre réutilisable dans une VM VirtualBox.

**Fonctionnalités clés**:
- **Ingestion de fichiers**: `.md`, `.docx`, `.pdf`, `.json`, `.xml`
- **Génération de documents**: `.docx`, `.md`, `.pdf`
- **API RESTful** (FastAPI) pour interagir avec l’agent
- **Base de données** (SQLite + Chroma pour les embeddings)
- **Déploiement conteneurisé** (Docker Compose)
- **Pipeline CI/CD** (GitHub Actions)
- **100% local et offline** après le setup initial

---

## Composants Clés

| Composant          | Technologie               | Rôle                                                                 |
|--------------------|---------------------------|----------------------------------------------------------------------|
| **LLM Engine**     | Ollama (Mistral-7B)       | Inférence locale du modèle de langage (gratuit, téléchargeable)     |
| **Document Ingestion** | LangChain Loaders     | Parsing des fichiers (PDF, DOCX, MD, JSON, XML)                     |
| **Vector Store**   | Chroma                    | Stockage persistant des embeddings sur disque                      |
| **Agent Logic**    | LangChain (ReAct)         | Raisonnement et actions (génération de docs basés sur les données) |
| **API Layer**      | FastAPI                   | Endpoints pour upload, requêtes et génération de documents          |
| **DB**            | SQLite + Chroma           | Métadonnées utilisateur et stockage vectoriel                      |
| **Output Generation** | Pandoc, python-docx   | Conversion et génération de fichiers (MD → PDF/DOCX)               |
| **Deployment**     | Docker Compose            | Conteneurisation pour réutilisation en VBox                        |
| **Storage**        | `/mnt/data1_100g/agent_llm_local/` | Stockage centralisé des données, modèles et vecteurs |

---

## Architecture Diagramme (Text-Based)

```text
+-------------+     +-------------+
| User Input  |     | GitHub Repo |
| (CLI/API)   |<--->| NoXoZ_job   |
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
