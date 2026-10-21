# Efficient plan for the 110 limitation items

10 October 2026. This is a plan only: nothing in it has been executed. The program is still at `USER_REQUESTED_STOP_CHECKPOINT` after scope #43, and each wave below needs your authorization.

This version merges three inputs:
- the v1 synthesis, [supporting/PLAN_110_v1_draft.md](supporting/PLAN_110_v1_draft.md), which holds the full 110-row table in Appendix A;
- the waste critique, [supporting/CRITIQUE_waste.md](supporting/CRITIQUE_waste.md);
- the wrongly-killed critique, [supporting/CRITIQUE_wrongly_killed.md](supporting/CRITIQUE_wrongly_killed.md).

Inputs are the gap ledger [supporting/gap_ledger.json](supporting/gap_ledger.json) and the per-item triage [supporting/triage_rows/](supporting/triage_rows/).

---

## 1. The one thing that matters

A tenfold win needs `N_calls × D_call × t_layer ≤ T_C / 10`. The current numbers are:

| | Today | Source |
|---|---|---|
| Calls per price (k × σ/e) | k_eff ≈ 586-1,067 (bounded AE, span $64, 15 medians, dyadic M) | E07/E24 schedules; ε=$0.01 saved, others modelled |
| Depth per call | 555,774 (B4x12) / 663,704 (B8x52) T-layers | A10 accepted source |
| Logical layer time | 100 ns assumed. Demonstrated complete loops run at 446-550 ns (d=3); projections are 1-10 µs | H01/C15 |
| Classical time-to-accuracy | 0.06-22.5 s (16-core laptop, preintegrated RQMC / OSS) | Stage C c2/c5 timing |
| **Miss factor** (needs ≤ 1) | **2×10⁵ to 4×10⁶** at current k and 100 ns. 554 to 1.7×10⁴ even at a hypothetical k=3 | gap_ledger.json |

**How the 110 items act on this inequality.**
- **4-6 items decide it.** These are the achievable estimator constant, an idealized oracle floor, the logical-layer anchor, and the comparison conventions.
- **About 8 items can move one term by ≥2×.**
- **About 37 items are certification debt or cheap audits.** They matter only once a construction survives.
- **About 60 items are dormant conditionals or a different task.**

The 43 scopes completed so far, including the E11 L2 bridges, each move the miss by ≤ 1.3×. **That was the inefficiency:** claim-grade rigour spent on percent-level certificates for a construction that is 10³-10⁶× off budget.

**Current verdict.**
- With evidence-backed constants, the answer is **no**: the residual miss is ≥ 10²-10³.
- With an optimistic but not absurd corner (all four conditions below), the answer is **borderline**. Under matched parallelism or symmetric coverage, it can cross 10× in non-overhead cells:
  - a 99% estimator with k ≈ 3-30;
  - an idealized oracle of about 3,000 reaction layers;
  - layers of 100 ns or less;
  - free magic-state supply.

So the decision rests on two unknowns (the estimator constant and the oracle floor) and on three **contract conventions that you, not research, should fix** (§3).

## 2. What changed from v1 (and why)

| Change | Reason |
|---|---|
| **Parallelism is now an explicit convention, not a hidden assumption.** DP1 is reported for (a) 1 quantum lane vs 1 classical core and (b) L lanes vs 16 cores, using per-lane k_lat | v1 called "one serial lane vs 16 cores" quantum-favourable. It is quantum-**adverse**. Fixing this cuts the optimistic-corner miss by ~11-16× (wrongly-killed F1) |
| **B8x52 at $0.001 is back in DP1**, treated at zero deterministic bias on the quantum-favourable side. One desk task prices tightening the $0.00124 bias bound | It was excluded on a loose *upper* bound designed for the $0.01 budget. For a negative claim, excluding the cell closest to 10× is not safe (F2) |
| **Classical coverage convention as two columns**: practice CI vs distribution-free 99% | C09 says this alone can move the inequality 2-5× toward quantum (F6) |
| **The estimator credit is a joint table, not "2×".** It covers span × mean bound × dyadic/non-dyadic M, screened jointly with E04. It also names window/QSP amplitude-estimation constants (to be verified against primary sources) | The E03/U2 credit reaches 4× at three cells. U2 §4 wrongly said "not reachable" (F3). The 15-median factor may be compressible (F4) |
| **The oracle floor uses unlimited width under one explicit budget W, and reports the loader's share of the floor** | A width-capped floor is not quantum-favourable. If loading dominates the idealized floor, A04/A03 become floor-deciding (F5, F7) |
| **The first wave shrinks.** Two agents run the k bracket and the floor, one small agent the bias/depth desk task, and an orchestrator script builds the decision table. Everything else moves to the branch where it is produced once | Most of v1's first wave did not feed the decision and was redone later (waste fixes 1-3) |
| No standalone independent recompute; no scope factory before GO; register by script; manuscript drafting in parallel; the headline scopes merge into one | Third copies of the same numbers; a single-use abstraction; 66 record-only items do not need agent review (waste fixes 4, 5, 11, 15, 16) |
| The supply default (1e12 T/s) is no longer a GO gate; required T/s and width become necessary-condition columns | An unevidenced default blocked GO by itself (F5) |
| C14's "2× forward" depth reading is closed as an error | The saved per-iterate depths are 1.03-1.16× the clean source (F9) |

