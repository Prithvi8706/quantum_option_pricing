# Bounded matched arithmetic comparator protocol

Frozen before acquisition, 2026-09-17. Development only, not a new confirmation
campaign. Historical D1/D2 outcomes are already known. No claims of prospective
case selection, human expert approval, quantum advantage or publication priority.
Pre-freeze development includes unit tests and a D2 precision/overflow preflight
of `raw_plan`; no matched cost outcome has been acquired. The historical
reflection ledger was inspected in planning. This is a bounded development
protocol, not a blinded preregistration.

## Question and fixed menu

Does the standby reflection construction retain a lower *logical composition
projection* when the same pricing task is implemented with explicit conventional
arithmetic or Fourier aggregation? A ratio of projections is not a runtime
speedup or a bound on the ratio of actual costs.

- Contracts: exactly D1 and D2 from `run_minimal_pivot_week2.CASES`, including
  their spot, rate, maturity, Gaussian factors and strikes. No reserved E cases.
- Gaussian cutoff 4. Coordinates q=1 and q=2 for exhaustive finite-target
  diagnostics (4/16 D1 paths; 16/256 D2 paths). These are **not** substituted for
  the continuous price. Basis/circuit checks have separate smaller registers.
- Primary continuous comparison: q=10, absolute dollar tolerance 1, confidence
  at least 95%, canonical AE independent median with 17 repetitions, at most
  10,000,000 A/A-inverse calls. No tolerance sweep or post-result tuning.
- Arithmetic: signed width 40, fractional bits 20, Taylor degree 24, spot 100;
  coefficients and affine rounding from the existing directed `raw_plan`.
  Strip trailing zero Horner coefficients as the existing implementation does.
  Separately certify the signed post-strike difference; do not infer this from
  independent operand bounds alone.
- Two otherwise identical arithmetic routes: Cuccaro ripple sum and exact
  Fourier modular sum. Sum all price words, subtract d*K, positive part,
  compare a uniform integer selector with the payoff integer, and uncompute.
  Exploit the zero accumulator for both: ripple copies the first word then
  uses a modular adder omitting the unused highest carry; Fourier replaces the
  initial QFT on zero by Hadamards. Invert the actual shortened circuit for
  uncomputation. Test coherent action on the stated zero-workspace subspace.
  The selector encodes payoff probability exactly, avoiding an unpriced
  arcsine/square-root rotation. Overflow and selector width must be certified.
- Reflection: the archived q=10 degree menu 16/32/64/128, using the audited
  corrected IQFT-swap ledger, minimum feasible projected cost. Confirm the
  reviewed constant-sign correction does not change D1/D2. Finite diagnostics
  use the same scalar polynomial menu. Do not silently replace frozen sources.

## Comparable ledgers and verification

Both arithmetic implementations pay for affine Gaussian-to-log conversion,
fixed-point exponential, aggregation, payoff/selector, every inverse, common
Gaussian loading, AE control overhead, zero reflection, IQFT including swaps,
and explicitly allocated clean workspace. Build/count actual reversible
components rather than estimate multiplication counts from a big-O expression.
Component composition is not a simulation or optimization of the full circuit.
Reflection instead pays its own exponential marginal rotations and QSP/control
pipeline; it is not charged fictitious arithmetic price registers.

Use the existing ideal logical U/CX gate model: CCX decomposes to 6 CX and
9 U; one extra control on a U/CX stream is bounded by 2 CX per U and 6 CX
per CX. Include a controlled-global-phase allowance where relevant. Use the
same controlled clean-workspace zero reflection convention for all routes.
Also report, for every route, the standard control-cancellation implementation
`C(A S0 A-dagger) = A C(S0) A-dagger`: replace twice-controlled-A cost by twice
uncontrolled-A cost in each controlled Grover step. This secondary matched
ledger is fixed before acquisition, not selected after seeing the winner.
No physical noise, native rotation synthesis or fault-tolerant T budget exists;
these remain missing, not zero physical error. Mathematical exact Fourier
angles define the oracle; bound stored-angle deviation separately, without
calling compiler resource counts a native accuracy certificate.

Carry forward the same directed continuous representation allowance. Arithmetic
also pays its certified exponential/input-rounding error, state-preparation
operator error, Fourier angle bridge where applicable, and numerical decoding.
Use exact rational AE scheduling, outward bounds, and fail closed on overflow,
nonpositive remaining tolerance, query cap or missing terms. Finite-grid prices
computed in binary64 are diagnostics, not independent rigorous certificates.
Arithmetic's declared price decoder multiplies the ideal AE sin-squared label
by `decoder_scale = 2*beta_upper`. Assert its scale bridge and one multiplication
rounding fit the declared decoding allowance. Approximate numerical sin-squared
decoding and native execution would require separate certification.

Tests: exhaustive small aggregation basis maps (including modular wrap), coherent
phase-sensitive superpositions, compute/uncompute, arithmetic component clean
workspace and independent integer reference, complete small payoff-flag map,
schedule and ledger boundaries. For market-sized arithmetic, deterministic
endpoint basis checks plus universal analytic bounds, **not** a full statevector
simulation. Enumerate all small finite-grid inputs in the integer reference and
compare intended real payoff with the declared arithmetic bound.

Primary outputs: feasible/infeasible status, deterministic allowance components,
M and calls, total projected CX, qubits, and component breakdown for each route.
Report aggregation-only comparison separately. If either arithmetic budget fails,
report that failure without replacing parameters. No cost ranking among admitted
routes is promoted to best-algorithm or quantum-over-classical advantage.

## Stops, provenance and closeout

Stop at the fixed menu. Refuse unsupported cases rather than introduce joint
path tables. If explicit component acquisition is infeasible, retain the failed
receipt and identify the missing comparison; do not invent a full cost. No
hardware jobs, new confirmation seeds, financial trades or author outreach.

Hash protocol, source and input artifacts before acquisition; write outputs
exclusively and retain failures. Repeat in the existing isolated pinned research
environment, verify hashes and deterministic results, then obtain separate AI
mathematics/evidence and implementation reviews. Fix findings, rerun affected
checks, run the integrated suite, and record limitations before PR and merge.
AI review is not the still-pending independent human novelty assessment.

Primary constructions: [Cuccaro et al.](https://arxiv.org/abs/quant-ph/0410184),
[Draper](https://arxiv.org/abs/quant-ph/0008033), and
[Kim/Cui/Lee/Park's author-uploaded preprint](https://www.researchgate.net/publication/408635511_Scalable_Quantum_Derivative_Pricing_through_Fourier-Arithmetic_Payoff-Oracle_Design).
This is an implementation-specific comparator inspired by those constructions,
not a reproduction of their complete pricing implementations.
