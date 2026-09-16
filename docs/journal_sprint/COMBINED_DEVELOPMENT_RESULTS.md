# Combined development: what composes, what helps, what fails

Date2026-09-17. User requested a bounded integration of all three proposals and
ideas from Quantum Week beyond IonQ. No confirmation, remote jobs or hardware
execution was authorized by these experiments or claimed. Old archives/producers
remain unchanged. All results below are development, not held-out confirmation.

## Outcome

The naive combination was counterproductive. A corrected integration produced
a substantial **quantum-versus-quantum sampling-variance improvement** at the
same polynomial approximation bias and the same per-shot compiled CX count.
It does NOT establish quantum-over-classical advantage or continuous-price
accuracy. Classical methods benefit from the same control and remain strong.

The supported architecture is:

    reusable finite-model moments
             |
    polynomial control subtraction BEFORE normalization
             |
    normalized QSP residual block + classical control expectation
             |
    repeated valuations with moments reused, new signals still paid

Quantum Fourier feature discovery is an evaluated branch, not the selected
winner. MPS compression remains a diagnostic, not a compiled replacement loader.
Forcing those components into the selected path would misrepresent the evidence.

## Stage1: faithful integration/ablation

Original two-asset/two-date GBM business contract, L4/q2 finite grid:256paths.
Feature discovery uses128training indices at strike100, with128other indices
for representation RMSE. Strikes90/95/100/105/110 reuse the selected feature
words but refit coefficients on training labels. These are not new confirmation
datasets. The finite strike100 price is12.7682053323; this is NOT the earlier
continuous-model price near9.20.

-95representation records: classical exact Walsh search, full-pool greedy
  search, geometric control, and quantum Fourier sampling with256/1024shots
  across8repetitions per budget and5strikes.
-Quantum training is Fourier sampling with an actual amplitude-preparation/H
  circuit, not a replication of IonQ's variational parity method. Classical
  exact FWHT receives the identical training vector. Its access is not restricted
  to low-order features. Full vector/table preparation costs are disclosed.
-At strike100, raw finite payoff SD15.8253 falls to1.3681 with geometric control,
  1.7549 with full-pool greedy parity selection, and9.3187 for the1024shot
  replicate0 Fourier selection (same features as exact FWHT, up to ordering).
  The quantum-selected representation is not superior to these strong controls.
-QSP degree4/8 circuits were synthesized and their actual Hadamard expectations
  checked. A separate16path coherent PREP/SELECT/PREP-inverse circuit combined
  the QSP call and a sampled parity control, reconstructing the approximate
  price within2.59e-11. It used9qubits and43,156compiledCX gates per test circuit.
-In that smoke test, LCU normalization increased from62.0526to120.2090 (1.937x).
  All180larger finite-grid algebraic screens had worse single-Hadamard price
  variance than the matching raw-LCU representation. This does not prove every
  possible control/QAE method fails: it rejects this particular assembly.

## Stage2: adaptive correction, explicitly chosen after Stage1

Write the discounted call as D*B/2*(x+abs(x)), with x=(A-K)/B. Let P4 be a
degree4Chebyshev approximation to abs, and Pd a higher-degree approximation.
Instead of subtracting a separate signed LCU control from the raw QSP block,
synthesize **Pd-P4** directly and normalize it by its own small coefficient sum.
Add back the tractable expectation of D*B/2*(x+P4(x)).

The raw comparator also gets the analytically tractable linear term; we do not
force it to estimate that term quantumly. Raw and residual QSP represent the
same Pd approximate payoff. This isolates a representation/normalization change
from changes to approximation accuracy.

At strike100:

| Metric | Degree8 | Degree16 |
|---|---:|---:|
| Raw QSP price scale beta | 56.7266 | 54.9631 |
| Residual QSP price scale beta | 3.0010 | 4.7663 |
| Scale reduction | 18.9026x | 11.5316x |
| Price-estimator variance reduction | 370.6859x | 127.9594x |
| Raw/residual CX per Hadamard circuit | 14,624 /14,624 | 28,992 /28,992 |
| Raw/residual qubits | 10 /10 | 10 /10 |
| Raw/residual polynomial-price difference | 8.70e-14 | 7.99e-14 |
| Bias against exact finite-grid call | -1.12817 | -0.176253 |
| Truncation price-bound expression | 3.74751 | 1.98397 |

The variance is beta^2*(1-mu^2), calculated from the ideal Hadamard expectation.
For independent shots, estimator variance is this quantity divided by shot count.
The reported factor is NOT an observed hardware runtime speedup, a confidence
coverage guarantee, or a QAE oracle-count measurement. The bias remains even
with unlimited shots. The loose analytic truncation expressions above do not
include a uniform floating-phase/synthesis certificate.

