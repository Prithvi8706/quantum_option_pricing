# Independent classical comparator review

22 September 2026. Read-only review of the new results against the archived
compound/residual timing receipts, plans, raw replicate rows, pricing sources,
combined references and fixed-iid certificate. No price acquisition, large
campaign, held-out case or new method search was run.

**No blocking comparator or target mismatch found.** The two quoted cold times
are supported by whole-process receipts and their own penny-width empirical
intervals. The strict C4 statistic is valid under its stated ideal iid and exact
evaluation premises, but its timing is acquisition plus charged training, not
the same fresh-process timing scope as the two RQMC receipts.

## Timings, uncertainty and common financial target

| Comparator | Recorded seconds | Maximum interval radius across three strikes | Scope |
|---|---:|---:|---|
| C4 parity RQMC | 11.1059177 | 0.001461906616 | Fresh subprocess, imports, new native cache, retraining, full price/output |
| H8 earlier streaming RQMC | 13.847206 | 0.007014339522 | Fresh subprocess, imports, new native cache, retraining, full price/output |
| C4 fixed-iid | 267.8373668 | 0.008009838951 | Timed acquisition plus archived training charge; ideal-premise statistical guarantee |

The first receipt is in
[controlled cold receipts](../../results/controlled_residual_feasibility/cold_v1/receipts.json);
the H8 receipt is in
[compound cold receipts](../../results/compound_feasibility/cold_timing_v1/receipts.json).
Both return codes are zero. Their wrappers start the timer before launching the
fresh child process and stop it after that process exits. Both pass `--retrain`
and a fresh native-cache directory. C4 uses 8,192 outer states, 16 future
scenarios and 32 randomizations; H8 uses 8,192, 256 and 32 respectively. Their
entire three-strike work is charged to each individual requested quantum price.
No division by three or unpaid policy-training advantage is assigned to the
classical side.

C4's previous cold implementation took 12.4439924 seconds; the new parity
implementation is the faster recorded eligible choice. H8's new parity code took
21.1855197 seconds, so retaining the **earlier 13.847206-second implementation**
is appropriate. The faster H8 method caps the inner payoff at 2048 and adds its
analytic 0.000039808970-dollar uncapping allowance to the upper endpoint. It
therefore addresses the same original uncapped compound target with an explicit
bias allowance; it is not a cheaper price for a substituted contract. C4's parity
method directly targets the uncapped contract.

I reconstructed all six selected cold intervals from their raw replicate
lower/upper values using the recorded 32-replicate Student-t endpoint formula.
The reconstructed endpoints agree with the stored summaries within 1e-12.
The empirical radii at strikes 3/6/9 are:

| Model | Strike 3 | Strike 6 | Strike 9 |
|---|---:|---:|---:|
| C4 | 0.001461906616 | 0.000640751203 | 0.000302362713 |
| H8 | 0.007014339522 | 0.006101260363 | 0.005431273899 |

These are empirical RQMC uncertainties. A Student-t interval over scrambles does
not become a nonasymptotic 99% guarantee merely because its radius is small.
The exact policy/Jensen **expectation** bracket and its empirical sampling
interval are different assertions. The summary correctly keeps that distinction.

Each of the six selected intervals overlaps its independent archived reference
interval. I checked this directly against
[combined reference summaries](../../results/compound_feasibility/reference_combined_v1/summaries.json),
not just the stored Boolean comparison report. Reference roots 2026092404 and
2026092414 differ from the cold roots 2026092506 and 2026092416. The reference
combines its independent H4/H8 acquisitions by an equal-weight endpoint estimate;
stopped matrix-run samples are not counted again. The references themselves use
empirical Welch intervals and are not exact prices or a coverage experiment.
Overlap is a consistency check, not proof of true-price accuracy.

## Strict fixed-iid C4 comparison

The predeclared
[iid plan](../../results/compound_feasibility/bounded_iid_v1/plan.json)
uses 4,194,304 outer samples, 16 disjoint inner samples per outer state, cap 128,
cap allowance 0.000026442540 dollars, and endpoint failure 0.005. Source inspection
confirms independent inner groups rather than the shared inner net used by RQMC.
For either endpoint, the employed range 2*cap*exp(-r*tau) is conservative, and the
radius is

    sqrt(2*s²*log(4/0.005)/N)
      + 7*range*log(4/0.005)/(3*(N-1)).

The two endpoint failure allocations sum to 0.01 **per price**. This does not
claim simultaneous 99% coverage of all three strikes. The price interval includes
the Jensen policy gap and analytic cap tail; it is not only a Monte Carlo
standard error around an uncorrected policy price.

I recomputed both radii for all three strikes from the archived sample variances,
then reconstructed the confidence endpoints and cap allowance. They agree with
[iid summaries](../../results/compound_feasibility/bounded_iid_v1/summaries.json)
within 1e-14. The three midpoint radii are 0.008009838951, 0.006225429317 and
0.004685943325. Every interval contains its corresponding archived reference
interval. The original individual iid samples are not all archived; this review
reconciles the saved sufficient statistics and source, not a new sample replay.

The 267.8373668-second figure is explicitly `elapsed + fit['seconds']` in
[bounded_iid.py](../../research/compound_feasibility/bounded_iid.py).
Its timer covers the acquisition loop, including its first compiled-kernel use;
the policy training cost is charged from the archived fit. Imports, loading and
writing the plan, and final summary serialization are outside this acquisition
timer. Calling it a full cold-process time would overstate the receipt. The
review requested the new summary call it **recorded acquisition-plus-training**.
The resulting recorded tenfold budget is 26.78373668 seconds; it is a stricter
statistical comparison coordinate with this stated timing limitation.

The sampling theorem idealizes independent draws and exact evaluation. Neither
the iid run nor the empirical RQMC run has a full floating-point/PRNG financial
certificate. This limitation must remain visible when contrasting either with
quantum theorem-level accuracy. The quantum full-price certificate is also
explicitly unclosed; the cost screen grants its missing financial work for free
instead of claiming matched completed financial guarantees.

## Fairness and limits of the resulting comparison

The retained comparator is the strongest **measured eligible implementation
among these archived acquisitions**, not a proof of globally optimal classical
pricing. GPU code, quadrature and other structured methods remain eligible. No
classical method is excluded because it benefits from the same controls, and no
slower new H8 implementation is substituted to make quantum cost look better.

Each cold time is one development timing sample, not a latency distribution,
confidence interval, or a held-out speedup estimate. Selection between earlier
and newer development methods is disclosed. Policy correctness is not assumed:
the policy/Jensen bracket pays for exercise quality. Training uses separate
frozen seeds and is charged even when the moment policy is selected.

The quantum comparison is deliberately favorable to the constructed quantum
implementation: the whole three-price classical time is charged to one quantum
output, while the optimistic quantum screen grants setup, tight moments and
surrogate/regret work at zero cost. Failure of that particular circuit schedule
is supported. It does not establish a quantum lower bound, optimal classical
latency, or a positive end-to-end advantage under matched certified machine
arithmetic.
