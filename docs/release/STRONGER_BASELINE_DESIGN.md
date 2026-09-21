# Next bounded study: strengthen the arithmetic baseline

Status update, 2026-09-21: this proposal has been implemented as two separately
frozen studies. See the [results and qualifications](STRONGER_ARITHMETIC_RESULTS_20260921.md).
The text below preserves the original design; its proposed menu is superseded
by the executable protocols linked from that closeout.
This addresses the main open objection to the
[matched study](../journal_sprint/MATCHED_ARITHMETIC_RESULTS_20260917.md): expensive
unrecycled Horner arithmetic is not the best available arithmetic baseline.

## Fixed scientific comparison

Retain D1/D2, the exact archived Gaussian model coefficients, cutoff4, q10,
the arithmetic Asian-basket contract, $1 absolute error and at least95%
confidence. Retain the17-repetition AE convention and10-million-call cap.
Report both logical control ledgers and all allocated qubits; neither ledger
is hardware runtime. No E-case/confirmation seeds are opened by this design.

## Three separately testable changes

1. **Workspace reuse only.** Preserve the old integer arithmetic map exactly.
   Make live-register ownership explicit. Reuse a scratch word only after its
   complete state is demonstrably zero and unentangled for every valid input.
   Emit compute/copy/uncompute gates; do not replace their cost with a hypothetical
   recycled width. Compare depth/count tradeoffs as well as qubits.
2. **Range-reduced exponential.** Approximate exp(x/2^s), then square s times.
   Division of negative fixed-point integers needs a signed rounding allowance.
   Keep intermediate magnitude and floor-rounding bounds at every squaring;
   lower degree alone is not sufficient evidence of smaller total error/cost.
3. **Comparable residual/control strategy.** If a classical degree-four offset
   is used, bound its coefficients and expectation exactly as for reflection.
   A signed residual requires explicit normalization/shift, decoder and new
   scale/error accounting. Do not assume the positive-payoff selector encodes
   a signed residual. Account for computing and uncomputing the control too.

Do not combine all three immediately. Establish correctness of each change
against its parent, then test the combined route. Keep the old comparator and
reflection menu as versioned references rather than rewriting their sources.

## Required error argument before emission

For squaring stage j, suppose the exact nonnegative magnitude is at most B_j
and the implemented approximation differs by at most e_j. A usable recurrence
is `e_(j+1) <= 2*B_j*e_j + e_j^2 + u_j`, where u_j bounds that multiplication's
rounding. Bound both exact and approximate intermediate magnitudes and prove
signed overflow cannot occur. Include the final spot multiplication and affine
input quantization; scalar exp accuracy is not yet a full price budget.

Use directed arithmetic to propagate these terms through average/positive part,
normalization, loading, decoder and AE. Native synthesis and physical errors
remain unknown, not zero. A certificate failure produces an infeasible row.

## Freeze the executable menu, not just this intention

Proposed development menu: fractional bits20/24, widths40/48, Taylor degrees
8/12/16 and reduction exponents1/2/3. The existing40/20/24 unreduced implementation
is the reference. Validate the proposed menu's implementability, fixed resource
caps, exact source versions and test workload before signing the final protocol.
Any narrowed menu must be fixed before comparing cost outcomes and justified.

Primary outcome: minimum feasible **control-cancelled projected CX** per
contract, with conservative-ledger CX, qubits, depth, deterministic allowances
and AE query counts as secondary outcomes. Select on the complete declared
menu; retain all infeasible rows. Claim a benefit only against the corresponding
matched reference. Report ties and reversals, not only successful configurations.

## Acceptance and stopping criteria

- Exhaustive small signed-input tests against an independent integer reference.
- Phase-sensitive coherent checks of changed subcircuits, not basis values alone.
- Clean-workspace and full inverse checks; universal overflow certificates.
- Small finite targets and full continuous error ledger share one financial target.
- Actual emitted component counts; explicit extra recomputation caused by reuse.
- Separate pinned-environment replay and independent implementation review.
- One frozen bounded menu; no repeated post-result precision tuning presented
  as confirmation. Stop and document missing certification or resource-cap failure.

If arithmetic closes the gap or wins, report that result and revise the
encoding-aware decision. If reflection retains a benefit, the objection is
weaker but novelty, hardware performance and classical advantage are still
separate questions. Obtain human assessment before a confirmation campaign.
