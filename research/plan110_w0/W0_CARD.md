# W0 authorization card (plan110)

Authorized by the user on 11 October 2026 ("proceed with first wave"). The plan is docs/program_plan_20261010/PLAN_110_EFFICIENT.md.

## Contract conventions

The user fixed these in chat on 11 October 2026; where the user deferred, the orchestrator fixed the value. The primary value is used for DP1. Every other value is reported as a sensitivity column.

| Convention | Primary | Sensitivity columns |
|---|---|---|
| Parallelism matching | One quantum machine against one 16-core classical machine. The quantum machine may run parallel lanes only inside budget W | 1 lane vs 1 core (H16 grid); L lanes vs 16 cores |
| Classical confidence | Practice confidence intervals, as Stage C does them (chosen by the user) | Distribution-free 99%, symmetric with the quantum worst-case guarantee (C09 b) |
| Width budget W | 1e7 logical data qubits per quantum machine (oracle plus all lanes) | 1e6, 1e8 |
| Magic-state supply | 1e12 accepted T states/s, equal to 1e5 factories at one state per 100 ns | 1e11, 1e13 |
| Logical layer time | 100 ns | 10 ns, 1 us, 10 us |
| Statistical split | e = 0.45 eps (retained C05) | e = eps (zero deterministic bias) |
| Negative-result wording | "No design with certified constants reaches 10x" (achievability, not a query-lower-bound impossibility) | n/a |
| B8x52 at $0.001 | Eligible at zero deterministic bias (quantum-favourable) | Also reported as ineligible under the current $0.00124 bound |

**IBM cloud hardware.** It is not used. It cannot execute even one oracle call: about 4e9 T gates on error-corrected logical qubits. Because of that, it cannot inform the latency inequality. The program stays local, as its plan requires.

## Workstreams and limits

- **Rigour:** R0 screen for every workstream. The procedure is spec, then script, then JSON with input SHA256s and measured/modelled/assumed labels, then one self-check.
- **Writes:** only to `research/plan110_w0/` and `results/plan110_w0/`. Never to `.context/`, `results/limitation_program_20261001/`, `docs/limitation_program_20261001/`, `docs/limitation_audit_20261001/`, `progress.json` or `primitives.py`. No git operations. No SCI or ROOT lifecycle.
- **Interpreter:** any script whose numbers enter the decision table runs under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4). The C2 harness imports numpy and scipy, so the classical timing grid uses the Stage C environment that harness was built for.
- **Concurrency:** at most 3 agents at once. Each appends one JSON row per sub-result.
- **Token cap:** about 1.5M.
- **CPU:** the H16 1-16 worker classical grid runs only on an idle machine, after the agents finish (the C2 harness has a strict idle gate).
- **Early stop:** if k_lat times the coarse floor exceeds 30 times the 10x threshold under every convention, stop W0 and write the DP1 memo.
