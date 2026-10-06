# Guarded constant integration: independent tests and review

Local review, 1 October 2026. **All 16 integration tests passed in 9.03 seconds.** They exercise the emitted gates for small complete graphs at the production 72-bit/40-fractional-bit precision, using independent Python integer formulas for expected results. This confirms the new library's guarded logarithm dispatch, unchanged fallback and optional general-constant interface. It is not a complete B4/B8 replay or a resource/runtime result.

## What was checked

The canonical graph implements a signed guard, highest-bit index, subtraction of 40, left shift by 40 and multiplication by the positive integer ln(2) coefficient 762123384786. For each nonnegative power-of-two boundary through bit 70, the preceding word and the power itself are checked; zero, the negative sign boundary and the all-one word are included. The independent reference uses:

~~~text
guarded = max(signed72(raw_input), 1)
q = bit_length(guarded) - 1 - 40
output = q * 762123384786 mod 2^72
~~~

Every reachable exponent from -40 through 30 occurs. The graph retains full-width named outputs for the result, an alias, exponent and guarded input. Outputs begin with arbitrary nonzero 72-bit words. Every emitted result matches output XOR with the independent integer value, and all inputs/workspace are restored.

Dispatch and fallback tests additionally establish:

- A changed offset, coefficient or guard shape keeps the original arithmetic leaf, key, metadata bytes and gate bytes.
- The identical ln(2) coefficient in the exponential range-reduction chain remains a wider fallback. Test inputs include range-reduction values outside signed seven bits.
- An unrestricted ln(2) operand is not narrowed from its coefficient alone.
- An explicitly selected inverse-ln(2) general replacement uses the contract zero_low_bits=0 and matches floor(signed72(x)*coefficient/2^40), modulo 2^72, including nonzero low bits and signed extremes.
- ln(2) cannot be forced through the general replacement map. Original target/source semantic mismatches, later changed nodes and foreign output IDs are rejected.
- Forged signed-seven-bit contracts on exponential leaves, unsupported signed widths, missing zero-low premises, changed cached contracts and corrupt cached gate files are rejected.

These are functional integration tests. The larger numerical caps used for the small graphs avoid treating workspace availability as part of the arithmetic assertion. Production-budget selection belongs to the separate complete-source experiment.

## Independent arithmetic and interface review

The logarithm proof gives a seven-bit signed q. Its product with the positive coefficient fits signed 47 bits over the entire promised interval [-64,63], including both endpoints. The 47-bit child therefore computes the original result exactly. Its sign extension to the 72-bit output is copied from the computed product before cleanup, preserving arbitrary output XOR. The high input sign-extension bits are redundant under this theorem; they are not promised zero.

The library snapshots and validates the same SSA graph before dispatch. Original source inputs, outputs, operation parameters, lookup literals and gate hashes are checked. A structural logarithm proof is attached to the actual call; exponential and unclassified ln(2) calls retain their original bytes. General replacements have no narrowed-input promise. Cache keys include strategy, precision, coefficient, lowering and contract; reloaded metadata, gate hash and resource fields are checked.

No signed-arithmetic, structural-proof, dispatch or cache correctness issue was found within this interface. At the reviewed revision, the library validates the archived full-width contiguous input/output-register layout and deliberately rejects other archived layouts. The compact executor separately supports nonuniform metadata. Integrating a new one-bit output leaf into this library would need an explicit compatibility update and tests.

This review credits no additional SSA storage narrowing, full-source gain, financial error certificate or quantum advantage.

## Reproduction and observed receipt

Run from the repository root in the existing pinned environment:

~~~powershell
.context/frontier_t0_env/Scripts/python.exe -m pytest research/limitation_program_20261001/test_constant_integration.py -q
~~~

Observed output:

~~~text
................                                                         [100%]
16 passed in 9.03s
~~~

Ruff and git diff whitespace checks passed for the new test file. No package installation, production B4/B8 gate replay, progress-file edit or remote action was performed.

Reviewed SHA-256 snapshots:

| File | SHA-256 |
|---|---|
| constant_library.py | fec444607c3232b01a1194e0401dd5c8e141dbe47af45f61394651e1570bda69 |
| log_constant_multiplier.py | 3aa552a1f59b51b2cdbd3e6f1338378456405520bd40d98449284f9a23a9137f |
| test_constant_integration.py | 21c9c723cc350388ad45459bbcbef2346cc45cb7511e817e36d3aa6ade510d9c |

Implementation: [constant_library.py](../../research/limitation_program_20261001/constant_library.py), [log_constant_multiplier.py](../../research/controlled_source_completion/log_constant_multiplier.py). Tests: [test_constant_integration.py](../../research/limitation_program_20261001/test_constant_integration.py). Same-graph proof: [prove_log_exponent.py](../../research/limitation_program_20261001/prove_log_exponent.py) and [A07 result](../../results/limitation_program_20261001/A07_run001/result.json).
