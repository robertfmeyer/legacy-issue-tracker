# Legacy App (Intentionally Legacy)

This directory contains an intentionally "legacy-style" backend service.

The goal is to provide a realistic baseline that can be modernized incrementally.

## How to run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r legacy_app/requirements.txt
uvicorn legacy_app.app:app --reload
