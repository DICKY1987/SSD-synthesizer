Software Requirements Specification (SRS) — Reentry Decision Matrix Subsystem
1. Introduction
1.1 Purpose

Define a precise, complete, and traceable specification for the Reentry Decision Matrix subsystem that governs re-entry decisions after trades, using a rule-based 4D (or reduced) matrix and associated services (rule engine, persistence, performance tracking, data model). The SRS consolidates the attached design materials into a single source of truth. 
 

1.2 Scope

Scope covers the Python subsystem responsible for: defining matrix dimensions; producing per-cell MatrixCell decisions; initializing defaults via a DefaultRuleEngine; persisting configurations via MatrixDataManager; and tracking results via MatrixPerformanceTracker. Downstream trade execution (e.g., MQL4 EAs) consumes outputs (parameter_set_id, action_type). 
 

1.3 Definitions, Acronyms, Abbreviations

MatrixCell: Atomic decision record with fields such as parameter_set_id, action_type, size/confidence modifiers, and stats helpers. 
 

Generation (R0/R1/R2): Original trade (R0) and up to two re-entries (R1, R2) in reduced architecture. 

Action Types: NO_REENTRY, SAME_TRADE, REVERSE, INCREASE_SIZE. 

Market Context (full matrix): PRE_NEWS_*, NEWS_WINDOW, POST_NEWS_*, session states, etc. 

Future Event Proximity (reduced): IMMEDIATE, SHORT, LONG, EXTENDED. 

1.4 References

4D Matrix.md — Full matrix design (dimensions, rule engine, data model, persistence). 
 
 

multidimensionalreentrydecisionsysteminPython.md — Complete implementation narrative (matrix, rules, persistence). 
 

Reduced Multi-Dimensional Matrix System – Complete Implementation.md — Reduced architecture with R1/R2, duration scoping, and event proximity. 
 
 

1.5 Overview

Section 2 describes the product at a high level; Section 3 specifies functional/performance/design constraints; relationship maps and traceability are embedded throughout.

2. Overall Description
2.1 Product Perspective

The subsystem exposes a deterministic mapping from (signal type × time/duration × outcome × context/proximity) to a MatrixCell decision. Full architecture uses Market Context; reduced architecture replaces context with Future Event Proximity and bounds re-entry generations (R1/R2). 
 
 
 

2.2 Product Functions

Define matrix dimensions (signals, time/duration, outcomes, context/proximity). 
 
 
 
 

Initialize each cell with rule-driven defaults (news window, flash move, momentum, etc.). 
 
 

Persist matrices per symbol with versioning and a “current” pointer. 
 

Track performance and compute basic stats per cell; gate significance at N≥30. 
 

2.3 User Characteristics

Target users are quantitative traders/engineers who tune parameters, set overrides, and promote versions; they require deterministic, auditable behavior (no ML adaptation).

2.4 Constraints

Safety rules: e.g., No re-entry during news window after losses (full matrix). 

R-generation cap: hard stop after R2 (reduced matrix). 

Statistical gating: treat cells as significant only with ≥30 samples. 

2.5 Assumptions and Dependencies

Inputs exist to derive market context (news windows, session states) or future event proximity; trade outcomes and durations are available from the execution layer/logs. (Contexts/proximity enumerations define what the subsystem expects.) 
 

3. Specific Requirements
3.1 Functional Requirements
3.1.1 Core Matrix Engine (Systems → Subsystems → Components → Modules)

Name & Role

System: Reentry Decision Matrix

Subsystem: ReentryMatrix — in-memory 4D mapping of inputs to MatrixCell. 

Dependencies

Consumes: signal type, time/duration, outcome, context/proximity. Produces: MatrixCell. Depends on DefaultRuleEngine (initialization) and MatrixPerformanceTracker (stats). 
 

Source Documents
4D/full: 4D Matrix.md; Reduced: Reduced Multi-Dimensional…. 
 

Requirements

The engine SHALL define dimensions:

Full: signal_types, time_categories, outcomes, market_context. 
 
 
 

Reduced: signal_types, reentry_time_categories (ECO only / NO_DURATION for others), outcomes, future_event_proximity, with R0/R1/R2 storage patterns. 
 
 

The engine SHALL store the matrix as [signal][time/duration][outcome][context/proximity] → MatrixCell. 
 

The engine SHALL call DefaultRuleEngine to populate each cell with defaults on initialization. 

3.1.2 Data Model

Name & Role

Component: MatrixCell — encapsulates decision (parameter_set_id, action_type) + modifiers + stats helpers. 

Dependencies

Produced by ReentryMatrix; consumed by execution layer (external).

Requirements

Fields SHALL include parameter_set_id, action_type (NO_REENTRY, SAME_TRADE, REVERSE, INCREASE_SIZE), size/confidence multipliers, delay, attempt limits, user_override. 
 

Methods SHALL expose get_success_rate, get_average_pnl, and is_statistically_significant(N≥30). 

3.1.3 Default Rule Engine

Name & Role

Subsystem: DefaultRuleEngine — priority-ordered rules to assign initial MatrixCell values across the matrix. 

Requirements

The engine SHALL apply prioritized rule sets (e.g., news-window, flash-move, momentum, reversal…); else fallback is conservative NO_REENTRY. 
 

News window safety (full matrix): after loss (outcome ∈ {1,2}) during NEWS_WINDOW → NO_REENTRY; profitable ECO_HIGH during news → cautious continuation. 

Flash move handling: FLASH + outcome==1 → small REVERSE; FLASH + outcome==6 → SAME_TRADE continuation. 
 

Momentum continuation: MOMENTUM/ECO_HIGH + good outcomes → increase size/continue based on time category or proximity. 
 

Reduced architecture SHALL replace news-window with future proximity rules and enforce generation limit (stop after R2). 
 

