# Held exact Bernstein conversion QA, version 5

This is a prospective, single-run arithmetic equivalence check. It does not
approve any approximation row, full financial source, resource estimate,
candidate, emission, G2 claim or quantum advantage. Financial and circuit
fixture credit, gate replays and price samples are all zero. No coefficient
fitting, source walker, interval witness or saved financial corpus is run.

The fixed-row profiling diagnostic completed at
`A13_recovery_profile_d10_s4_run001`, manifest
`e099b1547056d12eb81e920bcaaf71bb1a33bc2bc5223643cd60cb8881190983`.
It identified exact Bernstein conversion as a material verifier cost. This QA
does not promise a timing improvement or that a later all20 audit will fit its
unchanged budget. The original failed audit004 remains failed, including its
14 partial proof rows, manifest
`334aa0386e0321b7fb9690a52378a8c94234b5c0488fa50464d89d076ca20471`.
Neither the profile nor this QA promotes those rows.

The reference is the sole `exact_bernstein` function from immutable
`audit_exp_frontier_recovery_v4.py`, SHA
`61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba`.
The new sole function is `integer_bernstein` from
`bernstein_integer_kernel_v5.py`, SHA
`695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048`.
The kernel's mandatory final argument is a no-argument checkpoint. QA supplies
`lambda: check(started)`; the reference receives the same `started` creation
clock. Root may later place the kernel behind the original five-argument
auditor ABI in a new version; this QA imports no auditor or kernel module.

For the paper equivalence, let n be the requested Bernstein degree, m the
maximum coefficient degree (zero for an empty vector), L a positive common
coefficient denominator and D a positive common denominator for left a and
width h. With A=Da, H=Dh and c'_k=Lc_k, the transformed monomial integer is
q_j=sum over k>=j of c'_k binom(k,j) A^(k-j) D^(m-k) H^j, divided by L D^m.
Thus it is exactly the reference monomial after substitution x=a+ht. A
positive common multiple of binom(n,j), j<=min(n,m), converts the reference
Bernstein sum to one integer numerator and denominator per coordinate. Terms
j>m are zero. Empty vectors, degree elevation and h=0 retain the same result.
The original valid empty degree=-1 case returns an empty list. Positive common
denominators change the arithmetic representation, not the rational value.

The entire fixed corpus is defined before execution in the validator source
and named in the JSON method. Twenty oracle cases use degrees 0..5, including
signed dyadic and non-dyadic coefficients/domains, cancellation, exact zero,
empty coefficient lists, missing higher coefficients, degree elevation,
degenerate left=right domains, and low-degree values with 384/544-bit dyadic
denominators. Every coefficient and endpoint is a Fraction; the largest
literal numerator/denominator bit length is bounded by 546.

The independent oracle evaluates p(a+(b-a)t) by Horner evaluation at n+1 exact
rational t values (i/n, or zero for n=0). It constructs the Bernstein basis
matrix binom(n,j)t^j(1-t)^(n-j) directly and solves by exact Gaussian
elimination. It does not use either power-to-Bernstein conversion formula.
The matrix remains nonsingular when a=b because its basis is in t, while its
right-hand side then becomes constant. There are exactly 20 systems, 75
evaluation points, 345 basis matrix entries and 1,395 elimination cell updates;
dimension is at most six and the update cap is 4,096. Both old and new output
vectors must equal the independent oracle exactly, including list length and
Fraction representation.

One additional empty degree=-1 compatibility check and three exact ValueError
comparisons cover reversed domains, excess coefficient count and empty degree
below -1. Two additional reference-equivalence checks use all coefficients
c_k=1/k! through degree79 and111 on the exact domain [-1/128,1/128]. These
complete vectors have 80 and112 coordinates. They are fixed Taylor examples,
not fitted or source-corpus data, and the small Gaussian oracle is not applied
to them. Exactly 267 successful output coordinates are compared across the
small and Taylor checks. The 26 declared checks are QA, with zero fixture
credit.

The new validator is
`verify_a13_bernstein_equivalence_v5.py`. It extracts only the named function
definitions by AST, rejects decorators, defaults, annotations, imports and
classes, and compiles them in an explicit Fraction/comb/lcm and small-builtin
environment. Neither module body executes. The validator itself uses only
standard-library modules. Root freezes its exact bytes, this Markdown, the
JSON method, both source functions and the actual pinned interpreter before
execution. Method fields for the validator and interpreter remain null to
avoid a circular self-pin; the required exact CLI SHA arguments are their
external root-issued pins. All six files are freshly hashed before extraction
and again at terminal sealing; all expected values must match independently
read actual bytes and unchanged full stat/reparse identity. This is a scoped
QA input map, not a claim that the historical full runtime maps were re-audited.

Run only from the workspace with the pinned interpreter, `-B` before `-m`:

```
.context/frontier_t0_env/Scripts/python.exe -B -m research.limitation_program_20261001.verify_a13_bernstein_equivalence_v5 --kernel-source-sha256 <695c10...70048> --validation-source-sha256 <root-pin> --method-md-sha256 <root-pin> --method-json-sha256 <root-pin> --interpreter-sha256 <root-pin> --output <absolute fresh receipt>
```

The sole fresh receipt is
`results/limitation_program_20261001/A13_Bernstein_equivalence_check_run001`.
Limits are 180 process CPU seconds, 150 CPU seconds for work admission and
600 seconds from actual process creation; one process/thread and no workers.
All imports, source reads/hashes, AST compilation, arithmetic, serialization,
output verification and terminal fresh hashes are charged. Each source and
record is at most 1MiB. Input reads and output writes are chunk guarded;
output verification uses a bounded whole read with checks before and after.
Arithmetic loops are
checkpointed; no individual arbitrary-precision operation can be preempted,
so an observed overshoot fails rather than certifying a hard bound. A fresh
work unit is not admitted after 150 CPU seconds. No caps are increased or
retry performed.

Success retains exact vectors and their canonical compact-JSON SHA in
`finite_equivalence_results.json`, a scoped summary and a manifest with exact
owned membership and six canonical ROOT-relative frozen inputs. The manifest
excludes its own SHA. Any exception after receipt creation adds a constant
authoritative `FAILED_UNSEALED.json`; such a marker invalidates every partial
success-looking file, including a partially or fully written manifest.
Budget status in that generic emergency marker is null with hard state
uncertified, rather than an invented censor diagnosis. A pre-mkdir failure has
no QA receipt and requires separate root failure retention. Existing files and
old receipts are never edited or overwritten.

Status: author-only, unexecuted. Root must review and freeze the final pins
before the single actual validation. Only an actual terminal PASS can support
the arithmetic-kernel equivalence premise of a later new auditor; all20 proof
approval and candidate release remain separate.
