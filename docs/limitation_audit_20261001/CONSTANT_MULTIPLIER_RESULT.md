# Exact ln(2) multiplication reduces the complete arithmetic circuit depth

Local experiment, 1 October 2026. **Specializing the remaining expensive ln(2) multiplication reduces complete-source T-depth by another 12.5% for B4×12 and 12.4% for B8×52, within the previous logical-qubit budgets.** Combined with the retained lookup and variable-multiplier improvements, depth is now 2.48× and 2.44× lower than the original Stage A sources. This resolves another avoidable arithmetic cost; quantum pricing advantage remains unestablished.

## The small limitation and its exact replacement

The previous [executed arithmetic results](EXECUTION_RESULTS.md) retained a general 72-bit constant multiplier for the fixed-point ln(2) coefficient `762123384786`, with 40 fractional bits. Here, all targeted operands come from a bit-extraction node that shifts left by 40. Their low 40 bits are therefore identically zero.

For the 72-bit operand `A = U << 40`, interpreting both words as signed two's-complement gives:

```text
signed72(A) = signed32(U) × 2^40
floor(signed72(A) × 762123384786 / 2^40)
    = signed32(U) × 762123384786
```

This eliminates the discarded product portion exactly, including negative operands. The coefficient remains a positive integer: storing it as a signed 40-bit constant would give the wrong sign. The required output is still the original 72-bit word, XORed into an arbitrary initial output register; all inputs and workspace are restored.

We also encode the coefficient with 13 nonadjacent signed terms instead of 23 positive binary terms. A carry-save tree combines the weighted input bits, followed by one carry-propagating addition and complete uncomputation. Negative weights use the exact identity `−b × 2^j = (1−b) × 2^j − 2^j`. The implementation uses only X, CX and exact CCX gates.

The local experiment library selects this leaf only when the same SSA graph proves the zero-low-bit condition. Matching the coefficient alone is insufficient. Other calls retain their archived leaves. Cache keys include the input contract, coefficient, precision and lowering strategy; cached gate hashes are checked.

## Four alternatives tested

These costs include computation, output XOR and cleanup. CCX uses the same exact seven-T decomposition and all-to-all logical scheduling as the baseline.

| Constant-multiplier leaf | Logical qubits | T gates | T-depth |
|---|---:|---:|---:|
| Previous general leaf | 433 | 80,808 | 46,176 |
| Binary shift-add | 289 | 34,440 | 19,680 |
| Signed-digit shift-add | 289 | 18,004 | 10,288 |
| Binary carry-save | 2,341 | 20,188 | 1,184 |
| **Signed-digit carry-save, retained** | **1,405** | **11,396** | **1,152** |

The retained leaf has 40.08× lower T-depth and 85.9% fewer T gates. Its larger scratch allocation fits after repacking independent leaves under the existing budgets. The 289-qubit signed-digit shift-add remains an implemented alternative when workspace is tighter.

## Complete-source result

The comparison starts from `multiplier_v2`, which already includes the exact 32-row coefficient lookup and carry-save variable multiplication. Selection minimizes complete-source capped T-depth, then T count and qubits.

| Circuit | Proved calls | Logical qubits, before = after | T-depth before | T-depth after | Further reduction | T gates after |
|---|---:|---:|---:|---:|---:|---:|
| B4×12 | 78 | 550,158 | 2,784,902 | **2,436,454** | **12.51%** | 632,258,326 |
| B8×52 | 650 | 4,460,490 | 2,995,256 | **2,624,696** | **12.37%** | 5,191,385,654 |

Complete Clifford+T depth also falls from 8,277,427 to 7,226,923 and from 8,920,741 to 7,803,425. Against the original Stage A circuits, the combined changes reduce T gates by approximately 30.3% and 30.4%.

**Only the recomputed capped schedules support the same-budget claim.** The result JSON also records `fixed_batch_t_depth`, an arithmetic-only comparison that keeps the previous batches. With the new scratch sizes, those unchanged batches would exceed the caps: 569,531 qubits for B4 and 4,623,695 for B8. Their depth values are counterfactual diagnostics, even though they happen to equal the valid repacked depths.

## Verification and scope

- **61 tests passed**, including 16 new tests: exhaustive small signed words across all four strategies; production-width signed edges and random values; historical-leaf equivalence; nonzero outputs; inverse execution; invalid promises; proof dispatch and cache corruption checks.
- Four complete gate replays passed against the independent financial IR: B4's previous random input, all-zero uniforms and all-maximum uniforms; B8's previous random input. Each restored every input and workspace bit. The B4 replays each include 30 negative specialized operands; B8 includes 234.
- Financial targets, precision, coefficient tables and input laws are unchanged. Every other leaf is reused byte-for-byte, including the previously improved lookup and variable multiplier.

Complete-source replays sample financial inputs; they are not exhaustive financial validation. The signed arithmetic proof and small-word exhaustive tests address the replacement itself. Physical routing, magic-state supply, estimator cost and the continuous-price certificate are outside this experiment. No measured end-to-end runtime or advantage follows from these source counts.

## Local evidence and reproduction

Implementation: [constant_multiplier.py](../../research/controlled_source_completion/constant_multiplier.py). Guarded compiler and experiment: [experiment_constant_multiplier.py](../../research/limitation_audit_20261001/experiment_constant_multiplier.py). Evidence: [protocol](../../results/limitation_audit_20261001/constant_multiplier_v1/protocol.json), [all candidates and replays](../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json), [verification receipt](../../results/limitation_audit_20261001/constant_multiplier_v1/verification.json) and [SHA-256 manifest](../../results/limitation_audit_20261001/constant_multiplier_v1/manifest.json).

From the repository root, use a fresh output directory:

```powershell
.context/frontier_t0_env/Scripts/python.exe -m research.limitation_audit_20261001.experiment_constant_multiplier --source-root results/limitation_audit_20261001/multiplier_v2 --output results/limitation_audit_20261001/constant_multiplier_reproduction
```

The exact executed producer is archived alongside the results. Its hash matches the preregistered protocol; the maintained producer differs only in formatting, verified by identical Python ASTs. Everything was executed and saved locally; nothing was pushed or published.
