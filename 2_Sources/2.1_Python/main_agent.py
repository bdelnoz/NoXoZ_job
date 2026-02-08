#!/usr/bin/env python3
################################################################################
# PATH: 2_Sources/2.1_Python/main_agent.py
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Target usage: Entrypoint FastAPI (API + UI manuelle)
# Version: v1.1.0 – Date: 2026-02-08
#
# Fix v1.1.0:
# - CORS configurable (ENV) + mode dev
# - UI: API_BASE dynamique (window.location.origin) -> plus robuste
# - Ajout endpoints root + health
# - Code un peu moins "monolithique"
################################################################################

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from api.router import router as api_router

APP_TITLE = "NoXoZ_job API"
APP_VERSION = "1.0"


def _get_allowed_origins() -> list[str]:
    """
    CORS:
    - Si tu sers l'UI depuis la même app => inutile, mais ne gêne pas.
    - Si tu sers l'UI ailleurs => configure NOXOZ_CORS_ORIGINS
      ex: "https://127.0.0.1:8443,https://localhost:8443,http://127.0.0.1:3000"
    - Si NOXOZ_CORS_ANY=1 => allow_origins=["*"] (DEV ONLY).
    """
    if os.getenv("NOXOZ_CORS_ANY", "0") == "1":
        return ["*"]

    raw = os.getenv(
        "NOXOZ_CORS_ORIGINS",
        "https://127.0.0.1:8443,https://localhost:8443,http://127.0.0.1:8443,http://localhost:8443",
    ).strip()

    origins = [x.strip() for x in raw.split(",") if x.strip()]
    return origins


app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Middleware CORS (au cas où UI/clients ne sont pas same-origin)
allowed_origins = _get_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # mets True seulement si tu utilises cookies/sessions
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    # UX: landing direct vers la page utile
    return RedirectResponse(url="/manual_operation")


@app.get("/health", include_in_schema=False)
async def health():
    return JSONResponse({"status": "ok", "app": "main_agent", "version": APP_VERSION})


