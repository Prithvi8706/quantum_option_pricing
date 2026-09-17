# Four-paper audit and bounded transfer results

Status: full **author-version** reading and equation/method audit completed;
selected identities and a loader improvement independently implemented. This is
not reproduction of every author's experiment or proof of quantum advantage.
Earlier development closeout: [PRE_LITERATURE_CLOSEOUT.md](PRE_LITERATURE_CLOSEOUT.md).

## Source and review boundary

Read all 32 pages of the four pinned author PDFs, including appendices, tables,
figure captions and references. PDF hashes/URLs/page counts are in
`results/journal_sprint/four_paper_audit_v1/sources.json`. PDFs remain in ignored
`.context/four_papers_v1`, not redistributed with the project. The Walsh paper's
four-page author preprint has the conference DOI on its arXiv record. The
six-page publisher version was inaccessible; equivalence is **not verified**.
The other three audits likewise identify the precise arXiv versions reviewed.
This is a main-agent audit, not independent subagent or human review.

Equation ledgers and methodology assessments:

- [Autocallable exponential integration](FOUR_PAPER_AUTOCALLABLE.md)
- [Arithmetic resource estimation](FOUR_PAPER_ARITHMETIC.md)
- [Regression/state-preparation optimization](FOUR_PAPER_REGRESSION.md)
- [Walsh loader correction](FOUR_PAPER_WALSH.md)

Read-only author-code inspection: pinned Walsh notebook; arithmetic constant
adder, estimator and superposition test helper; both Classiq finance notebooks.
Hashes are in `author_code_v2.json`. These current repository commits are not
assumed to be the exact commits used for the papers. No author code was executed,
no AGPL code copied, no Classiq synthesis/cloud execution submitted, and no
published resource-estimator plots independently reproduced.

## What actually transfers

| Component | Decision for the existing arithmetic Asian basket |
|---|---|
| Partial exponential comparator payoff | Not a drop-in replacement: arithmetic mean is not exponential of mean log-price. Keep the QSP/LCU route and its error obligations. |
| Arithmetic Pareto selection | Applicable to a separate explicit-arithmetic comparator route; benchmark our bit widths, controlled inverses and cleanup, not published thousand-bit crossovers. |
| Rotation sharing | Implemented in a deterministic marginal loader, avoiding the regression algorithm's postselection. |
| Walsh constant-phase correction | Applied as a verification requirement: compare controlled full operators, not state fidelity alone. No truncated WSL replacement admitted. |

## Independent results, not imported author results

New producers: `four_paper_probes.py`, `run_four_paper_probes.py`, and
`run_four_paper_baselines.py`. Acquisitions preserve all tested cases, including
the first library-based implementation (`four_paper_probes_v1`).

1. Geometric product probabilities agree with direct finite sums to
   2.23e-16 in the bounded sweep, including zero/negative rates. Inclusive
   endpoint identities are checked separately.
2. On a four-entry test, omitting the Walsh mean term leaves fidelity about
   0.0339 even as the small-angle parameter decreases. Retaining it gives
   fidelity about 0.999999991 at epsilon=0.001, **but success probability is only
   2.72e-7**. High conditional fidelity does not mean cheap preparation.
3. At q10, Gaussian regression-style small-angle loading succeeds with
   probability 0.000975845. An independently derived arcsin/envelope repair gives
   0.313312 and exact target amplitudes in real arithmetic. These are analytic
   branch evaluations, not compiled loader executions. The repair is standard
   rejection/amplitude-transduction reasoning, not established novelty.
4. The implemented deterministic loader groups all disjoint prefix rotations at
   a tree level into a cyclic Gray-code multiplexer. It uses the old certified
   plan's stored angles; no new Gaussian fitting, rejection or added ancilla.
   At q6, unoptimized native decomposition changes **1876 CX to 62 CX**, depth
   **7432 to 116** in the stated RY/RZ/H/X/CX basis. This comparison is against
   our inefficient prefix implementation, not a state-of-the-art loader.
5. q10 compiled marginal: **1022 CX, 999 RY, depth 2012**, all-to-all ideal
   logical gates. Exact rational angle accounting bounds the operator change
   from the stored-angle tree by **3.78604e-16** per marginal. Add this to the
   prior loader error; do not replace it or count it as physical gate synthesis.

