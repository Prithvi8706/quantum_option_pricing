# Focused source check, 22 September 2026

This is a follow-up to the repository's broad September22 search, not another
claim of exhaustive literature coverage. The experiment tests conditional
controls and policy localization specifically. Search results and publication
dates were distinguished from PDF upload/crawl dates.

| Primary source | Status / reading depth | What matters here | Decision |
|---|---|---|---|
| [Blanchet, Hamoudi, Szegedy, Wang: Quantum speedup of non-linear Monte Carlo problems](https://arxiv.org/abs/2502.05094), v2,22 Oct2025 | NeurIPS2025 manuscript; full text archived from prior investigation; Section3 assumptions, Algorithms2–4 and appendix obligations rechecked | Conditional raw moment must be bounded for every exercise state in this formulation. It explicitly permits residual noise around a regression function. This means residual substitution is already within the prior theory; it is not a new quantum speedup theorem. | Relevant theory, not pricing advantage or novelty proof |
| [Sun, Wang, Blanchet: Optimal Quantum Speedups for Repeatedly Nested Expectation Estimation](https://arxiv.org/abs/2602.08120),8 Feb2026 | arXiv preprint; full text previously archived; Sections1.2,3.1–3.3 and algorithms rechecked live | Generalizes nesting under source-access assumptions. Deterministic level scheduling handles a variable-time obstruction. A rare boundary event cannot simply multiply a fixed coherent circuit's runtime by its probability. | Background for a genuinely new coherent localization algorithm; not needed for a flat mean |
| [Kothari and O'Donnell: Mean estimation when you have the source code](https://arxiv.org/abs/2208.07544) | SODA2023 paper; archived full text, main theorem and source-access definition reread | Stronger variance-sensitive query scaling than our conservative signed dyadic implementation. Unknown constants and implementation costs remain. The unit-constant sensitivity curve is not this algorithm's compiled resource estimate. | Retain as an explicitly uncompiled improvement opportunity |
| [Maurer and Pontil: Empirical Bernstein Bounds and Sample Variance Penalization](https://arxiv.org/abs/0907.3740),2009 | Full primary PDF accessible; Theorem4 and proof conditions rechecked | Supplies fixed-N confidence bounds using proved support and sample variance. Apply to independent outer groups, split moment failures before choosing the smaller of two bounds, retain the range term after zero observations. | Implemented statistical tool; exact iid/real-evaluation premises explicit |
| [Rogers and Shi / Curran bounds as developed by Thompson: Fast narrow bounds on the value of Asian options](https://www.jbs.cam.ac.uk/wp-content/uploads/2020/08/wp0209-1.pdf) | Cambridge primary working paper; Sections2–4 relevant conditioning/lower/upper derivations checked; classical foundational work, not a2026 result | Conditioning, geometric controls and replacing the true in-the-money event with an approximate event have long histories. Our two-control/parity decomposition must not be marketed as their invention. Stronger one-dimensional conditional integration remains a classical competitor. | Classical prior art; no new advantage inferred |
| [Chen et al.: Nested Expectations with Kernel Quadrature](https://proceedings.mlr.press/v267/chen25av.html),2025 | ICML2025 proceedings; previously investigated full manuscript, not rerun in this follow-up | A relevant additional classical method if a candidate survives the cheaper control-variate baseline. | Implementation deferred because current quantum resource gate fails |

Targeted searches for quantum residual/control-variate option pricing and
exercise-boundary localization did not establish an existing end-to-end
implementation that closes this project's cost gap. That search outcome is
not evidence of novelty. The present contribution is a project-specific
derivation, tested implementation, uncertainty audit and cost comparison.

No vendor hardware claim was used to improve the crossover. T-layer times in
the sensitivity table are hypothetical inputs; they are not achieved system
specifications, physical cycle times or a promised architecture.
