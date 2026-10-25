# Review of P2, A2a and U1, and the v4 sign-off (24 October 2026)

**What this is.** An independent **AI** review by Claude (Opus 5.5), requested by the author on 24 October 2026. It is
the fourth AI review of these items. It is **not a human review**. It does not move any item from R1 to R2, and it
does not discharge the human-review step that PLAN_110 §4 and the N1 card require.

## Author decisions recorded here

| Decision | Status | Source |
|---|---|---|
| **v4 draft** (`manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v4.md`, checkers 99/99 and 186/186) | **Approved by the author, 24 Oct 2026** ("v4 draft approved") | chat instruction |
| **R2 sign-off** for scope #44 (window class, margin 26× < 30×) | **Not given; still open.** See the last section | — |

The draft itself is unchanged: it is hash-pinned, and `check_v3.py` forbids approval wording inside the draft.

## Verdicts

| Item | Verdict | Major findings | Minor findings |
|---|---|---|---|
| **P2 derivation** (`docs/frontier_probe_20261021/P2_DERIVATION.md`) | **Sound.** c(0.003) = 4.179 is a valid bound for 800 ≤ N ≤ 1,048,575 | none | R-P2-1 to R-P2-4 (doc wording) |
| **A2a proof**, steps 2 and 4 (`docs/claim_debts_20261022/A2A_CLIP_SPLIT_CERTIFICATE.md`) | **Sound**, given the inherited run002 premises | none | none new |
| **U1 premises** (iid draws, 1e-9 slack) (`docs/claim_debts_20261022/U1_CERTIFICATE.md`) | **Acceptable as stated assumptions; not material to the conclusion** | none | R-U1-1, R-U1-2 |

## P2

I re-derived every step of §1-§4 by hand: the outcome law, the eigen-branch mixture, the amplitude-error rule, the
lattice-sum bound, Poisson summation, the half-weight rectangle DTFT, the Φ₁ decay and the constant
2/((1+√3/2)(√3/2)) = 1.2376043, the alias sum π²/8, the cot Laurent-series monotonicity, the energy expansion, and the
midpoint-rule and series-tail bounds. Each holds as written.

**Monotonicity in N is analytic, not only numeric.** With c fixed, I_c and I_tot do not depend on N. Each correction
divided by N has the form (a + b ln N)/N^p with p ≥ 1 and a, b ≥ 0, or decreases through κ(N), so every one decreases
for N ≥ 2. The numerator rises and the denominator falls, so the bound increases in N.

**Independent checks** (`research/review_20261024/independent_checks.py`, `results/review_20261024/run001/checks.json`):

| Check | Result |
|---|---|
| Optimal window (DPSS, the top eigenvalue of the band-limiting matrix): leakage at c = 4.179 | 2.9530e-3 (N = 800), 2.9671e-3 (N = 100,924). Two methods (dense eigh and scipy) agree to 4e-16 |
| Kaiser β = 3.87, exact discrete leakage | 2.9641e-3 (800), **2.97059e-3 (100,924)**, 2.97063e-3 (298,456). Always above DPSS, as it must be, and below the target 2.996e-3 |
| Parts 1-2 bound, re-implemented in mpmath with adaptive quadrature | 0.99700973 at N = 800. The recorded certified value is 0.99700937, which is lower as expected because it carries the rigorous quadrature error. Both are below the true value 0.99703591 |
| N and k at the binding cell, from the closed-form root of the Δ quadratic | N = 100,924 and k = 8.761786, both exact matches |
| Parts 3-4 with 3 rotations per controlled phase (the doc counts 2) | δ₃₄ = 1.92e-6 at N = 298,456, so the 4e-6 reserve still holds |

**What the DPSS check adds.** Kaiser's leakage is within 0.12% of the optimum at every N tested. No window of 2N+1
taps can bring c below about 4.174 at δ = 0.003, so the certified 4.179 is within 0.12% of the best possible value
for this estimator class. Changing the window cannot move k below about 8.75. This supports the NO-GO and could go
into the paper as a robustness sentence.

**Minor findings** (wording only; no number changes):
- **R-P2-1.** §2 says the lattice loss is "below 1e-11". Its worst case over G is (1+4c)/K = 1.61e-11, and it is
  1.24e-11 at the binding N. It sits inside the 4e-6 reserve. Say "below 2e-11".
- **R-P2-2.** §5 says "all N ≥ 800, parts 1-4". Parts 1-2 hold for all N ≥ 800, but the parts 3-4 reserve holds only
  while g ≤ 21, i.e. N ≤ 1,048,575 (the code comment at `p2b_parts34.py:66` says this). No cell exceeds 298,456.
- **R-P2-3.** §4 counts the inverse QFT as g(g−1) rotations, i.e. 2 per controlled phase. The textbook decomposition
  uses 3. No effect (R-P2 table above).
- **R-P2-4.** The window state is prepared in a binary register, but the controlled powers are driven by subset-sum
  bits. Converting between the two is query-free reversible arithmetic, and its T cost is negligible next to 2.3e13,
  but §1 should say that it is needed.

## A2a, steps 2 and 4

**Step 2 (on Cᶜ the leak is β).** I checked it against the run002 source,
`experiment_box_muller_native_financial_bridge_v2.py`:
- `ell = (1+α)e^L + β` is defined at line 2844.
- `ell` enters the band at line 2892 and the mean-stock error at line 2989, in both places only through
  `max(β, ell)` or `140 − ell`.
