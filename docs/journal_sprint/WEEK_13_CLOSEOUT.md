# Week 13 closeout

Working closeout: fixed production and replay complete; final regression and
independent evidence review are being finalized. Do not infer certification.

## Scope checklist

- [x] Small path-dependent/Asian-basket raw and geometric-residual encodings.
- [x] Independent scalar-formula, bit-order, joint probability, full-state and
  inverse checks; six cases/24 circuits completed.
- [x] Same-target finite classical summation and shared-control RQMC references.
- [x] Nonnegative beta1 residual range and distinct finite/analytic offsets.
- [x] Componentwise dollar-error contracts with unknown bounds retained.
- [x] Measured loader/payoff/A/inverse CX, depth, qubits and simulator costs.
- [x] Structured preparation implemented; arithmetic extension assessed with
  dimension/precision/error dependence and explicitly unknown compiled costs.
- [x] Bounded Heston theorem-access and genuine signed nested-Asian audit.
- [x] Immutable source/protocol snapshot, stage checkpoints and strict replay.
- [ ] Final full regression, final independent-agent evidence review and log.
- [ ] Certified continuous-price admission or quantum-advantage claim: blocked,
  not a required positive outcome for completing this feasibility week.

Results and quantitative limitations: [WEEK_13_RESULTS.md](WEEK_13_RESULTS.md).
Source freeze `e59782a7`; no production retuning or confirmation data.

## Week 14 handoff

Three planned blocks remain after week13 closeout: weeks14-16. The unchanged
[roadmap](WEEKS_11_16_IMPLEMENTATION_PLAN.md) requires an admission gate for
certified end-to-end work. No week13 continuous-price encoding passed it.

Allowed next research work: finite-target nonzero-Grover diagnostics, faithful
comparator implementation/audits and resource accounting. Clearly mark these as
finite-target development. Resolving continuous-price admission requires better
bias/error enclosures and a non-enumerative normalized arithmetic oracle; it is
not accomplished by feeding an empirical discrepancy into the bias field.
No confirmation or manuscript advantage claim should be advanced without the
separate validity/novelty gates. A route replacement requires a visible replan.

This turn requests implementation plus independent reviews. Changes remain on
local `research/week13-quantum-encoding`; no new PR, push or merge is authorized
by this request. Earlier week12 PR#3 remains merged; it does not include week13.
