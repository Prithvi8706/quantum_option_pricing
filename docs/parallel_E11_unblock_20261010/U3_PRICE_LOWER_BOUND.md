# U3: certified lower bound on the B4x12 price (design prospectus only)

Status: design only, written 2026-10-10. Nothing here is a saved, reviewed or verified artifact. No controller, launcher, verifier or reporter was run. Nothing under `.context/`, `results/limitation_program_20261001/` or `docs/limitation_program_20261001/` was written. **No new scientific bound was evaluated**: no exp, log, Φ, price, probability or moment value of the proposed route exists. The only computations are exact rational law constants (pure-constant identities) and SHA256 pins, made by `research/parallel_E11_unblock_20261010/U3_U5/u3_u5_pure_constants.py`. Its output is `u3_u5_pure_constants_run001.json` (SHA256 `1640869cf17c4c545c4eaaf5cc5d8a1cd7b7210566ac6244dcedf9d3fbabfa0d`). The program remains at `USER_REQUESTED_STOP_CHECKPOINT` after scope #43. Any evaluation of this route is a new scope and needs explicit user authorization.

---

## 0. Answer in brief

1. **What U3 is for.** The verdict "a moment-consuming (Hadamard / Kothari–O'Donnell) estimator cannot beat bounded AE on B4" currently rests on the *uncertified* RQMC price 3.5189. U3 makes it rigorous through one chain of inequalities. Any valid certificate S ≥ E[g²] satisfies

   S ≥ E[g²] ≥ (E g)² ≥ (m_f − L1)²

   so it suffices that **(m_f − L1)² > S\***. Here m_f is a certified lower bound on the continuous price, L1 is the #43 conditional bridge E|Y_N − Y| ≤ 0.045202052, and S\* is the planner's break-even moment against the bounded schedule. Against the saved E07 schedule, PLAN_43 §2(b) puts S\* at about 0.3–0.9 USD² across the four targets (≈0.6 at ε = 1/100). This is a workflow evaluation, not a saved schedule. The ~0.95 USD target is sqrt(0.9) ≈ 0.949. A cheaper bounded schedule (U2's halved or support-tight wrapper) lowers S\*, so a bound that clears the current S\* also clears every cheaper comparator.
