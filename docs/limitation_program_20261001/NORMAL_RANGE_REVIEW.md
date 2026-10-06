# Independent review of the exact normal-radius interval proof

**Verdict:** no soundness defect found in the interval rules or the two structural refinements for the frozen B4/B8 graphs. [A07_run003](../../results/limitation_program_20261001/A07_run003/summary.json) is a reviewed static proof component for the current digital target. It establishes nonnegative 46-bit radius inputs and 43-bit outputs at all 30 / 234 square-root sites. It does not adopt a narrowed circuit, change SSA packing or measure a resource gain.

This review read [interval_bounds.py](../../research/limitation_program_20261001/interval_bounds.py), [test_interval_bounds.py](../../research/limitation_program_20261001/test_interval_bounds.py), [prove_normal_ranges.py](../../research/limitation_program_20261001/prove_normal_ranges.py), the SSA provenance validator and the exact integer evaluator. No implementation, protocol, archived result or progress file was changed. No new scientific tests, financial gate replays or circuit experiments ran.

## Integer rules and modular overflow

Intervals contain signed two's-complement integer words, with the fixed fraction applied only by operations that require it. The `safe` rule accepts arithmetic endpoint bounds only when the entire interval fits the signed word; otherwise it returns the full signed domain. Add/sub endpoint arithmetic is monotone, and multiplication uses all four rectangle corners followed by monotone integer floor. Negative coefficients are handled by sorting both constant-product endpoints after signed integer floor. These rules preserve containment even when the true operation wraps modulo the word width.

The full-domain fallback trades tightness for correctness. A wrapped result is not represented by a falsely narrow unwrapped interval. Unsupported operations also start at the full domain. Positive-part bounds are the monotone image of the signed interval. The positive-divisor division refinement uses unsigned nonnegative numerator and positive denominator endpoints; other division cases fall back conservatively.

## Input preparation is part of the theorem

A declared uniform input narrower than the word has raw support `0..2^bits-1`, and its high bits are zero. A full-width uniform word instead uses the full signed interval, including the negative half of its raw support. Inputs with another preparation mode also use the full signed domain.

Both reviewed production graphs declare **only 32-bit uniform inputs inside 72-bit words**: 60 words for B4 and 468 for B8. Thus the narrowed input intervals agree with the actual source preparation contract. The generic evaluator accepts wider words for testing, but those words would violate this declared source domain; this proof does not cover such invalid input preparations. A future dispatch must bind to the same target and preparation declarations rather than attach the range promise to an arbitrary standalone square-root input.

## Unsigned primitives and bit extraction

Square root and MSB act on the **raw unsigned operand**, as the integer evaluator specifies. A wholly negative signed interval converts to the corresponding upper unsigned interval. A signed interval crossing zero conservatively becomes the entire raw word range. Integer square-root endpoints use `isqrt(raw << f)`; the output is then converted back to a signed-word interval if necessary. MSB uses the unsigned highest-bit index and handles zero as index zero. Neither rule interprets a negative raw operand as a negative real number.

Bit extraction follows the evaluator's signed/unsigned shift choice and output mask. Full-width left shift can use the signed input interval because multiplication by a power of two gives the same raw modular word under either interpretation; overflow falls back. Narrow masking that cannot be enclosed by the unmasked endpoints uses the full masked raw range. General variable shifts enumerate the bounded shift classes, with `k>=w` mapped to zero and `k<=-w` to sign saturation. Saturation safely covers arbitrarily larger shift magnitudes.

## Comparators, selection and coefficient lookup

The comparison interval is constant only when all represented operand pairs have the same strict signed ordering; otherwise it includes both flag values. Boolean results are converted to signed-word form, including the one-bit-word edge case.

General selection takes a branch union unless the flag is known zero or one. Same-SSA patterns `select(lt(x,y),y,x)` and `select(lt(x,y),x,y)` receive monotone max/min bounds. These refinements depend on the actual producer identities, not on two unrelated intervals looking similar. Using a nonboolean signed flag merely causes a wider branch union, so its low-bit selection semantics remain covered.

Lookup bounds include **every literal row**, with each coefficient reduced to its signed word representation. The proof does not assume a favorable subset of addresses or estimate coefficient ranges from sampled paths. The reviewed production tables and node shapes match the evaluator's literal lookup semantics.

