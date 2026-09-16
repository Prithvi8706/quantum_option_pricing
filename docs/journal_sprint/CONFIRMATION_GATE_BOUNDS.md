# Confirmation gate work: directed partial encoding bounds

Status: new development, not a confirmation campaign or a claim of quantum
advantage. This explicitly continues the existing arithmetic Asian/PCA route.
Original week13-15 producers, outputs, seeds and gate decisions remain unchanged.
No new hardware run, collaborator sign-off or independent subagent review is
claimed for this increment. The user requested work toward the blockers, not
permission to relabel unknown errors as zero or silently change applications.

## Target and implementation semantics

Business parameters are exact decimal numbers spelled by str(Basket parameter).
The continuous target has log means m and covariance C under correlated GBM.
The archived floating means mhat and PCA factor B are interpreted as exact
binary-float values, defining a nearby Gaussian law with covariance P=BB^T.
All calculations below are outward decimal intervals,80significant digits.
Bounds cover this declared decimal-parameter target; they do not certify the
remaining floating payoff, loading or compiled rotation implementation.

Normal coordinates are independent standard Gaussians, conditioned on the cube
E={|Z_j|<=L}. Midpoint rounding Q has |Q_j-Z_j|<=h=L/2^q. Let D=exp(-rT),
S_i=exp(mhat_i+B_i Z), A=mean(S_i), G=exp(mean(log S_i)), raw payoff
F=D(A-K)+, residual H=D[(A-K)+-(G-K)+]. AM-GM gives0<=H<=F<=DA.
The residual continuous price uses the continuous analytic geometric-call
offset, not the finite-grid control mean. Both offsets remain distinct.

Every lower/upper pair in output encloses a **bounding expression**, not the
actual pricing error. A large upper bound is failure of this screen to establish
accuracy, not proof that the true error is large. No observed discrepancy is
inserted as a guaranteed error bound.

## Directed arithmetic foundation

