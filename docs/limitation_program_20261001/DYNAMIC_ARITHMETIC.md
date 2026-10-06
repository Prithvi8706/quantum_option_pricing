# Measurement-based arithmetic fragment

One fulladder channel passed 15 fixtures and an independent dense-matrix
evaluation of its actual saved primitive operations. It maps five logical
input wires to the fulladder XOR permutation, preserving arbitrary dirty sum
and carry outputs, and resets both initially fresh scratch wires.

Exact arithmetic in `Q(omega)`, with `omega^4=-1`, proves the fresh-target
four-T AND phase correction. Each corrected measurement cleanup has amplitude
`1/sqrt(2)`. Every two-measurement branch therefore has exactly `K=U/2`, with
probability `1/4`, preserving arbitrary superpositions and external-reference
entanglement. Basis-state agreement alone was not the acceptance criterion.

| Paid resource | Measurement-based fragment | Unitary control |
|---|---:|---:|
| T or T-dagger gates | 8 | 28 |
| Serial logical T depth | 8 | 28 |
| Fresh zero scratch wires | 2 | 2 |
| Measurements | 2 | 0 |
| Scheduled conditional CZ corrections | 2 | 0 |
| Scheduled conditional X resets | 2 | 0 |
| Worst-case serial primitive slots | 34 | 66 |

The control contains four actual seven-T Toffoli decompositions. Measurement
outcomes, classical result storage, feedforward and reset slots are charged.
This is the declared compute/copy/uncompute control, rather than a claim about
the cheapest standalone unitary fulladder. A direct dirty-carry construction
needs only two exact Toffoli gates, or 14 T gates; its separate emitted-circuit
comparison is queued. The accepted 8-versus-28 receipt remains unchanged.
Physical feedback time, routing, factories and integration into a financial
arithmetic leaf remain unpriced. The fragment establishes a logical T saving;
it changes no accepted source cost, financial error or quantum-advantage claim.
Its cleanup is a deterministic unitary channel after correction, requiring
an explicit adjoint-channel implementation wherever source uncomputation is
needed; reversing a list containing measurements is not a circuit inverse.

[Frozen result](../../results/limitation_program_20261001/A16_dynamic_run001/summary.json),
[exact proof](../../results/limitation_program_20261001/A16_dynamic_run001/exact_channel_derivation.json),
[resource ledger](../../results/limitation_program_20261001/A16_dynamic_run001/resource_ledger.json).

The fair 14-T control and a separate two-bit clean-XOR adder are now authored
and statically reviewed. The latter has one four-T fresh-target AND and one
measurement, compared with a direct seven-T Toffoli control. Its proposed
contracts preserve both inputs, XOR the modular sum into arbitrary output,
reset four fresh temporaries and retain an independent measurement record.
The adjoint channel uses fresh scratch and a new record. Eight fixed fixtures
and an independent Kraus evaluator are ready; they have not run during the
exclusive Stage C timing job. The analytic general-width recipe remains a
lifetime argument, without emitted 72-bit circuits or compiler cost credit.

A separate native-width implementation is now authored and statically reviewed.
It emits uncontrolled and coherently controlled 72-bit clean-XOR addition,
with explicit fresh-record adjoint channels. One shared caller-owned record
namespace reserves distinct classical results across composed invocations.
Its prospective 19-fixture packet includes small-width primitive phase and
reference checks, exact carry/lifetime bindings, native macro-level checks and
matched original Cuccaro unitary arrays. None has executed yet. Expected
counts of 564/1,565 T gates are still algebraic author-stage values, not
measured resource results. Both channels require 284 fresh scratch wires and
141 measurement/correction/reset slots; complete financial compiler and
physical runtime integration remain separate.
