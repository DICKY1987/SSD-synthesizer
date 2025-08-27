# Software Requirements Specification (SRS) — Economic Calendar → Signal System (HUEY_P)

## 1. Introduction

### 1.1 Purpose  
Define a precise, complete, and traceable architecture for the Economic Calendar → Signal System that transforms calendar data into timed trading signals integrated with MT4/Excel, including decomposition from Systems → Subsystems → Components → Modules.

### 1.2 Scope  
Covers data acquisition, transformation, event enhancement (anticipation & equity opens), real-time monitoring, strategy ID generation, parameter/ risk logic, signal export, configuration, dashboards, logging, and persistence (Excel DataStore & optional SQLite via Python implementation).

### 1.3 Definitions, Acronyms, Abbreviations  
- **EMO-E**: High-impact economic event.  
- **EMO-A**: Medium-impact economic event.  
- **EQT-OPEN/CLOSE**: Equity market open/close events.  
- **RCI Strategy ID**: 5-digit Regional-Country-Impact code.  
- **SignalEntrySheet**: Excel→MT4 signal bridge sheet.  

### 1.4 References  
- **Manual/Guide**: *calendar_config_guide.md* (configuration & usage).  
- **Manual/Overview**: *Economic Calendar Trading System Documentation.md* (Python & system overview).  
- **Specs**: *Ultra-Detailed Technical Documentation.txt* (modules, functions, data structures, ops).  
- **Specs**: *eco cal to signal SYSTEM ARCHITECTURE OVERVIEW.txt* (end-to-end flow & constraints).  
- **Specs**: *eco_calendar_system_analysis.txt* (algorithms & exact timings).  
- **Specs**: *Economic Calendar Strategy ID Generation.txt* (alt hash/pset mapping).  

### 1.5 Overview  
The system imports weekly calendar data (auto: Sunday 12:00 PM CST; hourly retries), enriches with anticipation & equity-open events, orders chronologically with conflict resolution, monitors every 15s with offset-based triggers, selects parameter set/strategy ID, and exports signals to MT4 via SignalEntrySheet.

---

## 2. Overall Description

### 2.1 Product Perspective (Layered Architecture)  
**System → Subsystems → Components → Modules** (with layers):

- **Data Sources**: ForexFactory/other CSVs; equity-open schedule.  
- **Data Processing (Excel/VBA, Python)**: CSV parsing, normalization, impact filtering, anticipation & equity injection, quality scoring. (VBA & optional Python pipeline).  
- **Communication/Bridges**: File-based integration via SignalEntrySheet and MT4 data path (no sockets/C++ specified).  
- **Execution & Re-entry**: 15-second timer, offset-based triggering; MT4 EA processes signals (re-entry handled by EA/policy).  
- **Persistence**: Excel DataStore (named ranges, hidden sheets); optional SQLite DB in Python variant.  
- **Configuration Management**: CalendarConfig dashboard, named ranges, backup procedures.  
- **Monitoring, Logging, Deployment**: Health score, error handling (severity/categories), dashboard refresh. (Deployment: VBA modules & MT4 EA; Python optional FastAPI service).  

### 2.2 Product Functions  
- Weekly auto-import + hourly retries; manual override.  
- Impact & quality filtering; CST standardization; CHF exclusion.  
- Anticipation events; equity-open injection.  
- Conflict-aware chronological queue.  
- Offset-based trigger (default −3m) on 15s loop.  
- Strategy-ID (RCI) assignment & parameter-set selection.  
- Signal export to SignalEntrySheet; MT4 execution.  

### 2.3 User Characteristics  
Advanced user of MT4/Excel; operates CalendarConfig dashboard to tweak anticipation hours, offsets, and schedules; uses diagnostics and emergency stop.  

### 2.4 Constraints  
- Time zone standardized to CST; equity opens at fixed CST times.  
- Offset rules per event type; minimal inter-event spacing 5 minutes.  
- 4 fixed parameter sets differ only by lot size (VBA baseline).  
- CHF events excluded.  

### 2.5 Assumptions and Dependencies  
- Downloaded CSV is discoverable and valid; DataStore available; MT4 data path accessible; SignalEntrySheet present; optional Python service & SQLite when deployed in that mode.  

---

## 3. Specific Requirements

### 3.1 Functional Requirements (Systems → Subsystems → Components → Modules)

