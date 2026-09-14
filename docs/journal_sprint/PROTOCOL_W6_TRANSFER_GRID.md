# Week 6 v1: fixed calibration/transfer grid

Local declaration before observations; not independently timestamped registration.
Discovery selected from week 5, not held-out confirmation.

Matrix: all C6, n=6, scale=.125, tolerance=$1; reference A budget 294912;
direct, A-matched and CX-capped unchanged from the checked week-5 ledger.
Calibration shots per state: 4096 and 16384. Independent design-specific
calibration and validation streams, 100 fixed repetitions per cell.
Calibration f=.02,g=.07; validation df in [-.02,0,.03], dg in [-.03,0,.03].
Guard is .03 per rate, alpha_cal=.025 and alpha_validation=.025 throughout.
Nine grid points are not a guarantee over the continuous rectangle.
Total: 32400 attempts; bound-refused contracts acquire no observations.

All bound/refusal/design decisions precede diagnostic target access. Save these
decisions before sampling. Hash protocol and Python dependencies in planned
configuration, snapshot before sampling, preserve incomplete runs on failure.
Separate calibration charges: 8192 or 32768 shots per acquired trial; never
amortize them. Pricing schedules/gate counts do not change with calibration size.

Week-5 archive elapsed about 7.1 seconds with 5.78 MB records for 7200 attempts.
Linear planning estimate: about 32 seconds and 26 MB records (not a guarantee).
Limits checked between 100-repetition cells: 900 seconds elapsed, 250 MB records;
require 1 GB free disk before launch. A limit failure is incomplete execution,
not scientific early stopping; preserve partial records and never report as complete.

Report every cell's delivery, containment, false declarations with all three
denominators (attempts/acquisitions/declarations), unresolved/incompatible counts,
nonempty median radii, full interval components, and separate cost axes.
Predefined descriptive contrasts: high minus low calibration delivery within
each contract/rate/design; multidepth minus direct within contract/rate/calibration.
Report delivery range over all nine rate points, not just the best point.
No simultaneous, conditional-on-delivery or zero-risk guarantee from frequencies.
No claim that synthetic drift generally helps, or that non-delivery establishes
a universal precision floor. Further ablations require separate declaration.
