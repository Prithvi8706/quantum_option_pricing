# CRITIQUE (wrongly_killed_critic): PLAN_110 levers that were killed or under-tiered

Scope: an adversarial review of `scratchpad/plan110/PLAN_110.md`, looking for the opposite error: levers that were killed, deferred or tiered too low, unsafe kill criteria, dependency errors, and gap-ledger arithmetic that would change tiering. Nothing was executed except read-only arithmetic on the saved ledger (`gap_ledger.json` rows) and the E07/U2 schedule formula.

Labels: **CONFIRMED** means it is checked against repository text or recomputed here. **PLAUSIBLE** means the reasoning holds but needs a W0 screen.

## Verdict in one paragraph

The P-tier "NO" survives every finding below; the evidence-backed residual stays at 10^2 or more. The **Tier-O conclusion does not survive, and neither does the branch-N headline that depends on it.** PLAN §0 and §4.4/(b2) say that even the optimistic corner misses 10x by 8-41x in honest cells and needs t_layer < 100 ns. Three things in the plan produce that result:

1. Running at **one serial lane** is labelled quantum-favourable, which is wrong (F1).
2. The **one non-overhead cell that is closest to 10x** (B8x52, $0.001) is dropped because of a bias upper bound that was never tightened (F2).
3. The plan omits the documented **symmetric-rigour coverage convention** (F6) and an **E03 credit of 4x, not 2x**, at two cells (F3).

Correct these and Tier O reaches 10x at 100 ns in several non-overhead cells. The O-corner then no longer needs a hypothetical k = 3: evidence-backed per-lane constants with about 11 lanes reach about 1x at 10 ns. DP1 as written would return NO-GO and branch N would publish "every eligible cell misses 10x even at Tier O". A referee could overturn that with the plan's own rows. The fixes are cheap (all S, analytic, W0) and are listed at the end.

---

## F1. Parallel lanes and parallelism matching: mislabelled as quantum-favourable and left out of every tier (CONFIRMED, changes tiers)

**Evidence.**
- PLAN §2.1, "Assumptions common to every column (all quantum-favourable)", lists: "calls run serially at one lane, and the 15 repetitions are not parallelised". For a *latency* inequality, serial execution is quantum-**adverse**.
- `gap_ledger.json` itself carries `T_Q_kcur_100ns_longestchain_s` = (M-1)·D·t. That is 15x below `T_Q_..._serial_s` in every row (B8 $0.10: 543.6 s vs 8,154.6 s).
- rows_H H16 (notes): "longest-shot k ~57 for the audited $0.01 15-shot schedule" vs k_total ~853. The same row gives single-worker classical as T_1 <= 16·T_16, "<=16x quantum-favourable".
- PLAN §2.1 also lists "classical stays at the measured 16-core laptop time" as quantum-favourable. Measured against a one-lane quantum machine, a 16-core classical time is not favourable to quantum.
- rows_E E20: lanes are blocked "until ... the C-family contract fixes how parallel quantum hardware is matched against classical parallelism". `implementation_plan/ESTIMATION.md` (E20 acceptance): "Complete paid latency is compared under the same physical budget". **No item in PLAN_110 owns that contract decision.** C01 is "desk record ... then close" (Appendix A), and §8 stops the E20 lane schedules.
- E20's "width bound" (P ~ 1e3-1e4 lanes, >= 4e9 logical qubits; Appendix A) is computed against the *current* depth at k = 3 and $0.001. At the Tier-O floor the lane count needed is about 2-16, so the plan's "just parallelize" rebuttal is too strong by 2-3 orders of magnitude.

**Recomputed from ledger rows** (floor 3,000, e = eps, 100 ns unless stated):

