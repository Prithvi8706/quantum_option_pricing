# Executed alternatives: what we kept, what failed, and what remains conditional

Date: 1 October 2026. This follows the seven small experiments in the [research audit](README.md), then tests a multiplier because the first full-source measurements show that multiplication dominates. Eight scoped experiments have now been attempted. This is an execution record, not a claim that every alternative in the 110-entry literature audit has been implemented.

**The strongest retained result is an exact coefficient lookup plus an exact carry-save multiplier and a memory-capped schedule.** B4x12's emitted arithmetic-source T-depth falls from 6,032,678 to 2,784,902 under the same 550,158 logical-qubit cap. B8x52's schedule falls from 6,393,144 to 2,995,256 under its original 4,460,490-qubit cap. The cost model still assumes all-to-all logical connectivity and the existing exact seven-T Toffoli decomposition. These are circuit-resource improvements, not measured hardware runtimes or quantum advantage.

Archived Stage A results, financial formulas, coefficient values, word precision, input laws and estimator requirements were not rewritten. New circuit libraries and receipts live in [the execution results directory](../../results/limitation_audit_20261001/).

## Decisions at a glance

| Small obstruction | Executed result | Decision |
|---|---|---|
| Repeated equality scans in coefficient lookup | Real 32-row log lookup: 3,136 to 420 T gates, 1,600 to 226 T-depth, same 724 qubits | **Installed as the default lookup lowering**; historical implementation remains selectable |
| Reverse Toffolis in an eligible real fragment | Five-control MCX: 49 to 28 T gates; all 8 measurement branches checked, with 3 feedback rounds | **Keep the emitted dynamic circuit**; integration into the unitary compiler needs a separate backend |
| 72-bit flags and small indexes retained everywhere | Exact storage packing reduces serial B4x12 workspace by 55,204 qubits and B8x52 by 426,296 | **Keep the opt-in compiler/storage path**; no arithmetic precision change |
| Gaussian generation requires Box-Muller | Explicit 4-, 6-, 8- and 10-qubit preparation circuits and inverses pass; MPS compression also tested | **Keep the prototypes**, pending rotation synthesis and a price-error bridge |
| Heston time stepping might be replaceable wholesale | Local covariance and literal theorem-hypothesis checks find incompatibilities, including for A1's stated tail bound | **Reject direct theorem transfer**, retain a narrower negative-leverage tail-proof question |
| An unbounded payoff might become two bounded probabilities | Exact finite-law identity and sampler work; naive shifted-grid substitution fails; the tested bounded barrier case worsens a simple query-precision budget by 10.15 times | **Keep the identity and sampler**, do not adopt this rewrite for this case |
| Retaining an entire path costs too much memory | Eight-step nonlinear toy: 76 to 56 qubits, but 15 to 27 leaf calls | **Keep as a memory/time tradeoff**, without claiming a full financial-path result |
| Sequential partial-product addition dominates arithmetic | Carry-save multiplier plus memory-aware scheduling substantially reduces full-source T-depth within the old qubit caps | **Keep the explicit multiplier backend and schedules**; select according to workspace budget |

## 1. The requested 32-row coefficient lookup

The previous circuit recomputed a full address equality for every row. The replacement shares address prefixes, switches between sibling prefixes using CNOTs, and factors out the first row as an unconditional XOR constant. It emits only X, CX and CCX gates. It neither approximates a coefficient nor substitutes a relative-phase Toffoli.

The precise interface is `out[j] ^= table[address mod 2**bits][j]`, with signed coefficients represented modulo the output width. Inputs are preserved, arbitrary initial outputs are supported, and all prefix scratch returns to zero. Unlisted rows are zero, matching the historical leaf behavior.

| Existing coefficient table | Shape | T gates before → after | T-depth before → after | Qubits before → after |
|---|---:|---:|---:|---:|
| Log | 32 × 9 | 3,136 → 420 | 1,600 → 226 | 724 → 724 |
| Atan | 32 × 9 | 3,136 → 420 | 1,600 → 226 | 724 → 724 |
| Cosine | 64 × 8 | 8,064 → 868 | 4,096 → 466 | 653 → 653 |
| Normal CDF | 256 × 8 | 46,592 → 3,542 | 23,552 → 1,898 | 655 → 655 |

