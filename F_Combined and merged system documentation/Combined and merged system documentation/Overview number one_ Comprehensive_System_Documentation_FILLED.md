# Extractable Facts Catalog (for Template Filling)

This document lists information that **can be copied verbatim into your template** without inventing or inferring anything. Each item includes a citation back to the provided documents.

> **Note:** I need the actual template file (or its field list) to insert these values into specific fields. Until then, this catalog shows exactly what can be filled, with sources.

---

## 1) Document & Project Metadata

- **Project Name:** HUEY_P Algorithmic Trading System with MQL4 DLL Socket Bridge. fileciteturn1file0L3-L3
- **Document Version (Spec):** 1.0. fileciteturn1file0L4-L4
- **Date (Spec):** August 14, 2025. fileciteturn1file0L5-L5
- **Status:** Draft. fileciteturn1file0L6-L6
- **Authors/Owners:** Richard Wilks (System Architect), Trading Development Team. fileciteturn1file0L7-L7
- **Document Classification (Spec):** Internal - Trading System Architecture. fileciteturn1file0L8-L8
- **Document Title (Manual):** HUEY_P_ClaudeCentric Trading System — Technical Manual v1.0. fileciteturn1file12L1-L3
- **Manual Version / Last Updated / Classification / Audience:** Version 1.0; Last Updated: January 15, 2025; Classification: Technical Reference Manual; Audience: Expert Developers and System Architects. fileciteturn2file0L39-L42

---

## 2) Business Goals & Success Criteria

- **Primary Goals (Spec):** Automated straddle trading; dynamic risk management; Python-based analysis & monitoring; sub-100ms trading/signal latency; multi‑source signal processing. fileciteturn2file5L29-L35
- **Success Criteria (Spec):** 99.95% availability (Sun 23:00 GMT – Fri 22:00 GMT); <200ms p99 trade-exec; <5s EA↔Python sync; <1s emergency close; <30s reconnection. fileciteturn2file5L36-L41

---

## 3) Scope

- **In Scope:** MT4 EA; Windows C++ DLL socket bridge; Python monitoring interface; SQLite; TCP 5555; CSV signal processing; error/perf monitoring; multi‑env deploy. fileciteturn2file5L45-L53
- **Out of Scope:** MT5; non‑Windows OS; direct broker API outside MT4; HFT (sub-second); 3rd‑party signals beyond CSV/DLL. fileciteturn2file5L55-L60

---

## 4) Stakeholders

| Name | Role | Email | Responsibilities |
|------|------|-------|------------------|
| Richard Wilks | System Architect & Lead Developer | richard.wilks@trading.local | Overall system architecture, MQL4 EA development |
| Trading Operations Team | System Users | ops@trading.local | Day-to-day system operation and monitoring |
| Risk Management | Risk Oversight | risk@trading.local | Risk parameter validation and compliance |
| IT Infrastructure | System Administration | infra@trading.local | Server maintenance and deployment |

Source: fileciteturn2file5L62-L70

---

## 5) Architecture Highlights

- **Architectural Goals & Constraints (Manual/Spec excerpts):** Modularity (StateManager, SignalManager, LogManager), Fault tolerance & recovery, Low‑latency, Observability, Maintainability; Windows+MT4/32‑bit constraints; real‑time processing ≤100ms. fileciteturn1file2L54-L67
- **High‑Level System Layers (Manual):** Data Sources (Economic CSV, Config, Python ML) → VBA/Excel pipeline → Communication Bridge (File, Socket DLL, Pipes) → MT4/MQL4 (EA, Reentry, State, Monitoring) → Persistence (SQL/CSV/YAML). fileciteturn1file12L37-L69
- **Communication Port:** TCP socket on port **5555** (EA↔DLL↔Python). fileciteturn2file1L25-L36 fileciteturn2file6L3-L6 fileciteturn2file8L5-L9

---

## 6) Requirements (Selected)