| Cell | Plan O (k=3, 1 lane) | O with matched 1-lane vs 1-core (T_C x16 bound) | Latency tier: k_lat = k_P/11 (11 parallel median lanes), 100 ns | same, 10 ns |
|---|---:|---:|---:|---:|
| B4x12 $0.10 | 8.06 | 0.50 | 50 | 5.0 |
| B4x12 $0.03 | 13.7 | 0.85 | 51 | 5.1 |
| B4x12 $0.01 | 41 | 2.56 | 204 | 20 |
| B4x12 $0.001 | 19 | 1.19 | 75 | 7.5 |
| B8x52 $0.10 (overhead) | 1.13 | 0.07 | 7.7 | 0.77 |
| B8x52 $0.03 (envelope) | 2.81 | 0.18 | 11.4 | 1.14 |
| B8x52 $0.01 | 8.43 | 0.53 | 46 | 4.6 |
| B8x52 $0.001 (see F2) | 2.07 | 0.13 | 9.0 | 0.90 |

**Caveats.**
- k_lat = k_cur/4.76/11 assumes the E04 1.75x survives splitting into independent lanes. Without E04 (it is an adaptive IQAE-class controller and may not be lane-compatible), k_lat is about 2x larger.
- T_1 <= 16·T_16 is an upper bound; H16's 1-16 worker grid gives the real factor.

The direction is not in doubt. Under either symmetric parallelism convention, Tier O drops by roughly 11-16x. The "P-k + floor + 10 ns" column moves from the plan's 8-10x miss to about 1x in the B8 cells.

**Consequences.**
- (i) §0 item 2, §2.3, and the (b2) definition of done ("every eligible cell misses 10x under Tier O, 100 ns") would be false under a matched-parallelism convention. Their scope has to change to "single lane vs 16-core classical, width-capped" (a weak negative) unless the matching rule is fixed first.
- (ii) DP1's formula `M_DP1 = D_floor x 10 x k_lo x (sigma/e) x 100 ns / T_C_env` has no lane term. It uses the total-call k, so it cannot see this lever.
- (iii) H16's own trigger ("run the 1-16 worker grid only if a miss is <= 16x") **already fires at Tier O** (B8 $0.001 at 2.07, B8 $0.01 at 8.4). Yet the plan defers the grid to A1. That is a dependency error: the grid is a few CPU-minutes and decides the 1-lane convention.

**Fix (S).** Add a "parallelism-matching rule" deliverable to W0-WS1, owned by C01/C09 with E20 and H16. Report DP1 under both (a) 1 lane vs measured single-core T_C, from the H16 grid run now with strict idle gating, and (b) L lanes vs 16 cores. Use k_lat = per-lane calls/(sigma/e) and report width and supply per lane. Move H16's grid from A1 to W0 (CPU only).

## F2. B8x52 at $0.001 is excluded from DP1 on a bias *upper bound*, and that exclusion is quantum-adverse for a negative claim (CONFIRMED, changes tiers)

**Evidence.**
- `STATUS.md` (A02/C06 rows): the B8 bound $0.001239557505461456 is a certified bound that was designed to fit the "unchanged 11/2000" headroom of the $0.01 contract. It was never tightened for $0.001. One component bound (polar-CDF/BV) is already only B8 <= $0.000117. The remainder comes from the native cos, stock and barrier bridge terms, which were bounded loosely for a 5.5e-3 budget. This is not a measured bias.
- rows_C C02: "for the negative result, ignoring it is quantum-favourable and therefore safe", and the C02 trigger is "defer it unless the $0.001 gap falls below about 10x". **At Tier O the cell's miss is 2.07, so the trigger has fired.**
- PLAN §4.3 defines `M_DP1 = min over eligible cells`, and (b2) requires that "every eligible cell misses". Excluding the cell is the *quantum-adverse* treatment, the opposite of what C02 says the negative result may do.
- rows_E E01 and rows_H H16/H17/H14/H01 all use B8 $0.001 as the decision cell (k* ~ 0.06, "only ~8x short", TRIG-HWACT 6,520 layers). PLAN §3 TRIG-HWACT also uses it. So the plan uses this cell for its triggers and leaves it out of its verdict.

