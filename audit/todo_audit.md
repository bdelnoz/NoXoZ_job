FILENAME: todo_audit.md
COMPLETE PATH: ./audit/todo_audit.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:26:19

---

# TODO Backlog (Audit)

## P0
- **Secret remediation**: remove `certs/key.pem` from version control; rotate any associated certs.
  - Effort: 0.5 day
  - Risk: HIGH
  - Depends on: None
- **Runnable stack**: add FastAPI service to `docker-compose.yml` or provide a verified run script.
  - Effort: 1-2 days
  - Risk: HIGH
  - Depends on: None

## P1
- **Documentation alignment**: update architecture and structure docs to match actual repository layout.
  - Effort: 0.5-1 day
  - Risk: MEDIUM
  - Depends on: P0 runnable stack
- **Dependency reproducibility**: decide on `requirements.txt` vs `Pipfile` as source of truth.
  - Effort: 0.5 day
  - Risk: MEDIUM
  - Depends on: None
- **Testing stabilization**: ensure `chromadb` and `sentence_transformers` are installed for tests.
  - Effort: 0.5 day
  - Risk: MEDIUM
  - Depends on: Dependency reproducibility

## P2
- **Legacy cleanup**: clarify status or remove unused scripts/duplicate endpoints.
  - Effort: 0.25 day
  - Risk: LOW
  - Depends on: None
- **License**: add a project license file.
  - Effort: 0.25 day
  - Risk: LOW
  - Depends on: None

## Conclusion
STATUS: SUCCESS
