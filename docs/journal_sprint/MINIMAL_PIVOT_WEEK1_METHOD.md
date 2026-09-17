# Study W1: shared-reflection centered basket encoding

## Fixed target and proposition

Keep the arithmetic Asian basket A(z)=d^-1 sum_i exp(mu_i+F_i z),
payoff max(A-K,0), K>=0, and the existing finite coordinate grid in [-L,L].
Model inputs and grid nodes are exact stored binary numbers for this statement;
the continuous-financial-model bridge is a separate obligation.

Define c_i=exp(mu_i+L sum_j |F_ij|)/d and
a_ij(z_j)=exp(F_ij z_j-L|F_ij|). Then 0<a_ij<=1 and
A=sum_i c_i prod_j a_ij. Let C=sum_i c_i and h=C/2-K.

For fixed row i and path z, let V_i be the tensor product of RY rotations
whose zero amplitude is sqrt(a_ij). With R=2|0^d><0^d|-I,

    <0^d| V_i^dagger R V_i |0^d> = 2 prod_j a_ij - 1.

LCU coefficients c_i/2 for these row reflections, plus signed constant h,
give the numerator A-K. Their absolute sum is

    B_ref = C/2 + |C/2-K| = max(K,C-K).

Preparing coefficient amplitudes sqrt(|w_i|/B_ref), applying SELECT and
unpreparing therefore block-encodes (A-K)/B_ref. SELECT is a Hermitian
involution in exact arithmetic. Constant and unused index slots use identity
preparations; the zero signal state is a +1 eigenstate of R. Apply a minus
index phase for a negative constant. Garbage-space action need not equal
the earlier implementation: the projected block is the contract.

Implement SELECT by a single row-indexed V, one shared R, and V inverse.
For each coordinate, combine the row index and local coordinate bits into
one multiplexer. Do not construct a separate controlled reflection per row.

There are d+1 coefficient slots, d*q path qubits, d signal ancillas and
ceil(log2(d+1)) index qubits. The marginal input count is d^2*2^q; the padded
multiplexer count is d*2^(q+ceil(log2(d+1))). This removes subset enumeration,
not the exponential dependence on coordinate precision q or growth in C.
It is not a poly(log d) algorithm. B_ref is not asserted optimal on the actual
basket support or universally smaller than every alternative centered scale.

## Logical operator-error certificate

All real coefficients, conditional PREP probabilities and marginal exponential
values are enclosed with directed decimal intervals. Floating angles are
chosen, then their sine/cosine values are enclosed independently. For an RY
rotation, operator error equals the Euclidean error of its first column.
Disjoint controlled blocks incur the maximum of their individual errors;
sequential layers incur their sum by telescoping unitary products.

The Gray-code multiplexer computes its Walsh coefficients exactly as rational
numbers from the stored binary angles. Each coefficient is rounded once.
The sum of absolute coefficient rounding errors divided by two bounds the
resulting RY-product operator error. This includes the multiplexer synthesis,
not later arbitrary native-gate optimization.

Let delta_P bound all PREP layers and delta_V all coordinate multiplexers.
The reflection signal error is at most 2*delta_P+2*delta_V+delta_pi. The final
term bounds the stored binary global pi against mathematical pi; retain it
when controlling the signal. For the original tensor-reflection control the
bound is 2*delta_P+delta_V. Clifford/Toffoli signs are exact in this model.

This certificate concerns the entire ideal logical signal unitary, not just
the small tested good block. It does NOT certify hardware noise, subsequent
U/CX transpiler rounding, fault-tolerant synthesis, QSP projector phases,
probability loading, amplitude estimation, or the complete dollar error.

The mathematical radius is enclosed in B_interval. The scalar diagnostic
uses outward binary B. W2 must explicitly propagate that normalization
bridge through QSP, alongside signal and projector errors; copying the
signal certificate into the old pricing archive would be invalid.

## Prior art and claim boundary

- Probability-to-reflection conversion and LCU are established primitives;
  see [qubitization](https://arxiv.org/abs/1610.06546) and
  [QSVT](https://arxiv.org/abs/1806.01838). We do not claim their invention.
- [Derivative Pricing using QSP](https://arxiv.org/abs/2307.14310)
  already develops quantum payoff encodings and resource reductions. Merely
  using QSP for a financial payoff is not a new contribution. W1 screened
  its abstract and relevant framing; it is not a fresh full reproduction.
- [Karhunen-Loeve option pricing](https://arxiv.org/html/2402.10132v1)
  already addresses Asian options. Relevant sections 2.3, 3.3, 4-6 were
  inspected, including the inner averaging and outer estimation in equations
  43-45. Our finite-factor signal avoids that particular inner estimation
  construction, but different encodings and error regimes prevent inferring
  a superior end-to-end complexity from this observation.
- [Dicke-state LCU](https://arxiv.org/abs/2507.20887) was screened at abstract
  level. It is another reminder that improved LCU realizations are active
  prior art, not evidence that this finance construction is globally new.

Candidate contribution: an explicit shared-reflection realization for this
separable basket, its logical error certificate, and reproducible comparisons
against equally multiplexed original and subset-centered realizations.
Field-wide novelty remains unestablished. W2 requires a claim-specific
prior-art comparison and independent expert review; this is not an
exhaustive literature novelty clearance or a guarantee of journal acceptance.
