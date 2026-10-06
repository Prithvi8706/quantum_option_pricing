# Independent A20 multiplication-sharing review for prospective V5

The two selected stock closures implement the same native scalar function of
their clipped-log input. Exactly five nodes differ only by reversing the two
operands of same-width signed72/F40 multiplication. A separate semantic
signature may canonicalize those `mul` operands to justify the same fixed
eight-word lookup table. The original ordered source/leaf bindings and their
resource costs must stay unchanged. Actual ordered backend depths differ.

This is a bounded prospective proof/text/metadata review, with no gate emission,
scalar stock evaluation, table construction, price evaluation, producer retry
or component approval. It supplies no whole-source cost or financial theorem.
The failed V4 producer and diagnostic's structural rejection remain immutable.
A new root-reviewed preregistration is required before any V5 execution.

## Fixed evidence and checks

Selection is the actual B4x12/min-depth source's assets0/1, date0, bounded at
each original `clipped_log` SSA. Both complete closures contain45nodes, with
common normalized output45 and identical source-signed clamp literals
`[-12193974156573,9145480617430]`. The five differences are:

| Normalized output | Asset0 ordered args | Asset1 ordered args | Constant raw word |
|---:|---|---|---:|
| 11 | `[6,10]` | `[10,6]` | 183251937963 |
| 18 | `[6,17]` | `[17,6]` | 9162596898 |
| 22 | `[6,21]` | `[21,6]` | 218157069 |
| 31 | `[6,30]` | `[30,6]` | 3029959 |
| 35 | `[6,34]` | `[34,6]` | 27545 |

All five have operation `mul`, parameters `{}`, and unchanged output identity.
Normalized value6 is the same range-reduction residual function. Every other
normalized operation, ordered arguments, parameter/literal and output is
identical; there is no asset-dependent constant or clamp repair here.

The independent metadata inspector reconstructed both45-node postorder
closures directly from the fixed target/census, reproduced the previously
saved SSA correspondence, checked exactly these five reversals, and confirmed
that sorting only the two `mul` operands yields identical45-node semantic
metadata. It then bound all10actual accepted source calls and their selected
leaf metadata to the original owner's expected hashes. Fixed30CPU/90wall
inspection completed at0.25CPU/0.078wall; these are administrative guards,
not timing comparisons. Evidence is
`research/limitation_program_20261001/continuation_20261004/A14/A20_MUL_METADATA_REVIEW_v5b.json`,
SHA `0e3f461b75a069580aff670110f9269165b5a709e4c59e4b0061c699462f67d7`.
There is no complete historical-owner/runtime admission claim from this subset.

Selected immutable inputs:

- Original target: `A10_coefficient_run001/B4x12/min-depth/target.json`, SHA
  `a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384`.
- Original source: corresponding `source.json`, SHA
  `d40db71a1946f49e40683b6686579bc572f668de03f5968ccc5911189760e21f`.
- Original owner manifest: `A10_coefficient_run001/manifest.json`, SHA
  `0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40`.
- E22 B4x12 census, SHA
  `35b9cf84b23b10d871dbb64e5af1bdfe9c9ce58db811ac089f7729c6eebfabb3`.
- Saved independent two-closure diagnostic summary, SHA
  `32cbff9cabe75e561070954f50d9389771caa08da8f50f00c8cba208a5bc15b6`.
- Held producer builder `arithmetic_free_basket_signal_v2.py`, SHA
  `4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a`;
  V4 independent auditor, SHA
  `1c57ba091babaf32e38315a567fa440f860ae809ab71f8b6b2903c3633362407`;
  V4 producer controller, SHA
  `29caac64dbb3c217d4ee6366b326f0aa10cc57f0805c3fcdf0043a087b74bf3d`.

The first metadata inspector assumed a `files` field in the pinned flat A10
legacy owner and stopped with `KeyError: 'files'` before producing its result.
Its source/preflight remain unchanged; failure metadata and the exact
tool-returned traceback text are retained in `A20_METADATA_REVIEW_v5_failure.json`.
A distinct v5b inspector changes only that explicitly checked legacy schema
and fresh result route; its preflight fixes the same corpus/budgets. It does
not promote the failed inspector or the earlier scientific failure.

## Native multiplication and eager-value proof

Let `M=2^72`, `Q=2^40`, and `s(x)` decode a raw72word as signed two's complement.
The source IR's full-word multiplication is

`mu(x,y) = floor(s(x)*s(y)/Q) mod M`.

Integer multiplication is commutative, so the integer product, its arithmetic
floor quotient and the final raw word are identical under `(x,y)->(y,x)`.
This includes negative nonmultiples ofQ: equality uses the same product before
flooring, and does not substitute truncation toward zero. The source IR
`evaluate` uses `(v[0]*v[1])>>f` followed by the common72-bit mask; `ir.py` SHA
`3a4af54bd2e439ef060b747ea8f26a0897ce9e4a119509b57fb018d936d5d223`.

