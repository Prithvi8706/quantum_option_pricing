# Remaining finite-policy regret and baseline confidence

The new joint arithmetic certificate does **not** finish the financial price
certificate. The estimator still needs a confidence interval for the same
digital baseline and a regret certificate for the same digital decision.
Archived real-policy samples do not establish either by themselves. Tight
residual moment transfer is optional if the bounded-output estimator is used.

## Concrete route for C4, compound strike 6

For regret, draw fresh independent q32 outer words, evaluate the exact digital
policy once per outer state, and draw a fixed number of independent q32 future
word blocks. Compute the real interpretations of digital `c0_d` and each
digital residual `R_d`, and form

```
Z_d = c0_d - mean(inner R_d),
H_d = min(B_d, (Z_d-Kc)+ - d*(Z_d-Kc)),
d = 1(V_d>Kc).
```

The inner sample mean can use exact rational arithmetic; it must not silently
introduce another fixed-point rounding. Conditional Jensen bounds regret before
the outer clipping. Its clipping excess is bounded using the same projection
argument as the joint certificate: compared with exact `Z`,
`h_d(Z)<=B+|V_d-V*|`, where `V*=clip(V_d,L,U)`. The two comparisons charge
`2*e_c0+2*e_residual+e_projection+|B_d-B|`. Together with the finite-control
bias this is covered conservatively by the already recorded joint arithmetic
and financial bridge budgets. Pay outer discount rounding as well.

Thus a fixed-N empirical-Bernstein upper bound for the discounted bounded
`H_d`, plus these deterministic additions, can certify the same implemented
decision. A reasonable first fixed design remains `2^20` outer samples and
16 future samples each, with regret failure probability 0.001. It passes only
if the **new** observed bound, including all additions, is below $0.003. The old
C4 regret result motivates this sample size but does not predict or guarantee
passage. A failure must not be repaired by repeatedly sampling to an unadjusted
confidence threshold. This run was not launched: the exact-digital baseline
screen below already entails multiple days in the current evaluator, while
the quantum cost gate fails by a large margin.

For the baseline, draw independent q32 outer words and estimate the exact
digital `base_6`. A rigorous bounded-mean inequality is a valid conservative
backstop. Faster useful alternatives would require an actually validated
control, tail truncation, certified floating evaluation, or faster exact
implementation; none is assumed free here. RQMC with empirical replicate
intervals is a different guarantee and cannot silently replace the allocated
rigorous confidence requirement.

## Executed 32-draw cost screen

`range_sampling_screen.py` draws 32 fixed-seed development inputs (seed
2026092805), evaluates the pruned/optimized exact digital C4 baseline in Python,
and reads a universal baseline range from the integer range proof. This is a
timing and planning experiment, not a statistical certificate.

| Quantity | Executed or derived value |
|---|---:|
| Exact baseline evaluation time | 0.4937 seconds for 32 samples |
| Mean sample time in this evaluator | 15.43 ms |
| Certified baseline range | $0 to $2,642.016071363 |
| Baseline error / failure allocation | $0.003 / 0.002 |
| Empirical-Bernstein samples required even at zero variance | 15,619,107 |
| Corresponding serial time at measured rate | 240,974 seconds; 2.79 days |
| Diagnostic sample variance | 4.54074 dollars squared |
| Planning sample count if that variance persisted | 31,051,383 |
| Corresponding serial time | 479,065 seconds; 5.54 days |
| Unconditional Hoeffding backstop sample count | 2,678,769,518,611 |

The empirical-Bernstein screen uses the same radius already used in this
project, `sqrt(2*s^2*log(4/delta)/N)+7*B*log(4/delta)/(3*(N-1))`.
The zero-variance count is a necessary condition for **this selected bound and
support**, not an information-theoretic sample lower bound. The diagnostic
variance estimate has only 32 observations and is explicitly not a variance
certificate. Wall-clock projections are serial extrapolations of this Python
evaluator and include no claimed GPU/compiled implementation speed.

The screen exposes the next concrete work requirement: accelerate and certify
the exact baseline evaluation, or develop a valid cheaper baseline certificate,
before scheduling a fixed independent confirmation run. There is no defensible
reason to report the outstanding confidence requirement as complete merely
because the law and arithmetic errors now fit their budgets.

Results: [range_sampling_screen.json](../../results/controlled_priority_completion/range_sampling_screen.json).
No manuscript claim should infer full price certification, advantage, or
held-out confirmation from this development screen.
