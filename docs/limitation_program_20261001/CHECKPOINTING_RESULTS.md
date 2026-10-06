# Paid checkpointing on the real financial source

The bounded A18 experiment retains a verified workspace tradeoff. One actual first-date, first-asset Gaussian-plus-Estrin-exponential closure uses **22,831 instead of 29,130 logical qubits**, reducing total subgraph allocation by **21.6238%**. It costs **6.3488 times the T work** and **5.9799 times the T depth**. The exact financial function, precision, input law, masks and leaf bytes remain unchanged.

The saving survives one full B4 integration: **365,630 rather than 371,929 qubits** against the matched retain-all control, a checkpoint contribution of **6,299 qubits (1.6936%)**. The full checkpoint point costs **26.2782% more T work** and **25.1087% more T depth** than that control. It remains a nondominated logical workspace alternative; the accepted parallel coefficient source remains the preferred latency source.

## Frozen scope and resource caps

The original financial builder was instrumented to identify its first stock exponential, followed by complete equality of its optimized graph with the accepted B4 target. Structural fingerprints map the chosen stock to SSA4021 and its clipped log to SSA3579. Extraction includes all 159 atomic producer groups and 181 produced values in its ancestor closure. Every outgoing edge is preserved, including shared constants/normals and atomic lookup siblings; 28 protected boundary values receive separate full 72-bit output destinations.

All 60 original 32-bit random-input registers remain allocated: 1,920 qubits. Together with 2,016 boundary-output qubits, the fixed floor is **F=3,936**. Retain-all transient workspace is **W0=25,194**: 10,405 active intermediate qubits plus 14,789 private native leaf qubits. Argument copy registers and unused high output bits are included in that private cost.

The prospective total caps were F+floor(0.75W0)=**22,831** and F+floor(0.50W0)=**16,533**. An independently checked mandatory move needs at least **19,445** qubits. Its lookup coefficient belongs to an atomic eight-output group, so counting only one coefficient would understate the predecessor floor. Both 50% attempts are therefore infeasible before any circuit is emitted.

The random inputs have 2**32 midpoint values per coordinate. The coefficient lookup has 32 rows. These are different quantities.

## Four declared attempts

| Method / workspace cap | Result | Actual qubits | T gates | T-depth | Clifford+T depth |
|---|---|---:|---:|---:|---:|
| Retain-all control | Measured reference |29,130|13,113,506|407,232|1,281,196|
| Block checkpointing /75% | Verified nondominated point |22,831|83,254,388|2,435,202|7,593,794|
| Block checkpointing /50% | Mandatory-leaf lower bound exceeds cap |—|—|—|—|
| Cost-aware recursive eviction /75% | Search exhausted; no executable circuit |—|—|—|—|
| Cost-aware recursive eviction /50% | Mandatory-leaf lower bound exceeds cap |—|—|—|—|

Block checkpointing uses 13-group blocks in the original topological order. Cross-block dependencies are protected or reconstructed through paid invocations. The successful circuit contains **1,058 computes and 1,058 erases**, including **899 recomputations**, plus 28 boundary copies. Every compute and erase requires its predecessor groups live. Slots are reused only after their actual gate inverse clears them. Repeated arguments have separate copied native registers. Physical span highwater and live allocation both fit the declared cap.

The failed cost-aware search recorded **100,013 checks against a 100,000 bound**: 100,000 admitted checks followed by 13 over-limit abort checks during exception unwinding. This is a budget-accounting deviation on a failed, nonexecutable attempt. Its partial plan is discarded and the receipt is preserved. A separate versioned scheduler corrects terminal budget propagation; ten tiny fixture tests passed. It was not applied to the financial subgraph again, and no fifth candidate attempt was added.

## One full B4 integration

The extracted clean subroutine produces its protected boundary values, computes all outside calls, copies the full native pricing output, reverses every outside call and runs the clean subroutine again to erase the boundary copies. Both complete subroutine invocations are charged. The control uses the identical outside allocations and execution order with the retain-all subroutine. One bank is reused between extracted workspace and outside private scratch; the maximum, rather than the sum of percentage savings, determines the actual global allocation.

| Full B4 source | Logical qubits | T gates | T-depth | Clifford+T depth |
|---|---:|---:|---:|---:|
| Preferred accepted parallel latency source |550,141|520,720,662|555,774|1,661,253|
| Matched serial integration / retain-all subroutine |371,929|533,834,168|16,153,504|50,118,829|
| Matched serial integration / paid checkpoint subroutine |365,630|674,115,932|20,209,444|62,744,025|

The combined serial/checkpoint layout uses **33.5389% fewer qubits** than the preferred parallel source, with **29.4583% more T work** and **36.3627 times its T depth**. Most of that memory difference comes from the declared serial private-workspace packing. The isolated checkpoint contribution remains 6,299 qubits against the matched control. These figures are logical all-to-all circuit costs under exact seven-T Toffoli expansion; they do not establish lower physical pricing latency.

## Verification and next work

**80 new distinct tests passed**: 58 scope/scheduler/circuit fixtures, 12 full-integration fixtures and 10 future-budget fixtures. Exhaustive small-word cases exercise dirty outputs, repeated arguments, aliases, atomic lookup outputs and clean inverses. Adversarial cases reject missing predecessors, dirty overwrites, missing external dependencies, insufficient caps and tampered allocations/bindings.

Three actual extracted subgraph gate replays checked every computed value against the original exact integer trace and all 28 dirty full 72-bit outputs. Three separate complete B4 pricing replays passed on the saved random, all-zero and positive-payoff vectors, with full input, checkpoint, boundary and scratch restoration. Subgraph replays are not counted as complete financial replays. Program totals are **852 distinct tests and 41 complete financial gate replays**.

Independent audits freshly scanned 55 actual subgraph arrays and 60 actual B4 arrays in both forward and literal-inverse directions, reconstructed original dependencies/compact widths, and reconciled every allocation, copy, work/depth charge and frontier decision. B8 was not run. Existing code and receipts were preserved; all work remained local.

This addresses the tested intermediate-memory component of A18. Broader memory/physical constraints remain. G2 continuous-dollar certification, G3 a compatible 99% estimator, G4 matched classical timing and G5 physical runtime are still open; quantum advantage is unproved. Next is the bounded [A19 reversible streaming harness](NEXT_STREAMING.md): two assets, four dates and two checkpoint placements, preserving the exact monitored arithmetic-basket payoff and paid cleanup.

Evidence: [subgraph protocol/results](../../results/limitation_program_20261001/A18_run001/summary.json), [subgraph audit](../../results/limitation_program_20261001/A01_run015/summary.json), [one B4 integration](../../results/limitation_program_20261001/A18_B4_run001/summary.json), [full B4 audit](../../results/limitation_program_20261001/A01_run016/summary.json), [future budget fix](../../results/limitation_program_20261001/A18_budgetfix_run001/summary.json).
