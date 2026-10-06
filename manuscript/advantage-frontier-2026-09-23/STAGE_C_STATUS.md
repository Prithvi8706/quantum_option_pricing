# Stage C status and handoff — 2 October 2026

**6 October checkpoint:** the table below is the historical 2 October manuscript handoff. Later local timing work and the failed C8 deadline attempt are recorded in the [current limitation status](../../docs/limitation_program_20261001/STATUS.md) and [final checkpoint](../../docs/limitation_program_20261001/FINAL_CHECKPOINT_20261006.md). The separate generic A14 Stage C resource rejection remains distinct from that classical C8 work.

Written for the next agent, or anyone who picks this work up cold. It records where the
measured requirements-frontier paper stands when PR #13 merges, how to resume, and which
decisions are still open. The rules are in [ANALYSIS_SPEC_STAGE_C.md](ANALYSIS_SPEC_STAGE_C.md)
(frozen; changes only through its dated deviation log D1–D12) and the plan in
[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

**Verdict (fixed wording): "No defensible significant quantum advantage established yet."**
Every stop-rule row computed so far holds STOP. The paper is a requirements and negative
result; it claims neither advantage nor impossibility.

## Glossary

| Term | Meaning |
|---|---|
| Claim C1–C7 | The paper's claims (IMPLEMENTATION_PLAN.md §1). Claim C2 is the smoothing claim, C3 the oracle bracket, C4 the decision-point miss factors, C6 the frontier, C7 the hardware screen |
| Item C1–C8, Q0–Q10, T0, L1–L8, X1 | Plan work items (IMPLEMENTATION_PLAN.md §3). "Item C2" (timing) is not "claim C2" (smoothing) |
| T0 / Q0 | Pinned environment / provenance replay of the six 23 September scripts (Stage B) |
| Q4 | Payoff validation: the quantum circuit's integer arithmetic (IR) against an independent float64 reference |
| E1–E10 | Entries in `docs/research_investigation/2026-09-23/ERRATA.md`; E10 is the non-unique PCA basis |
| D1–D12 | Dated deviations in the Stage C spec's log |
| QF / CF | A choice that favours the quantum / the classical side. A larger classical time T_C is QF |
| ε, k, t_layer | Price accuracy ($), estimator constant (quantum calls per σ/ε), time per logical T layer. Decision point: ε = $0.001, k = 3, t_layer = 100 ns |
| T_C, σ_Q, D_max | Measured classical time to accuracy; per-sample sd of the plain payoff the oracle computes; the largest oracle T-depth per call that still allows a 10× quantum win, D_max = T_C / (10 · k·σ_Q/(0.45ε) · t_layer) |
| Development cases | Equal-weight basket knock-out call, S0 = K = 100, H = 140, σ = 0.3, ρ = 0.4, r = 0.03, T = 1; shapes 4×12 (assets × dates) and 8×52 |
| Canonical basis | Closed-form PCA factor (spec §0.1) replacing `numpy.linalg.eigh`, whose basis is build-dependent (E10) |
| H1, P1–P3, Q1 | H1 is the 23 September hypothesis that discretely monitored basket payoffs defeat classical smoothing (`docs/research_investigation/2026-09-23/DECISION.md` §5); its falsifier said STOP. P1 is the classical exponent pilot, P2 the one-step-survival pilot, P3 the compiled 16-process pilot, Q1 the scored oracle depth (scripts in `research/advantage_frontier_20260923/`) |
| N1–N6 | The narrowings attached to the L1 GO_NARROWED recommendation (`literature/L1_PRIOR_ART.md` §5) |
| B4x12 / B8x52 | Development cases: 4 assets × 12 monitoring dates and 8 assets × 52 |

## Item status at merge

| Item | Status | Commit (code) | Results |
|---|---|---|---|
| T0 environment | Done, passed | `d3a6950d` | `results/frontier_replay_20261001/t0_environment.json` |
| Q0 replay | Done, failed exact equality on 8×52 P3 only; attributed (E10) | `d3a6950d` | `results/frontier_replay_20261001/` |
| L1 prior art | Done; recommendation GO_NARROWED (open decision 1) | — | `literature/L1_PRIOR_ART.md` |
| L2 venues | Done; recommendation Quantum / QIP (open decision 2) | — | `literature/L2_VENUES.md` |
| C1 rates | Done | `9079e185` | `results/frontier_classical_20261001/c1/` |
| C2 timing | Done (D1, D3, D4 apply) | `18d0ca31` | `results/.../c2/` |
| C3 Ref A, Ref B | Done; agreement test passes in both cases | `f03166eb`, `18d0ca31` | `results/.../c3_refa/`, `c3_refb/` |
| Q4 payoff validation | Done; literal fails only through D2; D2 recomputation passes at 1.79×10⁻⁵ | `f03166eb`, `0083f086` | `results/.../q4/`, `q4_d2/` |
| σ_Q (development) | Done | `f961193c` | `results/.../sigma_dev/` |
| C5 smoother rates | Done | `f03166eb` | `results/.../c5/rates/` |
| C7 rates | Done | `9d734ff5` | `results/.../c7/rates/` |
| C7 depth (a) | Done | `9d734ff5` | `results/.../c7/oracle/` (depth (b) failed there, D12) |
| C7 depth (b) | Done under D12: clean dependency-only T-depth 3,343,110 (4×12), 3,341,190 (8×52), 3,344,038 (16×52); compiled artifacts untracked, SHA-256 manifest tracked | `b4a4bdc9` | `results/.../c7/oracle_d12/` |
| C4 coverage | Raw estimates running, then scoring | `9d734ff5` | `results/.../c4/`, `c4_score/` |
| C5 timing, C7 timing | Queued after C4 (exclusive timing runs; refused if the machine is busy) | `9d734ff5` | `results/.../c5/timing/`, `c7/timing/` |
| C8 out-of-sample | Not started. Cut deadline 4 October 00:00 IST | `9d734ff5` or later | `results/.../c8/` |
| C6 GPU | Not started (code not written). Cut deadline 5 October 00:00 IST; if cut, carry g ∈ {1, 10, 100} | — | — |
| Final decision table | Interim only (`decision_interim_v2/`); rerun `decision.py` once C5/C6/anchors exist | `9d734ff5` | — |

Results produced after the merge go into a follow-up PR from the same branch. **Merge PRs from this branch with a merge commit, never a squash.** Result files record the commits they ran from (for example `18d0ca31`), and a squash would leave those commits unreachable from `main`.

Why work continued after Q0 failed: the Stage B spec required the mismatch to be reported and added to ERRATA, not tuned away, and the plan stops only if the STOP decision itself fails. The mismatch was fully attributed (E10) and STOP reproduced.

Cut deadlines (spec, "Schedule, exclusivity and cuts"; Day 1 = 1 October 2026): an item not started by its deadline is cut and reported as not done. C5: 3 October 00:00 IST (already started, so it will be completed). C8: 4 October 00:00 IST. C6: 5 October 00:00 IST.

Concurrency at merge: the author's separate limitation-program job was running on the same machine. Timing runs (C5, C7 timing) wait up to 2 hours for an idle machine and are then refused (D6); a refused run is recorded, and it should be re-queued when the machine is idle.

## How to resume

Every run starts from a clean detached worktree of a committed revision (spec §0); runners
refuse a dirty checkout and never overwrite an output directory. The pinned interpreter is
`.context/frontier_t0_env/Scripts/python.exe`. To rebuild it on another machine, run
`py -3.12 research/frontier_replay_20261001/t0_env.py build` after downloading the wheels in
`t0_requirements.lock`. Example:

```
git worktree add --detach .context/stage_c_<commit> <commit>
cd .context/stage_c_<commit>
PY=<repo>/.context/frontier_t0_env/Scripts/python.exe
RES=<repo>/results/frontier_classical_20261001
$PY -m research.frontier_classical_20261001.c4_coverage score --res $RES --out $RES/c4_score
$PY -m research.frontier_classical_20261001.c5_smoothers timing --out $RES/c5 --rates $RES/c5/rates/c5_rates.json
$PY -m research.frontier_classical_20261001.c7_c8_cases timing --item c7 --out $RES --rates $RES/c7/rates/c7_rates.json
$PY -m research.frontier_classical_20261001.c7_c8_cases rates  --item c8 --out $RES
$PY -m research.frontier_classical_20261001.c7_c8_cases timing --item c8 --out $RES --rates $RES/c8/rates/c8_rates.json
$PY -m research.frontier_classical_20261001.decision --res $RES --out $RES/decision_final
```

The C7/C8 oracle phase must write inside the worktree that runs it (D12):
`--out <worktree>/results/frontier_classical_20261001`, then copy the result out. Timing runs
(C2, C5 timing, C6, anchors, C7/C8 timing) need an idle machine. They wait up to 2 hours,
then refuse (D6). Do not run them alongside other jobs, including the author's separate
limitation-program runs.

## Open decisions for the next agent (verdict requested)

The author asked the next agent to give its own verdict on these and will hear it before
deciding.

1. **Novelty checkpoint (plan item L1).** Recommendation: GO_NARROWED. The frontier argument is
   published (Babbush 2021, Hoefler 2023, Chakrabarti 2021, Stamatopoulos–Zeng 2024, Laura et
   al. 2026). The paper survives as a *measured instantiation* for option pricing, under
   narrowings N1–N6 in `literature/L1_PRIOR_ART.md` §5, and possibly with a softer title.
   Accept, reject or re-scope (the plan's fallback contribution)?
2. **Venue (plan item L2).** Recommendation: *Quantum* (needs arXiv quant-ph endorsement;
   fee waivable), fallback *Quantum Information Processing*. `L2_VENUES.md` §3 notes that the
   recommendation predates GO_NARROWED, and that a computational-finance or benchmark venue may
   fit the narrowed claims at least as well.
3. **The author's limitation program** (separate, uncommitted at merge:
   `docs|research|results/limitation_*_20261001/`, new modules and an edit to
   `research/controlled_source_completion/primitives.py`). Its compact sources report lower
   compiled depth (787,566 and 820,268 clean T-depth) than the favourable leaf-table score.
   Decide whether they enter the claim C4 table as a labelled fourth depth row (deviation
   needed), and make sure the `primitives.py` edit (it changes the default lookup lowering)
   does not land before C7/C8 depth (b) finish, or that it lands as a new labelled row.

Pending author actions regardless of the verdict: check arXiv endorsement; personal
verification (`AUTHOR_VERIFICATION.md`, to be created in Week 3); a named human expert review
before any submission.
