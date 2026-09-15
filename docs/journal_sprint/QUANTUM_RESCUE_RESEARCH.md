# Quantum pricing: research landscape and a defensible contribution

## Executive assessment

The most promising immediate repair is representation-aware reliability, not
adding another fashionable quantum algorithm. The existing pipeline spends
precision on a sinusoidal approximation to the payoff, magnifies amplitude
uncertainty when converting it to dollars, and uses a finite calibration whose
uncertainty can dominate additional pricing shots. A newer estimator cannot
automatically remove those three costs. A useful contribution must explain
which bottleneck dominates, change the responsible component, and demonstrate
the resulting benefit under a consistent target and cost convention.

Two implementations accompany this assessment: an exact finite-grid payoff
oracle and a calibrated Bernoulli confidence-sequence construction. Their
ingredients are established methods. The research opportunity is a rigorously
defined, empirically supported decision framework for when an encoding and
acquisition procedure can deliver a requested dollar tolerance, including when
it should decline. Neither implementation by itself establishes novelty or
quantum advantage. Detailed measured outcomes are in
[the discovery results](RESCUE_RESULTS.md).

The literature through 15 September 2026 contains substantial overlapping work.
In particular, calibrated, noise-aware Bayesian scheduling and end-to-end
financial error accounting already occur together in a recent CVA study.
Simply combining those themes is no longer a convincing distinct contribution.
The narrower opportunity is simultaneous stopping validity, finite calibration
uncertainty, explicit representation error and measured delivery cost, with
strong classical alternatives and negative regimes included.[^1]

This is a broad relevance-filtered field assessment, not an exhaustive review
of all quantum computing or a proof that no competing work exists. Novelty
requires a more targeted priority check once the final claim is fixed.

## Measured outcome of the intervention

In the declared stationary-readout discovery, the exact oracle raised fixed-time
$1 declarations from 0/30 to 30/30 for E014 and E025 under both budget axes.
It reduced direct circuits from 13 to 7 qubits and from 268-272 to 126 logical
CX gates. Three other non-E001 contracts still failed to deliver. The anytime
variant was more conservative, and a subsequent pilot-mixture reanalysis did
not give robust E014 delivery at equal shots. Classical 64-term summation
remains sufficient on every tested contract. These findings establish a repair
to this implementation, not a novel primitive or quantum advantage. Full
denominators, failures, compiler-baseline corrections and limits appear in
[the results record](RESCUE_RESULTS.md).

The pilot follow-up's theoretical guarantee applies to prospective use of the
fixed procedure; its post hoc selection is not automatically covered by that
guarantee on the reused discovery data.

## 1. The research question

The target is a continuous, discounted, risk-neutral expected payoff. It is not
the expected terminal stock price and not merely the probability of measuring
a circuit qubit. If the encoded price is O+S*a and its deterministic discrepancy
from the continuous target is bounded by B, a valid amplitude interval must be
mapped to dollars and enlarged by B. When B is already at least the requested
tolerance, more samples cannot make this particular bound-based declaration
possible. This is a limitation of the representation and certificate, not a
universal lower bound on the pricing problem.

Four different questions must remain separate. Is the encoded mathematical
quantity correct? Does the inference cover that quantity under its observation
model? Can the procedure deliver the requested tolerance at an acceptable cost?
Is it more useful than existing quantum and classical approaches? A positive
answer to an earlier question is not an answer to a later one. This distinction
is particularly important for small vanilla-option instances, where analytic
pricing and finite-grid summation are formidable classical alternatives.

The earlier evidence through week 10 established substantial reproducibility
and diagnostic reliability, but declaration success was concentrated on E001
and paid representation selection did not improve delivery. Those results
remain unchanged. The new experiment is a separately declared intervention,
not an amended version of the earlier controller experiment.

## 2. Amplitude-estimation advances

The September 2026 geometric-schedule work replaces conventional power-of-two
ladders with denser geometric schedules and exact likelihood processing. Its
reported empirical constants are attractive and make it a relevant modern
benchmark. However, its query advantage is not a guarantee about this project's
dollar intervals under finite calibration uncertainty. Changing the schedule
without changing the payoff representation can leave the dominant error
allowance untouched.[^2]