Among non-overhead cells, B8 $0.001 is the closest to 10x at Tier O. Its miss is 2.07, against 8.4 for the best cell the plan calls "honest" (B8 $0.01). Its classical time is a measured confirmation (22.53 s, preint n = 131,072; rows_F F01), so it is not an overhead artefact. The "8-41x" sentence in §0/§2.3 holds only because this cell is excluded.

**Fix (S).**
- In DP1 and in branch N, treat B8 $0.001 as eligible with zero deterministic bias (e = eps) on the quantum-favourable side.
- Add one W0-WS1 desk item, owned by C02 with A07/G2. Decompose the 0.00124 bound by term, and estimate what bound tightening, or how many extra word or grid bits, would bring it to <= $0.00055, plus the depth cost. A few extra bits on 72-bit words are a few-% depth increase, not a gap term.

## F3. The E03/U2 estimator credit is 4x, not 2x, at B8 $0.10, B4 $0.10 and B8 $0.01, and U2 contains a wrong "not reachable" sentence (CONFIRMED arithmetic)

**Evidence.**
- `docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md` §4 says: "With (3, 47), M/4 needs m <= 5.811476 at eps = 1/10 and m <= 3.514349 at eps = 1/100. Neither is reachable under the orientation price once the bridge is added."
- The orientation prices in `results/frontier_classical_20261001/c1/c1_summary.json` (port_check) are B4 3.5189 and B8 3.2816. With L1 = 0.0452:
  - B4 needs m = 3.564 <= 5.81 at 1/10, which is **reachable**;
  - B8 needs m = 3.327 <= 5.81 at 1/10 and <= 3.514 at 1/100, which is **reachable in both** (U2 checked only the B4 price).
- My recomputation of the exact E07/U2 formula, `e(m,M) = 2*pi*sqrt(m(S-m))/M + S*pi^2/M^2 + 2^-39 <= 0.45*eps` with dyadic M:

| Cell | span 64, m = price+L1 | span 42.67 (3,47), m = price+L1 | span 38.82 (211,53), barrier-free m = 6 | continuous M (no dyadic step), span 38.82, m = price+L1 |
|---|---|---|---|---|
| B4 $0.10 | x2 | **x4** | **x4** | 5.2x |
| B8 $0.10 | **x4** | **x4** | **x4** | 5.4x |
| B8 $0.01 | x2 | **x4** | x2 | 4.3x |
| B8 $0.001 | x2 | x2 | x2 | 3.5x |
| B4 $0.001 | x2 | x2 | x2 | 3.4x |

- PLAN §2.1 credits "E03/U2 p-aware **or** support-tight halving (2.0)". rows_E E03 itself says the p-aware bound "quarters it at $0.10". The two mechanisms compose: support-tight changes the span, and the mean bound changes sqrt(a(1-a)).
- At $0.10, the (211,53) wrapper plus a *barrier-free* bound of about 6 USD (U1 §6 screens barrier-free routes at about 6) reaches x4 with no barrier-aware certificate.
- The dyadic M step costs a further 1.2-1.4x. Every k_eff spread in the ledger (586-1,067) is dyadic rounding.

**Effect.** At the best cells, the evidence-backed k falls by about 2x more than the P column says: about 112 instead of 224 at B8 $0.10.

**Honest caveat in the other direction.** rows_E E04 says its 1.75x is "partly the same p-awareness as E03". Applying E03 at 4x together with E04 at 1.75x may double count, so W0-WS3 must screen them jointly.

**Fix (S).** In WS3, recompute E03 as the joint (span, mean-bound, dyadic or non-dyadic) table above. Record the correction to the U2 §4 sentence. Size the U1 target as m <= 5.81 at $0.10, where a barrier-free bound suffices, and m <= 3.514 at B8 $0.01.

