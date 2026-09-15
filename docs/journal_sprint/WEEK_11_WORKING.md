# Week 11 working record

Started 2026-09-15 under the [revised plan](WEEKS_11_16_IMPLEMENTATION_PLAN.md).
Final status: week-11 development closed; see [closeout](WEEK_11_CLOSEOUT.md).
This working document preserves intermediate history, not submission readiness.

Continuation: the method-specific timing runner and gated reference/main runner
are implemented; pilot, references and main comparison completed and replayed.
Full regression passed 569 tests. See [results record](WEEK_11_RESULTS.md), the
[prior-work update](WEEK_11_NOVELTY_MATRIX.md) and prospective
[week-12 design](WEEK_12_DESIGN_MANIFEST.md). Sections below describing the first
increment are retained as its historical status, not the latest execution state.

## Implemented first increment

`research/journal_sprint/price_contract.py` adds a prospective, opt-in interface:

- Price target identifier/definition and currency; encoding offset/sensitivity.
- Exactly six named price-unit bias components, each with a bound or explicit
  unknown and provenance. Observed error is separate and never becomes a bound.
- Composition evidence and assumptions are mandatory. Bounds are caller-supplied
  assertions: metadata cannot verify a theorem, certify floating-point arithmetic
  or establish noise-model applicability.
- Unknown bias blocks the adapter into the existing `Encoding` planner. A bound
  below tolerance means only eligibility for statistical design, not successful
  delivery. A bound exhausting tolerance is a sufficient-screen failure, not
  physical impossibility.
- Explicit setup/pilot/two-calibration/pricing resource stages, separate shot,
  logical-CX and elapsed-time totals, no mixing measured and projected costs,
  and unknown propagation rather than zero substitution. Counts include failed
  attempts when preparing stage totals. Depth/qubits are not additive fields.

All six bias components must be represented even if zero. Zero needs an explicit
justification, such as no SDE discretization for exact GBM at contractual dates.
The caller supplies a compatible price-target telescoping/propagation argument;
the schema alone cannot detect double-counting or missing physical effects.
The numerical-enclosure term must account for relevant floating-point uncertainty.
No archived implementation, experiment or manuscript result was changed.

The interface has no true-price, exact-amplitude or pricing-observation input.
Tests check unknown refusal, observed-error independence, invalid/duplicate fields,
overflow, evidence requirements, cost-axis separation and adapter compatibility.
This is input-boundary protection, not a complete information-flow proof: caller
code and run manifests still need review to exclude ground-truth leakage.

## Prospective baseline protocol

Added [week-11 baseline protocol v1](PROTOCOL_W11_BASELINES_V1.md). It separates
128-row timing pilot, reference refinement and a capped main development matrix;
requires pilot feasibility review before larger acquisition; reserves candidate
held-out cases; and distinguishes approximate RQMC uncertainty from certification.
No baseline runner or new stochastic observations were produced in this increment.
The cent-to-dollar tolerance ladder is a transparent normalized research choice,
not a demonstrated institutional pricing requirement.

## Evidence and claim reconciliation

| Existing work | Classification | Permitted interpretation |
|---|---|---|
| Weeks 1-10 interval/calibration/circuit/replay work | Development and diagnostics | Conditional methodology and software checks; week-10 confirmation NO-GO retained |
| Exact finite-grid rescue | Development | Small-circuit resource improvement; exponential table, no quantum advantage |
| Encoding decision experiments | Development | Conservative sufficient planner with refusals |
| Equal-calibration allocation study | Development | 300/1080 versus 300/1080 fixed CP; no established improvement |
| Twelve Asian-basket benchmark cases | Development | Strong classical baselines; reference and timing limitations retained |
| Heston scalar screens/nested soluble toy | Diagnostic | Partial applicability tests/negative control, not quantum solvers |
| New interface unit tests | Software validation | Contract checks, not coverage/novelty evidence |
| Weeks 11-16 plan and new baseline protocol | Prospective | Planned tasks, not completed campaigns |

No existing result is promoted to confirmation. Existing dirty/untracked files
and archives were inspected and preserved; no bulk staging, commit or PR action.

## Remaining week-11 work

- Implement the interleaved timing runner and method-specific setup accounting;
  validate it before acquisition and run the bounded timing/memory pilot.
- Freeze affordable reference/main matrices based on that pilot, then refine
  references and run isolated development measurements.
- Audit the reserved candidate cases for prior exposure before confirmation use.
- Update the nearest-prior-work matrix with precise method distinctions; no new
  literature/priority verification was performed in this increment.
- Freeze week-12 effect criteria, repetition rationale and compute budget.
- Produce a week-11 closeout only when these tasks/gates have a recorded disposition.

## Verification

Initial targeted run: 76 passed (34 new contract cases plus existing encoding
and allocation tests), 2.97 seconds. Ruff passed both new Python files.
Full regression: `venv\Scripts\python.exe -m pytest -q` returned 538 passed,
11 upstream Qiskit warnings, no failures/errors/skips, in 287.69 seconds.
No stochastic benchmark ran concurrently. Local documentation validation checked
76 links; tracked diff and all four new files passed whitespace checks. Git
reported only its existing LF-to-CRLF conversion warnings. No new benchmark
performance measurement or scientific result follows from these test timings.
