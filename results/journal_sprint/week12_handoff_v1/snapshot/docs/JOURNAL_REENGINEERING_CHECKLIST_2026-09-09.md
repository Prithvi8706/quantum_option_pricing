# Journal Reengineering Checklist

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
