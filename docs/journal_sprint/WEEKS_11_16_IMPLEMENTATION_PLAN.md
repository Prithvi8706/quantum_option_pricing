# Revised implementation plan: weeks 11-16

Updated 2026-09-15. Status: prospective plan, not executed week closeouts.

This is the active forward plan for the remaining six working-week blocks of
the [original roadmap](../JOURNAL_REENGINEERING_RESEARCH_2026-09-09.md).
Weeks 1-10 retain their recorded development closeouts; completed development
does not mean that confirmation or submission gates passed. In particular,
[week 10](WEEK_10_CLOSEOUT.md) closed with NO-GO for confirmation/submission.
The subsequent encoding/allocation/shortlist work is reusable preparation, not
retroactive completion of weeks 11-16. Historical archive names do not override
this schedule. The original 4-8-week reserve remains a contingency, not work
silently squeezed into these six weeks. Calendar duration depends on capacity.

## 1. Paper objective and scope

Scope clarification following the user's quantum-paper discussion: the intended
paper remains quantum-centered. Primary question: after state preparation,
payoff evaluation, uncomputation, calibration and precision costs, can a concrete
quantum encoding plus amplitude-estimation procedure offer a defensible resource
benefit against the best applicable classical solver? A benefit must be tested,
not assumed; a novel quantum contribution remains unestablished.

Supporting question: can an encoding-aware, calibration-aware decision procedure
deliver a specified dollar tolerance more reliably or at lower total cost than
strong fixed and adaptive alternatives, under explicit assumptions? Statistical
allocation or classical baseline work alone does not fulfill the primary aim.
The six-week sequence remains unchanged; the week-14 paper-scope decision must
explicitly distinguish a quantum result from a narrower reliability alternative.

Target ONE integrated paper: a validated quantum encoding/estimation contribution
supported by a conditional decision method, matched comparisons and clearly
bounded application transfer. A reliability-only alternative needs an explicit
scope decision, not automatic substitution for the user's original objective.
European/digital contracts remain regression controls. Asian baskets are the
primary harder application to attempt, not an assumed quantum advantage case.
The [25-problem survey](HARD_PRICING_25.md) is a selection map, not a promise to
implement 25 algorithms. Heston and genuine nested exposure receive bounded
feasibility audits; at most one can replace the Asian application before the
week-14 freeze, with an explicit schedule/scope revision. Otherwise they remain
documented follow-on projects.

Candidate novelty is the decision problem and its validated solution, NOT new
CP intervals, confidence sequences, PCA, control variates or QAE. A distinct
theorem, useful decision result or substantive reproducible finding must still
be established against the nearest prior work. A renamed combination is not
enough. Neither publication readiness nor quantum advantage is guaranteed.

## 2. Starting evidence: reuse, do not rerun as confirmation

| Available component | Evidence and limitation |
|---|---|
| Fixed/sequence inference, dollar mapping, calibration and replay | Existing foundation; guarantees remain conditional on the declared response/transfer model |
| Exact finite-grid payoff oracle | Reduced direct circuit resources and rescued two European cases; exponential table construction, not scalable loading |
| Encoding-aware conservative planner | Implemented with refusal and cost accounting; sufficient screen, not an optimal rule or impossibility test |
| Paid equal-calibration pilot | 300/1080 declarations, identical aggregate count to fixed CP; no established delivery improvement |
| Asian classical benchmark | 12 contracts, 768 main estimates and 192 independent reference estimates; strong PCA/control/conditional RQMC, no quantum Asian implementation in this benchmark |
| Heston/nested diagnostics | Scalar applicability screen and analytically soluble nesting negative control; neither is a quantum pricing solver |
| Regression verification | Last recorded full suite: 504 passed; software correctness checks are not a novelty or coverage proof |

Evidence: [rescue](RESCUE_RESULTS.md), [decision rule](ENCODING_DECISION_RULE.md),
[allocation](ALLOCATION_RESULTS.md), [shortlist follow-through](SHORTLIST_FOLLOWTHROUGH.md).

## 3. Architecture: extend the research package, keep archived methods frozen

```text
Financial task + target price + tolerance + confidence + resource cap
    -> candidate representations: offset O, sensitivity S, bias bound B, costs
    -> design/pilot policy: encoding, calibration m0/m1, pricing cap/depth
    -> fresh acquisition + valid fixed-time or sequential inference
    -> dollar interval + deliver/refuse + complete resource ledger
    -> matched classical/quantum evaluation -> replay -> claim ledger/manuscript
```

