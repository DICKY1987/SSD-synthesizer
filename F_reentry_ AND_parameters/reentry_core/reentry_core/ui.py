from __future__ import annotations
from typing import Any, Dict, List
class UI:
    @staticmethod
    def config(blueprint: Dict[str, Any]) -> Dict[str, Any]:
        return blueprint.get("ui_requirements", {})
    @staticmethod
    def grid_columns(blueprint: Dict[str, Any], grid_name: str = "combinations") -> List[Dict[str, Any]]:
        grids = blueprint.get("ui_requirements", {}).get("grids", {})
        grid = grids.get(grid_name, {})
        return grid.get("columns", [])
    @staticmethod
    def color_for_decision(blueprint: Dict[str, Any], decision: str) -> str:
        cmap = blueprint.get("ui_requirements", {}).get("presentation", {}).get("color_map", {}).get("decision", {})
        return cmap.get(decision, "#000000")
    @staticmethod
    def color_for_action(blueprint: Dict[str, Any], action: str) -> str:
        cmap = blueprint.get("ui_requirements", {}).get("presentation", {}).get("color_map", {}).get("action", {})
        return cmap.get(action, "#000000")
