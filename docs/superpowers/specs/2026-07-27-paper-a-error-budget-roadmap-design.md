# Repository Specification: Eight-Week Paper A Error-Budget Study

Promoted from the approved /office-hours roadmap and all-angle review
Branch: main
Repo: Prithvi8706/quantum_option_pricing
Status: WRITTEN SPECIFICATION — AWAITING USER REVIEW
Mode: Builder

## Problem Statement

Paper A currently presents a 50-configuration by five-noise-level IQAE study as evidence that near-term QAE option pricing misses its theoretical break-even. The repository contains useful experiments and a complete manuscript, but the current evidence does not support the paper's strongest interpretation:

- the 250-row dataset has one stochastic result per configuration/noise pair;
- the reference path does not preserve continuous Black-Scholes, exact finite-grid, ideal finite-shot IQAE, and noisy IQAE prices as separate quantities;
- the reported noiseless mean error of about $0.203 is described as an irreducible discretization floor even though it may also contain IQAE, shot, payoff-approximation, and implementation effects;
- the existing oracle metric is not shot weighted;
- the one-qubit IBM experiment does not validate the complete option-pricing circuit or the synthetic noise model;
- figures, confidence intervals, provenance, and resource accounting are insufficient for a strong empirical paper.

The two-month project will replace the current headline-first study with a result-independent investigation of how support truncation, finite-grid discretization, circuit/payoff encoding, finite-shot IQAE estimation, synthetic gate noise, and physical circuit burden jointly determine delivered pricing accuracy.

## What Makes This Cool

The strongest version of Paper A does not merely report that noise increases error. It makes each layer of the QAE pricing pipeline measurable and auditable, then shows how improving one layer can worsen another. More uncertainty qubits may reduce finite-grid bias while increasing depth, two-qubit gates, shot-weighted A-equivalent invocations, Grover applications, and noise exposure. That accuracy-resource tradeoff is more useful than a single query-count break-even claim.

A small-dimensional arithmetic Asian option extension adds one bounded stress test: path dependence increases state dimension and reversible arithmetic costs, exposing whether conclusions drawn from a one-dimensional European payoff survive even the smallest path-dependent case.

## Constraints

- Paper A is the only manuscript in scope.
- The work has an eight-week horizon and is executed primarily by one researcher.
- European calls are the complete statistical benchmark.
- Arithmetic Asian calls are a small-dimensional stress test, not an equal second benchmark.
- Simulator experiments are the evidentiary core.
- IBM access is limited and supports narrow sanity checks only.
- Overnight local compute is available, but cloud/HPC capacity is not assumed.
- Paper B's RQMC and variance-reduction thesis remains separate.
- The deployed dashboard must remain stable.
- Venue selection and venue-specific formatting are deferred until evidence is frozen.
- No result, including the current $0.203 value, is protected from correction.

## Premises

1. **The existing Paper A is evidence to audit, not a manuscript to polish.** Its 250-row dataset and $0.203 interpretation cannot remain canonical without reconstruction.
2. **The publishable contribution is a preregistered empirical protocol for delivered finite-shot IQAE accuracy, not error decomposition by itself.** The paper separates support conditioning, finite-grid discretization, circuit/payoff encoding, estimator behavior, synthetic noise, failures, and total error; estimates procedure-level effects with replicated runs; and connects dollar-price accuracy to realized shot-weighted circuit burden over a fixed 50-contract benchmark. Week 1 must establish the specific distinction from prior European-call error-budget, noise, and resource studies before stochastic work begins.
3. **European calls carry the full statistical study.** Asian calls are bounded small-d stress tests with pilot stop conditions, not an equal second benchmark.
4. **Simulation carries the main evidence.** Limited IBM access supports narrow circuit-level checks only; it does not validate the full synthetic noise model.
5. **Physical burden must include shots.** Unweighted A-equivalent invocations, shot-weighted A-equivalent invocations, Grover applications, circuit depth, and shot-weighted gate burden are separate quantities.
6. **Paper A preserves Paper B's main thesis.** It uses analytic/exact references and basic Monte Carlo context, not a full RQMC or variance-reduction comparison.
7. **The research pipeline is isolated from the deployed dashboard.** Reproducibility takes priority over forcing scientific semantics into display-oriented code.
8. **Scope is controlled by predeclared feasibility gates.** n=5 stochastic promotion, any finite-shot/noisy d=2 work inside its five-day box, and larger hardware checks are earned by measured runtime/resource results rather than promised upfront. n=6 stochastic IQAE, d>2 Asian work, and mitigation are outside this roadmap.

## Approaches Considered

### Approach A: Error-Budget First

Rebuild the evidence around continuous, support-conditioned, exact finite-grid, exact circuit-encoded, ideal finite-shot IQAE, and noisy finite-shot IQAE prices. Add balanced independently seeded condition replicates, signed error identities, qubit scaling, full circuit/shot resource accounting, a bounded d=2 Asian stress test, and narrow hardware checks.

- Effort: Large
- Risk: Medium
- Strength: Clear causal story that remains publishable under mixed or negative results.
- Weakness: Requires rerunning most experiments and may weaken existing headline numbers.
- Reuses: European circuit construction, Black-Scholes code, existing option grid, noise-level ideas, manuscript structure, IBM access workflow.

### Approach B: Noise-Mitigation First

Make mitigation the main question by comparing unmitigated and mitigated pricing using readout mitigation, twirling, or zero-noise extrapolation.

- Effort: Large
- Risk: High
- Strength: Solution-oriented narrative with possible hardware relevance.
- Weakness: Mitigation multiplies execution cost and does not repair the missing error decomposition.
- Reuses: Current noisy simulator and hardware workflow.

### Approach C: Broad Benchmark Suite

Cover European, digital, and Asian payoffs across multiple noise channels and QAE variants.

- Effort: Extra large
- Risk: High
- Strength: Broad reusable benchmark dataset.
- Weakness: Produces breadth without one memorable causal result and is unlikely to reach equal validation depth in eight weeks.
- Reuses: Existing European, digital, Asian, and plotting code.

## Recommended Approach

Use Approach A. The paper's central question becomes:

> Over a fixed 50-contract European-call benchmark, how do support conditioning, finite-grid discretization, circuit/payoff encoding, finite-shot adaptive IQAE behavior, failures, controlled synthetic noise at n=3, and realized circuit-and-shot resource proxies determine delivered pricing accuracy, and which conclusions differ from query-only accounting?

The working title is:

> **Beyond Oracle Counts: An Empirical Error-Budget and Resource Analysis of Noisy Quantum Amplitude Estimation for Option Pricing**

The Asian subtitle is retained only if the Asian results contribute more than a resource table.

## Scientific Definitions

For option configuration x, qubit count n, replicate s, and noise specification eta, let A=[L,U], m=P(S_T in A), D=exp(-rT), and g(s)=(s-K)^+. The six-price ladder is:

- P_BS(x) = D integral_0^infinity g(s)f(s)ds: continuous, untruncated Black-Scholes price.
- P_support(x) = (D/m) integral_L^U g(s)f(s)ds: continuous payoff expectation conditional on the retained support, matching the normalization used by state preparation.
- P_grid(x,n) = D sum_i pi_i g(x_i): exact expectation under the frozen finite point grid and discrete probabilities, with the exact call payoff evaluated classically.
- P_circuit(x,n) = D h_x,n(a_sv): exact ideal-statevector circuit expectation, where a_sv is the marginal probability of the named objective qubit and h_x,n is the frozen payoff post-processing map.
- P_hat_ideal(x,n,s): the selected finite-shot IQAE procedure's raw point estimate after dollar post-processing, without synthetic gate noise.
- P_hat_noisy(x,n,eta,s): the same adaptive procedure's delivered point estimate under the specified synthetic noise model. This is a procedure output, not an assumed single physical noisy amplitude.

The support audit separately stores retained mass m, omitted probability 1-m, omitted discounted payoff C_tail = D integral_(A complement) g(s)f(s)ds, the normalization factor, and support-conditioning error. The exact identity P_BS = m P_support + C_tail is validated.

The finite-grid mathematics is frozen independently of the selected software environment. For 2^n points, x_i = L + i(U-L)/(2^n-1). The core European circuit uses normalized pointwise lognormal-density weights pi_i = f(x_i)/sum_l f(x_l), matching the intended Qiskit LogNormalDistribution semantics; integrated bin masses are not substituted silently. An independent implementation computes pi_i and a_calc = sum_i pi_i a_objective(x_i), which must agree with the circuit's statevector marginal a_sv.

Signed deterministic components are:

- e_support = P_support - P_BS
- e_grid = P_grid - P_support
- e_encode = P_circuit - P_grid

For each fixed configuration and n, stochastic effects are defined at the condition-mean level over independently seeded replicate sets:

- e_est_mean = E_s[P_hat_ideal] - P_circuit
- Delta_noise(eta) = E_s[P_hat_noisy(eta)] - E_s[P_hat_ideal]
- e_total_mean(eta) = E_s[P_hat_noisy(eta)] - P_BS
- e_total_mean = e_support + e_grid + e_encode + e_est_mean + Delta_noise

Per-run identities are checked only for valid complete records that share the same deterministic references; aggregate identities use identical included record sets. Absolute magnitudes are reported separately and are never stacked additively because signs can cancel.

The IQAE epsilon target is expressed in raw objective-probability units, not dollars and not square-root amplitude. `e_est_mean` includes finite-shot variation, estimator bias, and adaptive-stopping behavior; it is not described as deterministic algorithmic bias. Noisy IQAE intervals are called algorithm-reported intervals, and containment of P_circuit is diagnostic rather than calibrated coverage.

## Frozen Protocol Annex

This annex is normative. If prose elsewhere in this document is less specific, this annex controls. Any change to a frozen value requires a new protocol version before the affected output is inspected.

### A. European benchmark, strata, domain, and replacement rule

The benchmark is the Cartesian product of five target forward-moneyness values, five maturities, and two volatilities. For every row, `K=100`, `r=0.05`, dividends are zero, and

\[
m_F=\frac{S_0e^{rT}}{K},\qquad S_0=100m_Fe^{-0.05T}.
\]

`S0` is stored at the eight-decimal value shown below and is not recomputed from a rounded display value. The canonical row order is moneyness, then maturity, then volatility. Every row has analysis weight `1/50=0.02`; no result-dependent weighting is allowed.

