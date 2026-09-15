# Week 10 evidence-gate closeout

2026-09-15. Week-10 evidence-gate work completed and locally verified.
This week defines, tests and evaluates next-stage feasibility. It does not
promise that every unresolved research problem has been solved.

## Deliverables and disposition

| Gate | Result |
| --- | --- |
| Full methods comparison with screened basket paper | Completed bounded HTML methods/results review; [overlap and target audit](WEEK_10_WORKING.md). No source reproduction or broad priority claim. |
| Predeclared numerical stress | Original 80 cases retained; required topology gate failed. Separately disclosed three-case diagnostic extension passes. |
| High-precision strategy | Closed-form large-shot boundary tails checked against small-count beta inversion; polynomial branch inversion at 80 and 100 digits. |
| Feasible matched comparison | [Concrete E001 design](WEEK_10_MATCHED_DESIGN.md), bounds recomputed, classical budget 6999; native stopping-guarantee audit required before execution. |
| Scientific decision before confirmation | NO-GO for frozen confirmation or submission now; GO for further methodological development. |

## Numerical evidence

`results/journal_sprint/week10_stress_v1`: 80 cases, zero enclosure failures,
zero precision instabilities, 40 disconnected final sets, 10 empty sets,
but zero disconnected final [1,2] intersections. Execution completed;
the scientific topology criterion failed. No original result was replaced.

`week10_stress_v2`: disclosed extension to 83 cases, zero enclosure failures,
zero instabilities, 43 disconnected final sets, including three disconnected
[1,2] intersections; 10 empty. The extension was selected after an exploratory
production-only probe, not independent confirmation.

`week10_stress_v3`: same 83 cases after source formatting, same counts and
byte-identical records as v2 (SHA256
`21fc2c6219a91090eaa183f06d5bbaa6213f86b91c981b1d6c11c8829836ce39`).
Use v3 with current producing sources; earlier archives retain their original
snapshots. v3 is a replay, not new independent evidence.

The small-count boundary-identity validation's largest endpoint difference
was 5.10588878461e-49. Large-shot cases use 30000 and 100000 shots with zero
or all successes. Interior counts at those sizes remain unvalidated. Calibration
is the explicitly restricted zero-error, 64-shot scenario with guards 0/.01;
do not generalize this matrix to arbitrary calibration or physical noise.
160 bisections and finite high-precision arithmetic are not directed intervals.

## Verification

Separate `verify_week10` checks complete output and source inventories, hashes,
live producer identity, case identity, all 83 deterministic replays, summary
counts, enclosure, precision stability and required disconnected topology.
v3 passed: 83 records replayed, 11 archived files checked. Reports live outside
the immutable run directory. This is implementation-independent numerical
reference checking plus replay, not independent human review or fresh
Macroscope/Astra approval.

Final-tree regression: **420 passed, 11 upstream warnings, 295.86 seconds**;
report `results/journal_sprint/tests_week10_final_v1.xml`. The warnings concern
the existing Qiskit packaging/deprecations, not new test failures. Ten focused
week-10 tests include analytic boundary identities, disconnected intersections,
scope rejection and verifier tampering checks. Ruff passed for all three new
Python files; `git diff --check` and local documentation link checks passed.
Final replay report: `results/journal_sprint/week10_verification_final.json`.
An earlier integrated run passed 418 tests before two verifier tests were added;
the final 420-test run supersedes that regression count.

## Why confirmation is held

The new diagnostic strengthens reliability testing, not estimator novelty.
Existing declaration success remains concentrated on E001; the paid controller
still has no demonstrated delivery gain. The bounded methods comparison does
not establish a sufficiently distinctive journal contribution. A substantive
methodological advance or a convincingly scoped reliability contribution with
matched evidence is needed before claiming a strong journal candidate.

Next-stage priorities: resolve native adaptive-stopping comparability; implement
the matched runner with exact summation and complete costs; validate general
large-count interior tails if that numerical claim is pursued; then freeze a
confirmation protocol with fresh seeds and justified replication. Submission,
authorship verification, journal fees and external PR review remain later gates.
No new quantum advantage, unconditional coverage or successful adaptation claim
is supported by week 10.

## Reproduction

From the repository root, using the existing environment (choose new output
paths; archives cannot be overwritten):

```powershell
venv\Scripts\python.exe -m research.journal_sprint.week10_stress --extension --output results/journal_sprint/week10_stress_replay
venv\Scripts\python.exe -m research.journal_sprint.verify_week10 --source results/journal_sprint/week10_stress_replay --report results/journal_sprint/week10_replay_verification.json
venv\Scripts\python.exe -m pytest -q
```

Outputs are local workspace artifacts, not automatically published by creating
these files. No new PR, push or merge has been performed for week 10.