#### 3.1.1 Data Acquisition Layer (System)  
**Role:** Detect & import weekly calendar file automatically; validate freshness; manual override.  
**Dependencies:** File system; CalendarConfig schedule.  
**Consumes/Produces:** CSV → Raw Calendar Sheet/Array.  
**Modules:**  
- *system_infrastructure.bas* — directory paths, MT4 path validation, timers.  
- Import scheduler (Sunday 12:00 PM CST; hourly retries).  
**Interfaces:** Manual import button.  

#### 3.1.2 Data Transformation Pipeline (Subsystem)  
**Role:** Filter (High/Medium), normalize (CST, currency), quality score, enhance structures.  
**Dependencies:** Raw CSV; mapping tables.  
**Consumes/Produces:** Raw rows → Processed Events Array.  
**Modules/Components:** CSV parser, quality scorer, normalization utils.  

#### 3.1.3 Event Enhancement Engine (Subsystem)  
**Role:** Generate anticipation rows & inject equity market opens; merge into queue.  
**Dependencies:** Processed events array; user config (anticipation hours/count).  
**Consumes/Produces:** Processed events → Enhanced events (anticipation+equity).  

#### 3.1.4 Chronological Ordering & Conflict Resolution (Component)  
**Role:** Multi-criteria sort; ensure ≥5-minute separation by priority.  
**Dependencies:** Enhanced events.  
**Rules:** Priority: EMO-E(100) > EMO-A(80) > EQT-OPEN(60) > ANTICIPATION(20).  

#### 3.1.5 Real-Time Monitoring Engine (Subsystem)  
**Role:** 15-second loop detects offset-based trigger times.  
**Offsets:** EMO-E −3m, EMO-A −2m, EQT-OPEN −5m, ANTICIPATION −1m.  
**Tolerance:** ±30s window for execution.  

#### 3.1.6 Strategy Identification (Subsystem)  
**Role:** Assign 5-digit RCI Strategy IDs; anticipation IDs may be +1000 over base; equity opens have special IDs.  

#### 3.1.7 Parameter Set Management (Component)  
**Role:** 4 fixed sets (only lot size differs) with selection logic (sequential/random/impact-based).  
**Sets:** 0.01 / 0.02 / 0.03 / 0.04 lots; SL=20, TP=40, distances=10, expire=24h, trailing=0, max spread=3.  

#### 3.1.8 Risk & Performance Logic (Subsystem)  
**Role:** Performance oscillator (0–100) selects parameter set; risk modifiers (drawdown, wins/losses, volatility, equity close proximity).  

#### 3.1.9 Signal Integration Layer (Subsystem)  
**Role:** Export signals to SignalEntrySheet (symbol, distances, SL/TP, lot, expire, trailing, comment, strategy_id, pset_id).  
**Downstream:** MT4 EA executes trades; results fed back to performance history.  

#### 3.1.10 Data Store & Dashboard (Subsystem)  
**Role:** Centralize calendar/system state; drive dashboards (next events, config, parameter sets, timers).  
**Fields:** Calendar rows 104-203; status rows 206-207; parameter sets & performance history areas.  

#### 3.1.11 Error Handling & Health Monitoring (Subsystem)  
**Role:** Categorized logging, recovery (timer, file system, MT4), health scoring & uptime.  
**Severity/Categories:** INFO/WARNING/ERROR/CRITICAL; CAT_SYSTEM, CAT_TIMER, CAT_FILE_SYSTEM, CAT_CALENDAR, CAT_SIGNAL_PROCESSING.  

#### 3.1.12 Python Implementation (Optional System Variant)  
**Role:** FastAPI server, AsyncIOScheduler/APScheduler, SQLite persistence, UPSERT, WebSockets, Pydantic config. (Complements Excel/VBA baseline.)  

---

### 3.2 Performance Requirements  
- **Timer cadence:** 15 seconds; **trigger tolerance:** ±30 seconds.  
- **Throughput:** Efficient array operations; minimal Excel recalculation; background processing; memory management.  
- **Latency:** Offset-based pre-triggering (e.g., EMO-E at −3 minutes).  

### 3.3 Design Constraints  
- **Event types & offsets:** EMO-E −3m, EMO-A −2m, EQT-OPEN −5m, ANTICIPATION −1m.  
- **Impact filtering:** Only High/Medium; CHF excluded.  
- **Priority ordering:** EMO-E>EMO-A>EQT-OPEN>ANTICIPATION; ≥5-minute de-conflict.  
- **Parameter sets:** Fixed 4-set baseline (lot size variation only).  
- **Time zone:** All times normalized to CST.  

---

## 4. Architecture Mapping (Decomposition Summary)

### 4.1 Systems → Subsystems → Components → Modules

