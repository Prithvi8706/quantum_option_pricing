F30 completed the bounded three-rank development D1 fit and contraction
diagnostic screen. WholeF30 acceptance remains false: original-price
certification and coherent loading-plus-estimation costs were not supplied.

- Author: `research/independent_110_20261004/F30/rank_screen_v2.py`, SHA256
  `5638a1d54a5b470bef0689384fbc2dd772ab098c1d75ccf05bac24b3421c2450`.
- Assumptions: `docs/independent_110_20261004/F30/ASSUMPTIONS_run002.txt`,
  SHA256 `a2f5915bf7a442116d2718399555eb1155c7d9b73eb39c85325288b2952575b1`.
- Frozen protocol: `results/independent_110_20261004/F30/run002/protocol.json`,
  SHA256 `32359eab663811c19f12c18fcfeddbe93ac1d6fb10eab6984ec644f6185676d3`.
  Six input files/356,016 bytes,10CPU/30wall seconds,4MiB input,2MiB output,
  16output files,1,601 payoff evaluations and2,048 validation-draw caps.
- Frozen nodes/weights/validation:
  `research/independent_110_20261004/F30/corpus_run002/fixed_data.npz`, SHA256
  `a9b21d8596a906a4865ebb22e2cd8cd5ba65a07b3eb00554ee6dda3d5b0a9ed8`.
- Independent pre-run receipt: `docs/independent_110_20261004/F30/STATIC_REVIEW_run002.json`,
  SHA256 `62ad0114727f4c98313ef288a58218c3f1c266a5c0848f17eeb9ac3a84bbf237`.
- Result: `results/independent_110_20261004/F30/run002/summary.json`, SHA256
  `d6a08003f28cd74d33f70d6e81c4d47c3d1fbfde95205693586887b8e36f139a`.
  The three `rank_*_cores.npz` files retain fitted cores, grid approximations
  and signed validation predictions. `training_and_validation.npz` retains
  the shared targets, covariance/PCA factor and all singular values.
- Sealed manifest: `results/independent_110_20261004/F30/run002/manifest.json`,
  SHA256 `1517f89a97f724bf01c0597985027827faf1f3505f6d52fc32d83d55071f7a6b`.

The original plain D1 one-asset/two-date Asian contract and its existing
unconditional PCA map were retained. No barrier, F03 transform or new
high-dimensional workload was introduced. One33x33 training grid supplied
1,089 unique targets;512 separate frozen validation targets were evaluated
once. These1,601 evaluations and one weighted SVD are shared evidence, not
three independent training runs. Validation did not select a rank.

| Rank | Core parameters | Weighted training residual | Validation RMSE ($) | Validation maximum error ($) | Contraction multiplies/adds |
|---|---:|---:|---:|---:|---:|
| 2 | 132 | 0.131424 | 0.210486 | 1.151458 | 134 /129 |
| 4 | 264 | 0.000503196 | 0.202082 | 1.182091 | 268 /259 |
| 8 | 528 | 6.11e-15 | 0.202072 | 1.182097 | 536 /519 |

The full weighted training-grid sum was10.190374782365748 dollars. Rank
contraction changes were approximately4.87e-5,1.07e-9 and0 dollars in
floating arithmetic. These are truncated finite-grid diagnostics. They
do not certify the original price; the near-roundoff rank8 grid residual
coexists with validation RMSE about0.202 dollars. Negative fitted values
were archived rather than clipped: training counts97/79/178 and validation
counts45/49/29. Counts alone do not establish their magnitude or a
mathematical failure of the continuum integrand.

Checks: source AST/compile without project imports; metadata-only
nodes/validation preparation and corpus freeze; independent static review;
one prescribed three-rank payoff/SVD invocation; covariance reconstruction,
weighted residual/discarded-singular consistency, direct contraction and
finite Cauchy diagnostics; frozen-input hashes rechecked before sealing;
sealed output manifest hashes and membership verified. The timer starts
inside run after NumPy import/protocol read and is a stopping guard, not
a measured end-to-end performance comparison.

Preserved failed preflight: v1 author/proof, `corpus_run001/fixed_data.npz`
and `results/independent_110_20261004/F30/run001/protocol.json` remain intact.
The default launcher was Python3.9.13/NumPy1.26.4, contrary to the stated
project environment. `PREFLIGHT_REJECTED.json` and
`docs/independent_110_20261004/F30/STATIC_REVIEW_REJECTION_run001.json`
record rejection before any payoff, SVD orATTEMPT. Freshv2 uses the enforced
`.context/frontier_t0_env/Scripts/python.exe` Python3.12.4/NumPy2.0.2. The
financial specifications, ranks, seed, evaluation budget and stop did not
change. This was metadata preflight recovery, with no scientific retry.

[Sakurai, Takahashi and Miyamoto v1](https://arxiv.org/html/2405.00701v1),
SecII.1.2 andIII.2, supplies context for SVD and classical tensor contraction.
The exact cached HTML is pinned in the protocol; displayed header/version
chronology is recorded in the assumptions. Its European/Fourier/parameter
learning demonstration was not transferred as a D1 Asian error theorem.

Read `INTEGRAL_ERROR_OBLIGATIONS_run002.md` for missing quadrature, tail,
interpolation, rounding and coherent-loading error obligations. Quantum
loading is closed for this uncertified representation at the bounded stop
rule. No loader compilation, physical-cost adoption, matched timing,
20percent quantum gain, originalB4/B8 validation or advantage was claimed.
