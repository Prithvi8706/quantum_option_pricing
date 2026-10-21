# A13 exact metadata-membership index: finite QA preregistration

This new check is limited to the existential path/hash predicate used by V5
`selected_inputs`. The sealed profile manifest is
`44ab18466e03906e05f6b370aaf7a6791ccfeda811ea7d32870b4a05e66a195f`.
Its selected scan used 3.71875 CPU / 4.062 wall seconds and 5275 comparisons.
Those are historical diagnostic observations under checked adapters and profiling
overhead, not a matched performance comparator or complete `source_packet` cost.

The candidate retains the full ordered snapshot and every duplicate position. It
indexes the exact pair `(verified_input_path, original_expected_sha256)` without
normalization, case folding, hash replacement, or collapsing full records. It
performs no binding, hashing, path resolution, archive selection, inventory or
header admission. All such existing obligations remain with the unchanged caller.

Conditional proof: for a finite fixed sequence of complete records with typed
string membership fields, the index entry for `(p,h)` consists exactly of all
positions whose two fields equal `(p,h)`. Induction on append establishes this
invariant, including duplicate records and one path with multiple hashes. Its
entry is nonempty exactly when the original existential predicate holds. This is
a proof of that predicate transformation on a verified snapshot, not a proof of
receipt validity. Malformed records and changing snapshots lie outside the
equivalence contract. The module rejects incomplete or incorrectly typed rows
and copies read-only row dictionaries; current historical rows contain only
primitive metadata. A future integration must construct the index only after
the complete unchanged owner admission and retain all rows in its authorization.

Before execution, a static reviewer freezes exactly the four new source/preflight
files plus the pinned V5 author and the sealed profile manifest in a fresh
`a13-membership-index-finite-qa-frozen-v1` JSON. This check reads only those six
pinned files and the freeze record. It does not admit or interpret the profile's
full maps, recover old proofs, or claim complete interpreter provenance. The
launcher/version information is recorded; the empty external runtime map makes
no historical runtime assertion. The pinned V5 file is parsed and only the exact
single `any(...)` expression in `selected_inputs` is compiled. No historical
module or scientific definition is executed.

Fixed corpus: every sequence of length 0 through 4 over eight atoms: matching
path, same path/other hash, another path, case mismatch, strict path prefix,
backslash spelling, archive-looking path, external-looking path. Twelve ROOT
relative path/hash queries cover positives and negatives. This fixes 4681
corpora, 56172 original/indexed/oracle predicate comparisons, 4681 full-record
retention checks and 56172 exact witness-position checks. The separate oracle
enumerates all positions. Four invalid-input rejections and three snapshot
guards are operational contract checks, not equivalence claims for malformed
input. There is no adaptive corpus, real owner traversal or membership adoption.

The fresh receipt is
`results/limitation_program_20261001/A13_continuation_20261004_membership_QA_run001`.
One execution only. Hard caps: 25 process CPU seconds, 20 CPU admission seconds,
90 wall seconds, selected work 15 CPU / 65 wall, 12 terminal owned files / 1 MiB.
The process clock starts at controller load. Budgets include extraction, candidate
import, checks, hashing and retention. A terminal fresh actual-byte check covers
all six prospective pins. The manifest excludes its own hash and the temporary
failure marker. Failure preserves `FAILED_UNSEALED.json`; no retries or budget
increases are authorized. Passed finite QA requires exact counts and all checks.

CLI: `.context/frontier_t0_env/Scripts/python.exe -B
research/limitation_program_20261001/continuation_20261004/A13/membership_index_finite_qa_v1.py
--freeze <reviewer-frozen-json>`.

Passing this diagnostic authorizes only the finite predicate equivalence result.
It authorizes no V6 integration, all20 run, scientific row, fixture/replay/sample
credit, source emission, G2, adoption, performance claim or quantum advantage.
The V5 failure and all 18 partial rows remain failed/unapproved. Next obligations
are a separate full metadata controller profile with retained reference duties
and a budget feasibility assessment of remaining mathematics before an all20
scientific preregistration can be considered. No Stage C timing is performed.
