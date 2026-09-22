# Separate predeclared bounded confidence run

Frozen after the empirical diagnostic, before this run. Date 2026-09-22. This is a development diagnostic with a different seed, not held-out confirmation.

Use the identical capped, discounted 256-step weak-Euler Asian contract in heston_pilot_protocol.md, with no control variate. Independently draw sign vectors with NumPy PCG64 seed22094026 and average each payoff with its sign-reversed antithetic payoff. The pair means are iid in [0,R], R=200 exp(-.03), under the ideal random-bits model. For epsilon=$.25, delta=.05, fix M=ceil(R^2 log(2/delta)/(2 epsilon^2)) pairs. Hoeffding then gives P(abs(samplemean-true capped finite-model mean)>epsilon)<=delta under iid sampling and exact evaluation. Pseudorandom generation and floating-point numerical implementation are stated assumptions; this does not certify uncapped or continuous-Heston pricing, and is not a bitwise equivalence proof for the published fixed-point circuit.

Stream batches of8192 pairs, including generation in timing. Stop after120s if incomplete; report actual samples without attaching the fixed-M guarantee to an incomplete run. Record exact M, elapsed time, mean, cap exceedances, maximum observed raw payoff and negative variance events. The cap is part of the output contract, never inferred from the observed maximum. No tuning or early stopping based on prices.
