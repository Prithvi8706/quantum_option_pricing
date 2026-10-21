# U1: certified continuous B4x12 price upper bound (design prospectus)

Status: **design only.** Nothing here is a saved, reviewed or verified artifact. No controller, launcher, verifier or reporter was run, and no SCI was performed. The program remains at `USER_REQUESTED_STOP_CHECKPOINT` after scope #43, and nothing beyond #43 is authorized. Nothing under `.context/`, `results/limitation_program_20261001/`, `docs/limitation_program_20261001/` or `docs/limitation_audit_20261001/` was written. No candidate bound was evaluated numerically. Section 6 gives only leading-order screening magnitudes, labelled as such, to answer the plausibility question.

Written by a parallel workflow subagent on 2026-10-10. This page is not a review receipt and gives no independent approval.

Files in this design:
- this page;
- `research/parallel_E11_unblock_20261010/U1/u1_symbolic_terms.py` (SHA256 `70b5ab24e2b04c0ebabed11fb3a5b18c1e5edfb2cb694b29c542267fc663f28b`), a symbolic helper;
- its output `research/parallel_E11_unblock_20261010/U1/u1_symbolic_terms_run001.json` (SHA256 `3966bcc46abb2ef75e889aaa11914a18cdf934f182a4a14ba8e006674021b476`). The output records 49 exact checks, all true. The helper ran under system CPython 3.9.13 with `-I -S -B` and the standard library only. It is design metadata, not a pinned-environment artifact.

---

## 0. Answer first

- **Recommended route: R7, the second-moment (Lo/Scarf) bound on the unbarriered arithmetic basket Asian call.** It needs nothing beyond `exp` of exact rationals and one outward square root. Every exponent is an integer multiple of 1/2000, so the bound is a closed form in the single transcendental q = e^{1/2000}:

  ```
  E[Y] <= m_f := (d/2) * ( beta + sqrt(V + beta^2) ),   d = q^-60
  beta = E[A] - 100 = (100/12) * sum_{j=1..12} (q^{5j} - 1)
  V    = Var(A)     = (100^2/144) * sum_{j,l=1..12} q^{5(j+l)} * [ (1/4)(q^{15 min(j,l)} - 1) + (3/4)(q^{6 min(j,l)} - 1) ]
  ```

- **Plausibility verdict: yes, with a comfortable margin.**
  - The condition is m_f + L1 <= m* at ε=1/100, with L1 = 0.045202052 and m* = 10.242691369. Equivalently, m_f <= ~10.1975 USD.
  - A leading-order screen puts R7 at about 7.5 to 8.2 USD (not a bound; see section 6).
  - The vanilla-domination route R1 screens at about 9.0 USD. It also plausibly passes, with a thinner margin, and needs normal-CDF enclosures.
- **What no barrier-free route can do.** No barrier-free upper bound can plausibly reach the ε=3/100 threshold (~5.22) or reliably reach the ε=1/1000 threshold (~6.04). Every such bound is at least the unbarriered Asian price, which screens at about 6. Those targets need a barrier-aware route (section 3, R5).
- **Upside if U1 succeeds.** It supplies one input to a future mean-aware bounded-AE schedule at ε=1/100: at most 2x fewer calls (983,025 → 491,505). It is not itself an estimator saving.

---

## 1. Contract (original B4x12 parameters)

| Item | Value | Source |
|---|---|---|
| Assets / dates | 4 / 12, t_j = j/12, j=1..12, maturity T=1 | `G0_run003/B4x12_task.json` `/assets`, `/dates`, `/observation_times`, `/maturity_years` |
| Spots | S_i(0) = 100 each (initial basket $100) | `/spot_each_asset_dollars`, `/notional_semantics` |
| Volatility | σ = 3/10 each | `/annual_volatility_each_asset` |
| Correlation | equicorrelation ρ = 2/5 between Brownian drivers | `/equicorrelation` (the field `/equity_covariance_matrix` is the correlation matrix) |
| Rate / drift | r = 3/100, risk-neutral log drift μ = r − σ²/2 = −3/200 | `/annual_rate`; `barrier_oracle_depth.py` line 77 `(RATE - .5*SIGMA**2)*dt` |
| Weights | A = (1/48) Σ_{i,j} S_i(t_j); basket B_j = (1/4) Σ_i S_i(t_j) | `/payoff`; `barrier_oracle_depth.py` lines 85, 87 |
| Strike | K = 100 | `/strike_dollars` |
| Barrier | H = 140, strict: alive iff max_j B_j < 140, equality knocks out | `/barrier_equality`; line 86 `g.lt(..., H)` |
| Discount | d = exp(−3/100), applied once, no extra notional | `/discount`, line 88 |
| Ideal law | S_i(t_j) = 100 exp(μ t_j + σ(√ρ W_0(t_j) + √(1−ρ) W_i(t_j))) with independent standard BMs W_0..W_4, i.e. 12 common and 48 idiosyncratic iid N(0,1) increments with exact decimal constants | `/model`, `/continuous_sampling`; #42 run001.md lines 109–112 (exact contractual squares 3/1000 and 9/2000, verified by helper checks) |