## Same-SSA normalization

The normalization refinement recognizes a shift of the same positive `x` by the exact chain `0-(msb(x)-f)`. The graph snapshot validates unique ordered SSA producers, and the matcher verifies the predecessor operations, argument identities and fraction literal.

For `x>=1`, let `m=floor(log2(x))`. Then shifting by `f-m` gives a word in `[2^f,2^(f+1)-1]`, whether the shift is left or arithmetic right. The guard `f+1<w` keeps that normalized result below the signed sign bit. Because the positive signed input has `m<=w-2`, both the exponent subtraction and its negation fit the signed word in this guarded case; no hidden shift-amount wrap invalidates the identity. If the positivity, literal or producer chain differs, the refinement does not apply.

The successful certificate records this normalization at **30 / 234** SSA values. This is a structural all-domain rule; finite production traces are corroborating checks, not its justification.

## Same-SSA bin residual

The bin refinement ties the residual to the literal-address construction in the same graph:

`index = bits(x-origin, k, b)`

`center = bits(index, -k, full_word) + offset`

`residual = x-center`.

It requires `step=2^k`, `offset-origin=step/2`, and the whole input interval inside `[origin,origin+2^b*step)`. It also checks that the preceding subtraction, left shift and center addition have not fallen back to the full-word interval. For these recognized operations, a non-full arithmetic bound establishes that the necessary intermediates avoid wrap. The index therefore equals the unmasked bin quotient, yielding residual `[-step/2,step/2-1]`. Changed centers or unrelated producer chains cannot use the special bound.

The production certificates contain one accepted bin-residual refinement per graph. Other residuals retain their conservative propagated intervals; the review does not claim every possible bin pattern was tightened.

## Provenance, tests and numeric endpoint checks

I independently verified **12 saved manifest artifacts**, **five frozen dependency/snapshot pairs** and **two frozen target hashes**. Both target byte hashes also match the current accepted A09 source targets exactly, so the graph proof applies after A09's exact multiplier substitution. A09 did not change the graph, precision, loading law or integer multiplication semantics.

Every saved square-root site was checked against its actual target node and recorded input/output SSA values. Its saved endpoints satisfy the unsigned integer-square-root relation exactly. The two interval families are identical across both cases:

| Radius input interval | Radius output interval |
|---|---|
| `[0, 50,300,143,395,876]` | `[0, 7,436,772,992,539]` |
| `[0, 55,729,367,232,324]` | `[0, 7,827,840,524,725]` |

All input maxima are below `2^46`, and all output maxima below `2^43`. The site list covers exactly all **30 / 234** target square-root nodes, with no additional assumed range promise.

The saved regression receipt reports **11 tests passed in 0.87 seconds**. It covers every small signed input pair at widths 1..5 and every allowed fraction `0<=f<w`, signed arithmetic/wrap, unsigned sqrt/MSB, bit extraction, saturated shifts and both refinement negative controls. The production containment checks cover 13 / 11 vectors and **74,074 / 514,822** SSA trace values. These samples cannot establish a theorem over all production bit strings; the reviewed inductive rules and structural refinements provide that justification.

[A07_run002](../../results/limitation_program_20261001/A07_run002/summary.json) remains a preserved failed harness attempt. It included `f==w`, which the existing SSA validator explicitly rejects. A07_run003 corrected the test domain to the existing `f<w` contract and added an explicit rejection test for all-fractional words. This was a harness-contract correction, not removal of an arithmetic counterexample.

## Practical limit of this result

The current radius bounds are suitable evidence for a later guarded exact specialization. Such an experiment still needs a versioned input-range interface, exact clean leaf verification, fallback handling, full capped-source accounting and financial gate replay before adoption. The SSA validator establishes graph provenance rather than complete typing of every possible malformed operation; reuse should stay bound to the validated current primitive semantics and frozen target.

No square-root leaf has been narrowed by this run, no output high bits have been removed from storage and no resource improvement is credited. This proves a property of the current finite integer function. It does not certify continuous Gaussian loading, dollar error, estimator confidence, a matched classical runtime or physical quantum advantage.
