# Where to look for a defensible pricing advantage

Assessment date: 2026-09-15. These are research hypotheses and reading directions,
not demonstrated advantages, exhaustive literature coverage or guaranteed novelty.
The linked abstracts were checked this turn; the broader previous assessment
and its reading-depth distinctions remain in [QUANTUM_RESCUE_RESEARCH.md](QUANTUM_RESCUE_RESEARCH.md).

## Does the current result make the project useless?

No, but it has not achieved the original superiority objective. The code and
validation work are useful infrastructure. A reliable negative result or useful
methods contribution can be valuable, but neither automatically meets a journal's
novelty standard. More experiments around a weak baseline do not solve this.

There are two separate claims to avoid confusing: a literature search did not
establish a new algorithm here; it did NOT prove no undiscovered method exists.
Also, a new algorithm is not mandatory for an application contribution: a carefully
established new regime of benefit could matter. That regime is absent so far.

Our European calls have a Black-Scholes formula, and 64-term classical grid
summation already meets the current dollar tolerances. These are excellent
correctness tests and poor targets for demonstrating practical superiority.
Keep them as regression tests; do not force a favorable conclusion from them.

Distinguish query advantage, fault-tolerant resource crossover and measured
end-to-end runtime advantage. Fewer ideal oracle calls is not automatically
fewer gates, lower cost or faster pricing. Simulated quantum runtime is not
hardware runtime, and noise-free asymptotic scaling is not a NISQ benchmark.

## 1. Multi-asset, path-dependent pricing: closest continuation

My recommendation for an application pivot is an arithmetic Asian basket or
barrier basket with correlated assets, starting with a simple validated model.
Vary assets, monitoring dates and dollar tolerance systematically. More raw
dimensions alone are not evidence of hardness: effective dimension and smoothness
can make classical integration unexpectedly good.

Read [Hok and Leitao, multidimensional pricing (January 2026)](https://arxiv.org/abs/2601.04049).
It studies calibrated marginal distributions, dependence and quantum-accelerated
integration; its reported query benefit is not a measured hardware runtime win.

Question to pursue: after improving classical variance reduction and accounting
for coherent path generation, does any cost crossover survive? Baselines should
include randomized Sobol QMC, Brownian-bridge/PCA constructions where applicable,
control variates, and multilevel methods when discretization is material.
Use identical model, bias target and uncertainty requirement.

Stop or change direction if benefits disappear against those baselines, or if
loading/path-generation complexity erases the query saving. This is an application
change, not implemented as part of the encoding-rule request.

## 2. Nested expectations: stronger theoretical motivation, larger scope change

Examples to investigate include exposure/CVA with genuinely nested conditional
valuations and early-exercise continuation values. First verify that the chosen
formulation cannot remove nesting analytically or through a strong surrogate.
Not every CVA calculation is genuinely an expensive nested problem.

Read [Blanchet et al., Quantum speedup of non-linear Monte Carlo problems (2025)](https://arxiv.org/abs/2502.05094).
The work develops quantum methods for nonlinear functionals, including nested
conditional expectations, with theoretical speedup under its assumptions.

Question: can a financially meaningful instance meet those assumptions with an
efficient coherent inner computation and explicit error propagation? Compare
with classical multilevel nested estimation, regression/surrogate approaches,
and variance reduction. Charge inner and outer work, training/preprocessing and
uncomputation. Do not translate a theorem's oracle model into a hardware claim.

This is probably the most interesting theoretical reading direction, but is
substantially more work than modifying the present European-call circuit.

## 3. Scalable payoff encoding and state preparation: closest methods direction

Read [Stamatopoulos and Zeng, Derivative Pricing using Quantum Signal Processing](https://arxiv.org/abs/2307.14310),
published in Quantum in 2024. It replaces costly payoff arithmetic with QSP and
analyzes fault-tolerant resources. Its advantage estimates require demanding
logical resources, not currently demonstrated local performance.

Question: can a payoff-specific approximation reduce total resources at a fixed
dollar tolerance, including state preparation, polynomial degree, rotation
synthesis and amplitude estimation? The kink at a strike and the distribution
of probability mass make uniform approximation quality and expected-dollar
error different objectives. Turning that observation into a valid bound and
scalable circuit could be worth investigating; novelty must still be checked.

Our current exact table is a small-grid baseline, not the scalable answer: it
enumerates 2^n rotations and a distribution table. A large-n win must avoid
hiding exponential classical preprocessing or quantum loading. Test increasing
n and report total resources, not only objective-rotation gates.

## 4. Quantum quasi-Monte Carlo: investigate the finite regime carefully

Read [Recchia et al., Quantum Quasi-Monte Carlo (September 2026)](https://arxiv.org/abs/2609.03625).
The paper explicitly does not claim asymptotic improvement over classical QMC;
it identifies a possible pre-asymptotic query-benefit window.

Question: does that window remain for a concrete option payoff after coherent
net construction, encoding bias and physical implementation cost? Vary precision
and resolution together, against an optimized classical low-discrepancy baseline.
Showing that the window closes is also informative, but is not a positive
advantage result. Do not equate this with beating plain Monte Carlo alone.

## A practical reading worksheet

For each candidate paper, write down: exact financial task; theorem assumptions;
oracle access and construction; claimed cost metric; strongest classical
comparator; bias/variance accounting; hardware assumptions; and one explicitly
unresolved limitation. Then propose ONE falsifiable extension and a kill criterion.
Search titles and forward citations, and inspect released code/resource tables
before trying to combine algorithms. These suggestions are hypotheses inferred
from the sources, not author-endorsed open problems or claims of priority.

My suggested order: build the strongest classical Asian/basket benchmark first;
study scalable payoff/loading methods in parallel; then decide whether a nested
problem is justified. Continue the [encoding-aware rule](ENCODING_DECISION_RULE.md)
as a resource/error accounting layer, not as evidence of superiority itself.
