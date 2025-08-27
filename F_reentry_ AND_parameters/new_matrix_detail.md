# New Trade Matrix — Detailed Specification (Post-Stack State)
*Version:* post-stack-2025-08-17

This document defines the **canonical matrix** of trade combinations after **all requested modifications**:
- Removed signals: `ANTICIPATION_4HR`, `ANTICIPATION_12HR`
- Future-event buckets reduced to **4** with revised ranges
- Reentry **durations apply only** to `ECO_HIGH` and `ECO_MED` with **4** duration buckets
- Reentry **outcomes compressed to 3** buckets **only** for: `ANTICIPATION_1HR`, `ANTICIPATION_8HR`, `EQUITY_OPEN_ASIA`, `EQUITY_OPEN_EUROPE`, `EQUITY_OPEN_USA`
- Two reentry generations (G1, G2)

---

## 1) Dimensions

### 1.1 Signal Types (8)
`ECO_HIGH, ECO_MED, ANTICIPATION_1HR, ANTICIPATION_8HR, EQUITY_OPEN_ASIA, EQUITY_OPEN_EUROPE, EQUITY_OPEN_USA, ALL_INDICATORS`

**Removed:** ANTICIPATION_4HR, ANTICIPATION_12HR

### 1.2 Future-Event Proximity Buckets (4)
| Name | Minutes until event |
|---|---|
| IMMEDIATE | 0–15 |
| SHORT | 16–60 |
| LONG | 61–480 |
| EXTENDED | 481–1440 |

### 1.3 Reentry Duration Buckets (apply **only** to ECO_HIGH & ECO_MED)
| Name | Duration (minutes) |
|---|---|
| FLASH | 0–15 |
| QUICK | 16–60 |
| LONG | 61–90 |
| EXTENDED | >90 |

### 1.4 Reentry Outcome Buckets
- **Standard (6)** — applies to: ECO_HIGH, ECO_MED, ALL_INDICATORS (names not constrained here; count = 6).
- **Compressed (3)** — applies to: ANTICIPATION_1HR, ANTICIPATION_8HR, EQUITY_OPEN_ASIA, EQUITY_OPEN_EUROPE, EQUITY_OPEN_USA  
  - **BUCKET_1**: Breakeven OR Partial loss OR Stop loss  
  - **BUCKET_4**: Partial profit  
  - **BUCKET_5**: Hit take profit target

### 1.5 Reentry Generations
- **2** (G1 and G2).

---

## 2) Counting Model

Let:
- |S| = 8 signals
- |F| = 4 future buckets
- |K| = 4 duration buckets (only for ECO_HIGH/ECO_MED)
- |O_std| = 6 outcomes (standard)
- |O_cmp| = 3 outcomes (compressed)
- G = 2 reentry generations

**Original trades:**  
`|S| × |F| = 8 × 4 = 32`

**Reentries (split by signal rules):**
- ECO_HIGH + ECO_MED: `G × (|O_std| × |K| × |F|) = 2 × (6 × 4 × 4) = 192` **per signal** → ×2 signals = **384**
- Compressed 5 signals: `G × (|O_cmp| × 1 × |F|) = 2 × (3 × 1 × 4) = 24` **per signal** → ×5 signals = **120**
- ALL_INDICATORS (std outcomes, no durations): `G × (|O_std| × 1 × |F|) = 2 × (6 × 1 × 4) = 48`

**Reentry subtotal:** `384 + 120 + 48 = 552`  
**Grand total per symbol:** `Original (32) + Reentries (552) = **584**`

**Across 20 pairs:** `584 × 20 = 11,680` combinations.

---

## 3) Per-Signal Contributions (audit)
| Signal | Original Combos | Reentry Combos (2 gens) | Total per Signal | Reentry Outcome/Duration Mode |
|---|---:|---:|---:|---|
| ALL_INDICATORS | 4 | 48 | 52 | 6 outcomes (standard), no durations |
| ANTICIPATION_1HR | 4 | 24 | 28 | 3 outcomes (compressed), no durations |
| ANTICIPATION_8HR | 4 | 24 | 28 | 3 outcomes (compressed), no durations |
| ECO_HIGH | 4 | 192 | 196 | 6 outcomes × 4 durations |
| ECO_MED | 4 | 192 | 196 | 6 outcomes × 4 durations |
| EQUITY_OPEN_ASIA | 4 | 24 | 28 | 3 outcomes (compressed), no durations |
| EQUITY_OPEN_EUROPE | 4 | 24 | 28 | 3 outcomes (compressed), no durations |
| EQUITY_OPEN_USA | 4 | 24 | 28 | 3 outcomes (compressed), no durations |

**Check:** Sum of "Total per Signal" = **584** (must equal 584).

---

## 4) JSON Spec
A machine-readable JSON spec is provided alongside this document, mirroring the definitions above.

**File:** `new_matrix_spec.json`

---

## 5) Change Log (relative to original baseline)
1. Removed `ANTICIPATION_4HR` and `ANTICIPATION_12HR`.  
2. Reduced future-event buckets from 6 → 4; new ranges set for LONG (61–480) and EXTENDED (481–1440).  
3. Reentry durations restricted to `ECO_HIGH`, `ECO_MED` with 4 buckets (FLASH, QUICK, LONG, EXTENDED).  
4. Reentry outcomes compressed to 3 buckets for 5 specified signals.  
5. Two reentry generations retained.

**Resulting reduction per symbol:** from 3,660 → **584** (−**84.04%**).  
**Resulting reduction across 20 pairs:** from 73,200 → **11,680** (−**84.04%**).

