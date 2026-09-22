# Controlled-residual compound-pricing follow-up

[Findings](../../docs/controlled_residual_feasibility/RESULTS.md),
[derivation](../../docs/controlled_residual_feasibility/DERIVATION.md),
[protocol](../../docs/controlled_residual_feasibility/PROTOCOL.md),
[parity extension](../../docs/controlled_residual_feasibility/PARITY_EXTENSION.md),
[primary sources](../../docs/controlled_residual_feasibility/SOURCES.md).

Run from the repository root with the existing isolated environment:

```powershell
$pricingPython = '.context/antithetic_feasibility_env/Scripts/python.exe'
& $pricingPython -m research.controlled_residual_feasibility.acquire --out results/controlled_residual_feasibility/pilot_v1
& $pricingPython -m research.controlled_residual_feasibility.acquire --mode classical --out results/controlled_residual_feasibility/classical_v1
& $pricingPython -m research.controlled_residual_feasibility.parity_acquire --out results/controlled_residual_feasibility/parity_pilot_v1
& $pricingPython -m research.controlled_residual_feasibility.parity_acquire --mode classical --out results/controlled_residual_feasibility/parity_classical_v1
& $pricingPython -m research.controlled_residual_feasibility.parity_iid --out results/controlled_residual_feasibility/parity_iid_v1
& $pricingPython -m research.controlled_residual_feasibility.cost --out results/controlled_residual_feasibility/cost_v1
& $pricingPython -m research.controlled_residual_feasibility.cold_timing
& $pricingPython -m research.controlled_residual_feasibility.summarize
& $pricingPython -m research.controlled_residual_feasibility.validate
```

Directories refuse overwrite. Use new output names for reruns; `cost`,
`summarize`, `cold_timing` and `validate` have explicit versioned dependencies
or destinations to update when running a new acquisition. Run cold timings
sequentially with other numerical work finished. Pytest can run independently:

```powershell
& $pricingPython -m pytest research/controlled_residual_feasibility research/compound_feasibility research/antithetic_feasibility -q
```

| Module | Purpose |
|---|---|
| `bounds.py` | Conditional/global lognormal spread moments, continuation interval, flat residual and regret bounds |
| `acquire.py` | First control pilot and classical comparison; original capped-contract bridge retained |
| `parity.py` | Uncapped-price put-complement residual, analytic moments, shared/disjoint conditional sample kernels |
| `parity_acquire.py` | Independent parity pilot and whole-price RQMC brackets |
| `parity_iid.py` | Fixed-N statistical moment/regret/flat-mean bounds, with explicit preprocessing costs |
| `cost.py` | Actual signed estimator schedule, component-derived arithmetic subtotal, ideal sensitivity and unresolved error contract |
| `cold_timing.py` | Fresh process, cache and training for C4/H8 representative full pricing |
| `summarize.py` | Reference reconciliation, crossover budgets and standalone PNG/PDF moment chart |
| `validate.py` | Regression tests and source/artifact hash receipt |

Reuse is explicit: model, Brownian bridge/PCA and training from
`research/compound_feasibility`; signed-QAE scheduling and emitted arithmetic
records from `research/antithetic_feasibility` and its results. Prior evidence
and manuscripts are not modified. No simulator time is called quantum time.

Seed roots:2026092501 first pilot,2026092502 first classical comparison,
2026092503 parity pilot,2026092504 parity comparison,2026092505 fixed iid,
2026092506 cold pricing. Policy training is independent and reused from its
archived2026092402 root, with its cost charged; cold runs retrain it.

The statistical certificate requires ideal iid sampling and real evaluation.
The quantum finance circuit and physical layout are incomplete. Read the
error/access assumptions before using any resource number as a projection.
