# Independent mathematical referee review

Date: 2026-09-21. Reviewer: separate AI mathematical-review agent, assigned
independently of the existing implementation and of the new label adapter.
This is AI-assisted review, not human expert endorsement or a formal proof.

## Verdict and consequential findings

The restricted normalization result, fixed-point residual construction, and
declared ideal-logical error schedules have coherent mathematical foundations.
Independent rational reconstruction found no violation in any of the 18
signed-residual records. A fixed set of 1,332 production-grid nodes also passed
independent pointwise checks. These checks support correctness within the
specified model; they establish neither a new quantum primitive nor a general
complexity advantage.

One consequential interface gap was identified during this review. The frozen
residual decoder accepts a binary64 probability, while canonical AE produces
an integer label whose mathematical meaning is a generally nonrepresentable
real probability. The frozen budget does not certify this conversion. This
is a classical numerical obligation even with perfect quantum gates. An
abstract exact-label/exact-decoder theorem remains valid, but the frozen
decoder alone cannot support a complete executable binary64 delivery claim.
The root agent implemented a separate opt-in adapter, which this reviewer did
not author. Its conversion and median arguments are sound; its bounded audit
finds ample margin without changing any archived schedule. See the disposition
below. Frozen acquisition evidence has not been rewritten.

| Finding | Severity / disposition |
| --- | --- |
| AE-label-to-binary64 conversion absent from frozen residual delivery interface | Material qualification; addressed by the separate opt-in adapter and added allowance, subject to use of that adapter. Historical frozen result remains explicitly scoped. |
| No new primitive or substantial new abstract theorem demonstrated | Major publication limitation; theorems must support an implementation/comparison paper, not be advertised as foundational novelty. |
| Projected resource ratios are not optimized-cost ratios or runtime bounds | Major claim restriction, already explicit in the restricted propositions. |
| All 18 reconstructed residual inequalities and schedules pass | Positive mathematical evidence, conditional on the reviewed parent and offset certificates. |
| Nominal degrees 12 and 16 coincide after quantization | Interpretation limitation: 24 primary configuration pairs share coefficient lists; they are not independent approximation families. |
| Physical execution and classical rigorous-confidence comparison remain unproved | Open gates; no change of admission status is warranted. |

## Materials actually inspected

No applicable `AGENTS.md` was found in the workspace or checked ancestor paths.
The following method/protocol documents were read: stronger arithmetic method,
protocol, results and review dated 20260921; signed residual method and protocol
dated 20260921; `CLAIM_THEOREMS_20260917.md`; minimal-pivot Week 1 and Week 2
methods. Their mathematical restrictions were compared against implementation.

Implementation inspection covered complete files
`research/stronger_arithmetic/{budget,circuits,residual,residual_circuits,
residual_components,run_study,run_residual,verify_residual}.py`;
`research/journal_sprint/{claim_assessment,control_offset_enclosure,
decimal_enclosure,encoding_enclosure,week2_pipeline,week2_decoding,
normal_loader_budget,reversible_fixed_point,asian_basket}.py`; the first 120
lines of `run_minimal_pivot_week2.py` establishing contracts and integration;
and the first 220 lines of `matched_arithmetic.py` establishing its logical
compiler and original component convention. This was not a new exhaustive
gate-level audit of every production circuit.

The review read the three replay receipts named in the release closeout:
`stronger_arithmetic_pinned_replay_20260921.json`,
`signed_residual_pinned_replay_20260921.json`, and
`residual_parent_pinned_replay_20260921.json`. The independent check reads all
18 full residual records and 72 range-reduced primary records, retaining
input hashes. Historical full-suite and pinned-suite counts were read in the
closeout; this reviewer did not rerun either suite or independently inspect
every historical test case.

For the new bridge, this reviewer inspected
`research/assessment_20260921/label_bridge.py`, `verify_label_bridge.py`,
`tests/test_assessment_label_bridge.py`, the pre-execution
[label protocol](../LABEL_BRIDGE_PROTOCOL.md), and the machine-readable
[corrected bridge receipt](../provenance/label_bridge_v2.json), with the
[original receipt](../provenance/label_bridge_v1.json) retained for history.
Passing targeted tests
were reported by the root agent; this reviewer reviewed their assertions and
the numerical derivation rather than presenting those tests as its own run.

The primary mathematical references were inspected directly as described in
the final section. The broader novelty search belongs to the separate
literature review, not this review's independent search scope.

## Exact target and representation contract

