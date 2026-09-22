# Release validation

22 September 2026. The computational candidate is commit
`a0a95659ac6f833c475653fecddf8cd67b58a1d2`. Later release-receipt and review commits
do not change the financial or quantum implementation unless explicitly noted.

## Repository checks

- `venv/Scripts/pytest.exe -q -m 'not slow'`: **1,672 passed, 2 deselected**,
  20 upstream Qiskit warnings, 788.93 seconds. The two marked slow cases were
  excluded; this is not a new full financial confirmation campaign.
- `venv/Scripts/ruff.exe check research/controlled_completion_followup`:
  **passes** for all new follow-up code.
- `git diff --check`: passes after preserving the exact bytes of four hashed
  historical pytest transcripts through file-specific whitespace attributes.
  Their upstream-warning whitespace was not edited, and code whitespace checks
  were not disabled.
- Full-repository Ruff: **does not pass**. The recorded run reports 4,675
  findings: 345 in files already on `origin/main` and 4,330 in preserved research
  sources/snapshots included with this evidence package. None is in the new
  follow-up directory. Most are historical compact formatting and long lines;
  unused-import/star-import/naming findings also remain. No broad lint-pass
  claim is made, and the frozen evidence was not reformatted to hide its history.
- `venv/Scripts/python.exe -m mypy src/ app/ tests/`: unavailable in the existing
  project environment (`No module named mypy`). Type checking is not claimed
  to have passed. This change does not modify `src/`, `app/` or existing tests.

## Isolated environment and committed checkout

A new virtual environment was created without system or user site packages.
The locked dependencies installed successfully; Qiskit imports from that new
environment, not the user's roaming Python installation. A detached worktree at
the candidate commit is used for replay. The original workspace's recorded
experiment outputs are not overwritten by it.

The machine-readable
[receipt](../../results/controlled_completion_followup/release_validation/receipt.json)
records the commit, interpreter, commands, return codes, elapsed verification
times and SHA-256 hashes of per-command logs. It must have `all_passed: true`
before merging. Tests and regenerated arithmetic/financial/physical model
outputs are verification calculations, not timings of quantum hardware.

The original manuscript has no diff. Historical compilation evidence is
preserved byte-for-byte, downloaded third-party full texts remain local, and
the corresponding primary-source URLs/hashes are included in provenance.