Every address of all four real tables was executed, including inverse cleanup and nonzero outputs. Additional tests cover partial and constant tables, ignored high address bits, a small complete compiled graph, and a complex state entangled with a reference. The latter also checks the literal seven-T decomposition, including phases. Cache keys include the new lowering version, preventing reuse of a legacy equality-scan leaf under the new implementation.

The log lookup saves 86.61% of its T gates. The full-source benefit is much smaller: about 0.11% of T gates, because lookup is not the dominant operation. B4x12 was replayed on a seeded input and both uniform-register endpoints; B8x52 on a seeded input. These execute the emitted complete circuits with nonzero outputs and workspace restoration, rather than only evaluating the financial IR.

Implementation: [exact_lookup.py](../../research/controlled_source_completion/exact_lookup.py). Baseline and integration: [primitives.py](../../research/controlled_source_completion/primitives.py). Receipts: [lookup_v2](../../results/limitation_audit_20261001/lookup_v2/summary.json).

## 2. Cleanup inside a real multi-controlled gate

This uses the actual five-control `primitives.mcx` ladder. Its three reverse AND gates are replaced by H, measurement, conditional CZ on the two original controls, and conditional X reset. The forward ANDs and the target Toffoli retain their original exact lowering.

All 128 logical basis columns, including a reference wire and arbitrary target, are checked in each of eight measurement branches. Every branch equals the ideal MCX divided by `sqrt(8)`. The maximum forward and logical-inverse discrepancies are below `6e-17`. Deliberately omitting the phase corrections reduces the chosen superposition's fidelity to 0.5859375, so the check detects coherent damage.

The fragment saves 21 T gates but requires three sequential cleanup feedback rounds. No hardware latency was measured. Logical inversion repeats the verified MCX channel; it does not reverse measurement instructions. Consequently this is an emitted alternative backend fragment, not an instruction silently inserted into `Program.undo`.

Circuit and receipt: [mcx5.qasm](../../results/limitation_audit_20261001/mcx_cleanup_v1/mcx5.qasm), [result.json](../../results/limitation_audit_20261001/mcx_cleanup_v1/result.json).

## 3. Exact flags, indexes and retained storage

The new analysis propagates conservative possible-one masks through constants, inputs, comparisons, bit extraction, table rows, selection and selected other operations. Operations without a proof keep their full width. This is not precision reduction or a range inferred from a few sampled paths.

The compact binding keeps each leaf's original full arithmetic interface. Proved-zero high output bits receive distinct private temporary wires. They are never aliased to another output or discarded while dirty. The executor checks that private workspace returns to zero after every invocation and enforces declared input-width promises.

| Serial source | Original logical qubits | Compact logical qubits | Saved |
|---|---:|---:|---:|
| B4x12 | 414,989 | 359,785 | 55,204 |
| B8x52 | 3,374,477 | 2,948,181 | 426,296 |

Both compact complete sources passed a seeded gate replay with nonzero outputs. Exhaustive small-graph tests check the masks against the independent integer interpreter. A separately emitted signed comparison reduces its output from 72 bits to one, saving 71 qubits with identical T cost. Copy-CNOT reductions are recorded in the receipts.

These figures concern serial storage. They are not added to the multiplier's parallel-schedule gains: that combination has not been emitted and checked.

Implementation: [compact_storage.py](../../research/controlled_source_completion/compact_storage.py). Receipts: [compact_storage_v1](../../results/limitation_audit_20261001/compact_storage_v1/summary.json).

## 4. Direct Gaussian preparation, including an actual failed attempt

