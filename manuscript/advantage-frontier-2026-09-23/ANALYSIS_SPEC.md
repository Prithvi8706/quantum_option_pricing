# Prospective analysis specification — 27 September 2026

This specification starts a new, versioned **compiler-accounting stage**, after the
September 24 errata. Commit this file before executing this stage. It does not
retroactively preregister the September 23 investigation or freeze analyses that
have not yet been designed. Archived evidence remains unchanged.

## Stage A: Q1–Q3 and generic Q5

- Reproduce dependency-depth accounting for the archived C4_f40 and H8_f40 sources
  using the actual leaf bound to each call. Compare the cheapest/median operation
  scores on exactly those source targets. These are in-sample comparisons, not a
  general bracket theorem or a lower bound over quantum algorithms.
- Compile B4x12 and B8x52, with the existing September 23 `build` financial graph,
  Box–Muller midpoint uniforms q=32, f=40 and 72-bit words. Preserve its Estrin
  polynomial, prefix accumulation, spot guard and strict barrier comparison.
  Use existing exact constant folding/CSE, the generic primitive library and the
  truncated signed multiplier. Do not borrow compound-specific operand ranges.
- Charge constants, parameter-specific constant multiplication and the actual
  log/cos lookup tables. Archive optimized targets, bound leaf manifests and
  emitted primitive gates. New libraries live under the new output directory;
  never let a cache miss write into an archived library.
- Report clean source T-count, dependency T-depth, serial depth, and valid wave
  schedules with limits unrestricted, 128 and 32. Report logical width for every
  schedule and whether it fits 10,000/100,000 logical qubits. Those caps are
  diagnostics, not an implemented space-constrained compiler.
- Replay gates against exact integer IR on B4: 16 pseudorandom inputs plus all-zero,
  all-maximum, midpoint and alternating endpoints; B8: two pseudorandom inputs
  plus all-zero and all-maximum. NumPy PCG64 seed 2026092701, shapes in that order.
  Use nonzero XOR output registers. Replay every input on the serial and unrestricted
  wave implementations. Exact outputs, preserved inputs and zero restored workspace
  are required. Abort/report a mismatch; do not silently change the financial law.
- Check forward dependency depth <= half of clean wave T-depth, equal T-counts
  across serial/wave schedules, and valid source/leaf hashes. Equality of a
  node-specific score to that same compiled DAG is an accounting consistency
  check, not independent validation of an optimal circuit.

## Frontier interpretation

Use `barrier_decision.json` as historical context only. Its classical seconds are
modelled time-to-accuracy, its sigma is empirical, and k is a favourable unknown
constant rather than a proved 99%-confidence estimation schedule. For each shape
substitute the newly compiled clean-source depth into the same budget identity:
Q = k*sigma/(0.45*epsilon), D_max = T_C/(10*Q*t_layer).
Keep historical epsilon=0.001, k=3, t_layer=100 ns as the primary comparison and
the existing full epsilon/k/layer grid as sensitivity if recomputed. The source
omits the estimator, reflections, phase synthesis, error correction and routing;
its product with Q is a sensitivity estimate, not a hardware runtime prediction.
Preparation of uniform bits is counted separately as Hadamards; no free QRAM.

The stage passes when the frozen executions and accounting checks succeed,
regardless of whether their outcome favours either method. An implementation
that misses its budget does not disprove other circuits or establish a universal
obstruction. No claim of quantum advantage follows from passing this stage.

## Deferred work and deviations from the three-week sequence

The existing isolated, version-pinned Python 3.9.13 environment is used for this
bounded stage; archive its interpreter/package receipt. This **does not complete
T0** (a fresh hash-pinned environment) or Q0 (a fresh six-script provenance replay).
Those remain open. The September 24 provenance replay is prior evidence only.

Q4's 10,000-path independent floating-point bridge, rare barrier-flip bound and
continuous-law error budget remain open. Gate replay certifies the digital
implementation only. Q6 range specialization, Q7 alternative adders, Q8 matched
precision and Q9 an actual constrained-width schedule remain open.

Before C1–C8 or final X1 runs, commit a separate extension fixing fit windows,
whole-scramble bootstrap sampling, joint parameter uncertainty, reference agreement
and precision goals, coverage tests, and held-out selection. Do not call those
experiments preregistered by this document. No new classical fitting or choice of
favourable sigma is performed in Stage A. The 24 generated cases stay untouched.

The plan's fixed verdict is the current status, not a required experimental
outcome. If new evidence changes it, report that evidence rather than preserving
a negative finding by construction.
