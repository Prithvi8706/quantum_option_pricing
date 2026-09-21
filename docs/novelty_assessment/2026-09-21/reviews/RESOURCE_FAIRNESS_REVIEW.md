# Independent AI review: resources, comparator fairness and reproducibility

Date: 2026-09-21. Reviewer scope: circuit/resource accounting, comparator
fairness, evidence provenance and relevant resource/classical literature.
This reviewer did not implement the frozen pricing circuits or produce their
acquisitions. The checker written for this review is a secondary read-only
analysis. This is AI-assisted review, not an independent human endorsement.

**Verdict: conditional-go for a narrow certified comparator-sensitivity and
reproducibility paper; no-go for a new-primitive, generally superior arithmetic,
physical speedup or quantum-over-classical advantage paper on this evidence.**
The D2 ledger reversal is real within the stated model. Its mechanism is
largely the stronger comparator receiving a classical control; it is useful
evidence that the earlier apparent advantage depended on baseline design.
That is scientifically informative, but does not establish that a
control-variate idea or resource-selection principle is new.

## Materials and actual verification

Inspected the primary/residual protocols, methods, results and review closeout;
the earlier matched-arithmetic method/results; encoding-decision rule;
classical baseline protocols and current week-two classical archive;
`research/stronger_arithmetic` component assembly, acquisition, analysis and
verification code; relevant `journal_sprint` resource/schedule/conditional-call
implementations; and release receipt/replay tooling. The key original documents
are [results](../../../release/STRONGER_ARITHMETIC_RESULTS_20260921.md),
[primary method](../../../release/STRONGER_ARITHMETIC_METHOD_20260921.md),
[residual method](../../../release/SIGNED_RESIDUAL_METHOD_20260921.md), and
[earlier comparator method](../../../journal_sprint/MATCHED_ARITHMETIC_METHOD_20260917.md).

A new [standard-library checker](resources/check_archived_resources.py) passed;
its [machine-readable receipt](resources/archived_resource_check.json) records:

- All 148 primary layout rows and 18 residual configurations: 332 new-row CX
  ledgers, plus both ledgers for the two selected reflection references.
- Complete primary/residual file inventories: 78 and 23 hashed payload files,
  respectively, plus each `complete.json`; these agree with the original
  verifiers' 79/24 total-file counts.
- Live hashes for 223 and 310 source/input entries and source commit binding
  for 216 and 222 source files. Seventy-four historical text files in each
  source set required the originally declared CRLF/LF normalization; stronger
  arithmetic source and protocol bytes were checked strictly.
- Frozen acquisition heads `9511bc0c8cb25421707428abec8ca8f22ba02cfc` and
  `60e735e1783a9aadec2fe42acfc007c16030fac2`. The latter contains the
  `23f8d948` residual implementation and committed primary input archive;
  implementation freeze and acquisition head are different facts.
- Independent integer reconstruction of initial A, both oracle directions,
  controlled-zero and good reflections, full IQFT swap terms, allocation,
  loader additions, and inherited residual conversion/aggregation inverses.
- Independent rational one-dollar and minimal-dyadic-schedule checks, using
  separately written code and a different rational pi enclosure.
- Actual XML testcase counts: 1,645 and 315, with no failure/error/skip nodes.
  These are historical passing receipts, not 1,960 independent tests and not
  new test executions.

This check did not re-emit gates, prove every certificate, rerun finite-grid
diagnostics, execute AE, or rerun the full suites. Existing pinned receipts
report full certificate/finite-diagnostic replay and selected gate emission;
this reviewer inspected those receipts rather than relabeling them fresh work.
Six distinct primary configurations and two residual oracles were re-emitted
in that earlier closeout, not the entire nominal menu. Hash agreement makes
an expensive unchanged-code rerun unnecessary for this scoped review.

## What the D1/D2 reversal means

The selected plans reconstruct as follows. CX is the standard
control-cancelled composition projection; qubits are the declared fully
allocated total, including the clean zero-reflection workspace.

