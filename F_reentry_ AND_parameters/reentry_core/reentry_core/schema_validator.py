from __future__ import annotations
import json, pathlib
from typing import Any, Dict

def _fallback_validate(bp: Dict[str, Any]) -> None:
    required = ["schema_version","conventions","enumerations","persistence","rules","ui_requirements"]
    missing = [k for k in required if k not in bp]
    if missing: raise ValueError(f"Blueprint missing top-level keys: {missing}")
    if "canonical_coordinate_order" not in bp["conventions"]:
        raise ValueError("conventions.canonical_coordinate_order is required")
    if len(bp["conventions"]["canonical_coordinate_order"]) != 6:
        raise ValueError("canonical_coordinate_order must have exactly 6 elements")

def validate_blueprint(bp: Dict[str, Any], schema_path: str) -> None:
    try:
        import jsonschema  # type: ignore
    except Exception:
        _fallback_validate(bp); return
    schema = json.loads(pathlib.Path(schema_path).read_text(encoding="utf-8"))
    jsonschema.validate(instance=bp, schema=schema)