Classical estimators are parallel evaluators of the same financial target, not
observations to feed into the Bernoulli interval machinery. Reference truths,
statevector amplitudes and held-out results stay outside controller inputs.

| Layer | Reuse | Planned extension |
|---|---|---|
| Targets/references | `asian_basket.py`, `classical_baselines.py`, `numerical_reference.py` | Isolated cost-to-accuracy reference studies and uncertainty-aware comparisons |
| Encoding/error contract | `exact_payoff.py`, `pricing_bounds.py`, `encoding_decision.py` | Explicit componentwise bias/resource record; bounded Asian encoding prototype |
| Design policy | `allocation_rule.py` | New versioned unequal-calibration/target-delivery policy, retaining old arms |
| Inference | `calibrated_readout.py`, `intervals.py`, `anytime_readout.py` | Conditional validity for the actual selection/stopping policy; depth extension only if justified |
| Comparators/resources | Existing IQAE/BAE/BIQAE integrations and circuit/resource tools | Audit native stopping, actual execution costs and small nonzero-depth comparisons |
| Evidence | `storage.py`, runners, verifiers and tests | Fresh protocols, exclusive output directories, independent reference checks and frozen analysis manifest |

All code paths above are under `research/journal_sprint/`. New modules/names are
to be settled in the relevant week; this document does not claim they exist.
Do not refactor away historical implementations or make the dashboard the source
of scientific truth. Preserve failed attempts and snapshot the dirty patch plus
environment whenever an experiment is run.

For each encoding require `|P - (O + S*a)| <= B`, with B accounting for relevant
tail/renormalization, discretization, loading, payoff arithmetic and synthesis
errors. Use compatible targets and justified propagation bounds to avoid double
counting. Record empirical error separately from certified bounds; an unknown
component blocks a certified claim. A supplied readout-transfer guard does not
certify arbitrary gate noise, correlations or drift.

## 4. Six-week implementation sequence

### Week 11 — Freeze the question, error contract and strong baselines

1. Reconcile the evidence/claim matrix and existing uncommitted work without
   discarding any archive. Mark each artifact as development, confirmation or
   diagnostic; retain the negative allocation result.
2. Specify the encoding/error/resource interface above, with explicit units,
   assumptions, unsupported-state handling and no-ground-truth-input tests.
3. Define an economically motivated tolerance ladder, confidence meanings,
   total-budget axes and development/held-out split before new comparisons.
   Select tolerances for the pricing use case, not after observing a quantum win.
4. Refine Asian numerical references and run isolated, interleaved classical
   timings. Charge PCA/setup, pilot/control fitting and inference separately
   and end-to-end; report both one-off and explicitly amortized workloads.
   Target reference uncertainty below a predeclared fraction of tolerance
   (proposed: 10%); unresolved reference uncertainty blocks precise rankings.
5. Update nearest-prior-work distinctions and estimate pilot runtime/memory.
   Freeze a bounded week-12 experiment manifest and stop/expand criteria.

Deliverables: interface/specification tests, baseline/reference report, novelty
matrix update, compute estimate, and `WEEK_11_CLOSEOUT.md` with explicit blockers.
Gate: comparable targets and costs, adequate references, a testable primary
claim and executable local budget. No hardware access assumed.

### Week 12 — Unequal calibration and tolerance-delivery policy

1. Implement separate calibration counts m0 and m1 plus pricing count/cap n.
   Use the existing delta-method allocation only as a planning heuristic; it
   is not the final interval, a proof of optimality, or a measured benefit.
2. Choose the encoding and allocation using declared design inputs and/or a
   paid pilot; acquire fresh terminal calibration and pricing observations.
   Include pilot costs, minimum counts, uncertain design rates, both readout
   asymmetries and transfer-floor sensitivity.
3. Optimize predicted probability of tolerance delivery or target-constrained
   cost, rather than spending the full budget to minimize width. For the first
   implementation keep a fixed fresh validation batch. Any early stopping or
   depth adaptation must use an explicitly valid sequential construction;
   repeatedly inspecting fixed-time CP intervals is not acceptable.
