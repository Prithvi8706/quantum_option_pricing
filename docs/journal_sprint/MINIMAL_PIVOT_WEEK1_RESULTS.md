# Minimal-pivot study: Week 1 results

## Outcome and historical status

The bounded Week 1 construction/resource study is complete. Same arithmetic
Asian basket; no contract pivot. There is a substantial circuit-component
improvement over our previous centered construction, not demonstrated quantum
advantage over classical pricing. Field-wide novelty remains provisional.

Historical weeks 13/14 were merged. Week 15 reproduction was completed, but
its confirmation campaign remained blocked. This study does not retroactively
unblock it. [Two-week plan](MINIMAL_PIVOT_STUDY_PLAN.md),
[derivation and claim boundary](MINIMAL_PIVOT_WEEK1_METHOD.md).

## Implemented contribution

The new shared-reflection signal realizes the centered basket with d+1 LCU
coefficient slots instead of the subset construction's 1+d*(2^d-1). On the
four-factor model that is **61 to 5 slots**, at the same centered scale
498.570187 (versus the original uncentered scale 698.570187).

This is not a new lower scale than our old centered method in these cases.
It is a less expensive realization of that scale, with a directed-interval
logical signal error certificate. Both competing baseline families received
the same consolidated-multiplexer optimization.

## Actual compiled component costs

U/CX basis, optimization level 1, fixed transpiler seed 717. q means bits per
Gaussian coordinate. Counts exclude probability loading, QSP/AE and physical
synthesis. Quoted comparisons are against our implementations, not a claim
to beat all published encodings.

| d,q | Optimized original CX | Optimized subset-centered CX | New reflection CX |
| --- | ---: | ---: | ---: |
| 2,1 | 21 | 44 | 37 |
| 2,2 | 37 | 76 | 69 |
| 4,1 | 82 | 636 | 154 |
| 4,2 | 146 | 1,148 | 282 |

At d4/q2, new versus optimized subset: **4.07x fewer CX** (75.4% reduction),
depth 1,753 to 383, and qubits 18 to 15. With one signal control, CX falls
8,202 to 2,132 (3.85x fewer) and qubits 19 to 16. A retained loss: at d2/q2,
controlled depth increases from the subset baseline's 915 to 963.

At production resolution d4/q10, the new signal was actually constructed
and compiled: **47 qubits, 65,562 CX, 49,175 U, depth 91,665**. It uses 16,384
marginal inputs, not an enumerated 2^40-path table. No 47-qubit statevector
simulation, complete pricing execution, hardware run or timing advantage is
claimed. The whole ideal logical signal operator-error upper bound is
1.6492655e-14 (rounded upward for this report); native transpilation and
physical synthesis are outside this certificate.

## Pricing diagnostics and adverse evidence

On the small d4/q2 finite distribution, exact classical enumeration gives
12.7682053323. The degree128 scalar polynomial gives 12.7380157776, bias
-0.0301895547. This is a scalar diagnostic, not a quantum execution result;
the finite target is not the continuous option price.

The ideal degree128 payoff-approximation envelope is 0.605222 for centered
versus approximately 0.848004 for original. This benefit was already available
in the earlier centered scale. It excludes the rest of the pricing budget.

The fixed-error CX-times-degree screen does NOT consistently favor reflection:

| Payoff-only tolerance | Original proxy | Reflection proxy | Interpretation |
| --- | ---: | ---: | --- |
| 0.7 | No degree <=128 passes | 36,096 | Degree-menu limitation, not advantage |
| 1 | 18,688 | 36,096 | Reflection loses |
| 2 | 9,344 | 18,048 | Reflection loses |
| 5 | 4,672 | 4,512 | Small coarse-tolerance proxy win only |

This proxy omits probability preparation, phase projectors, AE, synthesis
and statistical error. A smaller normalization alone is not enough to choose
the encoding. Retain both families in the encoding-aware decision rule.

## Evidence and reproducibility

Authoritative acquisitions under `results/journal_sprint/`:

- `minimal_pivot_week1_v2`: main grid, production compile, scalar diagnostics.
- `minimal_pivot_week1_subset_v2`: stronger centered-subset control.
- `minimal_pivot_week1_replay_v2` and `minimal_pivot_week1_subset_replay_v2`:
  separate existing pinned-environment repeats of those acquisitions.
- `minimal_pivot_week1_verification_v2.json`: all archived-source/artifact
  hashes and exact numerical-payload replay checks. No numerical fields are
  removed for comparison; timestamps/environment manifests are separate.
- `minimal_pivot_week1_full_tests_v2.xml`: final integrated test receipt.

Final integrated suite: **1,114 passed**, 12 legacy dependency warnings,
437.78 seconds. The 22 new focused tests also passed in the separate pinned
environment (overlapping coverage, not 22 additional distinct tests).
Ruff undefined/unused-name checks and Git whitespace checks passed.

The v1 acquisitions are preserved as preliminary development evidence; the
protocol records the stronger-baseline amendment. They are not confirmation.
Validation includes small full-operator checks, good-block algebra, involution,
controlled global phase, short complex QSP response, coefficient sign cases,
zero factors/branches, precision caps and structural scaling. This is automated
verification and author-side mathematical review, not independent peer review.

An additional d4/q2 statevector spot check used path basis words 0,37,128,255;
the largest projected-block discrepancy from direct basket evaluation was
3.331e-16. This is a four-input floating-point check, not exhaustive validation
or the proof of the interval certificate.

Reproduce with the pinned environment and single-thread BLAS settings:

Both checked environments used Python3.9.13, qiskit-terra0.46.3, numpy2.0.2,
scipy1.13.1 and pytest8.4.2. Dependency pins are in
`research/journal_sprint/requirements-week15-replay.txt`. Set
`OPENBLAS_NUM_THREADS`, `OMP_NUM_THREADS` and `MKL_NUM_THREADS` to `1`.

```powershell
venv/Scripts/python.exe -m research.journal_sprint.run_minimal_pivot_week1 NEW_MAIN_DIRECTORY
venv/Scripts/python.exe -m research.journal_sprint.week1_subset_control NEW_SUBSET_DIRECTORY
venv/Scripts/python.exe -m research.journal_sprint.verify_minimal_pivot_week1 NEW_RECEIPT.json
venv/Scripts/python.exe -m pytest -q
```

The verifier checks the named v2 acquisition/replay pair; producer output
directories and verification receipt must not already exist. The new signal
producer is `research/journal_sprint/reflection_centered_signal.py`.

## Week 2 decision

Proceed with the same problem and BOTH encoding alternatives. First integrate
the new signal with probability preparation, QSP, offset and estimation;
propagate stored-radius and logical/physical error terms. Then evaluate a
frozen fresh development/confirmation matrix and matched conditional RQMC
baselines, retaining failures. Do not open confirmation before its full error
and cost gates pass.

Paper candidate: certified resource-efficient centered basket block encoding
and an encoding-aware error/cost selection rule. A credible journal claim
requires the claim-specific novelty comparison, integrated validation and
appropriate independent review. W1 alone neither establishes classical
superiority nor makes the manuscript ready for a Q1 journal.