Let d be the number of asset/date entries, not just the number of assets.
The continuous contract is a discounted call on their equally weighted
arithmetic mean under the stated correlated geometric Brownian motion model.
D1 has one asset and two dates, sigma 0.2, strike 95; D2 has two assets and two
dates, sigma 0.25, strike 105 and asset correlation 0.4. Both use spot 100,
rate 0.03 and maturity 1, with two uniformly spaced monitoring dates. D1's
stored correlation parameter does not create a second asset.

The finite target is

\[
A(z)=d^{-1}\sum_i\exp(\mu_i+F_i z),\qquad
V_q=D\mathbb E_q[(A-K)_+].
\]

Here stored binary64 means and factors are interpreted exactly. Coordinates
are independent normals conditioned on the cutoff cube, with exact cell
masses and exact uniform cell midpoints. Production has cutoff 4 and q=10.
The continuous contract parameters instead have exact decimal semantics.
`encoding_enclosure` charges the bridge between the corresponding Gaussian
models, truncation/renormalization, and midpoint discretization.

The model bridge uses covariance residuals and a conservative positive lower
bound on the true covariance spectrum. Rotational coupling of Gaussian
factors, Cauchy-Schwarz, and exponential second moments bound price changes.
The payoff's 1-Lipschitz property carries basket errors to call errors. The
tail identity correctly takes the maximum of positive omitted mass and the
opposite renormalization term; it does not add two biases with the same sign.
The midpoint inequality uses a coordinatewise log displacement bounded by
`cutoff / 2**q` times each row's l1 norm. No contradiction was found in these
mechanisms. The new bounded script does not independently recompute these
historical representation enclosures.

Restoring a finite-model polynomial control leaves this finite call target
unchanged. It does not turn q1/q2 diagnostics into q10 results or the finite
grid into the continuous contract without the separate representation bound.

## Restricted theorem audit

**Independent-cube normalization.** For nonnegative c_i, C=sum c_i and K>=0,
excluding C=K=0, the minimum fixed exact normalization of
f(t)=sum c_i t_i-K over the whole independent cube is

\[
\alpha_* = \max(K,|C-K|)=C/2+|C/2-K|.
\]

Every projected unitary block is a contraction, giving the lower bound from
the endpoint range [-K,C-K]. A row reflection with block 2t_i-1 and weights
c_i/2 plus constant C/2-K attains it by signed LCU. The shared reflection is
a valid block-diagonal factoring of these conjugations. Hermitian-involution
structure, not merely one matching projected entry, supplies the intended
QSP signal plane. This is a useful explicit specialization of established
LCU/block-encoding machinery, not a new primitive. See Low-Chuang Section 3.1
and Gilyén et al. Section 4.3 below.

The independent cube is larger than the actual correlated basket support.
The exact counterexample C=1, K=3/4, fixed t=1 has actual norm 1/4 and
cube norm 3/4. Thus instance-optimal normalization is false without further
conditions. Negative c_i are outside the proposition. C=0,K>0 gives a
constant target; C=K=0 has normalization infimum zero but admits no division
by zero. The reviewed theorem already makes these restrictions explicit.

**Degree/cost planning proxy.** Under constant positive g,beta,a,e and a
continuous n>a/e, W=g beta n^2/(en-a) has minimizer n=2a/e, value
4g beta a/e^2. The reported nonnegative difference identity is exact.
It ceases to be an implemented-algorithm theorem when degree is discrete,
dyadic AE or caps intervene, or per-query work, normalization, loader
precision or deterministic allowances depend on n. A quadratic normalization
criterion follows only under the stated common proportionality constants.
The calculus is not substantial theorem novelty.

**Finite-menu selection and projected ratios.** Minimizing the declared
composition formula among feasible menu entries is valid and useful, but is
enumerated optimization, not a theorem about unlisted encodings. Two upper
bounds U_1,U_2 do not order their unknown optimized costs. The supplied
counterexample U_1=200,U_2=100,T_1=10,T_2=90 is exact. A ratio of these
composition formulas must retain its resource-model qualification.

## Range-reduced arithmetic certificate

At Q=2^f, signed X is shifted to Y=floor(X/2^s), evaluated by fixed-point
Taylor/Horner coefficients floor(Q/k!), squared s times with floor
rescaling, then multiplied by the integer spot. For either sign of X,

\[
0\le X/(2^sQ)-Y/Q\le(2^s-1)/(2^sQ).
\]

