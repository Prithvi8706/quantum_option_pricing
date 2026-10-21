# U5: certified continuous B4x12 second moment (design prospectus only)

Status: design only, written 2026-10-10. Nothing here is a saved, reviewed or verified artifact. No controller, launcher, verifier or reporter was run. Nothing under `.context/`, `results/limitation_program_20261001/` or `docs/limitation_program_20261001/` was written. **No new moment, variance or price bound was evaluated.**
- The decimal displays of M_g, M_g/2, M_g² and M_g²/4 are exact readings of the saved, audited E03 support rational.
- Law constants come from `research/parallel_E11_unblock_20261010/U3_U5/u3_u5_pure_constants.py` (output `u3_u5_pure_constants_run001.json`, SHA256 `1640869cf17c4c545c4eaaf5cc5d8a1cd7b7210566ac6244dcedf9d3fbabfa0d`).
- The program remains at `USER_REQUESTED_STOP_CHECKPOINT` after scope #43.

Notation:
- f is the continuous discounted strict-140 B4x12 payoff, and d = e^{−3/100}.
- M = 40d is the continuous support (E17).
- M_g = 42680645928225·2^−40 ≈ 38.8178213 is the audited digital support (E03).
- g is the digital payoff the estimator samples.
- L1 ≈ 0.045202052 and RMS ≈ 1.2752285 are the #43 conditional bridges, per own profile (use the exact saved rationals in any scope, not the displays).

---

## 0. Answer in brief

1. **Feasible.** A certified continuous B4x12 second moment is feasible symbolically by several routes. The cheapest, **R1**, needs **no new moment machinery**. Since 0 ≤ f ≤ M, we have f² ≤ M·f, so **E f² ≤ M·m_up**. Bhatia–Davis gives **Var f ≤ m_up·(M − m_up)** when m_up ≤ M/2. Here m_up is any certified price upper bound, the same certificate U2's mean-aware schedule needs.
2. **Digital transfer is simpler without Minkowski.** Apply R1 directly to g, with the audited support [0, M_g] and E g ≤ m_up + L1:
   - E g² ≤ M_g·(m_up + L1);
   - Var g ≤ (m_up + L1)(M_g − m_up − L1), when m_up + L1 ≤ M_g/2.

   This uses #43's **L1**, not its L2/RMS, and dominates the Minkowski transfer for R1-type bounds (§4).
3. **E10 reuse.** E10's C4/H8 machinery is reusable as a **numerical engine** for the analytic routes R2/R2′. That covers the exact-rational exp ledger, interval arithmetic, E[A²]/E[AG]/E[G²] term generation, and the cross-sign rule, which here falls entirely in the *exact-constant-exponent* case.
   - Not reusable: its **theorem** (the compound parity residual under a policy premise) and its **numbers** (0.786189, 118.413579).
   - R2's (G−K)^+ partial moments need a new Φ enclosure, the same primitive U3 needs.
4. **Beats the bounded-payoff fallback?** Yes, readily.
   - R1 beats Var ≤ M_g²/4 ≈ 376.7058 iff m_up + L1 < M_g/2 ≈ 19.4089 (digital), or m_up < M/2 (continuous).
   - Every U2 halving threshold m\* (19.159773, 5.267484, 10.242691, 6.086186) is below M_g/2. So any m certificate U2 could use also makes R1 beat the fallback.
5. **Does it matter for estimator cost (given U2)? No.**
   - The saved E07 schedule and both U2 variants are bounded AE. They consume only the support span and, in U2, a *mean* bound. The Bernoulli amplitude variance a(1−a) is a function of the mean, so a payoff variance certificate has no entry point.
   - The only moment consumer, the Hadamard planner, needs S ≲ S\* ≈ 0.3–0.9 USD² (PLAN_43 §2(b); unsaved workflow evaluation). Every valid certificate satisfies S ≥ E g² ≥ (E g)². That is ≈12.4 by uncertified orientation, and rigorously ≥ (m_f − L1)² once U3 passes.
   - Hence **no achievable U5 bound, however tight, can reduce estimator work**.
   - ESTIMATION.md's E11 acceptance clause, "lowers certified estimator work relative to the support bound", therefore cannot be met. E11's own "On failure" branch applies: keep continuous moments as conditional evidence and continue with the rigorous bounded estimator.
