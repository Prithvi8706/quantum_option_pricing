# Formulations and classical comparators: atomic limitation audit

Date: 1 October 2026. This is a research audit of [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md), not a replacement of its benchmark verdict. No new pricing experiment or quantum circuit was run for this memo. The alternatives below are screened against the existing one-price, absolute-error, 99%-confidence contract. A different payoff, stochastic model, or output is explicitly a different experiment.

The central finding is that several **components have known alternatives**, particularly exact/fast-forwarded Heston sampling, structured quantum integration, change of measure, and PDE formulations. None of the sources checked establishes a practical tenfold crossover for the repository's exact contracts. Conversely, the repository does not justify universal claims that quantum advantage requires an unstructured problem, a classical precision exponent at least three, or a quantum-only variance reduction.

Status vocabulary: **component solved** means the mathematical subproblem has a construction under stated assumptions; **conditional** means transfer to this workload needs proof or implementation; **different task** means the proposal changes the contract; **not established** means this search did not verify the desired result, not that no result exists. Proposed pass/fail thresholds are development decisions, not results already obtained.

Local evidence read: [antithetic results](../antithetic_feasibility/RESULTS.md), [compound results](../compound_feasibility/RESULTS.md), [residual results](../controlled_residual_feasibility/RESULTS.md), [barrier falsifier](../research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md), and the barrier preintegration implementation. These results already contain qualifications that the synthesis sometimes shortens too aggressively.

## F01 — A measured RQMC slope is not a classical lower bound

**Source:** §§2.3, 4 Failure 6, 5A, 6. The measured cost exponents near one for calls/digitals and 1.6–1.9 for barriers describe the methods, cases, and sample range tested.

**Alternative/status:** Improve the classical transformation, or find a different quantum formulation whose own exponent is different. **Not established:** neither the measured slope nor the selected classical algorithm is an optimality theorem. The local barrier study explicitly lists untried multi-direction smoothing, bridge-ordered survival, importance sampling, and GPU execution.

**Transfer trap:** Extrapolating a finite-range slope over several orders of magnitude, or assuming that adding dimensions leaves the same slope and constant unchanged. The reported barrier times at the target count are modelled from measurements, not all direct time-to-accuracy acquisitions.

**Small test:** Refit the existing scramble results over several adjacent sample-count windows, with uncertainty across independent scrambles. Pass for using an extrapolation only if its predicted uncertainty agrees with an independently acquired next sample size; otherwise keep the frontier confined to the measured range. This does not require opening confirmation cases.

## F02 — The standard deviation of one path does not determine RQMC error

**Source:** §§2.1–2.3, 4 Failure 3. The simple speedup identity uses iid Monte Carlo variance.

**Alternative/status:** Maintain two quantities: the quantum estimand's path standard deviation, and the variance of an independently scrambled classical quadrature estimate. **Component solved:** this is an accounting correction. They are different objects; replacing one with the other incorrectly credits an unsmoothed quantum oracle with the classical transformation's benefit.

**Transfer trap:** Writing classical RQMC cost solely as a power of `sigma/e`. The constant depends on coordinate ordering, smoothness, ANOVA structure, scrambling, and the actual estimator. The local H1 report correctly uses the plain quantum payoff's standard deviations 5.73 and 5.15.

**Small test:** For every candidate row, record the function actually computed by each oracle and the measured variance of each classical replicate. Pass only if every variance reduction in the quantum ledger has a corresponding implemented or fully specified coherent transformation.

## F03 — Smoothness after the Gaussian transformation must be checked

**Source:** §§2.3, 5A: smooth scrambled-net integration can outperform generic amplitude estimation asymptotically.

