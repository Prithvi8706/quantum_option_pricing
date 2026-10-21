# Scalar AS241 IR preflight

Author-stage design only. No graph, compiled leaf, gate replay, quantum cost, or new
test has been emitted. Stage C timing jobs remain untouched. This design depends
on the single native-transform certificate succeeding and on an independently
reviewed law-transfer receipt before any sampler adoption.

## Exact ABI and source bindings

- One original-style uniform raw input `k`, unsigned 32 bits, with 72-bit native
  registers and 40 fraction bits. Its distribution is uniform on all `2^32` words.
- The exact scaled midpoint is `u_raw = (k << 8) + 128`. The shift is a bit shift,
  not a fixed-point multiplication. It gives `(2*k+1)*128` with no rounding.
- One named signed 72-bit output `Z`, representing the new signed-restored AS241
  approximation. The output is not the exact downward-rounded normal quantile.
- Independent invocations use independent raw words. This is a different scalar
  law from the accepted finite paired Box-Muller source.
- Central coefficients are the exact saved published decimals and nearest-even
  f40 raw words in `A02_quantile_central_run002/central_certificate.json`.
- Ordinary-tail coefficients are the exact saved published decimals and
  nearest-even f40 raw words in `A02_quantile_tail_run001/tail_certificate.json`.
- The logarithm uses exactly the original archived 32-by-9 degree-eight table and
  literal `ln2_raw = 762123384786` bound by `C06_pair_run001` and the forthcoming
  `A02_quantile_transform_run002`. No coefficient regeneration or fitting.
- The central `r` constant is the saved `ceil_f40(289/1600)`. The ordinary-tail
  subtraction is the saved nearest-even `f40(8/5)`, raw `1759218604442`.
- Division is the positive-magnitude native semantics
  `floor((numerator_raw << 40) / denominator_raw)`. A mathematical range proof
  does not establish an emitted divider, cleanup, gate cost, or typed dispatch.
- Square root is mathematically `isqrt(nonnegative_argument_raw << 40)`. The
  archived unsigned-46 native contract is a reference, not a new-site adoption.

All constants must enter with `Graph.const_int` or exact integer node parameters.
`Graph.c` and `Graph.cmul` use floating conversion, so published-decimal rounding
must not flow through those convenience methods.

## Branch and sign decisions

Let `S = 2^40`, `q_raw = u_raw - S/2`, and
`p_raw = min(u_raw, S-u_raw)`. The comparisons and both arguments to each select
are evaluated and paid. The negative sign flag is the exact comparison
`u_raw < S/2`; no midpoint equals one half.

The mathematical central branch is `3/40 <= u <= 37/40`, equivalently
`p >= 3/40`. The largest ordinary-tail midpoint uses the fixed lower raw word
`k_tail = 322122546`; the first central midpoint uses `k_central = 322122547`.
Define exact integer constants:

```
P_TAIL = (2*322122546+1) << 7
P_CENTRAL = (2*322122547+1) << 7
Q_CENTRAL = S/2 - P_CENTRAL
P_BRANCH = nearest_even_integer(3*S/40)
```

The preregistered branch comparison is `p_raw < P_BRANCH`. Its correctness is an
integer obligation, not an assumption about floating decimals:

```
P_TAIL < 3*S/40 < P_CENTRAL
P_TAIL < P_BRANCH <= P_CENTRAL
P_CENTRAL - P_TAIL = 256
```

Every lower-half midpoint has raw value congruent to 128 modulo 256. Hence there
is no possible input between these adjacent boundary words, and comparison with
`P_BRANCH` agrees with the exact `3/40` branch. Equality with `P_BRANCH` is not a
midpoint. Reflection about one half preserves this statement in the upper half.

The branch is inclusive centrally. Equality at `3/40` or `37/40` cannot occur for
the q32 midpoint law, because those rational denominators contain a factor five.

## Both SSA branches must be safe

`Graph.select` does not avoid computing its unused operand. A tail input fed
directly into the central polynomial can make its `r` negative; a central input
fed directly into the ordinary-tail transform can make its transformed `r`
negative. Neither is allowed to inherit the selected branch's proof premise.

The fixed paid guards are:

```
q_abs_raw = select(sign, -q_raw, q_raw)
q_central_raw = min(q_abs_raw, Q_CENTRAL)
p_tail_raw = min(p_raw, P_TAIL)
```

For every selected central input, `q_abs_raw <= Q_CENTRAL`, so its guard is
inactive. For every selected tail input, `p_raw <= P_TAIL`, so its guard is
inactive. No additional scalar approximation error enters the selected result.

Every input to the unused central branch lies in the already certified central
domain. Every input to the unused tail branch is a genuine q32 ordinary-tail
midpoint, including the fixed guard value. In particular, `p_tail_raw` remains
odd times 128. The existing exact logarithm normalization proof, its eleven low
mantissa zero bits, and its 960 cell/exponent combinations therefore remain
applicable to both selected and unselected tail evaluations.

