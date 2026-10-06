# Investigating the quantum advantage limitations one component at a time

Research date: 1 October 2026. The starting document is [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md). This audit asks, for each small obstruction, whether another area has solved that component, what assumptions the solution needs, and whether it can improve this project's unchanged pricing task.

**Execution follow-up:** The user authorized trying the alternatives. [Executed results and retained fixes](EXECUTION_RESULTS.md) records eight scoped experiments: all seven questions in the queue below, plus a multiplier follow-up. The default 32-row lookup is now cheaper and exact; a carry-save backend with memory-capped scheduling substantially improves the full arithmetic circuits. Conditional and failed candidates remain explicitly labelled. The sections below preserve the original literature-pass scope.

**Latest local follow-up:** [Exact ln(2) constant multiplication](CONSTANT_MULTIPLIER_RESULT.md) removes another avoidable arithmetic cost. Four implementations were compared; the retained signed-digit carry-save leaf reduces complete-source T-depth by a further 12.5% and 12.4% under the same qubit budgets. Signed tests and complete gate replays passed. Combined depth gains against Stage A are now 2.48× and 2.44×; full pricing advantage remains unestablished.

**Plan for continued local execution:** [Implementation plan for every limitation](IMPLEMENTATION_PLAN.md) turns all 110 scoped points into experiments, proofs and audits with dependencies, acceptance checks, stopping rules and pass/fail follow-ups. It covers every substantive part of the foundation document and defines how to continue without repeated run requests.

**The first finding is that several listed costs are avoidable implementation choices. The full pricing advantage remains unestablished.** A useful investigation must preserve both facts. We have completed a detailed first research pass covering the original document's limitation families, with **110 individually scoped entries**, plus one executed circuit experiment. Some entries revisit the same obstruction from different interfaces; they are not 110 independent barriers or independent literature confirmations.

The original manuscript and its result artifacts are unchanged. This is a separate research record. Current emitted-source evidence comes from [Stage A](../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md), with reproduction qualifications from [Stage B](../../manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md) and the [errata](../research_investigation/2026-09-23/ERRATA.md). Existing Stage C work was not rerun or replaced.

## Start with the completed small result

[Removing reverse Toffoli gates from temporary AND cleanup](FIRST_COMPONENT_RESULT.md) isolates a single operation. We independently verified that measurement plus phase correction can erase an eligible temporary AND without a reverse Toffoli. Both measurement branches agree with the coherent reference operation, including inputs entangled with a reference.

This saves seven T gates for that eligible cleanup under the existing exact-Toffoli lowering. It introduces measurement and feedforward. It does not yet change the production compiler or establish full-source latency savings. The derivation, runnable script, negative control and result receipt are linked from the report.

## The research record

| File | Entries | What is broken into smaller questions |
|---|---:|---|
| [Arithmetic and loading](ARITHMETIC_AND_LOADING.md) | A01–A20, 20 | Uniform randomness, Gaussian conversion, direct state preparation, tensor networks, precision, range proofs, adders, multipliers, roots, division, exponentials, CORDIC, QROM, cleanup, controls, memory and streaming paths |
| [Estimation and certification](ESTIMATION_AND_CERTIFICATION.md) | E01–E25, 25 | Access-model limits, the hidden k constant, variance versus range, QFT, control factoring, fusion, confidence allocation, unknown moments, digital-law certification, nested estimation, heavy tails, multiple outputs, Greeks, parallel AE and QSP |
| [Formulations and classical comparators](FORMULATIONS_AND_CLASSICAL_COMPARATORS.md) | F01–F32, 32 | RQMC rates, smoothness, structured integration, Sobol circuits, barrier switching surfaces, rare events, changes of measure, MLMC, Heston exact transitions, quantum fast-forwarding, nesting, controls, rough volatility, PDEs, tensor methods and quantum walks |
| [Hardware and cost models](HARDWARE_AND_COST_MODEL.md) | H01–H18, 18 | Feedback, logical timing, algorithmic fault tolerance, factories, native CCZ, cat qubits, qLDPC, addressable gates, asymptotic overhead, active volume, photonics, storage, parallelism and complete failure budgets |
| [Price requirements and evidence](CONTRACT_AND_EVIDENCE.md) | C01–C15, 15 | The output, dollars, confidence, tenfold threshold, error allocation, continuous-law bridge, barrier flips, fitted exponents, timing, comparator completeness and unsupported universal conclusions |

