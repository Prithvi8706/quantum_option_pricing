# Hardware implementation plan

These are planned local actions. Dependencies identify required input interfaces; a related investigation need not be fully solved to supply one. Existing evidence is preserved, and failed finite screens close only the tested branch.

## H01 Decoder latency is not universally tens of microseconds

**Status:** audit. **Priority:** 3. **Inputs:** G0, C15.

**Original point:** 3 hardware table; 5 root cause B. **Next action:** Make a versioned hardware timing table with explicit pulse, syndrome, decoder and feedback endpoints.

1. Recover each timing boundary from its figure/table.
2. Separate single-shot delay from sustained throughput.
3. Apply H18's whole-computation admissibility test.

**Alternatives:** Integrated FPGA reaction loop; Original surface-code projection retained as a separate scenario.

**Accept only when:**

- Every latency has a primary-source locator, date, code distance, logical error and demonstrated/projected label.
- No small-code result replaces an application-scale clock without an H18 failure check.

**Stop or change approach:** Screen the existing anchors plus at most two newer primary constructions; missing sustained-error data closes that substitution.

**If accepted:** Pass admissible timing records to H03/H17; retain old scenarios with their dates. **If rejected:** Mark unsupported replacements unavailable and continue with the bounded scenarios.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H01_<run>/`.

## H02 Fast standalone decoding is not the entire reaction loop

**Status:** audit. **Priority:** 3. **Inputs:** H01.

**Original point:** 3 hardware table; 5 root cause B. **Next action:** Build one end-to-end reaction-loop timeline from acquisition through transport, decoding and conditional pulse dispatch.

1. Identify link bandwidth and synchronization requirements.
2. Check whether feedback waits for one syndrome or many.
3. Export bottleneck and endpoints.

**Alternatives:** Integrated controller; Distributed decoder/controller model.

**Accept only when:**

- All serial stages are charged; overlap has a stated dependency reason.
- Kernel latency and complete reaction latency are distinct fields.

**Stop or change approach:** Stop after two complete timelines; an unmeasured link remains an explicit parameter, not zero.

**If accepted:** Feed the measured/projected loop into H03. **If rejected:** Retain a sensitivity interval; reject a claimed nanosecond layer based only on a kernel.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H02_<run>/`.

## H03 A code cycle and a logical T layer are different quantities

**Status:** ready. **Priority:** 2. **Inputs:** G0, H17.

**Original point:** 2.4; 3 hardware timing; 5 root cause B. **Next action:** Map a short signed multiply-add chain into reaction dependencies, independent of the code-cycle duration.

1. Choose a leaf already emitted in the latest library.
2. Construct a dependency timeline under each schedule.
3. Compare latency and qubits at equal failure allowance.

**Alternatives:** Conventional lattice surgery; Time-optimal teleportation with explicit prepared resources.

**Accept only when:**

- Every measurement that gates a later operation is represented.
- Count preparation, feedforward, connectivity and extra workspace; recover the original schedule as a control.

**Stop or change approach:** Compare two gate schedules for one leaf and one dependent chain; no whole-source credit before a compatible mapping exists.

**If accepted:** Scale the accepted mapping in H17 and check factory demand in H05/H06. **If rejected:** Keep the conventional mapping and record the failed assumptions.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H03_<run>/`.

## H04 Repeating distance-many syndrome rounds per operation is not mandatory in every architecture

**Status:** conditional. **Priority:** 4. **Inputs:** H03, H18.

**Original point:** 5 root cause B. **Next action:** Make an assumption-to-circuit checklist for a transversal fault-tolerance construction using one existing adder.

1. Identify gates unavailable transversally.
2. Charge their replacements.
3. Check whole-run failure and reaction dependencies.

**Alternatives:** Algorithmic fault tolerance; Conventional repeated syndrome extraction.

**Accept only when:**

- Transversal gate set, input magic-state quality, decoder, connectivity and accumulated failures satisfy the construction.
- Finite resources are recorded; constant rounds are not equated to a fixed nanosecond clock.

**Stop or change approach:** One finite adder mapping and one assumption audit; if a required decoder/gate is absent, defer scaling.

**If accepted:** Send the compatible gate schedule to H17. **If rejected:** Close this direct transfer and retain the missing-interface list.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H04_<run>/`.

## H05 Fifteen-to-one distillation is not the only magic-state supply

**Status:** ready. **Priority:** 2. **Inputs:** H17, H18.

**Original point:** 4 Failure 5 magic-state supply. **Next action:** Replace only the factory model for the actual T-state demand, keeping the computation and error allowance fixed.

1. Extract time-dependent magic-state demand from the circuit.
2. Size factories for peak/buffered demand.
3. Check rate, footprint and failures jointly.

