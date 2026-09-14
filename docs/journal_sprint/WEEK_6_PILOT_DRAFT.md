# Next discovery pilot: calibration cost and transfer-position sensitivity

Historical draft. Subsequently executed under
[week-6 v1 protocol](PROTOCOL_W6_TRANSFER_GRID.md); see [results](WEEK_6_RESULTS.md).
The draft text below preserves the state before execution.

Draft chosen from week-5 discovery; no observations generated here. This is
not a protocol freeze or a promotion of the best observed configuration.

## Question

Does the E001 CX-capped delivery signal persist across the allowed readout
transfer region, and do additional calibration shots materially improve useful
dollar delivery for the other bound-feasible contracts?

The favorable week-5 transfer pair lies at a corner of the supplied rectangle.
Do not infer robustness across that rectangle from this one corner and its
center. Retain all C6 contracts and pre-refusals, not only the favorable E001.

## Proposed pilot matrix for review before execution

- Fixed n=6/c=.125 and $1 tolerance; no representation search in this pilot.
- Reference A budget 294912; retain direct, A-matched and CX-capped schedules.
  Pricing CX is one cost axis only; calibration and other operations stay visible.
- Calibration shots per state 4096 and 16384, with independent draws for every
  design trial. Report marginal calibration cost, not hypothetical amortization.
- Calibration f=.02,g=.07; validation rate changes on the grid
  df in [-.02,0,.03] and dg in [-.03,0,.03]. All nine resulting rate pairs are
  valid probabilities and inside the supplied .03 allowances. This is a chosen
  grid, not a sampled real-device population or a guarantee over every rate.
- 100 repetitions per cell; fixed alpha_cal=.025/alpha_validation=.025, no
  optional stopping. Total proposal: 32400 attempts, before execution limits.
- Retain all interval components, median-radius denominators, containment,
  delivery, false declarations per attempt/acquisition and among declarations.

## Gates before running or expanding

1. Review the matrix and finalize a versioned prospective protocol. Bound
   calculations and resource ledger checks precede all diagnostic target access.
2. Estimate local runtime/storage from completed discovery; set a between-cell
   time limit and preserve partial failures. No hardware or paid service implied.
3. Predefine contrasts (within a rate cell and design, calibration-budget effect;
   within a rate cell and calibration budget, each multidepth design vs direct).
   Do not use a post hoc best rate cell as a robustness summary.
4. Test any claim about the source of non-delivery with separately declared
   ablations; do not infer a universal precision floor from finite budgets.
5. Only after these fixed-design checks consider a pilot-based selector using
   allowed observations and bounds, followed by a fresh fixed validation batch.

The current prior-work distinction remains a candidate reliability/resource
study, not a demonstrated new generic amplitude estimator. Modern-estimator
head-to-head fairness and numerical certification remain separate open work.
Held-out confirmation, author approvals, Macroscope and PR gates remain open.