| Case/route | Price slope | Deterministic dollars | AE M | A CX | Total CX | Total qubits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| D1 reflection | 17.518533 | 0.45473744 | 128 | 8,412,708 | 36,469,403,102 | 55 |
| D1 residual arithmetic | 31.054257 | 0.10296484 | 128 | 24,149,637 | 104,719,289,723 | 4,733 |
| D2 reflection | 42.703876 | 0.60039730 | 512 | 63,331,046 | 1,101,392,680,835 | 103 |
| D2 residual arithmetic | 62.108514 | 0.20538904 | 256 | 43,196,209 | 375,312,500,844 | 5,162 |

D2 reflection/residual ratios are **2.9346016409** in the cancelled ledger
and **3.2891600107** in the conservative ledger. Arithmetic allocates
**50.1165 times** the total qubits. D1 residual arithmetic uses about 2.8714
times the cancelled CX and 86.0545 times the allocation of reflection.
These are dimensionless ratios of declared ledgers, not runtime ratios.

Comparing the selected residual with the best raw arithmetic mixes precision
and control changes. A cleaner existing-data ablation uses its exact
width-48/fraction-24/degree-8/reduction-1 raw parents, D1_28 and D2_28:

| Fixed conversion parent | Raw A CX | Residual A CX | Raw to residual M | Raw to residual slope | Total-CX reduction |
| --- | ---: | ---: | ---: | ---: | ---: |
| D1 | 18,917,901 | 24,149,637 | 1024 to 128 | 248.4341 to 31.0543 | 6.28793x |
| D2 | 37,964,541 | 43,196,209 | 2048 to 256 | 496.8681 to 62.1085 | 7.04275x |

The parent conversion and precision are identical within these pairs. The
signed-control oracle makes A more expensive: **27.65% in D1, 13.78% in D2**.
The exact eightfold reduction in selector-derived price scale reduces the AE
schedule eightfold, overcoming that overhead. Deterministic arithmetic
allowances also change, so this isolates the whole added control construction,
not an abstract effect of centering alone.

Against reflection, D1 has the same M and a substantially dearer arithmetic A.
D2 has both a cheaper arithmetic A and half as large M. Its reflection slope
is smaller than arithmetic's, yet its larger approximation allowance leaves
less statistical margin. Query demand depends jointly on normalization and
the complete error allocation, rather than the slope alone.

The earlier raw-arithmetic result remains valid for its historical comparator.
The broader inference that reflection wins against comparably controlled
arithmetic is superseded. The later result should be presented as a stronger
baseline correcting that interpretation, not as evidence that either earlier
acquisition was fraudulent or that control variates were newly invented.

## Error, confidence and schedule sensitivity

All selected plans use the same D1/D2 contracts, q10 conditional-normal
midpoint representation, cutoff 4, one-dollar tolerance, 17 independent ideal
AE repetitions and ten-million-call cap. Representation allowances bridge
each finite oracle back to the financial target; arithmetic and reflection
do not compute identical finite functions. Matched financial accuracy does
not require identical arithmetic maps, but does require those separate bridges.

The schedule uses price slope L and deterministic allowance B with

`B + L*(pi/M + pi^2/M^2) <= 1`,

and charges `17*(2*M-1)` calls to A/A-inverse. A per-run success lower bound
0.8, independent repetitions and a median give Hoeffding failure bound
`exp(-2*17*0.3^2) = 0.0468877 < 0.05`. This is a theorem-based ideal-model
plan, not empirical 95% price delivery, hardware validity or certification of
native finite-precision sin-squared decoding. The latter representation-to-float
obligation remains explicit in the residual method.

The checker fixed an algebraic sensitivity menu of common additional dollar
allowances `{0, .025, .05, .1, .15, .2}`, holding the selected circuits and
certificates fixed. This is a calculation on existing ledgers, not a physical
noise estimate, confirmation experiment, or reoptimized menu. D2 residual's
remaining schedule slack is only **$0.02307139**, versus reflection's
**$0.13596722**. At an added $0.025, residual M doubles to 512 and reflection
stays at 512; the CX ratio becomes **1.46586625**, so residual **still wins**.
At $0.15 both selected-route schedules have doubled relative to their original
values and the ratio is approximately 2.9332. The jump in the headline factor
is relevant to robustness; no physical-error value has been estimated here.

