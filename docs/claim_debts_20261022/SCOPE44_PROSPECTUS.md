# Scope #44: the merged headline scope, prospectus (written before any run)

22 October 2026. The user authorized the claim-grade debts, including lifting the scope-#43 stop. This prospectus
fixes what scope #44 computes, and from which inputs, before the computation runs. Its own runs go to
`results/claim_debts_20261022/scope44/`.

## 1. What the scope certifies

It certifies **one number per estimator class**: the binding-cell M = k / k_10x at the primary conventions (B8x52,
ε = $0.001), together with the convention columns of the headline table. The definitions are fixed and unchanged
from the N1 headline:
- k_10x = T_C / (10 · (σ/e) · D_eff · t_layer);
- M = k / k_10x;
- σ/e = σ_q / (0.45 ε).

There are four inputs.

| Input | Value it must reproduce | Source (cited by sha256 at run time) |
|---|---|---|
| k, window certified | 8.762 | `results/frontier_probe_20261021/p2/run002/p2_window.json` |
| k, window quantum-only mean (the class C03 can complete) | 9.058 | `results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json` |
| D_eff | 2,296 layers (W0 floor, q+). The C11 compiled value is a second column, if C11 delivers one | `results/plan110_w0/ws_floor/floor.json`, `results/claim_debts_20261022/c11/run001/summary.json` |
| T_C | 8.89 s | Stage C 22.53 s divided by the paired QF speedups (2.078 × 1.220); `results/c10_challengers_20261022/` |
| σ_q | binding-cell value | `results/frontier_classical_20261001/sigma_dev/sigma_dev.json` |

## 2. Independence requirement

The run must recompute the binding-cell row with **new code**:
- It may not import or copy `headline_m.py` or `headline_m_probe.py`.
- It must read the raw inputs listed above.
- It must agree with `results/frontier_probe_20261021/headline/run006/headline_table.json` to within 1e-9 relative.

A mismatch is reported as a failure, not reconciled after the fact.

## 3. Eligibility and completeness gates

- **Eligibility.** The binding cell is eligible at ε = $0.001 only if the certified bias is ≤ 0.55 ε. The bias comes
  from `results/claim_debts_20261022/a2a/run001/summary.json` (the A2a clip-split certificate). If that certificate
  is absent or fails, the scope reports the binding cell as **ineligible on certified bias**. The headline then falls
  back to the smallest eligible cell, using the same rule as run006's `summary_min_M_eligible_non_overhead`.
- **Completeness (C03).** The complete-price status comes from `results/claim_debts_20261022/c03/<run>/c03_ledger.json`.

## 4. Decision rule (fixed now)

**NO-GO holds** if every explicit class has M > 1 at the primary conventions and in every single-departure column.

Rigour follows PLAN_110 §4:
- If the window margin is ≥ 30×, the scope is **R1**.
- If it is < 30×, R2 is required. In that case this scope delivers R1 and lists the remaining R2 lifecycle steps:
  independent human peer review, ROOT registration and a sealed receipt under `.context/`. Those steps are outside
  this session's write permissions.

## 5. What is out of scope

The scope does not cover:
- new physics;
- a new classical timing;
- the physical-layout and hardware items H03/H06/H17 (TRIG-HWACT has not fired);
- any claim of advantage.