6. **Recommendation.** Do not spend a scope on U5 for estimator purposes. If E11's "digital moment transfer" item must be closed formally, piggyback R1-direct on U2's m certificate at near-zero marginal cost. A peer must accept the non-Minkowski transfer against ESTIMATION.md's wording (O3). Record the result as "transferred, not advancing".

## 1. Assumptions

| # | Assumption | Source |
|---|---|---|
| A1 | Contract and law as in U3 §1 (A1, A2). | `barrier_fast_classical.py`; E17 |
| A2 | Continuous support: 0 ≤ f < 40d. On survival A < 140; at H = 140 > K, f ≤ d(H−K). | `docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md` para 3; #42 run002 "payoff < 40" |
| A3 | Digital support, all inputs: g ∈ [0, 42680645928225·2^−40], independently audited. | `results/limitation_program_20261001/E03_support_run001/summary.json` `/cases/0/payoff_raw_bounds`; `E03_support_audit_run002/summary.json` |
| A4 | f is #42's ideal Y and g is #42's Y_N in law. **Open** (U3 O1/O2, U2 O2). | — |
| A5 | #43 per own profile: E\|Y_N − Y\| ≤ L1 and E[(Y_N − Y)²] ≤ L2SQ (RMS = outward sqrt128). Conditional on the passed #42 all12 criterion. | #43 profile JSONs; ROOT 87d7dec3… |
| A6 | The Hadamard planner consumes a raw second-moment upper bound S, with radius sqrt(S) centred at 0. | `estimator_hadamard.py` `intervals` (radius = root_upper(moment)) |

## 2. Routes

**R0 (saved fallback).**
- E f² ≤ M² = 1600·e^{−3/50}, and Var f ≤ M²/4 = 400·e^{−3/50} (E17 support with Popoviciu).
- Digital: E g² ≤ M_g² ≈ 1506.8232536 and Var g ≤ M_g²/4 ≈ 376.7058134. These are exact readings of the saved rational.

**R1 (support × mean; Bhatia–Davis).** For 0 ≤ f ≤ M:
- f² ≤ M·f, so E f² ≤ M·E f ≤ M·m_up.
- Var f = E f² − μ² ≤ (M − μ)·μ. On μ ∈ [0, m_up], the maximum is m_up(M − m_up) if m_up ≤ M/2, and M²/4 otherwise.
- With U3's lower bound as well: Var f ≤ min{ m_up(M − m_up), M·m_up − m_low² }.
- Inputs: one price upper bound m_up. U2's certificate route, e.g. m_up = d·min(40, T(K)) with U3's tail tiers T1–T3 at k = K, needs Φ and exp only.
- **Floor:** R1 ≥ M × (true price). That is ≈137 USD² by uncertified orientation (38.818 × 3.5189). Truth itself is plausibly far lower; any valid bound sits above the true E f².

**R2 (E10-type AM–GM control, barrier dropped).**
- f ≤ d(A−K)^+ ≤ d[(A−G) + (G−K)^+], because A ≥ G and the positive part is 1-Lipschitz and monotone. Minkowski then gives

      sqrt(E f²) ≤ d·[ sqrt(E(A−G)²) + sqrt(E((G−K)^+)²) ].

- **E(A−G)² = E A² − 2E[AG] + E G².** These are exponential sums with exact constant exponents. With spot² factored out there are 117 distinct exponents for E A², 12 for E[AG] and 1 for E G², and the maximum |exponent| is 3/20 (helper).
- **E((G−K)^+)².** It equals 100²·[e^{2δ+2v}Φ((δ+2v)/√v) − 2e^{δ+v/2}Φ((δ+v)/√v) + Φ(δ/√v)], with δ = −13/1600 and v = 143/7680. Every Φ argument is rational/sqrt(rational), and no log is needed because K = S0.
- **Floor:** R2 ≥ d²·E[((A−K)^+)²], the *vanilla* second moment. The barrier is ignored, so R2 cannot see the knock-out reduction.

**R2′ (exp-only).**
- f² ≤ d²(A−K)², so E f² ≤ d²(E A² − 200·E A + 10⁴).
- No Φ at all. It is looser, because it also counts the A < K mass.

**Combination.** The minimum of the valid upper bounds {R0, R1, R2, R2′} is valid. Var ≤ min(Bhatia–Davis, S_f − m_low²).