Normalization is not additive bias. The residual magnitude certificate
justifies a shift H and selector denominator; the estimated signed residual
is restored using the classical offset. The integer identity
`Pr[U < R+H] = (E[R]+H)/2^m` is ordinary affine amplitude encoding and is exact
on the certified integer range. Floor rounding, reciprocal, Horner/scaling,
offset discount bridge and binary64 decoder errors are separate terms in the
project's certificate. The full mathematical reviewer should judge their
universal derivations; this resource audit checked their accounting interfaces
and selected schedule use, not every boundary proof anew.

## Fairness of the resource comparison

The complete arithmetic assembly charges conversion and aggregation forward
and inverse, sum-to-strike translation and restoration, control evaluation,
positive part, residual subtraction, shift, comparator and cleanup. Loaders
and selector Hadamards are added outside that component. There is no free
payoff rotation assumption or omitted arithmetic uncompute detected in the
inspected logical composition. Uniform selectors implement counting, with no
additional threshold approximation when certified ranges fit.

Both ledgers apply the same outer AE convention. The cancelled ledger uses
the standard identity controlling `A*S0*A†` by controlling only `S0`; this is
not a new primitive. The conservative ledger's expensive gate-by-gate controls
are deliberately pessimistic. Agreement between those ledgers rules out that
one particular control convention as the source of the reversal.

However, internal compilation remains asymmetric: reflection uses established
level-1 component compilation and projected control bounds; reversible
arithmetic uses explicit X/CX/CCX decomposition with CCX charged six CX/nine U,
and earlier aggregation uses its stated level-0 convention. A common named
CX basis does not make global optimizations, phase synthesis or layout equal.
This is fair enough for a declared-model case study, not for an optimized
cross-implementation performance claim. A ratio of two upper projections
does not bound the ratio of actual optimized costs: their respective slack is
unknown. No nonzero lower bound on competing optimal costs has been proved.

Widths and depths need equally careful wording:

- The same integer map in shared-scratch baseline layouts changes D1 arithmetic
  A from 1,835 to 1,113 wires and depth 1,457,262 to 2,905,250; D2 changes
  3,465 to 1,299 wires and 1,466,110 to 5,810,090 depth. Counts are unchanged.
  Those depths are emitted/remapped X/CX/CCX dependency depths, not CX or
  physical execution depths.
- Selected residual A uses 2,364/2,578 wires, including 914 shared conversion
  scratch wires and 1,207 total/oracle-private wires. Separate zero-reflection
  ancillas then yield 4,733/5,162 total. This allocation is conservative,
  not a lower bound on required width. More aggressive reuse, restricted
  reflections on an invariant clean-workspace subspace, or pebbling could
  change it, but none is silently credited here.
- Residual depths 6,220,602 and 11,696,282 are composition upper bounds.
  Comparing them numerically as if they were the primary remapped depths,
  or comparing either to an unavailable full optimized reflection depth,
  would be unsound.

Native rotation synthesis, T-count/T-depth, routing, error correction,
magic-state supply, physical failures and wall time remain missing. Those
unknowns restrict practical interpretation. They are not fabricated zero costs.

## Nominal menu, offset setup and the classical target

The primary Cartesian menu is complete. Nevertheless, after trimming trailing
zero coefficients, it contains **50 distinct conversion-map parameter groups
among 74 nominal configurations** (100 layout/map pairs among 148 layout
rows). There are 24 degree-12/16 duplicate pairs. The 18 residual configurations
contain **12 distinct circuit-parameter/count groups**, with six such pairs.
Nominal degrees have separate conservative certificates even when their
emitted integer maps match. They are legitimate retained protocol entries,
not independent algorithmic evidence or 166 distinct circuits. No winner
depends on hiding these duplicates.

