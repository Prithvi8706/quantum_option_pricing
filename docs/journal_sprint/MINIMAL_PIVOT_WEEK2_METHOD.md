# W2 integration and accounting

## Implemented pipeline

The standby candidate and original encoding share the same adapter:
product-normal loader -> signal/QSP residual -> Hadamard expectation readout
-> canonical amplitude estimation -> classical degree-four offset and decoding.
No global joint-price table is used in the production-resolution plan.

Let x=(A-K)/B, low polynomial l, high polynomial h, and normalized residual
r=(h-l)/rho (with the archived coefficient discrepancy included). The price
approximation is O+beta E[r(x)], where

    O = exp(-rT) B/2 E[x+l(x)], beta = exp(-rT) B rho/2.

The offset O is evaluated from directed finite-grid basket moments. The
Hadamard test has flag-one probability p=(1-Re E[U_QSP])/2. The price decoder
is O+beta*(1-2p). Confusing a real amplitude with its squared magnitude would
be a different algorithm; the integration tests explicitly check this sign
and probability convention against an independent scalar response.

QSP uses the same signal plane as W1. The W2 adapter applies an explicit
R=2P-I instead of constructing R from pi/2 projector phases. Each signal,
reflection and projector is appended as an atomic gate, avoiding accumulation
of hundreds of global phases in one circuit-level binary number. Both signal
families receive this adapter. No W1 producer or archive is overwritten.

## Deterministic dollar accounting

All numerical components are outward rounded using the existing directed
interval implementation. The ledger includes continuous-to-finite model,
tail and midpoint error; binary discount; polynomial approximation; residual
coefficient bridge; archived uniform QSP phase-response error; signal and
loader errors; projector phase wrapping; radius bridge; offset, scale and
decoder rounding.

For the ideal and stored radii, on the good block

    |x_real-x_stored| <= |B_real-B_stored|/B_stored.

The residual polynomial derivative is bounded by sum_k k^2 |r_k| since
|T'_k(x)|<=k^2. Multiplication by beta yields the price radius-bridge term.
The phase-response certificate is used at x_real, while this derivative
bound bridges the intended residual polynomial to x_stored; no unproved
Lipschitz constant for the complex QSP response is substituted.

Unitary products telescope: degree signal errors and all projector errors
add in operator norm. A preparation state error delta changes a bounded
expectation by at most 2delta. The folded-loader certificate adds exact
rational multiplexer rounding to the earlier directed tree-angle bound.
For each projector the actual stored wrapped global phase is compared with
-phi modulo an interval enclosure of real 2*pi. The R sign contributes the
stored-pi discrepancy separately. Decoder rounding uses a conservative
binary64 operation bound on offset+beta*(1-2p), for p in [0,1].

Scope matters: ideal **controlled logical gates and exact AE/QFT** are the
execution model for this ledger. Qiskit's subsequent native decompositions,
fault-tolerant rotation synthesis, device noise and readout errors are not
certified by it. The physical execution entry remains null. Neither a logical
schedule nor a small statevector match promotes the production gate.

The separate directed decoder encloses sin^2(pi*y/M), using symmetry to keep
the trigonometric series argument in[0,pi/2], and encloses the median of an odd
set of outcomes by medians of lower/upper endpoints. It then encloses the
stored-offset/stored-beta price. The tiny runner's ordinary libm decoder is a
diagnostic and is checked separately, not silently treated as certified.

AE estimates the probability of the stored logical A, with its exact inverse.
Consequently deterministic A-versus-target bias is accounted once in dollars;
the AE theorem applies to that actual probability. Uncontrolled errors in each
physical invocation would require a different repeated-execution analysis and
cannot be covered by this argument. They remain in the unknown physical entry.

## Statistical schedule and resources

[Canonical amplitude estimation](https://arxiv.org/abs/quant-ph/0005055)
provides amplitude error at most pi/M+pi^2/M^2 with success at least8/pi^2.
Use the conservative success lower bound0.8. An odd median of R independent
trials fails with probability at most exp(-0.18R). Choose the smallest power
of two M fitting the remaining dollar budget, then the smallest odd R with
that failure bound<=0.05. Counts include R*(2M-1) calls to A or A inverse.
The small actual circuit uses M8 and21 simulated measurement repetitions;
it is a convention/correctness demonstration, not a dollar1 production run.

Production resource projections include loaders, controlled residual signals,
controlled QSP projectors, R, the extra AE controls, both A directions, flag
reflections, zero reflections and inverse QFT. Controlling a U/CX signal
gate-by-gate uses at most2CX per U and6CX per CX; single-qubit gate upper
projections are also charged when applying a second control for AE.
The zero reflection is actually compiled using a clean-ancilla v-chain. Its
workspace is explicitly added to the qubit count, not borrowed invisibly.
No cancellation across block boundaries is assumed. These are conservative
composition projections, not optimized whole-circuit costs, T counts, or
hardware runtime measurements. Classical setup/certification timing is archived
separately and must not be omitted when making later end-to-end comparisons.

## Classical comparison semantics

All three classical methods target the original continuous GBM expectation,
not the tiny midpoint grid. A separately sampled1024-path pilot fits the
geometric control. Each reported mean uses16 independent replicates;
antithetic MC pairs stay within each replicate. RQMC scrambles are independently
seeded. Student-t halfwidths across replicates are diagnostic, approximate95%
intervals; they do not prove finite-sample coverage or enclose numerical/model
errors. Conditional root residuals are checked, not directed certificates.
Agreement between methods is not proof that any approximate interval covers.

Thus this study can compare proposed logical dollar1 schedules with classical
empirical dollar1 precision, but cannot claim a matched rigorous-confidence
hardware race. Unknown execution costs/coverage are explicit blockers, not zeros.

## Precision-cost diagnosis, not an algorithmic lower bound

The archived uniform approximation bounds at degrees16/32/64/128 are
0.0199634873,0.0099999551,0.0050024247,0.0025017672: approximately proportional
to1/n. For this uniform absolute-value approximation strategy, increasing
accuracy is therefore not free inside an AE oracle.

For a simplified fixed-q model, write payoff error a/n, remaining total
allowance e, AE work proportional to beta/(e-a/n), and per-A circuit cost
proportional to g*n. The resulting continuous proxy is

    work(n) proportional to g*beta*n^2/(e*n-a),  n>a/e.

Differentiation places its minimum at n=2a/e, where the payoff and statistical
allowances are balanced. The optimized proxy scales as g*beta*a/e^2, not
1/e. Since a and beta both carry normalization B (rho held fixed), reducing
B can improve constants quadratically even if g rises. This explains why
W1's signal-times-degree proxy can give a different choice from W2.

If midpoint precision must also increase so2^q grows proportionally to1/e,
our dense marginal multiplexer construction can add another inverse-error
factor. These are conditional planning-model observations, not fitted scaling
results, lower bounds on quantum pricing, or a proof that alternative encodings
cannot win. They identify a specific obstruction: constant-factor signal
savings alone do not preserve AE's oracle-query scaling in total gate cost.
Distribution-aware approximation, a different payoff realization, or structured
loading would need fresh proofs and matched experiments; none is claimed here.
