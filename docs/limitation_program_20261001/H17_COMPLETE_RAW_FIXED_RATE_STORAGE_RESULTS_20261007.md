# Complete raw caller fixed-rate256 exact conditional storage

The verified complete signed raw clip/upstream/fused-row/shift demand now has exact conditional minimum storage at fixed hypothetical usable rate256 per logical step. The T-coordinate and Clifford+T-coordinate are isolated models with zero prefill and arrival-overflow-consume ordering; they are not converted into each other or physical time.

| Isolated logical coordinate | Exact capacity | Attaining necessity interval | One-less first miss | Unserved |
|---|---:|---|---:|---:|
|logical_ASAP_Clifford_T_layer|2638|34111 to 34150|34150|1|
|logical_ASAP_T_layer|15491|12139 to 12184|12184|1|

The T interval carries27011 demands and11520 arrivals strictly after its first step; the CT interval carries12622 and9984. The initial arrival is excluded from extra-capacity accounting. Each attaining interval witnesses necessity; the saved complete at-minimum feasible record and one-less first starvation certify exactness. ROOT checked saved scalar/conservation/first-miss identities without rerunning a capacity scan, demand trajectory, producer or control. The saved horizon domain47129/134698 and total1539118 belong to the new complete raw caller.

Capacities15491/2638 equal the older fused-scope results, but the wholecaller horizons, source and bindings changed. No matched storage saving or quantified improvement is inferred. Earlier88 fixed-grid failures, old row-only/fused scopes and every failed artifact remain preserved.

The sole SCI exited0 in 1.9686155 wall seconds and sealed9 files/52362 bytes. Preseal CPU/wall/RSS were 1.703125 seconds/1.6553360000252724 seconds/38682624 bytes, under original process caps. Exact terminal CPU is unavailable. Current26 source/model definitions,121 selected-role original stat8 identities,127 cache absences and parent9 inventory remained bound. Independent SOURCE/final FIELD and ROOT saved verification passed.

The rate is hypothetical usable accepted-state supply. Physical clock, factory yield/noise, transport, storage quality, architecture and compatible full-program scheduling are not proved. Neither G5, physical buffer feasibility, hardware adoption, global fixture nor quantum advantage is promoted. The next work is compatible physical delivery evidence and the original financial time-average/path/payoff error chain.

Evidence: [ROOT receipt](../../.context/H17_COMPLETE_RAW_FIXED_RATE256_MINIMUM_STORAGE_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json), [final independent FIELD](../../.context/H17_COMPLETE_RAW_FIXED_RATE256_MINIMUM_STORAGE_SAVED_VERIFIER_INDEPENDENT_FIELD_PEER_run001.json), [manifest](../../.context/complete_raw_fixed_rate_storage_20261007/actual_minimum_run001/manifest.json), [T-coordinate witness](../../.context/complete_raw_fixed_rate_storage_20261007/actual_minimum_run001/logical_T_coordinate_minimum_storage.json), [CT-coordinate witness](../../.context/complete_raw_fixed_rate_storage_20261007/actual_minimum_run001/logical_Clifford_T_coordinate_minimum_storage.json), [complete raw demand](H17_COMPLETE_RAW_CALLER_DEMAND_RESULTS_20261007.md) and [combined32 checkpoint](../../.context/OVERNIGHT_CONTINUATION_CHECKPOINT_20261007_run020.json). ROOT SHA256: `246346d2a62d02596f5c91629341f6afe6b77f464a33feca16d90ff7e85b4e1f`.
