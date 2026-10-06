# First signed leaf: minimum80 product with explicit sign extension

The local experiment passed for the first ordered signed38 by signed42 leaf. Computing the complete 80-bit product and explicitly extending its computed sign preserves the original signed144/floor40/full72 output semantics. ROOT verified all 60 owned files. The original 64 forward cases, 64 actual inverse cases, 900 scalar pairs, four fixed controls, and eight exact phase columns passed.

| Complete standalone resource | Original112 | Minimum80 |
| --- | ---: | ---: |
| Native rows | 19,908 | 19,396 |
| Allocated qubits | 5,362 | 5,170 |
| T gates | 66,822 | 65,926 |
| ASAP T-depth | 1,216 | 960 |
| Clifford+T depth | 3,193 | 2,585 |

T-depth improved by 21.1%, T work by 1.34%, and storage by 3.58%. Both resource columns include full computation, all 72 dirty-output copies, and the complete inverse. Caller argument copies remain separately owed. The comparison reads the immutable original producer and independent-audit resource records; it does not regenerate or replay an old comparison array.

The shorter product retains all low40 carries. Product bits40 through79 feed output bits0 through39, and the computed product bit79 feeds each remaining high output bit. This restores negative arithmetic-floor results, including negative nonmultiples, without using operand-sign XOR at zero. Exhaustive small scalar pairs include the case where the product width is no greater than the fractional width. The fourth control rejects omitted or corrupted high sign-copy plans.

The producer finished at 123.625 CPU seconds and 140.51 wall seconds under the unchanged 180/150/600 limits. Its saved packet retains all 11 original input-owner maps and histories. The separate independent scientific audit also passed at 130.484375 CPU seconds and 138.60 wall seconds. It reconstructed every saved gate row and allocation, the full signed product and output extension, all 64 forward/inverse cases, 900 scalar pairs, four controls, eight absolute-phase columns, and the resource ledger. ROOT verified all 18 audit files. The audit retains 12 current owner maps and the distinct historical producer scopes.

The other five leaves, caller copies, full polynomial/source integration, capped schedule, G2, cost comparison, and adoption remain open. The next ordered signed38 by signed40 leaf has a separately reviewed minimum78 design. No quantum advantage or new fixture credit follows from this standalone result.

Evidence: [sealed manifest](../../results/limitation_program_20261001/A13_d4_s4_first_signed_leaf_min80_run001/manifest.json), [actual comparison](../../results/limitation_program_20261001/A13_d4_s4_first_signed_leaf_min80_run001/actual_minimum80_vs_saved112_resources.json), and [ROOT verification](../../.context/A13_D4_S4_FIRST_SIGNED_LEAF_MIN80_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json).

Independent audit: [sealed manifest](../../results/limitation_program_20261001/A13_d4_s4_first_signed_leaf_min80_audit_run001/manifest.json) and [ROOT verification](../../.context/A13_D4_S4_FIRST_SIGNED_LEAF_MIN80_INDEPENDENT_AUDIT_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json).