4. Derive/check the conditional containment statement for the implemented
   policy. Test extreme amplitudes, nonidentifiable readout, B >= tolerance,
   disconnected/empty sets, numerical boundaries and infeasible budgets.
5. Run matched development comparisons against fixed CP, equal-calibration
   pilot CP and the conservative planner. Include equal total shots and
   separately equal logical-gate budgets; retain all abstentions and failures.

Deliverables: versioned policy, mathematical assumptions/argument, focused and
full regression tests, frozen development protocol, replay and ablation report.
Gate: a valid procedure and an honest effect estimate. A tie is a negative
result, not grounds to tune on confirmation data. If there is no useful distinct
effect, narrow the method claim and reassess novelty before a large campaign.

### Week 13 — Harder-payoff encoding and state-preparation feasibility

1. Build a small Asian-basket quantum encoding with independently checked
   semantics. Start at simulator-feasible assets/dates/precision selected by
   the week-11 pilot; the existing 2/4-asset, 12/52-date classical sweep does
   not imply circuits at those dimensions can be simulated.
2. Compare raw and at most one promising residual/conditional representation.
   Tighten payoff-aware truncation and scale bounds; account for signed
   residual ranges and any root/CDF, arithmetic, loading and uncompute costs.
   Give the classical comparator the same mathematical simplifications.
3. Use the existing finite table as a small correctness reference, NOT evidence
   of scalable preparation. Assess one structured preparation/arithmetic route
   with explicit accuracy/resource dependence. If unavailable, label larger
   results as cost models or blocked feasibility, not executed quantum prices.
4. Reserve at most one of five working days for the two alternative audits:
   Heston full theorem assumptions/coherent sampler costs, and one genuinely
   path-dependent nested target with classical MLMC/RQMC/surrogate baselines.
   Document missing proofs, moment bounds and sampling access. Do not expand
   the soluble nested toy into a claimed advantage benchmark.

Deliverables: small-circuit validation, componentwise error budget, measured
small-instance resource counts, larger-instance assumptions, and route decision.
Gate: a justified bias allowance below tolerance and an explicit acquisition
cost model for any certified application claim. If the Asian route fails,
retain it as a documented limitation; do not pretend a research blocker was
solved. Replacing it requires a visible replan, potentially using the reserve.

### Week 14 — End-to-end comparisons, ablations and pre-confirmation review

1. Connect the validated policy to the encodings that passed week 13. Compare
   direct sampling with faithful fixed IQAE, depth-limited AE and at least one
   modern noise-aware comparator where its implementation/model applies.
   Audit native stopping and guarantee interpretation; a posterior interval
   is not automatically a frequentist certificate.
2. Include actual small nonzero-Grover-depth executions if feasible. The k=0
   allocator alone cannot establish an AE query speedup. Validate synthetic
   response tables against the circuits/model they purport to represent.
3. Compare against closed form/direct finite summation where available and
   strong MC/control/PCA-RQMC/conditional methods for the harder application.
   Report cost-to-tolerance, confidence interpretation and setup amortization.
4. Ablate encoding, equal/unequal calibration, pilot cost, stopping, depth and
   transfer allowances. Stress model mismatch and distinguish failure outside
   assumptions from violation of an in-model guarantee.
5. Audit queries, shots, logical CX/depth, qubits and classical runtime separately.
   Any fault-tolerant crossover is conditional on stated logical-to-physical
   overheads, synthesis accuracy, clock rates and parallelism; simulator timing
   is not quantum-device runtime. Investigate variance-aware estimation or
   coherent QMC only if it addresses a measured bottleneck and fits the budget.
6. Perform independent-formula/replay review and request bounded collaborator
   review of selected claims. Freeze the method, one primary application,
   primary outcomes, held-out regimes and analysis before confirmation.

Deliverables: comparison/ablation report, updated claim matrix, resource audit,
review issue dispositions and signed-off confirmation protocol where possible.
Gate: validity and a defensible prior-work distinction, not necessarily quantum
superiority. If neither a useful method result nor a substantive limitation
study survives review, remain in development and use/revise the reserve.

### Week 15 — Fresh confirmation and independent reproduction

1. Run only after the week-14 gate passes. Use new seeds and held-out contract/
   noise regimes not used to choose the method; discovery reruns are not fresh
   confirmation. Choose repetitions from the predeclared effect/uncertainty
   target and multiple-comparison plan, not a default of 30 trials.