## 3. Decisions that are yours (cheap, high leverage)

These are contract choices in C01/C09. Settling them up front removes whole branches of research. The first wave reports results under every option, so they do not block it.

1. **Parallelism matching.** Should the quantum machine be compared at an equal number of lanes, at an equal physical budget, or as one lane against the 16-core laptop?
2. **Classical coverage convention.** Should the classical side be held to practice confidence intervals, or to the same worst-case 99% guarantee as the quantum schedule?
3. **Width / physical budget W.** What qubit and factory budget is admissible when evaluating the floor, lanes and supply?
4. **Claim wording if the answer is no.** Should it read "no construction with certified constants reaches 10×" (achievability, which is what the evidence supports), or "unreachable" (which needs query lower bounds)?

## 4. Waves

At most 3 agents run at once. Every workstream appends one JSON row per sub-result to its own file, so a usage-limit stop loses at most one row. CPU runs execute in the background and notify on exit.

### W0: decision inputs (about 4-6 working days; R0 screen rigour)

| Workstream | Items | Output |
|---|---|---|
| **Script** (orchestrator, no agent) | F31, C14, C04, C02, E24, F01 (labels only), F02, H16 (score), C09 (columns) | `decision_table.json`. Every cell × {1-lane/1-core, L-lane/16-core} × {practice, distribution-free coverage} × {e = 0.45ε, e = ε}. Columns: M_DP1, depth needed for 10×, t_layer needed, required T/s and width. Extends the existing `gap_calc.py` |
| **CPU, background** | H16 | The 1-16 worker classical grid with strict idle gating, about CPU-minutes. It turns the parallelism convention into measured numbers |
| **Agent WS-k** | E01, C11 (bracket), E25, E08, E03 (+U1/U2), E04, E20 (lanes) | `k_bracket.md` with three parts:<br>• an access-model lower bound;<br>• k_lo, the achievable constant with an explicit 99% guarantee, including window/QSP amplitude estimation if primary sources give constants;<br>• the joint E03/U2 span × mean × dyadic table screened with E04, and per-lane k_lat |
| **Agent WS-floor** | A01 (+A16, A09, A08, A02, A07, A13, F05, F20 as parameters) | Idealized clean-call **reaction-layer floor**, computed coarse first (half a day) and refined only if within 10× of threshold. Reported at unlimited width under budget W, with the loader's share of the floor. If loading is ≥ 50%, cost A04/A03 analytically |
| **Agent WS-bias** (small) | C02, A07/G2 | Decomposes the B8 $0.00124 bias bound and prices tightening it to ≤ $0.00055. Closes the 2× depth reading |

**Early stop.** If k_lat × coarse floor exceeds 30× the threshold in every convention, stop W0 and write the DP1 memo. Do not finish "for the record"; branch N produces those numbers once, at proper rigour.

### DP1: your go/no-go (one-page memo)

`M_DP1 = min over eligible cells of D_floor × 10 × k × (σ/e) × t_layer / T_C`, reported per convention.

| Outcome | Rule | Next |
|---|---|---|
| **NO-GO** | M_DP1 > 3 in every eligible non-overhead cell, under the conventions you fixed in §3 | Branch N |
| **GREY** (now the most likely) | 1 < M_DP1 ≤ 3, or the answer flips between conventions | One ≤ 1-week wave on the deciding term only (usually k constants or the floor), then a DP1 re-decision. GREY happens at most once |
| **GO** | M_DP1 ≤ 1 in an eligible non-overhead cell | Branch A |

### Branch N: rigorous negative / frontier result (about 1.5-2.5 weeks)

