
# Reentry DB Views & Automation Pack

This pack adds analytics views, rotates persona-based reentry profiles, and snapshots weekly KPIs.

## Files
- `sqlite_reentry_create_views.py` — Creates analytics views for each symbol in the SQLite DB.
- `reentry_profile_rotate.ps1` — Copies persona CSVs into the EA config directory per symbol.
- `reentry_kpi_snapshot.ps1` — Exports enriched executions and action KPIs to CSV via `sqlite3.exe`.
- `Task_ProfileRotate.xml` — Windows Task Scheduler (daily 06:45) to run profile rotation.
- `Task_KPIWeekly.xml` — Windows Task Scheduler (Sundays 18:00) to run KPI snapshot.

## Usage

### 1) Create views
```powershell
python /mnt/data/sqlite_reentry_create_views.py --db C:\FX\data\trades.db --symbols EURUSD,GBPUSD,USDJPY
```

### 2) Rotate profiles
Place persona CSVs here: `C:\FX\ReentryProfiles\<persona>\<SYMBOL>_reentry.csv`  
Example: `C:\FX\ReentryProfiles\conservative\EURUSD_reentry.csv`

Run manually:
```powershell
powershell -ExecutionPolicy Bypass -File /mnt/data/reentry_profile_rotate.ps1 -ProfilesRoot "C:\FX\ReentryProfiles" -ConfigRoot "C:\MT4\MQL4\Files\config" -Symbols "EURUSD,GBPUSD,USDJPY"
```
Dry run:
```powershell
powershell -ExecutionPolicy Bypass -File /mnt/data/reentry_profile_rotate.ps1 -WhatIf
```

### 3) KPI snapshot
Requires `sqlite3.exe` on PATH or provide full path via `-SQLiteExe`.
```powershell
powershell -ExecutionPolicy Bypass -File /mnt/data/reentry_kpi_snapshot.ps1 -DbPath "C:\FX\data\trades.db" -SQLiteExe "C:\Program Files\SQLite\sqlite3.exe" -OutDir "C:\FX\reports\weekly" -Symbols "EURUSD,GBPUSD,USDJPY"
```

### 4) Import scheduled tasks
Open **Task Scheduler** → **Import Task...** → select the XML file. Edit paths, account, and triggers if needed.

## Notes
- Views reference `trades_<SYMBOL>`, `reentry_executions_<SYMBOL>`, and `reentry_chains_<SYMBOL>` populated by your migrator.
- The KPIs view leaves `sharpe` as `NULL`; compute Sharpe ratio in Python/R/Power BI where standard deviation is available.
- Profile rotation uses a day-of-week → persona map; adjust inside the script to your policy.