The August 2026 windowed least-squares construction is especially relevant to
depth-limited devices. Its method and theorem address a tunable query/depth
tradeoff and angle-uniform accuracy. Importantly, its even-depth measurements
use a shifted Loschmidt-echo observable, whereas odd depths use the marked
projector. It cannot be reproduced faithfully by sampling only this project's
usual odd Grover sequence and attaching the published theorem to it. Its
measurement model, resource accounting and noise response must be implemented
before a comparison is meaningful.[^3]

Bayesian methods remain useful for proposing measurements and allocating
resources. The recent contrast-aware CVA method models depth-dependent loss,
uses posterior information to schedule depths, and reports a realistic
finite-contrast interpretation rather than a universal runtime advantage.
Its credible intervals must not be silently relabeled as frequentist
confidence sequences. This distinction creates an opportunity for a hybrid
architecture: a flexible scheduler proposes a measurement, while a separate
valid inference layer decides whether precision can be declared.[^1]

Assessment: modern schedules should eventually be tested with the improved
oracle, but they are not the first intervention. They require a faithful native
implementation and a costed observation model. A posterior-driven proposal
can be valuable even when the posterior itself is not used as the coverage
certificate. New asymptotic superiority is not the proposed claim.

## 3. Payoff encoding and circuit synthesis

Quantum signal processing offers a principled route to encoding derivative
payoffs without expensive conventional arithmetic. The derivative-pricing QSP
study reports substantial fault-tolerant resource reductions, but its resource
requirements still involve a demanding logical-computation regime. Its results
are motivation for investigating approximation and oracle cost together, not
evidence that those savings transfer directly to the present small simulator
circuits.[^4]

Piecewise QSVT state preparation addresses amplitudes that admit useful
piecewise-polynomial approximations. This is relevant when structured state
loading becomes the scaling bottleneck. Applying it would require explicit
block encodings, polynomial approximation bounds, success probabilities and
synthesis costs. Loading a classically precomputed vector and labeling it QSVT
would not reproduce that contribution.[^5]

Uniformly controlled rotations provide a much smaller immediate implementation
step. They are established circuit-synthesis tools, not a new discovery.
Recent work continues to optimize uniformly controlled structures, but that
does not make a standard library multiplexer a reproduction of the new
optimization framework.[^6][^7] The prototype uses the established multiplexer
as a transparent finite-grid baseline; it does not claim to implement the
December 2025 synthesis algorithm.

For a grid point x_i, define y_i=max(x_i-K,0)/(U-K). A controlled rotation
Ry(2 asin(sqrt(y_i))) makes the objective probability exactly y_i in ideal
arithmetic. With the same grid probabilities, a=sum_i pi_i*y_i and
P_grid=exp(-rT)*(U-K)*a. The old map has sensitivity
S_old=exp(-rT)*(U-K)*2/(pi*c). Therefore S_exact/S_old=pi*c/2, approximately
0.19635 at c=0.125. This is an algebraic comparison of the two implementations,
not a newly discovered quantum speedup.

The exact map removes the old sinusoidal linearization allowance. Support and
grid error remain. It also moves amplitudes away from the old offset-centered
encoding, so the observed Bernoulli variances change; a precision improvement
must be measured rather than inferred solely from the sensitivity ratio.
Finite rotation synthesis and physical gate noise would introduce additional
allowances beyond this ideal prototype.

The limitation is decisive: the table contains 2^n entries. At n=6 that is 64
angles, and direct classical summation also needs only 64 terms. A successful
table oracle can expose a poor baseline and improve the experiment without
being a scalable algorithm. It should become a baseline that compressed,
piecewise or arithmetic oracles must match, not be advertised as a solution to
high-dimensional quantum data loading.

## 4. Sequential validity and finite calibration

Confidence sequences are intervals valid simultaneously over sample sizes.
Modern concentration and betting literature gives a mature foundation for
constructing them, including likelihood-ratio mixtures and nonnegative
supermartingales. This is established statistics, not a quantum novelty
claim.[^8][^9]

