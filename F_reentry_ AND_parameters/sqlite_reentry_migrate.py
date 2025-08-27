
    #!/usr/bin/env python3
    import argparse, sqlite3, sys, datetime
from typing import List

DDL_CHAINS = lambda sym: f'''
CREATE TABLE IF NOT EXISTS reentry_chains_{sym} (
  chain_id TEXT PRIMARY KEY,
  original_trade_id INTEGER NOT NULL,
  chain_trades INTEGER NOT NULL DEFAULT 1,
  total_pnl REAL NOT NULL DEFAULT 0,
  chain_status TEXT NOT NULL DEFAULT 'ACTIVE',
  started_at TEXT NOT NULL DEFAULT (datetime('now')),
  ended_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_reentry_chains_{sym}_status ON reentry_chains_{sym}(chain_status);
'''

DDL_EXECUTIONS = lambda sym: f'''
CREATE TABLE IF NOT EXISTS reentry_executions_{sym} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL DEFAULT (datetime('now')),
  action_no INTEGER NOT NULL,
  chain_id TEXT,
  source_trade_id INTEGER,
  reentry_trade_id INTEGER,
  size_lots REAL,
  entry_price REAL,
  generation INTEGER,
  confidence REAL,
  status TEXT,
  exec_ms INTEGER,
  error TEXT
);
CREATE INDEX IF NOT EXISTS idx_reentry_exec_{sym}_chain ON reentry_executions_{sym}(chain_id);
CREATE INDEX IF NOT EXISTS idx_reentry_exec_{sym}_source ON reentry_executions_{sym}(source_trade_id);
CREATE INDEX IF NOT EXISTS idx_reentry_exec_{sym}_status ON reentry_executions_{sym}(status);
'''

DDL_PERF = lambda sym: f'''
CREATE TABLE IF NOT EXISTS reentry_performance_{sym} (
  action_no INTEGER PRIMARY KEY,
  execs INTEGER NOT NULL DEFAULT 0,
  wins INTEGER NOT NULL DEFAULT 0,
  total_pnl REAL NOT NULL DEFAULT 0,
  avg_pnl REAL NOT NULL DEFAULT 0,
  success_rate REAL NOT NULL DEFAULT 0,
  sharpe REAL NOT NULL DEFAULT 0,
  last_updated TEXT NOT NULL DEFAULT (datetime('now'))
);
'''

REQUIRED_TRADE_COLS = [
  ("is_reentry", "INTEGER NOT NULL DEFAULT 0 CHECK (is_reentry IN (0,1))"),
  ("source_trade_id", "INTEGER"),
  ("reentry_action", "INTEGER CHECK (reentry_action BETWEEN 1 AND 6)"),
  ("reentry_generation", "INTEGER NOT NULL DEFAULT 0"),
  ("outcome_classification", "TEXT"),
  ("chain_id", "TEXT")
]

RECOMMENDED_INDEXES = lambda sym: [
  (f"trades_{sym}", f"idx_trades_{sym}_chain", "chain_id"),
  (f"trades_{sym}", f"idx_trades_{sym}_source", "source_trade_id")
]

def table_exists(conn, name: str) -> bool:
  cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
  return cur.fetchone() is not None

def column_exists(conn, table: str, column: str) -> bool:
  cur = conn.execute(f"PRAGMA table_info({table})")
  return any(row[1] == column for row in cur.fetchall())

def index_exists(conn, index: str) -> bool:
  cur = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index,))
  return cur.fetchone() is not None

def ensure_trade_columns(conn, table: str):
  if not table_exists(conn, table):
    # Minimal baseline schema for trades_<SYMBOL>
    conn.execute(f"""
      CREATE TABLE {table} (
        ticket INTEGER PRIMARY KEY,
        open_time TEXT,
        close_time TEXT,
        type TEXT,
        lots REAL,
        open_price REAL,
        close_price REAL,
        profit REAL
      )
    """)
  # Add required reentry columns if missing
  for col, spec in REQUIRED_TRADE_COLS:
    if not column_exists(conn, table, col):
      conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {spec}")

def ensure_indexes(conn, table: str, symbol: str):
  for tbl, idx, cols in RECOMMENDED_INDEXES(symbol):
    if tbl != table:
      continue
    if not index_exists(conn, idx):
      conn.execute(f"CREATE INDEX {idx} ON {tbl}({cols})")

def ensure_pair_objects(conn, symbol: str):
  trades_table = f"trades_{symbol}"
  ensure_trade_columns(conn, trades_table)
  ensure_indexes(conn, trades_table, symbol)
  # Create reentry tables
  conn.executescript(DDL_CHAINS(symbol))
  conn.executescript(DDL_EXECUTIONS(symbol))
  conn.executescript(DDL_PERF(symbol))

def main():
  ap = argparse.ArgumentParser(description='Apply per-pair reentry DB migrations (SQLite).')
  ap.add_argument('--db', required=True, help='Path to SQLite DB file')
  ap.add_argument('--symbols', required=True, help='Comma-separated list, e.g., EURUSD,GBPUSD,USDJPY')
  args = ap.parse_args()
  symbols: List[str] = [s.strip().upper() for s in args.symbols.split(',') if s.strip()]
  if not symbols:
    print('No symbols provided.', file=sys.stderr)
    sys.exit(2)
  conn = sqlite3.connect(args.db)
  try:
    with conn:
      for s in symbols:
        ensure_pair_objects(conn, s)
    print(f"Applied migrations for: {', '.join(symbols)}")
  finally:
    conn.close()

if __name__ == '__main__':
  main()
