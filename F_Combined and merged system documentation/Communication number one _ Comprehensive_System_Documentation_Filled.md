# 📘 Comprehensive System Documentation (Filled from Communication Docs)

## 1.0 System Overview & Architecture
**1.1 Purpose and Scope**  
The HUEY_P trading system implements a **hybrid communication architecture** enabling bidirectional exchange between:  
- MetaTrader 4 Expert Advisor (MQL4)  
- Python interface applications  
- External signal sources【13†source】

**1.2 Architectural Diagrams**  
Communication stack shows dual modes: **Socket Bridge (DLL-based)** and **CSV File Exchange (file-based)**【13†source】.

**1.3 Data Flow Diagrams (DFDs)**  
- CSV cycle: Python → `trading_signals.csv` → EA → trade execution → `trade_responses.csv` → Python【13†source】  
- Socket cycle: Python client → DLL socket bridge → EA → confirmations back via JSON【13†source】  

**1.4 Stakeholders & Responsibilities**  
- **Developers**: implement protocols (CSV, socket)【12†source】  
- **Users/Traders**: monitor via GUI apps【13†source】  
- **System**: EA executes trades and manages state【13†source】  

---

## 2.0 Data Models & Persistence
**2.1 Logical Data Model**  
CSV files as entities:  
- `trading_signals.csv` (signals in)  
- `trade_responses.csv` (execution feedback)  
- `system_status.csv` (state reporting)  
- `error_log.csv` (errors)【11†source】  

**2.2 Physical Database Schema**  
CSV schemas defined (field names, types, constraints). Example: `signal_id,symbol,direction,lot_size,...`【11†source】  

**2.3 State Management**  
- EA maintains status in `system_status.csv`【11†source】  
- Python monitors CSV/socket responses【13†source】

---

## 3.0 Interfaces & APIs
**3.5 Communication Contracts (Runtime Bridges)**  
- **CSV**: atomic file writes, cooperative locks, retry/backoff【11†source】  
- **Socket**: JSON schemas (trading_signal, trade_confirmation, status_update, error)【13†source】  

**3.6 Signal Queueing & Ordering**  
- CSV requires unique `signal_id` within 24 hours; expired signals rejected【11†source】  

**3.7 Legacy Integration Modules**  
- Explicit: CSV exchange (file-based)【13†source】  
- Socket DLL bridge【13†source】

---

## 4.0 Core Logic & Behavior
**4.2 Error Handling & Exception Strategy**  
- Error codes categorized (validation, execution, system)【11†source】  
- Recovery actions: skip, retry, adjust lot, restart EA【11†source】

**4.5 Safety Controls**  
- EA state machine includes PAUSED and ERROR states【11†source】  

---

## 5.0 Deployment & Operations
**5.1 Infrastructure & Environment**  
- MT4 terminal with EA loaded  
- Python apps (strategy, monitoring)【13†source】  

**5.3.1 Multi-Format Configuration & Profile Management**  
- Enable CSV with `EnableCSVSignals=true`【12†source】  
- Enable sockets with `EnableDLLSignals=true`【12†source】

**5.6 Broker/Terminal Failover SOP**  
- Automatic fallback from socket → CSV when sockets fail【13†source】

**5.7 Observability & SLOs**  
- Latency benchmarks: CSV ~15s, Socket ~1s【12†source】  
- Reliability: CSV success rate 99.8%, Socket 98.5%【12†source】  

---

## 6.0 Non-Functional Requirements (NFRs)
**6.1 Performance**  
- CSV throughput: 4 signals/min  
- Socket throughput: 120 signals/min【12†source】

**6.3 Availability & Reliability**  
- CSV MTBF >30 days  
- Socket MTBF >7 days【12†source】

**6.4 Auditing & Logging**  
- Errors logged in `error_log.csv`【11†source】

---

## 7.0 Security Specifications
- **File locking** prevents race conditions【11†source】  
- **Firewall requirements** for socket ports 5555 and 9999【13†source】

---

## 8.0 Model Governance (for AI/Trading Systems)
*(No explicit details in provided docs)*

---

## 9.0 Requirements Traceability (RTM Layer)
Example linkage (from CSV schemas):  
- REQ-001: Signal must have unique `signal_id` → validated by EA parser【11†source】  

---

## 10.0 Cross-View Linking
- Communication docs explicitly reference both **CSV** and **Socket** modes with fallback linking【12†source】【13†source】

---

## 11.0 Export Strategy
- **Developer View**: CSV/socket schemas【11†source】【13†source】  
- **Ops View**: Troubleshooting guide, benchmarks【12†source】  