**Alternatives:** 15-to-1 distillation baseline; Cultivation with usable-distance escape.

**Accept only when:**

- Record successful output rate, rejected attempts, footprint, transport and error per output.
- Factories, data and routing fit simultaneously; both schemes obey the same total failure allowance.

**Stop or change approach:** Compare two factories on one demand profile; absent finite noise/output data makes the cultivation result conditional.

**If accepted:** Integrate the winning compatible supply into H17. **If rejected:** Retain baseline supply and disclose which factory parameters are missing.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H05_<run>/`.

## H06 T-state supply and Toffoli-state supply must be matched to the circuit

**Status:** partial. **Priority:** 2. **Inputs:** H17, H18.

**Original point:** 3 arithmetic and factories; 4 Failure 5. **Next action:** Export separate CCX, T-rotation and Clifford demands before pricing native Toffoli supply.

1. Reconcile with existing native-CCX capacity sensitivity.
2. Lower the chosen leaf in both gate sets.
3. Recompute full scheduled demand rather than multiply claimed savings.

**Alternatives:** Exact seven-T CCX; Native CCZ/Toffoli factory or compatible catalysis.

**Accept only when:**

- One arithmetic CCX is charged exactly once; residual rotations still pay their synthesis demand.
- Native gate timing, workspace, state error and routing use one architecture.

**Stop or change approach:** Two lowerings for one leaf and one source; reject combinations that remove the same gate twice.

**If accepted:** Update H05/H17 with the matched state types. **If rejected:** Keep seven-T costs as the accepted baseline; native counts remain sensitivity data.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`; `research/controlled_priority_completion/capacity_screen.py`.

**New receipt:** `results/limitation_program_20261001/H06_<run>/`.

## H07 Distillation is not logically necessary for every non-Clifford implementation

**Status:** conditional. **Priority:** 4. **Inputs:** H18.

**Original point:** 3 non-Clifford operations; 5 root cause B. **Next action:** Translate one adder into a protected cat-qubit gate set and audit its noise assumptions.

1. Check gate identities locally on small registers.
2. Price every correction and protected operation.
3. Test the noise/error assumption ledger.

**Alternatives:** Bias-preserving direct non-Clifford gates; Distilled gate baseline.

**Accept only when:**

- Bias, leakage, nonadiabatic errors and physical gate durations are stated.
- The translated adder implements the same signed modular function and meets the allocated error.

**Stop or change approach:** One gate translation; if usable finite error/duration data are missing, stop before full-source extrapolation.

**If accepted:** Continue with the complete cat architecture in H08. **If rejected:** Leave a conditional architectural branch, not a demonstrated timing improvement.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H07_<run>/`.

## H08 An alternative physical qubit does not automatically eliminate all factories

**Status:** conditional. **Priority:** 4. **Inputs:** H07, H17, H18.

**Original point:** 5 root cause B; 6 new hardware. **Next action:** Insert the pricing leaf schedule into a complete cat architecture cost model.

1. Extract finite cost formulas from primary architecture evidence.
2. Map the same adder/multiplier chain.
3. Compare simultaneous space and latency.

**Alternatives:** Cat-qubit architecture; Surface-code baseline.

**Accept only when:**

- Include Toffoli preparation, teleportation, transport and idling.
- Use pricing's operation counts and failure budget, not a cryptographic workload's speedup.

**Stop or change approach:** One full leaf model; no source claim if gate costs cannot be composed at the actual connectivity.

**If accepted:** Add an independently labelled hardware scenario to H17. **If rejected:** Record the unavailable finite mapping and continue with supported architectures.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H08_<run>/`.

## H09 Surface-code physical-qubit overhead is not universal

**Status:** conditional. **Priority:** 4. **Inputs:** H15, H18.

**Original point:** 4 Failure 5 memory; 5 root cause B. **Next action:** Split the source allocation into stored data, active logic, ancillas and factories before substituting qLDPC storage.

1. Measure live storage after A18.
2. Choose finite code blocks.
3. Charge all movement between storage and active logic.

**Alternatives:** Surface-code storage; Bivariate-bicycle/qLDPC storage plus explicit active-gate interfaces.

**Accept only when:**

- Finite code blocks, connectivity, conversion costs and logical error are recorded.
- Storage savings exclude active arithmetic and factories unless those mappings are also supplied.

**Stop or change approach:** One finite allocation at each current B4/B8 cap; missing memory-to-logic conversion closes this direct integration.

