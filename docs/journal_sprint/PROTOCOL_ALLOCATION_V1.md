# Fixed-total-budget encoding/allocation check

Declared 2026-09-15 before new observations. Method development on known European
contracts, NOT an experiment on the 25 harder problems. No results required to
be positive; retain every outcome and any failed run.

- Six C6 contracts, existing n=6 linearized/exact_table profiles from verified
  rescue_encoding_v2 input files. Tolerance $1.0.
- Before any observation choose encoding minimizing cost*S^2/(tau-B)^2 over
  B<tau. Cost here is 1 per shot, since TOTAL SHOTS is the primary objective.
  This is a noiseless design proxy, not noise-robust dominance or true optimality.
  No true amplitude or price enters selection.
- Total cap 65536 acquisition shots per trial, including pilot and both calibration
  states. Logical CX reported separately. No wall-time/hardware advantage claim.
- Three arms: fixed_cp (16384 calibration/state and 32768 pricing); pilot_cp
  (1024 paid pricing-pilot shots, then allocation below); single_hoeffding
  (16384 calibration/state then earlier planner within remaining 32768 shots,
  possibly refusing/ending early). All use the same deterministic encoding choice.
  Main comparison is pilot_cp versus the strong fixed_cp baseline.
- pilot_cp uses observed pilot success rate and a DECLARED DESIGN ASSUMPTION
  f=.02,g=.07 to project CP interval widths for m in {1024,4096,8192,16384,24576}
  shots PER calibration state; n=65536-1024-2m future pricing shots. Rank by
  projected dollar radius, tie by m. Expected/rounded projection counts are
  forecasts, never measured data. Run the selected allocation even if forecast
  misses tolerance; actual terminal CP interval alone decides delivery.
- Discard pilot observations from validation inference. Draw both calibration
  states and pricing samples fresh AFTER allocation. No calibration stopping or
  pricing peeking. alpha_cal=.025, alpha_val=.025. One encoder means no extra
  across-encoder calibration correction. Future validity is conditional on pilot,
  and does not require the design f,g assumption to be correct.
- Two stationary simulated readout scenarios: (.02,.07) and (.07,.02), deliberately
  swapping asymmetry for the second scenario. Guards 0,.003,.03 are supplied
  allowances, not realized drift. Model excludes coherent gate/correlated errors.
- 30 repetitions, 6 contracts, 2 readout scenarios, 3 guards, 3 arms = 3240 rows.
  Fresh namespace allocation_v1; purpose-separated streams by full trial identity
  and pilot/calibration/validation. Arms use independent streams; not paired trials.
- Report all cells, forecast versus actual radius, calibration allocations,
  total shots/CX, refusals, interval misses and wrong declarations. Risk guarantee
  is per invocation, unconditional, model-conditional; not conditional on declaration
  or simultaneous across methods/3240 trials. No post hoc winner coverage claim.
- Exclusive archive with source/protocol/input snapshots and manifest. Deterministic
  replay plus algebra, invalid-input, and sample-accounting tests. Old archives and
  previous modules remain unchanged. No paid jobs or publication claim.
