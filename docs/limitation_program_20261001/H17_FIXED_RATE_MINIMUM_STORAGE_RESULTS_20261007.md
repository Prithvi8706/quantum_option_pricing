# Exact minimum buffer storage at fixed logical supply

The earlier complete-row grid failed all88 scenarios. A separate follow-up now certifies the exact minimum storage needed at hypothetical rate256 usable T-family states per step of each isolated logical coordinate. Both capacities succeed for their entire saved horizons; reducing either capacity by one causes a one-state shortage.

| Separate coordinate | Exact minimum states stored | Attaining demand interval | First miss with one less state | Shortage |
|---|---:|---|---:|---:|
| ASAP T layer | 15,491 | 5290 through 5335 | 5335 | 1 |
| ASAP Clifford+T layer | 2,638 | 13959 through 13998 | 13998 | 1 |

The convention remains zero initial inventory, arrival first, capacity overflow discarded, then batch consumption. These are two separate logical clocks with no physical conversion. The new declared capacity domain is0 through1,429,652; the original grid capacities16,64,256,1024 and all its failures remain frozen.

For arrivals A and demand D, let S_t be cumulative arrivals minus demand, H_t = S_(t-1) + A_t, and P_t the maximum of zero and H_1 through H_t. With sufficient unlimited-buffer prefixes, exact minimum capacity is max_t(P_t - S_t). The independent interval argument needs capacity at least the demand in j through t minus arrivals strictly after j. Excluding the first arrival is essential because usable stock immediately before demand j is already bounded by capacity.

The T-coordinate witness contains27,011 demanded states against11,520 later arrivals, proving the15,491-state lower bound. The Clifford+T witness contains12,622 demanded states against9,984 later arrivals, proving the2,638-state lower bound. Saved full-horizon feasibility at those bounds proves attainability. At15,490, T step5335 demands381 but serves380; at2,637, Clifford+T step13998 demands373 but serves372. Thus the burst/storage obstruction in the earlier grid has a precise conditional solution at this fixed rate.

The SOURCE also reconciles independent peak/interval formulas with the procedural buffer model. The independent FIELD and ROOT saved checker validate the recorded attaining interval, complete feasibility flags, conservation and one-less misses without rerunning trajectories or scanning capacities. All9 sealed files and122 original selected identities are checked. Scientific preseal CPU was1.234375 seconds; ROOT observed exit0 after1.5960269 wall seconds under unchanged CPU180/admission150/wall600 and150MiB RSS caps. ROOT saved receipt SHA256 is `6845b69274a90a22adbc9f9c074c301495d6938c77a27fa86e79afa2103df82a`.

This solves the mathematical storage requirement for the stated logical supply assumption. Physical layer duration, factory yield, state fidelity, routing, noise during storage, correction cost and full-estimator compatibility still need compatible evidence. A higher storage number alone does not establish a feasible physical architecture or quantum advantage. Rate optimization and changed scheduling are separate experiments; no whole-limitation or global fixture credit is added.

The [original failed grid](H17_FULL_ROW_CONDITIONAL_BUFFER_RESULTS_20261007.md), [new sealed manifest](../../.context/h17_full_row_fixed_rate_storage_20261007/actual_minimum_run001/manifest.json) and [ROOT saved verification](../../.context/H17_FULL16_FIXED_RATE256_MINIMUM_STORAGE_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) preserve both results. Everything remains local.
