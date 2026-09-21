# V2A: deterministic application feasibility gate

Recorded before inspecting this experiment's outputs. This is discovery, not
held-out confirmation, and does not amend July's frozen experiment.

Use the existing C6 contracts, support q_total=1e-5, n=(3,4,5,6), and payoff
scale c=(.125,.25,.5): 72 configurations. No stochastic or hardware jobs.
Evaluate sufficient deterministic feasibility for $1 and 1% of spot. A failed
bound is unresolved, not proof that actual pricing accuracy is impossible.

Keep the circuit's point-density grid. Bound support error by discounted omitted
payoff plus omitted mass times the maximum in-support payoff. Bound grid error
by discounted half grid spacing plus payoff range times total variation between
normalized point densities and exact conditional nearest-grid-cell masses.
Bound encoding error by exp(-rT)*(U-K)*pi^2*c^2/48. Sum the three absolute bounds.
These are exact-arithmetic mathematical bounds evaluated with ordinary floating
point, not formally verified numerical enclosures.

Compute bound inputs separately from diagnostic exact prices. Diagnostic support,
grid and encoded errors must each obey their bound to tolerance 1e-9 dollars;
the signed error ladder must telescope. Test the affine price map against the
existing implementation. Test actual ideal pricing-circuit objective probabilities
for C6 at n=3,c=.25; no noisy-circuit validity claim follows from that test.

Preserve protocol, relevant source snapshots, all 72 rows, environment metadata,
pass/fail checks and completion hashes in an exclusive new output directory.
Do not widen the matrix after seeing a disappointing outcome within this version.
