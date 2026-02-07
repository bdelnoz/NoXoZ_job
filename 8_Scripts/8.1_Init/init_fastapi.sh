#!/bin/bash
# PATH: /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.1_Init/init_fastapi.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Initialisation complète FastAPI avec fichiers, contenu minimal, requirements.txt et checks existants
# Version: v4.0 - Date: 2026-02-05
# ------------------------------------------------------------------------------

BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
SRC_DIR="$BASE_DIR/2_Sources/2.1_Python"
REQ_FILE="$BASE_DIR/requirements.txt"

EXEC=false
SIMULATE=false
PREREQUIS=false
INSTALL=false
REPLACE_ALL=false

# Gestion arguments
for arg in "$@"; do
    case $arg in
        --help|-h)
            echo "Usage: $0 [--exec] [--simulate] [--prerequis] [--install]"
            echo "Options lors des diff : r = replace, sk = skip, ra = replace all restant"
            exit 0
            ;;
        --exec|-exe) EXEC=true ;;
        --simulate|-s) SIMULATE=true ;;
        --prerequis|-pr) PREREQUIS=true ;;
        --install|-i) INSTALL=true ;;
        *) echo "Argument inconnu : $arg"; exit 1 ;;
    esac
done

# Vérification prérequis
if [ "$PREREQUIS" = true ]; then
    echo "[CHECK] Vérification des prérequis..."
    command -v pipenv >/dev/null 2>&1 || echo "[WARN] pipenv non installé"
    command -v python3 >/dev/null 2>&1 || echo "[WARN] Python3 non trouvé"
    exit 0
fi

# Installation prérequis
if [ "$INSTALL" = true ]; then
    echo "[INSTALL] Installation des prérequis..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
    pip install pipenv
    exit 0
fi

# cd vers racine
cd "$BASE_DIR" || { echo "Erreur cd"; exit 1; }

# pipenv
echo "[INFO] Activation pipenv shell"
pipenv shell

# requirements.txt
echo "[INFO] Création/maj $REQ_FILE"
cat > "$REQ_FILE" <<'EOF'
fastapi>=0.95.0
uvicorn>=0.21.0
chromadb>=0.4.0
python-docx>=0.8.11
pydantic>=1.10.0
python-multipart
pandas
sqlalchemy
pypdf
pdfplumber
lxml
markdown
langchain
chromadb
unstructured
python-docx
pypdf
EOF

# Installation dépendances
echo "[INFO] Installation des dépendances via requirements.txt"
pip install -r "$REQ_FILE"

# Fichiers + contenu
declare -A FILES_CONTENT

FILES_CONTENT["$SRC_DIR/main_agent.py"]='from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:11111"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)'

FILES_CONTENT["$SRC_DIR/api/__init__.py"]=''
FILES_CONTENT["$SRC_DIR/api/dependencies.py"]='# Placeholder pour dépendances FastAPI'

FILES_CONTENT["$SRC_DIR/api/router.py"]='from fastapi import APIRouter
from .endpoints import upload, generate, status

router = APIRouter()
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(generate.router, prefix="/generate", tags=["Génération"])
router.include_router(status.router, prefix="/status", tags=["Statut"])'

FILES_CONTENT["$SRC_DIR/api/endpoints/upload.py"]='from fastapi import APIRouter, UploadFile, File
from services.ingestion import parse_and_store_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    result = await parse_and_store_file(file)
    return {"status": "success", "filename": file.filename, "result": result}'

FILES_CONTENT["$SRC_DIR/api/endpoints/generate.py"]='from fastapi import APIRouter, Form
from services.generation import generate_document

router = APIRouter()

@router.post("/")
def generate_doc(prompt: str = Form(...), template: str = Form("default")):
    doc_path = generate_document(prompt, template)
    return {"status": "success", "file_path": doc_path}'

FILES_CONTENT["$SRC_DIR/api/endpoints/status.py"]='from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_status():
    status = {"api":"online","llm":"running","chroma":"available"}
    return status'

FILES_CONTENT["$SRC_DIR/services/ingestion.py"]='async def parse_and_store_file(file):
    filename = file.filename
    return f"Fichier {filename} reçu et prêt à être traité"'

FILES_CONTENT["$SRC_DIR/services/generation.py"]='def generate_document(prompt: str, template: str = "default"):
    filename = f"output_{template}.docx"
    return f"Document {filename} généré avec le prompt: {prompt}"'

FILES_CONTENT["$SRC_DIR/services/vector_store.py"]='# Placeholder pour interactions avec Chroma Vector Store + SQLite'

# Création dossiers
mkdir -p "$SRC_DIR/api/endpoints" "$SRC_DIR/services"

CREATED=(); REPLACED=(); SKIPPED=()

for FILE in "${!FILES_CONTENT[@]}"; do
    CONTENT="${FILES_CONTENT[$FILE]}"
    if [ -f "$FILE" ]; then
        DIFF=$(diff <(echo "$CONTENT") "$FILE")
        if [ -z "$DIFF" ]; then
            SKIPPED+=("$FILE")
        else
            echo "-------------------------"
            echo "Diff trouvé pour $FILE :"
            echo "$DIFF"
            if [ "$SIMULATE" = true ]; then
                echo "[SIMULATE] Remplacement proposé pour $FILE (non exécuté)"
                REPLACED+=("$FILE")
            else
                if [ "$REPLACE_ALL" = true ]; then
                    echo "$CONTENT" > "$FILE"
                    REPLACED+=("$FILE")
                else
                    echo "Remplacer (r), skip (sk), replace all restant (ra)? [r/sk/ra]"
                    read -r CHOICE
                    if [ "$CHOICE" = "r" ]; then
                        echo "$CONTENT" > "$FILE"
                        REPLACED+=("$FILE")
                    elif [ "$CHOICE" = "ra" ]; then
                        echo "$CONTENT" > "$FILE"
                        REPLACED+=("$FILE")
                        REPLACE_ALL=true
                    else
                        SKIPPED+=("$FILE")
                    fi
                fi
            fi
        fi
    else
        if [ "$SIMULATE" = true ]; then
            echo "[SIMULATE] Création proposée de $FILE"
            CREATED+=("$FILE")
        else
            echo "$CONTENT" > "$FILE"
            CREATED+=("$FILE")
        fi
    fi
done

# résumé final
echo "==========================="
echo "Résumé des actions :"
echo "Créés : ${#CREATED[@]}"
for f in "${CREATED[@]}"; do echo "  - $f"; done
echo "Remplacés : ${#REPLACED[@]}"
for f in "${REPLACED[@]}"; do echo "  - $f"; done
echo "Skipped : ${#SKIPPED[@]}"
for f in "${SKIPPED[@]}"; do echo "  - $f"; done
echo "==========================="
echo "[INFO] Initialisation FastAPI terminée avec structure, fichiers et requirements.txt"
