# Stage C specification review — dispositions

1 October 2026. Three critic agents (Claude Code subagents) reviewed version 1 of
[ANALYSIS_SPEC_STAGE_C.md](../ANALYSIS_SPEC_STAGE_C.md) before any Stage C run. They were
read-only and had separate lenses: statistics (S01–S18), fairness and claims (SCF-01–SCF-20),
and feasibility (F01–F18). Raw findings: `stage_c_spec_statistics.jsonl`,
`stage_c_spec_fairness.jsonl`, `stage_c_spec_feasibility.jsonl`. There were 56 findings:
0 critical, 33 major and 23 minor. All three reviewers judged that none bears on the fixed
verdict. This is internal AI-agent review, not peer review.

All findings were accepted except where noted. Where critics disagreed, the stricter
symmetric option was taken, and the alternatives are listed.

| Theme | Findings | Disposition in version 2 |
|---|---|---|
| Classical comparator | SCF-01, S10 | §0.3: T_C = minimum over all validated estimators and both platforms, including the plain-MC anchors. Preint-CPU-only becomes a QF sensitivity |
| Basis roles and rotation recipe | SCF-02, S06, S07, S17, F10 | §0.1 pins the Helmert form, lexsort order and tests (column order, thread invariance, factor hashes). §0.2: canonical primary; rotations inside exact eigenspaces (4×12 included) with a fixed recipe; archived and T0 eigh factors also run; QF/CF basis sensitivities; paired bootstrap |
| Timing conventions | SCF-03, SCF-04, F05, F18 | C2: three conventions; all-16 submit-to-result primary (QF); load-balanced on 22 workers as the CF sensitivity (SCF-03 also proposed 16 workers; one pool kept). Warm primary (CF, disclosed); fresh-cached carried as QF; P3 pipeline pinned; scope is the knock-out only |
| Measured confirmation | SCF-05, S09, F06 | n_run = 2^⌈log2 n(ε)⌉; 20 replications with fixed seeds; median wall time; pooled-sd accuracy check that scales T_C, never re-chooses n. SCF-05's rerun-once rule was not adopted (one pre-set scaling instead) |
| n(ε) flags and windows | S01, SCF-16, S12, F07 | No floor on n(ε). Two-sided flags. T_C below 2^13 is measured at the smallest mark. Windows for truncated runs; truncation decided once, before any fit |
| σ_Q | SCF-07, S11, F08 | §0.4: 2^20 iid paths, ddof 1, for every case, primary. S11 proposed keeping P1's value for development cases; not adopted. P1's value is reported beside it |
| Oracle depth and claim C4 table | SCF-08 | Favourable score kept for the unchanged stop rule, labelled QF. Compiled depths for item C7/C8 cases. New decision-point table with three depths; headline = clean dependency-only compiled depth |
| Claim C2 rule | SCF-09, S10, F14 | Interval-based, per (case, payoff, method), all development and item C7 cases. F14's point-estimate rule was not adopted. F14's OSS-BB Sobol order was adopted |
| Untried smoothers | SCF-10 | Listed as not done (numerical smoothing, barrier IS, preint + OSS, and Xie–He–Wang 2019 from the L1 screen). Deviation row 2 stays open |
| Q4 | SCF-11, S14, F12, F13 | IR file and hash pinned; IR input law in the reference; ≥ 10⁴ draws (the fallback was dropped); law error, Clopper–Pearson flip bound and arithmetic summed; the quantum share is reduced if the total exceeds ε/10 |
| References | SCF-12, S02, S03, S15, F02, F03, F15 | Ref A fixed at 2^22 × 64, with its unreachable ε/10 target stated now. Time-ordered OSS kept as a disclosed deviation. Ref B: 6 machine-hours per case on 16 CPU processes (F03). S03 proposed 12 hours and SCF-12 proposed 20; one overnight slot was chosen and the plan reading disclosed. Inverse-variance reference. Holm-adjusted secondary tests |
| Coverage | S04, S05, SCF-12 | Primary cell, Bonferroni-level under-coverage rule with recalibrated n(ε), 4×12 arm at 2^17, 8×52 decision-point coverage stated as assumed. Reference-limited threshold 0.25× the half-width (S02); SCF-12's /10 not adopted |
| Rigorous sensitivity | SCF-13, S16, F16 | Both sides use the knock-out range. Maurer–Pontil classical; quantum k from L3 when available, else a labelled transferred approximation |
| 0.45ε share | SCF-14 | Disclosed as QF; e_C = 0.9ε as a CF row |
| Power plan | SCF-15 | Balanced on AC primary (QF, disclosed); never changed between primary repeats |
| Port check | SCF-19, S08, F01 | P3 root reuse disclosed; single-thread factor hash check; failures not re-run |
| P1 supersession | SCF-20 | Stated as a deviation from plan item C1 |
| GPU pipeline and float32 | SCF-06, S18, F04, F17 | Host uniforms on 4 feeders; ndtri, GEMM and estimand on the device (F04). SCF-06's fully device-side Sobol was not adopted: uniform generation is about 3% of per-point time once ndtri and GEMM move to the device. Float32 is eligible at ε/10, the same as Q4 (SCF-06); S18's $10⁻⁵ report-only gate was not adopted. Anchor construction pinned |
| Item C7/C8 details | SCF-17, S13, F08 | Case indices; C8 generator pinned; bins ≤ 1, ≤ 10/3, ≤ 10; consequence of any non-STOP stated; T_C = all-16 model, labelled QF. F08 proposed the historical median as primary; it is kept as a sensitivity for consistency with item C2 |
| Seeds, memory, schedule, cuts | F09, F10, F11 | Seed key with case_index and purpose; chunking rule; exclusivity for timing runs; day order; cut rule decided from elapsed time only |
| Naming | SCF-18 | "item" vs "claim" used throughout; claim C7 is outside Stage C |