For Bernoulli observations with s successes in n trials, the implementation
uses the Jeffreys beta-mixture likelihood ratio

M_n(q)=B(s+1/2,n-s+1/2)/(B(1/2,1/2)*q^s*(1-q)^(n-s)).

The set M_n(q)<=1/alpha is inverted by bisection around s/n. This resembles a
Bayesian expression but the guarantee is not a posterior-credibility claim:
each fixed-alternative likelihood ratio is a martingale under the null, its
fixed mixture remains nonnegative, and Ville's inequality controls crossing
1/alpha at any time. Boundary q=0 or 1 is handled by the corresponding limiting
supermartingale argument. The associated proof is detailed in
[the mathematical specification](RESCUE_THEORY.md).

For a fixed finite menu of Grover depths, allocate validation failure allowance
across the per-depth processes before observing results. Depths may then be
sampled predictably using past data, provided the conditional Bernoulli response
at each depth remains the same. Keep unobserved depths in the menu with full
intervals. A fixed independent calibration acquisition supplies its own
confidence rectangle. Union-bound the calibration event and all validation
processes, invert every sine branch, and map the resulting set to dollars.

This architecture removes the need to justify repeated stopping with ordinary
fixed-time intervals for the new procedure. It does not retroactively certify
native IQAE or Bayesian implementations. It also does not allow arbitrary
within-depth drift, correlations, data-dependent confidence allocations or
post hoc representation selection. Finite calibration uncertainty and supplied
transfer assumptions still limit precision even as pricing shots increase.

The implementation uses floating-point log-beta calculations and engineering
padding. High-precision comparisons and finite-horizon exact probability checks
test this implementation; they do not constitute directed-rounding proofs.
Nor does a correct martingale proof establish that real hardware satisfies the
assumed response law.

## 5. Integration, variance reduction and alternative problem classes

Quantum quasi-Monte Carlo combines coherent low-discrepancy point preparation
with amplitude estimation. The September 2026 paper explicitly distinguishes
a proposed finite-budget advantage window from an asymptotic improvement over
classical QMC. This distinction matters: replacing plain Monte Carlo with
classical randomized QMC can materially change the benchmark to beat.[^10]

Nonlinear quantum Monte Carlo addresses nested conditional expectations and
related nonlinear functionals. Its multilevel construction is a plausible
longer-term route for genuinely expensive financial expectations. The target
is substantially different from a single-asset, single-date call with a closed
form. Transferring the theorem requires coherent access to the relevant inner
and outer procedures, including their cost and approximation error.[^11]

Market-consistent multi-asset pipelines also already exist. The January 2026
NIG/copula pricing work joins density recovery with quantum integration and
reports query savings. It is relevant to problem realism, but query counts
must not be interpreted as routed-gate or wall-clock savings without the
remaining implementation costs.[^12]

For classical baselines, control variates, randomized QMC and multilevel methods
should be allowed the same model information. A classical control variate
whose mean is known analytically cannot be withheld just to make the quantum
arm look favorable. Conversely, a residual-encoding quantum construction must
pay for evaluating both the original payoff and the control coherently.
Predictable or independently trained coefficients are needed when the
inference guarantee depends on how a control is fitted.

Assessment: a high-dimensional Asian, nested-risk or portfolio problem may
eventually justify a broader experimental target. Changing to one now would
also require new representations, references, inference validation and fair
baselines. The current repair first determines whether the existing failures
are avoidable implementation choices. It does not use a more complicated
application name as a substitute for a demonstrated method.

## 6. PDE, variational and other quantum approaches

A local-volatility pricing algorithm based on the Kolmogorov equation and a
2026 variational imaginary-time approach for lookback options illustrate
genuinely different routes to pricing. The latter explicitly addresses the
jump conditions associated with updating a running maximum. These are not
plug-in replacements for an amplitude estimator: they change the encoded
mathematical object, evolution procedure and readout requirements.[^13][^14]

The 2024 stochastic-volatility pricing study likewise makes the dynamics and
their resource realization central to the algorithmic design. It is a useful
reference for future applications beyond the present closed-form model,
rather than a reason to append stochastic volatility without an executable
cost analysis.[^15]

