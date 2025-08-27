# reentry_service (FastAPI)

Tiny FastAPI wrapper around `reentry_core` exposing:

- `POST /decide` — evaluate REENTRY vs END_TRADING for a combination
- `POST /cell` — evaluate MatrixCell defaults for a combination
- `POST /migrate/sqlite` — run SQLite migrations from the blueprint
- `GET  /ui/config` — fetch UI configuration from the blueprint

## Prereqs

1) Install the library `reentry_core` (zip provided separately) and your Python deps:

```bash
pip install -r requirements.txt
pip install -e ../reentry_core   # or: pip install reentry_core-*.whl
```

2) Place your blueprint files where the service can see them (defaults below).

## Run

```bash
# default paths (override with env vars below)
export BLUEPRINT_PATH=reentry_blueprint.yaml
export SCHEMA_PATH=reentry_blueprint.schema.json

uvicorn reentry_service.main:app --host 0.0.0.0 --port 8080
```

### Env vars

- `BLUEPRINT_PATH` — path to the YAML (or JSON) blueprint (default: `reentry_blueprint.yaml`)
- `SCHEMA_PATH` — path to the JSON Schema (default: `reentry_blueprint.schema.json`)

## Example requests

```bash
curl -s http://localhost:8080/ui/config

curl -s -X POST http://localhost:8080/decide -H 'content-type: application/json' -d '{
  "symbol": "EURUSD",
  "signal_type": "MOMENTUM",
  "time_category": "QUICK",
  "outcome": 6,
  "context": "NEWS_WINDOW",
  "generation": 0
}' | jq

curl -s -X POST http://localhost:8080/cell -H 'content-type: application/json' -d '{
  "symbol": "EURUSD",
  "signal_type": "MOMENTUM",
  "time_category": "QUICK",
  "outcome": 6,
  "context": "NEWS_WINDOW",
  "generation": 0
}' | jq

curl -s -X POST http://localhost:8080/migrate/sqlite -H 'content-type: application/json' -d '{
  "db_path": "reentry.sqlite"
}' | jq
```
