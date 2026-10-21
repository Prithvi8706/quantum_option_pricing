# E11 unblock design notes U1–U5: index, ranking and next scopes

Status: **design index only**, written 2026-10-10 by a workflow subagent (label `e11_readme`). It is not a review receipt, preregistration or authorization. No controller, launcher, verifier or reporter was run. Nothing outside this file was written in the repository. The program stays at `USER_REQUESTED_STOP_CHECKPOINT` after scope #43. `progress.json` `/phase` begins `USER_REQUESTED_STOP_CHECKPOINT:43`, and the #43 ROOT receipt has `beyond44_SCI_authorized: false`.

Notes indexed here. Hashes were recomputed today and match the hashes the notes cite for each other.

| Note | SHA256 (prefix) | Helper(s) under `research/parallel_E11_unblock_20261010/` |
|---|---|---|
| `U1_PRICE_UPPER_BOUND.md` | `543e620e` | `U1/u1_symbolic_terms.py` (`70b5ab24`), output `_run001.json` (`3966bcc4`) |
| `U2_MEAN_AWARE_SCHEDULE.md` | `6a4d5996` | `U2/mean_aware_schedule_arithmetic.py` (`b1f24a29`) and `U2/tight_span_variant_arithmetic.py` (`4ba6fc57`), outputs `cac54669`, `6de53a16` |
| `U3_PRICE_LOWER_BOUND.md` | `19102e98` | `U3_U5/u3_u5_pure_constants.py` (`b5b75812`), output `1640869c` |
| `U4_SCOPE44_FOUR_TARGET_PROSPECTUS_DRAFT.md` | `aaca085c` | none (an inline Fraction check, not saved) |
| `U5_SECOND_MOMENT.md` | `63236741` | shares the U3_U5 helper |

---

## 0. Bottom line

