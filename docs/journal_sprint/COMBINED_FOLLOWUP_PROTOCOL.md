# Adaptive development follow-up: normalize after control subtraction

2026-09-17. The first combined acquisition completed: all180controlled-LCU
screens had higher Hadamard price variance than raw LCU. The integrated16path
test was correct but beta increased1.937times. This follow-up is explicitly
selected after seeing those results, not a preregistered confirmation.

Retain the original256path finite development target, strikes90..110. Construct
the degree4 even Chebyshev control for abs(x); combine with the exactly tractable
linear call term. For high degrees8/16/32, synthesize the residual polynomial
P_high-P_4 directly, normalized by1.001times its coefficient L1 sum rho (synthesis
slack below unit magnitude). This implements
subtraction before QSP normalization, unlike the previous signed-LCU assembly.
Compare against the stronger raw-QSP baseline that ALSO treats the linear term
analytically. Both approximate the same P_high payoff, so systematic bias matches.
Compare actual Hadamard circuits at strike100, with inverse/signal tables paid.

Compute control expectations without the full joint path table by expanding
moments of the arithmetic basket: sum multinomial compositions of degree<=4,
then factor each lognormal moment across independent encoded normal coordinates.
This costs a combinatorial number of terms in degree/dimension and q-dimensional
marginal sums, not a magically free input oracle. The moments are strike-independent
and can be reused. Full finite enumeration is used only to verify the moment
identity; all classical comparators get those same moments/controls.

Classical same-representation comparison: exact finite variance of raw payoff,
true payoff minus polynomial control, and approximation minus polynomial control.
The QSP Hadamard variance is beta^2 minus squared residual expectation. Report
its reduction versus raw QSP at identical polynomial bias, NOT a quantum/classical
speedup or universal bound. Feature selection in this follow-up is analytical,
not quantum-trained. The Fourier-discovery module remains an evaluated/rejected
branch; do not claim all ingredients are beneficial simultaneously.

Use three fixed phase seeds and1500nfev cap per degree/polynomial as before.
Retain every attempt. No uniform phase certificate, scalable basket signal,
MPS circuit, hardware latency or continuous-target admission is supplied.
Same reuse counts1/5/25/100 apply to both sides. Generic QSP/control-variate
composition is not claimed novel without a dedicated prior-work comparison.
