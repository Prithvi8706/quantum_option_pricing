# Compound Asian-basket feasibility experiment

Read [the findings](../../docs/compound_feasibility/RESULTS.md) and
[frozen protocol](../../docs/compound_feasibility/PROTOCOL.md).

Run from repository root using the existing isolated environment:

```powershell
$pricingPython = '.context/antithetic_feasibility_env/Scripts/python.exe'
& $pricingPython -m pytest research/compound_feasibility -q
& $pricingPython -m research.compound_feasibility.acquire --out results/compound_feasibility/pilot_v1
& $pricingPython -m research.compound_feasibility.acquire --out results/compound_feasibility/scaling_v1 --outer 13 --inner 8,10 --replicates 32 --training results/compound_feasibility/pilot_v1/training.json --root 2026092405
& $pricingPython -m research.compound_feasibility.multilevel --out results/compound_feasibility/multilevel_v1
& $pricingPython -m research.compound_feasibility.streaming --out results/compound_feasibility/reference_stream_v1
& $pricingPython -m research.compound_feasibility.streaming --out results/compound_feasibility/reference_refine_v1 --cases H4,H8 --outer 15 --inner 12 --replicates 32 --root 2026092414
& $pricingPython -m research.compound_feasibility.combine_reference
& $pricingPython -m research.compound_feasibility.bounded_iid --out results/compound_feasibility/bounded_iid_v1
& $pricingPython -m research.compound_feasibility.compile --out results/compound_feasibility/compiled_v1
& $pricingPython -m research.compound_feasibility.cost --out results/compound_feasibility/cost_v3
& $pricingPython -m research.compound_feasibility.precision --out results/compound_feasibility/precision_v1
& $pricingPython -m research.compound_feasibility.cold_timing
& $pricingPython -m research.compound_feasibility.summarize
& $pricingPython -m research.compound_feasibility.validate
```

All output directories refuse overwrite. Choose fresh paths to rerun. Some
derivation scripts refer to v1/v3 input archives explicitly; update those paths
when creating a fresh acquisition. `cold_timing`, `combine_reference`,
`summarize` and `validate` have fixed append-only output names.

Dependencies: Python3.9, numpy, scipy, numba, matplotlib, pytest and the existing
repository reversible arithmetic. Versions and source hashes are in final
validation. Exponential/multiply resource records and Gaussian loader counts
are reused from `results/antithetic_feasibility/compiled_blocks_v1`; those are
actual emitted blocks, not hardware timings. No quantum device or GPU was used.

## Code and outputs

| Module | Function / artifact |
|---|---|
| `model.py` | Exact-date GBM, factorized future returns, geometric control, analytic tail/moment bounds, policy features |
| `acquire.py` | Independently trained policy, crossed RQMC lower/Jensen upper bounds, raw replicate diagnostics |
| `streaming.py` | Algebraically identical estimator without N-by-M temporary arrays; independent reference and timing runs |
| `multilevel.py` | Executed antithetic nested MLRQMC with frozen allocation |
| `bounded_iid.py` | 4,194,304 independent outer states, 16 independent inner paths per state, empirical-Bernstein endpoints |
| `combine_reference.py` | Equal-weight combination of independent reference groups; empirical Welch endpoint intervals |
| `quantum_schedule.py` | Explicit quantum-inner hierarchy, coherent repetition requirements, signed outer schedule, exact toy spectral checks |
| `reversible.py`, `compile.py` | Real clean GBM step and capped payoff gate streams, including cleanup |
| `cost.py` | Macro arithmetic subtotal, all source/inverse calls, normalization sensitivity, ideal coordinates and physical limitations |
| `precision.py` | Paired finite-input and integer-payoff diagnostics, not uniform error certificates |
| `cold_timing.py` | Fresh process and native compilation cache; independent policy training charged |
| `summarize.py` | Crossover budgets, all reference prices, PNG/PDF plots |
| `validate.py` | Executed test receipt and final source/artifact hashes |

`reference_v1` is a deliberately stopped, memory-heavy implementation. Its 80
partial rows are preserved and excluded from combined evidence because
`reference_stream_v1` repeats those seeds. `cost_v1` and `cost_v2` are earlier
screens retained for provenance. `cost_v3` is authoritative: it weights each
fixing before accumulation and uses the improved analytic outer moment bound.
The query count comparison is not a proof that the best possible quantum
algorithm loses. No hidden held-out cases were opened.