Each research entry identifies its original location, a precise obstacle, alternatives and sources, its current status, transfer conditions, and a small experiment or proof obligation. Primary-source access depth is disclosed. Some leads have only an abstract-level check; they are not treated as established transfer results.

## What solved means in this investigation

| Status | Meaning |
|---|---|
| Already implemented here | The idea cannot be counted again as a future improvement |
| Component solved in the literature | A construction or theorem exists for that subproblem under stated conditions |
| Verified in this audit | A specifically described calculation or test was executed here |
| Conditional for this project | A missing assumption, interface, certificate or cost comparison prevents transfer |
| Different task | The proposed benefit changes the payoff, model, output or accuracy requirement |
| Not established by this search | No applicable solution was verified in this bounded search; this is not a claim that none exists |

No source is labelled a complete pricing solution merely because it demonstrates a quantum primitive, improves another quantum implementation, or proves a query bound.

## Important changes to the working picture

1. **Controlling every arithmetic gate is not an outstanding obstacle in the current wrappers.** That factoring is already implemented. See E05 and A17; it corrects the explanation but contributes no new arithmetic speedup.
2. **Equal forward and cleanup T cost is not fundamental.** The executed first component result makes this concrete. See A16 and the linked experiment.
3. **Box–Muller and permanent 72-bit intermediates are replaceable choices.** Direct Gaussian preparation, exact narrow metadata, different arithmetic and reversible memory scheduling are separate candidates. See A01–A19.
4. **The original QSP scope is too narrow.** Its applicability must be checked against the actual payoff structure. See E22 and A20, rather than treating all multi-date/multi-asset payoffs as a single class.
5. **The moment-certification cost belongs to particular estimators.** Alternative estimators and stopping requirements are separated in E09–E12; a variance theorem is not automatically a dollar-error certificate.
6. **Heston time stepping has a concrete alternative worth an assumption audit.** F14–F15 distinguish exact transitions and a 2026 quantum fast-forwarding construction. Passing one parameter condition does not establish model compatibility.
7. **Shared control variates are not automatically disqualified.** F20 derives the condition under which a shared rewrite improves the relative comparison by making the coherent source sufficiently cheaper.
8. **Hardware claims need their timing boundaries.** H01–H04 separate decoding, feedback, extraction cycles and logical gates. Faster component evidence is useful without being inserted as an unsupported complete logical clock.
9. **The claim that another factor of about 100 is all that remains is not a proved ceiling.** A compatible emitted combination is required to establish either an improvement or its limit. See A20's follow-on discussion and C13.
10. **Classical cubic precision cost and absence of structure are not necessary conditions for advantage.** The actual complete-time inequality decides the case. See F16, F31 and C14.

These findings reopen individual design choices. They do not reverse the archived results for the implementations actually tested.

## Coverage of the original document

