# Encoding and sequential-validity discovery results

## Disposition

The exact finite-grid oracle repairs a measurable weakness in the previous
implementation. It improves fixed-time $1 delivery on E014 and E025 under both
equal-shot and equal-logical-CX budgets. It does not establish quantum advantage,
solve all contracts, or make the elementary oracle construction novel.
The anytime-valid inference components are implemented and tested, but neither
sequential variant matches fixed-time delivery consistently at the same cap.

This study was declared in [PROTOCOL_RESCUE_V1.md](PROTOCOL_RESCUE_V1.md).
The pilot-mixture follow-up was declared only after the first results, in
[PROTOCOL_PILOT_CS_V1.md](PROTOCOL_PILOT_CS_V1.md). It is reanalysis of the same
stored paths, not new independent evidence. The
[research report](QUANTUM_RESCUE_RESEARCH.md) and
[mathematical specification](RESCUE_THEORY.md) explain attribution and assumptions.

The pilot construction's guarantee is for prospective use with a fixed rule.
Its post-result selection and reanalysis here do not establish selection-adjusted
95% coverage on the reused data. Reported follow-up counts are descriptive.

## 1. Primary equal-shot result

Each entry below is declarations out of 30 attempts, guard zero, n=6, 32768
pricing shots maximum, plus 16384 calibration shots per state. Validation
readout rates are f=.02 and g=.07; this is a synthetic, stationary readout model,
not gate-noise simulation or hardware execution. All arms include their own
representation bound in the dollar interval.

| Contract | Old oracle, fixed CP | Exact oracle, fixed CP | Exact oracle, Jeffreys CS | Exact oracle, pilot CS follow-up |
| --- | ---: | ---: | ---: | ---: |
| E001 | 30/30 | 30/30 | 30/30 | 30/30 |
| E014 | 0/30 | 30/30 | 0/30 | 1/30 |
| E025 | 0/30 | 30/30 | 30/30 | 30/30 |
| E030 | 0/30 (refused) | 0/30 | 0/30 | 0/30 |
| E038 | 0/30 (refused) | 0/30 | 0/30 | 0/30 |
| E049 | 0/30 | 0/30 | 0/30 | 0/30 |

Under equal logical CX, the exact-oracle E014 Jeffreys and pilot CS arms both
declare 30/30. The cheaper exact oracle receives more shots under that cap;
this is why the equal-shot and equal-CX results must be separated. All other
zero-guard declaration counts in the table are unchanged under equal CX.
Encoding contrasts use distinct random streams and are descriptive, unpaired
contrasts; the inference variants reuse the same underlying path within each
encoding/condition and are not independent acquisitions.

The fixed-time exact-oracle intervention passes its declared discovery screen
of improvement on two non-E001 contracts under both axes. The initial Jeffreys
CS fails that screen: only E025 improves on both axes. The pilot follow-up
technically clears the weak positive-difference screen through E014's 1/30,
but that is not robust delivery. It is not promoted as a satisfactory E014
equal-shot solution, and the screen should not be treated as a significance
test or evidence of broad superiority.

## 2. Transfer-allowance sensitivity

For the exact oracle with fixed-time CP and equal shots, declarations were:

| Contract | Guard 0 | Guard .003 | Guard .03 |
| --- | ---: | ---: | ---: |
| E001 | 30/30 | 30/30 | 30/30 |
| E014 | 30/30 | 0/30 | 0/30 |
| E025 | 30/30 | 30/30 | 0/30 |
| E030 | 0/30 | 0/30 | 0/30 |
| E038 | 0/30 | 0/30 | 0/30 |
| E049 | 0/30 | 0/30 | 0/30 |

The actual validation rates equal the calibration rates in every condition.
Thus these are different *supplied allowances* applied to stationary data, not
experiments demonstrating robustness to realized drift. The exact oracle's
E001 result at guard .03 improves over the old oracle's 0/30 in this particular
design. It must not be generalized to arbitrary time-varying or gate noise.

The results distinguish deterministic eligibility from useful statistical
delivery. E030 and E038 become bound-eligible with the exact oracle, but neither
delivers under the tested budgets. E049 also remains unresolved. Improving the
encoding does not eliminate finite calibration uncertainty or leave enough
statistical tolerance in every contract.

## 3. Representation and resources

| Contract | Old total B | Exact support+grid B | Old direct CX | Exact direct CX |
| --- | ---: | ---: | ---: | ---: |
| E001 | 0.048755 | 0.013512 | 268 | 126 |
| E014 | 0.501995 | 0.111559 | 268 | 126 |
| E025 | 0.359078 | 0.078506 | 268 | 126 |
| E030 | 2.399314 | 0.959200 | 268 | 126 |
| E038 | 1.931005 | 0.675848 | 272 | 126 |
| E049 | 0.732712 | 0.152846 | 268 | 126 |

All exact direct circuits use 7 qubits versus 13 in the old implementation.
The amplitude-to-dollar sensitivity decreases by 2/(pi*.125), approximately
5.093 times, while the old analytic encoding allowance disappears. The ideal
finite-grid identity and every tested Grover marginal agree within the declared
1e-9 tolerance. This is a finite-table implementation result; the table has
64 entries and scales exponentially with n. Rotation-synthesis error and
physical circuit errors are outside this ideal check.

