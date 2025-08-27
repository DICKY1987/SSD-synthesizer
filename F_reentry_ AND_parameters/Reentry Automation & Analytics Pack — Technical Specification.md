# Reentry Automation & Analytics Pack — Technical Specification

## 1. Purpose & Scope

This specification defines the automation, data, and operational components that surround your MT4 reentry logic. The pack you now have:

* Creates and maintains **per-symbol database schema** for reentry lineage, executions, and KPIs.
* Provides **analytics views** for reporting.
* Manages **persona-based per-symbol CSV profiles** that the EA reads at runtime.
* Schedules **daily profile rotation** and **weekly KPI exports**.
* Supplies **end-to-end installation, autodiscovery, verification**, and **task rendering** driven by a single JSON config.

> **Boundary:** This pack does **not** contain the EA itself. It assumes your EA (or a bridge) reads `MQL4\Files\config\<SYMBOL>_reentry.csv`, makes decisions/entries, and writes trade/reentry records to SQLite as specified herein.

---

## 2. System Context

### 2.1 Actors & Responsibilities

* **EA (MT4)**

  * Reads: `…\MQL4\Files\config\<SYMBOL>_reentry.csv` (per-symbol, persona-specific reentry actions 1–6).
  * Writes: `trades_<SYMBOL>` (extended columns), `reentry_executions_<SYMBOL>` records for each realized reentry, updates `reentry_chains_<SYMBOL>` and `reentry_performance_<SYMBOL>` (or leaves KPIs to analytics jobs).
* **Automation Pack (this repo of scripts & tasks)**

  * Creates/maintains DB schema and views.
  * Rotates persona profiles into EA config path.
  * Exports weekly KPI CSVs.
  * Verifies install health and paths.
  * Renders Windows Task Scheduler XML jobs from JSON config.

### 2.2 Data Flow (high level)

1. **Profiles**: Daily Task copies persona CSVs → EA config path.
2. **EA runtime**: EA loads per-symbol CSV → executes reentries → records lineage/executions in DB.
3. **KPI export**: Weekly Task runs sqlite3 queries → exports enriched executions & action KPIs to CSV → operator review.
4. **DB maintenance**: Idempotent migrator ensures tables/columns exist for new symbols.

---

## 3. Configuration (Single Source of Truth)

### 3.1 `reentry_pack_config.json`

```json
{
  "symbols": ["EURUSD","USDJPY","GBPUSD","USDCHF","USDCAD","AUDUSD","NZDUSD","EURJPY","GBPJPY","EURGBP"],
  "paths": {
    "profiles_root": "C:\\FX\\ReentryProfiles",
    "config_root": "C:\\MT4\\MQL4\\Files\\config",
    "db_path": "C:\\FX\\data\\trades.db",
    "sqlite_exe": "C:\\Program Files\\SQLite\\sqlite3.exe",
    "scripts_dir": "C:\\FX\\scripts",
    "reports_dir": "C:\\FX\\reports\\weekly",
    "logs_dir": "C:\\FX\\logs"
  },
  "personas": {
    "cycle_map": {
      "Monday": "conservative",
      "Tuesday": "moderate",
      "Wednesday": "aggressive",
      "Thursday": "conservative",
      "Friday": "moderate",
      "Saturday": "conservative",
      "Sunday": "moderate"
    },
    "fallback_cycle": ["conservative","moderate","aggressive"]
  },
  "scheduling": {
    "profile_rotate": { "time": "06:45", "frequency": "DAILY" },
    "weekly_kpi":     { "day": "Sunday", "time": "18:00" }
  }
}
```

* **Edit once**; every script and task uses these values.
* `detect_mt4_config.ps1` can auto-set `paths.config_root`.

---

## 4. Data Contracts

### 4.1 Trades Table (per symbol, created/extended by migrator)

`trades_<SYMBOL>` (baseline columns may already exist; migrator adds the reentry columns if missing)

