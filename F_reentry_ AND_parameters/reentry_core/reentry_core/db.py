from __future__ import annotations
import sqlite3, pathlib
from typing import Any, Dict
class DB:
    @staticmethod
    def migrate_sqlite(path: str, blueprint: Dict[str, Any]) -> None:
        ddl = blueprint["persistence"]["database"]["ddl"]["sqlite"]
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(path)
        try:
            con.executescript(ddl)
            con.commit()
        finally:
            con.close()
    @staticmethod
    def generate_postgres_sql(blueprint: Dict[str, Any]) -> str:
        return blueprint["persistence"]["database"]["ddl"]["postgres"]