Ideal payoff: Y = d·(A − 100)^+ · 1{max_j B_j < 140}. This is the Y of #42/#43.

The helper derives and checks exactly:
- μ = −3/200 and the per-date drift −1/800;
- the per-date common variance a² = σ²ρ/12 = 3/1000 and the idiosyncratic variance b² = σ²(1−ρ)/12 = 9/2000, matching the #42 premise;
- S0 = K;
- the R1 coefficients d1 = √t/4 and d2 = −√t/20;
- integrality of every exponent in units of 1/2000: r·t_j = 5j, σ²t_m = 15m, σ²ρ·t_m = 6m, r·T = 60.

## 2. What U1 must deliver (the target condition)

The estimator reads the digital amplitude a = E[g]/64, where g is the native, already-discounted payoff node under the finite input law; that is the E02 binding, see U2 note O2. #43 gives, per own profile π ∈ {primary90, independent130} and conditional on the #42 criterion (which passed):

```
E[Y_N] <= E[Y] + E|Y_N - Y| <= m_f + L1_pi,     L1_pi = saved exact /payoff_L1_upper  (display 0.045202052)
```

The saved schedule (E07: ε=1/100, δ=9/2000, span 64, M=65536, 15 repetitions) uses the worst case sqrt(a(1−a)) <= 1/2. With BHMT Theorem 12 (k=1), a mean-aware schedule at M' = 32768 meets δ iff

```
e(m, M') = 2*pi*sqrt(m*(64-m))/M' + 64*pi^2/M'^2 + 2^-39  <=  9/2000,     m = m_f + L1_pi <= 32.
```

- The 2^-39 term is the E02 readout allowance quoted by the parallel U2 note.
- The helper independently re-derived the inward threshold from the saved Machin π enclosure: **m\* >= 10.242691369 USD** (floor at 1e-9). Without the readout term it is 10.242691380. This agrees with the U2 note's 10.242691368 to within 1e-9.
- So U1 succeeds for this purpose iff a certified **m_f <= m\* − L1 ≈ 10.197489** USD for each profile separately.
- Repetitions do not depend on a. Calls would be 15·(32768 − 1) = 491,505.

The same formula at the unsaved baselines for the other targets needs m_f <= ~19.1146 (ε=1/10), ~5.2223 (3/100) and ~6.0410 (1/1000). These figures come from the U2 note and are not preregistered schedules.

## 3. Candidate routes (symbolic comparison)

All routes start from the pointwise inequality **Y <= d·(A − 100)^+**. It holds because 1{survival} <= 1 and (A−100)^+ >= 0.

