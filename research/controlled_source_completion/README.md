# Controlled compound source completion

This is the same parity-controlled compound Asian-basket investigation, carried
through emitted reversible arithmetic, an explicit mean-estimation schedule,
independent validation and a cost/precision audit. It does not demonstrate
quantum advantage. See
[RESULTS.md](../../docs/controlled_source_completion/RESULTS.md),
[DERIVATION.md](../../docs/controlled_source_completion/DERIVATION.md) and
[CHECKLIST.md](../../docs/controlled_source_completion/CHECKLIST.md).

Run from the repository root, using the existing environment:

```powershell
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.run diagnose --samples 64
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.run compile
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.validate
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.optimize
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.validate --revision v2
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.phase_precision
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.phase_certificate
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.spectral_validation
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.cost --revision v2 --phase-fraction 64
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.fusion_validation
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.cost --revision v2 --phase-fraction 64 --fused
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.audit
.context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_source_completion/test_completion.py research/controlled_residual_feasibility research/compound_feasibility -q
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.final_checks
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.report
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_source_completion.archive
```

Compilation uses a cache of emitted `.npy` gate libraries. To reproduce fresh
artifacts without touching the archived evidence, copy this project to an
isolated checkout or change `run.ROOT`. The code is Python 3.9 compatible; the
recorded environment includes NumPy 1.26.4, SciPy 1.13.1, Numba 0.60.0,
Qiskit 0.45.3, mpmath and pytest. No quantum service or GPU is required.

The financial graphs are hierarchical, not flattened multibillion-gate files.
`source.json` supplies the register bindings, copy/forward/inverse schedule,
leaf-library path and resource counts. Each leaf has an actual X/CX/CCX gate
array and hash. `compiler.execute` executes those gates on a supplied basis
input, including the hierarchy's cleanup. The final estimator envelope records
integer QPE powers/repetitions, adaptive decoding, signed phase and reflection
conventions. Arbitrary rotations are specified symbolically and remain
unsynthesized; the entire pricing QPE has not been executed.

Version 1 is the initial compiler. Version 2 performs bit-exact constant folding
and common-expression reuse. The separate 64-bit phase circuit was an explicit
development response to a failed precision budget, not a held-out confirmation.
Numerical diagnostics compare the integer financial program with an independent
NumPy/SciPy implementation on identical finite inputs. Simulator CPU seconds
are never used as quantum runtime. Existing policy fits and classical timing
records are consumed read-only, and the manuscript is unchanged.