We specified a different finite target explicitly: a standard normal conditioned on `[-6,6]`, binned into equal-width intervals, with each label representing its interval midpoint. Prefix probabilities determine controlled rotations. This is a concrete small test of direct preparation, in the spirit of [integrable-distribution loading](https://arxiv.org/abs/quant-ph/0208112). It is not the archived digital Box-Muller law, and it is not a QSVT implementation.

The first attempt using the pinned Qiskit 1.4.6 multiplexer and optimization level 2 failed at six qubits: maximum amplitude error was about `1.88e-6`. Disabling that optimization fixed the six-qubit case, but the library's small-angle cutoff failed the ten-qubit tolerance. We replaced it with an explicit Walsh/Gray decomposition that does not prune small nonzero angles. All four sizes now pass forward and inverse checks; maximum amplitude errors are below `1.1e-15`.

The ten-qubit circuit contains 976 arbitrary RY rotations and 1,022 CNOTs. These are **not** 976 T gates. Clifford+T synthesis and its error budget remain open. Numerical tensor-train compression of the same amplitude vector with bond cap eight has trace distance about `3.49e-11`; an MPS preparation circuit has not yet been synthesized.

There is an analytic scalar quantization bound, but it does not certify the contract. With spacing `h` and cutoff `L`, a coupling gives

`W1(N(0,1), conditional midpoint-grid law) <= h/2 + 2*phi(L) + L*P(|Z|>L)`.

At ten qubits this is about `0.0058594`. It controls unit-Lipschitz scalar observables; a discontinuous barrier needs a separate boundary analysis. Numerical angle and state comparisons are also not interval-certified loading proofs. The [arithmetic-free QSVT construction](https://arxiv.org/html/2210.14892v2) remains a distinct unimplemented candidate.

Implementation and receipts: [experiment_gaussian.py](../../research/limitation_audit_20261001/experiment_gaussian.py), [gaussian_v3](../../results/limitation_audit_20261001/gaussian_v3/summary.json).

## 5. Heston compatibility: a more restrictive result than the initial screen

The fast-forwarding model requires independent variance processes and excludes variance correlation with other assets' equity drivers. Its sufficient truncation conditions also include `kappa^2 > 2*kappa*xi*rho - rho^2*xi^2 >= 0`. These are separate from the `eta >= 5` condition. See [the model and truncation analysis](https://arxiv.org/html/2602.03725v1#S6.SS2.SSS2).

From the local factor matrices, we computed the actual covariance algebraically and verified the matrix identities numerically:

`Cov(dV) = rho^2*C + (1-rho^2)*I`, and `Cov(dS,dV) = rho*C`, for standardized Brownian increments.

| Local case | Eta | Largest off-diagonal variance covariance | Middle term of the stated tail inequality |
|---|---:|---:|---:|
| A1 | 8 | 0 | -0.6225 |
| A4 | 8 | 0.075 | -0.6225 |
| S4 | 1.28 | 0.147 | -1.5225 |
| B8 | 2.88 | 0.294 | -1.1725 |

A1 passes the covariance and eta checks, but the literal sufficient tail inequality fails. A4 additionally fails covariance compatibility. Negative leverage makes the displayed middle term negative; rescaling time cannot change that sign. This does not disprove fast-forwarding for these cases. It identifies a missing tail proof and, for multiple assets, a model mismatch. The discontinuous knock-out also requires an extension beyond the cited Lipschitz payoff premise.

Receipt: [heston_screen_v1](../../results/limitation_audit_20261001/heston_screen_v1/summary.json). The original seven-item research queue's eta-only observation was deliberately not treated as acceptance.

## 6. Two bounded probabilities: identity succeeds, proposed shortcut does not

For positive `A`, mean `m`, event `E` contained in `{A>K}`, and law `qA=A*q/m`, the identity is

`E_q[(A-K)*1_E] = m*P_qA(E) - K*P_q(E)`.

We executed it on a two-asset, 128-by-128 finite normal grid with a barrier. Direct and decomposed discounted prices agree within `3.2e-15`. The finite tilted law factors into a mixture of two products of tilted one-dimensional laws. An implemented sampler drew 131,072 paths; its event frequency agreed with the exactly summed finite probability within the specified statistical check.

Simply shifting continuous Gaussians and rebinding them to this grid is wrong for this finite target. The negative control has total variation discrepancy `7.41e-5`. The exact finite mixture fixes that mismatch, but still needs a coherent preparation circuit.

For a joint one-cent error target, the receipt allocates both absolute probability errors and failure probabilities, and identifies the separate normalizer, preparation and discretization terms. In this particular bounded barrier example, an equal-cost `1/error` query screen is 10.15 times worse for the decomposition than direct bounded-payoff estimation. This is a conditional cost screen, not a quantum-estimator execution. The two indicators still require the asset and barrier arithmetic.

Receipt: [bounded_probabilities_v1](../../results/limitation_audit_20261001/bounded_probabilities_v1/summary.json).

## 7. A smaller path workspace with paid recomputation

Both schedules implement eight iterations of the isolated nonlinear transition `x_next=x*x mod 32`. One retains every intermediate until cleanup. The other recursively recomputes checkpoints. Both emit real reversible gates and pass every five-bit input, nonzero output and inverse check.

| Schedule | Qubits | Leaf calls | T gates | T-depth |
|---|---:|---:|---:|---:|
| Retain intermediates | 76 | 15 | 46,200 | 15,600 |
| Recompute checkpoints | 56 | 27 | 83,160 | 28,080 |

This solves a small memory question while exposing its price. It does not prove that recomputation improves pricing latency or that this toy transition models a financial process.

Receipt: [pebbling_v1](../../results/limitation_audit_20261001/pebbling_v1/summary.json).

## 8. Follow the dominant cost: exact carry-save multiplication

The candidate generates only the low `w+f` unsigned product bits, reduces partial-product columns with reversible carry-save compressors, performs one final carry-propagating addition, and applies the exact two's-complement corrections. It copies bits `f:f+w` to the output and reverses the computation. The signed shift and modulo semantics match the current multiplier.

| 72-bit, 40-fraction-bit leaf | Existing truncated multiplier | Carry-save candidate |
|---|---:|---:|
| Qubits | 441 | 14,148 |
| T gates | 289,968 | 198,520 |
| T-depth | 90,592 | 3,696 |

The extra workspace matters. A fixed maximum number of parallel leaves gave the best capped B4x12 depth of 6,079,060, worse than the lookup-only 6,026,790. We retained this failed schedule screen. A first-fit scheduler that accounts for each leaf's actual scratch size avoids unnecessarily serializing small operations and fits the original qubit caps.

| Complete arithmetic source | Archived T gates → candidate | Archived T-depth → candidate | Logical-qubit cap, unchanged |
|---|---:|---:|---:|
| B4x12 | 907,483,318 → 643,086,598 | 6,032,678 → 2,784,902 | 550,158 |
| B8x52 | 7,458,042,774 → 5,281,621,254 | 6,393,144 → 2,995,256 | 4,460,490 |

The candidate in this table combines **only** the exact lookup, exact carry-save multiplication and emitted memory-capped schedule. Measured cleanup, compact SSA storage, approximate Gaussian preparation and toy recomputation are not credited here. All other archived leaf bytes were reused and hash-checked. The complete source remains the same financial integer function.

The leaf checks exhaust every signed input pair for widths one through four and every supported fractional width. Production checks cover signed extremes, random values, nonzero outputs and inverse execution at 32, 72 and 96 bits. The full capped-source replay records are in the case-specific comparison receipts.

Implementation: [carry_save_multiplier.py](../../research/controlled_source_completion/carry_save_multiplier.py), [budget_schedule.py](../../research/controlled_source_completion/budget_schedule.py). Receipts: [multiplier_v2](../../results/limitation_audit_20261001/multiplier_v2/).

## Verification and reproduction

Use `.context/frontier_t0_env/Scripts/python.exe`, the existing pinned Python 3.12 research environment. The ordinary repository `venv` lacks Numba. No package installation or archived-result overwrite was needed.

The focused and existing regression suites passed **66 tests**. They cover lookup, compact binding, multiplier arithmetic, capped scheduling, existing source leaves, complete source binding, parallel execution and the original truncated multiplier. The only three warnings were pre-existing Qiskit QFT deprecation warnings. Ruff passed for all newly added implementation and experiment files.

Each experiment is a module under `research.limitation_audit_20261001` and takes `--output <new-directory>`. The lookup, compact-storage, multiplier, Gaussian, MCX-cleanup, bounded-probability, Heston-screen and pebbling commands are preserved in [verification.json](../../results/limitation_audit_20261001/execution_verification_v1.json). Commands refuse to reuse the top-level result directory. Failed preliminary runs remain labelled as failed attempts; completed result directories are named explicitly above.

## The remaining small questions

The accepted changes remove demonstrated implementation waste. They do not finish the estimator, synthesis, physical-layout or continuous-price error budgets. The next direct Gaussian tasks are to emit the promising bond-eight preparation, synthesize rotations to a stated operator-error allowance, and prove the resulting error for the actual payoff. The Heston task is narrower now: a negative-leverage tail argument and the exact joint covariance must be addressed before compiling a replacement transition. A combined compact-storage/carry-save schedule is another exact, independently testable compiler question.
