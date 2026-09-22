# Independent final technical review

2026-09-22. Reviewed the new truncated multiplier and emitted-source evidence,
financial-law/control derivation, rotation library, conditional physical model,
and the final results/checklist/claim ledger and reproduction guide. This review
is independent of the authors of the arithmetic redesign, financial bridge and
synthesis/physical model. The reviewer implemented two small baseline compiler
fixes after reporting them; the coordinating agent separately reviews those
fixes. These are AI-agent reviews, not human referee reports or endorsements.

**No blocking scientific or implementation defect was found in the reviewed
P3/P4/P5 work under its stated assumptions.** The appropriate release is a
reproducible failed-feasibility investigation with partial certificates. It is
not a completed 99% continuous-price implementation, physical design, advantage
result, or novelty clearance. Clean-checkout release verification is recorded
separately below when completed.

## Findings and disposition

The baseline review identified the shared-CNOT copy-depth issue and Windows/
working-directory library-path dependence. Both were repaired, with flattened
gate-schedule and relocation regressions. Their scope and effect on historical
evidence are documented in [REVIEW_BASELINE.md](REVIEW_BASELINE.md). Historical
source snapshots and manifests are preserved; T-depth/count conclusions are
unchanged by the copy-depth correction.

The final integration review requested three small corrections:

1. The FT test file was renamed to `test_ft_checks.py`; the reproduction command
   must use that name. The corrected command was inspected.
2. The FT test's check of an archived ledger basename must normalize Windows
   backslashes before `Path(...).name`, so POSIX verification accepts the
   preserved Windows metadata.
3. The summary must distinguish the **interval certificate of each gate
   string** from the separate **high-precision signed controlled-phase
   diagnostic**. The 4-by-4 sign/wiring diagnostic is not itself a directed
   interval certificate. The exact adjoint and controlled-phase identities
   explain how the certified single-qubit errors compose.

All three corrections are now present and were inspected. Future FT metadata
uses POSIX separators, while its test also accepts the preserved Windows metadata.
The coordinating agent separately reviewed the compiler depth/path corrections
and their tests and reported no blocker. Clean-checkout verification remains a
separate release check below.

## Arithmetic redesign

The signed-product argument is valid for every `0 <= f <= w`. For unsigned word
representatives A, B and sign bits a, b, expanding
`(A-a*2^w)*(B-b*2^w)` leaves the two recorded sign corrections modulo `2^(w+f)`;
the cross term vanishes. Taking bits `f:f+w` is exactly signed floor division
modulo `2^w`, including negative products and wraparound. The endpoint cases
`f=0` and `f=w` satisfy the same argument.

The emitted implementation computes shifted partial products into distinct
scratch, adds the required low portions, clears each partial product, applies
the sign corrections, copies the output slice and inverts the computation.
Inputs and nonzero XOR outputs have the advertised semantics. The proof does
not rely on empirical input ranges or an absence of overflow.

The seven multiplier tests were independently rerun: **7 passed in 5.98 s**.
They exhaust small signed domains and exercise production-width edge/random
operands, output masks and inverses. The five new target JSON objects equal
their historical targets exactly. This supports transfer of the old digital-law
definition and phase approximation, but not transfer of continuous-model
financial moments or regret.

A separate fresh emission of all three production-width multipliers matched
their committed gate arrays and register mappings exactly: 46,664, 86,200 and
166,624 X/CX/CCX gates at widths 56, 72 and 96. This binds the reviewed generator
to the actual production leaves, independently of the artifact cache. The
[receipt](../../results/controlled_completion_followup/review_baseline_p3_binding.json)
records that additional check.

The artifact audit was rerun with its receipt redirected to the review's own
[output](../../results/controlled_completion_followup/review_baseline_p3_audit.json).
It verified all **895 historical artifacts and 25 preserved snapshot files**,
the five unchanged targets and **324 new leaf-file hashes/counts**. The new
financial T-count reductions are 1.905505/1.908652 for C4/H8 at f=40; scheduled
T-depth reductions are 1.730717/1.734879. The favorable source-only 1 ns figures
are 97.267769/838.032589 seconds. These miss both the stated empirical comparison
budgets and, for C4, the stronger fixed-iid 26.784-second tenfold budget.

The claims correctly attach this rejection to the specified implementation and
schedule. A valid schedule upper bound is not a quantum lower bound, and the
ideal unit-constant query coordinate is not an implemented estimator.

## Financial bridge

The singular first radial cell is integrated rather than treated by a false
uniform Box--Muller Lipschitz bound. The remaining radial-cell estimate follows
from monotonicity and a telescoping sum; the angular estimate uses the sine/cosine
Lipschitz bound and the finite radial expectation. Independence of future words
is justified because none of the four models splits a Box--Muller pair at tau.

The spot-tail/reset coupling pays for the original tail and the independent
future growth of the changed tau state. The finite/continuous path comparison
uses the Lipschitz property of guarded exponentiation. Nested conditional
expectation and the two positive-part maps contract the coupled L1 difference;
quantized histories need not reconstruct continuous histories exactly.

