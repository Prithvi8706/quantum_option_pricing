# Verified project state

Assessment date: **2026-09-21**, verified against the session UTC clock.
Repository: Prithvi8706/quantum_option_pricing. This record distinguishes
source/evidence inspection from new experiments and historical claims.

## Source and Git baseline

The takeover head was `49b8f0a5a1394198b98e20b6e091f86a5f1ad532` on
`research/stronger-arithmetic-20260921`. Fetch confirmed `origin/main` at
`da3080d19a8f746cab31bbee157a5d591c6b56fb`, the PR #8 merge. The five reported
commits exist in the stated order, directly above that merge:

| Commit | Meaning |
| --- | --- |
| `9511bc0c` | Frozen shared-workspace/range-reduction implementation and protocol |
| `23f8d948` | Separate signed-residual implementation, protocol and verifier |
| `60e735e1` | Complete primary acquisition; input publication before residual acquisition |
| `add768dc` | Residual evidence and combined comparison |
| `49b8f0a5` | Results/review closeout |

They initially had no remote development branch. `dev` was created at that head
and pushed; the first verified remote SHA was exactly `49b8f0a5...`.
Subsequent assessment commits preserve this ancestry and authorship.
[Consolidation](BRANCH_CONSOLIDATION.md) records final Git operations.
Local `main` initially lagged at `103ddfd1`; neither local nor remote `main`
is advanced by this task. An old local reference is not the current remote
stable integration point.

No applicable AGENTS.md was found in the workspace or checked ancestor paths.
The active checkout had no tracked modifications before work began. Numerous
historical artifacts, local environments and reading copies were untracked;
they were inventoried before classification. The linked review worktree had a
modified tracked bytecode file; it is preserved, not treated as new research.

## Financial and mathematical target

Risk-neutral correlated geometric Brownian motion, discretely monitored
arithmetic Asian-basket call, with spot 100, rate .03 and maturity 1:

`V = exp(-rT) E[(A(Z)-K)_+]`,
`A(Z) = (1/d) sum_i exp(mu_i + F_i Z)`, with `Z ~ N(0,I)`.

Here d is the number of asset/date values and Gaussian factors in these square
models. The archived binary64 means/factors are interpreted exactly; PCA
orientation is pinned rather than assumed identical across LAPACK versions.
The continuous target refers to continuous Gaussian inputs at the specified
monitoring dates, not a continuously monitored Asian contract.

| Case | Assets | Monitoring dates | d | Volatility | Strike | Cross-asset correlation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| D1 | 1 | 2 | 2 | .20 | 95 | .30 parameter, vacuous for one asset |
| D2 | 2 | 2 | 4 | .25 | 105 | .40 |

Both new studies use cutoff 4, q=10 bits per independent Gaussian coordinate,
exact conditional normal cell masses and midpoint nodes. Tail/midpoint and
stored-model allowances connect the finite computation to the declared price.
They retain a $1 absolute-error contract, at least 95% confidence in the
specified ideal-logical model, 17 independent AE repetitions and a
10,000,000 A/A-inverse call cap. D1/D2 are development cases. Existing E1/E2
results are historical evaluation material already seen; no fresh holdout is
opened by this assessment.

## Construction and implementation map

| Layer | Implemented content | Authoritative locations |
| --- | --- | --- |
| Signal | Separable exponential probabilities, row-indexed shared reflection, signed LCU centering | `research/journal_sprint/reflection_centered_signal.py`, versioned `reviewed_reflection_signal.py`; W1 method |
| Reflection pricing | Residual QSP, degree-four classical moment offset, Hadamard readout, canonical AE | `week2_pipeline.py`, `week2_explicit_ae.py`, `week2_decoding.py`; W2 method |
| Arithmetic | Fixed-point log conversion, range-reduced exponential, ripple aggregation, positive part and uniform comparator, compute/uncompute | `research/stronger_arithmetic/{budget,circuits,components,run_study}.py` |
| Signed control | Certified p4 control, signed floor Horner, shift H, restored offset, price/error ledger | `research/stronger_arithmetic/{residual,residual_circuits,residual_components,run_residual}.py` |
| Selection | Feasibility from deterministic-plus-AE budget, then finite-menu CX minimum; no physical selection | `claim_assessment.py`, `stronger_arithmetic/analyze.py` |
| Classical comparison | MC/geometric control, PCA RQMC, conditional RQMC, separately paid pilot/setup | `asian_basket.py`, `run_minimal_pivot_week2.py`; earlier `classical_baselines.py` |
| Provenance | Hash/commit binding, full-menu certificate replay, selected gate re-emission | `stronger_arithmetic/verify*.py`, `research/release_checks/` |
| New interface check | Directed exact AE-label to float conversion and all-label schedule overlay | `research/assessment_20260921/` |

