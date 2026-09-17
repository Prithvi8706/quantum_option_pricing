# Bounded matched arithmetic comparison: results and decision

Date: 2026-09-17. The fixed D1/D2 development study is complete, replayed and
independently AI-reviewed; verification and review closeout is recorded in the
[review log](MATCHED_ARITHMETIC_REVIEW_20260917.md).
See the [protocol](MATCHED_ARITHMETIC_PROTOCOL_20260917.md) and
[method/limitations](MATCHED_ARITHMETIC_METHOD_20260917.md).

## Supported finding

For these two contracts and the declared implementations, the reflection route
has lower ideal logical CX projections than the explicit fixed-point arithmetic
routes at the same $1 accuracy target and at least95% confidence. The ordering
holds with both the historical conservative control ledger and the standard
control-cancelled ledger. This is **not quantum-over-classical advantage**, a
hardware speedup, a new primitive, or superiority over optimized arithmetic in
general. A ratio of upper projections does not bound a ratio of actual costs.

| Case / selected route | Deterministic dollar allowance | AE M | Conservative projected CX | Control-cancelled projected CX | Allocated total qubits |
| --- | ---: | ---: | ---: | ---: | ---: |
| D1 reflection, degree64 | 0.45473744 | 128 | 354,203,646,982 | 36,469,403,102 | 55 |
| D1 ripple arithmetic | 0.10189903 | 1,024 | 4,795,253,895,265 | 560,069,542,723 | 3,682 |
| D1 Fourier arithmetic | 0.10189903 | 1,024 | 4,797,944,670,395 | 560,364,116,309 | 3,680 |
| D2 reflection, degree128 | 0.60039730 | 512 | 10,555,616,671,767 | 1,101,392,680,835 | 103 |
| D2 ripple arithmetic | 0.18790249 | 2,048 | 19,250,344,005,889 | 2,248,246,010,763 | 6,943 |
| D2 Fourier arithmetic | 0.18790249 | 2,048 | 19,258,400,674,483 | 2,249,117,660,229 | 6,941 |

All schedules use17 repetitions. A/A-inverse calls equal17*(2*M-1), and all
selected plans remain below the frozen10,000,000-call cap. Of12 configurations
(four reflection degrees plus two arithmetic routes for each case), eight
have feasible logical schedules. All failed-degree budgets remain in the archive.

Ripple/reflection projection ratios are **13.5381 for D1 and1.8237 for D2** in
the primary ledger; **15.3572 and2.0413** after control cancellation. Arithmetic
has a smaller deterministic approximation allowance but a larger probability-
to-price scale and therefore needs more AE queries. Reflection also uses a
degree-four classically computed offset/residual encoding; this is a comparison
of full declared quantum routes, not a causal experiment changing only centering.

The arithmetic width deliberately retains Bennett/Horner intermediate scratch.
It is not space optimal, range reduced or an implementation of the best known
exponential. The comparator therefore supports a narrower claim than "beats
arithmetic pricing." Compiler/decomposition differences and classical setup
costs are explicitly described in the method; this is not a uniformly optimized
whole-circuit or classical-plus-quantum runtime comparison.

## Fourier aggregation is not the improvement here

Both arithmetic routes encode the **same integer payoff**. Forward aggregation
CX counts, before its required inverse, are:

| Case | Efficient zero-start ripple | Zero-start Fourier |
| --- | ---: | ---: |
| D1, two40-bit price words | 666 | 4,900 |
| D2, four40-bit price words | 1,918 | 8,180 |

Fourier saves one A-workspace qubit, corresponding to two total qubits under
the common fully allocated zero-reflection convention, but costs more CX.
There is no contradiction with an aggregation preprint's comparison against
a different weighted-adder baseline. Here equal-weight ripple is linear in
word width; the exact Fourier construction has quadratic phase growth.

More importantly, aggregation **plus its inverse accounts for under0.061% of
the arithmetic A-circuit CX projection in all four rows**. This is a concrete
bottleneck finding for this implementation: improving only this adder cannot
materially reduce its A-circuit CX count at fixed workspace and other components.
It is not a universal lower bound on arithmetic pricing cost. Conversion,
normalization and query count deserve attention before another adder search.

## Finite targets, verification and reproducibility

The four small grids exhaust292 input words in total, not292 independent
statistical trials. Maximum pointwise arithmetic-price discrepancies from
the real-exponential finite target were:

| Case / bits per coordinate | Observed maximum | Directed arithmetic allowance |
| --- | ---: | ---: |
| D1 /1 | 0.000246313 | 0.000525338 |
| D1 /2 | 0.000417109 | 0.000796123 |
| D2 /1 | 0.000358058 | 0.002752618 |
| D2 /2 | 0.000864481 | 0.003838721 |

These are binary64 diagnostics within the declared allowance, not measured
quantum prices or continuous-price certificates by themselves. Reflection's
scalar approximations to the same finite reference are also archived; they
are not asserted to equal the arithmetic integer payoff.
Displayed decimals are rounded summaries; the archive retains exact reported
binary64 diagnostics and full directed allowance strings.

The larger arithmetic conversion/payoff components were actually emitted and
counted, with deterministic endpoint basis checks and clean-workspace checks.
Small aggregation tests compare complex amplitudes, controls and inverse maps,
including nonzero initial flags and modular overflow. The full large pricing
circuits were neither statevector simulated nor run on hardware.

Primary and isolated-environment replay results are byte-identical. Sources
and protocol were frozen at68e78e3f. Evidence:

- [Primary results](../../results/journal_sprint/matched_arithmetic_v1/results.json)
- [Finite diagnostics](../../results/journal_sprint/matched_arithmetic_v1/finite.json)
- [Isolated replay](../../results/journal_sprint/matched_arithmetic_replay_v1/results.json)
- [Independent AI review and verification closeout](MATCHED_ARITHMETIC_REVIEW_20260917.md)
- [Full1,271-test receipt](../../results/journal_sprint/matched_arithmetic_full_tests_v1.xml)
- [Clean-checkout reconstruction receipt](../../results/journal_sprint/matched_arithmetic_clean_verification_v1.json)

Reproduce into new, nonexistent output directories:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
venv/Scripts/python.exe -m research.journal_sprint.run_matched_arithmetic NEW_PRIMARY_DIR
.context/week15_env_v1/Scripts/python.exe -m research.journal_sprint.run_matched_arithmetic NEW_REPLAY_DIR
venv/Scripts/python.exe -m research.journal_sprint.verify_matched_arithmetic NEW_PRIMARY_DIR NEW_REPLAY_DIR NEW_RECEIPT.json
```

The verifier requires the acquisition sources to be committed before running,
with all recorded bytes preserved. Independent environments are dependency-
pinned; matching one such replay is not proof of cross-platform portability.

## Explicit scientific decision

Close this bounded comparator task. Retain reflection as the lowest projected
logical-cost candidate **within this menu**, but keep production choice unset
and the scientific candidate on standby. Do not automatically promote it.

The supportable contribution now includes a reproducible full-component
tradeoff against explicit arithmetic comparators and a measured aggregation
bottleneck, alongside the restricted correctness/decision results from the
[claim assessment](CLAIM_ASSESSMENT_RESULTS_20260917.md). It still needs independent
human assessment to establish significance against the nearest prior work.

If further development is authorized, the informative next comparator is
space-reused/range-reduced arithmetic with a matched residual/control strategy,
not another aggregation-only optimization. Hardware/synthesis error, matched
strong classical cost comparison, external human novelty review and a fresh
confirmation campaign remain open. No superiority to RQMC is established.
