# Week 9 claim-to-evidence audit

14 September 2026. Current claim authority for the new working manuscript.

| Candidate statement | Evidence | Boundary / remaining work |
| --- | --- | --- |
| Model-conditional price containment | Finite calibration and validation confidence sets plus deterministic representation allowance; week-4 derivation and calibrated inversion | Requires binomial observations, valid transfer bounds and valid representation bounds. Floating-point implementation is not formally certified. |
| Contract-specific analytical bounds replace illustrative allowances | Weeks 1–2 bound audit; week-8 n5/n6 menu | Bounds are analytical constructions, not directed-rounding certificates. Some contracts fail the $1 bound-only gate. |
| Fixed multidepth designs sometimes deliver useful precision | Week 5: 516 declarations / 4800 acquisitions; week 6: 2729 / 21600 | Mostly E001. Logical pricing CX costs are not total hardware/runtime costs. No broad quantum advantage. |
| Empirical CI misses and dollar errors are different | Week 6: 3 misses, all unresolved. Week 7: 9 arm-level misses, including 3 declared with midpoint error below $1 | Zero observed erroneous declarations does not imply perfect coverage or zero future error risk. |
| Paid representation selection was evaluated honestly | Week 8: 5400 procedures, 1800 additional pilot acquisitions, 900 declarations | All 36 descriptive unpaired delivery contrasts were zero. Promotion screen failed. Do not describe successful adaptation. v2 corrects execution-limit checking and is not a new replicate. |
| Independent numerical implementation agrees on a finite matrix | Week 9: 312 comparisons, zero missing reference components | N=128 validation, N=64 calibration; no final multicomponent references in this matrix. Unit tests cover branch inversion separately. Not universal numerical proof or production-sized beta-tail validation. |
| Novelty is plausible enough for further investigation | Earlier six readings plus focused week-9 primary-source refresh | Priority and journal sufficiency unestablished; newly screened basket paper needs full methods comparison. |
| Publication-ready comparison / confirmation | Not established | Native algorithm smokes and classical baselines exist, but matched end-to-end comparison, frozen fresh confirmation and external review remain open. |

The calibration failure budget is 0.025 and validation budget 0.025 in the
current procedure. Under their assumptions a union bound gives at least 0.95
joint containment in exact arithmetic. This standard argument is not a new
coverage theorem, does not justify the transfer allowances, and does not assert
95% coverage conditional on the event of declaring precision.

The historical contribution document's statements that calibration is absent
and bounds are merely illustrative are superseded. Its proposed controller
remains a hypothesis, not a result. Earlier manuscripts and withdrawn historical
error-floor/slope claims are not reinstated.

Source results: [week 5](WEEK_5_FIXED_RESULTS.md), [week 6](WEEK_6_RESULTS.md),
[week 7](WEEK_7_RESULTS.md), [week 8](WEEK_8_RESULTS.md),
[week 9](WEEK_9_RESULTS.md). This audit does not alter author contributions.