The common degree-four offset is transparent: D1/D2 record respectively
28,672/245,760 cell visits, 70/549 exponential calls, and 1,025 CDF boundaries
per case. Work is counted separately, not assigned a universal runtime.
Requiring a classical expectation is a real assumption; it is tractable here
because moments of a fixed low-degree polynomial over the independent finite
Gaussian model can be computed without the full product grid. Scaling to
higher degree/dimension needs its own analysis. The offset should be reused
and amortized identically across routes when applicable.

The existing [week-two classical archive](../../../../results/journal_sprint/minimal_pivot_week2_classical_v1/results.json)
is more relevant than the older eight/32-date smoke. At 16 replicates of
4,096 paths plus a paid 1,024-path pilot (66,560 total), the D1/D2 approximate
95% halfwidths are respectively 0.00010426/0.00061091 for RQMC/control and
0.00006011/0.00015253 for conditional RQMC/control. These are development
Student-t approximations with floating arithmetic, not rigorous dollar-error
certificates or verified RMSE. They nevertheless give strong evidence that
these two small Gaussian contracts are easy classically. A quantum gate
reduction alone has little demonstrated practical economic significance.
Comparing those classical seconds directly with quantum CX counts is invalid.

The implemented monotone strike-root preintegration formula is established
classical work; the [source notes](resources/PRIMARY_SOURCE_NOTES.md) map it to
Liu/Owen. This should strengthen the comparator discussion, not be presented
as a new classical method.

## Skeptical questions and dispositions

| Objection | Finding and disposition |
| --- | --- |
| 1. Earlier arithmetic lacked a comparable control | Yes; exact-parent ablation confirms query reduction dominates. Resolved mechanism; narrows novelty claim. |
| 2. Signed residual/control is established | Control identities and bounded signed expectation encoding are standard. Exact nearest QAE-control attribution belongs to main novelty review; no new control-variate principle is claimed. |
| 3. Shift/decoder is a known affine encoding | Direct counting proves it; engineering certification is the addition. Limitation on mathematical novelty. |
| 4. Reversal survives both ledgers | Yes, independently reconstructed. Resolved for declared costs. |
| 5. Compiler conventions are unequal | Documented and consequential. Narrow present claim; a common selected-oracle basis check is bounded further work. |
| 6. Expensive operations omitted | No missing logical component detected in selected compositions. Native/physical and total classical setup costs are outside ledger, so practical superiority stays excluded. |
| 7. Classical offset cost is free | Work counts are retained, but no matched end-to-end time. Resolved transparency; limitation for practical claim. |
| 8. Accuracy/confidence match | Same financial contracts and ideal sufficient $1/95% convention; different finite approximations have separate bridges. Physical confidence and actual delivered prices unestablished. |
| 9. Normalization/rounding/overflow | Components and signed units are documented and linked; no accounting omission found. Full universal proof judgment remains with the independent mathematical audit. |
| 10. Width undermines interpretation | Yes for a practical blanket recommendation. D2 is a width/CX tradeoff; no memory-constrained winner was established. |
| 11. Two cases/fixed degrees limit generality | Yes. Fixed schedules show sensitivity; no universal crossover surface follows. Narrow claim, do not describe selected cases as confirmation. |
| 12. Nominal configurations duplicate | Yes, quantified above. Resolved reporting issue; retain all protocol rows. |
| 13. Decision rule exceeds a table minimum | The AE export is a constrained minimum of computed costs. Earlier calibration planner adds a valid prospective sufficient screen, but standard probability tools and no general optimality theorem. |
| 14. Upper-projection ratio bounds true ratio | False. Explicit limitation; fatal only to a stronger speedup/lower-bound claim. |
| 15. A stronger arithmetic implementation could remove advantage | Plausible, particularly for D1. R2 supplies a consequential comparator lead; not tested here. Fatal to universal reflection superiority, not to this historical comparative finding. |
| 16. Classical task is already easy | Existing conditional-RQMC development evidence strongly supports that concern. Quantum-over-classical practical paper is not supported. |

## Prior art, remaining work and final disposition

