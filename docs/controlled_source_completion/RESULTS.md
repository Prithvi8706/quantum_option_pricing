# Controlled compound source: completed feasibility investigation

22 September 2026. **No defensible significant quantum advantage established yet.**
The recommended complete-source/explicit-estimator investigation is now executed.
The first two follow-up priorities, independent validation and resource/precision
reconciliation, are complete as specified in [CHECKLIST.md](CHECKLIST.md). The
result rejects this constructed implementation under the stated latency screens.
It does not prove that every quantum approach to this financial model is impossible.

## Decision and acceptance contract

Keep the original compound call on the arithmetic Asian-basket continuation
value, the four development models, strikes 3/6/9 and the same controls. The
acceptance criterion remains a penny of absolute error, 99% per-price confidence
and at least a tenfold latency improvement over a strong eligible classical
implementation. A full price, its uncertainty and all setup/output costs count.
No held-out case was opened, and no manuscript claim was changed.

The previous variance pilot answered whether the put-complement residual was
small. This work answers whether an explicit coherent source and estimator can
exploit it affordably. They cannot in this implementation. Sampling savings are
overwhelmed by reversible path generation and analytic-control/policy arithmetic.
The same controls already make classical full pricing inexpensive.

The completed work is a resource/implementation result, evidence level 4. Generic
source-access quantum mean-estimation advantages remain literature-level results
at level 3, with no project-specific lower bound against structured classical
pricing. Neither level 1 hardware advantage nor level 2 conditional end-to-end
fault-tolerant advantage is established.

## What was actually implemented

The hierarchical source includes midpoint-uniform preparation, a reversible
Box-Muller transform, both halves of every GBM path, guarded stock evaluation,
arithmetic and geometric averages, geometric put/call controls, moment-matched
continuation, the existing regression where selected, analytic lower/upper
clipping, exercise decision, signed residual and inverse cleanup. There is no
free Gaussian loader, QRAM, path-price lookup table or assumed arithmetic leaf.
Finite one-dimensional coefficient QROMs are paid as emitted gates.

Every arithmetic leaf has a gate file. The source contains hundreds of millions
to billions of gates, represented hierarchically to reuse definitions. Its gate
executor traverses that hierarchy; it is not an analytic oracle-count formula.
Version 2 removes repeated expressions and folds constants exactly, reducing
T counts by about 10% from the preserved initial compilation.
The final estimator also fuses compute/phase/uncompute, removing a redundant
internal cleanup pair. This approximately halves the arithmetic of its earlier
modular wrapper. Both stages of resource evidence are preserved.

