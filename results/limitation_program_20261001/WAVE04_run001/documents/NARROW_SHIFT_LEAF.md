# Exact signed7-count shift leaf

The specialized shift keeps two native 72-bit inputs and a full 72-bit output XOR. Only the count calculation uses seven bits, under an explicit proved sign-extension contract. A positive count performs a modular left shift; a negative count performs an arithmetic right shift. The count is an unscaled signed integer, independent of the 40 fractional data bits.

| Resource | Archived full-count shift | Signed7 candidate |
|---|---:|---:|
| Native and workspace qubits | 1,735 | 807 |
| T gates | 37,100 | 8,162 |
| T-depth | 8,736 | 4,481 |
| Clifford+T depth | 24,108 | 15,329 |

These are actual emitted leaf arrays under the existing exact seven-T Toffoli and logical all-to-all scheduling model. Component measurements cannot be substituted for full-source or physical runtime gains.

The circuit copies the data into workspace, conditionally reverses its bits for a negative count, computes the unsigned count magnitude, and uses one left-shift barrel. Incoming bits equal the original data sign for a negative count and zero otherwise. A final conditional reversal restores the direction. It copies every result bit into the arbitrary output word, then literally reverses the complete computation. The minimum count `-64` has unsigned magnitude `64`; it never becomes a signed negative magnitude. The same construction handles oversized shifts exactly for smaller data widths.

The prospectively frozen [leaf receipt](../../results/limitation_program_20261001/A07_shift_leaf_run001/summary.json) passed **27 distinct tests**. These include 1,176,528 exhaustive small-word forward/inverse checks, 70,912 production forward/inverse checks across all 128 counts and 277 data patterns, archived-leaf equivalence, native interface and dirty output checks, oversized small-word shifts, magnitude and mux identities, and invalid count promises. Input registers and every private workspace bit are checked after execution.

The leaf alone cannot authorize specialization. Integration must prove the range at the actual count SSA value, retain generic fallback bytes when the proof fails, and keep both native argument-copy costs. Full capped source screening, financial replay when eligible, and independent cost reconciliation are separate requirements. G2-G5 and the wider A07 limitation remain open. All work is local.
