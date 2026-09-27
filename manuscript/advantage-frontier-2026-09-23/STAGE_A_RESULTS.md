# Stage A results — 27 September 2026

**No defensible significant quantum advantage established yet.** This stage
closes the missing generic gate compilation and replay for the two knock-out
development cases. It does not close an end-to-end pricing or hardware comparison.
The generic emitted sources miss the historical latency budgets by more than
the earlier operation-table scores. This is evidence about this compiler and
these assumptions, not a lower bound on other quantum implementations.

## What was executed

The [prospective specification](ANALYSIS_SPEC.md) was committed as `b1a2bca7`
before execution. Both sources use q=32 midpoint uniforms, f=40, 72-bit words,
coherent Box–Muller generation, constant folding/CSE, Estrin exponentials,
generic exact leaves and the truncated signed multiplier. No compound-specific
operand-range certificate is borrowed. Costs include the financial source
forward computation, output XOR and inverse cleanup; uniform Hadamards are
reported separately. Gates, lookup tables, targets and bindings are archived.

| Case | Forward dependency T-depth | Clean scheduled T-depth | Clean T-count | Logical qubits | Uniform Hadamards | Basis cases passed |
|---|---:|---:|---:|---:|---:|---:|
| B4x12 | 1,671,555 | 6,032,678 | 907,483,318 | 550,158 | 1,920 | 20 |
| B8x52 | 1,670,595 | 6,393,144 | 7,458,042,774 | 4,460,490 | 14,976 | 4 |

Every basis case was executed on both the serial and unrestricted wave schedule
with nonzero output registers. Each matched the original and optimized integer
IR, preserved inputs and restored workspace. These are sampled basis checks,
not exhaustive verification or a certificate against a continuous financial law.

| Case | Parallel leaf limit | Clean T-depth | Logical qubits | Fits 100,000 logical qubits? |
|---|---:|---:|---:|---|
| B4x12 | all | 6,032,678 | 550,158 | No |
| B4x12 | 128 | 6,401,958 | 550,158 | No |
| B4x12 | 32 | 10,980,938 | 550,158 | No |
| B8x52 | all | 6,393,144 | 4,460,490 | No |
| B8x52 | 128 | 21,428,752 | 3,966,424 | No |
| B8x52 | 32 | 79,765,906 | 3,518,968 | No |

These schedules retain every SSA intermediate. Restricting concurrent leaves
does not implement storage reuse or a qubit-cap scheduler. Neither shape fits
10,000 or 100,000 logical qubits in any emitted schedule; this is not a width
lower bound. The dependency bound is for this fixed clean-leaf decomposition,
whereas wave depth is a valid all-to-all logical schedule. Physical routing,
factory capacity, error correction and decoder reaction have not been mapped.

## What changed in the cost evidence

| Source | Cheapest operation score / exact forward DAG | Median operation score / exact forward DAG |
|---|---:|---:|
| C4_f40 (archived range-specialized) | 0.6119 | 1.0772 |
| H8_f40 (archived range-specialized) | 0.6018 | 1.0725 |
| B4x12 (new generic) | 0.2647 | 0.6232 |
| B8x52 (new generic) | 0.2690 | 0.6270 |

The C4/H8 accounting reproduces the archived call-specific depths. It does not
validate an operation-table bracket on other circuits. Both scores undercount
the new generic sources. This comparison also changes the implementation of
leaves: it is not a matched study isolating only constant multiplication or
lookup costs. Range specialization remains a separate, unexecuted optimization.

## Historical-budget substitution, not a new end-to-end result

For epsilon=$0.001, k=3, e=0.45 epsilon and t_layer=100 ns, substitute each
unrestricted clean-source depth into Q=k sigma/e and D_max=T_C/(10 Q t_layer).
Sigma is the historical empirical standard deviation of the plain payoff.
Classical T_C is the unchanged September 23 fitted time-to-accuracy model,
including its disclosed first-chunk timing problem (ERRATA E5). It is not a
fresh warm measurement or a timed run delivering a certified $0.001 price.

| Case | Historical T_C (s) | D_max (T-layers) | Source-only QD t (s) | Miss of 10× budget | Layer time needed for 10× (ps) |
|---|---:|---:|---:|---:|---:|
| B4x12 | 5.8608 | 153.535 | 23028.1 | 39,291.8× | 2.545 |
| B8x52 | 27.1188 | 789.448 | 21961.5 | 8,098.2× | 12.348 |

