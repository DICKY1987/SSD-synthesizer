from __future__ import annotations
import re
from typing import Dict, Any

class IDCodec:
    def __init__(self, read_t: str, read_r: str, comp_t: str, comp_r: str):
        self.readable_template = read_t
        self.compact_template  = comp_t
        self._readable_re = re.compile(read_r)
        self._compact_re  = re.compile(comp_r)
    @classmethod
    def from_blueprint(cls, bp: Dict[str, Any]) -> "IDCodec":
        f = bp["conventions"]["id_format"]
        return cls(f["readable"]["template"], f["readable"]["regex"], f["compact"]["template"], f["compact"]["regex"])
    def build(self, combo: Dict[str, Any], compact: bool=False) -> str:
        t = self.compact_template if compact else self.readable_template
        return t.format(**combo)
    def parse(self, combination_id: str) -> Dict[str, Any]:
        m = self._readable_re.match(combination_id) or self._compact_re.match(combination_id)
        if not m: raise ValueError(f"Invalid combination_id: {combination_id}")
        d = m.groupdict()
        if "outcome" in d: d["outcome"] = int(d["outcome"])
        if "generation" in d: d["generation"] = int(d["generation"])
        return d
