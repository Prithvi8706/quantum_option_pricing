# V2B: tighter bound, unchanged pricing representation

Implemented the [recorded comparison](PROTOCOL_V2B.md) and
[cancellation-aware bound](TIGHTER_GRID_DERIVATION.md). All **72 configurations**
pass the separate grid-error, total-error and non-increase checks. Support,
encoding, affine post-processing, discovery contracts and n/c choices are unchanged.

## Main result

Configurations with a positive statistical allowance within **$1 increase from
4/72 to 14/72**, spanning four of six contracts rather than one. For **1% of spot**,
the count increases from **2/72 to 13/72**. These are sufficient deterministic
feasibility outcomes, not completed finite-shot price certificates.

| Contract | Old smallest bound ($) | New smallest bound ($) | New grid component ($) | Configurations with $1 allowance |
|---|---:|---:|---:|---:|
| E001 | 0.461899 | 0.048755 | 0.013338 | 9 |
| E014 | 1.934951 | 0.501995 | 0.109686 | 2 |
| E025 | 1.387075 | 0.359078 | 0.077166 | 2 |
| E030 | 6.390650 | 2.399314 | 0.952217 | 0 |
| E038 | 5.420240 | 1.931005 | 0.669789 | 0 |
| E049 | 2.508483 | 0.732712 | 0.150076 | 1 |

All displayed minima occur at n=6,c=.125 within this matrix. They are not general
optimality claims. The new bound exploits cancellation in nearest-cell rounding,
with explicit density-derivative remainder bounds and kink/endpoint treatment.
It does not change the circuit target or use exact prices to select allowances.

## Remaining limit

E030 and E038 have encoding bounds of approximately $1.440115 and $1.255157 at
the smallest tested c=.125. Even eliminating their grid bounds would not open a
$1 budget under this certificate. These are worst-case encoding bounds; this is
not a claim of a universal accuracy floor or an impossibility result.

The next useful work has two separate purposes:

1. Test finite-shot dollar intervals on the now-feasible configurations, using a
   new frozen protocol, strong fixed baselines and honest preprocessing costs.
2. For the two unresolved contracts, investigate a justified sharper encoding
   bound or a prospectively versioned scale/representation change. Smaller c
   amplifies probability-to-price sensitivity and is not a free improvement.

Do not enlarge this completed matrix after seeing its outcome. The remaining
classical baseline reconstruction, modern AE comparisons, noise calibration and
independent contributor review are still required for the intended journal paper.

## Evidence

The extended sprint suite passes **59 tests** with nine legacy Qiskit warnings
(15.24 seconds). Machine-readable evidence is `results/journal_sprint/tests_v2b.xml`.
Lint and formatting checks pass, and all 24 completed-run artifact hashes were
verified. The full legacy repository suite was not rerun in this step.

Successful outputs are in `results/journal_sprint/pricing_gate_v2b/`, including all
rows, old/new bounds, remaining probability budgets, derivative-remainder details,
archived diagnostic comparisons, source/protocol snapshots and completion hashes.
The runner checks the V2A baseline hashes before using its diagnostic records.

New tests cover derivative envelopes, every discovery contract's grid bound,
runner serialization and combined dollar-interval conversion. The latter use
constructed probability intervals containing the exact amplitude: they validate
the conversion, not a newly observed finite-shot coverage rate. Existing ideal
pricing-circuit tests remain in the sprint suite; no hardware or noisy-circuit
claim is added. The original V2A failed attempt and successful retry remain intact.

To reproduce in a fresh output directory:

```powershell
.\venv\Scripts\python.exe -m pytest research/journal_sprint/tests -q
.\venv\Scripts\python.exe -m research.journal_sprint.run_tighter_gate --output results/journal_sprint/pricing_gate_v2b_independent
```
