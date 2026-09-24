# Advantage-frontier pilots (23 September 2026)

Development diagnostics for [the decision report](../../docs/research_investigation/2026-09-23/DECISION.md).
None of these runs is held-out confirmation, a certified price, or a quantum execution.

| Script | What it measures | Output in `results/advantage_frontier_20260923/` |
|---|---|---|
| `classical_exponent_pilot.py` | P1: RQMC error-vs-work exponents for 4x12 and 8x52 GBM basket call, digital and knock-out payoffs; plain, geometric control, first-principal-direction preintegration; implied quantum per-call budgets | `classical_exponent_pilot.json`, `.log` |
| `barrier_oss_pilot.py` | P2: one-step-survival conditioning (Glasserman-Staum, basket version) for the knock-out | `barrier_oss_pilot.json`, `.log` |
| `frontier.py` | D_max(eps) for the strongest measured barrier method, with classical speed-up g, estimator constant k and logical T-layer time; precision needed to fit a given oracle depth | `frontier.json` |

H1 falsifier ([results](../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md)):

| Script | What it measures | Output |
|---|---|---|
| `barrier_fast_classical.py` | P3: compiled (numba) 16-process version of the strongest knock-out method, rate to 2^17 and wall time | `barrier_fast_classical.json`, `.log` |
| `barrier_oracle_depth.py` | Q1: depth-optimized knock-out oracle in the project IR, scored (not emitted) by critical path with cheapest/median certified-leaf costs per operation type; optimistic, see ERRATA E3 | `barrier_oracle_depth.json` |
| `barrier_decision.py` | Stop/continue rule and full (eps, k, t_layer) grid | `barrier_decision.json` |
| `provenance_replay_diff.py` | Field-by-field diff of the archive against a replay of the committed scripts | `provenance_replay_20260924.json` |

P3 needs numba (anaconda python was used); Q1 needs the project's numba env
(`.context/antithetic_feasibility_env`); the decision script runs in `venv`.

Run the P1/P2/frontier scripts from the repository root with the project environment:

    venv/Scripts/python.exe research/advantage_frontier_20260923/classical_exponent_pilot.py
    venv/Scripts/python.exe research/advantage_frontier_20260923/barrier_oss_pilot.py
    venv/Scripts/python.exe research/advantage_frontier_20260923/frontier.py

P1 takes about 7 minutes and P2 about 3 minutes, single-threaded (BLAS threads pinned to 1).
Seeds are fixed development roots (2026092231, 2026092232); prices reproduce exactly and
timings vary by machine. The archived JSON/log files came from runs of these scripts before
their output paths were redirected into `results/` and line-wrapped for lint; the numerical
code is unchanged. Timings are single-thread numpy, a deliberately weak classical
implementation that favours the quantum side of every budget.