For true |x|<=h and |X/Q-x|<=dx, the implemented reduced domain is bounded
by (h+dx)/2^s plus that shift error. Taylor's Lagrange remainder is bounded
by exp(R) R^(n+1)/(n+1)!, coefficient errors propagate through Horner, and
each floor adds less than 1/Q. If |z_true|<=B and |z_hat-z_true|<=e, then
one square has error at most 2Be+e^2+1/Q. The code uses precisely this
recurrence, then adds the separate input bridge
spot*exp(h+dx)*dx. The integer final spot multiplication introduces no extra
fixed-point rounding.

Full products are bounded before their retained slices. The signed lower
limit includes -2^(w-1); the upper limit is strict. Additions, shift/add spot
prefixes, all row sums, poststrike subtraction, and the selector numerator
are range checked. Modular gate arithmetic matches unbounded signed-floor
arithmetic only when those checks pass. Scratch reuse is permitted by clean
compute/copy/uncompute, not by a basis-state-specific reset.

At f20, nominal Taylor degrees 12 and 16 both reduce to degree 9 after zero
coefficient removal. At f24 both reduce to degree 10. This occurs for all
two cases, two word widths and three reductions: 24 duplicate pairs among
the 72 primary range-reduced configurations, before pairing layouts. Their
nominal remainder certificates can differ even though their integer map and
gate sequence coincide. Counting them as distinct implementations or as
independent evidence of degree sensitivity would be misleading.

## Signed residual theorem and unit audit

For B enclosing |A-K| over the cutoff cube, let x=(A-K)/B,
g(x)=(x+p4(x))/2 and C(A)=B g(x). Then the exact identity is

\[
r(A)=(A-K)_+-C(A)=\frac B2(|x|-p_4(x)).
\]

The degree-four Chebyshev coefficients of |x| are
(2/pi,0,4/(3pi),0,-4/(15pi)). Absolute summation of the remaining tail
gives 2/(5pi). If eta is the sum of exact stored-coefficient discrepancies,
then |r(A)|<=B(1/(5pi)+eta/2). This is a **normalization bound**, not an
additive payoff bias: the residual is retained and estimated.

The stored polynomial has exact witnesses

\[
r(K)/B=-4587328911378127/72057594037927936<0,
\quad r(K+B)/B=859275365064993/72057594037927936>0.
\]

These are domain witnesses, not promises that both points are reachable in
every financial grid. They disprove a universally unsigned or clipped
interpretation of this residual.

The input integer is a **sum of spots**, not the averaged basket. With
t=sum_integer-dKQ, k=floor(Q/(dB)), a_j=floor(Qb_j) and S=floor(QdB),
the required integer map is

\[
v=\lfloor tk/Q\rfloor,\quad
y\leftarrow\lfloor vy/Q\rfloor+a_j,\quad
C_{int}=\lfloor yS/Q\rfloor,\quad
R_{int}=\max(t,0)-C_{int}.
\]

All divisions floor toward negative infinity. The coefficients b_j already
describe g; adding x or halving again would be wrong. Inspection of the
current emitter found neither duplication.

If E bounds each parent's spot error, then |Ahat-A|<=E and

\[
\Delta_x=E/B+d(B+E)|k/Q-1/(dB)|+1/Q
\]

is valid. With R=1+Delta_x, coefficient errors delta_j and
h4=delta4, h_j=R h_(j+1)+1/Q+delta_j, the implemented polynomial error is
h0. The derivative and magnitude sums Lg=sum j|b_j|R^(j-1),
G=sum |b_j|R^j yield

\[
E_C=dB(L_g\Delta_x+h_0)+|S/Q-dB|(G+h_0)+1/Q,
\quad E_R=dE+E_C.
\]

Thus |R_int/Q-d r(A)|<=E_R. `residual_sum_error_upper` is in sum-scaled
undiscounted dollars; the price allowance is D E_R/d. Dividing again or
adding the parent D E separately would respectively undercount or double
count errors. The current completed residual budget uses the correct units.

The analytic residual bound is intersected with direct integer intervals
only after proving it for the unbounded reference. For
J=floor(upper Q(dB rho+E_R)), integrality justifies **floor**, not ceiling.
H=2^bitlength(J) is strictly greater than J, including J=0. With
2^m=2H, the shifted threshold lies strictly between 0 and 2^m. Signed word
and product checks establish that the modular circuit has this value.

A uniform m-bit selector U gives exactly
a=Pr[U<R_int+H]=(E[R_int]+H)/2^m. No additional threshold discretization
is needed. This is an affine encoding through a standard reversible
comparison; the signedness and careful certificate are useful engineering,
not evidence of a new quantum primitive.

