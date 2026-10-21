# DP1 memo: go / no-go after W0

> **Errata (12 Oct 2026, after the branch-N R1 recompute and review).** These corrections come from `results/plan110_n1/headline/receipt.md`, `research/plan110_n1/estimator/estimator_card.md`, `research/plan110_n1/hwclassical/` and `results/plan110_n1/review/REVIEW.md`. They narrow the margin. The NO-GO under the primary conventions stands.
>
> 1. **Two departures, not three.** "Reaching M ≤ 1 with explicit constants needs at least three favourable departures" is wrong. The symmetric distribution-free classical convention costs the classical side about 37× at the binding cell, measured from Stage C data. My 2-5× assumption was too small.
>    - That convention alone takes explicit M to about 6.3, or 11.2 without the uncertified U1 mean bound.
>    - Adding the idealized all-free oracle gives 0.31.
>    - The primary verdict therefore depends heavily on the practice-CI choice.
> 2. **B8x52 at $0.001.** The table used e = 0.45ε there. That cell is admitted on the modelled clamp tightening (bias about $0.00047), not on "zero bias". A consistent zero-bias reading gives explicit M of about 104.
> 3. **Floor provenance.** The headline M values use W0's R0 floor. N1's independent floor is 1.55× less favourable, and with it alone M = 1,258 / 364 / 13.5. R1 confirms the verdict, not the exact quoted values.
> 4. **New conditional credit.** Direction-select control is covered by BHMT Theorem 12, which is worth about 2× on k; explicit M becomes about 200.
> 5. **Open escape.** A control-variate residual oracle could shrink the payoff span and so lower the bounded-AE k directly. It has not been measured and is not closed.

11 October 2026. All work here is W0 (R0 screen) under the conventions in [research/plan110_w0/W0_CARD.md](../../research/plan110_w0/W0_CARD.md). All values are modelled unless marked measured. Nothing in `.context/`, STATUS or the progress records was touched, and the stop checkpoint after #43 still stands.

## The result

The test is M = (estimator constant achieved) ÷ (largest estimator constant that still gives a 10× win). **M ≤ 1 means 10× is reached.** The table gives the minimum M over eligible, non-overhead cells. The tightest cell is always B8x52 at $0.001 (made eligible at zero bias, see below).

The primary conventions are: one quantum machine with 1e7 logical qubits against one 16-core classical machine; practice confidence intervals; 100 ns logical layers; 1e12 T/s supply; the current Box-Muller sampling law; and e = 0.45ε.

| Estimator class | k (total calls / (σ/e)) | **M, primary** | Lowest M with one favourable departure |
|---|---:|---:|---:|
| Certified today (E07 schedule) | 586-1,067 | **801** | n/a |
| Best with an explicit 99% constant (conditional credits included) | 187-198 | **232** | 11.5 |
| Window / QSP amplitude estimation (no explicit constant in any source) | 6.9-7.4 | **8.6** | 0.43 |

The favourable departure in the last column is the idealized "all-free" oracle: a free loader, a free exponential, and narrower words.

**Verdict under your conventions and your wording: NO-GO.** No design with certified constants reaches 10×. The best explicit-constant design misses by 232× in its best eligible cell. Reaching M ≤ 1 with explicit constants needs at least three favourable departures stacked together. An example is the idealized all-free oracle, plus zero deterministic bias, plus one quantum lane compared against one classical core, which gives M = 0.51.

## What W0 established

- **Oracle floor** (WS-floor). An idealized clean call takes 326 reaction layers for B4x12 and 740 for B8x52 at 1e7 qubits. That is roughly 900-1,700× below today's accepted sources of 555,774 and 663,704.
  - **Magic-state supply binds before depth.** One B8x52 call at 100 ns needs 4.4e12 T/s, against the 1e12 budget.
  - The loader is 36-56% of the floor.
  - Files: `results/plan110_w0/ws_floor/`.
- **Estimator constant** (WS-k). The certified constant today is 586-1,067.
  - With every conditional credit applied, the best explicit worst-case 99% constant is about 187-198. Those credits are the U1 mean bound, the U2 support-tight wrapper and non-dyadic M.
  - Window and QSP estimators reach about 7-26 in one chain, but **no primary source gives a finite worst-case constant**.
  - The rigorous query lower bound is about 1.7-1.85.
  - The estimator constant is now the single largest gap between "what is proved" and "what may be possible".
  - Files: `results/plan110_w0/ws_k/`.
- **Classical parallelism** (H16 grid, measured). Going from 16 workers to 1 costs 6.4-10.2×, not 16×. The 16-worker times reproduce Stage C: B8x52 at $0.001 measured 23.46 s against 22.53 s. Files: `results/plan110_w0/ws_small/h16_grid/run001/`.
- **Bias and depth convention** (WS-small).
  - B8x52 at $0.001 becomes eligible by lowering one stock clamp three binades, at about 0% depth cost and re-certification only.
  - The correct per-call depth is one Grover iterate: 571,034 for B4x12 and 770,356 for B8x52, 1.03-1.16× the clean source. C14's "2×" reading is wrong.
- **Register.** All 110 items have a record: 4 decision-critical (done), 8 credited levers, 12 deferred certification debts, 26 closed or folded, 35 dormant with triggers, 25 parked as a different task. File: `results/plan110_w0/register/run001/`. This completes the initial pass over the 110 items.

## What would overturn NO-GO

Two of these are needed together:
1. **An explicit worst-case 99% constant for window/QSP amplitude estimation**, of about 7-10. This moves M from 232 to about 9. It is open research.
2. **An oracle approaching the idealized all-free floor**: a loader and exponential far cheaper than today, at the current sampling law. Together with (1) this gives M ≈ 0.4.
3. **Or** a relaxed convention, such as one lane against one core, a distribution-free classical rigour, 10 ns layers, or a supply above 1e12 T/s.

## Options

- **A. NO-GO → branch N (recommended).** Write the rigorous negative/frontier result, scoped to "no design with certified constants reaches 10× under these conventions". It needs one merged headline scope plus two R1 cards and the manuscript; about 3-4 weeks and 3-9M tokens. The "what would overturn it" list becomes the frontier section.
- **B. GREY probe first (≤1 week).** Attempt one thing: an explicit worst-case constant for window/QSP amplitude estimation. That is the only lever that moves M by more than 10×. Then go to branch N with the result either way. Even a successful probe leaves the primary M at about 9, so the branch-N verdict would stand unless the oracle also improves.
- **C. GO.** Not supported by the evidence.

Files: decision table `results/plan110_w0/decision/run002/`. run001 is preserved; it wrongly included the F20 σ-credit, which needs a σ-normalised estimator.
