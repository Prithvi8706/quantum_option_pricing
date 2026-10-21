# Signed-square integration review

This independent development review checks that the exact square circuit is
substituted only for multiplication whose two arguments identify the same
SSA value. Equal values in a sample are insufficient. The original two native
input registers, full output word, argument copies, storage masks and fallback
leaf bytes remain part of the implementation contract.

## Evidence already obtained

The real accepted A11 B4×12 and B8×52 archives both loaded successfully into
the square library. Every existing unsigned 46-bit square-root contract was
revalidated at its actual site, and the existing signed seven-bit logarithm
contracts remained present. These are two successful pytest cases in the
development JUnit file `.context/square_integration_candidate.xml`.

An additional local 72-bit/f40 integration check passed for signed endpoints,
including the minimum signed word, maximum signed word and minus one. It
verified arbitrary high-bit output XOR words, aliased output names, complete
input/workspace restoration, unsigned square-root input bit 45, unchanged
accepted square-root metadata/gate bytes, and reloading the new square archive.
The temporary gate files were removed by Python's temporary-directory context;
the development result is `.context/square_production_local_check.json`.

The leaf algebra is consistent with signed multiplication. Diagonals have
positive weight even for the sign bit. Off-diagonal terms have their doubled
weight at column i+j+1 and are negative only when one factor is the sign bit.
Complementing each negative partial bit and adding its fixed negative weight
correction reproduces the product modulo 2^(w+f). The implementation retains
low columns until final carry propagation, copies the desired shifted product
bits to the arbitrary output word, and reverses all computation. The second
native input register is untouched by the leaf and remains copied by the source.

## Fixes required before acceptance

The first full integration run exposed an inherited constructor restriction:
the square library inherits the square-root default `active_bits=46`, which
rejects a valid six-bit square-only graph. Its own constructor now passes
`min(46, target['width'])` to the inherited range machinery. This does not change
the square dispatch or any 72-bit financial target.

The square-entry detector initially returned false for a non-dictionary
`spec` before examining the outer `same_ssa_arguments` contract. That can skip
specialized validation in the reader. Outer promises now trigger validation
even when their specification is malformed. The new reader also needs this
protection for the inherited `unsigned_input_bits` contract, without editing
the already frozen square-root modules. Malformed specifications now cause
an explicit ValueError.

Finally, a square-only external source must undergo the typed, ordered, unique
SSA validation before proving argument identity. The existing conservative
storage-mask pass does not provide that validation. A source containing signed
logarithm or narrowed square-root promises already receives stronger graph
validation; the square-only source now receives it explicitly before storage-mask analysis.

All three findings were sent to the implementation owner before protocol freeze.
The development first run ended with two passed cases and 44 setup errors from
the constructor issue. It is not an acceptance receipt or an arithmetic
counterexample. Three additional typed-SSA negative controls were added after
that run, giving 49 collected cases for the final suite.

## Final verification

The final implementation passed all 49 cases in
`research/limitation_program_20261001/test_square_integration.py`. These include
all 64 small signed words, distinct SSA inputs with equal and unequal sampled
values, signed literal lookup rows, full native register/copy accounting,
fresh cache and archive reloads, hidden/missing/false promises, malformed specs,
register/resource/SHA corruption, target/table mutations, schedule fingerprints,
and boolean identifiers, duplicate outputs and forward SSA references.

The guard-test graphs use enough workspace for either native leaf family; the
prospective full financial experiment separately enforces the unchanged A11
B4/B8 qubit caps. Passing these checks establishes exact digital integration.
It does not establish continuous-dollar error, estimator confidence,
matched classical performance or physical quantum advantage.

Current verdict: all three findings were fixed before the full-source protocol
was frozen. The final development run passed 49 cases in 16.66 seconds. The
prospective source run then passed the same frozen 49 cases in 14.50 seconds;
Ruff passed. Its [archived JUnit evidence](../../results/limitation_program_20261001/A10_square_run001/integration_tests.xml)
and [executed snapshots](../../results/limitation_program_20261001/A10_square_run001/protocol.json)
record the accepted test implementation and exact code hashes.

The complete-source resource screen produced 1.7812% / 1.5820% T-depth gains,
below the frozen 2% threshold in both cases. No new full financial circuit
replay was run, as the prospective stop rule required; the A11 baseline stays
accepted. The exact square leaf and measured candidate remain preserved for
separate work/space assessment. This is exact integration evidence, not a
continuous-price or physical quantum advantage certificate.