Across all5strikes, reductions range348.9–376.9x at degree8 and127.0–131.4x at
degree16. Degree32 residual synthesis failed the preset three-seed bounded
test (sampled maximum error about0.01159); all attempts remain archived and no
degree32success is counted. Raw degree32synthesis succeeded, but one raw attempt
hit the1500evaluation cap. Successful optimizer termination alone was not
treated as an accepted polynomial fit.

## Strong classical comparison and reuse

Classical raw finite payoff variance at strike100 is250.4403. The same degree4
polynomial control reduces it to0.750517. In comparison, residual quantum
Hadamard variances are8.41522and22.6840 at degree8and16. Thus the demonstrated
quantum representation improvement is not evidence of superiority over direct
classical controlled sampling. Classical exact summation also solves the256path
benchmark, so this benchmark cannot support a computational-advantage claim.

The control moments E[A^k], k0..4, are computed by multinomial expansion and
factorized expectations over independent finite normal coordinates, not by a
joint payoff table. This example uses70terms/1120marginal exponential entries.
Agreement against joint enumeration is within9.26e-16 relative error (diagnostic,
not a directed certificate). Moments are independent of strike and available
to classical and quantum methods equally.

Reuse counts1/5/25/100 amortize these70terms and feature-discovery setup. New
strike labels/refits and256entry signal tables remain payable. Phase synthesis
is recorded through all attempts and can be reused across strikes. Its reported
solver evaluation count is not wall-clock time or a QPU call count. There is no
measured QPU latency/energy break-even and no executed nested-risk campaign.

## MPS/loading result

Classical TT-SVD compression of the1024entry normal amplitude vector:

| Bond dimension | Tensor parameters | Observed vector error |
|---|---:|---:|
| 1 | 20 | 0.6512 |
| 2 | 72 | 0.04061 |
| 4 | 232 | 5.59e-5 |
| 8 | 680 | 5.00e-13 |

These are floating compression diagnostics. Tensor parameter counts are not
gate counts; an MPS circuit and rigorous preparation error still need to be
constructed. Low-rank classical simulators receive the same representation.

## What we borrowed from Quantum Week

IonQ's parity/workflow studies motivated testing representation selection and
setup reuse, not assuming those parts are advantageous. The non-IonQ QCE25
gate-aware-depth study motivated critical-path costing with explicit illustrative
u=1/cx=10duration units; these are not IonQ timings or hardware calibration.
The QCE26 magic-informed-search work supports inspecting non-Clifford resources,
not treating magic as sufficient evidence of practical advantage. The bosonic
displacement-decision paper assumes a different signal-access model and was not
silently imported as a digital basket oracle. Sources and scope decisions are
listed in [Stage1protocol](COMBINED_DEVELOPMENT_PROTOCOL.md) and
[adaptive follow-up](COMBINED_FOLLOWUP_PROTOCOL.md).

## Verification / handoff

Twenty focused tests passed before follow-up acquisition. Stage1's separate
week15-environment replay reproduced all6numeric payloads exactly, excluding two
timings, and verified32source/artifact hashes. Follow-up replay and full regression
completed:5follow-up numeric payloads reproduce exactly (one timing excluded),
34source/artifact hashes checked. Full regression906passed/20legacywarnings in
378.42s. Producer code did not change during acquisition/replay. Same-producer replay is
not independent scientific review. No hardware or independent subagent review
is claimed. Original evidence is preserved, including failed synthesis attempts.

Artifacts: `results/journal_sprint/combined_development_v1` and
`polynomial_residual_v1`, with separate replay archives/receipts.

Clean-checkout verification at commit `1f140c3d`, using the existing isolated
week15 environment: 20 focused tests passed (8 legacy warnings, 13.96s).
Both replay checks passed again: 11 numeric payloads and 66 source/artifact
hash entries across the two archive pairs. Receipts are
`combined_clean_tests_v1.xml`, `combined_clean_replay_check_v1.json`, and
`polynomial_residual_clean_replay_check_v1.json` under the results directory.
This clean-checkout check did not rerun the full regression or acquisitions;
those were run separately as described above. No independent reviewer is implied.

The next meaningful implementation target is the control-subtracted QSP route:
scalable basket signal construction, stable higher-degree synthesis, full dollar
error certification and a continuous-target comparison. Novelty against existing
QSP and polynomial-control literature remains unestablished. The candidate
contribution is normalization-aware quantum pricing design—not a demonstrated
new asymptotic speedup. Confirmation remains blocked.
