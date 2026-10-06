# Frozen B4/B8 task and reconciled arithmetic baseline

Local execution, 1 October 2026. G0/C01-C03/C13 and A01 are completed for the current knock-out arithmetic sources. Their gate/price/error scopes remain separate; no new scientific pricing or gate replay was performed. Every current target was rebuilt from the original financial builder and exact optimizer and matched both the accepted target and Stage A original graph.

The payoff is one unit of the equal-weight basket Asian call: exp(-0.03)*max(mean of all asset/date spots-100,0), paid only when every monitored equal-weight basket is strictly below 140. Each asset starts at 100, volatility is 0.30, equity correlation is 0.40, maturity is one year and observations are equally spaced. Barrier equality knocks out. The initial basket is $100; output is already discounted dollars, with no extra notional multiplier. B4 uses 4 assets/12 dates; B8 uses 8 assets/52 dates.

The digital source uses 32-bit midpoint uniforms, the existing paired Box-Muller arithmetic, f=40/72-bit words, clipped log spots in [log(2^-16),log(4096)], degree-12 Estrin exponentials and signed modular integer semantics. These choices define the accepted digital function; their continuous-price effects remain unproved. Output Y is interpreted as signed integer/2^40.

The unchanged tolerance grid is $0.10, $0.03, $0.01 and the B4/B8 final $0.001 test, with at least 99% per-price confidence and complete latency at most one tenth the fastest eligible complete classical time. The historical 0.45*epsilon statistical share is a planning reference. Every missing error bound and failure allocation is null, not zero; G2-G5 remain unresolved.

| Case | Nodes / forward calls | T gates | Capped T-depth | Clifford+T depth | Logical qubits | Separate uniform H |
|---|---:|---:|---:|---:|---:|---:|
| B4x12 | 5,038 / 4,978 | 632,258,326 | 2,436,454 | 7,226,923 | 550,158 | 1,920 |
| B8x52 | 41,654 / 41,186 | 5,191,385,654 | 2,624,696 | 7,803,425 | 4,460,490 | 14,976 |

Each target node and forward invocation is attributed exactly once. Uniform inputs have no arithmetic leaf. Scalar-normal ancestors stop at inputs; correlation includes the scaled common/idiosyncratic combination and deterministic log-increment drift; path/payoff begins after those increments. Cross-stage shared constants/nodes have an explicit shared bucket. Output XOR is charged once to path/payoff.

## B4x12 attribution

| Category | Nodes | Forward calls | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|---:|---:|
| uniform_preparation | 60 | 0 | 0 | 0 | 0 |
| scalar_normals | 2,768 | 2,768 | 322,783,020 | 1,494,720 | 1,165,168 |
| correlation | 157 | 157 | 7,930,272 | 72,576 | 86,560 |
| path_payoff | 2,051 | 2,051 | 301,545,034 | 1,143,648 | 1,184,726 |
| shared | 2 | 2 | 0 | 0 | 0 |

Top three work operations: mul (571,737,600 T), sqrt (28,035,840 T), cmul (16,451,400 T). Top three deterministic batch-owner depth operations: mul (1,264,032 layers attributed), cmul (565,280 layers attributed), sqrt (450,386 layers attributed).

Independent forward weighted-DAG T-depth is 496,883; all 222 capped batches and their scratch/copy costs reconcile. Clean argument-copy CX count is 2,710,944; output XOR adds 72 CX.

## B8x52 attribution

| Category | Nodes | Forward calls | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|---:|---:|
| uniform_preparation | 468 | 0 | 0 | 0 | 0 |
| scalar_normals | 21,536 | 21,536 | 2,517,707,556 | 11,658,816 | 1,165,168 |
| correlation | 1,301 | 1,301 | 59,480,512 | 614,016 | 76,352 |
| path_payoff | 18,347 | 18,347 | 2,614,197,586 | 10,318,176 | 1,383,176 |
| shared | 2 | 2 | 0 | 0 | 0 |

Top three work operations: mul (4,707,306,240 T), sqrt (218,679,552 T), cmul (130,198,768 T). Top three deterministic batch-owner depth operations: mul (1,264,032 layers attributed), cmul (712,864 layers attributed), sqrt (450,386 layers attributed).

Independent forward weighted-DAG T-depth is 495,923; all 230 capped batches and their scratch/copy costs reconcile. Clean argument-copy CX count is 22,591,008; output XOR adds 72 CX.

Category depths overlap within parallel batches and must not be summed as serial elapsed time or multiplied into separate speedup factors. Deterministic batch ownership sums to the complete scheduled depth but is attribution only: tied or hidden leaf costs can become dominant after a change. The independent DAG bound concerns this fixed leaf decomposition, with no routing/factory model; it is not a lower bound on all implementations.

Actual immutable gate arrays for 59 unique leaves were scanned for X/CX/CCX counts and hashed. Reconstructed counts reproduce all seven source count fields, exact seven-T/six-CX/two-H CCX expansion, serial depths, both capped depths, qubits and copy costs. Prior evidence contains three B4 and one B8 sampled full-source replays; none was repeated here. The environment is the existing pinned local Python, not a new installation.

Receipts: [G0 summary](../../results/limitation_program_20261001/G0_run003/summary.json), [frozen tasks/error ledgers](../../results/limitation_program_20261001/G0_run003/), [A01 accounting](../../results/limitation_program_20261001/A01_run003/), and [producer](../../research/limitation_program_20261001/baseline.py). Each run has a prospective protocol, verification, next action and manifest.

Next: combine exact compact SSA storage with the accepted parallel leaf library under the unchanged caps. Recompute these ledgers after any adoption and then screen the dominant remaining arithmetic. Price certification, an estimator for this source, matched actual classical target timings and a compatible physical mapping are separate unfinished gates. Nothing was pushed, uploaded or published.