Eight scoped primary sources, including non-IonQ QCE papers and the strongest
classical method mapping, are recorded with publication/version/access details
in [source notes](resources/PRIMARY_SOURCE_NOTES.md). They establish prior art
for reversible Horner, memory management, pricing error/resource budgeting,
encoding comparisons and resource-driven algorithm selection. The D1/D2
numbers and integrated directed artifact package may be new project-specific
results; literature absence is not established by that observation.

The defensible paper claim is: **For two specified arithmetic Asian-basket
contracts under a reproducible ideal-logical dollar/confidence contract,
strengthening the arithmetic baseline with a comparable signed classical
control changes the logical-CX ordering in D2 while exposing a large width
tradeoff; normalization, approximation budget and compilation assumptions must
be stated together when comparing encodings.**

One bounded follow-up is justified if the paper aims to carry more than an
artifact/negative-result note: pin a common resource basis and cleanup policy
for the selected D1/D2 oracles, and compare one literature-informed optimized
arithmetic implementation (R2 is the clearest lead) under the same target and
error bridge. Preserve all outcomes and treat it as a separate development
comparison. That task should not expand into an advantage search or require
paid hardware. A complete manuscript and qualified human review remain needed;
additional full-suite reruns without source changes do not answer novelty.

No implementation blocker or evidence mismatch was detected within this
resource scope. Material limitations remain: incomparable optimization slack,
no full residual/reflection physical-depth comparison, two already observed
contracts, easy classical baselines, and no human novelty assessment. No
consensus beyond this reviewer's scope is implied. Frozen archives/producers
were unchanged; this reviewer made no branch operation, commit, push,
researcher contact or publication action.

## Independent integration-plan review

Reviewed on 2026-09-21 at local dev `601ebcdc3e3910e0228fdf2920970dcc0e744e11`:
[branch consolidation](../BRANCH_CONSOLIDATION.md),
[promotion plan](../MAIN_BATCH_PLAN.md), initial references, cleanup receipt,
preservation inventory/manifest/receipt, actual Git ancestry and live remote
heads. This bounded pass made no Git mutation and did not repeat scientific
acquisitions or the full artifact byte-verification run.

**No integration-plan blocker found.** Local heads and `git ls-remote --heads`
both list exactly main/dev. Local main remains `103ddfd1`, remote main remains
`da3080d1`, and the documented 26-commit difference is correct. All initially
inventoried branch tips are ancestors of current dev; every removed local or
remote tip is also an ancestor of `b90c2e30`, the recorded pre-cleanup pushed
dev. Stash and original-main archival references remain at their recorded
SHAs. The local recovery bundle lists the former tips and detached worktree
heads. The preservation manifest independently totals 13,783 selected files
and 254,488,741 bytes; its scope is correctly limited to preservation, not
scientific revalidation.

The first snapshot `23f8d948` is exactly the two original source commits above
remote main: 28 changed paths, including eleven tests, twelve package files,
four method/protocol documents and `.gitattributes`. It adds no results archive.
The five older archive files directly loaded by these tests already exist at
that snapshot. Stronger-arithmetic source/tests and the four method/protocol
documents have not changed since it. The full proposed chain through
`49b8f0a5`, `5f96b9ec`, `b90c2e30` and `601ebcdc` preserves original producer
and acquisition commit identities. The three frozen new-study archive trees
and the relevant producer trees show no changes after the original closeout.

Readiness is appropriately stated as readiness **for scoped review**, with
normal integration checks, numerical-interface conditions and later evidence
attachments explicit. The common-policy comparison and publication package
remain unexecuted. Keeping both versions of the adapter and promoting its
complete reviewed snapshot avoids silently replacing provenance. Ordinary
merges with temporary review heads satisfy the two-permanent-branch model.
One minor wording correction was sent to the coordinator: the cleanup JSON
records operation output, rather than full command-line arguments.

At this review instant remote dev was still `b90c2e30`; verification of the
subsequent assessment push belongs to the final delivery receipt. This review
does not certify a later push that had not yet occurred.
