# First gate-resolution increment: results

Implemented directed partial error enclosures and non-enumerative safe payoff
normalization, preserving the current Asian/PCA architecture and all originals.
No algorithm/advantage, full-price certification or confirmation claim follows.
See [derivations and scope](CONFIRMATION_GATE_BOUNDS.md) and
[concrete remaining implementation plan](CONFIRMATION_UNLOCK_PLAN.md).

Producer/protocol freeze e38ee513. Deterministic development archive
results/journal_sprint/encoding_enclosure_v1 completed all576rows (six original
input records, three cutoffs, two representations,16precisions),49files; strict
replay reproduced all decimal endpoint strings exactly. There were no failed
audit cells or sampled acquisitions. The six archived records represent only
three distinct contracts; duplicates from different original precision records
are not six independent application validations.

## Improvements and the remaining resource bottleneck

For week14's two-asset/two-date case at L=3,q=1:

| Bounding expression | Previous float evaluation | New directed upper bound |
|---|---:|---:|
| Tail/renormalization | 2.242099 | 1.157855 |
| Raw midpoint discretization | 250.455719 | 94.991133 |
| Residual midpoint discretization | 313.126138 | 133.902673 |

These are upper-bound expressions, not observed pricing errors. The new Gaussian
model bridge is about2.06e-13dollars raw and3.30e-13residual, so rounded PCA/log
coefficients are not the main obstacle in this case. The old floating bounds
were not directed certificates; the comparison illustrates tightness, not two
independently certified implementations.

At L=4, the first tested q meeting the **partial**$0.25deterministic budget is:

| Contract | Representation | Previous expression q | New q | Normal qubits | New partial upper bound |
|---|---|---:|---:|---:|---:|
| 1asset/2dates | raw | 12 | 10 | 20 | .143163 |
| 1asset/2dates | residual | 12 | 10 | 20 | .242489 |
| 2assets/2dates | raw | 13 | 10 | 40 | .202071 |
| 2assets/2dates | residual | 13 | 11 | 44 | .158142 |
| 2assets/3dates | raw | 13 | 10 | 60 | .223333 |
| 2assets/3dates | residual | 14 | 11 | 66 | .172221 |

The previous-expression column is a separate diagnostic recomputation in
encoding_enclosure_old_comparison_v1.json, not part of the frozen576row audit.
It uses existing float tail+midpoint expressions; the new partial budget also
includes model bridge/offset allowances. Neither column is minimum physical
precision, a built circuit, or a full error-budget pass. No L=3candidate meets
this partial budget within the tested q range because this tail bound alone
exceeds it; that is a limitation of the bound, not proof of actual price error.

For two assets/two dates, the raw candidate changes52normal bits under the old
screen to40under the new one: a4096fold smaller *hypothetical table*. But2^40
entries is still enormous; no such table/circuit was built. The residual still
needs44normal qubits before arithmetic workspace. The production oracle must
be non-enumerative. Product loading alone does not solve this.

Safe L=4normalization upper bounds are483.835211(raw) and237.184496(residual),
computed without a payoff table. Their ratio is only about2.04, much smaller
than the coarse finite table's roughly7.83scale ratio. Those normalizations
apply to different domains/representations of the approximation; they are not
new measured cost ratios. This exposes why the earlier small-table improvement
cannot be extrapolated to a scalable pricing advantage.

## Verification and integrity

38new focused tests passed/8upstream warnings in14.77s before acquisition.
Tests cover directed primitives,130digit CDF cross-checks, exact-rational
arithmetic checks, ambient-context independence, perturbed-model bridge sanity,
safe-scale domination on a small grid,24dimension non-enumeration, unknown-bias
refusal, exclusive output ownership, tampering and durable failure markers.

The first iteration had two failing arithmetic reference tests: rounded mpmath
references differed from exact zero-width decimal results. Replaced those
references with exact Fractions, not wider production intervals. No evidence
or method threshold was altered based on study outcomes. New-source Ruff passed.
Full regression passed845tests/20legacy warnings in380.26s
(tests_encoding_enclosure_full.xml). Clean source checkout52357dac passed38new
tests/8warnings in15.76s and reproduced49files/576decimal rows exactly using
the existing isolated week15 environment, not another fresh installation.
Receipts: tests_encoding_enclosure_clean.xml and
encoding_enclosure_clean_replay_v1.json. Producing code/protocol remain unchanged
sincee38ee513; Git whitespace checks pass. Old producers and original evidence
remain unchanged. The comparison/design sidecars are explicitly supplementary,
not quietly added inside the frozen49file archive.
No independent subagent/human review is claimed for this increment; the proof
and code need that additional scrutiny before scientific promotion.

## Gate disposition

Improved: deterministic approximation bounds, Gaussian model/offset rounding
allowances, non-enumerative normalization and precision-dependent screening.
Still unknown: actual state-preparation, payoff arithmetic, rotation/synthesis
and remaining numerical implementation errors. The opt-in PriceContract adapter
keeps those unknown, so application admission and confirmation remain NO-GO.
No PR/push/merge requested for this increment; work remains on the local research
branch. Actual collaborator sign-off and a defensible contribution remain open.
