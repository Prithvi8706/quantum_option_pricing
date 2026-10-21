# Local limitation-program status

This is the current execution ledger for the [complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md). Plan status includes earlier evidence; execution status records this program's scoped results. A passed component does not close the entire limitation.

Updated UTC: 2026-10-01T15:40:35.395269+00:00. All execution is local.

Current phase: signed7 shift complete; exact non-restoring root leaf queued.

Next action: Implement one exact non-restoring square-root leaf under the existing unsigned46 guard, retaining native72 input/output XOR and charged signed remainder cleanup. Exhaust small widths/fractional counts and production boundaries; screen the nondominated leaf against the accepted digit-by-digit root, then both capped A07_shift_run001 sources. Preserve validated signed7 shifts and generic fallback. No approximation or G2-G5 closure is claimed..

Accepted source: [A07_shift_run001](../../results/limitation_program_20261001/A07_shift_run001/summary.json).

| Case | T gates | T-depth | Clifford+T depth | Logical qubits |
|---|---:|---:|---:|---:|
| B4x12 | 629,425,006 | 936,810 | 2,781,579 | 550,141 |
| B8x52 | 5,172,716,094 | 969,512 | 2,912,185 | 4,460,481 |

## Evidence gates

| Gate | Current status |
|---|---|
| G0 | passed for current B4/B8 task and provenance |
| G1 | passed for current exact B4/B8 source: structural arithmetic, tests, full emitted replays and independent cost audits |
| G2 | open |
| G3 | open |
| G4 | open |
| G5 | open |

## Arithmetic

| Item | Limitation / work item | Plan status | Current execution |
|---|---|---|---|
| A01 | Separate uniform preparation, normal loading, correlation and payoff costs | ready | Exact signed7 control leaf passed27 tests and proof-dispatched integration52 tests; full capped source Tdepth reduced4.3447% B4 and5.7887% B8, Twork reduced0.7121% and0.7220%, same qubit caps/target/copies/other leaf bytes. All4 financial dirty-output cleanup replays passed. Independent61-array/220-metadata audit passed; scoped A07 component adopted, wider limitation and G2-G5 open. |
| A02 | Replace Box-Muller only after a complete scalar-loader comparison | partial | not started |
| A03 | Certify recursive-loading integrals and conditional angles | partial | not started |
| A04 | Turn Gaussian MPS compression into an emitted, synthesized circuit | partial | not started |
| A05 | Allocate and compose loading error across independent draws | ready | not started |
| A06 | Combine exact compact storage with the latest arithmetic schedule | partial | accepted exact component |
| A07 | Prove reachable ranges before narrowing arithmetic | ready | Exact signed7 control leaf passed27 tests and proof-dispatched integration52 tests; full capped source Tdepth reduced4.3447% B4 and5.7887% B8, Twork reduced0.7121% and0.7220%, same qubit caps/target/copies/other leaf bytes. All4 financial dirty-output cleanup replays passed. Independent61-array/220-metadata audit passed; scoped A07 component adopted, wider limitation and G2-G5 open. |
| A08 | Benchmark a matching clean carry-lookahead adder | ready | exact leaves verified; full-source gains below 2% threshold; baseline retained |
| A09 | Extend the measured multiplier frontier without assuming Karatsuba wins | partial | accepted exact signed-CSA/prefix component; about 3.3% more T work, G5 unresolved |
| A10 | Finish constant-product and square specialization after the ln(2) win | partial | One exact signed square verified:70 new distinct tests; independent audit reconciles61 arrays/222 metadata locations. Full-source depth gains1.7812%/1.5820% miss predeclared2% threshold; no financial replay/adoption. T work falls4.44%/4.69%; retain component and candidate, A11 baseline unchanged. |
| A11 | Match square-root interfaces and charge remainder cleanup | ready | Adopted same-target unsigned46 tight/fused sqrt after78 new distinct tests,4 full financial replays and independent cost audit; full A11 non-restoring/Newton/Heston scope remains open |
| A12 | Screen reciprocal division with exact quotient correction | ready | not started |
| A13 | Search a bounded exponential degree/segment frontier | ready | not started |
| A14 | Bound CORDIC/log-cosine transfer before circuit work | conditional | not started |
| A15 | Preserve the completed exact coefficient-lookup replacement | complete | existing verified component |
| A16 | Extend measured cleanup into a verified dynamic arithmetic backend | partial | not started |
| A17 | Audit existing fusion and phase-check remaining controlled boundaries | audit | not started |
| A18 | Apply paid reversible pebbling to a real financial subgraph | partial | not started |
| A19 | Test reversible streaming on the unchanged monitored payoff | conditional | not started |
| A20 | Test arithmetic-free loading on the actual sum-of-exponentials threshold | conditional | not started |

