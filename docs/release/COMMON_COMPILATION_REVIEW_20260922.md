# Independent AI review of PR #9

Date: 2026-09-22. Reviewer: separate `pr_review` AI agent, not the author of the
compiler producer, manuscript, plotting code or acquired results. This reviewer
authored only this report and the independent receipt checker. This is an
integration and scientific-claim review, not human expert approval, an exhaustive
new literature review, formal circuit verification or submission endorsement.

## Reviewed change and disposition

Reviewed [PR #9](https://github.com/Prithvi8706/quantum_option_pricing/pull/9),
head **`72470e1b94a5e24a1646a85f8f950207b9771329`**, against main
**`257b2359aabe0976cddc8a7b41daeb181bc434cf`**. The reviewer independently queried
the remote PR metadata, changed-file list and checks, inspected the new source,
tests, acquisition receipts, tables, figures, final manuscript and documentation
diff. At inspection the PR was open, draft and mergeable, with `dev` as head.

**Disposition: no unresolved actionable blocker to merging this scoped change.**
Preserve the source/acquisition commits with a normal merge; do not squash them.
This report authorizes no external publication or contact. The actual merge
commit is subsequently recorded by GitHub; this report does not claim that a
merge had already occurred when the review was written. A final metadata-only
commit may add this report and verification receipt without changing the
reviewed implementation, evidence or manuscript. The reviewer also inspected
the subsequent README/checklist cleanup before its commit: it replaces stale
Week 16 and batch-plan descriptions with draft-complete/human-gates-open status
and adds the new source/artifact directories to the map. No code, experiment,
manuscript or scientific conclusion changes in that cleanup.

The independent finding is restricted: under the second explicit ideal U/CX
policy, reflection remains lower-CX in D1 and residual arithmetic remains
lower-CX in D2. D2 reflection/residual ratios are 3.1289554633 with control
cancellation and 3.4731856745 with fully controlled preparation/inverse. The
103 versus 5,162 allocated-qubit tradeoff remains material. No best-in-class,
hardware-runtime or quantum-over-classical conclusion follows.

## Materials and independent checks

- Read the earlier bounded follow-up plan, frozen protocol, producer and common
  compiler, historical walk/readout and controlled-zero implementations,
  arithmetic component interfaces, and label-conversion adapter.
- Inspected the common controlled-U template, preservation of controlled block
  global phases, inverse counts, Grover minus phase, control cancellation,
  clean v-chain workspace, full inverse-QFT swaps and Hadamards, and arithmetic
  X/CX/CCX translation. The declared identity padding is explicit and uniformly
  charged; it is not an optimization claim.
- Independently executed the original 13 small compiler tests: **13 passed**.
  These exercise full small matrices including nonzero global phase, inverse
  and control-cancellation equivalence, clean zero reflection and composition.
  After the JSON guard correction, inspected the new numeric-drift regression
  and final archived JUnit: **33 tests, zero errors/failures/skips**, including
  14 compiler/guard and 19 existing label/decoder tests. The 13 independently
  executed tests overlap those 33 and are not added to them.
- Wrote and ran a [separate receipt checker](reviews/common_compilation_20260922/check_receipt.py)
  with **no project-producer imports**. Its
  [receipt](reviews/common_compilation_20260922/independent_receipt.json)
  verifies 224 exact acquired-source/input/output byte-hash bindings and
  committed source text correspondence, all six
  component compositions, all twelve complete AE ledgers, inverses, widths,
  serial-depth arithmetic, historical deltas, winners and exact ratios.
  An independently constructed rational Machin enclosure for pi establishes
  positive error-budget margins for all six unchanged schedules after adding
  the archived certified label-conversion bound. It does not independently
  reimplement directed trigonometry or certify numerical native gates.
  Git text correspondence normalizes CRLF to LF on both sides, consistently
  with the frozen producer, because legacy text attributes permit checkout
  line-ending conversion. This normalization is confined to Git-text comparison;
  recorded acquisition hashes still bind the exact raw working-tree bytes.
  It does not mean that every recorded source hash equals its Git blob hash.
- The receipt's execution HEAD is the acquisition freeze
  `568b9997e4b47ae5cbded936ee51b39b3fe5d283`; the final reviewed PR above contains
  those same source/evidence bytes plus the completed manuscript/documentation.
- Inspected all three PNG figures visually, both table families, manuscript
  equations and newly completed Section 7.3. The six new CX/width/M entries,
  ratios, 3,968-label total and reflection cost reconciliation agree with the
  archived evidence. Generated figures are readable and distinguish historical
  menus from the new six-route comparison. Plot source/hash manifests were
  inspected; the coordinator separately performed byte-identical artifact
  regeneration. The reviewer did not repeat full production gate re-emission.
- Inspected final README, checklist, project-log and closeout diffs. Historical
  source/evidence paths are not modified by this PR. Current readiness statements
  keep human, physical, confirmation and submission gates open.

Reproduce the independent reconstruction from repository root into a new file:

```powershell
.context/week15_env_v1/Scripts/python.exe docs/release/reviews/common_compilation_20260922/check_receipt.py results/journal_sprint/common_compilation_20260922_v2 .context/new_independent_common_receipt.json
```

## Findings, corrections and limitations

| Finding | Disposition |
| --- | --- |
| Source-only rechecking could miss input changes during acquisition. | Reviewer requested end-of-run input hashing; author added it before acquisition freeze. Completed v2 checks every recorded input and source. |
| Compiler version and offline classical work needed an explicit treatment. | Author pinned Terra 0.46.3 before acquisition, recorded offset operations, and identified reused phase synthesis as offline work rather than a zero-cost runtime claim. |
| First acquisition mistook tuples versus JSON lists for model drift. | Retained v1 failure occurred before any six-oracle row. The canonical-JSON correction preserves exact numeric comparison; the new regression rejects changed values. A separate source freeze and v2 archive preserve provenance. |
| Native floating-point transpiler arithmetic is not newly certified by gate-count identities. | Protocol, abstract, Section 7.3 and conclusion explicitly restrict the count model to ideal decompositions; no executable-native price guarantee is claimed. This remains a limitation, not a closed physical-delivery gate. |
| Historical depth conventions were not comparable. | New U+CX serial-schedule upper bounds use one convention. Manuscript correctly avoids optimized DAG-depth, spacetime or runtime superiority. |
| Manuscript initially had malformed inline math delimiters. | Author corrected delimiters and currency escaping; final inspected text uses GitHub-compatible math. |
| Raw-parent and historical best-raw configurations could be confused. | Tables, captions and text explicitly distinguish the matched w48/f24 parents from lower-width historical minima. |
| Restrictive compiler policy could be mistaken for global compiler robustness. | Text limits the finding to two explicit policies and six selected implementations; stronger arithmetic or a different compiler can change rankings. |
| Two development cases cannot establish general prevalence or new priority. | Manuscript keeps the comparator-case-study framing and credits established residual estimation, signed shifting, QSP, arithmetic and workspace methods. Human significance review remains outstanding. |

Both attempts together used 395.421875 process CPU seconds; the successful
attempt's sampled peak RSS was 185,151,488 bytes. These are comfortably within
the declared limits. They describe acquisition work, not quantum execution.
All six v2 rows completed; no unfavorable route was dropped and no schedule
was retuned after seeing a resource outcome. Clifford+T synthesis is correctly
reported as unavailable without a shared certified synthesis allowance.

## PR checks and scope boundary

The actual GitHub check **“Macroscope - Correctness Check” was SKIPPING** at the
reviewed head. It did not supply a passing correctness review and is not counted
as one. The independent AI review above is separate. The fresh targeted tests
and source/evidence reconstruction are the stated validation, not a claim of
passing unavailable CI or of a fresh full integrated test run.

No independent human researcher participated in this review. Scientific
significance, author accountability, license/release clearance, venue choice
and submission approval remain open. Physical error, optimized depth/runtime,
matched classical crossover and quantum advantage remain unestablished.
