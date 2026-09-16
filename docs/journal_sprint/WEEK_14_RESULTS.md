# Week 14: finite-target comparisons and ablations

## Scope and provenance

Development completed under the week13 gate: **not** a certified continuous-price
benchmark, fresh confirmation, new AE algorithm, or quantum advantage result.
Producer/protocol freeze: `76914458`. The prespecified run completed all93tasks,
2022files/2399090bytes, from2026-09-16T15:41:18.900014Z to15:41:40.831970Z
(21.931956s elapsed). No production failure or unattempted task; all16native IQAE
trials completed without a cap. Cap/failure handling is tested with fixtures,
not represented as an observed production failure trace.

Evidence: `results/journal_sprint/w14_finite_v1`, external derived
`w14_analysis_v1.json` (58cells), external strict `w14_replay_v1.json`.
All93tasks and2022files numerically replayed, including raw checkpoints, frozen
plans, native ledgers, sources, environment and immutable week13 input identity.
Runtime fields are checked for validity, not numerical equality across replays.

The one application kernel is week13 case3: two assets, two dates, strike100,
one normal bit per independent dimension,16paths and5qubits. Its finite price is
18.585163266148694, not the continuous numerical reference near9.20. Residual
estimates add the **finite** geometric-control mean16.71328592428006, not the
continuous analytic mean8.466374499742882. Raw/residual payoff scales are
39.78319764432297/5.08412714637781. Both continuous contracts remain unknown_bias.

There are912trial outcomes:288fixed,480policy,16native IQAE,96csAE and32classical.
Matched/ignored-noise analyses reuse observations; these are not912independent
acquisitions. There are20separate exact response characterizations, not hardware
shots. Counts for policy/fixed/source csAE comparisons are seeded synthetic
draws under their specified models; native IQAE uses the finite-shot Sampler.

## Circuit response and resources

Compiled statevector and independent density evolution agree with ideal sine
and per-A/A-inverse global-depolarization formulas to2.254e-14maximum error,
over raw/residual, k=0..4 and eta=0/.02. Reflections are ideal in this model;
eta is known, not estimated. This does not validate arbitrary device noise.

| k | CX per circuit, both encodings | Raw unitary depth | Residual unitary depth |
|---|---:|---:|---:|
| 0 | 16 | 24 | 32 |
| 1 | 84 | 158 | 182 |
| 2 | 152 | 292 | 332 |
| 3 | 220 | 426 | 482 |
| 4 | 288 | 560 | 632 |

All use5qubits. Measurement-inclusive depths are separately recorded. Native
IQAE decomposition can differ from the fixed response circuits; use its actual
ledger, not the fixed table's depth. Aeq counts forward plus inverse preparation
calls; Q counts Grover applications. Reflections contribute to compiled CX.

## Main finite-target comparisons

Delivery means reported interval half-width at most$1, not proof of a$1 error
on every run. The table is the ideal-model diagnostic. Costs are per attempt;
native rows give observed means. No precision-matched efficiency theorem follows
from differently stopped methods or a single small target.

| Method | Shots | Aeq | Logical CX | Raw delivery | Residual delivery |
|---|---:|---:|---:|---:|---:|
| Direct, shot budget | 640 | 640 | 10240 | 0/16 | 16/16 |
| Direct, query budget | 3200 | 3200 | 51200 | 16/16 | 16/16 |
| Depth-limited CP,128shots at each k=0..4 | 640 | 3200 | 97280 | 16/16 | 16/16 |
| Native IQAE, raw | 512 | 1856 | 53888 | 8/8 | -- |
| Native IQAE, residual | 256 | 256 | 4096 | -- | 8/8 |

Thus multidepth's raw delivery benefit at equal shots is not an equal-query or
equal-CX advantage: direct3200 and multidepth both deliver, with1.9times the CX
for multidepth. Native IQAE retains upstream adaptive stopping and beta intervals;
the repeated-look implementation guarantee is not newly proved here. The
residual native runs finish at k=0, so their improvement is not AE amplification.

