# Complete-row conditional finite-buffer result

All88 preregistered complete-row buffer scenarios failed. This is a verified negative result for the stated local model. It identifies burst and storage obstructions that aggregate supply totals miss.

| Separate logical coordinate | Tested scenarios | Passed | Failed |
|---|---|---|---|
| ASAP T layer |44|0|44|
| ASAP Clifford+T layer |44|0|44|

The fixed grid uses rates1/4,1/2,1,2,4,8,16,32,64,128,256 usable T-family states per unit of the separately named logical coordinate, and capacities16,64,256,1024. Initial inventory is zero. At each timestamp arrivals floor(r*t)-floor(r*(t-1)) occur first, overflow is discarded, then demand consumes inventory. Failed scenarios stop at their first miss; future deliveries and physical clocks are not invented. The two clocks have no common physical calibration.

The T-coordinate peak batch is1266, greater than the grid's maximum buffer1024. Under arrival-overflow-consume batching, the capacity bound alone prevents serving that batch. In the Clifford+T coordinate the peak is428, yet even rate256 and capacity1024 fail. Its saved first miss is at logical step13982: demand328, served256, unserved72. The unlimited-buffer prefix condition passes for that scenario; finite storage discards earlier surplus and does not sustain the later burst. Recorded overflow discarded through that miss is3472296 states. This directly demonstrates that unlimited prefix supply is necessary but insufficient.

The original model's only input guard change accepts the saved82531-step Clifford+T horizon rather than stopping at32768. Its recurrences, rate/capacity grid, CPU180/admission150/wall600,150MiB RSS and32MiB output limits are unchanged. The actual run used6.75 preseal CPU seconds and34525184 sampled peak RSS bytes; ROOT observed scientific exit0 after7.2117752 wall seconds. The nine sealed files passed independent saved verification, including original histogram totals, provenance, first-miss identities, conservation and the saved procedural/closed-form reconciliation. The saved checker does not reconstruct a trajectory or rerun the grid.

Retain the entire failed grid. A future bounded alternative must separately preregister a larger buffer, burst-sensitive supply or changed schedule and charge its consequences. Do not alter this completed grid or label a higher logical rate as an available physical factory. Physical layer duration, usable-state quality, yield, transport, storage noise, correction cost and full-estimator compatibility remain open. No fixture, hardware feasibility or quantum advantage credit is added.

The [sealed manifest](../../.context/h17_full_row_conditional_supply_20261007/actual_grid_run001/manifest.json) has SHA2567288296d10afb9ab94609ce3a5071baf98499f4117742e7890b52cab4ecf7b6a. The [ROOT saved verification](../../.context/H17_FULL16_CONDITIONAL_USABLE_SUPPLY_BUFFER_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) has SHA256`34af20bbad6b7a84554de4f3fba61110523ffbd9906fd2744bb446645db4913f`. The [saved display](../../.context/E11_CANDIDATE_H17_FULLROW_VERIFIED_SAVED_DISPLAY_run001.json) keeps both coordinates separate. All work remains local.
