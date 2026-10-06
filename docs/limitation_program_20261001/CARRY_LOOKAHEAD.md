# A08: exact prefix add/sub screen

The two clean prefix adders are exact, but neither meets the preregistered **2% complete-source T-depth reduction**. Keep the accepted [A10 inverse baseline](../../results/limitation_program_20261001/A10_inverse_run001/summary.json). No new full financial gate replay ran and no prefix candidate was adopted.

This closes one finite A08 experiment, not the entire carry-lookahead family. Brent-Kung is a useful exact component for a separate experiment inside the dominant multiplication leaves; the present screen changed only direct SSA add/sub calls.

## Prospective scope and saved receipts

The successful prospective [protocol](../../results/limitation_program_20261001/A08_run001/attempt002/protocol.json) froze two variants, widths 24/40/72, a 4,096-qubit leaf ceiling and the exact accepted B4/B8 source. It required at least 2% full-source T-depth reduction **in each case**, no increase in Clifford+T depth, and the existing actual qubit caps. An increased T count was allowed and recorded for later physical costing. The family stopped after its static screen because both variants missed the depth threshold.

The [summary](../../results/limitation_program_20261001/A08_run001/attempt002/summary.json), [verification](../../results/limitation_program_20261001/A08_run001/attempt002/verification.json), [leaf screen](../../results/limitation_program_20261001/A08_run001/attempt002/leaf_screen.json) and [manifest](../../results/limitation_program_20261001/A08_run001/attempt002/manifest.json) retain the emitted gate arrays, source bindings, capped schedules, per-node decisions, fallback identities and executable snapshots. The successful run took 110.68 wall seconds and 100.20 process CPU seconds, within the 30-minute ceiling.

The original attempt is preserved at [A08_run001](../../results/limitation_program_20261001/A08_run001/FAILED_ATTEMPT.md). Its arithmetic tests passed; two toy dispatch assertions used scaled float outputs as integer words. The corrected attempt requests the evaluator's integer trace. Both prospective protocols and their original code snapshots remain saved. No arithmetic implementation changed between attempts.

## Exact leaf and proof

[carry_lookahead.py](../../research/controlled_source_completion/carry_lookahead.py) emits only X, CX and CCX. Its interface is

`|a,b,z,0> -> |a,b,z XOR ((a +/- b) mod 2^w),0>`.

Every input and initial output bit pattern is permitted. Signed two's-complement and unsigned interpretations share this modular bit map. Fractional scaling is unchanged. There is no range restriction or approximation, and `input_contract={}`. Output wires only receive X/CX gates; they never control a gate. Input wires are never gate targets.

For one input bit, `p=a XOR b`, `g=a AND b`, hence `g*p=0`. A contiguous high/low interval pair composes as

`G = Gh XOR (Ph AND Gl)`, `P = Ph AND Pl`.

The two generate terms are disjoint because `Gh*Ph=0`, so XOR equals carry OR. Also `G*P=0`: the first product vanishes by high disjointness; the second by `Gl*Pl=0`. This invariant proves every out-of-place prefix node. The builder never substitutes XOR for OR outside that domain.

Kogge-Stone doubles contiguous interval lengths in dense stages. Brent-Kung first builds aligned blocks and then distributes completed prefixes into each block's right subtree. Both use copied stage states, so mutations of one endpoint cannot change another node's source semantics. Index bounds truncate incomplete end blocks; no power-of-two width assumption or omitted padding constant is used. Only the first `w-1` generate/propagate pairs need prefixes, since modular arithmetic discards the carry out.

Addition uses carry-in zero, with `carry_i=G_[i-1:0]`. Subtraction computes `a+(~b)+1` in private scratch, with `carry_i=G_[i-1:0] XOR P_[i-1:0]`; bit zero explicitly receives the carry-in one. Prefix computation and input-complement scratch are reversed after the result copy. This clears all workspace while preserving the arbitrary output XOR. Pure basis permutations plus this clean-map proof also establish the same action on superpositions; the tests do not introduce a phase oracle or relative-phase Toffoli replacement.

## Exact verification

[test_carry_lookahead.py](../../research/limitation_program_20261001/test_carry_lookahead.py) passed all **22 tests** in 14.17 seconds:

- **299,584 literal-gate executions** cover every `a,b,z` at widths 1 through 5, both operations, both variants and forward/inverse execution. Each checks the modular integer result, preserved inputs and zero scratch.
- **6,558 prefix patterns** cover all three allowed singleton `(g,p)` states through width 7 in both networks, including incomplete end blocks. A negative disjointness control demonstrates that unrestricted OR-to-XOR substitution is false.
- Widths 24, 40 and 72 cover carry chains, sign endpoints, modular wrap, single bits, 64 seeded random pairs per width, zero/nonzero outputs, inverse execution, independent signed/unsigned formulas and the current ripple reference.
- Toy complete compact schedules cover repeated input arguments and aliased named outputs with different nonzero initial outputs. Dispatch binds against the immutable target and rejects a foreign output ID.
- Every non-add/sub leaf retains its original key, metadata bytes and gate bytes. The financial target bytes, baseline hashes, executable snapshots and saved dependency hashes remain unchanged.

These tests and the structural proof establish the exact leaf interface. The stopped candidates did **not** receive complete financial gate replays. Saved full-source resources are exact counts and upper-bound depths of the emitted capped schedule, not measured physical runtimes.

