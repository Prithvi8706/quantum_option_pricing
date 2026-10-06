# Preparation-error composition

Two preparation-error bounds passed 12 meaningful fixtures, including a
correlated-state counterexample and an independent density-matrix check.
For tensor products, trace distance is at most the sum of scalar distances.
For independent pure products, the exact squared distance is
`1-product(1-D_i^2)`, bounded by `sum(D_i^2)`. Purity and product structure are
required for that sharper bound; equal marginal states alone do not suffice.

A payoff operator with values between $0 and $40 changes its expectation by
at most `40*D` dollars. The explored $0.001 loading-bias allowance therefore
permits total preparation trace distance at most `1/40000`. This allowance was
not inserted into the current Box–Muller price ledger.

| Independent drivers | Conservative scalar distance | Pure-product scalar distance, approximately |
|---:|---:|---:|
| B4: 60 | 1/2,400,000 | 3.2275×10⁻⁶ |
| B8: 468 | 1/18,720,000 | 1.1556×10⁻⁶ |

The saved pure-product allowances are conservative 128-bit dyadic lower
enclosures of `1/(40000*sqrt(draws))`; all comparisons use exact arithmetic.
Six archived q10 MPS errors were screened against these thresholds. Their
floating-point compression estimates are not rigorous preparation certificates,
emitted circuits, synthesized rotation costs or continuous-price bridges.
The truncated binned q10 Gaussian law remains different from the current q32
Box–Muller law.

State-preparation law bias and repeated coherent gate errors are separate.
A bound for one prepared basis state does not supply a full unitary operator
bound. The next bounded component certifies the first two Gaussian prefix
probability and angle levels while retaining the full-tree count.

Evidence: [result](../../results/limitation_program_20261001/A05_loading_run001/summary.json),
[exact certificate](../../results/limitation_program_20261001/A05_loading_run001/certificate.json).

The [independent audit](../../results/limitation_program_20261001/A05_loading_audit_run001/summary.json) passed. Only the archived q10 bond-eight numerical error passes both scalar thresholds for both cases; it still supplies no rigorous preparation or synthesized-circuit certificate.

The first two prefix levels are now certified: three conditional nodes, two
exact Clifford rotations and one synthesized rotation. The actual uncontrolled
two-qubit prefix uses 116 T gates and 194 Clifford gates. Its scalar `omega^5`
phase is tracked; coherent controlled use requires that phase to be compensated.
The full q10 tree still has 1,020 uncertified conditional nodes, and 47 archived
floating-point omissions have not been proved exactly zero. The independent
root audit passed: a separate 190-digit interval calculation checked every
saved operation, all boundary masses and angle brackets, and the whole-angle
four-dimensional matrix. Omitting the tracked scalar would fail the operator
check, confirming the need to compensate it before controlled use.
[Prefix receipt](../../results/limitation_program_20261001/A03_prefix_run001/summary.json).
[Actual-operation audit](../../results/limitation_program_20261001/A03_prefix_audit_run001/summary.json).

The separate uniform-x grid certificate fails its $0.001 law allowance at q10.
For this fixed certificate formula, the first widths that fit are 24 bits for
B4 and 27 for B8, requiring 16,777,215 and 134,217,727 full-tree conditional
nodes per scalar driver. Those counts motivate testing compressed loading,
but they do not prove that every compressed loader is expensive or that q10
has a large actual price bias. The $0.001 law allowance and $0.001 preparation
allowance are separate proposed allocations; neither changes the current
Box-Muller ledger.
[Grid screen](../../results/limitation_program_20261001/A03_law_screen_run001/summary.json),
[independent exact audit](../../results/limitation_program_20261001/A03_law_screen_audit_run001/summary.json).
