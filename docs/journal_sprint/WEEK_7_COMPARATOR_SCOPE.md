# Week 7: native comparator semantics and fair scope

Read-only source audit of the pinned local checkouts and adapters. This is
not a new head-to-head experiment, coverage validation or latest-version survey.
The separate reviewer checked checkout HEADs against week-3 planned records,
and matched the inspected source hashes. No source modifications were reported.

BAE pin: `4e1e13d6b151c9a3ca02157ebf6963c1c29ea793`.
BIQAE pin: `bbd28a3efa659e1c0feec6b86ba13389cb127dbd`.

| Question | Native BAE / current adapter | Native BIQAE / current adapter |
|---|---|---|
| Target and output | Amplitude a; posterior weighted mean and SD, including theta-particle representation | Amplitude a; mapped interval and midpoint |
| Uncertainty semantics | Posterior SD, not a validated 95% frequentist confidence interval | Equal-tail Beta quantiles with alpha/max_stages; transported prior fitted from samples; source terminology alone establishes no frequentist coverage |
| Stopping | Cumulative cost checked before another acquisition; may overshoot nominal maxPT | Stops at amplitude interval width <=2 epsilon; no native hard acquisition budget; wrapper has a 1000-job safety cap |
| Query cost | Sum (2m+1)n probing cost; calibration-enabled paths need separate accounting scrutiny | Native sum kn Grover calls; adapter separately logs sum (2k+1)n, including k=0 |
| Finite asymmetric readout and transfer | Coherence damping/plug-in Tc estimation is not this nuisance model | Ideal probability/Beta updates contain no such calibration/transfer envelope |
| Reproducibility caveat | Upstream unseeded default_rng prevents replay from wrapper global seed alone | Wrapper uses persistent seeded generator and separately seeds prior-fitting randomness |

## Concrete local evidence

In `results/journal_sprint/external_bae_sparse/src/algorithms/BAE.py`, inspect
`adaptive_phase` and `inference_warmup`; in `algorithms/samplers.py`, inspect
`param_of_interest` and `mean_and_std`. `utils/models.py` contains `QAEmodel.measure`,
`damp_fun` and `likelihood_theta`. Its damping model is
exp(-m/Tc) p + (1-exp(-m/Tc))/2; learned Tc enters as a plug-in posterior mean.
This does not propagate two finite readout-rate calibration intervals.

In `results/journal_sprint/external_biqae_sparse/src/biae.py`, `_get_prior`
transports 1000 posterior samples and fits Beta parameters;
`_compute_confidence_interval` updates parameters; `estimate` controls interval
width stopping and native query accounting. Native endpoint post-processing
does not by itself add a deterministic continuous-price representation bound.

Adapters: [BAE smoke](../../research/journal_sprint/bae_smoke.py) and
[BIQAE smoke](../../research/journal_sprint/biqae_smoke.py).
Archived week-3 BAE v2 reports 223 actual A-equivalents for nominal budget 200.
BIQAE v2 reports 40 Grover calls but 180 A-equivalents, interval approximately
[.133317,.209960] for a=.17. Single ideal smokes are not comparative evidence.
These local third-party caches are not automatically licensed publication assets.

## Disposition for the next study

Both native adapters remain candidates for **separately designed ideal-response
exploratory comparisons** of estimation error, reported uncertainty, stopping
and actual acquisition costs. First control disclosed random streams, preserve
native stopping behavior and count overshoot/safety termination. Match encoded
targets and dollar transformations; do not compare native Grover calls against
our A-equivalents or label SD as a confidence interval.

Neither current pinned adapter is a matched native comparator for the week-7
finite-calibrated asymmetric-readout/transfer guarantee. A calibration-aware
likelihood extension would be a modified algorithm needing separate validation.
Using our conservative inversion on an upstream acquisition schedule would
compare acquisition policies under our inference, not native BAE/BIQAE coverage.

Accordingly, week 7 makes **no native BAE/BIQAE superiority claim**. The main
matrix remains gated on an explicitly matched claim. The week-3 classical
European/Asian baselines also remain a separate experiment, not evidence that
current query counts beat classical pricing runtime.
