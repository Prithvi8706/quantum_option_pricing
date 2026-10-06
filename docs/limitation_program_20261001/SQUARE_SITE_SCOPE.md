# Exact same-SSA square feasibility

An exact square specialization is mathematically viable, but the accepted A09
schedule offers little direct depth benefit from improving these calls alone.
Proceed with one bounded clean-leaf screen for T work and workspace reduction;
rank its integration priority again after the square-root experiment. This
inventory does not build a circuit or credit any resource improvement.

| Accepted A09 source | All multiplication calls | Exact same-SSA squares | Batches where squares reach maximum depth | Batches tied with distinct multiplication | Batches with only squares at maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| B4x12 | 1,440 | 144 | 52 | 51 | 1 |
| B8x52 | 11,856 | 1,248 | 58 | 58 | 0 |

Every selected site has literal equality of its two argument SSA identifiers.
Equal sampled values, similar expression trees and overlapping intervals are
insufficient to admit a specialization. The sites are the three successive
self-products in each exponential Estrin power chain: the range-reduced input
is squared, its square is squared, and the resulting fourth power is squared.
There are 48 copies of each level in B4x12 and 416 in B8x52. The interval
inventory records existing signed bounds and separately computes square
endpoint bounds before word wrap; some of these mathematical bounds exceed
signed72. No narrower-input or nonnegative-output promise is adopted.

For a signed w-bit input, write
`x = sum(a_i * 2**i, i < w-1) - a_(w-1) * 2**(w-1)`. Its exact square has:

- One diagonal Boolean bit `a_i` at product column `2*i`, including the positive
  sign-bit diagonal when it survives the product modulus.
- One off-diagonal Boolean product `a_i*a_j`, for `i < j`, at column `i+j+1`.
  The extra column accounts for the two equal cross-products.
- Negative cross-products exactly when the pair includes the sign bit.
  Complement each negative product and add the fixed negative-weight correction.

Compute the product modulo `2**(w+f)`, retain every column below f through
carry propagation, and extract columns f through f+w-1. Only columns at or
above w+f may be dropped. This produces exactly
`floor(signed(x)**2 / 2**f) mod 2**w`, including wrapped results.

| Mathematical signed72/f40 normal form | Generic multiplier with identical inputs | Symmetric square |
| --- | ---: | ---: |
| Retained Boolean terms | 4,688 | 2,356 |
| Diagonal monomials | 56 | 56 |
| Off-diagonal terms | 4,632 | 2,300 |
| Negative terms | 82 | 40 |
| Fixed correction | 2^72 | 2^72 |
| Maximum initial column height, including correction | 72 | 38 |

The existing generic circuit uses a Toffoli for every partial term, including
diagonals bound to distinct copies of the same source input. A square builder
could copy the 56 diagonal bits with CNOTs and compute the 2,300 distinct
off-diagonal products once. These are normal-form opportunities; complete
reversible CSA compression, the prefix adder, output copy and inverse cleanup
must all be emitted and measured before claiming a T-count or width saving.

The polynomial coefficients agree universally on Boolean inputs with the
existing `signed_partial_terms`, including the full72/f40 case. Complement
constants cancel exactly modulo the retained product width. Exhaustive tests
also passed for all signed inputs at widths 1 through 6 and all fractional
scales 0 through w: 27 configurations and 768 signed input cases. A negative
control shows why low columns must remain: at width3/f3, signed x=3 gives
`9 >> 3 = 1`; deleting terms below column3 before summation gives zero.

Saved A09 batch costs were reconciled against their actual call indices and
leaf metadata. Making every square free while holding those batches fixed
would remove only 2,824 T-depth layers from B4x12's 1,218,582 and none from
B8x52's 1,268,304. This is an optimistic diagnostic for those fixed batches,
not an achievable gain or a bound on a different packing/schedule. The square
and distinct-multiply leaves currently have identical 1,412 T-depth. Most
square maxima therefore remain pinned by a distinct multiplication in the
same batch. Deterministic ownership of tied batches is also reported, but it
is an accounting choice and must not be interpreted as exclusive leverage.

The concrete next experiment is one full72/f40 symmetric signed square leaf
using the existing CSA recurrence and Brent–Kung final adder. Preserve all 112
product columns needed for floor extraction. Validate arbitrary 72-bit output
XOR, historical multiplier equivalence, forward/inverse operation and clean
workspace on exhaustive small signed inputs and production edge/random
patterns. Dispatch only on validated same-SSA argument equality and keep the
generic multiplier fallback. Then screen complete capped schedules against
the current accepted source, with separate T-count, width and depth decisions.
Stop this branch if the measured complete leaf offers no useful improvement;
the normal-form term ratio alone does not justify integration or replay.

[Inventory and arithmetic receipts](../../results/limitation_program_20261001/A09_square_scope_run001/summary.json)
contain every site, interval class, producer pattern, batch maximum and frozen
input hash. [The local inventory script](../../research/limitation_program_20261001/inventory_square_sites.py)
does not edit accepted sources or progress. No gates were executed, no circuit
or source gain was credited, and nothing was pushed.
