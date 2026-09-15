# Model-conditional reliability and resource accounting for quantum option pricing
Working manuscript, 15 September 2026. Discovery and diagnostic evidence through week 10;
not submission-ready. Authors and contribution statements await actual work,
accountability and approval. This supersedes the early scientific working draft,
not the preserved historical DOCX/LaTeX artifacts.

## Abstract

Quantum pricing experiments can estimate a circuit amplitude precisely without
establishing comparable precision for the intended continuous option price.
We study a procedure that propagates finite readout-calibration uncertainty,
stipulated calibration-to-validation transfer allowances and contract-dependent
representation error into dollar intervals, allowing refusal or unresolved
outcomes. Fixed-design discovery studies show useful delivery concentrated in
one tested contract. A paid representation-selection experiment provides no
delivery gain over either fixed comparator in the tested cells. An independently
implemented high-precision inverse agrees with production enclosures on 312
predeclared small-count cases. These results support an auditable reliability
study, not quantum advantage, successful adaptive optimization, unconditional
noise robustness or formally certified floating-point coverage.

## 1. Motivation and relation to prior work

Amplitude-estimation option pricing is established, including circuit and
resource considerations ([Stamatopoulos et al., 2020](https://quantum-journal.org/papers/q-2020-07-06-291/)).
Iterative confidence-set estimation and Bayesian-assisted scheduling also
precede this study ([IQAE](https://www.nature.com/articles/s41534-021-00379-1),
[BAE](https://quantum-journal.org/papers/q-2025-09-11-1856/),
[Bayesian-assisted IQAE](https://quantum-journal.org/papers/q-2026-01-14-1962/)).
The candidate contribution is therefore the audited integration of uncertainty,
refusal and dollar-delivery costs, not a new generic estimator. A newly screened
[basket-pricing paper](https://arxiv.org/abs/2509.09432) also studies accuracy and
resource tradeoffs; the [week-10 methods comparison](WEEK_10_WORKING.md)
identifies overlap and a target-matching concern without claiming priority.
See the bounded
[research refresh](WEEK_9_RESEARCH_REFRESH.md) and earlier reading ledger.

## 2. Target and uncertainty model

For a contract and representation, let the encoded price be O+Sa with S positive
and amplitude a in [0,1]. A contract-dependent deterministic allowance B bounds
the difference from the continuous price. B combines support, grid and encoding
allowances; it is not an empirical correction fitted to the exact answer.

At Grover depth k, p_k(a)=sin²((2k+1)asin(sqrt(a))). Observed success probability
is q_k=f_k+(1-f_k-g_k)p_k(a), with false-positive and false-negative rates f_k,g_k.
Finite zero/one calibration samples define a rectangle of plausible rates.
Supplied transfer allowances expand this rectangle for validation. They are
assumptions, not quantities validated by obtaining a narrow output interval.
Depth-dependent gate noise, correlated observations and arbitrary state-preparation
error are not covered simply by writing this readout model.

## 3. Inference and declaration

Calibration uses two Clopper–Pearson intervals with total failure allocation
0.025. Validation uses depth-wise binomial intervals sharing allocation 0.025.
For each validation interval and expanded calibration rectangle, form an outer
interval for p_k, invert every monotone sine branch, and intersect the resulting
amplitude unions across depths. If positive response contrast cannot be certified,
use the full amplitude interval. Empty intersections are incompatible, not precise.

Map the hull [aL,aU] to [O+S aL-B, O+S aU+B], without clipping away uncertainty.
Declare the requested tolerance tau only if its radius is at most tau; otherwise
report unresolved. A bound-only failure can refuse acquisition. Coverage of the
price interval and error of its midpoint are distinct outcomes.

Under valid calibration, validation and representation assumptions, the standard
union-bound construction gives at least 0.95 price containment in exact arithmetic.
For selection based on pilot history, fresh final observations support the same
argument conditional on that history, provided the stipulated model remains valid.
This does not give coverage conditional on successful declaration. The production
floating-point padding is an engineering safeguard, not a proof of directed rounding.

## 4. Discovery design and resource accounting

Protocols and source snapshots precede their corresponding local runs. This is
local predeclaration, not externally timestamped preregistration or fresh
confirmation. We retain refusals, unresolved outcomes, calibration/pilot costs
and failed promotion screens. Exact pricing references are used for evaluation,
not as inputs to the representation-selector interface.

Resource reports distinguish A-equivalent queries, pricing CX counts, shots and
calibration/pilot acquisitions. Compiled profiles are all-to-all logical profiles
without routing, not fault-tolerant or wall-clock estimates. Equal A-equivalent
budgets need not imply equal CX costs. Native BAE/BIQAE source smokes and strong
classical baseline runs exist, but are not a matched end-to-end competition.

## 5. Results

| Study | Observation | Interpretation |
| --- | --- | --- |
| Week 5 fixed designs | 7200 attempts; 4800 acquisitions; 516 declarations; 4284 unresolved | All declarations were E001. Equal-A multidepth pricing CX cost was approximately 15.62 times direct. |
| Week 6 transfer grid | 32400 attempts; 21600 acquisitions; 2729 declarations; 3 CI misses, all unresolved | 2724 declarations were E001, 1 E014 and 4 E025. Zero erroneous declarations observed. |
| Week 7 ablations | 21600 acquisition attempts; 14400 acquisitions; 28800 executed inference arms; 5042 arm declarations | Shared-observation arms are not independent acquisitions. Nine CI misses included three declared intervals whose midpoint errors remained below $1. All four readiness candidates failed. |
| Week 8 representation selection | 5400 procedures; 3300 final acquisitions; 2100 refusals; 1800 additional pilot acquisitions; 900 declarations | All declarations were E001; all 36 delivery contrasts were zero. Paid selection failed its promotion screen. |

Weeks 5–8 are different discovery designs and their counts must not be pooled as
one homogeneous coverage trial. Week-8 v2 preserves the original seed records;
it corrects execution-limit checking and is not an independent replication.
The three week-7 declared CI misses had midpoint errors approximately $0.473,
$0.237 and $0.461: a miss is not automatically an erroneous $1 declaration.
Zero observed erroneous declarations does not imply zero risk.

The week-8 selector paid 51,677,184 pricing CX for two candidate pilots (15.65%
of its 330,301,440 cap), leaving 278,624,256 for final pricing. Across all week-8
procedures, represented shots totaled 284,589,600 and pricing CX totaled
1,089,951,639,000. These are logical experiment-accounting quantities, not a
hardware speedup. Both deterministic representation infeasibility and statistical
uncertainty limit delivery; neither is fixed by reporting encoded-target precision.

Full cell-level evidence and costs: [week 5](WEEK_5_FIXED_RESULTS.md),
[week 6](WEEK_6_RESULTS.md), [week 7](WEEK_7_RESULTS.md),
[week 8](WEEK_8_RESULTS.md).

## 6. Independent numerical diagnostic

A predeclared matrix uses 128 validation shots per depth and 64 calibration shots
per state, two schedules, four calibration configurations, three guards and 13
observation vectors. The reference uses 80-decimal arithmetic, independent beta-CDF
bisection and explicit amplitude polynomials for k=0,1,2, rather than production
SciPy quantiles and trigonometric inversion. All 312 reference unions were enclosed
by production sets when comparing whole components without extra comparison
tolerance. Eighteen reference sets were empty, 78 full and none finally
multicomponent. Separate tests exercise five-branch k=2 inversion; this does not
turn the final matrix into a multicomponent-intersection test campaign.

Maximum observed endpoint slack was approximately 1.10e-13 in amplitude. The
diagnostic is finite and uses ordinary high-precision arithmetic, not rigorous
interval arithmetic. It does not establish universal enclosure, large-count beta-tail
accuracy, continuous-price bound certification or experimental noise validity.
See [protocol](PROTOCOL_W9_NUMERICAL.md) and [results](WEEK_9_RESULTS.md).

A subsequent week-10 diagnostic exercised large-shot boundary tails using
closed-form binomial identities and independent polynomial inversion. Its
initial 80-case matrix passed enclosure and precision checks but failed the
required disconnected-intersection topology gate. A disclosed, exploratory
three-case extension produced 83 cases with zero enclosure failures or
80-versus-100-digit instabilities, including three disconnected final
intersections. This closes a finite test-coverage gap, not large-count interior
beta-tail validation or formal floating-point certification. See
[week-10 closeout](WEEK_10_CLOSEOUT.md) for preserved runs and qualifications.

## 7. Limitations and conclusion

The tested paid controller did not improve delivery. Broad contract coverage,
matched native/classical comparisons, physical transfer justification, numerical
certification and fresh frozen confirmation remain open. Discovery concentration
on E001 precludes general usefulness claims. The study currently offers a
reproducible reliability-accounting candidate with negative adaptation evidence;
journal-level novelty and sufficiency remain to be demonstrated.

The next stage should address evidence gaps rather than relabel failed screens
as success. Historical unsupported error-floor and slope claims stay withdrawn.
No submission or authorship decision is authorized by this draft.
