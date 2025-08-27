BEGIN;

    INSERT INTO reentry_performance_EURUSD (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_EURUSD rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_USDJPY (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_USDJPY rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_GBPUSD (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_GBPUSD rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_USDCHF (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_USDCHF rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_USDCAD (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_USDCAD rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_AUDUSD (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_AUDUSD rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_NZDUSD (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_NZDUSD rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_EURJPY (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_EURJPY rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_GBPJPY (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_GBPJPY rp WHERE rp.action_no = a.no);
    

    INSERT INTO reentry_performance_EURGBP (action_no, execs, wins, total_pnl, avg_pnl, success_rate, sharpe, last_updated)
    SELECT a.no, 0, 0, 0.0, 0.0, 0.0, 0.0, datetime('now')
    FROM (SELECT 1 as no UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) a
    WHERE NOT EXISTS (SELECT 1 FROM reentry_performance_EURGBP rp WHERE rp.action_no = a.no);
    
COMMIT;