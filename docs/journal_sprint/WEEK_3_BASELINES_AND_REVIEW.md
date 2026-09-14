# Week 3 baseline results and review status

12 September 2026. Discovery work; not journal readiness or a quantum-advantage
claim. The PR remains held pending the requested review providers and final
review checks. Original completed archives have not been rewritten.

## Classical and larger-circuit results

The [classical protocol](PROTOCOL_W3_CLASSICAL.md) produced 480 estimates:
six European contracts plus arithmetic Asian calls with 8 and 32 monitoring
dates, three estimators, two evaluation budgets, ten repetitions per cell.
European Black–Scholes prices agree with independent quadrature within 1e-8.
Asian reference estimates are 6.35216816 (SE 0.00001927) and 5.91056204
(SE 0.00002340), respectively; neither is exact truth.

At 16,384 evaluation paths, the Asian RMS deviations from those references are:

| Dates | Plain MC | Independent-pilot CV-MC | Scrambled RQMC + CV |
|---|---:|---:|---:|
| 8 | 0.0701715 | 0.00158005 | 0.000419316 |
| 32 | 0.0437351 | 0.00140406 | 0.000321825 |

CV methods additionally use 1,024 pilot paths: 17,408 total per trial. Reference
generation is separately recorded. RQMC is not uniformly best across the six
European smoke cells. These ten-repetition results do not establish coverage,
an asymptotic convergence rate, or practical quantum speedup. Inverse-normal
RQMC clips numerical endpoints to machine epsilon; no exact unbiasedness claim
is made for that finite-precision implementation.

The [larger-register protocol](PROTOCOL_W3_RESOURCES.md) completed 20 circuits.
Maximum ideal-probability discrepancy is 2.29e-13 (tolerance 1e-9).
Initial smoke: 0.384 seconds, estimated 32 KiB state array; total 53.23 seconds.
At n=5, k=0/1 use 210/3,698 CX gates; at n=6 they use 280/13,124.
Total registers are 11/13 qubits. No routing, density-matrix noise or hardware
was simulated here. Archived `compile_seconds` includes bound/preparation work;
the current runner calls it `preparation_and_compile_seconds` instead.

## Stronger comparator source smokes

Public source checkouts are local caches, not bundled publication assets.

- BAE: `alexandra-frca/BAE`, commit
  `4e1e13d6b151c9a3ca02157ebf6963c1c29ea793`. An ideal a=.17 source smoke
  with 200 particles completed after a nominal 200-A-equivalent budget.
  Actual measurement costs, including warmup and final-step overshoot, are
  recorded. Posterior SD is not converted to a confidence interval. Upstream
  resampling uses unseeded `default_rng`, so the recorded global seed alone
  does not guarantee replay. No noisy calibration or coverage validation here.
  Initial import failed because the host's `src` package shadowed upstream's
  namespace directory; the isolated-subprocess namespace adapter fixes this.
- BIQAE: `Kirin0570/BIQAE`, commit
  `bbd28a3efa659e1c0feec6b86ba13389cb127dbd`. Source file has an Apache-2.0
  header. Run in a separate Qiskit 1.4.2/Aer .15.1 environment, preserving the
  algorithm's fitted-Beta intervals and width-based stopping. Corrected local
  a=.17 smoke gives midpoint .17163861, interval [.13331722,.20996000],
  100 shots, 40 Grover queries and **180 A-equivalent queries**. Those cost
  units are different; do not compare 40 directly with our A-equivalent costs.
  The first adapter used an integer simulator seed, repeating the same random
  stream per job. That result is explicitly invalidated; retry uses one
  advancing Generator. This was our adapter error, not an upstream failure.

Both are plumbing smokes, not a matched benchmark or frequentist validation.
No author-source algorithms were silently replaced with our interval method.

## Independent review and corrections

A separate agent audited the accumulated work, including 480 classical rows,
10,000 stress inferences, archived hashes and larger-circuit reconstruction.
It reported no demonstrated result-invalidating defect, while identifying:

1. A dependency recipe inconsistent with the successful legacy environment.
   A separate fresh environment now passes all 89 current sprint tests and
   replays the 24-circuit gate, matching original gates, depths, ideal and noisy
   probabilities within 1e-9. All 54 installed package pins and a successful
   `pip check` are archived. This is validated compatibility for the replayed
   scope, not a claim that every historical experiment was rerun.
2. Missing output overrides: added for classical, readout and larger-resource
   runners, retaining exclusive output creation.
3. Comparator completion preceding golden acceptance: acceptance now precedes
   completion; the verifier also checks historical golden outcomes.
4. Unknown classical method strings falling back to MC: now rejected.
5. A handoff snapshot lacking standalone dependencies: explicitly labeled a
   supplement to the repository, not an independently runnable package.
6. The misleading timing label described above: corrected prospectively.

The final integrated repository suite passed **253 tests**, with 11 legacy
warnings, in 192.24 seconds (`tests_week3_final_integrated.xml`). The 16-test
focused check and the 89-test fresh-environment sprint run also passed.
These totals overlap; do not add them together.
They cover multi-date geometric-control quadrature, readout output handling,
and failed-golden rejection without a completion marker. Ruff passes.
The v2 summary script verified 926 artifact hashes across ten archives,
including both comparator smoke wrappers, installed environments and clean
circuit replay. It also checks historical golden acceptance. The separate
modern-environment stream regression reproduced [3,0,1,1,2] twice.

Final comparator smoke archives are `week3_bae_smoke_v2` and
`week3_biqae_smoke_v2`; each includes a producing-wrapper snapshot and manifest.
The BIQAE environment's 37 package pins and successful dependency check are
also archived. BAE remains non-deterministic in its disclosed upstream
resampling component; no source-level reproducibility claim is substituted.

The independent reviewer was spawned with explicit `model: gpt-6-astra`, and
the request was accepted. It subsequently retracted its unsupported statement
that Astra was unavailable; it did not independently inspect runtime metadata.
This is an automated review, not an independent human or journal referee review.
After a usage-limit interruption, a second explicitly requested Astra reviewer
completed the bounded final check of fixes and corrected artifacts. It verified
all 926 hashes, confirmed the comparator ledgers and stream regression, and
found exact agreement in recorded resources and ideal/noisy probabilities for
all 24 original/clean circuit pairs. It found no new demonstrated
scientific-invalidating defect. This final check supplements the earlier
accumulated-work audit; it did not repeat every week-1/2 experiment or citation.
Macroscope is not installed/connected locally;
its CLI requires account setup and credits. No Macroscope review has occurred.

## Confirmation decision: hold

Do not freeze or launch held-out confirmation yet. First define a claim that
survives the demonstrated response-model failures and correctly distinguishes
unconditional erroneous declaration from correctness conditional on delivery.
Then specify matched comparator budgets, deterministic representation limits,
calibration costs and strong fixed baselines before any adaptive-policy promotion.
The current results support a discovery/methodology contribution, not a claim
that the pricing method beats strong classical alternatives or works on hardware.

Contributor acceptance and publication spending remain unconfirmed. No names
or contributions have been invented, and no paper has been submitted.
