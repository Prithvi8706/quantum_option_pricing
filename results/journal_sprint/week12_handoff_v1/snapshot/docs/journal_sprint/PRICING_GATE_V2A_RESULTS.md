# V2A results: actual-contract deterministic feasibility

Follow-up: [V2B tightens the grid bound on the unchanged matrix](PRICING_GATE_V2B_RESULTS.md).
The V2A results below remain the preserved baseline.

Continuation of the first sprint. Executed the prospectively recorded
[V2A protocol](PROTOCOL_V2A.md), with 6 discovery contracts, 4 grid sizes and
3 payoff scales: **72 configurations**. No stochastic campaign or hardware run.

## Result

All 72 configurations pass the diagnostic checks for the separate support, grid
and encoding bounds and the signed error identity. The price transformation also
matches the existing implementation. Actual ideal pricing-circuit objective
probabilities match independent calculations on all six contracts at n=3,c=.25.

Only **4/72** configurations have a positive statistical error allowance within
$1, all on E001. Only **2/72** do so within 1% of spot, again on E001. These counts
are deterministic feasibility, not completed statistical price certificates.

| Contract | Smallest total bound ($) | Support component | Grid component | Encoding component |
|---|---:|---:|---:|---:|
| E001 | 0.461899 | 0.000173 | 0.426482 | 0.035244 |
| E014 | 1.934951 | 0.001873 | 1.542643 | 0.390435 |
| E025 | 1.387075 | 0.001339 | 1.105163 | 0.280573 |
| E030 | 6.390650 | 0.006983 | 4.943552 | 1.440115 |
| E038 | 5.420240 | 0.006059 | 4.159024 | 1.255157 |
| E049 | 2.508483 | 0.002770 | 1.925847 | 0.579866 |

Each minimum occurs at n=6,c=.125 within this fixed matrix. That is a discovery
observation, not a general optimality claim. No bound was fitted to observed
pricing errors. See the [derivation](PRICING_BOUND_DERIVATION.md) for assumptions
and the distinction between bound inputs and diagnostic exact answers.

## What this changes

The statistical prototype alone is not sufficient for the intended paper. The
simple grid bound dominates and leaves no statistical budget for five of six
contracts at these tolerances. Increasing shots cannot reduce these deterministic
terms. Yet failure of a conservative bound does not imply that the actual error
is large: the bound may be loose.

Next work should therefore assess a tighter analytically justified grid bound,
then compare it against explicitly versioned alternative representations. Do not
silently replace point-density weights with integrated masses: that changes the
circuit target and requires new circuit and baseline validation. Any larger n/c
matrix must be a new recorded experiment, not an extension hidden inside V2A.
Only after this gate is useful should a truth-blind resource controller and fresh
finite-shot validation be tested on actual price tolerances.

The supporting bound uses lognormal CDF/tail evaluations and O(2^n) grid work.
Those costs must enter eventual comparisons. European closed-form pricing remains
a correctness reference, not a credible practical quantum-advantage target.

## Verification and retained failure

The initial full runner failed on serialization of a NumPy boolean. Its partial
output and source snapshot remain in `results/journal_sprint/pricing_gate_v2a/`
with `FAILURE.md` and no completion marker. After an explicit native-bool fix,
the **same scientific configuration** completed in
`results/journal_sprint/pricing_gate_v2a_retry1/`. No failed attempt was erased.
A new end-to-end runner regression covers this bug.

Tests comprise the original 32 sprint cases plus 14 new cases for mathematical
bounds, affine conversion, six actual ideal pricing circuits, invalid inputs and
runner serialization. The extended sprint suite passes **46 tests**, with nine
legacy Qiskit warnings. The earlier full-repository 196-test result belongs to the
preceding sprint; it is not represented as a rerun of the extended repository.
New test evidence is saved separately in `results/journal_sprint/tests_v2a_final.xml`.

Successful run artifacts include every row, bound components, diagnostic exact
prices, feasibility allowances, configuration, relevant source/protocol copies,
and completion hashes. No pre-existing Paper A code or original scientific
outputs were changed.

To repeat without overwriting evidence:

```powershell
.\venv\Scripts\python.exe -m pytest research/journal_sprint/tests -q
.\venv\Scripts\python.exe -m research.journal_sprint.run_pricing_gate --output results/journal_sprint/pricing_gate_independent_rerun
```
