
-- SQLite Reentry Tables Template (Per-Symbol)
-- Replace ${SYMBOL} with your symbol code (e.g., EURUSD) before running.
-- Note: SQLite lacks conditional ALTER COLUMN; use the Python migrator for idempotent column adds to trades_${SYMBOL}.

BEGIN;

CREATE TABLE IF NOT EXISTS reentry_chains_${SYMBOL} (
  chain_id TEXT PRIMARY KEY,
  original_trade_id INTEGER NOT NULL,
  chain_trades INTEGER NOT NULL DEFAULT 1,
  total_pnl REAL NOT NULL DEFAULT 0,
  chain_status TEXT NOT NULL DEFAULT 'ACTIVE',
  started_at TEXT NOT NULL DEFAULT (datetime('now')),
  ended_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_reentry_chains_${SYMBOL}_status ON reentry_chains_${SYMBOL}(chain_status);

CREATE TABLE IF NOT EXISTS reentry_executions_${SYMBOL} (
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
CREATE INDEX IF NOT EXISTS idx_reentry_exec_${SYMBOL}_chain ON reentry_executions_${SYMBOL}(chain_id);
CREATE INDEX IF NOT EXISTS idx_reentry_exec_${SYMBOL}_source ON reentry_executions_${SYMBOL}(source_trade_id);
CREATE INDEX IF NOT EXISTS idx_reentry_exec_${SYMBOL}_status ON reentry_executions_${SYMBOL}(status);

CREATE TABLE IF NOT EXISTS reentry_performance_${SYMBOL} (
  action_no INTEGER PRIMARY KEY,
  execs INTEGER NOT NULL DEFAULT 0,
  wins INTEGER NOT NULL DEFAULT 0,
  total_pnl REAL NOT NULL DEFAULT 0,
  avg_pnl REAL NOT NULL DEFAULT 0,
  success_rate REAL NOT NULL DEFAULT 0,
  sharpe REAL NOT NULL DEFAULT 0,
  last_updated TEXT NOT NULL DEFAULT (datetime('now'))
);

COMMIT;