| Column                      | Type    | Notes                               |
| --------------------------- | ------- | ----------------------------------- |
| ticket (PK)                 | INTEGER | Trade ticket                        |
| open\_time                  | TEXT    | ISO-like                            |
| close\_time                 | TEXT    | ISO-like                            |
| type                        | TEXT    | buy/sell                            |
| lots                        | REAL    |                                     |
| open\_price                 | REAL    |                                     |
| close\_price                | REAL    |                                     |
| profit                      | REAL    |                                     |
| **is\_reentry**             | INTEGER | 0/1                                 |
| **source\_trade\_id**       | INTEGER | Ticket of parent trade              |
| **reentry\_action**         | INTEGER | 1–6 bucket chosen                   |
| **reentry\_generation**     | INTEGER | 0 for originals, 1..N for reentries |
| **outcome\_classification** | TEXT    | ML/B/MG bucket label or code        |
| **chain\_id**               | TEXT    | UUID/ID string grouping the chain   |

*Indexes:* `idx_trades_<SYMBOL>_chain(chain_id)`, `idx_trades_<SYMBOL>_source(source_trade_id)`

### 4.2 Reentry Chains (per symbol)

`reentry_chains_<SYMBOL>`

| Column              | Type    | Notes                     |
| ------------------- | ------- | ------------------------- |
| chain\_id (PK)      | TEXT    | Unique chain identifier   |
| original\_trade\_id | INTEGER | Root ticket               |
| chain\_trades       | INTEGER | Count of trades in chain  |
| total\_pnl          | REAL    | Aggregate P\&L            |
| chain\_status       | TEXT    | ACTIVE / STOPPED / ENDED  |
| started\_at         | TEXT    | default `datetime('now')` |
| ended\_at           | TEXT    | nullable                  |

*Index:* `idx_reentry_chains_<SYMBOL>_status(chain_status)`

### 4.3 Reentry Executions (per symbol)

`reentry_executions_<SYMBOL>`

| Column             | Type    | Notes                     |
| ------------------ | ------- | ------------------------- |
| id (PK)            | INTEGER | AUTOINCREMENT             |
| ts                 | TEXT    | default now               |
| action\_no         | INTEGER | 1–6                       |
| chain\_id          | TEXT    | FK to chains (logical)    |
| source\_trade\_id  | INTEGER | Ticket triggering reentry |
| reentry\_trade\_id | INTEGER | Ticket created by action  |
| size\_lots         | REAL    | Executed size             |
| entry\_price       | REAL    |                           |
| generation         | INTEGER | 1..N                      |
| confidence         | REAL    | Optional metric           |
| status             | TEXT    | NULL/OK/ABORTED/ERROR     |
| exec\_ms           | INTEGER | Execution latency         |
| error              | TEXT    | Error detail if any       |

*Indexes:* by `chain_id`, `source_trade_id`, `status`

### 4.4 Reentry Performance (per symbol)

`reentry_performance_<SYMBOL>`

| Column          | Type    | Notes            |
| --------------- | ------- | ---------------- |
| action\_no (PK) | INTEGER | 1–6              |
| execs           | INTEGER | Total executions |
| wins            | INTEGER | pnl > 0          |
| total\_pnl      | REAL    |                  |
| avg\_pnl        | REAL    |                  |
| success\_rate   | REAL    | wins/execs       |
| sharpe          | REAL    | computed offline |
| last\_updated   | TEXT    | default now      |

### 4.5 Analytics Views (per symbol)

* `v_reentry_execs_enriched_<SYMBOL>`: `reentry_executions` + joined `trades` for `src_*` and `ret_*` P\&L context.
* `v_trades_with_reentry_<SYMBOL>`: `trades` with reentry columns.
* `v_reentry_chain_summary_<SYMBOL>`: pass-through chain summary.
* `v_reentry_action_kpis_<SYMBOL>`: derived KPIs (execs, wins, totals, avg, success\_rate; `sharpe` left `NULL`).

---

## 5. Profile Contract (EA Input)

### 5.1 `reentry_profile_template.csv` (per symbol)

Columns: `Action,Type,SizeMultiplier,DelaySeconds,ConfidenceAdjustment,Parameters`

* **Action**: `1..6` (bucket slot)
* **Type**: `NO_REENTRY|SAME_TRADE|REDUCE_SIZE|INCREASE_SIZE|AGGRESSIVE|REVERSE|WAIT_SIGNAL|CUSTOM`
* **SizeMultiplier**: float (relative lot scaling)
* **DelaySeconds**: integer ≥ 0
* **ConfidenceAdjustment**: float (offset, optional)
* **Parameters**: free-form `key=value;key=value` for EA/bridge

