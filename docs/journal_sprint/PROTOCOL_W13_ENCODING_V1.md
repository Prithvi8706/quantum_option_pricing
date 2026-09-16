# Week 13: finite Asian-basket encoding feasibility, v1

Development diagnostics only. Frozen before production; no confirmation data,
shot experiment, fitted coefficient, hardware execution or advantage test.

## Targets and fixed schedule

Discrete arithmetic Asian under existing Basket defaults: spot100, sigma.3,
rate.03, maturity1, correlation.5, strike100. Cases (assets,dates,bits/normal):
(1,2,1), (1,2,2), (1,2,3), (2,2,1), (2,2,2), (2,3,1).
One-asset cases are path-dependent diagnostics; 2-asset cases are baskets.
The week-11 classical pilot did not select a quantum precision: these are
prospectively selected feasibility sizes capped at eight state qubits plus flag.
They are NOT replacements for week-11's contractual 12/52 monitoring dates.
Cutoff L=3, tolerance $1; no selection after observing results.

Encode d=assets*dates independent standard normals with 2^q midpoint cells on
[-L,L]. Weights are exact-model Gaussian cell masses divided by cube mass,
evaluated numerically; coordinate zero uses the least significant register.
PCA maps independent normals to the contractual log-price covariance.
Raw F=D(A-K)+; sole alternative R=F-H, H=D(G-K)+, coefficient exactly1.
AM-GM gives 0<=R<=F: this choice avoids a signed range, without claiming that
a fitted beta>1 would also be nonnegative. No pilot/control fitting cost.
For either finite table scale=max(table), flag probability=value/scale.

Finite-grid reconstruction uses E_grid[H] as residual offset and must equal
E_grid[F]. Continuous-model approximation instead uses analytic E[H]. Record
both and their difference; they are not the same finite expectation.
Classical finite summation uses identical tables. Continuous-model RQMC uses
the same beta1 geometric control and raw payoffs, 16 independent scrambles of
4096 points per case, purpose-separated `week13_development_v1` streams.
Report all replicate means, standard errors across scrambles, per-scramble
descriptive path sample variances (not IID variance estimates under Sobol dependence)
and runtime; these numerical references are NOT certified truth or bias bounds.
Tests use distinct fixture contracts and TEST_ONLY namespace, never these streams.

## Circuit and cost checks

Compare two loaders for each of two representations in each case: dense generic
StatePreparation versus tensor-product one-dimensional StatePreparation.
Both feed the same full UCRY payoff table. Compile u/cx, optimization0,
seed13001, no connectivity constraint. Execute compiled exact statevectors,
check every joint flag/state probability against independently evaluated table
weights (absolute tolerance1e-10), compare the full intended positive-amplitude
state up to global phase (1-fidelity tolerance1e-10), and execute inverse back
to zero (1e-10). These floating diagnostics are not implementation error bounds.
Record loading, payoff, total A and inverse A resource counts separately.
Counts are logical arbitrary-angle gates, NOT Clifford+T, routed, noisy or
fault-tolerant resources. No nonzero-Grover experiment is claimed this week.
Compiler/statevector time is classical simulator time. Record setup/table and
classical summation times separately; no runtime speedup based on these timings.

## Componentwise error derivation

Let log S_i=mu_i+B_i Z, D=exp(-rT), C={all |Z_j|<=L}, p=P(C).
For any 0<=Y<=F<=D mean(S_i),

|E Y-E[Y|C]| <= D mean_i {E S_i sum_j[Phi(-L-B_ij)+Phi(-L+B_ij)]}
                    +(1-p)/p D mean_i E S_i.

First term uses Gaussian exponential tilting and union bound; second bounds
renormalization. E S_i=exp(mu_i+||B_i||²/2), p=(Phi(L)-Phi(-L))^d.
For midpoint spacing2L/2^q, coordinate displacement<=L/2^q. A cube-wide raw
Lipschitz bound is D mean_i[exp(mu_i+L||B_i||_1)||B_i||_1]. Multiply by L/2^q.
For R add the geometric bound D exp(mean(mu)+L||mean_i B_i||_1)
||mean_i B_i||_1 before multiplying by L/2^q. Call is1-Lipschitz.
This conservative bound is not a measured bias or a lower bound.
Raw/residual tail bounds can coincide despite smaller residual variance.

Ideal mathematical preparation and rotation would have zero implementation
error, but numerical state preparation, payoff arithmetic, rotation synthesis
and numerical enclosure are UNKNOWN for the implemented continuous-price
certificate. Observed statevector agreement does not set these to zero.
The analytic geometric offset's floating error also needs numerical enclosure.
GBM at contractual dates has no SDE time-step bias; continuous monitoring is a
different target. No model/calibration error against market data is certified.

Use PriceContract with missing components=None: planner must refuse admission.
Gate requires all component bounds justified and sum below$1 plus explicit
acquisition cost. Failing this gate is a valid completed feasibility outcome.

## Structured route and larger cases

Product Gaussian loading is executable here, costs O(d*2^q) generic 1D gates
and classical marginal setup O(2^q). It does NOT remove O(2^(dq)) payoff table
generation/rotations, nor imply polynomial accuracy dependence as q increases.
Assess reversible covariance/arithmetic/exponential/payoff computation as the
one structured extension; quantify dimensional/precision dependence and list
missing synthesized circuit/error constants. No fictitious large gate counts.
Charge forward work, flag rotation and inverse workspace computation, plus
A inverse and reflections if AE is later used. Any learned preparation needs
training and error accounting. Alternative Heston/nested audit is a bounded
sidecar, not a route substitution. No production expansion after results.

## Evidence and failure rules

Exclusive output directory, copied producing sources/protocol, hashes, versions,
fixed schedule, per-case and per-stage start/completion records, result rows
and final manifest atomically renamed after exclusive write, flush and fsync.
Completed setup/reference/circuit records survive a later-stage failure;
failed-stage elapsed time and unknown counts are explicit. Catchable interrupts
are recorded; process kill/power loss may leave only the last durable checkpoint.
Failures retain partial directory and failure marker; never label complete or
overwrite. Exact expected file inventory and source identity checked on replay;
recompute deterministic numerical results with environment-scoped tolerances.
Timings must be finite/nonnegative but are not replayed as identical. Exact
Python/NumPy/SciPy/Qiskit/platform/thread metadata must match the replay environment;
cross-environment replay requires a separate assessed procedure, not this verifier.
Independent final scientific and implementation reviews precede closeout.
