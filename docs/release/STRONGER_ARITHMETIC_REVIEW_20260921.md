# Stronger arithmetic study: review record

Date: 2026-09-21. These are independent AI reviews of specific mathematical and
implementation scopes, not human novelty assessment or journal peer review.
Authors of a component are not described as its independent reviewers.

## Primary source freeze

Commit `9511bc0c` freezes the workspace/range implementation and acquisition
protocol before the full menu is acquired. Existing journal-sprint producers
and historical evidence are unchanged. Commit `23f8d948` adds the separate
signed-residual implementation and protocol; it does not alter the first freeze.

## Reviews and corrections before acquisition

- Galileo reviewed the range-reduction mathematics independently of McClintock's
  budget implementation. Review covered signed shift rounding, repeated-square
  recurrence, the final spot factor and signed intermediate bounds. It also
  derived the signed-residual normalization and identified the negative residual
  witness that prevents direct reuse of the original unsigned payoff encoding.
- Zeno independently reviewed the primary runner. Recorded dependency versions,
  complete cap-failure rows, comparison against all primary arithmetic choices,
  and an exact archived-original-plan check address the substantive findings.
  Frozen dependency directories reject untracked Python modules. Primary case
  progress identifies the configuration if an unexpected exception aborts a run.
- McClintock independently reviewed Galileo's residual certificate and the
  residual component assembly. The review checked signed 96-bit products,
  48-bit intermediates, allocation, inverse/phase behavior, and the complete
  deterministic error ledger. The JSON tuple/list replay issue was corrected
  using type-sensitive canonical JSON comparisons. Negation of Decimal bounds
  uses exact `copy_negate()` rather than ambient-context rounding.
- Cross-interface review found an early p4-versus-g mismatch: the circuit now
  evaluates the certificate's complete g=(x+p4)/2 polynomial directly, with no
  second addition or halving. Certificate-backed circuit tests cover the exact
  implemented operation order.
- Galileo independently reviewed runner integration, offset restoration and
  finite diagnostics. Reported residual errors and bounds now use matching
  per-basket units. The residual-versus-reflection comparison is named explicitly;
  the separate overall decision includes primary arithmetic and preserves ties.
- Zeno independently reviewed the combined analysis/export and found no material
  blocker. The export retains all 148 primary and 18 residual configurations,
  including any failures, and does not enable physical/production selection.

Lorentz implemented separate verifiers with independent rational schedules and
integer resource composition. Those verifiers replay certificate producers and
therefore do not constitute independent mathematical derivations of every bound.
Their reported gate reconstruction scope distinguishes selected re-emission
from archive metadata and inherited conversion evidence.

## Final acquisition and replay

Both acquisitions completed: 148 primary layout rows and 18 residual rows, with
no certificate or cap failures in these menus. The complete suite passed 1,645
tests; the separate pinned environment passed the 315 overlapping new tests.

Primary replay checked every certificate, finite diagnostic, schedule and both
CX ledgers, and re-emitted four configurations across both layouts. Residual
replay checked all 18 configurations and re-emitted the two selected oracles.
An additional pinned reconstruction compared D1_28/D2_28 (the selected residual
parents) against their complete primary component records in both layouts,
with exact equality. This supplies selected-route evidence without claiming
that all menu gates were independently re-emitted. Receipts are linked in the
[results closeout](STRONGER_ARITHMETIC_RESULTS_20260921.md).

Final dispositions: Galileo found no mathematical-interpretation blockers;
Lorentz found no technical/evidence blockers within the stated scope. Both
checked the actual completed results and passing replay receipts. Final edits
clarified the direction of reported cost ratios and replaced pending replay
wording with the precise completed coverage. CSV/summary/input exports regenerate
byte-for-byte; 213 local documentation link targets resolve. No further code
changes followed the passing full and pinned test runs.

No human novelty assessment, hardware run, fresh confirmation, submission or
successful external Macroscope/Astra review is implied by this review record.
