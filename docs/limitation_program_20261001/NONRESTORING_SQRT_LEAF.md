# Exact non-restoring square-root leaf

The candidate matches `out XOR isqrt(unsigned(input)<<40)` for every unsigned46 input, including bit45. The native input and arbitrary XOR output remain 72 bits. All stored signed remainders, root work, the modular-adder operand and its helper are reversed and erased after the result copy.

| Actual emitted resource | Accepted tight digit-by-digit root | Non-restoring candidate |
|---|---:|---:|
| Qubits | 2,350 | 2,213 |
| T gates | 219,128 | 54,180 |
| T-depth | 105,582 | 30,960 |
| Clifford+T depth | 312,836 | 93,052 |

The [prospectively frozen leaf receipt](../../results/limitation_program_20261001/A11_nonrestoring_leaf_run001/summary.json) passed **28 distinct tests**. Checks exhaust small native widths1–6 across active widths and supported fractional counts, every legal input and arbitrary output word, forward and inverse execution, and workspace/input restoration. Production checks include zero, one input quantum, maximum input, the highest active bit, adjacent perfect-square boundaries, 128 seeded inputs, and exact comparison with Python `isqrt` and the accepted root. Native24/40/72 fixtures and invalid-domain controls are included.

The recurrence uses one unconditional Cuccaro modular add per radix-four digit. A sign-dependent operand represents either `-(4Q+1)` or `+(4Q+3)`. The next root bit depends only on the completed remainder's sign. The [research context and invariant](NONRESTORING_RESEARCH_CONTEXT.md) explain why temporary modular overflow is legal and why final signs remain exact. The implementation keeps all44 signed45-bit remainder registers until the literal inverse; no remainder storage or cleanup is omitted.

The candidate improves all four matched resource dimensions and qualifies for source screening. That leaf result alone does not establish full-source adoption, physical runtime or quantum advantage. Actual SSA input guards, preserved native copies and adopted shifts, complete capped scheduling, financial replays and independent auditing remain required.
