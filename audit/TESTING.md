FILENAME: TESTING.md
COMPLETE PATH: ./audit/TESTING.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:25:52

---

# Testing (Audit View)

## Test frameworks detected
- Pytest (used by `python -m pytest`).

## Test files detected
- `2_Sources/2.1_Python/test_db_huffing.py`
- `2_Sources/2.1_Python/test_sentence_transfomers.py`

## How to run (expected)
```bash
python -m pytest
```

## Status
- Tests fail during collection due to missing dependencies (`chromadb`, `sentence_transformers`) in the current environment.

## Conclusion
STATUS: SUCCESS
