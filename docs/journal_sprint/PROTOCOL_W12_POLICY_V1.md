# Week-12 policy specification v1: pre-acquisition foundation

2026-09-16. Supplements [the development manifest](WEEK_12_DESIGN_MANIFEST.md).
No runtime pilot or main development observations have been acquired under this
specification. A runner with source/input snapshots and accounting must pass its
own tests before acquisition. This is not a confirmation protocol.

## Frozen planning choices

Keep the manifest's five arms, C6 profiles, $1 tolerance, total cap, count menus,
scenarios, guards, sample sizes and interest thresholds. Preselect encoding with
the existing shot-axis proxy before any pilot. Reject/refuse unknown or exhausted
bias before sampling; preserve that outcome and its zero consumed shots.

The old fixed CP and equal-pilot arms retain their historical allocations and
equal-pilot CP forecast. The three new arms use the following delta-method proxy,
not a predicted finite-sample delivery probability or certificate:

`R = B + S/c * (z * sqrt(q*(1-q)/n + (1-a)^2*f*(1-f)/m0 + a^2*g*(1-g)/m1) + guard)`.

Design f=.02, g=.07, c=1-f-g, a=clip((q-f)/c,0,1), z=2.241402727604947.
These rates stay fixed even for the swapped evaluator scenario. Paid new arms
use q=(pilot_successes+.5)/1025; this smoothing avoids exactly zero variance from
an extreme pilot. Fixed-target uses the prior design assumption a=.5 (q=.475),
not evaluator amplitude. Pilot uncertainty and nonlinear CP geometry are not
certified by this heuristic. The transfer term is first-order planning only.

For each m0,m1 in {256,1024,4096,8192,16384,24576}, set n=cap-pilot-m0-m1;
discard n<256. Unequal-full uses cap=65536. Target arms use caps
{8192,16384,32768,65536}; pilot cost is 1024 for paid arms and zero otherwise.
All three share design rates, feasible calibration menu, forecast and tie rules.

Target arms select least total shots among R<=.9*tolerance, then smallest R,
then lexicographic (m0,m1,n). The .9 margin is an engineering choice fixed before
observations, not a guaranteed delivery probability. If none qualifies, execute
the minimum-R candidate, ties by total shots then (m0,m1,n); do not invent a
certificate or erase the failed forecast. Unequal-full always minimizes R with
the same tie ordering. Record whether the forecast margin was met separately
from actual terminal delivery. No tuning on the runtime pilot's delivery results.

The old equal-pilot arm retains its unsmoothed rounded-count CP forecast; its
allocation mechanism is unchanged. A common delta proxy may additionally be
logged for diagnostics but must not be mislabeled as that arm's selection score.

## Conditional containment argument

Let H contain predeclared metadata and paid pilot observations. Encoding selection
precedes the pilot. Conditional on H, chosen m0,m1,n are fixed and positive;
terminal calibration errors and pricing successes are fresh binomial batches.
The pilot is excluded from terminal inference. The runner must enforce this
separation; a function signature alone cannot prove it.

Use CP calibration coordinate error probabilities .0125 each and pricing .025.
For every H and every valid fixed parameter, their joint coverage is at least
1-.0125-.0125-.025=.95 by the union bound. Independence between the three
interval events is unnecessary for this bound, but each conditional binomial
sampling assumption is necessary. Integrating over H retains unconditional .95
coverage, regardless of whether the design forecast was accurate.

On this event, supplied valid transfer bounds enclose validation f,g. For positive
contrast and q=f+(1-f-g)*a, the lower amplitude corner is
`(q_lower-f_upper)/(1-f_upper-g_lower)` and the upper corner is
`(q_upper-f_lower)/(1-f_lower-g_upper)`, clipped to [0,1]. If positive contrast is
not certified, retain [0,1]. An incompatible intersection yields no declaration.
Mapping with `|P-(O+S*a)|<=B` gives a containing dollar interval. A declaration
with radius <= tolerance then has unconditional erroneous-declaration risk <=.05
under these assumptions, not .05 conditional on declaring or simultaneous over
the experiment. Bias/composition/transfer bounds must actually be justified.

This is the exact-arithmetic argument for established CP/union-bound inversion,
not a new theorem of quantum advantage. Existing floating-point padding and
numerical tests are engineering safeguards, not directed-rounding proof.
Unknown systematic bounds, drift outside the guard, correlated shots, pooling
pilot counts or optional stopping invalidate the claimed interpretation.

## Acquisition gate

Before the 90-row runtime pilot: test independent unequal-count endpoints,
historical-arm equivalence, unknown bias, extreme pilots, incompatibility,
budget accounting, source identity, stream separation, durable failed attempts
and deterministic replay. Freeze the acquisition implementation and source hashes.
Then apply the manifest's runtime projection gate before the 7400-row main study.
Do not mark week 12 complete from policy-unit tests alone.
