from __future__ import annotations
import os, time, pathlib, re
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

# Import local library
from reentry_core import load_blueprint, IDCodec, RuleEngine, DB, UI

DEFAULT_BLUEPRINT_PATH = os.environ.get("REENTRY_BLUEPRINT", "/mnt/data/reentry_blueprint.yaml")
DEFAULT_SCHEMA_PATH    = os.environ.get("REENTRY_SCHEMA", "/mnt/data/reentry_blueprint.schema.json")

app = FastAPI(title="Reentry API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Cache ----------------
_bp_cache: Dict[str, tuple[float, Any]] = {}

def _load_bp(path: Optional[str], schema_path: Optional[str]):
    bp_path = path or DEFAULT_BLUEPRINT_PATH
    sc_path = schema_path or DEFAULT_SCHEMA_PATH
    p = pathlib.Path(bp_path)
    if not p.exists():
        raise HTTPException(400, f"Blueprint not found: {bp_path}")
    mtime = p.stat().st_mtime
    cached = _bp_cache.get(bp_path)
    if cached and cached[0] == mtime:
        bp = cached[1]
    else:
        bp = load_blueprint(bp_path, schema_path=sc_path)
        _bp_cache[bp_path] = (mtime, bp)
    return bp

# ---------------- Models ----------------
class Combo(BaseModel):
    symbol: str = Field(..., description="Instrument symbol (e.g., EURUSD)")
    signal_type: str
    time_category: str
    outcome: int = Field(..., ge=1, le=6)
    context: str
    generation: int = Field(..., ge=0)

class DecideRequest(BaseModel):
    combo: Combo
    blueprint_path: Optional[str] = None
    schema_path: Optional[str] = None

class DecideResponse(BaseModel):
    combination_id_readable: str
    combination_id_compact: str
    decision: Dict[str, Any]
    evaluated_cell: Dict[str, Any]

class CellRequest(BaseModel):
    combo: Combo
    blueprint_path: Optional[str] = None
    schema_path: Optional[str] = None

class CellResponse(BaseModel):
    combination_id_readable: str
    combination_id_compact: str
    evaluated_cell: Dict[str, Any]

class MigrateSqliteRequest(BaseModel):
    db_path: str
    blueprint_path: Optional[str] = None
    schema_path: Optional[str] = None

class UIConfigResponse(BaseModel):
    ui_config: Dict[str, Any]

# ---------------- Helpers ----------------
def _validate_combo_against_enums(bp, combo: Dict[str, Any]) -> None:
    enums = bp.get("enumerations", {})
    # Symbol pattern
    sym_pat = enums.get("symbol", {}).get("pattern")
    if sym_pat and not re.match(sym_pat, combo["symbol"]):
        raise HTTPException(400, f"symbol does not match pattern {sym_pat}")
    # Enumerated fields
    for fld in ("signal_type","time_category","context"):
        allowed = (enums.get(fld, {}) or {}).get("allowed")
        if allowed and combo[fld] not in allowed:
            raise HTTPException(400, f"{fld} '{combo[fld]}' not in allowed set: {allowed}")
    # Outcome range already validated by Pydantic; generation range from blueprint if provided
    gen_range = (enums.get("generation", {}) or {}).get("range")
    if gen_range is not None:
        mn = gen_range.get("min", 0); mx = gen_range.get("max", 9999)
        if not (mn <= combo["generation"] <= mx):
            raise HTTPException(400, f"generation {combo['generation']} outside allowed range [{mn},{mx}]")

def _codec_and_engine(bp):
    return IDCodec.from_blueprint(bp), RuleEngine(bp)

# ---------------- Routes ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ui/config", response_model=UIConfigResponse)
def ui_config(blueprint_path: Optional[str] = Query(None), schema_path: Optional[str] = Query(None)):
    bp = _load_bp(blueprint_path, schema_path)
    return {"ui_config": UI.config(bp)}

@app.post("/decide", response_model=DecideResponse)
def decide(req: DecideRequest):
    bp = _load_bp(req.blueprint_path, req.schema_path)
    combo = req.combo.model_dump()
    _validate_combo_against_enums(bp, combo)
    codec, engine = _codec_and_engine(bp)
    cid_readable = codec.build(combo, compact=False)
    cid_compact  = codec.build(combo, compact=True)
    decision = engine.evaluate_decision(combo)
    cell = engine.evaluate_cell(combo)
    return {
        "combination_id_readable": cid_readable,
        "combination_id_compact": cid_compact,
        "decision": decision,
        "evaluated_cell": cell
    }

@app.post("/cell", response_model=CellResponse)
def cell(req: CellRequest):
    bp = _load_bp(req.blueprint_path, req.schema_path)
    combo = req.combo.model_dump()
    _validate_combo_against_enums(bp, combo)
    codec, engine = _codec_and_engine(bp)
    cid_readable = codec.build(combo, compact=False)
    cid_compact  = codec.build(combo, compact=True)
    cell = engine.evaluate_cell(combo)
    return {
        "combination_id_readable": cid_readable,
        "combination_id_compact": cid_compact,
        "evaluated_cell": cell
    }

@app.post("/migrate/sqlite")
def migrate_sqlite(req: MigrateSqliteRequest):
    bp = _load_bp(req.blueprint_path, req.schema_path)
    try:
        DB.migrate_sqlite(req.db_path, bp)
    except Exception as e:
        raise HTTPException(500, f"Migration failed: {e}")
    return {"status": "ok", "db_path": req.db_path}
