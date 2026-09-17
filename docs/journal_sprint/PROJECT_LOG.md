# Journal reengineering: running record

## 2026-09-17: tighter approximation, centered signal and control-offset enclosure

Added bounded d<=4 centered subset LCU, discrete minimax candidate generation
with a separate directed-rounding/Markov uniform certificate, reusable directed
finite-model moments/control offsets, and a new fully archived acquisition.
Prior frozen producers/evidence unchanged; no hardware or remote writes.

Eight polynomial/phase candidates and16family/degree outcomes retained.
Degree128 payoff bound reduced1.672791->0.848004 dollars at original radius;
centering further reduces it to0.605222. Known q10 dollar-bound sum reduced
1.874862->1.050076(original/minimax) or0.807293(centered/minimax). Two unknowns
remain: signal implementation and execution; total_bound=None, no admission.
Product-loader state error<=2.05632e-13 and q10 offset rounding bounds<=3.20e-15
now included. q10 moments70terms/579exp/261120cell visits, reused acrossfamilies.

Cost tradeoff retained: original d4 B698.57->centered498.57 but terms5->61,
reflections16->128. Matched tiny d2/q1 signal-only CX206->1020. Not a full
controlled-circuit runtime claim. Original/minimax finite bias worsens to+$0.55215
despite improved uniform bound; centered/minimax bias-$0.03019, not confirmation.
Same classical controls remain strong and target a different exact finite estimand.

99focused tests passed before the last discount-bridge and verifier tests were
added. Independent agents reviewed mathematical components and runner before
acquisition. Separate-environment replay:15exact numerical payloads (named
timings excluded),74hash entries checked. Full/clean verification pending closeout.
See [results](NORMALIZATION_APPROXIMATION_RESULTS.md) and
[protocol](NORMALIZATION_APPROXIMATION_PROTOCOL.md).

## 2026-09-17: phase and separable-signal barrier development

Implemented new producers without changing earlier evidence: symmetric QSP
continuation with analytic Jacobian, directed interval Laurent phase-error
bounds, separable basket LCU/projected walk, and an unknown-preserving dollar
error ledger. The joint signal table is absent; marginal lookup still scales
as O(d^2*2^q). Product loading is separate and paid, not a joint StatePreparation.

All degrees8/16/32/64/128 passed the 1e-8 uniform phase gate; degree128 bound
5.51e-15. q10 original-model signal plan uses47qubits/16,384marginal entries,
not a compiled production circuit. Actual q2 signal:3,828CX; tiny integrated
degree8 product-loader/Hadamard circuit:16,488CX, discrepancy1.32e-14.

Safe ideal radius698.5702 versus old observed109.1852. Degree128 observed
finite-price bias+$0.04089; q10 partial known dollar bound$1.874862 with four
unknown implementation terms. Quantum controlled variance652.26 versus same
classical control18.26; no classical superiority or confirmation inferred.

57 focused mathematical/circuit tests passed before acquisition; runner failure
and no-overwrite test passed separately. Eight numeric payloads reproduced
exactly in the existing isolated week15 environment,52hash entries checked.
Initial interval-complex conjugation API failure was repaired before acquisition.
Full regression:964passed/12legacywarnings in423.32s. Five supplemental tests
were added after full-suite collection and passed in the final focused suite;
no subsequent full-suite rerun is implied.
Separate-environment final focused suite:63passed in14.58s, including four
replay-verifier tamper tests and a nonuniform q3 integrated loader check.
Supplemental q3 degree8 expectation discrepancy3.89e-15. Independent agent
reviews found no blocker for partial development scope; fixed-config and missing
contemporaneous model-input archival limitations are documented in results.
Post-acquisition model hex reconstruction is explicitly not an original snapshot.
Synthetic review also found a conservative future-run rejection mismatch:
dimensionless phase acceptance versus fixed dollar identity tolerance. Current
<6e-15 phase fits are unaffected; preserve frozen v1 and fix the next producer's
dollar-scaled allowance. This does not create false admission. F-only Ruff and
whitespace checks passed. No hardware submission or remote push/merge.
Clean checkout `6529472a`:63focused tests passed in15.88s in the existing
isolated week15environment; eight stored payloads/52hash entries verified again.
No full acquisition/regression rerun from that checkout. Clean receipts saved
as `barrier_clean_tests_v1.xml` and `barrier_clean_replay_check_v1.json`.
See [barrier results](BARRIER_DEVELOPMENT_RESULTS.md) and
[frozen protocol](BARRIER_DEVELOPMENT_PROTOCOL.md).

## 2026-09-17: bounded integration of representation/QSP/reuse proposals

User authorized all-three development and broader Quantum Week research. Added
actual Fourier-sampling feature circuits, full-pool classical competitors,
finite-table QSP payoff circuits, coherent signed-control LCU smoke test,
MPS compression diagnostics and fair setup-reuse ledgers. No old producer edit,
hardware submission, confirmation, remote push/merge or paper-advantage claim.

Stage1:95representation records,180LCUvariance screens,5strikes,2QSPdegrees.
Every LCUscreen was worse in Hadamard variance than its raw comparator; the
actual16path composite circuit was correct within2.59e-11 but normalization
grew1.937x. Quantum Fourier selection did not beat strong geometric/greedy
controls on the center case. All6numeric Stage1payloads replay exactly in the
existing isolated week15environment, excluding timings;32hashes checked.

Explicit adaptive follow-up: subtract degree4polynomial control BEFORE QSP
normalization; compute/reuse finite-model basket moments through70multinomial
terms. At strike100, degree8/16gave370.69x/127.96x lower ideal Hadamard price
variance than raw QSP, with identical per-shotCX counts and identical polynomial
bias. Classical controls also improve strongly. Degree32residual phase fitting
failed; every attempt/cap retained. No continuous accuracy or classical speedup
inferred from this finite256path experiment. MPS circuit remains unimplemented.

Twenty focused tests passed before follow-up acquisition. Full regression
906passed/20legacywarnings in378.42s. Follow-up replay reproduced all5numeric
payloads exactly, including failed phase-fit attempts (timing excluded), and
checked34hashes. Total66source/artifact hash entries checked across both replays.
Clean checkout of implementation commit `1f140c3d` in the existing isolated
week15 environment: 20 focused tests passed (8 legacy warnings, 13.96s), and
both archive replay checks passed again (11 numeric payloads, 66 hash entries).
The clean-checkout run did not repeat full regression or acquisition. Its three
receipts are `combined_clean_tests_v1.xml`, `combined_clean_replay_check_v1.json`
and `polynomial_residual_clean_replay_check_v1.json` in `results/journal_sprint`.
F-only Ruff and whitespace checks passed. No independent scientific/subagent
review claimed. See
[complete results](COMBINED_DEVELOPMENT_RESULTS.md),
[bounded protocol](COMBINED_DEVELOPMENT_PROTOCOL.md), and
[adaptive protocol](COMBINED_FOLLOWUP_PROTOCOL.md).

## 2026-09-17: table-free raw arithmetic confirmation-unblock attempt

Implemented reversible signed fixed-point affine/Horner/raw-call/comparator
gates with clean uncompute, explicit overflow/error bounds and an ideal
controlled-RY Gaussian loader error enclosure. Original frozen producers and
week13-15 evidence remain unchanged. Forty focused tests passed before the
large audit. Initial unit-test failures were repaired before acquisition.

Original two-asset/two-date candidate, L4/q10/f24/w40: actual emitted payoff
program3,637logical qubits,10,102,977X/CX/CCX gates, depth1,597,792. Prospective
ideal representation bias<=0.203585334 dollars, arithmetic<=0.001514075dollars.
No path payoff table was constructed. This is not full hardware compilation,
validated PriceContract, physical error certificate or a quantum-advantage result.
Large initial basis checks passed. Separate week15-environment regeneration
reproduced plans, loader angles, all10,102,977gates/hash/resources exactly; an
additional true-flag case passed with all workspace clean. Final focused suite
41passed/8legacywarnings in10.74s in that existing isolated environment.
Full regression886passed/20legacywarnings in426.78s. Subsequent test-only cleanup
removed three unused imports; the final isolated41test run covers that cleanup.

