# Why quantum amplitude estimation has not beaten strong classical option pricing

**Foundation document for the measured advantage-frontier paper.**
Draft, 23 September 2026. Affiliation: VIT Vellore. Author names, human approval and
submission details are not asserted. This is AI-assisted research writing.

This document explains in detail why six constructions in this project, covering three
option contracts and all built with one toolchain, failed to produce a significant quantum
advantage in option pricing. They are not six independent confirmations. Corrections
made on 24 September are listed in
[ERRATA.md](../../docs/research_investigation/2026-09-23/ERRATA.md). It covers what each
obstacle is, why it holds, and what it would take to remove it. It is a negative and
requirements result, **not** an advantage claim. The verdict remains:
**no defensible significant quantum advantage established yet.**

All numbers come from this repository's executed studies or from primary sources
checked during the 22–23 September investigation. The evidence map (§9) gives exact
file locations.

---

## 1. The question and the standard of success

The task is to return **one classical, discounted option price**:
- absolute error at most $0.10, $0.03 or $0.01 per $100 notional ($0.001 in the final
  test);
- at least **99% confidence** per delivered price.

"Significant advantage" means at least **10 times lower complete latency** than the
fastest eligible classical method. Complete latency includes setup, state preparation,
arithmetic, uncomputation, estimator repetitions and readout.

The classical comparator is the strongest applicable method, not plain Monte Carlo:
- control variates;
- randomized quasi-Monte Carlo (RQMC) with principal components;
- conditioning and preintegration;
- multilevel methods;
- compiled, multicore execution.

Four evidence levels are kept separate throughout:

| Level | Meaning | Status for option pricing |
|---|---|---|
| L1 | Demonstrated end-to-end hardware advantage | None, anywhere |
| L2 | Conditional end-to-end fault-tolerant crossover under explicit hardware assumptions | None found; this project's six constructions (three contracts) all fail it |
| L3 | Algorithmic/query advantage in an access model | Generic quadratic speedup over plain Monte Carlo only |
| L4 | Improvement over another quantum implementation | This project's manuscript and circuit improvements |

---

## 2. The single inequality behind every failure

### 2.1 What the quantum algorithm saves

Pricing by simulation averages random payoffs. Let σ be the standard deviation of one
payoff sample, and e the statistical error allowance (this project uses e = 0.45ε).

- **Classical Monte Carlo** needs N_C ≈ z²·(σ/e)² samples, with z ≈ 2.6 at 99%.
- **Quantum amplitude estimation** (and variance-sensitive mean estimators) needs
  N_Q ≈ k·(σ/e) calls to a coherent oracle.

The constant k collects:
- the estimator's intrinsic constant (at least about π for canonical amplitude
  estimation);
- the source and inverse calls inside every Grover iterate;
- the median or confidence repetitions needed for 99%;
- phase-estimation discretization.

The quantum algorithm therefore saves a factor of about **σ/e (divided by k) in the
number of samples**. That is the quadratic speedup. At penny accuracy on a $100
contract, σ/e is typically 10³ to 10⁴, which is why the idea is attractive.

### 2.2 What each quantum sample costs

A quantum oracle call is not one classical sample. Define

> **ρ = (latency of one complete coherent oracle call) / (latency of one classical sample)**

The complete times are then T_C = N_C·c_C and T_Q = N_Q·ρ·c_C, where c_C is the
classical time per sample. Their ratio, the quantum speedup, is

> **T_C / T_Q ≈ z²·(σ/e) / (k·ρ)**   against plain Monte Carlo.

A tenfold win requires

> **ρ ≤ z²·(σ/e) / (10·k)**

With σ/e = 10³ and k = 3, ρ must be below about 200. **One complete quantum oracle
call may cost at most a few hundred classical samples, and often only a few** (see
§2.4). Across this project, ρ ranges from about 10³ to 10⁹, depending on the assumed
logical clock and the classical hardware. The ratio is set out in §3.

### 2.3 Against strong classical methods the quadratic saving disappears

