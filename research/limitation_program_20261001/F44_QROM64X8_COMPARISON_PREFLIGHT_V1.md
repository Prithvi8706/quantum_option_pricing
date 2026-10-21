# Standalone F44 QROM64×8 comparison, version 1

This is an author-only, unexecuted comparison of two lookup components using the exact saved Stage C run003 table. ROOT separately freezes the three author files, publishes the component READY, prepares the protocol, and freezes that protocol before running the comparison. This authoring task creates no READY, protocol, result directory, gate array, replay, phase result, or resource measurement.

The original Stage C run003 manifest is `7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa`, with 34 self-excluded owned files, 851 frozen inputs, and 2,842 external runtime inputs. All 35 actual owned members remain exact. Its resource gate failed and its row remains `REJECTED`. This comparison grants no replacement, adoption, financial execution, G2 transfer, whole-caller cost transfer, credited gate replay, fixture credit, price sample, or advantage claim.

The new files are:

- `experiment_f44_qrom64x8_comparison_v1.py`
- `F44_QROM64X8_COMPARISON_PREFLIGHT_V1.md`
- `f44_qrom64x8_comparison_preflight_v1.json`

The proposed result route is `results/limitation_program_20261001/F44_QROM64X8_comparison_run001`; the separately ROOT-owned READY route is `.context/F44_QROM64X8_COMPARISON_ROOT_READY_run001.json`. Both must remain absent during authorship. No executed or frozen source is edited.

## Exact inputs and source derivation

The retained table is the complete 64×8 array of signed 72-bit integer words from Stage C's `primary90_literals.json`, SHA `9bfbeb64c13efe5268e610f9d6aac91f3a925bd3ab4d3a52522e9c75687fef04`. This includes 64 exact F44 centers and 448 already selected coefficients. No decimal refit, interval calculation, coefficient selection, or tolerance adjustment occurs. The 90-digit origin is metadata, not a new numerical certificate.

The original naive helper comes from `f44_cosine_stage_c_source.py`, SHA `6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74`. The new controller's narrow `lookup_naive` contains four fixed interface setup statements followed by the exact AST of that source's `helper_compute` QROM64x8 branch. During an authorized run, the controller compares those AST statements and every normalized baseline row with the actual saved Stage C QROM event. It does not import or execute the original builder.

The shared-prefix alternative is the exact text-derived `lookup_shared` definition from `research/controlled_source_completion/exact_lookup.py`, SHA `a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c`. Its entire function AST is retained, including constant-row factoring, zero-residual pruning, sibling switching, and cleanup. Under the pinned Python 3.12.4 default `ast.dump(node, include_attributes=False)` serialization, that function's SHA is `eaa7e9a6a9670be002eb5600b7a646d9308e287c5f886b89bb5a14e5c083dd45`. No external helper import, dynamic compilation, or `exec` occurs. An earlier A15 use supplies source provenance only; its proof or cost is not transferred to this comparison.

The actual row validator, complete native scheduling, and exact CCX phase functions are retained as text and exact AST from the independently authored, unexecuted fragment `.context/f44_stage_c_independent_gate_audit_author_fragment_v1.py`, SHA `55851031aeb748ca8e802caf8c51d8f113b0ed3846bf8bd66deca75e705f34b1`. The complete CCX macro assignment is bound to the same source. All other lookup construction and diagnostics are local to this new controller.

Unused large exact-oracle integers in the primary90 JSON are decoded as decimal strings with `parse_int=str`; they are not converted to integers or scientifically reused. Only the 512 selected, canonically spelled, at-most-23-character signed72 table integers are converted. The controller does not alter Python's integer-to-decimal conversion policy.

## Identical complete wrappers

Both standalone arrays use exactly 1,301 wires:

| Wires | Role | Entry and exit |
|---|---|---|
| 0–71 | Full72 external address | Arbitrary, preserved |
| 72–647 | Eight full72 external output words | Arbitrary dirty XOR targets |
| 648–719 | Full72 private address copy | Zero, restored zero |
| 720–1295 | Eight full72 private output words | Zero, restored zero |
| 1296–1300 | Five reusable clean prefix ancillas | Zero, restored zero |

Each array copies all 72 address bits, computes the lookup into the 576 private output bits, XOR-copies all 576 bits into the dirty external outputs, applies the literal inverse of the entire body, and uncopies all 72 address bits. Full argument copies, output copies, body inverse, and cleanup are paid in the gate and depth counts. The candidate does not bypass this wrapper by targeting external outputs directly.

The original saved QROM trace occurs once, at rows `[6698, 42230)`, with compute `[6770, 24176)`, copy `[24176, 24752)`, and inverse `[24752, 42158)`. These are immutable source metadata, not new measurements. The controller injectively maps the standalone ports to that event's actual external address/output banks and the first 653 original shared private wires. It checks every opcode, operand, zero-padding slot, row boundary, and argument-copy count against the saved full native array. Unused original caller wires are omitted only from this standalone normalization. No original caller qubit count or depth is reduced or transferred.

The native array cap is prospectively fixed at 65,536 rows per algorithm. Every build, replay, row comparison, and resource traversal has at least one budget guard per 128 native rows. Only canonical X/CX/CCX rows, distinct valid operands, zero unused operands, and a little-endian native int32 Nx4 payload are admitted. Both complete arrays are saved.

## Universal lookup identity and phase

The naive body computes one six-bit minterm at a time, builds its five-AND-prefix ladder, XOR-copies every set output literal bit, reverses the ladder, and restores complemented address bits. Exactly one minterm is active for each low-six-bit address.

For the shared body, let the factored constant row be `base = table[0]` and the residual row be `table[i] XOR base`. At a recursive prefix node a clean target evolves through `P*x`, `P*(1-x)`, `P*x`, and zero by CCX, CX, CX, and CCX. The two recursive children restore their own stack slots. Pruning an all-zero residual subtree changes no output. The high-address branch, complemented high bit, low-address branch, and restored high bit cover every six-bit address exactly once. Consequently constant-row XOR followed by the selected residual XOR yields the exact retained row.

Neither body reads the upper 66 address bits. The wrapper preserves all 72 address bits and implements the same `address mod64` selection for every full72 address. Negative signed table words are reduced modulo `2^72` only for output bit extraction; the retained signed integers remain unchanged.

The bodies target only their private output words. The output copies implement an affine XOR translation for every arbitrary 576-bit external dirty output. Literal body inverse and argument uncopy restore all 653 private bits. This proves full dirty-output universality beyond the two diagnostic dirty patterns.

Only exact X, CX, and CCX permutations are used. The fixed 15-event, 7-T, 6-CX, 2-H CCX expansion is prospectively verified over all eight basis columns in the integer cyclotomic ring with `zeta8^4 = -1`. Two H events contribute a common denominator of two; the surviving column must have numerator positive two. Thus no relative or unknown global phase is accepted. This phase check is an operator proof, with zero fixture credit. The universal computational-basis identity extends linearly to coherent inputs.

## Fixed diagnostics and cost comparison

For each algorithm, the main cohort contains all 64 low-six-bit addresses and two dirty patterns: all eight output words zero, and all eight output words all ones. These are exactly 128 cases. A second four-case cohort combines low addresses 0 and 63 with one high address bit at 6 or 71 and all eight output words all ones. Its oracle remains the retained row selected by `address mod64`.

Each cohort receives one complete forward sweep and one complete inverse sweep. Every forward case compares all 1,301 wires, including every high input bit and every zero private bit; every inverse case recovers its entire initial allocated state. There are exactly 132 forward and 132 inverse logical calls per algorithm, 528 logical calls in total, and eight physical bit-cohort sweeps with lane counts 128 and 4. No sample, seed, new address, dirty pattern, fallback, corpus expansion, or parameter retuning is authorized after an outcome.