Same continuous business contract:96development classical repetitions across
three methods/two sample budgets plus three separately recorded1024path pilots.
At4096paths, conditional RQMC/control replicateSD0.00031465 across16scrambles.
No certified interval/continuous truth or unit-mismatched speedup claimed.
All96prices, pilot values, identities and summaries replay exactly in the
separate environment, excluding timing fields. F-only Ruff check and staged
whitespace check passed. Producer hashes are protected against newline conversion
in new files; no old frozen producer was edited.
Local implementation/evidence commit dfb3e690. Clean checkout of that commit
passed41focused tests/8legacywarnings in8.48s using the existing isolated week15
environment; all21source-hash entries and11artifact-hash entries matched.
This last check did not repeat the full886suite or large gate regeneration;
those are the separately recorded successful checks above.

See [results and review packet](REVERSIBLE_ARITHMETIC_RESULTS.md),
[construction protocol](REVERSIBLE_ARITHMETIC_PROTOCOL.md). Confirmation remains
blocked on integrated scientific/cost/statistical review and a defensible fixed
primary claim; actual collaborator sign-off cannot be fabricated. No new PR,
remote push/merge, human review or independent subagent review claimed.

## 2026-09-16: confirmation-gate numerical development

User requested work toward unblocking confirmation. Kept the existing Asian/PCA
route and original evidence. Implemented80digit directed interval primitives,
sharper tail/conditional midpoint bounds, a Gaussian mean/covariance rounding
bridge, analytic-control offset enclosure and non-enumerative safe normalization.
Opt-in screening still preserves unknown implementation components and refuses
admission. No novelty, full certificate, human sign-off or confirmation claimed.

Frozen producer/protocol e38ee513;38focused tests passed before acquisition.
Final full regression845passed/20warnings in380.26s. Clean source checkout52357dac
passed38newtests in15.76s and exact49file/576row replay using the existing isolated
week15 environment. No producing-code changes after freeze.
Deterministic audit completed/replayed576rows/49files, no sampled prices or
failed cells. For two assets/two dates atL4, the partial$0.25screen moves raw q13
under the old float expression to q10 under the new bound (52to40normal bits),
but still implies2^40entries for a table oracle. Non-enumerative safe scales
483.835(raw)/237.184(residual) expose a much smaller normalization benefit than
the coarse table. These are bounds/candidate sizes, not implemented circuits.

Prepared [remaining unlock plan](CONFIRMATION_UNLOCK_PLAN.md), including exact
zero-event denominator examples and unresolved inference/novelty/human gates.
See [derivation](CONFIRMATION_GATE_BOUNDS.md) and
[results/verification](CONFIRMATION_GATE_BOUNDS_RESULTS.md). New work remains
local; no fresh independent subagent review or remote merge claimed this turn.

## 2026-09-16: week15 reproduction complete; confirmation blocked

PR#4 merged weeks13-14 atd5e1c3f2 after independent Bacon/Darwin acceptance,
807fresh full tests and both replays. User authorized week15 start-to-end with
review/merge, but its scientific gate remains NO-GO. Executed the explicitly
permitted fresh-environment reproduction and blocked-confirmation fallback;
did not invent a held-out campaign or silently replace the application.

Protocol e9c673ef; installer amendment/source checkout958a7a9c. New isolated
Python3.9.13 environment,22matching pins, module paths inside new prefix,
pip check0. Fresh123tests passed/17warnings in44.37s; strict week13 replay
104files/6cases/24circuits and week14 replay2022files/93tasks passed. All6scalar
formula cases passed and all58analysis cells exactly reproduced. Both original
archives remain intact. Raw installer logs preserved and losslessly ZIP archived.
Independent Bacon software/provenance and Darwin scientific/claims reviews
ACCEPT at7ce21101. Darwin independently reconciled96ideal fixed intervals and
all six rate numerators/denominators across50confidence cells; main's separate
tracked-only checkout verified11artifact files and both ZIP-member hashes.
No algorithm, original seed, tolerance or producer-source change. This is new
environment reproduction on the same host, not confirmation or a new proof.
See [week15 closeout](WEEK_15_CLOSEOUT.md), [protocol](WEEK_15_REPRODUCTION_PROTOCOL.md)
and [independent review](WEEK_15_REVIEW.md) for final dispositions/merge status.
The original confirmation milestone remains incomplete; week16 remains planned.

## 2026-09-16: new independent weeks13-14 premerge review

User now authorized review and merge, superseding earlier local-only handoffs.
PR#4 includes both weeks13and14. New independent reviewers Bacon and Darwin
accepted implementation/provenance and scientific claims respectively, with no
blockers for finite-target development. Fresh full suite807passed/20warnings,
389.99s, and both archives strictly replayed (104+2022files). Macroscope skipped
because credits are exhausted; no hosted-CI or human-review pass is inferred.
See [merge review](WEEK_14_MERGE_REVIEW.md) for exact scope/checks. Scientific
week15 confirmation gate remains NO-GO regardless of merge readiness.

## 2026-09-16: week14 finite-target development completed; confirmation held

User requested full week14 work and independent subagent reviews. Followed the
week13 gate: no continuous-price encoding was admitted, so the executable scope
is finite-target development, not a completed continuous end-to-end benchmark.
Producer/protocol76914458; all93tasks completed,912trial outcomes (including
paired analyses),20response checks,2022files/2399090bytes,21.931956s elapsed.
Strict replay passed all files/tasks;58cell prespecified analysis generated.
Full807tests passed in two disjoint invocations; clean checkout1fbea8b6 passed
72newtests and strict replay with the same pinned environment. Independent
scientific and software evidence reviews ACCEPT; four wording corrections
applied. Complete review receipts are recorded in the linked closeout/review.

Added actual nonzero-Grover raw/residual circuits, independent density checks,
native IQAE and source-faithful noisy csAE, fixed/direct and five-policy ablations,
finite classical/direct-sum baselines, explicit resource and failure accounting.
Maximum response discrepancy2.254e-14. Residual scale reduces finite-target effort
for classical and quantum estimators. EqualA direct/multidepth delivery ties;
multidepth costs1.9times CX. Ignored-noise residual multidepth yields12empty
sets and15/16hull misses, all retained. No quantum advantage or new algorithm.

Independent pre-acquisition findings fixed: nested-manifest inventory bypass,
unenforced native pin, csAE checkpoint durability, depth conventions and coverage
denominators. Main integration also corrected the Grover constructor, checkpoint
failure propagation and a fixture-detected analysis category collision, all before
production. Final review/clean-checkout receipts are in
[review](WEEK_14_REVIEW.md) and [closeout](WEEK_14_CLOSEOUT.md).
Human review packet prepared, not sent/signed. Continuous unknown_bias and
prior-work distinction remain unresolved; week15 NO-GO. Two planned blocks
remain (weeks15-16), gated. No remote push/PR/merge; unrelated local work preserved.
See [results](WEEK_14_RESULTS.md) and [claims/gate](WEEK_14_CLAIMS_GATE.md).

## 2026-09-16: week-13 development completed and independently reviewed

User requested full week13 completion followed by independent subagent review.
Implemented simulator-feasible Asian raw/beta1 geometric-residual encodings,
product/dense loaders, explicit finite-versus-continuous offsets, componentwise
unknown-preserving price contracts and durable per-stage provenance/replay.
Hooke independently checked formulas; Euler found and verified fixes for five
software/provenance/audit issues before production. Ampere supplied the bounded
Heston and signed nested-Asian exposure audit. No alternative was silently promoted.

Frozen producer/protocol `e59782a7`; final pre-acquisition focused suite51passed.
Fixed study completed6cases/24circuits in28.214414s, no failed/unattempted cases,
no shots or hardware run. Strict replay verified104files/all24circuits, and a
separate stdlib audit recomputed all six cases. Nine-qubit total CX510->264 with
product loading, residual scale68.811691->14.020197. These are small encoding
improvements using known identities, not a new algorithm or quantum advantage.