The virtual-Gaussian control comparison correctly includes both initial-state
and future-word discrepancies. Bounding the geometric put as a function of
mean log stock avoids a false global stock-coordinate Lipschitz claim. The
result is an average control-bias bound, not a uniform or exact conditional
identity; the reachable capped-state witness appropriately disproves the latter.

Joint baseline/residual cancellation uses the same decision and policy value.
Remaining arithmetic, final clipping, approximate discount and finite-policy
regret are explicitly separate. The low-precision witness disproves a uniform
bound at one reachable input; it does not prove a large expectation error. The
new summary preserves that distinction and does not convert small f=40
diagnostics into a certificate. The financial/FT cross-reviews provide additional
independent scopes in [REVIEW_FINANCIAL.md](REVIEW_FINANCIAL.md) and
[REVIEW_FT.md](REVIEW_FT.md).

## Synthesis and conditional physical accounting

All 95 magnitudes have exact rational/pi targets and reproducible directed
interval checks against their actual gate strings. The common tolerance gives
`2*N_R*epsilon <= 0.0005` for every recorded schedule. Multiplicities include
all three rotations in each controlled-phase decomposition, and exact QFT T
gates remain separately charged. The upgraded arithmetic changes neither the
phase target nor the estimator call count.

The phase conventions are sound: negative targets use full adjoints; execution
reverses the stored matrix-product order; and removal of global W factors or
replacement of the three unconditional P gates by Rz representatives changes
only the whole circuit's global phase. The inherited reflection sign is retained.

The factory recurrence is conservative under its independent stochastic-Z
premises: a union over triples bounds undetected input errors, while the
zero-error event lower-bounds acceptance. Retry counts count whole capped groups,
so an extra factor of the retry limit would double-count their exhaustion
probabilities. The critical-path recurrence and whole-machine idle exposure are
consistent with the deliberately serial execution and parallel factory siblings.

The empirical logical-error fit, primitive durations, accepted-input noise,
factory interfaces, routing capacity, controller reliability and decoder
throughput remain assumptions. Huge serial time estimates are conditional upper
bounds, not impossibility results. Null online-price costs remain outstanding.
The documentation correctly avoids claiming that synthesis alone closes P5.

The financial and FT focused suites were independently rerun together:
**20 passed in 67.95 s**. This includes every stored rotation certificate and
both signed controlled-phase conventions. These checks overlap the coordinating
agent's complete suite and must not be added as independent experiment counts.

## Claim and release scope

The quantitative results table, break-even coordinates and current checklist
reconcile with the new ledger. The strongest supported conclusion is that the
specified controlled coherent implementation still fails the acceptance screen,
despite a substantial exact circuit improvement, and that specific financial
and physical obligations remain. P3 is failed; P4 and P5 are partial; held-out
advantage confirmation remains ineligible. This matches the artifacts.

The existing manuscript has a different D1/D2 workload, one-dollar/95% contract,
finite Gaussian construction and ideal U/CX comparison. The follow-up does not
inherit that certificate. The paper/novelty assessment in the baseline review
supports a narrowly scoped feasibility report, with no promise of publication
or new primitive/theorem.

This review did not execute a full pricing QPE or physical circuit, formally
verify the numerical libraries, or establish a global financial arithmetic
certificate. Those limitations are part of the result, not hidden passes.

## Clean-checkout release verification

**Passed.** I inspected the completed
[receipt](../../results/controlled_completion_followup/release_validation/receipt.json)
and independently recomputed all six recorded log SHA-256 values. Every log
matches its receipt and every subprocess exited zero. The replay began from a
clean committed worktree at
`a0a95659ac6f833c475653fecddf8cd67b58a1d2` using a newly installed Python 3.9.13
environment with system/user site packages excluded. Qiskit loaded from that
isolated environment, not the original user's roaming site.

The replay passed **109 tests with three upstream Qiskit deprecation warnings**,
the preserved-archive/gate audit, all five complete source/phase executions,
all four fused executions, deterministic financial-bridge calculation and
updated FT calculation. The arithmetic replay took 131.69 seconds of CPU time;
this is a verification duration, not quantum performance. Recompilation changed
only new result paths/timing diagnostics inside the disposable checkout, as the
receipt explicitly records. Original evidence was retained.

I compared the tested commit with the release branch: the only later Python
addition in these two research packages is the replay harness itself. The
reviewed scientific source is unchanged. Later review text and validation
receipts do not change the compiled algorithm. Actual platform replay was on
Windows; POSIX path behavior is covered by the normalization regressions, not an
executed Linux replay.

All reviewer-requested corrections are resolved. **No outstanding technical
review blocker remains for merging this scoped feasibility report.** The
coordinator reports that the optional external Macroscope review did not run
because its credit balance was exhausted; it is not counted as a passed review.
The scientific limitations and unmet advantage/full-price gates above remain
unchanged by release approval.
