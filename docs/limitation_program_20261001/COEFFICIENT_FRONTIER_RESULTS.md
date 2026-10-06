# Exact top-three coefficient frontier: local result

The `min-depth` portfolio is adopted as `A10_coefficient_run001`, extending the accepted `A09_range_run001` source. All 119 exact leaf tests, 72 integration tests and four complete financial gate replays passed; independent audit `A01_run014` confirmed the decision. The financial target bytes, external law and native 72/40 arithmetic are unchanged. This is a bounded A10 component; other coefficients, squares and financial sources retain their own unresolved scopes.

| Case | Previous T-depth | Accepted T-depth | T-depth reduction | Accepted T gates | T-work reduction | Actual logical qubits |
|---|---:|---:|---:|---:|---:|---:|
| B4x12 | 719,916 | 555,774 | 22.8002% | 520,720,662 | 0.116903% | 550,141 |
| B8x52 | 743,064 | 663,704 | 10.6801% | 4,267,435,214 | 0.001627% | 4,460,479 |

Accepted Clifford+T depths are 1,661,253 /2,026,465, below 2,154,117 /2,264,545. Actual qubit counts and caps remain 550,141 /4,460,479. The main gain is scheduled depth; T work changes only slightly. Costs use the existing exact seven-T Toffoli/all-to-all model and do not establish elapsed physical runtime.

## Bounded scope and exact behavior

The prospective inventory ranks coefficients by combined deterministic depth ownership across both cases. Its fixed top three are 1067016148260,60222732077 and22906492245. Hypothetical fixed-batch zero-cost ceilings pass the pre-existing0.1% attribution cutoff, but were only screening diagnostics. The actual matched baseline leaves still use original ripple shift-add gates with 433 qubits; earlier ln(2)/inverse-ln(2) screens did not cover these coefficients.

Each coefficient received four existing exact strategies and two new CSA/prefix variants: binary shift-add, signed-digit shift-add, binary CSA, signed-digit CSA, binary CSA with Brent-Kung final sum, and signed-digit CSA with Brent-Kung final sum. This is18 standalone candidates, with no additional coefficient or input-width search. Same-coefficient nondominance includes the baseline and all six siblings; strict baseline improvement and T-work or scratch improvement are required before source eligibility. Coefficients implementing different functions are never compared as equivalent leaves.

| Coefficient | Selected strategy | Old leaf T-depth | New T-depth | Old T gates | New T gates | Old qubits | New qubits |
|---|---|---:|---:|---:|---:|---:|---:|
| 1067016148260 | signed-digit-prefix-carry-save | 40,848 | 385 | 71,484 | 36,764 | 433 | 3,656 |
| 60222732077 | binary-prefix-carry-save | 40,976 | 401 | 71,708 | 50,652 | 433 | 5,143 |
| 22906492245 | binary-prefix-carry-save | 36,576 | 385 | 64,008 | 46,676 | 433 | 4,717 |

Every leaf retains one complete native signed input and a complete arbitrary XOR output. Its contract is exactly `zero_low_bits=0`, which imposes no input restriction. The exact coefficient's binary or nonadjacent signed-digit expansion produces the modular product, with full 112-bit complement correction and every low carry column retained. The slice implements `floor(signed(x)*c/2**40) mod2**72`, including negative rounding. The prefix family retains both CSA rows, a separate product and all helpers; full output copy is followed by literal inverse cleanup. Its larger workspace is fully charged.

The coefficient reader and scheduler v7 validate literal coefficient, actual immutable cmul binding, canonical specification/key, strict full-domain contract, family markers and native interface before compact masks. All pre-existing range, root, shift, log and lookup contracts and bytes are preserved. No guard, precision or finance-law change is used to obtain the gain.

The actual scope is 14 changed B4 calls and one changed B8 call: coefficient 1067016148260 appears once in both cases, 60222732077 once in B4, and 22906492245 twelve times in B4. Two coefficients are absent from B8; absence is checked against its actual target rather than assumed. All nonspecialized metadata/gates, including the 32-row lookup, retain exact accepted bytes. SSA widths, masks, offsets, proof reasons and argument/output copy counts remain identical.

## Portfolio selection and verification

Two portfolios were frozen after leaf tests/costs and before source tests/costs. `min-depth` chooses each eligible leaf by T-depth, T count, CT-depth, qubits and declared strategy order. `min-work` chooses by T count, qubits, T-depth, CT-depth and order. Identical maps are deduplicated before emission. Both actual portfolios cleared the unchanged both-case2% T-depth criterion, CT-depth nonincrease, actual qubit caps and leaf work/scratch improvement. Both remain resource-nondominated: `min-work` uses fewer T gates while `min-depth` has less depth. The declared summed-depth/work/qubit selection chose `min-depth`; only it received the four saved financial replays. The alternative remains a measured resource point and is not credited with extra financial replay or adoption.

Leaf tests exhaust small signed inputs, signed/zero coefficients, fractional boundaries, dirty outputs and inverse cleanup, then test all actual coefficients across all six strategies at native24/40/72, extrema/power boundaries and seeded random inputs, including actual archived72-bit controls. Integration tests exercise immutable bindings, typed family/spec/key/contract errors, cache/gate corruption, dirty outputs/aliases and the preserved range/root/shift/lookup guards. The full pricing replays use the frozen three-B4/one-B8 vectors and require exact dirty-output XOR plus restoration of every input/workspace bit.

The first audit, `A01_run013`, failed an obsolete assumption that every global coefficient occurs in both cases. Its failed receipt and original code are preserved. The versioned auditor checks exactly one matching entry when actual case calls exist, exactly zero when absent, the fixed global union and shared coefficient SHA/resources. No source/leaf gate, test, input, selection rule or acceptance threshold changed after the producer freeze.

The successful audit scanned 80 actual arrays, 378 metadata locations and froze 1,221 inputs. It independently parses every actual shift-add, CSA/ripple and CSA/Brent-Kung circuit, exact digits, signed correction, copies and inverse; verifies all 18 sibling decisions and both portfolio maps; reconstructs full source counts, preserved guards, DAG/capped packing and Pareto/tie-break selection; and reconciles all four producer replays. Its algebraic certificate checks 47,874 finite arithmetic cases, including 2,274 tiny negative products, while the identities establish unrestricted signed semantics. The audit adds no gate replay or pytest credit.

This wave adds **191 distinct successful tests and four complete financial replays**, bringing the program to **772 cases and 38 replays**. G2 dollar-error certification, G3 compatible99% estimation, G4 matched classical timing and G5 physical runtime remain open. No quantum advantage is established. All work stayed local; nothing was pushed, uploaded or published.

Receipts: [leaf](../../results/limitation_program_20261001/A10_coefficient_leaf_run001/summary.json), [source](../../results/limitation_program_20261001/A10_coefficient_run001/summary.json), [independent audit](COEFFICIENT_SOURCE_COSTS.md), [wave packet](../../results/limitation_program_20261001/WAVE07_run001/summary.json). Next: [A18 paid checkpointing](NEXT_CHECKPOINTING.md).
