from __future__ import annotations
import json, pathlib
from typing import Any, Dict, Optional
try:
    import yaml  # type: ignore
except Exception:
    yaml = None
from .schema_validator import validate_blueprint

class ReentryBlueprint(dict):
    pass

def _load_yaml_or_json(path: str) -> Dict[str, Any]:
    p = pathlib.Path(path)
    if not p.exists(): raise FileNotFoundError(f"Blueprint not found: {path}")
    txt = p.read_text(encoding="utf-8")
    try: return json.loads(txt)
    except Exception: pass
    if yaml is None: raise RuntimeError("PyYAML is required to load YAML. pip install PyYAML")
    return yaml.safe_load(txt)

def load_blueprint(path: str, schema_path: Optional[str] = None) -> ReentryBlueprint:
    bp = ReentryBlueprint(_load_yaml_or_json(path))
    if schema_path: validate_blueprint(bp, schema_path)
    return bp