## Estimators

| Item | Limitation / work item | Plan status | Current execution |
|---|---|---|---|
| E01 | Generic quadratic query scaling versus exploitable structure | audit | not started |
| E02 | Replace hypothetical k with executable source and inverse counts | ready | not started |
| E03 | Match range or variance normalization to the actual amplitude oracle | partial | not started |
| E04 | Remove QFT/QPE only when the complete bounded-estimator schedule improves | ready | not started |
| E05 | Factored external controls already avoid controlling every arithmetic gate | complete | existing verified component |
| E06 | Fused graph compute and uncompute is already implemented | complete | existing verified component |
| E07 | One complete-price error and confidence ledger | partial | not started |
| E08 | Further confidence allocation optimization against the already optimized schedule | partial | not started |
| E09 | Unknown variance without treating unknown sigma as an absolute-error certificate | conditional | not started |
| E10 | Acquire analytic moment bounds with outward rounding | partial | not started |
| E11 | Transfer second moments to the identical finite source with an L2 bridge | conditional | not started |
| E12 | Anytime-valid statistical moment acquisition | ready | not started |
| E13 | Exact uniform-selector payoff loading is already implemented | complete | existing verified component |
| E14 | Replace prohibitive nested constants only with an explicit coherent schedule | conditional | not started |
| E15 | Measured adaptive inner estimation is not a coherent outer oracle | partial | not started |
| E16 | Finite-variance heavy tails have query alternatives with explicit bias and weights | conditional | not started |
| E17 | Infinite variance and undefined mean require different contracts | audit | not started |
| E18 | Multi-output tasks need their own norm, confidence and access contract | conditional | not started |
| E19 | Quantum Greeks must compete with classical adjoint differentiation | conditional | not started |
| E20 | Entangled parallel AE must pay for all source lanes and physical scheduling | conditional | not started |
| E21 | Convert RMSE to the allocated high-probability dollar guarantee | ready | not started |
| E22 | Classify actual payoff predicates before importing log-domain QSP | ready | not started |
| E23 | QSP approximation, rotation synthesis and dollar bias are one budget | conditional | not started |
| E24 | Optimize the error split only over supported certificates | ready | not started |
| E25 | Adaptive Bayesian/likelihood designs need a coverage proof | conditional | not started |

## Formulations

| Item | Limitation / work item | Plan status | Current execution |
|---|---|---|---|
| F01 | Keep measured classical slopes inside their validated range | ready | not started |
| F02 | Separate path variance from randomized-quadrature variance | audit | not started |
| F03 | Verify smoothness of the transformed Gaussian integrand | ready | not started |
| F04 | Test structured integration of a certified residual | conditional | not started |
| F05 | Charge the whole payoff in coherent Sobol integration | conditional | not started |
| F06 | Isolate the active barrier-date switching surface | ready | not started |
| F07 | Screen rare-event proposals with their likelihood-ratio costs | ready | not started |
| F08 | Keep the exact bounded rewrite; reject the losing two-probability shortcut | partial | not started |
| F09 | Do not retain variance-based quantum rates in an infinite-variance model | conditional | not started |
| F10 | Reallocate multilevel work using separate classical and quantum costs | partial | not started |
| F11 | Reduce the base cost before spending on fine corrections | ready | not started |
| F12 | Separate positivity, coupling quality and Heston convergence proofs | ready | not started |
| F13 | Audit non-Lipschitz antithetic theory at the square-root boundary | audit | not started |
| F14 | Screen exact Heston transitions at contractual dates | conditional | not started |
| F15 | Repair the actual fast-forwarding assumptions before compilation | partial | not started |
| F16 | Identify the exact failed factorization before changing a nested model | audit | not started |
| F17 | Certify exercise-policy error near the continuation boundary | ready | not started |
| F18 | Match nested-estimation theorems to the actual contract and costs | audit | not started |
| F19 | Expand one deterministic nested schedule instead of hiding depth constants | conditional | not started |
| F20 | Evaluate controls by residual size times full oracle cost | partial | not started |
| F21 | Treat rough-volatility precision rates as measured contract-specific results | conditional | not started |
| F22 | Charge factor rank and bias in a Markovian rough-process lift | conditional | not started |
| F23 | Certify dimension compression on both architectures | ready | not started |
| F24 | Specify the exact Asian/barrier PDE before costing a quantum solve | conditional | not started |
| F25 | Propagate overlap readout error into dollars and repeated evolution cost | conditional | not started |
| F26 | Audit one SPDE/BDSDE update only for an independently justified model | conditional | not started |
| F27 | Choose the exact multi-output error norm before pricing its penalty | audit | not started |
| F28 | Match a valid barrier Greek against a classical adjoint or smoothed estimator | conditional | not started |
| F29 | Treat an aggregate portfolio as one declared observable | conditional | not started |
| F30 | Compare tensor compression with direct classical contraction | conditional | not started |
| F31 | Replace exponent requirements with the matched complete-time inequality | audit | not started |
| F32 | Use quantum walks only when the financial input has a real mixing bottleneck | conditional | not started |