2. Report tolerance delivery, interval coverage, erroneous declarations both
   unconditional and among declarations, completion/abstention, and total cost.
   Give uncertainty intervals and retain first-attempt failures in denominators.
   Use independent scrambles for RQMC uncertainty and label approximate coverage;
   do not apply binomial CP inference to correlated Sobol points.
3. Reproduce the small benchmark from pinned source in a fresh environment/output
   directory. Independently check raw counts, a mathematical reference and one
   full table. Automated independent-formula checks are not human peer review.
4. If a material bug changes the frozen method, preserve the failed campaign,
   issue a versioned amendment and obtain genuinely fresh confirmation data.
   No quiet retuning or selective removal of losing regimes.

Deliverables: confirmation archive, full tests, replay/hash report, uncertainty
analysis and independent reproduction note (human review only if actually done).
Gate: claims survive the frozen analysis, or are explicitly narrowed/withdrawn.
If development remains blocked, record that instead of calling week 15 a
completed confirmation campaign.

### Week 16 — Manuscript, artifact review and submission-readiness decision

1. Finish the integrated manuscript: precise contribution/prior work, error and
   selection theory, implementation, classical/quantum comparisons, held-out
   results, negative findings, limits and reproducibility. Draft these sections
   incrementally during weeks 11-15, not all from scratch in the final week.
2. Generate every primary table/figure from a frozen analysis manifest. Check
   each claim against a proof, actual run or clearly labeled resource model.
3. Finish clean-environment smoke/replay tests, license/dependency and artifact
   audits. Reconcile intended changes into a reviewable diff without deleting
   user work or staging large/unrelated archives indiscriminately.
4. Obtain actual external critique; use Macroscope/Astra if connected and
   authorized at that time, and record unavailable checks honestly. Automated
   reviews do not replace collaborator accountability. Prepare a reviewed PR
   package; publication of a PR/merge follows the applicable explicit request.
5. Refresh the literature/novelty assessment and verify current quantum-focused
   journal fit, subscription/APC/waiver options and posting policies from official
   sources. No price or journal acceptance is guaranteed by this plan.
6. Record actual contributions, final author approval, funding/conflicts,
   code/data availability and applicable AI-use disclosures. Limited contributor
   work follows [these packages](TEAM_WORK_PACKAGES.md), not automatic author
   slots. Obtain human decisions on venue, fees and submission.

Deliverables: reproducible submission candidate, review/correction log, journal
fit/fee note, author approvals where supplied, and `WEEK_16_CLOSEOUT.md`.
Gate: submission-ready only if scientific, reproducibility and human sign-offs
are complete. Otherwise list the exact outstanding work. Submission, paid jobs,
and external messages are not authorized merely by this planning document.

## 5. Workload, evidence discipline and outcome labels

The lead owns implementation and the main analysis. Two small substantive
collaborator packages remain independent comparator reproduction and statistical
limitations review, initially estimated at 3-5 hours each plus final manuscript
review, subject to actual competence/availability. No work or review is attributed
to someone who did not perform it. Do not make the core implementation depend on
unconfirmed collaborators; independent human review remains a readiness item.

Every week records: planned versus completed tasks, commands/environment/source
hashes, tests/replay, all attempts/failures, measured results versus forecasts,
scientific gate decision and carried blockers in [PROJECT_LOG.md](PROJECT_LOG.md)
and its own closeout. Preserve previous checklists and archives; add evidence
links before marking a publication-level requirement complete.

Distinguish the eventual outcome explicitly:

- **Method improvement:** better matched-budget tolerance delivery or cost,
  with validated conditional guarantees and a demonstrated prior-work distinction.
- **Conditional quantum resource benefit:** a query/gate/crossover result whose
  loading, arithmetic, accuracy and hardware assumptions are all visible. This
  is not a measured end-to-end device win.
- **Measured end-to-end quantum advantage:** requires actual matched execution
  and strong classical comparison at the same task/accuracy; not promised here.
- **No advantage found:** publishable only if the methodological/limitation
  finding is genuinely new and sufficiently substantive for a suitable venue.
  Otherwise revise or extend; completing six blocks does not establish novelty.

Immediate next implementation task: week 11, beginning with the shared error/
resource contract and a frozen, independently timed classical baseline protocol.
