# Week 1–2 closeout

Evidence availability: historical result, reading and test paths below refer to
the originating local workspace unless explicitly listed as included in the PR.
See [archive inputs and reconstruction](ARCHIVE_INPUTS.md) for the preserved
location, exclusions and configurable verification commands.

Continuation: [week 3 circuit validation and baseline development](WEEK_3_PROGRESS.md).

10 September 2026. **Technical feasibility sprint complete; administrative sign-off pending.** Neither paper has been submitted or published. The outcome is a tested foundation for a stronger study, not a journal-ready paper or a demonstrated quantum advantage.

## Start here

| Deliverable | File |
|---|---|
| Revised scientific narrative | [Replacement working manuscript](MANUSCRIPT_WORKING_DRAFT.md) |
| Six full-paper readings and novelty assessment | [Literature supplement](LITERATURE_SUPPLEMENT.md) |
| Finite-shot dollar outcomes | [V2C results](PRICE_INTERVALS_V2C_RESULTS.md) |
| Next-stage design, before confirmation | [Prospective amendment draft](PROSPECTIVE_AMENDMENT_DRAFT.md) |
| Historical Paper B disposition | [Evidence disposition](PAPER_B_EVIDENCE_DISPOSITION.md) |
| Small genuine collaborator tasks | [Team work packages](TEAM_WORK_PACKAGES.md) |

## Completed first-two-week work

The historical data and manuscripts were preserved and their claims audited. The expanded sweep's deviation from a precomputed quantum reference was distinguished from continuous Black–Scholes error. The replacement manuscript removes the unsupported discretization-floor claim. Both disputed Paper B slope sets are excluded because neither has adequate producing-run evidence; no historical result was fabricated or silently selected.

All six assigned primary papers have been read in full text, including appendices and references. The literature supplement separates established tools from the candidate application contribution and identifies specific calibration, cost and statistical gaps. Two additional 2026 low-depth papers were abstract-screened and explicitly remain future full-reading candidates.

A modern source benchmark was pinned and reproduced with golden tests and reduced independent replication. The sprint implemented conservative all-branch interval inversion, independent pilot/validation streams, model-mismatch tests and explicit refusal/incompatibility outcomes. The original generic prototype retained 26,600 records; comparator work retained 160,000 estimations on 140,000 distinct generated datasets.

Application work then derived and checked contract-specific dollar bounds over 72 configurations. A tighter grid bound increased the count with positive one-dollar statistical allowance from 4 to 14, spanning four of six pilot contracts. V2C added 43,200 attempt records, including 36,000 executed response simulations and 7,200 pre-refusals. All were verified for unique identity, interval reconstruction and resource arithmetic.

The first section of the [master checklist](../JOURNAL_REENGINEERING_CHECKLIST_2026-09-09.md) has 13 of 14 items closed. The sole remaining item is an actual agreement on contributor responsibilities, available time and budgets. The later scientific/publication sections remain later-stage requirements and are not marked complete merely because the feasibility sprint is done.

## Main finding and decision

At the largest tested shot budget, fixed ideal multidepth estimation delivers one-dollar intervals in 51.08% of all attempts, versus 33.33% for equal-A-query direct quantum sampling. This is a useful model-based pilot result. It does not establish superiority over the best classical pricing algorithms or modern AE methods.

The bound-only selector principally saves resources by refusing the two infeasible contracts. It does not yet demonstrate an adaptive scheduling benefit. The evidence supports the research direction **contract-aware delivered precision with auditable bounds and costs**; it does not support a generic new-estimator or hardware-advantage claim.

Proceed to the bounded methods-development gates in the amendment: circuit-level response checks, stronger baseline implementations, resource profiling and a frozen confirmation design. Do not launch an expensive main matrix or submit the current manuscript. If adaptation fails against a strong fixed method, retain the fixed method and report that negative result.

## Verification record

- Full repository regression: **225 passed, 9 legacy Qiskit warnings, 410.62 seconds**, before the three closeout-analysis unit tests were added. XML: `results/journal_sprint/tests_week12_closeout.xml`.
- Updated sprint suite: **64 passed, 9 warnings, 18.90 seconds**, including the three new denominator/interval tests. XML: `results/journal_sprint/tests_closeout_sprint.xml`. These overlap the full suite; they are not 289 distinct tests.
- All 43,200 V2C records checked; V2A successful retry, V2B and V2C archived manifest hashes passed. Machine-readable evidence: `results/journal_sprint/week12_closeout_v1/verification.json`.
- Ruff checks pass for the sprint source, excluding the preserved third-party vendor file under the existing lint configuration.
- Existing user edits were preserved. Original manuscripts, historical datasets and the failed first V2A attempt remain intact. No commits, submissions, author additions, external messages, paid services or hardware jobs were made.

Source formatting and the explanatory timing string were cleaned after the verification run; the run retains its original source snapshot. This affects neither its raw inputs nor calculations. The final handoff snapshot records the final files separately.

## Human sign-off still required

The two collaborator packages are deliberately bounded at an estimated initial 3–5 hours each plus later manuscript review. No acceptance or completed contribution has been inferred. Their independent work must actually occur; generated notes under their names would not constitute independent review.

Please supply the lead's weekly availability, whether each collaborator accepts the proposed package, and the maximum publication fee. Until then the operating assumption remains local-only compute with no paid services. Actual authorship must reflect completed qualifying contributions, final approval and accountability—not the reason someone wants a publication.

## Reproduce without overwriting

From the repository root, use the existing environment:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe -m research.journal_sprint.closeout --output results/journal_sprint/week12_closeout_independent_01
```

Choose a new output directory for every independent run. The verification command re-inverts the saved observations; it is not an independent stochastic replication. For a new V2C simulation, use `python -m research.journal_sprint.run_price_intervals --output` with a new directory; the existing purpose-separated seeds reproduce the same protocol draws unless a prospective replication amendment changes them.