## Offset, decoder, and confidence

The control expectation is obtained from exact finite-model moments through
degree four. Multinomial expansion and independence factor each moment into
marginal exponential sums; the production product grid is not enumerated.
`moment_enclosure` uses exact truncated normal cell masses, directed CDFs,
and geometric progression of node exponentials. The model/q/cutoff/strike/
radius/polynomial binding is checked before reuse. A matching binding is not
itself a proof that an arbitrary supplied certificate is true; archive
integrity and re-enclosure remain necessary. The archive supplies those
checks, and the code correctly describes the offset certificate as trusted
mathematical evidence.

If the archived offset O approximates D0 E[C(A)], restore it and charge
its enclosure discrepancy. The discount bridge is bounded by
|D-D0| B sum |b_j| on the true domain |x|<=1. The affine ideal decoder
is O-DH/(dQ)+D 2^m a/(dQ). Its slope L, not the control magnitude, governs
loader perturbations. Product preparation state error <=d epsilon_loader
gives the conservative price allowance 2L d epsilon_loader. The constant
offset adds no preparation sensitivity.

Stored affine constants and two binary64 operations have an explicit
bound; the error bound covers endpoints a=0,1 and subnormal absolute error.
It does not cover conversion of the real AE label to binary64. The newly
reviewed adapter encloses sin^2(pi*y/M), chooses a float, and directly bounds
that float's distance from the enclosure. For an odd sample, sorted lower
and upper endpoints enclose the median. Coordinatewise perturbations of at
most eta change the median by at most eta, so **add L_upper eta** to the
existing deterministic budget. That derivation avoids an assumption about
libm sine's accuracy.

The new receipt exhausts 384 labels for M=128 and M=256 and checks all 18
budgets. Its actual added allowances are approximately 1.7020e-15 dollars
(D1) and 3.4159e-15 dollars (D2). Independently, the simpler sufficient bound
for correctly rounded labels, L_upper*2^-53, is at most 6.8955e-15 dollars,
while the smallest archived schedule margin is 0.02307138946 dollars. This
shows why the interface can be repaired without changing resource orderings.
Using the adapter and its additional allowance is an explicit new condition;
it must not be silently attributed to the frozen producer.