Quantum neural networks, annealing, QAOA and generic variational optimization
address different optimization or learning tasks. They could propose an
experimental design or approximate a distribution, but would add training,
model-error and validation burdens here. No primary evidence identified in
this assessment makes them a direct repair for the current confidence or
encoding gaps. Classical shadows are attractive for many-observable settings;
this experiment measures one known objective and has not established that a
shadow-measurement overhead buys anything. These families are screened out of
the immediate intervention, not declared useless in general.

Cryptographic algorithms, quantum communication and unrelated Hamiltonian
simulation breakthroughs do not directly change the present pricing oracle or
its dollar error budget. The relevant transfer is an implementable component
with a demonstrated role in this problem, not the general existence of a
powerful quantum algorithm elsewhere.

## 7. Company developments and their limits

IBM's July 2026 account of trusted quantum computation reports demonstrations
in specialized sampling and dynamical-simulation settings, with validation
central to the claims. It motivates independent validation and strong
classical comparison, but is not evidence of advantage in financial pricing.
Its claims must retain their stated tasks and assumptions.[^16]

IBM's mitigation documentation also distinguishes expectation-value Estimator
workflows from Sampler workflows. ZNE, PEC and related techniques have
nontrivial sampling or learning overheads; mitigation settings are not a
universal guarantee of unbiased, narrow pricing intervals. In particular,
an Estimator mitigation feature cannot simply be enabled on this legacy
Sampler path and assumed to preserve the binomial model.[^17]

Google's October 2025 Quantum Echoes announcement concerns verifiable quantum
dynamics and related applications. Its lesson for this project is to specify
exactly what is verified and what classical competitors are used. Its reported
speedup must not be transferred numerically to an unrelated expectation
estimation workload.[^18]

Quantinuum's Helios announcement and August 2026 cloud partnership report
progress in programmable hardware and logical-qubit demonstrations. Official
emulator documentation provides concrete connectivity and noise-model
parameters. These offer possible future experimental platforms, but physical
fidelity, error-detected logical demonstrations and universally fault-tolerant
algorithm execution are different evidence categories.[^19][^20][^21]

Assessment: none of these company developments removes the need to build the
payoff oracle, pay the loading and measurement costs, or justify the confidence
model. No paid hardware job is needed to discover a representation-level
bottleneck. Hardware should enter after a locally validated experiment defines
which mechanism must be measured, including noise-model failure conditions.

## 8. Candidate selection

| Candidate | Gap addressed | Immediate decision | Main disqualifying risk |
| --- | --- | --- | --- |
| Exact finite-grid payoff | Encoding allowance, dollar sensitivity, circuit cost | Implement and compare | Exponential table; exact classical summation remains strong |
| Calibrated confidence sequences | Repeated stopping and predictable depth sampling | Implement with proof and tests | Stationary response and finite calibration assumptions |
| Geometric/WLSAE scheduling | Estimator query/depth efficiency | Next matched benchmark | Different observables or guarantees; implementation costs |
| Contrast-aware Bayesian scheduling | Noisy measurement choice | Relevant competitor/proposal mechanism | Close prior art; posterior width is not a confidence guarantee |
| Piecewise QSP/QSVT | Structured loading and payoff scalability | Follow after baseline repair | Polynomial, block-encoding and synthesis overheads |
| Quantum QMC/multilevel residuals | Harder integration targets | Longer-term application route | Strong classical competitors; coherent oracle requirements |
| Generic mitigation or QML | Hardware noise or learned proposals | Not an immediate claimed solution | Model mismatch, overhead and no demonstrated benefit here |

The first two choices are complementary: one reduces the scale of the
statistical task, while the other makes its stopping rule defensible. There is
no requirement that a promising intervention be recently invented. Recent
literature determines the novelty bar; an older technique can still expose and
repair a consequential weakness in the present implementation.

## 9. Contribution and promotion criteria

