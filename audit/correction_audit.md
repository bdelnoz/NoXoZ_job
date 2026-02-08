FILENAME: correction_audit.md
COMPLETE PATH: ./audit/correction_audit.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:26:11

---

# Corrections Audit

## Priority list (P0/P1/P2)

### P0 (Critical)
1. Remove `certs/key.pem` from the repository and replace with environment-managed secrets.
   - Effort: 0.5 day
   - Risk: HIGH (secret exposure)
   - Dependencies: None
2. Provide a validated deployment path that includes the FastAPI service (Docker Compose or explicit run scripts).
   - Effort: 1-2 days
   - Risk: HIGH (stack cannot run as documented)
   - Dependencies: None

### P1 (High)
1. Align documentation structure with actual repository tree and runtime ports.
   - Effort: 0.5-1 day
   - Risk: MEDIUM (operator confusion)
   - Dependencies: P0.2
2. Provide a reproducible dependency installation path (requirements.txt vs Pipfile).
   - Effort: 0.5 day
   - Risk: MEDIUM (tests and runtime not reproducible)
   - Dependencies: None

### P2 (Medium)
1. Remove or archive legacy files (`status.ORI.py`, `fastapi_full_monitor.py`) or document their purpose.
   - Effort: 0.25 day
   - Risk: LOW
   - Dependencies: None
2. Add a LICENSE file to clarify usage rights.
   - Effort: 0.25 day
   - Risk: LOW
   - Dependencies: None

## Conclusion
STATUS: SUCCESS
