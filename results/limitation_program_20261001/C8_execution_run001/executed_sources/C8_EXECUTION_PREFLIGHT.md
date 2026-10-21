# C8 prospective local execution preflight

Author-only, 3 October 2026. No cases, factors, payoffs, fits, tests, preparation or
timing were evaluated to write this preflight. The companion JSON freezes the Git
blob SHA-256 inventory read from commit
`b4a4bdc9bd21099fd1382dff7f9e57c470a54d3a`. This document is prospective evidence,
not an execution receipt or a solved limitation.

The next C8 slot follows terminal W10 evidence. All financial, MPS and other compute
jobs must be terminal before admission. Timing reserves the whole machine for the
supervisor, the unchanged producer and its descendants, including Windows spawn
children and resource trackers. No heavy job from any session may share that slot.
The supervisor requires the actual `WAVE10_run002` terminal summary/manifest,
verifies every owned and frozen-input SHA, and copies its own packet into the new
receipt before input generation. Its included receipts must contain MPS, financial
run005 and the independent financial auditor; their outcome need not adopt a new
financial method.
The CPU-censored `WAVE10_run001` remains an immutable failed attempt with zero
credit; it does not satisfy this gate.

## Checkout, output and deadline

Use the new detached worktree
`C:/Users/prith/quantum_option_pricing/.context/stage_c_c8_20261003_run001`, whose
HEAD must be the exact commit above and whose tracked/untracked status must be
clean. Preserve `.context/stage_c_b4a4bdc9` and its untracked C7 output under
`results/frontier_classical_20261001/c7/`; do not clean or reuse that worktree.
The root agent created the new worktree; runtime admission must still verify it.

The interpreter is `.context/frontier_t0_env/Scripts/python.exe`: Python 3.12,
NumPy 2.0.2, Numba 0.60.0, llvmlite 0.43.0 and SciPy 1.13.1. Capture fresh versions,
distribution files, native DLL/PYD bytes, interpreter/base-interpreter bytes,
thread variables, CPU/core/affinity/power-plan/AC state and the frozen lock.
The runtime copy includes adjacent CPython/CRT DLLs and requires the pinned venv to
disable base/user site packages. Version equality and captured installed files do
not reconstruct the hashes of the original locked wheel archives.
Reject nonempty inherited `PYTHONPATH`, `PYTHONHOME` or `NUMBA_CACHE_DIR` before
capture or generation. Confine existing Python search paths and installed
distribution locations to the pinned venv, base runtime, fresh worktree or frozen
executed-source directory. Capture any permitted existing zip archive. Verify
the imported scientific module and existing cached-bytecode paths against the
same captured bytes before input generation and again afterward.

The prospective runtime inventory cap is 24,000 files and 2 GiB. A read-only
metadata admission probe counted 20,754 files / 1,137,169,506 bytes, including
existing bytecode; the earlier 20,000-file assumption was corrected before any
execution. Retain every existing PYC/PYO, DLL and other captured runtime file.
This file-cap correction uses no numerical outcome and leaves the 900-second
inventory guard, phase wall limits and 25,000-file terminal-owned cap unchanged.
The historical T0 environment receipt is context only: its lock SHA starts `9ee324`,
whereas this commit's lock SHA is
`eadf9b8eeddd27340904ba920e57dba681d2d2c40e293725a6339761e9ae9ecd`.
Do not infer fresh lock admission from the historical `installed_matches_lock`.

The first receipt is
`results/limitation_program_20261001/C8_execution_run001`; it must be absent.
Both original C8 phase directories below must also be absent. Capture receipts
outside the detached worktree so `require_clean()` keeps its original meaning.
Do not edit original code, the spec, the lock or archived output.

The original rates producer must actually launch before
**4 October 2026 00:00 IST** (`2026-10-03T18:30:00Z`). Preparation or a supervisor
launch alone does not meet the deadline. Once rates start in time, timing may
start after that deadline. A missed start is `not done`; it is not a reason to
change cases, sample counts or the calendar rule. Preserve every failed or
censored attempt; no automatic retry, overwrite, cleanup or resume.

