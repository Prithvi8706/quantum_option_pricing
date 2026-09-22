# Antithetic option-pricing feasibility: executed decision

Date: 22 September 2026. Read with the [frozen protocol](PROTOCOL.md) and
[preceding research investigation](../research_investigation/2026-09-22/DECISION.md).
All cases below are development cases. The manuscript, historical results, and
unopened confirmation cases are preserved.

## Decision

**No defensible significant quantum advantage established yet.** The explicit
antithetic construction tested here fails its feasibility screen by a large
margin. Stop scaling **this implementation and estimator schedule** toward an
advantage claim. Do not run the held-out confirmation study on it.

This is an executed negative feasibility result, not a proof that quantum
antithetic pricing is impossible, and not fulfillment of the advantage objective.
We compiled arithmetic blocks, implemented and tested an explicit estimation
schedule, built its resource composition, and measured substantially stronger
classical methods. We have **not** produced a monolithic, certified financial
quantum circuit or a fully placed fault-tolerant computer. Those distinctions
matter: the large resource estimates are for the declared construction, not
lower bounds on every possible implementation.

The original variance pilot found a real benefit. It omitted the decisive
competition: classical pricing receives that benefit too, its controlled base
is cheap, and coherent path arithmetic must be repeated many times. The new
work quantifies those obstacles. Reopening the route requires a different
coherent simulator/arithmetic and a materially cheaper explicit mean estimator,
with a measured cost target; more assets or more variance plots are insufficient.

## Contract and what was actually compared

The intended output remains a classical price for a continuously evolving,
discretely monitored arithmetic Asian basket under correlated Heston dynamics.
There are twelve contractual dates, spot/strike 100, and rate .03. Internal
refinement uses 12, 24, 48, 96, 192 and 384 steps without changing monitoring.
Development models:

| Case | Assets | Maturity | kappa | theta = v0 | xi | leverage | equity correlation | Feller ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | 1 | 1 | 2 | .09 | .3 | -.5 | .3 (irrelevant for one asset) | 4 |
| A4 | 4 | 1 | 2 | .09 | .3 | -.5 | .3 | 4 |
| S4 | 4 | 1 | 2 | .04 | .5 | -.7 | .3 | .64 |
| B8 | 8 | 2 | 1.5 | .12 | .5 | -.7 | .6 | 1.44 |

The fixed acceptance criterion is absolute error $.10/$.03/$.01, 99% success
per delivered price, and at least 10x complete latency improvement on 20/24
held-out cases at each claimed tolerance, at least 3x on every case. A planning
screen of 10 million physical qubits and 60 seconds is retained. Tenfold is an
engineering margin, not a statistical significance test.

**Neither side has completed that continuous-model accuracy contract here.**
Classical acquisitions estimate a Gaussian-input, discretized price in floating
arithmetic. The quantum construction proposes finite Gaussian inputs and fixed
arithmetic, with bounded values for the estimation schedule. The bridges between
these laws, continuous-time bias, payoff truncation, and numerical errors are
open. Thus the numbers below are a **cost feasibility screen with explicit
unproved accuracy assumptions**, not a matched, certified end-to-end race.

The acquisition starts from the two benign models; stress models test variance
robustness. No test case was promoted to independent confirmation. The
four-asset boundary case has Feller ratio below one; the chosen variance update
remains nonnegative in exact arithmetic because kappa*theta exceeds xi^2/4.
This does not supply the smooth-coefficient assumptions of the antithetic
convergence theorem.

## Executed classical competition

Implemented in [the new research package](../../research/antithetic_feasibility/):

- Numba-compiled drift-implicit truncated-Milstein log-price/variance paths;
  fine, adjacent-swap fine and summed-increment coarse paths.
- Independently trained geometric-GBM Asian control with analytic expectation;
  identical useful model information is made available to the quantum proposal.
- Scrambled Sobol, asset PCA and Brownian bridge, with setup included in sampling
  times. An independent residual Gaussian price mode is integrated analytically
  conditional on variance paths; the remaining scalar exercise root is solved.
- MC, controlled RQMC, conditional controlled RQMC, multilevel allocations, and
  a hybrid of controlled RQMC at the base with iid antithetic corrections.
- Independent full-truncation log-Euler reference acquisitions; a separate
  capped-payoff empirical-Bernstein check with a formal sampling inequality.

