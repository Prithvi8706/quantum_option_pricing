# A09: accepted exact signed-complement CSA/prefix multiplier

The Brent-Kung variant passed the bounded experiment and all four complete financial gate replays. Relative to the frozen A10 inverse baseline, full capped-source T-depth falls **31.2923% / 30.5033%** for B4/B8. Total T work increases **3.2995% / 3.3095%**, so this is a measured depth/work tradeoff that still needs physical costing.

The selected exact source is [A09_run001](../../results/limitation_program_20261001/A09_run001/summary.json). Its [protocol](../../results/limitation_program_20261001/A09_run001/protocol.json), [verification](../../results/limitation_program_20261001/A09_run001/verification.json), [leaf screen](../../results/limitation_program_20261001/A09_run001/leaf_screen.json) and [manifest](../../results/limitation_program_20261001/A09_run001/manifest.json) preserve executed code, emitted gates, bindings, schedules, node attribution and replay receipts. All old evidence, compiler modules and the original accepted source remain unchanged.

This family jointly changes signed partial-product encoding/correction and the final prefix adder. The measured gains cannot be assigned solely to the final adder without an ablation. It uses the frozen A08 prefix builder as an exact child; the separate direct-add A08 screen remains a stopped branch.

## Prospective scope and selection

Before testing, the protocol froze exactly two variants, Brent-Kung and Kogge-Stone, at width 72/fraction 40. The acceptance rule required one variant to reduce complete capped-source T-depth by at least 2% in **both** financial cases, with no increase in Clifford+T depth and no cap violation. Increased T work was permitted and explicitly disclosed. The fixed caps were 550,150 / 4,460,481 logical qubits from [A10_inverse_run001](../../results/limitation_program_20261001/A10_inverse_run001/summary.json).

Both variants qualified statically. Brent-Kung had the lower summed T-depth and was the only variant sent to complete financial replay. The experiment completed in **203.19 wall seconds / 195.88 process CPU seconds**, below the 30-minute ceiling. These are local research execution times, not estimates of quantum hardware runtime.

## Exact signed arithmetic

[prefix_multiplier.py](../../research/controlled_source_completion/prefix_multiplier.py) implements

`|a,b,z,0> -> |a,b,z XOR (floor(signed(a)*signed(b)/2^f) mod 2^w),0>`.

Every signed `w`-bit input pair and initial output word is allowed. There is no range, sparsity, square-input or zero-low-bit promise. The output is full width, inputs are preserved, workspace is clean, and inverse execution gives the same XOR map. Negative nonintegral products use **floor**, including `floor(-1/2^40)=-1`; truncation toward zero would be wrong.

Write each signed operand as `sum(a_j*s_j*2^j)`, where `s_j=+1` except `s_(w-1)=-1`. A partial bit `t=a_j AND b_i` has coefficient `s_j*s_i`: negative exactly when one index is a sign-bit index. The double-sign term is positive.

For `n=w+f`, terms at column `k=i+j>=n` vanish modulo `2^n`. Every retained negative term is encoded using

`-t*2^k = (1-t)*2^k - 2^k`.

The circuit computes its complement with X then CCX into a fresh wire, and adds the fixed correction `C=-sum_negative(2^k) mod 2^n` as constant-one wires in the same CSA columns. This is a full-domain algebraic identity, not a reachable-input assumption. For the production 72/40 leaf there are **4,688** retained partial terms, **82** negative terms, and

`C = -2*sum(2^k,k=71..111) mod 2^112 = 2^72`.

Thus the correction is one constant bit at column 72. No sequential sign-correction subtractions are required.

Each CSA triple uses `sum=x XOR y XOR z` and `carry=(x AND y) XOR ((x XOR y) AND z)`. The carry terms are disjoint, so this XOR is exactly majority. It preserves `x+y+z=sum+2*carry`. Fresh sum/carry wires preserve all predecessors for reversal; carries leaving column `n-1` vanish only modulo `2^n`.

**All low columns 0 through f-1 remain present through reduction and final carry propagation.** Dropping these columns before accumulation is invalid: with w=4,f=2,a=b=3, retaining only above-cutoff partials yields 1, while `floor(9/4)=2`.

The final two full `n`-bit rows are copied into fresh registers. The frozen clean-XOR prefix child adds them into a separate full `n`-bit product and preserves both rows. If `P` is the signed product and `r=P mod 2^n`, Euclidean division gives `P=q*2^n+r`, hence

`floor(P/2^f) mod 2^w = floor(r/2^f)`.

Copying product bits `[f:f+w]` therefore implements the exact desired floor, including negative products. The parent reverses all computation after this copy. Outer output wires only receive the contiguous CX copy and never control a gate. All parent input wires are controls only. The outer compute/copy/reverse structure proves arbitrary-output XOR and cleanup on superpositions as well as basis states; no relative-phase substitution is used.

## Leaf and integration verification

All **24 tests** passed in **46.96 seconds**. [test_prefix_multiplier.py](../../research/limitation_program_20261001/test_prefix_multiplier.py) contributes:

- **61,888 literal-gate executions** covering widths 1..5, every fraction 0..w and every signed input pair, zero/all-one initial outputs and both directions, with input and workspace restoration.
- An independent exhaustive integer check of signed partial weights, complement correction, modular residue and floor extraction; explicit negative controls for omitted correction and prematurely dropped low carries.
- Production 72/40 sign endpoints, single bits, carry-rich pairs, 64 seeded random pairs, nonzero output words and inverse runs, checked against Python signed integer floor and the historical carry-save multiplier.
- Structural checks that output wires never control computation, input wires are never targets, and invalid widths/fractions/variants reject.

