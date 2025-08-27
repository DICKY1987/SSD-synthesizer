# Comprehensive System Documentation Template (Populated)

## 1. Core Details

- **Business Domain**:  
  Financial Services – Algorithmic Trading

- **Project Name**:  
  MT4 Multi-Source Signal Execution System

- **Goals and Success Criteria**:  
  - Achieve sub-10ms signal processing latency (excluding broker execution)  
  - Support 30 concurrent currency pair EAs with 99.9% signal delivery reliability  
  - Implement risk-adaptive parameter management with 10 distinct risk profiles  
  - Provide three-tier communication failover ensuring zero signal loss  
  - Enable reentry logic for failed/partial trades with performance tracking

- **Stakeholders and Owners**:  
  | Role | Name | Contact |  
  |------|------|---------|  
  | Principal Systems Architect | Trading System Architect | architect@trading.system |  
  | Risk Management Lead | Risk Management Team | risk@trading.system |  
  | Development Team Lead | Development Team | dev@trading.system |  
  | Operations Lead | Operations Team | ops@trading.system |

---

## 2. Technical Context

- **Operating Environments**:  
  Windows 10/11; MT4 Terminal; Local development and production

- **Compliance / Regulatory Context**:  
  Financial trading regulations; Risk management compliance

- **Data Classification**:  
  Internal, Trading Signals, Financial Data

- **Performance and Reliability Targets**:  
  - 99.9% signal delivery success rate  
  - 99.5% trade execution success rate  
  - Signal processing latency < 10ms  
  - Communication failover < 100ms

- **Integration Points**:  
  - MT4 Terminal – MQL4 EA Integration – Trade execution and market data  
  - Python Analytics Engine – TCP Socket / Named Pipes / File System – Signal generation & ML analytics  
  - Economic Calendar System – CSV Data Feed – News-based signal generation

---

## 3. Communication Architecture

- **Communication Modes**:  
  - **Primary**: Socket Bridge (TCP, DLL-based) – ~1-2s latency  
  - **Fallback**: CSV File Exchange – ~15s latency

- **CSV Protocol File Structure**:  
  - `trading_signals.csv` – Input: Python → EA  
  - `trade_responses.csv` – Output: EA → Python  
  - `system_status.csv` – Status: EA → Python  
  - `error_log.csv` – Errors: EA → Python

- **Socket Configuration**:  
  - Primary Port: 5555  
  - Alternative Port: 9999  
  - Timeout: 30s  
  - KeepAlive: Enabled  
  - Max Connections: 5

---

## 4. Data Structures

- **Trading Signals (CSV)**:  
  Columns: `signal_id, symbol, direction, lot_size, stop_loss, take_profit, comment, timestamp, confidence, strategy_id`

- **Trade Responses (CSV)**:  
  Columns: `signal_id, trade_id, status, execution_price, timestamp, error_message`

- **Economic Calendar (CSV)**:  
  Columns: `Time, Currency, Event, Impact, Actual, Forecast, Previous`

- **Reentry Governance Checklist (CSV)**:  
  Controls include: Allow Reentry, Min Delay Seconds, Max Generations, Daily Loss Limit, Min Confidence, Blackout After N Losses, Max Position Size, Spread Guard, Freeze Level Guard, Retries, Magic Base Offset, Queue Mode, Profile Path, Live Profile Reload, Execution Logging, Performance Snapshot

- **Reentry Profile Template (CSV)**:  
  Columns: `Action, Type, SizeMultiplier, DelaySeconds, ConfidenceAdjustment, Parameters`

---

## 5. System Architecture

- **Architectural Goals**:  
  - Modularity (multiple independent signal sources)  
  - Reliability (three-tier failover)  
  - Performance (sub-10ms signal processing)  
  - Maintainability (hybrid modular approach)  
  - Auditability (signal-to-execution tracking)  
  - Risk Control (dynamic parameter selection)

- **Constraints**:  
  - MQL4 language only (no MQL5 features)  
  - Native functions only  
  - File system access limited to MT4 directories  
  - Communication limited to TCP, Named Pipes, Files  
  - SQLite for persistence

---

## 6. Key Components

- **Signal Sources**: AI/ML, Technical Indicators, Economic Calendar, Manual Input  
- **Core Processing**: Strategy Mapper, Parameter Resolver, Signal Processor  
- **Execution Layer**: MT4 EA Cluster (30 currency pairs)  
- **Reentry Engine**: Handles failed/partial trades  
- **Data Stores**:  
  - `signal_id_mapping.csv`  
  - `all_10_parameter_sets.csv`  
  - `reentry_configs/`  
  - SQLite database

---

## 7. Observability & Governance

- **Audit Trail**: SQLite database logs signals and executions  
- **Governance Controls**: Defined in governance_checklist.csv & Reentry_Governance_Checklist.csv  
- **Monitoring & Analytics**: KPI tracking scripts (e.g., `reentry_kpi_snapshot.ps1`)
