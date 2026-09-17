# Quantum Option Pricing

Research into encoding-aware quantum option pricing: circuit construction,
explicit error budgets, amplitude estimation, and comparison with strong
classical methods.

The project has grown from a European-option dashboard into a reproducible
research codebase. Its primary harder application is **arithmetic Asian-basket
pricing under risk-neutral geometric Brownian motion**. European and digital
options remain regression controls and historical experiments.

**Status — 17 September 2026:** the latest two-week construction and integration
study is complete within its bounded scope. The reflection-centered candidate
remains on standby. We have demonstrated improvements over selected quantum
baseline constructions, **not quantum-over-classical advantage**. Confirmation
and submission readiness remain open; no paper is recorded as submitted or
published.

## Start here

- [Latest matched arithmetic comparison and scientific decision](docs/journal_sprint/MATCHED_ARITHMETIC_RESULTS_20260917.md)
- [Claim assessment, restricted proofs and prior-art boundaries](docs/journal_sprint/CLAIM_ASSESSMENT_RESULTS_20260917.md)
- [Completed work and remaining tasks](checklist_17.9.26.md)
- [Latest integrated study results](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_RESULTS.md)
- [Signal construction and derivation](docs/journal_sprint/MINIMAL_PIVOT_WEEK1_METHOD.md)
- [Integration, error budget and precision-cost analysis](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_METHOD.md)
- [Running project log](docs/journal_sprint/PROJECT_LOG.md)
- [Verified integration handoff](docs/journal_sprint/STUDY_MERGE_CLOSEOUT.md)

## Research question

Can a concrete quantum encoding and estimation procedure provide a defensible
pricing benefit after charging for state preparation, payoff approximation,
uncomputation, statistical precision and execution costs?

The work separates three questions:

1. Does a circuit implement the intended finite mathematical target?
2. Can the full error budget support a stated price tolerance and confidence?
3. Is the resulting cost competitive with the best applicable classical method?

A positive answer to the first question does not establish the other two.
Similarly, reducing one quantum circuit's cost is not a classical speedup.

## What is implemented

- **Quantum encodings:** finite reference circuits, structured Gaussian loading,
  separable basket signals and a shared-reflection centered construction.
- **Integrated estimation:** residual quantum signal processing (QSP), directed
  classical offsets, Hadamard readout, explicit canonical amplitude estimation
  (AE), and interval-based outcome decoding.
- **Encoding-aware decisions:** accuracy and resource screening, degree/encoding
  selection among supported logical plans, and explicit refusal when requirements
  cannot be certified. Physical/production promotion remains disabled.
- **Classical comparisons:** Monte Carlo, control variates, randomized
  quasi-Monte Carlo (RQMC), and conditional RQMC, with recorded setup/pilot costs.
- **Inference and validation:** calibration-aware fixed/sequential methods,
  transfer checks, finite-target comparator studies, ablations and negative controls.
- **Evidence tooling:** frozen protocols, source/artifact hashes, exclusive output
  directories, replay verifiers, tests and preserved failed attempts.

The [four-paper audit](docs/journal_sprint/FOUR_PAPER_AUDIT.md) and
[latest prior-art assessment](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_PRIOR_ART.md)
explain which ideas transfer to this application and which assumptions do not.
Known primitives are not presented as newly invented algorithms.

## Latest results: improvements and limits

### Matched arithmetic follow-up

The bounded D1/D2 study now includes explicit fixed-point conversion, efficient
ripple or Fourier aggregation, payoff encoding, uncomputation and matched AE
planning. Reflection has lower declared logical CX projections than these
arithmetic implementations: ripple/reflection ratios are13.54 and1.82, or15.36
and2.04 with standard control cancellation. These are **ratios of projections,
not runtime speedups**; the arithmetic baseline is not space- or exponentiation-
optimal. Fourier aggregation costs more than efficient ripple in this menu and
aggregation contributes under0.061% of arithmetic A-circuit CX. Primary and
isolated replay agree exactly. See the
[full comparison and limitations](docs/journal_sprint/MATCHED_ARITHMETIC_RESULTS_20260917.md).
The candidate remains on standby; quantum-over-classical advantage is not established.