## F4. Confidence-amplification constant: E08 closes the 99% lever after looking at median counts only (PLAUSIBLE, possibly a 3-8x lever on serial k)

**Evidence.**
- rows_E E08: "minimal odd median count ... 15 vs ~11 shots, <=1.4x. Nothing else remains to screen. Close now."
- The current constant is 15 independent canonical shots of M-1 calls, each succeeding with probability 8/pi^2 (U2 §1, E07 `financial_bounded_schedule.py`). Medians cost a factor 15 on serial calls.
- Phase-estimation windows that reach confidence 1-delta inside one longer chain could replace that factor. Examples are Kaiser-window phase estimation and QSP-based amplitude estimation. With these, the cost scales like ln(1/delta)/pi rather than 15. For delta = 0.003 the ratio is roughly 15/1.85, about 8x serial, before the window's own constants.
- A grep of `docs/`, `research/` and `manuscript/` finds **no** Kaiser-window or QSP-AE entry. Kothari-O'Donnell is recorded only with "unknown constants" (`docs/controlled_residual_feasibility/SOURCES.md`, `docs/independent_110_20261004/E09/THEOREM_AND_CONTROLLER.md`).
- The literature names here come from general knowledge and are **not** repository evidence. WS3 must check them against primary sources.

**Why it matters.** This lever acts on *serial* k without the width cost of F1. On the plan's own §2.2 arithmetic it is the difference between k ≈ 224 and k ≈ 30-60.

**Fix (S).** Name window and QSP amplitude-estimation constants explicitly in WS3 and in the C11 bracket. Change E08's kill to "close the median-allocation sub-lever only".

## F5. DP1 and GO rules contain unsafe kill criteria: a width cap, a default supply bound, and an achievability k (CONFIRMED as plan text)

1. **Width.** PLAN §4.3 takes D_floor "at <= 10x the current width cap". A negative claim of the form "even the idealized oracle misses" needs the **unlimited-width** floor, which WS2 already computes, as the quantum-favourable input. rows_A A08 closes log-depth adders only "under the frozen qubit cap". The plan is also inconsistent about width: the O tier grants unlimited magic supply (about 4.6e8 physical qubits in factories) and an uncapped-width credit (1.8x), yet refuses lanes (F1) on width grounds. **Fix:** state a single explicit width/physical budget W and evaluate floor, lanes and factories under that same W.
2. **Supply.** GO requires "required T/s <= the user-set supply bound (default 1e12 T/s)". The O corner needs 4.6e12 (PLAN §2.1), so the default alone blocks GO with no evidence behind it. Meanwhile the supply levers were all killed as "<1.1x on latency" or "non-binding" (rows_H H05 "supply is a non-binding term", H07 cat/non-distillation "acts on non-binding supply", rows_F F23, rows_A A04 "cut scalar-normal T-count by ~10-100x", A16, A09 "95% of T-count"). Cultivation is listed in `implementation_plan/HARDWARE.md` but frozen. That is a dependency error: either supply is not a GO gate, or TRIG-SUPPLY and its levers have to be evaluated at DP1. **Fix:** drop the default and report required T/s and width as necessary-condition columns. If the user sets a bound, run H05/F23/A04 T-count analytic lines (S) in W0-WS4.
3. **k_lo is an achievability number.** WS3 defines k_lo as "the smallest k with a written 99% worst-case guarantee and explicit constants". Using an *upper* bound on achievable k to declare NO-GO is not quantum-favourable. Branch N's title ("advantage not reachable for this task") then overclaims. rows_E E01 has the correct framing: an explicit-constant *lower* bound with k* ~ 0.06 against the current source. At the idealized floor, any lower bound below about 1 leaves the I tier open. **Fix:** either (a) scope the branch-N claim to "no construction with certified constants" and report the k_lo achievability bracket, or (b) use a query lower bound for the "not reachable" wording. Also: "if k_lo > 30, flag early NO-GO" (§9, day 1-2) would fire on total k even when per-lane k_lat <= 30 (F1). Apply the 30 threshold to k_lat.