| Route | Statement | Transcendentals to enclose | Uses barrier? | Looseness (qualitative) | Could meet 10.1975? | Could meet 5.22 / 6.04? |
|---|---|---|---|---|---|---|
| **R0 cap** | On survival A <= max_j B_j < 140, so Y < 40d·1{A>100, alive}. Hence E Y <= 40d·P(A>100, alive) | a probability of a non-Gaussian event (no closed form) | yes | Needs P <= 0.263. P(A>100) >= P(G>100) with G the geometric mean (lognormal, median ≈ 100·e^{−13/1600}), so P(A>100) is close to 1/2. Survival removes only the upper tail, so a certified P <= 0.263 is not credible | **no (reject)** | no |
| **R1 vanilla domination** | Convexity of x ↦ (x−100)^+ with weights 1/48: (A−100)^+ <= (1/48) Σ_{i,j} (S_i(t_j) − 100)^+. With identical marginals, E Y <= (1/12) Σ_j [100 q^{5j−60} N(√(j/12)/4) − 100 q^{−60} N(−√(j/12)/20)] | q, N(x) for 24 arguments, √(j/12), π (for 1/√(2π)) | no | Ignores basket diversification (ρ=2/5) and time averaging. Volatility term ∝ (1/√(2π))·(1/12)Σ√(j/12) | **plausibly yes, thin margin (screen ≈ 9.0)** | no |
| **R2 comonotonic split** | For any fixed K_j with (1/12)ΣK_j = 100: (A−100)^+ <= (1/48)Σ_{i,j}(S_i(t_j) − K_j)^+ | as R1, plus fixing K_j | no | Improves R1 only to second order near the money; the optimal K_j needs root finding | yes (≈ R1) | no |
| **R7 second moment (Lo/Scarf)** | E X^+ = ½(E X + E\|X\|) <= ½(E X + sqrt(E X²)) with X = A − 100 | q only, plus one sqrt | no | Captures diversification and averaging exactly through Var(A). Pays the Scarf factor ½ vs φ(0) ≈ 0.399 on the s.d. Leading-order volatility-term ratio R7/R1 = [½·sqrt((ρ + (1−ρ)/4)·650/1728)] / [(1/√(2π))·(1/12)Σ_j √(j/12)] < 1 (screen ≈ 0.81) | **plausibly yes, wide margin (screen ≈ 7.5–8.2)** | no |
| **R3 conditioning (Rogers–Shi / Curran-type)** | E(A−K)^+ <= E[(E[A\|Λ] − K)^+] + ½E[sqrt(Var(A\|Λ))] with a scalar Gaussian Λ | certified 1-D quadrature of lognormal conditional moments | no | Close to the unbarriered Asian price (screen ≈ 6) | yes, but costly | no / borderline |
| **R5 barrier-aware (future)** | For example upper-bound survival via AM ≥ GM: 1{max_j B_j < 140} <= 1{max_j G_j < 140}, with G_j the date-j geometric basket, then a joint Gaussian computation | multivariate Gaussian or lognormal integrals | yes | Only family that can approach the knock-out price (uncertified RQMC 3.5189) | yes | possibly; open research |

**Why any barrier-free route stops near 6.** All of R1, R2, R3 and R7 bound d·E(A−100)^+, which is itself an upper bound and not the knock-out price. A leading-order Gaussian proxy of the unbarriered Asian puts d·E(A−100)^+ near d·(φ(0)·sd(A) + β/2), about 6. So the 3/100 target is out of reach for these routes, and 1/1000 (6.04) is at best borderline even for an exact unbarriered price.

**Rejected refinements.**
- Call-spread subtraction: Y <= d[(A−100)^+ − (A−140)^+] with E(A−140)^+ >= E(G−140)^+ from AM ≥ GM. G is lognormal with log s.d. sqrt(σ²(ρ + (1−ρ)/4)·325/864) ≈ 0.14, so 140 lies about 2.4 s.d. above, and the gain is O(10^-2) USD. Not worth a field.
- Capping R7 at 40 using mean and variance only: gain is negligible because 40 is about 3 s.d. away.

## 4. Proofs

### 4.1 Common step

Y >= 0 and Y = d(A−100)^+·1_alive <= d(A−100)^+ pointwise. Every quantity is integrable: lognormals have all moments. Hence E Y <= d·E(A−100)^+.

### 4.2 R7 (recommended)

Let X = A − 100.
1. Use X^+ = (X + |X|)/2.
2. By Cauchy–Schwarz (or Jensen), E|X| <= sqrt(E X²).
3. Therefore E X^+ <= ½(E X + sqrt(E X²)).
4. Write β = E X and V = Var A. Then E X² = V + β².

Moments of the ideal law:
- E S_i(t_j) = 100 e^{r t_j}.
- E[S_i(t_j) S_k(t_l)] = 100² exp(r(t_j + t_l) + σ² c_ik min(t_j, t_l)), where c_ii = 1 and c_ik = ρ for i ≠ k. This holds because the log is Gaussian with Var = σ²(t_j + t_l + 2c_ik min).

Hence, with q = e^{1/2000}:
- β = (100/12) Σ_j (q^{5j} − 1).
- V = (1/48²) Σ Cov = (100²/144) Σ_{j,l} q^{5(j+l)} [¼(q^{15m} − 1) + ¾(q^{6m} − 1)], with m = min(j, l). Of the 16 ordered asset pairs, 4 have c = 1 and 12 have c = ρ.