### Circuit construction

The shared-reflection signal replaces the earlier subset-centered construction's
`1 + d * (2^d - 1)` coefficient slots with `d + 1`, where `d` is the model's
Gaussian-factor dimension. For the four-factor example, that is **61 to 5 slots**.

At four factors and two bits per coordinate, the compiled signal uses **282 CX
gates versus 1,148** for the optimized subset-centered baseline: about **4.07x
fewer CX**, with depth reduced from 1,753 to 383. These are signal-component
counts, excluding probability loading and the complete QSP/AE pipeline. The
optimized original uncentered signal is cheaper still at 146 CX; the intended
centering benefit comes from the wider accuracy/resource tradeoff.

At four factors and ten bits per coordinate, a **47-qubit signal circuit was
constructed and compiled**. It was not simulated as a 47-qubit statevector or
executed as a complete pricing algorithm. See the
[Week 1 results](docs/journal_sprint/MINIMAL_PIVOT_WEEK1_RESULTS.md).

### Integrated logical-cost study

The frozen menu contains four contracts, two encodings and four polynomial
degrees: **32 logical-plan configurations**, alongside **24 classical
method/budget cells**. Nine quantum configurations pass the ideal-logical
deterministic-plus-AE planning gate for a $1 tolerance at 95% confidence.

| Case | Original/reflection projected CX ratio | Approximate selected reflection CX |
| --- | ---: | ---: |
| D1 | 4.03x | 3.54e11 |
| D2 | 2.01x | 1.06e13 |
| E1 | 4.02x | 4.28e12 |
| E2 | Neither encoding meets the fixed accuracy menu | No feasible plan |

Ratios compare the lowest-cost feasible plan within each implemented encoding
family, including its selected degree and AE budget. They are **logical
composition projections**, not measured hardware speedups or globally optimal
cost ratios. The large absolute costs remain important.

Two complete tiny, 10-qubit AE pipelines were simulated. Their distributions
agree with an independent Fourier-kernel calculation within `2.25e-12`.
However, at the same tiny degree and AE schedule, reflection uses **more** CX:
1,147,295 versus 911,871. These coarse toy runs do not certify $1 continuous-price
delivery. Classical replicate t intervals are approximate diagnostics, not
proved coverage guarantees.

See the [full Week 2 results](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_RESULTS.md)
for the contract definitions, error budgets, unfavorable cases and timing scope.

## What is closed, and what remains open?

Completed development is not kept open merely because an investigation produced
a negative result or has a stated limitation.

| Work package | Current disposition |
| --- | --- |
| Original Weeks 1–13 | Development closed within recorded scopes; negative gates retained |
| Original Week 14 | Finite-target study closed; broader continuous-price comparison incomplete |
| Original Week 15 | Fresh-environment reproduction closed; confirmation campaign blocked |
| Additional two-week minimal-pivot study | Construction and bounded validation closed; candidate on standby |
| Original Week 16 | Final integrated manuscript and submission-readiness work remain open |

The principal open questions are a defensible distinction from nearest prior
work, an execution/synthesis/noise model for physical claims, and a matched
continuous-target comparison against strong classical methods. Any confirmation
campaign needs admission, a frozen analysis and genuinely fresh data first.

A narrower ideal-logical resource/error paper would need an explicit scope
decision and independent novelty assessment; it is not automatically
publication-ready. Hardware superiority is not established by this repository.
The [dated checklist](checklist_17.9.26.md) separates these decisions from finished
implementation tasks. Older plans and drafts are historical, not current claims.

## Reproduce and verify

### Tested environment

The recorded replay environment is **Windows, Python 3.9.13, NumPy 2.0.2,
SciPy 1.13.1 and qiskit-terra 0.46.3**. The
[pinned replay requirements](research/journal_sprint/requirements-week15-replay.txt)
cover the research replay and focused tests, not all legacy app/Aer/Finance
dependencies. This is a historical reproducibility environment, not a claim of
compatibility with current Qiskit releases or every operating system.

From the repository root, in PowerShell with Python 3.9 available:

```powershell
py -3.9 -m venv .context/readme_replay_env
.context/readme_replay_env/Scripts/python.exe -m pip install pip==23.2.1
.context/readme_replay_env/Scripts/python.exe -m pip install -r research/journal_sprint/requirements-week15-replay.txt
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
```

Use the recorded Python patch version for environment parity. Do not upgrade or
mix the legacy research environment with a modern hardware SDK environment.
The root `requirements.txt` is for the legacy dashboard; it is not the study's
reproduction specification.

### Check the archived study

```powershell
.context/readme_replay_env/Scripts/python.exe -m research.journal_sprint.verify_minimal_pivot_week1 .context/readme_w1_check.json
.context/readme_replay_env/Scripts/python.exe -m research.journal_sprint.verify_week2_final .context/readme_w2_check.json
.context/readme_replay_env/Scripts/python.exe -m research.journal_sprint.analyze_week2 .context/readme_w2_analysis.json
```

Choose **new output filenames** for each invocation; evidence writers refuse
overwrites. These commands verify recorded source/artifact integrity, compare
stored numerical replays and regenerate analysis. They do not reacquire the
expensive experiments and do not constitute independent scientific peer review.
The Week 2 final verifier uses the named authoritative archive directories.

### Run focused study tests

```powershell
.context/readme_replay_env/Scripts/python.exe -m pytest -q tests/test_reflection_centered_signal.py tests/test_week1_subset_control.py tests/test_week2_pipeline.py tests/test_week2_explicit_ae.py tests/test_week2_decoding.py tests/test_week2_analysis.py
```

These **51 tests** passed in the separate pinned environment. The latest full
repository suite passed **1,143 tests**, with 12 legacy warnings, in the original
full environment from a clean checkout. That full suite also exercises older
dependencies absent from the minimal replay environment; the test totals overlap.
See the [verification handoff](docs/journal_sprint/STUDY_MERGE_CLOSEOUT.md).

For fresh acquisitions, follow the
[frozen study protocol](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_PROTOCOL.md) and
[producer instructions](docs/journal_sprint/MINIMAL_PIVOT_WEEK2_RESULTS.md).
Use new output directories, retain failed runs, and freeze source files during
provenance-sensitive tests. Use `run_week2_explicit_ae` for tiny AE acquisition,
not the original runner's superseded `tiny` option. Final analysis v2 includes
the inverse-QFT swap-cost correction; raw projections alone are not the final
comparison.

## Repository map

```text
research/journal_sprint/   Active research implementations, runners and verifiers
research/paper_a/          Earlier research package and regression tests
docs/journal_sprint/       Protocols, methods, results, audits and project log
results/journal_sprint/    Versioned evidence, replay records and test receipts
tests/                    Pricing and research regression tests
src/                      Earlier pricing models and experiment utilities
app/                      Legacy dashboard; not the current research interface
data/, figures/           Historical datasets and generated figures
checklist_17.9.26.md       Dated completion and remaining-work checklist
```

The old dashboard and Paper A/B/C framing are retained only as historical code
and documents. Earlier “canonical numbers,” submission-ready labels and broad
novelty assertions are not endorsed as current conclusions; consult the
[claim ledger](docs/journal_sprint/CLAIM_LEDGER.md) and later closeouts.
The historical single-qubit hardware primitive is not validation of the current
Asian-basket pipeline or evidence of an end-to-end pricing advantage.

## Evidence and contribution standards

- Separate compiled circuits, simulations, projections and device executions.
- Preserve protocols, source hashes, failed attempts and negative findings.
- Do not use reference truths or held-out outcomes to tune a supposedly frozen
  policy, and do not relabel deterministic replay as fresh confirmation.
- Keep commits reviewable and attribute only work actually performed.
- Latest integration: [PR #6](https://github.com/Prithvi8706/quantum_option_pricing/pull/6).
  Macroscope skipped its review because credits were exhausted; local verification
  is documented, but a successful external review is not claimed for that PR.

## License

Project code is available under the [MIT license](LICENSE). Consult the separate
license notices for any third-party material retained in the repository.