Classical pricing does not use plain Monte Carlo. RQMC with principal components and
smoothing converges like n^(−r) with r close to 1 on smooth or smoothable payoffs, so
its cost is about (σ/e)^(1/r) ≈ σ/e. That is **the same scaling as the quantum
estimator**. The sample-count advantage then collapses to a constant, and the speedup
becomes roughly c/(k·ρ). With ρ ≫ 1, this is far below one.

Write the classical cost exponent as p_C (cost ∝ ε^(−p_C)); quantum has p_Q = 1. The
room for any quantum gain is p_C − 1:

| Payoff (4×12 and 8×52 GBM baskets, measured) | Best classical p_C | Room for quantum |
|---|---:|---:|
| Arithmetic Asian basket call, preintegrated RQMC | 1.01–1.04 | ≈ 0 |
| Basket digital, preintegrated RQMC | 0.99–1.03 | ≈ 0 |
| Discretely monitored knock-out, best smoothing tried | 1.58–1.90 | 0.6–0.9 |

The quantum advantage can only grow like ε^(−(p_C−1)), so even the knock-out's room
grows very slowly as the accuracy target tightens.

### 2.4 The same law as a depth budget

Divide the classical time by the number of quantum calls and the time per logical T
layer (t_layer). The largest T-depth one complete oracle call may have is

> **D_max = T_C / (10 · k · (σ/e) · t_layer)**

This is the most useful form, because it can be compared directly with a compiled
circuit.

### 2.5 Worked example (the final experiment)

Take the 8-asset × 52-date knock-out basket at ε = $0.001. Assume a generous 100 ns
logical T-layer and k = 3.

| Quantity | Value |
|---|---|
| σ of the payoff | $5.15 |
| e = 0.45 × $0.001 | $0.00045 |
| σ/e | ≈ 11,400 |
| Quantum oracle calls k·σ/e | ≈ 34,000 |
| Minimal compiled oracle depth (forward + inverse) | 9.0×10⁵ T-layers, i.e. 0.09 s per call at 100 ns |
| Total quantum time | ≈ 3,100 s |
| Classical (compiled, 16 cores, strongest method) | **27.1 s** |
| D_max for a 10× win | **789 T-layers per call** |

The quantum computation is about **110 times slower**. To be 10 times *faster* it needs
about **1,100× improvement**. At a more realistic 10 µs per T-layer, quantum takes about
3.6 days against 27 seconds.

---

## 3. Anatomy of ρ: why one quantum sample is so expensive

ρ is the product of two independent penalties.

**How many logical operations an oracle call contains.** A classical path sample is
written in floating point, discards its intermediates, and runs at native speed. A
coherent oracle must:

1. **Prepare randomness coherently.** Every Gaussian needs Box–Muller (a logarithm, a
   square root and a cosine) or an equivalent loader. The 8×52 basket uses 468
   Gaussians per path.
2. **Do every arithmetic step reversibly in fixed point.** A 72-bit fixed-point
   multiply is thousands of Toffoli gates. There is no floating-point unit, and no
   operation may discard information.
3. **Evaluate transcendental functions by polynomials.** The exponential uses range
   reduction and a degree-12 polynomial: about 12–15 multiplies, about 7 of them on the
   critical path when arranged for minimum depth. The 8×52 basket needs 416 exponentials per path.
4. **Uncompute everything.** Every intermediate must be reversed, which doubles the
   work.
5. **Be controllable.** The oracle sits inside controlled Grover iterates or phase
   estimation.

Certified leaf depths from the project's range-specialized compiler (72-bit words, 40
fractional bits):

| Operation | T-depth of cheapest certified leaf |
|---|---:|
| add / subtract | 1,152 |
| multiply | 11,088 (range-narrow) to 79,312 |
| square root | 225,193 |
| divide | 398,256 |

A depth-optimized knock-out oracle for 8×52, built in the project IR and scored with the
cheapest certified leaf of each operation type, has a clean-call score of 9.0×10⁵
T-layers. It is 1.8×10⁵ even if Gaussian preparation were free. The construction used
Estrin polynomials, parallel-prefix paths, tree sums and unlimited parallelism. This is a
score, not an emitted circuit: on a compiled source, the same rule reads about 0.6× of
the true depth, so it is optimistic for quantum.