- The `clipping_and_band` obligation (line 3079) names the lower clip as the only source of `ell`.

`clip_split_certificate.py` first reproduces run002's ζ exactly, and every band g_j to within 1e-5, with `ell`. Only
then does it substitute β. The per-stock chain also holds: an unclipped site has S_N ≤ b_j·S_I + β, and a clipped
site has S_N ≤ ell. On Cᶜ, therefore, B_N ≤ b_j·B_H + β.

**Step 4 (P_fin(C)).** The pieces hold:
- C ⊆ ∪{x_I ≤ L + λ_j}, pointwise on the shared raw-uniform space.
- On the 2^32-point midpoint grid, E cos θ = E sin θ = E sin 2θ = 0 and E cos²θ = 1/2 exactly. With R̂ ⊥ θ, this gives
  E Y_k = 0 and E Y_k² = E[R̂²](a_k² + b_k²)/2.
- The total variance per date is a² + b² = 9/(100·nt) however the normals are packed into pairs.
- E[R̂²] ≤ 2 + D_S·B² follows from the KS distance and R̂² ≤ B².
- s uses a lower bound on log 100, which is the safe direction.

I recomputed the total from the certificate components (an exact match, 3.63374e-4 ≤ 5.5e-4). I also recomputed the
Bernstein exponent at all 13 dates: the minimum is 72.268, and P(C) ≈ 2.8e-30 ≤ 1e-29.

**Not re-verified here.** The run002 premises themselves: the stock and prefix envelopes, the transport lemma, and the
independence of whole pairs and of radius and angle. The certificate discloses these, and run002 has its own audit.

## U1

- **The arithmetic.** I recomputed the EB bound at 60 digits from the saved totals. m_cert = 3.2880389500 is an exact
  match. Maurer & Pontil (2009) Thm 4 is applied correctly: it is one-sided, uses ln(2/δ), and uses R = 40 ≥
  40e^{−rT} = 38.82.
- **The contract.** `eb_sample.py` simulates the same contract that A2a's Y uses: r = 0.03, σ = 0.3, ρ = 0.4, 52
  dates, strict barrier 140, and A averaged over all stock-date words.
- **Headroom.** N = 100,924 stays valid for any mean up to 3.32687. That is 0.0388 above m_cert, or 4.8 EB
  half-widths. So the U1 premises only matter if they fail badly.
- **The iid premise.** It is the standard Monte Carlo premise, and I find no evidence against it. I drew a fresh
  sample from a different generator family (Philox, seed 20261024, n = 2^22). Its mean is 3.28504, which is z = 1.75
  from the PCG64 mean: unremarkable. Its own UCB plus A2a is about 3.2969, still below 3.32687. The RQMC price
  (3.28162) and the C09 sample's UCB (3.28251) are also consistent.
- **R-U1-1, the 1e-9 slack.** It covers float rounding in each payoff and in the sums: per payoff about 1e-12; for the
  saved fsum totals, below 1e-15 on the mean. It does **not** cover a float-induced barrier flip, because one flip
  moves the mean by up to 40/n = 4.8e-6. The expected effect of flips is about 1e-10 or less, but it is not a
  worst-case bound. The headroom absorbs about 8,000 flips. Suggested wording: "1e-9 covers arithmetic rounding;
  barrier-decision flips are covered by the 0.0388 headroom, not by the slack."
- **R-U1-2, provenance.** `u1/progress.jsonl` logs `eb_sample_done run001` twice. The exclusive-create directory rules
  out a silent overwrite, but nothing on disk shows whether other seeds were tried. Preregistration, an R2 step, is
  what closes this. The risk is low given the 4.8× headroom.
- **Not reviewed here.** The binding E[g] = E[Y_N] (U2 note O2), and the C03 failure-share change.

## Files

How to run: `.context/frontier_t0_env/Scripts/python.exe -I -B research/review_20261024/independent_checks.py run001`.
It needs numpy, scipy and mpmath, so it runs without `-S`. Wall time is 139 s.

| File | sha256 |
|---|---|
| `research/review_20261024/independent_checks.py` | 137f3cc8505084b43d29ccb90104f02a0947f7ab1549fe09349441357e6ac2d9 |
| `results/review_20261024/run001/checks.json` | b232cf4e480ed1b55d9efd1163647d352484767e5325cebc08ff49ea6c2bf87f |

## R2: why it is not signed off

PLAN_110 §4 requires R2 for scope #44 because the window margin (26×) is below 30×. R2 has three parts:

1. **Human peer review.** Neither this review nor the earlier three is one. Recording any of them as human review
   would misstate the paper's evidence grade.
2. **Preregistration.** The R2 rerun's n, seeds, δ, script hashes and decision rule must be fixed before it runs.
3. **A sealed run with a saved verifier and a receipt under `.context/`.** The project reserves writing there for the
   author.

**Ways forward:**
- **(a)** Ask one human reader to check the three items above, using this note as a guide. P2_DERIVATION.md is about
  160 lines.
- **(b)** Submit v4 at R1. Its status block already says plainly that it is AI-reviewed, so the journal's referees
  provide the human review. If you take this route, record the decision to waive the internal R2 gate, with its
  reason, so the plan and the paper agree.
- **(c)** Have the R2 package (preregistration prospectus, sealed-run script and verifier) drafted now, so that only
  your approval, the run and the human review remain.