## Unchanged numerical work

The original module generates all 24 cases, indices 100 through 123, in six
strata: 4x12, 4x52, 8x12, 8x52, 16x12 and 16x52, four cases per stratum. For each
`s,j`, it uses `Generator(PCG64(SeedSequence([2026092301,s,j])))`, drawing H/S0,
sigma and rho in that order from U(1.15,1.6), U(0.15,0.45) and U(0.1,0.7).
S0=100, K=100*(0.9,1.0,1.1)[(s+j)%3], r=0.03 and T=float(1+j%2).
Development cases are excluded. No generated values are present in this preflight.

Rates use the original canonical closed-form PCA, 16 workers, 32 scrambles,
2^17 points, prefix marks m6..17, 4096-point Sobol chunks, clipped SciPy ndtri,
single-thread BLAS and original Numba kernels with fastmath disabled. The saved
arrays retain all six estimands; C8 summaries select `knockout_pre`. Fits use
the primary [10,17] and sensitivities [8,17], [12,17], with the unchanged 4000
whole-scramble bootstraps. Sigma_Q retains 2^20 iid paths, ddof1 and its original
1000 bootstrap resamples. There is no C7 truncation for C8, including 16x52.

Rate seed keys are `[2026100181,case_index,0,0,s]`, s0..31. Timing keys are
`[2026100181,case_index,1,0,s]`, s0..15. Sigma_Q keys are
`[2026100107,case_index,7,0,0]`; rate/bootstrap and sigma-bootstrap roots are
2026100112 with the original purpose/stream fields. Seal the complete prospective
key inventory before any outcomes; these are source-derived keys, not saved
worker-stream observations.

Timing retains one warm 16-stream run per case to 2^17 and OLS T(n)=a+b*n on
m13..17. Primary T_C($0.001) is the all-16 warm **model** evaluated at the rates
n(eps); the per-scramble median model is a sensitivity. It is CPU preint only,
without a per-case price reference, 20-replication accuracy confirmation, cold
or load-balanced arms, or a measured hardware crossover. Coverage remains
assumed under the frozen Stage C specification.

From the fresh worktree, execute the unchanged original arguments:

```text
<pinned-python> -m research.frontier_classical_20261001.c7_c8_cases rates --item c8 --out C:/Users/prith/quantum_option_pricing/results/frontier_classical_20261001
<pinned-python> -m research.frontier_classical_20261001.c7_c8_cases timing --item c8 --out C:/Users/prith/quantum_option_pricing/results/frontier_classical_20261001 --rates C:/Users/prith/quantum_option_pricing/results/frontier_classical_20261001/c8/rates/c8_rates.json
```

## Prospective companion capture and its limits

Freeze companion code and this policy before any case generation. Admission first
captures exact Git/checkout code, spec, lock and bounded runtime bytes. Only then
may an isolated companion process import the frozen case generator and canonical
factor function, generate all fixed inputs, and seal the case/seed/expected-factor
inventory. Store every expected L as float64 C-order bytes and its SHA-256, with
shape/dtype/order and source/runtime bindings. Do not display, rank or select
generated cases before the original rates process starts. Do not compute payoffs
or inspect results in this capture phase.

The unchanged original workers regenerate their factors. They do **not** emit
factor-L hashes, and this companion cannot certify the bytes actually used inside
those workers. Expected-factor hashes plus identical pinned source/runtime are
reproducibility evidence. They must never be relabelled worker-time hashes or a
retroactive satisfaction of the spec's stronger every-used-L SHA requirement.
No instrumentation, monkeypatch or intrusive producer change is authorized.

Before timing, require successful rates termination, all 24 exact case identities,
the original m17 settings, complete prefix files and expected summaries. Freeze
the exact original-path `c8_rates.json` bytes, hash them and verify an immutable
receipt copy. Pass the original path to the unchanged timing command; verify its
SHA after timing. The original producer has no internal-read hash trace, so keep
that narrower limitation explicit. No writer may modify the rates input during
timing. Live mutable control files are provenance only; bind their verified
immutable copies as frozen receipt inputs.

