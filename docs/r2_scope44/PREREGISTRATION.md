# Scope #44 at R2: preregistration

**Status: DRAFT for the author's approval.** Drafted by Claude on 25 October 2026. Nothing has been run with the
real seed, and the real seed cannot exist until this file is approved and committed (§4). Dry runs use a different
seed (§8).

**Why R2.** PLAN_110 §4 asks for R2 on a published headline whose margin is below 30×. The window class's binding-cell
margin is 26× (scope #44, R1, `results/claim_debts_20261022/scope44/run001/scope44_receipt.json`).

## 1. The claim

At the binding cell (B8x52 knock-out basket, ε = $0.001, primary conventions), every certified window
amplitude-estimation row of §5 has M > 1 in the primary column and in every single-departure column. M ≤ 1 would be
needed for a tenfold advantage. Equivalently, **the NO-GO holds**. The headline is M for the protocol as run (row
W_proto). v4 reports 26.1.

The claim rests on four certified pieces. This scope re-executes them sealed, and it draws one fresh preregistered
sample:

| Piece | R1 value | What this run does |
|---|---|---|
| P2 window constants c(δ), parts 1-4, valid for 800 ≤ N ≤ 1,048,575 | 4.179 (δ = 0.003), 6.052 (1e-4), 4.197 (2.9e-3) | Re-certifies all three with the pinned R1 code. Each must reproduce exactly |
| A2a bias \|E Y_N − E Y\| | 6703058386012589/2^64 = 3.634e-4 ≤ 0.55ε | Re-runs both paths with the pinned R1 code. Must reproduce exactly |
| U1 mean bounds on E[g] | m = 3.28804 (R1 sample) | A **fresh** sample with a preregistered seed. It gives m_U (upper) and m_L (lower) |
| M per row and column | 26.08 (window), 26.96 (quantum-only mean) | Recomputed for all five rows of §5 |

## 2. What changes from R1, and why

1. **The U1 sample is new, and its seed is fixed by this document.** The R1 log records the sample step twice, and
   nothing on disk shows whether other seeds were tried (24 Oct review, R-U1-2). Here the seed is the SHA-256 of
   this approved, committed file plus the manifest (§4). It cannot be chosen after the fact.
2. **Quantum-favourable rows are added.** A NO-GO must survive the reading most favourable to quantum. R1 evaluated
   the window class at P2's m (3.3268), and the quantum-only mean class at its worst stage-1 outcome. Both are
   slightly unfavourable to quantum. This scope adds:
   - W_proto, the protocol as run;
   - W_oracle, with the exact mean given for free;
   - Q_lower, the fewest calls over stage-1 successes.

   The decision uses every valid row (§6). The R1 rows are kept as continuity checks.
3. **Wording fixes from the 24 Oct review** (`docs/review_20261024/REVIEW.md`):
   - P2 holds for 800 ≤ N ≤ 1,048,575, not "all N ≥ 800" (R-P2-2). Every N used here is checked against that range.
   - Parts 3-4 are checked again with 3 rotations per controlled phase, not 2 (R-P2-3).
   - The 1e-9 U1 slack covers arithmetic rounding only. Barrier-decision flips are covered by headroom, not by the
     slack (R-U1-1).

## 3. Fixed code and inputs

Every file the run executes or reads is listed, with its sha256, in `research/r2_scope44/manifest.json` (31 files).
The manifest groups them as sealed-run code, reused R1 code, the R1 sampler and its saved totals, the A2a premises,
cited inputs, and R1 records that must reproduce.

Manifest sha256: `226e74491936a8e24e33a33c3049c10892777b10e403733cc3d7584923b6c840`

The steps refuse to load a file whose hash differs from the manifest.

## 4. Seed and sealing

- **Seed.** `seed_hex = SHA-256("r2-scope44-u1-seed-v1\n" ‖ bytes of this file ‖ "\n" ‖ bytes of manifest.json)`.
  The U1 generator is numpy PCG64 `default_rng` seeded with the eight 32-bit words of seed_hex.
- **Real-mode gates.** `sealed_run.py --author-run` refuses to run unless all of the following hold:
  - the interpreter is the pinned `.context/frontier_t0_env` 3.12.4, run with `-I -S -B`;
  - this file cites the manifest hash above exactly once;
  - every manifest hash matches;
  - the Approval block below has no `<placeholders>`;
  - this file, the manifest and every listed file are committed, unmodified, and pushed;
  - no earlier run used a different preregistration;
  - no earlier run passed.
- **Outputs.** Every output is created exclusively under `results/r2_scope44/RUN/`. The receipt goes to
  `.context/R2_SCOPE44_SEALED_RECEIPT_RUN.json`; that is the author's write, made by running the script.

## 5. Procedure and definitions

The steps run in order, each in its own process. A failing step stops the run.

| Step | Flags | What it does |
|---|---|---|
| p2 | -I -S -B | Calls `p2_window_constant.certify` for (β 3.87, δ 0.003), (5.72, 1e-4) and (3.88, 2.9e-3), with γ = 0, δ_target = δ − 4e-6, N0 = 800, grid 0.001 and bracket [c_R1 − 0.05, c_R1 + 0.10] |
| a2a | -I -S -B | Runs the A2a primary path, the independent path and the summary (the R1 scripts), with outputs redirected into the run |
| u1_sample | -I -B | First reproduces the R1 sample (seed [2026102231, 8, 52], n = 2^23). Its totals must match bit for bit. Only then does it draw the fresh sample: n = 2^23, seed from §4, same contract |
| u1_bound | -I -S -B | m_U = UCB + bias and m_L = LCB − bias, with one-sided empirical Bernstein (Maurer & Pontil 2009, Thm 4) at R = 40, slack 1e-9, δ_U = 1e-4 and δ_L = 1e-4. The bias is the A2a step's |
| headline | -I -S -B | N, k and M for the rows below. Parts 3-4 budget ≤ 4e-6 for every N. Continuity against the R1 receipt |

**Rows.** S = 8192/211, e = 0.45ε, and k = N / (σ_q/e). For a mean m, N(c, m) = ⌈c / Δ(m)⌉, where Δ(m) is the
largest Δ with √(m(S−m))·Δ + SΔ²/4 + 2^-39 ≤ e.

| Row | Calls | Valid when |
|---|---|---|
| **W_cont** | N(4.179, price + L1), i.e. P2's m (v4 continuity) | m_U ≤ price + L1 |
| **W_proto** | N(4.179, m_U). This is the protocol as run, and it is **the headline** | always |
| **W_oracle** | N(4.179, m_L): a lower bound with the exact mean known for free, holding with probability ≥ 1 − δ_L | always |
| **Q_cont** | max(⌈6.052/D1⌉, 800) + N(4.197, price + 2S(D1/2 + D1²/4)), with D1 = 0.0035 and δ1 = 1e-4 (R1) | always |
| **Q_lower** | The same stage 1 + N(4.197, m_L): the fewest calls over stage-1 successes | always |

**M.** M = k · 10 · (σ_q/e) · D_eff · t_layer / T_C, with t_layer = 100 ns. T_C, σ_q, D_eff and the departure factors
are read exactly as in `SCOPE44_PROSPECTUS.md` and the R1 recompute. The columns are:
- primary;
- all_free_oracle (D_eff all-free);
- one_lane_one_core (T_C × h16);
- symmetric_distfree (T_C × the distribution-free factor);
- all_free_plus_symmetric (stacked);
- compiled_iterate_primary (C11). This column is informational.

## 6. Decision rule (fixed now)

- **NO_GO_CERTIFIED** if all three hold:
  1. Every valid row has M > 1 in each of the four explicit single-departure columns: primary, all_free_oracle,
     one_lane_one_core and symmetric_distfree.
  2. The A2a bias is ≤ 0.55ε.
  3. Every parts 3-4 budget holds.
- **NO_GO_NOT_CERTIFIED** otherwise. It is reported as found. It is not reconciled, rerun or redefined.
- **Not part of the decision:** the stacked column all_free_plus_symmetric (R1 value 0.075) and the compiled column.
- **Probability.** The rows that use m_U or m_L hold with probability ≥ 1 − 2·10^-4 over the U1 sample, under the
  iid premise. δ_U stays charged to the C03 failure union, as in R1. δ_L enters only the NO-GO statement.

## 7. Predictions (from R1)

- c = 4.179, 6.052 and 4.197 exactly.
- The A2a bias equals R1 exactly.
- The R1 sample totals reproduce bit for bit.
- m_U ≈ 3.29 ± 0.004.
- W_proto: k ≈ 8.72, M ≈ 25.9 to 26.0.
- W_cont = 26.076 and Q_cont = 26.957, matching R1 to 1e-9 relative.
- The smallest explicit M, about 1.29, is in the all_free_oracle column.
- Outcome: **NO_GO_CERTIFIED**.

## 8. Gates, failures and dry runs

- **Deterministic steps** (p2, a2a, the R1 reproduction, continuity) must reproduce R1 exactly. A mismatch is
  `FAILED_AT_<step>`, and it means the environment or code is not what was preregistered.
- **After a failure,** the outputs are kept. A rerun needs a new RUN name and the same preregistration, hence the same
  seed. A failure caused by the science (rather than by a crash or the environment) is reported, not rerun.
- **Dry runs** (`--dry-run OUT RUN`) are package QA only:
  - they use the seed tag `r2-scope44-u1-DRY-RUN-seed-v1`, so they reveal nothing about the real sample;
  - they may not write under `.context/` or `results/r2_scope44/`;
  - they are not R2 evidence.

## 9. Lifecycle: who does what

This condenses the limitation-program lifecycle. It keeps the steps that bear on the claim: preregistration,
author QA, independent peer review, root readiness, the sealed release, the saved verifier and the result review. It
drops the program's metadata-custody and CPU-admission steps. The author may reinstate them.

| # | Step | Who | Artifact |
|---|---|---|---|
| 1 | Prospectus and code | Claude (done) | this file, `research/r2_scope44/` |
| 2 | Author static QA: a dry run, then the verifier on it | Claude (done) | `results/r2_scope44_dryrun/dry_run001/` |
| 3 | Independent peer review of the method (part A) | **a human reviewer** | `docs/r2_scope44/HUMAN_REVIEW_PACKET.md`, part A |
| 4 | Root ready: approve, fill in the Approval block, commit and push | **the author** | this file, committed |
| 5 | Sealed release | **the author** | `results/r2_scope44/run001/`, `.context/R2_SCOPE44_SEALED_RECEIPT_run001.json` |
| 6 | Saved verifier | **the author** | `.context/R2_SCOPE44_VERIFICATION_run001.json` |
| 7 | Actual-result review (part B), then the R2 record | **the human reviewer**, then **the author** | packet part B; one line in `CURRENT_NUMBERS` |

**When R2 is complete.** Only when steps 5 and 6 pass **and** the human reviewer signs part B. Until then the paper
says R1.

## 10. Cited premises, not re-verified here

PLAN_110 §5 says existing receipts are cited by SHA. This scope cites the following without re-verifying them, and
the human reviewer is asked whether that is acceptable:
- σ_q (`sigma_dev`);
- the classical wall T_C (C2/C5 timing with the C10 run006 speedups);
- D_eff (the W0 floor and the N1 floor sheet);
- the RQMC price (used only in the continuity rows and in Q_cont);
- the run002 A2a premises;
- the U2 binding E[g] = E[Y_N] (U2 note O2).

## Approval

- Approved by (author): <name>
- Date: <YYYY-MM-DD>
- Human reviewer for parts A and B: <name>