> **Daily persona rotation** copies `<ProfilesRoot>\<persona>\<SYMBOL>_reentry.csv` → `…\MQL4\Files\config\<SYMBOL>_reentry.csv`.

---

## 6. Components & Interfaces

### 6.1 Database Layer

* **`sqlite_reentry_migrate.py`**
  **CLI:** `--db <path> --symbols EURUSD,GBPUSD,…`
  **Behavior:** Ensures `trades_<SYMBOL>` (adds reentry columns), creates `reentry_chains_*`, `reentry_executions_*`, `reentry_performance_*` and indexes. **Idempotent**.
* **`sqlite_reentry_create_views.py`**
  **CLI:** `--db <path> --symbols …`
  **Behavior:** Creates/ensures four analytics views per symbol. **Idempotent**.
* **`seed_reentry_performance.py` / `seed_reentry_performance.sql`**
  Seeds rows `action_no=1..6` per symbol if missing.

### 6.2 Profile Management

* **`reentry_profile_rotate.ps1`**
  **Params:** `-ProfilesRoot -ConfigRoot -Symbols -Persona (opt) -PersonaCycle -WhatIf -LogPath`
  **Behavior:** Chooses persona via `cycle_map` (or `-Persona`), copies per-symbol CSVs to EA config path; logs actions. **Dry-run** supported via `-WhatIf`.

### 6.3 KPI Exports

* **`reentry_kpi_snapshot.ps1`**
  **Params:** `-DbPath -SQLiteExe -OutDir -Symbols -WhatIf`
  **Behavior:** Exports `v_reentry_execs_enriched_*` and `v_reentry_action_kpis_*` to CSV per symbol; emits a `SUMMARY.txt`.

### 6.4 Task Rendering & Scheduling

* **`render_reentry_tasks.py`**
  Reads `reentry_pack_config.json`, emits Task XMLs:

  * `Task_ProfileRotate.xml` — daily at `scheduling.profile_rotate.time`.
  * `Task_KPIWeekly.xml` — weekly on `scheduling.weekly_kpi.day` at `time`.
* **Windows Tasks** (import or register):

  * **Profile Rotate** → runs `reentry_profile_rotate.ps1` with configured symbols/paths.
  * **Weekly KPIs** → runs `reentry_kpi_snapshot.ps1`.

### 6.5 Install, Detect, Verify

* **`detect_mt4_config.ps1`**
  Searches `%APPDATA%`, `%LOCALAPPDATA%`, `%ProgramFiles%`, `%ProgramFiles(x86)%` for `MQL4\Files\config`; prints (or updates JSON with `-UpdateJson`).
* **`install_reentry_pack.ps1`**
  **Params:** `-ConfigPath -AutoDetectMT4 -RegisterTasks -TaskPrefix -RunUser -RunPass`
  **Behavior:** Copies scripts to `scripts_dir`, runs DB migrate, creates views, seeds KPI rows, renders tasks, and optionally registers them via `schtasks`.
* **`verify_reentry_install.ps1`**
  **Behavior:** Checks DB tables/views (via `sqlite3.exe` if present), presence of scripts, and at least one `<SYMBOL>_reentry.csv` in `config_root`.

### 6.6 Governance Artifacts

* **`governance_checklist.csv` / `.md`**
  Maps **controls** → EA inputs / CSV columns → **enforcement points** → **telemetry**.
  Examples: `AllowReentry`, `MinDelaySeconds`, `MaxGenerations`, `DailyLossLimit`, `MaxPositionSize`, `MaxSpreadPoints`, `BlackoutAfterLosses`, `ReentryMagicBase`, etc.

---

## 7. End-to-End Operational Workflows

### 7.1 First-Time Installation

1. *(Optional)* `detect_mt4_config.ps1 -UpdateJson -ConfigJson .\reentry_pack_config.json`
2. `install_reentry_pack.ps1 -ConfigPath .\reentry_pack_config.json`

   * Migrates DB for all `symbols`
   * Creates analytics views
   * Seeds KPIs
   * Renders Task XMLs into working dir
