# F23 fixed covariance-compression screen

F23's bounded initial rank screen is complete: **RETAIN_FULL_RANK_NO_ELIGIBLE_COMPRESSED_SOURCE**. All six rank rows and 18 fixed barrier-band cases are retained. None meets the isolated proposed $0.001 compression allowance. This is a negative certificate-method result; actual price bias has no proved lower bound.

The unchanged original B4x12/B8x52 GBM arithmetic-basket knock-out contracts retain every monitoring date, strict basket <140 survival, original drift and parameters. The explicitly proposed continuous approximation projects log-price covariance onto canonical descending modes while retaining the original deterministic drift. That changes covariance and marginal stock means. The finite q32/native72f40 source is not replaced, and its existing G2 certificate is not transferred.

The frozen ranks were B4:24,36,47 and B8:208,312,415. The population proof derives E|S-S_rank| <= S0 exp(rt) sqrt(2 omitted_variance/pi), gives the call coupling bound, and separately controls barrier switching using basket perturbation Markov bounds and the original full-model common-factor lognormal band density. Fixed eta=1,5,10 dollar widths were used. The law-independent discounted support cap is also included.

| Case | Rank | Call coupling upper bound, approximate display |
| --- | ---: | ---: |
| B4x12 | 24 | 2.449864 dollars |
| B4x12 | 36 | 1.384487 dollars |
| B4x12 | 47 | 0.305033 dollars |
| B8x52 | 208 | 1.063350 dollars |
| B8x52 | 312 | 0.654698 dollars |
| B8x52 | 415 | 0.037175 dollars |

All six knock-out certificates reduce to the loose support cap, approximately $38.817822, far above $0.001. Rounded-up displays above are explanatory; exact outward rational upper bounds in `rank_bounds.json` are authoritative. A smaller bound or a different compression might work; this screen proves neither actual bias magnitude nor an impossibility of compression.

One isolated interval/mapping run passed. Dyadic120 outward rational arithmetic encloses Machin pi, sine/eigenvalues, square roots, exponential and log-band expressions with analytic remainders. It certified 462 adjacent spectral order checks, 64 contractual-time marginal variance enclosures, 12 exact asset variance identities, 6 omitted trace checks, 18 fixed band cases and 2 full-rank zero identities: 564 grouped checks. No approximate eigenvalue tie was selected. These checks support the explicit population proof; no paths, samples, gates or prices were evaluated.

The prewritten protocol, proof and exact source are `PROTOCOL.json`, `OMITTED_MODE_PROOF.md` and `research/independent_110_20261004/F23/screen_covariance_compression.py`. Prospective `FREEZE.json` SHA256 is `edaed427c525859fe81d4c58e9fdfee696deb5a74f0c703108e782c86543cc8c`, binding 15 selected inputs and 695,836 bytes. Root reviewed the frozen proof, enclosure arithmetic and ordering/coupling before authorizing the sole run. Command:

```text
.context/frontier_t0_env/Scripts/python.exe -I -S -B research/independent_110_20261004/F23/screen_covariance_compression.py run --freeze-sha256 edaed427c525859fe81d4c58e9fdfee696deb5a74f0c703108e782c86543cc8c
```

Receipt: `results/independent_110_20261004/F23/screen_run001/manifest.json`, SHA256 `5e978d8b5592657acb1b09561f884ec0b49c69901aba368aebd709137d5e8ae9`. The seven-file packet is complete and uncensored, with no failure marker. All frozen input/runtime selections were checked before and after. Only the selected launcher/base interpreter were pinned; no full runtime/dependency integrity claim is made. No failed scientific run or retry occurred.

The current full-rank model/source remains. A compressed source still requires a sufficiently tight payoff-specific bound, changed finite-law/loading/arithmetic bridges, clean reversible preparation/path/inverse/reflection and complete estimator cost. Since no rank passed the bound, compilation and matched timing were not attempted. The $0.001 allowance is a prospective isolated screen, not a new shared budget. Zero new global fixture credit, gate replay credit, samples, source adoption, financial delivery or advantage credit are added. Shared basis, sources, receipts, progress, STATUS and manuscript remain unchanged; root owns reconciliation and separate fresh integrity verification.
