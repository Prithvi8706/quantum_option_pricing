# Week 7 v1: pricing, calibration and stipulated-guard ablation

Local prospective declaration before observations; selected from prior discovery,
not independently timestamped preregistration or held-out confirmation.

## Acquisition matrix

All C6, fixed n=6/scale=.125, tolerance=$1; unchanged sufficient bound refusals.
Reference pricing A budgets 294912 and 1179648 (1x/4x). Fixed designs direct,
A-matched k=(0,1,2), CX-capped k=(0,1,2) using existing compiled profiles and
integer allocation rules. Calibration shots per state 4096/16384. 100 independent
repetitions per contract/budget/calibration/condition/design acquisition cell.
Calibration f=.02,g=.07. Actual validation conditions:

- stationary: f=.02,g=.07;
- small_transfer: f=.03,g=.06 (stipulated shifts +.01,-.01);
- boundary_transfer: f=.05,g=.04 (stipulated shifts +.03,-.03).

6 x 2 x 2 x 3 x 3 x 100 = **21600 acquisition attempts**. Refused attempts
acquire neither pricing nor calibration counts. Bounds/refusals/allocation and
cost ledgers are saved before diagnostic truth access. Diagnostic answers feed
only the synthetic sampling model and later outcome evaluation, never allocation.
Independent calibration and validation namespaces include every acquisition key.

## Inference arms and validity

Guard widths 0, .01, .03 per rate. Only analyze guards that cover the declared
condition: stationary has 3 arms, small_transfer 2, boundary_transfer 1. Never
apply a narrower false guard and call it calibrated. All arms use exactly the
same acquired counts/calibration within an acquisition. They are paired inference
contrasts, not additional acquisitions. Each arm uses alpha_cal=.025 and
alpha_validation=.025; no simultaneous-over-arms claim is made. The rectangle
can differ by depth in reality; these allowances are stipulated, not estimated.

Expected **43200 attempted arm analyses**, including refusals. Retain per-arm
interval components, median radii with nonempty denominator, containment,
delivery, incompatible/unresolved states, erroneous declarations per attempt,
acquisition and among declarations. No oracle-known-readout arm is used.

## Contrasts and costs

Pricing 4x-minus-1x and calibration 4x-minus-1x: within contract, other fixed
axes, design and valid guard. Separate acquisitions => unpaired descriptive
frequency differences. Guard wider-minus-narrower on the same observations:
paired descriptive differences at fixed actual condition; verify wider sets
enclose narrower sets. Do not conflate changing actual drift with guard width.
Report multidepth-minus-direct within every matched set of other axes.
Undefined rates stay null. Keep all cells, not only favorable contrasts.

Charge pricing shots/A-equivalents/CX/U/depth and calibration shots once in
acquisition totals, not once per inference arm. Larger calibration costs 24576
extra shots per acquired trial. Setup timing and synthetic runtime are separate
from gate counts. No runtime, native-estimator or classical speedup claim.

## Predeclared exploratory readiness screen

Evaluate each fixed (pricing budget, calibration size) CX-capped candidate under
guard .03: require >=90/100 declarations in **every** condition of **each** of
the four currently bound-feasible contracts, and >=10 percentage-point delivery
gain versus direct in each such cell. All C6 still enter attempt accounting.
Any erroneous declaration must be investigated, not discarded or retried.
This is an engineering screen for further independent validation, not a test of
population reliability/significance or a quantum-advantage criterion. Native
comparator fairness and numerical/transfer assumptions remain additional gates.
Do not build/promote an adaptive selector if this screen fails. A pass would
only justify a separately declared fresh validation design, never confirmation
on these same observations. No optional stopping or choosing a winning guard.

## Execution safeguards

Prior 32400-attempt/21600-inference week-6 run took 29.43 s. Planning estimate
for this multi-arm pilot is under two minutes and under 150 MB records, not a
guarantee. Require 1 GB free; check 900-second and 500-MB record limits between
100-attempt cells. Save partial failure state without completion on failure.
Record source/protocol/upstream hashes before sampling and preserve snapshots.
Use exclusive output directories; no hardware, paid service or submission.
