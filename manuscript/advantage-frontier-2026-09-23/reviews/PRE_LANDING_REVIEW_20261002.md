# Pre-landing review of PR #13 — raw findings (2 October 2026)

Five read-only reviewer subagents ran on the branch at `f03166eb`. This file keeps the three
that reviewed the branch (maintainability, spec conformance, claims against evidence),
verbatim apart from formatting. The two reviews of the author's separate, uncommitted
limitation-program work are deliberately not published. Dispositions are in the PR #13
description and the Stage C deviation log (D1–D12). This is internal agent review, not peer review.

## Reviewer: maintainability (14 findings)

**Overall.** I reviewed all Python in the requested paths, code and docs only, against the maintainability checklist, plus ruff and import checks. The core numerics are tidy, ruff-clean, and well tested against the P1/P2/P3 originals: basis.py, kernels.py, oss.py, fit.py and scrambles.py.

The main risks are about running the tests and replaying the archived runs:
- **New tests never run in the health check.** The eight test modules sit outside pytest testpaths, and the health venv has no numba. They pass or fail only if someone runs them by hand in the T0 env, and no doc says how.
- **Q0 attribution scripts can't be rerun from a clean clone.** Some read untracked dumps from the wrong directory, and one archived input (order_8x52) has no script that produced it.
- **Provenance recording has drifted.** Only C1 and C2 record the dirty flag and the code/spec hashes. The c7/c8 oracle phase imports primitives.py, which the user has modified, but records only the HEAD commit.

Smaller items:
- **Dead code and stale docstrings:** timed_chunk's `sub`, summarize.py's overwritten key, the uncalled c4 `score` and the missing `run`, the kernels.py docstring, the c7_c8 usage line without `--rates`, and the garbled 2b docstring that is archived into JSON.
- **One prefix loop copied five times** and already diverging.
- **Port-check fragility:** C1's port check fails with a KeyError if Q0 matches.
- **23 new ruff errors** in q0_attribution, on top of a repo lint that was already failing (4713 errors).

No hard-coded absolute paths or mutable default arguments were found. The per-worker caches (_FACTORS, _RUN_FACTOR, _L) are intentional and keyed correctly.

### [P2] pyproject.toml:18 (test-coverage; confidence 9)

The eight new test modules are never collected by the health-stack pytest. That covers research/frontier_classical_20261001/test_*.py (basis, kernels, oss, fit, scrambles, timing, refb) and research/frontier_replay_20261001/test_q0.py. They sit outside testpaths, and the health venv cannot import them anyway: venv/Scripts/python.exe has no numba (verified: ModuleNotFoundError), while the T0 env has numba 0.60.0. No doc in the repo gives the command that runs them, so a 'full health check' passes without running any of the port and bit-exactness guards the archived runs depend on.

> testpaths = ["tests", "research/paper_a/tests", "research/journal_sprint/tests"]

**Fix proposed:** Document the command (for example `.context/frontier_t0_env/Scripts/python.exe -m pytest research/frontier_classical_20261001 research/frontier_replay_20261001`) in the Stage C results or PR. Alternatively, add these dirs to testpaths behind `pytest.importorskip("numba")` so they skip visibly instead of silently.

### [P2] results/frontier_replay_20261001/q0_attribution/attribution_diagnostic_L.py:19 (replayability; confidence 9)

Several committed attribution scripts cannot run from a clean clone. attribution_diagnostic_L.py:19 and scramble_inprocess.py:9 (`L0 = np.load(HERE / "dump_conda_1264.npz")["L"]; _s = p3.setup`) load a dump from HERE, but that file is not tracked there. It exists only in the untracked `.context/frontier_q0_attribution_dumps/`. summarize.py:16 (`DUMPS = ROOT / ".context" / "frontier_q0_attribution_dumps"   # 41 MB each; kept untracked`) hard-depends on those untracked files. summarize.py:34 (`order_1264 = np.load(HERE / "order_8x52_numpy1.26.4.npy")`) loads a tracked artifact that no committed script produces. So attribution_summary.json cannot be regenerated, and its argsort-difference field has no recorded provenance.

> L_1264 = np.load(HERE / "dump_conda_1264.npz")["L"]

**Fix proposed:** Point the two scripts at DUMPS, or note in each docstring that the dump is untracked. Make summarize.py skip the dump-hash entries (and say so) when DUMPS is absent. Add the code that wrote order_8x52_numpy1.26.4.npy, for example as a `save` branch in attribution_diagnostic.py.

### [P2] research/frontier_classical_20261001/c7_c8_cases.py:151 (maintainability; confidence 7)

The run-provenance boilerplate is copy-pasted into every runner and has drifted. c1_rates.py:109-118 and c2_timing.py:209-220 record commit, `dirty`, spec_sha256, lock_sha256, code_sha256 and the numpy version, and each defines its own identical `sha()`. c3_refa.py:53, c3_refb.py:106, c4_coverage.py:105 and q4_payoff.py:219 record only `git rev-parse HEAD`. c5_smoothers.py:99-101 and c7_c8_cases.py:151-152 write just commit.txt. The c7/c8 `oracle` phase imports research.controlled_source_completion.compiler, which imports primitives.py, and primitives.py currently has uncommitted edits in the shared tree. A run from that tree would record a HEAD commit for code that differs from it, with nothing marking it dirty.