| ID | S0 | K | r | T | sigma | m_F | M stratum | T stratum | vol stratum | weight |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| E001 | 79.00622404 | 100 | 0.05 | 0.25 | 0.15 | 0.80 | M1 deep OTM | T1 short | V1 low | 0.02 |
| E002 | 79.00622404 | 100 | 0.05 | 0.25 | 0.30 | 0.80 | M1 deep OTM | T1 short | V2 high | 0.02 |
| E003 | 78.02479296 | 100 | 0.05 | 0.50 | 0.15 | 0.80 | M1 deep OTM | T2 short | V1 low | 0.02 |
| E004 | 78.02479296 | 100 | 0.05 | 0.50 | 0.30 | 0.80 | M1 deep OTM | T2 short | V2 high | 0.02 |
| E005 | 76.09835396 | 100 | 0.05 | 1.00 | 0.15 | 0.80 | M1 deep OTM | T3 medium | V1 low | 0.02 |
| E006 | 76.09835396 | 100 | 0.05 | 1.00 | 0.30 | 0.80 | M1 deep OTM | T3 medium | V2 high | 0.02 |
| E007 | 74.21947891 | 100 | 0.05 | 1.50 | 0.15 | 0.80 | M1 deep OTM | T4 long | V1 low | 0.02 |
| E008 | 74.21947891 | 100 | 0.05 | 1.50 | 0.30 | 0.80 | M1 deep OTM | T4 long | V2 high | 0.02 |
| E009 | 72.38699344 | 100 | 0.05 | 2.00 | 0.15 | 0.80 | M1 deep OTM | T5 long | V1 low | 0.02 |
| E010 | 72.38699344 | 100 | 0.05 | 2.00 | 0.30 | 0.80 | M1 deep OTM | T5 long | V2 high | 0.02 |
| E011 | 88.88200204 | 100 | 0.05 | 0.25 | 0.15 | 0.90 | M2 OTM | T1 short | V1 low | 0.02 |
| E012 | 88.88200204 | 100 | 0.05 | 0.25 | 0.30 | 0.90 | M2 OTM | T1 short | V2 high | 0.02 |
| E013 | 87.77789208 | 100 | 0.05 | 0.50 | 0.15 | 0.90 | M2 OTM | T2 short | V1 low | 0.02 |
| E014 | 87.77789208 | 100 | 0.05 | 0.50 | 0.30 | 0.90 | M2 OTM | T2 short | V2 high | 0.02 |
| E015 | 85.61064821 | 100 | 0.05 | 1.00 | 0.15 | 0.90 | M2 OTM | T3 medium | V1 low | 0.02 |
| E016 | 85.61064821 | 100 | 0.05 | 1.00 | 0.30 | 0.90 | M2 OTM | T3 medium | V2 high | 0.02 |
| E017 | 83.49691377 | 100 | 0.05 | 1.50 | 0.15 | 0.90 | M2 OTM | T4 long | V1 low | 0.02 |
| E018 | 83.49691377 | 100 | 0.05 | 1.50 | 0.30 | 0.90 | M2 OTM | T4 long | V2 high | 0.02 |
| E019 | 81.43536762 | 100 | 0.05 | 2.00 | 0.15 | 0.90 | M2 OTM | T5 long | V1 low | 0.02 |
| E020 | 81.43536762 | 100 | 0.05 | 2.00 | 0.30 | 0.90 | M2 OTM | T5 long | V2 high | 0.02 |
| E021 | 98.75778005 | 100 | 0.05 | 0.25 | 0.15 | 1.00 | M3 ATM | T1 short | V1 low | 0.02 |
| E022 | 98.75778005 | 100 | 0.05 | 0.25 | 0.30 | 1.00 | M3 ATM | T1 short | V2 high | 0.02 |
| E023 | 97.53099120 | 100 | 0.05 | 0.50 | 0.15 | 1.00 | M3 ATM | T2 short | V1 low | 0.02 |
| E024 | 97.53099120 | 100 | 0.05 | 0.50 | 0.30 | 1.00 | M3 ATM | T2 short | V2 high | 0.02 |
| E025 | 95.12294245 | 100 | 0.05 | 1.00 | 0.15 | 1.00 | M3 ATM | T3 medium | V1 low | 0.02 |
| E026 | 95.12294245 | 100 | 0.05 | 1.00 | 0.30 | 1.00 | M3 ATM | T3 medium | V2 high | 0.02 |
| E027 | 92.77434863 | 100 | 0.05 | 1.50 | 0.15 | 1.00 | M3 ATM | T4 long | V1 low | 0.02 |
| E028 | 92.77434863 | 100 | 0.05 | 1.50 | 0.30 | 1.00 | M3 ATM | T4 long | V2 high | 0.02 |
| E029 | 90.48374180 | 100 | 0.05 | 2.00 | 0.15 | 1.00 | M3 ATM | T5 long | V1 low | 0.02 |
| E030 | 90.48374180 | 100 | 0.05 | 2.00 | 0.30 | 1.00 | M3 ATM | T5 long | V2 high | 0.02 |
| E031 | 108.63355805 | 100 | 0.05 | 0.25 | 0.15 | 1.10 | M4 ITM | T1 short | V1 low | 0.02 |
| E032 | 108.63355805 | 100 | 0.05 | 0.25 | 0.30 | 1.10 | M4 ITM | T1 short | V2 high | 0.02 |
| E033 | 107.28409032 | 100 | 0.05 | 0.50 | 0.15 | 1.10 | M4 ITM | T2 short | V1 low | 0.02 |
| E034 | 107.28409032 | 100 | 0.05 | 0.50 | 0.30 | 1.10 | M4 ITM | T2 short | V2 high | 0.02 |
| E035 | 104.63523670 | 100 | 0.05 | 1.00 | 0.15 | 1.10 | M4 ITM | T3 medium | V1 low | 0.02 |
| E036 | 104.63523670 | 100 | 0.05 | 1.00 | 0.30 | 1.10 | M4 ITM | T3 medium | V2 high | 0.02 |
| E037 | 102.05178350 | 100 | 0.05 | 1.50 | 0.15 | 1.10 | M4 ITM | T4 long | V1 low | 0.02 |
| E038 | 102.05178350 | 100 | 0.05 | 1.50 | 0.30 | 1.10 | M4 ITM | T4 long | V2 high | 0.02 |
| E039 | 99.53211598 | 100 | 0.05 | 2.00 | 0.15 | 1.10 | M4 ITM | T5 long | V1 low | 0.02 |
| E040 | 99.53211598 | 100 | 0.05 | 2.00 | 0.30 | 1.10 | M4 ITM | T5 long | V2 high | 0.02 |
| E041 | 118.50933606 | 100 | 0.05 | 0.25 | 0.15 | 1.20 | M5 deep ITM | T1 short | V1 low | 0.02 |
| E042 | 118.50933606 | 100 | 0.05 | 0.25 | 0.30 | 1.20 | M5 deep ITM | T1 short | V2 high | 0.02 |
| E043 | 117.03718944 | 100 | 0.05 | 0.50 | 0.15 | 1.20 | M5 deep ITM | T2 short | V1 low | 0.02 |
| E044 | 117.03718944 | 100 | 0.05 | 0.50 | 0.30 | 1.20 | M5 deep ITM | T2 short | V2 high | 0.02 |
| E045 | 114.14753094 | 100 | 0.05 | 1.00 | 0.15 | 1.20 | M5 deep ITM | T3 medium | V1 low | 0.02 |
| E046 | 114.14753094 | 100 | 0.05 | 1.00 | 0.30 | 1.20 | M5 deep ITM | T3 medium | V2 high | 0.02 |
| E047 | 111.32921836 | 100 | 0.05 | 1.50 | 0.15 | 1.20 | M5 deep ITM | T4 long | V1 low | 0.02 |
| E048 | 111.32921836 | 100 | 0.05 | 1.50 | 0.30 | 1.20 | M5 deep ITM | T4 long | V2 high | 0.02 |
| E049 | 108.58049016 | 100 | 0.05 | 2.00 | 0.15 | 1.20 | M5 deep ITM | T5 long | V1 low | 0.02 |
| E050 | 108.58049016 | 100 | 0.05 | 2.00 | 0.30 | 1.20 | M5 deep ITM | T5 long | V2 high | 0.02 |

The primary benchmark domain is European calls with `S0>0`, `K>0`, `r in [0,0.10]`, zero dividends, `T in [0.25,2.00]`, and `sigma in [0.15,0.30]`. The 50 rows above are the only stochastic benchmark inputs. Deterministic validation fixtures may sit exactly on a boundary or immediately outside it. Out-of-domain inputs fail with one of `NONPOSITIVE_SPOT`, `NONPOSITIVE_STRIKE`, `RATE_OUT_OF_RANGE`, `MATURITY_OUT_OF_RANGE`, `VOLATILITY_OUT_OF_RANGE`, `NONZERO_DIVIDEND_UNSUPPORTED`, or `UNSUPPORTED_PAYOFF`; no clamping is allowed in the research package.

Replacement is allowed only before E1 and only for a deterministic construction failure that is not repaired by correcting the implementation. Replacement never occurs because a row is slow, noisy, difficult, or unfavorable. The fixed replacement pool has one candidate per broad `(M stratum, T stratum, vol stratum)` cell. Its ID is `R-{M1..M5}-{S|M|L}-{V1|V2}`; target `m_F` is `{0.82,0.92,1.00,1.08,1.18}` for M1-M5, maturity is `{0.375,1.00,1.75}` for short/medium/long, volatility is `{0.18,0.27}` for V1/V2, and `S0=100m_F exp(-0.05T)` stored to eight decimals. The lowest lexical replacement ID in the same broad cell is used once. A second failure in that cell, or any replacement after E1 begins, forces a versioned benchmark amendment and a restart of E1; it is not silently substituted. The manifest records original ID, replacement ID, reason, approving protocol version, and pre-result timestamp. Weights remain 0.02 and are reassigned from the removed row to its replacement.

#### A.1 Frozen nested subsets `C12` and `C6`

Every stochastic run in this specification draws its contracts from `E001`-`E050`. No stochastic estimate, replicate mean, or cross-`n` comparison is ever computed on a contract outside that table.

The common cross-`n` subset is

```text
C12 = {E001, E006, E009, E014, E017, E022, E025, E030, E033, E038, E042, E049}
```

`C12` is balanced by construction: six `V1` and six `V2` rows; every maturity stratum `T1`-`T5` appears at least twice; and moneyness strata appear `M1:3, M2:2, M3:3, M4:2, M5:2`, with the two extra rows placed on deep OTM (largest relative error) and ATM (canonical case). `C12` is the single subset used for every subset claim in this document: the E2 Stage B pilot, the E3 `n=5` fallback matrix, the E4 common `n=3` versus `n=4` noise comparison, and the conditional common `n=3/4/5` comparison. Because `C12` is a subset of the full benchmark, every cross-`n` conclusion rests on contracts shared with the `n=3` full-50 result.

The calibration and conditional-realism subset is

```text
C6 = {E001, E014, E025, E030, E038, E049}
```

`C6` is a moneyness-by-maturity diagonal `(M1,T1), (M2,T2), (M3,T3), (M4,T4), (M5,T5)` plus one long high-volatility ATM row, giving three `V1` and three `V2` rows and covering all five moneyness and all five maturity strata. `C6` is a subset of `C12`. It is used for E2 Stage A shot-budget selection and for the conditional E4 backend-inspired noise snapshot.

The four `n=5` feasibility cells are

```text
N5 = {E001, E009, E030, E042}
```

