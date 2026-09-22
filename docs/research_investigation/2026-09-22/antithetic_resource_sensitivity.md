# Antithetic resource sensitivity coordinate

Date: 2026-09-22. This calculation reads the preserved development pilot variances; it reruns no paths.

**This is an uncompiled sensitivity model, not a lower bound, resource estimate, or feasibility result.**

Let sigma_l=sqrt(V_l), where V_l is the observed antithetic correction variance, and include the independent level-zero payoff variance. Assume oracle costs c_l=c0*w_l with w0=1 and w_l=2.5*2^l for l>=1. The latter counts two fine paths plus one coarse path relative to a 12-step base path; it ignores fixed overhead and all differences in reversible implementation.

If, illustratively, an estimator costs k*c_l*sigma_l/e_l to achieve additive statistical error e_l, minimizing the sum of those costs subject to sum(e_l)=epsilon_stat gives e_l proportional to sqrt(w_l*sigma_l), and

```
B = (sum_l sqrt(w_l*sqrt(V_l)))^2
Tq = k*c0*B/epsilon_stat
c0_allowed = Tc*epsilon_stat/(10*k*B).
```

This algebra assumes a particular additive error allocation; it does not establish that an implemented quantum estimator attains the model. Statistical error budget is 0.45*0.01=0.0045 price units. The remainder is reserved but has not been shown sufficient for bias or any other error. The chosen 10-fold latency criterion is a practical target, not statistical significance.

| Case | Base V0 | Exact base sigma0 term in B expansion | Base sqrt(sigma0) term inside sum | Full B, levels 0--5 |
|---|---:|---:|---:|---:|
| A1 | 135.583966013 | 11.6440528173 | 3.41233832105 | 50.3254894827 |
| A4 | 63.0278325752 | 7.93900702703 | 2.81762435875 | 28.7225271777 |

The base contribution is included exactly as the saved sample estimate permits: w0*sigma0=sqrt(V0), plus its cross terms with the other levels after squaring the sum. Full precision values and all six per-level terms are retained in the JSON.

Allowed c0 below is in **microseconds per illustrative base coherent oracle**, before any fixed overhead:

| Classical total Tc (seconds) | k | A1 allowed c0 (microseconds) | A4 allowed c0 (microseconds) |
|---:|---:|---:|---:|
| 0.1 | 1 | 0.894179082 | 1.56671451 |
| 0.1 | 10 | 0.0894179082 | 0.156671451 |
| 0.1 | 100 | 0.00894179082 | 0.0156671451 |
| 1 | 1 | 8.94179082 | 15.6671451 |
| 1 | 10 | 0.894179082 | 1.56671451 |
| 1 | 100 | 0.0894179082 | 0.156671451 |
| 10 | 1 | 89.4179082 | 156.671451 |
| 10 | 10 | 8.94179082 | 15.6671451 |
| 10 | 100 | 0.894179082 | 1.56671451 |

Caveats:

- Uses empirical sample variances; no certified variance bounds or remaining-bias proof.
- Weights are an uncompiled arithmetic step-count model ignoring fixed overhead and reversibility details.
- Unknown k stands in for estimator constants, logarithmic factors, repetitions, and confidence allocation; k=1 is not guaranteed.
- No loading, phase, quantile, truncation, precision, or query-floor cost is separately included.
- No classical controls or quantum controls are included; changing controls changes every variance.
- Only levels 0..5 are included, with no justified terminal level or bias certificate.
- Classical total runtimes are illustrative coordinates, not measured strong-comparator price delivery times.
- No fixed setup, measurement, decoding, or physical failure budget is charged; any such costs reduce available c0.
- This conditional algebra is neither a lower bound nor evidence of feasible quantum advantage.

The entries specify a budget to compare with a separately compiled and physically scheduled coherent oracle. They do not predict its duration. Level-zero classical diagnostic CPU timings cannot be substituted for c0. Strong classical methods receive the same controls and problem information.

Reproduce with `python docs/research_investigation/2026-09-22/antithetic_resource_sensitivity.py`.

Artifacts: [source](antithetic_resource_sensitivity.py), [full-precision JSON](antithetic_resource_sensitivity.json), [underlying pilot protocol/results](antithetic_logheston_pilot.md).
