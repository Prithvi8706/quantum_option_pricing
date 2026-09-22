# Exact intermediate ranges for the existing digital source

This is a deterministic range certificate for the existing **f40/q32** financial
source. It quantifies every finite uniform-word input, and does not use a sampled
maximum. All four development models have zero unresolved signed-arithmetic
overflow sites after the structural lemmas below. This closes the intermediate
range obligation for these source graphs; it does **not** bound their difference
from real arithmetic, certify policy regret, or establish quantum advantage.

| Model | SSA nodes | Log normalization lemmas | Interpolation cells | Exponential reductions | Remaining overflow sites |
|---|---:|---:|---:|---:|---:|
| C4 | 10,436 | 58 | 222 | 74 | 0 |
| C8 | 19,673 | 106 | 414 | 146 | 0 |
| H4 | 10,492 | 58 | 222 | 74 | 0 |
| H8 | 38,760 | 208 | 816 | 290 | 0 |

The source uses intentional two's-complement masks and bit shifts. Their exact
modular semantics are included; absence of signed arithmetic overflow does not
mean these intentional bit operations were replaced by real arithmetic.

## Proof mechanism

`range_audit.py` propagates inclusive integer intervals, with exact Python integer
endpoints, through each SSA operation. Multiplication and division are rounded
exactly as in the digital target. A result crossing a signed wrap boundary is
replaced by the full signed interval. Comparisons plus selections implement
recognized minimum, maximum and absolute-value patterns. Lookup ranges include
every reachable coefficient row. No floating-point rounding occurs in the
integer interval propagation.

The following dependencies require more than ordinary interval arithmetic.

1. For an interpolation cell of raw width `s`, the implemented clipped cell
   index and center imply `-s/2 <= local <= s/2-1` exactly.
2. For positive raw `X`, logarithm normalization uses
   `e=floor(log2(X))-f` and shifts `X` by `-e`. Its raw mantissa lies in
   `[2^f,2^(f+1)-1]`, including right-shift truncation.
3. For exponential reduction let `Q=2^f`, `C=round(Q/ln(2))`, and
   `L=round(Q*ln(2))`. The constructed integers satisfy
   `k=floor(X*C/Q^2)` and `r=X-k*L`. Consequently
   `r=X*(Q^2-C*L)/Q^2 + theta*L`, `0<=theta<1`. Exact outward integer
   bounds follow from the known interval for `X`. The lemma is applied only
   when the preceding fixed multiplications cannot wrap.
4. The moment ratio and dispersion share the same nonnegative stock words.
   Discarding that dependence produces three inconclusive sites in H4/H8;
   the following identities close them without changing the source.

For item 4, write stock raw integers `x_i>=0`, `S=sum(x_i)`,
`B=floor(S/d)`, and `Q=2^40`. Here `d` is 4 or 8, so the basket coefficient
and `1/d^2` are exact binary fractions. Set `b` to the certified minimum `B`.
The audit checks `b>0`, `b^2>Q`, nonnegative stocks, and absence of preceding
signed wraps before applying either bound. It recognizes the actual SSA
summations, squares and coefficients; this is not an assertion about an
unrelated real-arithmetic model.

For the second moment, the exact rounded source uses nonnegative raw
coefficients `c,e`, `sum(floor(x_i^2/Q))`, and `floor(S^2/Q)`. Since
`sum(x_i^2)<=S^2` and `S<d(B+1)`, its raw numerator is at most
`(c+e)*(B+1)^2/Q^2`. The mean-return coefficient is at least `Q`, so
the squared denominator is at least `B^2/Q-1`. Its division is bounded by

```
ratio_raw <= floor((c+e)*(b+1)^2/(b^2-Q)).
```

For dispersion, the rounded variance numerator satisfies

```
variance_raw * Q <= (d-1)*B^2 + 2*d*B + d + Q.
```

The rounded square root and quotient therefore obey

```
dispersion_raw <= floor(sqrt(Q^2*((d-1)*b^2+2*d*b+d+Q)/b^2)).
```

Both right-hand sides decrease as positive `B` increases over the stated
domain. Subsequent regression multiplications then fit the original 72-bit
word. These are range statements; numerical accuracy of the policy is a
separate question.

## Compiler interface and scope

`ranges_for_compiled(data, model)` returns `{bounds, target_sha256, guaranteed,
signed_overflow_sites, width, fraction_bits}`. `bounds` maps each **compiled
target** SSA value to its raw signed interval. It regenerates
`optimize(prune(full_source, requested_outputs))` and requires exact equality
with the supplied target, except that an omitted historical input-preparation
field is normalized to its documented default `uniform`.

It then transfers intervals through canonical exact constant folding, aliases
and commutative expression keys. Bounds for identical expressions are
intersected; missing expressions, changed tables or changed outputs fail
closed. The guarantee concerns reachable inputs of the bound financial graph,
not every possible bit pattern presented to an isolated narrower leaf.

This creates a defensible opportunity to specialize multiplier operands:
C4's largest certified operand requires 55 signed bits; H8's requires 57.
Many need only 40--42. Output widths and sign extension still have to be paid,
and an actual compiled implementation and replay are required before reporting
any resource reduction. This document does not count a width histogram as a
speedup.

## Validation and reproduction

```
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_priority_completion.range_audit
.context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_priority_completion/test_range_audit.py -q
```

The tests exhaust reduced-width operation inputs and reduced-precision
elementary-function inputs, check rounded correlated identities, verify the
annotated source is unchanged, and check production-width corner traces lie
inside the certified intervals. The corner traces are implementation checks,
not the proof of the universal range statements.

Results: [range_audit.json](../../results/controlled_priority_completion/range_audit.json).
The full joint arithmetic expectation certificate, tight moment transfer and
finite-policy regret remain separate obligations.
