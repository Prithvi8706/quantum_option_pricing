# Week-11 quantum contribution and prior-work checkpoint

Updated 2026-09-15. Focused primary-source refresh, not an exhaustive priority
search or full independent proof audit. This supplement does not retroactively
claim that newly screened methods have been implemented.

The user's objective remains a quantum-centered pricing result. Week-11 classical
work is the comparison infrastructure, not that result. The k=0 statistical
allocator cannot demonstrate amplitude-estimation query scaling. A successful
allocation experiment alone must not be presented as a new quantum algorithm.

| Prior work, source and reading depth this turn | Occupied territory | Consequence for this project |
|---|---|---|
| [Ramôa/Santos, BAE, Quantum 2025](https://quantum-journal.org/papers/q-2025-09-11-1856/); publisher abstract/status refresh | Noise-aware adaptive estimation and experimental cost trade-offs | No claim of first noise-aware or resource-adaptive QAE. Compare faithful native behavior, not a weakened fixed-schedule substitute. |
| [Labib, September 2026 preprint](https://arxiv.org/abs/2609.02715v1); abstract/status refresh | Non-power-of-two deterministic depth schedules, likelihood estimation and depth/query trade-offs | A new ladder ratio or depth cap is not sufficient novelty; reported constants need their own reproduction before use. |
| [Recchia et al., September 2026 preprint](https://arxiv.org/abs/2609.03625v1); abstract/status refresh | Coherent low-discrepancy nets and finite-query advantage windows; no claimed asymptotic improvement over classical QMC | A coherent-Sobol construction alone is not ours. An application would need payoff/loading costs and comparison to optimized RQMC. |
| [Kim et al., July 2026 preprint](https://arxiv.org/html/2607.14518v1); focused introduction, sample-estimable formulation and depth analysis | TT-informed marginal loading, latent basket-CDF matching and fixed-depth online resource scaling | Payoff-relevant distribution compression and CDF-based pricing control are already studied. Fixed-circuit sample bounds are not a blanket certificate for arbitrary adaptive training. |
| [Hok/Leitao, January 2026 preprint](https://arxiv.org/abs/2601.04049); abstract and HTML keyword screen | Market-consistent multidimensional QAE pricing pipeline and query comparisons | Neither adding assets nor using market distributions is enough. Absence of an HTML keyword is not proof a comparator is absent from every version. |
| [Herman et al., February 2026 preprint](https://arxiv.org/abs/2602.03725v1); abstract/status refresh, earlier focused assumptions audit retained | Coherent samplers and speedups for CIR/restricted Heston and certain multidimensional processes | A scalar parameter screen does not implement the sampler or establish all theorem conditions. Finite resource costs remain necessary. |
| [Blanchet et al., v2](https://arxiv.org/abs/2502.05094v2); metadata/abstract refresh, earlier focused section-3 reading retained | Quantum-designed multilevel approximations for nonlinear/nested expectations | Generic QAE around classical nesting is not the same algorithm. arXiv now lists a NeurIPS 2025 proceedings reference; do not describe it solely as an unreviewed preprint. |

## Testable distinctions, not established novelty

1. **Supporting method:** fresh-sample, encoding-aware allocation of two unequal
   calibration budgets and a pricing budget, evaluated by delivered dollar
   tolerance and full acquisition cost. CP/CS ingredients and variance-allocation
   heuristics are standard. A useful application-specific decision result still
   needs to survive strong fixed/equal-pilot comparisons and a closer priority audit.
2. **Quantum-centered candidate:** a task-specific encoding/preparation route
   with a complete dollar error budget and actual nonzero-depth AE, whose full
   resource profile remains useful against strong classical conditioning/RQMC.
   This is a research question, not an implemented or proven advantage result.
3. **Potential loader validation question:** after fitting a payoff-relevant
   state, can independent validation produce a useful price-error allowance
   after counting training, validation and repeated coherent loading? Inference:
   fixed-parameter concentration motivates fresh validation, but neither a new
   theorem nor an uncovered literature gap follows from that observation.

For any learned loader, distinguish fixed architecture depth from depth/training
needed at a specified accuracy. Classical samples used to train/validate a loader
can also price the claim; compare that direct alternative. Approximation error
must enter B, not be hidden behind high state fidelity or a mean training loss.

## Decision

GO for bounded development/benchmarking. NO-GO for claims of quantum advantage,
new quantum algorithm, optimal allocation or submission readiness. Keep the
quantum resource/encoding feasibility gate explicit before scaling the publication
campaign. Do not relabel the week-11 classical benchmark as a quantum experiment.
