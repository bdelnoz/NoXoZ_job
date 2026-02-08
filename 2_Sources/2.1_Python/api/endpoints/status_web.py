from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import httpx

router = APIRouter()

# Base directory pour tes scripts Python
BASE_DIR = Path(__file__).resolve().parents[2]  # remonte vers 2.1_Python

# Liste des fichiers Python à surveiller
PYTHON_FILES = [
    "api/dependencies.py",
    "api/router.py",
    "api/endpoints/generate.py",
    "api/endpoints/status.py",
    "api/endpoints/upload.py",
    "chroma_integration.py",
    "main_agent.py",
    "services/generation.py",
    "services/ingestion.py",
    "services/vector_store.py",
    "temp.py",
    "test_db_huffing.py",
    "test_sentence_transfomers.py"
]

# Endpoints health à tester
HEALTH_ENDPOINTS = [
    {"name": "Generate", "url": "https://127.0.0.1:8443/api/generate/health"},
    {"name": "Upload", "url": "https://127.0.0.1:8443/api/upload/health"},
    {"name": "Status", "url": "https://127.0.0.1:8443/api/status/health"},
    {"name": "WEB Status Page THIS PAGE !!!!!!!!!", "url": "https://127.0.0.1:8443/api/monitor/health"}
]

@router.get("/web_status", response_class=HTMLResponse)
async def web_status():
    results = []
    async with httpx.AsyncClient(verify=False) as client:
        for ep in HEALTH_ENDPOINTS:
            try:
                resp = await client.get(ep["url"], timeout=3)
                if resp.status_code == 200:
                    status = "✅ OK"
                else:
                    status = f"❌ {resp.status_code}"
            except Exception as e:
                status = f"❌ Error: {str(e)}"
            results.append({"name": ep["name"], "status": status})

    # Vérification des fichiers Python
    files_status = []
    for f in PYTHON_FILES:
        file_path = BASE_DIR / f
        files_status.append({
            "name": f,
            "status": "✅ Found" if file_path.exists() else "❌ Missing"
        })

    # Générer HTML
    html = """
    <html>
    <head>
    <title>Status Python et Endpoints</title>
    <style>
        body { font-family: monospace; background:#1e1e1e; color:#f0f0f0; }
        table { border-collapse: collapse; width: 80%; margin:auto; }
        th, td { border:1px solid #888; padding:8px; text-align:left; }
        th { background:#333; }
        td { background:#222; }
        a { color: #4fc3f7; text-decoration:none; }
    </style>
    </head>
    <body>
    <h2 style="text-align:center;">Status des Endpoints Health</h2>
    <table>
    <tr><th>Endpoint</th><th>Status</th></tr>
    """
    for r in results:
        html += f"<tr><td>{r['name']}</td><td>{r['status']}</td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Status des Fichiers Python</h2><table><tr><th>Fichier</th><th>Status</th><th>Voir</th></tr>"

    for f in files_status:
        link = f"/api/monitor/read_file?file_path={f['name']}"
        html += f"<tr><td>{f['name']}</td><td>{f['status']}</td><td><a href='{link}' target='_blank'>Voir</a></td></tr>"

    html += "</table></body></html>"
    return HTMLResponse(content=html)

# Endpoint pour lire un fichier Python
@router.get("/read_file", response_class=HTMLResponse)
async def read_file(file_path: str):
    full_path = BASE_DIR / file_path
    if not full_path.exists() or not full_path.suffix == ".py":
        raise HTTPException(status_code=404, detail="File not found")
    content = full_path.read_text()
    content = content.replace("<", "&lt;").replace(">", "&gt;")
    return HTMLResponse(f"<pre>{content}</pre>")
