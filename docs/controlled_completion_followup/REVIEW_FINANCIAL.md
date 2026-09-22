# Independent review of the finite financial bridge

22 September 2026. Reviewed by the separate fault-tolerance workstream, without
editing the financial implementation. Scope:
`financial_bridge.py`, `financial_arithmetic_audit.py`, their result artifacts,
`FINANCIAL_BRIDGE.md`, and the source/IR definitions to which the bounds apply.

**No blocking mathematical or implementation finding.** The new result supports
the stated partial closure of the exact-real finite probability law and its
analytic-control bias. It does not close the implemented arithmetic, finite
policy regret, surrogate mean, tight-moment transfer or full-price certificate.

The independent analytic checks were:

- The first Box–Muller radial cell has error `2I(h/2)-I(h)`. Applying the Mills
  upper bound to the positive term and monotonic lower bound `I(h)>=h*r(h)`
  gives the stated singular-cell estimate; the other cells telescope with
  the factor h/2. The angular term uses independence and the Lipschitz
  sine/cosine bound, including the finite radial mean correction.
- Guards affect spot evaluation at every fixing, while the latent state resets
  only at tau. The source code matches this premise. Clipping of log spots is
  nonexpansive; the stock map after clipping is 4096-Lipschitz. The even
  Box–Muller split is true for all four models, permitting independent
  conditional future couplings and contraction of the outer positive-part map.
- The stock/log tail inequalities follow from the one-sided normal stop-loss
  bound and exponential tilting. Their implementations avoid cancellation
  between nearly equal tail probabilities. The tau-reset term pays for the
  changed future initial stock and its independent mean growth.
- For the control identity, couple the unguarded virtual Gaussian future from
  the finite tau state to the original GBM. Distance to the clipping interval
  is 1-Lipschitz, so its expected tail is bounded by the original tail plus
  the initial-state discrepancy. Couple the clipped virtual future to the
  finite future next. This yields the stated stock term; repeating the
  argument in log coordinates gives `(3n+1)e_step/2`. The geometric-put
  Lipschitz constant is `max(k,0)<=2K` in its log-average, so it remains valid
  near small stock levels and for negative k.
- Baseline/residual cancellation holds for any common implemented decision
  derived from the same policy value. The residual arithmetic error must
  include final Y clipping and baseline rounding, as explicitly stated. The
  finite regret inequality follows from convexity and 1-Lipschitz continuity
  of `(x-Kc)+-d(x-Kc)` for either binary decision; it is not a transferred
  continuous-law regret certificate.
- The control counterexample is reachable: the input word count/probability,
  tau guard, negative k and nonzero Gaussian-growth bias are consistent with
  the financial graph. The f24 arithmetic witness reconstructs its dyadic
  output exactly and encloses the real reference using the negative-k
  simplification; the reported uniform error failure does not imply the
  corresponding expectation failure.

The interval calculations and outward serialization match their documented
scope. The corner checks reconstruct signed pre-reduction arithmetic for
their stated sampled operations; they are correctly labeled diagnostics.
No sampled maximum is promoted to a global error bound. The remaining numerical
margin near $0.001971 is an available budget, not an arithmetic certificate.

The existing 16 financial checks were replayed independently. They cover the
radial integrals, all model/date tail comparisons, independence premises,
law/control budgets, reachable control witnesses and the f24 arithmetic failure.
The review confirms the contribution as a useful partial certificate and
retains the overall no-advantage/no-complete-price conclusion.