2. **Proposed route (Route B: "Curran sub-event + cap + Doob knock-out charge").** This is the task's "explicit sub-event + convexity" idea made tractable. For any event D, any cap c ≥ 0, and pointwise:

   f ≥ d·[(A−K)·1_D − (A−K−c)^+] − d·c·1_KO

   Taking expectations gives

   m_f ≥ d·{ C1(D) − T(K+c) − c·P̄_KO }

   - **C1(D)** = E[(A−K)1_D] is exact and closed form for D = {ln G > λ'} (exponential tilting).
   - **T(k)** is any certified upper bound on the vanilla tail E[(A−k)^+].
   - **P̄_KO** is a Doob maximal-inequality bound on the knock-out probability, built from the terminal discounted basket.

   Every Φ argument has the form (rational)/sqrt(rational), because K = S0 = 100 and every threshold is parametrized as 100·e^{rational}. **No logarithm oracle is needed.** The only new primitive is a certified normal-CDF enclosure. The exponential ledger can be reused from E10.
3. **How strong.** The ceiling is the true price, about 3.52 by uncertified orientation. The target is about 27% of that ceiling. The dominant loss is the knock-out charge c·P̄_KO. My assessment is **plausible but not assured** that Route B clears ~0.95 + L1.
   - The plain geometric-mean variant (Route A) is **marginal**, because it also pays the AM–GM gap at the money.
   - The decisive design choice is the basket-call upper bound inside the Doob term. A Rogers–Shi conditioning on the terminal geometric basket is exactly lognormal here (β = 1), so it needs no root finding.
   - Disclosure: to rank the routes I made an informal mental order-of-magnitude check (no code, no recorded values). It is not a result. The preregistration in §7 fixes a broad symbolic grid that does not depend on it.
4. **Limit of the verdict.** U3 covers estimators that consume the raw second moment E[g²]. `estimator_hadamard.py` sets its interval radius to sqrt(moment), centred at 0. A *centred* estimator that consumed Var(g) would need a separate certified variance lower bound. §6 sketches one; it is plausibly weak.

---

## 1. Assumptions

| # | Assumption | Source |
|---|---|---|
| A1 | Contract: 4 assets, 12 dates t_j = j/12, S0 = K = 100, H = 140, σ = 3/10, ρ = 2/5 (equicorrelated), r = 3/100, T = 1. A = mean of the 48 fixings. f = d·(A−K)^+·1{every date basket < H}, with d = e^{−3/100} and a strict barrier. | `barrier_fast_classical.py` line 39 and `setup`/`estimand`; E17 `MOMENT_PROOF_v2.md` para 1 |
| A2 | Risk-neutral GBM: ln X_{i,j} ~ N(ln100 + (r−σ²/2)t_j, σ²t_j); Cov(ln X_{i,j}, ln X_{k,l}) = σ²ρ_{ik}·min(t_j, t_l). | same `setup` (`mu`, `cov`) |
| A3 | The continuous payoff in the certificate is **the same random variable** as #42/#43's ideal Y on the #42 coupling: same law, same parameter semantics (exact decimals versus binary64 literals) and same clamp convention. **Not yet established**; see obligation O1. | `E11_B4X12_ALL48_STOCK_MATRIX_RESULTS_20261007.md` (the "exact driver mappings" and "same clamp" wording) |
| A4 | g, the estimator's digital payoff, equals the #42 coupling's Y_N in law (node 5697 and the Hadamard input law). **Open**, as U2 obligation O2 also records. | U2 §3 item 2 |
| A5 | #43 L1 per own profile: E\|Y_N − Y\| ≤ `/payoff_L1_upper`, display 0.045202052. It is conditional on the #42 all12 criterion, which passed. | #43 profile JSONs; ROOT receipt 87d7dec3… |
| A6 | Planner cost is non-decreasing in its supplied moment S, so any S ≥ m_low² costs at least the planner at m_low². **Unverified**; see obligation O4. | `estimator_hadamard.py` `intervals`, `candidate`, `optimized_plan` |

## 2. Why a lower bound settles the moment-estimator question

- Jensen's inequality gives E[g²] ≥ (E g)² for any real g. On the digital side, E g ≥ E Y − E|Y_N − Y| ≥ m_f − L1 (A3–A5).
- Any certificate the planner could legally consume is an upper bound S ≥ E[g²]. So S ≥ (m_f − L1)². Under A6, the planner cost at every legal S is at least its cost at (m_f − L1)².
- If (m_f − L1)² ≥ S\*(ε) for each target ε, then no certified raw-moment input, from any route (E10-style analytic, U5, statistical acquisition), can make the planner cheaper than the bounded schedule at that ε.
- The required m_f is **sqrt(S\*_max) + L1**. With PLAN_43's unsaved S\*_max ≈ 0.9 this is about 0.949 + 0.045 ≈ 0.994 USD.
- If the comparator is U2's halved schedule (calls ×1/2), the planner's cost ∝ sqrt(S)/e gives S\* roughly ×1/4. The required m_f then falls to about 0.47 + 0.045. These are scaling statements, not saved planner evaluations; see O3.

## 3. Route B: theorem and proof

**Pointwise lemma.** Let u = A − K, c ≥ 0, D any event, and KO = {∃ j: B_j ≥ H}. Then

    f ≥ d·[u·1_D − (u − c)^+] − d·c·1_KO.

*Proof.*
- First, min(u^+, c) = u^+ − (u − c)^+, and u^+ ≥ u·1_D. Hence min(u^+, c) ≥ u·1_D − (u − c)^+.
- On survival, f = d·u^+ ≥ d·min(u^+, c) ≥ RHS, and 1_KO = 0.
- On KO, f = 0. The bracket is at most min(u^+, c) ≤ c, so RHS ≤ 0. ∎

The helper checks this algebra on 36 hand-written cases, which are not law samples.

**Expectation.**

    m_f ≥ d·{ E[(A−K)1_D] − E[(A−K−c)^+] − c·P(KO) }.

The three terms are bounded as follows.

### C1: exact sub-event term (Curran-type)

Let Λ = ln G, where G is the geometric mean of the 48 fixings, and let D = {Λ > ln100 + κ'} with κ' rational. Tilting gives E[e^U 1{Λ>ℓ}] = E[e^U]·Φ((μ_Λ + Cov(U,Λ) − ℓ)/s_Λ). Then

    C1 = (1/48)·Σ_{i,j} 100·e^{r t_j}·Φ((−13/1600 − κ' + γ_j)/s) − 100·Φ((−13/1600 − κ')/s),

with s² = Var Λ = **143/7680**, E Λ − ln100 = **−13/1600**, and γ_j = Cov(ln X_{i,j}, Λ) = **11·j·(25−j)/64000**. The mean of γ_j equals s². All three are exact identities from the helper.

- C1 is an *exact* value for each κ', not a bound. Every κ' gives a valid lower bound, and the maximum over κ' approaches E[(A−K)^+] up to the Curran conditioning gap. That gap is small for Asian averages; this is literature knowledge, not certified here.
- Unlike Route A, C1 does **not** pay the AM–GM gap E[A] − E[G].

### C2: tail term T(k) ≥ E[(A−k)^+], with k = K + c = 100·e^{κ_c} and κ_c rational

The minimum of any valid upper bounds is valid. Three tiers:

- **T1 (comonotone / per-fixing convexity):** (1/48)·Σ forward BS calls on single fixings, each with log-moneyness κ_c (rational). Loose, because single-fixing volatility exceeds A's.
- **T2 (AM–GM):** E[A] − E[G] + E[(G−k)^+]. E[A] = (100/12)·Σ e^{j/400} and E[G] = 100·exp(−13/1600 + 143/15360) are exponentials only; the Black call on G uses Φ. Loose by the AM–GM gap.
- **T3 (Rogers–Shi):** E[(m(Λ)−k)^+] + ½·sqrt(E[A²] − E[m(Λ)²]), where m(Λ) = E[A|Λ] = Σ_l w_l·E[X_l]·exp(β_l(Λ−μ_Λ) − β_l²s²/2) and β_l = γ_l/s².
  - The variance part is a difference of exponential sums. All exponents are exact constants (117 distinct in E[A²] once spot² is factored out; maximum |exponent| 3/20, inside E10's |x| ≤ 8 domain). The E10 V2 cross-sign rule (cancellation only for exact constant exponents) therefore applies.
  - The first part needs a certified bracket for the root of m(Λ) = k. m is increasing, so use bisection with exp enclosures. Upper-bound E[(m−k)^+] on the bracket as E[(m−k)1{Λ>ℓ_lo}] + (k − m(ℓ_lo))·P(ℓ_lo < Λ ≤ ℓ_hi).

### C3: knock-out probability P̄_KO ≥ P(KO) (Doob)

- M_t = e^{−rt}·B(t) is a positive martingale.
- KO implies M_{t_j} ≥ e^{−r t_j}H ≥ e^{−rT}H =: λ, using r ≥ 0. Here λ = 140·e^{−3/100}, an exp enclosure.
- For a < λ, X_j = (M_{t_j} − a)^+ is a non-negative submartingale. Doob's inequality gives

      P(KO) ≤ P(max_j X_j ≥ λ − a) ≤ E[(M_T − a)^+]/(λ − a).

- Given only the law of M_T, this is the sharp model-free bound (Azéma–Yor / Blackwell–Dubins).
- Basket-call upper bounds for E[(B_T − k)^+], with k = a·e^{rT} = 100·e^{κ_a} and κ_a rational:
  - **K1 (per-name, comonotone):** a single-name BS call with σ = 0.3.
  - **K2 (AM–GM):** E[B_T] − E[G_B(T)] + Black(G_B).
  - **K3 (Rogers–Shi on Λ_T = ln G_B(T)):**
    - Exact constants: Var Λ_T = Cov(ln S_i(T), Λ_T) = **99/2000**, so β = 1 and E[B_T | G_B] = **G_B·e^{81/4000}**.
    - The first term is therefore an *exact Black formula with no root finding*. Its log-moneyness is κ_a − (−3/200) − 81/4000, which is rational.
    - The slack term is ½·sqrt(E[B_T²] − e^{81/2000}·E[G_B²]): sixteen exponentials, all with exact constant exponents.
- Use min(K1, K2, K3) inside the bound and then min(1, ·) on P̄_KO.

**Route A (cross-check, weaker).** Replace (A−K)1_D by (G−K)^+, and the tail by E[(G−K−c)^+]: m_f ≥ d·{Black_G(K) − Black_G(K+c) − c·P̄_KO}. This is valid because A ≥ G and min(·, c) is monotone. It pays the AM–GM gap near the money.

**Digital transfer.** E g ≥ m_f − L1_π for each own profile π, using the exact saved rational `/payoff_L1_upper`, not the display. m_f itself does not depend on the profile when d is enclosed afresh from below. If the archived own-profile discount enclosure [L, U] is used instead, the lower endpoint L is what enters.

## 4. Strength assessment (no evaluation performed)

- **Ceiling.** m_f ≤ true price. The uncertified orientation is 3.5188852 (`c1_summary.json` /port_check/B4x12/price). The target ~0.994 (m_f, including L1) leaves about 2.5 USD for all losses.
- **Losses, in plausible order of size.**
  1. The knock-out charge d·c·P̄_KO. It is unavoidable in this family, and it is linear in c.
  2. The cap loss: E[(A−K)^+] − E[min((A−K)^+, c)] would be counted in exact arithmetic, but the T(K+c) bound inflates it further.
  3. The Curran conditioning gap in C1, plausibly small.
  4. The Doob date relaxation e^{−r(T−t_j)} ≥ e^{−rT}, at most 3%.
- **Optimal cap.** The trade-off in c is d/dc C-part = P(A > K+c) against P̄_KO. The best c is where the upper tail of A falls to the knock-out bound. That is a moderate cap, not 40.
- **Sensitivity.** Every loosening of P̄_KO by Δ costs c·Δ dollars. With K1 (single-name σ) the knock-out bound inherits no diversification. K3 recovers the basket volatility and is the recommended primary.
- **Verdict.**
  - Route B with K3 and T3: plausible to clear ~0.994, not assured.
  - Route B with only K1/K2 and T1/T2: marginal.
  - Route A: marginal to insufficient.
  - The preregistered decision in §7 settles it. No result is claimed here.
- **If Route B falls short**, two tightenings are possible, each a separate preregistration:
  - (i) A sharper knock-out term that also intersects with the payoff region, P(KO ∩ {Λ > ℓ}), using the same tilt and Doob argument under the tilted measure. This needs a new proof that the tilted basket stays a submartingale. It is **not** established.
  - (ii) A certified one-dimensional quadrature of the first-principal-component preintegrated payoff. This is the `estimand` structure in `barrier_fast_classical.py`, but a 47-dimensional outer expectation remains. **Not plausible as a certificate.**

## 5. Certification machinery (reuse map)

| Primitive | Needed for | Reuse | New work |
|---|---|---|---|
| exp enclosure on exact rationals, \|x\| ≤ 8 | e^{r t_j}, d, λ, e^{κ}, moment sums | E10 V2 `RationalExpLedger` (`experiment_e10_continuous_moment_only_v2.py` lines 1058–1118): Taylor with geometric remainder and outward dyadic rounding | none (re-instantiate) |
| exact rational interval arithmetic | everything | E10 `interval/plus/minus/times/scale` (lines 947–979) | sign-aware composition for the differences in C1 and T3 |
| sqrt enclosure | s, Φ arguments, RS slack terms | `isqrt` outward/inward, as in #43 sqrt128 | trivial |
| π enclosure | 1/sqrt(2π) in Φ | E07 Machin enclosure (`schedule.json` `pi_enclosure_exact`) | none |
| **Φ enclosure** | C1, T1–T3, K1–K3 | none in the repository's certified runs | **new**: alternating Taylor series of erf with x² rational (x = p/sqrt(q), so x² = p²/q exactly), giving rigorous brackets once terms decrease. Use the Mills-ratio bounds φ(x)·x/(1+x²) ≤ 1−Φ(x) ≤ φ(x)/x for \|x\| beyond a fixed cut. Needs its own controls (Φ(0) = 1/2, symmetry, a value pinned by an independent method). |
| log | none | E11 scalar log oracles (not needed) | parametrize all thresholds as 100·e^{rational} |
| root bracket | T3 only | none | bisection with exp enclosures; fixed iteration count |

Cost scale: E10 evaluated about 9.2k moment references for H8 within 161 CPU s. Route B needs fewer than 3k exponential references plus O(10²) Φ enclosures per grid point.

## 6. Extension: variance-consuming (centred) estimators

The repository has no centred planner. If one is introduced, its break-even must be expressed in Var(g), and U3 then needs a **variance lower bound**:

- **Continuous.** Let F = {f = 0} ⊇ KO. Then Cov(f, 1_F) = −E f·P(F), and Cauchy–Schwarz gives Var f ≥ (E f)²·P(F)/(1 − P(F)). A certified q ≤ P(F) is needed, for example q = P(G_B(T) ≥ H) ≤ P(B_12 ≥ H) ≤ P(KO). That is a closed-form lognormal tail, but it needs ln 1.4, so the E11 log oracle would be required.
- **Digital.** P(g = 0) ≥ P(Z) ≥ P(KO_ideal) − p, where p is #43's mismatch probability (≈1.08e−3). So Var g ≥ (m_f − L1)²·q_g/(1 − q_g), with q_g = q − p.
- **Assessment.** Plausibly weak, because q is a terminal-only tail. The status is undetermined. Do not schedule it unless a centred planner exists.

## 7. Preregistration sketch (for a future, separately authorized scope)

- **Fixed symbolic grid**, chosen before any evaluation and independent of the informal check in §0:
  - κ' ∈ {−1/10, −1/20, 0, 1/20, 1/10} − 13/1600;
  - κ_c with c = 100(e^{κ_c} − 1), κ_c ∈ {1/40, 1/20, 1/10, 3/20, 1/5, 3/10, 7/20};
  - κ_a ∈ {0, 1/20, 1/10, 3/20, 1/5, 1/4}, keeping only grid points with a < λ, decided by enclosure.
  - Tiers: {K1, K2, K3} × {T1, T2, T3}.

  Every grid point is a valid deterministic lower bound, so reporting the maximum is valid. There is no statistical multiplicity. Each point is rounded outward on its own.
- **Outputs:** m_f lower (exact rational) and, per own profile, m_g = m_f − L1_π.
- **Decision.** PASS for a target ε iff m_g² ≥ S\*(ε). S\*(ε) must come from a saved, preregistered planner evaluation (O3), not from PLAN_43's workflow numbers. A miss is a negative feasibility record with no regridding.
- **Controls.**
  - (i) Φ at 0 and symmetry.
  - (ii) C1 at κ' → −∞ reproduces E[A] − K. Use a fixed very negative κ' and check against the exp-only E[A] − K within the declared tail slack.
  - (iii) The exact martingale identity at a = 0: K1 must return E[M_T] = 100 exactly up to enclosure width, so P̄_KO(a=0) = 100/λ = (5/7)·e^{3/100}. This is a control of the Doob path, not a selected grid point.
  - (iv) Rejection of a > λ.
  - (v) The pointwise-lemma algebra.
- **Caps:** as #42/#43 (180/150/600 s, 150 MiB, 131072/524288-bit frontiers). Same isolated interpreter, stdlib only.

## 8. Premises (SHA256 recomputed 2026-10-10)

| Premise | Path | SHA256 |
|---|---|---|
| #42 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md` | c43d0f35483491de3b3057c0803ac24011767f57b9fb40e63e902d82ec4cdc90 |
| #43 results page | `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md` | 512e879c42b206b0d79897850b39d3fcc167cc0e7188abf901bbdfa6ed639b04 |
| #43 ROOT receipt | `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json` | 87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7 |
| #43 manifest | `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/manifest.json` | 2f3162d8647888e424a01caadc0eff70cb481167a291a23462789eff380fa3f9 |
| #43 primary profile (`/payoff_L1_upper`) | `.../primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json` | c488f82b5fe04f578b33f2a060b99e6da387263b0da49cb2651691f1a23d32d6 |
| #43 independent profile | `.../independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json` | 663e25dd2fc990185400972b7f1c3be0fe04cb87a780dd7adfd35e2b61584910 |
| #42 prospectus (coupling, Q32 midpoint law) | `.context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run001.md` | d673d81da8e91a3ad84db02f85f8e7d7fe5ce276ff5fcd8944747623f9530364 |
| #42 prospectus (payoff < 40, [L,U], eta) | `.context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run002.md` | 04b491906b3dfadfb790fee41f7bca8dfc98991a7929770c785ad1ced3c0cc59 |
| all48 matrix (ideal-law wording) | `docs/limitation_program_20261001/E11_B4X12_ALL48_STOCK_MATRIX_RESULTS_20261007.md` | 5c1a7caf810340ed54710b3bf4a9795e7389d2284c6a18c86ae36982364dba92 |
| E07 bounded schedule | `results/limitation_program_20261001/E07_schedule_run001/schedule.json` | 4fdd33add8e18f83680bcda21f38fb0bb67cc1017323717b89a52165cb59b335 |
| Hadamard planner (raw-moment radius) | `research/controlled_priority_completion/estimator_hadamard.py` | 70c4cc7ce22718fdf65d326ba1b7e70d712afcc730df5707c25bf6ee05267776 |
| Contract parameters | `.context/advantage_frontier_replay/research/advantage_frontier_20260923/barrier_fast_classical.py` | 18611d7db2f896516f7aed2e67be988beafba0ef54f3bfb395c88447104c5472 |
| Orientation price (uncertified) | `results/frontier_classical_20261001/c1/c1_summary.json` | 5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123 |
| E10 machinery | `research/limitation_program_20261001/experiment_e10_continuous_moment_only_v2.py`; `E10_CONTINUOUS_MOMENT_ONLY_PREFLIGHT_V2.md` | 087d56a6c5847a50ba889e1743e4dbb49a7458e8d2e9347042596d1af8a49161; 6eae176f59e6d400ebd56db325403d857ccd5141f2e875b25bc66b43dc41d2f9 |
| Four targets | `.context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json`; `manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md` | de6d09fe50db48939e335d2a9aa4db112a3371a12d66fa7177b76bf5eae10e25; b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637 |
| STATUS rows E10/E11 | `docs/limitation_program_20261001/STATUS.md` | 0e8dbe484afe274c7a723dc8a823c4eaa520198364950c158a69745bedf22d88 |
| Parallel U2 | `docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md` | 6a4d5996753da15bfff6b150847dfac177e4bdf4b0095facd05bcdfaa6a2ef10 |
| Session design notes (not authorities; re-verified where used) | scratchpad `wf1/PLAN_43.md`; `wf1/moment_estimator_inventory.json` | 3d44ee1ddb19dcb23bc3418b2a9cc96b49014dc69b0e59c01b1f3f5859f3d405; e3712e9b164a86ce0086f4b4c070c512e724d797ff851ad5c2a75ce8ed8b5b29 |

Re-verification of the session notes:
- PLAN_43 §2's statement "S ≥ (E g)² ≈ 12.4" uses the uncertified price and is correct as orientation only. U3 is what would certify it.
- The inventory's E10 values (C4 0.786189, H8 118.413579) match `E10_CONTINUOUS_MOMENT_RESULTS.md` and do **not** apply to B4x12.

## 9. Open obligations

- **O1 (law identity).** Prove that the certificate's f is #42's ideal Y. This covers parameter semantics (decimal versus binary64 driver literals), the clamp convention, and the exact covariance factor. Otherwise add a certified E|Y − f| term.
- **O2 (digital law).** Bind Y_N to the estimator's g: the node and the Hadamard input law (the same as U2 O2).
- **O3 (break-even).** A saved, preregistered planner evaluation of S\*(ε) at all four targets, against the saved E07 schedule and against any adopted U2 schedule. PLAN_43's 0.3–0.9 are workflow evaluations.
- **O4 (monotonicity).** Prove the planner cost is non-decreasing in S, or evaluate the comparison over all S ≥ m_g².
- **O5 (Φ primitive).** A new certified Φ enclosure with independent controls, plus an independent second implementation for the saved verifier, as E10's audit did for exp.
- **O6 (T3 root bracket).** Fixed bisection count; failure to bracket gives a negative record.
- **O7 (lifecycle).** The full #42/#43-style lifecycle: prospectus, peer, ROOT, SOURCE, READY, SCI, FIELD and ROOT verification, behind a user authorization beyond scope #43.
- **O8 (centred estimators).** Only if introduced: §6's variance lower bound.

## 10. Non-claims

This note is a design. It contains:
- no measured or evaluated price bound, bias, probability or moment;
- no accuracy policy;
- no estimator saving (U3 can only *confirm* the absence of one);
- no confidence or runtime claim;
- no G2 promotion;
- no physical delivery;
- no quantum advantage;
- no fixture or 110-item credit.

The orientation price 3.5189 is uncertified. "Plausible" in §4 is an engineering judgement, not a result. E11 stays partial.
