# H1 falsifier: executed result

23 September 2026, corrected 24 September (see [ERRATA.md](ERRATA.md)). This executes a
**reduced** version of the one-week H1 falsifier specified in
[DECISION.md §6](DECISION.md#6-recommended-direction-and-staged-experiment). Deviations
are listed in [PREREGISTRATION_DEVIATIONS.md](PREREGISTRATION_DEVIATIONS.md). The stop rule
was stated there before the P3/Q1 runs, according to the working record. It was written
after the P1/P2 pilots and first committed together with these results, so the ordering is
not externally time-stamped. All cases are development cases; no held-out case was
generated, and nothing here is a certified price or a quantum execution.

## Decision

**STOP H1.** The stated stop condition fires on both executed cases, with a large margin.

At a price accuracy of $0.001, 100 ns per logical T-layer and estimator constant k = 3,
a depth-optimized, leaf-table-scored knock-out oracle is **1,138× (8×52) and 5,765× (4×12)
deeper** than the budget a 10× win allows against the compiled classical pricer, whose
time is modelled from measured per-point cost. The stop threshold was 10×. Correcting the
classical first-chunk overhead would raise the 4×12 figure to about 15,000× (ERRATA E5).

Within the rule's admissible region (ε ≥ $0.001, t ≥ 100 ns, k ≥ 3) no executed case
survives. **No defensible significant quantum advantage established yet.**

## Contract

Equal-weight arithmetic-average basket call with discrete knock-out: payoff 0 if any
monitoring date's basket value is at least 140. Correlated GBM with σ = .3,
equicorrelation .4, S0 = K = 100, r = .03, T = 1, exact at the dates. Cases are 4 assets
× 12 dates and 8 × 52. Statistical error allowance is 0.45ε with 99% (t, 15 degrees of
freedom) intervals from 16 independent scrambles.

## Classical side (P3, measured per-point cost; T_C modelled)

[`barrier_fast_classical.py`](../../../research/advantage_frontier_20260923/barrier_fast_classical.py)
implements the strongest measured method from P1: analytic preintegration along the first
principal direction, with Newton roots for the strike and every date's barrier. It is a
numba-compiled kernel with single-thread BLAS gemm, run as one scramble per process across
16 processes, and it matches the P1 numpy estimator to 10⁻¹³ per point.

| Case | Price (32 scrambles) | RQMC rate r, n = 2⁹…2¹⁷ (point fit) | Time per scramble to 2¹⁷ points | Modelled classical time to $0.001 |
|---|---:|---:|---:|---:|
| 4×12 | 3.51889 ± .00009 | 0.633 | 7.7 s | 5.9 s |
| 8×52 | 3.28162 ± .00010 | 0.527 | 28.4 s | 27.1 s |

Prices agree with P1 (3.51852 ± .00015; 3.28156 ± .00021). The rate stays well below the
n⁻¹ that smoothing restores for calls and digitals, so the barrier keeps its
exponent room for quantum. The implementation is CPU-only. No GPU library was installed,
and a faster classical side would only shrink the quantum budget further.

## Quantum side (Q1, built in the IR and scored, not emitted)

[`barrier_oracle_depth.py`](../../../research/advantage_frontier_20260923/barrier_oracle_depth.py)
builds the knock-out payoff oracle in the project's reversible fixed-point IR. It uses the
same Box–Muller generator, correlated increments, spot guard and exp range reduction as
the compound source. Its construction choices aim to reduce depth (optimality was not
tested):
- Estrin rather than Horner for the degree-12 exp polynomial;
- a parallel-prefix path;
- tree sums and a tree maximum over dates.

Each IR operation is charged the cheapest (or median) T-depth among certified leaves of
that operation type in the range-specialized f=40 library
(`results/controlled_priority_completion/range_compile_v1/leaves_f40`), whatever the
operand ranges. The oracle itself is not range-certified, emitted or scheduled. The
critical path assumes unlimited parallelism, no routing, and no factory or reaction
limits, and a clean call is charged forward plus inverse. On the compiled C4 compound
source, the same cheapest-leaf rule gives 0.61× (median rule 1.08×) of the true
dependency-only depth. It is therefore optimistic for quantum, although it undercounts
non-power-of-two constant multiplies and cosine lookups (ERRATA E3). In an interactive
check, the IR's fixed-point output agreed with a floating-point knock-out payoff on the
same finite inputs to within 2×10⁻⁸, with no knock-out misclassification in 52 draws.
That check is not yet archived as a script (ERRATA E4).

| Case | Gaussians | Leaf costs | Clean-call T-depth | Clean-call T-count |
|---|---|---|---:|---:|
| 4×12 | Box–Muller | cheapest certified leaf per op | 8.85×10⁵ | 1.5×10⁸ |
| 4×12 | free (zero cost) | cheapest | 1.68×10⁵ | 6.0×10⁷ |
| 8×52 | Box–Muller | cheapest | 8.99×10⁵ | 1.2×10⁹ |
| 8×52 | free (zero cost) | cheapest | 1.82×10⁵ | 5.2×10⁸ |
| 8×52 | Box–Muller | median leaf per op | 2.10×10⁶ | 3.4×10⁹ |

These are compiler-specific scores, not emitted-circuit depths and not lower bounds on
every possible circuit.

## Comparison

In the formulas below, Q is the number of oracle calls, σ_Q is the per-sample standard
deviation of the oracle's estimand, and D_max is the largest per-call T-depth a 10× win
allows:

    Q = k * sigma_Q / (0.45 eps),   D_max = T_classical / (10 * Q * t_layer).

σ_Q is the plain knock-out payoff's per-sample standard deviation (5.73 for 4×12, 5.15 for
8×52), because that is what the oracle computes.

