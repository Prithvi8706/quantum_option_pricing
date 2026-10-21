# Exact signed range multiplication: local result

The `mixed24-40` portfolio is adopted as `A09_range_run001`, following 45 exact leaf tests, 68 integration tests, four complete financial gate replays and independent audit `A01_run012`. The preceding accepted source was `A11_nonrestoring_run001`. The financial function, target bytes, 72/40 precision and external input law are unchanged. This completes a bounded exact operand-range component of A09; it does not close the entire limitation or establish quantum advantage.

| Case | Previous T gates | Accepted T gates | T-work reduction | Previous T-depth | Accepted T-depth | T-depth reduction | Actual logical qubits |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B4x12 | 619,528,126 | 521,330,110 | 15.8505% | 787,566 | 719,916 | 8.5898% | 550,141 |
| B8x52 | 5,095,520,430 | 4,267,504,654 | 16.2499% | 820,268 | 743,064 | 9.4120% | 4,460,479 |

Accepted Clifford+T depths are 2,154,117 / 2,264,545, below the preceding 2,342,011 / 2,472,617. Actual qubits are 550,141 / 4,460,479, within the preceding caps of 550,141 / 4,460,481. The two-qubit B8 difference comes from the charged packed scratch allocation; SSA retained storage, masks, proof reasons and native argument/output copy counts are identical. These are exact seven-T Toffoli, all-to-all scheduling-model costs; routing, factories, error correction and elapsed physical runtime remain unproved.

## What changed and why it is exact

Both native multiplier arguments and the arbitrary XOR output remain 72 bits. At each actual SSA call, complete signed intervals prove that both inputs are sign extensions of their selected active words. The declared bins are 24, 40 and 72; a positive value whose top unsigned bit is one can require an extra signed bit. Neither sampled magnitudes nor a value that requires signed41 is accepted as signed40.

The kernel constructs the signed partial plane using the active sign bits. Exactly-one-sign terms have negative weight; complementary partials plus their fixed negative-weight correction represent the product modulo the full 112-bit word. This full modulus also handles negative products shorter than the output slice. All product columns below bit40 remain in the CSA and final prefix carry computation. Thus the copied slice equals `floor(signed(a)*signed(b)/2**40) mod2**72`, including tiny negative products that floor to -1. The leaf copies into the full dirty output and literally reverses its complete computation, restoring both inputs and all scratch.

| Selected ordered active bits | B4x12 calls | B8x52 calls |
|---|---:|---:|
| 24 by 72 | 190 | 1,662 |
| 40 by 72 | 238 | 2,078 |
| 40 by 40 | 7 | 7 |
| 72 by 24 | 2 | 2 |
| 72 by 40 | 90 | 702 |
| Total changed calls | 527 | 4,451 |

The remaining 913 / 7,405 multiplications retain the archived generic leaf. All accepted non-restoring roots, signed7 shifts, log constants, coefficient lookup rows and other nonspecialized metadata/gate bytes are preserved. No new external input restriction or same-SSA-only square dispatch is introduced.

The prospective leaf screen emitted the eight non72-by-72 ordered pairs. All passed the matched nondominance and T-work/scratch criteria. For orientation, 24-by-72 uses 82,768 T gates and 6,066 qubits; 40-by-72 uses 130,704 and 9,474; the generic native multiplier uses 205,716 and 14,861. Whole-source costs, rather than these leaf ratios, determine adoption.

## Bounded screen and evidence

One exact CSA/Brent-Kung family and three active widths were frozen before tests and resource screens. Two source portfolios were frozen: `mixed40` and `mixed24-40`. Both cleared the preset 2% full capped T-depth criterion in both cases, with no CT-depth increase and with work/scratch improvements. `mixed24-40` dominated `mixed40` across all four complete-source dimensions in both cases and won the declared depth/work/qubit selection. Only that winner received financial replays.

Leaf tests exhaust small signed operand pairs, fractional boundaries, dirty outputs and inverse cleanup, then exercise native24/40/72 extrema, power boundaries, negative tiny products and random pairs. Integration tests reject malformed/boolean contracts, missing markers, forged intervals, binding mutations, bad cached schedules and altered gate hashes; they preserve and revalidate the existing root/shift guards. The financial replays use the frozen three B4 and one B8 vectors with arbitrary nonzero full output words and complete cleanup.

The independent audit scanned 68 unique actual gate arrays and 354 metadata locations and froze 910 inputs. It parses actual partials, full correction, CSA compressors, Brent-Kung sum, native copy and literal inverse. It independently checks the signed polynomial, compressor, prefix and slice identities, with 6,844 finite arithmetic checks including 1,241 tiny negative products, re-proves both actual operand guards and all preserved root/shift guards, rebuilds source counts and capped packing, and reconciles the four producer replays. It adds no extra financial replay credit.

This wave adds **113 distinct successful pytest cases and four complete financial gate replays**, bringing the verified program totals to **581 cases and 34 replays**. G2 continuous-dollar error, G3 a compatible 99% estimator, G4 matched classical timing and G5 physical runtime remain open. Everything was executed locally; nothing was pushed, uploaded or published.

Receipts: [leaf](../../results/limitation_program_20261001/A09_range_leaf_run001/summary.json), [source](../../results/limitation_program_20261001/A09_range_run001/summary.json), [independent audit](RANGE_SOURCE_COSTS.md), [wave packet](../../results/limitation_program_20261001/WAVE06_run001/summary.json). The next bounded component is the [remaining exact coefficient frontier](NEXT_CONSTANT_FRONTIER.md).