### Functional (Spec)
- **FR‑001** Automated Straddle Strategy with timing/one‑straddle constraint. fileciteturn1file1L15-L23
- **FR‑002** Multi‑Source Signal Processing (autonomous EA, DLL socket, CSV) with processing intervals. fileciteturn1file1L24-L31
- **FR‑003** Dynamic Risk Management (defaults: 2% risk, 5% daily loss cap, streak handling, emergency halt). fileciteturn1file1L33-L41
- **FR‑004** Python real‑time monitoring dashboard update every 5s with system health. fileciteturn1file8L1-L8
- **FR‑005** Comprehensive logging & daily CSV with 30‑day rotation. fileciteturn1file8L10-L17

### Non‑Functional / SLOs (Spec)
- Availability 99.95%; Trade exec <200ms p99; Signal proc <100ms p95; DB <50ms p95; Socket recovery <5s; Memory <500MB. fileciteturn1file8L21-L31

---

## 7) Signal Sources & Protocols

- **Six Signal Input Modes:** Manual, Indicator‑based, External feed, Internal logic, CSV, Time‑slot activation. fileciteturn2file2L3-L11
- **CSV Signal File Spec (columns, enums, example):** filename pattern, encoding, required headers; timestamp/symbol/signal_type/entry/SL/TP/lot_size/comment/expiry with constraints. fileciteturn2file6L25-L94
- **Socket Endpoint:** tcp://localhost:5555 with publish/subscribe message types. fileciteturn2file6L3-L6

---

## 8) Risk Management & Safety

- **Circuit Breaker:** Daily drawdown, min‑equity, consecutive‑error limits trigger emergency stop (close all, delete pending, pause state). fileciteturn2file2L43-L66
- **Dynamic Lot Sizing (EA):** Risk % of equity; broker constraints; margin safety checks; rounding to lot step. fileciteturn2file4L18-L51

---

## 9) Reentry Logic (Six‑Sided Die)

- **Outcome Classification → Action 1..6** mapping via `DetermineNextAction(R, ML, MG, B)`. fileciteturn2file3L11-L38
- **Reentry Action Config Structure** (type, multiplier, delay, confidence, params). fileciteturn2file3L54-L62
- **Aggressive Profile CSV Example.** fileciteturn2file7L1-L8

---

## 10) Maintenance & Operations

- **Daily Maintenance (bash script):** Health check, config backups, log rotation, DB optimize, performance report. fileciteturn1file6L12-L32 fileciteturn1file6L36-L59 fileciteturn1file6L61-L72 fileciteturn1file6L74-L118
- **Weekly Maintenance (PowerShell):** Analyze system, validate configs, weekly report with counts. fileciteturn1file11L26-L60

---

## 11) Configuration & Deployment

- **Environment Variables (names/defaults):** `HUEY_DATABASE_PATH`, `HUEY_LOG_LEVEL`, `HUEY_SOCKET_PORT=5555`, `HUEY_CONFIG_PATH`, `HUEY_BACKUP_DIR`. fileciteturn2file1L30-L39
- **Deployment Checklist (selected):** Enable MT4 DLL imports; copy .ex4/.dll; init SQLite; configure firewall for port 5555; run diagnostics. fileciteturn2file1L19-L27

---

## 12) Beginner Roadmap (Context you may map to training/onboarding fields)

- **Target Audience:** Complete Programming Beginner. **Duration:** 8–12 months (300–400 hours). **Approach:** Single developer. fileciteturn1file7L3-L6
- **Environment Setup steps and validation tests** (VS Code, Git, Python; MT4 install & settings; C++ tools). fileciteturn1file7L29-L47 fileciteturn1file7L71-L90 fileciteturn1file7L101-L106
- **Integration & Testing checklist** (signal flow, DB ops, error handling; benchmarks). fileciteturn1file13L35-L71

---

## 13) Additional Definitions (Glossary)

Key terms you can map directly if your template includes a glossary: Anticipation Event; Circuit Breaker; Die Roll Logic; Economic Calendar System; Execution Engine; Magic Number; Parameter Set; Reentry Chain; Reentry Generation; Signal Integration Layer; State Machine; Straddle Trade; Trading Cycle. fileciteturn2file0L3-L27

---

### What I still need from you
Please provide **the template file or a list of its exact field names** so I can produce a filled version instantly using only the sourced values above.