Plausible ranking (no evaluation): R1 versus R2 is undetermined, since both ignore different structure. R2′ is the loosest of the three. Each is far above the true E f² and far below R0's 1506.8.

## 3. E10 machinery: what can and cannot be reused

| E10 component | Reuse for B4x12 | Note |
|---|---|---|
| `RationalExpLedger` (V2 lines 1058–1118): Taylor with geometric remainder, \|x\| ≤ 8, outward dyadic rounding, fixed degree and digits | **Yes** | B4 exponents lie within \|x\| ≤ 3/20 once spot² is factored out. |
| Interval arithmetic (`interval/plus/minus/times/scale/average`, lines 947–979) | **Yes** | — |
| `moment_terms` (lines 1119–1195): E A², E AG, E G² enumeration | **Adapt** | E10 enumerates future-date families with time hulls after the exercise date. B4 needs all 12 contractual dates from t = 0, 4 assets, σ² = 9/100, ρ = 2/5, as **point** parameters. |
| Cross-sign cancellation rule (V2 repair: only for exact constant exponents) | **Yes, fully** | With point parameters every exponent is an exact constant, so grouping is allowed throughout. This is the simplest case of the V2 rule. Required precision must still be fixed a priori (80/160-digit analogue). |
| Semantic contract: source literals read as raw AST, decimal and binary64 hulls | **Pattern only** | B4's literal semantics must be fixed against #42's ideal Y (O1). This is a different source and a different hull. |
| Conditional policy theorem E[Y²] ≤ 2q²E[(A−G)²] | **No** | Specific to the C4/H8 compound parity residual under g ≤ L ≤ C ≤ U ≤ c0. Irrelevant to the B4 knock-out. |
| Certificate values 0.786189 (C4) and 118.413579 (H8) | **No** | Different contract (σ 0.2/0.4, ρ 0.2, compound). STATUS row E10 says "separate from the original B4/B8 knock-out source". |
| Five controls | **Partly** | The lognormal identity controls carry over. The elapsed-date and weakened-policy rejections do not. New controls: the Φ primitive, exactness of E[A] = (100/12)Σe^{j/400}, and E(A−G)² ≥ 0 by the explicit square-nonnegativity proof. |
| Independent audit oracle (signed scaled-Horner, 1024-bit) | **Yes** | It serves as the second implementation for the saved verifier. |
| Lifecycle and caps (180/150/600, stdlib-only, isolated 3.12.4) | **Yes** | Workload is far smaller than H8: about 130 distinct exponentials against E10's 445 endpoints. |

**Missing.** (i) A certified Φ, needed by R2 and by any m_up for R1. (ii) A certified price upper bound (U2/U1). (iii) The law-identity binding O1. E10 offers none of these.

## 4. Transfer to the digital payoff (E11 item 2)

**Direct R1 on g (recommended).** With support [0, M_g] and E g ≤ m_up + L1:
- E g² ≤ M_g·(m_up + L1);
- Var g ≤ (m_up + L1)(M_g − m_up − L1), when m_up + L1 ≤ M_g/2 = 42680645928225·2^−41 ≈ 19.4089107.

It needs no continuous second moment and no L2 bridge.

**Minkowski (literal ESTIMATION.md route).**
- sqrt(E g²) ≤ sqrt(S_f) + RMS, and sd(g) ≤ sd(f) + RMS, because centring cannot increase ‖g − f‖₂.
- Against the fallback: Var g < M_g²/4 iff sd(f) < M_g/2 − RMS ≈ 18.134 (re-verifies PLAN_43 §2(c)).
- For an R1-type S_f = M·m_up, Minkowski gives M·m_up + 2·RMS·sqrt(M·m_up) + L2SQ. This exceeds the direct M_g(m_up + L1), since M_g ≤ M and 2·RMS·sqrt(M·m_up) ≫ M_g·L1 for any m_up ≥ L1. **So the direct route dominates whenever an m_up exists.**
- Minkowski is needed only for an R2/R2′-type S_f that comes without a mean bound.

**Wording check (ESTIMATION.md, E11 acceptance).** "Minkowski uses a proved L2 b, not merely an L1 price-error allowance" forbids putting L1 *into Minkowski*. The direct route does not use Minkowski. It uses E g ≤ E f + E|g − f| together with the digital support, both proved. A reviewer must still accept that this satisfies the item's intent (O3).