**How long each logical operation takes.** Fault-tolerant machines protect each logical
qubit with an error-correcting code whose cycle is about 1 µs on superconducting
hardware. The expensive non-Clifford T and Toffoli gates need "magic states" from
distillation or cultivation factories, and their timing is gated by the decoder's
**reaction time**.

| Anchor | Value | Status |
|---|---|---|
| Surface-code cycle (Google Willow) | 1.1 µs | Demonstrated (memory only, no logical gates) |
| Real-time decoding latency (Willow, d = 5) | ≈ 63 µs, excluding feedback | Demonstrated |
| Reaction time assumed by Gidney 2025 | 10 µs | Projection |
| CCZ / lattice-surgery period (Gidney 2025, d = 25) | 25 µs | Projection |
| 33-bit addition, ripple-carry lattice surgery | ≈ 1.6 ms | Projection (Fast for the Curious) |
| Same, reaction-limited carry-lookahead, 1 µs reaction | ≈ 20 µs | Projection, large space cost |
| Trapped-ion all-to-all layer (Quantinuum Helios) | ≈ 55 ms | Demonstrated |
| Neutral-atom logical layers | ≈ 0.5–4 ms | Demonstrated |
| Classical CPU addition | < 1 ns | Commodity |
| Classical GPU throughput | ≈ 10¹³ operations per second | Commodity |

A logical arithmetic operation is therefore **10⁴ to 10⁹ times slower** than its
classical counterpart. The same verified sources price Chakrabarti et al.'s compiled
options circuit (10⁴ logical qubits, 10¹⁰ T gates) at **3.7 days per single circuit
repetition** under standard 1 µs-cycle assumptions. The classical target was about one
second.

---

## 4. The six attempts: what was tried, why it failed, what would fix it

### Failure 1: antithetic quantum multilevel Monte Carlo on correlated Heston baskets

**The idea.** Stochastic volatility forces time-stepping. Multilevel Monte Carlo places
most work on cheap coarse levels and estimates small fine-level corrections. The
antithetic coupling of Giles and Szpruch makes those corrections tiny without Lévy-area
simulation, and a variance-sensitive quantum estimator pays only for that small
variance.

**What was built.** A classical controlled RQMC and antithetic MLMC benchmark, compiled
Heston-step circuits (≈2.9 million T gates per 32-bit step), a Gaussian loader, and an
explicit signed dyadic estimator schedule.

**Why it failed.**
- *The coupling helps classical equally.* Correction variance fell ≈570–600× for both
  sides.
- *The cost lives at the base level.* In the $0.01 four-asset hybrid, the base level
  took 10.17 of 13.75 classical seconds (≈74%, ≈81% for one asset), priced with
  controlled RQMC whose per-path variance fell from ≈63 to ≈1.14. Making every
  correction free would improve classical by only 1.35×.
- *Coherent Heston steps are expensive.* Even charging only the square-root dependency
  depth, with k = 1, 100 ns per T-layer and everything else free, it missed by
  **32–523×**. The explicit schedule would take about 230 years serially.
- *The favourable variance rate is not universal.* At a Feller ratio below one, the
  measured rate was β ≈ 1.24, not 2.

**What would fix it.** A coherent Heston step roughly 10³–10⁴× cheaper, with k near 1,
so that ρ at the base level falls to tens. No known arithmetic or hardware roadmap
provides this.

### Failure 2: compound Asian option via quantum-inside-quantum estimation

**The idea.** A compound option is an option on a conditional expectation. Naive
classical nested Monte Carlo costs about ε⁻³ to ε⁻⁴; nested quantum estimation
(Blanchet et al.) costs about ε⁻¹. The apparent gap looked better than quadratic.

**Why it failed.**
- *Classical removed the nesting.* Under GBM, future returns are independent of the
  current level, so one set of simulated future factors serves every outer state.
  Conditional geometric controls give near-exact inner values: the exercise-policy
  bracket was only $4×10⁻⁸ to $6×10⁻⁶ wide. Twelve contracts were priced in 8–16 s.