The stored default amplified profiles appear to show very large improvements:
for E001 at k=1, old 13088 CX versus exact 566. A post-result compiler sanity
check exposed a stronger old baseline. The old oracle leaves workspace qubits
7..12 clean (zero-state probability 1.0 in the inspected E001 statevector).
Restricting its Grover reflection to active qubits 0..6 gives 992 CX with the
same amplified amplitude, 0.7776645243983171. Thus a 23-fold generic amplified
oracle saving would be misleading: the inspected optimized comparison is
992/566, about 1.75-fold. This diagnostic was performed for E001 only.

The main delivery experiment uses k=0 and is unaffected by that reflection
optimization. Future amplified benchmarks must include the stronger reflection
baseline and verify workspace assumptions for every instance, including noise.
All counts use logical u/cx compilation without routing, optimization level 1,
seed 1729. They are not hardware-native gates, T-counts or execution-time savings.

For reproduction of the compiler diagnostic: build the old E001 n=6 circuit
with c=.125 and q=1e-5, construct an oracle Z on objective qubit 6, create
`GroverOperator(oracle, state_preparation=ec.circuit, reflection_qubits=list(range(7)))`,
compose one iterate after A, and transpile with the settings above. Compare its
statevector objective marginal against the default profile before using its cost.

## 4. Stopping and cost accounting

The Jeffreys CS gives 330 declarations across its 2160 attempt identities;
the fixed-time CP gives 480. Each includes 360 pre-acquisition refusals.
The pilot follow-up gives 355 declarations over the same identities, retaining
the same refusals. These counts are descriptive across heterogeneous cells;
they are not three independent validation campaigns or a pooled coverage trial.

On exact-oracle E001 at guard zero and equal shots, the Jeffreys CS stops at
1024 pricing shots in all 30 runs. With the 32768 calibration shots, that is
33792 total shots, versus 65536 for a 32768-shot fixed procedure. The pilot CS
cannot declare from the pilot itself and stops at 2048 total pricing shots in
that cell, or 34816 including calibration. Quoting a 32-fold total-shot saving
from the pricing prefix alone would hide calibration cost.

All original 4320 inference rows have zero observed interval misses and zero
erroneous $1 declarations. The 2160 pilot-derived rows also have zero observed
misses and erroneous declarations. Refusals are not counted as covered intervals.
Finite observations do not imply zero risk or prove universal coverage. The
mathematical guarantee is conditional on the model and exact arithmetic.

## 5. Classical comparator and remaining novelty gap

Exact classical summation uses the same 64-term grid. It completed in about
0.0010-0.0024 seconds per reported evaluation, including the probability/grid
calculation inside that function but excluding earlier support-bound setup.
Single timing observations are not a stable performance benchmark. Errors
against the continuous reference ranged from about 0.000085 to 0.046602 dollars,
all within the retained support+grid allowances, which are below $1 on all six
contracts. Closed-form Black-Scholes is also available for these models.

Consequently there is NO end-to-end quantum advantage in this experiment.
The exact oracle improves the quantum implementation, while classical
summation already handles every tested instance. A future contribution must
either make an explanatory reliability result sufficiently general and useful,
or transfer the method to a genuinely harder integration problem with strong
classical comparators. Merely reproducing a standard table oracle or standard
confidence sequence cannot fill the methodological novelty gap.

## 6. Failures, archives and verification

`rescue_encoding_v1` is retained as a failed run. All six circuit profiles
completed, but the first pricing serialization encountered a NumPy Boolean.
Its failure record lists two computed rows; its JSONL contains zero persisted
rows. A Boolean-conversion fix and runner serialization regression were added
before rerunning. No stochastic outcome was changed to pass a scientific screen.
A prior unit test also caught integer/Boolean aliasing in a cache key; typed
cache keys fixed it before the first experiment.

`rescue_encoding_v2` is the completed original discovery archive, with source
snapshots, six paired profiles, classical reference records and all 4320 rows.
`rescue_pilot_cs_v1` is a separate completed post-result reanalysis, with all
2160 derived rows and its source-manifest link. Original files remain unchanged.
All these are local workspace artifacts; no new PR or publication was created.

`verify_rescue` passed the 4320-row deterministic replay, 77 archived-file
integrity checks and recomputed bound/target arithmetic. Its report is
`results/journal_sprint/rescue_verification_v1.json`. It does not pretend to be
independent peer review or a second circuit-profile experiment. Pilot replay
also passed all 2160 derived rows and rechecked the 4320-row input archive;
report `results/journal_sprint/rescue_pilot_verification_v1.json`.

The first integrated suite passed 440 tests with 11 upstream warnings in
273.99 seconds. The new pilot method then passed seven additional focused
tests, including conditional-mixture expectation, high-precision endpoint
checks and exclusion of pilot-only declarations. Final-tree regression passed
**447 tests, zero failures or skips, 11 upstream warnings, 280.51 seconds**;
report `results/journal_sprint/tests_rescue_final_v1.xml`. Ruff passed on all
eight new Python/test files, and local document-link/whitespace checks passed.

## 7. Next scientific decision

Keep the exact oracle as a stronger small-grid baseline. Keep the anytime
construction as a validity layer, without claiming it is always more efficient.
Do not promote the pilot follow-up's 1/30 E014 equal-shot delivery as a robust
solution. Do not use the unoptimized amplified reflection as the sole baseline.

The next focused research claim should concern encoding-aware dollar-delivery
decisions with finite calibration: establish a useful criterion, compare it
against the improved fixed baseline, and map regimes of success and refusal.
Only then freeze fresh confirmation seeds. Remaining work includes better
calibration allocation, faithful modern AE competitors, scalable payoff/loading
methods, physical-noise validation and a targeted novelty comparison. These
are research tasks, not results that the present intervention has already proved.