a subset of `C12` occupying the four corners of the moneyness-by-maturity plane with balanced volatility strata: `E001` deep OTM/short/low volatility and `E009` deep OTM/long/low volatility span the low-amplitude, high-round-count regime that drives worst-case IQAE runtime; `E042` deep ITM/short/high volatility spans the high-amplitude regime; and `E030` ATM/long/high volatility carries the widest retained support. These four are a feasibility probe for runtime, memory, depth, and two-qubit count, not an accuracy claim, so they are selected for cost coverage rather than statistical balance.

`C6`, `N5`, and `C12` are frozen before E1 and are never reselected, extended, or reordered from observed results. The 12 `V01`-`V12` configurations defined in E0 are deterministic semantics and boundary fixtures only: they carry no stochastic benchmark claim, no replicate mean, and no cross-`n` comparison, and they are never substituted for `C12`, `C6`, or `N5`.

### B. Candidate software environments

Two isolated candidates are frozen. Neither changes the dashboard/runtime environment.

**Historical reconstruction candidate `paper-a-historical-py39-v2`:** Python 3.9.13; `qiskit-terra==0.46.3`; `qiskit-aer==0.12.2`; `qiskit-algorithms==0.3.1`; `qiskit-finance==0.4.0`; `numpy==2.0.2`; `scipy==1.13.1`. The `qiskit` metapackage is **absent** — only `qiskit-terra` is installed, and `import qiskit` resolves to the terra shim reporting `0.46.3`. `qiskit-ibm-runtime` and external transpiler plugins are absent.

*Amendment record (2026-07-29, pre-E1, before any affected output was inspected).* Version `v1` of this candidate declared `qiskit==0.45.3`, `qiskit-terra==0.45.3`, and `numpy==1.26.4`, and dismissed the README's Qiskit 0.46.3 reference as stale. That was inverted. The live `venv/` — captured verbatim in `research/paper_a/ENVIRONMENT_ACTUAL.json` — contains `qiskit-terra 0.46.3` and `numpy 2.0.2`. Its `pyvenv.cfg` is dated 2026-06-08 15:20, and `data/noise_sweep_results.csv` and `data/noise_sweep_expanded.csv` were written the same evening at 19:01 and 19:50, placing the environment 4.5 hours before the dataset it produced. `requirements-dev.txt` has been modified in exactly two commits, both at project inception, so its `qiskit==0.45.3` line is an unfulfilled pin that was never reconciled against the installed environment; `ROADMAP.md` line 52 repeats it. `README.md` lines 9 and 185 were correct. The existing datasets themselves carry no environment metadata of any kind, which is one of the provenance gaps this specification exists to close.

**Current paper candidate `paper-a-current-py312-v1`:** Python 3.12.10; `qiskit==2.4.2`; `qiskit-aer==0.17.2`; `qiskit-algorithms==0.4.0`; `qiskit-finance==0.4.1`; `qiskit-ibm-runtime==0.47.0`; `numpy==2.2.6`; `scipy==1.15.3`. External transpiler plugins, including `qiskit-ibm-transpiler`, are absent; core Qiskit preset pass managers are used. IBM jobs run from this isolated paper environment, not the deployed app environment.

A candidate is usable only if a clean lock install passes the semantic and instrumentation fixtures. If both pass, the current candidate is the primary paper environment and the historical candidate is the compatibility audit. If only the historical candidate passes, it becomes primary and current migration is reported as unresolved. If neither passes, implementation stops for a versioned spec amendment.

### C. European objective probability and dollar post-processing

The payoff rescaling factor is frozen at `c=0.25` for every shot-based run in this specification (E2, E3, E4, E6, E7). Because `E0` forces the state-preparation PMF to agree with the independently calculated `pi_i` to `1e-12`, `e_encode` is dominated by the `sin^2` linearization error, which is a direct function of `c`; `c` simultaneously sets the objective-amplitude span and therefore the shot cost of reaching a fixed `epsilon_target`. E1 therefore reports a deterministic-only sensitivity sweep over `c in {0.05,0.10,0.25,0.50}`. That sweep uses no shots, changes no stochastic run, and requires no new protocol version. Changing the frozen stochastic value away from `c=0.25` does require a versioned amendment before E2 outputs are inspected.

For support `[L,U]` with `L<K<U`, grid point `x_i`, and exact call payoff `g_i=max(0,x_i-K)`, define

\[
y_i=\frac{g_i}{U-K},\qquad
\theta_i=\frac{\pi}{4}(1-c)+\frac{\pi c}{2}y_i,\qquad
a_i=\sin^2(\theta_i).
\]

The independently calculated objective probability and statevector target are

\[
a_{calc}=\sum_i\pi_i a_i,\qquad a_{sv}=P(\text{named objective qubit}=1).
\]

The frozen inverse map is the Qiskit `LinearAmplitudeFunction` map

\[
h(a)=(U-K)\frac{2}{\pi c}\left(a-\frac12+\frac{\pi c}{4}\right).
\]

Therefore

\[
P_{circuit}=e^{-rT}h(a_{sv}),\qquad
\widehat P=e^{-rT}h(\widehat a),\qquad
CI_P=e^{-rT}[h(a_{lo}),h(a_{hi})].
\]

`h` is applied exactly once and discounting is applied exactly once. Raw `h(a)` and discounted values may be negative because of finite-shot estimation; they remain stored. A separately named `presentation_clipped_price=max(0,price)` may be shown but is never used for error, interval, completion, or failure calculations.

The selected IQAE point estimate is the raw objective-probability field `result.estimation`. The selected interval is the raw `result.confidence_interval` produced with IQAE `confint_method="beta"`, `epsilon_target=0.01`, and `alpha=0.05`. `result.estimation_processed` and `result.confidence_interval_processed` are stored only as cross-checks and must agree with the explicit `h` map before discounting to the frozen tolerance. No field named `mle`, `estimate`, or presentation-clipped output may substitute for the selected fields without a new protocol version.

### D. Streams, resampling, and stochastic inclusion

Every stochastic stream key is the UTF-8 string

```text
paper-a/v1 | namespace | experiment_uuid | phase | config_id | n | replicate | condition | purpose
```

with no whitespace normalization beyond the literal separators shown. `SHA-256(key)` is computed; the first 128 digest bits, interpreted as four big-endian unsigned 32-bit integers, initialize NumPy `SeedSequence`, and generators use `PCG64DXSM`. Python `hash()` is forbidden. Frozen namespaces are `paper-a/pilot/v1`, `paper-a/main/v1`, `paper-a/mc/v1`, and `paper-a/asian/v1`. Purposes include `shots`, `noise`, `bootstrap`, and `audit`. Ideal and every noise condition use independent shot streams; every noisy condition also uses an independent noise stream. Pilot and main namespaces never overlap. Transpilation is deterministic and uses the separate fixed seed `20260727`.

Primary intervals use `B=10,000` resamples. Within each contract and condition, valid first-attempt replicates are sampled with replacement to their observed included count, condition means are recomputed, and the fixed 50 equal-weight contract mean is then formed. Ideal and noisy replicates are resampled independently. For simultaneous noise-response bands, one ideal resample is shared across the four noise levels while each noisy condition is independently resampled. Configurations are never resampled for the primary interval. Any configuration bootstrap is labeled finite-benchmark sensitivity.

A first planned attempt is `complete` only when IQAE returns, the selected raw estimate and interval are present, all sampler invocations have finalized records, and the run record is durably appended. A complete record is `valid` only when the estimate is finite and in `[0,1]`, the interval is finite and ordered with `0<=lo<=hi<=1`, deterministic references and hashes pass, each recorded invocation has a positive integer effective-shot count, and `actual_*` and `reconstructed_*` provenance rules are satisfied. Retries are never primary observations.

For fixed main-run replicate count `R`, a numerical condition mean requires at least `R_min=max(8,ceil(0.8R))` valid first-attempt records in that `(config,n,condition)` cell. Every contract used by a primary or common-subset numerical claim must meet `R_min`; otherwise that numerical claim is withheld and only completion/failure plus the frozen missing-outcome bounds are reported. The E2 GO gate requires at least 90% first-attempt completion, at least 90% valid records, no more than 5% invalid intervals, and no more than 10% exceptions in every required pilot wave and every n=5 promotion condition. Completion and failure summaries always use all first planned attempts, including invalid and missing outcomes.

### E. Compute, resource, and promotion thresholds

One overnight-equivalent is exactly 10 wall-clock hours on the designated local machine with no concurrent paper experiment. The E2 pilot stops at 24 wall-clock hours. The main gross budget is 140 hours and the schedulable budget is 105 hours; at least 35 hours remain reserve. Projection uses the one-sided 95% upper confidence bound of the median observed per-attempt runtime within each `(n,condition)` resource stratum, multiplied by planned attempts, plus 15% orchestration overhead.

| Gate | Frozen threshold |
|---|---|
| Worker peak memory | no attempt may exceed 70% of physical RAM; promotion requires p95 <=60% |
| n=3 first-attempt wall time | p95 <=10 minutes |
| n=4 first-attempt wall time | p95 <=30 minutes |
| n=5 first-attempt wall time | p95 <=45 minutes and maximum <=60 minutes |
| Executed ISA depth, n=3/4 | maximum per invocation <=100,000 |
| Executed ISA two-qubit gates, n=3/4 | maximum per invocation <=50,000 |
| Circuit-shots, any core attempt | `sum_j effective_shots_j <=262,144` |
| Per-invocation shots | one of `{512,2048,8192}` in E2; the selected value is fixed for E3/E4 and never exceeds 8192 |
| Required E3/E4 projection | all mandatory n={3,4} ideal and n=3 controlled-noise work must fit <=105 hours and <=70% RAM |
| Valid records per cell | `R_min=max(8,ceil(0.8R))` |
| Pilot/main first-attempt completion | >=90% per required wave/condition |
| Pilot/main exception rate | <=10% per required wave/condition |
| Invalid interval rate | <=5% per required wave/condition |

The four n=5 pilot configurations are the frozen Annex A.1 set `N5={E001,E009,E030,E042}`. Full-50 n=5 ideal promotion requires every n=5 ideal, `p=1e-3`, and `p=1e-2` pilot condition to meet the valid-record/completion/failure gates; no OOM or deterministic repeated failure; p95 runtime <=45 minutes; maximum runtime <=60 minutes; p95 memory <=60%; maximum executed depth <=75,000; maximum executed two-qubit count <=40,000; circuit-shots <=262,144 per attempt; and a full-50 ideal projection <=35 hours. If all technical gates pass but the 35-hour projection fails, n=5 is restricted to the frozen 12-contract benchmark subset `C12`. If any technical gate fails, n=5 stochastic IQAE is not promoted. n=6 remains deterministic/template-only.

### F. Controlled synthetic-noise ISA contract

The controlled family uses the exact simulator ISA basis `['rz','sx','x','cx','measure']`, all-to-all connectivity, no initial layout, no routing, translation by the core Qiskit translator, optimization level 1, no approximation, no scheduling, and `seed_transpiler=20260727`. Each measured logical IQAE round circuit is transpiled once. The recorded ISA QPY bytes and hash are the circuit executed by Aer; primitive-side or backend-side retranspilation is disabled. A run is invalid if the executed circuit hash differs from the recorded ISA hash.