The initial library decomposition dropped small rotations, giving a q10 operator
bound of 6.17443e-10. It is preserved as a diagnostic, not passed off as identical
to the old error certificate. The final decomposition computes Walsh/Gray-code
rotation coefficients as exact rationals and rounds each once, with no hidden
threshold. For fixed control words, signed angles are summed exactly; the maximum
angle discrepancy/2 at each layer bounds that layer's operator error. The sum
of layer bounds covers arbitrary input states and controlled use. Tests also
check the entire controlled operator for q1..4 and inverses, not only |0> output.

Generic dense-state preparation is included as an additional strong quantum
control in `four_paper_baselines_v1`, at compiler optimization levels 0 and 3.
At q6/level3 in the U/CX basis: prefix1874CX/depth3150,
folded62CX/depth108, standard62CX/depth102. The standard loader is slightly
shallower; our contribution here is preserving the existing certified angle
plan with an explicit operator-error bridge, not beating that standard loader.
Do not advertise the large prefix-to-multiplexer reduction without that control.
The final method is a known circuit-synthesis technique, not a new quantum
algorithm or evidence against classical simulation of these small cases.

Verification: full regression **1092passed**,12legacywarnings (429.55s), including
21new tests. Final probe and strong-baseline payloads replayed bit-for-bit using
the pre-existing isolated week15 environment. Replay receipts check critical
producer hashes and all acquisition artifacts; this is not independent agent or
human scientific review. Source-acquisition helpers are not runtime dependencies
of the numeric experiment. The exploratory v1 producer was superseded; its
results are preserved, but only v2 has a current-producer replay guarantee.
No remote push, PR, merge or hardware execution was performed.
Clean checkout `6c14d69f`:21new tests passed in the existing isolated environment;
both stored replay/hash checks also passed. This did not rerun the full suite
or acquisition from the clean checkout. Verification receipts are archived
under `results/journal_sprint/four_paper_clean_*`.

## How an actual advantage would have to arise

Let the amplitude oracle encode price as `P = c + R*a`, and let
`e_stat = e_total - sum(certified systematic errors)` be strictly positive.
Any unknown systematic component means this comparison is not yet admissible.
For a particular proved AE schedule, write its query budget as
`N_Q(e_stat/R, delta)`; include preparations, inverses, reflections, shots,
classical construction, decoding and fault-tolerant synthesis in `T_Q`.
Compare with the **measured** cost of the best classical method at the same
continuous target, error and failure probability, including conditioning and
randomized quasi-Monte Carlo (RQMC). Formal AE query scaling alone is insufficient.

For intuition only, suppose classical RMS error behaves as `A*N^(-alpha)` and
AE queries as `c*R/e_stat`. Ignoring setup and logarithmic factors, a necessary
cost-rate screen is

`cost_Q/cost_C < A^(1/alpha)/(c*R) * e_stat^(1 - 1/alpha)`.

This is a conditional scaling identity, **not a fitted crossover prediction**.
For alpha=1/2 tightening precision can compensate for a slow quantum oracle.
For alpha=1 there is no exponent advantage; constants dominate. For alpha>1
the classical asymptotic rate is better under this model. RQMC rates cannot be
assumed universal or inferred from a conveniently selected small pilot.

Combining improvements multiplies only costs on the same executed path. Parallel
depth, total gate count, loader success and payoff scale cannot be multiplied
as independent headline speedups. Amdahl's law limits payoff-only gains.

## Priority and stopping rules

1. **Existing basket, immediate:** integrate the certified multiplexer as an
   optional producer in a new pricing archive; preserve old archives. Complete
   signal-operator and execution-model bounds. The old partial $0.807293 sum
   remains partial: this loader change does not resolve those missing terms.
2. **Existing basket, competing encoding:** cost explicit reversible payoff plus
   a uniform-threshold comparator against QSP at identical accuracy. Exact
   finite payoff removes polynomial bias but buys expensive arithmetic; no
   benefit is assumed. Use width-specific arithmetic selection and clean inverses.
3. **Separate contract study:** the strongest direct fit of the autocallable idea
   is best/worst-of path-dependent payoff with log-domain comparisons. This is
   an alternative study, not permission to relabel the existing Asian contract.
   Its classical controls must include conditional smoothing and RQMC. Nested
   expectations remain a separate possible direction, not a result of these papers.
4. Reject an encoding if its scale/success/implementation costs erase the gain.
   Promote only a predeclared, independently verified same-error comparison.

**Conclusion:** a substantial, checked improvement to our quantum circuit is
available. None of these four papers, nor our new tests, secures end-to-end
quantum superiority. The defensible outcome today is a tighter quantum resource
and correctness study with a clearer advantage test—not a positive advantage
claim manufactured by combining incompatible improvements.