1. **None of U1–U5 can change the advantage verdict.** The most any of them can do is halve the bounded-AE Grover calls (2x). The gap ledger has B4x12 at ε=0.10 at about 1.1e5x at the current k and 10 ns, and most cells at 1e3–1e4x even at k=3. A 2x saving leaves every cell far above the 10x criterion. The value of these items is **rigor and accounting**: closing E11 honestly, either as "≤2x, conditional" or as a certified negative. It is not progress toward G3–G5.
2. **The best estimator lever is U2 §4, the support-tight wrapper.** It needs no mean certificate. Comparing a 47-bit selector against 3·Yraw (span 128/3 USD) halves M at ε=1/10 and 1/100 using only the audited E03 support. **I reproduced this independently** (section 3). It is also the only saving here that does not depend on the open law/node binding (U2 O2). Its cost is a new wrapper emission, which no note has costed.
3. **Combining U1 with U2 §4 is the one finding no note states.** U1 says no barrier-free bound can reach the 3/100 or 1/1000 thresholds. That holds only for the span-64 wrapper (thresholds 5.22 and 6.04 after the L1 bridge). Under the (3,47) support-tight wrapper the halving thresholds become 9.267 and 11.203. After subtracting L1 = 0.045202 they are about 9.22 and 11.16, above U1's R7 screen of about 7.5–8.2. So **R7 plus the support-tight wrapper plausibly halves M at all four targets.** Either alone halves only at 1/10 and 1/100. Caveats: the R7 range is a screen, not a bound, and this combination is still conditional on U2 O2.
4. **U3 and U5 can only confirm a negative.** No valid moment certificate can make the Hadamard planner cheaper than bounded AE. U3 would make that rigorous; U5 shows a second moment has no entry point into the cost. Both rest on an **unsaved** break-even S\* ≈ 0.3–0.9 USD².
5. **U4 (#44 four-target check) has close to zero information value.** Pure constants force 13 of the 15 rows per profile, and the other 2 follow from verified displays. It buys custody (scope count 43 → 44), not knowledge.

## 1. Summaries

### U1: certified continuous B4x12 price upper bound (design)

- **Route R7.** The second-moment (Lo/Scarf) bound on the unbarriered Asian call: E[Y] ≤ (d/2)(β + sqrt(V + β²)). It is closed form in the single transcendental q = e^{1/2000}, with an outward exact-rational recipe (N=10 Taylor, 2^-192 power grid, 2^-128 sqrt grid). It needs no Φ and no log.
- **Target.** m_f + L1 ≤ m\* = 10.242691369 at ε=1/100, so m_f ≤ about 10.1975. That would allow, but not perform, a halved schedule: 983,025 → 491,505 calls.
- **Plausibility.** The leading-order screen puts R7 at about 7.5–8.2 USD (margin about 2 USD). R1, vanilla domination, screens at about 9.0 and is documented only as an alternative.
- **Byproduct.** E[Y²] ≤ d²(V + β²), screened at about 180–190 USD², as an optional informational field. It gives no estimator gain.
- **Cost.** Under 1 s of arithmetic, plus the full lifecycle.

### U2: mean-aware bounded-AE schedule (design)

- **Mean-aware schedule.** It replaces sqrt(a(1−a)) ≤ 1/2 with sqrt((m/64)(1−m/64)). Exact halving thresholds are m\* = 19.159773, 5.267484, 10.242691 and 6.086186 USD at ε = 1/10, 3/100, 1/100 and 1/1000. PLAN_43's rounded 19.16, 5.27 and 6.09 round **up** and are not sufficient as stated. Quartering is out of reach at every target.
- **m must bound the digital E[g].** A continuous certificate transfers through the #43 L1 bridge: m_f ≤ m\* − L1.
- **§4 support-tight normalization.** Use `sel_b < c·Yraw` with c·sup Yraw ≤ 2^b. With (3,47), span = 128/3. This halves M at 1/10 and 1/100 with **no** mean certificate, and raises the mean thresholds at 3/100 and 1/1000 to 9.27 and 11.20.
- **Rotations.** All IQFT rotations for halved schedules at ε ≥ 1/100 already exist (pi/8 … pi/65536). ε=1/1000 needs new pi/131072, pi/262144 and pi/524288.

### U3: certified price lower bound (design)

- **Purpose.** Make the "moment estimators cannot win" verdict rigorous via S ≥ E[g²] ≥ (E g)² ≥ (m_f − L1)² > S\*. This needs m_f ≳ 0.994 USD against PLAN_43's unsaved S\*_max ≈ 0.9.
- **Route B.** A pointwise lemma f ≥ d[(A−K)1_D − (A−K−c)^+] − d·c·1_KO, built from three terms:
  - an exact Curran-type sub-event term C1, tilted on ln G;
  - a tail bound T(K+c), tiers T1–T3;
  - a Doob maximal-inequality bound on P(KO), with a Rogers–Shi K3 bound that is exactly lognormal (β=1).
- **New primitives.** It needs a certified Φ enclosure (none exists in the repository) and a T3 root bracket.
- **Assessment.** "Plausible, not assured."

### U4: scope #44 four-target accuracy check (prospectus draft)

- **What it checks.** It compares the sealed #42 mean m, the #43 L1 and the #43 L2SQ, per profile, against the half-budgets ε/2 and the 11/2000 E07 headroom.
- **Forced outcome.** Lemmas S0–S3 force 13 of 15 rows per profile from pure constants: 5/147 and 97/2940 both exceed 3/200, and 9409/7350 > 1. Expected result: compatible only at ε=1/10, through the mean and L1 rows. Everything else is ruled out for this fixed route.
- **Lifecycle.** A full 19-step lifecycle is mapped. The note itself rates its expected value as low and suggests an annotation as the cheaper alternative.

### U5: certified continuous second moment (design)

- **R1.** E f² ≤ M·m_up (f² ≤ M·f), and Bhatia–Davis gives the variance bound. Applied directly to g with the audited support M_g and E g ≤ m_up + L1, it dominates the Minkowski/RMS transfer.
- **Fallback.** Any m usable by U2 beats the E03 fallback, since every m\* < M_g/2 = 19.408911.
- **Conclusion.** No moment certificate can reduce estimator cost. Bounded AE never reads a moment, and the planner needs S < S\* ≤ (E g)². Do not spend a scope on U5. If E11 item 2 must be closed formally, piggyback R1-direct on U1's certificate.

## 2. Ranking by expected value

| Rank | Item | What it could deliver | Conditional on | Cost / risk |
|---|---|---|---|---|
| 1 | **U2 §4 support-tight wrapper (3,47)** with the U2 schedule variant | 2x fewer calls at ε=1/10 and 1/100 with no mean certificate. Only the E03 all-input support enters | Nothing beyond E03 support (re-checked for 3·Yraw) | **High.** It needs:<br>- a new wrapper (×3 multiplier and uncompute, 47-bit comparator, extra selector bit);<br>- source-graph and marking checks;<br>- a support re-check and a re-derived readout (128/3 is not a power of two, so 2^-39 is only a placeholder);<br>- new IQFT ledgers at 12 and 15 bits;<br>- a per-call cost delta, which is not evaluated. |
| 2 | **U1 R7 upper bound** (plus U5 R1-direct as a free informational field) | A certified m_f. With span 64, halving at 1/10 and 1/100. With (3,47), plausibly at all four targets (section 0 item 3). Also the first certified B4x12 continuous second-moment bound | U2 O2 / U1 O2: Y_N is the E02 comparator input under the finite Hadamard input law (open; E07 lists `finite_input_law_and_joint_Box_Muller` open). Also the #42 criterion | **Low compute** (seconds). Lifecycle cost only. The outcome is fairly predictable (screen margin about 2 USD), so information gain is moderate. Alone it changes no estimator; it needs a schedule scope (rank 3) |
| 3 | **U2 §3 span- and mean-parametrized schedule certificate** | A saved, exact `certified_schedule` variant with inputs (span, m). Reproduces E07 at (64, 32). Emits the unconditional (3,47) rows and the conditional mean rows | A wrapper (rank 1) or an m certificate (rank 2) to be usable | **Low.** Pure exact arithmetic with tests. New schedules at 1/10, 3/100 and 1/1000 are a new preregistered choice |
| 4 | **U3 lower bound** | A rigorous negative: no certified moment input makes the Hadamard planner competitive | A **saved** planner S\*(ε) evaluation (U3 O3, not yet existing), planner monotonicity in S (O4), law identity (O1/O2) | **Medium-high.** It needs a new certified Φ primitive with an independent second implementation, a root bracket and a fixed grid of 5×7×6 = 210 (κ', κ_c, κ_a) points × 9 tier pairs. Strength "plausible, not assured." Value is accounting only |
| 5 | **U5 standalone** | E11 item 2 "transferred, not advancing" | m_up (U1), O3 reviewer wording decision | Do not run standalone; piggyback on U1 |
| 6 | **U4 / #44 four-target check** | Saved custody of "fixed polar-safe route fits only ε=1/10" | #42/#43 conditional premises | A full 19-step lifecycle for a predetermined outcome. Prefer an annotation |

Dependencies:
- **U1 → U2 §3.** The mean-aware halving uses U1's m_f.
- **U2 §4 → U2 §3 → IQFT/E07 ledger rows.** The support-tight wrapper needs the schedule variant, which then needs new IQFT and E07 ledger rows.
- **U5 R1 → U1.** U5's direct route needs U1's m_up.
- **U3 → saved planner S\*(ε) and the Φ primitive.** U5's "no gain" verdict becomes rigorous only after U3.
- **Shared open obligation.** Every item except the U2 §4 *worst-case* rows inherits U2 O2 / U3 O1–O2, the law and node binding. U4 inherits the #42/#43 premises P1–P10.

## 3. Spot-checks performed here

I wrote an independent script in the session scratchpad (`scratchpad/e11_readme/spotcheck.py`, not in the repository). It ran under the pinned `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4), imported no repository module, and reads saved records only.

| Claim | Source checked | Result |
|---|---|---|
| U1 contract: σ=0.3, ρ=0.4, r=0.03, T=1, S0=K=100, H=140 strict, 4×12, discount once, weights 1/4 and 1/48 | `G0_run003/B4x12_task.json`; `barrier_oracle_depth.py` lines 33, 77, 85, 86, 87, 88 (line numbers confirmed). U3's `barrier_fast_classical.py` line 39 carries the same literals (sha `18611d7d` confirmed) | **Verified** |
| U1 exact constants: a²=3/1000, b²=9/2000, μ=−3/200, exponent units 5j/15m/6m/60 per 1/2000, Σmin(j,l)=650, β₁=13/8, V₁=17875/96, leading screen 7.683 undiscounted | exact Fractions | **Verified** |
| U1/U2 halving thresholds at span 64 | π_hi from `E07_schedule_run001/schedule.json /pi_enclosure_exact`; readout 2^-39 from the E02 ledger `/classical_readout_error_allowance` = [1, 549755813888] | 19.1597737614, 5.2674847074, 10.2426913698, 6.0861860219. These match U2's truncations. U1's 10.242691369 differs from U2's 10.242691368 only by truncation. **Verified, including that 19.16, 5.27 and 6.09 round up** |
| E07 M=65536 reproduced, 983,025 calls; baselines 8192, 16384 and 524288 at the other targets | same | **Verified** |
| **U2 §4 support-tight halving** | E03 `/cases/0/payoff_raw_bounds` = [0, 42680645928225]. 3·sup = 128041937784675 ≤ 2^47; 211·sup ≤ 2^53 | (3,47) and (211,53): worst case fits at M/2 for ε=1/10 and 1/100, and the least M there is 4096 and 32768. At 3/100 and 1/1000, M/2 needs m ≤ 9.26707589 / 11.20258479 for (3,47) and m ≤ 11.20892106 / 14.47690470 for (211,53). **Verified arithmetic.** Wrapper cost and readout: **not verified** (U2 itself says unevaluated) |
| M_g/2 = 19.408911 (U5); every m\* below it | E03 rational | **Verified** |
| U4 S0–S3: B_band = 481689599/566466967836; 5/147 > 3/200 and > 11/2000 and < 1/20; 97/2940 = (194/5)/1176 with the same orderings; 9409/7350 > 1; 9/2000 + 11/2000 = 1/100 | exact Fractions; budgets read from the four-target ROOT review (`/four_original_targets_dollars`, `/bias_budgets_dollars`) and E07 `complete_price_ledger.json` (`/assessment/remaining_dollar_headroom` = [11, 2000]) | **Verified.** Premise "U ≥ d" (#43 P2) **not re-checked** |
| L1 display 0.045202052 and RMS 1.275228500, both profiles | `E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md` line 7 and the following lines | **Verified** (display only; no limbs decoded) |
| U3 constants: Var ln G = 143/7680, E ln G − ln100 = −13/1600, γ_j = 11j(25−j)/64000, K3 Var = Cov = 99/2000 (β=1), E[B_T \| G_B] = G_B·e^{81/4000} | exact Fractions | **Verified** |
| Rotations pi/8 … pi/65536 exist | `E02_IQFT_run001/rotations.json` keys | **Verified** |
| E24 13/20 is a 15-qubit IQFT ledger; T-counts 255,951,625,444,980 (15 bits) vs 511,911,060,861,915 (16 bits) | `E24.../13_of_20/iqft_operations.json` (swap wires span 15), `digital_estimator_row.json`, E02 ledger | **Verified.** The Rz count of 4095 was not counted |
| Orientation price 3.5188852273893136 | `c1_summary.json` | **Verified** (uncertified, as all notes say) |

## 4. Unverified, wrong or weak claims (flags)

1. **Interpreter deviation.** All design helpers ran under system CPython 3.9.13. That covers U1, both U2 helpers, the U3_U5 helper and U4's inline check. The standing project rule is the pinned 3.12.4 with `-I -S -B`, never system 3.9. The pure-constant results I re-checked reproduce under 3.12.4. Any preregistered SOURCE must use the pinned environment, as U1 O7 already notes.
2. **S\* ≈ 0.3–0.9 USD² is unsaved.** It comes from PLAN_43 §2(b): K_H ≈ 5540–5873 against calls·e = 4423.6. Both U3's target (m_f ≳ 0.994) and U5's "no gain possible" depend on it. Not verified here.
3. **U1 screens are not bounds.** R7 at 7.5–8.2 rests on a first-order expansion plus a "~5%" guess for the higher-order terms. R1 at about 9.0 is first order. I deliberately did **not** evaluate R7 numerically, so the route stays non-adaptive for a future preregistration. My exact check covers only the first-order coefficients.
4. **U1's "3/100 and 1/1000 need a barrier-aware route" is incomplete.** It is true only for the span-64 wrapper. Under U2 §4 the thresholds roughly double (section 0 item 3). U1's ε=1/10 and 1/100 use cases are **made redundant** by the support-tight wrapper if that wrapper is adopted.
5. **Law/node binding is open (U2 O2).** Every m-certificate-based saving, U3's transfer and U5's digital transfer assume Y_N (node 5697) under the #42 coupling has the circuit's finite Hadamard input law. E07 lists `finite_input_law_and_joint_Box_Muller` as open. The #42 and #43 records are conditional.
6. **U2 §4 cost.** The per-call cost of the ×3 multiplier, the extra selector bit and the uncompute was not evaluated ("expected small" is unproved). The readout allowance 2^-39 is a placeholder, and decoding with S' = 128/3 needs a non-dyadic multiply.
7. **U3 details.**
   - The Doob step writes E[(M_T − a)^+] but bounds basket calls E[(B_T − k)^+]. The factor e^{−rT} relating them is implicit and must be explicit in a prospectus.
   - Refinement (i), the tilted submartingale, is unproved.
   - There is no certified Φ in the repository.
   - Planner monotonicity in S (O4) is unproved.
8. **U5 orientation numbers.** The scratch MC values E f² ≈ 44.47 and Var ≈ 32.09 are not in the repository (U5 says so). U1's 180–190 USD² is a screen. Whether direct support×mean transfer satisfies ESTIMATION.md's E11 wording needs a reviewer decision (U5 O3).
9. **U4 predicted values.** MEAN_1 compatibility uses m ≈ 0.04648. That was decoded from #42 limbs in the PLAN_43 scratch, not from a results page, so it was not re-checked. The L1_1 row follows from the verified display. U4 must not peer-review its own draft (it says so).
10. **Unsaved baselines.** Only the ε=1/100 schedule is saved. All 1/10, 3/100 and 1/1000 schedule numbers in U1, U2 and U5 are unsaved formula evaluations.

## 5. Recommended next preregistered scopes after #43

Ground rules:
- Run one scope at a time.
- Use waves of at most 4 parallel agents, saving after each lifecycle step.
- Each scope's closing receipts keep `USER_REQUESTED_STOP_CHECKPOINT=true` and set `beyond<N+1>_SCI_authorized=false`.
- No design-note author (U1–U5 or this README) takes the peer, FIELD-peer or audit role for its own design.

**Option 0 (recommended if the goal is only the ≥10x verdict): no new E11 scope.**
- E11's maximum effect is a conditional 2x, so the advantage verdict does not depend on it.
- Record U2's threshold corrections, U4's S0–S3 lemmas and U5's "no moment gain" verdict as annotations.
- Authorization needed: "Yes, add an annotation (no lifecycle, no credit) to the #43 results/STATUS records." Editing `docs/limitation_program_20261001/` is outside this design's write scope.

**If the user wants E11 estimator work carried to a saved result, do these in order:**

1. **#44 = `E11_B4X12_CONTINUOUS_PRICE_UPPER_R7` (U1, with U5 R1-direct as an informational field).**
   - The decision fields should be fixed *before evaluation* against both span 64 and the (3,47) span at all four targets. This extends U1 §7, so the prospectus peer must accept the extension.
   - Authorizations:
     - (a) "Lift the #43 stop for #44 metadata work (prospectus through ROOT release)";
     - (b) separately, "Authorize #44 SCI";
     - (c) choose U1's fixed recipe as written (no R1/R3 fallback).
2. **#45 = span- and mean-parametrized bounded-AE schedule certificate (U2 §3 item 3, generalized to span S').**
   - Exact arithmetic with tests. It reproduces E07 at (64, m=32) and emits the (3,47) worst-case and mean-aware rows.
   - Authorizations:
     - (a) and (b) as above for #45;
     - (c) a decision whether the unsaved targets 1/10, 3/100 and 1/1000 become saved schedules (a new preregistered choice).
3. **#46+ = support-tight wrapper (3,47) emission and audit.**
   - New predicate, support re-check of 3·Yraw, readout re-derivation, per-call cost delta, then IQFT ledgers (12 and 15 bits; 18 bits plus new rotations for 1/1000) and an E07 ledger row.
   - This is several A/E-category scopes.
   - Authorization: an explicit "yes" to **change the B4 wrapper** (a circuit change, not just a schedule), plus a/b per scope.
4. **Law/node binding scope (U2 O2).** Required before any mean-certificate-based saving can be claimed unconditionally.
   - Authorization: a/b for that scope.

**Deferred.**
- **U3.** Run first a small scope that saves the planner S\*(ε) at the four targets (U3 O3), together with the monotonicity statement (O4). Proceed to the Φ primitive and Route B only if the user wants the negative made rigorous for the manuscript.
- **U4 / #44-as-drafted.** Not recommended. If the user wants the count, the authorization is U4's step 0: "lift the stop for #44 metadata work" and, separately, "authorize #44 SCI".

## 6. Non-claims

This README claims none of the following:
- no certified price, moment, variance or bias;
- no schedule change, estimator saving or wrapper change;
- no review, peer acceptance or authorization;
- no G2–G5 progress;
- no 110-item credit;
- no quantum advantage.

Spot-check results are pure-constant arithmetic and reads of saved records. They are not program artifacts. E11 stays partial.
