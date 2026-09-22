# Common-policy comparison and manuscript closeout

Date: 2026-09-22. Scope: the six fixed D1/D2 oracles, a focused manuscript draft,
and evidence-derived tables and figures. This is deterministic logical-resource
analysis of development cases, not fresh confirmation or physical execution.

## Finding

The case-dependent CX ordering survives the declared common compiler policy.
Reflection remains lowest-CX in D1; signed-residual arithmetic remains lowest-CX
in D2 among the three selected routes per case. D2 reflection/residual ratios
are **3.1289554633** with control cancellation and **3.4731856745** with fully
controlled A/A-inverse. The historical ratios were 2.9346016409 and 3.2891600107;
the changed projections demonstrate compiler-policy sensitivity, not new data
about quantum execution speed.

| Case / route | AE size M | Allocated qubits | Common controlled CX | Common control-cancelled CX |
| --- | ---: | ---: | ---: | ---: |
| D1 reflection | 128 | 55 | 345,327,182,288 | 36,477,214,772 |
| D1 exact raw parent | 1,024 | 2,754 | 5,638,322,087,193 | 658,467,218,787 |
| D1 residual | 128 | 4,733 | 893,953,445,821 | 104,719,289,723 |
| D2 reflection | 512 | 103 | 11,146,299,105,743 | 1,174,336,099,955 |
| D2 exact raw parent | 2,048 | 3,191 | 22,636,125,188,209 | 2,643,233,541,099 |
| D2 residual | 256 | 5,162 | 3,209,243,659,974 | 375,312,500,844 |

The raw parents are specifically `D1_28` and `D2_28`, w48/f24, degree eight,
range reduction one. They match the selected residual construction's parent;
they are not the lowest-CX raw rows in the historical full menu. This follow-up
does not search or claim optimality over other compiler policies or oracles.

The paper's defensible contribution remains an auditable comparator case study:
matching classical control and normalization can change the preferred quantum
implementation, and the gate/width tradeoff must be reported. The result does
not establish a new residual-estimation principle, universal encoding rule,
publication-level originality, or quantum-over-classical advantage.

## Policy and numerical scope

The [frozen protocol](COMMON_COMPILATION_PROTOCOL_20260922.md) uses Terra 0.46.3,
U/CX basis translation at optimization level zero, fixed controlled-U/CCX
templates, global-phase accounting, full IQFT, inverse and clean-workspace
costs. All six routes use the same rules. Arithmetic component records were
re-emitted and compared against the complete archived records. Reflection
blocks were compiled under the new policy instead of importing old optimized
block counts. No nominal configuration or AE size was retuned.

The controlled-U template deliberately retains one identity U, and a phase U
is retained even for zero phase. These are declared circuit-policy choices,
not claims of optimal compilation. The only nonlocal rewrite is the exact
control-cancellation identity used in the second ledger.

All six original schedules remain feasible after the canonical-label conversion
allowance. Exact rational checks cover every label for the required AE sizes
128, 256, 512, 1,024 and 2,048. The financial target, cutoff four, ten Gaussian
bits per coordinate, one-dollar tolerance, at least 95% ideal confidence,
17 repetitions and call cap are inherited unchanged.

Counts refer to ideal exact decomposition identities. They do not supply a new
certificate for floating-point native transpiler parameter errors. `U+CX`
is an explicitly serial depth upper bound; optimized dependency depth,
spacetime, runtime and Clifford+T comparisons are not established. There is no
certified common rotation-synthesis allocation or physical-error allowance.
Historical certified offset work is recorded separately; phase preprocessing
is reused, not re-timed or made free in a runtime comparison.

## Provenance and bounded acquisition

- Initial policy/source freeze: `3c3a3e225caae535f093100d600564cbdad7e0c1`.
- [Retained v1 failure](../../results/journal_sprint/common_compilation_20260922_v1/failed.json):
  the first parent-plan guard compared Python tuples with serialized JSON lists.
  Canonical JSON values agreed. The attempt produced no six-oracle rows.
- Corrected freeze: `568b9997e4b47ae5cbded936ee51b39b3fe5d283`, before retry.
  A regression test preserves rejection of numeric drift. No scientific menu,
  compilation rule or target changed in response to an observed ranking.
- [Complete v2 archive](../../results/journal_sprint/common_compilation_20260922_v2/results.json)
  and [completion receipt](../../results/journal_sprint/common_compilation_20260922_v2/complete.json):
  six rows, twelve AE ledgers, input/source hashes rechecked at completion.
- v2 used 380.8125 CPU seconds, 413.2307288 wall seconds, and sampled peak RSS
  185,151,488 bytes. Combined attempts used 395.421875 CPU seconds, below the
  two-hour allowance; the memory cap was 16 GiB. These are acquisition costs,
  not quantum pricing runtime estimates.

Frozen historical producers and archives are preserved. The new archive is
separate and neither supersedes their bytes nor relabels development evidence
as confirmation.

## Deliverables and checks

The [complete manuscript draft](../../manuscript/2026-09-22/main.md) supplies the
financial model, restricted mathematical construction, signed arithmetic and
error derivations, nearest-prior-art discussion, historical and new results,
limitations, evidence links and AI-use disclosure. Human authorship approval,
significance review, venue selection and submission remain open.

The [artifact guide](../../manuscript/2026-09-22/README.md) gives reproduction
commands. Three figures are supplied as PNG/SVG/PDF, with CSV/Markdown tables,
the complete historical 166-row data, new six-row costs, error allowances and
a claim/evidence map. Manifests bind source/input/output hashes. Both artifact
families regenerate byte-for-byte under the recorded plotting environment.

Fresh targeted validation: **33 passed** (14 compiler/guard tests and 19 existing
label/decoder tests), 17 legacy Qiskit warnings, no failures; see the
[JUnit receipt](../../results/journal_sprint/common_compilation_tests_20260922.xml).
Tests include full small controlled-unitary/global-phase checks, inverses,
clean workspace and control cancellation. Ruff passes. Historical 1,645/315
test receipts were not rerun or added to these counts.

The [independent AI review](COMMON_COMPILATION_REVIEW_20260922.md) records scope,
findings and disposition; it is not a human endorsement. The review uses a
separate reconstruction of all twelve ledger totals and rational feasibility,
in addition to source, manuscript and figure inspection.

Integration is tracked in [PR #9](https://github.com/Prithvi8706/quantum_option_pricing/pull/9),
with `dev` as head and `main` as base. Preserve all producer/acquisition commits
using a merge commit, without squashing or deleting `dev`. The PR's recorded
merge status and final review identify the actual reviewed and integrated SHAs.
