
BASE_DIR="/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job"
REQ_FILE="$BASE_DIR/requirements.txt"


# cd vers racine
cd "$BASE_DIR" || { echo "Erreur cd"; exit 1; }

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
PyPDF2
pdfplumber
lxml
markdown
langchain
chromadb
unstructured
python-docx
PyPDF2
EOF

# Installation dépendances
echo "[INFO] Installation des dépendances via requirements.txt"
pip install -r "$REQ_FILE"