The helper checks this grouped polynomial (119 monomials) for exact equality against an independent 48×48 brute-force covariance sum (2,304 terms, no grouping). It also checks β(1) = V(1) = 0 and Σ_{j,l} min(j,l) = 650.

Conclusion: **E Y <= (d/2)(β + sqrt(V + β²)) with d = q^{−60}.**

### 4.3 R1 (documented alternative)

1. Convexity with weights 1/48 gives E(A−100)^+ <= (1/48) Σ E(S_i(t_j) − 100)^+.
2. Black–Scholes under the exact lognormal law gives E(S(t) − 100)^+ = 100[e^{rt} N(d1) − N(d2)] with d1 = (r + σ²/2)√t/σ = √t/4 and d2 = (r − σ²/2)√t/σ = −√t/20, since S0 = K.
3. The four assets are identical in law.

A note on monotonicity: (S_t − 100)^+ is a submartingale when r >= 0, so each term is at most the t=1 term. This orders the terms but is not used in the bound.

### 4.4 Outward exact-rational evaluation (fixed recipe for R7)

Every component below is monotone in the right direction, so each enclosure gives a valid upper bound.

| Quantity | Enclosure |
|---|---|
| q_lo, q_hi | x = 1/2000, N = 10. q_lo = Σ_{k<=10} x^k/k! (positive terms, so q_lo <= q). q_hi = q_lo + 2x^{11}/11! (Lagrange remainder with e^x <= 2). Both are exact rationals |
| Powers | Positive powers of q_hi by repeated multiplication. After each product, round **up** onto the 2^-192 grid |
| Structured terms | Each term coef·q^{base}(q^{e} − 1) has coef > 0 and e > 0, so it is increasing in q >= 1. Evaluate at q_hi to get V_up and β_up |
| Discount | d_up = 1 / (q_lo^60 rounded down on 2^-192). Since q_lo^60 <= e^{3/100}, d_up >= e^{−3/100} |
| Square root | s_up = (isqrt(floor((V_up + β_up²)·4^128)) + 1)/2^128, with the exact check s_up² >= V_up + β_up² |
| Result | m_f_up = d_up·(β_up + s_up)/2 as an exact rational, plus an outward 1e-9 display (round up) |

Expected sizes: denominators of a few hundred bits, about 300 multiplications. That is far below the 131072-bit frontier and well under 1 s of CPU time.

## 5. Second-moment byproduct (PLAN_43 "certified continuous second moment", premise P11)

The same arithmetic gives, at no extra cost:

```
E[Y^2] <= d^2 * E[((A-100)^+)^2] <= d^2 * E[(A-100)^2] = d^2 * (V + beta^2)
```

Var Y <= E Y² as well. This would be the first certified continuous B4x12 second moment. E10 covers only C4/H8 (STATUS row E10).

The screen suggests about 180–190 USD². That is below the 374.95 threshold at which a direct variance transfer beats the E03 bounded-payoff fallback (PLAN_43 §2(c)), so it could unblock the "digital moment transfer" item.

It still gives **no estimator gain**: the Hadamard planner needs S of about 0.6 USD², and any valid S is at least (E g)² ≈ 12.4.

Recommendation: preregister it as an optional informational field in the same scope. It is never consumed by a schedule.

## 6. Plausibility decision (screening only; these are not bounds)

The helper emits the exact first-order coefficients in x = ln q: β₁ = 13/8 and V₁ = 17875/96 = 100²σ²(¼ + ¾ρ)·650/1728. These are pure constants. They are labelled screen-only and are not operands of any certificate.

- **R7 leading order:** ½(13/8 + sqrt(17875/96 + (13/8)²)) ≈ 7.68 undiscounted, about 7.46 after d ≈ 0.970.
  - Every higher-order Taylor term of V and β is positive, so the true R7 value is larger than the screen.
  - All exponents are at most 300 units (0.15). The higher-order terms therefore raise V by a few percent (5% is a reasonable guess), and the square root by about half that.
  - Screening range for R7: about 7.5–8.2 USD.
  - Against the requirement of about 10.1975 USD, the **margin is about 2 USD (20–25%)**.
