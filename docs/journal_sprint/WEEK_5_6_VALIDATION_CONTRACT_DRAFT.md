# Week 5–6 fixed-validation and resource-selection contract

Draft informed by week-4 discovery, not a frozen confirmation protocol.
No held-out contracts or new pilot/validation observations are generated here.

## Scientific scope decision

Retain **model-conditional, readout-only scope** for the current method.
The formal argument assumes valid deterministic pricing bounds, independent
binomial observations, and calibration intervals plus independently justified
transfer allowances that enclose each validation depth's readout rates.
Finite calibration alone cannot validate drift bounds. A goodness-of-fit
pass, a fitted noise curve, or absence of incompatibility cannot establish them.
Gate noise, correlated shots, arbitrary preparation errors and hardware
generalization remain excluded unless separately justified.

Primary report: interval containment, delivered tolerance, unconditional
erroneous-declaration frequency and full cost. Report conditional error among
declarations with its actual denominator; never label it bounded by .05 from
the current union-bound argument. Interval noncontainment and midpoint error
above tolerance are different events and must both remain visible.

## Immutable design record required before a validation batch

Record contract ID/parameters; candidate-menu version; chosen n/scale/support;
deterministic bound components; price sensitivity/offset; dollar tolerance;
calibration preparation assumptions; transfer allowances and justification;
calibration/validation confidence allocations; calibration shots; fixed depths
and shot counts; seed namespaces; implementation/environment hashes; numerical
scope; cost units; refusal conditions and failure handling.

Keep exact price/amplitude answers in a separate diagnostic record. They cannot
enter candidate ranking, transfer-bound choice, shot allocation or stopping.
The deterministic decision interface takes only contract parameters, analytical
bounds, resource records, declared assumptions and independent pilot data.

## Acquisition and decision order

1. Compute candidate bounds/resources; refuse before quantum acquisition when
   no sufficient deterministic allowance remains. Count classical setup time.
2. If using a pilot, allocate its cost explicitly and finalize exactly one design.
   Pilot information may select the design, but its counts are not recycled as
   fresh fixed-design validation observations.
3. Acquire the declared calibration and one fixed validation batch. Conditional
   independence and confidence spending must match the actual design. The
   week-4 calibration/validation split is .025/.025; any changed allocation
   needs a new prospective design, not retrospective selection from outcomes.
4. Expand calibration intervals only by predeclared justified transfer bounds.
   If contrast is uncertified, preserve the full-set/unresolved outcome.
   Invert all branches; empty sets are incompatibility, not an automatic retry.
5. Expand the amplitude hull by the unchanged deterministic dollar bound;
   do not clip price endpoints. Deliver only if the resulting radius <= tolerance.
6. Record every attempt, refusal, cost, incompatible/unresolved result and
   declaration. Repeated validation needs a valid sequential design or explicit
   error spending first; rerunning until a useful result appears is forbidden.

## Discovery work required before freezing confirmation

- Measure the remaining compiled profiles for each proposed schedule. Existing
  n=5/6 profiles cover k=0/1; week-4 synthetic k=2 observations do not establish
  its compiled gate count or physical runtime.
- Compare strong fixed choices at matched costs, with all calibration/pilot
  acquisition counted. Record pricing A-equivalents and simple calibration
  preparations separately; inference arms sharing data do not duplicate cost.
- Establish comparator adapters' interval/stopping semantics, complete upstream
  randomness control where reproducibility is claimed, and matched targets.
  BAE/BIQAE single-target smokes are not head-to-head performance evidence.
- Assess whether calibration/transfer uncertainty prevents useful dollar
  precision even at larger shot budgets before optimizing a controller.
- Freeze the utility rule, budget matrix, primary contrasts and minimum useful
  effect before generating the prospective unseen confirmation population.
- Make a go/no-go decision after fixed-baseline results. If allocation does
  not improve useful delivery/cost, retain a narrower limitation/reliability
  paper only if its contribution is substantive; no adaptive win is presumed.

Confirmation remains on hold. This draft neither authorizes paid compute nor
changes the outstanding Macroscope/PR requirement or contributor approvals.