**Alternative/status:** Choose transformations that preserve appropriate mixed smoothness, use preintegration, or move the integral to another coordinate system. **Conditional.** [Owen's smooth-integrand analysis](https://statistics.stanford.edu/technical-reports/scrambled-net-variance-integrals-smooth-functions) gives variance of order `n^-3` with dimension-dependent logarithms under smoothness assumptions. [Basu and Owen](https://arxiv.org/abs/1512.02713) explicitly study when transformations preserve the variation or smoothness needed for QMC/RQMC rates.

**Transfer trap:** A smooth payoff in prices need not be smooth with bounded derivatives on the unit cube after inverse-normal transformation; derivatives can diverge near the endpoints. Smoothing an exercise kink alone does not establish the strongest RQMC theorem.

**Small test:** Write the transformed integrand and inspect its mixed derivatives at Gaussian tails and exercise/barrier boundaries. Pass for citing a rate theorem only when its function-space assumptions are verified; otherwise describe the rate as measured.

## F04 — `p_Q = 1` is specific to generic mean estimation

**Source:** §2.3 and §5A. The former fixes the quantum precision exponent at one; the latter correctly admits structured integration.

**Alternative/status:** Hierarchical interpolation/quadrature plus quantum estimation of residuals. **Component solved in function classes; conditional here.** [Heinrich's Sobolev integration result](https://doi.org/10.1016/S0885-064X(02)00008-0) gives errors proportional, up to qualifications and logarithms, to `n^(-s-1/2)` classically and `n^(-s-1)` quantumly for the stated `p >= 2` classes, where `s = r/d`. Thus precision-cost exponents are `1/(s+1/2)` and `1/(s+1)`.

**Transfer trap:** Comparing a structure-exploiting classical method with an unnecessarily unstructured quantum algorithm, or assigning the theorem's smoothness class to a discontinuous barrier integrand. Its constants and coherent residual evaluation still need charging.

**Small test:** Select one already-smoothed two-dimensional development integral. Construct a coarse interpolant with an analytically integrated mean and bound the residual. Pass if the complete quantum residual cost improves over plain AE at fixed certified accuracy; compare the same interpolant plus classical RQMC.

## F05 — Coherent Sobol points solve net preparation, not the entire comparison

**Source:** §6, quantum quasi-Monte Carlo row.

**Alternative/status:** [Recchia et al.](https://arxiv.org/html/2609.03625v1) construct coherent Sobol coordinates using binary linear maps and study a query-count window comparing QMC error upper bounds. **Component solved:** this structured coordinate generation. **Not established:** superiority over this repository's tuned scrambled RQMC or an end-to-end pricing crossover. The paper's implementation examples are linear integrands; its window omits the full function-implementation cost, and part of its dimensional analysis uses a fitted net-quality ansatz.

**Transfer trap:** Treating a loose classical discrepancy upper bound as a measured classical error, or treating fewer black-box queries as lower latency. A linear integrand with known coefficients also has an elementary classical integral.

**Small test:** Substitute one actual repository payoff and the same Sobol matrices into both estimators. Pass only if the query saving survives measured classical error, 99% success amplification, and the complete coherent payoff cost. Net generation alone is not the bottleneck removed.

## F06 — Barrier preintegration leaves a specific switching surface

**Source:** §4 Failure 6. The tested one-direction smoothing failed to restore a near-one RQMC error rate.

**Alternative/status:** Multi-direction preintegration or domain partitioning by the active barrier date. **Conditional.** In [the actual code](../../research/advantage_frontier_20260923/barrier_fast_classical.py), each date yields a barrier root, then `zh` is their minimum. Even if each root is smooth, the identity of the minimum changes. This identifies a concrete remaining nonsmoothness rather than an unexplained failure of all smoothing. [Numerical smoothing](https://arxiv.org/abs/2111.01874) provides a root-finding/integration framework under regularity assumptions.

**Transfer trap:** The theorem for a suitable scalar boundary is not automatically a theorem for the minimum of 52 moving boundaries. Replacing the contractual discrete barrier with continuous monitoring changes the price.

**Small test:** On the 4-by-12 development case, log the active date and the gap between the two smallest roots. Smooth or partition only near root ties. Pass if cost times replicate variance improves over existing preintegration and the price agrees within a prespecified error allowance. A negative result isolates this particular mechanism, not all smoothing.

## F07 — Survival conditioning is one proposal, not the last rare-event method

**Source:** §4 Failure 6, one-step-survival rate.

**Alternative/status:** Importance sampling followed by an active-subspace rotation and preintegration; or sequential Monte Carlo with survival-oriented weighting. **Conditional.** [Yu and Wang, 2026](https://arxiv.org/abs/2603.01763) study the first combination, particularly for out-of-the-money pricing and Greeks. [Sen, Jasra and Zhou](https://arxiv.org/abs/1608.03352) construct unbiased SMC option estimators and test barriers and TARNs. Neither source verifies the exact repository basket knock-out case.

**Transfer trap:** Learned proposals have training costs and likelihood-ratio tails; SMC resampling creates dependence. A quantum version cannot assume classical resampling or a cheap coherent likelihood ratio for free.

**Small test:** Fit one low-parameter Gaussian tilt on separate development data, freeze it, and compare equal-time variance with existing barrier preintegration. Pass if total cost to the same uncertainty improves, including training. Only then consider a coherent tilt circuit.

## F08 — An unbounded call can sometimes become two bounded probability estimates

**Source:** §5A, heavy tails; §§2.1, 5F, normalization and moment certification.

**Alternative/status:** Change of measure. The general technique is established in [Geman, El Karoui and Rochet's numeraire work](https://doi.org/10.1017/S002190020010289X) and in [Lee's transform-pricing analysis](https://math.uchicago.edu/~rl/dft.pdf); the following direct identity needs only a nonnegative integrable random variable, not a tradable-numeraire interpretation. **Component solved mathematically; coherent efficiency conditional.**

Let `A >= 0`, `m = E_Q[A] > 0` be known, and define `dQ_A/dQ = A/m`. For an event `E` on which `A > K`,

```text
E_Q[(A-K) 1_E] = m P_QA(E) - K P_Q(E).
```

Use `E = {A > K}` for an Asian call, or additionally require survival for the knock-out. Both estimated random variables are indicators. This removes unbounded payoff loading and the need for a finite second moment of the original payoff from this representation. For `K >= 0`, another exact form is `m E_QA[(1-K/A)+ 1_survival]`, taking the expression as zero on `A=0`. It avoids subtraction of two probability estimates. It can also be encoded as one predicate `U A > K` plus survival, with an independent uniform `U` in `[0,1]`, instead of evaluating a reciprocal. Finite uniform precision still needs an error bound.

For GBM, write `A = sum_j w_j exp(mu_j + b_j^T Z)`, `Z ~ N(0,I)`, with nonnegative weights. Then `Q_A` is a mixture: choose `j` with probability `w_j exp(mu_j + ||b_j||^2/2)/m`, and draw `Z ~ N(b_j,I)`. This follows by completing the square in the Gaussian density. It uses model structure and is available classically too.

**Transfer trap:** Two probabilities require an error allocation in dollars; cancellation can be costly. The single-predicate version has normalization `m`, which may be substantially larger than the original payoff standard deviation. The mixture loader, shifted Gaussian generation, comparisons, path arithmetic, and 99% success still cost resources. For a generic heavy-tailed law, sampling `Q_A` may be hard. These identities do not themselves establish a speedup.

**Small test:** Verify the mixture identity on a two-asset, two-date GBM case against direct integration; derive an explicit price-error allocation `exp(-rT)(m e_A + K e_Q) <= epsilon_stat`. Pass to compilation only if the two complete indicator schedules cost less than the original payoff schedule under the same tail and confidence accounting.

## F09 — Infinite variance changes both sides' precision exponents

**Source:** §5A, heavy-tailed payoffs; §7, classical exponent requirement.

**Alternative/status:** Quantum estimators under a bounded `p`th moment, `1 < p < 2`, rather than a variance bound. **Component solved in oracle models; conditional in pricing.** [Wu et al.](https://arxiv.org/abs/2301.09680) give heavy-tail quantum mean estimation as a bandit subroutine. [Quantum Speedups for Stochastic Optimization with Heavy-Tailed Noise](https://arxiv.org/html/2607.25492v2), Appendix C, proves a scalar quantum query lower bound of order `(sigma/epsilon)^(p/(2(p-1)))` and matching-type estimator results up to logarithms.

**Transfer trap:** Retaining quantum `epsilon^-1` after losing the finite-variance premise. At `p=3/2`, the scalar classical moment-model exponent is three and the quantum exponent is 3/2: the improvement is still quadratic in sample count, but the exponent difference is 1.5. A tractable change of measure may eliminate this apparent hard regime for both sides.

**Small test:** Identify one specified financial model/payoff with a finite first moment, a verified usable `p`th moment bound, and no cheap bounded re-expression found. Pass only after charging coherent sampling, tail truncation and comparison with robust classical estimation and importance sampling. The repository's GBM cases are not evidence for such a regime.

## F10 — Antithetic coupling has already solved a mathematical component

**Source:** §4 Failure 1, correction variance falls by roughly 570–600 times.

**Alternative/status:** Keep the coupling and optimize which side estimates which levels. **Component solved under its assumptions:** antithetic MLMC can avoid explicit Levy-area simulation while reducing correction variance. [Giles and Szpruch](https://arxiv.org/abs/1202.6283) distinguish smooth from piecewise-smooth payoff rates. [An et al.](https://arxiv.org/abs/2012.06283) analyze quantum-accelerated multilevel methods.

**Transfer trap:** The classical benefit does not make coupling useless for quantum; it makes the *relative comparison* more demanding. Conversely, a small correction variance is insufficient if its complete coherent cost or the base level dominates.

**Small test:** Recompute optimal per-level allocations using separate measured classical costs and candidate coherent costs; permit a classical base and selected quantum correction levels. Pass only if their sum, including base uncertainty, beats the best complete classical allocation. Use explicit schedules before making a crossover claim.

## F11 — The 74% base fraction gives a fixed-allocation floor, not a universal floor

**Source:** §4 Failure 1; local A4 base time 10.17 of 13.75 seconds.

**Alternative/status:** Replace the coarse approximation, condition the base more strongly, use an analytic surrogate plus residual, or amortize a base over genuinely repeated requests. **Conditional.** For the *existing allocation*, keeping the classical base and making corrections free gives at most `13.75/10.17 ~= 1.35` speedup. This is an exact accounting consequence of those times.

**Transfer trap:** Declaring all hybrid MLMC schemes capped at 1.35, or declaring success after computing only corrections. An amortized base also requires the declared task to include enough prices for reuse, with equivalent reuse allowed classically.

**Small test:** Try one cheaper level-zero control and retune all allocations. Pass if the base plus its residual uncertainty falls below the tenfold total budget; fail early if the base alone already exceeds it. The base target is independently testable before designing fine quantum paths.

## F12 — The Feller issue is not solved by observing positivity

**Source:** §4 Failure 1: the S4 case has Feller ratio 0.64 and fitted correction exponent about 1.24.

**Alternative/status:** Boundary-adapted discretization, exact CIR transitions, or a different coupling. **Conditional.** The [original Giles–Szpruch Heston example](https://people.maths.ox.ac.uk/~gilesm/files/aap14.pdf), §6.2, explicitly says the square-root coefficients do not satisfy its Lipschitz assumptions, even in its favorable numerical parameter regime. The repository correctly makes the same distinction.

**Transfer trap:** Treating `beta = 2` as a proved Heston result whenever the Feller ratio exceeds one; or assuming positivity of a discrete update proves convergence and moment bounds. The measured S4 exponent is not a universal lower bound either.

**Small test:** Freeze the S4 parameters and compare two couplings across a few refinement levels with matched random inputs. Pass for a numerical candidate if correction cost/variance improves without detectable bias; pass for theorem use only after checking boundary and moment assumptions. These are separate gates.

## F13 — Non-globally-Lipschitz MLMC theory is relevant but not a blanket Heston fix

**Source:** §4 Failure 1, favorable variance rate not universal.

**Alternative/status:** [Pang and Wang](https://arxiv.org/html/2305.12992v2) analyze modified Milstein antithetic schemes for specified non-globally-Lipschitz SDEs, including superlinear growth. **Component solved for that assumption class; transfer not established.**

**Transfer trap:** Confusing failure of global Lipschitzness through growth at infinity with the singular derivative of `sqrt(v)` at zero. A theorem addressing the first does not automatically cover the second. A title match is insufficient.

**Small test:** Make a one-page assumption-by-assumption map from the paper's coefficient, derivative, monotonicity, and moment hypotheses to the repository's S4 variance process. Pass only if every hypothesis can be verified or a justified transform supplies it; otherwise retain this as a lead, not a claimed repair.

## F14 — Heston does not intrinsically require every internal Euler/Milstein step

**Source:** §4 Failure 1: stochastic volatility forces time-stepping and expensive square roots.

**Alternative/status:** Exact transition simulation. [Broadie and Kaya](https://pubsonline.informs.org/doi/abs/10.1287/opre.1050.0247) provide exact Heston simulation using integrated variance. [Choi and Kwok](https://arxiv.org/html/2301.02800v1) use Poisson conditioning to remove modified-Bessel evaluations in an exact-simulation construction. **Component solved classically for the stated process; coherent and correlated-basket implementation conditional.**

**Transfer trap:** Exact simulation does not mean free finite-precision sampling. Inversion, conditional integrated-variance sampling, special functions, truncation of series, and correlated assets can move the cost elsewhere. Contractual monitoring dates remain even if artificial internal refinement is eliminated.

**Small test:** First price one asset at the 12 contractual dates with an exact-transition reference and compare cost/error with the current internal refinement. Then list the coherent sampler primitives before compiling anything. Pass if the entire transition is cheaper at the same law accuracy, not merely if it uses fewer dates.

## F15 — A 2026 quantum fast-forwarding result is a concrete conditional reopening

**Source:** §4 Failure 1 and §6 stochastic-volatility row.

**Alternative/status:** [Quantum Speedups for Derivative Pricing Beyond Black-Scholes](https://arxiv.org/html/2602.03725v1), §§6.1–6.2, gives a quantum sampling/fast-forwarding construction related to Broadie–Kaya and an asymptotic gate-complexity result for specified Heston models. **Component solved under paper assumptions; practical transfer conditional.** Its scope includes path-dependent Lipschitz, piecewise-linear payoffs, asset–asset correlations with decoupled variance processes, explicit tail restrictions, and `eta = 4 kappa theta / xi^2 >= 5` in the loading/discretization analysis. This is stronger than the ordinary Feller threshold.

**Local check:** The documented Feller ratios are `2 kappa theta/xi^2`: A1/A4 = 4, S4 = 0.64, B8 = 1.44. Their eta values are therefore 8, 1.28, 2.88. **A1/A4 pass this one condition; S4 and B8 fail it.** This is not a check of the paper's remaining restrictions.

**Transfer trap:** Asymptotic end-to-end gate complexity is not a compiled fault-tolerant latency crossover. Verify the repository's exact joint Brownian covariance against the paper's model; matching only equity correlation numbers is insufficient. A discontinuous knock-out payoff is outside the cited Lipschitz premise.

**Small test:** Map A1, then A4, to every model/tail/loading hypothesis and derive the primitive list for one contractual transition. Pass the first gate only if all assumptions hold; pass the second only if a complete clean transition has a better error-certified cost than the current path construction. This deserves attention before another large MLMC experiment.

## F16 — GBM factor reuse is specific, but absence of Markov structure is not necessary

**Source:** §4 Failure 2 and §5D: a rescue is described as needing no exploitable Markov structure or no exploitable structure.

**Alternative/status:** Seek structure that is cheaper to exploit coherently, not a completely structureless financial model. **The claimed necessity is unsupported.** The local compound benchmark factorizes future GBM paths into current spots times reusable future factors. That proves a strong simplification for this family. It does not prove every Markov model has equally cheap conditional values.

**Transfer trap:** Making a model non-Markovian solely to hurt classical pricing can make coherent sampling harder too. Conversely, Markovianity is an aid to dynamic programming, not a guarantee of a small or easy state representation.

**Small test:** Identify exactly which factorization a proposed model breaks, then measure its conditional-state dimension and cheapest classical approximation. Pass only if the extra coherent work grows more slowly than the measured classical difficulty; a new model label alone fails.

## F17 — The tiny exercise-policy bracket is an observation, not a population certificate

**Source:** §4 Failure 2: development brackets about `4e-8` to `6e-6` dollars.

**Alternative/status:** Localize work near the exercise boundary, with certified upper/lower continuation bounds; use the same localization classically and quantumly. **Conditional.** The [compound results](../compound_feasibility/RESULTS.md) distinguish the exact expectation inequalities from the sampled gap and state that the observed gap is not itself a confidence bound.

**Transfer trap:** A rare region can contribute to policy error yet be absent from a small test set. Uniform inner accuracy is also potentially wasteful far from the exercise boundary, but coherent adaptive stopping requires an actual variable-cost construction.

**Small test:** On existing development states, bound the contribution from `|continuation - strike| <= h` and the classification error outside it. Pass if the residual error is bounded below the allocated budget at lower total cost than the current uniform policy/Jensen calculation. A narrow empirical average alone fails.

## F18 — Classical nested complexity is assumption-dependent

**Source:** §4 Failure 2: the best classical nested methods are approximately `epsilon^-2`.

**Alternative/status:** Nested MLMC, randomized MLMC, regression, and factorized conditional evaluation. **Component solved for particular nesting classes; not a universal pricing theorem.** [Sun, Wang and Blanchet](https://arxiv.org/html/2602.08120v1), Definition 1.1 and Theorems 1.4/1.6, assume Lipschitz dependence on the inner value, a finite terminal second moment, fixed depth, unit-cost trajectory steps, and free function evaluation. Their stated classical exponents approach two with qualifications on the error norm; the quantum theorem controls RMSE.

**Transfer trap:** Treating these as literal seconds or a lower bound against all structured classical methods; treating exact `epsilon^-2` as proved for arbitrary repeated nesting and nonsmooth outer functions.

**Small test:** For any new nested payoff, tabulate the outer Lipschitz constants, terminal moments, conditional sampling cost, depth, and required error norm. Pass only if the theorem actually applies; then substitute real evaluation costs and a common 99% guarantee.

## F19 — More nesting changes logarithms and constants, not automatically the leading exponent

**Source:** §4 Failure 2: the gap is said to shrink with nesting depth.

**Alternative/status:** Deterministic level scheduling avoids a direct quantization's variable-runtime problem. **Component solved in the [Sun–Wang–Blanchet access model](https://arxiv.org/html/2602.08120v1).** At fixed depth `D`, its quantum rate is `epsilon^-1 log^(3D+1)(1/epsilon)` at the outermost level. The leading precision exponent remains one; growing logarithmic factors and hidden depth constants can destroy a practical crossover.

**Transfer trap:** Letting depth grow with accuracy while quoting a theorem that holds depth constant, or describing a finite-log penalty as a different leading precision exponent.

**Small test:** Expand one explicit `D=2` schedule, including per-level source and inverse calls, rather than assigning a single optimistic constant. Pass if its actual calls improve on the existing nested schedule at the target error and confidence; an asymptotic expression alone fails.

## F20 — Shared controls hurt relative sampling gain only under a cost premise

**Source:** §4 Failure 3 and §5D: variance reduction is symmetric and shrinks quantum advantage.

**Alternative/status:** Optimize the joint product of residual size and coherent cost. **Component solved analytically:** suppose a control changes standard deviation to `a sigma`, coherent per-call cost by `b_Q`, and classical sample cost by `b_C`. In the iid-MC versus variance-sensitive-QME model, ignoring setup,

```text
T'_Q / T_Q = a b_Q
T'_C / T_C = a^2 b_C
(T'_C/T'_Q) / (T_C/T_Q) = a b_C/b_Q.
```

If `b_Q = b_C`, a shared control with `a < 1` indeed reduces relative quantum speedup. But relative speedup improves whenever `b_Q < a b_C`: the new representation makes the coherent oracle sufficiently cheaper. Therefore a quantum-exclusive control is **not necessary**. This is a deduction from the document's model, not a new advantage result.

**Transfer trap:** Applying the iid variance formula to RQMC, or ignoring control evaluation, fitting, and certification costs. Different controls may optimize the two architectures.

**Small test:** For one parity or numeraire rewrite, measure/compile both the residual and its full source cost. Pass only on total time at equal accuracy. Reporting the variance factor by itself is insufficient.

## F21 — Rough volatility is not a single classical precision exponent

**Source:** §6 rough-volatility row quotes approximately `epsilon^-1.3` to `epsilon^-1.6`.

**Alternative/status:** Brownian bridges, smoothing, sparse grids, RQMC, extrapolation, and different rough-process representations. **Conditional.** [Bayer, Ben Hammouda and Tempone](https://arxiv.org/abs/1812.08533) demonstrate substantial gains for rough Bergomi European pricing across selected parameters. This supports a stronger comparator menu, not one universal exponent for all rough models and all path-dependent payoffs.

**Transfer trap:** Conflating weak discretization error, quadrature error, per-path cost and measured overall cost. European smoothing may not preserve a path barrier's regularity. Rough Heston and rough Bergomi are different models.

**Small test:** For one proposed rough contract, separate kernel approximation, time discretization, integration, and floating-point error. Pass for an exponent claim only after measuring total cost against total error over a declared range with uncertainty. Otherwise use the published methods as candidates, not fixed baseline rates.

## F22 — A Markovian lift can remove long memory without making the state small for free

**Source:** §4 Failure 2 and §6, non-Markov/rough candidates.

**Alternative/status:** Approximate a fractional kernel by a sum of exponentials and evolve auxiliary factors. **Component solved under assumptions; conditional for this workload.** [Bayer and Breneis](https://arxiv.org/abs/2309.07023) prove weak rough-Heston approximation bounds for specified European claims; [their simulation work](https://arxiv.org/abs/2310.04146) tests efficient weak schemes, including path-dependent and Bermudan examples.

**Transfer trap:** The number of factors, stability, payoff assumptions, and kernel bias must be paid. The lift aids classical solvers too; it does not make a difficult conditional expectation easy or establish quantum advantage.

**Small test:** Increase lift rank on one development case while separately refining time steps. Pass if a small rank meets a fixed bias allowance and lowers full path cost; only then cost its coherent update. Failure means this lift/rank target fails, not that rough models cannot be approximated.

## F23 — More assets and dates do not imply equal scaling on both architectures

**Source:** §6, more-assets/more-dates row.

**Alternative/status:** Exploit separability, low-rank covariance, temporal compression, or a factor model. **Conditional.** The question is how effective dimension, arithmetic work, memory, and parallel scheduling each scale. The present 4-by-12 and 8-by-52 cases cannot establish a law for arbitrary dimensions.

**Transfer trap:** More contractual dates cannot simply be discarded as numerical refinement. A low-rank Gaussian approximation changes the model unless its pricing error is bounded. Giving quantum a compressed model while timing classical on the full model is unmatched.

**Small test:** At fixed contractual accuracy, compare covariance ranks and quantify the price error from omitted modes using a payoff-appropriate bound. Pass if the same compressed law is valid on both sides and the complete quantum/classical ratio improves. Merely reducing qubits is not the pass condition.

## F24 — Quantum PDE/linear-system algorithms offer a different source construction

**Source:** §6, quantum PDE row.

**Alternative/status:** Solve the backward pricing PDE coherently instead of generating every path. **Conditional.** [Miyamoto and Kubo](https://arxiv.org/abs/2109.12896) explicitly address multi-asset finite differences and extraction of a price from a quantum solution state. This is more than an unspecified appeal to HHL, but its dimensional comparison is to the relevant grid method, not a proof against all probabilistic classical pricing.

**Transfer trap:** A state of grid values is not a classical point price. Conditioning, matrix access, stability, payoff loading, success probabilities, grid precision, and scalar extraction can dominate. Asian averages and barriers require suitable state augmentation or boundary updates.

**Small test:** Formulate the exact repository contract as a small augmented PDE and write the complete dimension, sparsity, conditioning, state-preparation and observable-extraction ledger. Pass if its optimistic complete cost is competitive with measured RQMC before building a large PDE circuit.

## F25 — Forward PDEs can simplify output structure, but readout is still costly

**Source:** §6, quantum PDE row; §1, one classical price.

**Alternative/status:** [Guseynov et al.](https://arxiv.org/html/2511.04942v1) evolve a local-volatility density using Schrodingerisation and recover prices from overlaps. **Component solved for the stated construction; conditional transfer.** Theorem III.5 charges `O(e_st^-2 log(1/delta))` copies for swap-test overlap estimation. The multi-asset discussion additionally assumes an efficient factorized or short-factor-sum payoff state.

**Transfer trap:** Counting the small swap-test circuit while omitting the repeated cost of preparing its input states. Price recovery includes normalization and a ratio of overlaps, so overlap error must be converted into a dollar error. Short-factor payoff representations are assumptions to verify, especially for path dependence.

**Small test:** Bound both relevant overlaps away from unstable normalization regimes for one candidate payoff, propagate errors to dollars, and multiply required state copies by complete PDE evolution cost. Pass only against the best eligible classical method on the same contract.

## F26 — SPDE/BDSDE methods extend the model class without yet removing oracle cost

**Source:** §6, stochastic-volatility/PDE possibilities.

**Alternative/status:** [Li et al., 2026](https://arxiv.org/html/2606.31076v1) use backward doubly stochastic representations and quantum multilevel estimation for prices and Greeks. **Conditional algorithmic result.** Their estimator assumes efficient quantum encoding, and the construction specifies reversible one-step update oracles and strong-error requirements; the cited square-root sampling improvement does not supply a compiled fault-tolerant implementation of those updates.

**Transfer trap:** Treating a more sophisticated stochastic environment as a free hard classical workload. Extra noise, conditional expectations, smoothness/moment requirements, and representation bias also enter quantum cost. Switching to an SPDE is a new financial model.

**Small test:** Identify one concrete SPDE model justified independently of quantum advantage and audit a single forward/backward update's arithmetic and assumptions. Pass only if the complete update plus level allocation gives a plausible finite target. Keep this below direct Heston fast-forwarding in priority for the current repository.

## F27 — The square-root multi-output penalty is model- and norm-dependent

**Source:** §6, many strikes, portfolios, Greeks.

**Alternative/status:** Quantum multivariate mean estimation, shared payoff evaluation, or a single aggregate observable. **Component solved in access models; conditional.** [Cornelissen, Hamoudi and Jerbi](https://arxiv.org/abs/2111.09787) distinguish binary-value and phase access, Euclidean error, covariance, and low-precision regimes where generic quantum advantage disappears. A standalone `sqrt(K)` multiplier is not a universal law for every collection of prices or risk outputs.

**Transfer trap:** Comparing componentwise 99% prices with one vector RMSE guarantee; ignoring covariance or the cost of producing all K classical outputs. Shared paths and structure are available classically.

**Small test:** Specify whether the output is K separately accurate prices, one portfolio total, or a vector with an aggregate norm guarantee. Then map that exact guarantee to the estimator and charge shared source/payoff work. Pass only with matched failure probability and output costs.

## F28 — Quantum gradients need comparison with adjoints, including discontinuities

**Source:** §6, Greeks row.

**Alternative/status:** Quantum gradient algorithms and smoothing/Malliavin representations. **Different task from one price; conditional advantage.** [Stamatopoulos et al.](https://arxiv.org/abs/2111.12509) study quantum financial sensitivities and resource scenarios. [Giles and Glasserman's adjoint work](https://people.maths.ox.ac.uk/~gilesm/codes/libor_AD/) supplies the relevant shared classical gradient computation; the author discussion also explains why discontinuous payoffs require additional treatment.

**Transfer trap:** Comparing a quantum gradient with K separate finite-difference repricings when a valid adjoint exists. The opposite mistake is assuming naive pathwise differentiation works through a digital or knock-out discontinuity.

**Small test:** Choose a specific first-order sensitivity of the current barrier payoff and implement a valid conditional-smoothed classical derivative estimator before pricing the quantum gradient oracle. Pass only if its bias, variance and cost are matched; second-order Greeks need their own analysis.

## F29 — A portfolio total can be one output, but reuse changes the benchmark

**Source:** §§1, 6, many-strikes/portfolios row.

**Alternative/status:** Compute the expectation of a weighted portfolio payoff directly, or amortize a distribution/model representation across a declared sequence of requests. **Different task if the requested output changes; otherwise conditional.** Linearity removes any requirement to estimate each constituent price separately when only the total is requested.

**Transfer trap:** Calling a portfolio-total result an improvement for K individual prices. Conversely, charging K independent quantum prices is unnecessarily pessimistic for one linear aggregate. Netting can reduce variance on both sides, and classical pathwise payoff reuse can be extensive.

**Small test:** Define a small fixed portfolio and derive its aggregate payoff before either estimator is chosen. Pass if the aggregate source's complete cost/variance improves the matched ratio; include training/setup amortization over the actual number of delivered outputs. This does not rescue the existing single-contract claim automatically.

## F30 — Tensor networks are both a possible loader and a classical competitor

**Source:** §§5D, 6, structured models and alternate PDE approaches.

**Alternative/status:** Tensor-train compression of pricing integrands, solution states, or parameter surfaces. **Conditional.** [Quantum-inspired variational PDE pricing](https://arxiv.org/abs/2207.10838) and [tensor-train Fourier parameter learning](https://arxiv.org/abs/2405.00701) are relevant classical alternatives. [Tensor-train Greeks](https://arxiv.org/abs/2507.08482) demonstrate reusable representations in a specific multi-asset example. These sources do not give a universal low-rank guarantee for barrier path payoffs.

**Transfer trap:** A small tensor rank can make both classical contraction and quantum preparation cheap. Training on a large classical dataset is not free state preparation, and interpolation accuracy at random test points is not a worst-case financial error guarantee.

**Small test:** Fit one low-rank approximation to a small development integrand, track rank and out-of-sample integral error as assets/dates increase, and compare direct contraction with coherent loading plus AE. Pass quantum screening only if low-rank structure helps the quantum total more than the corresponding classical contraction.

## F31 — Cubic classical precision cost is not a requirement for advantage

**Source:** §7, best classical cost at least `epsilon^-3`; §4 Failure 2 and §5D requirements language.

**Alternative/status:** A sufficient finite-accuracy constant improvement can produce a crossover even when exponents match; structured algorithms can have different paired exponents; heavy-tail or mixing parameters introduce additional axes. **The universal requirement is rejected.** The source document already labels §7 a sensitivity frontier, and this qualification must remain attached to every row.

**Transfer trap:** Turning a practical warning about quadratic speedups into a theorem of impossibility. The actual acceptance test is complete quantum time at most one tenth the fastest eligible complete classical time, at equal output/error, independent of the asymptotic label.

**Small test:** For each proposed alternative, compute `T_Q = setup_Q + estimator_cost_Q + readout_Q` and compare with the actual eligible `T_C`, including error certification on both sides. Pass on this inequality; do not reject solely because the classical exponent is below three or accept solely because it is above three.

## F32 — Quantum-walk speedups need a pricing problem that actually needs mixing

**Source:** §5A, quantum-walk MCMC screen.

**Alternative/status:** Quantum walks can accelerate preparation/reflection for suitable reversible chains, with benefits depending on spectral gap and overlap along a preparation schedule. **Component solved in specified models; pricing transfer not established.** [Wocjan et al.](https://arxiv.org/abs/0811.0596) combine mixing and precision improvements for partition functions. [Montanaro's full paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4614442/), Theorems 3.4–3.5, states the reversible-chain, overlap and initial-state premises.

**Transfer trap:** Direct Gaussian simulation of GBM has no slow MCMC mixing bottleneck to accelerate. Introducing an artificial Markov chain does not create an advantage. A difficult posterior-calibration or constrained-distribution problem would be a changed input/model task unless already part of the pricing contract.

**Small test:** Identify a financially justified distribution that lacks a competitive direct sampler, specify its best classical chain and credible alternatives, and estimate the relevant observable's autocorrelation as well as the spectral gap. Pass only if coherent transition construction and stationary-state preparation preserve a meaningful complete advantage.

## What is worth doing first

1. **F15: Heston fast-forward assumption audit.** It directly attacks the existing repeated-step construction, and at least A1/A4 satisfy the readily checked eta threshold. No extrapolation to S4/B8 is justified.
2. **F08: bounded probability decomposition.** The identity is already derived; a tiny exact/numerical check and two-indicator cost ledger can determine whether it helps normalization and certification without a large circuit project.
3. **F20: control plus cost criterion.** Apply it to each proposed rewrite before dismissing shared controls or celebrating a variance plot.
4. **F06: active barrier-date switching diagnostic.** It identifies the remaining nonsmoothness in actual code and can sharpen the comparator with a small, isolated experiment.
5. **F04: structured residual integration.** Test a small smooth integral first; transfer to high-dimensional barriers is a separate question.

PDEs, rough models, SPDEs, Greeks and MCMC remain research branches with more substantial assumption or task changes. A successful component test earns further investigation; it does not by itself overturn the present no-advantage verdict.

## Source-check depth and open verification

Full text was opened and relevant theorem/algorithm passages checked for quantum Sobol integration, repeated nesting, Heston fast-forwarding, Poisson-conditioned Heston simulation, forward-PDE readout, SPDE/BDSDE quantum updates, the original Heston antithetic example, non-globally-Lipschitz antithetic MLMC, and the 2026 heavy-tail lower bound. Some older comparator and tensor/Greek sources were checked at their primary abstract/author-summary level only; their full transfer proofs were not audited. No claim of exhaustive literature search or complete proof review is made.

The strongest unresolved transfer checks are: the joint correlated-Heston law and all tail conditions in F15; an efficient finite-law mixture sampler and full error ledger in F08; applicability of smoothness classes in F04/F06; and complete readout/input-conditioning cost in F24/F25. These are deliberately separate small questions.
