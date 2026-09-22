# Source and estimator specification

22 September 2026. This follows the same compound Asian-basket/parity residual
investigation. It does not introduce a new financial workload or claim a new
quantum mean-estimation theorem.

## Financial output versus digital output

Retain the previous notation and derivation in
[PARITY_EXTENSION.md](../controlled_residual_feasibility/PARITY_EXTENSION.md).
For the continuous GBM contract,

    q = exp(-r(T-tau))/2, k = 2(K-a),
    F = q(E[A|X]-k), Pg = q E[(k-G)+|X],
    R = q[(k-G)+-(k-A)+], C = F+Pg-E[R|X],
    d = 1(V>Kc), Y = d(F+Pg-V-R),
    P = exp(-r*tau) { E[(V-Kc)+] + E[Y] + E[regret] }.

Here regret=(C-Kc)+-d(C-Kc) is nonnegative. Dropping it without an error bound
changes the requested price. The policy, regression coefficients, geometric
control, moment-matched approximation and continuation interval are retained.

The compiled source instead defines a finite random variable Y_d. Independent
q-bit midpoint uniforms are prepared by Hadamards. Paired Box-Muller transforms
compute two normals using log, sqrt and cos; common/idiosyncratic factors produce
the equicorrelated path increments. Both halves of the trajectory are included.
The arithmetic is signed fixed point with 32 integer bits and f fractional bits.
Spots are guarded between 2^-16 and 4096 at fixings; the conditional state is
reset to the guarded state at tau. Elementary functions use explicit arithmetic
and finite one-dimensional coefficient QROMs. They are not tables of prices or
paths. All QROM address comparisons, output writes and cleanup are charged.

The source computes every analytic control and policy operation, the put
complement R, the exercise decision and the signed output. Finally it clips the
digital Y to the representable +/-B, with B the rounded exp(-r(T-tau))*K.
Therefore E[Y_d^2] <= B^2 follows for *every* input word, independently of the
financial interpretation of preceding modular operations. This bound can be
used without a classical variance acquisition.

The tighter existing continuous-model moment and regret certificates do not
automatically apply to Y_d. In particular, analytic Gaussian controls need not
equal conditional expectations under a finite Box-Muller input law. The source's
existence and sampled numerical agreement do not prove that missing bridge.

## Clean arithmetic and hierarchy

Each leaf is an actual list of X, CX and CCX gates. A leaf XORs its result into
an output register, preserves its inputs and restores scratch to zero. Every
invocation copies arguments into distinct local slots, preventing aliasing when
the same SSA value appears twice. Leaf outputs bind to fresh SSA words; scratch
is reused between leaf invocations.

For a graph F, the clean source executes F, copies the named result to a separate
output register, then executes F inverse. Its inverse is explicit. All SSA
temporaries are retained until cleanup; this is a costly space choice, not an
optimal reversible pebbling scheme. Exact constant folding and expression reuse
produce version 2 without changing a single output bit. Version 1 is preserved.

Counts are sums of emitted leaf definitions plus all argument copies, output
copies and inverse calls. A fixed exact seven-T Toffoli expansion is used.
Depths run leaves serially, with all-to-all ASAP scheduling inside each leaf.
They describe this implementation and are not lower bounds on arbitrary circuits.

## Explicit known-moment mean estimator

