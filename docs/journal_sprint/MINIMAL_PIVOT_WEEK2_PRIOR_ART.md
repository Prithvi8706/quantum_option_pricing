# W2 claim-specific prior-art assessment

Search date2026-09-17. Targeted searches combined Asian/basket option pricing,
block encoding, LCU, centering/reflection, normalization and2025/2026 work.
Only primary research sources support the conclusions below. Search absence
is not proof of originality; this is not exhaustive novelty clearance.

## Direct overlap

[Derivative Pricing using QSP](https://arxiv.org/html/2307.14310v2): reviewed
the construction around equations17-27 and the derivative-pricing application
around29-41. It already replaces explicit exponentiation/payoff arithmetic
with polynomial amplitude transformations, retains garbage registers, and
connects the result to amplitude estimation. Our different separable basket
signal does not make QSP pricing or this pipeline architecture new. A matched
resource comparison requires the same contract, precision and synthesis model;
the published headline reductions cannot be transplanted into our ledger.

[QSVT](https://arxiv.org/abs/1806.01838) and
[qubitization](https://arxiv.org/abs/1610.06546) already supply the underlying
block-encoding/LCU/reflection calculus. W1's identity is an application of that
calculus. The plausible contribution is implementation, certified error/resource
tradeoffs and a decision rule, not a newly discovered quantum primitive.

## Recent proposed advantage: important accounting qualification

[Quantum Quasi-Monte Carlo, September2026](https://arxiv.org/html/2609.03625v1):
reviewed the Sobol mapping, error split, feasibility window and implementation
sections2.2-5.3, particularly equations2.18,4.14,5.10-5.35. Its pre-asymptotic
comparison separates net error from AE error; it does not claim an asymptotic
improvement over classical QMC. Crucially, equation5.27 reports sum k as the
effective query budget, while section5.2 also gives total oracle calls as
Nshots*sum(2k+1). The examples use2048 shots. Their plots therefore cannot
establish our fully charged runtime advantage. The numerical integrands are
small weighted sums, not our lognormal Asian payoff; function loading also
needs scalable arithmetic beyond the prototype lookup implementation.

Our inference: coherent Sobol loading is a possible future encoding experiment,
but replacing the product-normal loader also requires a certified inverse-normal
map, new discrepancy/error analysis for this payoff, and full oracle accounting.
Do not adopt it mid-study or import its advantage claim. Keep it as an untested
alternative, not a positive result of our implementation.

## Other recent pricing work

[Multidimensional pricing pipeline, January2026](https://arxiv.org/html/2601.04049v1):
reviewed the marginal recovery and QAMC sections3.1.3-3.2.2, equations13-29.
It combines recovered marginal distributions with a dependence model and
quantum integration. Its complexity theorem assumes access to the relevant
oracles. That is not evidence that our constructed oracles are cheaper than
conditional RQMC. Distribution recovery is also a different task from our
fixed known GBM, so adding it would expand scope rather than close this gap.

[PDE-based multi-asset pricing, May2026](https://arxiv.org/abs/2605.26610):
abstract screened only. It addresses European pricing PDEs under local/stochastic
volatility with explicit grid-size complexity. It was not reproduced or
formula-audited here. Treat it as a separate research route requiring a larger
pivot, not a drop-in solution for the existing path-average circuit.

## Precision dependence and additional scope checks

The introduction of [Lubinsky's Bernstein-constant paper](https://lubinsky.math.gatech.edu/Research%20papers/BrnstnDec05CA.pdf)
was inspected for the best uniform approximation of absolute value. The
inverse-degree behavior is established approximation theory, not our discovery.
Our method note derives a conditional cost model for combining that behavior
with AE and the present multiplexer implementation; it is not a new lower
bound on all quantum pricing algorithms.

[Hermitian embedding and GQSP for2D Black-Scholes, June2026](https://arxiv.org/abs/2606.00458)
was abstract-screened as another PDE route. It does not supply a validated
drop-in cost improvement for our arithmetic path-average signal, and was not
implemented or claimed as a reproduced advantage here.

## Final assessment

No supported claim of a new fundamental algorithm, global-best encoding or
classical superiority emerges from this targeted review. A practical circuit
construction can still be research, but assembling known primitives and a
small favorable component comparison is insufficient by itself for the user's
desired strong journal claim. Keep the candidate standby pending broader
matched evidence and independent expert novelty review; do not recast the
standby result as journal-ready or rename a literature method as our invention.