> (out_dir / "commit.txt").write_text(subprocess.run(

**Fix proposed:** Move the shared runner boilerplate (sha, commit/dirty/spec/lock/code hashes, DEV, the B{na}x{nt} name) into one helper module, and call it from every runner so all outputs record `dirty`. Consider refusing to start when dirty is true.

### [P3] research/frontier_classical_20261001/c7_c8_cases.py:4 (replayability; confidence 9)

The documented `timing` invocation leaves out `--rates`, which timing() needs (line 99: `rates_summary = json.loads(Path(rates_path).read_text())`). argparse declares it optional (line 145: `ap.add_argument("--rates")`), so following the docstring fails with TypeError: Path(None). c5_smoothers.py:93 has the same optional `--rates` for its timing phase.

> python -m research.frontier_classical_20261001.c7_c8_cases timing --item c7|c8 --out <dir>

**Fix proposed:** Add `--rates <rates json>` to the usage line, and in both runners error out when phase == 'timing' and --rates is missing (`ap.error(...)`).

### [P3] results/frontier_replay_20261001/q0_attribution/summarize.py:54 (dead-code; confidence 9)

The dict-literal value for `pooled_run_repeatable_in_T0` (lines 53-54) is an `== ... or "string"` expression that line 63 always overwrites (`summary["pooled_run_repeatable_in_T0"] = all(...)`). The first computation is dead, and its `or` gives a confusing bool-or-string type.

> == json.loads((HERE / "pooled_repeat_t0_b.json").read_text())["results"] or "non-timing fields compared below",

**Fix proposed:** Delete the key from the dict literal and keep only the line-63 assignment.

### [P3] results/frontier_replay_20261001/q0_attribution/attribution_diagnostic_L_single_thread.py:5 (stale-docstring; confidence 9)

A garbled edit spliced a sentence into the docstring mid-clause, producing '...by mistake into the unchanged P3 run...'. The title still says 'diagnostic 2' although STAGE_B_RESULTS.md and summarize.py call this one 2b. Because the script stores `purpose=__doc__`, the garbled text is archived verbatim in attribution_result_L_single_thread.json (verified).

> numpy 1.26.4 with LAPACK threads pinned to 1, as P3 workers do (L_8x52_numpy1.26.4_single_thread.npy). Diagnostic 2a used a multithreaded-MKL L by mistake into the unchanged P3 run in the T0 environment. If the

**Fix proposed:** Rewrite the docstring as 'diagnostic 2b' with the 2a note as its own sentence. Regenerating the result JSON would change archived output, so at most annotate it rather than rerun.

### [P3] results/frontier_replay_20261001/q0_attribution/attribution_diagnostic.py:9 (lint; confidence 9)

The q0_attribution scripts add 23 ruff errors to the health-stack lint (`ruff check .`), including F401 for this unused `os` import, E401/E702 multi-imports and semicolons in pooled_repeat.py, save_L_single_thread.py and scramble_inprocess.py, and many E501 lines in summarize.py. research/frontier_classical_20261001 and research/frontier_replay_20261001 are ruff-clean. The repo-wide lint was already failing (4713 errors at HEAD), so these errors are added on top of an existing failure.

> import os

**Fix proposed:** Remove `import os` and run `ruff check --fix` plus manual line wraps on q0_attribution/*.py. Alternatively, exclude the archived diagnostic scripts in pyproject's extend-exclude if they must stay byte-identical.

### [P3] research/frontier_classical_20261001/c1_rates.py:53 (replayability; confidence 8)

port_check gets the B8x52 reference price only from a Q0 *mismatch* entry (lines 51-53), and takes B4x12 from the archive. Replaying C1 against any Q0 report where `/results[1]/price` matched would therefore fail with a KeyError at line 66 (`q0_replayed_price=replayed[name],`). The 4x12/8x52 asymmetry is also hard-coded.

> replayed["B8x52"] = m["replayed"]

**Fix proposed:** Initialise both cases from the archived price, then override with any `/results[i]/price` mismatch, so a matching replay falls back to the archived value.

### [P3] research/frontier_classical_20261001/c4_coverage.py:47 (dry; confidence 8)

The prefix-mean accumulation loop (draw a CHUNK, cumsum, fill the 2^m marks, advance total/count) is copied five times. The copies are scrambles.run_scramble:102-113, timing.timed_scramble:83-92, c3_refa.oss_scramble:35-41, c4_coverage.preint_scramble:44-57 and c5_smoothers.smoother_scramble:44-52, and they have already diverged. c4 uses `min(sc.CHUNK, n_top)` (it should be `n_top - count`), timing uses `min(CHUNK, n_top - count)`, and the others always draw a full CHUNK. Results are equal today only because every n_top is a power of two of at least CHUNK.

> size = min(sc.CHUNK, n_top)

**Fix proposed:** Factor out one `prefix_means(sampler, per_point_fn, marks)` helper, used by all five, with the `n_top - count` sizing.

### [P3] research/frontier_classical_20261001/kernels.py:6 (stale-docstring; confidence 8)

The module docstring is out of date. `six_estimands` is used for more than the C1 rate study: through sc.run_scramble it also drives the C7/C8 rates and the m_top_rule probe. Line 7, 'timing (C2) uses `knockout_preint` alone', is also wrong now, because C2's `rqmc` method uses the later-added `knockout_plain`, which the docstring never mentions.

> preintegration of P1 (classical_exponent_pilot.evaluate) for the C1 rate study only;

**Fix proposed:** Update the docstring to list the three kernels and their consumers (C1/C7/C8 rates and the probe; C2/C4/sigma_Q).

### [P3] research/frontier_classical_20261001/c4_coverage.py:67 (dead-code; confidence 8)

`score` is not called anywhere in the repo (git grep), has no CLI phase and no test. The module docstring describes a function that does not exist: '`run` archives raw estimates'. Coverage, which is the point of item C4, can only be computed by ad hoc imports, so the scoring step of the archived run cannot be replayed.

> def score(estimates, levels, reference, ref_hw99, alpha_cells=18):

**Fix proposed:** Add a `score` phase to main(), reading the raw .npy files and the C3 reference JSON, and a small synthetic test of the coverage and Clopper-Pearson output. Rename `run` in the docstring to what actually exists.

### [P3] research/frontier_classical_20261001/timing.py:105 (dead-code; confidence 8)

timed_chunk computes and returns `sub` (sub-chunk partial sums), and its docstring advertises them, but the only consumer, c2_timing.load_balanced, never reads r["sub"]. It is extra work inside the timed task and misleads readers about how the small-n load-balanced marks are computed: they come from chunk 0's completion clock, not from sub.

> sub = {2 ** m: float(cs[2 ** m - 1]) for m in range(sc.M_MIN, 13)} if chunk == 0 else {}

**Fix proposed:** Drop `sub` and its docstring clause, or use it in load_balanced if sub-chunk means were intended.

### [P3] research/frontier_classical_20261001/c2_timing.py:87 (magic-coupling; confidence 7)

Constants that must agree are kept in separate modules. fit.T995_15 (15 dof) and n_eps's hard-coded `4.0` (sqrt 16) assume 16 scrambles, but c2_timing defines SCRAMBLES = 16 on its own. Changing either silently mismatches the half-width rule. c1_rates.py:61 indexes the estimand column as a bare `5` (`n["prefix"][5, n["ms"].index(m)]`), while c7_c8_cases uses `ESTIMANDS.index(e)`. q4_payoff.py:206-208 repeats the 1e-4 allowance three times.

> hw = T995_15 * means.std(ddof=1) / math.sqrt(SCRAMBLES)

**Fix proposed:** Define SCRAMBLES_C2 once in fit.py, derive T995 and sqrt from it, and import it in c2. Use ESTIMANDS.index("knockout_pre") in c1. Name ALLOWANCE in q4.

### [P3] research/frontier_classical_20261001/c2_timing.py:127 (test-coverage; confidence 7)

No test covers the logic that produces the headline T_C numbers. t_c picks between three conventions (measured confirmation with a rate-scaled wall time, measured small-n mark, modelled all-16) and computes fresh_cached. fit_ab and load_balanced's elapsed-per-mark are also untested. The same applies to the spec-pinned c7_c8_cases.c8_cases generator (no test pinning its 24 cases), q4_payoff.reference/load_target, and oracle.build_case's restore of module constants.

> def t_c(block, c1_est, eps):

**Fix proposed:** Add synthetic-block unit tests for each t_c branch, fit_ab and load_balanced. Add a test pinning c8_cases() (for example, a hash of the case tuples). Add a test that build_case leaves the module constants of barrier_oracle_depth unchanged after an exception.

## Reviewer: spec conformance (12 findings)

**Overall.** I reviewed the branch at f03166eb, read-only, against ANALYSIS_SPEC_STAGE_C.md v2.1 and ANALYSIS_SPEC_STAGE_B.md. I wrote no files.

**Two bugs bias reported numbers.** Both were logged as deviations D1 and D2 in commit 0083f086, after the reviewed HEAD. They still apply to f03166eb.
- **Q4 (P1, classical-favourable):** delta_fp is taken over the spot-clip edge draws, where the IR clips by design and the reference does not. The flip bound becomes absurd: delta_fp = 9.7e3 (4x12) and 2.9e6 (8x52), total = 9.46e4 and 2.82e7. Q4 then fails, and e_Q = 0 would become the primary quantum share. This is from the run at f03166eb in the shared tree (q4/q4.json), which is not committed at the reviewed HEAD.
- **C2 small-n rule (P2, quantum-favourable):** marks are stamped only per 2^12-point chunk. T_C at $0.10 and $0.03 is therefore overstated and not monotone in eps. Example, 8x52 preint: 0.91 s at $0.10 against 0.55 s at $0.01.

**Code that matches the spec.** I checked these:
- Canonical factor: Helmert columns, sine time basis, lexsort order and rotation recipe. All seven factor hashes in c1_summary match the spec, and the port check passed bit-exactly.
- Five-word seed keys for C1, C2 confirmation, C3 A/B, C4, Q4 and sigma_Q, with the correct purpose codes.
- Fit windows, B = 4000 whole-scramble bootstrap with the shared index, n(eps) formula and flags, and the claim C2 rule. I recomputed every canonical r and n(eps) from the archived .npy files and they match exactly.
- C2 conventions: all-16 primary, per-scramble median, load-balanced with 22 workers; repeat indices; confirmation key; n_run rounding; one-sided pooled scaling; the n(eps) <= 2^21 gate; fresh and cold runs.
- Ref A: 64 scrambles at 2^22, t_.995,63. The AS241 coefficients are correct.
- Ref B: PCG64 key, one-factor stepping, z_.995, 6 h budget.
- C4: cells, Clopper–Pearson intervals, Bonferroni over 18 cells, widened coverage, empirical c.
- OSS-BB: Sobol order and bridge.
- C8 generator. Q4 input law: midpoint uniforms, Box–Muller pairing, factor indexing, discount.
- T0/Q0 against Stage B; the only gap is the ruff import check.

**Results JSON.** No NaN or Infinity in c1, c2 or c3_refb.
- Ref B is consistent with C1 preint: 4x12 3.5186773 ± 4.1e-5 against 3.5186900; 8x52 3.2817661 ± 1.06e-4 against 3.2817760. Per-worker spreads are as expected.
- C2 anomalies: negative modelled times in the per-scramble and load-balanced sensitivities (e.g. -0.0148 s), and load-balanced times larger than all-16. The second comes from O(chunks^2) fast_forward overhead plus building a new Sobol generator per task.

**Smaller spec deviations.**
- C5, C7 and C8 timing seed with the C2 root.
- The C7 truncation probe is a separate solo run instead of the first completed scramble.
- There is no 2 CPU-hour budget on depth (b).
- Most runner JSONs lack seeds, spec/lock/code hashes and a dirty flag; c2 lacks the lock hash and core counts.
- The idle wait falls back to running after 2 h.
- T_C(eps) bootstrap propagation is not implemented.
- The [14, M] window is dropped when M = 18.

**Not yet implemented at this HEAD:** the comparator minimum and validation (section 0.3), basis-row T_C, C4 recalibration, C6 and anchors, and sigma_Q for the development cases. I did not count these as deviations.

### [P1] research/frontier_classical_20261001/q4_payoff.py:185 (correctness / Q4 bias (classical-favourable); confidence 97)

delta_fp is taken over every draw, including the edge draws built to trigger the spot clip. On those draws the IR clips log spots to ln 4096 by design and the float reference (ref_raw, clip=False) does not, so delta_fp measures the designed clip difference, not fixed-point error. The arithmetic term two lines earlier drops clip-event draws (`ok = ~b_flip & ~k_flip & (ref[:, 3] == 0)`, line 183); delta_fp does not. In the run at f03166eb (results/frontier_classical_20261001/q4/q4.json, shared tree, not in the reviewed HEAD), delta_fp = 9743.6 for 4x12 and 2.91e6 for 8x52. delta = 10*delta_fp, so every one of the 10^7 flip paths lands in the band (band_count = 10000000, p_upper99 = 1.0). The flip bound is 9.46e4 and 2.82e7, the total fails, and e_q_if_failed = 0.0. The cause is this artefact alone: law error is about 6e-9 and arithmetic error about 2e-8. The spec text itself says 'over all draws', so the code follows a flawed literal rule. This was logged after the reviewed HEAD as deviation D2 in 0083f086, with a recomputation in q4_deviation.py.

> worst, delta_fp = max(worst, err), max(delta_fp, float(np.abs(m_ir - ref[:, 1]).max()))

**Fix proposed:** Compute delta_fp only on draws with no clip event (ref[:,3]==0), or against reference(..., clip=True); keep clip events counted separately; report the literal value only as the logged deviation. Do not carry e_Q = 0 into the decision table.

### [P2] research/frontier_classical_20261001/c2_timing.py:150 (correctness / C2 T_C bias (quantum-favourable); confidence 92)

The small-n rule reads the warm all-16 elapsed time at the smallest prefix mark at or above n(eps). Marks are stamped only after a whole 2^12-point chunk is evaluated (timing.py:90 `stamps[n] = time.perf_counter()`), so every mark from 2^6 to 2^12 carries the time for 4096 points per scramble, not n(eps). In results/frontier_classical_20261001/c2/c2_timing.json, primary T_C is not monotone in eps. 8x52/preint: T_C($0.10) = T_C($0.03) = 0.9097 s (n(eps) = 40 and 298), but T_C($0.01) = 0.5535 s (measured confirmation, n_run = 2048). 4x12/preint: 0.1377 s at $0.10 against 0.1244 s at $0.01. This follows the spec text literally, but the measured quantity does not correspond to n(eps) points. Logged after the reviewed HEAD as D1 in 0083f086.

> mark = min(m for m in warm_all16 if m >= max(n, 2 ** 6))

**Fix proposed:** Report these rows with the D1 note, or time small n(eps) runs at their own size (one chunk of 2^ceil(log2 n), as the confirmation runs do). Do not present eps = $0.10 and $0.03 T_C as measured times.

### [P3] research/frontier_classical_20261001/c2_timing.py:135 (impossible values in reported sensitivities; confidence 85)

The per-scramble-median (i) and load-balanced (iii) models are fitted on marks of 2^13 and above, then evaluated at any n(eps), including far below 2^13. Negative intercepts then produce negative times. In c2_timing.json: B4x12/preint fits.per_scramble[0] = -0.0157, t_c['0.1'].model_per_scramble_median = -0.01476, t_c['0.03'] = -0.00882; B4x12/rqmc fits.load_balanced[0] = -0.0114 and t_c['0.1'].model_load_balanced = -0.000374.

> model_per_scramble_median=sum(x * y for x, y in zip(block["fits"]["per_scramble"],

**Fix proposed:** For n(eps) < 2^13, apply the same measured-mark rule to the sensitivity conventions, or clamp and flag rows outside the fitted range. Do not tabulate negative times.

### [P3] research/frontier_classical_20261001/timing.py:103 (implementation artefact / CF sensitivity understated; confidence 80)

Load-balanced convention (iii) builds a new scrambled Sobol generator for every (scramble, chunk) task (2048 tasks per 2^19 run) and fast-forwards it by chunk*4096 points. scipy's fast_forward costs time linear in the skip: measured locally at 0.2, 6.9 and 103 ms for skips of 1, 32 and 127 chunks at d=48, and 1.6 to 223 ms at d=416, with the machine loaded. Per scramble the skipped points sum to sum_c c*4096, about 33M points, roughly 64 times the 2^19 points actually used. That overhead grows like n^2, so the linear T(n) = a + b*n fit is misspecified. The measured LB times come out above all-16 even with 22 workers instead of 16: 8x52/rqmc 50.2 s against 39.7 s, and 8x52/preint 94.9 s against 89.5 s.

> sampler.fast_forward(chunk * CHUNK)

**Fix proposed:** Cache one sampler per (scramble, worker), or give each task a contiguous chunk range so fast_forward cost stays O(1) per chunk. Otherwise disclose that the CF load-balanced sensitivity includes O(chunks^2) skip overhead and per-task Sobol construction.

### [P3] research/frontier_classical_20261001/c3_refb.py:106 (spec deviation / provenance (section 0); confidence 80)

Spec section 0 requires every JSON to record the seeds, code SHA-256, spec SHA-256, lock SHA-256 and the SHA-256 of every factor L, and every run to come from a clean worktree recorded in its JSON. ref_b.json (already run) records only the commit: no seed root, no code/spec/lock hashes, no dirty flag. c3_refa.py, c4_coverage.py, c5_smoothers.py (commit.txt only), c7_c8_cases.py (commit.txt only) and q4_payoff.py are the same. c2_timing.json has code and spec hashes but no lock_sha256, no seed root and no factor hash (c2_timing.py:214 lists spec_sha256 and c1_summary_sha256 only).

> workers=rows, commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT,

**Fix proposed:** Reuse c1_rates' meta block (commit, dirty, spec/lock/code SHA, roots, factor hashes) in every runner. For already-run Ref B and C2, record the missing hashes in the deviation log.

### [P3] research/frontier_classical_20261001/c2_timing.py:82 (spec deviation / seed keys; confidence 75)

all16() hard-codes the C2 root 2026100121. Item C5 timing (c5_smoothers.timing calls c2_timing.run_block) and the C7/C8 timing repeats (c7_c8_cases.timing calls c2_timing.all16) therefore seed their timing and confirmation scrambles with the C2 root. Spec section 0 requires each item's own root: C5 2026100151, C7 2026100171, C8 2026100181. For C5 the keys [2026100121, 0|1, 1|3, rep, s] are exactly C2's preint/rqmc timing and confirmation scrambles.

> tasks = [(run_id, case, method, (ROOT_C2, case.case_index, purpose, replication, s), n_top)

**Fix proposed:** Pass the item root into run_block/all16, or log it as a deviation before the C5/C7/C8 timing runs.

### [P3] research/frontier_classical_20261001/c7_c8_cases.py:63 (spec deviation / C7 truncation rule; confidence 70)

The spec decides 16x52 truncation 'from the first completed 16x52 H = 140 scramble' of the run. The code instead times a separate solo probe to 2^16 in the parent process, before the 16-process pool exists. The timed region also includes the parent's first six_estimands call (numba compile or cache load in a fresh worktree) and Sobol construction for d = 832.

> sc.run_scramble((C7_CASES[0], "canonical", (ROOTS["c7"], 2, 0, 0, 0), 16))

**Fix proposed:** Use the time to 2^16 of the first completed scramble inside the pooled 16x52 H=140 run, or log the probe as a deviation before running.

### [P3] research/frontier_classical_20261001/oracle.py:46 (spec deviation / C7-C8 depth (b) budget; confidence 70)

compiled_depths has no 2 CPU-hour budget. It records wall-clock seconds (perf_counter), not CPU time, and runs to completion. The spec says depth (b) has a 'budget 2 CPU-hours per case, otherwise reported as not done'. c7_c8_cases.oracle catches exceptions only, never a timeout.

> started = time.perf_counter()

**Fix proposed:** Enforce the budget (subprocess with timeout, or measure process CPU time) and mark the case not done when it is exceeded.

### [P3] research/frontier_classical_20261001/c2_timing.py:72 (spec deviation / exclusivity and machine state; confidence 65)

wait_idle proceeds with timing after 2 h even if the machine is not idle. The spec says timing-bearing runs start only when the 30 s CPU average is below 10% and no other python process uses CPU. Idleness is checked once per block, not before the fresh, cold and load-balanced runs later in the same block (the 8x52/preint block ran about 26 min). The meta records only the CPU name (line 218 `cpu=powershell("(Get-CimInstance Win32_Processor).Name"),`), not the core counts the spec requires, and machine_state lists only python processes using more than 0.5 s CPU in 5 s, not 'the list of running python processes'. In the C2 run all four checks were idle=True, so no realized bias. The same helper serves C5/C7/C8 timing.

> if state["idle"] or time.time() - t0 > max_wait_s:

**Fix proposed:** Refuse to time (or abort and log) when not idle; re-check before each sub-run; record physical/logical core counts and the full python process list.

### [P3] research/frontier_classical_20261001/c2_timing.py:134 (spec deviation / missing uncertainty propagation; confidence 55)

C1 spec: 'joint (A, r) draws propagated to n(eps) and T_C(eps)'. fit.summarize propagates bootstrap draws to n(eps) only (fit.py:85 `draws = n_eps(boot[:, 0], boot[:, 1], eps)`). c2_timing.t_c produces point T_C values only, with no bootstrap interval from the joint draws. Nothing at the reviewed HEAD computes it.

> out = dict(n_eps=n, model_all16_unrounded=model,

**Fix proposed:** Store the 4000 joint (A, r) draws (or the n(eps) draws) in c1_summary and map them through the all-16 model (and confirmation scaling) to give T_C(eps) percentile intervals.

### [P3] research/frontier_replay_20261001/t0_env.py:24 (spec deviation / T0 pass check; confidence 45)

Stage B: T0 passes only if 'each top-level package imports'. t0_requirements.in pins ruff==0.15.16 as a top-level package, but IMPORTS omits ruff, so t0_passed never checks it. Everything else in T0/Q0 matches Stage B. That includes the script order, unchanged walk/timing_key, the exact-field counts (1611/108/57/209/2112/270 = 4367, read from provenance_replay_20260924.json) and the honest q0_passed = False with 61 mismatches.

> IMPORTS = ["numba", "numpy", "scipy", "mpmath", "matplotlib", "pytest", "markdown", "qiskit",

**Fix proposed:** Add 'ruff' to IMPORTS, or state in the receipt that ruff is checked as a CLI tool.

### [P3] research/frontier_classical_20261001/fit.py:19 (spec deviation / sensitivity windows; confidence 40)

The [14, M] sensitivity window is produced only when M >= 19. Spec C1 defines the sensitivity windows as [8, M], [12, M], [14, M] with M the top prefix. For the C7 16x52 cases truncated to M = 18, the [14, 18] window is silently dropped. C8 (M = 17) correctly lists only [8,17] and [12,17], per its own text.

> if m_top >= 19:

**Fix proposed:** Use `if m_top >= 18` (or emit w14 whenever 14 < M), or note in the deviation log that C7 truncated cases omit [14, 18].

## Reviewer: claims against evidence (14 findings)

**Overall.** Most numbers in the branch documents reproduce from their evidence. Stage A tables check out against summary.json and historical_frontier.json: depths, T-counts, widths, scores of 0.2647/0.2690/0.6232/0.6270, the budget identity, misses of 39,291.8x and 8,098.2x, layer requirements of 2.545/12.348 ps, and 254 hashes. So do the WHY_NO_ADVANTAGE §2.5 example (calls ≈ 34,000, ≈ 3,100 s, ≈ 110x slower, ≈ 1,100x budget miss, ≈ 3.6 days), the T0 receipt (39 wheels, lock hash, versions), the Q0 counts (4,367 and 61) with STOP reproducing, the replay ratios (1,604x and 16,348x), the P1/P3 gap (2.06 SE, p ≈ 0.04), the Ref A/B half-width forecasts, the Stage C closed-form eigenvalues and factor hashes, and the review tallies (56 = 33 major + 23 minor; 49/7/14).

The material problems are in the Stage B / E10 narrative:
- **Hidden mismatch.** The list of 13 mismatched fields wrongly includes the fit constant. The inherited 't_c' substring rule silently treats every fit constant and the Q1 T-counts as timing, so the changed 8x52 fit constant is not reported as a mismatch.
- **"Most quantum-favourable".** True only at ε = $0.001. At $0.01 the archived factor gives the lowest classical cost of the four.
- **Non-uniqueness.** Presented as 8x52-specific, contradicting Stage C §0.1, which shows 4x12 is also degenerate.

Literature/venue issues:
- L1 makes a false range-containment claim (0.48–0.63 is not inside 0.55–0.73).
- L1's C2 wording ('restore near-n⁻¹ for calls and digitals') is contradicted by the branch's own committed C1 results.
- L2's primary venue recommendation is conditioned on a 'go' that L1 did not give.
- The review record mischaracterizes a correct reviewer claim about SeedSequence key padding as false.
- Stage C executions (C1, C2, Ref B) are committed but not recorded in AI_USE_LOG or any results document.

No overstatement of advantage was found. Every document keeps the 'no defensible significant quantum advantage' verdict and labels its impossibility statements as scoped. I opened Chakrabarti v3 and Case v2: the L1 statements '10 MHz at 1 s' and 'v2 16 Sep 2026' match the sources. Review was read-only; no repository files were modified.

### [P2] manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md:38 (number-mismatch / missing disclosure; confidence 90)

The 13 exact P3 mismatches in q0_provenance_replay.json are price, std_error, rate_r and the 10 rqmc_std_one_scramble entries (1+1+1+10). fit_constant is not among them. provenance_replay_diff.timing_key classifies any path containing the substring 't_c' as timing, so every `fit_constant` (P1 16, P2 4, P3 2) and Q1's `forward_t_count` / `clean_call_t_count` fall outside the 'exact' set. The 8x52 P3 fit constant did change (archive 0.2957187660 vs Q0 replay 0.3374739592, checked in .context/frontier_q0_replay_20261001), but it is counted only under timing_fields_changed (27). That contradicts the plan's Q0 criterion (IMPLEMENTATION_PLAN.md:157 'Exact equality of prices, rates, fit constants and depths') and qualifies E9/E10's '4,367 non-timing fields'.

> The 13 P3 fields are its price, standard error, rate, fit constant and per-n standard deviations.

**Fix proposed:** List the 13 fields correctly. Disclose that the inherited classification treats fit constants and Q1 T-counts as timing because of the 't_c' substring, and report the 8x52 fit-constant change. That makes at least 62 scientific-field differences. Optionally add a supplementary exact comparison of those fields, labelled as a diagnostic.

### [P2] manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md:87 (unsupported-causal / overstatement; confidence 85)

Classical cost depends on both the fit constant A and the rate r: n = (A*t995/(4e))^(1/r). The archived factor has the lowest r but also the lowest A (0.296 vs 0.338/0.443/0.438). Recomputing barrier_decision's formula from the four P3 outputs gives points/scramble at eps=$0.01 of 1,579.5 (archive), 1,655.2 (Q0), 1,783.9 (diag 2a) and 1,809.9 (diag 1). So at $0.01 the archive has the smallest classical cost and D_max, making it the least quantum-favourable. At $0.03 it is also lowest (256 vs 261.6/263.0). The ordering holds only at $0.001. The same claim appears in the Direction column of ERRATA.md E10 (line 22). Separately, item C1 evidence already committed on this branch (c1_summary.json, window [10,19]) gives 8x52 knockout_pre r = 0.640 (archived) and 0.644 (eigh), against 0.597 (canonical) and 0.601-0.626 (rotations). Under that protocol the archived factor is near the top of the range, not the bottom.

> The archived value is the lowest. A lower r means a higher classical cost and a larger D_max, so the archive is the most quantum-favourable of the four.

**Fix proposed:** Scope the claim to eps = $0.001 under the P3 protocol, e.g. 'at the decision point the archived factor gives the largest T_C of the four'. Note that at $0.01 it gives the smallest. Make the same correction in ERRATA E10, and note that the basis ranking is protocol- and window-dependent (C1).

### [P2] manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md:52 (internal-contradiction / unsupported-causal; confidence 75)

This passage and ERRATA E10 ('4×12 has no computed ties and reproduced exactly') present non-uniqueness as an 8x52-specific property tied to computed exact ties. ANALYSIS_SPEC_STAGE_C.md:63-64 states, correctly (I verified the closed forms), that the covariance has '(na−1)-fold' degeneracy for every time mode, '4×12: twelve 3-fold'. The 4x12 factor is therefore equally non-unique. It reproduced because MKL and OpenBLAS eigh happened to return bit-identical output: eigh_4x12_numpy1.26.4.npz vals and vecs equal the T0 single-thread eigh exactly. The cause is not an absence of degeneracy. Also, '12 groups' was computed (summarize.py) from eigh_8x52_numpy1.26.4.npz, the multithreaded-MKL decomposition that line 73 says was used 'by mistake'. The T0 single-thread decomposition used by the Q0 replay has 11 tie groups (ten pairs and one triple), so the count is build-dependent.

> The PCA factor L of the 8×52 covariance `Σ_asset ⊗ Σ_time` is not uniquely defined. In exact arithmetic the eigenvalues repeat. The computed eigenvalues contain 12 groups of exact ties (4×12 has none).

**Fix proposed:** State that both development covariances have exactly degenerate eigenspaces (3-fold for 4x12, 7-fold for 8x52). Say that the 4x12 factor reproduced because both builds returned the same basis, not because it is unique. Report the tie count as 'from the numpy 1.26.4 multithreaded decomposition; 11 in the T0 single-thread decomposition', or drop it. Apply the same fix to ERRATA E10.

### [P2] manuscript/advantage-frontier-2026-09-23/literature/L1_PRIOR_ART.md:208 (overstatement / contradicted-by-branch-evidence; confidence 75)

OSS was executed only on the knock-out (barrier_oss_pilot.json has knock-out rows only), so it cannot have restored calls or digitals. Item C1, committed on this branch (48936070), also contradicts 'restore' for 8x52. Canonical call_pre r = 0.950 with interval [0.897, 1.006] is 'inconclusive'. Archived/eigh call_pre and digital_pre (0.897-0.912) are 'inconclusive'. Under rotation3, call_pre r = 0.849 [0.801, 0.896] and digital_pre r = 0.848 [0.805, 0.895] are 'does_not_restore'. The Dalzell row (line 173, 'Our near-n⁻¹ RQMC rates on 48- and 416-dimensional baskets') depends on the same claim.

> the two smoothers we executed (first-PC preintegration, and one-step-survival conditioning after Glasserman and Staum) restore near-n⁻¹ RQMC for basket calls and digitals

**Fix proposed:** Attribute call/digital smoothing to preintegration only. Replace 'restore' with the item C1 labels per case and basis (8x52 calls inconclusive or basis-dependent), following the Stage C claim C2 rule.

### [P2] manuscript/advantage-frontier-2026-09-23/literature/L2_VENUES.md:146 (internal-contradiction; confidence 65)

L2's primary recommendation (Quantum) is conditional on L1 returning 'go', and says the paper 'must lead with the general frontier, the calculator and the checklist'. L1_PRIOR_ART.md (same commit) returns GO_NARROWED. It says the argument 'is already published in general and illustrative form' (line 6). Its binding narrowings forbid 'a new framework' / 'the first requirements frontier' (N1) and make the calculator domain-specific with the QEA citation (N4). By L2's own definition condition 1 is not met, and the proposed lead framing conflicts with L1. L1 itself notes the narrowed claims suit a computational-finance or benchmark venue 'at least as well'. L2 never reconciles the two.

> The L1 novelty checkpoint is a "go", meaning the frontier argument is not already published.

**Fix proposed:** Update L2 §3 to the actual GO_NARROWED outcome. Restate condition 1 and the lead framing in line with N1-N6, or state explicitly that the Quantum recommendation predates the checkpoint and needs re-evaluation.

### [P3] manuscript/advantage-frontier-2026-09-23/literature/L1_PRIOR_ART.md:180 (number-mismatch; confidence 90)

The same row gives Achtsis et al.'s range as 'std-dev exponents are 0.55–0.73'. The project range 0.48–0.63 (P2 OSS 8x52 r = 0.479 through P3 4x12 r = 0.633) is not inside it, because 0.48 < 0.55. The ranges overlap; one does not contain the other.

> Our 0.48–0.63 lies inside their range

**Fix proposed:** Write 'overlaps their range (our lower end, 0.48 for OSS at 8×52, lies below it)'.

### [P3] manuscript/advantage-frontier-2026-09-23/AI_USE_LOG.md:46 (misrepresented-review; confidence 85)

The closure reviewer's NS-07 (stage_c_spec_closure.jsonl line 63) claimed '[a,b,c] == [a,b,c,0]; [a,b,c,0] != [a,b,c,0,0]', i.e. 3- and 4-word keys can alias. I checked in the T0 env (numpy 2.0.2): SeedSequence([a,b,c]) and SeedSequence([a,b,c,0]) give identical state and identical default_rng output, while the 4- and 5-word keys differ. The reviewer's claim is true. STAGE_C_SPEC_REVIEW.md:62 ('false for five words') rebuts something the reviewer did not say. Also, not every key has five words: the spec's rotation key `default_rng([2026100101, case_index, q])` (ANALYSIS_SPEC_STAGE_C.md:86) and the reused port-check key `[2026092333, dim, s]` are 3-word keys. No actual collision exists among the declared keys.

> A reviewer's claim about SeedSequence key padding was tested and found false, and the code follows the specification's five-word keys.

**Fix proposed:** Record the reviewer's padding claim as confirmed. Then note that the declared keys are five words except the rotation and port-check keys, which have no 4-word counterparts, so they cannot collide.

### [P3] manuscript/advantage-frontier-2026-09-23/literature/L1_PRIOR_ART.md:169 (internal-contradiction; confidence 80)

The Verified-column legend (lines 162-164) defines 'yes' as 'full text or the relevant section was read' and 'abstract' as 'only the abstract or metadata was read'. Stamatopoulos & Zeng is marked 'yes' while saying only abstract and metadata were read, and §6 item 3 confirms the body was not re-read. Brehm & Weggemans (line 175, 'yes (abstract and metadata)') has the same problem. The matrix overstates how deeply these two sources were verified.

> yes (abstract and metadata; body not re-read)

**Fix proposed:** Change both entries to 'abstract'.

### [P3] manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md:536 (internal-contradiction / stale claim; confidence 70)

L1_PRIOR_ART.md §2 item 5 reports that the Grand Challenge v3 'never says "finance" or "option"' and only cites Chakrabarti et al. in a Table 3 caption. It prescribes the rewording 'cites the derivative-pricing threshold estimate among quadratic-only resource estimates (Table 3 caption)', and §6 item 5 asks for WHY_NO_ADVANTAGE to be updated. The branch still says the paper 'places derivative pricing in the quadratic-only class' under 'Independent expert analyses reach the same classification'. Also, the rewritten §2.5 still relies on the archived 8x52 rate (27.1 s) without pointing to ERRATA E10.

> "The Grand Challenge of Quantum Applications", 2025, which places derivative pricing in

**Fix proposed:** Apply L1's wording at line 536, add the PRX Quantum 7, 020101 citation, and add an E10 pointer beside the §2.5 classical model.

### [P3] manuscript/advantage-frontier-2026-09-23/AI_USE_LOG.md:45 (missing-disclosure; confidence 60)

The branch commits Stage C executions: item C1 port check and seven-basis rates (48936070), item C2 timing, and the 6-hour-per-case Ref B overnight run (f03166eb, results/frontier_classical_20261001/{c1,c2,c3_refb}). The AI use log records only authoring the spec and code. No results document, IMPLEMENTATION_PLAN header line or spec deviation log records these runs or their outcomes. As a result, Stage B/E10 statements about the basis family stand next to contradicting C1 evidence (see the r-ordering and calls/digitals findings).

> The main agent wrote both specification versions and the Stage C code.

**Fix proposed:** Add an AI_USE_LOG entry for the Stage C executions (who ran them, which commit, what was run), and add a short status line or results stub for C1/C2/C3 Ref B to the IMPLEMENTATION_PLAN header.

### [P3] manuscript/advantage-frontier-2026-09-23/literature/L1_PRIOR_ART.md:270 (internal-contradiction; confidence 55)

N3 is called 'binding on the draft', yet the Stage C spec frozen in the same commit (ANALYSIS_SPEC_STAGE_C.md:415-421) defines the decision-point table with three depths: the favourable leaf-table score (QF), clean dependency-only and clean scheduled. There is no Chakrabarti-type (~9.5×10³) row. The two documents define the 'optimistic end' differently: Chakrabarti hand count in L1, leaf-table score at 0.26-0.27 of compiled depth in Stage C.

> The Chakrabarti-type hand count is the optimistic end of the bracket. The decision must be reported at both ends.

**Fix proposed:** Either add a labelled hypothetical 9.5×10³-depth row to the claim C4 table (as the WHY_NO_ADVANTAGE robustness bullet already does), or revise N3 to name the leaf-table score as the optimistic end.

### [P3] docs/research_investigation/2026-09-23/ERRATA.md:22 (overstatement; confidence 40)

P3 pins BLAS/LAPACK threads to 1 before importing numpy, so as committed it only ever builds single-thread factors: the archive's and the T0 replay's. Of the other three hashes in attribution_summary.json, two came from diagnostic scripts that imported numpy before pinning (multithreaded MKL and OpenBLAS). The third (diagnostic 1) is a monkey-patched hybrid of numpy 1.26.4 eigh with numpy 2.0.2 argsort. They are valid PCA factors, but 'the same code produced' them overstates it. In P3's real execution path the observed spread is 0.527 vs 0.541.

> The same code produced five distinct, equally valid factors (L Lᵀ = Σ)

**Fix proposed:** Say 'five distinct valid factors were obtained (two from P3's single-thread path in the two environments, three from diagnostics)', and state the P3-path spread separately.

### [P3] manuscript/advantage-frontier-2026-09-23/AI_USE_LOG.md:37 (internal-contradiction; confidence 35)

L1_PRIOR_ART.md:27 says the search agents that wrote both L1 JSONL files 'were interrupted before they could summarize'. L2_VENUES.md:19 says l2_venues.jsonl was 'written by a search agent that stopped before it finished'. That implies all three searchers stopped early, not two.

> two were cut off by a usage limit after saving

**Fix proposed:** Reconcile the count across the three documents, or state which searcher finished.

### [P3] manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md:89 (imprecise-claim; confidence 30)

The diagnostic-1 price (3.2817120) differs from the archive (3.2816161) by 9.6e-5. That is within the archive's SE (1.02e-4) but larger than diagnostic 1's own SE (8.2e-5), so the claim depends on which SE is meant (the combined SE is 1.31e-4). Similarly, line 95's 'r between 0.53 and 0.57' does not quite contain the stated 0.527-0.572.

> Prices agree within one standard error.

**Fix proposed:** Say 'within one combined standard error (max |Δ| = 9.6×10⁻⁵ vs combined SE 1.3×10⁻⁴)' and use 0.527-0.572 consistently.