All12 application contracts remain unknown_bias; no$1 certificate. Two coarse
residual approximations still differ from numerical references by more than$1;
all are retained. Product loading leaves the exponential payoff-table bottleneck.
Final independent scientific and software evidence reviews both PASS, with no
remaining blockers in scope. Full final regression735passed,11legacy warnings,
355.00s. Separate clean source checkout8dc3f8fe passed51newtests in24.96s and
strictly replayed104files/24circuits using the same pinned environment. New-source
Ruff/whitespace checks passed; producing code/original evidence unchanged.
Three planned blocks remain (weeks14-16), subject to their scientific gates. See
[results](WEEK_13_RESULTS.md), [review](WEEK_13_REVIEW.md),
[closeout and handoff](WEEK_13_CLOSEOUT.md), and
[structured route](WEEK_13_STRUCTURED_ROUTE.md). No remote PR/push/merge this turn.

## 2026-09-16: week-12 development completed, negative gate retained

User requested complete week 12, separate subagent reviews and merge. Producing
freeze `9a97228a`; 104 focused/684 full tests passed before production. Reviewers
Dalton and Carver independently identified statistical/software blockers, corrected
before launch. Full dispositions include test pilot-v1 exposure and fresh pilot-v2
amendment; no policy/threshold tuning on production results.

Pilot-v2 completed/replayed 90 rows, projection 1244.864s passed. Main completed
all 7400 rows (2000 primary +5400 secondary) in 150.700 acquisition seconds,
297.210s including automatic replay. Verified 7721 files and every event/row;
independent audit covered 185 cells, 413,220,864 shots and 31,338,155,520 modeled CX.
Zero unattempted/failed/unresolved production attempts; statistical refusals retained.

Primary unequal-target and cost-aware fixed target both delivered 400/400 at
8192 shots. Saving versus full-budget CP was 87.5%, but saving versus fixed target
was zero: predeclared interest gate FAIL. Secondary target delivered 182/1080,
fixed-target 240/1080, other arms 300/1080. One target primary interval missed;
no >$1 erroneous declaration observed. Zero events do not prove zero risk.
No quantum advantage or confirmation promotion. Final separate-agent evidence
reviews found no remaining blockers with these qualified claims.