- **R1 leading order:** N(x) ≈ ½ + x/√(2π) gives per-date terms of about 100(0.1197√t + 0.015t + small). The average over dates is about 9.3 undiscounted, about 9.0 discounted. **Margin about 1.2 USD.**
- **Context:** the uncertified RQMC knock-out price is 3.5189 (`c1_summary.json /port_check/B4x12/price`). R7 is expected to over-estimate the price by about 2.1x and R1 by about 2.6x. That is acceptable, because only the 10.24 level matters.
- **Decision.** U1 via R7 is plausible with high confidence at ε=1/100, and also at ε=1/10, where the threshold is about 19.11. It is implausible at 3/100 and 1/1000 for any barrier-free route.

**Caution.** These screens informed the choice of route before any certified evaluation. That is a design choice, not a post-hoc selection. To keep the preregistration non-adaptive, the route, recipe, precisions and decision rule below are fixed in advance. The scope does not fall back to R1 or R3.

## 7. Preregistrable test design (fixed; no adaptive choice)

- **Scope name (proposal):** `E11_B4X12_CONTINUOUS_PRICE_UPPER_R7`. It requires explicit user authorization, because nothing beyond #43 is authorized.
- **Fixed literals:** σ=3/10, ρ=2/5, r=3/100, T=1, S0=K=100, H=140 (recorded, not used by R7), 4 assets, t_j = j/12, weights 1/48, d = e^{−3/100}.
  - The SOURCE asserts float equality against `G0_run003/B4x12_task.json` and against `barrier_oracle_depth.py` line 33, read as plaintext or AST only.
  - It also asserts the exact squares 3/1000 and 9/2000 against the #42 run001 premise.
- **Fixed recipe:** section 4.4 exactly (N=10, power grid 2^-192, sqrt grid 2^-128, outward 1e-9 display). No alternative precision may be tried.
- **Primary field:** `continuous_price_upper_R7` = m_f_up (exact rational, limbs) plus display.
- **Decision fields, per own profile π separately, no cross-profile minimum:**
  - Inputs: L1_π = saved exact `/payoff_L1_upper` from `{primary,independent}_fixed_polar_safe_h128_payoff_squared_L2_bridge.json`, and π_hi from `E07_schedule_run001/schedule.json /pi_enclosure_exact`.
  - `mean_aware_halving_input_condition_eps_1_100` = [m = m_f_up + L1_π <= 32] AND [e(m, 32768) <= 9/2000]. Here e(m, M) is evaluated with π_hi, an outward sqrt and the 2^-39 readout.
  - Informational only (not saved schedules): the same check at the U2 baselines for ε = 1/10, 3/100, 1/1000, fixed now. Expected outcome: pass, fail, fail.
- **Optional informational field:** `continuous_second_moment_upper` = d_up²·(V_up + β_up²) (section 5).
- **Required exact checks:** q_lo < q_hi; 1 <= q_lo; every structured term positive; grouped == 48×48 brute force; s_up² >= V_up + β_up²; m_f_up > β_up·d_lo/2 (sanity); m_f_up < 40 (sanity; the payoff is < 40).
- **Fixtures** (SOURCE tests; none is a certificate):
  1. ρ=1, single asset: V reduces to the one-asset form.
  2. q=1: β = V = 0.
  3. An altered model (σ=0.2) changes the polynomial.
  4. An independent q enclosure at N=14 agrees by containment.
  5. A negative branch is forced with a threshold of 0.
  6. A Monte Carlo cross-check is allowed only as a non-gating diagnostic.
- **Independent saved verifier:** a separate author recomputes m_f_up by the 2,304-term brute force from the same fixed recipe and requires exact equality. It also re-derives the threshold check.
- **Caps:** CPU 60 s, wall 300 s, RSS 150 MiB, frontier 131072 bits. The pinned interpreter `.context/frontier_t0_env/Scripts/python.exe -I -S -B` uses the standard library only (`fractions`, `math.isqrt`). Every write uses exclusive create.
- **Failure action (fixed):**
  1. Guard or check failure: seal a negative record with every field None, `FAILED` custody, credit 0, no retry or reseal. Repair is a distinct v2 SOURCE under the same formulas.
  2. Certified m_f_up + L1_π fails the ε=1/100 condition: valid negative outcome `halving_input_condition_not_met_R7`. There is no R1/R2/R3 fallback inside this scope; any other route is a new preregistration.
  3. #42 criterion or #43 field unavailable or mismatched: decision fields None, primary field still emitted.
