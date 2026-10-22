# 110-item plan: where it stands (22 October 2026)

> **Current numbers:** see [CURRENT_NUMBERS.md](CURRENT_NUMBERS.md) (headline run006; window 26.1, all-free 1.30, symmetric 1.50, no single departure reaches M <= 1). Figures below may be from earlier runs.

This is a read-me for the user on return. **Nothing is committed.** The commit at 38648422 holds the 21 Oct
frontier probe only; everything listed below dated 22 Oct is uncommitted, on branch `claude/kind-carson-9eedd7`.

## Plan position

| Plan stage (PLAN_110_EFFICIENT.md) | State |
|---|---|
| W0 decision inputs | Done (10-11 Oct) |
| DP1 | NO-GO (11 Oct), with the 12 Oct errata |
| Branch N (headline, R1 cards, manuscript) | v3 draft done (12 Oct); sign-off pending (yours) |
| Frontier probe P1-P3 (21 Oct) | Done; committed 38648422. P1 killed, P2 certified window constant, P3 desk |
| Register update | run002 (probe), run003 (C10), run004 (C09/H16), run005 (C03/H18); run001 unchanged |
| Fired triggers worked on 22 Oct | C10 (challengers), F06, F07, C09 (measured), H16 (re-measured), C03 (skeleton), H18 (desk) |
| Saved for later (your instruction) | Human check of P2; applying the v3 edits; pushing or merging the branch |

## Where the headline M stands now

Binding cell B8x52 $0.001, all inputs measured, after the C10 review. Source:
`results/frontier_probe_20261021/headline/run005`.

| Estimator class | Primary | Single departures | Minimal departures to M ≤ 1 |
|---|---:|---|---|
| Certified today (E07 schedule) | 1,666 | all-free 82.7; symmetric 96.0 | 3 |
| Canonical explicit (U1 + U2 + non-dyadic) | 482 | all-free 23.9; symmetric 27.8 | 3 |
| **Window, certified constant (P2; U1 + U2 + direction-select)** | **21.4** | all-free **1.06**; symmetric 1.23; 1 lane 2.22 | **2** (all-free + symmetric 0.061) |
| Window, quantum-only mean (U2 + direction-select, no classical price) | 22.1 | all-free 1.10; symmetric 1.27 | 2 |

How this moved:
- **11 Oct, DP1:** 232.
- **21 Oct, P2:** 10.3.
- **22 Oct, C10/C09/H16 plus the review:** 21.4. The classical comparator is 2.08× faster with the same estimator, and
  the cheapest distribution-free method was measured.

**Verdict.** The NO-GO stands at the primary conventions with a 21× margin and is robust to any single favourable
departure. Two departures together overturn it.

## Register state (run008, current)

Tiers (run008): T1 4, T2 6, T3 11, T4 31, T5 33, T6 25 (110 in total).

| Run | Rows changed | What changed |
|---|---:|---|
| run002 | 37 | F20, F04, E25 closed; C11 bracket 1.85-8.76; F05 live; 9 triggers flagged |
| run003 | 9 | C10 wave; F06 and F07 closed |
| run004 | 5 | C09 measured; H16 re-measured |
| run005 | 13 | C03 skeleton frozen; H18 desk condition; TRIG-HWACT un-fired (23.1 > 10) |
| run006 | 8 | Review adoption: QF T_C, replicated-RQMC symmetric factor, quantum-only mean option |
| run007 | 4 | Float32 GEMM (headline run006); r3 review |
| run008 | 3 | C10 closed (complete for applicable challengers); float32 consistency |

Every run has a CHANGES.md.

## What is waiting on you

1. **Human check of P2** ([P2_DERIVATION.md](../frontier_probe_20261021/P2_DERIVATION.md)). It has had one AI R2
   review. A second AI review of the C10/C09 work was running when this file was written; see
   `results/c10_challengers_20261022/review/`.
2. **The v3 edits.** Use [V3_EDITS_CURRENT.md](../frontier_probe_20261021/V3_EDITS_CURRENT.md): 15 items with the
   current numbers. It supersedes MEMO.md's list.
3. **Push or merge** the branch, and commit the 22 Oct work.
4. **Claim-grade debts that need authorization:**
   - C03 rows B2-B4: the 0.007 of the failure budget that is unallocated ([C03_SKELETON.md](../c03_skeleton_20261022/C03_SKELETON.md));
   - the A02/A07/A13 re-proofs behind the binding cell's eligibility;
   - the U1 certificate (frozen scope);
   - the C11 compile (circuit work).
5. **An optional cleaner timing.** Re-run the C10 paired timing with the Windows power-mode overlay at its default.
   That removes the assumption that the speedup ratio is state-invariant. I did not change system settings.

## Where to look

| Topic | File |
|---|---|
| The probe (P1-P3) | [docs/frontier_probe_20261021/STATUS.md](../frontier_probe_20261021/STATUS.md), [MEMO.md](../frontier_probe_20261021/MEMO.md) |
| C10, C09, H16 | [docs/c10_challengers_20261022/STATUS.md](../c10_challengers_20261022/STATUS.md) |
| C03 / H18 | [docs/c03_skeleton_20261022/C03_SKELETON.md](../c03_skeleton_20261022/C03_SKELETON.md) |
| Running log | [docs/frontier_probe_20261021/WORKLOG_20261022.md](../frontier_probe_20261021/WORKLOG_20261022.md) |
| Register | `results/plan110_w0/register/run005/REGISTER.md` and `CHANGES.md` |
