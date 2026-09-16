# Shortlist follow-through protocol

Frozen 2026-09-15 before stochastic benchmark observations. New work, not evidence
of quantum advantage. No positive-result threshold or retuning after results.

Asian basket: equal-weight assets 2/4; monitoring dates 12/52; strikes 90/100/110;
S0=100, sigma=.3, r=.03, maturity=1, asset equicorrelation=.5. Twelve contracts.
Exact GBM at contractual dates, no continuous-monitoring claim. Full-covariance
PCA Gaussian construction for raw paths. Conditional construction integrates
out the common terminal Brownian factor using the previously derived identity.

Methods: antithetic IID MC + geometric control (mc_cv); scrambled Sobol raw
(rqmc_raw); scrambled Sobol + geometric control (rqmc_cv); conditional scrambled
Sobol + conditional geometric control (conditional_cv). Each uses N=1024/4096
payoff evaluations and 8 independent repetitions per N. Total 768 estimate rows.
MC antithetic N means N/2 independent normal draws plus their negatives.

Fit each of the raw/conditional control coefficients on 1024 separate IID pilot
evaluations per contract. Reuse the frozen raw coefficient for mc_cv/rqmc_cv;
conditional_cv has its own separately trained coefficient. Charge pilot count
and time explicitly. Setup, estimation and reference timings kept separately.

Reference: 16 independent rqmc_cv scrambles of 8192 evaluations each, new RNG
namespace/purpose, not reused in training or main benchmark. Report reference
standard error; never call it exact truth or certified price. Target comparisons
use empirical deviation from that reference, labelled reference-relative RMSE.
RQMC uncertainty comes from independent scrambles, not within-net sample variance.
Any Student-t intervals are approximate. No binomial certificates on Sobol points.

PCA construction and scalar/geometric limits checked before acquisition. Normal
inverse endpoints clipped only to adjacent representable interior endpoints;
no formally rounded Gaussian tail/numerical error certificate claimed.
Conditional roots have a bounded bracket, explicit failure, 44 bisections and
saved maximum root residual; no silent unconverged output.

Heston: 72 deterministic combinations kappa=.5/2, theta=.04/.5, vol-of-vol=.2/.6,
rho=-.7/0/.3, Delta=1/12,1,3. Check ONLY displayed scalar truncation conditions
and eta>=5 from arXiv2602.03725v1, not full theorem applicability, market plausibility
or impossibility. No market parameters are fitted or changed to pass.

Nested negative control: Y~N(.2,1), X=Y+2Z, Z independent standard normal,
target E[(E[X|Y])+]. Closed-form inner and outer values make nesting unnecessary.
Record exact finite-inner bias for m=1,4,16,64,256; 8 independent simulations
with 2048 outer draws per m. Also record antithetic level corrections l=1..8
at 4096 independent outer draws each, with actual inner draws and nominal
payoff evaluations counted. This is a scalar exposure-style diagnostic, NOT
market CVA or implementation of the quantum nested algorithm.

Exclusive output, snapshots/hashes, retained failures, deterministic numeric
replay excluding elapsed timings. Single-thread numerical libraries for timing
comparability; no hardware or state-preparation resource advantage claim.
All streams use shortlist_v1 and purpose-separated identities.
