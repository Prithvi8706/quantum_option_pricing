# Project checklist — 17 September 2026

Snapshot after [PR #6](https://github.com/Prithvi8706/quantum_option_pricing/pull/6)
merged into `main` at `b074488c`. This checklist is a subsequent documentation
addition, not a file included in that merge.

Same-day update: [claim assessment and decision](docs/journal_sprint/CLAIM_ASSESSMENT_RESULTS_20260917.md)
adds restricted proofs, separate AI reviews and a retrospective sensitivity
study. Human expert novelty review and quantum advantage remain open.
The [bounded matched arithmetic follow-up](docs/journal_sprint/MATCHED_ARITHMETIC_RESULTS_20260917.md)
now supplies explicit comparator evidence; it does not promote confirmation.

**Bottom line:** the development work, reproduction work and two-week
minimal-pivot study are complete within their recorded scopes. The candidate
remains on standby. Scientific confirmation, quantum-over-classical advantage
and submission readiness are **not** complete.

Checked means completed within the stated scope, not that a scientific gate
passed. Negative findings count as completed investigations, not positive results.
Historical plans contain stale opening summaries; later closeouts and the
[project log](docs/journal_sprint/PROJECT_LOG.md) govern this snapshot.

## 1. Original roadmap status

| Work package | Completed work | Remaining qualification |
| --- | --- | --- |
| Weeks 1–2 | Evidence audit, research direction, feasibility and dollar-precision prototypes | Development only; not confirmation |
| Week 3 | Circuit, noise, classical-comparator and reproducibility checks | Model- and implementation-specific evidence |
| Week 4 | Finite calibration and transfer-validity work | Guarantees depend on declared assumptions |
| Week 5 | Fixed-design pricing costs and delivery study | No general superiority established |
| Week 6 | Transfer/calibration acquisition, reconstruction and analysis | No adaptive or confirmation promotion |
| Week 7 | Budget/guard ablations and comparator audit | Readiness screens failed; results retained |
| Week 8 | Paid representation-selection study and validation | Negative selector result retained |
| Week 9 | Claim/evidence reconciliation, numerical audit and reliability manuscript draft | Draft is not the final integrated quantum paper |
| Week 10 | Evidence-gate development and verification | Confirmation/submission gate closed NO-GO |
| Week 11 | Error contract, strong Asian-basket baselines and reference studies | Does not demonstrate quantum advantage |
| Week 12 | Unequal-calibration policy, matched development comparisons and replay | Method-interest gate failed |
| Week 13 | Small quantum Asian-basket encoding and feasibility audit | Continuous-price admission remained blocked |
| Week 14 | Finite-target comparisons, ablations, resource analysis and independent reviews | Original continuous end-to-end comparison incomplete |
| Week 15 | Fresh-environment reproduction and gate assessment | **Fresh confirmation campaign remains incomplete** |
| Week 16 | Earlier drafts and artifacts provide inputs | **Final manuscript/submission-readiness package remains open** |

References: [original retrospective log](docs/journal_sprint/PROJECT_LOG.md),
[revised roadmap](docs/journal_sprint/WEEKS_11_16_IMPLEMENTATION_PLAN.md),
[Week 14 closeout](docs/journal_sprint/WEEK_14_CLOSEOUT.md),
[Week 15 closeout](docs/journal_sprint/WEEK_15_CLOSEOUT.md).

The new study's “Week 1” and “Week 2” below are **additional research blocks**,
not replacements for original Weeks 15–16. Remaining work is not simply one
calendar week: gate resolution, confirmation and publication preparation have
uncertain duration.

## 2. Completed research and implementation

- [x] Implement fixed/sequential inference, dollar-price mapping, calibration,
  transfer checks, replay and resource accounting under documented assumptions.
- [x] Implement the encoding-aware conservative decision rule, including costs,
  accuracy screening and explicit refusal when requirements are unsupported.
- [x] Build strong classical Asian-basket comparators, including control variates,
  RQMC and conditional RQMC; retain setup/pilot costs and uncertainty limitations.
- [x] Survey 25 harder pricing problems and perform selected feasibility audits.
  This is a selection study, **not 25 implemented quantum pricing algorithms**.
- [x] Complete directed partial encoding/normalization bounds and bounded
  table-free arithmetic development; record unresolved confirmation requirements.
- [x] Evaluate combined representation/QSP/reuse proposals and polynomial residual
  QSP, including separable/centered signals, symmetric phases and minimax bounds.
- [x] Audit the four selected QCE-related papers and transferable methods;
  implement/check deterministic loader synthesis and relevant identities.
- [x] Preserve failed attempts, unfavorable comparisons, capped runs, original
  producers and superseded analysis receipts.

Evidence: [gate bounds](docs/journal_sprint/CONFIRMATION_GATE_BOUNDS_RESULTS.md),
[combined development](docs/journal_sprint/COMBINED_DEVELOPMENT_RESULTS.md),
[normalization study](docs/journal_sprint/NORMALIZATION_APPROXIMATION_RESULTS.md),
[four-paper audit](docs/journal_sprint/FOUR_PAPER_AUDIT.md).

## 3. Additional minimal-pivot study — both weeks completed

### Study Week 1: construction and feasibility

- [x] Keep the arithmetic Asian-basket contract rather than silently pivoting.
- [x] Construct the shared-reflection centered signal and logical error bound.
- [x] Compare against equally optimized original and subset-based constructions.
- [x] Compile small instances and a larger signal circuit; distinguish compilation
  from simulation and from complete pricing execution.
- [x] Record resource tradeoffs, tests and exact numerical replay evidence.

### Study Week 2: integrated bounded validation

- [x] Integrate loading, residual QSP, directed classical offset/error budget,
  Hadamard readout, canonical amplitude estimation and outcome decoding.
- [x] Add encoding/degree selection for logically feasible plans while keeping
  physical/production selection fail-closed.
- [x] Evaluate the frozen four-case, 32-configuration logical-plan menu and
  24 classical method/budget cells.
- [x] Run explicit tiny AE simulations and check their distributions against
  an independent Fourier-kernel calculation.
- [x] Repair controlled-power circuit expansion; retain interrupted runs.
- [x] Correct inverse-QFT swap accounting without rewriting raw evidence.
- [x] Verify six completed acquisition/replay archives and all 32 decision rows.
- [x] Complete method, prior-art, results and limitations documentation.
- [x] Keep the candidate on standby as requested.

**What improved:** selected reflection plans have about **4.03×, 2.01× and
4.02× lower projected logical CX cost** than selected original-encoding plans
in D1/D2/E1. These are quantum-construction comparisons, not device speedups or
quantum-over-classical advantage. E2 fails the fixed accuracy menu. At the tiny
fixed-degree/fixed-AE schedule, reflection costs more. These limits remain part
of the result.

Evidence: [study plan](docs/journal_sprint/MINIMAL_PIVOT_STUDY_PLAN.md),
[Week 1 results](docs/journal_sprint/MINIMAL_PIVOT_WEEK1_RESULTS.md),
[Week 2 results](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_RESULTS.md).

## 4. Verification, cleanup and GitHub — completed

- [x] Merge all completed branch work in PR #6, preserving 19 substantive commits.
- [x] Verify merged contents match the reviewed branch; synchronize local `main`.
- [x] Confirm GitHub attributes the research commits to the owner's account.
- [x] Remove generated bytecode from version control and today's temporary
  verification checkouts; preserve unrelated local research files.
- [x] Fix LF-to-CRLF conversion for 16 manifest-hashed sources without changing
  experiment code or weakening provenance checks.
- [x] Pass **1,143 tests** in the corrected clean checkout, with 12 legacy warnings.
  Working-tree and initial-checkout runs also passed 1,143 each; not additive.
- [x] Pass **51 overlapping focused tests** in the separate pinned environment.
- [x] Verify W1/W2 and earlier development/four-paper archive hashes and replay.
- [x] Regenerate W2 analysis byte-for-byte identically to authoritative analysis v2.
- [x] Pass Ruff F checks for all 81 changed Python files and Git whitespace checks.
- [x] Record final receipts and review limitations in the project log/handoff.
- [ ] Obtain a successful latest external code review: **Macroscope skipped PR #6
  because credits were exhausted**. This is not a passed review; no new Astra
  review is claimed for that PR.

Evidence: [integration handoff](docs/journal_sprint/STUDY_MERGE_CLOSEOUT.md),
[final clean-suite receipt](results/journal_sprint/merge_study_clean_full_tests_v2.xml).

## 5. Remaining scientific work — priority order

### A. Decide what claim can actually be supported

- [ ] Obtain independent expert assessment of novelty against the nearest prior
  work; distinguish an application-specific construction from a new primitive.
- [ ] Establish a defensible contribution beyond assembling known components:
  a checked theorem, useful decision result, or substantive reproducible finding.
  Restricted correctness propositions and a reproduced encoding-choice reversal
  are now documented, plus a reproduced full-component arithmetic comparison
  and aggregation-bottleneck finding. Publication-level novelty still needs
  external assessment; this gate is not automatically checked off.
- [x] Decide whether to advance the standby candidate, pursue another bounded
  experiment, or revise the claim/scope explicitly. Decision: close the bounded
  arithmetic-comparator study with a qualified logical-cost finding; keep the
  candidate on standby and production choice unset.
- [x] Implement and acquire the fixed D1/D2 ripple/Fourier comparison, including
  conversion, payoff, inverse, loader, AE and workspace costs; reproduce it in
  the isolated environment. This is not an optimized external solver comparison.
- [x] Complete separate mathematics and implementation/evidence reviews, fix
  verifier omissions, pass1,271 integrated tests and re-emit/verify the evidence
  from a clean checkout. Scientific admission remains a separate open gate.
- [ ] If quantum-over-classical advantage remains the target, demonstrate it under
  matched task, accuracy, confidence and resource assumptions. It is not established.

### B. Resolve implementation and comparison gaps before confirmation

- [ ] Specify the actual execution model and bound native synthesis/decomposition,
  controlled-operation and relevant noise errors; physical execution error is unknown.
- [ ] Propagate those errors through the complete target-price/statistical-delivery
  contract. Existing ideal-logical bounds alone do not certify physical delivery.
- [ ] Address or explicitly delimit the E2 menu failure, dense loader scaling,
  normalization/payoff-approximation cost and large absolute resource estimates.
- [ ] Complete an apples-to-apples continuous-target comparison with strong
  classical methods, including setup, loading, inverses, shots, accuracy and
  confidence interpretation. Approximate classical t intervals are not certificates.
- [ ] Validate any claimed practical crossover using explicit hardware/physical
  overhead assumptions or actual matched execution. Simulator timing is not a
  quantum-device runtime measurement; no hardware run has been demonstrated here.
- [ ] Update the claim matrix and obtain an explicit pre-confirmation gate decision.

### C. Finish original Week 15's blocked confirmation milestone

- [ ] After admission, freeze method, primary outcomes, budgets, confidence rules,
  held-out regimes, stopping rules and multiplicity treatment before acquisition.
- [ ] Run genuinely fresh confirmation data; development cases and deterministic
  replays must not be relabeled as confirmation.
- [ ] Evaluate delivery, coverage/error declarations and matched-cost effects with
  uncertainty; retain refusals, failures and negative results.
- [ ] Obtain independent reproduction/review and close the confirmation gate with
  a justified acceptance, narrower claim or documented NO-GO.

### D. Finish original Week 16's publication package

- [ ] Update the integrated quantum-centered manuscript; the earlier reliability
  draft is not a completed account of the new study.
- [ ] Generate final tables/figures from frozen analysis and trace each claim to
  a proof, measured result or explicitly labeled resource projection.
- [ ] Complete artifact/dependency/license and clean-environment release audits.
- [ ] Refresh literature and quantum-focused journal fit, current fees/waivers,
  access model and policies from official sources before choosing a venue.
- [ ] Obtain actual collaborator contributions, review and final author approval;
  record contributions accurately rather than assigning honorary author slots.
- [ ] Finalize code/data availability, funding/conflicts and applicable AI-use
  disclosures; obtain human approval for venue, spending and submission.
- [ ] Complete the Week 16 closeout and submission-readiness decision.
- [ ] Submit only after the scientific and human approval gates pass. No submission
  or publication is recorded as completed in this project snapshot.

## 6. Practical handoff

- [ ] Review remaining untracked local files individually if further cleanup is
  wanted; they were deliberately not deleted or indiscriminately committed.
- [x] Integrate this checklist through a dedicated documentation commit on `main`.
- [ ] Keep future commits tied to real implementation, tests, experiments or
  documentation; preserve genuine dates and authorship rather than padding activity.

**Next research action:** review the standby candidate's precise novelty and
execution/comparison gaps, choose a bounded follow-up with a predeclared success
criterion, and only then consider unblocking confirmation. A merge or a green
test suite does not itself establish journal readiness.
