
# Plan Détaillé des Étapes Techniques
*Bruno Delnoz – Projet LLM & Document Ingestion*
*Dernière mise à jour : 07/02/2026*

---

## **1. LLM Engine & Document Ingestion**
### **1.1. Ollama (Mistral-7B)**
- **Vérification du service**
  ```bash
  systemctl status ollama.service
  sudo systemctl start ollama.service
  journalctl -u ollama.service -f
  ```
- **Test de génération**
  ```bash
  ollama run mistral-7b "Test prompt"
  ```
- **Vérification des modèles**
  ```bash
  ollama list
  ls /mnt/data1_100g/agent_llm_local/models/mistral-7b/
  ```
- **Résolution des dépendances**
  ```bash
  ollama pull mistral-7b
  ldd $(which ollama)
  ```

### **1.2. Mixtral**
- **Compatibilité multi-modèles**
  ```bash
  ollama run mixtral
  ```
- **Tests de génération**
  ```bash
  ollama run mixtral "Test parallel prompt"
  ```

### **1.3. Document Loaders**
- **JSON/XML Loader**
  ```bash
  python test_json_loader.py
  ```
- **MD/DOCX/PDF Loader**
  ```bash
  python test_md_loader.py
  python test_docx_loader.py
  python test_pdf_loader.py
  ```

---

## **2. Vector Store**
### **2.1. Chroma Vector DB**
- **Initialisation**
  ```bash
  chroma run --path /mnt/data1_100g/chroma_db
  ```
- **Tests de persistance**
  ```bash
  python test_chroma_persistence.py
  ```

### **2.2. SQLite Metadata**
- **Initialisation**
  ```bash
  bash init_sqlite.sh
  ```
- **Tests de récupération**
  ```bash
  python test_sqlite_metadata.py
  ```

---

## **3. Agent Logic (ReAct + Pipelines)**
- **Compléter le code de décision/action**
  ```bash
  python agent_logic.py
  ```
- **Tests unitaires**
  ```bash
  python test_react_logic.py
  ```

---

## **4. API Layer (FastAPI)**
- **Vérification des endpoints**
  ```bash
  curl http://localhost:8000/upload
  curl http://localhost:8000/generate
  ```
- **Tests de charge**
  ```bash
  bash test_fastapi.sh
  ```

---

## **5. Output Generation**
- **Installation des dépendances**
  ```bash
  sudo apt install pandoc
  pip install python-docx
  ```
- **Tests de génération**
  ```bash
  python test_output_generation.py
  ```

---

## **6. Interface Web locale**
- **Intégration avec l’API**
  ```bash
  python frontend/index.html
  ```
- **Dashboard**
  ```bash
  python dashboard.py
  ```

---

## **7. Logging & Sécurité**
- **Finaliser log_manager.py**
  ```bash
  python log_manager.py
  ```
- **Permissions**
  ```bash
  chown -R user:group /mnt/data1_100g/
  chmod 700 /mnt/data1_100g/agent_llm_local/
  ```

---

## **8. Deployment**
- **Docker Compose**
  ```bash
  docker-compose up -d
  ```
- **Scripts d’initialisation**
  ```bash
  bash start_all.sh
  ```

---

## **9. Templates & CI/CD**
- **Création des modèles**
  ```bash
  python create_templates.py
  ```
- **Workflow CI/CD**
  ```yaml
  # .github/workflows/test_deploy.yml
  name: Test & Deploy
  on: [push]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - run: python -m pytest
  ```

---

# Annexe : CSV des Composants
*Mise à jour : 07/02/2026*

```csv
Composant Principal,Sub‑Composant / Module,Rôle / Fonction spécifique,Installation,Configuration,Testing / Création,Validation,E2E Validation,Détails Techniques / Fichiers & Folders
LLM Engine,Ollama (Mistral-7B),Inférence principale,prompt → réponse,Done,Done,Done,Done,Modèles: /mnt/data1_100g/agent_llm_local/models/mistral-7b/
LLM Engine,Mixtral,Variante LLM pour tests multi-modèles,Done,Done,Done,Todo,Modèles: /mnt/data1_100g/agent_llm_local/models/mixtral/
Document Ingestion,PDF Loader,Parsing PDF,extraction texte et métadonnées,Done,Done,Done,Done,Script: 2_Sources/2.1_Python/loaders/pdf_loader.py
Document Ingestion,DOCX Loader,Parsing DOCX,extraction texte et métadonnées,Done,Done,Done,Done,Script: 2_Sources/2.1_Python/loaders/docx_loader.py
Document Ingestion,MD Loader,Parsing Markdown,Done,Done,Done,Todo,Script: 2_Sources/2.1_Python/loaders/md_loader.py
```