decimal_enclosure.py uses ROUND_FLOOR/ROUND_CEILING for arithmetic. Python's
[Decimal documentation](https://docs.python.org/3.9/library/decimal.html) specifies
correct rounding for exp/ln/sqrt; these endpoints are enlarged by adjacent
representable numbers. Unary sign changes use copy_negate because ordinary
Decimal negation can round in the ambient context. No float CDF/exp/log enters
the enclosure. Exact archived floats use Decimal.from_float; export to a float
upper bound uses an explicit upward correction.

Pi uses Machin's identity16atan(1/5)-4atan(1/239),120alternating terms and an
enclosed first omitted term. Normal CDF uses

Phi(x)=1/2 + [sum_n (-1)^n x^(2n+1)/(2^n n! (2n+1))]/sqrt(2pi).

For |x|<=10, after n>=50 subsequent magnitudes decrease; stopping requires the
next term's outward upper bound below1e-65. Add a symmetric first-omitted-term
remainder before applying pi's enclosure. Negative x uses symmetry; interval
arguments use monotonicity. Domain/nonfinite/zero-division violations raise,
not silently extrapolate. Regression checks against130digit mpmath and exact
rational arithmetic are useful tests, not replacements for this derivation.

## Sharper tail and midpoint bounds

Let p=P(E), M_i=exp(mhat_i+||B_i||²/2), and
t_i=product_j[Phi(L-B_ij)-Phi(-L-B_ij)]. Exponential tilting gives
E[S_i 1_E]=M_i t_i. Thus conditional spot mean is M_i t_i/p.

For either nonnegative payoff J in {F,H},
E[J]-E[J|E]=E[J 1_notE]-(1-p)E[J|E]. Therefore a valid absolute bound is

T=max(D*mean_i M_i(1-t_i), (1-p)*D*mean_i M_i t_i/p).

This uses the exact product event mass instead of a coordinate union and the
maximum of opposite-signed contributions instead of summing their magnitudes.
It is still a conservative bound because DA replaces the call/residual payoff.

For any row, |S_i(QZ)-S_i(Z)| <= S_i(Z)[exp(h||B_i||_1)-1]. Since the call map
is1-Lipschitz, a raw midpoint bound is

Braw = D*mean_i [M_i t_i/p * (exp(h||B_i||_1)-1)].

For residual, add the same expression for the geometric log row, with
m_g=mean(mhat_i), b_g=mean(B_i), M_g=exp(m_g+||b_g||²/2), and its tilted mass.
This integrates spot sensitivity rather than replacing every spot by a global
cube maximum. Increasing q needs no finite-path enumeration.

## Gaussian model rounding bridge

For uniform monitoring dt=T/dates and positive equicorrelation rho,
lambda_min(C)>=sigma²(1-rho)dt/4=:lambda0. The temporal inverse is tridiagonal
with infinity norm<=4/dt; the correlation eigenvalues are1-rho and
1+(assets-1)rho. This lower bound is also safe for one asset/date.

Compute R=||P-C||_F outward. If S=sqrt(P), U=sqrt(C), then
S(S-U)+(S-U)U=P-C. Diagonalizing the two symmetric factors separately bounds
the Frobenius norm of this Sylvester solution by R/sqrt(lambda0)=delta.
The square polar decomposition B=S O admits an orthogonal O, including a
singular square B. Coupling the true law by U O Z gives a factor difference
with Frobenius norm<=delta. This is a standard matrix perturbation construction,
not a new quantum theorem; see the [matrix-square-root perturbation literature](https://doi.org/10.1016/0024-3795%2892%2990052-C).

For coupled Gaussian logs X,Y with mean error e and row-factor distance<=delta,
|exp X-exp Y| <= |X-Y|(exp X+exp Y). Cauchy-Schwarz gives the price contribution

sqrt(e²+delta²) * sqrt(2[exp(2mhat+2vhat)+exp(2m+2v)]).

Average over rows and discount for raw. For residual add the geometric row,
whose factor distance is at mostdelta/sqrt(d). The analytic geometric-call
formula is evaluated outward as well; the absolute difference from the stored
floating offset is a separately recorded allowance. This bridges rounded
PCA coefficients and log means without assuming a numerical eigensolver exact.
It does not enclose floating evaluation of every payoff or rotation.

## Non-enumerative safe normalization

Let Amax=mean_i exp(mhat_i+L||B_i||_1), and bound every pairwise log spread by
Rlog=max_ij[|mhat_i-mhat_j|+L||B_i-B_j||_1]. Raw payoff is at most
D*max(Amax-K,0). For residual, use the minimum of this and

D*Amax*[1-exp(-Rlog²/8)].

Justification: for a uniform random choice of the d log spots at a fixed path,
the log moment-generating function has second derivative equal to a tilted
variance bounded by Rlog²/4. Integrating twice on[0,1] gives
log(A/G)<=Rlog²/8. Thus A-G<=A[1-exp(-Rlog²/8)], and the call residual is no
larger than A-G. This is an application of the standard bounded-variable
(Hoeffding) argument, not a novelty claim. It supplies a safe mathematical
scale without max(table), but does not implement division, payoff arithmetic or
flag rotations. Their errors/costs still need bounds and actual circuits.

## Integration and frozen deterministic audit

screened_contract is opt-in and updates only tail/discretization for a matching
representation; it deliberately leaves every other component unknown. It is
not a model-identity attestation. Model bridge/offset allowances are recorded
separately until a complete implementation budget exists. Full admission remains
unknown_bias; to_encoding must still refuse it. Old contracts are never mutated.

Before generating the development evidence, freeze code/protocol and audit all
six immutable week13 input records, L in{3,4,5}, raw/residual and q=1..16:576rows.
Use illustrative partial deterministic budget$0.25, not a signed allocation or
confirmed effect size. Report the first tested q meeting that partial budget,
remaining normal qubits/table entries and safe normalization; no circuits or
new sampled prices are generated. Keep all rows, not just qualifying designs.
Strict replay must reproduce them and verify input/source hashes. No gate passes
merely because a partial budget passes. Unsupported domains fail visibly.

## Remaining work to unlock confirmation

1. Finish the implementation budget: loading approximation, fixed-point payoff,
   reversible uncompute, normalization/rotation/synthesis and numerical errors.
   Integrate a non-enumerative oracle; these new scales are inputs, not circuits.
2. Re-evaluate classical MC/control/PCA-RQMC/conditional costs on the identical
   admitted target; direct summation remains decisive for enumerated tables.
3. Assess a defensible contribution against prior work. [QSP derivative pricing](https://arxiv.org/html/2307.14310v2)
   reduces payoff resources for its constructions but is not a drop-in proof
   for this Asian residual. No new algorithm/advantage is established here.
4. For confirmation, keep native IQAE a qualified comparator unless its exact
   stopping implementation is justified. A [modified IQAE theorem](https://arxiv.org/abs/2208.14612)
   does not certify our unchanged native adapter. Do not relabel fixed CP as IQAE.
5. Once target/method are fixed, choose primary outcomes, error/delivery targets,
   held-out regimes, repetitions and multiplicity explicitly. Aasa and the
   collaborators must provide actual scientific review/sign-off. This development
   request cannot supply their agreement or establish authorship contributions.
