# N1 estimator workstream (plan110 branch N, rigour R1)

Items: E01, C11 (bracket), E03, E04, E08, E25, E20.

| File | What it is |
|---|---|
| `estimator_card.md` | The card. It has seven sections: access model and counting lower bound; achievability bracket with each conditional credit; lanes at W = 1e7; literature verification; the open problem; discrepancies against W0; caveats. |
| `estimator_card.json` | The same content in machine-readable form, plus the receipt (script, output and input SHA256s). |
| `recompute_estimator.py` | The independent recompute (stdlib only). Run it from the repo root with `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/estimator/recompute_estimator.py [out_dir/]`. Its JSON output is created exclusively, so a re-run needs a fresh out_dir. |
| `results/plan110_n1/estimator/estimator_recompute.json` | Every recomputed number, with its label and direction. |
| `results/plan110_n1/estimator/rows.jsonl` | 26 rows. Rows 1-9 are the literature checks from the run the logout cut off. Rows 10-20 come from the script. Rows 21-26 are hand-written: the counting-bound proof check, the four discrepancies and the open problem. |

**Resume note.** The earlier run had written only the 9 literature rows. Those rows were reused unchanged. Nothing was overwritten or deleted. No further sources were fetched, so the total stands at 8 fetches against a cap of 15.

**Headline.**
- The recompute reproduces every WS-k number the decision table uses:
  - certified k 586-1,067;
  - best explicit k 187-198;
  - window k 6.9-7.4 (DP1 row), 8.3-8.7 (δ = 0.003) and 23.5-25.7 (no credits);
  - counting lower bound 1.70 / 1.85;
  - primary M of 801, 232 and 8.6.
- Six literature sources were verified against their primary texts: Mande-de Wolf, Grinko, Fukuzawa, Berry, Patel and BHMT. Rall-Fuller and Nakaji were also verified. Nothing was contradicted.

**New findings.**
- **Direction-select control halves canonical calls.** BHMT Thm 12 still applies; the only missing piece is a call-cost certificate. With it, M falls from 801 to 401 and from 232 to 200.
- **The DP1 window row uses δ = 0.01.** Like for like, at δ = 0.003, M is 10.3.
- **Lanes add nothing for B8x52 at W = 1e7** once the floor designs and the shared T supply are used. The NO-GO verdict is unchanged.

**Scope.** Nothing in this work ran git, a controller, a launcher or a verifier. Nothing was written outside `research/plan110_n1/estimator/` and `results/plan110_n1/estimator/`.