## F6. The classical side was declared "every pending correction is adverse", but two corrections favour quantum (CONFIRMED as row text)

- **C09 symmetric-rigour convention.** rows_C C09: "A symmetric distribution-free 99% convention would shift the net up to ~2-5x in quantum's favour ... The coverage convention is the one C-family input that can move the inequality by more than 2x."
  - The quantum schedule is already a certified worst-case bound (E07 BHMT Theorem 12 with 15 medians). The classical side uses a practice CI from 16 scrambles.
  - PLAN §2.1 puts the classical term at x1 in every tier, and §1 says "every missing term is adverse to quantum or neutral", which includes "classical true-price coverage".
  - Under C09(b), Tier O for B8 $0.001 is 2.07/(2-5), about 0.4-1.0, and B8 $0.01 is 1.7-4.2.
  - **Fix:** carry C09(a)/(b) as two columns of the DP1 table. A negative claim must survive (b) or be scoped to the practice convention.
- **B8 $0.01 confirmation met its half-width in only 55% of runs** (ledger caveats; PLAN §1). Fixing that raises T_C, which favours quantum. §8 lists the 20-run confirmations as "adverse-only for quantum", which is the wrong direction label. The size is probably <= 1.5x, so this does not change tiers, but the label should be corrected.

## F7. The loader share carried into the idealized floor is taken from the capped source (PLAUSIBLE)

