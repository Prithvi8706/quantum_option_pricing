# Week 14 comparator implementation and research audit

Post-acquisition cross-reference: the body below preserves the pre-implementation
audit snapshot. Its then-pending native IQAE integration and circuit checks are
now completed in [week14 results](WEEK_14_RESULTS.md). Source csAE remains a
response-model comparator, not actual-count circuit fitting. BAE/BIQAE Asian
integration, continuous certification and native stopping proof remain unclaimed.
See [final review](WEEK_14_REVIEW.md) and [claim/gate matrix](WEEK_14_CLAIMS_GATE.md)
for current dispositions; audit-only statements below describe the audit itself.

2026-09-16; branch `research/week14-comparisons`. Bounded source/document audit only: no experiments, dependency changes, commits or human review performed. Existing results below are historical evidence, not rerun results. Main-agent Week 14 implementation may advance independently of this snapshot.

## Integration decision

The concrete authorized plan uses native `qiskit.algorithms.IterativeAmplitudeEstimation` from installed **Terra 0.46.3**, a finite-shot `qiskit.primitives.Sampler` with a persistent Generator and an invocation ledger. Use unchanged vendored csAE `evaluate_schedule` with a fixed finite-Asian target and independently circuit-validated global depolarization response for the depth-limited and modern noise-aware arms. This is a faithful source estimator on a matched response model; it need not ingest circuit counts to serve this explicitly model-based comparison. BAE integration is not required when csAE meets this scope. Actual Asian circuit executions and model-generated comparator acquisitions must remain separately identified.

A project fixed ladder followed by conservative inversion is a legitimate project baseline. Neither that baseline nor a heuristic power selector may be named native IQAE, native BAE or faithful Labib ML. The following specific adapter assessment supersedes the broader candidate inventory's integration suggestions.

### Specific authorized adapter: source audit verdict

**Suitable for bounded development, conditional on the planned circuit-response checks.** No adapter execution or experiments were performed by this audit.

- Native arm: inspected `venv/Lib/site-packages/qiskit/algorithms/amplitude_estimators/iae.py` and Terra's `qiskit/primitives/sampler.py`; local distribution metadata confirms 0.46.3. Use this exact import rather than silently substituting the separately installed `qiskit_algorithms` package. Terra sampler accepts a `numpy.random.Generator` and uses it directly; passing a repeated integer seed instead constructs a new generator each call. Create one generator per trial, reuse it for sequential acquisitions, and await jobs in order. Set finite shots explicitly and retain actual metadata/counts. The native Terra loop has the same normalized-theta stop, repeated-power pooling, beta CP allocation and Grover-count convention discussed below. Coverage review remains qualified; native execution itself is feasible.
- csAE design: call `flagship_schedule(4, base=64)` with other defaults unchanged. Reading the source gives depths `[0,1,2,3,4]` and shots `[68,67,66,65,64]`: base64 is the deepest-rung shot count, not 64 at every rung. Per simulated trial this is **330 shots, 650 Grover calls, 1630 Aeq**, and **718 source-convention queries** (`650+68`). These values are analytical accounting from source, not executed measurements.
- Fixed target: `a_range=(sqrt(a),sqrt(a))` is supported by the source's `rng.uniform`; both endpoints equal produce the fixed b required here. Request `return_extra=True`, retain `counts` and `theta_hat`, and calculate `a_hat=sin(theta_hat)**2` and `O+S*a_hat` externally. The returned `errors`, percentile fields and C95 still concern b, so do not reuse them as Asian probability/price metrics. At a=0 or 1 retain the source grid's endpoint approximation and report it; do not silently modify the search.
- Noise arms: use eta=0 or .02, with `model_eta=eta` versus 0. The source generates counts before using the likelihood for estimation; equal trial count, seed, schedule, target and eta give the same K for matched/ignored pairs. Assert exact equality of returned counts and targets. This is paired inference on one dataset, not two independent datasets. Known eta is an oracle-parameter benchmark and carries no calibration-learning claim. Eta=0 makes matched and ignored likelihoods identical, providing an exact null check.
- Response validation: on the **whole circuit register**, define `D_eta(rho)=(1-eta)*rho+eta*I/d`. Apply this channel after every forward A and inverse A, including the initial preparation; apply ideal unitary reflections between these blocks. Full-register depolarization commutes with every unitary and preserves I/d. There are `2k+1` noisy blocks, hence final state `V*rho_ideal+(1-V)*I/d` with `V=(1-eta)**(2k+1)`. A single objective-qubit bad flag has projector rank d/2, giving exactly `V*cos^2((2k+1)*theta)+(1-V)/2`. This derivation establishes the proposed model identity; independent explicit DensityMatrix evolution should check its implementation at every scheduled k, including k=0. For a different good-state projector, replace 1/2 by its rank/d; the csAE formula then need not apply.
- Scope: this channel is global depolarization per A/A-inverse block, not independent one-qubit/per-gate depolarization or noisy reflections. Check the API's eta convention against the channel definition. Evolve each block explicitly for the validation, rather than imposing the final visibility formula on the ideal output and calling that an independent check. No postselection on clean ancillas is permitted in this identity. Density-matrix probability validation supplies model evidence; csAE binomial draws remain simulated acquisitions, not actual circuit jobs.

