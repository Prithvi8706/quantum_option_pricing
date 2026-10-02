# Prospective analysis specification, Stage C — classical comparator and financial checks

Version 2.1, 1 October 2026. Committed before any Stage C run. It covers plan items C1–C8
(classical CPU/GPU comparator and statistics) and Q4 (payoff validation). Version 1 was
reviewed by three critic agents (statistics, fairness, feasibility; 56 findings, none
critical). Version 2 was then checked by a closure reviewer (49 closed, 7 partial, 14 new
problems, all addressed in 2.1). The dispositions are in
[reviews/STAGE_C_SPEC_REVIEW.md](reviews/STAGE_C_SPEC_REVIEW.md).
"Item C*n*" means a plan work item; "claim C*n*" means a paper claim. Gates check that each
item was executed as written. Outcomes are recorded whichever way they point. The git
commit is the only time stamp; nothing is registered externally.

## 0. Common rules

- **Environment.** T0 (`t0_requirements.lock`; receipt
  `results/frontier_replay_20261001/t0_environment.json`). Code in
  `research/frontier_classical_20261001/`; outputs in
  `results/frontier_classical_20261001/<item>/`. Runners refuse to overwrite an existing
  output directory. Every JSON records the seeds, code SHA-256, this file's SHA-256, the
  lock SHA-256 and SHA-256 of every factor L used. Archived evidence is read only.
- **Clean checkout.** Every Stage C run executes from a detached git worktree of a
  committed revision (recorded in its JSON), never from the shared working tree. Another
  session edits that tree concurrently, including uncommitted changes to
  `research/controlled_source_completion/`, which item C7's compilation imports.
  This file is frozen at its commit; later changes are only an appended, dated deviation
  log. Committed Stage C code may be added after it.
- **Executions.** The first complete execution of an item from a committed revision is
  primary. A re-run is allowed only after a crash, a failed validation, or a defect found
  by a test; its reason is logged in the deviation log before it starts, and every
  execution is reported. Code that affects timing is fixed at a recorded commit before the
  first timing run and is not changed after timings are seen.
- **Threads and memory.** Every runner sets OPENBLAS/MKL/OMP/NUMBA thread counts to 1
  before importing numpy (ERRATA E10). Sobol points are streamed in chunks of 2^12 (2^16
  for GPU feeders) through `Sobol.random`; no worker holds more than one chunk. Every Sobol
  run size and prefix is a power of 2 (iid runs are not restricted). When a Sobol run size
  is below 2^12 it is drawn as a single chunk of that size.
- **Contract.** Equal-weight arithmetic basket of `na` correlated GBM assets, `nt` equally
  spaced monitoring dates on (0, T]. Payoff `e^{-rT}(A − K)+·1{basket(t_j) < H ∀j}`, A the
  average over all asset/date prices. Exact-date simulation, no SDE bias. Development
  cases: S0 = 100, K = 100, σ = 0.3, equicorrelation ρ = 0.4, r = 0.03, T = 1, H = 140,
  shapes 4×12 and 8×52.
- **Case index** (fixed now, used in every seed key): 4×12 = 0, 8×52 = 1; item C7 cases
  2–8 in the order listed there; item C8 cases 100 + 4s + j.
- **Randomness.** Every generator is seeded by a five-word key
  `SeedSequence([root, case_index, purpose, replication, stream])`; Sobol generators
  (`scipy.stats.qmc.Sobol`, LMS + digital shift) use `stream` = scramble index.
  - Roots: C1 2026100111, C2 2026100121, C3 2026100131, C4 2026100141, C5 2026100151,
    C6 2026100161, C7 2026100171, C8 2026100181, Q4 2026100191, rotations 2026100101,
    bootstrap 2026100112, σ_Q 2026100107 (all items and cases).
  - Purpose: 0 rate; 1 timing; 2 Ref B iid; 3 confirmation; 4 coverage; 5 Ref A; 6 Q4 draws;
    7 σ_Q; 8 Q4 law and flip paths; 9 plain-MC anchors.
  - Replication: 0 for rate runs. Timing repeats: 0–4 warm, 5 fresh-cached, 6 cold, 10–14
    load-balanced. Confirmation: 100·eps_index + r, eps_index 0–3 for ($0.10, $0.03,
    $0.01, $0.001), r = 0–19. Coverage: 0–999, and 1000–1999 for the 4×12 2^17 arm. Q4
    draws: 0 iid, 1 near-barrier, 2 edge; Q4 paths: 0 law, 1 flip. Otherwise 0.
  - `stream`: scramble index, worker index, or 0.
  - Basis variants of one item share their scrambles (paired design). The only reuse of
    an old root is the item C1 port check, which reuses P3's key `[2026092333, dim, s]`
    and is disclosed as such.

### 0.1 Canonical PCA factor

