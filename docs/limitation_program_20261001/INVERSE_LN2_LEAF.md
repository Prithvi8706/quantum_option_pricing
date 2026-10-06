# Generic inverse-ln(2) constant multiplier: standalone leaf result

Local A10 experiment, 1 October 2026. Coefficient `1586259972792`, 72-bit signed inputs, 40 fractional bits, zero_bits=0. The independent target is `floor(signed72(x)*c/2^40) mod2^72`, XORed into an arbitrary existing output, with input preservation and zero restored workspace. No zero-low or narrow input assumption is used.

The observed pytest run completed 11 tests with 0 failures, 0 errors and 0 skips. The historical default cmul was built once and compared byte-for-byte, including registers/resources, with the actual archived leaf. Production checks include nonzero low fractional bits, signed extrema and boundaries, negative floor rounding, 128 seeded full72 randoms, both gate directions, arbitrary outputs and XOR involution. Small-width checks exhaust every input and fractional width across the frozen coefficient family.

| Leaf | Qubits | T gates | T-depth | Clifford+T depth |
|---|---:|---:|---:|---:|
| Historical actual/default | 433 | 68,908 | 39,376 | 118,133 |
| binary-shift-add | 369 | 50,988 | 29,136 | 87,413 |
| signed-digit-shift-add | 369 | 40,544 | 23,168 | 69,517 |
| binary-carry-save | 4,386 | 38,948 | 1,792 | 5,378 |
| signed-digit-carry-save | 3,552 | 31,136 | 1,792 | 5,378 |

Leaf Pareto set: signed-digit-shift-add, signed-digit-carry-save. Selection for the complete financial source is unresolved. Larger carry-save workspace can change cap-limited packing; the quickest leaf is not automatically the quickest complete source.

The original coefficient is unchanged: this is exact integer lowering, with no new logarithm approximation or payoff/law change. Seven-T CCX/all-to-all logical accounting is the same convention used for the baseline. No physical time, estimator completion, continuous-price certification or quantum advantage follows from these leaf counts. The earlier zero-cost full-source screens are not credited as achieved reductions.

Next: compare the surviving leaves in fresh complete compact source schedules, preserving the latest accepted target, signed-seven-bit implementation and original caps. Only subsequent actual source resources and cleanup replays can select an adopted default. All work remained local.

Receipts: [summary](../../results/limitation_program_20261001/A10_inverse_leaf_run001/summary.json), [verification](../../results/limitation_program_20261001/A10_inverse_leaf_run001/verification.json), [candidate gates and prospective protocol](../../results/limitation_program_20261001/A10_inverse_leaf_run001/), [test/producer](../../research/limitation_program_20261001/test_inverse_ln2_multiplier.py).