A defensible candidate contribution is an encoding-aware reliability decision
framework with an anytime-valid measurement layer. To become more than an
integration exercise, it needs a precise decision criterion and evidence that
the criterion identifies useful and useless regimes. The proposed question is:
under a fixed dollar tolerance and complete logical cost model, which
representations and measurement policies can reliably deliver, and when is
further acquisition unproductive?

For intuition only, under known readout rates with positive contrast c_r,
direct sampling and a Hoeffding bound require
N >= log(2/alpha)/2 * [S/(c_r*(tau-B))]^2 when B<tau.
Multiplying by per-shot gate cost yields a representation-aware conservative
cost score. This follows from standard concentration and affine propagation;
it is not a new complexity theorem. Unknown readout rates, branch ambiguity
and adaptive depth choice require a stronger analysis than this simple score.

The declared experiment isolates representation and stopping effects. It does
not test a new adaptive depth scheduler. Its promotion screen requires improved
descriptive delivery on at least two non-E001 contracts at zero transfer guard
under both resource axes, with zero observed erroneous declarations. Failure
must remain a negative result. Success would justify further development, not
prove a 95% empirical coverage rate from only 30 replications or establish
superiority to other published encodings.

The next genuinely methodological step is to derive and validate a selection
rule that uses bounds, calibration information and compiled costs without
seeing the true price. It must beat a strong fixed improved-oracle baseline,
not just the weaker historical linearized oracle. If it cannot, the correct
paper direction is an explanatory reliability benchmark rather than a
successful-controller claim.

## 10. Evidence needed before a journal claim

The theory should state the complete observation model, permitted adaptation,
confidence allocation and dollar-target mapping. A proof of the new combined
procedure is distinct from a claim that existing native algorithms were
invalid. Formal numerical certification remains a separate requirement if
the manuscript uses language such as certified floating-point enclosures.

The experiment needs matched targets, independent confirmation seeds after
freezing the final algorithm, enough replications to quantify delivery and
failure uncertainty, and strong classical comparators. Circuit resource
profiles should distinguish logical counts from routed native gates,
fault-tolerant resources and hardware time. State preparation, classical table
generation, calibration and failed acquisitions must remain in the ledger.

The novelty review should compare the final specific claim against calibrated
Bayesian AE, time-uniform statistical methods, exact payoff encodings, QSP
pricing, and resource-aware financial pipelines. It should not claim priority
from a broad search that failed to find an identically named algorithm.
Company announcements and promising preprints are research leads, not
independent endorsements of this project's findings.

The project can become stronger without a quantum advantage claim. A convincing
paper may demonstrate why an apparently small encoding choice changes reliable
dollar delivery, identify when calibration or discretization prevents that
improvement, and supply a reusable valid stopping construction. Whether that
is sufficiently novel remains conditional on the completed evidence and
focused comparison. Journal acceptance cannot be promised.

## Sources

Source dates below distinguish initial preprints, later versions and official
announcements where verified. Abstract-level sources support screening only;
their algorithms and proofs have not thereby been reproduced. The focused
methods evidence is strongest for sources 1, 3 and 9; the earlier six-paper
ledger remains separately preserved. No external paper's experiments were
independently rerun for this assessment.