## 5. Does any U5 bound matter for estimator cost? (given U2)

- **Bounded AE (E07, U2 halved, U2 support-tight).** The error formula is span·(π/M + π²/M²), or U2's 2π·sqrt(m(64 − m))/M + 64π²/M². Its inputs are the span and the mean bound only. A variance or second moment of g cannot enter, because the amplitude Bernoulli variance a(1−a) is fixed by the mean. **No effect.**
- **Hadamard / Kothari–O'Donnell planner.** Cost ≈ K_H·sqrt(S)/e. Against the bounded schedule this needs S < S\* ≈ 0.3–0.9 USD² (PLAN_43 §2(b), unsaved; U3 O3).
  - Every legal S ≥ E g² ≥ (E g)². That is ≈12.4 by uncertified orientation, a factor ≥ 13 above S\*. It is rigorous once U3's m_g² ≥ S\* holds.
  - Against U2's cheaper schedules S\* only falls.
  - **No effect, and none possible from any valid moment certificate.**
- **Centred / variance-consuming estimators.** None exists in the repository. If one were added, a Var(g) *upper* bound from U5 would be its input. Its break-even would still face Var g ≥ (E g)²·P(g=0)/P(g>0) (U3 §6). Not assessed; out of scope.
- **Outside E11.** A certified Var f could tighten a certified *classical* Monte Carlo comparator's sample count (Bernstein-type, n ∝ Var/ε² plus range terms). That helps the classical side, not the quantum one. It is noted for completeness and is not part of this route.

## 6. Premises (SHA256 recomputed 2026-10-10)

| Premise | Path | SHA256 |
|---|---|---|
| #43 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md` | 512e879c42b206b0d79897850b39d3fcc167cc0e7188abf901bbdfa6ed639b04 |
| #43 ROOT receipt | `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json` | 87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7 |
| #43 manifest | `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/manifest.json` | 2f3162d8647888e424a01caadc0eff70cb481167a291a23462789eff380fa3f9 |
| #43 profiles (`/payoff_L1_upper`, `/payoff_RMS_sqrt128_upper`, `/payoff_squared_L2_upper_L2SQ`) | `.../primary_...json`; `.../independent_...json` | c488f82b5fe04f578b33f2a060b99e6da387263b0da49cb2651691f1a23d32d6; 663e25dd2fc990185400972b7f1c3be0fe04cb87a780dd7adfd35e2b61584910 |
| #42 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md` | c43d0f35483491de3b3057c0803ac24011767f57b9fb40e63e902d82ec4cdc90 |
| #42 run002 (payoff < 40) | `.context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run002.md` | 04b491906b3dfadfb790fee41f7bca8dfc98991a7929770c785ad1ced3c0cc59 |
| E03 digital support and audit | `results/limitation_program_20261001/E03_support_run001/summary.json`; `E03_support_audit_run002/summary.json` | bb114ee72a837cd379987b73b9d40b7c3b9ebf6129340598cffd2551ca1c9524; 43209c88565a1281f4c643b075add354078c3511a33ef0fa9caa08688b83cd47 |
| E17 continuous support | `docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md` | 8427a39204ff66474dde1f4fc2dc010b714548f506cc9b37a177707fcd9f0ca6 |
| E10 results, summary, manifest | `docs/limitation_program_20261001/E10_CONTINUOUS_MOMENT_RESULTS.md`; `results/.../E10_continuous_moment_only_run002/summary.json`; `.../manifest.json` | 800750b3dbe013e499899f5b108c95e58b2f9b9f78b51b4bc1d67e863fcc7fd9; 02067de21cb64848ddb75c50efc1e5fca5938b95b4eb147474bb8e1cb9b8f66c; 16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668 |
| E10 V2 source and preflight | `research/limitation_program_20261001/experiment_e10_continuous_moment_only_v2.py`; `E10_CONTINUOUS_MOMENT_ONLY_PREFLIGHT_V2.md` | 087d56a6c5847a50ba889e1743e4dbb49a7458e8d2e9347042596d1af8a49161; 6eae176f59e6d400ebd56db325403d857ccd5141f2e875b25bc66b43dc41d2f9 |
| STATUS (E10 row: C4/H8 only) | `docs/limitation_program_20261001/STATUS.md` | 0e8dbe484afe274c7a723dc8a823c4eaa520198364950c158a69745bedf22d88 |
| E11 plan and acceptance | `docs/limitation_audit_20261001/implementation_plan/ESTIMATION.md` (E11 section) | 146b515c8c10a12574798b2354b43368e4dbfdf7a7591aa931c816a1502216a4 |
| E07 bounded schedule | `results/limitation_program_20261001/E07_schedule_run001/schedule.json` | 4fdd33add8e18f83680bcda21f38fb0bb67cc1017323717b89a52165cb59b335 |
| Hadamard planner | `research/controlled_priority_completion/estimator_hadamard.py` | 70c4cc7ce22718fdf65d326ba1b7e70d712afcc730df5707c25bf6ee05267776 |
| Contract parameters | `.context/advantage_frontier_replay/research/advantage_frontier_20260923/barrier_fast_classical.py` | 18611d7db2f896516f7aed2e67be988beafba0ef54f3bfb395c88447104c5472 |
| Orientation price (uncertified) | `results/frontier_classical_20261001/c1/c1_summary.json` | 5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123 |
| Four targets | `.context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json`; `manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md` | de6d09fe50db48939e335d2a9aa4db112a3371a12d66fa7177b76bf5eae10e25; b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637 |
| Parallel U2 (m\* thresholds, O2) | `docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md` | 6a4d5996753da15bfff6b150847dfac177e4bdf4b0095facd05bcdfaa6a2ef10 |
| Parallel U3 | `docs/parallel_E11_unblock_20261010/U3_PRICE_LOWER_BOUND.md` | (sibling note, same session) |
| Session notes (re-verified) | scratchpad `wf1/PLAN_43.md`; `wf1/moment_estimator_inventory.json` | 3d44ee1ddb19dcb23bc3418b2a9cc96b49014dc69b0e59c01b1f3f5859f3d405; e3712e9b164a86ce0086f4b4c070c512e724d797ff851ad5c2a75ce8ed8b5b29 |

