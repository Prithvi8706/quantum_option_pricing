# Week 9 v1: deterministic high-precision inverse cross-check

Declared before diagnostic execution. This is numerical validation of a finite
input matrix, not a stochastic coverage trial or formal interval-arithmetic proof.
No option-price observations, new representations or adapted schedules are selected.

## Question and independent reference

Does the floating-point finite-calibration inverse enclose a separately computed
high-precision reference set for fixed small-count, boundary and conflict cases?
Reference uses mpmath at 80 decimal digits, not SciPy Beta quantiles or production
trigonometric preimage/intersection helpers. Invert regularized incomplete beta
by 160 bisections. Independently invert the response polynomials in amplitude
coordinates on monotonic branches, using 160 bisections per root. The production
method instead constructs trigonometric branches in theta coordinates.

For k=0/1/2 the polynomials are respectively a;
9a-24a^2+16a^3; and 25a-200a^2+560a^3-640a^4+256a^5.
Branch endpoints are sin^2(j*pi/(2*(2k+1))) for j=0,...,2k+1.
Apply the same intended conservative per-depth readout rectangle, including the
full-set fallback when positive contrast is uncertified, but without the production
2e-14 padding. Reference bracketing is evaluated at high precision, not directed
rounding: do not call it certified exact arithmetic.

## Fixed matrix

Schedules [0] and [0,1,2]. Validation shots 128 at every depth. Calibration
shots 64 per state and error pairs (0,0),(1,4),(5,1),(32,32). Guards 0,.01,.03.
Alpha_cal=.025, alpha_validation=.025. Counts are deterministic rounded response
values under f=.02,g=.07 for amplitudes .001,.01,.1,.17,.3,.5,.7,.9,.999, plus
all-zero, all-128, alternating-zero/128 and alternating-128/zero count vectors.
13 count cases x 4 calibration pairs x 3 guards x 2 schedules = **312 cases**.
Some schedule-[0] edge vectors coincide; retain distinct declared case identities,
do not pretend they are independent random trials.

Check every reference component against the production union with no additional
comparison tolerance; record missing endpoints/components, empty/full cases,
component counts and maximum endpoint enclosure slack. A failure is retained and
investigated, not removed or corrected by changing the matrix after results.
Finite agreement does not prove universal enclosure, pricing-bound correctness,
production-scale beta-tail accuracy, realistic noise validity or coverage.

## Evidence and safeguards

Freeze protocol/dependency hashes and source snapshot before evaluation. Record
mpmath/Python/NumPy/SciPy versions. Cache deterministic beta quantiles only within
the fixed precision. Check a 900-second limit before and after each case; preserve
partial records/failure marker and do not write completion on failure.
Expected records below 10 MB; require 1 GB free disk and enforce 100 MB record limit.
Initial runtime estimate below five minutes, not a guarantee. Use exclusive run
directories. Any verification repeat uses identical cases, not new independent data.
