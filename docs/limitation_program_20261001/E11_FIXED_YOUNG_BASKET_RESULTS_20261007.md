# E11: fixed Young transport tightens the first-date basket certificate

The fixed-coefficient refinement passed the local run, independent saved-checker review and ROOT saved-result verification. It reduces the first-date basket's squared-error upper allowance by approximately 50%, retaining all four stock certificates and the paid average rounding. Each profile passes the exact strict-improvement criterion.

| Saved certificate display | Previous transport | Fixed Young transport |
|---|---:|---:|
| Basket squared-error upper allowance, dollars squared | 3.16823818462e-6 | 1.58411909472e-6 |
| Basket RMS upper allowance, dollars | 0.00177995454566 | 0.00125861793040 |

The profiles remain separate and agree at the displayed precision. These quantities are upper allowances on the specified native-to-continuous coupling. The full option-price, later-date and payoff transfers remain open.

Write the average of the four stock errors as E, with its Cauchy allowance A=sum(B_i)/4. The source's final stored quarter floor has error r bounded in magnitude by 1/Q, Q=2^40, so F=1/Q squared remains paid. With the predeclared delta=1/1000000000, the pointwise Young inequality gives `(E+r)^2 <= (1+delta)*E^2 + (1+1/delta)*r^2`. The new certificate is therefore `(1+delta)*A + (1+1/delta)*F`.

The previous certificate was `2*(A+F)`. Their exact difference is `(1-delta)*(A-F/delta)`. Consequently, the new allowance is no larger precisely when `delta*A >= F`, with strict improvement when the inequality is strict. Both own-profile saved records pass strictly. No stock/error independence, favorable rounding sign, exact divisibility or adaptive coefficient selection enters the argument. The complete signed difference is retained in canonical limb form; a failed criterion would preserve the parent certificate without adopting an improvement.

The [sealed thirteen-file packet](../../results/limitation_program_20261001/E11_first_date_basket_fixed_young_run001/manifest.json) has manifest SHA256 `fae644369f0e7aefdb2d0fab5f502fbdeca91d1e2fb5694b866bb65484c1de95`. The independently reviewed [ROOT saved verification](../../.context/E11_FIRST_DATE_BASKET_FIXED_YOUNG_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) passed with SHA256 `5143c18beee281a8e2f5903618179ad533dfa19424ee5685689a64bbee8d6b19`. The [rounded display](../../.context/E11_FIRST_DATE_FIXED_YOUNG_VERIFIED_ROUNDED_DISPLAY_run001.json) derives solely from its verified saved scalars.

The scientific test ran once with ROOT-observed exit zero under the unchanged CPU180/admission150/wall600 caps. The checker validates the thirteen-file seal, nine selected premises, current26 source definitions, current14-field release, original136 recorded custody roles, terminal command, canonical fractions, signed difference, exact criterion/adoption flags and five saved metadata controls. It does not replay the parent stock recipes, native arrays, source graph, guards, tails, series or original runtime union.

The [parent four-stock certificate](E11_FIRST_DATE_BASKET_RESULTS_20261007.md) remains frozen. This refinement closes the tested final-floor-transport substep. Later dates, barriers, payoff, full E11 closure and quantum advantage remain open. All files and runs are local.
