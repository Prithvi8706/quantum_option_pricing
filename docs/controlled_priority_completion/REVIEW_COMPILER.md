# Independent compiler and range review

Reviewer: estimator subagent, reviewing code authored by the root and range
subagent. This review does **not** independently approve the reviewer's own
Hadamard or bounded-output estimator. A different subagent reviews those.
This is an independent AI-agent technical review, not external peer review.

## Findings on the wave scheduler and range-specialized multiplier

No correctness blocker found in the reviewed compiler mechanisms.

1. **Private workspace and copies.** Each batch gives every leaf its own copied
   argument registers and scratch. Its outputs bind to distinct SSA words.
   A value used k times requires k copy rounds, even when repeated within one
   leaf. The maximum SSA argument multiplicity is sufficient: put occurrence j
   of each source value in round j, and all those CNOTs have disjoint controls
   and targets. The independent audit constructs these rounds explicitly and
   checks addresses and disjointness. The copies and uncopies are charged in
   Clifford-plus-T depth; they do not increment the T-depth convention.
2. **Dependencies and inverse.** Level construction puts every argument before
   its consumers. Calls in one wave have disjoint leaf wires after copying, so
   their execution can overlap. Each leaf implements a clean classical XOR
   permutation, including on nonzero output words. Repeating that same leaf is
   therefore its inverse on the clean-workspace subspace. Reversing wave order
   restores the needed original arguments and clears all SSA outputs. Since
   the circuits are exact X/CX/CCX permutations, this is a coherent statement,
   not only a computational-basis observation. For range-specialized leaves,
   the reachable original operands remain in their proved intervals during
   reverse execution.
3. **Resources.** Counts remain the sum of the same emitted primitive gates.
   A valid barrier schedule has forward T-depth equal to the sum over batches
   of their maximum leaf T-depth; repeating the clean leaves makes the inverse
   cost identical. Each batch's copy/un-copy rounds are paid twice across the
   full source. Space retains every SSA/output word and the maximum sum of
   private scratch in any batch. This is an all-to-all upper schedule. Its
   weighted atomic-leaf dependency calculation does not bound all possible
   circuits, gate-level pipelining or physical layouts.
4. **Asymmetric signed multiplication.** For certified a-bit and b-bit signed
   operands, retain n=min(w+f,a+b) product bits. For unsigned low-bit words A,B
   and sign bits alpha,beta,

       A_signed*B_signed = A*B-alpha*B*2^a-beta*A*2^b (mod 2^n).

   The omitted double-sign term is divisible by 2^n. Every correction uses at
   most the other operand's retained width. If n=a+b, the full signed product
   fits and sign extension before selecting output bits f through f+w-1 is
   correct, including f>=n. If n=w+f<a+b, no selected bit lies outside the
   retained product. The final copy and inverse arithmetic implement exactly
   the original signed-floor multiply modulo 2^w, with arbitrary XOR output.
   This does not assert correctness for out-of-range full-width operands.

The independent script `review_compiler.py` reconciles every existing saved
wave schedule's dependency order, private-wire assignments, copy rounds,
T-count, T-depth, Clifford-plus-T depth and workspace count. It also exhausts
all 1,024 inputs of an independently constructed five-bit primitive graph:
**253,952 intermediate signed values** are inside the range interpreter's
bounds. These checks supplement the algebra above; they do not substitute for
financial structural proofs.

## Range-certificate review

The generic interval operations preserve signed modular semantics. Signed
crossings widen to the full interval, unsigned operations explicitly reinterpret
their inputs, and intentional masked shifts are not confused with real
arithmetic. Min/max/absolute-value refinements are recognizable SSA identities.
The singular minimum signed integer in absolute value is handled by subsequent
modular normalization, not assumed representable as positive.

The interpolation-local and logarithm-mantissa bounds follow from the exact
clipped cell construction and most-significant-bit normalization. For exp, the
two checked fixed products imply k=floor(X*C/Q^2) and r=X-k*L. The floor's
fractional part gives the stated exact outward residual bounds. The first
product's no-wrap condition also ensures the intermediate k*Q shift fits, so
the identity does not silently discard an overflow in that shift.

The correlated financial lemmas were independently derived. Nonnegative
stocks, exact 1/d and 1/d^2 coefficients, and no preceding signed wrap imply
the moment-ratio bound

    (common+extra)*(B+1)^2/(B^2-Q).

