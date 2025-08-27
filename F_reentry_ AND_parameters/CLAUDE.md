# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This directory contains the **Reentry Automation & Analytics Pack** - an advanced trade reentry decision system for MetaTrader 4 that classifies trade outcomes into six buckets and executes follow-up actions based on configurable profiles and multi-dimensional analysis.

**Parent System**: HUEY_P Trading System (MT4 Terminal: F2262CFAFF47C27887389DAB2852351A)
**Core Purpose**: Automated reentry logic based on trade performance relative to key levels (ML, B, MG)
**Architecture**: FastAPI service + PowerShell automation + SQLite analytics + MQL4 EA integration

## Core Development Commands

### FastAPI Service Operations
```bash
# Environment setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Service startup (development)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Configuration with environment variables
set REENTRY_BLUEPRINT=C:\path\to\reentry_blueprint.yaml
set REENTRY_SCHEMA=C:\path\to\reentry_blueprint.schema.json
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Database Migration and Setup
```bash
# SQLite database migration (per-symbol)
python sqlite_reentry_migrate.py --db "C:\FX\data\trades.db" --symbols "EURUSD,GBPUSD,USDJPY"

# Create analytics views
python sqlite_reentry_create_views.py --db "C:\FX\data\trades.db" --symbols "EURUSD,GBPUSD,USDJPY"

# Seed performance tracking tables
python seed_reentry_performance.py --db "C:\FX\data\trades.db" --symbols "EURUSD,GBPUSD,USDJPY"
```

### PowerShell Automation
```powershell
# Detect MT4 configuration paths automatically
powershell -ExecutionPolicy Bypass -File detect_mt4_config.ps1 -UpdateJson -ConfigJson .\reentry_pack_config.json

# Full system installation
powershell -ExecutionPolicy Bypass -File install_reentry_pack.ps1 -ConfigPath .\reentry_pack_config.json

# Profile rotation (manual execution)
powershell -ExecutionPolicy Bypass -File reentry_profile_rotate.ps1 -ProfilesRoot "C:\FX\ReentryProfiles" -ConfigRoot "C:\MT4\MQL4\Files\config" -Symbols "EURUSD,GBPUSD,USDJPY"

# Weekly KPI snapshot generation
powershell -ExecutionPolicy Bypass -File reentry_kpi_snapshot.ps1 -DbPath "C:\FX\data\trades.db" -SQLiteExe "C:\Program Files\SQLite\sqlite3.exe" -OutDir "C:\FX\reports\weekly" -Symbols "EURUSD,GBPUSD,USDJPY"

# Installation verification
powershell -ExecutionPolicy Bypass -File verify_reentry_install.ps1 -ConfigPath .\reentry_pack_config.json
```

### Testing and Validation
```bash
# Python testing framework
python testing-framework.py

# Real-time monitoring server
python realtime-monitoring-server.py

# Signal queue risk system validation
python signal-queue-risk-system.py
```

## Six-Bucket Trade Classification System

### Core Logic Framework
The system classifies every closed trade into exactly one of six mutually exclusive buckets based on the trade's exit point (R) relative to three key levels:

- **ML**: Original stop loss level
- **B**: Breakeven level (entry price)  
- **MG**: Original take profit level

### Bucket Definitions and Actions
1. **R = ML** → Action 1 (typically NO_REENTRY)
2. **ML < R < B** → Action 2 (typically REDUCE_SIZE)
3. **R = B** → Action 3 (typically SAME_TRADE)
4. **B < R < MG** → Action 4 (typically INCREASE_SIZE)
5. **R = MG** → Action 5 (typically SAME_TRADE)
6. **R > MG** → Action 6 (typically AGGRESSIVE)

### Float-Tolerant Classification
```python
# Core classification logic (machine-readable)
def determineNextAction(R, ML, MG, B, tolerance=0.0001):
    if abs(R - ML) <= tolerance: return 1
    if ML < R < B: return 2
    if abs(R - B) <= tolerance: return 3
    if B < R < MG: return 4
    if abs(R - MG) <= tolerance: return 5
    if R > MG: return 6
    return 0  # Error case
