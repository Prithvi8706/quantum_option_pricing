# Week-12 development design: unequal calibration and target delivery

Prospective handoff from week 11, 2026-09-15. No asymmetric-allocation result has
been acquired. This is a development design, NOT the week-15 confirmation protocol
or a quantum-algorithm/advantage claim. The exact policy implementation and its
conditional validity argument must be versioned and frozen before observations.

## Scope and hypotheses

Reuse the six C6 European contracts and verified n=6 profiles from
`rescue_encoding_v2`, with existing linearized/exact-table representations and
their explicitly scoped ideal-grid bias allowances. No new physical preparation
certificate is implied. Keep actual amplitudes/prices evaluator-only; policy
inputs contain only encoding metadata, design parameters and paid pilot counts.

Primary engineering question: can an unequal-calibration, target-delivery policy
reduce acquisition cost on the preselected easy regression case E001 without
sacrificing useful delivery? This case is already known to favor successful
fixed-CP delivery; it is NOT held out or evidence of generalization.
Secondary question: does unequal allocation help harder C6 cases or merely move
costs around? Preserve prior equal-pilot/fixed-CP ties.

## Fixed comparison contract

- Tolerance $1, total cap 65536 shots including every pilot/calibration/pricing
  observation. Primary axis is total shots; actual logical CX is separately
  recorded and cannot be called a matched-CX comparison without a separate design.
- Stationary simulated readout (.02,.07) and swapped (.07,.02); guards
  0/.003/.03. Guards are supplied transfer assumptions, not measured drift.
- First implementation uses a pilot followed by a fixed fresh terminal batch.
  No repeated peeking at fixed-time intervals, no pilot pooling into inference,
  and no Grover-depth adaptation in this development experiment.
- Separate m0, m1 and n. Candidate calibration counts drawn from
  {256, 1024, 4096, 8192, 16384, 24576}; minimum pricing 256. Candidate total
  caps {8192, 16384, 32768, 65536}, including a 1024-shot pilot when applicable.
  Reject infeasible combinations explicitly. A declared design model guides
  forecasting; final fresh-sample CP inversion, not the forecast, decides delivery.
- Fix the forecasting objective/tie rules before acquisition. A normal-variance
  heuristic can propose allocations but is not a finite-sample certificate or
  proof of optimality. Incompatible or poorly conditioned design forecasts require
  an explicit fallback/refusal with paid costs retained.
- Retain the existing confidence split/transfer model and prove that conditioning
  on the pilot makes chosen terminal counts fixed; extend the two calibration
  coordinates to their actual distinct shot counts without weakening guarantees.

Five arms: existing fixed CP; existing equal-calibration paid pilot CP;
unequal-calibration paid pilot using the full cap; unequal-calibration paid pilot
targeting lower total cost; and a cost-aware fixed-design CP comparator using
the same feasible candidate menu, design information and terminal inference,
but no current-trial pilot. Its deterministic design assumptions/objective must
be frozen with the policy implementation before acquisition, without evaluator
truths or selecting the best fixed design retrospectively on reported outcomes.
The full-cap unequal arm isolates allocation from spending less; the cost-aware
fixed arm prevents a win solely against a baseline that always exhausts budget.
No method receives free discarded-encoder calibration.

## Acquisition and analysis budget

1. Pre-acquisition tests: unequal-count CP endpoints against independent binomial
   calculations; unknown B; count/cost validation; extreme amplitudes; transfer
   floors; simulated incompatibility; deterministic seed/replay and no-truth
   policy inputs. Do not claim a coverage proof from Monte Carlo alone.
2. Runtime pilot: six C6 cases, design readout, guard zero, three repetitions,
   five arms = 90 rows. Namespace `w12_asymmetric_pilot_v1`. Soft cap 15 minutes.
   If forecast evaluation is too expensive, amend the candidate search BEFORE
   the main development acquisition, preserving pilot outcomes.
3. Primary development cell: E001/design readout/guard zero, 400 independent
   trials per arm = 2000 rows, distinct namespace from the pilot.
4. Secondary development matrix: six C6 cases x two readouts x three guards x
   five arms x 30 trials = 5400 rows; disjoint namespace from the primary cell.
   The repeated primary cell in this matrix is descriptive, not extra tuning-free
   confirmation. Total maximum new rows including runtime pilot: 7490.
5. Main development wall cap two hours, launched only if runtime-pilot projection
   fits that budget including replay reserve. Otherwise record partial/defer or
   prospectively amend; no silent truncation based on results. No paid hardware.

400 trials bound a single Bernoulli proportion's worst-case standard error by
.025; this is a development precision rationale, not power for a 2-percentage-
point noninferiority claim. Secondary 30-trial cells are exploratory. Confirmation
requires its own effect-size/power/multiplicity plan and fresh held-out tasks.

Report delivery fraction and its uncertainty; interval misses; erroneous
declarations both unconditional and among declarations; total/expected shots;
logical CX; forecast versus observed radius; and failures/abstentions. For a
cost-oriented descriptive score, charge the full 65536 cap to a failed delivery
and actual cost to success, so refusing everything cannot masquerade as efficiency.
Keep actual consumed resources separately; the failure penalty is an analysis
convention, not an acquired shot count. Do not hide conditional-on-success costs.

Prospective development interest threshold: >=15% reduction in mean penalized
cost on the primary cell against BOTH fixed CP and the cost-aware fixed-design
arm, with delivery point estimate >=.95 and no more than .02 below either fixed
comparator. Report confidence intervals even if these descriptive
thresholds pass; passing is permission to consider confirmation, not proof of
superiority/noninferiority. A failed threshold is a negative development result,
not a reason to replace E001, lower the threshold or erase the experiment.

This supporting allocation work does not close the separate quantum contribution
gate. A quantum-centered paper still needs validated encoding/preparation,
nonzero-depth AE and full-cost comparison against the week-11 classical baseline.
