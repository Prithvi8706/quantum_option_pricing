# Matched arithmetic comparator: target, accounting and limits

The [bounded protocol](MATCHED_ARITHMETIC_PROTOCOL_20260917.md) compares concrete
implementations, not the best possible reversible arithmetic or a reproduction
of an external author's full solver. The Fourier-arithmetic preprint motivates
an aggregation replacement; we implement that replacement within our existing
GBM pricing task. No financial model or contract is changed.

## Targets and numerical bridge

For Gaussian input word x, the arithmetic route computes integer log words
L_i(x), then integer prices s_i(x) by fixed-point Horner evaluation. Every
multiply rounds downward after shifting by f bits. Coefficients, input error,
Taylor remainder and all Horner rounding are covered by the existing directed
exponential budget. The integer payoff is

`P(x) = max(sum_i s_i(x) - d*K*2^f, 0)`.

With an r-bit uniform selector u and flag `[u < P(x)]`,

`p_good = E[P]/2^r`, and `V_arithmetic = lambda*p_good`,
where `lambda = exp(-rate*T)*2^r/(d*2^f)`.

This avoids assuming a free payoff rotation. The selector, comparator, all
workspace and uncomputation are charged. It is exact for the integer payoff,
not the real exponential payoff. Both arithmetic alternatives share the same
integer target; reflection uses a different approximation to the **same
financial target**, connected by its own numerical error budget.

Aggregation is modulo 2^w. Separate universal bounds establish that interpreting
the actual sum and post-strike difference as signed words does not wrap. Even
if a polynomial approximation can be negative, two's-complement modular
addition remains algebraically correct. The post-strike bound explicitly
accounts for both signs, not just separate sum and strike magnitudes. The
selector bound guarantees no positive payoff bits are discarded.

Small finite-grid prices are exhaustive binary64 diagnostics. They are not
continuous prices or confidence intervals. Large conversion components are
actual emitted reversible permutations checked at fixed endpoint inputs.
No large statevector is claimed. Small phase-sensitive tests, exact reversible
gate identities and universal analytic bounds provide complementary evidence;
endpoint tests alone are not an exhaustive correctness proof.

## Aggregation and cleanup

The conventional route uses a linear-size Cuccaro-style modular adder with
one clean helper. Since the accumulator starts at zero, copy the first price
word, then add the others, omitting unused highest-carry computation.

The Fourier route starts its zero accumulator with Hadamards, applies the
controlled phases for the sum, then an inverse QFT with swaps. It uses no
aggregation helper but has quadratic phase growth in word width. Uncomputation
uses the actual shortened circuit's inverse. The logical CP-angle rounding
bridge includes the inverse QFT and is charged twice per compute/uncompute
cycle. This is not a certificate for rounded transpiler-native parameters.

For conversion E, aggregation G, strike/positive-part T and already-clean
threshold comparator C, the A circuit pays

`C_A = C_loader + 2*C_E + 2*C_G + 2*C_T + C_C`.

Selector Hadamards and global-phase control allowances also enter the U ledger.
Horner intermediate registers remain allocated; there is no hypothetical
workspace recycling hidden in the qubit count. This is deliberately not a
space-optimal or range-reduced exponential implementation. Both arithmetic
routes share these costs, so their difference isolates aggregation.

## Two explicitly distinguished logical ledgers

The primary ledger retains the earlier reflection study's conservative
gate-by-gate control convention. Count CCX as 6 CX and 9 U; an additional
control costs at most `6*C_CX + 2*C_U` CX. For M=2^m and R=17:

`C_total = R * [C_A + (M-1)*(2*C_controlled_A + C_controlled_zero + 1)`
`               + m*(m-1) + 3*floor(m/2)]`.

The +1 charges the controlled good-flag reflection; the final terms include
inverse-QFT controlled phases and swaps. All allocated A wires participate in
the zero reflection, with its clean ancillas counted separately.

The secondary ledger applies the standard identity
`C(A S0 A-dagger) = A C(S0) A-dagger` to **every** route. This replaces
`2*C_controlled_A` by `2*C_A`. It is a conventional control-cancellation
optimization, not a newly discovered quantum primitive. Tests compare complete
complex operators, including relative phases and a nonzero global phase in A.

The archived reflection counts include their established level-1 component
compilation. Arithmetic X/CX/CCX conversion uses its explicit fixed decomposition;
both aggregation alternatives use the same level-0 compiler settings. Thus the
comparison is of these declared composition models, **not an identically
optimized whole-circuit benchmark**. No claim that the arithmetic baseline is
optimal, or that the projection ratio bounds runtime speedup, follows.

## Error and confidence

Canonical AE uses `pi/M + pi^2/M^2` as a uniform probability-error bound.
The success probability exceeds 0.8. Seventeen independent repetitions and
the median give failure at most `exp(-0.18*17) < 0.05`.
The probability-to-price slope is lambda for arithmetic and 2*beta for
reflection. Exact rational pi bounds schedule M, with upward deterministic
price allowances and a fixed call cap.
The arithmetic decoder is explicitly `2*beta_upper` times the ideal AE
sin-squared label. A checked inequality fits the scale bridge and one binary64
multiplication inside the decoding allowance. This study does not implement
measured AE decoding or certify a library's numerical sin-squared evaluation.

Arithmetic pays the same directed representation allowance as reflection,
plus its own exponential/input error, loader operator error, Fourier angle
bridge and decoder rounding. With delta_L for one marginal loader and delta_G
for one aggregation, a conservative arithmetic contribution is
`2*lambda*d*delta_L + 4*lambda*delta_G`.

Physical noise, fault-tolerant synthesis, T counts and device runtime are
unknown. Classical model setup and the reflection route's degree-four moment
offset are not converted into CX costs; this is a quantum logical-resource
ledger, not a total classical-plus-quantum wall-time ledger. Classical RQMC
remains a separate, necessary comparator before any quantum advantage claim.

## Sources and provenance

- [Cuccaro et al., modular ripple arithmetic](https://arxiv.org/pdf/quant-ph/0410184),
  Section4.1/Table1: established linear-size arithmetic; our emitted variant is
  tested directly and is not claimed to match the paper's optimized gate count.
- [Draper, Fourier addition](https://arxiv.org/pdf/quant-ph/0008033): established
  Fourier-phase addition, not new here.
- [Kim, Cui, Lee and Park, author-uploaded July2026 preprint](https://www.researchgate.net/publication/408635511_Scalable_Quantum_Derivative_Pricing_through_Fourier-Arithmetic_Payoff-Oracle_Design),
  Theorem1 and Proposition2/Corollary3: aggregation and payoff preservation.
  Its aggregation-only benchmark does not supply our full pricing costs.
- [Brassard et al.](https://arxiv.org/pdf/quant-ph/0005055), equation1 and
  Theorem12: amplitude amplification/estimation and its probability bound.

Acquisition archives record source, protocol and prior-input hashes; replay
uses the isolated pinned environment. Separate AI review is not independent
human novelty assessment, authorship contribution or external peer review.
