# Journal Reengineering Checklist

Forward-plan update (16 September 2026): the active schedule is
[weeks 11-16](journal_sprint/WEEKS_11_16_IMPLEMENTATION_PLAN.md), incorporating
the week-10 gate and subsequent encoding/allocation/harder-pricing findings.
This is a prospective revision, not completion of the unchecked publication
requirements below. Earlier weekly closeouts remain historical evidence.

Weeks 11-14 are development-complete in their declared scopes; two planned blocks
(15-16) remain, with week15 confirmation currently NO-GO. Week 12's
[negative/tied result](journal_sprint/WEEK_12_CLOSEOUT.md) does not establish novelty.
[Week13](journal_sprint/WEEK_13_CLOSEOUT.md) completed six cases/24 validated
finite circuits,735passing tests and independent reviews; no certified
continuous-price or quantum-advantage admission follows from those checks.
[Week14](journal_sprint/WEEK_14_CLOSEOUT.md) completed finite-target comparisons,
93tasks/2022archived files,807passing tests and independent evidence reviews.
Its [claim/gate matrix](journal_sprint/WEEK_14_CLAIMS_GATE.md) preserves unresolved
application validity, prior-work distinction and human confirmation sign-offs.
The
[PR #2 verification checklist](journal_sprint/PR2_MERGE_CHECKLIST.md) records the
integration sweep separately from the publication requirements below.

Week-11 development [closeout](journal_sprint/WEEK_11_CLOSEOUT.md) records the
shared error/resource contract, refined classical references, full benchmark,
verification and remaining quantum contribution gate. It does not close the
publication-level requirements below or establish quantum advantage.

Current weekly evidence is indexed in [PROJECT_LOG.md](journal_sprint/PROJECT_LOG.md).
Week-6 [results](journal_sprint/WEEK_6_RESULTS.md) extend discovery, not the
publication-level sign-offs below. Unchecked main-study requirements are not
automatically closed by local pilot success or a passing test suite.

Companion to [the research report](JOURNAL_REENGINEERING_RESEARCH_2026-09-09.md). Updated with the [executed feasibility sprint](journal_sprint/WEEK_1_2_RESULTS.md). Checked items below have concrete sprint artifacts; unchecked items remain open. The isolated September protocol does not amend the frozen July protocol.

10 September closeout: [WEEK_1_2_CLOSEOUT.md](journal_sprint/WEEK_1_2_CLOSEOUT.md).
All technical items in the first section are complete; contributor acceptance,
actual availability and fee ceiling require human confirmation. Later sections
are publication-stage requirements, not claims that the first two weeks produced
a submission-ready paper.

## First two weeks: establish whether the stronger paper is feasible

- [x] Record publication status: the author confirmed on 9 September 2026 that neither manuscript has been submitted or published.
- [x] Define the candidate coherent contribution and reconsider the unpublished A/B split; see the contribution matrix. Novelty remains to be established.
- [ ] Agree actual contributor responsibilities, available time, compute capacity, and fee ceiling.
- [x] Preserve original CSV/manuscript versions and record recoverable code provenance; exact producing-run revisions remain unknown where evidence is absent.
- [x] Document the historical reference mismatch: stored QAE-reference deviation is not Black–Scholes error.
- [x] Remove the protected-status treatment of the $0.203 discretization-floor claim in the replacement working manuscript; originals remain historical.
- [x] Resolve Paper B reuse: exclude both historical slope sets because raw producing-run evidence is unresolved; see PAPER_B_EVIDENCE_DISPOSITION.md. No historical replication is claimed.
- [x] Read BAE, BIQAE, noisy likelihood AE, the 2024 IQAE-bias paper, and the two September 2026 preprints in full; see READING_LEDGER.md and LITERATURE_SUPPLEMENT.md.
- [x] Reproduce one reference-code benchmark for the chosen modern comparator; golden tests and reduced independent replication completed.
- [x] Write a contribution-by-prior-work matrix, specifying candidate distinctions and standard methods.
- [x] Draft a prospective protocol amendment for selectable payoff scaling, resource selection, stronger baselines, and new reliability outcomes; PROSPECTIVE_AMENDMENT_DRAFT.md is not a launched confirmation experiment.
- [x] Implement a tiny fixed-schedule interval prototype with independent selection/validation observations.
- [x] Test low, central, and high amplitudes, multiple feasible components, and deliberately incompatible noise models.
- [x] Measure the useful-interval/abstention trade-off before committing to a large simulator campaign.

Decision: advance the stronger method only if its conditional assumptions are explicit, its outputs are correct, and a useful distinction from existing methods is plausible. Otherwise finish the narrower July error-budget study.

## Scientific correctness

- [ ] Keep continuous, support, finite-grid, circuit, ideal finite-shot, and noisy procedure targets distinct.
- [ ] Verify signed identities and independent references.
- [ ] Convert amplitude uncertainty to price uncertainty with the actual contract-specific transformation.
- [ ] Separate deterministic bounds from observed deterministic errors.
- [ ] Keep exact target values outside the controller's selection inputs.
- [ ] Prove the fixed-schedule conditional containment statement, including calibration and numerical inversion error.
- [ ] Preserve all feasible parameter components; use a conservative enclosure when needed.
- [ ] Document the assumption that makes shots binomial; handle drift/correlation separately.
- [ ] Distinguish a proved noise envelope from a fitted model and empirical goodness-of-fit diagnostics.
- [ ] Label unresolved precision accurately; failure of a sufficient bound is not a universal impossibility proof.

## Experimental infrastructure

- [ ] Persist execution events before running circuits and reconcile interrupted raw/resource writes.
- [ ] Record all counts, requested/effective shots, submitted circuits, hashes, schedules, and failures.
- [ ] Confirm every intended noisy gate receives the specified channel using positive controls.
- [ ] Freeze software and retain the exact Git commit plus dirty patch when applicable.
- [ ] Validate accelerated response-table sampling against actual circuit execution.
- [ ] Keep response-table noise assumptions explicit; do not use it to simulate unmodeled drift.
- [ ] Measure pilot wall time, memory, depth, and failure rate before finalizing the main matrix.
- [ ] Reserve compute capacity for failed runs, replication, and corrections.

## Comparators and statistics

- [ ] Include fixed IQAE, direct quantum sampling, depth-limited estimation, and a modern noise-aware method.
- [ ] Apply known stopping-bias treatment where appropriate and count its overhead.
- [ ] Include closed-form/quadrature references, control-variate MC, and scrambled Sobol RQMC.
- [ ] Use Brownian bridge or PCA for path-dependent RQMC and count every scramble/path.
- [ ] Match target accuracy, confidence interpretation, and tuning budgets.
- [ ] Freeze held-out contracts/regimes before comparing the resource controller.
- [ ] Predeclare delivered error, erroneous precision claims, completion, and abstention as primary outcomes.
- [ ] Report erroneous declarations both unconditionally and among declarations.
- [ ] Plan enough independent trials for the desired reliability precision; do not infer 95% reliability from 20 runs.
- [ ] Preserve failed and missing first attempts in denominators; link retries separately.
- [ ] Resample within contracts for fixed-benchmark uncertainty; justify any population-level generalization.
- [ ] Report query counts, shots, maximum depth, total gates, setup/calibration costs, and simulator runtime separately.

## Transfer and publication package

- [ ] Validate digital payoff semantics and an arithmetic Asian stress case independently.
- [ ] Label the actual quantum dimensions executed; separate larger classical-only sweeps.
- [ ] Add hardware only if matched pricing circuits produce interpretable evidence.
- [ ] Complete the ablations in the report and publish negative outcomes.
- [ ] Build every primary figure/table from a single frozen analysis manifest.
- [ ] Ask an independent collaborator to reproduce the small benchmark and verify manuscript claims.
- [ ] Refresh the literature search and novelty matrix before submission.
- [ ] Select QIP subscription by default; consider Quantum/QST only if the realized contribution supports the stretch.
- [ ] Recheck actual publisher charges, institutional agreements, and posting policies.
- [ ] Record real author contributions, final approval, and accountability.
- [ ] Disclose any prior proceedings paper and describe the substantive extension where applicable.
- [ ] Prepare code/data availability, funding, competing-interest, and applicable AI-use statements.
- [ ] Submit to one journal at a time; allow a separate, uncertain peer-review timeline.
