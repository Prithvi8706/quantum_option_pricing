# Week 8 results: paid representation selection does not improve delivery

Discovery under [the declared protocol](PROTOCOL_W8_REPRESENTATION.md), not
confirmation or a generic new estimator. Exact targets were excluded from the
ranking interface; pilot cost was charged before fresh validation allocation.

## Complete outcomes and denominators

**5400 procedure attempts**, with 3300 final acquisitions and 2100 pre-refusals.
Additionally, the selector acquired **1800 candidate pilots**, two each in the
900 procedures with a genuinely selectable menu. These are not 1800 extra final
confidence declarations. There were **900 final $1 declarations and 2400
unresolved final intervals**, no incompatibilities. All 3300 final intervals
contained the price; zero erroneous declarations were observed. Neither observed
perfect containment nor zero errors proves universal or conditional-on-delivery
coverage. All three stipulated transfer conditions were retained.

Each policy has 1800 attempts (six contracts, three conditions, 100 repetitions):

| Policy | Final acquired | Pre-refused | Pilot acquisitions | $1 declarations |
|---|---:|---:|---:|---:|
| Fixed n5 | 900 | 900 | 0 | 300 |
| Fixed n6 | 1200 | 600 | 0 | 300 |
| Pilot selector | 1200 | 600 | 1800 | 300 |

Every E001 policy/condition cell delivered 100/100; every other acquired cell
delivered zero. Fixed n5 correctly refused E049; the selector chose its sole
n6 candidate without a pilot. E030/E038 were refused by every policy.
No refusal was substituted with another representation in a fixed baseline.

All **36 selector-minus-fixed per-attempt delivery contrasts were zero**, against
both fixed policies in all six contracts and three conditions. The readiness
screen passed only E001's three cells out of 12 feasible-contract/condition cells;
mean delivery gain was zero against each baseline, below the declared +10-point
requirement. **The selector fails the screen and is not promoted.**

## What the pilot selected

Paid selection operated only for E001/E014/E025. Of 900 such procedures, it
selected n5 **350 times** and n6 **550 times**. E049 adds 300 bypass selections
of n6. This is real observation-dependent selection, but **not demonstrated
beneficial adaptation**. The heuristic uses the observed pilot dollar radius,
not a validated forecast of the different full-budget allocations.

The two pilots each have 1024 shots per depth but unequal CX costs. Together
they consume 51677184 pricing CX, about 15.65% of the cap, leaving 278624256.

| Allocation | n5 shots per depth | n6 shots per depth |
|---|---:|---:|
| Fixed, full pricing-CX allowance | 29772 | 8389 |
| After two paid pilots | 25114 | 7076 |

This is equal **capped pricing-CX allowance**, not equal total resources.
Calibration is 32768 shots for fixed/bypass procedures and 49152 for paid-selector
procedures. Extra calibration is disclosed, never amortized or charged twice.

## Representation and interval geometry

Bounds (dollars) were calculated before any new sampling:

| Contract | n5 | n6 | Eligible choices |
|---|---:|---:|---|
| E001 | .093028 | .048755 | Both |
| E014 | .851082 | .501995 | Both |
| E025 | .580683 | .359078 | Both |
| E030 | 5.431435 | 2.399314 | Neither |
| E038 | 4.063174 | 1.931005 | Neither |
| E049 | 1.216272 | .732712 | n6 |

Reducing n lowers compiled ladder cost but increases the sufficient deterministic
bound. For stationary cells, median final dollar radii were:

| Contract | Fixed n5 | Fixed n6 | Selector |
|---|---:|---:|---:|
| E001 | .817 | .867 | .869 |
| E014 | 8.280 | 8.878 | 8.966 |
| E025 | 5.541 | 6.012 | 6.055 |
| E049 | Refused | 11.619 | 11.587 |

The cheaper n5 representation modestly reduced some widths without bringing
E014/E025 to $1. All 3300 final confidence sets had **one connected component**.
Their broad final hulls therefore were not produced by gaps between multiple
retained components in this experiment. This does not show that inference is
optimal, that branches may safely be discarded generally, or that another
representation/inference construction cannot improve delivery.

Each final record separates the deterministic radius contribution from the
statistical hull contribution; these two sum to the reported dollar radius.
For example, fixed-n5 E014 stationary median radius 8.280 includes deterministic
bound .851, leaving about 7.429 from the statistical hull. Representation-bound
improvement alone is not established as a sufficient cure by these data.

## Total cost and reproducibility

Pilot phase: 5529600 pricing shots + 14745600 calibration shots = 20275200.
Final phase: 156180000 pricing shots + 108134400 calibration shots = 264314400.
Combined **284589600 represented shots**, 485128800 pricing A-equivalents,
and 1089951639000 pricing logical CX. These counts describe synthetic binomial
acquisition, not that many physical circuits or a classical-runtime comparison.
Run elapsed 19.06 seconds; bound/menu setup .13381 seconds.

Reconstruction checked **81 archive hashes, 74 planned dependency hashes,
5400 selection events, 5400 records and 54 summaries**. Every menu, target,
pilot, score, selection, final allocation, confidence set and phase cost matched.
Event persistence precedes final acquisition in source order and in the tested
callback contract; archive equality alone is not an external timestamp proof.
Replay reuses producing numerical helpers and requires matching archived code,
not arbitrary updated dependencies. It is not independent numerical certification.

Archives: `results/journal_sprint/week8_representation_v1` and
`results/journal_sprint/week8_closeout_v1`. After review, a final-cell resource
limit check was added. `week8_representation_v2` / `week8_closeout_v2` repeat
the same protocol/keys and reconstruct unchanged results: raw records, selection
events, menu and targets match v1 byte-for-byte. V2 took 17.13 seconds. It is
not an additional independent replication and its counts are not pooled with v1.
Full regression passed 325 tests before this limit-only fix; 14 focused tests
passed afterward. See [the closeout](WEEK_8_CLOSEOUT.md) for exact review scope.

## Contribution decision

Retain the selector as a negative, fully costed ablation—not the paper's proposed
adaptive superiority result. The supportable direction remains **model-conditional
interval coverage and empirical precision delivery, with explicit representation,
calibration and resource costs**. The [selection scope argument](WEEK_8_SELECTION_SCOPE.md)
explains why a single fresh validation interval can follow pilot choice, and
why that does not imply correctness conditional on delivery.

Journal novelty and practical utility remain unestablished. Native BAE/BIQAE
superiority, real-device transfer validity, formal numerical bounds and classical
speedup are not demonstrated. Do not replace the failed criterion with a favorable
cell or lower guard; decide the next claim and evidence requirements explicitly.