For each `p in {1e-4,1e-3,5e-3,1e-2}`, construct Qiskit Aer errors with `depolarizing_error(p,1)` on every `sx` and `x` instruction and `depolarizing_error(p,2)` on every `cx` instruction. Store `p_1q=p` and `p_2q=p` separately. `rz` is treated as a virtual instruction and receives no channel. `measure`, reset, delay/idle, barrier, initialization, and classical instructions receive no channel. Readout error, thermal relaxation, coherent over-rotation, leakage, crosstalk, correlated error, drift, and calibration-derived channels are excluded. Any ISA instruction outside the frozen basis, any intended `sx`/`x`/`cx` without the matching channel, any channel on an excluded instruction, or any second transpilation fails validation. This model is called `controlled_uniform_depolarizing_v1`, never hardware realistic.

### G. Naive Monte Carlo context

The empirical sample-count grid is exactly `N in {256,1024,4096,16384,65536}` with 30 independent replications per contract and N. Streams use the frozen `paper-a/mc/v1` derivation with the N value included in `condition`; samples are not nested across N. The dollar-target grid is exactly `tau in {$1.00,$0.50,$0.25,$0.10,$0.05,$0.01}`.

For discounted payoff `Y=e^{-rT}(S_T-K)^+`, calculate its exact variance from lognormal truncated moments. With

\[
M_m=E[S_T^m1_{S_T>K}]=S_0^m e^{mrT+\frac12m(m-1)\sigma^2T}
\Phi\left(\frac{\ln(S_0/K)+(r+(m-\frac12)\sigma^2)T}{\sigma\sqrt T}\right),
\]

use `E[g]=M_1-K M_0`, `E[g^2]=M_2-2KM_1+K^2M_0`, and `v_i=e^{-2rT}(E[g^2]-E[g]^2)`. The equal-weight benchmark RMSE is

\[
RMSE_N=\sqrt{\frac1{50}\sum_i\frac{v_i}{N}},
\]

and the analytic sample count for target `tau` is `N_tau=ceil((1/50)sum_i v_i/tau^2)`. The empirical grid validates the `N^-1/2` trend and estimator implementation; it does not choose `N_tau` by the first noisy crossing. No antithetic variates, control variates, stratification, importance sampling, RQMC, wall-clock speedup, or sample-to-oracle equivalence appears in Paper A.

### H. Conditional d=2 Asian protocol

The only Asian contract is the one already specified at `S0=K=100`, `r=0.05`, `sigma=0.20`, `T=1`, with dates `{0.5,1.0}` and no `S0` in the average. It uses exactly three uncertainty qubits per date: `n1=n2=3`, six joint-state qubits total. The total joint-tail budget is `q_joint=1e-4`. Allocate `q_joint/(2d)=2.5e-5` to each marginal tail and define

\[
L^*=\min(F_{0.5}^{-1}(2.5\times10^{-5}),F_1^{-1}(2.5\times10^{-5}),0.98K),
\]
\[
U^*=\max(F_{0.5}^{-1}(1-2.5\times10^{-5}),F_1^{-1}(1-2.5\times10^{-5}),1.02K).
\]

The retained event is jointly `[L*,U*]^2`, not two independently normalized marginals. The exact bivariate lognormal probability on that rectangle is `m_joint`; total omitted mass is `1-m_joint`; omitted discounted payoff integrates the arithmetic-call payoff over the full complement. The construction must satisfy `1-m_joint<=1e-4`, omitted discounted payoff `<=0.0001*S0=$0.01`, and absolute support-conditioning bias `<=0.0001*S0=$0.01`.

With `Delta=(U*-L*)/7`, encode `S_t=L*+Delta*j_t`, `j_t in {0,...,7}`. `WeightedAdder` weights are `[1,2,4,1,2,4]`, producing `z=j_1+j_2 in {0,...,14}` on four sum qubits; the average is exactly `L*+(Delta/2)z`. The frozen logical budget is 15 qubits: six state, four sum, four adder ancillas, and one objective. A construction requiring more than 15 logical qubits, more than four ancillas, or a different arithmetic scale fails the day-3 gate rather than silently changing encoding.

By the end of working day 3, the implementation must have: independently calculated normalized joint pointwise probabilities; statevector PMF L1 error `<=1e-10`; objective-probability error `<=1e-10`; discounted price round-trip error `<=1e-8` dollars; all joint-tail gates passing; logical qubits `<=15`; transpiled depth `<=75,000`; transpiled two-qubit gates `<=40,000`; peak memory `<=60%`; and combined construction, transpilation, and statevector runtime `<=2 hours`. The projected remaining finite-shot work must fit `<=16 hours` across days 4-5 and the core circuit-shot limit. Only then may the extension run ideal finite-shot IQAE and at most one selected noisy condition, `p=1e-3`, using the E2-selected shot policy and 10 replicates. Otherwise E6 stops at the deterministic resource result or is omitted. No d>2 construction or estimate is permitted.

### I. Recording sampler/transpiler contract

The preferred adapter is an ordered append-only `RecordingSampler` coupled to one frozen transpilation service. For every IQAE primitive call it must record before execution: invocation ordinal, requested shots, effective shots, selected Grover power, logical measured-circuit QPY bytes/hash, objective and classical-bit mapping, algorithm metadata, and stream IDs. The transpilation service then records the full compilation contract, exact ISA QPY bytes/hash, depth and operation counts, and returns that same ISA circuit to Aer. After execution the adapter appends counts or quasi-distribution, primitive metadata, timing, status, and any exception. If an exception occurs, all completed invocation records and the failing invocation's available logical/ISA resources remain durable.

The adapter proves Grover-power identity by an audited map from each IQAE-constructed logical circuit to `construct_circuit(problem,k,measurement=True)` fixtures. It does not infer k from circuit depth. An initial sentinel zero in `result.powers` is excluded unless a recorded sampler invocation proves that `k=0` was actually submitted; repeated powers remain separate invocations. Effective shots come from the primitive call/result metadata, not from the configured default.

The only permitted fallback is `reconstructed-only-v1`. After IQAE completes, observed powers are reconstructed with `construct_circuit(problem,k,measurement=True)` under the frozen environment and transpilation contract. These populate only `reconstructed_logical_*`, `reconstructed_isa_*`, and `reconstructed_resource_*`; every `actual_circuit_*`, `actual_isa_*`, and `actual_gate_*` field is null. Reconstructed circuits cannot support claims about submitted depth, submitted gates, noise coverage of the actual circuit, shot-weighted gate burden, or an executed Pareto frontier. If effective shots and actual completed powers are exposed, `M_A_logical`, `M_A_executed`, and `M_Q_executed` may still be reported with provenance `observed_power_shot_only`; otherwise only template resource curves are allowed. No mixed actual/reconstructed record may pass validation.

## Research-Package Architecture

Paper A receives an isolated package:

```text
research/paper_a/
├── README.md
├── config.py
├── schema.py
├── references.py
├── noise.py
├── resources.py
├── statistics.py
├── validation.py
├── european/
│   ├── circuits.py
│   └── experiment.py
├── asian/
│   ├── circuits.py
│   └── experiment.py
├── configs/
│   ├── pilot.json
│   ├── european_main.json
│   ├── asian_pilot.json
│   └── hardware_validation.json
├── scripts/
│   ├── run_experiment.py
│   ├── validate_results.py
│   ├── aggregate_results.py
│   └── generate_figures.py
└── tests/
    ├── test_references.py
    ├── test_error_budget.py
    ├── test_resources.py
    ├── test_reproducibility.py
    └── test_smoke_pipeline.py
```

Generated artifacts are versioned under `data/paper_a/`, `figures/paper_a/`, and a new manuscript directory. Existing datasets and manuscripts remain historical inputs and are not overwritten.

### Component boundaries

- `config.py`: validates immutable JSON experiment configs.
- `schema.py`: defines versioned raw result and resource records.
- `references.py`: calculates the continuous, finite-support, exact-grid, and exact circuit-encoded reference ladder independently of IQAE sampling.
- `noise.py`: defines named synthetic and backend-inspired noise specifications.
- `resources.py`: instruments actual IQAE round circuits and calculates logical and shot-weighted burden.
- `statistics.py`: computes independent-condition estimands, within-configuration resampling intervals, completion/failure summaries, strata, and resource-proxy frontiers independently of plotting.
- `validation.py`: enforces probability, unit, balanced replicate-condition key, error-identity, schema, and dataset-completeness gates.
- `european/`: complete pricing benchmark.
- `asian/`: bounded small-d construction and feasibility experiments.

### Environment and instrumentation decision

The exact historical and current candidates, selection outcomes, package exclusions, recording adapter, and reconstructed-only fallback are frozen in Annex B and Annex I. The existing `venv/` is evidence to reconstruct, not an accepted lock. Selection is based on agreement of public scientific semantics rather than gate-for-gate identity: support probabilities, objective probability, payoff transfer function, dollar post-processing, selected logical `Q^k A` action, and fixed resource fixtures. A migration is rejected if it changes `pi_i`, the encoded objective transfer function, or the post-processing map without a new protocol version. The dashboard environment is unchanged.

Stock IQAE does not expose a caller-configurable maximum-round cap or a complete round-circuit log. The study records the implementation's internal confidence-allocation bound and actual completed invocations but does not claim `maximum-round termination`. A hard cap is outside this spec unless an audited local IQAE implementation receives a separate approved amendment.

## Canonical Result Record

Each raw run records at least:

- schema, experiment, first-planned-attempt, run, configuration, and deterministic stream-namespace identifiers;
- Git commit, config hash, complete environment lock, package versions, and UTC timestamp;
- payoff type and all financial parameters;
- monitoring dimension and uncertainty qubits;
- support rule and bounds, retained mass, omitted mass, omitted discounted payoff, support-conditioning bias, exact grid points and pointwise probabilities, payoff scaling, and distribution normalization;
- raw objective probability, raw processed payoff, raw dollar price, and any separately labeled presentation-clipped value;
- noise model name, full channel parameters, calibration source, replicate index, simulator/shot/noise stream identifiers, and transpiler seed;
- IQAE epsilon target in raw objective-probability units, alpha, implementation-specific internal round bound, shot policy, effective shots for each recorded sampler invocation, interval validity, and algorithm-reported interval;
- all deterministic reference layers plus ideal/noisy procedure outputs and condition-mean error components;
- actual recorded sampler invocations, Grover powers, circuits and stopping metadata where the adapter exposes them; otherwise explicitly labeled reconstructed fields;
- logical/ancilla qubits and per-recorded-round pre/post-transpilation resources;
- unweighted and shot-weighted A/A-inverse-equivalent invocations, Qiskit-compatible Grover applications, maximum executed depth, and shot-weighted 1q/2q gate burden;
- completion state, first-attempt validity, retry linkage, runtime, status, failure stage, exception class, and error message.

