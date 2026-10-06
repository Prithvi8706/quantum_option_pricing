# Hardware alternatives and the cost assumptions they change

Investigation date: 1 October 2026. This memo dissects the hardware, space and latency statements in sections 2 through 7 of [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md). It is a targeted primary-source investigation, not a complete survey of every platform.

Several component barriers have established alternatives. None of the checked sources supplies a complete implementation of this project's pricing oracle at its required confidence, error and resource budget. This distinction prevents improvements from unrelated machines being multiplied together into a fictional machine.

## H01 Decoder latency is not universally tens of microseconds

**Original:** section 3 hardware table and root cause B. **Alternative:** integrated FPGA decoding and feedback. Yang et al. report 550 ns from the end of the readout pulse to the start of feedback, on a distance-3 surface code, with a 1.25 microsecond QEC cycle. This is an experiment, but its error rates and code size do not establish application-scale fault tolerance. **Status:** the broad latency statement needs updating; the pricing bottleneck remains. **Small test:** record timing endpoints, distance, logical error rate and sustained throughput separately before considering any resource-model substitution. [Full paper, figure 1 and sections IV and VI](https://arxiv.org/html/2605.04892v1).

## H02 Fast standalone decoding is not the entire reaction loop

**Original:** root cause B treats decoder reaction as a bottleneck. **Alternative:** integrated control/network designs. Liu et al. measure a 446 ns decoding-feedback pipeline on a three-board distance-3 prototype; their larger-distance latency is an extrapolation. This is different evidence from a live processor executing a long universal computation. **Status:** an engineering component has improved. **Small test:** include syndrome aggregation, transport and feedback dispatch rather than using the decoder kernel time alone. [Full paper, system evaluation](https://arxiv.org/html/2603.16203v1).

## H03 A code cycle and a logical T layer are different quantities

**Original:** sections 2.4, 3 and 5B. **Alternative:** operation-specific scheduling, including gate teleportation and delayed corrections. Fowler's time-optimal construction can remove distance-proportional waiting under its preparation, measurement and fast-classical-processing assumptions. **Status:** a universal identity between code distance and every logical gate latency is false; an actual pricing schedule is absent. **Small test:** map one dependent multiply-add chain and record measurements that must await earlier outcomes. [Fowler, Time-optimal quantum computation](https://arxiv.org/pdf/1210.4626).

## H04 Repeating distance-many syndrome rounds per operation is not mandatory in every architecture

**Original:** root cause B's explanation of error-correction overhead. **Alternative:** transversal algorithmic fault tolerance. Zhou et al. give a theorem and circuit-level simulations for constant extraction rounds with suitable transversal operations, magic-state inputs, feedforward and decoding. **Status:** solved in a specified fault-tolerance model; no automatic nanosecond gate claim. **Small test:** map a short arithmetic circuit and inspect whether its decoder and connectivity meet the construction's assumptions. [Full paper, theorem 1 and hardware considerations](https://arxiv.org/html/2406.17653v2).

## H05 Fifteen-to-one distillation is not the only magic-state supply

**Original:** Failure 5's factory supply calculation. **Alternative:** magic-state cultivation. Gidney, Shutty and Jones report simulated preparation with substantially lower spacetime costs under specified noise models, including the escape to a usable code distance. **Status:** a concrete alternative factory model, not evidence that factories are free. **Small test:** replace only the factory model, retain the computation's state demand and required error per state, and include rejected attempts and output transport. [Full paper, results and conventions](https://arxiv.org/html/2409.17595v1).

## H06 T-state supply and Toffoli-state supply must be matched to the circuit

**Original:** Failure 5 and the seven-T arithmetic decomposition. **Alternative:** a native CCZ/Toffoli implementation, catalysis or a direct Toffoli factory. The local repository already has a native-CCX sensitivity in [capacity_screen.py](../../research/controlled_priority_completion/capacity_screen.py). **Status:** partly already assessed, not a new factor to stack on top of its result. **Small test:** preserve distinct counts of arithmetic CCX and synthesized rotations; price each with a compatible supply model. The same T gate must not be eliminated once by native compilation and again by a factory improvement.

## H07 Distillation is not logically necessary for every non-Clifford implementation

**Original:** section 3's account of expensive T and Toffoli gates. **Alternatives:** repetition-cat constructions and direct protected non-Clifford operations. Guillaud and Mirrahimi propose bias-preserving logical gate constructions that avoid the usual distillation route. **Status:** a conditional architectural alternative, not a universally demonstrated replacement. **Small test:** translate one adder into its protected gate set, including biased-noise assumptions and nonadiabatic errors. [Original construction](https://arxiv.org/abs/1904.09474), [resource and error analysis](https://arxiv.org/abs/2009.10756).

## H08 An alternative physical qubit does not automatically eliminate all factories

**Original:** root cause B and the hardware-announcement row in section 6. **Alternative:** complete cat-qubit architectural accounting. Gouzien et al.'s cryptographic estimate includes Toffoli preparation, teleportation and routing despite using cat qubits. **Status:** useful evidence of a different cost balance, with a different workload. **Small test:** borrow the gate-cost methodology, not its cryptographic speedup; insert this application's actual gate schedule and failure allowance. [Architecture analysis](https://arxiv.org/abs/2302.06639).

## H09 Surface-code physical-qubit overhead is not universal

**Original:** Failure 5's physical-cap failure and root cause B. **Alternative:** high-rate qLDPC storage, including bivariate-bicycle codes. Bravyi et al. provide low-overhead memory constructions. **Status:** storage overhead can improve, but memory alone does not price universal arithmetic. **Small test:** separate stored data, active computation, ancillas, decoding, connectivity and non-Clifford supply. [High-threshold and low-overhead fault-tolerant quantum memory](https://arxiv.org/html/2308.07915).

## H10 High-rate codes also have logical-operation research

**Original:** the caution that qLDPC counts need a separate gate schedule is appropriate, but should not imply such schedules are absent everywhere. **Alternative:** code families supporting efficient Clifford operations, combined with mechanisms for T gates. **Status:** partial progress toward computation, not just storage. **Small test:** map the addressability and operation sequence of a 32-bit adder; charge inter-block operations explicitly. [Computing efficiently in QLDPC codes](https://www.nature.com/articles/s41467-026-73061-9).

## H11 Addressable transversal non-Clifford gates are a distinct route

**Original:** root cause B. **Alternative:** He et al. construct codes with addressable transversal CCZ gates. The checked construction is not an LDPC code; its good asymptotic parameters do not determine finite-device cost. **Status:** a solved coding-theory subproblem under the paper's conditions. **Small test:** determine finite block length, stabilizer measurement cost, physical CCZ implementation and required connectivity before crediting a Toffoli speedup. [Full paper, theorem 1.1 and discussion](https://arxiv.org/html/2502.01864).

## H12 Constant asymptotic overhead is not a small finite constant

**Original:** root cause B and section 7's qubit requirements. **Alternative:** constant-space-overhead fault-tolerance theorems, including the September 2026 logarithmic-time result. Its space bound is `O(W + F(n))`; constant overhead requires the explicit width condition `W >= C_F F(n)`, with `n = Theta(log(WD/epsilon))`. **Status:** an asymptotic route with an additive space term and a width condition; no finite pricing crossover extracted here. **Small test:** check that condition and expand code-size and noise-threshold constants for a specified circuit width W and depth D. Stop the transfer when no usable finite construction is supplied. [Purely-logarithmic-time and constant-space-overhead fault-tolerant quantum computation](https://arxiv.org/html/2609.28461v1).

## H13 Idle space can dominate a physical mapping

**Original:** Failure 5's memory and capacity objections. **Alternative:** active-volume architectures that use limited nonlocal connectivity to reduce idle spacetime cost. The required metrics are logical memory, active volume and reaction depth, rather than T count alone. **Status:** an architectural construction; memory and reaction bottlenecks remain separately. **Small test:** lower one arithmetic leaf to active-volume blocks and compare at a fixed physical resource budget. [Litinski and Nickerson, active-volume architecture](https://arxiv.org/html/2211.15465).

## H14 Photonic clock rates cannot be inserted directly as logical-layer rates

**Original:** section 7's clock requirements. **Alternative:** photonic interleaving and resource-state production can trade storage against throughput. In the active-volume construction, delay length also affects reaction time. **Status:** potential architecture-specific improvements, not a free GHz logical clock. **Small test:** hold the number of emitters/resource generators, loss, memory delay and decoder fixed; calculate both throughput and dependency latency. [Architecture and photonic implementation](https://arxiv.org/html/2211.15465).

## H15 Millions of logical qubits in the emitted oracle are not an information lower bound

**Original:** Failure 5 and root cause E. **Alternative:** liveness-aware allocation, reversible checkpointing and fused arithmetic. [Stage A](../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md) explicitly says its schedules retain SSA intermediates. **Status:** the current width failure is real; its necessity is unproved. **Small test:** impose a logical-qubit cap on one path segment and produce a valid recomputation schedule. Report the added time, not just the smaller peak memory. Arithmetic alternatives are developed in [the companion memo](ARITHMETIC_AND_LOADING.md).

## H16 Classical parallelism is inexpensive in this benchmark but not literally free

**Original:** root cause E. **Alternative:** compare at stated latency and resource budgets, separately reporting throughput, setup and amortization. Quantum parallel estimation must likewise pay for its lanes and entangling operations. **Status:** an accounting correction; no symmetry of hardware costs is assumed. **Small test:** use measured multicore scaling rather than multiplying single-core throughput without limit. Compare cold one-price latency and warm repeated-price latency separately. [Existing warm-cost correction](../research_investigation/2026-09-23/ERRATA.md), [parallel estimation analysis](ESTIMATION_AND_CERTIFICATION.md).

## H17 T depth alone does not determine runtime

**Original:** section 2's depth budget and sections 4 and 7's sensitivity requirements. **Alternative:** architecture-aware scheduling. Even a zero-T Clifford circuit takes physical operations and communication. **Status:** the original identity is useful within its simplified model; it is not a complete runtime model. **Small test:** report T count, T depth, total logical depth, reactive measurement depth, workspace and routing separately. The 2025 acceleration study gives relevant architecture-dependent examples. [The Fast for the Curious](https://arxiv.org/pdf/2510.26078).

## H18 Error per operation must fall as the entire computation grows

**Original:** confidence requirements and projected factories are discussed separately. **Alternative:** join logical failure, factory error and estimation error in one declared allowance. **Status:** standard error-budget accounting, incomplete in this pricing comparison. **Small test:** for a schedule with N failure opportunities and allocated fault probability delta, start with the conservative requirement p <= delta/N, then use justified dependence-aware refinements. This is a union-bound calculation, not a hardware prediction. A faster small-code experiment is inadmissible if its error accumulates beyond the total allowance.

## How to combine improvements without inventing a speedup

For a specified circuit and architecture, an optimistic diagnostic is

`T_Q >= T_setup + max(D_react * t_react, N_magic / R_magic, T_routing, T_other_dependencies)`.

The maximum is a lower bound on execution time under overlapping resource constraints, not a generally achievable schedule. Some tasks cannot overlap and need additional time. Physical qubits must cover data, workspace, factories and routing simultaneously. The complete estimator multiplies or repeats only the appropriate parts of this schedule.

Three implications follow. Reducing factory cost does not speed a reaction-limited computation by the same factor. Reducing width may add recomputation depth. Replacing arithmetic can alter both the number and type of required magic states. Each combination therefore needs a newly costed schedule.

The historical score of about 900,000 T layers is not the best current emitted evidence. Stage A reports clean scheduled depths of 6,032,678 and 6,393,144 for its two generic knock-out circuits. Those figures still omit a completed physical implementation and financial-law certification. Comparisons in this audit preserve that distinction.

## Search scope and source access

Searches covered feedback decoders, time-optimal computation, algorithmic fault tolerance, cultivation, cat-qubit arithmetic, qLDPC memory and logic, addressable CCZ, constant-overhead constructions and active-volume architectures. Full primary texts were opened for the central claims. The cat-code overview entries include abstract-level primary records and the published architectural analysis; no fine-grained gate timing was inferred from their abstracts. Newly found 2026 theories remain theories unless explicitly identified as experiments.

Individual vendor layer timings in the original table were not all rebenchmarked or independently refreshed here. They must retain their original platform and experimental definitions; they do not support a universal lower bound. An omitted architecture is an unreviewed candidate, not a negative result.
