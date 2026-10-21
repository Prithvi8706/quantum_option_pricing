# A13: verified minimum65 versus matched wide112 leaf

The exact signed 27-by-38-bit minimum65 multiplier has now passed a matched comparison with an independently emitted wide112 multiplier. Both implement the same full 72-bit dirty-output XOR, preserve the inputs, and erase the private workspace through a complete inverse. This is a standalone logical-resource comparison for the ordered `d4_s4` multiplication at original node 14 with arguments `[13, 5]`.

| Resource | Matched wide112 | Minimum65 | Reduction |
|---|---:|---:|---:|
| T gates | 43,414 | 42,098 | 3.03% |
| T-depth | 1,128 | 752 | 33.33% |
| Clifford+T depth | 2,929 | 2,036 | 30.49% |
| Allocated logical qubits | 3,705 | 3,423 | 7.61% |
| Native gate rows | 13,250 | 12,498 | 752 rows |

The [saved comparison](../../results/limitation_program_20261001/A13_d4_s4_v14_matched_wide112_run004/matched_min65_vs_wide112_resource_comparison.json) uses the same exact 15-event, seven-T CCX decomposition and conservative ASAP dependency conventions. The sealed packet reconciles 64 forward and 64 inverse all-wire cases, 900 scalar cases, four controls, and eight absolute-phase cases with separate structural proofs. These checks do not add shared fixture credit.

The [ROOT saved-result verification](../../.context/A13_D4_S4_V14_MATCHED_WIDE112_ACTUAL_RESULT_ROOT_VERIFICATION_run004.json), independently reviewed before execution, passed against the complete 35-file output packet, both saved input unions, exact review/READY provenance, and the original resource caps. Its manifest hash is `e1dd0629c7aac9a8cca8bd9591931110e497f4d776ed2c7b73d13ab21b6756bf`; the final ROOT verification hash is `5e933040ae05eaa7350bb6caa3cfb8b84ebf60ad53cbf228347d381d86f3a062`.

The earlier CPU-censored V3 attempt remains immutable. V4 retained the numerical science and caps while removing a repeated path observation already covered by the fresh input-union loop. A subsequent saved-checker failure was confined to two missing original-input byte-size checks; an additive checker repair passed independent review and verified the existing successful SCI packet. The scientific run was not repeated for that bookkeeping repair.

Caller argument copies are excluded from these standalone resource rows. The next [caller-copy comparison](A13_CALLER_COPY_RESULTS_20261007.md) has now completed and passed saved verification with all 288 copy/cleanup CX gates included. Its T-depth reduction remains 33.33%; Clifford+T depths become 2,037 versus 2,930 and qubit counts become 3,568 versus 3,850. Full pricing-source integration and a direct comparison to its actual original multiplier remain separate tests. No whole-source reduction, new financial certificate, physical latency, or quantum advantage follows from this leaf comparison. All work is local.

The subsequent [complete approximation-row comparison](A13_FULL16_ROW_RESULTS_20261007.md) binds the archived A10 leaf as v14 reference and measures all selector/QROM/graph/copy/cleanup costs. Its single-replacement T-depth saving is 1.50% across the new candidate row. Original degree-twelve financial recertification remains a separate obligation.