Inapplicable or unavailable fields are explicit nulls with provenance. Retries never overwrite the first planned attempt, reconstructed circuits never populate `actual_*` fields, and no scientific field is inferred later from a filename.

## Data Flow

```text
immutable JSON config
        |
        v
configuration and feasibility validation
        |
        v
stratified option enumeration
        |--------------------> untruncated continuous reference
        v
finite-support selection
        |--------------------> support-conditioned reference + tail audit
        v
finite grid and exact payoff construction
        |--------------------> exact finite-grid expectation
        v
ideal state-preparation + payoff circuit
        |--------------------> exact statevector circuit expectation
        v
IQAE problem construction
        |--------------------> actual recorded round-circuit instrumentation or explicitly reconstructed-only fallback
        v
balanced independently seeded ideal finite-shot replicate set
        v
balanced independently seeded noisy finite-shot replicate sets
        v
append-only raw + resource JSONL
        v
checkpoint/resume and failure accounting
        v
scientific dataset validation
        v
independent-condition statistical aggregation
        v
frozen CSV tables + figures + claim-evidence audit
```

Each experiment directory contains its immutable config, manifest, environment snapshot, append-only raw records, failures, resources, aggregate tables, validation report, hashes, and a `COMPLETE` marker. Frozen runs are never overwritten.

Run states are explicit: `planned -> running -> partial -> validated -> frozen`, with `failed` available from any active state. Every stochastic job has an idempotency key derived from experiment UUID, phase, configuration, n, replicate, condition, and purpose. Resume skips only schema-valid completed keys; an interrupted or failed first attempt remains visible and any retry receives a linked attempt identifier.

The transpilation cache key hashes versioned QPY bytes of the complete measured logical round circuit; Qiskit, Aer, Algorithms, and transpiler-plugin versions; a canonical compilation-target snapshot including instruction/qubit tuples, coupling, durations, error properties, timing constraints, and dt; optimization, initial-layout, layout, routing, translation, synthesis, approximation, and scheduling settings; and the transpiler seed. Resource records are reusable only when this full key matches. Shots, counts, adaptive-round order, noise condition, execution metadata, and failures remain run-specific and never come from the transpilation cache.

## Experiment Program

### E0: Reference and semantics validation

Purpose: prove that support, grid, state preparation, payoff encoding, units, post-processing, and discounting are correct before stochastic experiments.

The fixed 12-configuration validation set uses K=100 and r=0.05:

| ID | S0 | T | sigma | Role |
|---|---:|---:|---:|---|
| V01 | 80 | 0.25 | 0.20 | deep OTM, short |
| V02 | 80 | 1.00 | 0.30 | deep OTM, high volatility |
| V03 | 90 | 0.50 | 0.15 | OTM, low volatility |
| V04 | 90 | 2.00 | 0.30 | OTM, long/high volatility |
| V05 | 100 | 0.25 | 0.15 | ATM, short/low volatility |
| V06 | 100 | 0.50 | 0.20 | ATM, medium maturity |
| V07 | 100 | 1.00 | 0.20 | canonical ATM |
| V08 | 100 | 2.00 | 0.30 | ATM, long/high volatility |
| V09 | 110 | 0.25 | 0.15 | ITM, short/low volatility |
| V10 | 110 | 1.00 | 0.25 | ITM |
| V11 | 120 | 0.50 | 0.20 | deep ITM |
| V12 | 120 | 2.00 | 0.30 | deep ITM, long/high volatility |

The supported domain, named validation errors, exact 50-contract benchmark, equal weights, construction rule, strata, and replacement audit are frozen in Annex A. Inputs outside that domain are rejected rather than silently clamped. Separate deterministic fixtures cover strike exactly on and between grid points, objective probabilities near 0 and 1, zero-payoff retained support, values immediately below and above the `T=0.25` and `sigma=0.15` minima, payoff scaling near its upper bound, zero synthetic noise, and invalid or degenerate inputs.

The support rule treats q_total as the total two-tail probability budget and is fixed across n for each configuration: L=min(F^-1(q_total/2),0.98K), U=max(F^-1(1-q_total/2),1.02K). The pilot compares q_total in {1e-2,1e-3,1e-4}, with predeclared wider fallbacks {1e-5,1e-6} if no candidate passes. It freezes the least-wide rule satisfying all three conditions across the 12 validation contracts and then all 50 final contracts: omitted probability 1-m <=1e-4; exact omitted discounted payoff C_tail <=0.01% of S0; and actual support-conditioning bias |P_support-P_BS| <=0.01% of S0. Tail probability, omitted payoff, normalization factor, support price, and support bias are stored separately.

For the selected support, the independent grid implementation freezes x_i=L+i(U-L)/(2^n-1) and normalized pointwise lognormal-density probabilities pi_i=f(x_i)/sum_l f(x_l). It does not infer a reference from circuit amplitudes or replace the point rule with integrated bin masses. The state-preparation probabilities must independently agree with pi_i, and the calculated objective probability a_calc must agree with the statevector marginal a_sv. P_support, P_grid, and P_circuit are cross-checked separately for n in {2,3,4,5}.

Additional gates:

- probability normalization residual <=1e-12;
- independently calculated and circuit PMFs agree with max elementwise error <=1e-12 and L1 error <=1e-10;
- calculated and statevector objective probabilities agree within 1e-10;
- payoff post-processing, discounting, and dollar round-trip residuals are <=1e-10*max(1,S0);
- discount is applied exactly once;
- raw and presentation-clipped values remain separate;
- signed error-identity residual is <=1e-10*max(1,S0);
- values below the frozen T/sigma minima are rejected with named validation errors;
- legacy and selected paper environments agree on the frozen public semantic outputs after documented API differences.

These deterministic tolerances are frozen. Tightening or loosening any value requires a versioned amendment before E1 outputs are inspected. Gate: no stochastic experiment starts until all reference, instrumentation, unit, and environment checks pass.

### E1: European reference-layer scaling

- the exact Annex A 50-row European table, IDs `E001`-`E050`, forward-moneyness definition, strata, equal 0.02 weights, supported domain, deterministic replacement pool, and replacement audit rule;
- the 12 `V01`-`V12` validation configurations are disjoint from the 50-contract benchmark by construction, because every benchmark `S0` is `100m_Fe^{-0.05T}` and every validation `S0` is a round value in `{80,90,100,110,120}`. The validation set carries deterministic semantics and boundary coverage only; every stochastic and subset claim uses `E001`-`E050`, `C12`, `C6`, or `N5` from Annex A.1;
- n in {3,4,5,6};
- compute P_BS, P_support, P_grid, and P_circuit without IQAE shots;
- report signed and absolute support, grid, and encoding errors;
- summarize the complete fixed benchmark with mean, median, quantiles, range, worst case, and strata by moneyness, maturity, and volatility;
- do not present bootstrap intervals as population inference over a market distribution. Any resampling of configurations is labeled a finite-benchmark sensitivity analysis;
- report omitted probability and payoff contribution for every configuration;
- run a support-rule sensitivity check on the 12 validation configurations;
- run a deterministic payoff-rescaling sensitivity sweep over `c in {0.05,0.10,0.25,0.50}` on `C12` at `n in {3,4}`. For each `c` report signed and absolute `e_encode`, the objective-amplitude span `max_i a_i - min_i a_i`, and the resulting shot-cost proxy for a fixed `epsilon_target`. This isolates the encoding-accuracy versus estimation-cost tradeoff using statevector evaluation only, with no shots and no change to the frozen stochastic value `c=0.25`.

This experiment replaces the unsupported use of p=0 IQAE error as a discretization floor and determines whether support, grid, or circuit encoding dominates before IQAE sampling begins. The `c` sweep answers the reviewer question of why the frozen rescaling factor is defensible, and supplies a second worked instance of the paper's central claim that improving one layer can degrade another.

### E2: IQAE shot, replicate, and feasibility pilot

Purpose: freeze the main stochastic design from measured circuit-shots, runtime, variance, ideal-target containment, completion/failure behavior, and resource growth.

IQAE is fixed at epsilon_target=0.01 in raw objective-probability units and alpha=0.05 for the pilot. The manuscript never converts this directly to $0.01. Stock IQAE has no caller-frozen maximum-round cap; the selected implementation's internal confidence-allocation bound, actual sampler invocations, and any audited local cap are recorded under distinct names.

Stage A compares fixed per-circuit shot budgets {512,2048,8192} on the frozen Annex A.1 subset `C6={E001,E014,E025,E030,E038,E049}`, n in {3,4}, five replicates, ideal simulation, and synthetic p=1e-3. Stage B runs the selected shot budget on the frozen Annex A.1 subset `C12` at n in {3,4}, plus the four frozen n=5 feasibility cells `N5={E001,E009,E030,E042}`, with 10 replicates under ideal, p=1e-3, and p=1e-2 conditions. Both stages run on benchmark contracts under the separate `paper-a/pilot/v1` namespace; no pilot record is reused as a main-run observation. The pilot executes in predeclared waves. After each wave, the remaining matrix is projected against the 24-hour cap; later waves do not start if the cap would be exceeded, and the missing cells remain documented rather than replaced post hoc.

Each first planned attempt stores raw `result.estimation`, raw beta-method `result.confidence_interval`, explicit Annex C dollar post-processing, ideal-target containment, invalid intervals, exceptions, every recorded sampler invocation, effective shots, completed Grover powers, and consumed resources. Completion probability is a co-primary outcome. Retries are linked sensitivity attempts and never replace failed primary attempts. A numerical `Delta_noise` claim requires Annex D's `R_min` in every included cell; otherwise only completion/failure and bounded sensitivity results are reported. Noisy interval containment is diagnostic and is not called calibrated coverage.

For replicate selection define D_i,eta=(mean_s P_hat_noisy(i,eta)-mean_s P_hat_ideal(i))/S0_i from independently estimated condition means, and define mu_eta=(1/50)sum_i E[D_i,eta]. The primary precision target is a 95% interval half-width <=0.001 for mu_eta at n=3 and p=1e-3. Ideal and noisy replicates are independently resampled within each configuration; configurations are not resampled for the primary interval. The selected R is the smallest fixed value in {10,15,20,30} whose conservative stratum-variance projection meets that target. Pilot and main-run stream namespaces are separate. If R=30 does not meet the target, the precision claim is dropped rather than compute expanded.

The pilot and main-run limits are Annex E's exact thresholds: a 24-hour pilot cap, 70% absolute memory ceiling, 10-hour overnight-equivalent, 140-hour gross budget, 105-hour schedulable budget, fixed runtime/depth/two-qubit/circuit-shot limits, `R_min`, and exact n=5 promotion rules.

This is a hard stop/go gate. If the minimum required E3 n={3,4} all-50 matrix and E4 n=3 all-50 controlled-noise matrix cannot fit the gross compute cap at the minimum allowed shot and replicate policy, E3/E4 do not begin. The benchmark or noise grid is not silently reduced. Gate: the main matrix, shot policy, replicate count, completion/failure rules, common comparison subsets, n=5 fallback, instrumentation contract, and numerical resource thresholds are frozen before E3 or E4.

