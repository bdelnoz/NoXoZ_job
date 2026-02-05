NoXoZ_job/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD
├── scripts/
│   ├── old_versions/           # Anciennes versions des scripts (pour changelog)
│   │   └── all_my_scripts.old_versions.txt
│   ├── setup_agent_llm.sh       # Script de setup principal
│   └── create-repo.sh          # Script pour créer des dépôts Git (à corriger)
├── src/
│   ├── main_agent.py            # Code principal de l'agent LLM
│   ├── WHY.MD                  # Motivations du projet
│   ├── README.md                # Documentation utilisateur
│   ├── CHANGELOG.md             # Historique des modifications
│   └── INSTALL.MD               # Guide d'installation
├── data/
│   ├── vectors/                 # Stockage des embeddings (Chroma)
│   └── metadata.db              # Base de données SQLite
├── docker-compose.yml           # Configuration Docker
├── requirements.txt             # Dépendances Python
└── outputs/                     # Fichiers générés (CV, lettres, etc.)