[^1]: Borras Espert et al., [A Noise-Aware Quantum Algorithm for Credit Valuation Adjustments on Real Quantum Hardware](https://arxiv.org/html/2607.12990v1), 14 July 2026. Methods 2.2.1-2.2.2 and interpretation in section 5; focused methods reading, not full proof audit.
[^2]: Farrokh Labib, [Quantum amplitude estimation beyond power-of-two schedules](https://arxiv.org/abs/2609.02715), 2 September 2026. Current abstract/metadata; earlier full reading recorded separately.
[^3]: [Nearly Optimal Amplitude Estimation at any Depth](https://arxiv.org/html/2608.24434v1), 25 August 2026. Measurement model, Algorithm 1 and Theorem 1 inspected; not a complete appendix verification.
[^4]: Nikitas Stamatopoulos and William J. Zeng, [Derivative Pricing using Quantum Signal Processing](https://arxiv.org/abs/2307.14310), initially 26 July 2023. Abstract-level resource screening; guessed v3 HTML unavailable.
[^5]: Oliver O'Brien and Christoph Sunderhauf, [Quantum state preparation via piecewise QSVT](https://quantum-journal.org/papers/q-2025-07-03-1786/), Quantum 9, 1786, 3 July 2025. Publisher abstract.
[^6]: Mottonen et al., [Transformation of quantum states using uniformly controlled rotations](https://arxiv.org/abs/quant-ph/0407010), 1 July 2004. Foundational synthesis reference; implemented through the installed UCRY primitive, tested independently.
[^7]: Chengzhuo Xu et al., [A Unified Framework for Optimizing Uniformly Controlled Structures in Quantum Circuits](https://arxiv.org/abs/2512.08675), v2, 10 December 2025. Abstract-level screening, not implemented.
[^8]: Howard et al., [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240), initial preprint 18 October 2018. Foundational time-uniform framework.
[^9]: Ian Waudby-Smith and Aaditya Ramdas, [Estimating means of bounded random variables by betting](https://arxiv.org/html/2010.09686v7), v7, 25 August 2022. Sections 2-2.1 inspected; the accompanying Bernoulli mixture derivation is explicit in the project specification.
[^10]: Paolo Recchia et al., [Quantum Quasi-Monte Carlo: a window for pre-asymptotic quantum advantage](https://arxiv.org/abs/2609.03625), 3 September 2026. Current abstract/metadata; earlier full reading recorded separately.
[^11]: Jose Blanchet et al., [Quantum speedup of non-linear Monte Carlo problems](https://arxiv.org/abs/2502.05094), v2, 22 October 2025; NeurIPS 2025. Updated title supersedes the initial Non-linear Quantum Monte Carlo title; abstract-level screening.
[^12]: Julien Hok and Alvaro Leitao, [Quantum computing for multidimensional option pricing: End-to-end pipeline](https://arxiv.org/abs/2601.04049), 7 January 2026. Abstract-level screening.
[^13]: [Quantum Algorithm for Local-Volatility Option Pricing via the Kolmogorov Equation](https://arxiv.org/abs/2511.04942), 7 November 2025. Abstract-level alternative-family screening.
[^14]: Florence Paquette et al., [Pricing Lookback Options on a Quantum Computer](https://arxiv.org/abs/2604.00389), 1 April 2026. Abstract-level alternative-family screening.
[^15]: Guoming Wang and Angus Kan, [Option pricing under stochastic volatility on a quantum computer](https://quantum-journal.org/papers/q-2024-10-23-1504/), Quantum 8, 1504, 23 October 2024. Publisher abstract/resource direction.
[^16]: Abhinav Kandala, Ali Javadi-Abhari and Jay Gambetta, IBM, [Researchers demonstrate quantum advantage through trusted quantum computation](https://www.ibm.com/quantum/blog/quantum-advantage), 30 July 2026. Official company account, not an independently reproduced pricing result.
[^17]: IBM, [Configure error mitigation](https://docs.quantum.ibm.com/guides/configure-error-mitigation) and [Error mitigation and suppression techniques](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques), official documentation accessed 15 September 2026. Current-service descriptions, not capabilities assumed available in the legacy environment.
[^18]: Google, [The Quantum Echoes algorithm breakthrough](https://blog.google/innovation-and-ai/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/), 22 October 2025. Official company account; task-specific claim.
[^19]: Quantinuum, [Introducing Helios](https://www.quantinuum.com/blog/introducing-helios-the-most-accurate-quantum-computer-in-the-world), 5 November 2025. Official announcement; marketing superlatives not adopted as comparative findings.
[^20]: Quantinuum, [Quantinuum and Oracle Partner to Accelerate Hybrid Quantum Compute Adoption](https://ir.quantinuum.com/news-releases/news-release-details/quantinuum-and-oracle-partner-accelerate-hybrid-quantum-compute), 11 August 2026. Official partnership/hardware context.
[^21]: Quantinuum, [Helios emulator documentation](https://docs.quantinuum.com/systems/user_guide/emulator_user_guide/emulators/helios_emulators.html), accessed 15 September 2026; displayed emulator configuration dated 18 November 2025. Parameters were not used as measured noise for the local experiment.