# ----------------------------------------------------------------------
# UI: Manual Operation
# ----------------------------------------------------------------------
@app.get("/manual_operation", response_class=HTMLResponse, include_in_schema=False)
async def manual_operation():
    # IMPORTANT:
    # - API_BASE est dynamique => même si tu changes host/port, ça suit.
    # - tes params fileType/operationMode sont gardés (UI only).
    return HTMLResponse(
        r"""
        <html>
        <head>
            <title>Manual Operation - Upload</title>
            <style>
                body { font-family: Arial, sans-serif; background:#1e1e1e; color:#f0f0f0; }
                .container { max-width: 900px; margin: 40px auto; padding: 20px; }
                h1 { text-align: center; }
                .card { background:#252525; padding: 20px; border-radius: 8px; margin-top: 20px; }
                label { display:block; margin-top: 12px; }
                select, input[type="file"], input[type="text"] { width: 100%; padding: 8px; margin-top: 6px; }
                .actions { display:flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
                button { padding: 10px 16px; border: none; border-radius: 4px; cursor: pointer; }
                .primary { background:#4fc3f7; color:#0b0b0b; }
                .secondary { background:#444; color:#fff; }
                .status { margin-top: 16px; padding: 10px; background:#1a1a1a; border-radius: 4px; }
                .note { font-size: 0.9em; color:#cfcfcf; margin-top: 8px; }
                .step-item { padding: 6px 8px; margin: 6px 0; border-left: 4px solid #4fc3f7; background:#202020; }
                .step-item.fail { border-left-color: #ff6b6b; color:#ffb3b3; }
                .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Manual Operation</h1>
                <div class="card">

                    <div class="note mono" id="apiBaseNote"></div>

                    <form id="uploadForm">
                        <label for="fileInput">Fichier à uploader</label>
                        <input id="fileInput" name="file" type="file" accept=".md,.markdown,.docx,.pdf,.json,.xml" required />

                        <label for="fileType">Type de fichier (UI only)</label>
                        <select id="fileType" name="fileType">
                            <option value="md">Markdown (.md/.markdown)</option>
                            <option value="docx">Word (.docx)</option>
                            <option value="pdf">PDF (.pdf)</option>
                            <option value="json">JSON (.json)</option>
                            <option value="xml">XML (.xml)</option>
                        </select>

                        <label for="operationMode">Mode d'opération (UI only)</label>
                        <select id="operationMode" name="operationMode">
                            <option value="ingest">Ingestion standard</option>
                            <option value="analyze">Analyse uniquement</option>
                            <option value="preview">Prévisualisation</option>
                        </select>

                        <label for="serverPath">Ingestion serveur (chemin relatif)</label>
                        <input id="serverPath" type="text" placeholder="ex: 3_Data/uploads/by_name/index/....md" />

                        <div class="actions">
                            <button class="primary" type="submit">Uploader</button>
                            <button class="secondary" type="reset">Réinitialiser</button>
                            <button class="secondary" type="button" id="serverIngestBtn">Ingestion serveur</button>
                            <a class="secondary" style="text-decoration:none; display:inline-block; padding:10px 16px; border-radius:4px;"
                               href="/manual_log">Voir logs</a>
                            <a class="secondary" style="text-decoration:none; display:inline-block; padding:10px 16px; border-radius:4px;"
                               href="/sqlite_info">SQLite info</a>
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
                const API_BASE = window.location.origin; // robuste: suit host/port actuel
                document.getElementById("apiBaseNote").textContent = "API_BASE = " + API_BASE;

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

                if (fileTypeParam) document.getElementById("fileType").value = fileTypeParam;
                if (operationModeParam) document.getElementById("operationMode").value = operationModeParam;

                if (promptParam) details.textContent = `Détails : prompt=${promptParam}`;
                if (operationModeParam || fileNameParam) {
                    status.textContent = `Statut : prérempli (mode=${operationModeParam || "n/a"}, fichier=${fileNameParam || "n/a"}).`;
                    if (fileNameParam) document.getElementById("serverPath").value = fileNameParam;
                }

                function renderSteps(steps, isError) {
                    if (!steps || !steps.length) {
                        stepList.innerHTML = isError
                            ? "<div style='color:#ff6b6b;'>Échec: voir détails.</div>"
                            : "<div>Aucune étape reçue.</div>";
                        return;
                    }
                    const stepsHtml = steps.map((step, index) => {
                        const line = `${index + 1}. ${step.timestamp} - ${step.message}`;
                        const className = step.status === "error" ? "step-item fail" : "step-item";
                        return `<div class="${className}">${line}</div>`;
                    }).join("");
                    stepList.innerHTML = stepsHtml;
                }

                async function handleUploadResponse(response) {
                    let result = null;
                    try {
                        result = await response.json();
                    } catch (err) {
                        status.textContent = "Statut : réponse non-JSON reçue.";
                        details.textContent = "Détails : " + err;
                        return;
                    }

                    if (!response.ok) {
                        status.textContent = `Statut : erreur (${response.status})`;
                        details.textContent = `Détails : ${result.message || "Erreur inconnue"}`;
                        renderSteps(result.steps, true);
                        return;
                    }

                    status.textContent = `Statut : ${result.status} - ${result.filename || ""}`;
                    if (result.result && result.result.message) details.textContent = `Détails : ${result.result.message}`;
                    else details.textContent = "Détails : upload terminé.";

                    const steps = (result.result && result.result.steps) ? result.result.steps : [];
                    renderSteps(steps, false);
                }

                async function uploadServerFile(relativePath) {
                    if (!relativePath || !relativePath.trim()) {
                        status.textContent = "Statut : donne un chemin relatif serveur.";
                        return;
                    }

                    status.textContent = "Statut : ingestion serveur en cours...";
                    details.textContent = `Détails : source serveur=${relativePath}`;
                    stepList.innerHTML = "<div>En attente des étapes...</div>";

                    try {
                        const response = await fetch(`${API_BASE}/api/upload/server-file`, {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ relative_path: relativePath })
                        });
                        await handleUploadResponse(response);
                    } catch (err) {
                        status.textContent = "Statut : erreur réseau.";
                        details.textContent = `Détails : ${err}`;
                        stepList.innerHTML = "<div style='color:#ff6b6b;'>Échec: erreur réseau.</div>";
                    }
                }

                serverIngestBtn.addEventListener("click", () => {
                    const rp = document.getElementById("serverPath").value;
                    uploadServerFile(rp);
                });

                // auto-ingest si query param file=...
                if (fileNameParam && operationModeParam === "ingest") {
                    uploadServerFile(fileNameParam);
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

                    try {
                        const response = await fetch(`${API_BASE}/api/upload/`, {
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


# ----------------------------------------------------------------------
# UI: Manual Logs
# ----------------------------------------------------------------------
@app.get("/manual_log", response_class=HTMLResponse, include_in_schema=False)
async def manual_log():
    return HTMLResponse(
        r"""
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
                .controls { display:flex; gap: 12px; align-items:center; flex-wrap: wrap; }
                button { padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; }
                .primary { background:#4fc3f7; color:#0b0b0b; }
                .muted { color:#aaa; font-size: 0.9em; }
                pre { white-space: pre-wrap; margin: 0; }
                a { color:#4fc3f7; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Manual Upload Logs</h1>
                <div class="controls">
                    <button class="primary" id="refreshBtn">Rafraîchir</button>
                    <span class="muted" id="lastUpdate">Dernière mise à jour : -</span>
                    <span class="muted">|</span>
                    <a href="/manual_operation">Retour</a>
                    <span class="muted">|</span>
                    <a href="/sqlite_info">SQLite info</a>
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
                const API_BASE = window.location.origin;
                const table = document.getElementById("logTable");
                const lastUpdate = document.getElementById("lastUpdate");
                const refreshBtn = document.getElementById("refreshBtn");

                function formatSteps(steps) {
                    if (!steps || !steps.length) return "Aucune étape.";
                    return steps.map(step => `${step.timestamp} - ${step.message}`).join("\\n");
                }

                async function loadLogs() {
                    try {
                        const response = await fetch(`${API_BASE}/api/upload/logs?limit=100`);
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


# ----------------------------------------------------------------------
# UI: SQLite Info
# ----------------------------------------------------------------------
@app.get("/sqlite_info", response_class=HTMLResponse, include_in_schema=False)
async def sqlite_info():
    import json
    import sqlite3
    from datetime import datetime

    from services.vector_store import METADATA_DB, UPLOADS_DIR, ensure_sqlite_schema

    def _safe_table_count(cursor: sqlite3.Cursor, table: str) -> int | None:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            return int(cursor.fetchone()[0])
        except sqlite3.Error:
            return None

    def _fetch_table_rows(cursor: sqlite3.Cursor, table: str, limit: int = 50) -> dict[str, list]:
        cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT ?;", (limit,))
        columns = [col[0] for col in (cursor.description or [])]
        rows = cursor.fetchall()
        return {"columns": columns, "rows": [list(row) for row in rows]}

    bootstrap = {
        "db_path": str(METADATA_DB),
        "tables": [],
        "files": {"columns": [], "rows": []},
        "documents": {"columns": [], "rows": []},
        "uploads": {"files": []},
        "errors": [],
    }

    try:
        ensure_sqlite_schema()
        conn = sqlite3.connect(METADATA_DB, timeout=5)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in cursor.fetchall()]
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [
                    {
                        "name": col[1],
                        "type": col[2],
                        "notnull": bool(col[3]),
                        "default": col[4],
                        "pk": bool(col[5]),
                    }
                    for col in cursor.fetchall()
                ]
                bootstrap["tables"].append({
                    "name": table,
                    "columns": columns,
                    "row_count": _safe_table_count(cursor, table),
                })

            if "files" in tables:
                bootstrap["files"] = _fetch_table_rows(cursor, "files", limit=50)
            if "documents" in tables:
                bootstrap["documents"] = _fetch_table_rows(cursor, "documents", limit=50)
        finally:
            conn.close()
    except sqlite3.Error as exc:
        bootstrap["errors"].append(f"SQLite error: {exc}")

    if UPLOADS_DIR.exists():
        for file_path in sorted(UPLOADS_DIR.rglob("*")):
            if file_path.is_file():
                stat = file_path.stat()
                bootstrap["uploads"]["files"].append({
                    "name": file_path.name,
                    "relative_path": str(file_path.relative_to(UPLOADS_DIR)),
                    "size_bytes": stat.st_size,
                    "modified_at": datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z",
                })

    bootstrap_json = json.dumps(bootstrap).replace("</", "<\\/")

    html = r"""
        <html>
        <head>
            <title>SQLite Info</title>
            <style>
                body { font-family: Arial, sans-serif; background:#1e1e1e; color:#f0f0f0; }
                .container { max-width: 1200px; margin: 40px auto; padding: 20px; }
                h1, h2 { text-align: center; }
                .card { background:#252525; padding: 20px; border-radius: 8px; margin-top: 20px; }
                .controls { display:flex; gap: 12px; align-items:center; flex-wrap: wrap; }
                button { padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; }
                .primary { background:#4fc3f7; color:#0b0b0b; }
                .secondary { background:#444; color:#fff; }
                .muted { color:#aaa; font-size: 0.9em; }
                textarea, input[type=\"number\"] { width: 100%; padding: 8px; margin-top: 6px; background:#1a1a1a; color:#f0f0f0; border:1px solid #444; border-radius:4px; }
                table { width: 100%; border-collapse: collapse; margin-top: 12px; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; vertical-align: top; }
                th { background:#333; }
                td { background:#222; }
                pre { white-space: pre-wrap; margin: 0; }
                a { color:#4fc3f7; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SQLite Info</h1>
                <div class="controls">
                    <a class="secondary" style="text-decoration:none; display:inline-block; padding:8px 12px; border-radius:4px;"
                       href="/manual_operation">Retour</a>
                    <span class="muted" id="dbPath">DB: -</span>
                </div>

                <div class="card">
                    <h2>Tables SQLite</h2>
                    <div id="tables">Chargement...</div>
                </div>

                <div class="card">
                    <h2>Fichiers (table files)</h2>
                    <div class="controls">
                        <button class="secondary" id="refreshFilesTable">Rafraîchir</button>
                    </div>
                    <div id="filesTable">Chargement...</div>
                </div>

                <div class="card">
                    <h2>Documents (table documents)</h2>
                    <div class="controls">
                        <button class="secondary" id="refreshDocsTable">Rafraîchir</button>
                    </div>
                    <div id="documentsTable">Chargement...</div>
                </div>

                <div class="card">
                    <h2>Fichiers uploadés (dossier)</h2>
                    <div class="controls">
                        <button class="secondary" id="refreshUploads">Rafraîchir</button>
                    </div>
                    <div id="uploads">Chargement...</div>
                </div>

                <div class="card">
                    <h2>Requête SQL (SELECT/PRAGMA)</h2>
                    <div class="controls">
                        <button class="secondary" id="presetFiles">Voir table files</button>
                        <button class="secondary" id="presetDocs">Voir table documents</button>
                    </div>
                    <label for="queryInput">Requête</label>
                    <textarea id="queryInput" rows="4">SELECT * FROM files ORDER BY updated_at DESC</textarea>
                    <label for="limitInput">Limite de lignes</label>
                    <input id="limitInput" type="number" min="1" max="1000" value="200" />
                    <div class="controls" style="margin-top:12px;">
                        <button class="primary" id="runQuery">Exécuter</button>
                        <span class="muted" id="queryStatus">Statut : prêt.</span>
                    </div>
                    <div id="queryResult" style="margin-top:12px;">Aucun résultat.</div>
                </div>
            </div>

            <script id="sqliteInfoBootstrap" type="application/json">__BOOTSTRAP_JSON__</script>
            <script>
                const API_BASE = window.location.origin;
                const tablesEl = document.getElementById("tables");
                const uploadsEl = document.getElementById("uploads");
                const filesTableEl = document.getElementById("filesTable");
                const documentsTableEl = document.getElementById("documentsTable");
                const dbPathEl = document.getElementById("dbPath");
                const queryInput = document.getElementById("queryInput");
                const limitInput = document.getElementById("limitInput");
                const queryStatus = document.getElementById("queryStatus");
                const queryResult = document.getElementById("queryResult");

                function applyBootstrap(data) {
                    if (!data) return;
                    if (data.db_path) {
                        dbPathEl.textContent = `DB: ${data.db_path}`;
                    }

                    if (Array.isArray(data.tables) && data.tables.length) {
                        renderTables(data.tables);
                    }

                    if (data.files && data.files.columns) {
                        filesTableEl.innerHTML = "";
                        filesTableEl.appendChild(buildTable(data.files.columns, data.files.rows || []));
                    }

                    if (data.documents && data.documents.columns) {
                        documentsTableEl.innerHTML = "";
                        documentsTableEl.appendChild(buildTable(data.documents.columns, data.documents.rows || []));
                    }

                    if (data.uploads && Array.isArray(data.uploads.files)) {
                        if (data.uploads.files.length === 0) {
                            uploadsEl.textContent = "Aucun fichier uploadé.";
                        } else {
                            const headers = ["Nom", "Chemin relatif", "Taille (bytes)", "Modifié le"];
                            const rows = data.uploads.files.map(file => [
                                file.name,
                                file.relative_path,
                                file.size_bytes,
                                file.modified_at,
                            ]);
                            uploadsEl.innerHTML = "";
                            uploadsEl.appendChild(buildTable(headers, rows));
                        }
                    }
                }

                function buildTable(headers, rows) {
                    const table = document.createElement("table");
                    const thead = document.createElement("thead");
                    const headRow = document.createElement("tr");
                    headers.forEach(header => {
                        const th = document.createElement("th");
                        th.textContent = header;
                        headRow.appendChild(th);
                    });
                    thead.appendChild(headRow);
                    table.appendChild(thead);

                    const tbody = document.createElement("tbody");
                    if (!rows.length) {
                        const emptyRow = document.createElement("tr");
                        const emptyCell = document.createElement("td");
                        emptyCell.colSpan = headers.length || 1;
                        emptyCell.textContent = "Aucune donnée.";
                        emptyRow.appendChild(emptyCell);
                        tbody.appendChild(emptyRow);
                    } else {
                        rows.forEach(row => {
                            const tr = document.createElement("tr");
                            row.forEach(value => {
                                const td = document.createElement("td");
                                td.textContent = value === null ? "NULL" : String(value);
                                tr.appendChild(td);
                            });
                            tbody.appendChild(tr);
                        });
                    }
                    table.appendChild(tbody);
                    return table;
                }

                function renderTables(tables) {
                    const wrapper = document.createElement("div");
                    wrapper.className = "grid";
                    tables.forEach(table => {
                        const card = document.createElement("div");
                        const title = document.createElement("h3");
                        const countInfo = table.row_count === null ? "n/a" : table.row_count;
                        title.textContent = `${table.name} (lignes: ${countInfo})`;
                        card.appendChild(title);

                        const colLines = table.columns.map(col => {
                            const flags = [];
                            if (col.pk) flags.push("PK");
                            if (col.notnull) flags.push("NOT NULL");
                            const suffix = flags.length ? ` (${flags.join(", ")})` : "";
                            return `${col.name} : ${col.type}${suffix}`;
                        });
                        const pre = document.createElement("pre");
                        pre.textContent = colLines.join("\\n");
                        card.appendChild(pre);
                        wrapper.appendChild(card);
                    });
                    tablesEl.innerHTML = "";
                    tablesEl.appendChild(wrapper);
                }

                async function loadTables() {
                    try {
                        const response = await fetch(`${API_BASE}/api/sqlite_info/tables`);
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || "Erreur de chargement.");
                        }
                        const data = await response.json();
                        dbPathEl.textContent = `DB: ${data.db_path || "-"}`;

                        if (!data.tables || !data.tables.length) {
                            tablesEl.textContent = "Aucune table trouvée.";
                            return;
                        }

                        renderTables(data.tables);
                    } catch (err) {
                        tablesEl.textContent = `Erreur: ${err}`;
                    }
                }

                async function loadFilesTable() {
                    try {
                        const response = await fetch(`${API_BASE}/api/sqlite_info/files?limit=200`);
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || "Erreur de chargement.");
                        }
                        const data = await response.json();
                        filesTableEl.innerHTML = "";
                        filesTableEl.appendChild(buildTable(data.columns || [], data.rows || []));
                    } catch (err) {
                        filesTableEl.textContent = `Erreur: ${err}`;
                    }
                }

                async function loadDocumentsTable() {
                    try {
                        const response = await fetch(`${API_BASE}/api/sqlite_info/documents?limit=200`);
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || "Erreur de chargement.");
                        }
                        const data = await response.json();
                        documentsTableEl.innerHTML = "";
                        documentsTableEl.appendChild(buildTable(data.columns || [], data.rows || []));
                    } catch (err) {
                        documentsTableEl.textContent = `Erreur: ${err}`;
                    }
                }

                async function loadUploads() {
                    try {
                        const response = await fetch(`${API_BASE}/api/sqlite_info/uploads`);
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || "Erreur de chargement.");
                        }
                        const data = await response.json();
                        if (!data.files || !data.files.length) {
                            uploadsEl.textContent = "Aucun fichier uploadé.";
                            return;
                        }

                        const headers = ["Nom", "Chemin relatif", "Taille (bytes)", "Modifié le"];
                        const rows = data.files.map(file => [
                            file.name,
                            file.relative_path,
                            file.size_bytes,
                            file.modified_at,
                        ]);
                        uploadsEl.innerHTML = \"\";
                        uploadsEl.appendChild(buildTable(headers, rows));
                    } catch (err) {
                        uploadsEl.textContent = `Erreur: ${err}`;
                    }
                }

                async function runQuery() {
                    const query = queryInput.value;
                    const limit = Number(limitInput.value || 200);
                    queryStatus.textContent = "Statut : exécution...";
                    queryResult.textContent = "Chargement...";

                    try {
                        const response = await fetch(`${API_BASE}/api/sqlite_info/query`, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ query, limit }),
                        });
                        const data = await response.json();
                        if (!response.ok) {
                            queryStatus.textContent = "Statut : erreur.";
                            queryResult.textContent = data.detail || "Erreur inconnue.";
                            return;
                        }

                        queryStatus.textContent = `Statut : OK (${data.row_count} ligne(s)).`;
                        queryResult.innerHTML = \"\";
                        queryResult.appendChild(buildTable(data.columns || [], data.rows || []));
                    } catch (err) {
                        queryStatus.textContent = "Statut : erreur.";
                        queryResult.textContent = `Erreur: ${err}`;
                    }
                }

                document.getElementById("runQuery").addEventListener("click", runQuery);
                document.getElementById("presetFiles").addEventListener("click", () => {
                    queryInput.value = "SELECT * FROM files ORDER BY updated_at DESC";
                    runQuery();
                });
                document.getElementById("presetDocs").addEventListener("click", () => {
                    queryInput.value = "SELECT * FROM documents ORDER BY ingestion_date DESC";
                    runQuery();
                });
                document.getElementById("refreshUploads").addEventListener("click", loadUploads);
                document.getElementById("refreshFilesTable").addEventListener("click", loadFilesTable);
                document.getElementById("refreshDocsTable").addEventListener("click", loadDocumentsTable);

                const bootstrapEl = document.getElementById("sqliteInfoBootstrap");
                if (bootstrapEl) {
                    try {
                        const data = JSON.parse(bootstrapEl.textContent);
                        applyBootstrap(data);
                    } catch (err) {
                        console.warn("Bootstrap data invalid", err);
                    }
                }

                loadTables();
                loadFilesTable();
                loadDocumentsTable();
                loadUploads();
            </script>
        </body>
        </html>
        """
    return HTMLResponse(html.replace("__BOOTSTRAP_JSON__", bootstrap_json))


# Inclure le router principal avec préfixe /api
app.include_router(api_router, prefix="/api")
