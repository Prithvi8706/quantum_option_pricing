# Week 3: circuit validation and baseline development

Latest: [classical baselines, larger resources and review status](WEEK_3_BASELINES_AND_REVIEW.md).
The classical matrix and larger-register profiles are now complete; pinned
BAE/BIQAE source smokes have run. Final environment/review checks and the PR
remain pending. The confirmation decision is hold, not a passed discovery gate.

## Earlier milestone record

The following dated circuit-milestone narrative preserves the state at that
milestone. For current test counts and completion status, use the latest link
above and the sequence disposition at the end of this document.

Update: [readout and dependence stress results](WEEK_3_STRESS_RESULTS.md) are now
complete at the response-model tier: 8000 datasets, 10000 inference records,
and an updated 73-test sprint suite. Classical baselines are next.

12 September 2026. The first week-3 milestone is complete: actual amplified
pricing circuits and logical resources, with two illustrative gate-noise channels.
The rest of week 3 remains in progress. No confirmation cases or hardware jobs
were launched, and week-1/2 outputs remain unchanged.

## Executed circuit gate

The prospective [circuit protocol](PROTOCOL_W3_CIRCUITS.md) specifies E001/E030,
n=3/4, payoff scales .125/.25 and Grover depths k=0/1/2: **24 actual circuits**.
The implementation uses the existing distribution and payoff preparation, its
inverse, the objective reflection and an all-zero reflection over the complete
input register. The circuit is compiled to u/cx at optimization level 0 with no
device coupling map.

All 24 statevector probabilities agree with independently calculated amplified
grid-objective probabilities to within **2.65e-14** (gate tolerance 1e-9).
For the 12 n=3 circuits, exact density-matrix results without noise also agree
with their statevector probabilities. These checks validate the ideal response
on this small matrix; they do not validate untested deeper/larger circuits.

| Distribution register | Actual total qubits | CX gates, k=0 | CX gates, k=1 | CX gates, k=2 |
|---|---:|---:|---:|---:|
| n=3 | 7 | 98 | 482 | 866 |
| n=4 | 9 | 148–152 | 1208–1220 | 2268–2288 |

The work/objective registers and zero reflection are not free. In this compilation,
moving from n=3 to n=4 more than doubles the k=2 CX count. Full compiled depths
range from 159 to 3693. These are all-to-all logical costs, not device-routed
gate counts or durations. The register sizes n=5/6 from the earlier candidate
matrix have not yet been profiled here.

The run took 19.31 seconds of local host time. Per-stage build, transpilation,
statevector and density-matrix times are recorded. The dense-storage estimates
are theoretical array sizes, not measured peak process memory. This timing is
not a projected quantum-device speedup.

## Noise result and model boundary

Each of the 12 smaller circuits was simulated with depolarizing lambda=.001 on
every compiled cx, and separately with amplitude damping gamma=.005 on every
compiled u. Noise models and eligible gate-location counts are archived. Other
gates are ideal; these are chosen channels, not measured calibration data.

The positive controls give probability 0 after full damping of an excited qubit
and probability .5 after full two-qubit depolarization. No shot sampling is
used: probabilities are taken from the saved density matrices.

Six of twelve amplitude-damping cases fall outside **every** prediction of the
earlier symmetric response family, even if eta is allowed to vary by case.
That family requires the noisy probability to remain between the ideal value
and .5. For example, E001/n3/c=.125/k1 has ideal probability .777624 but damped
probability .492552. E001/n3/c=.125/k0 moves from .402518 to .354486, away from
.5 rather than toward it. Thus the model fails here for structural reasons,
not merely because an unfortunate eta was selected.

All twelve depolarizing results remain inside their individual symmetric ranges.
This necessary condition does **not** establish that a common eta fits across
depths, or that the old illustrative envelope [.005,.015] is valid. No calibrated
envelope or hardware coverage claim is made.

These diagnostics were analyzed after the run and are labeled descriptive,
not preregistered parameter fitting. The next design must keep a model-only
claim, derive a broader valid response envelope, or explicitly reject the
unsupported channel family. It must not quietly treat gate error strengths as
the old per-A-equivalent eta.

## Preserved failure and implementation correction

The first run stopped at the damping control before any pricing case completed.
In a separate diagnostic, Aer returned `save_probabilities=[1,1]` while its saved
density matrix was `diag(1,0)` for the same fully damped circuit. This establishes
an inconsistent probability export in this installed environment; its deeper
dependency-level cause has not been established.

The retry computes the objective marginal directly from the density-matrix
diagonal and checks normalization and nonnegative diagonal entries. It does not
change the channel or pricing matrix. The initial failure remains in
`results/journal_sprint/week3_circuits_v1/failure.json`; the successful run is
`week3_circuits_v1_retry1`. No environment packages were changed.

Environment: Qiskit Terra .46.3, Aer .12.2, Finance .4.0, NumPy 2.0.2, SciPy
1.13.1. A later environment migration needs its own regression checks; it should
not silently alter existing reproducibility artifacts.

## Verification and artifacts

- Updated sprint suite: **69 passed, 11 legacy warnings, 13.82 seconds**.
  `results/journal_sprint/tests_week3_circuits.xml` records this run. The complete
  repository suite was not rerun this turn; its prior 225-test result remains
  documented in the week-1/2 closeout.
- All **94 successful-run artifact hashes** verified, including QPY circuits,
  source snapshots, protocol, channel dictionaries and per-case results.
- All **48 planned/completed execution events** reconcile to the 24 unique cases.
- Ruff passes for the sprint source under the existing vendor exclusion.
- Descriptive diagnostics and version information are in
  `results/journal_sprint/week3_circuit_analysis_v1/`.

Source: [circuit_gate.py](../../research/journal_sprint/circuit_gate.py) and
[analysis](../../research/journal_sprint/analyze_circuit_gate.py).

## Week-3 sequence disposition

1. Completed at the response-model tier: asymmetric readout and drift/correlation
   stress cases with predeclared outcomes. See the stress-results update above;
   hardware characterization and uncertain readout calibration remain unproved.
2. Completed: 480 costed classical estimates across European C6 and arithmetic
   Asian d=8/32, with independent-pilot CV and scrambled Sobol RQMC.
3. Completed at source-smoke tier: pinned BAE and BIQAE, with original interval
   and stopping semantics. No matched-performance or calibration-coverage claim.
4. Completed: 20 larger logical profiles after the declared initial smoke.
   Adaptive promotion is withheld; the existing fixed-choice evidence does not
   justify an adaptive superiority claim. Hardware costs remain unvalidated.
5. Decision: hold final confirmation. Discovery exposed response-model and
   conditional-delivery risks that must be resolved before protocol freezing.
6. Local verification and independent automated review performed; final fix
   recheck completed. Macroscope connection is still required before the PR.

Contributor acceptance, actual availability and publication fee ceiling remain
unconfirmed. Local-only compute and no paid services continue as working
constraints; this work does not invent anyone's contribution or approval.