## Hardware

| Item | Limitation / work item | Plan status | Current execution |
|---|---|---|---|
| H01 | Decoder latency is not universally tens of microseconds | audit | not started |
| H02 | Fast standalone decoding is not the entire reaction loop | audit | not started |
| H03 | A code cycle and a logical T layer are different quantities | ready | not started |
| H04 | Repeating distance-many syndrome rounds per operation is not mandatory in every architecture | conditional | not started |
| H05 | Fifteen-to-one distillation is not the only magic-state supply | ready | not started |
| H06 | T-state supply and Toffoli-state supply must be matched to the circuit | partial | not started |
| H07 | Distillation is not logically necessary for every non-Clifford implementation | conditional | not started |
| H08 | An alternative physical qubit does not automatically eliminate all factories | conditional | not started |
| H09 | Surface-code physical-qubit overhead is not universal | conditional | not started |
| H10 | High-rate codes also have logical-operation research | conditional | not started |
| H11 | Addressable transversal non-Clifford gates are a distinct route | conditional | not started |
| H12 | Constant asymptotic overhead is not a small finite constant | conditional | not started |
| H13 | Idle space can dominate a physical mapping | conditional | not started |
| H14 | Photonic clock rates cannot be inserted directly as logical-layer rates | conditional | not started |
| H15 | Millions of logical qubits in the emitted oracle are not an information lower bound | partial | accepted exact component |
| H16 | Classical parallelism is inexpensive in this benchmark but not literally free | ready | not started |
| H17 | T depth alone does not determine runtime | ready | not started |
| H18 | Error per operation must fall as the entire computation grows | ready | not started |

## Contract and evidence

| Item | Limitation / work item | Plan status | Current execution |
|---|---|---|---|
| C01 | One classical price is the current output | ready | completed scoped baseline audit; financial certificates remain open |
| C02 | Dollar accuracy cannot be silently weakened | ready | completed scoped baseline audit; financial certificates remain open |
| C03 | The complete price needs the complete confidence allowance | ready | completed scoped baseline audit; financial certificates remain open |
| C04 | Tenfold advantage is a chosen threshold | audit | not started |
| C05 | The statistical allowance of 0.45 epsilon is adjustable | ready | not started |
| C06 | Correct digital arithmetic is not a continuous financial-law certificate | conditional | not started |
| C07 | A few draws without barrier flips do not certify rare flips | conditional | not started |
| C08 | Fitted convergence exponents are not lower bounds | ready | not started |
| C09 | Modelled classical time is not a timed successful price | ready | not started |
| C10 | The strongest tested classical method is not automatically the strongest applicable one | ready | not started |
| C11 | A clean source is not an entire mean-estimation algorithm | partial | not started |
| C12 | Six constructions share three contracts and one toolchain | partial | not started |
| C13 | Optimizations interact and cannot be multiplied without a compatible schedule | partial | accepted exact component |
| C14 | A classical cubic exponent is not necessary for a crossover | audit | not started |
| C15 | References and stale numerical summaries need individual checking | audit | not started |

The [machine-readable ledger](../../results/limitation_program_20261001/progress.json) preserves decisions and receipt links. G2 continuous-dollar error, G3 compatible estimation, G4 actual matched classical timings and G5 physical resources remain separate obligations.
