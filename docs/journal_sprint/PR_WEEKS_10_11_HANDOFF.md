# Integration PR: week 10 through week 11

This PR continues merged PR #1 (weeks 1-9 and Macroscope corrections). It contains
the week-10 numerical evidence gate, encoding/rescue/allocation investigations,
harder-pricing assessment and the completed week-11 classical benchmark foundation.
Week 12 remains a prospective design. No quantum advantage, new quantum algorithm,
independent human review or submission readiness is claimed.

## Included evidence

Complete local archives are included losslessly in
`results/journal_sprint/week10_11_evidence_v1.zip`, with a per-file SHA256/size index
in the accompanying JSON. They extract under `results/journal_sprint`:

- `week10_stress_v1`, `week10_stress_v2`, `week10_stress_v3`;
- `rescue_encoding_v2` and `rescue_pilot_cs_v1`;
- `encoding_decision_v1`, `encoding_decision_v2`, `allocation_v1`;
- `shortlist_v1`;
- `w11_baseline_pilot_v1`, `w11_references_v1`, `w11_main_v1`.

The incomplete `rescue_encoding_v1` first attempt is also retained, including its
failure record; it is not represented as a successful complete archive. Relevant
test XML and numerical verification reports accompany these archives. Historical
snapshot code is evidence, not additional current implementations to import.
Original completion manifests are not regenerated, and failed/superseded results
are not erased to improve the narrative.

Bundle extraction refuses existing archive destinations. In the originating
workspace they already exist, so do NOT extract over them; use a fresh checkout
or a new output root. The bundle keeps thousands of machine-generated evidence
files out of the primary source diff without withholding their contents.

Local environments, downloaded third-party papers, `.claude` files, unrelated
manuscript outputs and the separate older user plan are excluded. Older omitted
week-1-9 archives retain the status documented in [ARCHIVE_INPUTS.md](ARCHIVE_INPUTS.md).
The existing six-edit stash is preserved; no blind stash application or broad
cleanup is part of this PR.

Archive metadata retains benign producer platform/compiler paths, hardware and
scoped Git provenance needed to interpret the measurements. The environment
records' tracked patches are the research-document changes included in this PR,
not credentials or the contents of ignored/private directories. Credential-pattern
and excluded-file checks are performed before publishing; these are a bounded
audit, not a guarantee against every possible secret representation.

## Reproduction and source-byte conventions

The acquisition/replay platform is Windows, Python 3.9, NumPy 2.0.2, SciPy 1.13.1,
Terra 0.46.3, Aer 0.12.2 and Finance 0.4.0. Additional dependencies are recorded in
`research/journal_sprint/requirements-week11.txt`; do not mix the older root
`requirements-dev.txt` Qiskit pin into this environment. The fresh-install recipe
is a candidate; validation below distinguishes clean source from a new environment.

Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and MKL_NUM_THREADS to 1 before Python.
Run commands from the repository root. Use NEW output paths for acquisitions;
never overwrite included evidence. Examples:

```text
python -m research.journal_sprint.evidence_bundle verify
python -m research.journal_sprint.evidence_bundle extract
python -m pytest -q
python -m research.journal_sprint.run_w11_baselines --output results/journal_sprint/w11_baseline_pilot_v1 --verify
python -m research.journal_sprint.run_w11_main --output results/journal_sprint/w11_references_v1 --verify
python -m research.journal_sprint.run_w11_main --output results/journal_sprint/w11_main_v1 --verify
python -m research.journal_sprint.run_allocation --output results/journal_sprint/allocation_v1 --verify
```

Strict verifiers compare live producing-source bytes with archived hashes.
Newly added producing Python/protocol files and all evidence retain original
bytes through `.gitattributes`. Existing source files follow the repository's
historical Windows line-ending convention. A different platform/line-ending
configuration, or a later source edit, can trigger a strict source-drift rejection;
use the frozen producer snapshots in a separate reconstruction checkout rather
than editing completion hashes or bypassing integrity checks. Cross-platform
bitwise replay is not asserted. See [historical replay](ARCHIVE_REPLAY.md).

## Validation and scientific limits

The pre-PR development suite passed 569 tests with zero failures/errors/skips.
Week-11 replay checked 132 pilot rows, 384 references and 2308 main/warmup rows;
independent arithmetic checked all 144 summary cells. Those are automated checks,
not independent human peer review. No hosted CI workflow currently exists in this
repository.

Clean-source-checkout validation of commit `cf2db2504bc281cf6de5e357aa36d038f9d4ef24`
passed on 2026-09-15 using the existing validated Python environment (not a fresh
dependency installation):

- Full suite: **580 passed, 11 legacy Qiskit warnings, 312.85 seconds**; report:
  `results/journal_sprint/tests_pr_weeks10_11_v1.xml`.
- Bundle verification and extraction: all 3708 original files preserved.
- Pilot numerical replay: 132 rows, including 4 warmups; timings not reproduced.
- Allocation verification: 3240 rows and 98 files.
- Documentation: 298 local links across 101 sprint Markdown files, none missing.

The tests regenerated one pre-existing tracked pytest bytecode file only in the
disposable checkout; no source file changed. The original workspace's tracked
tree remained clean. The bounded pre-commit audit found no flagged credential
patterns or archive hash/inventory mismatches.

Classical RQMC/control methods are already accurate on the current Asian cases.
Conditional integration lowers observed error at matched sample count but costs
more per deployment. These results define a benchmark for a quantum method, not
a quantum contribution in themselves. The roadmap explicitly retains the user's
quantum-centered objective; the statistical decision rule is supporting work.

See [week-10 closeout](WEEK_10_CLOSEOUT.md), [week-11 closeout](WEEK_11_CLOSEOUT.md),
[week-11 results](WEEK_11_RESULTS.md), and [forward plan](WEEKS_11_16_IMPLEMENTATION_PLAN.md).
