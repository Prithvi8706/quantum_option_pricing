# Comparator fairness and attempted falsification

Date 2026-09-21. Detailed independent implementation inspection and new
stdlib checks are in [RESOURCE_FAIRNESS_REVIEW.md](reviews/RESOURCE_FAIRNESS_REVIEW.md)
and its [receipt](reviews/resources/archived_resource_check.json).

## What the reversal actually shows

The historical reflection-versus-raw-arithmetic comparison gave the reflective
route a classical polynomial control without giving the arithmetic route an
equivalent strategy. The new residual route corrects that imbalance. It is
therefore principally a **comparator-design correction**, with a useful
quantitative consequence, not an unexpected new residual principle.

The minimum-to-minimum raw/residual ratios also change precision and oracle
structure. To isolate the strategy more closely, the independent review
recomputed existing exact raw parents D1_28/D2_28: w=48/f=24/Taylor degree 8/reduction s=1,
same conversion and aggregation as the selected residuals. In D2, the signed
oracle's A-CX rises from 37,964,541 to 43,196,209 (13.78%), while its price
slope and AE M shrink eightfold (M=2048→256). Total projected CX falls from
2,643,233,541,099 to 375,312,500,844, a factor 7.04275. This is an archived
component decomposition, not a new acquisition or a centering-only causal
experiment independent of the oracle change.

The D2 reflection/residual projected CX ratio is approximately 2.93460
with control cancellation (3.28916 in the conservative ledger). Residual
arithmetic uses 5,162 versus 103 total wires. D1 arithmetic uses more CX at the same M=128.
The contrast is explained by per-call cost and discrete query demand.

## Sixteen objections and dispositions

| Objection | Finding and disposition |
| --- | --- |
| 1. Earlier arithmetic lacked a comparable control | **Resolved as interpretation:** yes, this is the principal correction; exact-parent decomposition supports query-driven improvement. Narrow the claim. |
| 2. Signed-residual estimation is already known | **Resolved against broad novelty:** N1/N2/F2 are direct precedents; no new control-variate QAE principle. |
| 3. Shift/decoder is ordinary affine encoding | **Resolved against primitive novelty:** N2 §4 explicitly supplies it. |
| 4. Reversal depends on one resource ledger | **Resolved within scope:** both ledgers reproduce D1/reflection and D2/residual ordering. |
| 5. Compiler conventions are fully comparable | **Limitation; bounded follow-up:** same accounting basis does not mean identical optimization. Reflection uses optimized U/CX components; arithmetic uses streamed exact X/CX/CCX decomposition. Common-policy compilation is still needed for stronger implementation claims. |
| 6. Expensive operations are missing | **Partly resolved:** inspected formulas charge loader, conversion, controls, inverses, residual, selector, reflections and QFT swaps. Native synthesis/routing/error correction are absent by declared scope; do not claim physical cost. No exhaustive new production gate simulation occurred. |
| 7. Classical offset is free | **Resolved for quantum-only ledger; practical limitation:** recorded separately at 28,672/245,760 cell visits, 70/549 exp calls and 1,025 CDF boundaries for D1/D2. No seconds-to-CX conversion or total-runtime win is claimed. |
| 8. Accuracy/confidence are matched | **Resolved for ideal planning:** same targets/tolerance/canonical confidence; different deterministic components and slopes explicitly charged. **Limit:** classical t intervals are not matching rigorous guarantees; frozen residual label interface needed the new adapter. |
| 9. Normalization/rounding/overflow omitted | **Resolved within inspected certificate:** universal signed bounds, input/reciprocal/Horner/scale/offset/decoder terms and per-basket units checked. Parent/QSP proof mechanisms reviewed but not formally verified. |
| 10. Width undermines practical interpretation | **Major limitation:** D2 needs 50.1× and D1 about 86.1× reflection's wires. Lower CX need not mean lower spacetime cost or runtime. Width constraints can exclude residual arithmetic. |
| 11. D1/D2/menu dependence | **Claim-narrowing limitation:** two development cases do not establish prevalence or universal crossover. Keep all existing E-case failures and tiny unfavorable examples as historical context. |
| 12. Nominal configurations are identical | **Resolved by reporting:** 74 primary nominal acquisitions represent 50 conversion-map groups; 18 residual rows represent 12 circuit groups. Layouts/certificates remain separately retained; 166 rows are not 166 independent circuits. |
| 13. Decision rule is just table minimum | **Resolved against theorem novelty:** yes, for the implemented finite menu. Certification/refusal and discrete jumps are useful software, not new optimization theory. |
| 14. Ratios compare upper projections | **Claim-narrowing limitation:** two composition bounds do not bound optimized-cost ratios. Report only ratios of the stated formulas. |
| 15. Better arithmetic removes reflection wins | **Unresolved and potentially fatal to a superiority paper:** R2/R3/R5 show plausible stronger arithmetic/memory designs. Our narrower measured-menu claim survives, but an externally best-arithmetic claim does not. |
| 16. Classical methods already make the target easy | **Major practical limitation:** existing controlled/conditional RQMC diagnostics are strong and cheap. No matched rigorous-confidence hardware race exists. A quantum-advantage narrative is unsupported even if a quantum route saves gates. |

These are not sixteen coding defects requiring sixteen new experiments.
Several are reasons to change the paper's central claim.

## Error-budget and width sensitivity

The selected D2 residual plan has only about $0.0230714 unused schedule margin,
versus about $0.135967 for reflection. A **hypothetical**, common extra $0.025
deterministic allowance doubles residual M to 512 while reflection stays at 512.
Residual still wins by a factor 1.46587. This calculation holds the selected
oracles fixed; it is not a menu-wide reoptimization, a noise estimate or fresh
confirmation. The numerical label bridge is many orders smaller and changes
no schedules. See the independent resource receipt for exact values.

A width cap below 5,162 excludes the selected D2 residual implementation.
Alternative arithmetic layouts require their own certified evidence; it is
invalid to silently replace allocated wires by a hypothetical recycled width.
Residual depth is a serial composition upper bound, while primary workspace
depth is an emitted dependency depth. No complete matched depth ranking exists.

## What remains fair to claim

The financial contracts, finite-law definition and ideal error/confidence
goals are matched. The compared implementations and their stated resource
ledgers are reproducible. They support a local cost-order change, large width
tradeoff and the necessity of comparable control strategies. They do not
establish best-in-class implementation, practical crossover, generality or
quantum-over-classical advantage. The [bounded follow-up](BOUNDED_FOLLOWUP_PLAN.md)
addresses the most consequential remaining comparison uncertainty.