- **One merged headline scope (#44).** It covers the decision table, the oracle floor and the H03 recount by SHA citation, with every convention column. Rigour is R2 if the margin is < 30×, or R1 (independent recompute plus receipt) if the margin is ≥ 30×, since then precision cannot change the conclusion. You choose at DP1.
- **Two R1 cards.** One is the estimator access-model card (E01/C11/E03/E04/E08/E25/E20). The other is the hardware and classical card (H01/H02/C15 as a citation list, H17 necessary-condition columns, C09/C10 labels).
- **Manuscript drafting runs in parallel** (C12, E22, the F20/F04/F05 "even with free X" sentences). After that, only numbers are substituted, followed by review, audit and your sign-off.
- **The 110-item register is generated by script** from the triage rows and Appendix A, with about 10 records spot-checked.

### Branch A: advantage corridor (only after GO; months)

1. **A1, kill-first screens (2-3 weeks).** Classical strengthening runs first on CPU, but only on the GO cell. Then k certification (U1 R7 price bound and/or the U2 support-tight wrapper, plus E04), the deciding floor subgraph emitted at R1, and a hardware-activation scenario.
2. **DP2.** Recompute with certified values. Continue only if the miss is ≤ 1 at a non-overhead cell.
3. **A2.** Combined emission (C13) and the woken dormant items.
4. **A3.** Claim-grade G3/G4/G5: E07, C03, the full C11 compile, H17/H18 and the full G4 timing. **The scope factory is built here**, where it pays off.

## 5. Rigour tiers

| Tier | Use | Cost |
|---|---|---|
| **R0 screen** | W0, every kill, every register record | Spec → script → JSON with input hashes and measured/modelled/assumed labels → one self-check. About 0.2-0.5M tokens |
| **R1 component** | DP1-adjacent cards, branch-A levers before adoption | R0 plus an independent recompute along a different path, plus a one-page receipt. About 1M tokens |
| **R2 claim-grade** | **Only** headline numbers that will be published | The existing ~19-step lifecycle. About 2-5M tokens |

**Rule.** Component-level (L4) results never get R2. Several certificates that share inputs go into one scope. Existing receipts are cited by SHA, not re-verified.

## 6. Stop / deprioritize now

- **All further E11 scopes**, including the #44 four-target draft (U4) and more L2 bridges. The E11 design README (`docs/parallel_E11_unblock_20261010/README.md`) independently reached the same recommendation: no new E11 scope, annotations only. U1/U2 return only on branch A, as estimator credits.
- **Percent-level A-family certificates:** A13 screen v3, the A14 later stages, A20 metadata timing, extra A03 levels, the AS241 loader, and the A01 46-leaf reconciliation.
- **Classical re-timing for precision:** the C8 relaunch, GPU anchors, 20-run confirmations and the F01 32-scramble acquisition. Note one label correction: the B8 $0.01 confirmation met its half-width in only 55% of runs, so fixing it would *favour* quantum, though by ≤ 1.5×.
- **The H03 reaction-map rerun, new H05 fixtures, H18 admissibility checks on > 100 ns anchors, the E12 finance acquisition and the E20 P=1/2/4 lane schedules** (the lane question moves into the W0 convention table).
- **Different-task items** (Heston, nested, compound, rough volatility, SPDE, Greeks, portfolios): parked, with a register line only.

## 7. Effort

| Phase | Wall time | Peak agents | Tokens (est.) |
|---|---|---|---|
| W0 | 4-6 days | 3 (+script, +CPU) | 1-1.5M |
| DP1 | your call | — | — |
| GREY wave (if needed) | ≤ 1 week | 2 | 1-2M |
| Branch N | 1.5-2.5 weeks | 3 | 3-7M (R1 headline) / 5-9M (R2) |
| **To a finished negative/frontier result** | **about 3-5 weeks** | | **about 6-12M** |
| Branch A | 2-4+ months | 3-4 | 30M+ |

v1 estimated 3-4 weeks and 13-20M tokens for branch N. The waste critic's revision is 1.5-2 weeks and 6-10M. The figures above add W0's extra convention columns and a possible GREY wave.

**What "done" means:**
- **(a) Initial pass over all 110:** 110/110 register records with a status, an evidence pointer, a rigour tier and a reopen rule (by script), plus DP1 decided. Reached at the end of W0, in about 1 week.
- **(b1) Advantage claim:** one eligible non-overhead cell satisfies the inequality, with every term at R2 (G3, G4, G5), an independent replication, and no double counting.
- **(b2) Negative/frontier result:** the headline table shows the miss under every convention you fixed, the idealized floor still misses, the k bracket comes with its access model, and the necessary-condition columns are stated. The scope is explicit: this construction family, the fixed task, the strongest *tested* classical method, and certified constants.

## 8. First week, concretely

| Day | Action |
|---|---|
| 0 | You answer §3 (or say "report all conventions"), and authorize W0: 3 agents at R0, writes only to `research/plan110_w0/` and `results/plan110_w0/`, a ≤ 1.5M token cap, and the H16 CPU grid. |
| 1 | Start the script and the H16 grid in the background. WS-k starts first, because it is the cheapest falsifier. WS-floor starts with the coarse floor. WS-bias runs half a day. |
| 2-3 | k bracket delivered. The coarse floor is delivered, then refined if within 10×. The early-stop check runs. |
| 4-5 | `decision_table.json` filled for every convention. Register generated by script. DP1 memo. |
| 6 | **You decide DP1.** |