Guards require actual comparisons, selections, constants, storage and inverses.
They are not free classical branches or free range promises. No narrower input
contract may be installed until the complete new graph proves the corresponding
producer invariant at that exact native call site.

## Central magnitude and exact sign restoration

On the guarded nonnegative central magnitude, the required order is:

1. Compute the full 144-bit product `q_central_raw^2`, floor by shifting 40 bits,
   and subtract it from the archived central `r` constant.
2. Evaluate both positive-coefficient Horner polynomials in that `r`, using the
   native full-product-then-floor multiplication semantics at every stage.
3. Compute the nonnegative numerator
   `floor(q_central_raw * A_raw / 2^40)`.
4. Divide the positive numerator by the positive denominator with the specified
   unsigned shifted-numerator floor semantics.
5. Restore the original input sign by exact two's-complement subtraction from
   zero; select the negated or nonnegative quotient.

Multiplying the signed negative `q` before flooring would produce a different
function: in general, `floor(-a)` is not `-floor(a)`. The accepted central
certificate is specifically for positive-magnitude flooring followed by exact
sign restoration. That ordering must survive any optimization.

The two branches share one unsigned divider by selecting the numerator
`floor(q_central_raw*A_central_raw/S)` versus `A_tail_raw`, and selecting
`B_central_raw` versus `B_tail_raw`, before division. This retains the accepted
central floor order. Division must not move before the magnitude multiplication:
with exact toy raw integers `S=16,q=6,A=56,B=24`, the accepted order produces
`floor(floor(6*56/16)*16/24)=14`, whereas dividing first produces
`floor(6*floor(56*16/24)/16)=13`. This is an arithmetic counterexample, not a
claimed reachable financial path or an evaluated AS241 fixture.

The central domain and archived native certificate give `r >= 0`, positive
Horner outputs, denominator at least `S`, signed-72 stored values, full signed-144
products, and an unsigned-112 shifted numerator. The additional divisor-64 upper
bound is a separate mathematical interface proof in the transform certificate;
it does not validate a compiled divider or output-clamp optimization.

## Ordinary-tail magnitude and exact sign restoration

On `p_tail_raw`, normalize and evaluate the original archived logarithm exactly.
Negate the already rounded signed log word by subtraction from zero, apply the
native nonnegative sqrt interface, and subtract the saved nearest-f40 `8/5` raw
constant. Evaluate the ordinary-tail positive Horner numerator and denominator,
perform the positive magnitude division, then restore the original sign exactly.

The native-transform all-input proof must establish that input and mantissa
clamps are inactive, signed negation adds no new floor, the true/native sqrt
radicands stay above the declared lower margin, and the transformed native `r`
stays in `[0,3.21]`. Its fresh argument-sensitivity ledger replaces the old
hypothetical exact-transform floor allowance. Only the saved real rational error
and this fresh native arithmetic are composed.

For every guarded tail evaluation, the native radicand is unsigned 45 bits and
fits the archived unsigned-46 semantic interface; its shifted radicand is at
most 85 bits, within the conservative 86-bit interface allowance. Positive
denominator, stored-72, full-product-144, shifted-numerator-112 and divisor-64
proofs remain required at each new site. No clamp is assumed inactive without
that proof, including `Graph.div`'s raw-one denominator guard and
`Graph.sqrt`'s positive guard.

## Archived logarithm frontend

The current `Graph.log` calls `interpolate`, whose frontend calls
`coefficients(...)` to regenerate a table. A new sampler must not silently use
that route as an archival binding. A prospective exact frontend must insert the
already frozen table, the same msb/exponent/mantissa/index/center/local nodes,
the same signed Horner arithmetic, and the exact archived ln2 integer parameter.
It may reuse existing primitive operations; it must not mutate the existing
`ir.py`, its coefficient cache, or any frozen financial source.

The exponent is an unscaled signed integer. Scaling it by `2^40` is exact;
multiplication by the archived ln2 literal cancels that scale exactly, including
negative exponents. A raw integer exponent must not be mistaken for an already
scaled fixed-point quantity.

## Prospective execution boundary

Before emitting a complete graph or running new tests, freeze a separate single
scalar implementation protocol with these constants, exact branch and guard
rules, source fingerprints, one optimizer/compiler configuration and a bounded
fixture list. Source/result binding must preserve the new signed-restored law;
it must not claim the prior exact quantile-floor law or the original Box-Muller
law. Native guards need whole-graph validation before typed leaf reuse.

The first graph/semantic test may establish actual SSA equality and safe operand
interfaces. Reversible leaf generation, full invocation cleanup, dirty-output
XOR behavior, actual gate costs, independent source audit, financial native-path
error propagation and any replacement of the accepted financial sampler remain
subsequent separate steps. All eagerly evaluated guards and unused branches must
be present in the eventual resource bill.