The source-faithful csAE ladder uses shots[68,67,66,65,64],330shots,
650Q,1630Aeq,718source-query units and49480projected logical CX. It returns point
estimates, **no confidence intervals**. Ideal raw/residual mean absolute errors
are0.144987/0.012843. Matched-noise errors are0.148443/0.021892; ignoring noise
gives0.154073/0.095440. These descriptive errors are not tolerance certificates.

Classical IID finite-path sampling at3200evaluations has raw/residual mean
absolute errors0.290609/0.021448. The known control helps the classical estimator
too. Direct summation computes this entire16-path finite target exactly and is
already needed to construct the table oracle. A quantum end-to-end advantage
over this baseline is unsupported. Week11 continuous MC/control/PCA-RQMC/
conditional baselines remain important prior evidence, but are not relabeled
same-target week14 comparisons. Continuous admission is required before that
application-level comparison can be made honestly.

## Noise, transfer, allocation and denominators

For residual depth-limited inversion at eta=.02, matched-model delivery is16/16.
Ignoring eta on the **same counts** gives12empty confidence sets,15/16
unconditional hull misses and4/16declarations. None of those four declarations
has midpoint error above$1. Empty sets count as misses and abstentions, not
successful missing observations. Hull containment is weaker than containment
in every component of a disconnected confidence set.

All five unchanged week12 policy arms were run for stationary readout, unguarded
.03transfer and guarded .03transfer. The guard changes planning and inversion:
this is a policy-level ablation, not an identical fixed-plan count comparison.
Under guarded transfer all raw arms abstain, while all residual arms deliver
16/16. Residual unequal_target costs8192total shots,6144Aeq,98304CX; raw
unequal_target spends65536total shots,49152Aeq,786432CX and delivers0/16.
Calibration/pilot shots are charged. Unequal allocation is not claimed to beat
the fixed target arm: their delivery and total costs tie in this small case.

Unguarded residual transfer has4/16,2/16and1/16hull misses for fixed_cp,
pilot_cp and unequal_full respectively; these are outside the guarded model.
Several in-model direct cells have1/16misses; they are retained. Across all
confidence outputs no erroneous$1declaration was observed. That is not zero
risk: the pointwise CP95upper limit for0/16is.205907 and for0/8is.369417.
The full analysis reports unconditional and conditional-on-declaration rates;
the latter is undefined with zero declarations. An unconditional coverage
guarantee does not imply a5% conditional error rate among selected declarations.
There is no multiple-comparison-adjusted significance or confirmation claim.

## Runtime and amortization audit

Observed task time totals: setup.016974s;20response tasks9.376787s;
18fixed tasks1.141248s;30policy tasks5.502266s;16IQAE tasks3.264725s;
6csAE tasks.045748s;2classical tasks.330770s. They include Python/checkpoint work
and are not a fair device speed ranking. The archive separately records setup,
native preparation, transpilation and sampler timing. Fitting/inversion costs
are included in their enclosing task times, not isolated microbenchmarks.
Calibration basis states have zero modeled CX, not zero time. Synthetic
shot-weighted gate inventories are projected acquisition resources, not gates
actually executed on a quantum device. Hardware time is unknown.

For M uses of an unchanged compiled oracle, account as setup+M*per-use cost;
do not silently drop payoff enumeration, compilation or shared control setup.
This study measures one tiny setup and does not estimate a deployment crossover.
The payoff table still scales exponentially with precision/dimension. No
fault-tolerant clock, synthesis-error or physical-qubit advantage is estimated.

See [claims and gate](WEEK_14_CLAIMS_GATE.md), [review](WEEK_14_REVIEW.md),
[closeout](WEEK_14_CLOSEOUT.md) and [frozen protocol](PROTOCOL_W14_FINITE_V1.md).
