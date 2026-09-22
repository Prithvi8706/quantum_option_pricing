# Focused prior-art check for the companion benchmark

22 September 2026. This check concerns the proposed controlled compound
Asian-basket benchmark and its error/resource certificates. It does not reopen
the search for a different advantage mechanism. **No new quantum algorithm,
first resource estimate, or significant quantum advantage is established.**

Searches used combinations of “quantum compound option pricing”, “quantum option
pricing control variates resources”, “compound option basket”, and finite-law /
quantized control-variate bias, followed to primary papers. Exact-phrase searches
had poor recall and produced irrelevant chemistry hits. Those are not evidence
of novelty. The table records the relevant primary material actually examined;
it is a bounded comparison, not exhaustive coverage of finance or compilers.

| Primary source and status | Reading depth in this follow-up | Existing result that limits novelty | Defensible distinction for our work |
|---|---|---|---|
| [Blanchet, Hamoudi, Szegedy and Wang, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1b12cec51490d59484096f178c0f81be-Abstract-Conference.html), [paper v2](https://arxiv.org/pdf/2502.05094) | Sections 1.1 and 4 rechecked against the primary PDF; earlier repository assessment read the full paper | Call-on-call pricing is already an explicit application of quantum nested estimation. Generic nested-query bounds do not certify difficulty of a particular financial model. | Same-contract comparison after classical controls, emitted source cost and explicit estimator constants. Applying nested quantum estimation to a compound option is not our novelty. |
| [Kothari and O'Donnell, SODA 2023 / arXiv 2022](https://arxiv.org/html/2208.07544v1) | Theorems 1.1/1.3, Section 3.6 and the source-access discussion inspected; existing local full text consulted | Variance-sensitive source-code mean estimation, complex phases, binary-search reductions and the Hadamard-test alternative to phase estimation already exist. | Concrete finite-confidence allocation and its resource effect on this source. The Hadamard replacement is an implementation of existing ideas, not a new estimator theorem. |
| [Chakrabarti et al., Quantum 5, 463 (2021)](https://arxiv.org/html/2012.03819v3) | Sections 2, 3.3, 4.1.1 and resource tables inspected; appendix structure checked | Derivative-pricing resource estimation already includes path loading, normalization, approximation errors and arithmetic costs. | Emitted, replayable digital source plus controlled classical comparator and separately bounded law mismatch. Do not claim the first complete derivative-resource analysis. |
| [Wang and Kan, Quantum 8, 1504 (2024)](https://arxiv.org/html/2312.15871v3) | Tables 6–7, surrounding resource discussion and selected synthesis/Gaussian-loading appendix passages inspected | Asian/barrier resource comparisons already count T gates, T depth and logical qubits and show preparation can dominate. | Different compound Asian-basket output and strong classical controls; exact source artifacts and the financial-law bridge. A quantum-circuit improvement is not an advantage claim. |
| [Herman et al., arXiv:2602.03725v1 (2026)](https://arxiv.org/html/2602.03725v1), preprint on the inspected primary record | Sections 4.2–4.3 closely inspected in cached primary full text; current primary record checked | An explicit derivative-pricing framework already separates and couples truncation, discretization, arithmetic, distribution and estimation errors; improved quadrature analysis changes resources. | Concrete bounds for this midpoint Box–Muller/guard/reset implementation and this control identity. “We account for all errors” is neither a new general framework nor an achieved full-price certificate here. |
| [Lemaire, Montes and Pagès, JCAM 371 (2020)](https://arxiv.org/html/1903.10330), [publication record](https://arxiv.org/abs/1903.10330) | Sections 4.1 and 4.2.2, equations (4.2)–(4.5), and bias/MSE decomposition read | Quantized approximate control means introduce an explicit bias, and compound-option nesting can be removed using a known conditional pricing formula. | Our numerical coupling bound is for a different finite input law, guard/reset transformation and joint payoff/control combination. The general observation that approximate controls are biased is not new. |
| [Kemna and Vorst, JBF 14 (1990)](https://www.sciencedirect.com/science/article/pii/0378426690900395) | Publisher abstract and bibliographic record only; full text inaccessible in this follow-up | Variance-reduced Monte Carlo for average-value options is longstanding. | Do not present classical variance reduction for Asian options as a new contribution. No detailed theorem assessment is based on this abstract-only reading. |

The finite-policy identity also deserves restrained treatment. For a policy
d(X) in {0,1}, subtracting its value from the optimal one yields

    (C(X)-K)+ = d(X)*(C(X)-K) + regret(X),   regret(X) >= 0.

Taking conditional expectations and adding/subtracting a shared control gives
the baseline-plus-residual decomposition. This is elementary algebra and the
tower property. Analyzing that sum jointly avoids a needless pointwise
exercise-decision stability requirement, but does not establish a novel general
control or stopping theorem. The specific quantitative bounds and counterexamples
are the candidates for new analysis.

## Narrow claim that survives this check

“We provide an auditable controlled compound Asian-basket pricing benchmark that
connects the implemented finite probability law and reversible source to
explicit estimator costs, with separately verified error components and strong
classical comparisons. The evaluated implementation and conditional physical
models do not establish the declared quantum-over-classical crossover.”

That statement is a contribution description, not a priority claim. A manuscript
can substantiate it with the exact artifact bundle and comparisons, without
saying nobody has studied related compounds, controls, arithmetic or accounting.
The distinctive practical evidence is the conjunction of reproducible source
execution, the contract-specific law/control certificate, and a fair comparator;
whether that conjunction is sufficient journal novelty is an editorial judgment.

Before submission, the independent manuscript review should check that each
claimed new proposition is limited to its actual hypotheses and that all
reported improvements use a named comparator. The present bounded search found
no reason to promote the contribution to a new mean-estimation algorithm or a
quantum advantage result. It also found no exact duplicate of the entire emitted
benchmark among the inspected papers; that limited observation is not proof of
priority.