The covariance `Σ_asset ⊗ Σ_time` has exactly repeated eigenvalues: (na−1)-fold for every
time mode (4×12: twelve 3-fold; 8×52: fifty-two 7-fold; 16×52: fifty-two 15-fold).
`numpy.linalg.eigh` returns a basis inside them that depends on the LAPACK build, its
thread count and the numpy version. That changed the 8×52 estimates between the archived
run (numpy 1.26.4, MKL, one thread) and the T0 replay (numpy 2.0.2, OpenBLAS, one thread)
(ERRATA E10). Stage C uses closed forms, with no LAPACK call:

- asset factor: column 0 = `1/√na` (eigenvalue σ²(1+(na−1)ρ)); columns 1…na−1 = the rows
  of `scipy.linalg.helmert(na, full=False)`, i.e. `h_k(i) = 1/√(k(k+1))` for i ≤ k,
  `−k/√(k(k+1))` for i = k+1, else 0 (eigenvalue σ²(1−ρ));
- time factor for `t_i = iT/nt`: `v_m(i) ∝ sin((2m−1)iπ/(2nt+1))`, unit norm (first entry
  and sum positive), eigenvalue `(T/nt)/(4 sin²((2m−1)π/(2(2nt+1))))`;
- index = asset·nt + date; columns `(u_a ⊗ v_m)·√(λ_a μ_m)` ordered by
  `np.lexsort((m, a, −λ))` (eigenvalue descending, then asset index, then time index).

Tests: `L Lᵀ = Σ` to 1e-12; first column positive; the 4×12 column order and its first two
eigenspaces equal hard-coded values; L bit-identical with 1 and 22 BLAS threads.

### 0.2 Basis roles (fixed now)

- **Primary:** the canonical factor for every case and every downstream quantity.
- **Rotations:** q = 1…4. Inside each exactly repeated eigenspace of dimension d, taken in
  canonical column order: draw G (d×d standard normal) from
  `default_rng([2026100101, case_index, q])`, QR-factorise, and set
  `Q = Q_G·diag(sign(diag R_G))`, `L_E ← L_E Q`. Four rotations sample the basis family;
  they do not bound it.
- **Development cases also run** the archived factor and the T0 eigh factor (one thread).
  This separates the basis effect from the protocol effect relative to the recorded
  decision. Factor SHA-256 (of `L.tobytes()`, float64 C order):
  - 4×12: canonical `4bfc6ae9…a233a39`; archived = T0 eigh `1d1c4595…3abb800c` (this
    factor reproduced the 4×12 archive exactly in Q0);
  - 8×52: canonical `57a0d320…ecd28606f6`; archived
    (`q0_attribution/L_8x52_numpy1.26.4_single_thread.npy`) `f27a6b1d…ce81e16e`; T0 eigh
    `f980fbab…2ebbbf`.
- **Quantum-favourable sensitivity:** the basis with the largest T_C($0.001) among those
  run for a case. The decision-point table is recomputed under it. **Classical-favourable
  sensitivity:** the basis with the smallest T_C($0.001), labelled as selected after
  seeing outcomes. Paired bootstrap intervals of `r_basis − r_canonical` are reported.
- **T_C for basis rows.** Only the canonical factor gets measured confirmation. Every basis
  row (and the e_C row of section 0.4) uses the item C2 all-16 warm model at that row's
  n(ε). Candidates without basis variants keep their canonical T_C. The canonical row is
  also shown on the model convention, so rows compare like with like.

### 0.3 Classical comparator (fixed now)

For each case and ε, **T_C is the minimum of the primary T_C over every validated
estimator and both platforms** (DECISION §6, "the measured best classical method"). The
candidates are item C1 `rqmc` and `preint`, item C5 OSS-BB and OSS time-ordered, the item
C6 GPU kernels (including float32 variants admitted under the C6 rule), and the GPU and
CPU plain-MC anchors.

- **Validated** means the estimator passes the agreement test
  `|estimate − reference| ≤ hw99(estimate) + hw99(reference)` against the item C4
  reference, at its largest run (RQMC methods: 32 scrambles at 2^19; anchors: at N($0.001)).
- **Anchors** are timed end to end, like every other candidate: from launch to the final
  mean and half-width, including RNG setup, transfers and reduction, at
  `N(ε) = ⌈(z_{.995}·σ_Q/0.45ε)²⌉` paths. Primary = median of 3 runs, or 1 run where a run
  exceeds 10 minutes.
- The method and platform attaining the minimum are recorded per (case, ε).
- Labels: the preint-CPU-only T_C is a QF sensitivity. Taking a minimum over noisy
  candidates is CF (selection bias); the paper states this, and gives the runner-up next
  to the minimum.

### 0.4 Accuracy contract and σ_Q

- ε ∈ {$0.10, $0.03, $0.01, $0.001}; statistical share 0.45ε at 99% confidence, on both
  sides (historical allocation). Disclosed as quantum-favourable: the 0.55ε reserve exists
  for the quantum oracle's numerical and law error, which exact-date float64 classical
  pricing does not have. A classical-favourable sensitivity with e_C = 0.9ε (quantum
  unchanged) is in the decision-point table.