```

## Configuration Architecture

### Central Configuration (`reentry_pack_config.json`)
Centralized configuration controlling:
- **Symbols**: Trading pairs for reentry system
- **Paths**: Database, profiles, reports, and MT4 directories
- **Personas**: Conservative/Moderate/Aggressive profile rotation
- **Scheduling**: Automated task timing

### Profile System (`reentry_profile_template.csv`)
Per-symbol CSV configuration with six rows:
```csv
Action,Type,SizeMultiplier,DelaySeconds,ConfidenceAdjustment,Parameters
1,NO_REENTRY,0.0,0,0.0,""
2,REDUCE_SIZE,0.5,300,0.1,"spread_mult=1.5"
3,SAME_TRADE,1.0,180,0.0,"same_direction=true"
4,INCREASE_SIZE,1.5,120,0.2,"confidence_boost=0.1"
5,SAME_TRADE,1.0,60,0.0,"same_direction=true"
6,AGGRESSIVE,2.0,30,0.3,"reverse_allowed=true"
```

### Blueprint System (`reentry_blueprint.yaml`)
YAML-based configuration with JSON schema validation covering:
- Multi-dimensional matrix parameters
- Invariant rules and combination logic
- UI requirements and display preferences
- Database schema definitions

## Database Schema Extensions

### Core Reentry Tables (Per Symbol)
- **`trades_<SYMBOL>`**: Extended with reentry tracking columns
  - `is_reentry`, `source_trade_id`, `reentry_action`, `reentry_generation`
  - `outcome_classification`, `chain_id`

- **`reentry_chains_<SYMBOL>`**: Chain tracking and analytics
  - `chain_id`, `original_trade_id`, `chain_trades[]`, `total_pnl`
  - `chain_status`, `max_generation`, `creation_time`

- **`reentry_executions_<SYMBOL>`**: Detailed execution audit
  - `execution_time`, `action_no`, `chain_id`, `source_trade_id`
  - `reentry_trade_id`, `lot_size`, `entry_price`, `generation`
  - `confidence_score`, `execution_status`, `execution_time_ms`

- **`reentry_performance_<SYMBOL>`**: Per-action KPI tracking
  - `action_no`, `total_executions`, `successful_executions`
  - `total_pnl`, `average_pnl`, `success_rate`, `sharpe_ratio`

### Analytics Views
Automatically generated SQL views for each symbol:
- `reentry_summary_<SYMBOL>`: Chain performance overview
- `reentry_action_kpis_<SYMBOL>`: Per-action success metrics
- `reentry_enriched_executions_<SYMBOL>`: Detailed execution analysis

## FastAPI Service Architecture

### Core Endpoints
- **GET /health** → System health check
- **GET /ui/config** → Blueprint UI requirements
- **POST /decide** → Evaluate reentry decision with combination rules
- **POST /cell** → Return default cell evaluation
- **POST /migrate/sqlite** → Execute database DDL

### Request/Response Models
```python
class Combo(BaseModel):
    symbol: str
    signal_type: str
    time_category: str
    outcome: int  # 1-6 bucket classification
    context: str
    generation: int

class DecideRequest(BaseModel):
    combo: Combo
    blueprint_path: Optional[str] = None
    schema_path: Optional[str] = None
```

### Multi-Dimensional Matrix System
34,560 total combinations across:
- **Generations**: 0 (original), 1-3 (reentry levels)
- **Trade Types**: Various signal classifications
- **Time Categories**: FLASH, INSTANT, QUICK, SHORT, MEDIUM, LONG, EXTENDED
- **Outcomes**: 1-6 bucket results
- **Context**: Temporal relationship indicators

## MQL4 EA Integration

### CReentryLogic Class Structure
```mql4
class CReentryLogic {
private:
    ReentryAction m_actions[6];  // Actions 1-6 configuration
    bool m_enabled;              // System toggle
    
public:
    bool LoadReentryConfiguration(string symbol);
    int DetermineNextAction(double R, double ML, double MG, double B);
    bool ExecuteReentryAction(int action_no, /* trade details */);
}
```

### Integration Points
- **OnInit()**: Load reentry configuration from CSV
- **OnTrade()**: Trigger reentry analysis on trade closure
- **Profile Loading**: Read `config\<SYMBOL>_reentry.csv`
- **Magic Number Offset**: Base + 1000 + generation for reentry identification

## Automation and Scheduling

### Windows Task Scheduler Integration
- **Profile Rotation**: Daily 06:45 - `Task_ProfileRotate.xml`
- **Weekly KPI Reports**: Sundays 18:00 - `Task_KPIWeekly.xml`

### Governance and Risk Controls
Configurable enforcement parameters:
- `enabled`, `min_delay`, `max_generations`, `daily_loss_limit`
- `min_confidence`, `blackout_after_losses`, `max_position_size`
- Runtime validation with circuit breaker integration

## Development Safety and Constraints

### Live Trading Environment
- **Real Money Risk**: System connects to live trading account
- **Pre-deployment Testing**: Always test reentry logic in Strategy Tester
- **Profile Validation**: Verify CSV profile syntax before deployment
- **Database Backups**: Automated backups before schema modifications

### File Access Patterns
- **Config Files**: UTF-16 encoding for MT4 compatibility
- **Profile Rotation**: Atomic file operations to prevent corruption
- **Database Locking**: Handle SQLite locking during EA operations
- **Log File Management**: Append-only logs for audit trail

### Integration Dependencies
- **Parent EA**: HUEY_P_EA_ExecutionEngine_8.mq4 must support reentry module
- **Database Schema**: Requires parent trading_system.db structure
- **PowerShell Execution Policy**: Scripts require execution permissions
- **SQLite Tools**: `sqlite3.exe` required for automated reports

## Monitoring and Analytics

### Real-time Monitoring
```bash
# Service health monitoring
curl http://localhost:8000/health

# Configuration validation
curl "http://localhost:8000/ui/config?blueprint_path=./reentry_blueprint.yaml"

# Decision evaluation
curl -X POST http://localhost:8000/decide -H "Content-Type: application/json" -d '{
  "combo": {
    "symbol": "EURUSD",
    "signal_type": "STRADDLE",
    "time_category": "SHORT", 
    "outcome": 2,
    "context": "since_news",
    "generation": 0
  }
}'
```

### Performance Analytics
- **Chain Analysis**: Multi-generation reentry performance tracking
- **Action Effectiveness**: Per-bucket success rate analysis
- **Risk Metrics**: Drawdown and exposure monitoring
- **Temporal Patterns**: Time-based performance variations

This reentry system extends the HUEY_P Trading System with sophisticated post-trade analysis and automated follow-up execution, enabling adaptive trading strategies based on historical performance patterns and multi-dimensional market context analysis.