- *The best classical nested methods are ε⁻² anyway.* Nested multilevel Monte Carlo
  and the multilevel dual method both reach about ε⁻². Against those, the true quantum
  gap is about 1 (quadratic), not 3.
- *The quantum inner loop is enormous.* It needed 1.1×10¹⁵ to 4.9×10¹⁶ conditional
  source calls. The per-source budget for a 10× win was 1.7–44 ns, while one 32-bit
  multiply takes 7.6 ms at 100 ns per T-layer.

**What would fix it.** A financially real nested contract whose conditional value
cannot be reused, controlled or bracketed cheaply: no exploitable Markov structure and a
genuinely high-dimensional state, so that even nested MLMC stays above ε⁻². Even then
the best quantum theory (Sun et al., ICML 2026) gives ε⁻¹·log^(3D+1) against ε⁻², a gap
of 1 that *shrinks* with nesting depth D. The ρ problem would still need solving on top.

### Failure 3: controlled parity residual

**The idea.** Estimate only a small bounded residual left after a strong analytic
control (a put-call parity decomposition). A smaller residual variance means fewer
quantum queries.

**Why it failed.**
- *The mathematics worked.* Residual second moments fell 7.4–60.5×, and ideal query
  counts dropped to 218–508.
- *Variance reduction is symmetric, and it hurts quantum's relative advantage.* The
  classical side uses the same controls. The speedup factor is proportional to σ/e, so
  making σ smaller makes the quadratic advantage smaller: classical sample counts fall
  quadratically, quantum ones only linearly.
- *Each source call was still too slow.* A 10× win needed each complete coherent source
  in 3–5 ms. One compiled exponential alone takes about 0.26 s at 100 ns per T-layer.
- *Certification cost exceeded the budget.* Statistically certifying the residual
  moments cost 72–255 s of classical work, more than the classical price itself.

**What would fix it.** A variance-reduction mechanism usable only by the quantum side
(none is known), or a source 10²–10³× cheaper. Algebra on the estimand cannot repair ρ.

### Failure 4: the complete controlled source and an explicit estimator

**The idea.** Stop estimating costs and build every gate, together with a real
Kothari–O'Donnell-style mean estimator and a full error ledger.

**Why it failed.** It exposed the hidden constants.
- *The source is huge.* One clean evaluation for the four-asset model is 2.6×10⁹ T gates
  and 7.7×10⁸ T-layers deep. It has to include Box–Muller Gaussians, both path halves,
  geometric controls, the continuation policy and the residual, all computed and
  uncomputed.
- *k was enormous.* The conservative 99%-confidence schedule needed 1.5×10⁹ controlled
  calls, against 218 in the idealized count.
- *Even the idealized version failed.* 218 calls with everything else free took 4.7
  hours (C4) and 40 hours (H8) of arithmetic at 100 ns per T-layer, against a 1.1-second
  budget.

**What would fix it.** k near its theoretical floor and per-call depth reduced by about
10⁴. The next study attacked both.

### Failure 5: the priority completion, where everything was optimized

**The idea.** Remove the implementation inefficiencies.

**What it achieved.** The improvements were real and large:
- the estimator redesign cut controlled iterations 1,280× (C4) and 2,119× (H8);
- range-certified narrow multipliers cut source T work 2.37–2.39×;
- parallel wave schedules made the source 38–108× shallower, with paid workspace.

Together, that is roughly a 10⁵ improvement.

**Why it still failed.**
- *Far off the budget.* The best schedules needed 19,400 s (C4) and 58,849 s (H8) at a
  hypothetical **1 ns** per T-layer, about 1,000× faster than projections, against
  tenfold budgets of 1.11 s and 1.38 s. That is a miss of **17,468× and 42,499×**.
- *Magic-state supply.* Giving all 10 million physical qubits to 15-to-1 factories,
  delivery alone took 432 s and 3,849 s.
- *Memory.* The mapping used 0.9–3.2 million logical qubits, exceeding the physical-qubit
  cap even at distance 3.

**What would fix it.** A further 10⁴–10⁵. Known compilation levers such as
reaction-limited carry-lookahead arithmetic give about 10². There is no identified
source for the rest. **This study is the clearest evidence that the obstacle is
structural, not an implementation shortfall.**