A budget miss is ten times the modelled quantum/classical runtime ratio: do not
call it the slowdown factor. Picosecond entries are algebraic requirements at
fixed depth and hypothetical k, not physically supported clock assumptions.
Correcting the historical warm classical cost would tighten these budgets.
The archived sensitivity grid changes epsilon/k/layer and all three schedules;
it excludes preintegrated sigma because the compiled oracle computes the plain
payoff. No variance-reduced oracle is silently substituted.

The model still lacks an actual variance-sensitive estimator at 99% confidence,
certified moments, normalization, reflections/phase synthesis, the continuous-law
error budget, and physical resources. Q is fractional in this favourable model
rather than rounded into an executable schedule. T-layer timing assigns zero
latency to Clifford operations. The emitted Clifford-inclusive depths are also
archived; no hardware runtime is inferred from them. This is neither L1 nor a
complete L2 result, and it proves no classical or quantum complexity lower bound.

## Verification and review

- 254 frozen artifact hashes verified, including emitted gates.
- The executed producer and frozen specification match their receipt hashes.
- The maintained producer gained output-directory protection after the run began.
  Its scientific functions are AST-identical to the archived executed producer.
- The four existing parallel-schedule tests and two new accounting/archive tests
  passed; Ruff and diff whitespace checks passed.
- Independent AI review and dispositions are in [STAGE_A_REVIEW.md](STAGE_A_REVIEW.md).
  This is internal review, not external peer review or author verification.
- The existing isolated version-pinned environment was used. Fresh hash-pinned
  environment creation and the six-script clean replay are **not** claimed done.

## Checklist and next priorities

- [x] Inspect September 24 bottleneck changes and preserve historical evidence.
- [x] Commit this stage's prospective scope before running it.
- [x] Q1/Q2: exact C4/H8 dependency accounting and operation-score comparison.
- [x] Q3 accounting: bind actual node parameters/tables through generic compilation.
- [x] Q5 generic: emit B4/B8 sources, three schedules, planned basis replays and hashes.
- [x] Diagnose width and T-work; correct universal-negative and timing overclaims.
- [ ] T0/Q0: fresh hash-pinned environment and six-script replay, with timing separate.
- [ ] Q4: independent 10,000-path financial bridge, near-barrier stress cases,
      misclassification/bias bound and explicit discrete-to-continuous error allocation.
- [ ] C1/C2: prospectively freeze and execute rate uncertainty, warm/cold timings,
      and pricing runs at the required sample counts.
- [ ] C3/C4: independent reference prices and empirical confidence-coverage tests.
- [ ] Q6–Q10: range/precision/arithmetic sensitivity, actual width-constrained
      schedules and a consistent Clifford/physical-time model.
- [ ] Explicit estimator schedule and certified moment assumptions for an L2 claim.
- [ ] C5–C8: stronger classical arms, disclosed robustness cases and untouched holdouts.
- [ ] Final literature verification/novelty audit, harmonized frontier, LaTeX paper,
      clean-checkout release and full manuscript review; author/expert verification.

Next in dependency order: T0/Q0. The next scientific uncertainty to resolve is Q4:
whether this digital source approximates the stated barrier contract within the
allocated error, including rare barrier flips. Passing it would validate that
financial-law bridge, not the whole comparison or the cost crossover. No new
advantage direction was searched in this continuation.

## Reproduction

From the repository root, use the isolated Python interpreter:

```powershell
.context/controlled_closeout_repro/Scripts/python.exe -m research.frontier_completion_20260927.verify_stage_a
.context/controlled_closeout_repro/Scripts/python.exe -m research.frontier_completion_20260927.stage_a --output results/frontier_completion_20260927/replay_new
```

The producer refuses a nonempty output directory. Original execution details and
package versions are in [environment.json](../../results/frontier_completion_20260927/stage_a/environment.json).
The complete [summary](../../results/frontier_completion_20260927/stage_a/summary.json)
and [budget grid](../../results/frontier_completion_20260927/stage_a/historical_frontier.json)
contain unrounded numbers. CPU gate-simulation durations are reproducibility
metadata and are never treated as quantum hardware timings.