**If accepted:** Hand the addressable operation interface to H10/H17. **If rejected:** Retain memory-only savings as a separate component result.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H09_<run>/`.

## H10 High-rate codes also have logical-operation research

**Status:** conditional. **Priority:** 4. **Inputs:** H09, H18.

**Original point:** 5 root cause B qLDPC. **Next action:** Map a 32-bit adder through one finite qLDPC logical-operation scheme.

1. Locate the scheme's gate primitives.
2. Lower each adder gate.
3. Include nonlocal operation and state-supply costs.

**Alternatives:** qLDPC Clifford operations plus explicit T mechanism; Surface-code active region.

**Accept only when:**

- Charge inter-block gates, addressability, measurements and code conversion.
- Count finite qubits and operation latency at the required failure rate.

**Stop or change approach:** One adder mapping; no full-source projection without a non-Clifford interface.

**If accepted:** Compare with H03/H17 using the same adder function. **If rejected:** Document the missing logic interface and stop this architecture transfer.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H10_<run>/`.

## H11 Addressable transversal non-Clifford gates are a distinct route

**Status:** conditional. **Priority:** 5. **Inputs:** H18.

**Original point:** 5 root cause B cheap non-Clifford gates. **Next action:** Find finite parameters for an addressable transversal-CCZ code and map one Toffoli-heavy leaf.

1. Expand theorem parameters.
2. Identify an admissible physical gate model.
3. Count extraction, idle and gate errors.

**Alternatives:** Addressable transversal CCZ; Native factory-produced CCZ.

**Accept only when:**

- Finite block size, stabilizer extraction and physical CCZ connectivity are available.
- The construction is not mislabeled LDPC; unused block qubits still count.

**Stop or change approach:** One finite parameter extraction; missing physical CCZ/error implementation makes the timing branch unavailable.

**If accepted:** Compare its compatible state demand and latency with H06. **If rejected:** Keep the coding-theory result separate from application cost.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H11_<run>/`.

## H12 Constant asymptotic overhead is not a small finite constant

**Status:** conditional. **Priority:** 5. **Inputs:** H18.

**Original point:** 5 root cause B; 7 resource frontier. **Next action:** Evaluate the additive-space and width conditions of a constant-overhead construction for the current source width/depth.

1. Insert actual width, depth and total fault probability.
2. Check the width inequality.
3. Expand finite code/noise costs or record their absence.

**Alternatives:** Finite theorem construction; Explicit surface-code baseline.

**Accept only when:**

- Compute n, F(n) and required width with the construction's constants.
- Missing constants remain unknown; asymptotic O(1) is never assigned an arbitrary numerical overhead.

**Stop or change approach:** One full-text finite-constant audit; if no usable construction/constants are supplied, close the numerical-transfer branch.

**If accepted:** Add a finite admissible scenario to H17 only if all conditions pass. **If rejected:** Record a theoretical alternative with no credited crossover.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H12_<run>/`.

## H13 Idle space can dominate a physical mapping

**Status:** conditional. **Priority:** 4. **Inputs:** H15, H18.

**Original point:** 4 Failure 5 memory; 5 root cause B. **Next action:** Lower one multiplier to active-volume blocks and compare idle storage and reaction depth at fixed resources.

1. Translate primitive gates to blocks.
2. Count memory dwell and reaction dependencies.
3. Compare under simultaneous data/factory capacity.

**Alternatives:** Active-volume architecture; Conventional logical layout.

**Accept only when:**

- Record memory, active volume, reaction depth and required nonlocal connections.
- All three bottlenecks are costed; lower active volume alone is not a latency gain.

**Stop or change approach:** One leaf plus one dependent chain; reject any unimplemented connectivity assumption for accepted timing.

**If accepted:** Extend a compatible mapping through H17. **If rejected:** Retain component volume results with explicit missing routing.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H13_<run>/`.

## H14 Photonic clock rates cannot be inserted directly as logical-layer rates

**Status:** conditional. **Priority:** 5. **Inputs:** H13, H18.

**Original point:** 7 logical-layer timing. **Next action:** Model photonic throughput and feedback delay independently for the same dependency chain.

1. Determine resource-state consumption.
2. Size optical buffers and generators.
3. Calculate latency, loss and sustained output together.

**Alternatives:** Interleaved photonic resource states; Nonphotonic baseline.

**Accept only when:**

- Emitter count, loss, buffer/delay length and decoder throughput are fixed.
- Optical clock rate is distinct from dependency latency; losses consume the total fault budget.

**Stop or change approach:** One finite resource-generator/delay scenario and one sensitivity interval; missing loss data defers transfer.

**If accepted:** Insert compatible throughput and reaction limits into H17. **If rejected:** Keep the architecture as a conditional route, with no GHz logical-layer substitution.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H14_<run>/`.

## H15 Millions of logical qubits in the emitted oracle are not an information lower bound

