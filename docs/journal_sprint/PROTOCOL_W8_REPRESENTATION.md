# Week 8 v1: paid pilot choice with fresh fixed validation

Local declaration before observations, informed by prior discovery; not externally
timestamped preregistration or held-out confirmation. No native-estimator claim.

## Fixed menu and policies

All C6; n in {5,6}, scale=.125, same analytical support convention and $1 tolerance.
Existing compiled k=(0,1,2) profiles only. Refuse representations with sufficient
deterministic bound >=$1 before quantum acquisition. No exact price/amplitude
enters the menu, ranking, transfer allowance or shot allocation.

Three policies: fixed_n5, fixed_n6, pilot_select. If no eligible candidate,
pre-refuse. A single eligible candidate is selected without any pilot. Otherwise
pilot each eligible representation with 1024 pricing shots per depth and
4096 calibration shots per state. Rank its observed conservative dollar hull
radius (empty hull is worst); ties choose lower n. This is a simple declared
heuristic, not predicted full-budget precision or a globally optimal controller.
If all pilot hulls are empty, the same deterministic tie-break still fixes a
candidate; only the independent final validation may declare precision.

Selector interface accepts exactly n and pilot radius for each eligible candidate;
reject diagnostic fields. A pilot radius includes that representation's known
deterministic bound. Keep all pilot counts/components, scores, costs and selected
validation schedule in a durable event before generating final observations.

## Confidence, independence and costs

Total **pricing CX cap 330301440 per procedure**, including every pilot pricing
circuit and the final batch. Subtract pilot CX before computing the largest equal
shots-per-depth validation ladder that fits the remainder. Fixed baselines have
no pilot charge. No rounding up, hidden overshoot or amortized pilot cost.
Validation calibration is always fresh: 16384 shots per state. Pilot and final
calibration/validation all have separate seed namespaces. Other policies use
independent draws. Supplied guard=.03 per rate throughout; alpha_cal=.025 and
alpha_validation=.025 for the final interval. Pilot intervals guide choice only,
are not reused or jointly claimed as a final confidence guarantee.

Calibration shots are separate: 32768 for each acquired final batch, plus 8192
per actual pilot candidate (maximum 49152 per procedure). This is equal capped
pricing-CX comparison, **not equal total shots, calibration or physical runtime**.
Record pricing shots/A-equivalents/CX/U, pilot/final phase costs, max depth/qubits,
classical bound/setup timing, and wall time. Refusals acquire zero observations.

Calibration f=.02,g=.07. Actual pilot and final validation rates are stationary
(.02,.07), small_transfer (.03,.06), boundary_transfer (.05,.04), under independent
draws; fixed common conditions are stipulated, not inferred from the pilot.
The assumed .03 allowance must hold for final validation regardless of selection.
Selection changes no assumption and does not certify real drift.

6 contracts x 3 conditions x 3 policies x 100 fixed repetitions = **5400 procedure
attempts**. Bound audit before draws: both n feasible for E001/E014/E025; n6 only
for E049; neither for E030/E038. Expected 3300 final acquisitions and 2100
pre-refusals, plus 1800 pilot candidate acquisitions. These are different units.

## Declared analysis and engineering screen

Report all 54 cells, choices and pilot expenditure, final interval components,
deterministic/statistical dollar-radius terms, nonempty denominators, containment,
declared precision, incompatibility and false declarations per attempt/final
acquisition/declaration. Compare selector-minus-fixed separately against each
fixed policy within each contract/condition using procedure-attempt denominators.
Independent draws across policies => descriptive unpaired contrasts.

Exploratory readiness requires selector >=90/100 delivery in every condition of
all four menu-feasible contracts, plus mean delivery improvement >=10 percentage
points versus **each** fixed baseline across those 12 equally weighted cells.
Check the pricing-CX cap and maximum calibration charge; preserve/investigate
every erroneous declaration. This is not significance, population reliability,
equal-total-cost superiority or a guarantee conditional on delivery. A pass only
permits separately designed independent validation, not confirmation on this data.

Do not silently change heuristic, menu, guard or thresholds after observing results.
No new oracle-readout inference, noisy native comparator or quantum advantage claim.
Full-branch geometry/radius decomposition is diagnostic, not proof that all
non-delivery can be cured by a tighter inference method or different representation.

## Integrity and limits

Save planned protocol/dependency/upstream hashes, source snapshots and deterministic
menu before diagnostic targets. Preserve durable per-procedure selection events
and final records; replay must reconcile both. Exclusive output directories.
Require 1 GB free disk; check 900 seconds / 250 MB combined records+events between
100-attempt cells. Expected local run below two minutes, based on week-7 34.48 s
for 21600 acquisitions attempts; storage estimate below 60 MB, not a guarantee.
Failures retain partial events/records and no completion marker. No paid service,
hardware job, PR, submission or author addition is implied by this protocol.