### Failure 6: the discretely monitored knock-out basket

**The idea.** Find a payoff where classical smoothing fails, so the classical side keeps
a slow convergence rate and quantum has genuine exponent room.

**What was measured.**
- *The premise held.* With first-principal-direction preintegration (compiled, 16
  cores), the RQMC rate was only 0.53–0.63; one-step-survival conditioning gave
  0.48–0.57. Calls and digitals, by contrast, recovered rates of about 1.0.
- *The knock-out oracle was built to reduce depth.* It was constructed in the project's
  reversible IR and scored, not emitted, with cheapest-certified-leaf costs. An
  interactive check (not yet archived as a script) found its fixed-point output within
  2×10⁻⁸ of the floating-point payoff, with no knock-out misclassification in 52 draws.
  Its clean-call score is 8.9×10⁵ with Box–Muller Gaussians, and 1.7–1.8×10⁵ with free
  Gaussians.

**Why it failed.** At the decision point stated before the runs ($0.001, 100 ns, k = 3), against a classical time modelled from measured per-point cost:

| Case | Classical time | D_max | Oracle depth | Too deep by |
|---|---:|---:|---:|---:|
| 4 assets × 12 dates | 5.9 s | 154 | 8.85×10⁵ | 5,765× |
| 8 assets × 52 dates | 27.1 s | 789 | 8.99×10⁵ | 1,138× |

How robust it is:
- *At the decision point,* a hypothetical oracle with Chakrabarti et al.'s per-operator
  depth (≈9.5×10³, derived for a smaller payoff; not a floor) is still 13–65× too deep.
- *Correcting* the classical timing overhead makes the 4×12 miss about 15,000× rather than
  5,765× (ERRATA E5).
- *Joint quantum-favourable corners do exist in the sensitivity grid.* 19 of 192 rows come
  within 10×, and one fits (8×52 at $0.10 with k = 1, a 10 ns T-layer, free Gaussians and a
  variance the plain oracle cannot realise). Every such row needs a 10 ns T-layer and/or
  k = 1, outside the admissible region of the decision rule.

The exponent room exists, but it grows only like ε^(−0.7). Closing three orders of
magnitude that way needs accuracy many orders of magnitude tighter than any market
requires. This rests on extrapolating the fitted rate far outside the measured range, so it
is indicative only.

**What would fix it.** Any one of the following:
- an oracle about 1,000× shallower (a few hundred T-layers per complete multi-asset
  path, less than one current multiply);
- logical T-layers about 1,000× faster than projected;
- accuracy requirements about 10⁴× stricter than real ones.

---

## 5. The six root causes, and what removing each would require

### Root cause A: the quadratic ceiling (mathematics)

**Why it holds.** For estimating a mean by queries, quantum algorithms need on the order
of 1/ε queries, and this is a proven lower bound; classical sampling needs on the order
of 1/ε². **Quadratic is the maximum, not a starting point.** In smoothness classes
(Heinrich; Novak) the quantum gain over randomized classical integration is
1/(s+½) − 1/(s+1) ≤ 1 in the exponent, and it shrinks to zero as smoothness per
dimension grows. For smooth integrands, scrambled nets reach an RMSE of about n^(−3/2),
asymptotically better than generic amplitude estimation.

**What removing it requires.** A financially meaningful price whose *best* classical
algorithm costs ε⁻³ or worse while a quantum algorithm stays near ε⁻¹. The candidates
examined:
- *Nested or compound contracts:* classical multilevel methods reach ε⁻².
- *Heavy-tailed payoffs:* a change of measure makes classical estimators bounded.
- *Quantum-walk MCMC:* the only known gap that grows with a problem parameter, but no
  pricing task genuinely requires a slowly mixing Markov chain.
- *Discontinuous path payoffs:* the classical exponent stays at 1.6–1.9, a gap of at
  most about 0.9.

A new algorithmic discovery would be needed, together with evidence that no classical
reformulation recovers the structure.

### Root cause B: logical operations are slow (fault-tolerant hardware)

