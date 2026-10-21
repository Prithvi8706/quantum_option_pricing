# H05/H17: usable-state delivery and finite buffers

An executable local interface now checks whether explicitly declared usable T and CCZ deliveries meet every demand deadline within separate finite buffers. It charges rejected attempts and overflow, and adds transport delay before a delivery becomes available. Its times are abstract ticks; no physical production rate, state quality or storage lifetime is supplied by this model.

The [implementation](../../.context/hardware_delivery_interface_20261007/delivery_interface.py) passed [18 ordinary unit tests](../../.context/hardware_delivery_interface_20261007/test_results.json). The [independent ROOT review](../../.context/hardware_delivery_interface_20261007/root_independent_review.json) additionally checked 432 small schedules against a closed cumulative-prefix bound, finite-buffer inventory conservation, and 36 permutations of a mixed T/CCZ event schedule. These are artificial software checks, with zero shared scientific fixture credit.

Two useful counterexamples were reproduced:

- Six delivered T states can match six demanded states overall and still miss an early demand by three states.
- A schedule can pass every unbounded cumulative-supply prefix and still fail when a capacity-one buffer discards one of two states before consumption.

The declared same-time convention admits deliveries, discards excess inventory, then consumes demand. All simultaneous demands for the same state kind are combined. CCZ inventory supplies no T states without a separately specified conversion. Accepted delivery counts are premises about already usable states; attempted counts alone create no inventory.

The completed minimum65 pricing leaf now has a [sealed logical demand packet](../../.context/circuit_demand_bridge_20261007/actual_min65_run002/summary.json), with an [independently reviewed saved-result verification](../../.context/H05_H17_MIN65_LOGICAL_DEMAND_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json). Its 12,498 native rows expand to 96,694 macro events and 42,098 T gates. The two dependency coordinates reproduce the saved depths: 752 T layers and 2,036 Clifford+T layers. Peak demands are 252 T states in a T layer and 79 in a Clifford+T layer. The last T demand occurs at Clifford+T layer 2,035; the final Clifford layer is still charged.

The first runner stopped at its Windows command predicate before reading inputs or producing outputs. Its frozen failure remains recorded. A narrow second version corrected the base-Python versus venv-launcher distinction, then completed under the original caps. The saved verifier checks recorded dependencies, all macro groups, per-wire frontiers and demand histograms without rerunning the native circuit. Neither version changes the original scientific source.

The histograms now have a [completed 88-scenario conditional buffer grid](H17_CONDITIONAL_BUFFER_GRID_RESULTS_20261007.md), with a [passed ROOT saved-result verification](../../.context/H17_CONDITIONAL_USABLE_SUPPLY_BUFFER_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json). The grid tests explicitly hypothetical usable-state arrivals and finite buffer capacities in one logical coordinate at a time, with zero prefill. Physical clocks, factory acceptance probabilities, transport, state errors, storage errors, and full-estimator repetitions remain required inputs. H05/H17 and G5 remain open.

All files and tests were produced locally. No existing frozen research packet was changed and nothing was pushed.