This is a serious baseline menu, not an assertion of globally optimal classical
pricing. GPU kernels, tensor approximations, joint surrogate training and
adaptive unbiased methods were not implemented. Those could strengthen the
classical side. An analytic European Heston formula does not directly price this
arithmetic path-dependent contract; a full basket PDE has additional path-state
dimensions. Neither is excluded as a possible improved solver. Stopping on a
losing quantum construction does not require first exhausting every classical
method that might make it lose further.

There are 864 base/single-level acquisition rows, 960 benign correction rows and
480 stress correction rows. Initial acquisitions use 16 independent
scrambles/batches. Fresh multilevel acquisitions use 32 replicates, with plans
written before their acquisition. Sampling roots and child seeds are archived.
The final hybrid uses 32 base scrambles and 32 independent batches per
correction level, without post-selection of replicate outcomes.

### Useful numerical results

| Case, requested tolerance | Price estimate | Empirical 99% sampling half-width | First measured seconds, including control fit | Timing repeat seconds |
|---|---:|---:|---:|---:|
| A1, $.10 | 7.94451 | .02489 | 1.42 | 2.20 |
| A1, $.03 | 7.92941 | .00774 | 1.01 | 1.57 |
| A1, $.01 | 7.93022 | .00292 | 8.64 | 12.83 |
| A4, $.10 | 5.71254 | .02435 | 1.08 | 1.57 |
| A4, $.03 | 5.71254 | .00824 | 2.85 | 4.10 |
| A4, $.01 | 5.71413 | .00219 | 13.75 | 20.68 |

These are sampling intervals, **not** certified total-error intervals. Timings
are workstation observations, not stable benchmark distributions; repeated
execution used identical seeds to check reproducibility and timing, not to
claim more statistical evidence. Import and fresh native compilation are
excluded from these warm timings; a separately executed cold-process timing is
archived in [cold_classical_v1](../../results/antithetic_feasibility/cold_classical_v1/receipt.json).
That full cold-process acquisition took **45.68 seconds** for A4 $.01 and
reproduced the price and empirical sampling interval exactly. It includes
imports, fresh native compilation, control fitting, acquisition and output.
The original initial kernel warmup took 18.28 seconds. Hardware: Windows,
Intel Family 6 Model 170, 16 physical/22 logical CPUs; this implementation does
not use a GPU. The acquisition manifest records versions and source hashes.

The A4 base control reduces per-path variance from roughly 63 to 2.25;
conditional integration reduces it further to about 1.14. In the selected
$.01 hybrid allocation, the base consumed 10.17 of 13.75 seconds. Making all
corrections free could improve **that fixed allocation** by only about 1.35x.
This is not a bound on all retuned hybrid methods; it identifies where the cost
actually sits. A1's base share is approximately 81%.

The initially frozen all-RQMC and all-conditional-RQMC allocation models were
not reliable enough: at A4 $.01 their fresh sampling half-widths were .00513
and .00534, above the planned .0045 sampling allowance, and their costs were
27.43 and 25.99 seconds. Fine-level Sobol setup was costly at tiny sample counts.
These failures are retained. The hybrid is a subsequent development change,
not successful confirmation of the original allocation model.

![Classical diagnostic cost](../../results/antithetic_feasibility/decision_summary_v1/classical_precision_cost.png)

### Variance robustness

Fitting Var(Y_l) proportional to 2^(-beta*l) across the five measured correction
levels gives:

| Case | Unconditioned MC beta | Conditional RQMC pointwise-variance beta |
|---|---:|---:|
| A1 | 1.90 | 2.32 |
| A4 | 1.98 | 2.32 |
| S4 | 1.23 | 1.24 |
| B8 | 2.26 | 2.31 |

These are descriptive finite-level fits without inferential confidence bands,
not asymptotic exponents. Conditional RQMC pointwise variance is not the variance
of a scrambled quadrature estimate. In particular, the benign beta near two
does not extend to the boundary case. A universal beta=2 resource argument
would be unsupported.

![Correction variance](../../results/antithetic_feasibility/decision_summary_v1/variance_decay.png)

