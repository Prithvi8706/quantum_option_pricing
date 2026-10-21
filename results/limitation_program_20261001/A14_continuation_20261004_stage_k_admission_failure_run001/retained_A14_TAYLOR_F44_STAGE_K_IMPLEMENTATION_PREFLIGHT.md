# Fixed F44 Stage K arithmetic realization

Status: author draft, unexecuted and pending root freeze. This release describes one fresh signed52-by-signed38 multiplier and one signed ties-to-even f44-to-f40 rounder. It is Stage K only. There is no cosine coefficient generation, financial evaluation, source replacement, resource-improvement claim, candidate selection, Stage C approval or fixture credit.

The held F44 prospectus is bound byte-exact at Markdown `e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04` and JSON `526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3`. Complete actual original A14 source and independent audit003 maps and owned inventories are strict prerequisites. Both original rejected rows remain rejected. Their prior failure and diagnostic bytes stay expected inputs; no observed hash becomes an expected replacement.

The new builder is `taylor_f44_stage_k_source.py` and controller is `experiment_taylor_f44_stage_k.py`. Root must freeze both sources, this document and the implementation JSON, then issue a distinct `research/limitation_program_20261001/continuation_20261004/A14/PRODUCER_ROOT_READY_run001.json` with those four hashes, current existing new-code cache hashes, exact original packet hashes, fixed clocks and argv. A self-declared READY is not admitted. The exact future CLI is the pinned venv Python `-B -m research.limitation_program_20261001.continuation_20261004.A14.experiment_taylor_f44_stage_k --ready-sha256 ROOT_ISSUED_EXPECTED_SHA256`. The fresh receipt is `A14_continuation_20261004_stage_k_producer_run001`; no retry or overwrite is authorized.

The producer independently checks source/gate recurrence correspondence, records every allocated wire, and performs the fixed native diagnostics. A separately authored scientific auditor must inspect the actual binary rows with its own interpreter, structural recurrence, references and resources before Stage C can be released. This producer's successful packet cannot stand in for that auditor or root integrity. The auditor code and actual passed packet pins are presently unresolved; Stage C remains explicitly false.

## One signed multiplier

Input banks are full72 words at wires0..71 and72..143; the arbitrary dirty output is144..215. The ordered contract requires each input's high wires to equal its active sign bit, with active widths52 and38. The output XOR is `floor(signed(a)*signed(b)/2^44) mod2^72`. Out-of-contract words receive no generic full72 multiplication claim.

Use the complete 52-by-38 signed bit plane. A term is negative exactly when one operand index is its active sign position and the other is not. Compute a positive term with CCX into a fresh zero wire; compute a negative term as its complement using X then CCX. For each negative weight, add the fixed correction `-2^(i+j)` modulo2^116. The exact closed correction is `-(2^89-2^51-2^37) mod2^116`. There is no truncation at the active90-bit signed product boundary or the40/44 fractional boundary. The two minima produce positive2^88, requiring90 signed bits; the modulo116 representation preserves the correct high sign extension.

Reduce columns using one deterministic retained CSA schedule: consecutive triples in each column create fresh sum and, except at the modulus boundary, carry wires. The sum is `x XOR y XOR z`; carry is `xy XOR((x XOR y)z)`, whose terms are disjoint. All original and history wires remain until reverse. Unconsumed columns pass unchanged. Stop only when every column has at most two terms, copy them to two full116 rows and add with a fresh explicit116-bit ripple network. Retain all propagate and117 carry wires. Every low column participates before copying product bits44..115 to the dirty full72 output. Append the literal complete compute rows in reverse order. The primitive is one fixed CSA/ripple realization; no BK comparison, alternative multiplier or cost search is performed.

The structural consumer reconstructs allocations and the bit-plane/CSA/ripple recurrences independently of the builder functions and consumes every actual native row. It checks exact ports, constant correction, all layer metadata, all result banks, copy window and literal inverse. The universal arithmetic proof is distinct from the finite corpus: signed bit-plane identity, CSA/ripple invariants and `floor((xy+k*2^116)/2^44)=floor(xy/2^44)+k*2^72` establish the promised whole-input clean-XOR map. Compute never reads dirty output; input preservation and inverse restoration hold for superpositions in the contract subspace.

## One signed rounder and actual Boolean prefix

The rounder uses a full72 input and a full72 arbitrary dirty output. It copies arithmetic `z>>4`, including high sign extension, into a full72 quotient bank and copies the four remainder bits. Its three retained OR histories compute `r0 OR r1 OR r2 OR q0`; CCX with r3 produces the increment. The exact predicate is `r3 AND(r0 OR r1 OR r2 OR q0)`, equivalent to `r>8 OR(r=8 AND q odd)`. Negative words use floor quotient and Euclidean remainder; adding8 and shifting is not substituted.

A retained72-bit increment ripple computes quotient plus the increment into a fresh full72 result, preserving73 carry wires. Copy that result to the dirty output, then append literal reverse of all quotient/remainder/OR/increment/carry/result work. This rounder is universal for every signed72 input: quotient magnitude is at most2^67, so the possible +1 fits signed72. The structural consumer checks all banks, actual predicate boundary, every native row,72 output copies and complete inverse.