The V4 producer's `scalar_stock` and independent auditor's
`independent_stock_word` both decode the two `mul` inputs as signed72 integers,
form the full signed144 product, floor byQ, and reject a retained result outside
`[-2^71,2^71-1]`. For valid preceding nodes both operands are integers in that
same signed range; their product has magnitude at most2^142 and fits signed144.
Swapping those operands therefore preserves every product guard, the exact
unmasked retained integer, the no-wrap guard and its stored72-bit word. The
second-operand type/range guard is also unchanged because each preceding raw
operand already decodes into signed72. No active-width gate contract is used
by these offline scalar interpreters.

Prove the complete closure equality by induction over the common45-node
normalized topological sequence. Base value0 is the same clipped-log raw word.
Identical constants introduce identical raw/signed values. At unchanged nodes,
identical operation/params and equal mapped predecessor values produce equal
eager values. At each of the five swapped nodes, the multiplication identity
gives equal eager product and output. All later values, including the shift
count at normalized3 and final shifted stock output45, are then equal. The
two partial no-wrap scalar evaluators accept or reject the same input with the
same numerical guard truth. Under the source's total modular semantics, the
two closure words also agree independently of a no-wrap certificate.

This induction is over functions of the same boundary input; it does not assert
that the two actual assets have equal path/clipped-log realizations. It proves
neither global no-wrap safety nor `0<=F<8192Q` by itself. Existing support
binding and all original native/eager guards remain mandatory. The eight fixed
knots still require fresh actual scalar authorization and independent checks
in V5; this review evaluates none of them.

## Sharing signature and ordered backend limits

The safe implementation change is a separate semantic-sharing signature:
reconstruct each original closure without modifying the target or visitation
order, retain its original SSA and ordered `normalized_nodes` binding, then
sort exactly the two mapped operands of each well-typed `mul` in a separate
signature view. All other operations/arguments/params and clamp literals stay
exact. Do not commute `sub`, `cmul`, shifts or bit-window parameters, introduce
associativity/factoring, alter constants, or sort operands before assigning
the original normalized correspondence. Keep each raw template hash and add
a distinct semantic signature/hash. The independent auditor must derive the
same sharing proof from original source metadata rather than accept the
producer's signature alone.

Actual selected source backend metadata makes the cost boundary concrete:

| Outputs | Asset0 ordered active widths / leaf T depth | Asset1 ordered active widths / leaf T depth |
|---|---|---|
| 11,18,22 | `[72,40]` /1076 | `[40,72]` /1012 |
| 31,35 | `[72,24]` /1009 | `[24,72]` /913 |

All leaves have full72ports/fraction40/product112, but their sign-extension
promises are ordered. The first pair uses different held leaf keys
`44e04a2a2977eac24772` and `0e53da079f2257cd8c6b`; the second uses
`bb37d8eada9f1cbcbe7e` and `0d5149452181f9ada528`. Selected calls each retain
288argument-copyCX. Within each pair saved Tcounts/qubits match, but the
actual saved dependency depths differ. This review checks their owner-bound
metadata only; it does not replay or recount those historical arrays.

Consequently equal scalar semantics does not authorize swapping caller ports
under an unchanged ordered leaf, reusing a different active-width promise,
deduplicating old gate arrays, or transferring one asset's source depth/cost.
Any source/backend rewrite requires its own actual slot promises, ordered
bindings, new gate/copy/inverse accounting and capped schedule proof.

These ordered leaves do not block the restricted common-table component:
its new comparator/QROM recipes do not invoke the old scalar multiplication
arrays. On the same prescribed eight clipped-log knots the proven functions
give identical table literals for each selected asset. The existing builder
computes eight offline scalar words once and builds QROM from those words;
the existing independent checker separately derives the words and actual
recipe. Therefore no additional asset-dependent CMUL, second table, selector
correction or lookup normalization follows from these five swaps. Charge
offline construction and every actual loading/control/selector/preparation/
comparison/inverse gate exactly as the fixed component already requires.
Semantic canonicalization itself belongs to setup and guarded execution;
there is no free full-native-domain data oracle or full-source savings claim.

## Exact review disposition

Static semantic sharing is justified for this exact two-closure component,
under unchanged native72/F40 semantics, original clamps/labels/bindings,
the stated mul-only signature, preserved eager/support guards and fixed eight
knots. This permits consideration of one separate V5 preregistration with
the same2608component check families and unchanged180CPU/150admission/600wall.
It is not an execution release or a scientific PASS. All previous failed
sources/receipts and the diagnostic's structural-inequality result remain
immutable. Whole-source cost equality, general access, financialG2,99percent
delivery, adoption, quantum advantage and new fixture/replay credit remain
unproved/false.