- Primary decision point: ε = $0.001, t_layer = 100 ns, k = 3.
- **σ_Q** (ERRATA E6 plain-payoff convention), every case: the ddof = 1 sample sd of the
  discounted plain knock-out payoff over 2^20 iid exact-date paths in the canonical
  factor, normals from `SeedSequence([2026100107, case_index, 7, 0, 0])`, with a bootstrap
  95% interval. This is primary in every D_max. For the development cases, P1's archived
  values (2^14 paths, ddof 0) and Ref B's sd are reported beside it, not substituted.

### 0.5 Bias labels

Every choice that is not neutral carries a label in the tables: quantum-favourable (QF)
or classical-favourable (CF). A larger classical T_C is QF, because
D_max = T_C/(10·Q·t_layer). Where a choice is uncertain the primary is QF, and the CF
alternative is a labelled sensitivity. Labels fixed now beyond those in the items:

- **QF:** the 0.45ε classical share; the one-sided pooled-accuracy scaling in item C2; host
  generation of GPU uniforms; excluding float32 unless it passes ε/10, while Q4 only reduces
  the quantum share; the item C4 recalibrated T_C; the all-16 primary in items C7 and C8.
- **CF:** the minimum over noisy candidates; warm-only primary T_C.

## Item C1. RQMC rates with uncertainty