The fixed corpus is the prospectus's eight ordered multiplier pairs, each with dirty words0 and2^72-1 (16 cases); four signed quotient values times five remainders times those dirty words (40 cases); and all16 remainders times two quotient parities (32 Boolean-prefix cases). The last32 replay the actual emitted quotient/remainder/predicate compute prefix, compare its complete allocated wire state (including zero unused result/carry/output banks), then replay that prefix literally backwards and compare every wire to the original. They do not merely evaluate a Python Boolean expression. The56 full primitive cases test forward, inverse from the same initial state, and forward followed by inverse, giving168 actual full-leaf replays; the32 prefix cases give64 prefix replays. These are88 fixed diagnostics with zero newly credited fixtures. They are not the universal arithmetic or phase proof.

## Absolute phase and actual resources

Native storage is little-endian signed int32 raw Nx4 rows with opcode1 X,2 CX,3 CCX. Unused operand positions are zero; used operands are distinct and in range. The two raw binary files contain every row and have exact16-bytes-per-row size and their own SHA256 values.

Each CCX lowers with the fixed15-event exact7T sequence: H(target), CX(b,target), TD(target), CX(a,target), T(target), CX(b,target), TD(target), CX(a,target), T(b), T(target), H(target), CX(a,b), T(a), TD(b), CX(a,b). Its parity polynomial is `a+b+c-(a XOR b)-(a XOR c)-(b XOR c)+(a XOR b XOR c)=4abc`, giving absolute CCZ with no global phase offset; target H conjugation gives exact CCX. X/CX are exact real permutations. All gates are recognized and every inverse row is present; no relative-phase replacement is allowed.

Resources are counted from the complete new native arrays and full macro chronology: X/CX/CCX counts,7T per CCX, actual all-to-all ASAP T/Clifford+T depths, six CX and two H per CCX, and all allocated qubits. No old F40/product112 gate file or multiplier resource estimate is borrowed. Full primitive port banks and private histories are counted. Caller argument-copy costs belong to later source insertion and are explicitly outside the standalone leaf; Stage C must additionally pay `2*arity*72` inner copies and the full outer/clean/global inverse construction from the prospectus.

## Admission, bounded work and terminal integrity

One process has180 CPU/150 admission/600 creation-wall seconds, including imports, complete byte admission, runtime enumeration, generation, structural proofs, macro counts, all88 diagnostics, serialization, copies and terminal hashing. There is no JIT, scientific package, SDK, optional backend or numerical precision evaluation. The actual pruned standard library/DLLs, launcher, venv scripts/adjacent files, existing new-code caches and every loaded source/cache origin are frozen before the new builder is loaded. Base `Lib/site-packages` is excluded and denied by lexical/resolved paths. Runtime caps are24,000 files/2GiB; bookkeeping caps100,000 references/8GiB unique input/24GiB actual hash work. The two primitives together may emit at most1,000,000 native rows. New ownership is at most64 files/128MiB.

Actual hash reuse is invocation-local and requires unchanged full stat/reparse identity; expected values never seed an actual-byte cache. Two complete uncached input unions freshly resolve every saved lexical alias and unique actual path, rehash full bytes and check all original inventories and current runtime membership. The first occurs before work and the second before terminal sealing. Every emitted native file is separately hashed and included in the strict owned manifest. Own summaries/outcomes are exclusive; any error/censor leaves authoritative FAILED_UNSEALED and invalidates partial success, without overwriting old material. No budget fit or cost advantage is promised by authoring this recipe.

Artifacts are copied exact author/method/READY bytes, run_started, primitive_descriptors, two native binaries, native_gate_arrays, universal_structural_certificate, primitive_resources, fixed_diagnostics, summary, completion_outcome and self-excluded manifest. Producer PASS means these fixed arithmetic diagnostics and array-matched proof were retained under guards. It requires a later actual independent auditor and root fresh integrity before any Stage C release; cosine, changed-source, financial/G2, adoption and advantage flags stay false.


## Scoped continuation release, 4 October 2026

All new sources and ROOT releases are in
`research/limitation_program_20261001/continuation_20261004/A14/`; all handoffs are
in the matching docs namespace. Old author files, completed receipts, maps and
expected SHA values are read-only. The builder is an exact held-byte copy.
The controller changes only routing, namespace import admission and the owned
file-count guard to reserve one file for the self-excluded manifest. The saved
AST comparison binds all arithmetic, structural, fixed-corpus, phase and resource
functions without change. READY is `PRODUCER_ROOT_READY_run001.json` in the
scoped research directory; the original .context READY is neither created nor used.

The exact CLI is pinned Python with `-B -m
research.limitation_program_20261001.continuation_20261004.A14.experiment_taylor_f44_stage_k
--ready-sha256 ROOT_ISSUED_EXPECTED_SHA256`. ROOT reviews and freezes the actual
four scoped author/method files before issuance. The corpus stays exactly
16 multiplier,40 signed-rounder,32 actual Boolean-prefix diagnostics (88 total).
Acceptance is complete actual-array structure, whole-wire forward/inverse replay,
native absolute phase proof and paid primitive resources within180CPU/150admission/
600wall,1000000rows,64owned files/128MiB, including full prior input maps/current
runtime/two fresh uncached unions. Failure is retained as failure; no retry, new
variant, budget increase or partial-credit promotion. Launch stdout/stderr is
retained outside the scientifically owned receipt in this research namespace.

The independently authored checker has separate source and release. Its actual
sealed PASS plus separate ROOT fresh integrity remain required before any Stage C
release. Stage C is false in every Stage K artifact. All448 F44 literals, cosine
uniform envelope, eager caller ranges, total-map gates, source binding, complete
costs, financialG2, estimator99percent delivery and physical advantage remain open.