## Exclusivity, STOP and finite guards

D6 originally checks a 30-second CPU average below10% and other Python processes'
5-second CPU deltas, flags >0.5 CPU seconds, and waits up to7200 seconds per case.
It checks before pool creation; worker initialization and the total 24-case phase
have no finite original bound. Do not edit this checker or exempt unrelated
Python. A separate supervisor stays passive during original timing and avoids
hashing or numerical work inside the measured interval. Its own Python process
can still trigger D6 if it consumes CPU; such a refusal remains failed evidence.
Verify AC/Balanced-plan state externally as well, since the original checker
records battery state but does not enforce it.

Prospectively, a standalone Windows supervisor imposes **12 hours for the whole
rates phase and8 hours for the whole timing phase**, including admission/capture,
idle waits, startup/warmup, execution, descendants, hashing and output verification.
Pre-run inventory additionally has a900-second bound. These are external wall
guards, not original numerical stopping rules. There is no invented aggregate
CPU limit: record actual job-tree CPU accounting if obtainable, and state any
unavailable accounting. Reserve120 seconds within each phase for failure retention.
The child is created suspended, assigned to a kill-on-close Windows Job Object,
then resumed. The job covers every descendant; hard timeout terminates the entire
tree. Verify no surviving descendants before hashing final output. A job/admission
failure must not leave an uncontained process running.

Record full process identity inventories before, during and after timing. Reject
unrelated experimental/timing Python, native compute jobs or conflicting launch
roots; allow only the actual supervisor/verified matching launcher and its job
descendants. Root-level machine reservation remains necessary: bounded process
observations cannot prove absence of a transient external job between samples.
Known compute binaries and other Stage C supervisors are blocking even when idle.
Other process CPU increments are recorded, with no blanket application-name
exemptions. Aggregate CPU outside the owned tree at or above10% of logical hardware
capacity is blocking; an ordinary process's isolated CPU increment is not itself
an unconditional failure. The original D6 checker remains unchanged.
Unavailable protected-process CPU counters are reported explicitly. The observed
outside-CPU percentage is always a lower bound because new, exited or transient
processes can be missed even when every sampled counter is readable. This never establishes continuous
machine exclusivity or substitutes for the original complete machine-load check.
Preserve that observational limit and the original machine logs. The previous
Day2b shell wrapper has no whole-phase timeout and does not stop subsequent
commands after an earlier nonzero return; it is unsuitable for this C8 admission.

Oracle STOP is separate from operational timeout. Later depth(a) uses the original
favourable leaf-table score, D_min >10*D_max($0.001),100ns layers and k=3. Depth(b)
retains D8's7200-second per-case child wall limit and reports failed/censored
compiles as not done. Do not launch oracle work concurrently with timing. D12
requires compiler output inside its running worktree; the requested main-checkout
rates/timing paths are not affected. Oracle execution is not authorized by this
rates/timing supervisor preflight.

## Terminal receipt

Create one fresh immutable receipt. Freeze exact author code/preflight bytes before
execution; record actual executed paths and equal-SHA copies, with canonical
confined snapshot paths and no caller-provided expected-hash override. Verify
code/spec/lock/runtime pre/post and all copied producer files. Hash/copy work is
charged to the phase wall guard and bounded file/byte inventories. Preserve all
original outputs, stdout/stderr, process observations and failure diagnostics.
Write a terminal summary and manifest once, after successful or failed terminal
tree evidence; never publish a provisional manifest. If retention cannot be sealed
within the reserved budget, write an explicit failed-unsealed marker without a
manifest certificate. No failed/censored phase receives completion or fixture
credit; this author-only packet and companion capture have zero fixture credit.
The manifest uses the recognized canonical ROOT-relative `files` and
`frozen_inputs` maps. Mutable actual paths stay in separate scoped provenance.
If job-tree zero cannot be certified, preserve raw partial output and an explicit
failed-unsealed marker; do not hash/copy producer output or issue a manifest.

Completion of rates/timing still does not complete C8's oracle/decision work,
resolve G2..G5, demonstrate accuracy confirmation, or establish quantum advantage.
