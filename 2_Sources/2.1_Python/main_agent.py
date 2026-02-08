from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.router import router as api_router

app = FastAPI(title="NoXoZ_job API", version="1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://127.0.0.1:8443",
        "https://localhost:8443",
        "http://127.0.0.1:8443",
        "http://localhost:8443",
    ],
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
                .step-item { padding: 6px 8px; margin: 6px 0; border-left: 4px solid #4fc3f7; background:#202020; }
                .step-item.fail { border-left-color: #ff6b6b; color:#ffb3b3; }
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
                            <button class="secondary" type="button" id="serverIngestBtn" style="display:none;">Ingestion serveur</button>
                        </div>
                    </form>
                    <div class="note">Les options sélectionnées sont affichées à titre informatif côté UI.</div>
                    <div id="status" class="status">Statut : prêt.</div>
                    <div id="details" class="status">Détails : aucun upload.</div>
                    <div id="stepTitle" class="note">Étapes:</div>
                    <div id="stepList" class="status">Aucune étape pour le moment.</div>
                </div>
            </div>
            <script>
                const form = document.getElementById("uploadForm");
                const status = document.getElementById("status");
                const details = document.getElementById("details");
                const stepList = document.getElementById("stepList");
                const serverIngestBtn = document.getElementById("serverIngestBtn");

                const params = new URLSearchParams(window.location.search);
                const fileTypeParam = params.get("fileType");
                const operationModeParam = params.get("operationMode");
                const fileNameParam = params.get("file");
                const promptParam = params.get("prompt");

                if (fileTypeParam) {
                    const fileTypeSelect = document.getElementById("fileType");
                    fileTypeSelect.value = fileTypeParam;
                }

                if (operationModeParam) {
                    const operationModeSelect = document.getElementById("operationMode");
                    operationModeSelect.value = operationModeParam;
                }

                if (promptParam) {
                    details.textContent = `Détails : prompt=${promptParam}`;
                }

                if (operationModeParam || fileNameParam) {
                    status.textContent = `Statut : prérempli (mode=${operationModeParam || "n/a"}, fichier=${fileNameParam || "n/a"}).`;
                }

                async function handleUploadResponse(response) {
                    let result = null;
                    try {
                        result = await response.json();
                    } catch (err) {
                        status.textContent = "Statut : réponse non-JSON reçue.";
                        return;
                    }

                    if (!response.ok) {
                        status.textContent = `Statut : erreur (${response.status})`;
                        details.textContent = `Détails : ${result.message || "Erreur inconnue"}`;
                        if (result.steps && result.steps.length) {
                            const stepsHtml = result.steps.map((step, index) => {
                                const line = `${index + 1}. ${step.timestamp} - ${step.message}`;
                                const className = step.status === "error" ? "step-item fail" : "step-item";
                                return `<div class="${className}">${line}</div>`;
                            }).join("");
                            stepList.innerHTML = stepsHtml;
                        } else {
                            stepList.innerHTML = "<div style='color:#ff6b6b;'>Échec: voir les détails.</div>";
                        }
                        return;
                    }

                    status.textContent = `Statut : ${result.status} - ${result.filename || ""}`;
                    if (result.result && result.result.message) {
                        details.textContent = `Détails : ${result.result.message}`;
                    } else {
                        details.textContent = "Détails : upload terminé.";
                    }

                    if (result.result && result.result.steps && result.result.steps.length) {
                        const stepsHtml = result.result.steps.map((step, index) => {
                            const line = `${index + 1}. ${step.timestamp} - ${step.message}`;
                            const className = step.status === "error" ? "step-item fail" : "step-item";
                            return `<div class="${className}">${line}</div>`;
                        }).join("");
                        stepList.innerHTML = stepsHtml;
                    } else {
                        stepList.innerHTML = "<div>Aucune étape reçue.</div>";
                    }
                }

                async function uploadServerFile(relativePath) {
                    status.textContent = "Statut : ingestion serveur en cours...";
                    details.textContent = `Détails : source serveur=${relativePath}`;
                    stepList.innerHTML = "<div>En attente des étapes...</div>";
                    try {
                        const response = await fetch("/api/upload/server-file", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ relative_path: relativePath })
                        });
                        await handleUploadResponse(response);
                    } catch (err) {
                        status.textContent = "Statut : erreur réseau.";
                        details.textContent = `Détails : ${err}`;
                        stepList.innerHTML = "<div style='color:#ff6b6b;'>Échec: erreur réseau.</div>";
                    }
                }

                if (fileNameParam) {
                    serverIngestBtn.style.display = "inline-block";
                    serverIngestBtn.addEventListener("click", () => uploadServerFile(fileNameParam));
                    if (operationModeParam === "ingest") {
                        uploadServerFile(fileNameParam);
                    }
                }

                const params = new URLSearchParams(window.location.search);
                const fileTypeParam = params.get("fileType");
                const operationModeParam = params.get("operationMode");
                const fileNameParam = params.get("file");
                const promptParam = params.get("prompt");

                if (fileTypeParam) {
                    const fileTypeSelect = document.getElementById("fileType");
                    fileTypeSelect.value = fileTypeParam;
                }

                if (operationModeParam) {
                    const operationModeSelect = document.getElementById("operationMode");
                    operationModeSelect.value = operationModeParam;
                }

                if (promptParam) {
                    details.textContent = `Détails : prompt=${promptParam}`;
                }

                if (operationModeParam || fileNameParam) {
                    status.textContent = `Statut : prérempli (mode=${operationModeParam || "n/a"}, fichier=${fileNameParam || "n/a"}).`;
                }

                form.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    const fileInput = document.getElementById("fileInput");
                    if (!fileInput.files.length) {
                        status.textContent = "Statut : sélectionne un fichier.";
                        return;
                    }

                    const data = new FormData();
                    data.append("file", fileInput.files[0]);
                    const selectedType = document.getElementById("fileType").value;
                    const selectedMode = document.getElementById("operationMode").value;
                    details.textContent = `Détails : type=${selectedType}, mode=${selectedMode}`;

                    status.textContent = "Statut : upload en cours...";
                    stepList.innerHTML = "<div>En attente des étapes...</div>";

                    status.textContent = "Statut : upload en cours...";
                    try {
                        const response = await fetch("/api/upload/", {
                            method: "POST",
                            body: data
                        });
                        await handleUploadResponse(response);
                    } catch (err) {
                        status.textContent = "Statut : erreur réseau.";
                        details.textContent = `Détails : ${err}`;
                        stepList.innerHTML = "<div style='color:#ff6b6b;'>Échec: erreur réseau.</div>";
                    }
                });
            </script>
        </body>
        </html>
        """
    )

# Page de logs détaillés pour les uploads
@app.get("/manual_log", response_class=HTMLResponse)
async def manual_log():
    return HTMLResponse(
        """
        <html>
        <head>
            <title>Manual Upload Logs</title>
            <style>
                body { font-family: Arial, sans-serif; background:#1e1e1e; color:#f0f0f0; }
                .container { max-width: 1100px; margin: 40px auto; padding: 20px; }
                h1 { text-align: center; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; vertical-align: top; }
                th { background:#333; }
                td { background:#222; }
                .controls { display:flex; gap: 12px; align-items:center; }
                button { padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; }
                .primary { background:#4fc3f7; color:#0b0b0b; }
                .muted { color:#aaa; font-size: 0.9em; }
                pre { white-space: pre-wrap; margin: 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Manual Upload Logs</h1>
                <div class="controls">
                    <button class="primary" id="refreshBtn">Rafraîchir</button>
                    <span class="muted" id="lastUpdate">Dernière mise à jour : -</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Fichier</th>
                            <th>Status</th>
                            <th>Horodatage</th>
                            <th>Étapes</th>
                        </tr>
                    </thead>
                    <tbody id="logTable">
                        <tr><td colspan="5">Aucun log pour le moment.</td></tr>
                    </tbody>
                </table>
            </div>
            <script>
                const table = document.getElementById("logTable");
                const lastUpdate = document.getElementById("lastUpdate");
                const refreshBtn = document.getElementById("refreshBtn");

                function formatSteps(steps) {
                    if (!steps || !steps.length) {
                        return "Aucune étape.";
                    }
                    return steps.map(step => `${step.timestamp} - ${step.message}`).join("\\n");
                }

                async function loadLogs() {
                    try {
                        const response = await fetch("/api/upload/logs?limit=100");
                        const data = await response.json();
                        if (!data.logs || data.logs.length === 0) {
                            table.innerHTML = "<tr><td colspan='5'>Aucun log pour le moment.</td></tr>";
                            return;
                        }
                        table.innerHTML = "";
                        data.logs.slice().reverse().forEach(log => {
                            const row = document.createElement("tr");
                            row.innerHTML = `
                                <td>${log.id}</td>
                                <td>${log.filename || "-"}</td>
                                <td>${log.status || "-"}</td>
                                <td>${log.started_at || "-"}<br/>${log.finished_at || ""}</td>
                                <td><pre>${formatSteps(log.steps)}</pre></td>
                            `;
                            table.appendChild(row);
                        });
                        lastUpdate.textContent = `Dernière mise à jour : ${new Date().toLocaleTimeString()}`;
                    } catch (err) {
                        table.innerHTML = `<tr><td colspan='5'>Erreur de chargement: ${err}</td></tr>`;
                    }
                }

                refreshBtn.addEventListener("click", loadLogs);
                loadLogs();
            </script>
        </body>
        </html>
        """
    )

# Inclure le router principal avec préfixe /api
app.include_router(api_router, prefix="/api")