The earlier calibration-aware direct-sampling selector in
`encoding_decision.py` is a separate fixed-time k=0 method. Its CP/Hoeffding
argument and calibration costs must not be conflated with the current
canonical-AE planner.

## Current evidence and what it proves

| Evidence | Verified scope and limits |
| --- | --- |
| [Primary archive](../../../results/journal_sprint/stronger_arithmetic_v1/results.json) | 74 acquisitions, 148 paired layout rows; no failures in the frozen menu |
| [Residual archive](../../../results/journal_sprint/signed_residual_arithmetic_v1/results.json) | 18 configurations; all budget/cap feasible in their declared ideal model |
| [Combined export](../../../results/journal_sprint/stronger_arithmetic_analysis_v1/all_rows.csv) | All 166 new rows; historical reflection references remain separately identified |
| [Primary replay receipt](../../../results/journal_sprint/stronger_arithmetic_pinned_replay_20260921.json) | All certificates/finite diagnostics and both ledgers; selected gates only |
| [Residual replay receipt](../../../results/journal_sprint/signed_residual_pinned_replay_20260921.json) | All 18 configurations and offsets, selected complete oracles |
| [Parent replay](../../../results/journal_sprint/residual_parent_pinned_replay_20260921.json) | D1_28/D2_28 conversions in both layouts; six distinct primary configurations re-emitted across all prior receipts |
| [Integrated tests](../../../results/journal_sprint/stronger_arithmetic_full_tests_20260921.xml) | 1,645 passing cases, inspected receipt; not rerun or added to overlapping counts |
| [Pinned tests](../../../results/journal_sprint/stronger_arithmetic_pinned_tests_20260921.xml) | 315 passing cases, overlap the integrated suite |
| [Current independent checks](REVIEW_RECORD.md) | Rational certificate/resource reconstructions and bounded boundary diagnostics; no new pricing observations |

Gate counts are emitted-component logical U/CX projections, with one U per X
and six CX/nine U per CCX in arithmetic, and two declared AE control ledgers.
Counts include loading, inverses, selector work, zero reflections and inverse
QFT swaps. They do not include physical routing, fault-tolerant synthesis,
error correction or measured runtime. Residual depth is a composition upper
bound; primary layout depth is remapped dependency depth.

## Selected current results

| Case/route | Control-cancelled CX | Total allocated qubits | AE M |
| --- | ---: | ---: | ---: |
| D1 reflection | 36,469,403,102 | 55 | 128 |
| D1 signed residual | 104,719,289,723 | 4,733 | 128 |
| D2 reflection | 1,101,392,680,835 | 103 | 512 |
| D2 signed residual | 375,312,500,844 | 5,162 | 256 |

D2 reflection/residual is approximately 2.9346 in this ledger and 3.2892 in
the conservative ledger. The 2026-09-17 result that reflection beat raw
arithmetic remains a valid historical comparison; it is superseded as a
statement about the enlarged menu. New controls are not evidence that earlier
raw-comparator measurements were fraudulent.

## Open gates and historical material

The candidate is standby; production choice is null, confirmation unadmitted,
physical errors unknown, quantum-over-classical advantage unestablished.
Human novelty assessment and manuscript/submission preparation remain open.
The label adapter closes a limited classical numerical interface under ideal
AE assumptions; it does not promote any of these gates.

Consolidated older archives and the Paper A render are retained as historical
information, including failures and stale claims. Preservation is not a new
verification of every old experiment or a claim that the old manuscript is
ready. The authoritative new judgment is [PUBLICATION_DECISION.md](PUBLICATION_DECISION.md).