| Original part | Where its limitations are investigated |
|---|---|
| Introduction and evidence levels | C11–C12, C15; status definitions above |
| Section 1, scalar price and accuracy | C01–C05, E07, E18–E21 |
| Section 1, strong classical comparator | C08–C10, F01–F07, F18, F30 |
| Section 2.1, sampling law and k | E01–E03, E07–E10, E16–E17, E24 |
| Section 2.2, coherent-to-classical cost ratio | F02, F20, H03, H17, C04, C13–C14 |
| Section 2.3, RQMC removes exponent room | F01–F05, E01, C08 |
| Section 2.4, depth budget | E02–E03, H03, H16–H18, C04–C05 |
| Section 2.5, historical numerical example | C04, C09, C11; Stage A substitution; H17 |
| Section 3, random preparation and 468 normals | A01–A05 |
| Section 3, precision and arithmetic leaves | A06–A15 |
| Section 3, uncomputation and control | A16–A17, E05–E06; first component result |
| Section 3, hardware table and physical overhead | H01–H14, H17–H18, C15 |
| Failure 1, shared antithetic benefit | F10, F20 |
| Failure 1, dominating base level | F11 |
| Failure 1, costly Heston step | A08–A14, F14–F15 |
| Failure 1, Feller and variance-rate failure | F12–F13, F15 |
| Failure 2, classical factor reuse and policy bracket | F16–F17 |
| Failure 2, nested complexity and source calls | E14–E15, F18–F19 |
| Failure 3, shared residual variance and source expense | F08, F20, A13, A20, E03 |
| Failure 3, moment certification | E09–E12 |
| Failure 4, large source | A01–A20, E06, C11 |
| Failure 4, estimator constants | E02–E08, E14–E15, E24–E25 |
| Failure 5, optimized estimator and arithmetic | E08, A07–A10, A15–A19, C13 |
| Failure 5, factory supply and memory | H05–H15, A18–A19 |
| Failure 6, limited smoothing | F01–F07, C08–C10 |
| Failure 6, score versus emitted circuit | C07, C11, C15; Stage A |
| Failure 6, corners, free normals and mismatched variance | A01–A05, E03, F02, C13 |
| Failure 6, extreme-accuracy extrapolation | C02, C08, F31 |
| Root cause A, query ceiling and structured alternatives | E01, E16–E17, F04–F05, F09, F18–F19, F32 |
| Root cause B, hardware | H01–H14, H17–H18 |
| Root cause C, reversible arithmetic | A06–A20, E22–E23 |
| Root cause D, classical structure | F01–F04, F08, F10–F20, F30 |
| Root cause E, parallelism | E20–E21, H13–H16, A18–A19 |
| Root cause F, confidence | E07–E12, E21, E24–E25, C01–C03, H18 |
| Section 6, more assets or dates | A05, A18–A19, F23 |
| Section 6, discontinuous payoffs | F06–F07, C07 |
| Section 6, stochastic or rough volatility | F12–F15, F21–F22, F26 |
| Section 6, better compilation | A06–A20, C13 |
| Section 6, variance controls | F08, F20, E03, E09–E12 |
| Section 6, strikes, portfolios and Greeks | E18–E19, F27–F29 |
| Section 6, PDE solvers | F24–F26, C01 |
| Section 6, quantum QMC window | F05 |
| Section 6, new hardware | H01–H14 |
| Section 7, requirements frontier | C02–C05, C13–C15, F31; compatible cost model in H memo |
| Section 8, what is established | C06–C12, C15 |
| Sections 9–10, evidence map and references | Primary-source registers, C15; not every historical citation rederived |

## The next small questions in dependency order

The following order prioritizes interpretable results, not the largest advertised factors. These are proposed next experiments, not additional work already executed.

| Order | Small question | Concrete acceptance condition |
|---:|---|---|
| 1 | Can one existing 32-row coefficient lookup be cheaper? | Exact `out XOR table[address]` on every address, coherent/inverse correctness, and lower compiled cost under a fixed workspace cap; A15 |
| 2 | Can the verified cleanup replace an eligible real leaf fragment? | Full branch-channel equivalence plus measured T, measurement and feedback costs; first component result and A16 |
| 3 | Which flags and indexes can use fewer bits exactly? | Per-node proof of active width, followed by one emitted narrow leaf with unchanged semantics; A06 |
| 4 | Can we prepare one useful Gaussian more cheaply? | Certified target law, explicit forward/inverse, matched error allowance and complete synthesis cost; A02 and A05 |
| 5 | Does fast-forwarded Heston apply to A1 and then A4? | Every correlation, tail, payoff and parameter hypothesis verified before compiling a transition; F15 |
| 6 | Can two bounded probabilities replace expensive payoff normalization? | Correct measure-change sampler and joint dollar-error/confidence ledger; F08 |
| 7 | Can a small path subgraph fit a smaller workspace? | Emitted clean schedule with paid recomputation and measured peak width; A18–A19 |

Before approximate circuits support any price claim, the boundary/tail/grid bridge in C06–C07 must be closed. Exact-semantics compiler experiments can proceed without pretending that bridge is already complete.

## Boundaries of this pass

The broad literature pass, code inspection and first cleanup experiment are complete. A complete proof audit of every cited theorem, implementation of every proposed alternative, and an end-to-end hardware crossover are not claimed. Source-access limits are recorded in the individual memos; no absence-of-search-result is used as proof of impossibility.

The research method from here is deliberately small: choose one interface, state what must remain identical, implement or prove the replacement, measure the changed cost, and only then combine it with another improvement.
