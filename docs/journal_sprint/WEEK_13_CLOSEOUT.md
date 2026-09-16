# Week 13 closeout

Week13 is development-complete and independently reviewed. The full final
regression passed735tests (11legacy warnings,355.00s); clean-checkout focused
tests passed51, and all104archive files/24circuits replayed successfully.
Scientific and software subagents both returned PASS with no remaining blockers
in their review scopes. The continuous-price certification gate remains blocked.

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
- [x] Final full regression, final independent-agent evidence review and log.
- [ ] Certified continuous-price admission or quantum-advantage claim: blocked,
  not a required positive outcome for completing this feasibility week.

Results and quantitative limitations: [WEEK_13_RESULTS.md](WEEK_13_RESULTS.md).
Source freeze `e59782a7`; no production retuning or confirmation data.

Verification records: [full regression](../../results/journal_sprint/tests_week13_full_final_v1.xml),
[clean-checkout focused suite](../../results/journal_sprint/tests_week13_clean_checkout_v1.xml),
[clean-checkout replay](../../results/journal_sprint/w13_clean_checkout_replay_v1.json),
and [independent review dispositions](WEEK_13_REVIEW.md). The11warnings concern
the retained Qiskit/Terra API/package deprecations, not failed assertions.
New-source Ruff and whitespace checks passed. Producing files and all original
archive bytes remained unchanged after freeze; user stash/unrelated files preserved.

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

## Reproduction

Use the recorded Python3.9.13/NumPy2.0.2/SciPy1.13.1/Qiskit0.46.3 environment,
with OPENBLAS_NUM_THREADS, OMP_NUM_THREADS and MKL_NUM_THREADS set to1. The
strict replay intentionally rejects an incompatible environment rather than
claiming cross-platform numerical reproducibility. No package upgrade was made.

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
venv/Scripts/python.exe -m pytest -q
venv/Scripts/python.exe -m research.journal_sprint.run_w13 verify results/journal_sprint/w13_encoding_v1
venv/Scripts/python.exe scripts/verify_week13_independent.py results/journal_sprint/w13_encoding_v1
```

The archive is committed directly (104small files); no extra ZIP extraction is
needed for week13. Verification does not overwrite original results. A fresh
`run` requires a new exclusive directory and would be another development run,
not an independent confirmation study. The clean source checkout uses the same
existing environment: do not label it fresh-environment reproduction.
