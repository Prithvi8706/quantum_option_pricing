# Week 12 working record

2026-09-16. Started after PR #2 merged at `c7511947`. GitHub PR comments,
inline reviews and open issues were checked: none were present. Macroscope was
SKIPPED, not an approval. Work branch: `research/week12-unequal-calibration`.

## Stage A: policy and terminal-inference foundation

- Added `unequal_allocation.py` without changing historical producers: five-arm
  batch planning, explicit m0/m1/n and paid-pilot costs, shared candidate menu,
  deterministic target/fallback rules and fresh-batch unequal-count CP adapter.
- Specified the forecast before any development observations in
  [policy protocol](PROTOCOL_W12_POLICY_V1.md). It is a normal-variance planning
  heuristic, not a delivery certificate or probability estimate. Fixed-target
  uses an explicit prior design amplitude, never evaluator truth.
- Preserved old fixed and equal-pilot allocation behavior. Pilot counts cannot
  enter the terminal interface; fixed arms reject current-trial pilot input.
  The future runner must still enforce actual sample separation.
- Documented conditional-on-pilot CP/union-bound containment and deterministic
  bias/transfer assumptions. Numerical padding remains an engineering limitation.
- 53 new unit tests passed in 2.71 seconds; changed-file Ruff passed. Independent
  binomial-tail endpoint checks cover unequal calibration sizes, boundaries and
  incompatible counts; exact binomial sums check selected coordinate-coverage cases.

Full regression: **633 passed, 11 legacy Qiskit warnings, 302.60 seconds**;
report `results/journal_sprint/tests_week12_policy_v1.xml`. Used the existing
Python environment with BLAS/OMP/MKL thread counts set to 1 and bytecode writes
disabled. This is not fresh-environment reproduction. New-document local links
and Git whitespace checks passed. No runtime-pilot, primary-development or
secondary-development observations have been acquired.
No claimed performance improvement, quantum novelty or quantum advantage.

Stage A is complete and locally verified; week 12 remains in progress. Changes
are local on the work branch, not committed/pushed or included in a new PR.

## Stage B: reviewed source freeze and production runtime pilot

The stage-A status above is historical. Subsequent separate reviews are recorded
in [review dispositions](WEEK_12_REVIEW.md), including the pilot-v1 test-stream
exposure and prospective fresh pilot-v2 correction. Both reviewers found no
remaining acquisition blockers after fixes. 104 focused tests and a fresh full
suite of 684 tests passed (11 legacy Qiskit warnings, 321.87 seconds).

Producing implementation/protocol freeze: commit `9a97228a`. Production pilot-v2
completed all 90 rows in 1.739 acquisition seconds. The predeclared conservative
projection was 1244.864 seconds, below the 7200-second main workflow budget.
Strict source/event/numerical replay verified 90 rows and 205 files. The independent
audit checked 30 cells, 5,308,416 shots and 399,393,792 modeled logical CX.
These are synthetic development samples, not executed quantum circuits. The
optional NumPy environment-report warning about PyYAML did not prevent capture.

Main acquisition was launched only after that gate, with the unchanged 2000-row
primary and 5400-row secondary schedules. Its completion/result is recorded below
once acquisition and automatic replay finish; no outcome-based policy changes.

## Stage C: full development closeout

The main run and automatic replay completed: 7400 rows, 7721 files, 150.700s
acquisition and 297.210s total workflow. Independent arithmetic checked 185 cells.
Final separate-agent evidence reviews found no outstanding blockers. The primary
interest gate FAILED because unequal-target tied cost-aware fixed target at
8192 shots and 400/400 deliveries; secondary target delivery was worse.
All original observations and negative outcomes are preserved; no tuning/rerun.
The historical checklist below is now fully dispositioned; see
[final closeout](WEEK_12_CLOSEOUT.md) and [results](WEEK_12_RESULTS.md).

## Historical stage-A remaining gates (now dispositioned in final closeout)

- [ ] Acquisition runner: evaluator-only truth, purpose-separated random streams,
  exclusive outputs, before/after events, failed/partial attempt reconciliation,
  source/input/protocol snapshots and repeatable replay.
- [ ] Test schedules, all five arms, resource totals, refusal costs, deterministic
  replay and interruption recovery; freeze producing source before acquisition.
- [ ] Execute and verify the manifest's 90-row runtime pilot; retain all outcomes.
- [ ] Apply the two-hour projection gate including replay reserve. No expansion
  based on favorable delivery results; amend prospectively if runtime is infeasible.
- [ ] Run gated 2000-row primary and 5400-row secondary development studies.
- [ ] Analyze delivery/error uncertainty, actual and penalized costs, forecast
  calibration and the fixed interest threshold, including negative outcomes.
- [ ] Full regression, independent arithmetic/replay checks, final logs/closeout.

The original [manifest](WEEK_12_DESIGN_MANIFEST.md) controls sample counts,
thresholds and exclusions. This stage does not complete week 12.
