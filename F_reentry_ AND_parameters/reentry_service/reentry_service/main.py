from __future__ import annotations
import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from reentry_core import load_blueprint, IDCodec, RuleEngine, DB, UI

BLUEPRINT_PATH = os.getenv("BLUEPRINT_PATH", "reentry_blueprint.yaml")
SCHEMA_PATH    = os.getenv("SCHEMA_PATH", "reentry_blueprint.schema.json")

app = FastAPI(title="reentry_service", version="0.1.0")

_bp = None
_codec = None
_engine = None

class Combo(BaseModel):
    symbol: str
    signal_type: str
    time_category: str
    outcome: int
    context: str
    generation: int

class DecideResponse(BaseModel):
    combination_id: str
    source: str
    decision: str
    parameter_set: Dict[str, Any]

class CellResponse(BaseModel):
    combination_id: str
    action: str
    size_multiplier: float
    confidence_adjustment: float
    delay_minutes: int
    max_attempts: int

class SqliteRequest(BaseModel):
    db_path: str

def _load():
    global _bp, _codec, _engine
    _bp = load_blueprint(BLUEPRINT_PATH, schema_path=SCHEMA_PATH)
    _codec = IDCodec.from_blueprint(_bp)
    _engine = RuleEngine(_bp)

def _validate_combo(combo: Dict[str, Any]) -> None:
    enums = _bp["enumerations"]
    sigs = set(enums["signal_type"]["allowed"])
    tcat = set(enums["time_category"]["allowed"])
    ctxs = set(enums["context"]["allowed"])
    if combo["signal_type"] not in sigs:
        raise HTTPException(status_code=400, detail=f"Invalid signal_type: {combo['signal_type']}")
    if combo["time_category"] not in tcat:
        raise HTTPException(status_code=400, detail=f"Invalid time_category: {combo['time_category']}")
    if combo["context"] not in ctxs:
        raise HTTPException(status_code=400, detail=f"Invalid context: {combo['context']}")
    if combo["outcome"] not in set(_bp["enumerations"]["outcome"]["allowed"]):
        raise HTTPException(status_code=400, detail=f"Invalid outcome: {combo['outcome']}")
    gen_min = _bp["enumerations"]["generation"]["range"]["min"]
    gen_max = _bp["enumerations"]["generation"]["range"]["max"]
    if combo["generation"] < gen_min or combo["generation"] > gen_max:
        raise HTTPException(status_code=400, detail=f"generation out of range [{gen_min},{gen_max}]: {combo['generation']}")
    import re
    pat = _bp["enumerations"]["symbol"]["pattern"]
    if not re.match(pat, combo["symbol"]):
        raise HTTPException(status_code=400, detail=f"symbol does not match pattern {pat}: {combo['symbol']}")

@app.on_event("startup")
def on_startup():
    _load()

@app.get("/ui/config")
def ui_config():
    return UI.config(_bp)

@app.post("/decide", response_model=DecideResponse)
def decide(c: Combo):
    combo = c.model_dump()
    _validate_combo(combo)
    comb_id = _codec.build(combo)
    inv = _engine.evaluate_invariants(combo)
    res = inv if inv else _engine.evaluate_combination_defaults(combo)
    return {
        "combination_id": comb_id,
        "source": "invariant" if inv else "default_rules",
        "decision": res["decision"],
        "parameter_set": res.get("parameter_set", {})
    }

@app.post("/cell", response_model=CellResponse)
def cell(c: Combo):
    combo = c.model_dump()
    _validate_combo(combo)
    comb_id = _codec.build(combo)
    res = _engine.evaluate_cell(combo)
    return {
        "combination_id": comb_id,
        "action": res["action"],
        "size_multiplier": float(res.get("size_multiplier", 0.0)),
        "confidence_adjustment": float(res.get("confidence_adjustment", 0.0)),
        "delay_minutes": int(res.get("delay_minutes", 0)),
        "max_attempts": int(res.get("max_attempts", 0)),
    }

@app.post("/migrate/sqlite")
def migrate_sqlite(req: SqliteRequest):
    path = os.path.expanduser(req.db_path)
    DB.migrate_sqlite(path, _bp)
    return {"ok": True, "db_path": path}

@app.get("/health")
def health():
    return {"status": "ok"}