### E3: European ideal IQAE study

Required matrix:

- all 50 configurations at n in {3,4};
- the fixed replicate count and shot policy selected by E2;
- finite-shot ideal simulation;
- compare P_hat_ideal condition means against P_circuit;
- record aggregate ideal-target containment, estimator bias, variance, first-attempt completion/failures, exceptions, actual recorded sampler invocations or reconstructed-only fallback fields, Grover powers, effective shots, and resources.

The full n=5 matrix is included only if the `N5` E2 cells pass the frozen wall-time, memory, depth, two-qubit, failure-rate, and circuit-shot gates. Otherwise the frozen Annex A.1 subset `C12` is used, so that every n=5 contract is also present in the n=3 and n=4 matrices. n=6 remains exact-reference and template-circuit construction only unless IQAE is actually promoted. Without an executed adaptive run, n=6 reports A, Q, and selected Q^kA template resources, not adaptive-round counts, shot-weighted burden, or a Pareto-frontier point.

### E4: Main synthetic noise study

Core matrix:

- all 50 configurations at n=3;
- the fixed independently seeded replicate sets from E2;
- controlled uniform depolarizing rates p in {1e-4,1e-3,5e-3,1e-2};
- reuse the frozen E3 ideal records whenever configuration, n, replicate namespace, shot policy, logical/ISA circuit hash, and environment match; rerun only a predeclared audit sample for cross-batch reproducibility;
- the controlled model sets p_1q=p_2q=p for continuity with the historical study, stores them separately, and never calls the model hardware realistic;
- measurement/readout, reset, idle, thermal relaxation, coherent, leakage, crosstalk, and correlated errors are excluded from this controlled family and listed explicitly.

Scaling subsets and estimands:

- full-50 n=3 controlled-noise result;
- `C12` n=3 versus n=4 subset result, using the frozen Annex A.1 subset for both n values so the comparison is exactly matched by contract;
- the same `C12` set extended to n=3/4/5 only if n=5 passes every promotion gate;
- one conditional backend-inspired snapshot model on the frozen Annex A.1 subset `C6`, with a saved compilation target and execution-time properties where available.

Each round circuit follows Annex F exactly: basis `rz/sx/x/cx/measure`, all-to-all controlled-simulator target, optimization level 1, seed 20260727, one transpilation, QPY/hash identity at execution, Qiskit Aer depolarizing channels on `sx`, `x`, and `cx`, and all named exclusions. Validation fails on missing channels, excluded-operation channels, basis mismatch, hash mismatch, or second transpilation. The controlled sweep supports causal sensitivity; the backend-inspired subset supports limited realism and is never conflated with it. Cross-n conclusions use only common contracts and a common normalized accuracy metric.

### E5: Resource frontier

For every actually recorded IQAE sampler invocation j with submitted circuit C_j=Q^k_j A and effective shots N_j, report:

- number of distinct logical and ISA circuits and actual invocations;
- Grover powers and shots per invocation;
- M_A_logical = sum_j(2k_j+1): unweighted A/A-inverse-equivalent invocations;
- M_A_executed = sum_j N_j(2k_j+1): shot-weighted A/A-inverse-equivalent invocations;
- M_Q_executed = sum_j N_j k_j: Grover-operator applications, comparable to Qiskit's `num_oracle_queries` only after version-specific shot accounting agrees;
- pre/post-transpilation depth and gate counts per invocation;
- maximum executed depth;
- shot-weighted 1q and 2q gate burden;
- logical/physical qubit counts and SWAPs for backend-targeted transpilation;
- wall-clock simulator runtime as an engineering metric, not a hardware speed comparison.

The selected Qiskit version's `result.powers` structure is verified explicitly; any initial sentinel zero is never treated as an executed round, and repeated k rounds remain distinct. Reflections, controlled operations, and lower-level gates are excluded from the abstract A/Q metrics and reported through transpiled counts. `M_A_logical` is an invocation count, not circuit depth. Failed or interrupted first attempts retain every resource consumed before the exception.

Physical-resource reports freeze the complete compilation contract captured by the cache key. Depth is reported per circuit and as maximum executed depth; shot-weighted gate burden is the main aggregate proxy. Identical transpiled circuits may reuse resource records, but execution records remain distinct.

Construct executed accuracy-resource-proxy Pareto frontiers rather than declaring a global break-even or runtime-advantage threshold. Template-only n=6 circuits remain resource curves and are excluded from executed frontiers.

### E5b: Basic classical context

To avoid an unsupported system-level advantage claim while preserving Paper B's separate contribution, include one narrow descriptive table for naive Monte Carlo on the same 50 European contracts. Annex G freezes `N={256,1024,4096,16384,65536}`, 30 independent replications, the six dollar targets from $1.00 to $0.01, exact stream derivation, equal benchmark weights, the lognormal payoff-variance formula, analytic target sample counts, and the descriptive-only empirical grid. Do not add antithetic, control-variate, stratified, importance-sampling, or RQMC comparisons, and do not equate a classical sample with a quantum oracle application or hardware second.

### E6: Conditional d=2 arithmetic Asian stress test

Asian work begins only after the required European E0-E5 dataset and primary figures are frozen. It is time-boxed to five working days and is not on the paper's critical path.

The canonical contract uses K=100, S0=100, r=0.05, sigma=0.20, T=1, monitoring dates t={T/2,T}, and excludes S0 from the arithmetic average. The circuit encodes the joint distribution of (S_T/2,S_T) directly, not independent increments. The log-price vector uses mu_i=log(S0)+(r-sigma^2/2)t_i and covariance Sigma_ij=sigma^2 min(t_i,t_j). The joint retained event, conditional path distribution, total omitted mass, omitted discounted Asian payoff, and support-conditioning bias are audited separately.

Annex H freezes three uncertainty qubits per date, the `q_joint=1e-4` union-bound support construction, joint retained event, exact 15-logical-qubit budget, `WeightedAdder` weights `[1,2,4,1,2,4]`, four sum qubits, four ancillas, exact average map, joint-tail gates, and day-3 resource thresholds. Separate supports, alternate fixed-point scales, and added arithmetic-quantization layers are outside this spec. Exact path-grid enumeration covers all 64 index pairs using the same joint pointwise-density normalization and basis ordering as the distribution circuit. High-accuracy classical arithmetic-Asian pricing and a geometric-Asian or limiting-case calculation provide independent checks where applicable.

Maximum scope is one d=2 contract:

- correlated joint-state construction, transpilation, exact finite-path-grid reference, ideal statevector expectation, and resource profile;
- ideal finite-shot and at most `p=1e-3` noisy d=2 IQAE, 10 replicates each, only if every Annex H day-3 gate passes and the remaining projection is at most 16 hours;
- no d=4 or d=8 construction, resource estimate, or experiment appears in the eight-week roadmap.

The design records joint-support semantics, basis ordering, per-date discretization, averaging convention, arithmetic precision, payoff clipping/scaling, ancilla policy, qubits, depth, two-qubit gates, and any executed shot-weighted burden.

Asian stop gate: if d=2 cannot pass reference semantics or the five-day time box, the extension becomes a documented feasibility limit or is removed from the manuscript. It is never included in the title on speculative resource estimates, and it never delays the European paper.

### E7: Limited IBM hardware sanity check

Replace the current one-qubit-only interpretation with checks whose claims match their scope:

1. repeat the existing single-qubit amplitude primitive as a calibration baseline;
2. run a shallow n=2 integrated European state-preparation plus payoff circuit, without full IQAE, if depth permits;
3. optionally run one low Grover-power circuit if transpiled depth and queue access permit;
4. use fixed layouts and save the exact submitted ISA circuit, measured-bit mapping, Runtime-encoded result, job ID, backend, creation/start/completion timestamps, shots, job metrics, calibration ID where exposed, execution-time `job.properties()`, and compilation-target snapshot;
5. repeat across more than one session only if access permits and the European core is unaffected.

Compare the exact same saved ISA circuits under ideal simulation, a backend-derived model, and hardware. If execution-time properties or timestamps are unavailable, fields are explicit nulls and the simulator is labeled a time-nearest approximate backend model, not an exact matched snapshot. Hardware jobs are submitted opportunistically from Week 3 onward. Do not claim that agreement validates full IQAE or the controlled synthetic noise family.

E7 is complete either when the planned narrow circuits run successfully or when backend access, queue, credit, or depth limitations are documented. Hardware availability never blocks freezing or submitting the European simulator study.

## Statistical Design

- Use Annex A's exact 50-contract table rather than an undocumented random sample. The primary benchmark mean is equally weighted at 0.02 per contract; weights never change after results are inspected.
- Treat `(configuration,n)` as the matched scientific block. Replicate indexes are balance and provenance keys, not common-random-number pairs. Streams follow Annex D's literal SHA-256 to `SeedSequence` and `PCG64DXSM` derivation; Python `hash()` is forbidden.
- Share transpiler seed 20260727 and the same recorded ISA circuit across compared conditions. Use independent shot/noise streams per condition and separate pilot/main namespaces.
- Primary stochastic estimand: fixed-50 mean normalized delivered-estimate shift mu_eta at n=3, p=1e-3. Key secondary estimands: the full n=3 p-response curve, ideal estimator bias at n={3,4}, completion probability, aggregate ideal interval containment, and configuration heterogeneity. Higher-n noise subsets, strata interactions, backend-inspired noise, hardware, and all Asian quantities are exploratory.
- Estimate ideal and noisy condition means separately using Annex D's 10,000-resample procedure. Independently resample replicate observations within each condition and configuration; for joint noise-response bands, share the ideal resample across noise levels. Configurations are not resampled for the primary stochastic interval. Any configuration-resampling analysis is labeled finite-benchmark sensitivity, not market-population inference.
- The additive decomposition is evaluated at condition-mean level. Per-run noisy-minus-ideal differences are not treated as paired observations.
- Define aggregate ideal containment at n as the equal-weight mean over contracts of the within-contract indicator that P_circuit lies in the algorithm-reported ideal interval. Resample replicates within contract for uncertainty. Per-contract rates use exact binomial intervals and remain descriptive. Under noise, report `ideal-target containment rate`, not coverage.
- Preserve signed and absolute errors; report replicate variation separately from cross-contract heterogeneity.
- Report mean, median, standard deviation, interquartile range, quantiles, worst case, completion probability, and failure rate where relevant.
- Primary failure policy uses first planned attempts. Completion, validity, invalid-interval, exception, `R_min`, and claim-withholding rules are exactly Annex D; runtime, memory, depth, two-qubit, circuit-shot, and n=5 promotion thresholds are exactly Annex E. Missing-outcome sensitivity uses the full post-processing image `h([0,1])`. Retries remain linked sensitivity analyses.
- Prefer effect sizes and uncertainty intervals over large families of tests. Any formal tests, equivalence margins, or multiplicity correction are predeclared.
- Record, classify, count, and assess every failed run for selection bias. Do not rerun silently until success or claim a cause where evidence supports only an unresolved category.