This decreases for B>sqrt(Q). The dispersion bound follows by replacing
sum(x_i^2) by sum(x_i)^2, retaining the fixed-point square-rounding unit, and
dividing by the basket. Its squared ratio is also decreasing in positive B.
Thus using the certified minimum basket is conservative. The audit checks
the actual summations, squares, coefficients and guarded division structure.

`ranges_for_compiled` regenerates and compares the exact optimized target
before transferring ranges through canonical expressions. The old omitted
`preparation=uniform` default is normalized explicitly. It rejects changes to
the source, inputs, tables or outputs; intersection is used only for identical
expressions. This supports narrowing reachable operands in the specific bound
financial target. It does not certify a price error or a new arbitrary circuit.

## Joint arithmetic certificate: additional independent review

The separate `range_joint_arithmetic.py` and `RANGE_JOINT_ARITHMETIC.md` were
reviewed term by term. The core argument is sound for its explicitly stated
joint quantity: the **same digital baseline and correction use the same digital
policy value and exercise indicator**, then are compared with real arithmetic
on the same q32 guarded inputs. The policy cancels before final residual
clipping. Projecting the digital policy into exact Gaussian-control bounds
provides a bounded reference residual, which charges clipping by
e_c0+e_R+e_projection+e_support. Adding the unclipped cancellation error gives
the documented 2*e_c0+2*e_R+e_projection+e_support expression.

The coefficient/Taylor bounds, square-root radial expectation treatment,
lognormal standard-deviation denominators, and call/put sensitivities were
checked against the actual source. The proof does not require stable exercise
decisions or accurate regression coefficients. The high-precision coefficient
generator is not trusted as its own certificate: explicit interval formulas
verify its stored coefficients.

Before final sign-off, the reviewer requested executable checks for the
hand-selected exp domain/reduction constants, the forward and baseline value
caps, and a stated bound on the **digital** normal first moment below 2. These
have large slack in the fixed models. The author added exact integer exp
exponent/residual checks and interval checks of all financial exp/control
domains, stock/forward/policy caps, and the digital normal first moment. The
reviewer inspected those additions and found no remaining mathematical blocker
for the stated joint expectation bound. The reviewed code and result hashes
are recorded in the review receipt.

This certificate cannot justify reusing an old real-arithmetic policy's
baseline mean, regret samples or tight moment. A complete price still needs a
baseline estimator for the identical digital policy, its confidence/cost, the
finite-policy regret certificate, and the separate law/control bridge. It does
not change the failed cost gate or establish an end-to-end advantage.

## Validation provenance and remaining limitations

`results/controlled_priority_completion/review_compiler.json` is the executable
audit receipt. The root's saved full C4/H8/phase basis executions check complete
production gate programs and inverses. The isolated final-suite validation is
separate; the reviewer's initial local pytest invocation used the existing
research environment with user-site pytest enabled. Its result must not be
described as an isolated environment run.

No full coherent financial superposition/QPE was simulated, no physical layout
or decoder was validated, and no hardware runtime or quantum-over-classical
speedup follows from these compiler correctness checks.

## Final composed resources and wrapper binding

The reviewer checked `combined_cost.py` after the range-specialized sources
were emitted. Its replacement of financial/phase counts and wave depths is
consistent with the immutable source manifests. The Hadamard controlled-phase
multiplicities, signed highest angle bit, exact nearest-neighbor IQFT phases,
remaining synthesized IQFT angles and their three-single-rotation decompositions
reconcile with the verified rotation library. Serialized rotation T counts are
a conservative depth addition, not an optimized physical schedule.

The first composed cost artifact lacked an authoritative emitted wrapper bound
to the new workspace offsets and wave schedules. This was fixed: the root
emitted/replayed the bounded wrapper, and the reviewer implemented
`combined_wrappers.py` to emit the Hadamard wrapper and bind all six estimator
rows to source/schedule hashes, exact allocations, controller operations,
state preparation, measurements and synthesis multiplicities. Because the
reviewer authored that binding code, it requires the root's separate review;
this document does not label that part independently self-approved. Its tests
check the changed offsets, Y promotion, signed phase bits, hierarchy hashes,
controller import, integer repetition powers and actual rotation-string costs.