- **Calendar Processing System** (System)  
  - **Data Acquisition Layer** (Subsystem) → *system_infrastructure.bas* (timer, paths); Import Scheduler.  
  - **Data Transformation Pipeline** (Subsystem) → CSV Parser, Quality Scorer, Normalizer.  
  - **Event Enhancement Engine** (Subsystem) → Anticipation Generator; Equity Open Injector.  
  - **Chronological Queue** (Component) → Multi-criteria sorter; conflict resolver.  
  - **Real-Time Monitoring Engine** (Subsystem) → 15s timer; offset rules.  
  - **Strategy Identification** (Subsystem) → RCI encoder; anticipation +1000; equity IDs.  
  - **Parameter Set Manager** (Component) → 4 fixed sets + selection logic.  
  - **Signal Integration Layer** (Subsystem) → *SignalEntrySheet* writer; MT4 path handoff.  
  - **Data Store & Dashboards** (Subsystem) → Hidden DataStore; control panel.  
  - **Error Handling & Health** (Subsystem) → *error_handling_system.bas*; health score.  
  - **Python Variant** (System alt) → FastAPI/WebSocket, APScheduler, SQLite.  

---

## 5. Layered Decomposition (Explicit)

- **Data Sources:** Calendar CSVs (ForexFactory, etc.); injected equity opens.  
- **Data Processing (Excel/VBA, Python):** Filtering, enhancement, sorting (VBA); optional Python service w/ SQLite.  
- **Communication/Bridges:** File-based SignalEntrySheet + MT4 data path (no sockets/C++ specified).  
- **Execution & Reentry:** 15s trigger engine; EA executes/feeds performance history.  
- **Persistence:** Excel DataStore (named ranges/sheets); optional SQLite DB (Python).  
- **Configuration Management:** Dashboard controls; backup of named ranges; change management.  
- **Monitoring/Logging/Deployment:** Health score, error categories, dashboard refresh; deploy as VBA modules & MT4 EA; Python deploy via FastAPI.  

---

## 6. Traceability & Document Cross-References

For each subsystem in §3.1, sources are tagged as **Spec** and/or **Manual**. Where the **Manual** extends the **Spec** (e.g., 5 anticipation events vs 3), this is explicitly noted.  

**Spec-only constraints** (examples): fixed 4-set parameters; DataStore layouts; error severity/categories; health scoring.  
**Manual-only additions** (examples): strict 5-anticipation MQL4 path; anticipation ID +1000; equity IDs 81015/82015/83015.  

---

## 7. Relationship Mapping (Flows)

**Primary Flow (sequential):**  
Downloads → Raw Calendar → Processed Events → Enhanced Events (anticipation + equity) → Chronological Sort (conflict-safe) → Real-Time Monitoring (15s, offsets) → Strategy ID & Parameter Set → SignalEntrySheet → MT4 EA Execution → Performance History.  

**Cross-cutting:**  
- Error handling & health monitoring wrap all stages.  
- Configuration dashboard influences anticipation hours/count, offsets, import schedule.  

**Explicit Timing Chain Example:**  
*Calendar CSV* → *VBA pipeline* → *Event offsets (−3/−2/−5/−1)* → *Trigger window ±30s @ 15s tick* → *Write signal row to SignalEntrySheet* → *EA consumes*.  

---

## 8. Completeness Check

- **All major systems/subsystems present**: acquisition, transformation, enhancement, ordering, monitoring, strategy ID, params/risk, signal export, dashboards, error/health.  
- **Duplicates consolidated**: Priority/offset/conflict rules normalized to single definitions; anticipation count clarified: **Spec baseline = 3**; **Manual extension = 5** (documented as configurable—implementation-dependent).  
- **Traceability maintained**: Each requirement cites source(s); where manual adds constraints (anticipation IDs, special equity IDs), flagged.  

---

### Appendix A — Key Data Structures & Sheets (Excerpt)

- **Calendar Data (Rows 104–203):** Date, Time (CST), Title, Country, Impact, EventType, ParameterSet, Enabled, TriggerTime, Status, LastUpdate.  
- **System Status (Rows 206–207):** Health, Timer, MT4, CalendarStatus, LastUpdate, Uptime.  

### Appendix B — Exact Offsets & Priority  
- Offsets: EMO-E −3m; EMO-A −2m; EQT-OPEN −5m; ANTICIPATION −1m.  
- Priority: EMO-E 100; EMO-A 80; EQT-OPEN 60; EQT-CLOSE 50; ANTICIPATION 20.  
