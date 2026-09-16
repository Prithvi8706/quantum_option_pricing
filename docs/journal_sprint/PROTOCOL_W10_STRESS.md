# Week 10 bounded numerical stress protocol

Locally declared 2026-09-15 before execution. No random pricing acquisitions.
Historical week-9 code and results are not changed.

Matrix: schedules [1], [2], [1,2], [0,1,2]; validation shots
128, 30000, 100000; calibration shots 64 with errors [0,0]; guards
0 and .01. For each combination use all-zero, all-success and alternating
zero/success observations: 72 cases, retaining duplicate vectors under single
depth schedules. Add 8 cases at 128 shots: each schedule, all counts 64 and
all counts 127, guard zero. Total 80. These are deterministic diagnostics,
not independent coverage trials. Boundary observations exercise branch extrema;
single higher-depth schedules and their intersection exercise disconnected sets.

Reference: existing independent explicit polynomials at depths 0,1,2,
160 bisections; small-count beta inversion from week 9. Large-count tails
use exact binomial boundary identities: zero-success upper endpoint
-expm1(log(alpha/2)/N); all-success lower endpoint exp(log(alpha/2)/N).
No general large-count interior beta-tail accuracy is claimed. Validate these
identities against small-count beta inversion before the matrix. Repeat the
matrix at 100 decimal digits after 80 digits; require identical topology and
endpoint differences below 1e-40. This is stability, not directed rounding.

Production must enclose each whole reference component with no comparison
tolerance. Require at least one disconnected final reference intersection for
schedule [1,2], not just disconnected single-depth preimages. Preserve every
failure and exception. Exclusive output directory, snapshot source and protocol,
flush each record; 900-second elapsed check between cases. This is not a hard
per-operation timeout; only bounded small-count beta calls are used. Completion
marker means execution finished, not that every numerical assertion passed.

Verification: replay from unchanged source, check snapshot/output hashes,
case identity/count, all enclosure flags, precision stability and required
topology. A failure blocks a numerical pass and requires documented follow-up.
