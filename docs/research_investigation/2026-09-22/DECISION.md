# Significant quantum advantage investigation

Search date: **22 September 2026**. Primary-source search emphasized
22 September 2024 onward, especially 22 March–22 September 2026, and followed
foundational work where necessary. This is a selective research investigation,
not exhaustive literature or priority clearance. Manuscript and historical
archives are unchanged. Local baseline at inspection: `800ea15b` (PR #9 merge).

## Decision and evidence standard

**No defensible significant quantum advantage established yet.** There is no
demonstrated hardware advantage, and no completed, credible fault-tolerant
runtime crossover against strong classical methods for this project.

The primary next hypothesis is **variance-sensitive quantum multilevel pricing
using a coherently evaluated antithetic fine/swapped-fine/coarse correction for
correlated stochastic-volatility Asian baskets**. Its possible benefit comes
from avoiding Lévy-area simulation while preserving small correction variance.
It is a direct-pricing continuation. It is not the old suggestion to add assets,
nor simply weak Euler plus amplitude estimation. A specific 2026 source leaves
this quantum use of classical antithetic coupling unresolved. That is a reason
to investigate, not evidence of novelty or practical advantage.

The fallback is a **one-decision compound Asian-basket call**, using nonlinear
quantum Monte Carlo only if classical conditional integration, multilevel
estimators and surrogate-based value bounds fail to make it cheap. This changes
the contract but remains direct option pricing. CVA, exposure and nonlinear risk
are larger scope changes and are not the fallback recommended here.

Use these distinct evidence levels throughout:

| Level | Meaning | Finding here |
|---|---|---|
| 1 | Demonstrated complete hardware advantage at matched financial accuracy/confidence | None |
| 2 | Complete conditional fault-tolerant crossover with explicit architecture/resources | None yet; target of a successful new investigation |
| 3 | Algorithm/query advantage under specified access and regularity assumptions | Established generic mean/multilevel/nested results; not a lower bound for these structured financial instances |
| 4 | Improvement over a specified quantum implementation | Current manuscript and weak-versus-strong Euler circuit comparison |

**Prospective acceptance contract, fixed before any confirmation:** one classical
discounted continuous-model price for a discretely monitored Asian basket,
absolute error $0.10, $0.03 or $0.01 per initial basket value $100, at least 99%
success probability. Monitoring dates are contractual; internal SDE refinement
does not alter the contract. Relative error is not substituted for absolute
error. The 99% guarantee is **per delivered price**, not simultaneous coverage
of the 72 case/tolerance outputs in the confirmation study. A separately
claimed portfolio/vector contract must allocate failure across all its outputs
and charge the resulting extra work on both sides. The primary practical
criterion is **10-fold lower complete latency**,
including non-amortized setup, against the fastest eligible classical method.
Tenfold is an engineering margin against implementation/model uncertainty, not
a p-value. Require at least 20 of 24 frozen held-out cases to meet it at each
claimed tolerance, at least 3-fold on every case, and all accuracy contracts to
hold. Report every asset/date stratum. Any smaller favorable region needs a new
confirmation set, not retrospective selection.

Report classical CPU/GPU, quantum physical qubits and qubit-seconds separately;
latency advantage is not monetary or energy advantage. For the qualifying
prospective scenario impose a research planning ceiling of 10 million physical
qubits and 60 seconds per price. These are declared practicality screens, not
predictions of availability or user procurement requirements. Also publish
uncapped break-even surfaces so this choice cannot hide a result. Repeated
pricing is a separate workload with fixed output counts, equal amortization,
and simultaneous error accounting. All current pilot cases are development.

## Project diagnosis from the repository

Read the requested manuscript, common-compilation results, directions and
rescue assessment; the September 21 project-state/comparator/prior-art/publication
records; current classical source; current common-compilation archive and
historical classical timings. No newer manuscript or scientific release was
found. The old directions document partly refers to European-call work; the
September 22 Asian-basket manuscript is authoritative for the current target.

The present model has only one or two assets and two dates. Its $1 tolerance is
loose relative to the accuracy achievable classically. Matching the degree-four
control changes the ranking of the selected quantum routes; it does not make
the integration difficult. Common-policy control-cancelled CX totals are
36,477,214,772 for D1 reflection and 375,312,500,844 for D2 residual arithmetic.
The D2 reflection/residual ratio is 3.1289554633, with 103 versus 5,162 allocated
logical wires. These are ideal decomposition counts, not T counts or depth.
There is no legitimate direct conversion from them to hardware seconds.
[Authoritative common-policy record](../../release/COMMON_COMPILATION_RESULTS_20260922.md).

Reusable assets: directed price-error ledgers; continuous/finite-law bridges;
signed fixed-point arithmetic and overflow checks; clean-workspace and inverse
accounting; independently fitted classical controls; PCA and conditional RQMC;
complete-menu provenance and all-label decoder checks. Preserve D1/D2 and old
E cases as regression/history; none are fresh confirmation. The new task needs
new SDE/coupling and variance-sensitive estimation modules, not a relabeling of
the reflection/QSP comparison.

Fundamental obstacles are the classical accessibility of the integrand, strong
dimension reduction/smoothing, full coherent-oracle cost, and the need to return
a classical price. Query lower bounds for arbitrary black-box functions do not
prove that a known Asian payoff is hard. These obstacles persist under better
compilation. Implementation limitations include the unoptimized U/CX policy,
large arithmetic workspace, canonical dyadic AE/17 repetitions, conservative
range normalization, finite-law preparation and absent Clifford+T/physical
schedules. Those choices can improve, but no measured improvement currently
closes the classical gap. A shifted signed Bernoulli encoder generally uses a
range bound; it does not automatically exploit the small variance of a
multilevel correction.

## Screening table

Detailed reading depths, exact sections and venue/material searches are in
[QqMC/classical review](qqmc_review.md), [nonlinear review](nonlinear_review.md)
and [stochastic-volatility/hardware review](stochvol_hardware_review.md).
“Full” means main text and relevant appendices read, not formal proof checking
or independent reproduction. “Focused” means specified methods/proofs inspected.

| Source / date / status / depth | Mechanism and financial fit | Strong classical competition; hidden costs/failure mode | Evidence, burden, novelty opportunity, decision |
|---|---|---|---|
| [Herman et al.](https://arxiv.org/html/2602.03725v1), 3 Feb 2026 preprint; focused §§4–8 and relevant loading/discretization passages | Fast-forwarded CIR/restricted Heston; quantum Milstein sampling; §7.1 explicitly leaves antithetic use open | Exact/QE simulation, conditional RQMC, antithetic MLMC. Restricted correlations, lower-tail/derivative bounds and high-degree polynomial constants; no measured FT crossover | L3 against stated MC/MLMC, not all structured classical algorithms. High burden. **Investigate antithetic gap**, not already-published fast-forward theorem as novelty |
| [Giles–Szpruch](https://arxiv.org/pdf/1202.6283), Annals Applied Probability 2014; focused §§2–6 and proofs supporting §5.2 | Fine/swapped-fine average cancels leading path errors without Lévy areas; includes discrete Asian averages | Give same correction to classical MLMC/MLRQMC. Smooth coefficient and strike-neighborhood assumptions; Heston boundary not covered automatically | Classical foundation. Medium classical/high coherent burden. **Primary ingredient**, not new variance-reduction principle |
| [An et al.](https://arxiv.org/pdf/2012.06283), Quantum 2021; Theorem 2/proof, §4, Appendix A inspected | Variance-sensitive multilevel estimation converts correction variance into quantum complexity | Classical MLMC plus stronger QMC; query/sample cost is not a gate-free resource | L3 under access/rate conditions. Generic composition already known. **Use with explicit constants** |
| [Wang–Kan](https://arxiv.org/html/2312.15871v3), Quantum 23 Oct 2024; full main text/resources/appendices | Weak Euler uses signs instead of Gaussian state preparation for Heston Asians/barriers | Conditional controlled RQMC/MLMC; SDE bias, payoff cap, serial arithmetic, many qubits | L4 circuit improvement; conditional resource benchmark, no strong-classical crossover established. **Retain benchmark; reject unchanged route** |
| [Recchia et al. QqMC](https://arxiv.org/html/2609.03625v1), 3 Sep 2026 preprint; full | Coherent digital net plus AE; compatible input construction | Conditional/CAS RQMC and exact integration of numerical toy family; full shots, oracle loading, net bias | Conditional upper-bound/query comparison. High financial-oracle burden. **Background**, not primary advantage claim |
| [Blanchet et al.](https://arxiv.org/pdf/2502.05094), NeurIPS 2025, v2 22 Oct; full | Quantum-inside-quantum hierarchy for nonlinear expectations | Antithetic nested MLMC, ML-RQMC, kernel quadrature, regression. Uniform conditional moments and coherent inner routines | L3 generic oracle result; compound-call application already present. High burden. **Fallback investigation** |
| [Sun et al.](https://arxiv.org/abs/2602.08120), 8 Feb 2026 v1; ICML 2026 listed poster; full accessible v1, final inaccessible | Repeated nesting/optimal stopping | READ, LSMC/dual bounds; depth-dependent constants, coherent recursion | L3; repeated-nesting extension occupied. **Background**, inspect final/correct base convention before code |
| [Li et al. SPDE/BDSDE](https://arxiv.org/abs/2606.31076), 30 Jun 2026 preprint; focused, not full proof audit | Forward/backward schemes, nested QA-MLMC, Greeks | Classical MLMC/BSDE/PDE, tower-property simplification; reversible update oracles, smoothness/localization | L3 claims; no compiled pricing crossover. Large change. **Background/prior art** |
| [Guseynov et al. PDE](https://arxiv.org/html/2605.26610v1), 26 May 2026 preprint; focused §§III–IV, Appendices E–H | Grid evolution and extraction of selected European prices | Sparse/PDE/low-rank and pathwise RQMC/MLMC; norms, postselection, boundary approximations and extraction | Grid-based comparison, not all-classical advantage. High burden. **Reject as primary** |
| [Forward Kolmogorov pricing](https://arxiv.org/html/2511.04942v1), 7 Nov 2025 preprint; focused extraction/complexity screen | Forward density and payoff overlap rather than one backward-state amplitude | Classical expectation algorithms; density amplitude versus square-root distribution, overlap normalization, state preparation | Conditional algorithmic claims. **Background**, no resolved Asian full-path loading mechanism |
| [Erle–Koczor](https://arxiv.org/html/2608.24434v1), 25 Aug 2026 preprint; Theorem 1/Alg.1 and depth tradeoff inspected | Tunable AE depth/repetitions, no controlled Grover | Full runtime classical competition; reducing depth increases repetitions, angle-to-dollar conversion required | L3 estimation tradeoff/L4 candidate implementation gain. Medium burden. **Benchmark component only** |
| [Kothari–O'Donnell](https://arxiv.org/pdf/2208.07544), [SODA 16 Jan 2023](https://doi.org/10.1137/1.9781611977554.ch44); Theorems 1.1/1.3 and reductions inspected | Digital real-valued variance-sensitive mean, O(sigma/epsilon) source uses | Same residual/classical controls; reflections, quantile/phase routines and reversible code cost | L3 generic source-access result. High implementation burden. **Primary estimator candidate**, no constants assumed free |
| [Piecewise QSVT preparation](https://quantum-journal.org/papers/q-2025-07-03-1786/), Quantum July 2025; publisher/previous project screen | Structured smooth state loading | Analytic samplers and efficient classical evaluation; block-encoding and synthesis costs | Component L4 relevance. **Background**, pursue only if loader dominates measured total |
| [Hok–Leitao pipeline](https://arxiv.org/abs/2601.04049), Jan 2026 preprint; prior full-method review rechecked against abstract | Calibrated NIG/copula quantum integration | Fourier/COS/RQMC and paid calibration; oracle access not a classical sample | L3-style query comparison. **Background**, realism alone does not supply advantage |
| [Han et al. multi-option/CVA](https://doi.org/10.1080/14697688.2026.2614573), Quantitative Finance 2026; §5 access/output screen | Aggregate portfolio expectation with matrix/sample access | Shared paths, strike sorting, surrogates; loading all valuations; aggregate differs from every price | L3. High burden. **Background**; CVA is a larger pivot |
| [Chen et al. nested kernel quadrature](https://proceedings.mlr.press/v267/chen25av.html), ICML 2025; methods + relevant appendices | Structure can remove nested MC exponent | Training/kernel solve costs and smoothness at kink | **Required fallback classical challenger** |
| [Liu CAS](https://doi.org/10.1137/23M1548918), SIAM SISC 2024; financial methods/experiments | Conditional integration + active directions | Root-solving and training charged | **Required direct-pricing classical challenger** |
| [Chen et al. RQMC-IS](https://arxiv.org/html/2510.06705v2), v2 Dec 2025; 2026 journal assignment; §§4/5.2 read | Preintegration, importance sampling and effective-dimension reduction in Heston examples | Growth/positivity assumptions; not universal | **Required challenger**, especially against payoff kinks/tails |
| [Custers et al.](https://arxiv.org/html/2609.07169v1), 7 Sep 2026 preprint; §5.1/Table 6 read | Semi-closed geometric-Asian controls for arithmetic Asians under Volterra-Heston | Control evaluation/mean accuracy and multi-asset generalization must be charged | **Required control competitor**; single-asset result is not automatically a basket formula |
| [RQMC confidence](https://arxiv.org/html/2504.18677v2), Information and Inference 6 Mar 2026; confidence methods read | Betting/empirical-Bernstein intervals for bounded independent scramble means | Known range, tail and numerical allowances | **Use**; rigorous classical confidence cannot be excluded on grounds that current t intervals are empirical |
| [Case RQMC slopes](https://arxiv.org/html/2502.17731v2), 16 Sep 2026 revision; financial/rate sections read | Finite-window slope uncertainty, Asian preintegration | Shared bias invisible to scramble variance; timing exclusions | **Use diagnostic**, not asymptotic law |
| [Tensor-network grid pricing](https://arxiv.org/abs/2601.00009), Jan 2026 preprint; abstract only; [Fourier-RQMC](https://arxiv.org/abs/2403.02832), updated 2026, abstract only | Low-rank/grid and Fourier alternatives for multi-asset outputs | Rank/transform assumptions, setup and outputs | **Classical screen when structure fits**; no unverified rates imported |

Official QCE 2025 accepted papers/proceedings support the project's loading and
arithmetic prior art. The QCE 2026 finance workshop, technical program, poster,
tutorial and recording/materials access were screened; some materials were
restricted. Official QIP/TQC/STOC/FOCS/SODA and NeurIPS/ICML records were also
searched. Accepted talks, listed posters, preprints and proceedings are distinct
in the reading files. The STOC/QIP Hermite transform is a possible loading
component, not a finance result. No inaccessible talk or press release was
treated as proof. No external paper's full quantum experiment was reproduced.

## Ranked shortlist and why the ranking changes

| Rank | Opportunity | Plausible advantage / evidence | Relevance / novelty / effort / decisive evidence |
|---|---|---|---|
| 1 | Coherent antithetic variance-sensitive MLMC for correlated stochastic-volatility Asian baskets | Possible precision exponent improvement over MC/MLMC; RQMC may eliminate it. No level-2 evidence | Direct continuation; explicit open implementation question, but combination may be routine. High proof/circuit burden; one week to reject feasibility |
| 2 | One-decision compound Asian-basket via nonlinear quantum MC | Strong generic level-3 theorem; classical nesting can disappear | Direct specialized option, occupied broad theory. High burden; one week for classical bracket/resource screen |
| 3 | Coherent Sobol/QqMC for current or larger GBM Asian basket | Weakest case against strong classical integration; toy evidence insufficient | Closest code fit; weak new claim; a day can reject unchanged route |

Fast-forwarded restricted Heston is a comparator to rank 1, not an independently
new paper direction. Generic quantum PDE, variational pricing and larger
portfolios do not currently outrank these. A multi-strike price vector costs
more than an aggregate price. Classical paths, Fourier coefficients and fitted
surfaces amortize too. For Greeks compare AAD/pathwise/likelihood-ratio and
smoothed finite differences; for calibration compare COS/Fourier plus gradients
and offline surrogates. No free quantum training or full-vector readout is
assumed. Discontinuities introduce both classical smoothing opportunities and
quantum approximation/normalization costs.

## Primary hypothesis: what must be new and what must work

For a level-l path on a fine time grid, a second path with each adjacent pair
of Brownian vector increments swapped, and a coarse path using their sums,
define dollar-discounted corrections

    Y_0 = P_0,
    Y_l = (P_l(fine) + P_l(swapped))/2 - P_(l-1)(coarse).

The two fine paths have the same marginal law. Thus expectation telescopes to
the finest discretized price. Reversibly compute all three payoffs from the
same increment registers, perform signed addition/subtraction, estimate that
digital real-valued random variable, and uncompute. Selecting a random quantum
branch between the fine paths generally loses the pathwise cancellation.
Simply computing a shifted Bernoulli amplitude does not establish
variance-sensitive query demand.

The new evidence for reopening multilevel is specific: [Herman §7.1](https://arxiv.org/html/2602.03725v1#S7.SS1)
does not incorporate this antithetic approach. Existing [classical theory](https://arxiv.org/pdf/1202.6283)
and the [generic quantum theorem](https://arxiv.org/pdf/2012.06283) suggest a
composable route. Targeted title/citation/phrase searches did not locate the
exact complete construction; that does not establish first publication.

**Hypothesis:** for 2–8 correlated Heston assets with 12–52 contractual Asian
monitoring dates, maturities 1–2 years and the declared accuracy/confidence
contract, coherently computed antithetic corrections with a variance-sensitive
mean estimator achieve at least 10-fold lower total fault-tolerant latency than
the fastest validated conditional-control RQMC/MLRQMC/MLMC or other applicable
classical method, within the declared hardware ceiling, provided certified
coupling, truncation and arithmetic errors preserve the measured variance
decay and a compiled architecture meets the derived oracle-time budget.

This is a hypothesis about a prospective level-2 result. It is not an established
level-3 theorem for Heston. Its main falsifiers are classical slopes/constants
that match or beat quantum cost, a variance floor from coherent arithmetic,
failure to certify Heston boundary/tail bias, a coarse-level cost bottleneck, or
insufficient factory/latency/qubit resources. An isolated easier smooth model
can validate code; it cannot substitute for the stated financial target.

Let weak bias be O(h^alpha), correction variance O(h^beta), and complete
coherent sample cost O(h^-gamma), ignoring only explicitly tracked logarithms.
The generic allocation gives precision cost approximately

    epsilon^-1                       if beta > 2 gamma,
    epsilon^-1 log(epsilon^-1)^2      if beta = 2 gamma,
    epsilon^[-1-(gamma-beta/2)/alpha]  if beta < 2 gamma.

Also charge one-or-more-sample floors and theorem polylogarithms. Under
alpha=gamma=1, beta approximately 1.5 gives an exponent approximately 1.25;
beta=2 gives approximately 1. These are conditional deductions. Classical
antithetic MLMC already has exponent 2 when beta>gamma. If the *whole classical
algorithm* delivers error proportional to work^-r with r>=0.8, the beta=1.5
quantum candidate has no favorable precision exponent. At r near 1 it faces
both an exponent and constant problem. Measure whole-algorithm work, not just
one level's path count, before making this comparison.

The smooth-case beta=2 result must not be borrowed for an unsmoothed call.
Giles–Szpruch §5.2 includes discrete weighted Asian averages, with a
strike-neighborhood probability condition giving roughly beta=1.5-minus for
piecewise-smooth payoffs. Their coefficient assumptions fail for sqrt(v) near
zero. Feller positivity does not bound all inverse moments/derivatives.
[Pang–Wang](https://arxiv.org/pdf/2305.12992) broadens other coefficient classes,
but Assumption 3.2 still requires differentiability and polynomial bounds; its
3/2-Heston experiment is not a proof for square-root Heston. Localization needs
an expected-payoff error bound and its constants can remove the benefit.

Gaussian coupling is deliberate. Naive coarse Rademacher increments do not
equal sums of the fine sign increments, so weak Euler's cheap Hadamards cannot
be combined automatically with the standard multilevel rate theorem. Classical
weak/random-bit multilevel methods are relevant alternatives, but require their
own distribution hierarchy, coherent preparation and bias analysis.

There is a second coupling obligation: independently prepared, truncated
fixed-point Gaussians are not exactly closed under addition. The coarse law
inside Y_l must equal the fine law used for Y_(l-1), or the mismatch must receive
an explicit price-error allowance. A hierarchical finite law or a coupled
quantization construction must preserve both telescoping and small variance
without an exponential table. This cannot be settled by the floating-point
Gaussian development experiment.

Potential contribution: a certified finite-precision coupled oracle, proof that
its variance/error survives reversible implementation, and a robust measured
classical versus conditional physical crossover. Merely writing this correction
into a quantum register and invoking a generic theorem is likely insufficient
novelty. A correction to a literature implementation gap may be worthwhile
without satisfying the user's advantage criterion. Keep those outcomes separate.

### Fallback hypothesis and falsification

At an intermediate date tau=T/2, define the underlying option value
`C_tau = E[exp(-r*(T-tau))*(A_T-K)+ | F_tau]`, where A_T is the contractual
arithmetic basket average, including its already observed fixings. The
compound option price is `exp(-r*tau)*E[(C_tau-K_compound)+]`. Its state must
include spots, variances and the running average; it is a direct compound
option, not CVA or an artificially nested rewrite of a linear expectation.

**Fallback hypothesis:** on 2--8 asset stochastic-volatility compound Asians,
12--52 dates, T=1--2 and compound strikes $3/$6/$9, the nonlinear quantum
estimator supplies a price within $0.03/$0.01 at per-price 99% confidence at
least 10 times faster than the best paid conditional quadrature, antithetic
nested MLMC/MLRQMC, kernel quadrature or regression/value-bound method, within
the same physical planning ceiling. This depends on certified conditional
moments/tails and on a compiled coherent inner estimator, including median or
confidence amplification and inverse costs. A fallback activation requires its
own frozen 24-case confirmation allocation; it cannot inherit the primary
Asian results.

The broad nonlinear quantum theorem and a compound-call application already
exist in Blanchet et al., so neither is our novelty. The prospective contribution
would be a new end-to-end certified crossover for this financially distinct
contract, if it exists. The nine executed single-asset checks show why the
first falsifier is classical simplification: one-dimensional quadrature took
2.9--5.5 ms. For the basket case, train on disjoint data and compute lower and
upper continuation-value bounds; a bracket narrower than the error budget at
less than the quantum latency allowance rejects the direction. Also reject if
kernel/conditional methods match the precision exponent or the coherent inner
routine exceeds the full budget. See [full fallback review](nonlinear_review.md)
for the occupied prior art, uniform-moment assumptions and code-level caveat in
the accessible repeated-nesting preprint.

## Complete cost and break-even calculation

Use seconds throughout. Let c_Q,l be the duration of one complete coherent
correction invocation under an explicit schedule, including its inverse as
required by the invocation convention; let k_l contain actual estimator and
confidence constants. Set a_l = k_l c_Q,l sigma_l, with sigma_l in dollars.
For error allocations e_l summing to e_stat, an illustrative variance-sensitive
model is

    T_Q = S_Q + sum_l a_l/e_l + T_floor + T_measure_decode,
    e_l = e_stat sqrt(a_l)/sum_j sqrt(a_j),
    T_Q = S_Q + (sum_l sqrt(a_l))^2/e_stat + T_floor + T_measure_decode.

This is an allocation model, not a substitute for a concrete estimator's
integer calls and logarithms. Empirical sigmas are diagnostics; the final
algorithm needs valid variance information or an estimator that obtains it
with charged work. A useful classical MC allocation diagnostic is

    T_MLMC ~= S_C + z^2 [sum_l sigma_l sqrt(c_C,l)]^2/e_stat^2.

Here z is a Gaussian confidence diagnostic only; rigorous classical intervals
need their actual schedule/bounds. Replace T_MLMC by the *minimum validated
full cost* over classical finalists, including RQMC, when deciding advantage.
The universal practical test for the chosen implementation is

    T_Q <= T_C_best / 10.

A [reproducible sensitivity calculation](antithetic_resource_sensitivity.md)
uses the executed uncontrolled level variances, with an expressly uncompiled
oracle model `c_Q,l=c_0*w_l`, `w_0=1`, `w_l=2.5*2^l` for l=1,...,5. The weights
count two fine paths plus one coarse path relative to the 12-step base; they
do not establish an actual loading/arithmetic/scheduling cost. With common
estimator constant k, define `B=(sum_l sqrt(w_l*sqrt(V_l)))^2`, so the allocation
model becomes `T_Q approximately k*c_0*B/e_stat` before extra overhead.
Measured B values are 50.3255 (one asset) and 28.7225 (four assets), including
the independently measured base variances. At epsilon=$0.01, e_stat=$0.0045,
and a hypothetical classical delivery time of 1 second, a 10x win with k=10
permits c_0 at most 0.894 or 1.567 microseconds respectively. These are complete
base-oracle duration coordinates, not per-gate times. They scale linearly with
classical time and inversely with k; the artifact includes 0.1/1/10-second and
k=1/10/100 cases. No value of k or oracle duration has been validated. Controls
can change both sides, finite-law errors can change variances, and all estimator
logarithms, sample floors and physical overhead remain due. This exposes the
small permissible budget; it establishes neither feasibility nor impossibility.

If quantum resources total D_T serial T-layers and N_T magic states, a necessary
runtime bound under specified scheduling is

    T_Q >= S_Q + max(D_T tau_layer, N_T/R_factory, D_C tau_Clifford)
                  + T_measure_decode.

Routing, feed-forward and competing factory dependencies may make the bound
strict. No sum of individually favorable lower bounds is a complete schedule.
Physical accounting must provide logical widths, peak live memory, code family
and distance, physical gate/readout error and cycle times, routing, factory
count/area/output rate, and decoder throughput. Enforce, conservatively,

    N_locations p_logical + N_T p_bad_magic + p_other <= delta_physical.

Then physical qubits are data/ancilla/routing blocks plus factories, not the
logical width. None of these quantities are established for the new oracle.
The scenarios below therefore do not constitute level 2.

The published weak-Euler Asian example has approximately 1.2e11 T-depth,
2.4e11 T gates and 22,000 logical qubits. Its normalized finite-target error
0.0013, cap 200 and discount exp(-.03) correspond to about $0.2523, before a
continuous-model bias/tail bridge; success is 90%, not our new 99% contract.
[Wang–Kan §§5–6, Tables 5–6 and footnote 8](https://arxiv.org/html/2312.15871v3).

| Hypothetical effective T-layer time | Depth-only runtime | Classical time required for a 10x quantum win |
|---:|---:|---:|
| 0.1 microsecond | 12,000 seconds | 120,000 seconds |
| 1 microsecond | 120,000 seconds | 1,200,000 seconds |
| 10 microseconds | 1,200,000 seconds | 12,000,000 seconds |

These effective logical-layer times are sensitivity coordinates, not verified
vendor capabilities. They omit extra physical costs and favor the old quantum
implementation. In our bounded capped-discrete classical run, a conservative
Hoeffding statistical radius $0.25 at 95% required 45.25 seconds. Even at 100 ns,
the old depth is over 265 times slower; a 10x quantum win at that classical
budget would require over 2,650-fold depth reduction. This is a rejection
screen for that resource estimate, not a certified comparison of continuous
prices or a lower bound on future algorithms. Increasing confidence/tightening
the physical error ledger will not rescue the unchanged resource count.

## Executed checks, not proposed results

[Execution protocol](EXECUTION_PROTOCOL.md) and all scripts/results are retained.
No paid hardware, quantum device, complete fault-tolerant compilation, or
external full experiment was run.

| Executed workload | Result | Interpretation and limit |
|---|---|---|
| D1 existing PCA-RQMC + independent geometric control, 16 x 4096 paths | price 10.20720695; empirical 95% half-width $0.0001147; setup+fit+evaluation 0.1022 s | Continuous Gaussian target; t interval is empirical. Independent 1D conditioning quadrature gave 10.20718937 in 0.0130 s, numerical error estimate only |
| D2 same method | price 5.41185710; empirical half-width $0.0003674; 0.1004 s | Ordinary optimized classical structure already defeats a useful D1/D2 advantage narrative; not matched rigorous physical race |
| Exploratory 8 assets x 52 dates, sigma .3, correlation .4, K100 | price 5.52194891; empirical half-width $0.0004719; 7.2813 s | 416 nominal factors are not evidence of hardness; no independent truth/coverage assertion |
| Wang–Kan weak 256-step capped Heston target, 16 scrambled sets with antithetic paths | price 13.91778; empirical half-width $0.01286; 4.715 s | Not conditional-QMC/geometric-control state of the art; finite weak model only |
| Same capped weak model, fixed Hoeffding acquisition | price 13.92462472 +/- $0.249999985; 1,111,698 independent antithetic pairs; 45.2488 s | Nonasymptotic statistical bound under iid/exact-evaluation assumptions; floating error and continuous bridge not certified |
| Cap diagnostic in that acquisition | Four raw payoffs exceeded 200; maximum 213.1019 | A sampled maximum cannot certify an uncapped expectation. No inference about total tail price from four observations |
| Nine single-asset Black–Scholes compound-call cases | 2.9–5.5 ms via one Gaussian quadrature | Financial nesting can collapse; numerical quadrature errors, not interval certificates |
| QqMC toy/query sanity checks | Linear integrals exactly computable; complete listed-schedule oracle accounting exceeds 4096 times plotted effective queries | Independent arithmetic checks, not reproduction of quantum experiments |
| Antithetic log-Heston, 1 asset/12 dates, five refinement levels | Plain variance exponent 0.966; antithetic 1.965 +/- 0.082; finest variance reduction 571.5x | Eight batches of 2,048 paths per level; descriptive 95% slope interval, not asymptotic theorem |
| Same construction, 4 assets/12 dates | Plain exponent 0.980; antithetic 1.973 +/- 0.074; finest reduction 603.3x | Complete correction pilot 9.70 s; classical MLMC receives exactly the same benefit |

Full GBM results:
[`classical_screen.json`](../../../results/advantage_investigation_20260922/classical_screen.json),
[script](../../../research/advantage_investigation_20260922/classical_screen.py).
Heston results: [empirical pilot](heston_discrete_pilot_results.json),
[Hoeffding pilot](heston_hoeffding_pilot_results.json). Timings are local
single-process CPU measurements with setup/fitting charged as documented;
Python import/interpreter startup is excluded. No simulator timing is treated
as quantum hardware timing. These calculations were selected for diagnosis;
none becomes a held-out confirmation case.

The [antithetic protocol and results](antithetic_logheston_pilot.md) implement a
drift-implicit Milstein update for variance and a log-price Milstein update,
without Levy-area variables, with complete Brownian vectors swapped. The
contract retains 12 monitoring dates while numerical steps refine from 12 to
384. These development parameters have Feller ratio 4, so they are benign
interior cases. Empirical beta near 2 does not replace the roughly 1.5-minus
piecewise-smooth theorem, nor establish that theorem for square-root Heston.
The four-asset finest correction mean is -$0.00015555 +/- $0.00005118: small
variance is not a bound on remaining bias. Independent base-level sample
variances are 135.584 and 63.0278 squared dollars, much larger than correction
variances. Base-level controls and the full estimator may dominate the quantum
cost. A largest-shape memory check used 0.0711 GiB. Raw seeds, all batches,
timing partitions, source hashes and the deterministic-variance coupling check
are retained. No continuous-model accuracy certificate follows from this pilot.

## Classical competition and output/error contract

Implement the strongest classical arm first: conditional/GPCA or CAS scrambled
Sobol with geometric-Asian and martingale/low-order controls, then antithetic
MLMC and multilevel RQMC with the identical coupling and useful controls. Use
QE-M or a validated positivity-preserving Heston scheme as an independent
reference; validate single-asset European marginals with Fourier/COS and Asian
geometric transforms where applicable. Price the actual fixed monitoring dates.
The proposed cross-correlated variance processes are more general than the
single-asset affine setting of the new geometric-Asian formula; do not assume
that formula is an exact basket control mean. Use valid analytic controls,
martingale controls or independently computed means with their error and cost
charged. Any tractability gained by simplifying correlations belongs to both
competitors and changes the model declaration.
Richardson extrapolation or doubling agreement alone is not a bias certificate.

Adaptive quadrature/PDE should win low-dimensional validation cases; retain
them. Fourier methods apply where required transforms/payoffs are tractable,
not automatically to a general correlated arithmetic path functional. Screen
sparse grids/low-rank tensors on measured effective dimension/rank, and use
batched CPU/GPU implementations. LSMC/dual bounds are not necessary for an
ordinary Asian call, but become compulsory for the fallback/early exercise.
Importance sampling is compulsory if a putative advantage relies on rare tails.
Learned controls/surrogates get identical training information and paid training
on both sides. The value of a control mean includes its reference uncertainty.

Two ledgers must remain separate. Development can use empirical RQMC t intervals
and independent reference agreement. Final level-2 comparison requires a common
financial output guarantee: tail/localization + SDE + input quantization +
arithmetic + payoff/synthesis/loading + control offset + statistical error <=
epsilon. Use a planning allocation 10%, 20%, 5%, 10%, 5%, 5%, 45% respectively;
rebalance only during development and freeze before confirmation. Every term
must be applicable and measured/bounded, not filled with zero by omission.
Quantum statistical and physical failure budgets are each at most .005;
classical statistics may use .01 because there is no quantum execution failure.
Reference uncertainty, additionally, must be <=epsilon/10 and reported separately.
It is a validation allowance, not an extra permitted pricing error. When
checking against a reference interval of radius b_ref, require the candidate's
deviation plus b_ref to fit epsilon; overlapping intervals alone do not pass.
For the 72-output validation panel allocate reference failure at most
0.001/72 per output (union budget 0.001), separately from each method's per-price
contract. If two reference intervals are combined, allocate this amount between
them. Timing intervals and a lack of observed failures do not establish price
coverage. If reference bounds cannot be obtained, label validation exploratory.
Formal RQMC may use bounded-scramble empirical-Bernstein/betting intervals with
paid tail bounds. Using conservative Hoeffding as the sole classical finalist
would deliberately weaken the competition.

## Staged protocol and project changes

The investigation below is the authoritative proposed confirmation design;
individual reviewer files also contain alternative exploratory designs. None
has already been executed as confirmation.

**Week 1: feasibility, <=16 CPU-hours, <=16 GiB, no hardware spending.**

1. Fix the PSD correlated Heston model, contractual Asian averaging, tolerances,
   controls and complete cost units. Validate elementary increments, telescope
   identity, marginal equality under swaps and signed arithmetic. Use a smooth
   globally regular model only as a theorem/code check. Make the Heston boundary
   bridge an explicit open obligation.
2. Measure level-zero variance and level corrections on development cases with
   1/4 assets, 12 dates, S100/K100, r.03, T1, kappa2, theta=v0=.09, xi=.3,
   equity correlation .3, leverage -.5. Coupled normal construction and induced
   cross-variance correlations must be recorded. Fine refinement levels0–5,
   8 independent batches of 2048 paths per level; fixed root seed recorded in
   the script. Compare ordinary and antithetic corrections, not independent
   differences. Treat fitted alpha/beta as diagnostics with uncertainty.
3. Implement strong classical conditional/control RQMC and the same antithetic
   corrections. Use 32 independent scrambles, 2^8–2^16 points where affordable,
   separately paid training/pilot. Retain all method/case results. Fit full-work
   accuracy curves with whole-scramble resampling, not pointwise iid bootstrap.
4. Compile one coupled update and payoff block at two precisions (initially
   24/32 fraction bits), including load, control, both fine branches, coarse
   path and inverse. Produce T-count/T-depth/width, not CX-to-T guesses. Include
   mean-estimator phase/reflection/quantile work. Use circuit identities and
   small exact state checks for correctness; do not simulate long quantum paths.
5. Insert actual estimator schedules into the break-even relation. The cheapest
   useful experiment is this **classical-cost plus one-oracle cost envelope**.
   If a defensible optimistic scheduled implementation misses 10x across the
   region by orders of magnitude, stop before scaling. Failure of only a loose
   upper bound is inconclusive; identify the specific improvement needed rather
   than claiming an impossibility theorem.

**Weeks 2–3, only after a pilot pass:** attempt to close Heston boundary/payoff-tail and
fixed-point error bounds, verify finite preparation and variance stability,
construct the complete coupled oracle and real-valued estimator. Refine
classical smoothing, controls and multilevel allocation. All deterministic
preprocessing, failed pilot work and compilation costs are reported. Search
again for exact construction/priority and check accessible final proceedings.
Deliverable: source-bound ideal-logical ledger plus proven assumptions, not yet
an advantage claim.

Closing those bounds is a research dependency, not a promised two-week theorem.
If it remains open at the end of week 3, the crossover stays exploratory;
either preregister a financially justified regime with proved bounds or stop
the positive-claim timetable. A six-week positive paper is not assured.

**Week 4:** independently validate continuous-price references; compare two
SDE schemes and low-dimensional Fourier/PDE checks; evaluate optimized CPU and
available GPU finalists. Analyze physical code/factories for at least one
complete architecture, with cycle/error/routing assumptions and parameter
uncertainty. Probe 0.1/1/10 microsecond physical syndrome cycles, but compute
logical-layer duration from code and measurement schedule; do not equate them.
Deliverable: error-qualified crossover surface and frozen methods.
Freeze and report the actual classical CPU/GPU models, core/device counts,
precision, batching and memory. Include parallel classical implementations
where available and report multi-device scaling before claiming a broad
latency advantage. A comparison against one declared classical machine is a
machine-specific result; it does not establish advantage over unlimited
classical parallelism or economic advantage over a differently priced facility.

**Weeks 5–6:** open 24 held-out parameter vectors only after freezing code.
Use six ordered strata `(assets,dates)=(2,12),(2,52),(4,12),(4,52),(8,12),(8,52)`
with four cases j=0,1,2,3 in each stratum s=0,...,5. Set T=1+(j mod 2),
K/S0=`[.9,1,1.1][(s+j) mod 3]`, S0=100, r=.03 and equal basket weights.
Draw a common kappa from [1.5,3], theta from [.04,.12], and xi from [.2,.5]
independently and uniformly, rejecting the triple until the Feller ratio
`2*kappa*theta/xi^2` falls in the case's band: [2,3), [3,4), [4,6], or [.6,1.2]
for j=0,1,2,3 respectively. Thus six predeclared cases stress the boundary.
Draw each asset's v0 independently from [.04,.12], and common leverage from
[-.7,-.2] and equity correlation from [.1,.6]. This distinguishes theta and v0.
Use PCG64 with SeedSequence words `[2026102201,s,j]`, consuming draws in that
stated order; failed triples consume only their own three draws. Each numerical
interval is continuous uniform, so endpoint conventions have probability zero.

For the PSD construction set equity normals to
`sqrt(corr)*Z_common+sqrt(1-corr)*Z_asset` and variance normals to
`leverage*equity_normal+sqrt(1-leverage^2)*U_asset`, with all primitive normals
independent. Record the induced cross-variance and cross-leverage correlations.
There is no performance-based rejection or replacement of draws. Excluding a
boundary band from a theorem regime must occur before opening cases and requires
a new declared confirmation design; it narrows the paper claim. D1/D2/E cases
and today's pilots remain excluded from confirmation. These generation rules
are proposed now; the held-out values have not been generated or examined.

Use 64 independent scrambles or independent MLMC acquisitions per comparison,
with two independent reference constructions. SeedSequence roots proposed:
development 2026092202, reference 2026092203, confirmation 2026102202; child
streams indexed by case/method/level/replicate. Freeze all tuning, precision,
error and hardware menus first. Report paired timing/error uncertainty and
simultaneous intervals for the claimed speedup region; resample entire scramble
estimates. Mathematical coverage comes from the actual estimator proof, not
zero failures in 64 runs. If empirical coverage is itself claimed, run a
separately powered coverage study and include a binomial interval.

Planning compute: workstation pilot first; gated scaling budget <=200 CPU-hours
plus <=24 GPU-hours if available, <=64 GiB peak classical memory. These are caps,
not promises that reference precision is attainable. Report missing GPU tests
as incomplete classical validation, and unaffordable/unbounded references as
an unresolved comparison. No public hardware experiment is needed for level 2.

**Continue** only if coupling/error rates survive, the coarse-level work does
not already exceed the budget, an explicit physical model offers >=10x with
room for uncertainty, and references can be certified. **Revise** if a named
cost component or narrower preregistered model has a credible quantitative
repair; run new confirmation after any outcome-driven change. **Stop** the
advantage direction if conditional RQMC/MLRQMC removes the margin, normalization
or fixed-point noise destroys variance decay, the boundary bridge cannot fit,
or the full resource schedule misses the declared threshold. A useful negative
paper/circuit improvement remains an unsuccessful advantage objective.

Retain the current manuscript as its validated comparator study. Create the
prospective paper separately, provisionally titled **Antithetic quantum
multilevel pricing without Lévy-area simulation: error, resources and classical
crossover**. Its question is whether the full construction actually beats
strong classical pricing. Only after passing confirmation may the claim state
a conditional 10x crossover on the precisely listed parameter region and
hardware model. Do not put that positive claim in the current abstract now.

## Hardware causality and larger alternatives

The hardware review records primary technical sources for IBM, Microsoft,
IonQ, Quantinuum, Google, AWS, JPMorganChase, HSBC and Fidelity. No inspected
development completed the chain from verified capability to changed resources
to lower total pricing time to an actual crossover.

Reduced qubit overhead can enable more data/factories, but speed improves only
if the scheduled bottleneck changes. IBM's inspected qLDPC design includes
time/space tradeoffs; lower qubit count cannot be used as an equal runtime
factor. Microsoft parity/tetron work and Majorana claims do not establish a
large universal non-Clifford machine; the 2026 technical critique matters.
Google/AWS error-correction demonstrations and Quantinuum logical operations
are hardware evidence, not successful execution of this pricing depth. IonQ's
inspected resource rates are architectural projections, not measured pricing
resources. HSBC's bond-fill prediction and Fidelity's hidden-subgroup research
have different outputs. Details and access limits are in the hardware review.

For PDE candidates, let M be the spatial state dimension. Retrieving one price
from a normalized state requires precision scaled by the solution norm and
postselection factors; retrieving many prices adds output work. Pay for
conditioning, coefficient access, terminal/input preparation, domain/boundary
bias and time/space discretization. The May 2026 pricing paper itself has
single-price grid factors growing with dimension and compares against grid
baselines. A price expectation estimated by RQMC does not enumerate that grid.
Forward-density overlap can change extraction, but it does not automatically
prepare sqrt(probability) or encode a path-dependent joint law. None currently
offers a better-supported primary crossover than the test above.

## Claim ledger

| Claim | Status |
|---|---|
| The common-policy D2 quantum ranking reverses with matched controls | Established locally, level 4, declared implementation/menu only |
| Larger GBM dimension can remain cheap classically | Demonstrated exploratory precision diagnostics; not a theorem for all parameters |
| Published weak-Euler resources leave a very large practical gap | Resource sensitivity plus executed discrete classical screen; no matched continuous-price hardware race |
| Antithetic correction telescopes if fine marginals match | Algebraic identity; exact implementation and finite-law binding still required |
| Generic variance-sensitive quantum MLMC can improve MC precision exponents | Established level-3 theorem under rates/access assumptions, not a structured classical lower bound |
| Antithetic log-Heston corrections had beta approximately 2 in two development cases | Executed empirical diagnostic with descriptive intervals; equal classical benefit, benign Feller ratio 4 |
| Those rates apply to correlated square-root Heston in our circuit | Hypothesis; boundary, moments, quantization/loading and cost unresolved |
| Combining antithetic paths and quantum MLMC is publication-new | Unestablished; no exact prior located is not proof of priority |
| The new method has a 10x physical crossover | Unsupported until the complete protocol passes |
| New hardware announcements rescue option pricing | Unsupported without the full causal/resource chain |
| Negative finding or a better quantum circuit fulfills the requested advantage | False |

## Prioritized primary reading

1. [Herman et al.](https://arxiv.org/html/2602.03725v1): §7.1 antithetic gap,
   §7.2 error rates, §§6.2.1–6.2.3 restricted Heston, §8 PDE barriers. This
   identifies the precise reopening and its limits.
2. [Giles–Szpruch](https://arxiv.org/pdf/1202.6283): Assumptions4.1/5.3,
   Theorem5.4, §5.2 discrete Asian averages, §6.2 Heston caveat; [author code](https://people.maths.ox.ac.uk/gilesm/mlmc/)
   `antithetic.m`. Test cancellation and applicability before quantizing.
3. [An et al.](https://arxiv.org/pdf/2012.06283): Theorem2, Eqs3.9–3.13,
   ceiling/level costs and Appendix A. [Kothari–O'Donnell](https://arxiv.org/pdf/2208.07544):
   Theorems1.1/1.3, §4 reductions; compile the estimator, not just its payoff.
4. [Wang–Kan](https://arxiv.org/html/2312.15871v3): weak scheme, payoff
   normalization/footnote8, Tables5–6, arithmetic appendices. Reproduce units
   before borrowing a resource total.
5. [Chen et al.](https://arxiv.org/html/2510.06705v2): §4 and §5.2,
   Eqs37–39; [Custers et al.](https://arxiv.org/html/2609.07169v1): geometric
   transform/control construction and §5.1 Table6; [Liu CAS](https://arxiv.org/html/2212.13232v2):
   stochastic-volatility/Asian conditioning and numerical comparison. These
   are the classical methods most likely to terminate the proposed advantage.
6. [RQMC confidence](https://arxiv.org/html/2504.18677v2): bounded scramble
   confidence constructions and allocation; [Case](https://arxiv.org/html/2502.17731v2):
   §6, Tables11–12 and finite-window caveats. These prevent weak comparisons.
7. [Blanchet et al.](https://arxiv.org/pdf/2502.05094): Theorem3.2,
   Algorithms1–4, §4 compound call, AppendicesA–C; [nested kernel quadrature](https://proceedings.mlr.press/v267/chen25av.html):
   Theorem1/Corollary1, AppendixF and [code](https://github.com/hudsonchen/nest_kq).
   Read together before activating the fallback.
8. [QqMC](https://arxiv.org/html/2609.03625v1): Eqs5.1/5.27, Table1,
   §6 and AppendixC. Useful mainly to prevent overstating a query plot.
9. [PDE pricing](https://arxiv.org/html/2605.26610v1): AppendicesE–H,
   especially G.2/G.3 norm and readout costs; compare to pathwise classical
   integration, not only a full grid.

**Single next action:** build the classical-versus-coherent cost envelope for
one finite-precision antithetic correction **and the coarse/base level**,
including preparation, all three paths, signed output and uncomputation.
Include the chosen variance-sensitive estimator's actual reflection, phase,
quantile and confidence schedule. Place the resulting complete estimate beside
measured conditional-control MLMC/RQMC runtime in the break-even inequality.
This most directly decides whether the specific
remaining hypothesis deserves weeks of research. If its permitted oracle
duration is unattainable even in an explicit favorable architecture, stop.