BHMT Theorem 12 bounds one exact-label trial by
2pi sqrt(a(1-a))/M+pi^2/M^2, hence by pi/M+pi^2/M^2, with success >=8/pi^2.
For independent repetitions, conservatively replacing success by 0.8 and
taking the median of 17 gives failure <=exp(-0.18*17)<0.05. Our independent
exact binomial bound is 0.0025814628368384, so the advertised 95% is safe
under those assumptions. Independence, ideal controlled powers/QFT,
correct logical A/A-inverse, and the declared deterministic budget are all
required. This review does not replace the production schedule with the
sharper binomial rule. [BHMT, Theorem 12](https://arxiv.org/pdf/quant-ph/0005055v1).

The new bridge verifier initially tested previous-dyadic rejection using
only an upper bound on pi. That establishes minimality relative to that
chosen envelope. Strict mathematical rejection should use a lower pi bound.
This reviewer reported the distinction; the root agent corrected the verifier
to use the lower pi bound and retained both receipts. The v2 receipt supersedes
the original receipt's mathematical-minimality wording. This reviewer inspected
the correction, checked its current source/input hashes against v2, and checked
positive new margins and negative previous-M margins for all 18 rows. The
independent rational check also rejects previous M with a lower pi bound.
Final disposition: no outstanding mathematical blocker within the opt-in
label-bridge scope. No complete native-gate or physical-delivery claim follows.

## Bounded independent evidence

The [protocol](math/PROTOCOL.md) was written before execution. The
[script](math/check_certificates.py) imports no project certificate module.
It reconstructs residual algebra with exact rationals and an independent
Machin pi enclosure, checks all recorded stages' signed limits, decoders,
budgets, strict shifts and minimal dyadic schedules, and records input hashes.
The [receipt](math/independent_checks.json) records 18 passing rows and 1,332
selected q10 nodes in 4.85 seconds on Python 3.9.13.

| Selected record | Nodes | Largest enclosed spot error / parent bound | Largest enclosed sum-residual error / bound |
| --- | ---: | --- | --- |
| D1_00 | 36 | 0.000189615 / 0.000258369 | 0.001567354 / 0.008790614 |
| D2_00 | 1,296 | 0.000906939 / 0.001426449 | 0.010916515 / 0.129607007 |

Displayed numbers are rounded upward summaries of the receipt. All thresholds
stay within the archived certificate. This selected-node result supplements
the universal derivations; it is not an exhaustive q10 proof. Exact arithmetic
of a purported bound also cannot prove an inherited parent or offset theorem
whose assumptions have not been established. Those derivations were reviewed
analytically above; a machine-checked proof was not attempted.

The existing replay receipts distinguish all-row certificate reconstruction
from selected gate re-emission. They cover 74 primary certificates, all 18
residual certificates, two offsets, selected loader/reflections, six distinct
primary configurations in both layouts including the residual parents, and
two selected complete residual oracles. Their verifiers replay the same
certificate producers and hence are not independent derivations of every
bound. The new rational audit supplies additional independence for the
residual inequalities; it does not retroactively make every historical
certificate independently derived or every circuit fully simulated.

## Publication significance and remaining obligations

The strongest mathematical contribution visible here is a carefully specified
and auditable composition of known methods for a fixed application. Its
value is the explicit error/normalization/resource connection and the
matched-comparator consequence. That can support a reproducible comparative
study if the claim stays narrow. It cannot carry a paper whose main claim
is a new quantum primitive, a globally optimal normalization, a new
asymptotic speedup, or a theorem of quantum-over-classical advantage.

The D2 ordering change is consistent with introducing a comparable classical
control into the arithmetic route and reducing its AE sensitivity/query
count. Algebra does not make that causal decomposition unique: precision,
range reduction and implementation also differ. There is no reason to infer
a universal reversal from two development contracts. Large residual-oracle
width and alternate synthesis conventions can change practical rankings.

Remaining mathematical obligations for an executable scientific package are
to specify the new label adapter and allowance in the advertised contract,
carry physical/native synthesis error separately if hardware claims are ever
made, and keep rigorous quantum confidence distinct from approximate
classical RQMC Student-t intervals. The shared-reflection QSP phase-response
and every historical rotation/representation certificate were not derived
afresh in this pass. Human review of novelty, numerical analysis and circuit
assumptions remains valuable and has not occurred in this review.

## Primary mathematical sources checked

1. Gilles Brassard, Peter Hoyer, Michele Mosca and Alain Tapp,
   *Quantum Amplitude Amplification and Estimation*. arXiv
   [quant-ph/0005055v1](https://arxiv.org/abs/quant-ph/0005055v1),
   15 May 2000; published in AMS Contemporary Mathematics 305:53-74 (2002),
   [DOI 10.1090/conm/305/05215](https://doi.org/10.1090/conm/305/05215).
   Read the amplitude-estimation algorithm, Theorem 12 and proof, printed
   pages 18-20. It estimates an exact mathematical sin-squared label and
   supplies the success theorem used here; it does not certify this project's
   binary64 implementation.
2. Guang Hao Low and Isaac L. Chuang, *Hamiltonian Simulation by Qubitization*.
   [arXiv:1610.06546v3](https://arxiv.org/abs/1610.06546v3),
   11 July 2019, accepted version; Quantum 3, 163 (2019),
   [DOI 10.22331/q-2019-07-12-163](https://doi.org/10.22331/q-2019-07-12-163).
   Read Section 3.1, equations 8-10 and Lemma 5, printed page 8. It gives
   PREP/SELECT linear combination and l1 normalization, directly underlying
   the project's specialization. It explicitly separates this realization
   from optimal decomposition/gate-count questions.
3. Andras Gilyen, Yuan Su, Guang Hao Low and Nathan Wiebe,
   *Quantum singular value transformation and beyond: exponential
   improvements for quantum matrix arithmetics*.
   [arXiv:1806.01838v1](https://arxiv.org/abs/1806.01838v1), 5 June 2018;
   STOC 2019, pages 193-204,
   [DOI 10.1145/3313276.3316366](https://doi.org/10.1145/3313276.3316366).
   Read Section 4.3, Definition 51, Lemma 52 and its proof, printed page 46
   of the arXiv version. It states the LCU block-encoding/error composition
   that makes the basic algebra established prior art. Version-specific
   numbering is used; this was not a formula-by-formula reread of the entire
   67-page paper. The arXiv metadata inspected listed v1, not an invented
   revised version.

Sources checked 2026-09-21. The restricted propositions' significance was
assessed from their explicit derivations and these primary statements, not
from marketing or search snippets.
