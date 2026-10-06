# Independent review of the signed prefix multiplier

This review covers the exact arithmetic construction in
[prefix_multiplier.py](../../research/controlled_source_completion/prefix_multiplier.py)
and the immutable dispatch in
[experiment_prefix_multiplier.py](../../research/limitation_program_20261001/experiment_prefix_multiplier.py), exercised by
[test_prefix_integration.py](../../research/limitation_program_20261001/test_prefix_integration.py).
It concerns a finite signed integer function. It does not certify a continuous
financial price, estimator cost, physical execution time, or quantum advantage.

## Signed product and discarded bits

For a `w`-bit word, signed bit weights are `2**j` for `j < w-1` and
`-2**(w-1)` for its sign bit. A partial product therefore has negative weight
exactly when one operand bit is its sign bit. The sign-bit-by-sign-bit term has
positive weight. These statements hold for every input word, including both
signed extrema; no range or low-zero promise is needed.

For each negative partial bit `t` in column `k`, the producer uses
`(1-t)*2**k - 2**k`. This equals `-t*2**k` as an integer. Starting its fresh wire
with X and then applying CCX writes the complement of the ordinary partial bit.
The sum of all fixed negative weights is reduced modulo `2**n`, where
`n = w + f`, and its set bits are inserted into the carry-save columns.
High partial columns at `k >= n` may be omitted because their weights vanish
modulo `2**n`. Columns below the final shift are retained through every carry.

The carry-save step uses `sum = x XOR y XOR z` and
`carry = (x AND y) XOR ((x XOR y) AND z)`. Its two carry terms are disjoint,
so `sum + 2*carry = x+y+z`. Dropping only a carry leaving column `n-1`
preserves the represented residue. In particular, discarding individual low
partials before accumulation would lose carries into retained bits and would
compute a different function.

Let the full signed integer product be `P = q*2**n + r`, with
`0 <= r < 2**n`. Then
`floor(P/2**f) = q*2**w + floor(r/2**f)`. Consequently selecting residue bits
`f` through `f+w-1` equals the original signed floor modulo `2**w`, even when
`P` is negative. This is why reducing the product modulo before the final floor
is exact. For the current interface, `w=72`, `f=40`, and `n=112`.
Here the 82 negative partials occupy columns 71 through 111 twice. Their
fixed correction is `-2*(2**112-2**71) mod 2**112 = 2**72`: one constant
bit in column 72, consistent with the saved leaf screen.

## Clean nested addition

The final two carry-save rows are copied into distinct fresh `n`-bit registers.
A clean XOR prefix child preserves both rows and writes their modular sum into
a third fresh register. Its register layout is explicitly checked before
embedding, and its scratch wires remain distinct from all three registers.
The producer copies the retained product slice into the external output, then
reverses the entire enclosing computation, including the child gates.

The external output is never a control. Thus an arbitrary initial output word
receives XOR with the exact answer, while partial bits, correction bits,
carry-save wires, final rows, internal product, and child scratch return to zero.
The leaf consists only of X, CX, and CCX gates. This basis permutation introduces
no relative phase, and the exact gate reversal remains valid on superpositions.

## Integration and attribution

The replacement is restricted to frozen target nodes whose operation is `mul`.
Other operations retain their archived keys and metadata/gate bytes. The new
multiplier spec and saved metadata omit `input_contract`: both arguments and
the output keep their full original word widths, and no narrowed-input premise
is introduced. The current full-word archived executor must load this format
directly.

This family combines signed partial complement/correction encoding with a
prefix final addition. The previous carry-save implementation instead applies
signed corrections after its final addition. Any measured improvement belongs
to the combined replacement; it cannot be assigned solely to the final adder
without a separate ablation. T work and workspace can increase while depth
decreases; physical costing must account for that tradeoff. Individual leaf
depth savings are not complete
source savings, and a complete static source depth reduction is not a physical
runtime result.

## Verification receipt

The prospective producer run executed both test files after saving its
[protocol and executable snapshots](../../results/limitation_program_20261001/A09_run001/protocol.json):

```text
.context/frontier_t0_env/Scripts/python.exe -m research.limitation_program_20261001.experiment_prefix_multiplier --source-root results/limitation_program_20261001/A10_inverse_run001 --output results/limitation_program_20261001/A09_run001
```

Its embedded `pytest.main` ran `test_prefix_multiplier.py` and
`test_prefix_integration.py` together. The executing agent observed **24 passed
in 46.96 seconds**, including **16 independent integration cases**. This review
used that receipt and did not duplicate the gate tests or financial replays.
The saved [verification](../../results/limitation_program_20261001/A09_run001/verification.json)
records pytest exit code zero, 61,888 exhaustive small literal gate replays,
the 16 independent integration cases, and unchanged frozen dependencies.

The independent checks cover both prefix variants in a full `72/40` toy SSA
pipeline, distinct and repeated arguments, downstream multiplication,
nonzero named-output aliases, signed extrema, low-bit carry, seeded random
inputs, direct leaf inverse cleanup, archival execution, fallback byte identity,
immutable node/parameter/table bindings, cache version/hash corruption, contract
omission, persisted cache reuse, and in-memory metadata mutation rejection.

The saved [completed result](../../results/limitation_program_20261001/A09_run001/summary.json)
accepts Brent–Kung and contains three passing B4 and one passing B8 complete
financial gate replay receipts. Independently reading those receipts confirmed
their pass/cleanup status. This review also recomputed the hashes of all 16
current dependencies and their saved executable snapshots: each matched the
prospective protocol. It did not rerun those four financial gate executions.

A read-only check of both saved production sources validated every node/call
operation, parameter, SSA argument/output binding and actual native register
arity/layout. All registers retain contiguous full 72-bit words, and every new
`mul` metadata entry and spec omits `input_contract`. Thus the accepted sources
retain the typed full-word archive interface; the unchanged archived executor
also passed the independent toy-source checks above.

The selected complete source resource counts are:

| Case | Logical qubits | T count | T depth | Depth reduction vs accepted inverse baseline | T count increase |
| --- | ---: | ---: | ---: | ---: | ---: |
| B4x12 | 550,141 | 648,827,494 | 1,218,582 | 31.2923% | 3.2995% |
| B8x52 | 4,460,481 | 5,326,463,142 | 1,268,304 | 30.5033% | 3.3095% |

These are the saved schedules' logical counts for the combined multiplier
family. Physical runtime remains unknown; the approximately 3.3% additional
T work must be included when costing factories and execution time.

Reviewed executable SHA256 snapshots:

| File | SHA256 |
| --- | --- |
| `prefix_multiplier.py` | `1142fd2a4b9155144992659899b51d48231caddccbcfa0f184cf9cf7d7bb8393` |
| `carry_lookahead.py` | `5dc4ff809919cbe190075d53ffb9e838a5ef7090011c4396126d770829c7c4af` |
| `experiment_prefix_multiplier.py` | `4eade8f126aa5e7d1f3144cf078e93a6863d780887e0aed4d9f74defc1852a7e` |
| `test_prefix_integration.py` | `6c98057ddd2a44a495e3293b3da868e5517d2c9f57f55561d35f1bf15410d6d2` |

No arithmetic or dispatch correctness issue was found within this full-word
archived interface. The finite integer result and its saved resource/replay
evidence leave financial error certification, an explicit estimator schedule,
a timed matched classical comparator, and physical cost open.
