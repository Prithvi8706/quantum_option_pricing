# Week-12 reproduction and integration handoff

Scientific status: [development complete, interest gate failed](WEEK_12_CLOSEOUT.md).
Source freeze `9a97228a`; separate-agent review in [WEEK_12_REVIEW.md](WEEK_12_REVIEW.md).
No physical quantum advantage, confirmation or submission-readiness claim.

## Evidence bundle

`results/journal_sprint/week12_evidence_v1.zip` and its JSON index contain all
7928 files from `w12_runtime_pilot_v2` and `w12_development_v1`, losslessly.
Original evidence compresses to 8,362,812 bytes; exact uncompressed size is
30,963,685 bytes. ZIP SHA256:
`9f2dfa192c2dd947828fbbfaaf43b99d9189f8298968d90f104d81c74ab6477a`.
Main's nested pilot copy is provenance, not additional samples. Original completion
manifests, no-declarations, the interval miss and the negative gate are preserved.
Receipts and test XML accompany the ZIP as separately readable files.

Use the existing Windows/Python 3.9 research environment or the candidate
`research/journal_sprint/requirements-week11.txt` recipe. Fresh dependency
installation and cross-platform bitwise replay remain unvalidated. Set
OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and MKL_NUM_THREADS to 1; disable bytecode
writes when replaying snapshots. New producing files retain original bytes via
`.gitattributes`; existing producers follow the historical Windows CRLF convention.

From a fresh repository checkout:

```text
python -m research.journal_sprint.evidence_bundle verify --bundle results/journal_sprint/week12_evidence_v1
python -m research.journal_sprint.evidence_bundle extract --bundle results/journal_sprint/week12_evidence_v1
python -m research.journal_sprint.run_w12 --verify --output results/journal_sprint/w12_runtime_pilot_v2
python -m research.journal_sprint.run_w12 --verify --output results/journal_sprint/w12_development_v1
python scripts/verify_week12_independent.py results/journal_sprint/w12_development_v1
python -m pytest -q
```

Extraction refuses existing archive roots: do not run it over the originating
workspace's existing evidence. Use a fresh checkout; do not delete originals to
make extraction work. The previous week10-11 bundle can separately reconstruct
older evidence if needed; see [earlier handoff](PR_WEEKS_10_11_HANDOFF.md).

Acquisition commands are intentionally not presented as reproduction of measured
timings. Replaying saved draws is not new confirmation, and default namespaces
must not be reused to claim independent observations.

## Integration audit

Separate-source-checkout verification and publication/merge disposition are recorded
here once performed. No code changed after production acquisition. Local environment,
downloaded articles, private configuration, unrelated outputs and the six-edit
user stash are excluded/preserved. AI review does not imply Macroscope or human
approval; PR check state must be recorded as observed, including skipped checks.