Added after the review (not raised by the critics): runs execute from a clean detached
worktree, because another session was found editing the shared working tree on
1 October 2026, including `research/controlled_source_completion/primitives.py`.

## Closure round (version 2 → 2.1)

A fresh closure reviewer checked version 2 against all 56 findings
(`stage_c_spec_closure.jsonl`). It found 49 closed, 7 partially closed and 0 open, plus 14
new problems introduced or left by the revision (3 major, 11 minor). It judged version 2
not ready to freeze. Version 2.1 addresses every item:

| Item | Disposition in 2.1 |
|---|---|
| SCF-01 partial; new: anchors via throughput (major) | Anchors timed end to end at N(ε) = ⌈(z·σ_Q/0.45ε)²⌉; "validated" defined as passing the agreement test against the C4 reference; selection bias of the minimum labelled CF, runner-up reported |
| New: no primary-execution or re-run rule (major) | Section 0 "Executions": first complete execution primary; re-runs only for crash, failed validation or test-found defect, logged before they start; timing code fixed at a recorded commit; spec frozen at its commit |
| New: C4 recalibration propagation (major) | Every RQMC candidate's T_C × (c/t)^{1/r} with its own r, no re-run; anchors and items C7/C8 unchanged, with coverage stated as assumed |
| S07 partial; new: basis and e_C rows | All sensitivity rows use the all-16 warm model at their n(ε); canonical also shown on that convention |
| S18 partial | Float32 bound defined over the 32 scrambles |
| SCF-04 partial; new: factor in timing | Rate runs cache the factor; timed runs build it inside the timed interval. Repeats aggregated by OLS on per-mark medians |
| SCF-06 partial | Reason restated (feeder and transfer throughput, not CPU share); transport pinned to shared-memory double buffers; host generation labelled QF, kernel-only its CF bound |
| SCF-13 partial | Now fully adopted: the rigorous row waits for plan item L3; the archived compound schedule is not used |
| SCF-19 partial | A port or setup failure blocks item C1; continuation only by a dated deviation |
| New: C3 agreement-failure branch | Both prices reported; the reference giving lower coverage decides (QF); validations must pass against both |
| New: C7/C8/table details | C8 uses depth (a) for counts and trigger, reports (b); C8 T_C = all-16 model; trigger also for development cases; C7 rows labelled preint-CPU |
| New: seed gaps | Five-word keys everywhere, purpose codes 0–9, replication indices for every repeat type, σ_Q root, bootstrap root. The reviewer's claim that SeedSequence zero-padding makes shorter keys equivalent was checked and is false for five words; code uses the five-word keys as written |
| New: unlabelled choices | Section 0.5 lists the additional QF and CF labels |
| New: Q4 details | Absolute law error; δ defined on the traced max-basket node; no analytic bound used; at least 10⁴ draws with no fallback |
| New: coverage cells and resolution | Raw coverage primary; Bonferroni over 18 cells; resolution = hw99(A) + hw99(B) |
| New: overnight slot and exclusivity | Ref B runs alone; timing runs require no compute job of any session, checked with a Windows counter; power-of-2 rule scoped to Sobol runs |
| New: cut trigger | Calendar deadlines per item from the freezing commit's date; effects of each cut stated |
| New: 4×12 archived factor | Defined as the T0 single-thread eigh factor (it reproduced the 4×12 archive exactly), with hashes of all factors |
| Code findings CODE-01 to CODE-05 | 01–04 were already fixed in the code at review time (seed keys, rotation key and q = 1–4, per-worker cache, archived option and hashes). 05: a test now pins the canonical 4×12 factor's SHA-256 |
