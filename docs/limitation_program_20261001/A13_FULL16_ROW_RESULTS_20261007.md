# A13: complete approximation-row cost after one replacement

The complete four-segment, degree-four exponential approximation row passed its local circuit test and independent saved-result review. Replacing only v14 with the completed minimum65 multiplier reduces whole-row T count by 7.51859%, T-depth by 1.50189%, and Clifford+T depth by 1.26383%. Both variants allocate 17,240 logical qubits.

| Complete row resource | Archived40x72 v14 reference | Minimum65 v14 |
|---|---:|---:|
| T gates | 2,356,984 | 2,179,772 |
| T-depth | 34,623 | 34,103 |
| Clifford+T depth | 95,741 | 94,531 |
| Logical qubits | 17,240 | 17,240 |
| Native gate rows | 689,690 | 639,266 |
| CX gates | 349,818 | 324,898 |
| CCX gates | 336,712 | 311,396 |

Both variants include the signed selector, the 24 full-word center/coefficient QROM values, center subtraction, all sixteen graph nodes, eleven native leaf calls, full72 argument copies and uncopies for each call, shared private scratch, the dirty outer output copy, and the literal inverse of the complete computation. Each CCX is charged under the same exact ordered fifteen-event, seven-T macro. The verified scheduling transition is equivalent to that macro; the run does not claim to have iterated every macro event literally.

The reference uses the actual archived A10 range40x72 leaf at v14, with the other five products still using their full72 native leaves. This reference is a newly assembled degree-four candidate graph. It is distinct from the [matched-wide112 standalone benchmark](A13_MATCHED112_RESULTS_20261007.md) and [single caller-copy comparison](A13_CALLER_COPY_RESULTS_20261007.md), and from the original A10 degree-twelve pricing row. The standalone 33.33% T-depth gain therefore does not describe this whole row.

Both variants passed the fixed 64 forward and 64 literal-inverse basis cases on every allocated wire, including dirty outputs, input preservation, spectator preservation, and private-workspace cleanup. Four positive-first control categories cover selector, promised leaf contract, wire aliasing, and cleanup. Those finite cases are separate from the component/domain/injective-wire-map proof used for absolute-phase composition. The saved verifier checks the recorded cases, source and domain joins, hashes, count identities and qualifications; it does not rerun the oracle or recalculate scheduling depths.

The [sealed thirteen-file packet](../../.context/a13_full16_row_integration_20261007/actual_pair_run002/manifest.json) has manifest SHA256 `6e7a84527193dfcf4e0824c1830ad59a543aad206cad2de1b08dbd4322f3c9e4`. The independently reviewed [ROOT saved verification](../../.context/A13_D4_S4_FULL16_SINGLE_ROW_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json) passed with SHA256 `21a5c9cd69cebdc1fed23dc4cfe2eeeb2f65c59cdbe3ba3726e7d98d08091662`. Rounded percentages come only from the saved integer counts in the [verified display](../../.context/A13_FULL16_ROW_VERIFIED_ROUNDED_DISPLAY_run002.json).

ROOT observed exit zero. Saved preseal process CPU was 13.671875 seconds, wall time 14.2124661 seconds, and maximum sampled resident memory 54,075,392 bytes. External terminal wall time was approximately 14.563 seconds; exact terminal CPU is unknown. The original CPU180/admission150, wall600 and 150MiB resident-memory caps remained in force.

The first controller was held before execution for a missing `stat` import. Its narrow successor retained all 37 function/class bodies and the complete library. The first finalized saved checker was separately held for assuming an optional descriptor field; the corrected checker validates the actual original width72/F40 descriptor contract. Both holds and their files remain preserved. The successful scientific circuit run was performed once.

The next bounded test substitutes the existing archived40x72 leaf for the other five products, whose ordered proven widths are38x42,38x40,38x38,34x41 and34x34. Its baseline must reproduce the current minimum65-v14 row's gate bytes and integer resources. Private scratch must be sized from leaves actually used in each variant, with common full72 ports and graph unchanged. No next-candidate resource result is credited here.

The original financial G2/E11 certificate does not automatically transfer to this alternate approximation. Whole pricing-source cost, 48/416-site savings, hardware delivery, adoption and quantum advantage remain open. All tests and files are local.
## Subsequent verified replacement

The [five remaining range replacements](A13_OTHER5_EXISTING_RANGE_RESULTS_20261007.md) are now ROOT saved-verified. Their baseline reproduces this candidate's array and resources exactly. The resulting complete degree-four row uses1,429,652 T gates, T-depth30,103 and11,853 logical qubits; its candidate-specific financial accuracy join is next.
