# Reentry API (tiny FastAPI layer)

Drop-in service exposing endpoints over your **Reentry Blueprint**.

## Install & Run

```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Ensure reentry_core is installed (point to the folder you unzipped earlier)
pip install -e ../reentry_core
# Set paths or rely on defaults in /mnt/data
export REENTRY_BLUEPRINT=/mnt/data/reentry_blueprint.yaml
export REENTRY_SCHEMA=/mnt/data/reentry_blueprint.schema.json

uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- GET /health → {"status":"ok"}
- GET /ui/config → returns ui_requirements from the blueprint
  - Optional query: ?blueprint_path=...&schema_path=...
- POST /decide → evaluates invariants/combination rules and returns decision + evaluated cell
- POST /cell → returns evaluated default cell
- POST /migrate/sqlite → runs the blueprint's SQLite DDL against db_path

See README for example curl commands.