## Validation and Tests

### Unit tests

- continuous and finite-support reference consistency;
- support tail probability and omitted payoff calculations;
- exact grid points, probabilities, normalization, and payoff expectation;
- payoff scaling, clipping, inverse post-processing, and boundary amplitudes;
- discounting exactly once;
- signed error reconstruction across all five error layers;
- strike on-grid and between-grid fixtures;
- zero-payoff and near-boundary objective cases;
- explicit rejection of unsupported/degenerate financial inputs;
- deterministic configuration enumeration and random-stream derivation;
- run-state transitions, idempotency keys, and resume behavior;
- schema validation;
- instrumentation adapter: one record per sampler invocation, exact effective shots, logical/ISA hashes, partial-resource retention after an exception, and reconstructed circuits prohibited from `actual_*` fields;
- power accounting: initial sentinel excluded, repeated powers retained, variable shots handled, and M_A_logical, M_A_executed, and M_Q_executed tested independently;
- logical and shot-weighted invocation formulas;
- noise coverage: every intended ISA operation has a matching error, excluded operations do not, basis mismatch fails validation, and no second transpilation changes the recorded ISA circuit;
- cache invalidation when versions, target snapshot, plugins, scheduling, initial layout, or seed change.

### Statevector checks

- distribution probabilities against the independently calculated finite-grid probabilities;
- exact grid payoff against P_grid;
- objective-qubit marginal probability, selected by qubit/register identity rather than manual integer bit shifts, against independently calculated a_calc;
- raw payoff post-processing and discounted price against P_circuit, with presentation clipping tested separately;
- controlled checks that P_support, P_grid, and P_circuit differ only for their defined reasons.

Conditional Asian tests, if E6 starts:

- covariance equals sigma^2 min(t_i,t_j) and the joint retained probability is normalized;
- index/basis ordering agrees between exact enumeration and statevector probabilities;
- common-support integer sum maps exactly to the arithmetic average;
- any separate-support mode exposes and measures arithmetic-quantization error;
- joint omitted mass, omitted payoff, and support-conditioning bias satisfy their frozen gates.

### Integration smoke test

A tiny end-to-end run with two configurations, n=3, two seeds, ideal plus one noise condition, fixed low shots, raw/resource output, aggregate table, validation report, and one generated figure.

### Full-dataset gates

- expected row and required replicate-condition key counts;
- no duplicates;
- no missing required replicate-condition keys;
- package and schema consistency;
- complete resource fields;
- recomputed error columns equal stored values;
- first-attempt completion, valid-record, complete-record, invalid-interval, and failure thresholds equal the frozen protocol;
- condition-mean identities use identical included sets and missing-outcome sensitivity is present when required;
- hashes recorded before `COMPLETE` is created.

## Hard Scope Tiers

### Required submission-ready Paper A core

- E0 reference ladder and semantics;
- E1 European deterministic reference-layer scaling;
- E2 frozen shot/replicate pilot;
- E3 ideal finite-shot European study;
- E4 controlled synthetic noise study;
- E5 resource frontier;
- E5b basic naive-Monte-Carlo context;
- statistics, manuscript, reproducibility, and clean-environment rerun.

### Conditional appendix or small section

- one six-configuration backend-inspired noise subset;
- one or two narrow IBM circuits, or a documented access/depth infeasibility outcome;
- d=2 Asian construction/resource result if completed inside its five-day time box.

### Future work outside this eight-week roadmap

- finite-shot or noisy d=2 Asian IQAE not completed inside the five-day conditional box;
- any d>2 Asian construction or resource estimate;
- error mitigation experiments;
- full IQAE hardware execution;
- additional QAE variants or noise families.

Post-core work cannot delay freezing the required European dataset or starting the manuscript.

## Eight-Week Roadmap

### Week 1: Audit, pilot specification, and support/reference semantics

- Freeze the old manuscript and datasets as historical artifacts.
- Build a claim-to-source audit of every existing Paper A number.
- Complete a contribution-by-prior-work matrix covering error layers, finite-shot adaptive QAE, benchmark breadth, noise treatment, failure/containment analysis, and realized resource metrics; freeze the differentiated contribution statement before E2.
- Write and approve the frozen pilot specification before implementation planning proceeds, including the complete 50-row contract table and analysis weights.
- Reconstruct a historical lock and test one fully pinned current environment through the compatibility and instrumentation gates.
- Freeze the supported financial domain, 12 deterministic validation configurations, exact 50-contract benchmark, the nested `C12`/`C6`/`N5` stochastic subsets, support equations, point-grid convention, payoff rescaling factor, raw objective-probability semantics, IQAE parameters, noise channels, failure/retry policy, resource definitions, and numerical feasibility thresholds.
- Implement the continuous and finite-support reference layers and begin deterministic boundary tests.
- Start the methods and definitions sections of the manuscript while semantics are being fixed.

Exit gate: the contribution claim survives the prior-work matrix; the exact 50-contract table and weights are frozen; both candidate environment locks are reproducible; and P_BS, P_support, domain rejection, and support-tail audits pass for all validation fixtures.

### Week 2: Minimal vertical runner, grid/circuit references, and E0 completion

- Implement only the smallest config/schema/runner slice needed for E0 and the smoke run.
- Complete P_grid and P_circuit cross-checks, payoff scaling, discounting, and error identities.
- Add append-only raw records, idempotency keys, minimal resume logic, and validation output.
- Prove the recording sampler/transpiler contract on the smoke run: actual invocations, powers, effective shots, logical/ISA hashes, counts, metadata, and partial resources on failure; downgrade to explicitly reconstructed fields if actual capture is unavailable.
- Add M_A_logical, M_A_executed, M_Q_executed, and transpiled gate/depth metrics, expanding modules only when a second caller or distinct validation responsibility exists.
- Complete E0 and the end-to-end smoke experiment.
- Run E1 after E0 passes.

Exit gate: one command can create, resume, validate, and freeze a small pilot dataset; every reference layer agrees within its frozen tolerance; and the instrumentation adapter either captures actual submitted round circuits and shots or proves the documented reconstructed-only fallback before E2.

### Week 3: Shot/replicate pilot, resource conventions, and matrix freeze

- Run E2 Stage A and Stage B, including the four n=5 feasibility cells.
- Measure circuit-shots, wall time, peak memory, variance, ideal-target containment, completion/failure behavior, and resource growth.
- Freeze the main shot policy, replicate count, noise parameters, configuration strata, n=5 fallback, transpiler target/settings, and resource-counting convention.
- Submit narrow IBM jobs opportunistically if access and depth permit.
- Update manuscript methods with the frozen design.

Exit gate: planned work fits 10.5 of 14 overnight-equivalents, preserving the 25% reserve; the primary estimand hierarchy, completion/failure policy, shots, R, common comparison subsets, and promotion thresholds are frozen; and the required all-50 European core receives an explicit GO. If not, execution stops for a scope or schedule decision rather than silently shrinking the matrix.

### Week 4: European deterministic and ideal experiments

- Freeze E1 results.
- Run the required E3 n={3,4} ideal matrix and the frozen n=5 full or subset fallback.
- Validate the full error ladder, raw-probability and dollar interval units, aggregate ideal-target containment, replicate balance, completion states, and exceptions.
- Begin analysis of support, grid, encoding, and estimation effects.
- Build manuscript table/figure templates from validated partial aggregates rather than waiting until Week 7.

Exit gate: the ideal study passes dataset validation with every systematic discrepancy either resolved or recorded as a scope-limiting finding.

### Week 5: Main synthetic noise and resource study

- Run the E4 core n=3 controlled-noise sweep using independent condition streams and reused E3 ideal records where hashes and policies match.
- Run the `C12` n=3/4 comparison and extend the same `C12` set to n=3/4/5 only if n=5 passed promotion.
- Generate the conditional backend-inspired `C6` subset from a saved calibration snapshot if tooling and metadata pass validation.
- Freeze E5 resource tables, E5b naive-Monte-Carlo context, and accuracy-resource frontier inputs.
- Continue drafting results structure and limitations while batches run.

Exit gate: every first-attempt failure is recorded, classified, counted, and assessed for selection bias; required condition/configuration cells meet the frozen complete-record rule; common-contract cross-n comparisons are intact; and no claim depends on a single replicate, arbitrary replicate pairing, or undocumented retry.

### Week 6: Time-boxed conditional extensions and main-analysis buffer

- Confirm that the required European data and primary figures are frozen before beginning extension work.
- Spend at most five working days on the single d=2 correlated-joint-spot arithmetic Asian construction/reference/resource result.
- Attempt finite-shot or selected noisy d=2 runs only if the deterministic ladder, statevector agreement, and resource profile pass by the end of working day 3 and the remaining two days fit the frozen gates.
- Collect any completed opportunistic IBM jobs and save complete job/calibration metadata; document access or depth infeasibility if none complete.
- Use remaining time for European reruns, diagnostics, manuscript figures, and limitations.

Exit gate: extension claims match exactly what was executed, and no Asian or hardware delay changes the required European evidence.

### Week 7: Statistics, figures, and manuscript rewrite

- Produce frozen summary tables and within-configuration independently resampled condition-mean intervals, plus clearly labeled finite-benchmark sensitivity analyses.
- Generate five to six publication-resolution figures from frozen data only.
- Rewrite title, abstract, contributions, methodology, results, resources, hardware section, limitations, and conclusion.
- Expand related work around IQAE, state/payoff approximation, resource estimation, noise-aware amplitude estimation, and quantum-finance experiments.
- Build a claim-evidence matrix linking each numerical sentence to a table, figure, or raw field.

Exit gate: every result sentence can be regenerated from the frozen experiment manifest.

### Week 8: Adversarial review and release candidate

- Run scientific, statistical, and reproducibility audits.
- Invite an external faculty/domain reviewer if available; use an internal adversarial review as the non-blocking fallback.
- Re-run the paper from a clean environment using documented commands.
- Verify figure resolution, labels, equation discussion, limitations, citations, and page length.
- Create the final manuscript build and exact experiment release/tag only after approval.

Exit gate: clean-environment reproduction succeeds and no unsupported legacy claim remains in active documentation.

## Figures and Tables

Target figures:

1. Signed additive error decomposition by n and noise level, paired with a separate non-stacked absolute-magnitude view.
2. Support, finite-grid, and circuit-encoding error versus uncertainty qubits over the fixed benchmark.
3. Condition-mean noise-response curves with independently resampled replicate uncertainty and shared ideal-reference resamples across noise levels.
4. Accuracy versus shot-weighted A-equivalent, Grover-application, and gate-burden frontier.
5. Sensitivity by moneyness, maturity, and volatility.
6. Payoff-rescaling tradeoff from the E1 deterministic `c` sweep: signed `e_encode` against `c in {0.05,0.10,0.25,0.50}` on `C12` at `n in {3,4}`, with the objective-amplitude span on a second axis and the frozen `c=0.25` marked. This is the cheapest direct illustration of the paper's central claim that improving one layer degrades another, and it is available from statevector evaluation alone.
7. Asian resource scaling, included only if the stress test passes.