The independent Euler reference at 768 steps gives A1 7.92893 +/- .00416 and A4
5.71657 +/- .00468, empirical 99% sampling intervals. Agreement is reassuring
but uncertainty exceeds the proposed $.001 reference allowance at the tightest
tolerance. It is not a bias certificate. The fixed-N capped-payoff check, using
262,144 iid paths and a fitted independent capped geometric control, gives
sampling radii .03804 (A1, 40.53 seconds) and .03101 (A4, 109.98 seconds).
That bound uses the two-sided form of
[Maurer--Pontil, Theorem 4](https://arxiv.org/abs/0907.3740), assuming exact iid
sampling, bounded evaluations and the exact control mean. It certifies neither
floating arithmetic nor uncapped continuous-model bias.

## What was compiled and tested

Actual X/CX/CCX gate streams were emitted for signed fixed-point multiplication,
constant multiplication, square root, exponential, comparison, positive part,
and clean Heston steps. Width is f+16, where f is fractional precision. Standard
exact seven-T Toffoli decomposition gives the following logical counts:

| Block | Fraction bits | Allocated logical wires | T count | Dependency T depth |
|---|---:|---:|---:|---:|
| Square root | 32 | 2,397 | 226,240 | 109,017 |
| Multiply | 32 | 337 | 260,736 | 76,032 |
| Exponential/spot | 32 | 1,345 | 8,884,820 | 2,596,296 |
| Clean Heston step, h=1/12 | 24 | 3,323 | 2,003,176 | 540,199 |
| Clean Heston step, h=1/12 | 32 | 4,371 | 2,924,040 | 779,311 |

These are real block counts, not simulator timing converted into hardware
timing. Depth assumes all-to-all connectivity and that explicit gate ordering;
it is not an optimal circuit-depth lower bound. Large clean intermediate
registers and ripple arithmetic are implementation choices. Faster arithmetic,
space-time pebbling, spot-coordinate formulations and architecture-aware
scheduling could change these constants and require a new measurement.

The full price cost is a **hierarchical composition of these blocks**, with
declared serial block scheduling and retained path history. It is not a
gate-emitted complete price circuit. The h=1/12 and h=1/24 step T-count formulas
agree exactly with emitted streams. Payoff/control assembly has a charged block
envelope but no complete finance-to-gates equivalence proof yet.

Gaussian preparation is not free: an explicitly constructed one-dimensional
bin-mass table on [-8,8] compiles at q=10 to 1,022 CX and 792 arbitrary U gates,
with an upper count of 2,376 elementary arbitrary rotations. The table is 1,024
entries/8,192 bytes and is reused across coordinates. No full-path table or
QRAM is assumed. Rotation synthesis is unresolved and **excluded from the
quoted T totals**, with rotation counts separately exposed. This omission
favors the quantum cost screen; it cannot support a positive crossover.

A symmetric finite Haar hierarchy retains parents explicitly and swaps children
by negating the last detail coordinates. This preserves level marginals and
swap symmetry by construction instead of equating rounded child sums to their
parent. That mathematical coupling is tested. The complete fixed-point
simulation/error certificate is still open.

### Precision is material

At A4 level 5, 32 paired development paths give mean arithmetic price differences
-$.00144 at f=24 and -$.00000437 at f=32; maximum absolute differences are
$.00344 and $.0000101. A1 f=24 maximum difference is $.00669. A separate
64-path coupled correction diagnostic at A4 level 5 gives RMS arithmetic
correction difference .00117 at f=24 and .00000149 at f=32. These do not prove
uniform bounds or absence of variance floors; they justify carrying f=32 as the
main screen instead of treating f=24 as adequate.

Finite Gaussian q=10 at A4 level 5 gives a paired price difference of -.000337
+/- .000741 empirically at 99%; q=14 gives .00000293 +/- .0000546. Thus q=10
does not validate a $.0005 input allowance on this evidence. The q=10 quantum
costs are deliberately favorable sensitivity figures, not certified sufficient
precision. q=14 preparation has not been compiled. The Gaussian analytic
control expectation also needs its finite-law bridge; it is not automatically
the exact expectation of the finite quantum control.

## Explicit variance-sensitive schedule

The executed estimator is a signed dyadic-bin QAE construction using the
explicit amplitude-estimation inequality in
[Montanaro, Section 2, Theorem 2 and Algorithms 2--3](https://arxiv.org/abs/1504.06987).
This is a specified construction, not an assertion that this older estimator
is the best modern quantum algorithm.

For a variable centered at c, supply a **proved second-moment** bound
m2 >= E[(Y-c)^2]. Set s=sqrt(m2), and use dyadic bins starting at a power of two
between s and 2s. With K signed bins of upper bounds b_j, the shared QAE size M
is chosen as a power of two to satisfy

    tail + 4*pi*s*sqrt(K)/M + pi^2*sum(b_j)/M^2 <= e.

The first term is at most m2/B for truncation at B; it is zero only under a
proved bounded-support premise. The derivation uses disjoint bins,
sum(b_j E[|Y-c| 1_bin]) <= 4*m2, Cauchy--Schwarz, and the explicit QAE error
inequality. Odd median repetition counts use the binomial failure tail with
per-run success at least 8/pi^2; failure is allocated across bins and levels.
The code checks the spectral QAE distribution against the inequality.

Each run pays 2M-1 calls to A or its inverse, M-1 Grover iterates, and its QFT
rotations. Every signed bin and median is counted. The digital selector uses
exactly log2(b_j*2^f) uniform bits, so its success probability is |Y-c|/b_j on
the bin; using the whole value-register range would be an incorrect
normalization. All 104 distinct scheduled production-bin circuits were emitted
and fit the charged T-count/depth/workspace envelope. Clean scratch and flag
probabilities are exhaustively tested at small widths.

Controlled Grover powers may leave A uncontrolled around controlled
reflections. In this reversible function construction A-dagger uncomputes the
data-dependent workspace before the input reflection; the latter acts on the
noise/selector input subspace. The source call ledger counts preparations and
inverse operations instead of silently treating them as classical samples.

**Unproved inputs to the cost screen:** base centered second moment bounded by
four times its pilot variance; correction moment bounded by four times
(pilot variance + mean squared); absolute centered value bounded by 1,024 after
capping/guarding. These must be proved for the actual finite circuit law before
the schedule becomes a certified pricing algorithm. They are not established
by these samples. Statistical error receives .45*epsilon, and statistical
failure .004 across levels. The remaining numerical error budget is not closed.

The stronger source-access theorem in
[Kothari--O'Donnell, Theorem 1.1, Section 2 and Appendix A](https://arxiv.org/abs/2208.07544)
has O(sigma/epsilon) query scaling without these logarithmic factors. We did
not compile its phase-oracle and full high-confidence procedure. Its hidden
constants are not assigned optimistic numerical values in the explicit cost
table. A separate unit-constant envelope below tests the optimistic direction;
it is not an implementation of that theorem.

## Crossover: what the numbers actually say

For A4, f=32, levels 0--5 and epsilon=.01, the composition produces:

| Quantity | Value and scope |
|---|---|
| Calls to source or inverse | 215,532,014 |
| T count excluding arbitrary-rotation synthesis | 2.247e17 |
| Serial block T depth excluding rotations | 7.253e16 |
| Arbitrary-rotation count upper estimate | 9.386e13 |
| Retained-history logical wires | 964,332, a space policy, not a necessary minimum |
| Total serial time at a hypothetical 100 ns/T layer | approximately 230 years for this schedule |
| Largest single QPE run at 100 ns/T layer | approximately 55 days, even if other bins/medians run concurrently |

The years figure is a diagnostic consequence of a declared logical scheduling
model, **not a validated physical runtime prediction**. It combines conservative
implementation choices with favorable omissions such as unsynthesized
rotations. It is neither a rigorous lower bound nor a rigorous complete upper
bound on physical pricing runtime. It plainly gives no credible level-2 result.

Both f=24/32 and all three tolerances are archived. At f=32, the A4 $.10/.03
serial figures at the same hypothetical layer rate are about 20/60 years.
A1 gives about 8.6/35/120 years at $.10/.03/$.01. These are not made publishable
advantage results by changing the clock assumption within an order of magnitude.

For an ideal variance-sensitive scheme with per-level invocation latency c_l
seconds and effective query multiplier k, allocating absolute estimation
errors e_l with sum(e_l)=epsilon_stat gives the favorable continuous allocation

    T_Q = k * (sum_l sqrt(c_l*sigma_l))^2 / epsilon_stat.

This neglects integer schedules, failure amplification, setup and output cost.
It is a sensitivity relation, not a universal lower bound. A 10x target requires

    k * (sum_l sqrt(c_l*sigma_l))^2
        <= epsilon_stat * T_classical / 10.

The actual explicit ledger instead uses sum(N_A,l*c_A,l + N_G,l*c_reflection,l),
plus rotations, hardware and setup. Physical runtime must also satisfy the
magic-state throughput constraint T_count / (states per second).

### Give quantum substantially more favorable assumptions

Set k=1, use empirical sigma rather than doubled sigma, charge only one path's
current square-root dependency depth, and make other assets, arithmetic,
loading, exponentials, payoff, control, inverse overhead and confidence
amplification free. At 100 ns/T layer and epsilon=.01:

| Case | Base alone, all corrections free | Levels 0--5 | Warm classical latency used | Additional reduction needed for 10x, base / full |
|---|---:|---:|---:|---:|
| A1 | 75.02 s | 451.92 s | 8.64 s | 86.9x / 523x |
| A4 | 43.65 s | 231.46 s | 13.75 s | 31.7x / 168x |

This even grants bias eligibility when removing levels and compares with the
more expensive classical level-5 workload. The intermediate level-1/2/3 results
are saved. The conclusion does not depend on choosing six unnecessarily fine
levels. However, using a more expensive *cold* classical latency relaxes these
ratios; these warm ratios must not be quoted as the complete cold-start contract.
The cold subprocess measurement is reported separately. Likewise, a much faster
square-root circuit changes this envelope. It rejects no theorem and proves no
impossibility. Its purpose is to expose the scale and location of the required
algorithmic change before paying for another large experiment.

Using the measured **45.68-second cold classical** cost instead, the 10x quantum
budget is 4.568 seconds. Even the A4 square-root-only estimate needs a further
9.56x reduction with the base alone, or 50.7x with all six levels. This grants
quantum free setup as well as the other favorable omissions. It still is a
diagnostic comparison, since the financial error bridges remain unproved.

For the warm A4 data, the same screen requires effective square-root T layers
below 3.15 ns (base alone) or .594 ns (six levels), or equivalent reductions in
square-root dependency depth. Those are derived thresholds, not hardware claims.
A real estimator with k>1 tightens them proportionally.

![Optimistic sensitivity](../../results/antithetic_feasibility/decision_summary_v1/ideal_screen.png)

### Physical sensitivity, not vendor validation

The code also applies the approximate surface-code fit and two-level
distillation construction from
[Litinski, Figure 19 and Equations 10--11](https://arxiv.org/abs/1808.02892):
p_L approximately .1*(100*p)^((d+1)/2), roughly 2*d^2 physical qubits/tile,
176 tiles for the selected factory and 15*d cycles/output. Assumptions include
p=.001 or .0001, a 1 microsecond cycle, 20% factory throughput derating, a
2x data-tile routing reserve, and .005 physical failure budget.

For the retained-history A4 layout, data plus one factory exceed 96 million
physical qubits even at d=5, before satisfying the failure constraint. This
fails the 10-million planning cap **for that memory policy**. Recomputing
intermediates can trade time for space; the result is not a necessary physical
qubit count. Routing, decoder throughput, measurement latency, Clifford
scheduling and a full distillation/synthesis allocation remain unresolved.
No vendor announcement is credited as changing any of these assumptions.

## Error and claim ledger

| Item | Status | Consequence |
|---|---|---|
| Antithetic cancellation on benign development cases | Observed, reproduced with new classical implementation | Useful for both sides; not advantage |
| Uniform beta=2 over tested parameter region | Unsupported; S4 finite-level fit about 1.24 | Cannot use a universal favorable complexity exponent |
| Strong classical controlled/multilevel price estimates | Executed, empirical intervals | Serious cost comparator; total bias not certified |
| Independent reference price at $.001 uncertainty | Not achieved | No final $.01 accuracy confirmation |
| Finite Haar marginal/swap construction | Implemented and tested mathematically | Does not prove complete finite arithmetic error |
| Block unitaries, cleanup, decomposition | Tested; actual production gate counts archived | Level-4 implementation evidence only |
| Complete price circuit equivalent to financial estimator | Not completed | Macro costs must retain qualification |
| Estimator bound for supplied second moment/support | Derived and tested in the declared access model | Conditional algorithmic statement |
| Required second moment/support for actual finance circuit | Unproved | Schedule cannot be advertised as a certified price algorithm |
| Continuous-time, finite-input, arithmetic, cap and control-mean bridges | Diagnostics only, several gaps | Numerical-error budget not closed |
| Rotation synthesis/physical layout/decoder certificate | Not completed | No level-2 end-to-end projection |
| Significant advantage over strong classical pricing | Not established | Original acceptance objective remains unmet |
| Quantum pricing impossibility | Not established | Do not generalize rejection beyond this construction |

## Reproducibility and disposition

[README](../../research/antithetic_feasibility/README.md) contains commands,
dependencies and output mapping. [Raw artifacts](../../results/antithetic_feasibility/)
contain individual replicate records, frozen plans, compilation hashes and
gate streams, actual integer schedules, reference diagnostics and figures in
PNG/PDF. Tests cover covariance, Brownian bridge, conditional integration,
constant-volatility telescoping, controls, finite coupling, integer arithmetic,
scratch cleanup, exact Toffoli unitary, QAE probabilities and digital bin
normalization. A final validation receipt records the executed test result.

Continue decisions must be tied to **new evidence**:

1. **Stop now:** enlarging the existing parameter sweep, opening confirmation,
   optimizing only Gaussian loading, or presenting the present cost model as a
   positive advantage paper. The gate has failed before those investments.
2. **Reopen only with a concrete reduction:** compile a replacement base path
   generator and an explicit modern mean estimator. Bind their complete
   invocation cost and confidence schedule to the crossover relation above.
   Include a held-out arithmetic equivalence check and numerical-error ledger.
   A bare O(sigma/epsilon) citation or a faster isolated gate is insufficient.
3. **Paper direction:** preserve the existing comparative quantum manuscript.
   This work supports a separate, qualified feasibility/benchmark appendix or
   methods study if its novelty and error claims withstand review. It does not
   transform the manuscript into an advantage paper or guarantee publication.
4. **Fallback research question:** the prior one-decision compound Asian
   hypothesis remains a scope change requiring its own classical nesting-removal
   test. It was not implemented or validated in this antithetic acquisition and
   should not be quietly substituted for the failed target.

The most informative next action, if continuing quantum advantage research, is
**a replacement-oracle cost experiment**, not another variance pilot: demonstrate
an end-to-end controlled base estimator whose fully specified cost fits the
measured latency budget, then add corrections and prove the error bridges.
That is a conditional reopening test, not a recommendation to assume that
another implementation will succeed.

## Primary technical reading used for this implementation

| Source | Reading target | What it supplies / does not supply |
|---|---|---|
| [Giles--Szpruch, antithetic MLMC](https://arxiv.org/abs/1202.6283) | Coupling construction, convergence hypotheses, Section 5.2 examples | Classical antithetic mechanism; no automatic theorem for arbitrary square-root boundary parameters |
| [An et al., quantum-accelerated MLMC](https://arxiv.org/abs/2012.06283) | Theorem 2 and applications | Conditional query exponents; no charged coherent Heston circuit |
| [Herman et al., 2026](https://arxiv.org/html/2602.03725v1) | Section 7.1 | Motivation for investigating quantum antithetic coupling; not a demonstrated crossover or exclusive novelty claim |
| [Montanaro, 2015; corrected arXiv version](https://arxiv.org/abs/1504.06987) | Section 2, Theorem 2, Algorithms 2--3 | Explicit AE inequality and signed/variance-sensitive mechanism; instantiated schedule here has its own stated second-moment premise |
| [Kothari--O'Donnell, SODA 2023](https://arxiv.org/abs/2208.07544) | Theorem 1.1, Section 2, Appendix A | Stronger source-access mean estimation; no numerical pricing constants assigned here |
| [Maurer--Pontil, COLT 2009](https://arxiv.org/abs/0907.3740) | Theorem 4 | Empirical-Bernstein sampling bound; not floating/SDE error control |
| [Litinski, Quantum 3, 128 (2019)](https://arxiv.org/abs/1808.02892) | Figure 19, Equations 10--11 | Explicit architecture sensitivity model; not a current demonstrated device specification |

Full texts of the implementation references were read; the earlier investigation
contains the wider 2024--2026 venue/industrial/classical screening. This follow-up
does not claim exhaustive priority clearance or a new literature search covering
every recent mean-estimation or arithmetic circuit.
