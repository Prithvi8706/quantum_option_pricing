# WS-k (plan110 W0): k bracket

Items: E01, C11 (bracket), E25, E08, E03 with U1/U2, E04, E20 (lanes). Rigour: R0 screen.

| File | What it is |
|---|---|
| `k_bracket.md` | The report: headline, the five parts, caveats. |
| `k_bracket.py` | The script. Stdlib only; it ran under `.context/frontier_t0_env` 3.12.4 `-I -S -B`. Run: `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_w0/ws_k/k_bracket.py`. Outputs are created exclusively, so re-running needs a fresh output dir passed as argv[1]. |
| `results/plan110_w0/ws_k/k_bracket.json` | Every number, with input SHA256s (`meta`). |
| `results/plan110_w0/ws_k/rows.jsonl` | One row per sub-result: 7 literature rows written by hand, then rows from the script. |

**Self-checks (asserts in the script).**
- The E07 schedule at eps = $0.01 is reproduced exactly: 983,025 calls.
- The task formula with the 2^-39 readout picks the same M in all 16 cells.
- The IQAE and modified-IQAE theorem values reproduce the E04 screen: 6,471,874 and 6,491,064.
- The joint table reproduces the CRITIQUE F3 table and the U2 §4 halving pattern.
- In the window numerics, the DPSS value is at most the Kaiser value, which is at most the Berry et al. formula. The rectangular-window sanity check gives 0.903, above 8/pi^2.

**Literature checked.** Nine sources in total; seven were fetched or searched:
- Mande & de Wolf, arXiv:2305.04908;
- Berry et al., arXiv:2209.13581, App. D;
- Rall & Fuller, arXiv:2207.08628;
- Patel et al., arXiv:2403.18927;
- Nakaji, arXiv:2003.02417;
- Kothari & O'Donnell, arXiv:2208.07544.

The Grinko and Fukuzawa IQAE formulas were not re-fetched. They are taken from the repository's E04 screen, which cites its primary sources.

Nothing in this work ran a controller, launcher, verifier or git operation, and nothing was written outside the two `ws_k/` folders.
