# Reversible arithmetic development protocol (2026-09-17)

This is development, not confirmation or a new novelty claim. Frozen historical
producers are unchanged. Original case 3, two assets/two dates, raw arithmetic
Asian call: L=4, ten bits per normal, 24 fractional bits, 40-bit signed words,
degree-32 Taylor coefficients. These parameters were selected in development
after scalar arithmetic checks; there is no held-out performance inference.

## Construction and proof obligations

Little-endian two's-complement words; add modulo 2^w using the known Cuccaro
ripple-carry construction. Signed multiplication sign-extends read controls to
2w bits, adds controlled partial products, copies bits f..f+w-1 and uncomputes.
This implements floor(x*y/2^f), including negative operands. Registers must be
disjoint; temporary words start zero. Overflow is not prevented by modular
gates: the separate interval plan must prove interpretability.

Encode each midpoint Gaussian log as an intercept plus one integer constant
per input bit. Constants are floors of outward-enclosed coefficients times
2^f. Sum their individual error bounds. This avoids a table over paths.
For each relative log x, compute S0 exp(x) by fixed-point Horner coefficients
floor(S0*2^f/k!). Remove exact trailing zero coefficients without changing the
integer polynomial. Uncompute stored Horner stages after copying the result.

Let h bound the exact log, delta its encoding error, H=h+delta, u=2^-f.
The Taylor remainder is S0 exp(H) H^(N+1)/(N+1)!. Input perturbation costs
S0 exp(H)*delta. Horner error propagates as H*e + actual coefficient error
+ u per floor, except a provably zero intermediate has exact zero product.
Magnitude bounds propagate using absolute values and the same floor allowance.
The plan checks the log-map prefix, Horner intermediates, spot sum and strike
against the signed range; a false overflow flag is not an admitted design.

Subtract d*K*2^f from the sum of approximated spots, clamp at zero, and compare
the result y with a uniform M-bit selector u. M is selected from an outward
upper bound, ensuring y<2^M. Exactly y of the 2^M selectors satisfy u<y.
Therefore flag probability is E[y]/2^M, and price scale is
exp(-rT)*2^(M-f)/d. There is no payoff-angle approximation in this ideal logical
construction. Nonnegative clamping and max(call,0) are 1-Lipschitz, so the
uniform scalar spot error propagates to discount times that error in price.
All payoff work is uncomputed after flagging. A residual/geometric-control
kernel is NOT implemented by this raw-only protocol.

The Gaussian loader has 2^q-1 controlled RY nodes per independent normal,
not 2^(dq) payoff entries. Conditional node probabilities are enclosed from
normal CDF differences. Binary float angles are candidates only: a 64-term
directed sin/cos series on [0,2], with first-omitted-term remainder, bounds the
distance to each ideal node's first column. This equals the RY block operator
distance. Triangle/telescoping bounds sum node errors, then dimensions; pure
state trace distance is at most state-vector distance. Multiplication by the
actual payoff scale bounds the preparation-induced dollar error. This models
exact controlled-RY gates at stored angles, not synthesized/noisy hardware.
Inverse gates are exact adjoints in this model. Gate errors accumulated during
physical Grover execution require a separate implementation/noise model.

## Evidence and limits

The audit records source/input hashes, selected plan, loader angles, prior
encoding bounds, prospective composed bias, actual emitted payoff gates and
two full-workspace basis checks. Counts are logical X/CX/CCX, not hardware CX,
T counts, full A or complete Grover cost. Small exhaustive arithmetic tests and
a real comparator statevector/nonzero-Grover test complement, but do not turn
two large basis checks into exhaustive or large quantum execution evidence.
No timing win is claimed. No source snapshots or replay guarantee are implied
by hashes alone; archive checks must verify those hashes against available files.

Remaining gates: integrated scientific/code review, full implementation-cost
composition (including loading/reflections), same-target strong classical
comparison, useful contribution assessment, fixed statistical protocol and
actual collaborator/statistical sign-off. This audit never generates holdout
seeds, clears PriceContract unknowns, or declares confirmation unblocked.

Arithmetic references: [Cuccaro et al.](https://arxiv.org/abs/quant-ph/0410184),
[amplitude amplification/estimation](https://arxiv.org/abs/quant-ph/0005055).
The construction assembles standard arithmetic and indicator encoding; novelty
must concern a demonstrated distinct contribution, not these components alone.
