# A13 recovery audit: prospective exact DP optimization V4

This is an author-only operational prospectus. It does not authorize a launch,
approve retained candidate material, or establish that a new auditor will fit
its unchanged budget. No fitting transcript, interval proof, source graph,
resource formula, candidate choice, precision or acceptance rule changes.
Only a NEW auditor and NEW implementation release may implement the procedure
below. Every previously executed file and receipt remains immutable.

The original metadata source is `A13_recovery_run001`, manifest
`e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9`.
It certifies preservation of untrusted material; it is not a mathematical
screen PASS. Its original producer/auditor source pair remains distinct from
the future auditor's own source pins.

Actual audit003, based on `audit_exp_frontier_recovery_v3.py` SHA
`f094a5bd4738735bfae4775b6149fc354a9a15bad7e28850811aa1f0f27d7a3c`,
is FAILED and budget-censored. Its manifest is
`753ffde46904f2b4995efbdcb42b89161386e9267108179f9b0cc9dfe9a14551`,
with 35 owned, 984 frozen and 2842 external references. The admission guard
observed 270.0625 process CPU /283.675 wall seconds; terminal retention reports
286.390625 process CPU /301.5351886000135 wall seconds. Fourteen gzip rows
through `d10_s2` were retained. There is no successful summary, all20 index or
screen approval. Those files are failed-attempt provenance only, with zero
credit. No previously produced proof row may replace a fresh V4 proof.

The prospective route is NEW `audit_exp_frontier_recovery_v4.py`, fresh
`A13_recovery_audit_run004`, and NEW implementation V4 MD/JSON. The executable
and implementation pins remain null until authoring and static review. The
recovery ROOT helper remains unexecuted and cannot accept the failed audit003.
An actual complete uncensored audit004 PASS, followed by fresh ROOT integrity
verification, would be required before any candidate-release assessment.

## Scope fixed before implementation

Retain the exact20 grid: degrees4/6/8/10/12 crossed with segments1/2/4/8;
the separate original Estrin baseline; every successful or rejected row; all
32 recorded exchange rounds per completed segment; at most67 candidate
locations; and selection length `degree+2`, at most14. Preserve the actual
dyadic fitting residuals, original indices and signs, all structural transcript
checks, exact selected-node/threshold comparisons, round32 coefficients, and
nearest/ties-even signedf40 coefficient quantization. No solve or root search
is reexecuted. Fitting diagnostics remain separate from uniform proof.

Keep the primary90/order80 witness authorization by an independent130/order80
reconstruction and retain the independent112-term witness separately. The
112-term witness does not substitute for the primary80 interval authorization.
All actual72/product144/shift proofs, typed literals, selector coverage,
primitive ABI/legacy ADD-SUB-LT format checks, explicit MUL72/f40/product112
metadata, resource copy/bank/cleanup terms and exact dictionary keys stay fixed.

Keep 300 process CPU /270 work-admission /900 wall seconds, one thread,
64 owned files /128MiB, existing runtime/reference/byte-work limits, canonical
gzip settings, complete SHA maps, stat/reparse guarded bookkeeping caches,
uncached full terminal union verification and failure-retention rules. No
budget is raised. The new outcome may still refuse or censor. Candidate G2
allocations remain null; emission, adoption, cost transfer and advantage claims
remain false. Fixture, replay and price-sample credits remain zero.

## Exact integer representation

For a single already-validated round, write each residual as `n_i / 2^e_i`.
`finite_binary` must still independently validate every encoded value and its
power-of-two denominator. Set `e=max(e_i)` and `D=2^e`, and compute
`w_i=n_i << (e-e_i)`. Therefore every residual is exactly `w_i/D`.
No rounding, native-word truncation, modular arithmetic, decimal conversion,
float comparison or interval midpoint is used in this representation.

Discard zero residuals from the alternating selection only, exactly as before;
retain their original indices in the complete transcript. For nonzero values
use `h_i=abs(w_i)` and sign `s_i`. Multiplication by the common positive `D`
preserves signs, every height order and tie, every selected-set minimum, every
selected-set absolute-height sum and its ties. Lexicographic order of original
index tuples is unchanged. Thus integer selection and Fraction selection have
identical winning indices; the exact returned threshold and total are
`Fraction(B,D)` and `Fraction(T,D)` in the original canonical encoding.

The scale is local to this one exact residual vector. Do not share a scale or
result across unrelated rounds, segments or rows. This prospectus does not
introduce memoization of transcript approval or reuse any expected hash as an
observed value. Parse and check all 32 round records even when their values
happen to repeat.

## Pass one: independently determine the bottleneck

Sort the distinct positive integer heights. For a proposed threshold `b`,
filter to heights at least `b` in original index order. Greedily count sign
runs: take the first eligible point, then a point only when its sign differs
from the last taken sign. The count is the maximum alternating-subsequence
length, since an ordered alternating subsequence takes at most one point from
each sign run, and one point from every run realizes that count.

