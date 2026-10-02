# Stage B results — 1 October 2026

**No defensible significant quantum advantage established yet.** Stage B executed plan
items T0 (pinned environment) and Q0 (provenance replay) as specified in
[ANALYSIS_SPEC_STAGE_B.md](ANALYSIS_SPEC_STAGE_B.md), committed as `d3a6950d` before any run.
**T0 passed. Q0 failed its exact-equality rule** on one case. The failure was then fully
attributed by separately labelled diagnostics, and it does not change the STOP decision.

## T0: pinned environment — passed

| Check | Outcome |
|---|---|
| Interpreter | CPython 3.12.4, fresh venv, no system site-packages |
| Install | 39 wheels with `--require-hashes --no-deps --no-index`, return code 0 |
| Installed set equals the lock | Yes, exactly |
| `pip check` | No broken requirements |
| Imports | numba 0.60.0, numpy 2.0.2, scipy 1.13.1, mpmath, matplotlib, pytest, Markdown, qiskit 1.4.6, numba.cuda |
| CUDA smoke kernel | Ran on the RTX 4060 Laptop GPU (compute capability 8.9); result equals numpy exactly |
| Recorded | Core Ultra 7 155H, Balanced power plan, driver 610.74, MiKTeX 25.12, latexmk 4.88 |

Receipt: `results/frontier_replay_20261001/t0_environment.json`.

## Q0: provenance replay — failed exact equality on one case

All six scripts ran from a detached checkout of `d3a6950d` in the T0 environment and
exited 0. Every exact-field count equals the 24 September count.

| Archived output | Exact fields | Mismatches |
|---|---:|---:|
| classical_exponent_pilot.json (P1) | 1,611 | 0 |
| barrier_oss_pilot.json (P2) | 108 | 0 |
| barrier_fast_classical.json (P3) | 57 | **13** |
| barrier_oracle_depth.json (Q1) | 209 | 0 |
| barrier_decision.json | 2,112 | **48** |
| frontier.json | 270 | 0 |
| **Total** | **4,367** | **61** |

All 61 mismatches belong to the 8×52 case. The 13 P3 fields are its price, standard error,
rate and the ten per-n standard deviations (`rqmc_std_one_scramble`). The 48 decision
fields are its `points_per_scramble` at ε = $0.01 and $0.001, derived from the P3 rate and
fit constant. The 4×12 case reproduced every field. The replayed decision is **STOP H1**,
as archived. Report: `results/frontier_replay_20261001/q0_provenance_replay.json`.

**Disclosed limitation of the comparison.** Q0 uses `timing_key` from
`research/advantage_frontier_20260923/provenance_replay_diff.py` unchanged, as the Stage B
spec requires. It treats any field whose path contains the substring `t_c` as timing. That
also covers 38 non-timing fields: every `fit_constant` (16 in P1, 4 in P2, 2 in P3) and
Q1's `forward_t_count` and `clean_call_t_count` (8 each). They were not exact-compared in
Q0 or in the 24 September replay, and the counts above exclude them, although the plan's
Q0 criterion names fit constants. One of them changed in Q0: the 8×52 P3 fit constant,
0.2957187660 (archive) against 0.3374739592 (replay). Counting it, 62 scientific fields
differ, all in the 8×52 case. Compared separately, the other 37 are equal in Q0, and all 38
are equal in the 24 September replay outputs (untracked, `.context/advantage_frontier_replay/`).

| 8×52 field | Archive | Q0 replay |
|---|---:|---:|
| Price | 3.2816161 | 3.2816194 |
| Standard error | 1.020×10⁻⁴ | 1.035×10⁻⁴ |
| RQMC rate r | 0.527 | 0.541 |

## Attribution (diagnostics, not a replacement for Q0)

The PCA factor L of the covariance `Σ_asset ⊗ Σ_time` is not uniquely defined in either
development case. In exact arithmetic every time mode has an (na−1)-fold eigenvalue:
twelve 3-fold groups for 4×12 and fifty-two 7-fold groups for 8×52
([ANALYSIS_SPEC_STAGE_C.md](ANALYSIS_SPEC_STAGE_C.md), section 0.1). Both the basis that
`numpy.linalg.eigh` returns inside these eigenspaces and the order in which `argsort` places
tied computed values depend on the LAPACK build, its thread count and the numpy version.
Even the number of exactly tied computed 8×52 eigenvalues depends on the build: 12 groups
in the numpy 1.26.4 multithreaded MKL decomposition, 11 (ten pairs and one triple) in the
T0 single-thread decomposition. The same code therefore yields different, equally valid
factors. The 4×12 case reproduced because both builds returned the same decomposition (the
saved numpy 1.26.4 eigenvectors equal the T0 ones bit for bit), not because its factor is
unique.