- **P3b** (numba, 16 worker processes, one scramble per task). The primary per-chunk
  pipeline is P3's, pinned: `Sobol.random(2^12)` → `scipy.special.ndtri(clip(u, 1e-15,
  1−1e-15))` → single-thread BLAS GEMM → numba estimand (`cache=True`, `fastmath=False`).
  In rate runs the factor is cached per worker process. In timed runs (item C2) each run
  builds it once per worker inside the timed interval. A numba inverse normal or fused GEMM
  may be timed only as a CF sensitivity.
- Methods: `rqmc` (plain payoff) and `preint` (first-PC preintegration). Payoffs:
  knock-out, and for claim C2 the arithmetic basket call and the digital `100·1{A > K}`
  (P1 definitions). Deviation, stated now: P3b supersedes P1; P1's `rqmc_cv` rates for calls
  and digitals are cited only as historical point estimates without intervals.
- 32 scrambles per (case, basis); prefixes n = 2^6 … 2^19; every per-scramble prefix mean
  is archived.
- **Port check, run before any canonical run:** P3b `preint` knock-out with P3's root
  2026092333, Sobol stream `[2026092333, dim, s]`, s = 0…31, 2^12 chunks, n = 2^17, and the
  factor built as P3's `setup()` with one BLAS thread. The 8×52 factor hash must equal the T0
  single-thread hash in `q0_attribution/attribution_summary.json` (`f980fbab…`). Pass:
  every per-scramble prefix mean within 1e-12 relative of P3 run in the same environment,
  and the price within 1e-12 of the Q0 replay. A hash mismatch is a setup failure. Neither
  failure is re-run under other settings. A port or setup failure blocks item C1; any
  continuation is an appended, dated deviation.
- **Fit.** OLS of `log sd(n)` on `log n`, sd over scrambles of the prefix means.
  Primary window m ∈ [10, M] (M = top prefix: 19 here). Sensitivity windows [8, M],
  [12, M], [14, M]. Local slopes between consecutive m are reported.
- **Uncertainty.** Whole-scramble bootstrap (resample the 32 scrambles with replacement,
  keeping each full trajectory), B = 4000, index matrix from
  `default_rng([2026100112, case_index, 0, 0, 0])`, shared by all bases of the case.
  Percentile 95% intervals for r and A; joint (A, r) draws propagated to n(ε) and T_C(ε).
- **n(ε)** solves `t_{.995,15}·A·n^{−r}/√16 = 0.45ε` with the primary point estimates; no
  floor. Flags: extrapolated-high if n(ε) > 2^M, extrapolated-low if n(ε) < 2^10. The
  bootstrap summary gives the fraction of joint draws outside [2^10, 2^M].
- **Claim C2 rule**, applied identically to every (case, payoff, method) in items C1, C5 and
  C7, using the primary-window bootstrap 95% interval for r under the canonical factor:
  *restores* if the lower limit ≥ 0.9; *does not restore* if the upper limit < 0.9;
  otherwise *inconclusive*, reported with its interval. Claim C2 states each half only for
  the cases where it holds. A restoring knock-out case is named as a counterexample, and the
  general negative is then removed. The basis extremes are reported next to each label.

## Item C2. Timing and measured time to accuracy

Scope: development cases; knock-out payoff; methods `rqmc` and `preint` (and the item C5
and C6 methods under the same protocol).

- **Start states.** Warm: workers alive, cache loaded, a warm-up call done. Fresh-cached:
  new worker processes with a populated numba cache. Cold: empty `NUMBA_CACHE_DIR`. Every
  wall time runs from task submission to the final 16-scramble mean and interval,
  including per-run setup (factor, Sobol construction, dispatch, reduction).
- **Primary T_C is warm.** This is CF relative to the recorded decision (ERRATA E5) and to
  the complete-latency standard. It is justified because quantum compilation and
  start-up are also excluded. Fresh-cached T_C is carried into the decision tables as a QF
  sensitivity. Cold is reported only.
- **Repeats.** 5 warm, 1 fresh-cached and 1 cold repeat of 16 scrambles to n = 2^19.
- **Timing conventions**, each fitted as `T(n) = a + b·n` on marks n ≥ 2^13:
  (i) per-scramble median (historical; ERRATA E5); (ii) **all-16: submission until all 16
  prefix means exist (primary; QF** relative to (i) and (iii) on this hybrid P/E-core CPU);
  (iii) load-balanced: (scramble, 2^12-chunk) tasks using `Sobol.fast_forward`, on a
  dynamic pool of 22 workers, 5 warm repeats (CF sensitivity). Each convention is fitted by
  OLS on the per-mark medians over its repeats; ranges over repeats are reported.
- **Measured confirmation**, for ε ∈ {$0.01, $0.001} and each (case, method) with
  n(ε) ≤ 2^21:
  - n(ε) is the item C1 primary point estimate (canonical factor); n_run =
    2^⌈log2 n(ε)⌉ (QF; keeps Sobol balance);
  - 20 replications of the 16-scramble estimator with fresh scrambles,
    key `[2026100121, case_index, 3, 100·eps_index + replication, s]`;
  - record each replication's wall time and achieved 99% t half-width;
  - primary T_C = the median wall time;
  - pooled check: the per-scramble sd at n_run is estimated from all 320 scrambles, and
    hw16 = t_{.995,15}·sd/4. If hw16 > 0.45ε, primary T_C = median wall time ×
    (hw16/0.45ε)^{1/r}. n is never re-chosen;
  - also reported: the fraction of replications with half-width ≤ 0.45ε, and the model
    T_C at the unrounded n(ε) (CF sensitivity).
- **Where no confirmation is run** (ε ∈ {$0.10, $0.03}, or n(ε) > 2^21): T_C is the
  all-16 model a + b·n(ε), marked modelled. If n(ε) < 2^13, T_C is the median over the warm
  repeats of the all-16 elapsed time at the smallest prefix mark ≥ max(n(ε), 2^6).
- **Machine state.** Primary timings run on AC power under the T0 Balanced plan, disclosed
  as plausibly QF. The plan is never changed between primary repeats. Any
  higher-performance plan runs afterwards as a labelled CF sensitivity, chosen by the
  author. CPU model, core counts, worker count and the absence of affinity are recorded.
  Load is recorded as Windows `\Processor(_Total)\% Processor Time` averaged over the 30 s
  before the run, plus the list of running python processes (see the exclusivity rule).

## Item C3. Independent reference prices

For 4×12 and 8×52:

- **Ref A: one-step survival (OSS), RQMC.** P2's basket OSS (survival-truncated first
  asset-PC normal; product of conditional survival probabilities), ported to numba, with
  the canonical asset basis. n = 2^22 per scramble, 64 scrambles (key
  `[2026100131, case_index, 5, 0, s]`), fixed now. From P2's
  rates the expected 99% half-width is about $2×10⁻⁴ (4×12) and $5×10⁻⁴ (8×52). The plan's
  ε/10 resolution is therefore not expected, and this is stated now as a limitation.
  Deviation from plan item C3: Ref A is time-ordered OSS, not bridge-ordered, so that the
  reference does not depend on item C5, which may be cut. Bridge-ordered OSS is item C5's
  OSS-BB, compared with Ref A there.
- **Ref B: plain iid Monte Carlo** (exact-date one-factor stepping: a common normal plus na
  idiosyncratic normals per date; plain knock-out payoff) in numba on 16 CPU worker
  processes, each with a PCG64 stream from `SeedSequence([2026100131, case_index, 2, 0,
  worker])`. Budget, fixed now: 6 machine wall-clock hours per case on the 16-process pool
  (96 process-hours per case, 12 hours for both, one overnight slot). This exceeds the
  plan's 40–60 CPU-hours if that is read as core-hours, and falls below it if read as
  wall-hours; the reading is disclosed. Expected hw99 is about $4×10⁻⁵ (4×12) and $1.1×10⁻⁴
  (8×52). The run stops at the budget whatever the running difference. The GPU is not used
  for Ref B. hw99 = z_{.995}·SE.
- **Agreement tests.** hw99 uses t_{.995,63} (Ref A), z_{.995} (Ref B) and t_{.995,31}
  (P1, P3). Primary: Ref A vs Ref B per case, pass if `|A − B| ≤ hw99(A) + hw99(B)`.
  Secondary: P3 (archive and Q0 replay), P1 and P3b against the item C4 reference, each
  with z and a two-sided p, Holm-adjusted. A secondary failure does not change the
  reference. The P1/P3 4×12 gap (2.06 SE, p ≈ 0.04) is not significant at 1%, and item C3
  does not claim to explain it. The test's resolution is hw99(A) + hw99(B); the gap counts
  as resolved only if that is ≤ $10⁻⁴, which is not expected.
- **Item C4 reference.** If the primary test passes: the inverse-variance-weighted mean of
  Ref A and Ref B, hw99 = 2.576·(SE_A⁻² + SE_B⁻²)^{−1/2}. If it fails: both prices are
  reported; item C4 is run against each, and the reference giving the lower coverage
  decides under-coverage (QF); item C5 and the validation tests must pass against both.

## Item C4. Coverage of the classical interval

- Per development case: R = 1000 independent 16-scramble `preint` estimators (canonical
  factor; key `[2026100141, case_index, 4, replication, s]`, replication 0–999, and
  1000–1999 for the 2^17 arm), each run to 2^13. The nested
  prefixes give n ∈ {2^10, 2^11, 2^12, 2^13}; coverage across n is therefore dependent.
  For 4×12 only, a fifth arm at n = 2^17 (R = 1000). For 8×52, coverage at the decision-point
  n is not tested, and the paper states that it is assumed.
- Nominal 99% and 95% t-intervals (t_{.995,15}, t_{.975,15}). Coverage = fraction containing
  the item C3 reference; Clopper–Pearson 95% intervals; raw and with the interval widened
  by hw99(reference). A row whose reference hw99 exceeds 0.25× the 95% interval
  half-width is labelled reference-limited.
- **Primary check:** raw 99% coverage at n = 2^13 per case. If its Clopper–Pearson interval
  at level 1 − 0.05/18 (18 coverage cells in total) lies entirely below 0.99, the interval
  is declared under-covering. Then c = the empirical 0.99 quantile of
  `|estimate − reference|/(s/4)` over the R replicates replaces t_{.995,15}. Every RQMC
  candidate's primary T_C is multiplied by (c/t_{.995,15})^{1/r} with its own r, with no
  re-run; this is primary (QF), and the t-based value is a sensitivity. The anchors (iid,
  large N) and items C7/C8 are unchanged, and their coverage is stated as assumed.
  Over-coverage changes nothing.
- **Symmetric-rigorous sensitivity** (calculation). Both sides use the knock-out range
  R = e^{−rT}(H − K) and δ = 0.01. Classical: the smallest n with
  `√(2V ln(4/δ)/n) + 7R ln(4/δ)/(3(n−1)) ≤ 0.45ε` (Maurer–Pontil empirical Bernstein,
  two-sided), V = Ref B plain variance; the preint variance is a CF sensitivity. Quantum: k
  from plan item L3 for range R and σ_Q. This row is reported only once L3 is complete; the
  archived compound schedule is not used.

## Item C5. Stronger classical smoother

- **OSS-BB (primary item C5 method):** asset PCs 2…na are generated by Brownian bridge
  across dates, independently of the first asset PC. The first asset-PC increment at each
  date is drawn sequentially from the survival-truncated law. Sobol order: dims 1…nt are
  the PC1 increments in date order; then bridge levels, coarsest first, with the na−1 PCs
  interleaved inside each level (level-major, PC 2 first). No preintegration.
- **OSS time-ordered** (P2's construction in numba) is the secondary method.
- Each method gets item C1 rates (canonical asset basis, all bases of section 0.2 not
  required), item C2 timing, and the claim C2 rule. Unbiasedness passes if
  `|method − C4 reference| ≤ hw99(method) + hw99(reference)` at 2^19 × 32 scrambles.
- **Not executed in Stage C, recorded as not done:** multi-direction numerical smoothing
  (Bayer, Ben Hammouda, Tempone), barrier importance sampling (DECISION §6), preint combined
  with bridge-ordered OSS, and the importance-sampling-based smoothing of Xie, He and Wang
  (2019), which reports an improved rate for discrete barriers. PREREGISTRATION_DEVIATIONS
  row 2 stays open, and claims C2 and C4 name these methods as untried.

## Item C6. GPU comparator

- Port the `preint` kernel to `numba.cuda` in float64; also port item C5's best method if
  its primary CPU T_C($0.001) is lower than preint's. Scrambled Sobol uniforms are
  generated on the host with scipy (same seeds as the CPU run) by exactly 4 feeder
  processes, in chunks of 2^16 points, written to double-buffered
  `multiprocessing.shared_memory` blocks and copied to the device as float64. Inverse
  normal (CUDA `normcdfinv`), the PCA product and the estimand run on the device. The
  feeder count, chunk size and transport are not tuned after timing. Host generation is
  labelled QF: feeder and transfer throughput (about 0.9 GB/s of float64 uniforms at
  8×52) may bound the end-to-end rate. Kernel-only time is its CF bound.
- Validation: GPU and CPU estimates on identical points agree to 1e-10 relative at 2^16
  points, both development cases.
- Timing under the item C2 protocol. **Primary GPU T_C = end-to-end** from submission to
  the final mean. Sensitivities: kernel-only and 8 feeders (CF); host ndtri + GEMM as in P3
  (QF).
- Float32 or mixed precision is an eligible comparator (section 0.3) at ε if, on identical
  points at n_run over the 32 item C1 scrambles,
  `mean|d_s| + t_{.99,31}·sd(|d_s|)/√32 ≤ ε/10`, where d_s is the per-scramble difference
  from float64. This is the same allowance as Q4 gives the quantum oracle.
- **Plain-MC anchors:** `numba.cuda` `xoroshiro128p_normal_float64` (scalar seed
  2026100161 + 1000·case_index + run), exact-date one-factor stepping, plain knock-out
  payoff, 256-thread blocks, 8 blocks per SM. The same construction on 16 CPU processes
  (keys `[2026100161, case_index, 9, run, worker]`) gives the CPU anchor. Both are timed
  end to end at N(ε) as in section 0.3; throughput (paths per second) is also reported.
- The GPU factor g is reported as measured, next to the historical grid g ∈ {1, 10, 100}.

## Item C7. Missing arms (disclosed robustness checks)

- Cases (case_index): 16×52 H = 140 (2); 4×12 H = 120 (3); 4×12 H = 160 (4); 8×52 H = 120
  (5); 8×52 H = 160 (6); 16×52 H = 120 (7); 16×52 H = 160 (8).
- Each case: σ_Q (section 0.4); item C1 `preint` and `rqmc`, canonical factor, 32
  scrambles to 2^19; 3 warm item C2 repeats of `preint` to 2^19. For 16×52, truncation to
  2^18 is decided once, before any fit, from the first completed 16×52 H = 140 scramble:
  truncate all three 16×52 cases if 8 × (its time to 2^16) > 10 minutes. Then window [10, 18].
- T_C: the item C2 all-16 warm model, preint CPU only (labelled QF, since other comparators
  are not run for these cases); the per-scramble-median model is a sensitivity.
- **Oracle depth.** (a) The unchanged stop rule (STOP if D_min > 10·D_max($0.001) at
  100 ns, k = 3) uses the historical favourable Box–Muller leaf-table score
  (`barrier_oracle_depth`, extended only to accept the case's parameters). This is labelled
  as the QF lower end: 0.26–0.27 of the compiled forward dependency depth on the
  development sources. (b) Each case is also compiled with the Stage A pipeline (no basis
  replay; budget 2 CPU-hours per case, otherwise reported as not done), reporting the
  clean dependency-only (2 × forward) and clean scheduled depths.
- If any case fails STOP under depth (a), it is named in the limitations and in claim C4,
  and the plan's re-plan trigger applies. The same trigger applies to the development
  cases if any has oracle/D_max ≤ 10 at the decision point under depth (a).

## Item C8. Out-of-sample check (24 generated cases)

- Generator (DECISION §6): s = 0…5 over strata (na, nt) = (4,12), (4,52), (8,12), (8,52),
  (16,12), (16,52); j = 0…3; K/S0 = (0.9, 1.0, 1.1)[(s+j) mod 3]; for each (s, j),
  `rng = Generator(PCG64(SeedSequence([2026092301, s, j])))`, then
  H = 100·rng.uniform(1.15, 1.6), σ = rng.uniform(0.15, 0.45), ρ = rng.uniform(0.1, 0.7);
  T = 1 + (j mod 2); r = 0.03; S0 = 100. The runner generates the cases after this file is
  committed; they are not inspected before the run. Development cases never enter.
- Each case: σ_Q; item C1 `preint`, canonical factor, 32 scrambles to 2^17, window [10, 17]
  (sensitivity [8, 17], [12, 17]); 1 warm timing repeat to 2^17, fitted on marks
  2^13…2^17; T_C = the all-16 warm model (QF; preint CPU only); the item C7 oracle-depth
  rules (a) and (b); the unchanged stop rule.
- Report the distribution of oracle/D_max at the decision point under depth (a), with
  depth (b) beside it, and the counts at oracle/D_max ≤ 1, ≤ 10/3 and ≤ 10 under depth (a)
  (DECISION §6's 10× and 3× speed-ups correspond to ≤ 1 and ≤ 10/3). Any case ≤ 10 under
  depth (a) is named in the limitations and claim C4, and the re-plan trigger applies.
- Deviation, stated now: DECISION §6 designed this set for confirmation, with 64 scrambles
  and two reference constructions. Here it is an out-of-sample robustness check with 32
  scrambles and no per-case reference.

## Q4. Payoff validation (financial law)

- **IR evaluated:** `results/frontier_completion_20260927/stage_a/<case>/target.json`
  for B4x12 and B8x52, SHA-256 checked against `artifact_hashes.json` before use, via
  `ir.evaluate` (q = 32, f = 40), decoded to dollars. Draws are split over 16 processes.
- **Independent float64 NumPy reference** (written without importing the IR builder)
  using the IR's input law. Uniforms are u_i = (raw_i + ½)/2^32. Normals come in pairs
  (2j, 2j+1) as r·cos 2πv, r·sin 2πv with r = √(−2 ln u). Per date j, normal j(na+1) is the
  common factor (σ√(ρΔt)) and normal j(na+1)+1+i the idiosyncratic factor of asset i
  (σ√((1−ρ)Δt)). Drift (r − σ²/2)Δt. No spot clip; clip events are counted separately.
- **Draws** (at least 10⁴ per case): 5,000 iid; 5,000 rejection-sampled so that the
  maximum date basket is within 1% of H; edge draws (knocked out, A < K, spot-guard clip,
  all-zero and all-maximum raw inputs, and raw inputs at the Box–Muller extremes). Keys
  `[2026100191, case_index, 6, d, 0]` with d = 0 iid, 1 near-barrier, 2 edge.
- **Recorded:** the maximum absolute error on draws with no barrier or strike flip; counts
  of barrier misclassifications and A < K flips; δ_fp = the maximum
  |max_j basket_j (IR) − max_j basket_j (float)| over all draws, taken at the IR node that
  feeds the barrier comparison (`lt(·, H)`), located with `ir.evaluate(trace=True)`.
  Labelled empirical, not certified.
- **Error total.**
  - *Law error:* |price with continuous uniforms − price with q = 32 midpoint uniforms and
    the clip|, over 10⁷ common-random-number float64 paths (keys
    `[2026100191, case_index, 8, 0, worker]`); upper 99% bound of the absolute value,
    |mean| + z_{.995}·SE.
  - *Flip bound:* e^{−rT}(H − K + δ) × the one-sided 99% Clopper–Pearson upper limit of
    P(|max_j basket_j − H| ≤ δ) with δ = 10·δ_fp, from 10⁷ iid float64 paths (keys
    `[2026100191, case_index, 8, 1, worker]`). No analytic fixed-point bound is used. The
    plug-in estimate is reported beside it.
  - *Arithmetic:* the maximum unflipped absolute error.
  - Total = law + flip + arithmetic. Pass if total ≤ ε/10 = $10⁻⁴. If total > ε/10, the
    quantum statistical share becomes e_Q = 0.45ε − (total − ε/10), floored at 0, and the
    resulting Q and D_max are primary. The unreduced values become a QF sensitivity.

## Decision-point table (claim C4)

For 4×12, 8×52 and the item C7 cases: oracle/D_max at $0.001, 100 ns, k = 3, σ_Q, and the
section 0.3 comparator (for item C7 rows, the preint-CPU T_C, labelled QF), for three
oracle depths:

- the favourable leaf-table score (QF);
- the clean dependency-only compiled depth (**headline**);
- the clean scheduled depth.

Sensitivity rows:

- the QF and CF bases;
- fresh-cached T_C (QF);
- preint-CPU-only T_C (QF);
- e_C = 0.9ε (CF);
- the unreduced Q4 share, if Q4 reduced it (QF).

All D_max values use the archived k ∈ {1, 3, 10} grid and t_layer ∈ {10 ns, 100 ns, 1 µs,
10 µs} as sensitivity.

## Schedule, exclusivity and cuts (fixed now)

- **Exclusivity.** Timing-bearing runs (item C2, item C5 timing, item C6, the anchors, and
  the timing repeats inside items C7 and C8) start only when no compute job of any session
  is running: the 30 s average of `\Processor(_Total)\% Processor Time` is below 10%,
  and no other python process uses CPU. Both are recorded. Ref B runs alone in its own
  slot, so its wall-clock budget buys a fixed amount of work. Ref A, item C4 and the item
  C1 bases and rotations run in other non-timing slots.
- **Order** (Day 1 = the date of the commit that freezes this file, IST):
  - Day 1: item C1 port check, item C1 (all bases), item C2. Night 1: Ref B alone.
  - Day 2: Ref A, item C4, item C5, item C7, Q4.
  - Day 3: item C8, then item C6.
- **Cuts**, by calendar only: an item not started by its deadline is cut and reported as
  not done. Deadlines: item C5, Day 3 00:00 IST; item C8, Day 4 00:00; item C6, Day 5
  00:00. A started item is completed and reported. Effects: C5 cut → claim C2 worded "for
  the two smoothers tried"; C8 cut → reported as not done; C6 cut → no GPU candidate and
  no GPU anchor; the CPU anchor stays; T_C/g for g ∈ {1, 10, 100} is reported as a
  sensitivity, and the text says "strongest measured CPU implementation".
- **Trims before any cut** (pre-declared): rotations for the knock-out payoff only.

## Outputs and gates

Each item writes a JSON summary as in section 0. The Stage C gate: every item above
executed as written, or cut under the rule above with the reason recorded. The text of
claims C2, C4 and C6 follows the outcomes of items C1–C8 and Q4. Claim C7 (hardware) is
outside Stage C. No item establishes or refutes quantum advantage on its own. The fixed
verdict is the current status, not a required outcome.

## Deviation log (appended after freezing; dated)

- **D1, 2 October 2026 (item C2, small-n rule).** For n(ε) < 2^13 the rule reads the warm
  all-16 elapsed time at the smallest prefix mark ≥ n(ε) inside the 2^19 timing runs. Marks
  are stamped only after a whole 2^12-point chunk is computed, so for n(ε) < 2^12 the value
  is the time for 2^12 points, not n(ε). Effect, as recorded: T_C at ε = $0.10 and $0.03
  is overstated (8×52 preint: 0.91 s, against 0.55 s measured at ε = $0.01). This is QF and
  does not touch the decision point ($0.001, measured confirmation). No re-run; the values
  are reported with this note, and the paper does not use them as measured times.
- **D2, 2 October 2026 (Q4, δ_fp).** The literal rule took δ_fp over all draws, including
  the 20 constructed spot-clip draws, where the IR clips log spots and the reference by
  design does not. δ_fp became 9.7×10³ (4×12) and 2.9×10⁶ (8×52), the flip band covered
  every path, and the bound failed for that reason alone. The literal result is kept and
  reported. A labelled post-hoc deviation (`q4_deviation.py`) recomputes δ_fp over draws
  without a clip event and redoes only the flip-band count, with the same draws and
  seeds. Clip events stay counted separately, as section Q4 states.
- **D3, 2 October 2026 (item C2, sensitivity conventions below 2^13).** Conventions (i)
  and (iii) are fitted on marks n ≥ 2^13 and give negative times when evaluated far below
  (4×12 preint: −0.015 s at ε = $0.10). Such values are not tabulated. Rows with
  n(ε) < 2^13 are flagged, and only the measured mark (with D1's caveat) is reported.
- **D4, 2 October 2026 (item C2, load-balanced convention).** Each (scramble, chunk) task
  builds a scrambled Sobol generator and fast-forwards it by chunk·2^12 points, a cost that
  grows with the chunk index (about 64× the points used, per scramble at 2^19). The
  measured load-balanced times include this overhead and exceed the all-16 times. So
  convention (iii) is not a valid classical-favourable bound. It is reported with this note
  and not re-run.
- **D5, 2 October 2026 (provenance).** Ref A, Ref B, Q4, the C5 rates, the D2
  recomputation, σ_Q and the interim decision table recorded the commit only, and C2 lacks
  the lock and factor hashes. All ran from clean detached worktrees of the recorded
  commits, so code and spec hashes follow from git. From the commit that adds this entry,
  runners write full provenance (`provenance.py`) and refuse a dirty checkout.
- **D6, 2 October 2026 (timing harness, before any C5, C7 or C8 timing run).** The C2
  harness hard-coded the C2 seed root, so C5, C7 and C8 timing would have reused C2's
  scrambles. It now takes each item's root (C2's default is unchanged). A timing run is
  refused, not started, when the machine is still busy after the wait. Idleness is
  re-checked before the fresh-cached, cold and load-balanced sub-runs. Core counts and the
  full python process list are recorded. The measurement path is unchanged. C2's executed
  run was idle at every check.
- **D7, 2 October 2026 (item C7 truncation).** The first implementation timed a separate
  solo probe. It was replaced, before item C7 ran, by the rule as written: the time to 2^16
  of the first completed scramble of the pooled 16×52 H = 140 run.
- **D8, 2 October 2026 (items C7/C8, depth (b) budget).** The budget is enforced as
  2 hours of wall-clock time in a child process. The compile is single-threaded, so wall
  time ≥ CPU time, which errs toward "not done".
- **D9, 2 October 2026 (fit windows).** The sensitivity window [14, M] is now produced for
  M = 18 too (C7 16×52 cases if truncated). This was fixed before item C7 ran; C1 used M = 19.
- **D10, 2 October 2026 (T_C uncertainty).** C1 archives n(ε) percentile intervals, not the
  joint (A, r) draws. T_C intervals are formed in the decision step by mapping the n(ε)
  interval ends through the all-16 model (monotone in n), and labelled model-based.
- **D11, 2 October 2026 (no effect on executed runs).** C1's port check now falls back to
  the archived price when Q0 records no mismatch. C4's chunk sizing uses n_top − count.
  Neither changes an executed result: the port check passed, and every C4 size is a power
  of two ≥ 2^12.
- **D12, 2 October 2026 (item C7 depth (b), re-run logged before it starts).** The first C7
  oracle run (`results/.../c7/oracle/`, from `9d734ff5`) reported depth (b) as not done for
  every case: `FileNotFoundError`. The compiler's `resolve_library` resolves a leaf library
  through its `results/` suffix against the checkout that runs the code, and it refuses `..`.
  The output directory was in the main checkout, not in the running worktree, so the path
  resolved to a location that did not exist. Depth (a) is unaffected. Re-run under the
  execution rule (a defect, logged first), from a fresh clean worktree, with the output
  inside that worktree, copied to `results/.../c7/oracle_d12/`. The failed run is kept.