- **Lifecycle:** mirrors #43 (PLAN_43 §3), in this order:
  1. prospectus;
  2. operand inventory;
  3. independent prospectus peer, which must accept §4.2 and the monotonicity argument of §4.4;
  4. ROOT conditional review;
  5. SOURCE DRAFT;
  6. publication;
  7. disabled verifier;
  8. static peer;
  9. release;
  10. SCI, only after user authorization;
  11. verifier binding;
  12. FIELD peer;
  13. ROOT verification;
  14. reporter;
  15. audit.

  Independence: the FIELD peer must differ from both the SOURCE author and the checker author. This design's author must disclose authorship if it later takes any role.

## 8. Assumptions

1. **Ideal law.** The ideal Y of the #42/#43 coupling has exactly the stated GBM law with exact decimal constants. That is, the 60 ideal normals (Box–Muller of continuous uniforms) are iid N(0,1) and drive 12 common and 48 idiosyncratic increments. This is supported by #42 run001.md lines 17–19 and 109–112, and must be pinned by pointer in the prospectus.
2. **Same payoff in both bridges.** "Original parameters" means the contract in G0_run003, which is identical to the builder constants. The digital float or fixed-point constants are a native-side matter, covered by the #43 bridge and not by U1.
3. **AE error formula.** BHMT Theorem 12 with k=1, monotonicity of sqrt(a(1−a)) on [0, 1/2], and success probability >= 8/π² independent of a. These are as recorded for E07; the parallel U2 note re-derives them.
4. **Bridge scope.** The L1 bridge is conditional and per profile, as saved. U1 adds no assumption about it.

## 9. Premises (SHA256 recomputed 2026-10-10 from the working tree; read only)

| Premise | Path | SHA256 |
|---|---|---|
| Frozen contract | `results/limitation_program_20261001/G0_run003/B4x12_task.json` | `c7ac83c1019b649e46a12469cf15df1cede810539b96f18e7de313660117537f` |
| Original builder (constants line 33, drift line 77, alive line 86, payoff line 88) | `research/advantage_frontier_20260923/barrier_oracle_depth.py` | `1e0e225131c668f133ef05a5de3f78fbad4fb5307a2fc8c452d99d14c8dda929` |
| Baseline producer (builder provenance, observation times) | `research/limitation_program_20261001/baseline.py` | `9ac7e7f1375f49d78a6ead98d61314cdd9ff9a81dfaa074ad062615002816b17` |
| Classical Case defaults (cross-check only) | `research/frontier_classical_20261001/scrambles.py` | `40403b81a1b92d336bcb23a352029f2607ef859589f640e329075a597c49dc0f` |
| #42 ideal-law premises (exact squares, ideal coordinates) | `.context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run001.md` | `d673d81da8e91a3ad84db02f85f8e7d7fe5ce276ff5fcd8944747623f9530364` |
| #42 payoff < 40, discount enclosure | `.context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run002.md` | `04b491906b3dfadfb790fee41f7bca8dfc98991a7929770c785ad1ced3c0cc59` |
| #42 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md` | `c43d0f35483491de3b3057c0803ac24011767f57b9fb40e63e902d82ec4cdc90` |
| #43 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md` | `512e879c42b206b0d79897850b39d3fcc167cc0e7188abf901bbdfa6ed639b04` |
| #43 ROOT verification | `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json` | `87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7` |
| #43 manifest | `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/manifest.json` | `2f3162d8647888e424a01caadc0eff70cb481167a291a23462789eff380fa3f9` |
| #43 L1 (primary90) | `.../primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json` `/payoff_L1_upper` | `c488f82b5fe04f578b33f2a060b99e6da387263b0da49cb2651691f1a23d32d6` |
| #43 L1 (independent130) | `.../independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json` `/payoff_L1_upper` | `663e25dd2fc990185400972b7f1c3be0fe04cb87a780dd7adfd35e2b61584910` |
| Saved B4 schedule (π enclosure, δ, M, span) | `results/limitation_program_20261001/E07_schedule_run001/schedule.json` | `4fdd33add8e18f83680bcda21f38fb0bb67cc1017323717b89a52165cb59b335` |
| E02 ledger (readout 2^-39, amplitude law; cited via U2) | `results/limitation_program_20261001/E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json` | `d2eb29c7c92d6eda32879e5e040a8e5280432fa42417f7c60c1d2ac2db3ba405` |
| Four targets and bias budgets | `.context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json` `/four_original_targets_dollars`, `/bias_budgets_dollars` | `de6d09fe50db48939e335d2a9aa4db112a3371a12d66fa7177b76bf5eae10e25` |
| Why-no-advantage | `manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md` (it is not under `docs/limitation_program_20261001/`) | `b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637` |
| No certified B4x12 continuous moment (row E10) | `docs/limitation_program_20261001/STATUS.md`; `docs/limitation_program_20261001/E10_CONTINUOUS_MOMENT_RESULTS.md` | `0e8dbe484afe274c7a723dc8a823c4eaa520198364950c158a69745bedf22d88`; `800750b3dbe013e499899f5b108c95e58b2f9b9f78b51b4bc1d67e863fcc7fd9` |
| Joint law (first-date log variance 3/1000) | `docs/limitation_program_20261001/FINANCIAL_LAW_RESULTS.md` | `96dd78f8c275bfdfa79b89b23d0aff93556407732c1c668c04763a6b83366b90` |
| Uncertified RQMC price 3.5189 (orientation only) | `results/frontier_classical_20261001/c1/c1_summary.json` | `5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123` |
| Earlier design notes (re-verified, not trusted) | scratchpad `wf1/PLAN_43.md`; `wf1/moment_estimator_inventory.json` | `3d44ee1ddb19dcb23bc3418b2a9cc96b49014dc69b0e59c01b1f3f5859f3d405`; `e3712e9b164a86ce0086f4b4c070c512e724d797ff851ad5c2a75ce8ed8b5b29` |
| Parallel U2 note (unreviewed; threshold cross-checked) | `docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md` | `6a4d5996753da15bfff6b150847dfac177e4bdf4b0095facd05bcdfaa6a2ef10` |