The foundation is Kothari and O'Donnell,
[Mean estimation when you have the source code](https://arxiv.org/abs/2208.07544),
SODA 2023: Sections 3.1-3.5, Theorems 3.18-3.19, Section 4.1/Lemma 4.3 and
Appendix A. The archived full manuscript was checked; no new advantage-direction
search was performed. This implementation is a conservative constructive
known-second-moment variant. It does not implement the unknown-variance quantile
reduction or claim the final theorem's optimal constants. Equal stage failure
allocation adds a log-log confidence overhead asymptotically.

Suppose E[Y^2] <= s^2. Start with the mean in [-s,s], outward-rounded to an exact
dyadic interval. Let its current left endpoint be L and width W. Throughout the
successful interval contraction, |L| <= s. Choose a power of two S >=32s, so

    RMS((Y-L)/S) <= (s+|L|)/S <= 1/16.

Set epsilon_test=W/(2S). Theorem 3.19 distinguishes a mean offset <=W/4 from
one >=W/2 with probability at least 2/3. On a small result keep [L,L+3W/4]; on
a large result keep [L+W/4,L+W]. Both intervals contain the mean in the ambiguous
gap. Stop when the radius is <= the allocated flat-mean error before discount.
The adaptive controller stores exact rational endpoints; only the phase input
load is rounded to 64 fractional bits.

For z=(Y-L)/S, use U=(2|p><p|-I) diag(exp(-2i atan(z))), with |p> the uniform
random-input state. Theorem 3.18 gives the stated eigenphase localization with
probability >=7/9. QPE phase error epsilon_test/6 and failure <=1/9 imply the
test threshold |theta'|>1.42 epsilon_test. Integer QPE sizes are powers of two
M>=20*pi/(epsilon_test/6). This is intentionally conservative.

To see the QPE tail guarantee, an outcome at circular grid distance d has mass
at most 1/(4d^2). The chosen M leaves at least ten grid cells within tolerance.
Bounding both tails by (1/2) sum_{n>=9}1/n^2 <=1/16 is already below 1/9.
The spectral and QPE failure probabilities sum to at most 1/3. Odd repetition
counts are obtained from the exact Binomial(r,1/3) majority tail; a union bound
over stages is <=0.003. This is an explicit count, not a unit-constant s/error
substitution. The remaining quantum failure allocation is 0.0005 for coherent
phase-function approximation and 0.0005 for rotation synthesis.

The final controlled U runs the financial graph forward without control, computes
the angle graph forward, applies controlled phase gates to its signed binary bits,
then inverts the angle graph and financial graph. Retaining their work until
phase application cancels redundant internal cleanup pairs from the earlier
modular clean-oracle composition. This halves the arithmetic subtotal while
restoring all work after each controlled U. The earlier cost version is retained.
When the control is zero these operations cancel exactly. The reflection is
H/X on random bits, an AND ladder and controlled Z, inverse ladder, X/H, then
Z on the external control. That last Z matters: replacing the reflection with
its negative would introduce a measurable relative phase.

Every QPE power is paid as 2^j repetitions of U. Initial uniform preparation,
phase-register preparation, the full inverse QFT, repetitions, measurement bits,
classical loads and feedback are in the ledger. Repetitions are serial in the
main runtime screen; the longest single QPE chain is also reported, so unlimited
parallel repetition is not silently assumed to eliminate depth.

## Phase precision and synthesis obligations

The angle uses a separate 64-fractional-bit register, exactly promoting the
24- or 40-bit financial output. On [0,1], atan is approximated by degree-eight
Taylor polynomials on 32 intervals. For degree n>=1, the coefficient magnitude
is at most 1/n, from the two complex-log expansions. With half-width h=1/64,
the phase remainder is bounded by 2 h^9/[9(1-h)]. Reciprocal reduction handles
|z|>1; sign handling is explicit.

All 288 stored coefficients were checked against exact rational rounding
intervals. Positive-degree coefficients are rational at the dyadic centers.
Constant terms are enclosed using alternating atan series and Machin's formula
for pi; no floating quadrature is treated as a proof. The stored pi/2 constant
has at most 2e-16 phase error, also checked by rational intervals.

Nearest rounding of L, normalization shifts, reciprocal truncation, coefficient
rounding and the eight Horner multiply truncations are covered by 32 ulps:
normalization contributes at most two argument ulps; reduction at most two;
coefficient plus Horner errors are bounded by geometric sums with ratio h;
clipping the upper interpolation endpoint costs one ulp. Doubling the angle and
allowing the stored pi constant remain within

    delta_phase <= 32*2^-64 + 2 h^9/[9(1-h)] + 2e-16
                = 2.14266341390617e-16.

This applies to the compiled range |Y|,|L|<=100 and S>=16. Under a conservative
hybrid argument, an operator error eta per controlled U perturbs the final
outcome probabilities by at most 2*N_U*eta. The displayed bound fits 0.0005 for
all recorded schedules, including the support-only moment bound. Forty-bit phase
arithmetic failed this budget; its earlier result is preserved.

This closes the *phase-function* approximation obligation. It does not synthesize
the arbitrary controlled phases. CP(theta) is expanded into two CXs and three
single-qubit phases; the pi/2 inverse-QFT cases contribute exact T gates, and
the remaining rotations have a per-rotation operator-error requirement
0.0005/(2*N_R). Exact symbolic dyadic-radian/pi-rational targets are recorded.
Their Clifford+T sequences, routing, physical error correction, decoding and
factories remain unimplemented. Omitting their positive cost in a failed
feasibility screen cannot establish a successful end-to-end runtime.