| Factor L used by P3 (8×52) | Rate r | Price | Std. error |
|---|---:|---:|---:|
| numpy 1.26.4, MKL, 1 thread (archive; P3 workers pin threads to 1) | 0.527 | 3.281616 | 1.02×10⁻⁴ |
| numpy 2.0.2, OpenBLAS, 1 thread (T0, Q0 replay) | 0.541 | 3.281619 | 1.03×10⁻⁴ |
| numpy 1.26.4 eigh (MKL, multithreaded) with numpy 2.0.2 argsort | 0.570 | 3.281712 | 0.82×10⁻⁴ |
| numpy 1.26.4, MKL, multithreaded | 0.572 | 3.281689 | 0.79×10⁻⁴ |

Diagnostics, in order (all in `results/frontier_replay_20261001/q0_attribution/`):

1. The Sobol points and normals are identical across environments. With an identical L,
   the per-point estimand and whole in-process scrambles are bit-identical across
   environments, so the estimator itself is numerically stable.
2. Within one environment the factor is deterministic across calls and processes. The
   unmodified pooled P3 run repeats exactly.
3. Diagnostics 1 and 2a injected numpy 1.26.4 factors that were, by mistake, computed
   with multithreaded MKL (the diagnostic scripts imported numpy before P3 pins the
   threads). They did not reproduce the archive, and are kept as a record.
4. **Diagnostic 2b** injected the factor exactly as P3's workers build it (numpy 1.26.4, MKL,
   one thread) into the unchanged P3 run in T0. It **reproduces every non-timing P3 field
   of the archive exactly**, for both cases.

The mismatch is therefore attributed entirely to the factor L. The three 41 MB
intermediate dumps stay untracked in `.context/frontier_q0_attribution_dumps/`. Their
factor hashes are in `attribution_summary.json`.

## What this changes

- **ERRATA E10.** The archived 8×52 rate is one draw from a basis-dependent family. Over
  the four factors run, r spans 0.527–0.572, and the archived value is the lowest. The
  classical cost depends on the fit constant A as well as r: `barrier_decision.py` uses
  n(ε) = max(2⁸, (2.947·A / (4·0.45·ε))^(1/r)) points per scramble. At the decision point
  (ε = $0.001) the archived factor needs the most points of the four (124,959 against
  99,731–116,485), so at a given per-point time it gives the largest classical cost and
  D_max and is the most quantum-favourable. At ε = $0.01 it needs the fewest (1,579.5
  against 1,655.2–1,809.9), and at $0.03 it ties with the Q0 replay at the 2⁸ floor, below
  both diagnostics. These orderings hold under the P3 protocol. Under item C1's protocol
  (prefixes to 2¹⁹, primary window [10, 19]) the archived factor gives r = 0.640, above the
  canonical basis (0.597) and all four rotations (0.601–0.626), so the ranking of bases
  depends on the protocol and fit window (`results/frontier_classical_20261001/c1/c1_summary.json`).
  Prices agree within one combined standard error: the largest difference, archive against
  diagnostic 1, is 9.6×10⁻⁵ against a combined standard error of 1.3×10⁻⁴. No archived
  value was changed.
- **The decision is unchanged.** In the replay, at ε = $0.001, 100 ns and k = 3, the
  scored Box–Muller oracle depth is 1,604× D_max (8×52) and 16,348× (4×12). The stop
  threshold is 10×. These ratios use re-measured timings on the same laptop, not the C2
  timing study, and the historical favourable leaf-table oracle score (ERRATA E3).
- **Claim C2 is unaffected in direction.** Every factor run through P3 gives r between
  0.527 and 0.572 for the preintegrated knock-out, far from n⁻¹. The paper reports the basis spread next to
  the rate. Stage C builds a closed-form canonical basis and adds seeded rotation
  sensitivity ([ANALYSIS_SPEC_STAGE_C.md](ANALYSIS_SPEC_STAGE_C.md), section 0).
- **Not a new observation.** Case, [arXiv:2502.17731](https://arxiv.org/abs/2502.17731) v2
  (16 September 2026), reports that bases within a degenerate PCA eigenspace can change
  the measured RQMC exponent. The paper cites it; E10 is a project correction, not a finding.

This closes T0 and records Q0's outcome. It does not establish advantage. Nor does it
replace author verification or named human-expert review.