Re-verification of the session notes:
- The inventory's fallback numbers (1506.8232536 and 376.7058) match the exact E03 rational.
- Its "MC E f² ≈ 44.47, Var ≈ 32.09" is a session-scratch Monte Carlo. It is not in the repository, is uncertified, and is not used as a premise here.
- PLAN_43 §2(c)'s thresholds 18.134 (Minkowski sd) and 374.95 (event-split variance) are consistent with §4 above. The event-split figure needs the C_J ≥ 2E_s check, as PLAN_43 notes.

## 7. Open obligations

- **O1 (law identity).** f must be #42's ideal Y (parameter semantics, clamp, covariance factor), and g must be Y_N in law (node and Hadamard input law). Shared with U3 O1/O2 and U2 O2.
- **O2 (price upper bound).** R1 needs a certified m_up. That is U2's/U1's certificate, with its own lifecycle.
- **O3 (acceptance wording).** A reviewer decision on whether the direct support × mean transfer satisfies ESTIMATION.md's E11 item. Otherwise use Minkowski with RMS on an R2-type S_f.
- **O4 (Φ primitive).** Shared with U3 O5; required for R2 and for most m_up routes.
- **O5 (fixed precision).** If R2/R2′ is pursued, fix the digits and degrees a priori and keep the explicit nonnegativity proof for E(A−G)² ≥ 0, as in E10 V2.
- **O6 (decision record).** Record in E11 that the estimator-cost acceptance clause cannot be met by any valid moment certificate. This is rigorous after U3 and an orientation fact before it. E11's "On failure" branch then governs.
- **O7 (lifecycle).** Any evaluation is a new scope beyond #43 and needs explicit user authorization.

## 8. Non-claims

This note is a design. It contains:
- no evaluated second moment, variance or price bound;
- no measured bias;
- no accuracy policy;
- no estimator saving (the note argues none is possible from moments);
- no confidence or runtime claim;
- no G2 promotion;
- no physical delivery;
- no quantum advantage;
- no fixture or 110-item credit.

The E10 C4/H8 bounds are not B4x12 bounds. Orientation values (3.5189 price, ≈12.4 squared-price floor, ≈137 R1 floor) are uncertified. E11 stays partial.