**Why it holds.** Error correction multiplies time and space. A logical T or Toffoli
gate waits for magic-state delivery and decoder reaction. Demonstrated decoding latency
is tens of microseconds, and projections are 1–10 µs. A logical addition costs tens of
microseconds to milliseconds, against under a nanosecond classically.

**What removing it requires.** Sustained, reaction-limited logical T-layers of about
1–100 ns, 100–10,000× faster than any published roadmap (IBM, Google, Quantinuum, IonQ,
PsiQuantum). That in turn needs some combination of:
- much faster physical cycles;
- sub-microsecond decoding with feedback;
- cheap non-Clifford gates (for example transversal gates in higher-dimensional codes,
  or high-rate cultivation);
- physical error rates low enough that code distances, and hence cycles per logical
  operation, shrink sharply.

Qubit-count reductions, such as those from qLDPC codes, do not change serial latency
unless they relieve the scheduled bottleneck. IBM's bivariate-bicycle architecture
explicitly takes *longer* per T gate. Microsoft's topological approach is the only path
projecting clocks near 100 ns, and it is not demonstrated.

### Root cause C: reversible fixed-point arithmetic (circuits)

**Why it holds.** Quantum circuits cannot use floating-point units or discard
intermediates. Multiplication costs quadratically many Toffolis in the word width,
functions need polynomial evaluation, every intermediate must be uncomputed, and the
whole oracle must be controllable. A path that takes microseconds on a CPU becomes
10⁸–10⁹ T gates.

**What removing it requires.** Arithmetic-free constructions, in which prices are
encoded directly in amplitudes and the payoff is applied by quantum signal processing.
This works for simple one-dimensional payoffs; the manuscript's reflection/QSP route is
an example. For multi-asset path-dependent payoffs (averages of exponentials, maxima over
dates), no known construction avoids arithmetic without an exponential blow-up. The best
recent payoff-loading improvement (≈50× on the loading module, arXiv 2507.19039) does
not touch the dominant Gaussian and path arithmetic. This remains an open research
problem.

### Root cause D: classical methods use problem structure at native speed

**Why it holds.** Control variates, conditioning, preintegration, factor reuse,
principal components and Brownian bridges all exploit knowledge of the model. The
quantum side may use the same ideas, but pays ρ for every additional arithmetic step.
Shared variance reduction also shrinks the quantum advantage factor σ/e (Failure 3).

**What removing it requires.** A financially real problem with no exploitable structure.
In practice, financial models are designed to be tractable (Markov, affine, lognormal
factors), and that tractability is exactly what classical methods exploit.

### Root cause E: classical parallelism is almost free

**Why it holds.** Classical RQMC splits across cores and GPU lanes with near-linear
speedup at low marginal cost. Parallel amplitude estimation can also scale linearly
(arXiv 2508.06121, which corrects an earlier √P bound), but every parallel lane needs a
full copy of the oracle's workspace, hundreds of thousands to millions of logical
qubits. Under a practical qubit budget, only about 1–10 copies are available.

**What removing it requires.** Physical-qubit budgets of billions in order to run many
oracle copies. Even then, classical parallelism remains far cheaper per unit of work.

### Root cause F: the output contract (confidence and certification)

**Why it holds.** A 99% per-price guarantee forces the quantum estimator into repeated
runs, median amplification and fine phase resolution; that is what inflates k.
Classical confidence intervals come almost free from independent randomizations.
Certifying the variance or moment bounds that variance-sensitive quantum estimators need
can itself cost more than the classical price (Failure 3).

**What removing it requires.** Explicit estimators whose constants approach the
theoretical floor at 99% confidence, and variance information obtainable without
expensive certification. Theory permits small constants; the certified schedules
actually built here needed much larger ones.

---

## 6. Ideas that do not help, and why