**Status:** partial. **Priority:** 1. **Inputs:** G0, A06.

**Original point:** 4 Failure 5 memory; 5 root cause E. **Next action:** Combine the exact compact SSA allocator with the accepted carry-save and ln(2) library and rebuild capped schedules; A18 is needed only for the later recomputation branch.

1. Reuse the existing exact compact-storage implementation.
2. Integrate the latest leaf scratch sizes.
3. Replay B4 and B8 before considering recomputation.

**Alternatives:** Exact bit packing; Reversible checkpointing when packing is insufficient.

**Accept only when:**

- Use the unchanged financial target and arbitrary output XOR; restore every input/workspace bit.
- Show depth/qubit Pareto results with actual recomputation, not a width estimate alone.

**Stop or change approach:** First run packing alone; then at most three checkpoint policies on one segment. Reject any claimed memory gain without a clean replay.

**If accepted:** Adopt compatible Pareto improvements via C13; expose affordable estimator lanes to E20. **If rejected:** Keep the accepted baseline and record the measured width/depth tradeoff.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`; `research/controlled_source_completion/compact_storage.py`; `docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md`.

**New receipt:** `results/limitation_program_20261001/H15_<run>/`.

## H16 Classical parallelism is inexpensive in this benchmark but not literally free

**Status:** ready. **Priority:** 2. **Inputs:** G0, C09.

**Original point:** 1 classical comparator; 5 root cause E. **Next action:** Measure classical scaling at 1, 2, 4, 8 and up to 16 available workers with identical contracts and seeds.

1. Freeze worker affinity and workload.
2. Record resource and machine information.
3. Repeat the prescribed timings with reference-price checks.

**Alternatives:** Compiled multicore RQMC; GPU only if already locally available and eligible.

**Accept only when:**

- Report setup, cold one-price time, warm repeated time and throughput separately.
- No linear scaling extrapolation beyond measured worker counts; tuning is charged consistently.

**Stop or change approach:** One fixed scaling grid; an unavailable GPU arm is marked unavailable rather than triggering a download/cloud job.

**If accepted:** Use measured scaling in G4 and E20 comparisons. **If rejected:** Report saturation/overhead honestly and retain the fastest eligible observed method.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`; `docs/research_investigation/2026-09-23/ERRATA.md`.

**New receipt:** `results/limitation_program_20261001/H16_<run>/`.

## H17 T depth alone does not determine runtime

**Status:** ready. **Priority:** 1. **Inputs:** G0.

**Original point:** 2.4; 3 timing; 4 Failures 4-6; 7 frontier. **Next action:** Create one resource ledger for the latest accepted source before attaching any estimator or hardware clock.

1. Hash the accepted libraries and schedules.
2. Extract demand by schedule batch.
3. Attach architecture inputs only with provenance and matching gate set.

**Alternatives:** Reaction/factory/routing bottleneck lower bound; Explicit compatible schedule for an achievable upper bound.

**Accept only when:**

- Reconcile CCX/T count, T-depth, total logical depth, scratch, memory and data movement.
- Label max(reaction,supply,routing,other) a lower bound, not an executable runtime.
- Keep B4/B8 knock-out and C4/H8 residual source families separate.

**Stop or change approach:** One ledger per source and at most three compatible architectures; missing routing produces an incomplete scenario.

**If accepted:** Combine G3, G4 and H18 into G5 using actually scheduled overlap. **If rejected:** Keep source-only L4 results and mark missing physical interfaces explicitly.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`; `results/limitation_audit_20261001/constant_multiplier_v1/summary.json`.

**New receipt:** `results/limitation_program_20261001/H17_<run>/`.

## H18 Error per operation must fall as the entire computation grows

**Status:** ready. **Priority:** 2. **Inputs:** C03.

**Original point:** 1 confidence; 5 root causes B and F. **Next action:** Compute required per-operation and per-magic-state failure from the entire estimator invocation schedule.

1. Start from delta/N per opportunity.
2. Partition code, state and control errors.
3. Replace provisional counts with the final estimator schedule.

**Alternatives:** Conservative union bound; A dependence-aware bound only with a justified theorem.

**Accept only when:**

- Allocate hardware failure within the total 0.01 and count every repeated source, reflection and state use.
- Choose code distance and state error jointly with latency and footprint.

**Stop or change approach:** Use a provisional count range until G3; reject any fast hardware row whose accumulated failure exceeds its allocation.

**If accepted:** Recompute H01-H14 admissibility and close G5 only for the complete compatible configuration. **If rejected:** Increase protection/reprice, or reject the hardware scenario without changing the financial confidence requirement.

**Existing evidence:** `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md`.

**New receipt:** `results/limitation_program_20261001/H18_<run>/`.
