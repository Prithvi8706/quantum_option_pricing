# Stronger arithmetic comparator: construction and evidence scope

The [frozen protocol](STRONGER_ARITHMETIC_PROTOCOL_20260921.md) keeps the original
Asian-basket contracts and the full accuracy/confidence budget. This study changes
the concrete arithmetic implementation, rather than its financial target.

## Shared clean scratch

Each conversion keeps its input-dependent log and spot registers. Its affine
and polynomial scratch returns to zero after compute/copy/uncompute. Successive
conversions may therefore use the same scratch wires coherently. Their logs
and spots remain live until payoff evaluation and reverse conversion finish.
There is no measurement or basis-state-specific reset. Both layouts also reuse
one clean carry for aggregation, poststrike evaluation and comparison.

Gate counts are obtained from actual emitted X/CX/CCX programs. A streaming
wire map computes dependency depth for each layout, including all inverse gates.
Reuse can serialize operations and increase depth even while reducing qubits.
The controlled zero-state reflection cost is acquired separately for the actual
allocation. Consequently identical arithmetic gates need not imply identical
whole-AE logical cost when qubit counts change.

## Range reduction

Let Q=2^f, let X be the encoded log, and choose an integer s. The implemented map
uses Y=floor(X/2^s), a Taylor/Horner polynomial with coefficients
floor(Q/k!), repeated squaring z <- floor(z*z/Q), and exact integer multiplication
by the spot price. Negative shifts use floor semantics. The final spot scaling
uses actual reversible shift/add operations; it is not folded into the Taylor
coefficients. Trailing zero coefficients are omitted from emitted Horner stages,
while the original requested degree remains in the error certificate.

The certificate includes input quantization, shift error bounded by
(2^s-1)/(2^s Q), coefficient quantization, every fixed-product floor, and the
Taylor remainder. At a squaring stage with exact magnitude bound B and error e,
the propagated bound is 2 B e + e^2 + 1/Q. Exact integer intervals separately
bound full 2w-bit products, w-bit rescaled words, coefficient additions, spot
shift/add prefixes, partial basket sums, poststrike values and selector range.

The discounted scalar approximation error is added to the original continuous
representation allowance, Gaussian-loading allowance and decoder bridge. The
same rational pi bounds determine the minimum dyadic AE schedule, using 17
repetitions and the original query cap. Missing physical execution errors are
not assigned a zero value.

## Costs and verification

Logical decomposition uses one U for X and six CX/nine U for CCX. The historical
conservative controlled-U/CX ledger and the standard control-cancelled ledger
are both retained, with full inverse-QFT swap accounting. These are component
projections without global circuit optimization, hardware connectivity, native
synthesis, error correction, or runtime conversion.

Small tests compare independently evaluated signed integer maps, arbitrary XOR
outputs, complex amplitudes, clean scratch and inverses. Production conversion
components check the zero/max packed endpoints; these checks supplement the
universal proof and are not exhaustive production simulation. Scalar q1/q2
financial grids provide further diagnostics. No production statevector is built.

The archive verifier independently reconstructs schedules and both CX ledgers,
recomputes every certificate and finite-grid diagnostic, and checks hashes and
commit binding. Its default mode does not re-emit gate lists. Selected or full
gate reconstruction must be explicitly requested and is reported separately.
Independent AI review supplements these checks; human novelty review remains open.
