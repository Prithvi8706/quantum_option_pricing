# V2B: cancellation-aware grid bound

Record before inspecting V2B outcomes. Keep exactly V2A's C6 contracts,
n=(3,4,5,6), c=(.125,.25,.5), support q_total=1e-5, and tolerances $1/1% spot.
No added shots, new representations, stochastic campaign, or hardware jobs.

Replace the h/2 nearest-cell quantization bound by a density-expansion bound:
integrate the payoff difference against the constant density f(x_i) exactly on
each nearest-grid cell, retain their signed sum, and bound the remainder by
sup_cell|f'| times the integral of (s-x_i)^2. Divide by retained mass. Keep the
existing M*TV point-density-versus-cell-mass term, support and encoding bounds.
Take the smaller of the old and new quantization bounds; both are sufficient.

Calculate derivative suprema from endpoints and all analytic f'' roots inside
each cell, not from a numerical sample maximum. Diagnostic exact prices remain
outside the bound routine. This is standard numerical analysis, not a novelty
claim. Ordinary floating-point evaluation is not formal interval arithmetic.

Validate every separate grid and total bound on the unchanged 72 cases. Check
derivative envelopes numerically, explicit kink/endpoint handling, non-increase
against V2A, and end-to-end JSON serialization. Preserve source, protocol, prior
input hashes, rows and completion hashes in an exclusive new directory. Report
negative findings without widening this experiment's parameter matrix.