3. Import `Task_ProfileRotate.xml` and `Task_KPIWeekly.xml` in Windows Task Scheduler (or rerun installer with `-RegisterTasks`).

### 7.2 Daily Operation

* **06:45** (default): Profile rotation runs → persona CSVs refreshed in EA config path before trading day.
* EA reads per-symbol CSVs on init/reload; executes reentries; writes DB records.

### 7.3 Weekly Operation

* **Sunday 18:00** (default): KPI task exports enriched executions and action-level KPIs per symbol.
* Review outputs in `reports_dir`; optionally feed into BI dashboards.

---

## 8. Non-Functional Requirements

* **Idempotency:** All migrations and view creations can be rerun safely.
* **Determinism:** JSON config guarantees consistent scripts/paths; tasks rendered from the same JSON produce identical schedules/arguments (modulo `StartBoundary` timestamp).
* **Observability:**

  * Logs: `reentry_profile_rotate.ps1` appends to `logs_dir`.
  * CSV exports: auditable artifacts in `reports_dir`.
* **Security:**

  * Windows account for scheduled tasks should have least privileges for `scripts_dir`, `db_path`, and `config_root`.
  * Paths are local; no network calls.
* **Compatibility:**

  * **SQLite** with `sqlite3.exe` for exports; Python 3.x for migrations/views/seed.
  * **PowerShell 5.1+** for scripts.

---

## 9. Error Handling & Failure Modes

| Scenario                | Detection                    | Behavior               | Operator Action                                          |
| ----------------------- | ---------------------------- | ---------------------- | -------------------------------------------------------- |
| `config_root` not found | `verify_reentry_install.ps1` | Warning                | Run `detect_mt4_config.ps1` or set JSON path             |
| DB missing or locked    | Installer/verifier           | Error/Warning          | Ensure path/permissions; retry                           |
| `sqlite3.exe` missing   | KPI script/verifier          | KPI export skipped     | Install SQLite CLI or update path                        |
| Missing profile CSVs    | Verifier                     | Warning                | Populate `<ProfilesRoot>\<persona>\<SYMBOL>_reentry.csv` |
| EA not writing DB rows  | KPI exports show empty data  | KPI zeros/empty        | Check EA/bridge integration                              |
| Task not running        | Task history                 | Missed rotation/export | Verify credentials, “Run whether user is logged on”      |

---

## 10. Interfaces & Commands

### 10.1 Installer

```powershell
# Install end-to-end
powershell -ExecutionPolicy Bypass -File install_reentry_pack.ps1 -ConfigPath .\reentry_pack_config.json

# Auto-register Windows tasks (optional)
powershell -ExecutionPolicy Bypass -File install_reentry_pack.ps1 -ConfigPath .\reentry_pack_config.json -RegisterTasks -TaskPrefix Reentry
```

### 10.2 Migrations & Views

```powershell
python sqlite_reentry_migrate.py --db C:\FX\data\trades.db --symbols EURUSD,GBPUSD,USDJPY
python sqlite_reentry_create_views.py --db C:\FX\data\trades.db --symbols EURUSD,GBPUSD,USDJPY
python seed_reentry_performance.py --db C:\FX\data\trades.db --symbols EURUSD,GBPUSD,USDJPY
```

### 10.3 Profiles & KPIs

```powershell
powershell -ExecutionPolicy Bypass -File reentry_profile_rotate.ps1 -ProfilesRoot "C:\FX\ReentryProfiles" -ConfigRoot "C:\MT4\MQL4\Files\config" -Symbols "EURUSD,GBPUSD,USDJPY"
powershell -ExecutionPolicy Bypass -File reentry_kpi_snapshot.ps1 -DbPath "C:\FX\data\trades.db" -SQLiteExe "C:\Program Files\SQLite\sqlite3.exe" -OutDir "C:\FX\reports\weekly" -Symbols "EURUSD,GBPUSD,USDJPY"
```

### 10.4 Health Checks

```powershell
powershell -ExecutionPolicy Bypass -File verify_reentry_install.ps1 -ConfigPath .\reentry_pack_config.json
```

---

## 11. Governance Mapping (Excerpt)

