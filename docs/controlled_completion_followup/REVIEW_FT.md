# Independent synthesis and fault-tolerance review

22 September 2026. Reviewed by the financial-bridge agent, independently of the
author of the synthesis/factory model. Scope: `synthesis_rotations.py`,
`ft_model.py`, the FT tests, the 95-target synthesis artifact, all 32 conditional
physical scenarios, and the earlier phase/cost/envelope conventions they use.

**No blocking mathematical or gate-convention defect found in the reviewed
conditional model.** This is not approval of a physical architecture or a
complete financial-pricing certificate. The explicit conditional assumptions
and unclosed full-price costs must accompany any reported resource figures.

## Rotation and phase accounting

The library reconstructs each target from integer rational radians or a rational
multiple of pi. Its independent verifier multiplies the actual gate strings in
120-digit interval arithmetic and bounds the Frobenius error, which also bounds
the operator error. Gate execution order is the reverse of the stored matrix
product. Negative angles use the full product's adjoint, preserving the error
and T/Clifford counts.

The shared tolerance is 1/(4000*N_R,max), so the conservative perturbation bound
2*N_R*epsilon is at most 0.0005 for each archived schedule. All three constituent
rotations of each controlled phase are included. The inverse-QFT pi/2 controlled
phases use exact T gates; the remaining QFT angles are included in the library
usage. The pre-existing phase-function approximation allocation remains separate.

The P/Rz and global-W conventions are sound here. A controlled phase decomposes
into three **unconditional** single-qubit phase gates on its two wires plus two
CNOTs. Replacing P by an Rz representative, or removing W from a synthesized
single-qubit product, multiplies the whole two-qubit operation by a scalar. It
does not apply a phase only to the control-one branch. This differs from
discarding the controlled-reflection sign, which the inherited envelope correctly
retains as a Z on the QPE control. The signed two-qubit tests exercise both signs
for every target.

## Factory/retry and error exposure

Under the stated independent stochastic-Z input model and ideal distillation
operations, an undetected error requires at least three erroneous inputs. A
union bound over triples gives 455*e³, and no-error acceptance is at least
(1-e)^15. Hence the conditional output error upper expression

    e_next = 455*e³/(1-e)^15

covers all higher error weights. It does not use a leading-order 35*e³ term as an
exact bound. The evaluated recursion decreases from the raw input error in all
scenarios, making q=1-(1-p)^15 a conservative rejection bound at every level.

With R attempts per distillation group and L levels, the number of groups is

    N_T * sum_{j=0}^{L-1} (15R)^j,

and the maximum raw injection groups number N_T*(15R)^L. Multiplying these by
q^R and 2^-R_raw respectively correctly bounds exhaustion. The absence of an
extra R multiplying the first count is intentional: q^R is already the
probability of exhausting that whole retry group. The sequential critical-path
recursion pays for those retry caps while allowing the stated 15 siblings to
execute concurrently.

All provisioned patches are charged for the **entire** serial schedule, including
factory waits, routing, measurements, resets and feedback. The logical-fault
union bound therefore does not omit the dominant idle exposure. Logical faults,
output magic-state errors, exhausted retries and classical-controller faults
have separate allocations totaling 0.002.

I independently recomputed all 32 allocation cases with 100-digit Decimal
arithmetic, starting from the integer gate counts, supplied code distance, decimal
physical error assumption, retry counts and full patch-round exposure. Every
component and the total passed its allocation; integer invocation counts agreed
exactly. The independent receipt is
[financial_ft_cross_review.json](../../results/controlled_completion_followup/financial_ft_cross_review.json).
Reproduce it with `python -m research.controlled_completion_followup.financial_ft_cross_review`.
This numerical recomputation is an independent check, not a directed interval
certificate. Ordinary binary64 values in the FT artifact should be understood as
evaluations of the displayed conditional formulas, rather than exact outward
endpoints. The rotation certificates do use directed interval bounds.

## Scope limits that remain material

- The empirical logical-error fit is assumed to upper-bound each provisioned
  patch-round and primitive. The model has not established that assumption for
  a noise model, decoder and emitted physical layout.
- Gate durations, adequate decoding, raw-injection success/error, independent
  accepted inputs, distance-preserving interfaces, routing space and hop limits
  are assumptions. The nearest-neighbor hop-one scenario is not a placed circuit.
- The long serial execution figure is a conditional schedule upper bound. Its
  failure to compete is a statement about that deliberately conservative
  schedule, not a lower bound against other factories or architectures. The
  arithmetic-only failure screen remains separate evidence.
- The patch-to-physical-qubit formula is conditional on the assumed geometry.
  No physical qubit allocation, factory/routing layout or real-time decoder was
  constructed or tested.
- The controller CPU timings are five specific offline replays. They establish
  neither worst-case feedback latency nor full device I/O/output cost.
- The online surrogate, finite-policy regret, financial arithmetic and any tight
  moment transfer are still required. Null full-price accounting entries cannot
  be interpreted as zero. Rotation synthesis does not complete P4 or P5.

The first independent FT test execution passed the interval-library, signed-CP
and full-exposure checks but found a test-only Python type error: the malformed
rotation check compared an exact Fraction with an mpmath mpf. The author changed
that comparison to exact Fractions; an independent targeted rerun passed
(`1 passed in 1.75s`). The test file was also renamed to `test_ft_checks.py` so
directory collection includes it. These changes affect validation, not the
synthesized gates or the resource results. The author's subsequent complete FT
rerun reports `4 passed in 41.65s`.

The matrix/phase and exposure tests are executable independently of the synthesis
generator. Their final combined result should be retained with the release
validation receipt. No hardware or full pricing-QPE execution was performed in
this review.
