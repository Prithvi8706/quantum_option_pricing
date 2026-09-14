# Paper A Research Package

Isolated from `src/` and `app/`. The deployed dashboard is never affected by
anything here.

## Gates

    venv/Scripts/python.exe -m research.paper_a.scripts.run_e0

Exit code 0 means every deterministic semantic check passed and stochastic
experiments are unblocked. Non-zero means **no stochastic experiment may
start**. See the spec's E0 section for what each gate proves.

## Smoke run

    venv/Scripts/python.exe -m research.paper_a.scripts.run_smoke

Writes `data/paper_a/smoke/` with `raw.jsonl`, `resources.jsonl`,
`validation.json`, and `COMPLETE`. New runs also retain per-attempt journals of
the original result/resource payloads. Interrupted appends recover from those
journals without resampling or reconstructing actual resources. Legacy partial
pairs without journals fail closed and must be audited; they are not silently
repaired. Invalid reruns remove a stale completion marker and never publish a
new one. File writes are flushed and fsynced; this is not a guarantee against
every filesystem/power-loss failure or concurrent writers.

## Frozen values

Benchmark, subsets, support rule, rescaling factor, streams, and tolerances
are frozen in the spec's Frozen Protocol Annex. Changing any of them requires
a versioned amendment recorded **before** the affected output is inspected.

## Deliberate differences from `src/`

`src/quantum.py` clamps `sigma` to 0.15 for dashboard display. This package
**rejects** out-of-domain input with a named error and never clamps.
