# Reproduce the antithetic feasibility screen

Decision and qualifications: [RESULTS.md](../../docs/antithetic_feasibility/RESULTS.md).
Protocol: [PROTOCOL.md](../../docs/antithetic_feasibility/PROTOCOL.md).

Run from the repository root in PowerShell. The isolated environment is
`.context/antithetic_feasibility_env`, created with Python 3.9 and inherited
system packages; only numba 0.60.0 / llvmlite 0.43.0 were installed there.
Recorded dependencies also include numpy 1.26.4, scipy 1.13.1, qiskit, pytest,
psutil and matplotlib. Final validation records exact installed versions.
This code imports the repository's existing reversible arithmetic module.

Each acquisition refuses to overwrite an existing output directory. To rerun,
choose a fresh path. Scripts deriving results use the named v1 input archives;
change their ROOT/input paths explicitly if performing a new scientific run.
`audit_bins`, `summarize`, `cold_timing`, and `validate` use fixed new-output
names and must not be rerun over completed output. No script changes manuscript
claims or confirmation cases.

```powershell
$pricingPython = '.context/antithetic_feasibility_env/Scripts/python.exe'
& $pricingPython -m pytest research/antithetic_feasibility -q

# Base/single-level method menu.
& $pricingPython -m research.antithetic_feasibility.acquire --out results/antithetic_feasibility/classical_prices_v1 --cases A1,A4 --levels 0,2,4 --powers 8,10,12 --replicates 16
# Benign and stress antithetic corrections.
& $pricingPython -m research.antithetic_feasibility.acquire --out results/antithetic_feasibility/classical_corrections_v1 --cases A1,A4 --levels 1,2,3,4,5 --powers 8,10 --replicates 16 --corrections
& $pricingPython -m research.antithetic_feasibility.acquire --out results/antithetic_feasibility/stress_corrections_v1 --cases S4,B8 --levels 1,2,3,4,5 --powers 8 --replicates 16 --corrections

# Frozen allocations, then development hybrid.
& $pricingPython -m research.antithetic_feasibility.multilevel --out results/antithetic_feasibility/multilevel_v1
& $pricingPython -m research.antithetic_feasibility.hybrid_classical --out results/antithetic_feasibility/hybrid_classical_v1
# A repeat uses the same seeds and adds no independent accuracy evidence.
& $pricingPython -m research.antithetic_feasibility.hybrid_classical --out results/antithetic_feasibility/hybrid_timing_repeat_v1
& $pricingPython -m research.antithetic_feasibility.cold_timing

# Independent scheme, finite-input, arithmetic, and bounded-sampling checks.
& $pricingPython -m research.antithetic_feasibility.reference --out results/antithetic_feasibility/reference_euler_v1
& $pricingPython -m research.antithetic_feasibility.hierarchy --out results/antithetic_feasibility/finite_input_v1
& $pricingPython -m research.antithetic_feasibility.fixed_point --out results/antithetic_feasibility/arithmetic_diagnostic_v1
& $pricingPython -m research.antithetic_feasibility.fixed_corrections --out results/antithetic_feasibility/fixed_corrections_v1
& $pricingPython -m research.antithetic_feasibility.bounded_classical --out results/antithetic_feasibility/bounded_classical_v1

# Actual emitted blocks and specified macro/estimation schedules.
& $pricingPython -m research.antithetic_feasibility.compile_blocks --out results/antithetic_feasibility/compiled_blocks_v1
& $pricingPython -m research.antithetic_feasibility.cost_model --out results/antithetic_feasibility/complete_cost_screen_v1
& $pricingPython -m research.antithetic_feasibility.audit_bins
& $pricingPython -m research.antithetic_feasibility.sensitivity --out results/antithetic_feasibility/hierarchy_sensitivity_v1
& $pricingPython -m research.antithetic_feasibility.summarize
& $pricingPython -m research.antithetic_feasibility.validate
```

For a quick verification, run tests and inspect existing JSON. Rebuilding the
complete acquisition takes longer, especially arithmetic compilation and native
kernel warmup. No quantum device or GPU is used. Gate streams and classical
simulations do not constitute quantum hardware execution.

## Artifact map

| Directory under `results/antithetic_feasibility` | Contents |
|---|---|
| `classical_prices_v1`, `classical_corrections_v1`, `stress_corrections_v1` | Raw replicate rows, summaries, environment/source manifest, timing/memory receipts |
| `multilevel_v1` | Frozen predicted allocations and all fresh outcomes, including missed targets |
| `hybrid_classical_v1` | Frozen hybrid powers, 32-replicate prices, per-level timings |
| `hybrid_timing_repeat_v1`, `cold_classical_v1` | Same-seed reproducibility and timing, including full cold subprocess latency |
| `reference_euler_v1` | Independent discretization, uncertainty and training times |
| `bounded_classical_v1` | Capped payoff empirical-Bernstein sampling check |
| `finite_input_v1` | Paired finite Gaussian vs continuous Gaussian diagnostics |
| `arithmetic_diagnostic_v1`, `fixed_corrections_v1` | Independent integer reference and paired arithmetic errors |
| `compiled_blocks_v1` | Real block resources, exact decomposition, input/output registers, production step gate binaries, loader compilation |
| `complete_cost_screen_v1` | Macro operation ledger, every QAE bin/M/repetition, logical/physical sensitivity and unresolved assumptions |
| `bin_audit_v1` | All 104 actual scheduled bin circuits and normalization widths |
| `hierarchy_sensitivity_v1` | Shorter hierarchies, ideal square-root-only screen and break-even thresholds |
| `decision_summary_v1` | Descriptive variance fits; PNG and PDF scientific plots |
| `source_snapshot_v1` | Earlier source checkpoint, not the final full package |
| `final_validation_v1` | Final test output, version/hash manifest and final source snapshot |

Classical price intervals are empirical unless the bounded-sampling result is
explicitly specified. No result here is a certified continuous-model price
comparison, a hardware advantage, or a lower bound on all quantum algorithms.
