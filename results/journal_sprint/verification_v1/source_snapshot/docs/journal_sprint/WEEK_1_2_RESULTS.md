# Weeks 1–2: implemented feasibility sprint

9 September 2026. **Decision: proceed to a small application-level v2, not a large
simulation campaign or a submission.** The conservative inference baseline works
under its stated response model. Its adaptation benefit is not demonstrated.
Neither manuscript is submitted or published.

## What was actually executed

- Preserved historical data, manuscripts and relevant code in two exclusive,
  hashed evidence snapshots. Original scientific outputs are unchanged.
- Independently recomputed Black-Scholes references for all 250 expanded-sweep
  rows; checked the stored delta identity for every row.
- Pinned and reproduced a September 2026 comparator's source benchmark, retaining
  its Apache-2.0 license and unchanged code.
- Implemented all-branch binomial confidence-set inversion with a declared noise
  envelope, incompatible/unresolved outcomes and affine price-bound propagation.
- Ran **14,000 fixed-schedule trials**, **11,200 equal-A-cost direct-sampling
  trials**, and **1,400 independent-pilot trials**. All 26,600 records are retained.
- Ran **160,000 comparator estimations**, including paired matched/ignored-noise
  analyses on the same 20,000 observations. These are 140,000 distinct generated
  comparator datasets, not 160,000 independent datasets.
- Added numerical/statistical/circuit regression tests and a reproducible analysis
  plus artifact-integrity verification command.

This is a finite-shot response-model study. The circuit validation is an ideal
one-qubit statevector check, not noisy compiled pricing circuits or hardware.
The prototype simulation itself took approximately **44 seconds** locally;
that is software runtime, not quantum execution time or a speedup measure.

## 1. Historical audit: the old headline must change

The precomputation script stores QAE output in `price`; the expanded noise sweep
uses it as `ref_price`. Consequently, its `delta` is not Black-Scholes error.

| Synthetic p | Contracts | Stored mean delta | Recomputed mean absolute Black-Scholes error |
|---|---:|---:|---:|
| 0 | 50 | 0.203334 | 0.303837 |
| 0.0001 | 50 | 0.220154 | 0.289059 |
| 0.001 | 50 | 0.656951 | 0.751565 |
| 0.005 | 50 | 3.478250 | 3.596089 |
| 0.01 | 50 | 6.162819 | 6.304171 |

Neither the old nor the recomputed column isolates a deterministic discretization
floor. The reference itself has mean absolute Black-Scholes discrepancy 0.240812.
These absolute errors are not additive error-budget components. The old amplitude
tolerance also cannot be read as a one-cent price target.

Paper B is **not reconciled**: the checked-in dimension script has 10 trials,
the DOCX retains earlier slope claims, and the claimed raw 100-trial run has not
been located. Do not choose whichever slope looks better. Reproduce the classical
study with archived raw replications before reuse.

The [claim ledger](CLAIM_LEDGER.md) supersedes historical protected/canonical
claims. README and ROADMAP now carry explicit warnings. Old DOCX/LaTeX drafts
remain preserved; a clean replacement manuscript has not yet been written.

## 2. Modern comparator: reproduction passed

