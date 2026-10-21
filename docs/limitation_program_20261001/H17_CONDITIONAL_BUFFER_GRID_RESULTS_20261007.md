# H17: conditional usable-state arrivals and finite buffers

The completed minimum65 leaf's verified logical demand histograms now have an independently checked, sealed 88-scenario buffer-grid result. The [ROOT saved-result verification](../../.context/H17_CONDITIONAL_USABLE_SUPPLY_BUFFER_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) passed after the actual run exited zero. Its nine-file packet contains 119,614 bytes; the verifier checked the saved first-miss, prefix-supply, count and conservation identities without rerunning the buffer trajectories, grid or original circuit.

The two clocks remain separate: 752 logical T layers and 2,036 logical Clifford+T layers. Each scenario starts with zero inventory and assumes an explicitly hypothetical constant rate of already usable T-family states. At integer boundary `t`, arrivals are `floor(r*t) - floor(r*(t-1))`; the order is **arrival, discard overflow, consume demand**. There is no free prefill, inferred factory yield or CCZ-to-T conversion. The T-dagger Clifford/frame premise remains required.

The fixed grid tests eleven rates—1/4, 1/2, 1, 2, 4, 8, 16, 32, 64, 128 and 256—at capacities 16, 64, 256 and 1,024 in each clock. The following entries are the smallest passing **tested** rates, in usable states per layer of the named coordinate. “None” means no tested rate passed.

| Buffer capacity | T-layer coordinate | Clifford+T-layer coordinate |
| --- | --- | --- |
| 16 | None | None |
| 64 | None | None |
| 256 | 256 | 64 |
| 1,024 | 256 | 64 |

Two of the 44 T-coordinate scenarios passed; six of the 44 Clifford+T-coordinate scenarios passed. The rates in these columns are different logical units and cannot be compared as physical factory rates. The grid establishes neither a continuous optimum nor behavior outside its declared points.

The small-capacity failures have a concrete explanation within this boundary convention. The recorded peak demands are 252 T states in a T layer and 79 in a Clifford+T layer. Inventory available after overflow is at most the buffer capacity, so capacities 16 and 64 cannot serve these batches, even with larger simultaneous arrivals. This is a conditional consequence of the fixed schedule and batching rule, not a universal physical buffer lower bound. An unlimited-buffer cumulative-supply prefix test is necessary but can still miss losses caused by finite-buffer overflow.

The run retained the original caps: 180 process-CPU seconds, 150 admission-CPU seconds, 600 wall seconds, 150 MiB resident memory and 32 MiB total outputs. The recorded preseal observation was 0.90625 CPU seconds and 0.881117 wall seconds; the external terminal observation was 1.0894484 wall seconds. Exact terminal CPU time was not recorded. These are software observations, not hardware execution estimates.

Physical clock durations, usable-state acceptance probabilities, transport delay, state errors, storage lifetime and noise, and the complete estimator's repetition schedule remain required. H05/H17 and G5 remain open. This packet gives zero shared scientific fixture credit and proves no hardware adoption or quantum advantage.

The [saved summary](../../.context/h17_conditional_supply_20261007/actual_grid_run001/summary.json), [fixed arrival grid](../../.context/h17_conditional_supply_20261007/actual_grid_run001/hypothetical_constant_usable_arrival_grid.json), [independent recurrence checks](../../.context/h17_conditional_supply_20261007/actual_grid_run001/independent_recurrence_checker.json) and [qualification](../../.context/h17_conditional_supply_20261007/actual_grid_run001/qualification.json) record the exact scope. The earlier [delivery-interface results](H05_H17_DELIVERY_INTERFACE_RESULTS_20261007.md) describe the underlying deadlines, conservation rules and independently verified demand extraction.

The ROOT receipt's SHA256 is `8ef2e285b0d63e00912e284829882349a47e75601153d7195ee28087aa8c276e`; the sealed manifest's SHA256 is `08c4d131f044ca543ab5659dd1d82aaf2d6897f1d4fb5387305b1513191e19c5`. All work remains local. No frozen research packet was changed and nothing was pushed.