Feasibility for length `L` is therefore exact and monotone in `b`. Retain the
auditor's existing independent binary search over distinct heights. Let `B`
be the greatest feasible threshold, and require an alternating subsequence
exists. Do not read `B` from the declared primary threshold or compute a
nearby threshold with floating arithmetic.

## Pass two: prefix states for sum and lexicographic order

For each prefix, length `l` and ending sign `s`, retain at most one state:
the greatest exact integer sum, with the lexicographically smallest original
index tuple among states having that sum. Only points with height at least
`B` participate. The previous prefix state may be retained (skip the current
point), or the current point may extend the previous-prefix state of length
`l-1` ending in `-s`. The length-one proposal is the current point alone.

Implement these finite states as two arrays indexed by length rather than
copying a dictionary for each point. Visit lengths in descending order;
insert the length-one proposal last. This explicitly prevents the current
point from being reused within its own update. Store exact integer sums and
index tuples; prefer greater sum, then smaller tuple, using the original tie
rule. There are at most `2*L` live states. Tuple storage remains bounded by
the unchanged maximum selection length14.

Induction proves the state invariant. Every alternating subsequence in the
new prefix either omits the current point or appends it to the opposite-sign
previous prefix. Greater prefix sum dominates under any common future suffix;
for equal sums, appending a common suffix preserves the lexicographic order
of the equal-length prefixes. Taking the greater sum/smaller tuple among both
length-L ending signs therefore returns the exact second-pass optimum.
Require the selected minimum equals `B`, and retain all original comparisons
with declared indices, threshold, node positions and round chaining.

Do not collapse the two passes into one locally ranked bottleneck/sum/lex
state. Such pruning can be wrong: a future smaller height can make two prior
bottlenecks equal while the discarded lower-bottleneck prefix has the larger
sum. The fixed optimal bottleneck is necessary before additive dominance is
used. Likewise, do not keep a convenient declared path without independently
proving its threshold-constrained sum/lex optimality.

## Guards, evidence and prospective validation

Charge conversion, shifts, sorting, threshold scans, every prefix update,
returned Fraction construction and all existing JSON/check/write/hash work
to the same process clock. Check before and after each bounded pass and
within the point/state loops. Do not defer failure retention past the hard
budget or interpret an incomplete loop as a rejected architecture. Preserve
authoritative FAILED_UNSEALED/failure markers and the fresh receipt's partial
outputs without retry or overwrite.

The finite grid contains at most75 completed segment transcripts and at
most2400 recorded exchange rounds. These are input-structure bounds, not a
measured timing prediction. The expected saving is elimination of repeated
Fraction additions/comparisons/gcd normalization and per-point dictionary
snapshots inside the DP. No profile currently establishes that DP dominates
the complete auditor, and the independent Bernstein, native-range, resource,
gzip and complete-SHA work remains fully paid.

After the active machine reservation ends, require static source review and
AST comparisons showing that other mathematical/resource kernels remain
unchanged. NEW `verify_a13_recovery_dp_equivalence_v4.py` prospectively fixes
an independent exhaustive-subsequence oracle for its exact16 named
mixed-scale/zero/tie/bottleneck/infeasible examples (at most8 entries each).
It compares that oracle to both the pinned V3 Fraction selector and the new
integer selector. The helper extracts only each selected function's AST and
imports neither scientific auditor module. It evaluates no actual candidate
transcript or financial/interval/resource proof.

The separate finite-validation limit is 10 process CPU /8 work-admission /
30 creation-wall seconds, exactly16 fixed vectors and at most4096 exhaustive
subset enumerations. The fixed fresh receipt is
`A13_recovery_DP_equivalence_check_run001`. Root must pin both NEW sources,
this exact corpus and CLI before the single invocation:
`python.exe -B -m research.limitation_program_20261001.verify_a13_recovery_dp_equivalence_v4
--new-source-sha256 <V4 SHA> --validation-source-sha256 <validation SHA>
--output <absolute fresh receipt>`. Failure blocks V4 release; there is no
retry or expansion of this validation corpus. No tests, compiler, hash scan or
numerical work occur during an active reservation. Successful finite validation
is not the all20 audit and receives zero financial/circuit fixture credit.

Before launch, bind the full audit003 failed packet and root review003
`0108b046dcf9ebf55a85926d68f8e7d02036e039f9966d654e1773df61de96a6`
(1 owned /28 frozen), its exact old trio, both earlier failed recovery audits
and reviews, original raw42 capture and failed A13 packets, the successful
metadata source, all original method/source memberships and the full current
runtime. Canonical confinement, equal-SHA insertion and exact owned membership
are mandatory. A new owner pin or route never waives an older expected SHA.
Actual scientific screen approval can come only from all20 fresh V4 row
authorizations, a complete successful index/summary/completion/manifest, and
subsequent ROOT byte-integrity verification.