Hardware results should be a compact validation figure or appendix, not a headline figure unless the integrated small circuit produces repeatable evidence.

Target tables:

1. Experiment matrix and seed/shot policy.
2. Error-budget summaries.
3. Resource accounting definitions and results.
4. Failure and feasibility-gate outcomes.
5. Hardware jobs and calibration metadata.

## Manuscript Positioning

Standing limitation near the abstract and conclusion:

> This study does not demonstrate quantum advantage, hardware-runtime advantage, or a hardware-realistic noise process. It characterizes one reproducible finite-shot IQAE implementation under exact simulation and explicitly defined synthetic noise models using executed circuit-and-shot resource proxies.

Recommended claims:

- error decomposition itself is not claimed as new; the contribution is the preregistered, fixed-benchmark, replicated, failure-aware, exact-circuit-layer and shot-weighted empirical protocol;
- query-only analyses omit error and execution components that determine delivered price accuracy;
- support conditioning, finite-grid bias, circuit/payoff encoding, finite-shot IQAE behavior, failures, and synthetic noise can be measured separately and can partially cancel;
- across all 50 contracts, deterministic references scale over n={3,4,5,6}, ideal finite-shot behavior covers n={3,4}, and controlled noise covers n=3; noise-by-resolution interaction at n>=4 is a common-subset analysis and is not generalized to the full benchmark;
- increasing grid resolution must be evaluated against circuit and shot-weighted resource growth;
- under the evaluated configurations and models, state precisely which accuracy targets were reached, missed, or remained inconclusive under the compute cap;
- a d=2 Asian result is a bounded transfer/feasibility stress test, not a general Asian-pricing or novelty claim.

Claims to remove unless new evidence supports them:

- `$0.203 is the three-qubit discretization floor`;
- `p=1e-3 is the current IBM noise level`;
- `approximately 14 queries is the physical execution cost`;
- `the hardware primitive validates the full simulator model`;
- `QAE provides no usable advantage` as a general statement.

## Expected Reviewer Objections and Required Evidence

| Objection | Required answer |
|---|---|
| Error budgeting and noisy QAE option pricing already exist | Cite the overlap directly and claim only the differentiated fixed-benchmark, exact-circuit-layer, replicated adaptive-IQAE, failure-aware, realized-resource protocol supported by the Week-1 contribution matrix. |
| The decomposition is implementation-specific | Define all circuit semantics, bounds, scaling, versions, and show independent exact/statevector cross-checks. |
| These are not paired stochastic observations | Use independent-condition inference, condition-mean decomposition, balanced streams, and common-contract aggregation rather than arbitrary replicate pairing. |
| Noise model is unrealistic | Label the controlled model synthetic and include a saved backend-inspired subset without conflating the two. |
| Replication is insufficient | Use balanced independent condition replicates, explicit stream derivation, condition-consistent uncertainty intervals, failure reporting, and a justified R from the pilot. |
| Oracle accounting is misleading | Report M_A_logical, M_A_executed, M_Q_executed, circuit depth, and gate burden as distinct conventions. |
| Option configurations are cherry-picked | Publish the exact frozen 50-row table, weights, construction rule, replacement pool, and every failure. |
| Asian extension is superficial | Require a validated d=2 complete circuit or remove it from the title and reduce it to a limitation/resource note. |
| Hardware evidence is too weak | Narrow the claim, use the same circuit across ideal/noisy/hardware conditions, and preserve calibration metadata. |
| Novelty is only better bookkeeping | Connect the decomposition to changed rankings, cancellation, scaling, or an accuracy-resource frontier that query-only analysis cannot reveal. |
| Classical comparison is weak | State that Paper A studies delivered QAE behavior, use only basic context, and avoid claiming system-level advantage. |
| Results depend on obsolete software | Pin and justify one paper environment, preserve manifests, and cross-check semantics against the legacy implementation. |

## Predeclared Pilot Outcomes

The spec leaves no protocol ambiguity for implementation. The following are measured outcomes, not design choices:

1. Which Annex B candidate passes the semantic and instrumentation fixtures.
2. Whether Annex I's actual recording contract passes or the study is restricted to `reconstructed-only-v1` terminology and claims.
3. Which per-circuit shot budget in `{512,2048,8192}` and which `R` in `{10,15,20,30}` satisfy the frozen precision and compute rules.
4. Whether n=5 earns full-50 promotion, the frozen `C12` fallback, or no stochastic promotion under Annex E.
5. Whether the Annex H d=2 circuit passes the day-3 and five-day gates.
6. Whether the optional n=2 integrated European hardware circuit fits backend depth and queue constraints.
7. Whether IBM Runtime exposes execution-time properties and timestamps sufficient for an exact snapshot or only a time-nearest model.

These outcomes may narrow conditional evidence but cannot change the central European error-budget thesis, the exact benchmark, or the required simulator-first core.

## Success Criteria

By the end of eight weeks:

- all reported numbers derive from versioned, validated, frozen experiment directories;
- the European support, finite-grid, and exact circuit-encoded references have independent unit and statevector tests;
- continuous, finite-support, grid, circuit-encoded, ideal finite-shot, and noisy finite-shot prices are stored separately;
- all signed error components reconstruct total error exactly;
- stochastic findings use balanced independently seeded condition replicates and uncertainty intervals consistent with independent-condition inference;
- European deterministic discretization covers n={3,4,5,6}; executed ideal/noisy claims name their smaller n ranges explicitly;
- the full controlled-noise benchmark includes all 50 configurations at n=3 and common-contract higher-n subsets only;
- actual submitted shots and IQAE round circuits feed executed resource metrics when captured; reconstructed-only or template resources are labeled and excluded from executed frontiers;
- an accuracy-resource frontier replaces a one-number break-even claim;
- the required European paper is complete without Asian or hardware success;
- any d=2 Asian result is validated inside the five-day extension gate or omitted/reduced to a documented feasibility limit;
- hardware claims match the exact tested circuit scope, with access failure accepted as a documented non-blocking outcome;
- figures are generated at publication resolution from frozen summaries;
- the manuscript distinguishes raw objective probability, encoded payoff, and dollar-price precision;
- a clean environment reproduces the main tables and figures;
- the prior-work matrix supports a specific differentiated contribution; if it does not, the output is framed as a reproducible technical study rather than first-of-kind work;
- the primary normalized noise-shift estimand meets its predeclared precision target or is explicitly reported as inconclusive under the compute cap;
- at least one result demonstrates why the circuit layer, finite-shot behavior, failure analysis, or shot-weighted burden changes an interpretation suggested by query counts alone; no positive result is required;
- every full-benchmark and subset claim is visibly distinguished, and the paper makes no quantum-advantage, hardware-runtime, or hardware-realism claim;
- active Paper A documentation no longer repeats unsupported legacy claims. The deployed dashboard remains outside this roadmap and is not evidence for the revised paper.

## Distribution Plan

The research deliverable is distributed through the repository rather than the live dashboard:

- versioned source under `research/paper_a/`;
- frozen experiment manifests and derived tables under `data/paper_a/`;
- manuscript sources and build instructions under a new output directory;
- a Git tag or release identifying the exact submitted state;
- optional archived datasets attached to a release if repository size permits.

The live Railway dashboard remains unchanged unless a later, separately scoped update presents the corrected results.

## Next Steps

1. Review this repository specification and either request corrections or explicitly approve it in writing.
2. Only after explicit written-spec approval, invoke `superpowers:writing-plans` to create the task-by-task implementation plan.
3. Implementation, when separately authorized, begins with the Week-1 contribution, reference, environment, and instrumentation gates, never the main noisy sweep.
4. No code, experiment, environment installation, commit, hardware submission, or manuscript rewrite is authorized by this document alone.

## Written-Specification Approval Gate

This document now freezes the repository-level protocol required by the approved eight-week roadmap: Annex A fixes the benchmark and domain; B fixes environment candidates; C fixes objective and price semantics; D fixes streams, resampling, and inclusion; E fixes numerical feasibility thresholds; F fixes controlled noise; G fixes naive Monte Carlo context; H fixes the conditional d=2 Asian test; and I fixes actual-recording versus reconstructed-only resource claims. The 12 validation configurations, support-selection rule, error ladder, resource equations, cache contract, IBM metadata contract, contribution audit, roadmap, validation gates, and scope tiers remain part of this same specification.

No implementation plan, code change, experiment execution, environment installation, hardware job, or commit begins until the user explicitly approves this written specification.

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO/Strategy Review | `/plan-ceo-review` | Scope, contribution, schedule, claims | 2 | ROADMAP APPROVED | 7/10 → 9/10; narrowed novelty, removed out-of-scope d>2/mitigation work, added hard stop/go and exact-benchmark gates |
| Scientific/Statistical Adversarial Review | independent Plan review | Estimands, resampling, containment, validity | 2 | ROADMAP APPROVED | 6/10 → 9/10; repaired support mathematics, independent-condition inference, precision units, failure policy, common-contract comparisons, and MC protocol |
| Engineering/Qiskit Review | `/plan-eng-review` | Instrumentation, Qiskit semantics, resources, Asian feasibility | 2 | ROADMAP APPROVED | 4/10 → 9/10; added recording-wrapper contract, raw-probability semantics, three resource metrics, single-transpilation noise contract, cache completeness, correlated d=2 construction, and Runtime metadata fallback |
| Design Review | not applicable | No UI/dashboard changes | 0 | SKIPPED | Research package and manuscript only |
| DX Review | not run | CLI command ergonomics belong in the post-approval implementation plan | 0 | DEFERRED | Non-blocking for written-spec approval |

- **CROSS-REVIEW:** All three reviewers agreed that the error-budget-first European core is the right direction and that the original manuscript headlines must not be protected. All three independently identified support semantics, stochastic estimands, exact benchmark freezing, and operational Qiskit/resource semantics as the items the repository spec had to resolve.
- **VERDICT:** THE EIGHT-WEEK ROADMAP IS APPROVED. THIS WRITTEN REPOSITORY SPECIFICATION IS COMPLETE AND AWAITING EXPLICIT USER APPROVAL. IMPLEMENTATION PLANNING AND EXPERIMENT EXECUTION REMAIN BLOCKED UNTIL THAT APPROVAL.

**RESOLVED IN THIS SPECIFICATION:**
- Annex A freezes the exact 50-row benchmark, IDs, strata, equal weights, supported domain, and deterministic replacement rule.
- Annexes B, C, D, and I freeze environment candidates, payoff semantics, selected IQAE fields, independent streams, resampling, valid-record rules, and recording versus reconstructed-only provenance.
- Annexes E and F freeze runtime, memory, depth, two-qubit, circuit-shot, failure, n=5 promotion, and controlled-noise ISA thresholds.
- Annexes G and H freeze the naive-Monte-Carlo grids and the d=2 Asian qubits, common support, joint-tail audit, resource limits, and day-3 gate.