See [results](WEEK_12_RESULTS.md), [closeout](WEEK_12_CLOSEOUT.md),
[reviews](WEEK_12_REVIEW.md) and [handoff](WEEK_12_HANDOFF.md).
All 7928 evidence files are bundled losslessly; immutable manifests and original
archives preserved. Clean-checkout verification and authorized PR/merge follow.
Four planned weeks remain, beginning with week 13 quantum encoding/preparation.
Separate source checkout `02a369bd` subsequently passed 684 tests, 11 legacy
warnings, in 345.56s; strict replay rechecked all 7400 rows/7721 files and the
preserved pilot gate. Independent 185-cell audit and 327 local documentation
links passed. Full proposed-source/ZIP credential-pattern review flagged no issues.
Tracked trees stayed clean apart from these intentional verification notes/reports;
no producing code or original evidence changed. Ready for the authorized PR merge.
Published as [PR #3](https://github.com/Prithvi8706/quantum_option_pricing/pull/3);
the PR records the server-side disposition/merge commit. Separate reviews and
clean-checkout verification support integration, not the failed method claim.

## 2026-09-16: week-12 policy foundation started

No newly raised PR comments/inline reviews or open GitHub issues were found after
the PR #2 merge; Macroscope remains skipped. Created branch
`research/week12-unequal-calibration`. Added the five-arm policy specification,
unequal-calibration batch planning and fresh terminal CP adapter without modifying
historical producing modules. The forecast is explicitly heuristic; the documented
conditional containment argument requires fresh binomial samples and valid bias/
transfer bounds. No benefit or coverage guarantee beyond those assumptions claimed.

53 new tests pass, including independent unequal-count binomial endpoint checks,
old-arm equivalence, no-pilot fixed-arm inputs and budget/fallback behavior; Ruff
passes. Full regression: 633 passed, 11 legacy Qiskit warnings, 302.60 seconds;
`results/journal_sprint/tests_week12_policy_v1.xml`. No experimental observations or paid jobs
launched; acquisition/replay infrastructure is the next gate. See
[week-12 working record](WEEK_12_WORKING.md) and
[policy specification](PROTOCOL_W12_POLICY_V1.md). Week 12 is in progress.
Stage-A changes remain local and uncommitted; no push or new PR. Bytecode writes
were disabled for regression, and historical producing sources remain unchanged.

## 2026-09-16: PR #2 pre-merge sweep

User requested full verification, merge and a checklist. Tested exact PR source
`0796cb744375fac614c565a8f64fa8420c05b60d` in a separate checkout: 580 tests
passed, 11 legacy Qiskit warnings, 381.48 seconds. Existing Python environment
reused; no fresh-install or timing-performance claim. Full ZIP/member integrity,
bounded credential-pattern review, changed-Python Ruff, independent week-11
events/counts and 144-cell arithmetic checks passed. No Macroscope approval is
claimed: its PR check was SKIPPED and there were no review comments.

The historical encoding-v1 strict replay rejects changed live source, and its
frozen verifier reproduces the documented nested-manifest bug. A supplemental
frozen-producer audit verified all 1080 rows and hashes without changing evidence;
the corrected v2 verifier passes. No new implementation fix was required. Corrected
stale forward-plan status to week 12 next, five blocks remaining. Added the
[integration and remaining-work checklist](PR2_MERGE_CHECKLIST.md). Original
archives, unrelated files and the six-edit stash remain untouched.

Final replays completed: week-11 main 2308 rows/2415 files and references
384 rows/490 files; pilot, week-10, rescue, corrected encoding, allocation,
shortlist and confidence-sequence reanalysis also passed. Timings are not
reproduced. Integration decision: GO for the explicitly authorized PR #2 merge;
the linked PR retains the server-side merge event/commit. Quantum novelty,
advantage, confirmation and submission gates remain open. No producing-source
changes followed the tested commit; this sweep adds only docs and reports.

## 2026-09-15: weeks 10-11 integration packaging and verification

Packaged implementation, protocols, results and prospective week-12 design in
candidate commit `cf2db2504bc281cf6de5e357aa36d038f9d4ef24`. A lossless ZIP and
per-file SHA256 index retain 3708 evidence files, including failed/superseded
attempts, without rewriting producer manifests. Added a safe extractor and 11
tests. Excluded local environments, private configuration, downloaded papers and
unrelated outputs/plans; preserved the six-edit user stash and original archives.

A separate source checkout passed 580 tests with 11 legacy Qiskit warnings in
312.85 seconds using the existing Python environment, not a fresh installation.
Bundle extraction, 132-row pilot replay, 3240-row allocation verification and
298 local documentation links passed. Tests regenerated pre-existing tracked
bytecode in the disposable checkout only; no source differences. Bounded
credential-pattern and archive-integrity checks found no flagged issues.
See [integration handoff](PR_WEEKS_10_11_HANDOFF.md) for reproduction and limits.
Published as [PR #2](https://github.com/Prithvi8706/quantum_option_pricing/pull/2)
on branch `research/week10-evidence-gate`; opened for review, not merged.
No quantum advantage or submission readiness is asserted; week 12 is not executed.

## 2026-09-15: week-11 baseline acquisition continuation

Implemented method-specific setup, interleaved/fresh-training deployments,
durable attempt accounting, telemetry, source/protocol/environment snapshots and
separate pilot/reference/main gates. See [results](WEEK_11_RESULTS.md).
39 focused stage-A/shortlist tests and seven stage-B/C tests passed before
acquisition; Ruff passed after a pre-run line-length correction.

Pilot `w11_baseline_pilot_v1`: 128 measured rows plus four warmups, replayed
132 rows/234 files. References `w11_references_v1`: 384 estimates, 32 per contract,
12,582,912 reference evaluations plus 393,216 training evaluations; SE range
.00003506-.00006125 passes the predeclared diagnostic. Replay checked 384 rows/
490 files before main acquisition. Main `w11_main_v1`: 2304 measured comparisons
plus four warmups, all complete; acquisition 557.6676 seconds. Replay verified
2308 rows/2415 files. Independent raw-row post-processing checked 144 RMSE/cost
denominators (max RMSE discrepancy 4.663e-16). Two read-only audit-command issues
were corrected without changing/rerunning any acquired data. No concurrent
agent-launched test/benchmark during acquisition; external load remains a limit.

Full regression: 569 passed, zero failures/errors/skips, 11 upstream Qiskit
warnings, 277.76 seconds (`tests_week11_v1.xml`). Regression and main replay ran
concurrently only AFTER acquisition; their times are not performance evidence.
Ruff passed all seven week-11 Python/test files. Final documentation checks passed
116 local links across 11 documents and whitespace validation (only Git's existing
line-ending conversion warnings). See [week-11 closeout](WEEK_11_CLOSEOUT.md).

Refreshed the [quantum prior-work matrix](WEEK_11_NOVELTY_MATRIX.md) with explicit
reading depth and prepared the prospective [week-12 manifest](WEEK_12_DESIGN_MANIFEST.md).
Added a fifth cost-aware fixed-design comparator before any week-12 observations,
so future gains cannot rely solely on beating a baseline that exhausts its budget.
Clarified the active roadmap: the primary goal remains a quantum-centered resource
result; the statistical decision rule supports it rather than replacing it.
These classical measurements and supporting allocation plans do not establish
a quantum algorithm or advantage. No asymmetric trial, paid hardware, human
review, external assignment, commit, push, PR, merge or submission performed.

## 2026-09-15: week 11 started — shared contract and baseline protocol

Implemented the opt-in `price_contract.py` interface and focused tests; archived
encodings and experiments remain unchanged. Requires explicit componentwise
price-unit bias/provenance, preserves unknown bounds, blocks unknown-bias planner
inputs, separates observed error from bounds, and accounts for all acquisition
stages without mixing cost units or measured/projected evidence. These checks
do not prove supplied bounds, noise assumptions or absence of caller-side leakage.

Added the prospective [baseline protocol](PROTOCOL_W11_BASELINES_V1.md) and
[week-11 working record](WEEK_11_WORKING.md), including evidence classification,
staged compute gates, stronger references, interleaved timing, approximate RQMC
uncertainty and reserved candidate held-out cases. No new stochastic benchmark
or quantum experiment has run. Week 11 remains in progress; its runner, reference
measurements, novelty update and week-12 manifest are still outstanding.

Initial targeted validation: 76 tests passed in 2.97 seconds, including 34 new
contract cases; Ruff passed both new Python files. Full regression command
`venv\Scripts\python.exe -m pytest -q`: 538 passed, 11 upstream Qiskit warnings,
no failures/errors/skips, 287.69 seconds. Checked 76 local documentation links
and whitespace in the tracked diff/new files. No paid jobs, author assignments,
external reviews, commits, pushes, PRs or submissions.

## 2026-09-15: revised remaining six-week implementation plan

Added the active [weeks 11-16 plan](WEEKS_11_16_IMPLEMENTATION_PLAN.md) and linked
it from the original research report and master checklist. Weeks 1-10 remain
recorded development work; the post-week-10 discovery work is reused without
being relabeled as completed confirmation or later-week closeouts.

The revised sequence is: error/resource contract and strong classical references;
unequal-calibration tolerance-delivery policy; bounded Asian encoding and state
preparation; matched comparisons and novelty gate; fresh confirmation; manuscript
and submission-readiness review. Heston and genuinely nested pricing receive
bounded feasibility audits, not promises of two additional complete solvers.
Every stage has deliverables and explicit go/no-go criteria. The original reserve
is retained; a failed research gate is not silently converted into completion.

This turn changes documentation only. No experiments, asymmetric allocation,
new quantum circuits, human reviews, submissions, commits, pushes or PR actions
were performed. The 504-test result remains the last recorded implementation
verification, not a new run for this plan. Documentation validation passed:
88 local links across the four documents, no trailing whitespace, and
`git diff --check` (only Git's line-ending conversion warnings).

## 2026-09-15: implemented shortlist follow-through and applicability audit

Continued the three shortlisted research directions and examined allocation/
encoding suggestions. [Full follow-through](SHORTLIST_FOLLOWTHROUGH.md) distinguishes
implemented numerical results, analytical screens and work not yet implemented.
Froze [protocol](PROTOCOL_SHORTLIST_V1.md) before observations. No earlier modules
or archives were overwritten and no stronger manuscript claim was inserted.

Implemented `asian_basket.py`, `shortlist_diagnostics.py`, `run_shortlist.py` and
15 focused tests. New classical benchmark: twelve discrete Asian baskets (2/4
assets, 12/52 dates, three strikes), PCA Gaussian generation, independent pilot
control fitting, raw/control RQMC, antithetic control MC and conditional-control
RQMC. 768 main estimates plus 192 separate reference estimates; references have
estimated uncertainty and are not exact truths. Conditional integration improved
per-sample reference-relative RMSE in the twelve N=4096 cells but cost more local
evaluation time. Some errors approach the reference uncertainty. Concurrent tests,
fixed ordering and excluded setup/training make timings indicative, not an isolated
runtime-crossover study. These remain classical results, not quantum advantage.

Heston deterministic audit: 14 of 72 combinations pass the displayed scalar
truncation/regularity tests; full theorem applicability remains not established
in every row. Corrected the emphasis on negative correlation: failure of a displayed
sufficient condition alone does not establish a new gap; the paper explicitly
discusses nonnegative correlation as the harder moment regime. No coherent Heston
sampler or complete proof audit was performed.

Nested diagnostic: an analytically soluble scalar exposure-style negative control,
40 naive nested estimates and eight coupled antithetic levels. Exact positive bias
falls from .4887333 at one inner sample to .00304365 at 256; direct analytic inner
valuation makes that nesting unnecessary. This is not real CVA or a quantum-nested
implementation. Focused primary PDF readings clarified uniform moment, Lipschitz,
sampling-access and coupling requirements; failed HTML attempts used PDF fallbacks.

Calculated conservative basket truncation/scale bounds, including retained-mass
normalization. Tail allowance about .05003 dollars is not the full encoding bias;
quadrature/loading/synthesis remain missing. Cube-based scale upper bounds are large,
not lower bounds or impossibility claims. Derived an unequal-calibration planning
variance and illustrative allocation ratios; NO new asymmetric allocation experiment
was run, and the earlier pilot tie with fixed_cp remains unchanged.

Archive `results/journal_sprint/shortlist_v1`: replay checked 76 files, all 768 main
estimates, 192 reference estimates, 72 Heston screens, 40 nested estimates and eight
level diagnostics. Numeric replay excludes timings and uses 1e-10 tolerances;
source and archive hashes checked. Final full suite: 504 passed, zero failures/errors/
skips, 11 upstream warnings, 270.96 seconds (`tests_shortlist_v1.xml`). All four new
Python/test files passed Ruff; local links and whitespace checked. No failed/retuned
stochastic run in this stage. No paid hardware job, external peer review, new author,
commit, push or PR. Novelty and quantum advantage remain unestablished.

## 2026-09-15: 25 harder problems and matched-budget allocation continuation

Completed the requested [25-problem assessment](HARD_PRICING_25.md) BEFORE the
allocation implementation: distinct payoff/exercise/exposure/model variants,
each with target, proposed solution, strong classical comparator, first
experiment and stop criterion. These are proposals, not 25 new open problems
or implemented quantum solutions. The 28 source groups state reading depth.
Prioritized Asian/barrier baskets, theorem-compatible multi-asset Heston and
genuinely nested exposure valuation. Newly inspected Herman et al. 2602.03725v1
model definitions, Heston theorem, truncation and discussion; restrictions are
not silently generalized. Full proof/priority verification remains undone.

Added an explicit conditional Gaussian reduction for a restricted positive-factor
Asian basket. Twelve deterministic identity-versus-direct-quadrature cases agree
within 1.0658141036401503e-14, with numerical error estimates and tail bound recorded
in the report. This checks a known conditional-integration component, NOT a full
option benchmark, novel identity or quantum advantage. The classical comparator
must benefit from the same conditioning before any quantum comparison.

Then froze [allocation protocol](PROTOCOL_ALLOCATION_V1.md), implemented
`allocation_rule.py` and `run_allocation.py`, and tested selection, sample splitting,
terminal CP inversion, forecast/allocation logic and complete shot accounting.
Encoding is chosen before observations using a design proxy, not an asserted
noise-robust dominance rule. Only the selected encoding is calibrated. The paid
pilot chooses allocation; fresh calibration AND fresh pricing provide the final
interval. Projected counts are forecasts, never measured results.

Fresh `allocation_v1` check: 3240 rows, 1080 per arm, two stationary readout
scenarios and three guards on the six existing European contracts. The harder
problems are NOT tested by this run. At a matched 65536 total-shot cap, fixed_cp
and pilot_cp each deliver 300/1080, with cell-for-cell identical observed delivery;
single_hoeffding delivers 180/1080. Zero observed interval misses or erroneous
declarations. E030/E038/E049 remain unresolved. The pilot mostly selects the
baseline allocation and does not improve delivery; no superiority is claimed.
Mean calibration shots decline but both CP arms still spend exactly 65536 total.
See [complete results and conditional-validity argument](ALLOCATION_RESULTS.md).

18 new focused tests passed before acquisition. Final full regression: 489 passed,
zero failures/errors/skips, 11 upstream warnings, 278.14 seconds
(`tests_allocation_v1.xml`). Ruff passed all three new Python/test files.
Deterministic replay verified all 3240 records and 98 archived files, input
profiles and live source hashes. Separate PowerShell checks verified all shot/CX
identities, primary-arm equal budgets and declaration radii. Exactly 25 problem
entries and new local Markdown links checked. No allocation-stage failed run or
post-result retuning; old modules and archives preserved. No external peer review,
paid hardware jobs, new author, manuscript advantage claim, commit, push or PR.

## 2026-09-15: calibration-first encoding decision rule

User asked whether the lack of advantage invalidates the project, requested
directions for their own research, and authorized developing the encoding-aware
rule. Explained that the original superiority objective remains unmet; neither
a literature search nor this negative benchmark proves no advantage can exist.
No application-family pivot or positive novelty claim was silently adopted.

Added [research directions](ADVANTAGE_RESEARCH_DIRECTIONS.md) with checked primary
abstracts on multidimensional pricing, nonlinear/nested quantum Monte Carlo,
QSP payoff encoding and the finite-window quantum-QMC proposal. These are
reading directions and hypotheses, not new full-paper readings or discoveries.

Implemented `encoding_decision.py`: a finite-menu calibration-first selector,
simultaneous CP rectangles, a dollar-scaled Hoeffding certificate, explicit
approximation and calibration budgets, cost ranking, and one fresh terminal
pricing interval. Selection does not receive true prices or amplitudes.
All candidate calibration shots are charged; no-certification outcomes are not
presented as impossibility results. The [derivation and results](ENCODING_DECISION_RULE.md)
state the per-invocation model-conditional guarantee and established-method
attribution. This is k=0 direct sampling, not an amplitude-estimation speedup.

Froze [protocol](PROTOCOL_ENCODING_DECISION_V1.md) before new observations.
Fresh synthetic check: 1080 trial identities, 180 exact-table selections and
declarations (all E001), 900 refusals, zero observed interval misses or erroneous
declarations. E014/E025 are NOT rescued by this conservative planner, despite
their earlier fixed-interval successes. E001 zero-guard shots-axis mean pricing
shots 376.43, but mean TOTAL 65912.43 after 65536 menu-calibration shots. No
overall efficiency gain is claimed; certificate conservatism and calibration
overhead are explicit remaining weaknesses.

Preserved `encoding_decision_v1`: experiment completed, but its verifier wrongly
excluded the nested input complete.json manifest. Fixed the inventory exclusion,
added a regression, and reran as `encoding_decision_v2` with identical seeds.
All 1080 records are byte-identical; v2 is not another independent sample.
Corrected replay passed 1080 rows and 96 archived files, including input/source
hash checks. Output directories and unrelated work were not overwritten.

Verification: initial full regression passed 469 tests, 11 upstream warnings,
273.02 seconds (`tests_encoding_decision_v1.xml`). It collected before the two
additional archive/calibration tests. The post-fix focused suite passed all
24 tests, including exact binomial coverage sums and propagation checks. Counts
overlap and must not be added. Ruff passed all three new Python/test files;
new local Markdown links and `git diff --check` passed. No external peer review,
paid hardware job, manuscript superiority claim, author change, commit, push
or PR. Final status: working conservative planner; novelty and advantage unproved.

## 2026-09-15: broad research and measured encoding/sequential intervention

Used the deep-research skill for the requested primary-source field assessment.
The [research report](QUANTUM_RESCUE_RESEARCH.md) covers modern AE schedules,
calibrated Bayesian AE, QSP/QSVT, multiplexed rotations, QMC/multilevel methods,
PDE/variational alternatives and IBM/Google/Quantinuum developments. The July
2026 contrast-aware CVA paper is close prior art; generic noise-aware adaptive
pricing is not claimed as new. Source reading depth and limitations are stated.

Implemented an exact finite-grid payoff oracle and calibrated anytime
Bernoulli inference without changing historical pricing/inference modules.
Declared [the experiment](PROTOCOL_RESCUE_V1.md) before circuit profiling and
new stochastic observations. Exact-oracle fixed CP improved E014 and E025
from 0/30 to 30/30 dollar declarations under equal shots and equal logical CX
at guard zero. Other hard contracts remain unresolved. The unmodified
Jeffreys CS improved both axes only on E025, failing its promotion screen.
Classical 64-term summation still handles all six contracts, so no quantum
advantage or new primitive is claimed.

Preserved failed `rescue_encoding_v1`: six profiles completed, two rows
computed but zero JSONL records persisted before NumPy-Boolean serialization
failed. Added explicit Boolean conversions and regression testing; reran into
`rescue_encoding_v2` with the same protocol. A typed-cache fix was also tested
before experiments. Completed archive: 4320 shared-data inference rows,
720 refusal rows, 810 declarations, zero observed interval misses and erroneous
declarations. Separate verification replayed all rows, checked 77 files and
recomputed bound/target arithmetic; see `rescue_verification_v1.json`.

Declared a separate [pilot-mixture follow-up](PROTOCOL_PILOT_CS_V1.md) AFTER
seeing those results. It excludes the paid 1024-shot pilot from the subsequent
likelihood and reuses the original paths: 2160 derived rows, 355 declarations,
zero observed misses/errors. E014 equal-shot delivery is only 1/30: technically
positive but not a robust fix. No independent replication or selection-adjusted
coverage claim is made. Separate replay verified all 2160 rows and the original
4320-row input archive (`rescue_pilot_verification_v1.json`).

A stronger-baseline compiler check found that E001's old k=1 Grover reflection
can use active qubits only: 992 rather than 13088 CX, versus exact-oracle 566.
Recorded the correction rather than claiming a generic 23-fold improvement.
The k=0 experiment is unaffected. Full numbers, assumptions and remaining
novelty gaps are in [RESCUE_RESULTS.md](RESCUE_RESULTS.md); the explicit
conditional inference derivation is in [RESCUE_THEORY.md](RESCUE_THEORY.md).

Initial integrated suite: 440 passed, 11 upstream warnings, 273.99 seconds.
Seven subsequent pilot tests passed. Final integrated suite then passed all
447 tests, zero failures or skips, 11 upstream warnings, in 280.51 seconds
(`tests_rescue_final_v1.xml`). Ruff passed all eight new Python/test files;
local links and whitespace checks passed. No paid hardware execution, external review, new author,
commit, push or PR was performed. Existing week-10 local changes are preserved.

## 2026-09-15: week 10 evidence-gate results and verification

Completed the scoped methods review, numerical stress diagnostic and concrete
matched-comparison feasibility assessment. See [closeout](WEEK_10_CLOSEOUT.md)
and [matched design](WEEK_10_MATCHED_DESIGN.md). Original 80-case stress run
failed the required disconnected-intersection topology condition despite zero
enclosure failures; it is retained. A disclosed three-case extension passed
all 83 numerical comparisons, including three disconnected intersections.
The final formatted-source v3 reproduces v2 records byte for byte, not as an
independent experiment. Separate source/inventory/hash verification and replay
passed all 83 records. Ten focused tests passed; first integrated suite passed
418 tests with 11 upstream warnings. Final-tree regression then passed all
420 tests with 11 upstream warnings in 295.86 seconds, including the added
verifier tests. Ruff, whitespace and local documentation link checks passed.
Week-10 evidence-gate work is complete and locally verified; its scientific
decision remains a hold on confirmation/submission, not a claim of readiness.

Decision: continue methodological development, but do not launch frozen
confirmation or claim submission readiness. Large-count interior tails,
native adaptive-stopping comparability and journal-level novelty remain
explicit gaps. The current manuscript now includes the bounded diagnostic and
links to its limitations. No pricing campaign, new authors, external reviewer
approval, PR, push or merge is claimed for this week.

## 2026-09-14: week 10 started from merged main

PR #1 is merged; week 10 starts from commit
`77fd5ec14035094e74f941319560f8a5ab7cc4c0` on
`research/week10-evidence-gate`. Read the screened basket paper's primary
methods and results text, recorded overlap and target-matching concerns, and
outlined a matched comparison in [the week-10 work record](WEEK_10_WORKING.md).
Numerical stress implementation and execution remain pending; this is not a
completed week or a frozen confirmation campaign. Existing archives and
unrelated local files are preserved.

## 2026-09-14: neutral checks, reconciliation and final merge verification

User requested that neutral checks be inspected, blockers resolved, local edits
reconciled and PR #1 merged after thorough verification. The neutral conclusions
contained a negative review report, so they were not accepted as a green light.
See [the merge gate](MERGE_VERIFICATION.md) for each additional finding, two
non-reproducing reports, reconciliation decisions and verification evidence.
Six tracked user edits were preserved in a named recovery stash and reconciled;
unrelated untracked artifacts remain outside this PR. Historical evidence stays
immutable. Final test/push/merge disposition follows the linked gate and PR log.

Final integrated suite: 410 passed, 11 upstream warnings, 336.99 seconds. The
43,200-row closeout replay, week-3 926-hash audit and 312-case numerical diagnostic
passed. Numerical records remain byte-identical to week 9. Ruff, whitespace and
new documentation links passed. Normal exact-head merge is authorized by the
user; no administrative bypass or claim of automatic Macroscope approval.

Evidence availability: historical result, reading and test paths below refer to
the originating local workspace unless explicitly listed as included in the PR.
See [archive inputs and reconstruction](ARCHIVE_INPUTS.md) for the preserved
location, exclusions and configurable verification commands.

## 2026-09-14: Macroscope review remediation

User reported the completed review and requested necessary fixes. Read all 15
inline findings, including those the bot subsequently labeled no longer relevant.
Implemented safety/integrity, batch handling, record validation, smoke recovery,
independent dollar-gate and archive portability fixes in the separate PR checkout.
Preserved unrelated user edits and all immutable original experiment evidence.
See the [finding-by-finding response](MACROSCOPE_REVIEW_RESPONSE.md) for changes,
tests and limitations; [archive reconstruction](ARCHIVE_REPLAY.md) documents the
historical protocol supplement instead of rewriting the original snapshot.

Initial 52 new regression tests passed; a 53rd materialization test was then added.
Reran all 312 numerical cases with zero failures and byte-identical records to
week 9. Full suite: 390 passed, 11 upstream warnings, 142.10 seconds. Ruff and
whitespace checks passed. Fixes are pushed to PR #1 from the separate review
checkout; the main workspace's uncommitted edits remain untouched.
The prior Macroscope cost skip is superseded by the completed user-triggered
review, not by a claim of approval. No billing settings or author list changed.

## 2026-09-14: review PR opened at user request

User explicitly requested publication of the work as a PR so they can initiate
Macroscope review. Opened [PR #1](https://github.com/Prithvi8706/quantum_option_pricing/pull/1)
from `journal-reengineering-weeks-1-9` against `main`. This supersedes earlier
PR-hold status; Macroscope approval itself remains pending.

Included 19 pre-existing foundation commits and the sprint source/tests,
documents, licensed comparator extract and selected small evidence exports.
[Scope and exclusions](PR_REVIEW_SCOPE.md) explains why original manifests are
not complete replay archives in this checkout. Unrelated uncommitted Paper A
edits, local environments, downloaded papers and large archives remain local.
Sprint Ruff passed. A separate clean PR-tree full-suite check was started;
its disposition is recorded in the review-scope document and PR description.
The clean run produced 325 passes and 12 missing-fixture failures. Included the
small required baseline/configuration fixtures; all 27 tests in affected modules
then passed, including every prior failure. No tests were skipped or weakened.
Preserved original evidence bytes using Git attributes. Macroscope automatically
skipped the first review because its 39.12 USD estimate exceeded the 10 USD
per-review limit; no paid retry or billing change was initiated by the agent.
No merge, submission or authorship change was made.

## 2026-09-14: week 9 started and completed locally

User requested week 9 start to end, then resumed after network interruption.
[Plan](WEEK_9_PLAN.md), [step-by-step closeout](WEEK_9_CLOSEOUT.md),
[results](WEEK_9_RESULTS.md), [new manuscript](MANUSCRIPT_RELIABILITY_DRAFT.md).

- Reconciled weeks 5–8 into a claim/evidence audit and synchronized manuscript;
  corrected stale calibration/bound language while preserving historical drafts.
- Refreshed focused primary records, adding an explicitly abstract-only basket
  pricing overlap screen. No exhaustive-search or certified-novelty claim.
- Predeclared independent 80-digit numerical reference: 312 cases, zero missing
  components, 18 empty, 78 full, zero disconnected final reference sets. Maximum
  endpoint slack 1.1003482766924545e-13; finite diagnostic, not certification.
- Replayed all cases; checked 71 archive hashes, 67 snapshot hashes and six live
  producing dependencies. Historical week-5–8 manifest/summary checks retained
  distinct procedure and inference-arm denominators, not new pricing replays.
- Integrated suite: 337 passed, 11 warnings, 192.80 seconds. Nine new focused
  tests passed. Subsequent verifier-only provenance clarification passed replay
  and lint; not falsely included in the earlier full-suite run.
- Separate Astra-requested reviewer independently replayed 312 cases, ran nine
  tests and inspected test XML. Corrected “paired” to descriptive unpaired for
  week-8 contrasts and completed the linked results document.
- No new pricing trials, target-driven retuning or restored withdrawn claims.
  Paid selector remains negative; journal sufficiency remains unestablished.
  Macroscope/PR, submission and authorship gates remain open. No external write.
- Next: [week-10 proposal](WEEK_10_GATE_DRAFT.md), not an executed protocol.

This record captures milestone decisions, evidence and corrections, not every
terminal command. Prior week-1–8 entries remain below.

## Week 8 started

User requested start to end. [Plan](WEEK_8_PLAN.md) and
[prospective representation-pilot protocol](PROTOCOL_W8_REPRESENTATION.md)
freeze a paid, target-free pilot choice with fresh validation versus both fixed
representations. Bound-only menu audit completed before new draws; all outcomes
and costs will be logged, including negative selection results.

## 2026-09-13: week 8 complete locally

All five [planned items](WEEK_8_PLAN.md) completed. See the
[step-by-step closeout](WEEK_8_CLOSEOUT.md), [results](WEEK_8_RESULTS.md), and
[selection scope](WEEK_8_SELECTION_SCOPE.md).

- Audited n5/n6 bounds and existing compiled profiles before new draws. Fixed
  both baselines and an observable pilot-radius ranking heuristic; target-field
  injection is rejected at the selector interface. No representation/guard
  retuning after observing outcomes.
- Executed 5400 procedures: 3300 final acquisitions, 2100 pre-refusals, plus
  1800 paid pilot acquisitions. Persisted pilot observations, choice and fixed
  final schedule before generating fresh calibration/validation observations.
- Reconstructed all 5400 events/records and 54 summaries; checked 81 archive
  hashes and 74 planned dependencies. Preserved all pilot/final costs and
  36 selector-minus-fixed contrasts.
- Observed 900 declarations (all E001), 2400 unresolved final intervals, no
  incompatibilities, 3300/3300 price containment and zero erroneous declarations.
  These are frequencies, not zero risk or coverage conditional on delivery.
- Paid choices: 350 n5 / 550 n6; another 300 n6 bypasses for E049. All delivery
  contrasts were zero; only 3/12 cells met the >=90% threshold and both mean
  gains were zero. Selector fails and is retained as a negative ablation.
- Full regression: **325 passed**, 11 legacy warnings, 328.17 s. Separate
  Astra-requested source/data/claim review passed, identifying two minor issues.
  Clarified claim wording and added after-cell resource checks including the
  last cell. **14 focused tests** passed afterward, including three new boundary
  cases; no post-fix full-suite rerun claimed. Ruff and links checked.
- Preserved v1 and executed corrected-source v2 plus full replay. Records,
  selection events, menu and targets match byte-for-byte; outcomes unchanged.
  V2 is same-key replay, not another independent experiment to pool with v1.
  Reviewer accepted both fixes in final mechanical recheck.
- Decision: no adaptive promotion/main confirmation. Narrow candidate scope to
  model-conditional interval coverage and empirical precision delivery with
  explicit costs; novelty remains unestablished. [Week 9 gate](WEEK_9_GATE_DRAFT.md)
  is future claim/evidence work, not a completed experiment.

Archives under `results/journal_sprint`: `week8_representation_v1`,
`week8_closeout_v1`, `week8_representation_v2`, `week8_closeout_v2`.
Tests: `tests_week8_integrated_v1.xml`, `tests_week8_review_fix.xml`.
No original evidence overwritten, unrelated user work changed, author additions,
commit/push/PR, paid hardware or submission. Macroscope remains unconnected.
Eight scheduled weeks (9–16) plus reserve remain readiness-gated, not acceptance.

## Week 7 started

User requested start-to-end completion. [Week-7 plan](WEEK_7_PLAN.md) and
[prospective ablation](PROTOCOL_W7_ABLATION.md) separate pricing shots,
calibration shots and guard width at fixed actual transfer. Pinned comparator
semantics will be audited in parallel with local implementation. No main matrix
or adaptive claim is assumed. Completion and evidence will be appended here.

## 2026-09-13: week 7 complete locally

All five [planned items](WEEK_7_PLAN.md) completed start to end. The
[step-by-step closeout](WEEK_7_CLOSEOUT.md), [results](WEEK_7_RESULTS.md), and
[native-comparator audit](WEEK_7_COMPARATOR_SCOPE.md) record the evidence.

- Prospectively separated pricing budget, calibration budget and valid guard
  width while holding actual transfer fixed for paired guard comparisons.
- Executed 21600 acquisition attempts: 14400 acquired, 7200 refused. Shared
  guard arms produced 43200 arm attempts / 28800 executed inferences. Costs
  charged once per acquisition, not once per arm; represented shots 5089003200.
- Replayed every record and all 216 summaries; 77 archive and 71 planned
  dependency hashes checked, 19200 guard-enclosure comparisons passed.
- Archived 1008 descriptive contrasts and all four predeclared readiness
  screens. All failed: 1/12,1/12,3/12,3/12 cells passed, respectively. E001
  improves with more pricing shots; broad four-contract usefulness is not shown.
- Preserved 5042 arm declarations, 23758 unresolved outcomes and nine interval
  misses. Three misses were precise E001 intervals but midpoint errors remained
  <=$1; zero erroneous $1 declarations observed. No risk/coverage overclaim.
- Pinned BAE/BIQAE source audit confirms that their current native adapters do
  not supply the finite-calibrated asymmetric-readout/transfer guarantee. No
  mismatched native head-to-head win or modified baseline was invented.
- Ten new targeted tests passed before run; full regression **314 passed**,
  11 legacy warnings, 190.03 s. Ruff and local Markdown links checked.
- Separate Astra-requested final numerical/claim review passed. Closeout link
  completed. Mathematical/numerical certification remains separate.
  Reviewer executed full existing replay into `week7_sidecar_review_v1`, with
  separate aggregation; parent verified its three result JSON files match.
  Reviewer inspected test XML rather than personally rerunning pytest.
- Decision: no adaptive promotion or confirmatory main matrix. The
  [week-8 gate draft](WEEK_8_GATE_DRAFT.md) is a future design task, not an
  executed experiment. Nine scheduled weeks (8–16) plus reserve remain gated.

Evidence: `results/journal_sprint/week7_ablation_v1`,
`results/journal_sprint/week7_closeout_v1`,
`results/journal_sprint/tests_week7_integrated_v1.xml`. No archives overwritten,
unrelated user edits changed, author additions, commits, pushes or submissions.
Macroscope remains unconnected and the PR is held.

This is the central index and ongoing milestone log, not a verbatim transcript
of every command. Protocols, result notes, code, test outputs and hashed run
archives hold the detailed evidence. Negative results and unresolved gates
must remain visible; completion of a week does not mean publication readiness.

## Work completed before week 6

- [Weeks 1–2](WEEK_1_2_CLOSEOUT.md): evidence audit, pricing bounds and prototypes.
- [Week 3](WEEK_3_PROGRESS.md): circuit/stress/classical checks;
  [review and PR gate](WEEK_3_PR_GATE.md).
- [Week 4](WEEK_4_CLOSEOUT.md): finite calibration and guarded transfer discovery.
- [Week 5](WEEK_5_CLOSEOUT.md): compiled fixed-design cost comparison,
  7200 attempts, reconstruction and bounded automated review.

## 2026-09-13: week 6 started

User requested a clear ongoing Markdown record and week-6 execution.
The [week-6 protocol](PROTOCOL_W6_TRANSFER_GRID.md) develops the prior
[pilot draft](WEEK_6_PILOT_DRAFT.md). Retain all six contracts, nine stipulated
transfer positions, two calibration budgets and three fixed designs.
No adaptive tuning, held-out confirmation or real-device claims are authorized
by these discovery results. Status and evidence: [week-6 progress](WEEK_6_PROGRESS.md).

First execution completed: 32400 attempts in 29.43 seconds; 16 targeted tests
passed before acquisition. Raw archive: `results/journal_sprint/week6_transfer_grid_v1`.
This initial status is superseded by the completed closeout below.

Macroscope remains unconnected; PR, author approvals and submission remain held.

## 2026-09-13: week 6 completed locally

User requested completion without stopping at milestones. Continued through
reconstruction, predefined analysis, regression, bounded separate review and
next-stage decision. [Full step-by-step closeout](WEEK_6_CLOSEOUT.md) and
[results](WEEK_6_RESULTS.md) are the current state.

- Reconstructed all 32400 attempts / 324 cells, including 21600 acquisitions
  and 10800 refusals; checked 71 archive hashes and 66 planned dependency hashes.
- Recorded 2729 precision declarations and 18871 unresolved acquisitions.
  Three price-containment misses were unresolved; zero erroneous declarations
  observed. These outcomes do not imply zero risk or conditional coverage.
- Published all 162 calibration contrasts, 216 design contrasts and 36 range
  summaries. E001 CX-capped delivery ranged 0–99% at low calibration and 2–99%
  at high; rare E014/E025 declarations retained rather than suppressed.
- Full regression: 304 passed, 11 legacy warnings, 189.06 seconds. Ruff passes.
- Astra-requested review resumed after usage-limit interruption; no blocking
  scientific-reporting issue. Corrected per-contract depth wording and recorded
  the fail-closed live-source replay limitation; no mathematical proof claimed.
  Reviewer replayed all records using existing helpers with writes intercepted,
  separately calculated contrast checks, and ran 12 overlapping targeted tests.
- Scientific decision: no adaptive promotion or confirmatory main matrix.
  [Week-7 gate draft](WEEK_7_GATE_DRAFT.md) calls for separately declared
  ablation and fair-comparator work. No unexecuted future experiment is counted
  as completed. Ten scheduled weeks (7–16) remain, subject to readiness gates.

Archives: `results/journal_sprint/week6_transfer_grid_v1`,
`results/journal_sprint/week6_closeout_v1`; integrated test XML:
`results/journal_sprint/tests_week6_integrated_v1.xml`. Original archives and
unrelated user edits preserved. No PR/push/submission/author-list changes.

## Retrospective week-by-week log: weeks 1–5

Added 2026-09-13 from the linked existing evidence. Weeks 1–2 were closed out
jointly: the thematic split below is for navigation, not a claim that exact
work dates or a separate week-1/week-2 sign-off were recorded. Test counts from
overlapping suites are not added together. Failed and superseded artifacts
remain preserved; these summaries do not replace their provenance.

### Week 1 — evidence audit and research direction (joint sprint)

- Work: preserved historical manuscripts/data; distinguished encoded-reference
  deviation from continuous Black–Scholes error; removed unsupported floor
  claims from the replacement narrative. Excluded both disputed Paper B slope
  sets for lack of adequate producing-run evidence.
- Research: six assigned primary papers read in full; two additional 2026
  papers only abstract-screened. Separated established estimation tools from
  the proposed application contribution. Proposed small genuine collaborator
  packages without claiming acceptance, completed work or authorship.
- Outputs: [reading ledger](READING_LEDGER.md),
  [literature supplement](LITERATURE_SUPPLEMENT.md),
  [claim ledger](CLAIM_LEDGER.md),
  [Paper B disposition](PAPER_B_EVIDENCE_DISPOSITION.md),
  [working manuscript](MANUSCRIPT_WORKING_DRAFT.md),
  [team packages](TEAM_WORK_PACKAGES.md).
- Decision: pursue contract-aware delivered precision with auditable bounds
  and costs, not an unsupported generic new estimator or hardware advantage.
- Open: genuine contributor agreement, availability/budgets, and the later
  scientific/publication gates. Historical evidence was not fabricated.

### Week 2 — feasibility and dollar-precision prototypes (joint sprint)

- Work: pinned comparator with golden checks; conservative all-branch
  inversion, independent pilot/validation streams, mismatch/refusal outcomes.
  Generic prototype retained 26600 records; comparator work retained 160000
  estimations over 140000 distinct generated datasets.
- Application: examined 72 bound configurations; tighter grid bound increased
  positive $1 statistical allowances from 4 to 14, across four of six contracts.
  V2C recorded 43200 attempts: 36000 executed, 7200 pre-refused.
- Findings: largest-budget ideal fixed multidepth delivered in 51.08% of all
  attempts versus 33.33% for equal-A direct sampling. Not a best-classical or
  modern-estimator advantage. Bound-only selection mainly saved refusal costs,
  not demonstrated adaptive scheduling benefit.
- Checks: full suite 225 passed before three additional closeout tests;
  updated sprint suite 64 passed. All 43200 V2C records reconstructed.
- Evidence: [joint closeout](WEEK_1_2_CLOSEOUT.md),
  [V2C results](PRICE_INTERVALS_V2C_RESULTS.md),
  [next-stage amendment](PROSPECTIVE_AMENDMENT_DRAFT.md);
  archive `results/journal_sprint/week12_closeout_v1`.
- Decision: feasibility foundation complete, administrative sign-off pending;
  proceed to circuit checks and stronger baselines, not submission.

### Week 3 — circuit, noise, classical and reproducibility checks

- Work: actual-circuit/noise checks, readout/dependence stress, 480-row
  classical European/Asian matrix, pinned BAE/BIQAE source smokes, 20 larger
  logical profiles, and a fresh-environment circuit replay.
- Findings: response-model failures and matched-cost/conditional-risk questions
  prevented confirmation. No adaptive superiority or practical advantage.
- Checks: final integrated 253 passed; fresh-environment sprint 89 passed
  (overlapping scopes). Bounded automated review requested with `gpt-6-astra`;
  findings addressed and corrected artifacts checked, not human peer review.
- Evidence: [progress](WEEK_3_PROGRESS.md),
  [stress results](WEEK_3_STRESS_RESULTS.md),
  [baselines and review](WEEK_3_BASELINES_AND_REVIEW.md),
  [PR gate](WEEK_3_PR_GATE.md).
- Decision: hold confirmation. Macroscope unavailable/unconnected, PR held.
  Existing branch history and unrelated user edits prevent treating a broad
  staged tree as an isolated weekly PR; no bulk staging of result caches.

### Week 4 — finite calibration and transfer validity

- Work: 1200 calibration datasets / 3600 analyses; transfer/dollar experiment
  with 6000 attempts, 4000 acquisitions, 2000 pre-refusals and 8000 inferences.
  Charged calibration and distinguished wrong declarations from noncontainment.
- Findings: guarded intervals contained targets in all tested within-bound
  cells, but useful $1 delivery was largely E001. Exceeding supplied bounds
  could produce narrow wrong intervals; precision cannot validate assumptions.
- Checks: 271 integrated tests passed; 107 sprint tests overlap. Reconstructed
  all 6000 trial identities and 8000 inferences; 61 transfer hashes checked.
  Separate calibration checks covered 46 hashes and 1200 observations.
  Bounded Astra-requested review led to heading/reference corrections.
- Evidence: [closeout](WEEK_4_CLOSEOUT.md),
  [calibration progress](WEEK_4_PROGRESS.md),
  [transfer results](WEEK_4_TRANSFER_RESULTS.md),
  [validation contract draft](WEEK_5_6_VALIDATION_CONTRACT_DRAFT.md);
  archive `results/journal_sprint/week4_transfer_verify_v2`.
- Decision: local discovery milestones complete; develop fixed cost baselines
  before adaptive control. Real transfer justification, numerical certification,
  fair comparisons, confirmation and Macroscope/PR remain open.

### Week 5 — fixed-design pricing costs and delivery

- Work: ten missing k=2 profiles, 30 combined profiles and 40 fixed-cost
  comparisons. Recorded 7200 attempts: 4800 acquisitions, 2400 refusals,
  516 precision declarations and 4284 unresolved acquisitions.
- Findings: only E001 delivered $1 precision. Larger-budget CX-capped delivery
  was 6/100 stationary and 95/100 transfer versus direct's zero. Equal-A
  multidepth used about 15.6 times direct's pricing CX count. Neither result
  establishes broad advantage, continuous-region robustness or zero error risk.
- Checks: 287 integrated tests passed before verifier-only strengthening;
  11 targeted tests passed afterward, including five configuration mutations.
  v2 replay validated exact configuration and live/archive Python identity.
  Separate Astra-requested source/hash review accepted fixes; not independent
  numerical proof. Qualified local predeclaration versus timestamped registration.
- Evidence: [plan](WEEK_5_PLAN.md), [results](WEEK_5_FIXED_RESULTS.md),
  [closeout](WEEK_5_CLOSEOUT.md); archives
  `results/journal_sprint/week5_fixed_discovery_v1` and
  `results/journal_sprint/week5_fixed_verify_v2`.
- Decision: local week complete; choose transfer-position/calibration-size
  discovery for week 6. Keep adaptive promotion, confirmation and PR held.