- rows_A A02, A03 and A04 cap every loader at "<= 1.64x B8 dependency depth" using the A01 split of the **capped current** source (normals 39% of the 184,525 T-depth). TRIG-R2, the only reopen path, is defined on the P-tier residual, which is >= 2.9e3. **It can never fire.**
- In an idealized log-depth floor, multipliers and adders shrink by roughly 10-60x in Toffoli layers (rows_A A08/A09; the ledger's "one current multiply 11,088 T-depth"). The sequential Box-Muller transcendental chain (log, sqrt, cos) is then likely to dominate the floor. The ledger's own levers_ranked #2 already says "Gaussian preparation is ~80% of the leaf-score depth ... x~4-5 if free", and rows_F F05 says "free Gaussian preparation cuts oracle/D_max about 5x".
- A04 (MPS bond-8 loader, "most promising loader on T-count") is then floor-deciding, not "irrelevant at a ~10^3 gap".
- **Fix (S):** WS2 reports the loader share *of the floor*. If it is >= 50%, cost A04, A03 and a direct state-prep loader analytically at the floor in W0. Redefine TRIG-R2 on the O-floor residual.

## F8. F20/F04 reopen triggers are already met under corrected Tier O (CONFIRMED)

rows_F F20 and F04 reopen "only if the other levers bring the miss within ~4x". Under F1, F2 or F6, the B8 $0.001 and B8 $0.03/$0.10 cells are at 0.1-2x.

The F20 net credit after coherent preintegration depth is 0.75-2x (F20 row). It belongs in Tier O at <= 2x, not only in Tier I at 4.5x. It applies only with a sigma-normalised estimator: bounded AE does not gain from lower sigma, because the mean, and so sqrt(a(1-a)), is unchanged. That holds in Tier O, where k = 3 is sigma-normalised.

## F9. Gap-ledger and plan arithmetic checks

**Verified correct:**
- the D_max/gap formulas;
- every §1 row (k_eff, D_max, gaps at k_cur/k = 3/k = 1);
- the T_C envelope choice (`T_C_env` is used in the gaps, not the raw `T_C`; for example, B4 $0.03 uses 0.1244, not 0.1268);
- the P product 4.76 x 14.04 = 66.8;
- the O product 356 x 221 x 2.22 = 1.75e5;
- the §2.2 table, the 89 ns and 36-layer figures, the 4.6e12 T/s supply figure, and TRIG-HWACT 6,520 = 10 x 663,704/1,018.

**Errors and inconsistencies (none of these flips P, but they affect DP1 and GREY):**
1. **"M_DP1 is at least 84"** (§4.3). Recomputed with floor 3,000 and e = eps:
   - k = 120: B8 $0.10 = 45 (overhead cell), B8 $0.001 = 83 (excluded cell), B8 $0.03 = 112, B8 $0.01 = 337, B4 >= 322.
   - The "84" is either the overhead cell at k = 220 or the ineligible cell at k = 120. For the cells the DP1 rule actually admits, the minimum is 112 (k = 120) or 206 (k = 220).
   - The statement mixes cells across the plan's own eligibility rules. After F2 the relevant figure is about 83.
2. **The depth-convention flag is too pessimistic in the branch-A direction.** PLAN §1 says "Branch A would be 2x worse" if C14's "2 x forward" reading held. Two records show the 2x reading misreads the clean source as forward-only:
   - rows_A A01: "capped clean source 663,704 vs unlimited-width 2x184,525";
   - the ledger's saved E02 *per-iterate* depths (571,034 vs 555,774 for B4, 1.03x; 770,356 on an older source vs 663,704 for B8, 1.16x).

   The per-iterate depth is about 1.03-1.16x the clean source, not 2x. **C02 should close the 2x reading as an error.** The branch-A risk is <= 1.16x.
3. E20's "P ~ 1e3-1e4 lanes / >= 4e9 logical qubits" is computed at current depth and k = 3. It is not a bound at Tier O (F1).
4. The "8-41x in honest eligible cells" sentence (§0, §2.3) excludes B8 $0.001 (F2). It is correct only as conditioned on the current, untightened bias bound.

## What should change in the plan (all S, inside W0, no new lifecycles)

| # | Change | Owner | Cost | Why |
|---|---|---|---|---|
| 1 | Fix the assumption labels in §2.1/§1: serial one-lane and 16-core classical are **not** quantum-favourable; classical coverage and the 55% hit rate favour quantum | F31 | S | F1, F6 |
| 2 | Parallelism-matching rule in W0-WS1; DP1 under both conventions with k_lat; H16 1-16 worker grid moved to W0 (CPU minutes) | C01/C09 + E20 + H16 | S | F1 |
| 3 | B8 $0.001 included in DP1 at zero bias; decompose the 0.00124 bound and price the tightening | C02 + A07 | S | F2 |
| 4 | Joint E03/U2 table (span x mean bound x dyadic step), screened jointly with E04; correct the U2 §4 sentence | E03 (WS3) | S | F3 |
| 5 | Name window/QSP amplitude-estimation constants in WS3; narrow E08's kill | E01/E08/C11 | S | F4 |
| 6 | DP1 floor at the unlimited-width value under one explicit budget W; drop the 1e12 T/s default or activate the supply levers; k_lo labelled as achievability, early-NO-GO threshold on k_lat | F31/A01/H05 | S | F5 |
| 7 | C09(a)/(b) columns in the DP1 table | C09 | S | F6 |
| 8 | Loader share of the floor; TRIG-R2 redefined on the O-floor residual | A01/A02/A04 | S | F7 |
| 9 | F20 at <= 2x in Tier O | F20 | S | F8 |
| 10 | Close C14's 2x depth reading; restate M_DP1 >= 84 per cell | C02/C14 | S | F9 |

**What this does not change.**
- The P-tier verdict: residual >= 1e2 even after F1-F4.
- The STOP list for E11/L2 bridges, the percent-level A-family certificates and the T6 parking.

**What it does change.**
- DP1 is likely to land in **GREY rather than NO-GO** under a matched-parallelism or symmetric-rigour convention.
- The branch-N headline must either survive F1, F2 and F6 explicitly or be scoped to "single lane, width-capped, practice coverage, certified constants". Otherwise the frontier result is exposed to exactly these objections.
