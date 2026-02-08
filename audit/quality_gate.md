FILENAME: quality_gate.md
COMPLETE PATH: ./audit/quality_gate.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:24:59

---

# Qualitative Analysis & Quality Gates

## Table Findings
| ID | Category | Severity | Evidence | Rule violated |
| --- | --- | --- | --- | --- |
| QG-001 | security hygiene | HIGH | `certs/key.pem` stored in repo | Sensitive private material present in repository. |
| QG-002 | documentation | MEDIUM | `1_Documentation/1.2_Technical/structure.md` does not match actual tree | Documentation is inconsistent with repository content. |
| QG-003 | configuration | MEDIUM | `docker-compose.yml` lacks FastAPI service | Deployment configuration is incomplete for running the full stack. |
| QG-004 | testability | HIGH | `pytest` fails during collection (missing `chromadb`, `sentence_transformers`) | Tests are not executable in current environment without dependency resolution. |
| QG-005 | maintainability | LOW | `api/endpoints/status.ORI.py` duplicates `status.py` | Redundant/legacy files increase maintenance risk. |
| QG-006 | documentation | MEDIUM | README references `https://127.0.0.1:8443` while architecture doc uses `http://127.0.0.1:11111` | Inconsistent user-facing interface information. |

## Blocking Gates (explicit)
- Dependencies identifiable: PASS (requirements are listed in `requirements.txt` and `Pipfile`).
- Secrets exposed: FAILED (private key file `certs/key.pem` is stored in the repository).
- Code non-executable globally: FAILED (tests fail due to missing dependencies in the current environment; runtime requires external services and local paths).
- Architecture incoherent / unusable: FAILED (documentation and deployment configuration are inconsistent for a complete runtime stack).

## Conclusion
STATUS: FAILED
