# Antithetic pricing feasibility acquisition

Frozen before the new measurements, 22 September 2026. This implements the
authorized feasibility gate from the research investigation. Existing papers,
pilots and archives are preserved. No held-out confirmation cases are opened.

## Financial contract and decision

Risk-neutral, equal-weight arithmetic Asian call, spot 100, rate .03, twelve
contractual dates. Numerical refinement leaves those dates fixed. Base model:
kappa=2, theta=v0=.09, xi=.3, leverage=-.5, equity correlation=.3, maturity 1,
strike 100, one/four assets. Additional development stress models: four assets,
theta=v0=.04, xi=.5, leverage=-.7 (Feller .64); eight assets, kappa=1.5,
theta=v0=.12, xi=.5, leverage=-.7, equity correlation=.6, maturity 2.
Correlations use the previous pilot's full joint covariance.

Final acceptance remains continuous-model absolute error .10/.03/.01 dollars,
99% per-price confidence, 10x latency versus best applicable classical method,
and the earlier unopened 24-case confirmation protocol. This acquisition can
reject a concrete implementation before that expensive stage. No favorable
empirical confidence interval or resource upper bound is a proof of advantage
or of impossibility for all quantum algorithms.

## Classical work

Implement native compiled path arithmetic; iid MC and scrambled Sobol; PCA in
asset covariance and Brownian bridge in time; independent geometric-GBM call
controls; analytic preintegration of a residual common price Brownian mode
conditional on the entire variance process. Compare ordinary and antithetic
multilevel corrections and allocate work including the base level. Training,
sampling, setup and compilation/startup are separately reported. Frozen sampling
roots: training 2026092301, acquisition 2026092302, reference 2026092303,
verification 2026092304. Case/method/level/replicate index child streams.
Start levels 0--5, 16 independent scrambles/batches at powers 8/10/12, escalating
only promising/uncertain points to 32 scrambles and higher powers. Full curves
may use a subset of levels with all omitted entries explicit. Retain raw results.
Use independent refinement and an independently discretized reference for
diagnostic bias checking. Neither doubling nor scheme agreement certifies bias.
Rigorous capped/finite-law checks must be separately identified if used.

## Quantum construction and estimation

Build real X/CX/CCX reversible arithmetic blocks, retaining emitted gate counts,
dependency depth and clean-workspace checks at small widths. Initial production
fraction precisions 24/32, with explicit signed integer headroom. Account for
sqrt, products, constant products, exp at monitoring dates, controls, payoff,
signed correction, inverse and controlled operations. Count Clifford+T using a
specified exact Toffoli decomposition; record physical scheduling assumptions.
Finite Gaussian preparation uses an explicitly charged one-dimensional
amplitude table or a fully specified alternative, never a free QRAM/full-path
table. A symmetric finite Haar hierarchy preserves level marginals and swap
symmetry; rounding mismatches enter the error ledger.

Use an executable dyadic signed second-moment mean-estimation schedule derived
from the explicit amplitude-estimation error inequality in Montanaro 2015,
Theorem 2 and Section 2, rather than an unknown big-O multiplier. Include every
bin/sign, integer AE size, failure amplification, reflection, preparation and
inverse. Distinguish empirical second moments from proved bounds; compare a
favorable idealized sigma/epsilon envelope with the constructed estimator.
Failure of the latter cannot reject all variance-sensitive algorithms.

## Physical/runtime and stop gates

Measure classical hardware/environment and memory. Report logical qubits,
T-count/T-depth, Clifford depth and circuit-memory policy. Sweep explicitly
hypothetical effective logical T layers 0.1/1/10 microseconds and factory rates;
they are not verified vendor capabilities. If favorable bounds for this concrete
construction already lose badly, stop its advantage development and do not open
confirmation. A claimed level-2 success requires complete code-distance,
factory, routing/decoder and failure analysis plus the full error ledger.
Missing proof obligations remain unresolved, not zero.

Deliverable: source-bound acquisition, tests, compiled blocks, actual estimator
schedules, classical/quantum crossover surfaces, and a decision with exact
scope and unclosed obligations. Workstation budget <=16 CPU-hours initially,
16 GiB; isolated optional dependencies under .context. No paid services.
