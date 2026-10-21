# Actual payoff predicates and log-domain eligibility

The complete B4/B8 census and independent stored-IR audit passed. All 3,106
`lt`/`positive` predicates were classified once, with their native call sites:
349 in B4 and 2,757 in B8.

The financial structure contains 64 monitored arithmetic-basket conditions,
62 comparisons in maximum trees, two final strict survival comparisons and
two arithmetic-Asian strike positive parts. The source implements the monitored
conditions through each maximum tree and its final comparison; it does not emit
64 separate barrier comparison gates. The 464 guarded stock exponentials remain.
Path clipping contributes 928 comparisons; Gaussian/table/radical guards are
listed separately.

A single-asset log threshold does not supply the required basket or Asian
arithmetic. The two native-interface diagnostics preserve the actual averaging
coefficient and integer floors. They do not assert that their tuples are
reachable under the finite Box–Muller law, and do not prove that every possible
QSP construction fails.

No exact replacement theorem was supplied on the whole supported native domain,
so direct transfer is stopped at that prerequisite. A structured approximate
signal would need to pay for the sum of exponentials, normalization, threshold
ties, native errors, preparation, inverse and all oracle calls. No new source,
predicate circuit, gate, financial price or quantum observation was produced.

The first launch failed before analysis because its script import path was
missing. That attempt and its code remain frozen. The second version fixes that
launcher and makes the scope of the interface diagnostics explicit.

Evidence: [census](../../results/limitation_program_20261001/E22_census_run002/summary.json),
[independent audit](../../results/limitation_program_20261001/E22_census_audit_run001/summary.json),
[eligibility diagnostics](../../results/limitation_program_20261001/E22_census_run002/certificate.json).
