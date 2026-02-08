from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import httpx

router = APIRouter()

# Base directory pour tes scripts Python
BASE_DIR = Path(__file__).resolve().parents[2]  # remonte vers 2.1_Python
REPO_ROOT = Path(__file__).resolve().parents[4]

# Liste des fichiers Python à surveiller
PYTHON_FILES = [
    "api/dependencies.py",
    "api/router.py",
    "api/endpoints/generate.py",
    "api/endpoints/status.py",
    "api/endpoints/upload.py",
    "api/endpoints/status_web.py",
    "api/monitor.py",
    "chroma_integration.py",
    "main_agent.py",
    "services/generation.py",
    "services/ingestion.py",
    "services/vector_store.py",
    "temp.py",
    "test_db_huffing.py",
    "test_sentence_transfomers.py"
]

BASE_API_URL = "https://127.0.0.1:8443/api"
ENDPOINT_BASES = [
    {"name": "Generate", "path": "/generate"},
    {"name": "Upload", "path": "/upload"},
    {"name": "Status", "path": "/status"},
    {"name": "Monitor", "path": "/monitor"},
]

MONITOR_COMPONENTS = [
    {"name": "FastAPI", "key": "fastapi"},
    {"name": "ChromaDB", "key": "chroma"},
    {"name": "SQLite", "key": "sqlite"},
    {"name": "Ollama", "key": "ollama"},
    {"name": "Logs", "key": "logs"},
    {"name": "Last Prompt", "key": "last_prompt"},
]

@router.get("/status_web", response_class=HTMLResponse)
async def web_status():
    health_results = []
    status_results = []
    async with httpx.AsyncClient(verify=False) as client:
        for ep in ENDPOINT_BASES:
            try:
                resp = await client.get(f"{BASE_API_URL}{ep['path']}/health", timeout=3)
                if resp.status_code == 200:
                    status = "✅ OK"
                else:
                    status = f"❌ {resp.status_code}"
            except Exception as e:
                status = f"❌ Error: {str(e)}"
            health_results.append({"name": ep["name"], "status": status})

            try:
                resp = await client.get(f"{BASE_API_URL}{ep['path']}/status", timeout=3)
                if resp.status_code == 200:
                    status = "✅ OK"
                else:
                    status = f"❌ {resp.status_code}"
            except Exception as e:
                status = f"❌ Error: {str(e)}"
            status_results.append({"name": ep["name"], "status": status})

    monitor_components = []
    async with httpx.AsyncClient(verify=False) as client:
        try:
            monitor_resp = await client.get(f"{BASE_API_URL}/monitor/full", timeout=5)
            if monitor_resp.status_code == 200:
                data = monitor_resp.json()
                for component in MONITOR_COMPONENTS:
                    component_data = data.get(component["key"], {})
                    component_status = component_data.get("status", "unknown")
                    monitor_components.append({
                        "name": component["name"],
                        "status": component_status
                    })
            else:
                monitor_components.append({
                    "name": "Monitor Full",
                    "status": f"error {monitor_resp.status_code}"
                })
        except Exception as e:
            monitor_components.append({
                "name": "Monitor Full",
                "status": f"error {str(e)}"
            })

    # Vérification des fichiers Python
    files_status = []
    for f in PYTHON_FILES:
        file_path = BASE_DIR / f
        files_status.append({
            "name": f,
            "status": "✅ Found" if file_path.exists() else "❌ Missing"
        })

    shell_scripts = []
    for file_path in sorted(REPO_ROOT.rglob("*.sh")):
        relative_path = file_path.relative_to(REPO_ROOT)
        shell_scripts.append({
            "name": str(relative_path),
            "status": "✅ Found"
        })

    text_files = []
    text_patterns = (".txt", ".md", ".markdown")
    for file_path in sorted(REPO_ROOT.rglob("*")):
        if file_path.suffix.lower() in text_patterns:
            relative_path = file_path.relative_to(REPO_ROOT)
            text_files.append({
                "name": str(relative_path),
                "status": "✅ Found"
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
    for r in health_results:
        html += f"<tr><td>{r['name']}</td><td>{r['status']}</td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Status des Endpoints Status</h2><table><tr><th>Endpoint</th><th>Status</th></tr>"

    for r in status_results:
        html += f"<tr><td>{r['name']}</td><td>{r['status']}</td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Status des Composants</h2><table><tr><th>Composant</th><th>Status</th></tr>"

    for r in monitor_components:
        html += f"<tr><td>{r['name']}</td><td>{r['status']}</td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Status des Fichiers Python</h2><table><tr><th>Fichier</th><th>Status</th><th>Voir</th></tr>"

    for f in files_status:
        link = f"/api/monitor/read_file?file_path={f['name']}"
        html += f"<tr><td>{f['name']}</td><td>{f['status']}</td><td><a href='{link}' target='_blank'>Voir</a></td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Fichiers Shell</h2><table><tr><th>Fichier</th><th>Status</th><th>Voir</th></tr>"

    for f in shell_scripts:
        link = f"/api/monitor/read_file?file_path={f['name']}"
        html += f"<tr><td>{f['name']}</td><td>{f['status']}</td><td><a href='{link}' target='_blank'>Voir</a></td></tr>"

    html += "</table><br><h2 style='text-align:center;'>Fichiers Texte/Markdown</h2><table><tr><th>Fichier</th><th>Status</th><th>Voir</th></tr>"

    for f in text_files:
        link = f"/api/monitor/read_file?file_path={f['name']}"
        html += f"<tr><td>{f['name']}</td><td>{f['status']}</td><td><a href='{link}' target='_blank'>Voir</a></td></tr>"

    html += "</table></body></html>"
    return HTMLResponse(content=html)

# Endpoint pour lire un fichier Python
@router.get("/read_file", response_class=HTMLResponse)
async def read_file(file_path: str):
    full_path = REPO_ROOT / file_path
    allowed_suffixes = {".py", ".sh", ".txt", ".md", ".markdown"}
    if not full_path.exists() or full_path.suffix.lower() not in allowed_suffixes:
        raise HTTPException(status_code=404, detail="File not found")
    content = full_path.read_text()
    content = content.replace("<", "&lt;").replace(">", "&gt;")
    return HTMLResponse(f"<pre>{content}</pre>")