The independent [test_prefix_integration.py](../../research/limitation_program_20261001/test_prefix_integration.py) contributes 16 cases covering 72-bit pipelines, repeated same-SSA arguments without a square specialization, downstream products, output aliases with different nonzero initial values, old archived executor compatibility, unchanged lookup/add/bits leaves, immutable node/table/source bindings, cache reload and forged gate/version/contract rejection. The [independent review](PREFIX_MULTIPLIER_REVIEW.md) agrees with the normal form and records the depth/work tradeoff.

[experiment_prefix_multiplier.py](../../research/limitation_program_20261001/experiment_prefix_multiplier.py) replaces only frozen-target `mul` operations. New metadata preserves the full contiguous two-input/one-output interface and **omits `input_contract`**; a persisted cache with any injected contract field, including `{}`, rejects. Its versioned specification contains width, fraction, product width, variant and signed lowering. All non-mul leaves retain their original keys and exact metadata/gate bytes, including accepted signed7 logarithm and inverse-ln2 leaves. Financial target bytes, precision and input law remain unchanged.

## Leaf resources

These are measured resource counts and all-to-all ASAP depths of the actual clean leaf, using the repository's exact seven-T Toffoli expansion.

| 72/40 leaf | Qubits | Source gates | CCX | T count | T-depth | Clifford+T depth |
|---|---:|---:|---:|---:|---:|---:|
| Historical signed CSA/ripple | 14,148 | 57,302 | 28,360 | 198,520 | 3,696 | 10,853 |
| Signed-complement CSA/Brent-Kung | 14,861 | 59,140 | 29,388 | 205,716 | 1,412 | 3,841 |
| Signed-complement CSA/Kogge-Stone | 15,743 | 64,432 | 32,916 | 230,412 | 2,396 | 6,381 |

The Brent-Kung leaf reduces T-depth by 61.7965%, with 713 more qubits and 7,196 more T gates than the current CSA leaf. The full-source cap, rather than a fabricated leaf-size ceiling, governs source eligibility. This comparison is limited to the two prospectively selected variants.

## Full capped source resources

The replacement changes **1,440 / 11,856** forward variable-multiplication calls in B4/B8. The source includes their inverse cleanup and all other financial arithmetic. Capped packing is recomputed with the unchanged target and the prior actual caps.

| Case | Variant | Actual qubits | T-depth | Depth reduction | T count | T-work increase | Clifford+T depth |
|---|---|---:|---:|---:|---:|---:|---:|
| B4x12 | accepted A10 inverse baseline | 550,150 | 1,773,574 | — | 628,103,014 | — | 5,260,905 |
| B4x12 | selected Brent-Kung | 550,141 | 1,218,582 | 31.2923% | 648,827,494 | 3.2995% | 3,569,495 |
| B4x12 | screened Kogge-Stone | 550,146 | 1,480,150 | 16.5442% | 719,951,974 | 14.6232% | 4,234,657 |
| B8x52 | accepted A10 inverse baseline | 4,460,481 | 1,824,984 | — | 5,155,831,590 | — | 5,426,165 |
| B8x52 | selected Brent-Kung | 4,460,481 | 1,268,304 | 30.5033% | 5,326,463,142 | 3.3095% | 3,735,217 |
| B8x52 | screened Kogge-Stone | 4,460,468 | 1,538,432 | 15.7016% | 5,912,054,694 | 14.6673% | 4,413,435 |

The selected source uses 174 / 186 capped batches. Both selected cases fit the previous caps, reduce Clifford+T depth and pass the 2% threshold. T-depth here is the depth of the emitted capped schedule under its stated all-to-all model, a valid upper bound rather than proof of optimal depth or physical timing.

## Complete financial gate replay and decision

The selected variant passed all four prescribed full emitted-gate replays: B4 previous random, all-zero and positive-payoff inputs, and B8 previous random positive-payoff input. Each starts named outputs at the nonzero 72-bit pattern `a5a5a5a5a5a5a5a5a5`. Actual output words equal the unchanged integer target trace XOR that initial word; all input and workspace bits restore exactly. The [B4](../../results/limitation_program_20261001/A09_run001/B4x12/comparison.json) and [B8](../../results/limitation_program_20261001/A09_run001/B8x52/comparison.json) receipts retain the exact input words, expected/actual outputs and cleanup results.

Accept this exact component as the local arithmetic baseline, subject to the root's independent source-cost reconciliation. Keep the old inverse-ln2 source and both candidate receipts intact. Reconcile the **increased total T work** when assessing factories and physical runtime; a depth gain does not imply equal physical runtime improvement.

The next bounded operation can address the remaining dominant square-root/shift leaves or prove and separately screen same-SSA squaring. A09 is broader than this single successful family, so do not mark every multiplication limitation solved. No financial task, precision or law changed, and no new approximation error was introduced. G2 continuous-price error certification and G3–G5 estimator, classical comparator and physical advantage requirements remain open.

Reproduce locally with the pinned interpreter and a fresh output directory:

```powershell
.context/frontier_t0_env/Scripts/python.exe -m research.limitation_program_20261001.experiment_prefix_multiplier --source-root results/limitation_program_20261001/A10_inverse_run001 --output results/limitation_program_20261001/A09_new_attempt
```

No push, external application action, historical code change or progress-file mutation is part of this experiment.
