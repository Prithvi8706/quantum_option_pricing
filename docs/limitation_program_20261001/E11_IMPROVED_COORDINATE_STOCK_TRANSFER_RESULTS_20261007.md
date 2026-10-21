# E11: improved coordinate certificate reaches the first two stocks

The improved native-coordinate certificate now propagates to the original first two stocks and their subtotal. Both profiles passed independent source review, the local run and ROOT saved-result verification. Each stock's squared-error upper allowance is about **99.498% smaller**. This improves a certificate; it is not an observed RMS estimate or a financial price certificate.

| Squared-L2 upper allowance, approximately | Primary90 | Independent130 |
|---|---:|---:|
| Raw log transport | 8.04528421441e-12 | 8.04528421441e-12 |
| Each stock, dollars squared | 1.58411909231e-6 | 1.58411909231e-6 |
| Previous stock allowance, dollars squared | 0.00031537848318 | 0.00031537848318 |
| Two-stock subtotal, dollars squared | 6.33647636925e-6 | 6.33647636925e-6 |

The corresponding stock RMS-error upper allowance is approximately $0.00125862. The two profiles agree at the displayed precision; their exact fractions remain separate. Values come from the [verified rounded display](../../.context/E11_IMPROVED_COORDINATE_STOCK_VERIFIED_ROUNDED_DISPLAY_run001.json), not from a fresh numerical recipe.

The transfer takes the [verified new per-coordinate squared-L2 allowance](E11_NATIVE_COMPOSITION_RESULTS_20261007.md) `C`, following the [radial-cell improvement](E11_RADIAL_CELL_RESULTS_20261007.md), into the original five-term log proof. Each profile keeps its own coefficients and constant allowances:

`B_log_new = 5 * ((aN^2 + bN^2) * C + ea^2 + eb^2 + kappa^2)`.

The stock step retains the original native exponential allowance `A`, projection limit `M`, lower continuous Gaussian tail and upper tilted continuous Gaussian tail:

`B_stock_new = 3 * (A^2 + M^2 * B_log_new + T_lower + T_upper)`.

Only the coordinate and log transport allowances change. The sampler, native arithmetic, source log interval, projection proof, three original guards, moment order and both unconditional tail allowances remain the saved premises. The argument uses pointwise squared triangle inequalities; it assumes no independence of native coordinates, approximation errors or stock errors. Primary90 and independent130 profiles stay separate throughout.

The source scope is first-date B4x12 stock `4021`, the separately justified same-marginal stock `4417`, and their exact native subtotal `5573`. The second stock uses the original proof for its first-cosine source branch and the same saved stock projection operands. Its shared common factor with the first stock remains in the model. The subtotal uses `2 * (B_4021 + B_4417)` after the original no-wrap proof; it adds no rounding error. Other stocks, the four-stock basket average, later dates, payoff, policy, price, full E11 closure and quantum advantage remain open.

The subsequent [first-date basket certificate](E11_FIRST_DATE_BASKET_RESULTS_20261007.md) now covers the remaining two stocks and the four-stock native average, with its quarter-floor error paid. Later dates, payoff and option-price transfer remain open.

The [sealed thirteen-file packet](../../results/limitation_program_20261001/E11_improved_coordinate_first_two_stock_transfer_run001/manifest.json) has manifest SHA256 `50b215aff5abbfcc6a6ab76f0dfae5eaa2bae90e89f7791dc446b3d80391b454`. ROOT observed terminal exit zero under the unchanged CPU180, admission150 and wall600-second caps. The independently reviewed [ROOT saved verification](../../.context/E11_IMPROVED_COORDINATE_FIRST_TWO_STOCK_TRANSFER_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) passed with SHA256 `41050651adc292d1af230895d008ae88c70bdf9cebe065c4ac21230e91e8806f`. It checked all thirteen output hashes, selected certified premises, both profile identities, canonical base-2^32 rational limbs, five artificial metadata controls and source qualifications. Historical large decimal certificate fields remain opaque metadata and are not numerical recipe inputs.

The next proposed extension is the remaining two first-date stocks and their basket average. It needs exact source-branch witnesses, the retained projection premises and the actual quarter-scaling rounding allowance before any new certificate. All work remains local.