3.1.4 Persistence & Versioning

Name & Role

Subsystem: MatrixDataManager — save/load/version matrices per symbol; maintain current_matrix.json symlink/pointer. 
 

Requirements

File layout SHALL follow /reentry_matrices/<SYMBOL>/ with versioned JSON files and a current_matrix.json. 

Metadata SHALL include version, created_date, total_cells, user_overrides count (and reduced-arch fields where applicable). 

Save/Load SHALL serialize/deserialize matrix data and update the current link atomically. 
 

3.1.5 Performance Tracking

Name & Role

Subsystem: MatrixPerformanceTracker — record execution results per coordinate, compute summary and basic advanced stats; optional caching. (Significance threshold N≥30 is enforced by MatrixCell helper.) 

Requirements

The tracker SHALL support appends of execution records keyed by matrix coordinates and keep summary stats per key. (See design narrative around performance tracking in full/reduced docs.) 

The subsystem SHOULD surface underperforming cells for human review (user-controlled optimization; not auto-ML). (Design intent across docs.)

3.1.6 Integration Output (to Execution & Re-entry Layer)

Name & Role

Component: Decision Output Adapter (logical) — expose MatrixCell fields required by downstream execution (e.g., EA), notably parameter_set_id, action_type, and modifiers/attempt limits. 

Requirements

The adapter SHALL pass action_type semantics consistently (NO_REENTRY / SAME_TRADE / REVERSE / INCREASE_SIZE). 

The adapter SHOULD include notes and user_override flags for auditability. 

3.2 Performance Requirements

Matrix lookups SHOULD be constant-time (dictionary indexing).

Initialization time SHOULD scale linearly with the number of cells; reduced architecture aims to constrain cell count via duration scoping and R-generation bounds. 
 

Persistence operations SHOULD be I/O-bound and versioned; “current” pointer update required post-save. 

3.3 Design Constraints

Safety: Conservative fallbacks when no rule triggers. 

Event Risk (full): News window guardrails. 

Event Proximity (reduced): IMMEDIATE proximity triggers conservative behavior; limit generations to R2. 
 

4. Layered Decomposition

Data Sources

Trade outcomes/durations, market context or event proximity inputs used to address the matrix. (Context/proximity enumerations define expected inputs.) 
 

Data Processing (Python)

ReentryMatrix (dimension definitions, storage), DefaultRuleEngine (prioritized rules), MatrixCell (modifiers, stats), MatrixPerformanceTracker (per-cell stats). 
 
 

Communication/Bridges

Interface that hands MatrixCell outputs to execution layer (format TBD by downstream EA). (Action types and parameter_set_id are defined here.) 

Execution & Reentry

External EA or strategy engine consumes action_type → execute/no-reenter/reverse/size-up. (Defined semantics from MatrixCell.) 

Persistence

MatrixDataManager: versioned JSON per symbol + current_matrix.json. 
 

Configuration Management

User overrides are recorded in cells and counted in metadata. 
 

Monitoring, Logging, Deployment

Performance history CSV per symbol (noted in file structure) and summary stats methods in MatrixCell. 
 

5. Relationship Mapping

Hierarchical

System → Subsystems → Components → Modules:

Reentry Decision Matrix → {ReentryMatrix, DefaultRuleEngine, MatrixDataManager, MatrixPerformanceTracker} → {MatrixCell + rule modules + save/load modules}. 
 
 

Sequential Flow (Full Matrix)

Signal event closes → outcome/time known → ReentryMatrix lookup with market context → MatrixCell → execution → result recorded → PerformanceTracker updates stats. 
 

Sequential Flow (Reduced Matrix)

Trade closes → outcome + proximity (to next event) + (if ECO) duration → ReentryMatrix lookup → MatrixCell decision (respect R1/R2 bounds) → execution → performance update. 
 
 

Cross-cutting Rules

News window / flash move / momentum continuation influence defaults irrespective of symbol; reduced mode swaps to proximity rules. 
 
 

6. Traceability

From Manual/Spec

Dimensions (signals, time/duration, outcomes, context/proximity) and 4D mapping come directly from the attached specs. 
 
 
 

Default rules and priorities (news/flash/momentum) are specified with concrete outcomes and actions. 
 
 

Persistence layout and metadata are explicitly defined (directory scheme, symlink to current). 
 
 

Reduced architecture adds future event proximity, ECO-only durations, and an R2 cap. 
 
 

Spec-only constraints beyond narrative

Statistical significance threshold (≥30) is codified in MatrixCell helpers. 

Explicit action types are enumerated to standardize downstream consumption. 

7. Completeness Check

Systems & Subsystems represented: ReentryMatrix, MatrixCell, DefaultRuleEngine, MatrixDataManager, MatrixPerformanceTracker are captured with roles, dependencies, and requirements. (All appear in the attached docs.) 
 
 

Duplicates consolidated: Full vs Reduced architectures are harmonized; reduced adds proximity/duration scoping and R2 cap; both share core model and persistence pattern. 
 
 

Traceability preserved: Each requirement is source-referenced to the provided files using inline citations.

Appendix A — Architectural Decomposition (Roll-up)

Systems → Subsystems → Components → Modules

Reentry Decision Matrix System

ReentryMatrix (Core engine) → Dimensions module, Storage module (4D / reduced storage). 
 

DefaultRuleEngine (Rules) → NewsWindow, FlashMove, Momentum, (Reduced) FutureProximity, GenerationLimit, Fallback. 
 
 
 

MatrixCell (Data model) → Decision fields, Modifiers, Stats helpers. 
 

MatrixDataManager (Persistence) → Serializer, Versioner, Current pointer. 
 

MatrixPerformanceTracker (Monitoring) → Execution record store, Summary stats. 