| Control           | EA Input          | CSV Column       | Enforcement Point | Telemetry                      |
| ----------------- | ----------------- | ---------------- | ----------------- | ------------------------------ |
| Allow Reentry     | `AllowReentry`    | —                | Analyzer/Gate     | `trades.is_reentry`            |
| Min Delay (s)     | `MinDelaySeconds` | `DelaySeconds`   | Gate + Executor   | `reentry_executions.ts`        |
| Max Generations   | `MaxGenerations`  | —                | Analyzer/Gate     | `trades.reentry_generation`    |
| Daily Loss Limit  | `DailyLossLimit`  | —                | Gate              | P\&L aggregation               |
| Max Position Size | `MaxPositionSize` | `SizeMultiplier` | Executor          | `reentry_executions.size_lots` |
| Spread Guard      | `MaxSpreadPoints` | —                | Executor          | Exec logs                      |

> Full table provided in `governance_checklist.csv` / `.md`.

---

## 12. Testing Strategy

* **Schema smoke:** Run migrator on empty DB, confirm tables; rerun to confirm idempotency.
* **View integrity:** Insert synthetic trades/executions; confirm views aggregate correctly.
* **Profile rotation:** Use `-WhatIf` to validate source→dest mapping; then live copy for one symbol.
* **KPI exports:** Populate minimal `reentry_executions` + `trades`; run export; inspect CSVs.
* **Tasks:** Import XMLs; run “Run Now”; verify logs/CSV outputs.
* **Verifier:** Ensure it flags missing artifacts; confirm “PASSED” with complete setup.

---

## 13. Deployment & Rollback

* **Deploy:**

  1. Commit/edit `reentry_pack_config.json`
  2. Run installer
  3. Import/Register tasks
  4. Run verifier
* **Rollback:**

  * Disable tasks; back up DB; drop generated tables/views if required.
  * Profiles are just CSV copies—safe to restore from `profiles_root`.

---

## 14. Future Integration Hooks (Non-blocking)

* **Sharpe & risk KPIs**: Extend KPI job to compute Sharpe from rolling PnL series.
* **FastAPI façade**: Wrap `/migrate/sqlite`, `/views/create`, `/kpi/export` for service orchestration.
* **Live profile reload**: If EA supports, add periodic reload (already in governance table as optional control).

---

## 15. File Inventory (Created by this Pack)

* **DB & Views**: `sqlite_reentry_migrate.py`, `sqlite_reentry_migration_template.sql`, `sqlite_reentry_create_views.py`, `seed_reentry_performance.py`, `seed_reentry_performance.sql`
* **Profiles**: `reentry_profile_template.csv`, `reentry_profile_rotate.ps1`
* **KPI Exports**: `reentry_kpi_snapshot.ps1`
* **Tasks**: `render_reentry_tasks.py`, `Task_ProfileRotate.xml`, `Task_KPIWeekly.xml`
* **Install Ops**: `detect_mt4_config.ps1`, `install_reentry_pack.ps1`, `verify_reentry_install.ps1`, `reentry_apply_config.ps1`
* **Docs/Governance**: `governance_checklist.csv`, `governance_checklist.md`, `AUTOMATION_README.md`
* **Config**: `reentry_pack_config.json`

---

## 16. Acceptance Criteria

* **AC-1**: Running installer on a clean machine creates schema/tables/views for all symbols without error.
* **AC-2**: Daily profile rotation copies the correct persona CSVs into EA config for every symbol.
* **AC-3**: Weekly KPI export produces per-symbol CSVs populated when DB has data.
* **AC-4**: Verifier reports “PASSED” after installation and profile provisioning.
* **AC-5**: All paths and schedules match `reentry_pack_config.json`.

---

## 17. Glossary

* **Persona**: Named profile set (e.g., conservative/moderate/aggressive) mapping 1–6 outcome buckets to action types/parameters.
* **Chain**: A lineage of the original trade and subsequent reentries (tracked by `chain_id`).
* **Bucket**: One of six mutually exclusive classifications of how the prior trade performed (ML/B/MG relations), aligned to action slots 1–6.

---

**This specification fully describes how the created files interlock to produce a functioning, automated reentry support system around your EA: data schema, runtime profiles, scheduled operations, analytics exports, and governance controls—configured by a single JSON and verifiable end-to-end.**