| Case | D_max at $0.001, 100 ns, k=3 | Oracle / D_max, Box–Muller | Oracle / D_max, free Gaussians |
|---|---:|---:|---:|
| 4×12 | 154 | **5,765×** | 1,095× |
| 8×52 | 789 | **1,138×** | 230× |

### Robustness

- **A hypothetical oracle with Chakrabarti et al.'s per-operator T-depth** (≈9.5×10³,
  derived for their smaller autocallable benchmark; not a floor) would still be 13× (8×52)
  and 65× (4×12) too deep **at the decision point** ($0.001, 100 ns, k = 3). Across the
  full grid it would fit in 22 rows. Two of those are at 100 ns, and both need k = 1 and
  the preintegrated σ.
- **Joint corners** (ERRATA E1): 19 of 192 grid rows have oracle/D_max ≤ 10, and one fits:
  8×52 at ε = $0.10, k = 1, 10 ns per T-layer (roughly 100× faster than any projection),
  free Gaussians and a preintegrated σ this oracle cannot realise (ratio 0.92). Every such
  row needs a 10 ns T-layer and/or k = 1, outside the stop rule's admissible region.
- **Untried classical methods** (multi-direction numerical smoothing, bridge-ordered
  one-step survival, conditional pathwise smoothing, barrier importance sampling, GPU
  execution) could only raise classical speed, which lowers D_max. They were part of the
  stated protocol and were not run (PREREGISTRATION_DEVIATIONS).

Full grid: [`barrier_decision.json`](../../../results/advantage_frontier_20260923/barrier_decision.json).

## What this means

The only payoff class found where the strongest classical smoothing leaves the Monte Carlo
exponent intact still misses by three orders of magnitude, under assumptions chosen to
favour quantum. Across the project, six constructions over three contracts (Heston
antithetic MLMC; the compound Asian in four successive refinements; this knock-out), all
from one toolchain, each fail the 10× latency condition at their own stated operating
point. They are not six independent confirmations (ERRATA E8).

The defensible next deliverable is the measured-frontier paper described in DECISION.md
§6. It is a requirements and negative result, not an advantage result. Reopening
direct-pricing advantage would need new evidence of one of three kinds:
- a ≥10³ cut in coherent latency per operation;
- a pricing workload where the best classical exponent is ≥ 3;
- a mechanism outside quadratic mean estimation.

## Reproduce (local)

    # classical (needs numba; anaconda python was used)
    C:\Users\prith\anaconda3\python.exe research/advantage_frontier_20260923/barrier_fast_classical.py
    # oracle depth (needs the project's numba env for the IR imports)
    .context/antithetic_feasibility_env/Scripts/python.exe research/advantage_frontier_20260923/barrier_oracle_depth.py
    # decision
    venv/Scripts/python.exe research/advantage_frontier_20260923/barrier_decision.py

Environment: Windows, Intel Family 6 Model 170 (16 cores / 22 threads), numba 0.60.0,
numpy 1.26.4. The classical run took 32.7 s (4×12) and 62.4 s (8×52) wall time for all 32
scrambles.
