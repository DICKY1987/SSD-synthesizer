from __future__ import annotations
from typing import Any, Dict
import re
from .util import safe_calc

OPS = {
    "eq": lambda a,b: a == b,
    "ne": lambda a,b: a != b,
    "in": lambda a,b: a in b,
    "nin": lambda a,b: a not in b,
    "ge": lambda a,b: a >= b,
    "gt": lambda a,b: a > b,
    "le": lambda a,b: a <= b,
    "lt": lambda a,b: a < b,
    "between": lambda a,b: b[0] <= a <= b[1],
}

class RuleEngine:
    _ENUM_SUBSCRIPT_RE = re.compile(r"enumerations\.([A-Za-z_]+)\.([A-Za-z_]+)\[([A-Za-z_]+)\]")
    def __init__(self, blueprint: Dict[str, Any]):
        self.bp = blueprint
        self.enums = blueprint.get("enumerations", {})
        self.rules = blueprint.get("rules", {})
        self.defaults = blueprint.get("defaults", {})
        self._ctx = {"enumerations": self.enums, "defaults": self.defaults}
    def _resolve_value(self, val: Any, combo: Dict[str, Any]) -> Any:
        if isinstance(val, str) and val.startswith("$ref."):
            cur = self.bp
            for part in val[len("$ref."):].split("."):
                cur = cur[part]
            return cur
        if isinstance(val, str) and val.startswith("$calc:"):
            expr = val[len("$calc:"):]
            def repl(m: re.Match) -> str:
                sect, sub, fieldname = m.group(1), m.group(2), m.group(3)
                key = combo[fieldname]; value = self.enums[sect][sub][key]
                return str(value)
            expr = self._ENUM_SUBSCRIPT_RE.sub(repl, expr)
            return safe_calc(expr, {**self._ctx, **combo})
        return val
    def _ok(self, cnd: Dict[str, Any], combo: Dict[str, Any]) -> bool:
        return OPS[cnd["op"]](combo[cnd["field"]], cnd.get("value"))
    def _blk(self, blk: Dict[str, Any], combo: Dict[str, Any]) -> bool:
        if not blk: return True
        if "all_of" in blk: return all(self._ok(c, combo) for c in blk["all_of"])
        if "any_of" in blk: return any(self._ok(c, combo) for c in blk["any_of"])
        if "not" in blk: return not self._blk(blk["not"], combo)
        return True
    def evaluate_invariants(self, combo: Dict[str, Any]) -> Dict[str, Any] | None:
        invs = sorted(self.rules.get("invariants", []), key=lambda r: r.get("priority", 0), reverse=True)
        for inv in invs:
            if self._blk(inv.get("when", {}), combo):
                then = inv.get("then", {})
                po = {k: self._resolve_value(v, combo) for k, v in then.get("parameter_overrides", {}).items()}
                return {"decision": then.get("decision"), "parameter_set": po}
        return None
    def evaluate_cell(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        rules = sorted(self.rules.get("default_cell_rules", []), key=lambda r: r.get("priority", 0), reverse=True)
        for r in rules:
            if self._blk(r.get("when", {}), combo):
                set_cell = {k: self._resolve_value(v, combo) for k, v in r.get("set_cell", {}).items()}
                set_cell.setdefault("size_multiplier", 1.0)
                set_cell.setdefault("confidence_adjustment", 1.0)
                set_cell.setdefault("delay_minutes", 0)
                set_cell.setdefault("max_attempts", 0)
                return set_cell
        return {"action": "NO_REENTRY", "size_multiplier": 0.0, "confidence_adjustment": 0.0, "delay_minutes": 0, "max_attempts": 0}
    def evaluate_combination_defaults(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        rules = sorted(self.rules.get("default_combination_rules", []), key=lambda r: r.get("priority", 0), reverse=True)
        for r in rules:
            if self._blk(r.get("when", {}), combo):
                then = r.get("then", {})
                param = {k: self._resolve_value(v, combo) for k, v in then.get("parameter_set", {}).items()}
                return {"decision": then.get("decision"), "parameter_set": param}
        return {"decision": "END_TRADING", "parameter_set": {"size_multiplier": 0.0, "confidence_adjustment": 0.0, "delay_minutes": 0, "max_attempts": 0}}
    def evaluate_decision(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        inv = self.evaluate_invariants(combo)
        if inv: return inv
        return self.evaluate_combination_defaults(combo)