| Idea | Why it does not create advantage |
|---|---|
| More assets or more dates | Classical cost grows with the path length just as quantum cost does; principal components and preintegration keep classical convergence near 1/n for smooth payoffs |
| Discontinuous payoffs | Smoothing restores 1/n for digitals; knock-outs keep only 0.6–0.9 of exponent room, far too little (Failure 6) |
| Stochastic or rough volatility | Both sides pay for time-stepping; classical sparse-grid/QMC and Markovian-lift methods reach ε⁻¹·³ to ε⁻¹·⁶ for rough Bergomi |
| Better compilation | Worth ≈10⁵ in this project and still 10⁴× short; the known levers left are worth ≈10² |
| Variance reduction or controls | Symmetric, and it shrinks the quadratic advantage factor |
| Many strikes, portfolios, Greeks | Classical shares paths and uses adjoint differentiation; quantum multi-output estimation costs about √K more for K outputs |
| Quantum PDE solvers | Reading out a single price costs normalization and success-probability factors that grow with dimension; they beat only full-grid finite differences |
| Quantum quasi-Monte Carlo "pre-asymptotic window" | Compares an upper bound with the worst-case bound of *unscrambled* Sobol points; against scrambled RQMC the gap is zero or negative |
| New hardware announcements | None supplies a verified, pricing-relevant ≥10³ cut in latency per logical operation |

---

## 7. The requirements frontier

For a tenfold quantum win on a standard multi-asset path-dependent price, **at least one
row** must become true:

| Requirement | Where things stand today |
|---|---|
| ρ ≈ 10–100: one oracle call costs tens of classical samples | 10³–10⁹ measured and projected |
| Complete path oracle depth of about 10²–10³ T-layers | Leaf-table score of the depth-optimized oracle ≈ 1.8×10⁵ (free Gaussians); ≈ 9×10⁵ with Box–Muller |
| Sustained logical T-layer of about 1–10 ns | 1–10 µs projected; tens of µs demonstrated for decoding |
| Best classical cost ≥ ε⁻³ for a real price | No such pricing workload identified |
| Estimator constant k ≈ 1 at 99% confidence | Certified schedules used far larger constants |
| Accuracy of about 10⁻⁶ relative | Not required by any market |

Two conclusions follow. The obstacle is the **combination** of a mathematical ceiling (at
most quadratic, about zero against RQMC) with a **physical cost per logical operation
10⁴–10⁹ times the classical one**. Removing only one factor is not enough.

Independent expert analyses reach the same classification:
- Babbush et al., PRX Quantum 2021: quadratic speedups need about cubic–quartic
  separations, or roughly 10³× faster logic, to pay off;
- Hoefler, Häner and Troyer, CACM 2023;
- "The Grand Challenge of Quantum Applications", 2025, which places derivative pricing in
  the quadratic-only class.

---

## 8. What this project does establish

- An auditable account of where and by how much quantum amplitude-estimation pricing
  falls short of strong (not exhaustive) classical methods. It covers six constructions
  over three contracts, with executed classical baselines and explicit resource ledgers;
  two complete compiled sources, partial compiled charges and one leaf-table-scored oracle.
- A budget identity, D_max = T_C / (10·k·(σ/e)·t_layer), adapted from the break-even form
  of Babbush et al. and expressed in financial units. It is applied to each construction
  at its own operating point. Its content lies in the measured inputs, not the identity.
- Measured post-smoothing classical exponents, including the knock-out failure mode of
  RQMC.
- A requirements frontier stating what would have to change, and by how much.

These are L4 and requirements results. They support a scoped benchmark or negative-result
paper, subject to a prior-art and novelty review against Babbush 2021, Chakrabarti 2021,
Hoefler 2023, the Grand Challenge 2025 and Fast for the Curious 2025. They do not support
any claim of quantum advantage, nor a claim that advantage is impossible: no universal
lower bound was proved.

---

## 9. Evidence map

| Topic | Location in this repository |
|---|---|
| Investigation verdict, screening and reading list | `docs/research_investigation/2026-09-23/DECISION.md`, `SCREENING_TABLE.md` |
| Knock-out falsifier result | `docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md` |
| Classical exponents, one-step survival, frontier, compiled classical, oracle depth, decision | `research/advantage_frontier_20260923/`, `results/advantage_frontier_20260923/` |
| Failure 1: antithetic MLMC | `docs/antithetic_feasibility/RESULTS.md` |
| Failure 2: compound Asian | `docs/compound_feasibility/RESULTS.md` |
| Failure 3: parity residual | `docs/controlled_residual_feasibility/RESULTS.md` |
| Failure 4: complete source | `docs/controlled_source_completion/RESULTS.md` |
| Failure 5: priority completion | `docs/controlled_priority_completion/RESULTS.md`, `results/controlled_priority_completion/combined_cost.json` |
| Earlier comparator manuscript (L4) | `manuscript/2026-09-22/main.md` |

