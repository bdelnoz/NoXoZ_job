# Architecture Hybride – Agent LLM Local (Offline First)

## 1. Objectif du document

Ce document fusionne **le meilleur des deux architectures précédentes** :

* la **lisibilité, clarté conceptuelle et pédagogie** du document 1
* la **réalité opérationnelle, robustesse et maturité industrielle** du document 2

Le résultat est une **architecture unique, cohérente, réaliste et évolutive**, pensée pour un **agent LLM local autonome**, fonctionnant **offline**, capable d’ingérer, structurer, mémoriser et exploiter des connaissances personnelles (CV, chats, documents, historiques).

---

## 2. Principes fondateurs

* **Offline first** : aucune dépendance réseau après installation
* **LLM local réel** : `llama.cpp` comme moteur central
* **Mémoire longue durée** : embeddings + base relationnelle
* **Traçabilité totale** : logs, versions, pipelines reproductibles
* **Séparation claire des responsabilités** : ingestion, raisonnement, restitution

---

## 3. Vue d’ensemble de l’architecture

```
Utilisateur
   │
   ▼
Interface (CLI / Web UI légère)
   │
   ▼
API Locale (FastAPI)
   │
   ├── Orchestrateur Agent
   │       ├── Raisonnement LLM (llama.cpp)
   │       ├── Mémoire court terme (context window)
   │       └── Mémoire long terme (Vector DB)
   │
   ├── Base Relationnelle (SQLite)
   └── Base Vectorielle (Chroma)
```

---

## 4. Stack technologique retenue (choix optimisés)

### 4.1 Backend

* **Python 3.11+**
* **FastAPI** : API locale, rapide, typée
* **Uvicorn** : serveur ASGI

> Choix issu du doc 1 pour la clarté + doc 2 pour la robustesse

---

### 4.2 Moteur IA (cœur du système)

* **llama.cpp**
* Modèles **GGUF quantifiés** (Mistral, LLaMA, Mixtral selon usage)
* Exécution CPU prioritaire (GPU optionnel)

Rôle :

* génération de réponses
* raisonnement contextuel
* reformulation
* scoring sémantique

> Ici, le doc 2 est retenu sans concession : c’est la seule option réaliste offline.

---

### 4.3 Bases de données

#### Base relationnelle (mémoire structurée)

* **SQLite**
* Contient :

  * métadonnées documents
  * historique conversations
  * versions, sources, timestamps

Avantage : simplicité, portabilité, zéro serveur.

#### Base vectorielle (mémoire sémantique)

* **ChromaDB**
* Stocke :

  * embeddings de CV
  * embeddings de conversations
  * embeddings de documents divers

Permet :

* recherche par sens
* récupération de contexte pertinent

> Fusion directe des deux docs : PostgreSQL abandonné, trop lourd offline.

---

## 5. Pipelines de données

### 5.1 Ingestion

Sources possibles :

* CV (PDF, DOCX)
* Conversations ChatGPT / Mistral / autres
* Notes personnelles
* Documents techniques

Pipeline :

1. Extraction texte
2. Nettoyage / normalisation
3. Découpage en chunks
4. Génération d’embeddings
5. Indexation Chroma
6. Référencement SQLite

---

### 5.2 Exploitation

Lors d’une requête utilisateur :

1. Analyse de la question
2. Recherche sémantique (Chroma)
3. Sélection des chunks pertinents
4. Construction du prompt enrichi
5. Appel LLM local
6. Post-traitement et réponse

---

## 6. Orchestrateur Agent

Composant central chargé de :

* gérer le flux décisionnel
* choisir quand interroger la mémoire
* limiter le contexte
* tracer les raisonnements

Ce n’est **pas un simple chatbot**, mais un **agent avec mémoire**.

---

## 7. Interface utilisateur

### Options retenues

* **CLI avancée** (prioritaire)
* **Web UI minimale** (optionnelle)

  * HTML + JS simple
  * pas de framework lourd

Objectif : interaction rapide, locale, sans dépendance.

---

## 8. Déploiement

### Environnement

* Machine locale
* VM possible (VirtualBox)
* Docker Compose recommandé

### Stratégie

* installation unique online
* usage 100 % offline
* scripts reproductibles

---

## 9. CI / CD & maintenance

* Git pour versionnement
* GitHub Actions (si dépôt distant)
* Scripts de vérification locale

But :

* éviter la dérive
* garder un système propre

---

## 10. Sécurité et confidentialité

* Aucune donnée sortante
* Pas d’API cloud
* Données stockées localement
* Contrôle total utilisateur

---

## 11. Évolutions prévues

* Agents spécialisés (CV, carrière, technique)
* Scoring de confiance
* Mémoire hiérarchique
* Multi-modèles selon tâche

---

## 12. Conclusion

Cette architecture :

* garde la **clarté conceptuelle** du premier document
* assume la **réalité technique** du second

C’est une base **saine, crédible et durable** pour un agent LLM local sérieux.

Ce document doit devenir la **référence principale** du projet.
