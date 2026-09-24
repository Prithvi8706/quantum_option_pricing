# Provenance replay of the advantage-frontier pilots

24 September 2026. This responds to plan-review finding C14. The archived P1, P2 and P3
outputs were produced by pre-lint script versions writing to a session scratchpad, not by
the committed scripts.

**What was run.**
- *Checkout:* a detached checkout of commit `47706a21` at
  `.context/advantage_frontier_replay` (gitignored, per the repository's replay
  precedent).
- *Scripts:* every committed script, run in sequence from that checkout: P3
  `barrier_fast_classical.py`, P1 `classical_exponent_pilot.py`, P2 `barrier_oss_pilot.py`,
  Q1 `barrier_oracle_depth.py`, `barrier_decision.py` and `frontier.py`.
- *Interpreters:* the same three as the original runs:
  - `venv` (Python 3.9.13, numpy 2.0.2) for P1, P2, the decision and the frontier;
  - anaconda (Python 3.12.7, numba 0.60.0, numpy 1.26.4) for P3;
  - `.context/antithetic_feasibility_env` (numba 0.60.0) for Q1.
- *Comparison:*
  [`provenance_replay_diff.py`](../../../research/advantage_frontier_20260923/provenance_replay_diff.py)
  compared every JSON field recursively. Fields named for wall-clock timing, or derived
  from it (classical seconds, D_max, ratios, stop margins, environment strings), were
  classed as re-measurement fields. Everything else had to match exactly.

**Result.**
[`provenance_replay_20260924.json`](../../../results/advantage_frontier_20260923/provenance_replay_20260924.json):

| Archived output | Exact fields compared | Mismatches | Timing-derived fields (changed) |
|---|---:|---:|---:|
| classical_exponent_pilot.json | 1,611 | **0** | 1,214 (1,194) |
| barrier_oss_pilot.json | 108 | **0** | 10 (4) |
| barrier_fast_classical.json | 57 | **0** | 33 (24) |
| barrier_oracle_depth.json | 209 | **0** | 17 (0) |
| barrier_decision.json | 2,112 | **0** | 592 (584) |
| frontier.json | 270 | **0** | 162 (146) |

All prices, standard errors, RQMC rates, fit constants, pointwise standard deviations,
oracle depths and T-counts, and every non-timing field of the decision grid reproduce
exactly from the committed scripts. The committed scripts are therefore numerically
equivalent to the versions that produced the archive.

**Timing changed, as ERRATA E5 predicted.** With the numba cache already warm, the 4×12
scramble to 2¹⁷ points took 2.9 s (archived 7.7 s), and 8×52 took 22.4 s (archived 28.4 s).
The replayed decision is **STOP H1 again**:

| Case | Replayed modelled classical time to $0.001 | D_max | Oracle / D_max, Box–Muller (archived) |
|---|---:|---:|---:|
| 4×12 | 2.2 s | 58 | 15,269× (5,765×) |
| 8×52 | 21.4 s | 623 | 1,443× (1,138×) |

The archived decision values are kept unchanged as the historical record. The replay's
outputs remain only in the gitignored checkout; the diff report is the committed
evidence. Timing fields are re-measurements on the same laptop, not a controlled timing
study. That study is plan item C2.
