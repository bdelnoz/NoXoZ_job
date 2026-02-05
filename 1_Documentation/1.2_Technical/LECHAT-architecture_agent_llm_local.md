
# Architecture Complète pour un Agent Local d'AI de Gestion de Carrière

## Contexte
Ce document décrit l'architecture d'un agent local d'AI conçu pour ingérer, analyser et générer des documents professionnels (CV, lettres de motivation, emails) à partir de données personnelles et d'historiques de chat. L'objectif est de déployer cet agent dans un environnement local, avec une architecture modulaire, réutilisable et open-source.

---

## Objectifs
- **Ingestion de données** : CV, exports de chats (Le Chat, ChatGPT, Grok, Claude)
- **Génération de documents** : Lettres de motivation, CV personnalisés, emails
- **Déploiement local** : Utilisation de VirtualBox pour la virtualisation
- **Modularité** : Pipelines, API, base de données
- **Open-source** : Tous les codes et scripts seront hébergés sur un dépôt GitHub nommé `NoXoZ_job`

---

## Architecture Technique

### 1. Environnement de Déploiement
- **Localisation** : `/mnt/data1_100g/agent_llm_local/`
- **Virtualisation** : VirtualBox pour encapsuler l'environnement
- **Système d'exploitation** : Linux (Ubuntu/Debian recommandé)

### 2. Composants Principaux

#### a. Base de Données
- **Type** : PostgreSQL (open-source, robuste, support JSON)
- **Utilisation** : Stocker les CV, historiques de chat, métadonnées des documents
- **Schémas** :
  - `cv` : (id, contenu, format, date_creation)
  - `chat_history` : (id, plateforme, contenu, date)
  - `generated_docs` : (id, type, contenu, date_generation)

#### b. Moteur d'AI Local
- **Modèle** : Utilisation de Mistral AI (ou Llama 2) en local avec `llama.cpp` ou `transformers`
- **Fonctionnalités** :
  - Ingérer et analyser les fichiers (.md, .docx, .pdf, .json, .xml)
  - Générer des documents personnalisés
  - API pour interagir avec le modèle

#### c. Pipelines de Traitement
- **Ingestion** : Scripts Python pour parser et stocker les fichiers dans la base de données
- **Analyse** : Utilisation de NLP pour extraire les compétences, expériences, etc.
- **Génération** : Templates pour créer des lettres de motivation, CV, emails

#### d. API
- **Framework** : FastAPI (léger, performant, open-source)
- **Endpoints** :
  - `/upload` : Pour uploader des fichiers
  - `/generate` : Pour générer des documents
  - `/query` : Pour interroger la base de données

#### e. Interface Utilisateur (Optionnelle)
- **Type** : CLI ou interface web simple (Flask/Django)
- **Fonctionnalités** :
  - Sélectionner des fichiers à ingérer
  - Choisir le type de document à générer
  - Visualiser les résultats

---

### 3. Workflow

1. **Ingestion** :
   - L'utilisateur upload un fichier (CV, historique de chat)
   - Le pipeline parse le fichier et stocke les données dans la base de données

2. **Analyse** :
   - Le moteur d'AI analyse le contenu pour extraire les informations pertinentes

3. **Génération** :
   - L'utilisateur spécifie le type de document à générer (lettre de motivation, CV, email)
   - Le moteur d'AI génère le document en utilisant les données stockées

4. **Export** :
   - Le document généré est exporté dans le format souhaité (.docx, .md, .pdf)

---

### 4. Technologies et Outils

| Composant          | Technologie/Outils                          |
|--------------------|---------------------------------------------|
| Base de données    | PostgreSQL                                  |
| Moteur d'AI        | Mistral AI, Llama 2, `llama.cpp`, `transformers` |
| Backend            | FastAPI                                    |
| Pipelines          | Python, Pandas, NLTK, spaCy                 |
| Virtualisation     | VirtualBox                                 |
| Versioning         | Git, GitHub                                |
| Formats supportés  | .md, .docx, .pdf, .json, .xml              |

---

### 5. Structure du Dépôt GitHub (`NoXoZ_job`)

```bash
NoXoZ_job/
├── README.md
├── requirements.txt
├── config/
│   └── database_config.ini
├── scripts/
│   ├── ingestion/
│   ├── analysis/
│   └── generation/
├── api/
│   └── main.py
├── models/
│   └── llm/
└── docs/
    └── architecture.md
```

---

### 6. Étapes de Déploiement

1. **Installer VirtualBox** : Créer une machine virtuelle avec Linux.
2. **Configurer l'environnement** : Installer PostgreSQL, Python, et les dépendances.
3. **Cloner le dépôt** : `git clone https://github.com/NoXoZ_job.git`
4. **Configurer la base de données** : Créer les schémas et tables.
5. **Lancer l'API** : `uvicorn api.main:app --reload`
6. **Tester l'ingestion et la génération** : Utiliser les scripts fournis.

---

### 7. Exemple de Code

#### a. Script d'Ingestion (Python)
```python
import pandas as pd
from sqlalchemy import create_engine

def ingest_cv(file_path, db_uri):
    # Lire le fichier (exemple pour .csv)
    data = pd.read_csv(file_path)
    # Connexion à la base de données
    engine = create_engine(db_uri)
    # Stocker dans la base de données
    data.to_sql('cv', engine, if_exists='append', index=False)
```

#### b. API FastAPI
```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Logique pour traiter le fichier
    return {"filename": file.filename}
```

---

### 8. Perspectives d'Amélioration
- Ajouter une interface utilisateur graphique
- Intégrer plus de modèles d'AI locaux
- Automatiser les tests et le déploiement

---

## Conclusion
Cette architecture propose une solution complète, modulaire et open-source pour gérer localement la génération de documents professionnels. Tous les composants sont conçus pour être réutilisables et déployables dans un environnement VirtualBox.

---

**Auteur** : Bruno Delnoz
**Date** : 04/02/2026
