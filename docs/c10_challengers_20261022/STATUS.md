# C10 classical challenger wave (22 October 2026): status

> **Current numbers:** see [CURRENT_NUMBERS.md](../plan110_status_20261022/CURRENT_NUMBERS.md) (headline run006; window 26.1, all-free 1.30, symmetric 1.50, no single departure reaches M <= 1). Figures below may be from earlier runs.

This is register item C10, with F06 and F07. Its trigger fired after the frontier probe ("implement challengers (CPU)
only if a scenario reaches miss ≤ 3"; the all-free floor and the symmetric convention reached 0.51 and 0.28). This
is AI-assisted work and **not committed**, by instruction.

**Labels:** meas / mod / assm, with q+ / q− / 0. A faster valid classical method lowers T_C and raises M, so it is
**q−** for quantum.

**Code and outputs:** `research/c10_challengers_20261022/` and `results/c10_challengers_20261022/`.
- The Stage C harness (numpy, numba, scipy, T0 environment) runs as `-m` from the repo root.
- The pure-python screens run under `-I -S -B`.
- No Stage C file was edited.

## Result in one line

**Current numbers are in section 6** (after the R2 review); sections 1-5 are kept as run. The same Stage C `preint`
estimator with faster arithmetic is **2.08-2.25× faster** at the binding cell. Primary T_C is **10.84 s** (QF end; it
was 22.53 s). The cheapest distribution-free method is replicated RQMC, with factor **17.3** (iid: 33.8).

With every input measured, the best explicit M is **21.4**. **No single favourable departure reaches M ≤ 1** for any
explicit class: the closest is all-free at 1.06, then symmetric at 1.23. Two departures still do.

Killed:
- control variates under RQMC;
- two-direction smoothing (narrow margin);
- rare-event importance sampling (F07);
- barrier-date switching isolation (F06).

## 1. Faster arithmetic for the same estimator (kept)

**What changes.** Only the arithmetic: `fast_kernels.knockout_preint_fast` plus `fast_pipeline.ndtri_as241`.
- **Closed-form barrier roots.** The first canonical PCA column is u₀ ⊗ v₁, with u₀ constant across assets, so the
  loading is constant within each date. The 52 barrier roots are therefore closed form; Stage C used 8 Newton steps
  per date.
- **Cheaper strike root.** The strike root is a Newton solve over 52 date sums instead of 416 coordinates.
- **Fewer CDFs.** The closed-form integral needs 2·52 + 2 normal CDFs instead of 2·416 + 2.
- **Faster inverse normal.** Wichura's AS241 replaces scipy's `ndtri`.
- **Unchanged:** the factor, the GEMM, the Sobol points and the estimand.

**Equivalence** (meas):
- Per point against the Stage C kernel on 4,096 Sobol points: maximum relative difference 6e-13 (B8x52) and 4e-13
  (B4x12) (`selfcheck/run001.json`).
- AS241 against scipy: 1e-15 relative.
- Paired 16-scramble means agree to about 1e-14 in all 80 paired runs.
- So the challenger inherits Stage C's validation against the C4 reference.

**Profile per 2¹² chunk, B8x52, one process** (meas):

| Step | Stage C | Fast |
|---|---:|---:|
| Sobol | 3.7 ms | 3.7 ms |
| Inverse normal | 40 ms (scipy) | 14 ms (AS241) |
| GEMM | 33 ms | 33 ms |
| Kernel | 90 ms | 15.5 ms |

A Kronecker-factored GEMM was tried and dropped: it was slower than BLAS.

**Paired timing** (`timing/run001/c10_timing.json`; meas). The protocol is item C2 measured confirmation:
- 16 workers, 16 scrambles, all-16 wall time, warm workers;
- the factor built inside the timed interval;
- item C2's recorded n_run, its own seed root 2026102201, and 20 replications;
- the three methods share each replication's seeds and rotate their order;
- the machine was idle before every cell (CPU 8-9%, no busy python).

| Cell | n_run | Stage C `preint` | Fast kernel only | Fast kernel + AS241 | Speedup |
|---|---:|---:|---:|---:|---:|
| **B8x52 $0.001** | 2¹⁷ | 11.09 s | 6.10 s | **4.94 s** | **2.25×** |
| B4x12 $0.001 | 2¹⁷ | 1.156 s | 0.600 s | 0.451 s | 2.57× |
| B8x52 $0.01 | 2¹¹ | 0.235 s | 0.159 s | 0.130 s | 1.81× |
| B4x12 $0.01 | 2¹² | 0.0454 s | 0.0282 s | 0.0213 s | 2.14× |

The figures are medians. The half-widths and the fractions within 0.45ε are identical across methods, because the
points are identical.

**Machine state (important).** The unchanged Stage C harness (`c2_timing.all16`) re-timed today at the binding cell
gives **10.26 s** (`c2_harness_today/run001.json`), against 22.53 s on 1 October and 23.46 s in the H16 rerun.
- The power plan is the same (Balanced, AC).
- The Windows power-mode overlay today is **Best performance**. Item C2 recorded only the plan, not the overlay, so
  the 1 October overlay is unknown. It is most likely the default.
- Under the Stage C spec, a higher-performance setting is a labelled **CF sensitivity**. Today's absolute times are
  therefore CF, and I did not change the setting.
- **Primary T_C** is the 1 October primary divided by the paired speedup (meas ratio × meas time; it assumes the ratio
  is state-invariant, assm):

| Cell | Stage C T_C | Primary T_C (fast) | CF sensitivity: today's absolute time |
|---|---:|---:|---:|
| B8x52 $0.001 | 22.529 s | **10.03 s** | 4.94 s |
| B4x12 $0.001 | 2.688 s | 1.047 s | 0.451 s |
| B8x52 $0.01 | 0.5535 s | 0.306 s | 0.130 s |
| B4x12 $0.01 | 0.1244 s | 0.0583 s | 0.0213 s |

## 2. Challengers killed (all meas)

**Control variates on top of preintegration** (`cv_screen`, `rate_cv`).
- The controls are the preintegrated geometric Asian call, the linear average and the geometric-average knock-out;
  all have closed-form means.
- iid (4,096 paths): σ_h/σ_res = 1.81 (B8x52) and 1.71 (B4x12); 1.90 jointly.
- **Under RQMC** (32 paired scrambles to 2¹⁸): the sd ratio is **1.00 at every n from 2⁶ to 2¹⁸**. RQMC already
  integrates the smooth controls almost exactly (their RQMC se is about 2e-7). The remaining error is the knock-out
  structure, which the controls do not touch.
- **Killed.** The fitted rates are preint r = 0.600 (B8x52) and 0.629 (B4x12); n(0.001) is about 85.8k and 85.2k, so
  n_run 2¹⁷, the same as C2.

**Two-direction smoothing** (`rate_smooth2`; Stage C "not executed": multi-direction smoothing). The first direction
is integrated in closed form and canonical direction k by Q-node Gauss-Hermite.
- **k = 1** (asset dispersion): error ratio 1.00-1.03 at 6.6-13× the kernel cost.
- **k = 8** (second common time mode, B8x52): error ratio 1.93-2.03 at 6.6-13× the cost. Equal accuracy then takes
  6.64 × 1.93^(−1/0.6) ≈ **2.2× longer** than plain preint.
- **Q = 6 is biased** by −0.0017 (1.7ε); Q = 12 agrees with h.
- **Killed.**

**F07, rare-event / importance-sampling proposals** (`f06_f07/run001.json`, 2¹⁸ iid paths). P(knock-out) is 0.097 and
P(f > 0) is 0.425; the top 1% of payoffs carry 6.6% of the price (B8x52; B4x12 is similar). The price is not
rare-event dominated, so there is no region for importance sampling to concentrate on. **Closed as screened.**

**F06, active barrier-date switching surface** (same run). The binding date is spread over the late dates: the top 3
dates carry 30% for B8x52 and 65% for B4x12. The two smallest roots are within 0.05 in 44% (B8x52) and 20% (B4x12)
of paths. The switching surface is dense, not isolatable, and it is what holds the preint RQMC rate near 0.6.
**Closed as screened.**

**Not run, with reasons:**
- **Preint combined with bridge-ordered OSS.** OSS-BB is 920 s at the binding cell (C5 model), about 40× slower than
  preint, so the combination cannot beat preint.
- **Xie-He-Wang IS smoothing.** Its premise is a rare barrier region, which F07 rules out.

## 3. Effect on M

`research/frontier_probe_20261021/headline_m_probe.py run003 <c10_timing.json>` writes
`results/frontier_probe_20261021/headline/run003/` (mod). The measured cells' T_C is divided by the paired speedup;
everything else is unchanged. Binding cell (still B8x52, $0.001):

| Class | Primary | All-free | 1 lane vs 1 core | Symmetric (Stage C) | e = ε |
|---|---:|---:|---:|---:|---:|
| Certified today | 1,800 | 89.4 | 175.9 | 48.8 | 900 |
| Canonical explicit | 521.0 | 25.9 | 50.9 | 14.1 | 234 |
| **Window certified, δ = 0.003** | **23.1** | **1.15** | 2.26 | **0.63** | 10.4 |
| Window certified, δ = 0.01 | 19.4 | 0.96 | 1.90 | 0.53 | 8.7 |
| Window, no U1/U2 | 68.0 | 3.38 | 6.65 | 1.84 | 30.6 |

- **Minimal departures for the window class:** still one, but only the symmetric convention (0.63) suffices. The
  all-free floor now misses (1.15).
- **The symmetric column assumes** the iid per-point cost speeds up by the same factor as the RQMC run (assm; the
  kernel dominates both).
- **P3** (`p3/run003`). M ≤ 1 at the primary conventions now needs D_eff ≤ **99 layers**. No existing modelled
  design reaches it: best loader + free exponential gives 2.17, and the all-free floor 1.15.
- **Under today's CF machine state** (T_C 4.94 s): window M ≈ 47 (mod, CF sensitivity).

## 4. Hashes

| File | sha256 |
|---|---|
| research/c10_challengers_20261022/fast_kernels.py | 0b07f081…61fe (the smoothing kernel was appended after the timing run; the timing run records the hash it used) |
| research/c10_challengers_20261022/fast_pipeline.py | 58d46384…63db |
| research/c10_challengers_20261022/run_timing.py | 151e7ebf…bfe2 |
| research/c10_challengers_20261022/rate_cv.py | ead7138f…818c |
| research/c10_challengers_20261022/rate_smooth2.py | 21793c60…ef28 |
| research/c10_challengers_20261022/f06_f07_screen.py | 1a4311a9…20ea |
| results/c10_challengers_20261022/timing/run001/c10_timing.json | 11365822…1b85 |
| results/c10_challengers_20261022/c2_harness_today/run001.json | c734c7cf…5818 |
| results/c10_challengers_20261022/rate_cv/run001/rate_cv.json | 697f68ec…c329 |
| results/c10_challengers_20261022/rate_smooth2/run001/rate_smooth2.json | c58990cf…3d52 |
| results/c10_challengers_20261022/f06_f07/run001.json | a235a673…557e |
| results/frontier_probe_20261021/headline/run003/headline_table.json | de4a0f50… |
| results/frontier_probe_20261021/p3/run003/p3_desk.json | d35e32b8… |

## 5. C09 and H16 measured; M with every measured input (run004)

**C09: a timed, successful, distribution-free 99% price** (`c09_g4.py`; `results/c10_challengers_20261022/c09/*`;
meas).
- **Estimator:** iid preintegrated samples with the fast kernel, and the two-sided empirical-Bernstein bound (Maurer &
  Pontil, Thm 4) at δ = 0.01.
- **Range:** R = 17.30, from the frontier probe's analytic bound sup h ≤ 17.29 (mod; N1 assumed $40).
- **n:** fixed from an independent 2^16-point pilot with a 2% margin. The wall time includes the pilot.
- **Factor:** a same-state ratio against 6 practice-RQMC runs (preint_fast, item C2 n_run) taken before and after.

| Cell | n | EB bound | Target 0.45ε | Distribution-free wall (today) | Practice (today) | **Factor** | N1 modelled |
|---|---:|---:|---:|---:|---:|---:|---:|
| B8x52 $0.001 | 8.04e7 | 4.455e-4 | 4.5e-4 | 168.4 s | 4.99 s | **33.8** | 36.9 |
| B4x12 $0.001 | 9.54e7 | 4.448e-4 | 4.5e-4 | 17.8 s | 0.472 s | **37.6** | 40.3 |
| B8x52 $0.01 | 9.0e5 | 4.46e-3 | 4.5e-3 | 2.25 s | 0.140 s | **16.1** | 18.9 |
| B4x12 $0.01 | 1.05e6 | 4.45e-3 | 4.5e-3 | 0.24 s | 0.023 s | **10.3** | 10.6 |

All four runs succeeded, and every sample stayed inside [0, R].

**H16 with the fast method** (`h16_fast/run001`; meas, same-state ratio). The 1-worker / 16-worker ratio is 9.62
(B8x52 $0.001), 9.89, 8.86 and 11.03. The Stage C method, re-measured in the same state, gives 11.51, 10.69, 7.92 and
10.81; the H16 run001 values were 10.24, 9.36, 7.38 and 6.44.

**Headline run004** (`headline_m_probe.py run004 results/c10_challengers_20261022/overrides_run004.json`). The inputs
are:
- C10 T_C: 1 October primary ÷ paired speedup;
- the H16 ratio with the fast method;
- the C09 measured factors.

Binding cell B8x52 $0.001 in every row (mod, from meas inputs):

| Class | Primary | All-free | 1 lane vs 1 core | **Symmetric (C09 measured)** | All-free + symmetric |
|---|---:|---:|---:|---:|---:|
| Certified today | 1,800 | 89.4 | 187.1 | 53.3 | 2.65 |
| Canonical explicit | 521.0 | 25.9 | 54.2 | 15.4 | 0.77 |
| **Window certified (U1 + U2 + direction-select), δ = 0.003** | **23.1** | 1.15 | 2.40 | **0.684** | 0.034 |
| Window certified, δ = 0.01 | 19.4 | 0.96 | 2.02 | 0.574 | 0.029 |
| Window, U2 only (no orientation price) | 41.3 | 2.05 | 4.29 | **1.22** | n/a |
| Window, U1 only | 30.2 | 1.50 | 3.14 | 0.894 | n/a |
| Window, no U1/U2 | 68.0 | 3.38 | 7.07 | 2.01 | 0.10 |
| Window, without direction-select | 46.2 | 2.29 | 4.80 | 1.37 | 0.068 |

The U2-only and U1-only rows are from `derived/run002`; the rest are from `headline/run004`.

**Reading.** At the primary conventions, the best explicit margin is now **23×**.
- **Only one single departure still reaches M ≤ 1:** the symmetric distribution-free convention (0.68).
- **That departure needs the U1 credit.** U1 rests on an uncertified classical orientation price, which a symmetric
  comparison should not lean on (v3 §4.3). **Superseded later on 22 Oct:** a two-stage window estimator earns the mean
  bound quantumly (`p2/run003_self_mean`, k 9.058), so the symmetric value with no classical input is **0.707**
  (`derived/run003_self_mean`). The text that follows is the pre-supersession reading: without U1, the symmetric
  value is **1.22** (δ = 0.003) or 1.03
  (δ = 0.01).
- **Other single departures miss:** the all-free floor (1.15), loader + free exponential (2.17), and 1 lane vs 1 core
  (2.40).
- **Two departures reach M ≤ 1 for the window class:** all-free + symmetric (0.034), or all-free + failure 0.01
  (0.963, one cell).
- **P3** (`p3/run004`): D_eff ≤ 99 layers is needed at the primary conventions.

## 6. After the R2 review: current numbers (run005)

**Review** (`results/c10_challengers_20261022/review/c10_review.jsonl`, an independent AI agent).

**Passes:**
- the fast kernel is exactly the Stage C estimand (|Δ| ≤ 9.5e-13 on fresh and extreme points; 387-point
  quadrature);
- AS241 (1.2e-15 relative over 6.3M points, tails included);
- the CV negative (an RQMC-optimal β does not help either);
- run004's arithmetic.

**Two major findings, both adopted:**
- **(3) Speedup transfer.** Today's other same-state measurements give a Stage C / fast speedup of 2.08, not 2.25.
  The spec's QF rule applies, so primary T_C at B8x52 $0.001 is **10.84 s**. T_C is reported as a range, 10.0-10.8 s.
  The overlay explanation for the 2.2× machine difference is unverified.
- **(4b) The symmetric factor must be a minimum over distribution-free methods.** It is now measured, not modelled:
  C09b (`c09b_rep.py`) does replicated RQMC (m = 16-point digitally-shifted Sobol nets, empirical Bernstein on the
  replicate means, R = 17.30).

| Cell | C09 iid factor | **C09b replicated-RQMC factor** | Used (minimum) |
|---|---:|---:|---:|
| B8x52 $0.001 | 33.8 | **17.3** (2.96e7 points, bound 4.48e-4) | 17.3 |
| B4x12 $0.001 | 37.6 | **17.9** | 17.9 |
| B8x52 $0.01 | 16.1 | 83.5 (pilot-dominated) | 16.1 |
| B4x12 $0.01 | 10.3 | 49.3 (pilot-dominated) | 10.3 |

**Minor findings:**
- **Smoothing kill:** the margin is narrower, about 1.3-1.5× at the Q ≥ 16 needed for bias ≤ 0.1ε, and Q = 12 has
  a bias of +2.7e-4. Text corrected here; the kill stands for this kernel.
- **Envelope order:** fixed, by applying the speedup before the envelope (`apply_before_envelope`).
- **H16:** the QF maximum of the same-day ratio (9.62) and the ratio-transfer value (8.56) is used.
- **C09's B8x52 run** started at 14.7% CPU, against the < 10% idle rule. Noted.
- **Relative-difference statement:** the per-point agreement should be quoted as absolute, 1e-12.

**Headline run005** (`headline_m_probe.py run005 results/c10_challengers_20261022/overrides_run005.json`). Binding
cell B8x52 $0.001 in every row (mod, from meas inputs with QF choices):

| Class | Primary | All-free | 1 lane vs 1 core | **Symmetric (min over methods)** | All-free + symmetric |
|---|---:|---:|---:|---:|---:|
| Certified today | 1,666 | 82.7 | 173.1 | 96.0 | 4.77 |
| Canonical explicit | 482.1 | 23.9 | 50.1 | 27.8 | 1.38 |
| **Window certified (U1 + U2 + direction-select), δ = 0.003** | **21.4** | **1.06** | 2.22 | **1.23** | 0.061 |
| Window certified, δ = 0.01 | 18.0 | 0.89 | 1.87 | 1.04 | 0.051 |
| Window, quantum-only mean (U2 + direction-select) | 22.1 | 1.10 | 2.30 | 1.27 | 0.063 |
| Window, no U1/U2 | 62.9 | 3.13 | 6.54 | 3.63 | 0.18 |

**Reading (current).**
- **No single departure reaches M ≤ 1 for any explicit class** at δ = 0.003. The closest is the window class under
  the all-free oracle, at 1.06.
- **Minimal departures:** window class 2 (for example all-free + symmetric 0.061, or all-free + failure 0.01); canonical
  explicit 3; certified today 3.
- **The NO-GO is robust to any one favourable departure,** with a 21× margin at the primary conventions.

**Hashes for this section:**

| File | sha256 |
|---|---|
| research/c10_challengers_20261022/c09b_rep.py | 7f331ef9…4a94 |
| research/c10_challengers_20261022/build_overrides_run005.py | 0f06e433…ee43 |
| results/c10_challengers_20261022/overrides_run005.json | a3950d14…db2e |
| results/c10_challengers_20261022/c09b/B8x52_0.001_run001/c09b_rep.json | 39ac9d7a…afc9 |
| results/frontier_probe_20261021/headline/run005/headline_table.json | 3fd60a19…affa |
| results/frontier_probe_20261021/derived/run004_self_mean_run005/derived_selfmean.json | 92778957…731d |
| results/c10_challengers_20261022/review/c10_review.jsonl | a0f0c490…8a2c |

**Third review (r3, `results/frontier_probe_20261021/review/r3_review.jsonl`): no critical or major finding.**
Minor points, recorded here rather than by editing run scripts (their hashes are recorded):
- **(B) Pilot search in the C09b wall time.** It is about 8.6% of points and is **QF**, not "conservative for the
  classical side" as the c09b docstring says. Without the pilots the factor would be about 15.9 and window symmetric
  M about 1.35.
- **(B) Thin success margin.** The 2% n-margin gave only 0.34% slack on the bound. A miss would need a rerun. That
  caveat is q−.
- **(C) The minimum factor over methods is CF**, not QF. That is correct under spec section 0.3, as for T_C.
- **(C) Label and provenance defects.**
  - In run005 the `T_C_stageC` field holds the sped-up value.
  - run005's meta does not record the overrides file. Its provenance is
    `results/c10_challengers_20261022/overrides_run005.json` (sha a3950d14…db2e).
- **Reproduced.** All binding-cell numbers reproduce exactly, and the self-mean variant equals run005 × 1.0338.

**Float32 GEMM (run006).**
- **Admission.** `f32_check.py` (`f32/run001.json`) passes the spec's ε/10 check: mean shift about 1e-9 and largest
  per-point difference 1e-5, against 1e-4.
- **Paired timing.** `run_timing_f32.py` (`timing_f32/run001`; 10 replications) gives Stage C / fast / fast + float32
  of 11.22 / 5.01 / **4.11 s** at B8x52 $0.001, so float32 is 1.22× over fast. At B4x12 $0.001 it is 1.17 / 0.442 /
  0.451 s, no gain.
- **Machine state.** The B8x52 cell began at 14% CPU, above the < 10% idle rule. Noted.
- **Headline run006.** T_C = 22.53 / (2.078 × 1.220) = **8.89 s** (`overrides_run006.json`). Window M is **26.1**,
  all-free 1.30, symmetric 1.50, 1 lane 2.71. The symmetric factor and the one-core ratio are taken from the
  non-float32 fast method (assm). See CURRENT_NUMBERS.md.

**Untried challengers: desk dispositions** (mod; none of these was run).
- **GPU (Stage C item C6).** The laptop has no CUDA device, and the T0 environment has no GPU stack. A GPU comparator
  could only lower T_C further, which raises M (q−). It stays open as "untested", and the claim's label "strongest
  tested" covers it.
- **PDE / finite differences / sparse grids.** The contract is an 8-asset basket with 52 monitoring dates. A grid
  method works in 8 spatial dimensions, plus the running knock-out state. A tensor grid with even 30 points per
  dimension needs 30⁸ ≈ 6.6e11 nodes per date, and a sparse grid loses its rate on the barrier kink. Not competitive
  with 3e6 RQMC points. Register F24 already logs this.
- **MLMC / MIMC / MLQMC.** Each path is simulated exactly at the 52 contract dates, so there is no time-discretization
  bias for levels to correct. Levels over monitoring dates would change the contract. F10/F11 found that free
  corrections cannot beat tenfold even where levels exist. Not applicable.
- **Surrogates / learned control variates.** A surrogate needs training, and its mean must be certified or estimated.
  The CV screen above shows that under RQMC even closed-form smooth controls give a ratio of 1.00, because the
  residual error is the knock-out structure. A learned smooth surrogate would face the same limit. Expected gain is
  about 1. Not run.

C10 is therefore complete for applicable challengers. Adopted: the fast preint and float32 GEMM. Killed: CV,
two-direction smoothing, F06, F07. GPU is untested, with a q− direction.

## 7. Open points

- **Run 20 replications under the 1 October overlay.** That would remove the state-invariance assumption. It needs
  the user to set the power mode; I did not change system settings.
- **The H16 ratio and the C09 factor are done** (section 5).
- **Hashes for section 5:**

| File | sha256 |
|---|---|
| research/c10_challengers_20261022/c09_g4.py | 001f0ec7…d1c5 |
| research/c10_challengers_20261022/h16_fast.py | b56a8b8f…2acd |
| research/c10_challengers_20261022/build_overrides.py | 42cb76ab…0125 |
| results/c10_challengers_20261022/overrides_run004.json | 35d5bb46…c1ff |
| results/c10_challengers_20261022/h16_fast/run001/h16_fast.json | dbbfd442…99d1 |
| results/c10_challengers_20261022/c09/B8x52_0.001_run001/c09_g4.json | 8ce019bf…5552 |
| results/frontier_probe_20261021/headline/run004/headline_table.json | d2f1add7…9446 |
| results/frontier_probe_20261021/derived/run002/derived.json | 9028d3c0…11ee |
| results/frontier_probe_20261021/p3/run004/p3_desk.json | 66ff8af2…75e6 |
