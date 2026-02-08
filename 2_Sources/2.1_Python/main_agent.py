from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:8443"],  # HTTPS correct
    allow_methods=["*"],
    allow_headers=["*"],
)

# Page dédiée aux opérations manuelles (upload et options)
@app.get("/manual_operation", response_class=HTMLResponse)
async def manual_operation():
    return HTMLResponse(
        """
        <html>
        <head>
            <title>Manual Operation - Upload</title>
            <style>
                body { font-family: Arial, sans-serif; background:#1e1e1e; color:#f0f0f0; }
                .container { max-width: 900px; margin: 40px auto; padding: 20px; }
                h1 { text-align: center; }
                .card { background:#252525; padding: 20px; border-radius: 8px; margin-top: 20px; }
                label { display:block; margin-top: 12px; }
                select, input[type="file"] { width: 100%; padding: 8px; margin-top: 6px; }
                .actions { display:flex; gap: 12px; margin-top: 16px; }
                button { padding: 10px 16px; border: none; border-radius: 4px; cursor: pointer; }
                .primary { background:#4fc3f7; color:#0b0b0b; }
                .secondary { background:#444; color:#fff; }
                .status { margin-top: 16px; padding: 10px; background:#1a1a1a; border-radius: 4px; }
                .note { font-size: 0.9em; color:#cfcfcf; margin-top: 8px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Manual Operation</h1>
                <div class="card">
                    <form id="uploadForm">
                        <label for="fileInput">Fichier à uploader</label>
                        <input id="fileInput" name="file" type="file" accept=".md,.markdown,.docx,.pdf,.json,.xml" required />

                        <label for="fileType">Type de fichier</label>
                        <select id="fileType" name="fileType">
                            <option value="md">Markdown (.md/.markdown)</option>
                            <option value="docx">Word (.docx)</option>
                            <option value="pdf">PDF (.pdf)</option>
                            <option value="json">JSON (.json)</option>
                            <option value="xml">XML (.xml)</option>
                        </select>

                        <label for="operationMode">Mode d'opération</label>
                        <select id="operationMode" name="operationMode">
                            <option value="ingest">Ingestion standard</option>
                            <option value="analyze">Analyse uniquement</option>
                            <option value="preview">Prévisualisation</option>
                        </select>

                        <div class="actions">
                            <button class="primary" type="submit">Uploader</button>
                            <button class="secondary" type="reset">Réinitialiser</button>
                        </div>
                    </form>
                    <div class="note">Les options sélectionnées sont affichées à titre informatif côté UI.</div>
                    <div id="status" class="status">Statut : prêt.</div>
                </div>
            </div>
            <script>
                const form = document.getElementById("uploadForm");
                const status = document.getElementById("status");

                form.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    const fileInput = document.getElementById("fileInput");
                    if (!fileInput.files.length) {
                        status.textContent = "Statut : sélectionne un fichier.";
                        return;
                    }

                    const data = new FormData();
                    data.append("file", fileInput.files[0]);

                    status.textContent = "Statut : upload en cours...";
                    try {
                        const response = await fetch("/api/upload", {
                            method: "POST",
                            body: data
                        });
                        const result = await response.json();
                        status.textContent = `Statut : ${result.status} - ${result.filename || ""}`;
                    } catch (err) {
                        status.textContent = `Statut : erreur - ${err}`;
                    }
                });
            </script>
        </body>
        </html>
        """
    )

# Inclure le router principal avec préfixe /api
app.include_router(api_router, prefix="/api")