The resource report consumes every actual row of each complete saved standalone array. It reports source X/CX/CCX counts; exact 7-T count; Clifford CX and H counts; and complete chronological all-to-all ASAP T depth and Clifford+T depth. Every macro event synchronizes touched wire clocks; only T/Tdg increments the T clock, while every event increments the Clifford+T clock. The shared-minus-naive report covers all resource fields, including the identical full wrapper allocation. A particular cost direction is not required to pass the comparison. No whole-caller schedule, capped depth, financial resource gate, or Stage C acceptance is inferred.

The normalized baseline's source counts, T count, T depth, and Clifford+T depth must also exactly reconstruct the one QROM64x8 forward-event entry in the already saved `actual_prototype_resources.json`. That check consumes the complete original helper event, including its copies and inverse; it does not substitute an isolated body or transfer an event depth to the whole caller.

## Admission, runtime, and failure boundaries

The controller inherits isolated standard-library metadata operations from the unexecuted E12 independent auditor, while adapting caps, full Stage C map admission, and lookup-specific release fields. It requires the exact Python 3.12.4 launcher, base interpreter, `-I -S -B`, exact standard-library search path, absent interpreter ZIP, and a confined ROOT working directory. No site startup, scientific package, producer source, or historical helper module is imported.

The complete 34/851/2842 primary maps are directly admitted from the externally pinned Stage C manifest with their original expected SHAs. All 35 original owned files retain exact membership and bytes. The current standard-library runtime must equal all 2,842 original external expected members plus the original pinned launcher. Current runtime inventory, loaded module origins, present cache SHAs, declared absent caches, and selected original cache/runtime-absence metadata are checked in each full union. Historical nested manifests are opaque admitted inputs; they do not recursively promote additional runtime dependencies.

The directly admitted ROOT freeze of the original failed run001 also retains its exact 13-member, 11,426,616-byte inventory and original expected map. These partial scientific files remain opaque and unapproved, with no old manifest read or reuse. The admitted V2 prefit-failure witness retains the actual absence of its run002 output route. Both failure-history relations are rechecked in each union alongside the original declared cache contracts.

Two full fresh unions in the scientific run independently resolve and read all admitted expected inputs, the entire current runtime, and the externally frozen protocol. No hash cache, membership-only substitute, changed expectation, self-observed replacement, or waiver is used. Preparation likewise performs full initial and terminal verification, and performs no lookup emission, replay, phase proof, or cost calculation.

The fixed limits are 180 process CPU seconds, 150 admission/work CPU seconds, and 600 wall seconds. They include import/startup age, admission, complete hashing, arrays, proofs, diagnostics, cost, outputs, and terminal checks. ROOT executes `prepare` and `run` as separately released phases; the prepared protocol's SHA is mandatory for the run.

The inherited bounds remain 100,000 references, 8 GiB unique input bytes, and 24 GiB cumulative read/hash work. Current runtime is limited to 4,096 files and 512 MiB. The new release is limited to 16 files and 8 MiB. New owned retention is limited to 16 files and 16 MiB inclusive of the self-excluded manifest; prospective owned single files are limited to 64 MiB. Inherited input reads retain Stage C's 128 MiB individual cap because two already admitted source inputs are 70,830,265 bytes. Their original expected hashes are retained unchanged.

The complete packet has exactly 14 nonmanifest members and one manifest: protocol, run-start metadata, retained table, two native arrays, array descriptors, actual source binding, universal lookup proof, exact CCX phase proof, two diagnostic reports, resource comparison, summary, verification, and manifest. Actual inclusive inventory and encoded UTF-8 bytes are checked before and after sealing. Sealing reserves one additional member and 4,096 bytes for a fixed failure marker. A failed or censored attempt is authoritative and remains unsealed; no partial artifact grants scientific approval, no route is reused, and no fallback algorithm or budget expansion is available. ROOT owns all releases and actual tests.
