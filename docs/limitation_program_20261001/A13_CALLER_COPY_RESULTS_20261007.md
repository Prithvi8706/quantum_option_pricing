# A13: multiplier savings survive one caller shell

Both completed multipliers now pass the same caller shell, including 144 CX gates to copy the full 72-bit arguments and 144 CX gates to erase those copies. The complete leaf and its internal inverse remain charged. ROOT saved-result verification passed after independent review.

| Resource after caller copies and cleanup | Matched wide112 | Minimum65 |
|---|---:|---:|
| T gates | 43,414 | 42,098 |
| T-depth | 1,128 | 752 |
| Clifford+T depth | 2,930 | 2,037 |
| Allocated logical qubits | 3,850 | 3,568 |
| Native gate rows | 13,538 | 12,786 |
| CX gates | 7,110 | 6,640 |

The 33.33% T-depth reduction survives. Caller copies leave T count unchanged and add one Clifford+T layer to each variant. The common caller also adds 145 allocated wires: two full 72-bit input banks and one untouched spectator. Minimum65 uses 282 fewer qubits in this scope.

Each wrapper passed the original 64 forward and 64 literal-inverse cases on every allocated wire, preserving caller inputs and spectator and returning local/private workspace to zero. Three positive-first control categories reject swapped operand widths, wire aliasing and omitted cleanup. The omitted-cleanup example a=b=1 satisfies the component promise and is explicitly outside the financial second-operand hull. A separate absolute-phase composition witness uses the completed phase-one leaf proof and exact CX gates; the finite cases do not stand in for that universal proof.

The [sealed 11-file comparison](../../.context/a13_caller_copy_integration_20261007/actual_pair_run001/actual_caller_resources.json) has manifest hash `d21673e74ebf7afb77e5528c55e0ef45e3aa33e30eecb8bb7f4e9dfc00b518e0`. The independently reviewed [ROOT saved verification](../../.context/A13_V14_SINGLE_CALLER_COPY_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) passed with hash `2c53af378c7e3daab65d10d52d8833f7d85737f6ae828f0c891397b84d88dfb3`. Execution used 3.796875 process CPU seconds before sealing, approximately 3.992 seconds of wall time, and about 34.1 MB sampled resident memory under the original caps.

This verifies one ordered V14 caller shell. Matched wide112 remains the benchmark for this comparison; the actual original pricing-source multiplier must be bound separately before a source saving is claimed. Full 16-node integration, the other MUL leaves, selector/QROM, additions, outer output copy, financial cases and capped schedules remain separate tests. No whole-source G2 update, physical latency, adoption, shared fixture credit or quantum advantage is claimed. All files are local.

The subsequent [complete approximation-row comparison](A13_FULL16_ROW_RESULTS_20261007.md) now includes the selector, QROM, all sixteen nodes and cleanup, using the archived A10 leaf as its v14 reference. It measures a 1.50% whole-row T-depth saving from this single replacement. The original financial-certificate boundary remains open.
