# Does the NO-GO change? (frontier probe, 21 October 2026, round 2)

**Short answer: the verdict stands as worded, but its margin and robustness do not.**

At the primary conventions, every estimator class with an explicit worst-case constant still has M > 1 at the
binding cell (B8x52, $0.001):
- **10.29** for the window method certified here;
- **232.0** for canonical with the U1/U2 credits;
- **801.5** for the schedule certified today.

"No design with certified constants reaches 10×" therefore remains true. But P2 removes the largest gap in the
ledger: the explicit-constant margin falls about 22-fold, from 232 to 10.3. **One** favourable departure now takes
M to about 1 or below:
- the symmetric distribution-free classical convention: **0.28**. It is 0.82 even with **no** U1/U2 credit;
- the idealized all-free oracle: **0.51**;
- best loader plus free exponential: **0.97**;
- one quantum lane against one classical core: **1.005**, which just misses.

The R1 justification (a primary margin of at least 30×) no longer holds for the explicit class. All values are
mod; the window class is q+ in the sense of its conditional credits.

## What the probes found (both independently reviewed)

**P1, control-variate residual span: killed.**
- **Closed-form controls cannot reduce the span.** The payoff jumps by $38.6 across the arithmetic-basket
  barrier, and every closed-form-mean control is continuous there. So the residual span is at least $38.6
  against S = $38.8 for every β.
- **Every evaluated route stays below 4.** Using consistent gain pairing, the best is clipped/hybrid
  preintegration: **3.42** at D ratio 1, and **2.62** at the structure-aware ratio of 1.30. Closed-form controls
  give ≤ 1.59; unclipped preintegration gives 1.70.
- **More integration directions make it worse.** Preintegrating over 2 or 3 directions nets ≤ 0.70 once their
  node cost is charged.
- **The review's challenges are answered.** The R2 review raised the hybrid and multi-direction routes and a
  desk-cost overcount; all three are now evaluated.
- **Recommendation:** close F20/F04. The hybrid margin (3.42 against 4) rests on a measured tail and an assumed
  classical tail-time model.

**P2, explicit worst-case window constant: clears.**
- **The constant.** A Kaiser window has a closed-form transform. An explicit Poisson-aliasing bound makes the
  concentration bound increase in N, so a certificate at N0 = 800 holds for every larger N.
  - With finite readout and implementation error made explicit (parts 3-4: < 1e-11 and ≤ 1.9e-6),
    c(0.003) = **4.179** and **k = 8.762** at the binding cell.
  - The R2 review re-derived every inequality and brute-forced N up to 300,007 with no violation; its findings
    were minor only.
  - The literature check found nothing better than canonical (AQAE at about 409).
- **Conditions it still rests on:** the U1/U2 credits (as the 197.6 row does), the direction-select call cost,
  and the inherited cost model.

**P3, desk estimate of oracle cuts.** With k = 8.762, M ≤ 1 at the primary conventions needs D_eff ≤ 223 layers
(2.2e7 T per iterate), against 2,296 today. Only designs with both the loader and the exponential near-free get
there; either alone leaves M ≥ 4.4.

## What still holds the NO-GO up

1. **The primary practice-CI convention.** Under the symmetric convention it is gone (0.28; 0.82 with no
   credits).
2. **The current-law oracle**, Box-Muller plus a polynomial exponential, about 10× above the threshold.
3. **Conditional credits at the primary convention:**
   - without U1: 18.4;
   - without U1 and U2: 30.3;
   - without direction-select: 20.6;
   - with N1's floor alone: 16.2.

## Recommendation

- **Adopt P2 into v3, then put the revision through review.** P2 has now had one AI R2 review; a human check
  of [P2_DERIVATION.md](P2_DERIVATION.md) is still advisable before submission.
- **Reword the claim.** It should say the negative holds at the primary convention with a current-law oracle,
  with a margin of about 10×, and that a single departure overturns it.

## Suggested v3 edits (not applied)

1. **Abstract M table.** Re-label the window row "explicit worst-case constant (this probe)": 10.29 (δ = 0.003) /
   8.64 (δ = 0.01) at the primary convention, and 0.28 / 0.23 under the symmetric convention. Make it the "best
   explicit" row. Keep 232.0 as "canonical with U1/U2" and 801.5 as "certified today".
2. **Abstract "checkable threshold".** The explicit-class limits become about 223 layers and 2.2e7 T per
   iterate, up from 9.9 / 9.9e5. The all-free floor (114 layers) is then inside the limit, at M = 0.51.
3. **Abstract and §8 robustness.** "Robust only at the primary practice-CI convention" becomes "robust only at
   the primary practice-CI convention **and** a current-law oracle; one favourable departure suffices". Add
   1 lane vs 1 core at 1.005, and the no-credit symmetric value 0.82.
4. **§3 ledger and threshold table.** Add a window row: k 8.762, limits 223 / 2.2e7, all-free M = 0.51.
5. **§4.2.** Replace "no usable explicit worst-case constant" with the P2 certificate:
   - the window, the bound, N0 = 800, parts 3-4, c and k values, and their conditions;
   - the literature rows: AQAE 2407.16795 Thm 2 at about 409; Rall 2103.09717 Prop 5 and Hamoudi 2108.12172
     Prop 4.1, both canonical plus medians; KO, Rall-QSP and Kimmel-Low-Yoder / Belliardo-Giovannetti not
     explicit, or RMSE only.
6. **§4.2 and §8 "achievability" gap.** The gap between the counting floor (about 1.85) and the best explicit
   constant shrinks from about 100× to about 4.7× (8.762 / 1.85).
7. **§5.1-5.3.** Add the window rows. The minimal departures for the explicit class become one. Update the
   "Reading" paragraph and §9.1 item 4.
8. **§6 lever 1.** Mark it as met (c = 4.179 against a target of about 4.2). The remaining items are human
   review and the U1/U2 certificates.
9. **§6 lever 5, §7.3 and Appendix A.** Move F20/F04 to §7.1 "closed for this task", citing:
   - the jump argument;
   - the consistent-pairing nets: closed form ≤ 1.59, preintegration 1.70, hybrid 3.42 at D = 1 / 2.62 at
     D = 1.30, multi-direction ≤ 0.70;
   - the kill threshold of 4.

   Remove "That last escape is open" from the abstract, and reword the §1 exclusion of residual oracles to
   "examined and closed".
10. **§6 lever 2 / P3.** With the window constant, M ≤ 1 at the primary conventions needs the loader and the
    exponential near-free together (0.97); either alone leaves M ≥ 4.4.
11. **§8 rigour.** The ≥ 30× margin that justified R1 now holds only for the certified-today (801.5) and
    canonical (232) classes. The window class sits at 10.3×; its P2 constant has had an AI R2 review, but not a
    human one.
12. **§9 discrepancies.** Add "WS-k window c (DPSS 4.168, uncertified) vs P2 certified Kaiser 4.179: +0.3%".

Files: [STATUS.md](STATUS.md) (round 1, then round 2, with every number labelled and hashed),
[P2_DERIVATION.md](P2_DERIVATION.md), and `research/` and `results/` `frontier_probe_20261021/`.
