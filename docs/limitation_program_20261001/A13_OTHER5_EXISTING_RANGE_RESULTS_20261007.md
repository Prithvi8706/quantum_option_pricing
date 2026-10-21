# A13: existing range multipliers reduce the complete candidate row

The five remaining products can use the archived ordered40x72 multiplier on their complete proved input domains. The complete row passed its local circuit run and independent saved verification. This replacement saves34.4128% of T gates,11.7292% of T-depth,12.6942% of Clifford+T depth and31.2471% of allocated logical qubits against the previously verified minimum65-v14 row.

| Complete candidate row | Previous minimum65-v14 row | Other five range replacements |
|---|---:|---:|
| T gates | 2,179,772 | 1,429,652 |
| T-depth | 34,103 | 30,103 |
| Clifford+T depth | 94,531 | 82,531 |
| Logical qubits | 17,240 | 11,853 |
| Native gate rows | 639,266 | 424,966 |
| CX gates | 324,898 | 217,158 |
| CCX gates | 311,396 | 204,236 |

The re-emitted baseline exactly matches the [previous complete-row certificate](A13_FULL16_ROW_RESULTS_20261007.md) in gate-array SHA256, byte count and every integer resource field. Minimum65 remains at v14 in both variants. The changed products are v6,v8,v10,v11,v13, whose original ordered signed widths are38x42,38x40,38x38,34x41 and34x34. Their entire first-operand hulls fit signed40 and their second-operand hulls fit signed72. No operand swap, runtime width selection or sample-only width argument is used.

All shared full72 external ports, SSA banks, selector,24-word coefficient/center QROM, center subtraction, argument copies/uncopies, dirty output and literal whole-row inverse remain charged. Private scratch is allocated from leaves actually used in each variant and reused only after complete leaf cleanup. Removing the unused full72 multiplier from that maximum saves5,387 wires. Square inputs retain separate ordered local copies, and all leaf wire maps are injective.

Both variants passed64 fixed forward and64 literal-inverse cases on every allocated wire, with private workspace clean and inputs/spectator preserved. Each variant has its own state commitment because the workspace lengths differ; no equality between differently sized state hashes is asserted. Four positive-first control categories cover promised width order, square-copy aliasing, cleanup and selector equality. The complete native-domain/absolute-phase composition argument remains separate from finite basis tests.

With the earlier v14 replacement included, this row uses39.3440% fewer T gates,13.0549% less T-depth and13.7976% less Clifford+T depth than the first assembled degree-four reference using the archived40x72 v14 and full72 other products. These are comparisons within the same new approximation graph. They do not compare against the original A10 degree-twelve pricing program.

The [sealed thirteen-file packet](../../.context/a13_full16_existing_range_20261007/actual_pair_run001/manifest.json) has manifest SHA256 `6003e4f0303006dfc408851f6428b3027eb00574b344ea85a94013ca5392d838`. The independently reviewed [ROOT saved verification](../../.context/A13_D4_S4_FULL16_EXISTING_RANGE_OTHER5_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) passed with SHA256 `cefc995350aa79c68b7efb3ad88a6f0ce212f1792be4d43701de1bf37ba21986`. The [rounded display](../../.context/A13_OTHER5_VERIFIED_ROUNDED_DISPLAY_run001.json) derives percentages solely from saved verified integer counts.

Execution completed once with externally observed exit zero under the original CPU180/admission150, wall600,150MiB resident-memory and128MiB output caps. The saved verifier checks current output hashes,190 selected authority roles,107 cache absences, original62-file component membership,37 current source bodies, mappings, saved tests, counts and baseline identity. It SHA-streams the two new arrays without decoding them; it does not reopen the five original arrays or the previous output arrays, simulate circuits or recalculate resource schedules.

The next accuracy obligation is to bind the realized selector/table/graph to the existing selected approximation-error certificate and then join one actual first-stock caller: remainder3982 through candidate output15 and the source's signed exponent3979 shift to stock4021. Candidate alpha/beta require their own exact join; the old degree-twelve error certificate does not transfer automatically. Whole pricing costs, source-site extrapolation, hardware delivery, full financial G2 and quantum advantage remain open. All files and runs are local.