Minimal real source API, for the main adapter with already computed `a`, `seed` and `ntrials` (not a new CLI and not executed here):

```python
depths, shots = flagship_schedule(4, base=64)
out = evaluate_schedule(depths, shots, ntrials, seed,
                        a_range=(np.sqrt(a), np.sqrt(a)),
                        eta=0.02, model_eta=0.02, return_extra=True)
a_hat = np.sin(out['theta_hat']) ** 2
```

Reuse the same seed and eta with `model_eta=0.0` for the paired ignored-noise arm. Preserve unchanged vendor source and hash it in the run manifest. Circuit costs attached to these synthetic acquisitions are modeled execution costs from actual compiled circuit inventories; keep them separate from measured circuit-job costs. No posterior CI is claimed or required. The fixed-target replicate errors are empirical distributions at that target, not the reference paper's prior-averaged constants.

## Available code and native semantics

| Implementation and inspected location | Native stopping/output | Reuse status and assumptions |
|---|---|---|
| `qiskit-algorithms` **0.3.1**, locally installed at `results/journal_sprint/comparator_env/Lib/site-packages/qiskit_algorithms/amplitude_estimators/iae.py` | Adaptive `Q^k A`; stops when width of normalized theta interval is at most `epsilon_target/pi`; returns amplitude interval and its midpoint. `beta` means Clopper-Pearson here, not a Bayesian posterior. | Real native implementation. Uses V1 sampler results (`metadata`, `quasi_dists`), not BIQAE's V2 interface. Existing integration: `research/paper_a/scripts/run_smoke.py`, `recording.py`, `resources.py`; existing application wrappers in `src/quantum.py` are European/digital, not an Asian benchmark. |
| `research/journal_sprint/vendor/mlqae_core.py`, upstream `unitaryfoundation/csAE`, pin `202ffb8a462828d04dab13eef5005e295270d0e3` | Fixed `flagship_schedule(nmax, r=1.45, cap_divisor=1.3, base=1, slope=1)`; finish after prescribed shots, then coarse-grid ML, local zoom and quadratic interpolation. No native tolerance-stopping interval. | Apache-2.0 license and `vendor/NOTICE.md` present. `evaluate_schedule` generates its own binomial observations and random target amplitudes; no external-count input. Handles matched/ignored visibility noise. Native capped ladder is available; shot scaling is a specified design choice, not a new method. |
| `results/journal_sprint/external_bae_sparse/src/algorithms/BAE.py`, `algorithms/samplers.py`, `utils/models.py`; `alexandra-frca/BAE`, HEAD `4e1e13d6b151c9a3ca02157ebf6963c1c29ea793` verified | Adaptive posterior-utility acquisition with cost budget `maxPT`; checks budget before next acquisition, so final step may overshoot. Reports posterior means and SDs. Optional coherence learning uses a plug-in estimate. | `research/journal_sprint/bae_smoke.py` preserves upstream inference but fixes `a=.17`, `Tc=None`, `TNs=0`, 200 particles and nominal budget 200. No current Asian/noisy CLI. Model hook `measure` is an acquisition integration point; noise-learning calls require separate treatment. |
| `results/journal_sprint/external_biqae_sparse/src/biae.py`; `Kirin0570/BIQAE`, HEAD `bbd28a3efa659e1c0feec6b86ba13389cb127dbd` verified | Stops at amplitude interval width <= `2*epsilon`; Beta posterior quantiles with stage allocation; transports 1000 samples and fits a Beta prior between stages. | `biqae_smoke.py` uses an actual one-qubit ideal circuit, V2 local sampler and advancing RNG. Native algorithm has no hard acquisition budget; wrapper has a 1000-job safety cap. No readout/transfer-envelope likelihood. |
| BAE checkout `src/algorithms/IQAE.py` | Separate IQAE implementation, `modified=False` default, Chernoff-only assertion; theta-width stopping and accumulated same-power shots; `modified` changes allocation. | Available model-based source, not an additional validated Asian adapter. Do not mix its stopping/allocation with Qiskit's beta mode or identify it as the same implementation. |

