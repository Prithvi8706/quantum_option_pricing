# Audit A: exponential integration and autocallables

Primary: [Cibrario et al., arXiv:2507.19039v1](https://arxiv.org/abs/2507.19039v1),
11 pages. All sections, Algorithm 1, Tables I/II and figure captions reviewed.
Below is our technical audit, not a transcription or full experimental replication.

## Equation ledger

| Equation | Independent check and transfer obligation |
|---|---|
| 1 | GBM dynamics: fix measure. A historical fitted drift is not automatically a risk-neutral pricing drift. Our study keeps its risk-neutral model. |
| 2 | The exponential increment follows Ito's correction, with volatility times sqrt(dt). Exact for constant-coefficient GBM, not arbitrary local/stochastic volatility. |
| 3 | Probability loader needs square-root probabilities and normalization; retain truncation/discretization distinctions. |
| 4 | Good-flag probability, not amplitude, is the normalized payoff. A comparator implementation retains an auxiliary register; it cannot generally erase it for free. |
| 5 | Orthogonality of the path register yields the expectation. Scale and shift must be restored to obtain dollars. |
| 6 | Separate Gaussian loaders give independent driving coordinates; correlations need a factor transform. Parallel loaders save depth, not count or aggregate error. |
| 7 | Log returns add over time. Arithmetic-average asset prices do not: replacing the latter by averaged log returns changes the contract. |
| 8 | Number-to-amplitude mapping requires its argument in [0,1] and reversible treatment of garbage. |
| 9 | Square-root payoff transformation requires positivity and bounded range; polynomial precision is part of the price contract. |
| 10 | Comparator sums the prepared reference probability through the inclusive threshold. Success/failure garbage depends on the threshold; retain it in AE and its inverse. |
| 11 | Finite geometric distribution has normalizer sum(exp(a*r)); use a shifted exponent numerically to avoid overflow. |
| 12 | Binary expansion factorizes exp(a*r). Each bit's probability odds are exp(a*2^i); a product of RYs gives the finite distribution. Independently tested. |
| 13 | Sum the finite geometric series. The a=0 limit is (x+1)/2^n for the probability, not 0/0; negative rates also work. |
| 14 | Restricted support is inclusive. Its cardinality is x1-x0+1. The subsequent power-of-two prose uses x1-x0; do not implement that literally. |
| 15 | CDF saturates at 0/1 outside support. The numerator has x+1 and denominator x1+1. Our tests include both endpoints and a=0. |
| 16 | Tensor product preparation costs every marginal. Independence is in driving factors, not necessarily asset returns. |
| 17 | Initial accumulator must fit the signed fixed-point first increment. |
| 18 | Scaling, offset, coefficient rounding and Gaussian grid convention require a documented representation bound. |
| 19 | Accumulation needs guard bits to prevent modular overflow; retaining inputs permits an inverse. |
| 20 | Barrier predicate records each observation, using a specified strict inequality. Discrete monitoring is not continuous barrier monitoring. |
| 21 | First-hit coupon indicators must be disjoint; otherwise rotations compose rather than select a payoff. |
| 22 | Branch-selected rotation implements a coupon only on its activating subspace; omitted registers in shorthand are not discarded physically. |
| 23 | Put activation needs no prior coupon, terminal loss, and OR of barrier hits. This resolves the printed payoff formula's inconsistent 'all times' condition in favor of Algorithm 1's 'at least once'. |
| 24 | The zero-dollar branch usually needs nonzero encoded probability after a negative-payoff shift. |
| 25 | Dollar error is probability error times scale; depth savings that enlarge scale can lose overall. |
| 26 | Re-derive extrema from the **discounted** payoff. A safe larger undiscounted loss bound is possible for positive rates, but is not automatically the tight range; conventions must be consistent. |
| 27 | Gaussian tail expression is a conservative union-style bound, not exact tail mass. A probability tail alone is insufficient for an unbounded arithmetic-call payoff without a payoff-weighted tail bound. |
| 28 | Truncation and payoff range are coupled; solve jointly, then allocate a sum of error components. Bounding each by the whole tolerance is insufficient. |
| 29 | Count all rotation layers in synthesis error allocation; variational fitting error is separate from rotation synthesis error. |
| 30 | Comparator serial depth assumes the reference loader can really be prepared concurrently, with sufficient qubits and resources. |
| 31 | Count forward/inverse/reference preparations, reflection and controlled inequalities. Verify the exact-amplification assumptions before accepting one round. |

Unnumbered total-depth expression: the initial preparation and each Grover power
must be counted with the actual shot schedule. Multiple circuit shots require
multiple initial preparations. A sum of Grover powers alone does not capture all
execution time, and T-depth is not physical wall-clock time.
Table I's differing leading rotation-depth formulae also require checking the
synthesis assumptions: RY and RZ are related by Clifford conjugation, so their
asymptotic T costs cannot be treated as fundamentally different without a
specified construction/error convention. We did not reproduce that synthesis.

## Two derivations needed before transfer

For inclusive support `[l,u]`, reference probability through x is

`F(x) = (exp(a*(x-l+1))-1)/(exp(a*(u-l+1))-1)`.

For a flat distribution take the continuous a->0 limit. With `m=u-l+1`, choose
`N=2^ceil(log2(m))`. Prepare a geometric distribution on N points and select the
heavier end of length m (upper end for a>0, lower for a<0). Since m>N/2, its
probability is at least 1/2; shift to the desired support after selection. This
explains how a well-chosen bounding distribution can avoid a tiny success rate.
It is not true that an arbitrary distant interval in the full original register
can always be selected in one amplification round.

For initial good probability p, phase-matched one-round amplification has bad
amplitude proportional to `z+p*(z-1)^2`, where `z=exp(i*phi)`. It vanishes when
`cos(phi)=1-1/(2p)`, feasible only for p>=1/4. Preparation, its inverse, phase
rotations and a reflection must all be paid. Knowledge/error of p also matters.

For our arithmetic basket, spots [50,200] and strike 100 give a call payoff 25.
Exponentiating the mean log spot gives 100 and payoff zero. Thus applying the
paper's log-domain shortcut to an arithmetic mean is an invalid 'optimization'.
Mixture loading can encode the mean price, but the outer positive-part function
still requires a polynomial transformation or an arithmetic exercise predicate.

## Methodology and code audit

The paper separates resource analysis for the restricted-support loader from
simulation of the earlier full-support loading approach (Section V). Thus the
approximately 50-fold payoff T-depth claim is not a measured end-to-end hardware
speedup or a comparison with RQMC. The common Gaussian/arithmetic path limits
the total gain. Discretized exact enumeration is a validation reference, not a
competitive continuous classical solver.

Pinned author repository: Classiq/classiq-library at
`d09ddcbd5ffe6d853241e00f460f0f4006c4dc3f`, finance/autocallable_options.
Both notebooks inspected, not executed. Findings requiring care:

- Partial-loader `get_good_states_amplitude` says inclusive endpoints but uses
  endpoint exponent differences without +1. Direct finite-sum checks are
  recorded in `four_paper_baselines_v1/results.json`. We have not established
  the resulting Classiq execution error or contacted authors.
- Pricing notebook uses second coupon 3; paper Table II gives 5. Current source
  cannot be treated as exact reproduction of that table without reconciliation.
- The Gaussian grid uses left endpoints; ours uses cell midpoints. Matching
  cell probabilities does not make the finite price targets identical.
- Drift is explicitly derived from historical returns. Do not adopt this as
  our risk-neutral drift without changing and identifying the pricing measure.
- The final IQAE call is commented and a numeric result is printed literally.
  This is not a fresh execution receipt. We neither ran it nor count that
  printed number as independently reproduced evidence.

Recommended transfer: exact endpoint accounting and scale-aware comparator
design; a separate best/worst-of study if authorized. Do not claim the existing
Asian QSP error has disappeared or import the paper's component gain as ours.
