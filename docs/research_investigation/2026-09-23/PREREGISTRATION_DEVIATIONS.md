# H1 falsifier: deviations from the stated protocol

24 September 2026. The protocol was stated in [DECISION.md §6](DECISION.md) ("Research
direction: falsify or promote H1") before the P3/Q1 runs, according to the working record.
It was written after the P1/P2 pilots. It was first committed together with the results
(commit `47706a21`), so the ordering is not externally time-stamped. The executed
falsifier ([H1_FALSIFIER_RESULTS.md](H1_FALSIFIER_RESULTS.md)) was a reduced version.

| # | Stated in §6 | Executed | Likely bias of the deviation | Closed by paper-plan item |
|---|---|---|---|---|
| 1 | Cases 4×12, 8×52, **16×52**; barriers H ∈ {**120**, 140, **160**} | 4×12 and 8×52 at H = 140 only | Unknown (generality untested) | G16 |
| 2 | Compiled classical finalists: first-PC preintegration, **multi-direction numerical smoothing**, **Brownian-bridge-ordered one-step survival**, **barrier importance sampling** | First-PC preintegration only (compiled). One-step survival was run earlier in time-ordered form (P2, numpy) | Favours quantum: classical weaker than planned | G17 |
| 3 | **CuPy/CUDA GPU** versions and a GPU plain-MC throughput anchor | None. The GPU is visible, but no CUDA toolkit library is installed for numba | Favours quantum | G18 |
| 4 | n = 2⁶…2¹⁶, 32 scrambles, **whole-scramble resampling for rate intervals** | n = 2⁸…2¹⁷, 32 scrambles; point-estimate rates, no intervals (per-scramble estimates not archived) | Unknown; understates uncertainty | G2 |
| 5 | Record T_C(ε) at $0.10/$0.03/$0.01/$0.001 | T_C modelled from the fitted rate and measured per-point cost; the first-chunk overhead was spread into the per-point cost (ERRATA E5) | Mostly favours quantum (4×12 T_C inflated about 2.6×) | G3 |
| 6 | **Emit** the knock-out oracle with the compiler; record T-count, T-depth and qubits at **f = 24/32** under serial, wave and reaction-limited models | Built in the IR and **scored** at f = 40 from a per-operation leaf table (cheapest and median), dependency-only; not emitted; no width or schedule (ERRATA E3) | Mixed: the cheapest-leaf rule is optimistic for quantum (0.61× on C4) but undercounts some ops; precision not varied | G1, G6 |
| 7 | Take k from the explicit Hadamard/QAE schedules already certified | k ∈ {1, 3, 10} only | Favours quantum (explicit schedules imply far larger k) | G5 |
| 8 | Evaluate over t ∈ {0.1, 1, 10} µs and k ∈ {3, 10} | Grid covered t ∈ {10 ns, 100 ns, 1 µs, 10 µs} and k ∈ {1, 3, 10}, a superset | Adds quantum-favourable sensitivities | — |
| 9 | σ convention not stated | Decision used the plain knock-out σ (the estimand the oracle computes); the preintegrated σ is reported only as a sensitivity | — (the convention is now fixed) | ERRATA E6 |

The stop rule itself (stop if D_min > 10·D_max($0.001) at t ≥ 100 ns, k ≥ 3 against the
measured best classical method, on every case) was applied as stated, to the executed
cases. Most deviations favour the quantum side, so they would tend to make a STOP harder
to reach, not easier. That argues the STOP is robust, but it does not replace executing
the missing arms. The paper plan either executes each missing arm or reports it as not
done.
