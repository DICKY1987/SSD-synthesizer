
#!/usr/bin/env python3
import argparse, sqlite3, sys
from typing import List

def create_views(conn, sym: str):
    s = sym.upper()
    # Enriched executions view (joins source & reentry tickets to trades_<S> for PnL context)
    conn.execute(f"""
    CREATE VIEW IF NOT EXISTS v_reentry_execs_enriched_{s} AS
    SELECT 
      e.id, e.ts, e.action_no, e.chain_id, e.source_trade_id, e.reentry_trade_id,
      e.size_lots, e.entry_price, e.generation, e.confidence, e.status, e.exec_ms, e.error,
      t_src.open_time  AS src_open_time,
      t_src.close_time AS src_close_time,
      t_src.type       AS src_type,
      t_src.lots       AS src_lots,
      t_src.open_price AS src_open_price,
      t_src.close_price AS src_close_price,
      t_src.profit     AS src_profit,
      t_ret.open_time  AS ret_open_time,
      t_ret.close_time AS ret_close_time,
      t_ret.type       AS ret_type,
      t_ret.lots       AS ret_lots,
      t_ret.open_price AS ret_open_price,
      t_ret.close_price AS ret_close_price,
      t_ret.profit     AS ret_profit
    FROM reentry_executions_{s} e
    LEFT JOIN trades_{s} t_src ON t_src.ticket = e.source_trade_id
    LEFT JOIN trades_{s} t_ret ON t_ret.ticket = e.reentry_trade_id
    """)

    # Trades + lineage view
    conn.execute(f"""
    CREATE VIEW IF NOT EXISTS v_trades_with_reentry_{s} AS
    SELECT 
      t.*,
      t.is_reentry, t.source_trade_id, t.reentry_action, t.reentry_generation, t.outcome_classification, t.chain_id
    FROM trades_{s} t
    """)

    # Chain summary passthrough view
    conn.execute(f"""
    CREATE VIEW IF NOT EXISTS v_reentry_chain_summary_{s} AS
    SELECT chain_id, original_trade_id, chain_trades, total_pnl, chain_status, started_at, ended_at
    FROM reentry_chains_{s}
    """)

    # Action KPIs view (derived on the fly). Note: sharpe left NULL (compute offline).
    conn.execute(f"""
    CREATE VIEW IF NOT EXISTS v_reentry_action_kpis_{s} AS
    WITH base AS (
      SELECT 
        e.action_no,
        COALESCE(t_ret.profit, 0.0) AS pnl
      FROM reentry_executions_{s} e
      LEFT JOIN trades_{s} t_ret ON t_ret.ticket = e.reentry_trade_id
      WHERE e.status IS NULL OR e.status NOT IN ('ABORTED','ERROR')
    ),
    agg AS (
      SELECT 
        action_no,
        COUNT(1) AS execs,
        SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) AS wins,
        SUM(pnl) AS total_pnl,
        AVG(pnl) AS avg_pnl
      FROM base
      GROUP BY action_no
    )
    SELECT 
      action_no,
      execs,
      wins,
      total_pnl,
      avg_pnl,
      CASE WHEN execs = 0 THEN 0.0 ELSE (wins * 1.0) / execs END AS success_rate,
      NULL AS sharpe -- compute in external analytics where STDDEV is available
    FROM agg
    """)

def main():
    ap = argparse.ArgumentParser(description="Create analytics views for reentry tables per symbol.")
    ap.add_argument("--db", required=True, help="Path to SQLite DB")
    ap.add_argument("--symbols", required=True, help="Comma-separated list, e.g., EURUSD,GBPUSD")
    args = ap.parse_args()

    symbols: List[str] = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    if not symbols:
        print("No symbols provided.", file=sys.stderr)
        sys.exit(2)

    conn = sqlite3.connect(args.db)
    try:
        with conn:
            for s in symbols:
                create_views(conn, s)
        print("Created/verified views for:", ", ".join(symbols))
    finally:
        conn.close()

if __name__ == "__main__":
    main()
