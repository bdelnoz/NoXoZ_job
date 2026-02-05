cd /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job

echo "fastapi>=0.95.0" >> requirements.txt
echo "uvicorn>=0.21.0" >> requirements.txt
echo "chromadb>=0.4.0" >> requirements.txt
echo "python-docx>=0.8.11" >> requirements.txt
echo "pydantic>=1.10.0" >> requirements.txt

mkdir -p 2_Sources/2.1_Python/api/endpoints
mkdir -p 2_Sources/2.1_Python/services
touch 2_Sources/2.1_Python/api/{__init__.py,dependencies.py,router.py}
touch 2_Sources/2.1_Python/api/endpoints/{upload.py,generate.py,status.py}
touch 2_Sources/2.1_Python/services/{ingestion.py,vector_store.py,generation.py}

pip install fastapi uvicorn python-multipart pydantic pandas sqlalchemy python-docx PyPDF2 chromadb
pip install pdfplumber lxml markdown