The estimator implements an explicit, conservative known-moment variant of
[Kothari-O'Donnell](https://arxiv.org/abs/2208.07544), using Theorem 3.19 and an
adaptive interval contraction. Integer QPE powers, majority repetitions, source
and inverse calls, controlled reflection sign, full inverse QFT, random-register
resets, classical endpoint loads, measurement and decoding are specified.
A machine-readable controlled-U gate envelope binds every wire. Arbitrary
rotations remain unsynthesized and are recorded as an outstanding cost.

This is not the paper's unknown-variance algorithm or a demonstration of its
optimal constants. The conservative confidence schedule is especially expensive;
its failure is not a refutation of the optimal query theorem. A separate ideal
query sensitivity below grants much better constants and still fails.

## Complete source cost

Representative strike-6 sources, 40 fractional arithmetic bits and 32 random
bits per uniform, after exact expression reuse:

| Model | Logical qubits, clean Y source | T gates, one clean Y | T layers, serial leaf schedule | Seconds per Y at hypothetical 100 ns/T layer |
|---|---:|---:|---:|---:|
| C4 | 635,344 | 2,567,192,362 | 772,215,706 | 77.222 |
| H8 | 2,299,912 | 9,528,390,746 | 2,861,978,738 | 286.198 |

A clean Y evaluation includes its internal inverse cleanup. The final controlled U
runs the financial graph forward, then the angle graph, applies phases and
inverts both graphs before reflection. Its redundant internal cleanups are fused;
the table still omits the angle and reflection cost of one iterate. Depth is a valid
schedule for this compiler, not a lower bound on arbitrary arithmetic circuits.
The logical timing assumption is hypothetical; CPU simulator timings were not
converted into quantum performance.

## Classical comparison and deliberately favorable crossover screen

The retained classical baseline uses controlled, vectorized randomized QMC and
policy/Jensen price brackets, with prior independent reference agreement. C4
retains the faster new parity implementation; H8 retains the faster earlier
implementation. Each measured time includes all three strikes and is charged
in full to one requested price, favoring the quantum comparison. Empirical 99%
intervals are distinguished from the stricter fixed-iid statistical contract.
The source's finite-law financial bridge is not yet proved; the screen below
grants it at zero cost rather than claiming mismatched targets are equivalent.

For illustration, suppose the entire quantum mean estimate required only
ceil(sqrt(moment)/error) clean Y calls, with coefficient one, no extra inverse,
no confidence amplification, free baseline/regret handling and free setup.
This is a sensitivity coordinate, **not** the implemented algorithm or a
universal query lower bound. Give it the previous tight continuous-model moment
bound for free, despite the unproved transfer:

| Model | Measured classical full-price seconds | Total budget for 10x win, seconds | Idealized Y calls | Arithmetic-only hours at 100 ns/T layer |
|---|---:|---:|---:|---:|
| C4 | 11.106 | 1.111 | 218 | 4.68 |
| H8 | 13.847 | 1.385 | 508 | 40.39 |

Even at 1 ns/T layer, these favorable totals are approximately
168.3 s and
1453.9 s. The stricter
C4 classical statistical bound cost 267.84 s, implying a 26.784 s tenfold budget;
the C4 ideal screen still fails that budget even at 1 ns/T layer. No GPU or
additional classical method needs to be weakened or excluded to get this result.

The explicit conservative estimator is much more costly. With the tight
continuous-model moment *conditionally granted*, financial source f=40 and
phase f=64:

| Model | Controlled U calls | Arithmetic T gates | Logical qubits per serial execution | Arithmetic-only seconds at 100 ns/T layer |
|---|---:|---:|---:|---:|
| C4 | 1,540,372,419 | 3.986e+18 | 659,310 | 1.199e+11 |
| H8 | 6,287,324,746 | 6.004e+19 | 2,328,872 | 1.803e+12 |

These very large numbers are reproducible costs of this chosen schedule, not
predicted device runtimes or optimal-algorithm lower bounds. Giving all repeated
QPE runs independent hardware still leaves longest single QPE chains of
3.266e+08 s (C4) and
4.812e+09 s (H8) under
the same schedule/timing assumption. Optimizing constants cannot be confused
with a demonstrated crossover.

A separate schedule uses the unconditional digital support bound E[Y_d^2]<=B^2.
It needs roughly 4.65e11/4.74e11 controlled-U calls for C4/H8. Thus removing the
costly classical moment-certificate acquisition does not rescue this construction.
Using the tighter previous certificate would additionally charge 75.11 s/254.72 s
of acquisition including policy training, unless reuse is justified and shared
with the classical method. Surrogate pricing and regret certification are further
costs; H8's previous regret certificate also failed its assigned error budget.

In consistent units, a completed comparison would require

    T_setup + T_device + T_measurement/feedback + T_classical_outputs <= T_classical/10,
    T_device >= max(D_T * seconds_per_T_layer, N_T / delivered_T_states_per_second).

The known arithmetic already fails under generous assumptions. Synthesis,
non-T gate timing, routing, factories and error correction add obligations.
For example, even the illustrative data-only formula 2*d^2*Q at d=15 gives
296,689,500 and
1,047,992,400 physical qubits. These
distances are not justified for the enormous failure exposure, and factories
and routing are excluded. This is sensitivity analysis, not a physical design.

## First priority completed: independent validation

The focused test suite reports **55 passed, 3 warnings in 35.14s**. In addition:

- All four financial models were evaluated on 64 paired finite-input paths at
  each of two precisions: 512 development pairs, with all three strikes checked.
- Every emitted gate was executed for C4 and H8 at both precisions, before and
  after optimization: eight complete source executions. Outputs were bit-exact,
  inputs preserved and all scratch clean. Each used a nonzero residual case.
- Sixteen extra random cases per compiled source verified bit-for-bit agreement
  before/after optimization. Production-width arithmetic leaves were checked.
- Three complete high-precision angle circuits were executed. Thirty-six
  nontrivial finite spectral laws passed their promised test cases. An actual
  nine-qubit QPE statevector agreed with the independent distribution formula
  within 3.19e-14. Explicit QFT order and controlled-reflection sign were checked.
- Four combined financial/phase arithmetic traversals checked the final cleanup
  fusion at both precisions for C4/H8, with bit-exact angles and restored inputs
  and scratch. The diagonal phases were checked by their computed basis values;
  the enormous pricing statevector was not simulated.

The independent financial evaluator used NumPy/SciPy on the *same finite inputs*:

| Model | Fractional/random bits | Maximum absolute Y discrepancy over strikes | Maximum discounted baseline discrepancy |
|---|---:|---:|---:|
| C4 | 24/16 | 8.69e-05 | 9.67e-05 |
| C8 | 24/16 | 0.000158 | 8.13e-05 |
| H4 | 24/16 | 7.78e-05 | 0.000202 |
| H8 | 24/16 | 0.000374 | 0.000386 |
| C4 | 40/32 | 1.34e-09 | 1.53e-09 |
| C8 | 40/32 | 2.49e-09 | 8.92e-10 |
| H4 | 40/32 | 1.14e-09 | 3.41e-09 |
| H8 | 40/32 | 5.97e-09 | 6e-09 |

There were no sampled exercise-classification mismatches. These are development
diagnostics, not confidence coverage, tail/overflow proofs or held-out success.
No complete pricing QPE, noisy device or fault-tolerant machine was simulated.

## Second priority completed: cost and precision reconciliation

An independent audit recomputed gate counts from 324
distinct referenced gate files, checked their hashes/wires and reconciled the
forward/copy/inverse totals for the four final financial sources and the 64-bit
phase source. No hidden arithmetic leaf remains. All source calls and QPE powers
are explicit. The full logical ledger also lists outstanding synthesized-phase
and physical costs instead of filling them with favorable guesses.

Forty fractional phase bits failed the conservative accumulated error budget.
The separate 64-bit phase implementation fixes that issue: all 288 atan table
coefficients were verified by exact rational rounding intervals, and the derived
uniform phase error bound is 2.143e-16. This fits the allocated coherent
approximation failure for both the tight-moment and support-only schedules.
It does not certify the financial elementary functions or the finite-input law.
Single-qubit rotation sequences at the remaining per-rotation tolerance have
not been synthesized. Their count and error tolerance are recorded explicitly.

The inherited dollar budget remains .003 surrogate mean + .002 flat correction
+ .003 exercise regret + .002 financial numerical error = .01. Failure budgets
are .002 surrogate + .001 moment + .001 regret + .003 ideal quantum tests
+ .0005 phase-function error + .0005 rotation synthesis + .002 physical = .01.
Several terms remain obligations, so no completed 99% full-price certificate is
claimed. Finishing an audit is different from passing every obligation it lists.

## Claim ledger and next decision

| Claim | Status |
|---|---|
| Same compound financial research direction, existing policy/controls retained | Implemented; prior evidence preserved |
| Complete clean digital residual source and explicit estimator gate schedule | Implemented hierarchically; arbitrary phases specified, not synthesized |
| Correctness on the stated independent diagnostics | Executed; limits above |
| About 10% fewer source T gates and removal of redundant estimator cleanup | Quantum implementation improvements only |
| Tiny sampled f=40 financial arithmetic discrepancies | Observed; no global financial error guarantee |
| Uniform 64-bit complex-phase arithmetic bound within its allocation | Derived and coefficient rounding checked |
| Tight continuous moment/regret certificates apply to the digital source | Unproved |
| Full continuous-price numerical/statistical/physical certificate | Incomplete |
| Significant quantum advantage or supported physical crossover | Not established; current construction fails the resource gate |
| All possible quantum implementations of this contract are ruled out | Unsupported |
| Novelty or journal acceptance from this work | Not established; requires a separate review of the concrete claim |

The remaining work is ranked in [CHECKLIST.md](CHECKLIST.md). P1 and P2 are done.
P3 is a substantial reduction of the coherent cost within this same direction;
P4 is the financial bridge; P5 is synthesis/physical/full-price accounting; P6
is frozen confirmation and a supported manuscript claim. Larger variance pilots
or held-out sweeps are not the next useful step after this failed gate.

For the paper, the defensible current contribution is a reproducible feasibility
and resource analysis with controls and explicit failure/error accounting.
Publication would require a clear contribution beyond standard components and
independent technical review. These results cannot support an advantage title.
The existing manuscript has been left unchanged.

## Reproduce and inspect

[Code and commands](../../research/controlled_source_completion/README.md),
[derivation](DERIVATION.md), [checklist](CHECKLIST.md),
[final ledger](../../results/controlled_source_completion/cost_v3_phase64/ledger.json),
[validation records](../../results/controlled_source_completion/validation_v2/tests.json),
[full-source gate runs](../../results/controlled_source_completion/validation_v2/full_source_basis.json).
Initial versions, new development amendments, gate files, raw paired values and
previous experiments remain available. These artifacts complete the requested
investigation and checks; they do not fulfill the quantum-advantage objective.
