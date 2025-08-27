
#!/usr/bin/env python3
import argparse, sqlite3, json

def main():
    ap = argparse.ArgumentParser(description="Seed reentry_performance_<SYMBOL> with rows 1..6 if empty.")
    ap.add_argument("--db", required=True)
    ap.add_argument("--symbols", required=True, help="Comma-separated list")
    args = ap.parse_args()
    syms = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    conn = sqlite3.connect(args.db)
    try:
        with conn:
            for sym in syms:
                for a in range(1,7):
                    conn.execute(f"INSERT OR IGNORE INTO reentry_performance_{sym} (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated) VALUES (?,0,0,0,0,0,0,datetime('now'))", (a,))
        print("Seeded tables for:", ", ".join(syms))
    finally:
        conn.close()
if __name__ == "__main__":
    main()