An independent read-only review found no arithmetic correctness issue in the disjointness proof, arbitrary-length Brent-Kung stages, carry-in-one subtraction, clean XOR wrapper or immutable dispatch. It confirmed the distinction between exact tested leaves plus static source resources and a replay-verified adopted financial source.

## Leaf resources

The resource convention is the repository's exact seven-T Toffoli expansion and all-to-all ASAP gate schedule. Logical prefix-network stages do not directly equal this gate-level T-depth: shared control wires and the concrete decomposition matter.

| Width | Leaf | Variant | Qubits | T count | T-depth | Clifford+T depth |
|---:|---|---|---:|---:|---:|---:|
| 24 | add | ripple | 97 | 672 | 384 | 1,157 |
| 24 | add | Brent-Kung | 193 | 1,358 | 85 | 224 |
| 24 | sub | Brent-Kung | 217 | 1,358 | 85 | 229 |
| 24 | add | Kogge-Stone | 287 | 2,674 | 221 | 576 |
| 24 | sub | Kogge-Stone | 311 | 2,674 | 221 | 579 |
| 40 | add | ripple | 161 | 1,120 | 640 | 1,925 |
| 40 | add | Brent-Kung | 335 | 2,450 | 106 | 278 |
| 40 | sub | Brent-Kung | 375 | 2,450 | 106 | 283 |
| 40 | add | Kogge-Stone | 541 | 5,334 | 346 | 898 |
| 40 | sub | Kogge-Stone | 581 | 5,334 | 346 | 901 |
| 72 | add | ripple | 289 | 2,016 | 1,152 | 3,461 |
| 72 | add | Brent-Kung | 621 | 4,662 | 127 | 332 |
| 72 | sub | Brent-Kung | 693 | 4,662 | 127 | 337 |
| 72 | add | Kogge-Stone | 1,099 | 11,354 | 583 | 1,508 |
| 72 | sub | Kogge-Stone | 1,171 | 11,354 | 583 | 1,511 |

The ripple add/sub resources are identical under the current clean wrapper. All new leaves are under 4,096 qubits. Brent-Kung wins this two-variant leaf comparison at every screened width; this does not establish a universal prefix-adder optimum.

## Complete capped source screen

[experiment_adders.py](../../research/limitation_program_20261001/experiment_adders.py) subclasses the frozen constant integration library with `log_strategy=None` and replaces only direct full-word add/sub calls. It preserves signed7 logarithm leaves, inverse-ln2 leaves, lookup circuits and every other fallback byte. There are **1,990 / 17,210** replaced forward calls in B4/B8. Inner multiplication, square-root and shift adders retain their current implementation.

| Case | Variant | Actual qubits | T-depth | Depth reduction | T count | T-count increase | Clifford+T depth |
|---|---|---:|---:|---:|---:|---:|---:|
| B4x12 | accepted baseline | 550,150 | 1,773,574 | — | 628,103,014 | — | 5,260,905 |
| B4x12 | Brent-Kung | 550,143 | 1,747,142 | 1.4903% | 638,634,094 | 1.6766% | 5,183,355 |
| B4x12 | Kogge-Stone | 550,145 | 1,759,974 | 0.7668% | 665,268,254 | 5.9171% | 5,216,123 |
| B8x52 | accepted baseline | 4,460,481 | 1,824,984 | — | 5,155,831,590 | — | 5,426,165 |
| B8x52 | Brent-Kung | 4,460,464 | 1,796,756 | 1.5468% | 5,246,906,910 | 1.7665% | 5,343,221 |
| B8x52 | Kogge-Stone | 4,460,464 | 1,811,412 | 0.7437% | 5,477,245,550 | 6.2340% | 5,380,733 |

Both variants fit the caps and reduce Clifford+T depth. The stopping reason is the **less-than-2% whole-source depth gain**, not the increased T work. The concrete depth/work tradeoff is retained for future physical costing; this screen does not pronounce carry-lookahead impossible or universally unhelpful.

## Follow-up and compatibility

Freeze the dedicated prefix builder as this experiment's exact component. A separate A09 experiment can test it inside dominant carry-save multiplication where the final ripple addition and signed corrections occur. It must rebuild and verify those multiplier leaves, then repeat the capped whole-source screen; the present direct-add results cannot be credited to that future experiment.

The current frozen `ConstantIntegrationLibrary` accepts archived zero-low/signed-upper contracts but rejects an explicitly empty archived contract. New A08 leaf metadata uses `{}` as requested, which the compact scheduler accepts. If a later experiment adopts these leaves, an independently versioned integration reader must support empty contracts before using that accepted source as a new baseline. No current baseline is affected because A08 was not adopted.

Reproduce this bounded run with the pinned local interpreter and a fresh output directory:

```powershell
.context/frontier_t0_env/Scripts/python.exe -m research.limitation_program_20261001.experiment_adders --source-root results/limitation_program_20261001/A10_inverse_run001 --output results/limitation_program_20261001/A08_new_attempt
```

No precision or input-law change requires a new approximation certificate here. G2 financial-error certification, G3 estimator accounting, G4 matched classical timing and G5 physical costs remain separate open requirements; no quantum-advantage claim follows from this screen.