## 10. Primary references

- R. Babbush et al., "Focus beyond quadratic speedups for error-corrected quantum advantage," PRX Quantum 2, 010103 (2021). https://arxiv.org/abs/2011.04149
- S. Chakrabarti et al., "A threshold for quantum advantage in derivative pricing," Quantum 5, 463 (2021). https://arxiv.org/abs/2012.03819
- N. Stamatopoulos and W. J. Zeng, "Derivative pricing using quantum signal processing," Quantum 8, 1322 (2024). https://arxiv.org/abs/2307.14310
- T. Hoefler, T. Häner and M. Troyer, "Disentangling hype from practicality: on realistically achieving quantum advantage," CACM 66(5) (2023). https://arxiv.org/abs/2307.00523
- "The Grand Challenge of Quantum Applications" (2025). https://arxiv.org/abs/2511.09124
- McArdle, Dalzell, Kubica and Brandão, "The Fast for the Curious: how to accelerate fault-tolerant quantum applications" (2025). https://arxiv.org/abs/2510.26078
- Google Quantum AI, "Quantum error correction below the surface code threshold," Nature (2025). https://arxiv.org/abs/2408.13687
- C. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits" (2025). https://arxiv.org/abs/2505.15917
- A. Montanaro, "Quantum speedup of Monte Carlo methods," Proc. R. Soc. A (2015). https://arxiv.org/abs/1504.06987
- R. Kothari and R. O'Donnell, "Mean estimation when you have the source code; or, quantum Monte Carlo methods," SODA (2023). https://arxiv.org/abs/2208.07544
- D. An et al., "Quantum-accelerated multilevel Monte Carlo methods for stochastic differential equations in mathematical finance," Quantum 5, 481 (2021). https://arxiv.org/abs/2012.06283
- M. B. Giles and L. Szpruch, "Antithetic multilevel Monte Carlo estimation for multi-dimensional SDEs without Lévy area simulation," Ann. Appl. Probab. (2014). https://arxiv.org/abs/1202.6283
- J. Blanchet et al., "Quantum speedup of non-linear Monte Carlo problems," NeurIPS (2025). https://arxiv.org/abs/2502.05094
- Sun, Wang and Blanchet, "Optimal quantum speedups for repeatedly nested expectation estimation" (2026). https://arxiv.org/abs/2602.08120
- D. Belomestny, J. Schoenmakers and F. Dickmann, "Multilevel dual approach for pricing American style derivatives," Finance Stoch. (2013). https://doi.org/10.1007/s00780-013-0208-1
- "On the error rate of conditional quasi-Monte Carlo for discontinuous functions," SIAM J. Numer. Anal. (2019). https://arxiv.org/abs/1708.09512
- C. Bayer, C. Ben Hammouda and R. Tempone, "Numerical smoothing with hierarchical adaptive sparse grids and quasi-Monte Carlo methods for efficient option pricing" (2022). https://arxiv.org/abs/2111.01874
- M. B. Giles and B. J. Waterhouse, "Multilevel quasi-Monte Carlo path simulation" (2009). https://people.maths.ox.ac.uk/gilesm/files/jcf07.pdf
- Recchia, Yu, Koor and Rebentrost, "Quantum quasi-Monte Carlo: a window for pre-asymptotic quantum advantage" (2026). https://arxiv.org/abs/2609.03625
- Oshio, Wada and Yamamoto, "Near-Heisenberg-limited parallel amplitude estimation with logarithmic depth circuit" (2025, v3 2026). https://arxiv.org/abs/2508.06121
- P. Glasserman and J. Staum, "Conditioning on one-step survival for barrier option simulations," Operations Research 49(6) (2001).