The BAE/BIQAE HEAD checks establish revision identity only; wrappers additionally reject dirty checkouts before import. No fresh cleanliness, dependency or replay acceptance is claimed by this audit. External caches are not automatically approved redistribution assets.

### Native IQAE coverage and stopping audit

Inspected `iae.py` lines 286 onward: `T=int(log(min_ratio*pi/(8*epsilon))/log(min_ratio))+1`; beta intervals use `alpha/T`. Repeated equal-power acquisitions pool counts. The code assumes a constant batch size when adding previous shots, so fix actual shots per invocation. The Chernoff branch passes the current batch probability with pooled shot count; do not assume it has the same pooled-count behavior as beta without a separate audit.

The [original IQAE paper, v3](https://arxiv.org/abs/1912.05559v3) provides an ideal-oracle analysis. Operational assumptions here are independent finite-shot Bernoulli observations of `sin^2((2k+1)*theta)`, consistent state preparation/reflections, correct branch selection and the implementation's prescribed error allocation. A fixed-sample CP interval alone does not prove validity at an arbitrary adaptive stopping time. The match between repeated looks, theoretical rounds and this installed implementation remains a proof-review item, as already recorded in [Week 10](WEEK_10_MATCHED_DESIGN.md). This is not a demonstrated counterexample to IQAE's theorem.

Freeze epsilon, alpha, beta mode, min_ratio and finite batch size before development observations. “Fixed IQAE” should mean this fixed configuration; native IQAE still selects powers adaptively. There is no native `max_depth` argument in the inspected constructor. Clipping selected powers or replacing its stop rule produces a modified algorithm. An external safety cap must produce a retained censored/non-delivery record, not a successful native result. Fresh validation creates an explicitly modified procedure and its shots must be charged.

Require finite-shot metadata: the installed code has a separate exact-probability path when shots are absent, yielding a point interval and zero reported Grover queries. That path is not evidence of finite-shot cost-to-tolerance or nonzero-depth execution. Reconcile `result.powers` with invocation records because Qiskit includes a leading sentinel zero; reuse `research/paper_a/resources.py::executed_powers` rather than counting it as a circuit.

### Depth-limited and noise-aware interpretation

The [Labib reference, v1](https://arxiv.org/abs/2609.02715v1) is prior work on geometric schedules and noise-aware/depth-limited estimation. The inspected source estimates `b=sin(theta)` from **cosine-squared** observations and draws `b` uniformly in `(0.1,0.9)` by default. Its empirical error percentiles and C95 are prior-averaged benchmark quantities, not per-target confidence intervals. The interval on C95 in `run_comparator.py` is uncertainty about an error quantile, not an interval for an Asian price. Source comments describing exact global optimization do not establish a machine-verified global optimum for the finite-grid search.

For an Asian objective with `a=sin^2(theta)` and one-counts `H_k`, the convention-preserving transformation is `K_k=N_k-H_k` for the source cosine likelihood and `a_hat=sin(theta_hat)^2` on output. Do not directly use `b` errors as probability errors. An observations-only adapter would be needed only for a future claim that csAE fitted actual circuit measurements. The authorized unchanged-source fixed-target model benchmark does not require that extension; changing `a_range` fixes its simulated target but does not make it consume actual Asian observations.

Its visibility is `V_k=(1-eta)^(2k+1)` and response `V_k*cos^2((2k+1)*theta)+(1-V_k)/2`. `model_eta=None` uses the supplied true eta; label this known-noise/oracle-parameter inference, not learned calibration. `model_eta=0` is a paired ignored-noise ablation. Actual per-gate depolarization, amplitude damping, asymmetric readout and calibration-transfer envelopes are not established equivalents of this scalar visibility model.

The [BAE paper, v5](https://arxiv.org/abs/2412.04394v5) explicitly treats noise-aware adaptive estimation. Local `QAEmodel` uses `exp(-k/Tc)*sin^2((2k+1)*theta)+(1-exp(-k/Tc))/2`; its calibration experiment uses `(1+exp(-ctrl/Tc))/2`. These are different from Labib's visibility even at k=0. Match each comparator to its declared model or label the mismatch. The source's posterior SD is not a 95% frequentist interval, and a learned plug-in Tc does not propagate finite calibration uncertainty. Upstream unseeded `default_rng` resampling prevents deterministic replay from the smoke's global seed alone.

The [BIQAE paper, v2](https://arxiv.org/abs/2507.23074v2) supplies Bayesian acceleration prior art. Its inspected Beta fitting/quantiles must retain their posterior interpretation; the paper's claims do not by themselves certify finite-shot noisy Asian coverage. See the earlier [native semantics audit](WEEK_7_COMPARATOR_SCOPE.md) and [literature supplement](LITERATURE_SUPPLEMENT.md) for the existing appendix qualifications. Fresh browsing here refreshed primary abstract/version records, not a full rereading of every proof; the BAE publisher page failed and arXiv was used instead.

## Finite Asian target and response requirements

`research/journal_sprint/asian_encoding.py` provides a small conditional Gaussian midpoint grid (at most eight normal-register qubits), tabulated raw or AM-GM residual payoffs, and circuit preparation pieces. Fix the contract, grid, representation, weights, payoff normalization, objective bit and reflection convention for every arm. The common encoded target is `a=sum_i w_i*y_i/S`, with dollar map `O+S*a`. For this week14 protocol the residual offset is the FINITE geometric expectation, so both representations target the same finite arithmetic price. Week13 separately recorded the analytic continuous-model offset and its different application approximation. Give classical finite summation and sampling the same control identity.

For each actually executed nonzero k, compare ideal circuit objective probability against `sin^2((2k+1)*asin(sqrt(a)))` before using a synthetic response table. Verify the full preparation/inverse/reflection construction, including ancilla cleanup and bit order. A one-qubit rotation set from known a can check estimator plumbing but cannot establish Asian oracle preparation resources. Numerical agreement is diagnostic, not an outward-rounded certificate.

For a continuous-price claim, require a justified total deterministic bound B and `epsilon_a=(dollar_tolerance-B)/abs(S)>0`; map interval endpoints once and expand by B. Current Asian bound records explicitly leave implementation/enclosure components unbounded. Therefore finite-target comparisons may proceed while certified continuous Asian delivery remains blocked. Zero-payoff tables should use exact zero rather than invoke AE.

## Existing executable reuse commands (not executed here)

From the repository root, these commands address real existing entry points. Output directories must be absent. They reproduce their existing scopes only; none is an Asian circuit comparator command. Environments exist locally, but runtime dependencies were not tested in this audit.

```powershell
.\venv\Scripts\python.exe -m research.journal_sprint.run_comparator --output results/journal_sprint/week14_reference_replay
.\venv\Scripts\python.exe -m research.journal_sprint.bae_smoke results/journal_sprint/external_bae_sparse results/journal_sprint/week14_bae_smoke
.\results\journal_sprint\comparator_env\Scripts\python.exe -m research.journal_sprint.biqae_smoke results/journal_sprint/external_biqae_sparse results/journal_sprint/week14_biqae_smoke
```

The first command is the existing full six-case reference reproduction, not a bounded Asian smoke. It includes 160,000 estimations and paired noise data; budget separately before choosing to run it. No native Asian CLI was found in the inspected snapshot. Reuse Qiskit's `EstimationProblem` and installed `IterativeAmplitudeEstimation` through a new finite-shot adapter; do not invent flags on the old runners. Keep V1 IQAE and V2 BIQAE result formats explicit.

## Cost ledger and blocked claims

For every actual acquisition j retain k, requested/effective shots, counts, circuit identity, status and native stop/cap reason. Report `N=sum N_j`, `Q=sum N_j*k_j`, and `Aeq=sum N_j*(2*k_j+1)` separately. Aeq counts k+1 forward A and k inverse A per shot; include reflection gates in compiled resources. Native IQAE/BIQAE report Q. Labib reports `sum N_k*k + N_0`; preserve that historical unit alongside Aeq. BAE uses probing cost `(2*k+1)*N`; noise-learning controls require their own physically justified ledger, not automatic relabeling as integer Grover circuits.

Count warmup, calibration, pilot/selection, all repeated shots, discarded/replacement data and final budget overshoot. Historical Week 3 records report BAE 223 Aeq for nominal 200, and BIQAE 40 Q versus 180 Aeq; these are plumbing examples, not performance rankings. Keep unknown costs on failed jobs unknown rather than silently treating them as zero.

Record per-circuit compiled CX, depth and qubits plus shot-weighted CX; maximum depth is not the sum of circuit depths. Separately charge table enumeration, state preparation construction, transpilation, ML/particle fitting, calibration fitting and classical payoff evaluations. Show setup amortization explicitly. Simulator wall time is not device runtime. Exact finite summation is an essential baseline because the current oracle itself uses an enumerated table; strong MC/control/RQMC comparisons need the same target and setup accounting.

For the concrete plan, remain blocked on unperformed native Asian integration/execution, explicit circuit-response checks, implementation-specific claims of certified stopping coverage, continuous-price numerical/error enclosure, and any superiority/speedup/crossover claim beyond acquired evidence. BAE integration and a circuit-count Labib adapter are **not** gates for the authorized fixed-target csAE response-model comparison. They would become relevant only if those additional native methods or actual-count fitting were claimed. A comparator-only synthetic result does not close the actual-circuit requirement; the main plan's separate nonzero-k executions must supply that evidence.

## Prior work, distinction and collaborator review packet

No novelty is established by this audit. IQAE, capped geometric ladders, noisy likelihoods, Bayesian adaptive scheduling, independent validation, AM-GM control residuals and explicit error/cost accounting are prior work or standard methodology. The potential contribution is a carefully bounded empirical limitation/reliability study for specified finite Asian encodings, contingent on review and completed evidence. Replacing upstream inference with project inversion compares acquisition schedules under project inference; it is not native-comparator coverage or a new AE algorithm. Preserve negative results and the earlier failed/tied acquisition gates.

Prepare a bounded packet containing this audit; `WEEK_7_COMPARATOR_SCOPE.md`; `WEEK_10_MATCHED_DESIGN.md`; `WEEK_13_CLOSEOUT.md`; the Week 14 frozen protocol when available; comparator source/environment hashes and licenses; one complete successful trace and one capped/failure trace per implemented arm; independent response formulas and circuit checks; cost reconciliation; ablation table; and the exact proposed manuscript claims. Missing artifacts must be marked missing, not replaced with old smoke results.

Human collaborator review has **not** occurred. This document is an agent audit, not collaborator sign-off. No review request was sent. Proposed review checklist:

- [ ] Comparator reviewer verifies pinned algorithm, adapter-only changes, count convention, native stop and posterior/confidence wording.
- [ ] Statistical reviewer resolves IQAE rounds/repeated looks, nuisance assumptions, multiplicity and treatment of capped trials; distinguishes empirical containment from a theorem.
- [ ] Circuit reviewer independently checks actual Asian A, inverse/reflections, k>0 responses, noise applicability and full resource ledger.
- [ ] Application reviewer verifies common finite/continuous targets, residual offset, classical simplifications and all required price bounds.
- [ ] Claims reviewer checks prior-work attribution, negative results, absence of unsupported novelty/advantage, and a defensible limitation-study contribution.
- [ ] Record reviewer names, date, scope, objections, dispositions and explicit sign-off; unresolved issues retain development status.
- [ ] Freeze primary application/outcomes, held-out regimes, seeds, caps and analysis before confirmation; approval of this packet is not presumed.