Source: [csAE repository](https://github.com/unitaryfoundation/csAE), pinned at
`202ffb8a462828d04dab13eef5005e295270d0e3`; associated
[September preprint](https://arxiv.org/html/2609.02715v1).
This is source-code reproduction and reduced independent replication, not an
independent implementation or the authors' full million-trial study.

| Case | Our C95 | Reference | Result |
|---|---:|---:|---|
| Plain ladder golden test | 2.822877 | 2.82 ± 0.04 | Pass |
| Flagship golden test | 2.851871 | 2.85 ± 0.05 | Pass; C99 and parallel windows also pass |
| Independent cap-60 run | 2.792070 | 2.776 | Reference inside our 95% quantile CI [2.745432, 2.842784] |
| Independent cap-125 run | 2.911744 | 2.886 | Reference inside our 95% quantile CI [2.868665, 2.956970] |
| Noisy, matched likelihood | 4.717863 | Qualitative comparison | Lower error constant than ignoring noise |
| Same noisy observations, noise ignored | 5.884073 | Qualitative comparison | Worse |

The source estimates `b=sin(theta)` with a cosine-squared response. Our pricing
objective is probability `a=sin(theta)^2` with a sine-squared response. These C95
constants are **not** directly comparable to our probability errors. The source's
query convention is preserved; shots, Grover calls and A-equivalent calls are
also recorded separately. Its numerical grid optimizer is not treated as a
formal proof of global optimality.

## 3. Confidence-set experiment: useful, but conditional

Schedule k=(0,1,2,4,8), equal shots per depth, seven fixed probabilities from .01
to .99, 200 repetitions per probability/cell, nominal failure budget .05.
Table pools the seven fixed probabilities equally; each row has 1,400 trials.
The precision declaration uses probability half-width <= .01.

| Condition | Shots/depth | True probability contained | Incompatible | Precision declared |
|---|---:|---:|---:|---:|
| Ideal | 128 | 97.07% | 0.64% | 99.36% |
| Known eta=.01 | 128 | 97.00% | 0.50% | 99.43% |
| eta=.01 inside [.005,.015] envelope | 128 | 98.29% | 0.29% | 82.29% |
| Known eta=.01 | 512 | 95.64% | 0.71% | 99.29% |
| eta=.01 inside [.005,.015] envelope | 512 | 98.64% | 0.21% | 99.79% |
| True eta=.03, incorrectly assume zero | 128 | 15.57% | 70.21% | 29.79% |
| True eta=.03, incorrectly assume zero | 512 | 13.93% | 85.79% | 14.21% |
| Intentionally inconsistent response vector | Both | No coherent truth defined | 100% | 0% |

The envelope widens uncertainty and reduces low-budget declarations, as intended.
Its 128-shot case has one erroneous .01 declaration out of 1,400 trials: 0.071%
unconditionally and 0.087% among declarations. Known-noise cases observed none;
zero observed failures is not zero risk or proof of 95% reliability.

Containment and target-tolerance success are different events: a narrow interval
can miss the truth while its midpoint is still within the looser .01 target.
Nonempty-set midpoint RMSE excludes incompatible trials and must never be shown
without the incompatible rate. All records and denominators are preserved.

Under ideal 128-shot observations, 17.86% of sets had multiple components. These
were retained, not replaced with whichever likelihood mode looked best. The
certification decision uses the full hull, including gaps.

**Important failure boundary:** model misspecification can leave a nonempty but
incorrect interval. Even 100% rejection of the particular inconsistent vector
does not establish universal model-error detection. The actual paper will need
defensible calibration/model discrepancy treatment or explicitly limited claims.

### Equal-cost direct sampling

At 128 shots/depth, the multidepth schedule uses 640 shots, 1,920 Grover calls and
4,480 A-equivalent calls. Direct sampling gets 4,480 depth-zero shots. Under known
eta=.01, median nonempty radius is .004925 versus .009261 for direct sampling;
.01-precision declaration rates are 99.43% versus 57.14%. This is a controlled
response-model comparison, **not practical advantage over classical pricing**.
Compiled gates, loading, calibration, and runtime are not matched by A-cost alone.
The same-count grid MLE has slightly lower point RMSE here; it has no calibrated
confidence interval in this implementation.

### Pilot result: no adaptive win yet

The independent pilot chose 128 validation shots/depth in 95.57% of trials.
Containment was 97.00%, and .01-precision completion was 99.29%. Mean total cost,
including pilot, was **7,315.2 A-equivalent calls**, compared with **4,480** for
fixed-128 and **17,920** for fixed-512. It is cheaper than the expensive baseline
but costs about **63% more than fixed-128**, without a completion improvement.
That is a negative result for this controller, not something to hide or re-tune
inside v1. The next controller needs harder heterogeneous application cases.

### Price and uncertainty limits

The L=1 and L=100 maps with deterministic bound B=.1 are illustrations only.
No actual option contract has gained a proved dollar-error certificate here.
For known-noise 128-shot trials, the L=100, one-dollar declaration rate is 98.14%;
under the envelope it falls to 76.64%. Application encoding bounds are still needed.

Per-cell exact binomial confidence intervals are saved in analysis outputs.
The pooled fixed-grid rows are heterogeneous, not IID samples of market contracts.
A conservative 95% Hoeffding band for their mean rate has half-width about 3.63
percentage points. Per-cell intervals are marginal, not simultaneous. For zero
failures in 1,400 independent trials, a one-sided 95% upper bound on their average
failure probability is about .214%, not zero. No population generalization is made.

## 4. Validation and reproducibility

Tests cover all branches, endpoint counts, noise-envelope inclusion, exact
enumerated small-sample coverage, incompatible sets, invalid inputs, independent
streams, exclusive output paths, price units, pinned upstream source, comparator
count pairing, quantile ranks, missing-truth handling and ideal Qiskit response.
The isolated sprint suite passes **32 tests**; its eight warnings concern the
existing legacy Qiskit installation, not failed assertions.
The final full repository regression passes **196 tests**, with nine legacy
Qiskit warnings, in 282.78 seconds. Machine-readable evidence is retained in
`results/journal_sprint/tests_final.xml` and copied into the verification archive.

From the repository root, using the existing environment:

```powershell
.\venv\Scripts\python.exe -m pytest research/journal_sprint/tests -q
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
.\venv\Scripts\python.exe -m research.journal_sprint.run_comparator --output results/journal_sprint/comparator_independent_rerun
.\venv\Scripts\python.exe -m research.journal_sprint.run_prototype --output results/journal_sprint/prototype_independent_rerun
```

Existing output directories cannot be overwritten. Seeds and configurations are
frozen in [protocol v1](PROTOCOL_V1.md). All raw comparator arrays, prototype
JSONL records, summaries, environment versions and input/source hashes are under
`results/journal_sprint/`. Analysis checks all expected records and historical
delta identities. Verification checks completed artifact hashes and snapshots
the final runnable source package.

Implementation maintenance after the runs was limited to formatting, the audit
path correction, extra tests/analysis, and rejecting invalid family-wise alpha
before division across depths. The experiment's alpha=.05 behavior is unchanged.
Planned-run hashes retain the actual earlier source fingerprints; the final
verification snapshot is explicitly a final source snapshot, not falsely labeled
as the exact bytes at the beginning of every earlier run.

## 5. Next work and unfinished checklist items

The [contribution matrix and validity argument](CONTRIBUTION_AND_VALIDITY.md)
define the candidate paper. Move next to a **small, prospectively frozen actual
pricing study**: verified price transformations and deterministic bounds, a
truth-blind representation/resource selector, calibration assumptions, and the
strongest fixed quantum and classical baselines. Begin with a tiny European
validation set; add an Asian stress case only after correctness.

Do not yet launch the original large noisy matrices or submit jobs to hardware.
Full BAE/BIQAE implementations and full-paper/appendix reading remain outstanding.
Paper B needs raw-data recovery or a fresh reproducible classical experiment.
Contributor responsibilities, weekly hours, compute limits and fee ceiling need
confirmation. The author has requested a lead-heavy split with two small genuine
collaborator packages; see [the proposed assignments](TEAM_WORK_PACKAGES.md).
Independent scholarly/code reproduction by those collaborators is still pending.
These are open items, so this report does **not** mark every two-week task complete.
The next concrete work is laid out in [the application experiment draft](NEXT_EXPERIMENT_DRAFT.md),
which is deliberately not labeled a frozen protocol.
