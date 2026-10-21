# Exact unsigned square-root leaf screen

The narrowed leaf passed 42 tests and reduces the complete clean leaf's T-depth
from 225,193 to 105,582 under the unsigned 46-bit input promise. Its interface
still accepts a 72-bit input and XORs an exact 72-bit result into an arbitrary
initial output. Every stored remainder and temporary is restored to zero.
Full-source dispatch, scheduling and circuit replay must pass before adopting
any whole-source resource improvement.

The relevant range proof is
[A07_run003](../../results/limitation_program_20261001/A07_run003/summary.json):
all 30 B4x12 and 234 B8x52 square-root operands fit unsigned 46 bits and their
results fit 43 bits. The promised operand may have bit 45 set. Treating that bit
as a signed 46-bit sign and clamping it to zero would change the function.
This leaf performs `isqrt(raw_input << 40)` exactly; it introduces no such clamp.

| Complete leaf | Logical qubits | T gates | T-depth | Clifford+T depth |
| --- | ---: | ---: | ---: | ---: |
| Historical full72 clean square root | 4,733 | 467,264 | 225,193 | 667,238 |
| Padded historical46, clean child twice | 2,543 | 467,152 | 225,096 | 666,952 |
| Padded historical46, fused child copy | 2,497 | 233,576 | 112,548 | 333,476 |
| Tight43 root, clean child twice | 2,393 | 438,256 | 211,164 | 625,672 |
| **Tight43 root, fused child copy** | **2,350** | **219,128** | **105,582** | **312,836** |

The selected leaf cuts logical width by 50.35%, T count by 53.10% and T-depth
by 53.11% relative to the historical full72 leaf. These are exact seven-T
Toffoli counts and logical schedules with all-to-all connectivity; they do not
measure a physical execution time or establish quantum advantage.

The four candidates were declared before tests. The padded variant calls the
unchanged historical square-root builder at width 46. The tight variant runs
the same restoring square-root recurrence with 43 root bits and 45-bit stored
remainders instead of 46 root bits and 48-bit remainders. After s accepted
digits, remainder r satisfies `0 <= r < 2*q + 1`, where q is the s-bit partial
root. The next trial dividend `4*r + digit` is less than `2**(s+3)`. At the last
step `s=42`, 45 bits therefore hold every intermediate without truncation.
The comparison, conditional subtraction and literal reverse cleanup retain
the original exact floor function.

The safe wrapper computes the entire clean child, copies the result, and runs
the child again to erase its private result. The selected wrapper validates
the child's literal compute/copy/reverse boundary, binds the child's output
copy directly to the external output, and executes only one forward/reverse
pair. It rejects a damaged inverse, output participation during computation,
an altered output-copy boundary or aliased copy sources. High external output
bits are left unchanged because the computed result there is zero.

Validation covered every promised input for external widths 1 through 6,
every fractional scale 0 through the external width, and every active input
width. Initial outputs were exhaustive for widths up to 3; larger widths used
zero, all ones and seeded arbitrary words. Every case ran forward and inverse
and checked input preservation and all workspace bits. At width72/f40, all
four candidates matched independent integer `isqrt` and the historical leaf
on 214 production patterns, including scaled perfect-square neighbors, powers
of two, the unsigned bit45 case, maximum input and 64 seeded random inputs.
Invalid promises deliberately differed from the historical full72 function
and were rejected by the separate contract predicate. The sweep passed in
39.01 seconds; the complete leaf experiment took 46.70 seconds.

The implementation exports `build_narrow_sqrt(width=72, fraction_bits=40,
active_bits=46, algorithm="tight-digit-by-digit", embedding="fused-child-copy")`
and `leaf_spec` with the same parameters. `input_contract(46)` returns
`{"unsigned_input_bits": 46}`. Cache specifications include external width and
scale, active input width, unsigned domain, radicand/result/remainder widths,
algorithm, embedding and lowering version. The selected key is
`630122e3bf0b6072b4b7`.

[Prospective protocol, metadata, gate arrays and receipts](../../results/limitation_program_20261001/A11_leaf_run001/summary.json)
include frozen code and dependency hashes. The implementation is in
[narrow_sqrt.py](../../research/controlled_source_completion/narrow_sqrt.py),
with the repeatable local experiment and tests in
[test_narrow_sqrt.py](../../research/limitation_program_20261001/test_narrow_sqrt.py).
Nothing was pushed or sent to an external service.