Re-verification of the earlier notes:
- PLAN_43 §2(a) states thresholds "19.16, 5.27, 10.24, 6.09". The 10.24 figure is confirmed as a sufficient rounding (exact inward value 10.242691369). Per U2, the other three round upward and are not sufficient as stated.
- The 491,505 call count is confirmed.
- The inventory's statement that the estimator consumes only the span is consistent with `schedule.json /finite_error_formula`.

## 10. Open obligations

1. **O1 Ideal-law pin.** The prospectus must pin, by pointer, that the #42/#43 ideal Y has exactly the section 1 GBM law with exact decimal constants (run001 lines 17–19, 109–112). The peer must accept this pin.
2. **O2 Amplitude binding** (shared with U2 O2). Y_N (node 5697) must be the E02 comparator input, and the coupling marginal must equal the finite Hadamard input law. Otherwise m_f + L1 does not bound a.
3. **O3 Proof review.** An independent peer and ROOT must accept §4.2, including the 4/12 multiplicity grouping (machine-checked here only by the design helper), and the monotone outward recipe of §4.4.
4. **O4 Authorization.** The user must authorize both metadata work and SCI beyond #43.
5. **O5 Downstream.** A mean-aware schedule scope is needed:
   - a new `certified_schedule` variant at M=32768 (15-bit QPE);
   - IQFT rotation coverage (U2 reports this is already certified at ε=1/100);
   - an E07/E02 ledger and wrapper binding.

   U1 alone changes no estimator.
6. **O6 (optional).** A barrier-aware route (R5) is required before 3/100 or 1/1000 can be addressed. It is open research.
7. **O7 Helper metadata.** The helper ran under system Python 3.9. A preregistered SOURCE must run under the pinned 3.12.4 environment.

## 11. Non-claims

This page claims no certified price bound: no R1 or R7 value was evaluated, and the screens are not bounds. It also claims none of the following:
- a measured bias or price accuracy;
- an accuracy policy;
- an estimator, call or runtime saving;
- a schedule change;
- a moment or variance transfer;
- G2 progress;
- physical delivery;
- quantum advantage.

The bounds proposed here are upper bounds on the continuous price. They are not estimates of it. A passing future result would only supply an input that permits, but does not perform, a 2x shorter bounded-AE schedule at ε=1/100. E11 stays partial, and the 110-category ledger and all credits are unchanged.
