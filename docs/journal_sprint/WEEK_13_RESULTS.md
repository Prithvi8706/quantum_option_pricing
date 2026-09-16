# Week 13 results: validated finite Asian encodings, application gate blocked

2026-09-16. Producing freeze `e59782a71c3f79b117077807585888c226b49d67`.
Fixed [protocol](PROTOCOL_W13_ENCODING_V1.md); archive
[w13_encoding_v1](../../results/journal_sprint/w13_encoding_v1/planned.json).
Six cases, two representations, two loaders: all 24 compiled circuits completed.
No failed/unattempted cases, no shots, no hardware execution, no nonzero-Grover
experiment. This is development feasibility, not confirmation or advantage.

## Numerical outcomes

All prices below are USD for the specified discrete-monitoring GBM contract.
q is bits per independent normal, NOT total circuit qubits. The raw column is
the finite conditional-midpoint expectation. The residual column adds the
continuous-model analytic geometric-control mean. Raw and residual reconstruct
the SAME finite price only when the finite-grid control mean is used instead.
Each reference is beta1-control RQMC, 16 independent scrambles of4096 paths;
reported SE is across scramble means, not a certified absolute-error bound.

| Assets/dates/q | Raw grid approximation | Residual application approximation | RQMC control reference | Reference SE |
|---|---:|---:|---:|---:|
| 1/2/1 | 20.717663 | 10.911871 | 10.419941 | .000121 |
| 1/2/2 | 12.363241 | 10.481277 | 10.420005 | .000211 |
| 1/2/3 | 10.753461 | 10.427865 | 10.420140 | .000183 |
| 2/2/1 | 18.585163 | 10.338252 | 9.199579 | .000303 |
| 2/2/2 | 10.928719 | 9.333489 | 9.199481 | .000222 |
| 2/3/1 | 16.814463 | 9.436469 | 8.345202 | .000263 |

All six residual approximations are closer to their numerical references than
raw on this fixed small schedule. This is descriptive, not a theorem or an
independently confirmed improvement. In particular, residual errors against
reference are about$1.139 and$1.091 for2/2/1 and2/3/1: retain both failures.
The other residual discrepancies range from about$.00773 to$.49193, but do not
constitute certified tolerance delivery. Repeated dimensions have independent
reference scrambles; tiny reference differences are not contract changes.

This is the established geometric-control identity with beta=1, not a newly
invented algorithm. AM-GM makes its residual nonnegative for these equal positive
weights. A fitted beta>1 would require a signed-range audit. Both quantum and
classical arms receive the same control identity and analytic offset.

## Measured small-circuit resources and scale

Counts use u/cx, optimization0, no connectivity constraints; they are not
Clifford+T, routed or fault-tolerant counts. Circuit qubits include the flag.
CX counts below are for one forward A. Inverse A counts are also archived;
AE would additionally require repetitions and reflections.

| Assets/dates/q | Qubits | Table entries | Raw scale | Residual scale | A CX product | A CX dense |
|---|---:|---:|---:|---:|---:|---:|
| 1/2/1 | 3 | 4 | 44.374017 | 3.079955 | 4 | 6 |
| 1/2/2 | 5 | 16 | 74.805476 | 8.277430 | 20 | 30 |
| 1/2/3 | 7 | 64 | 92.442415 | 12.291759 | 76 | 126 |
| 2/2/1 | 5 | 16 | 39.783198 | 5.084127 | 16 | 30 |
| 2/2/2 | 9 | 256 | 68.811691 | 14.020197 | 264 | 510 |
| 2/3/1 | 7 | 64 | 37.032407 | 4.869673 | 64 | 126 |

CX totals coincide between raw/residual, but do not assume identical depth:
2/2/1 product raw depth24, residual32. In the9-qubit case, both have product
depth387 versus dense885. Loading alone is8CX product versus254CX dense;
the unchanged payoff table contributes256CX. Thus total forward CX drops
48.24%, but the payoff table now dominates. This comparison is against the
generic dense loader, not all competing quantum preparations.

Finite-grid payoff variance ratios raw/residual are254.44,362.41,436.90,85.18,
104.56,76.23 in schedule order. These are properties of the tiny finite tables,
not observed quantum-shot savings, universal variance ordering or novelty.
Per-scramble continuous-path sample variances are also archived as descriptive
statistics; Sobol paths within a scramble are dependent.

Maximum joint probability discrepancy was2.428613e-16, absolute1-fidelity error
2.220446e-15, inverse-return discrepancy2.664535e-15. Full-state overlap checks
relative phases up to a global phase. These floating diagnostics do not supply
rigorous synthesis/preparation-error enclosures or physical-noise bounds.

## Error gate and route decision

All12 representation contracts return `unknown_bias` and refuse admission to
the certification planner. The real-arithmetic tail/renormalization bounds,
evaluated in floats, are1.166185 for d2,2.242099 for d4 and3.303522 for d6.
Already these upper bounds exceed$1. Raw midpoint bounds range31.762080 to
290.223144; residual bounds51.826264 to347.093446. They are conservative upper
bounds, NOT lower bounds proving the actual error is that large.

State preparation, payoff arithmetic, rotation synthesis and numerical enclosure
remain unknown; the analytic offset's rounding also needs an enclosure. No
continuous-price certificate follows even where observed error is small.
The finite maximum scales in the table above require enumeration and cannot
be carried into a scalable arithmetic claim without a separate safe bound.

Decision: retain both finite encodings as week14 correctness/resource diagnostics,
with product loading preferred to the measured generic dense loader. Do not
promote any to certified continuous-price comparison or fresh confirmation.
The [structured arithmetic assessment](WEEK_13_STRUCTURED_ROUTE.md) gives
dimension/precision/error dependence and missing synthesized costs. The
[Heston/nested audit](WEEK_13_ALTERNATIVE_AUDIT.md) supplies no replacement
passing the gate. No silent route substitution or declaration of impossibility.

## Runtime, evidence and verification

The production archive spans28.214414seconds, including local persistence.
Recorded compile/statevector/inverse diagnostics total27.526965seconds;
table/model setup .006564seconds; shared RQMC references .233811seconds;
12 finite summation operations .000339seconds. Small wall-clock samples are
descriptive and host-specific, not benchmark confidence intervals. No simulator
time is reported as quantum-device time. All paths/tables/setup are charged;
direct summation already solves the finite target once its table is constructed.
Across six cases,96 scrambles evaluate393216 shared classical paths, not twice
that count for the two methods sharing each path.

Archive:104 files,269298bytes, with10 copied producer/protocol dependencies,
36 completed stage records plus matching starts, six complete case rows and
an immutable final manifest. Strict
[replay receipt](../../results/journal_sprint/w13_replay_v1.json) rechecked all
104files, six cases and24circuits in the producing environment. The separate
[stdlib audit](../../results/journal_sprint/w13_independent_formula_audit_v1.json)
recomputed covariance, cell masses, payoffs, offsets, moments, analytic bounds,
reference means/SEs and CX composition without importing the producer formulas.
It is not a second circuit simulation or numerical enclosure.

See [review dispositions](WEEK_13_REVIEW.md) and [closeout](WEEK_13_CLOSEOUT.md)
for final tests, independent-agent verdicts and week14 restrictions.
