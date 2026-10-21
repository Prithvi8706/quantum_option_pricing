F30 completed one bounded D1 rank2/4/8 diagnostic run and a separate
metadata-only seal recovery. This handoff supersedes the output-inventory
claim in HANDOFF_run002.md. Its sentence “sealed output manifest hashes
and membership verified” is withdrawn: the original manifest remains
invalid, preserved alongside every original scientific output.

The original manifest listed eight members: seven matched their raw bytes,
while SUCCESS.json was recorded as121 LF bytes but written as125 Windows
CRLF bytes. Nine original files, including the invalid manifest itself,
remain unchanged. Read-only newline normalization reproduces exactly the
expected old success hash. No scientific payload changed and no payoff,
fit or SVD was rerun. The original retained failure is
`docs/independent_110_20261004/F30/SEAL_FAILURE_run002.json`, SHA256
`c017b40589148f94b7bbc9303970d9a0c60e4bde66853659019a9358a2225a92`.

Use this recovered inventory for the actual output binding:

- Recovery author: `research/independent_110_20261004/F30/seal_recovery_v1.py`,
  SHA256 `5e378b7e465a4cd4da392c649c6edd9ee2138371b8c29ede7b311d72a8a2c6e1`.
- Prospective assumptions: `docs/independent_110_20261004/F30/SEAL_ASSUMPTIONS_run001.txt`,
  SHA256 `aad6a33ea862dd2ab034515018a0747b1a8fe31fcfedc916590a6320f8e32f55`.
- Frozen recovery protocol: `results/independent_110_20261004/F30/seal_recovery_run001/protocol.json`,
  SHA256 `35f3097a2071c432dfc4e5b5fcbc6f6b6ad8890d128bcc9f0fb6716fb40bbc80`.
  Nineteen files/441,588 bytes;2CPU/10wall,2MiB inputs,128KiB outputs,8owned
  file caps. The timer excludes initial protocol read.
- Independent static receipt: `docs/independent_110_20261004/F30/SEAL_STATIC_REVIEW_run001.json`,
  SHA256 `6d9085bc797ac15d34708b34fd0d425983ec829c125ee0e46f63918bc0bcf534`.
- Recovered summary: `results/independent_110_20261004/F30/seal_recovery_run001/summary.json`,
  SHA256 `a623e3d9b5addaf90978c21601ec76b289c0f5a35b0090d07bb74a1a04bc636e`.
- Actual recovered manifest: `results/independent_110_20261004/F30/seal_recovery_run001/manifest.json`,
  SHA256 `eb1e368145ab9c9e02aac90df75819dab79f12c74d0b82bcff3ba07da5bdfb6f`.
  It binds four listed owned members plus itself and nine root-relative
  external original outputs, including the failed original manifest.
  Five owned files total9,071 bytes. All listed actual hashes and complete
  owned membership were verified after execution. This hash exactly
  matches `docs/independent_110_20261004/F30/SEAL_RECOVERY_EXPECTED_MANIFEST_run001.json`,
  predicted independently before the recovery invocation.

Recovery checks comprised AST/compile, metadata-only corpus freeze,
independent static review, one fixed exact-byte inventory invocation,
original scientific-input pins, exact original mismatch reproduction,
final frozen-input recheck, actual owned/external hashes and the prior
expected manifest hash. Canonical UTF8 write_bytes avoids newline
translation. Recovery made zero scientific invocations and awards no new
scientific evidence beyond binding the existing artifacts.

Independent post-run review is recorded in
`docs/independent_110_20261004/F30/SEAL_POSTRUN_REVIEW_run001.json`, SHA256
`79efd71af757aca1c510e89c62a499ecebddd2ff44c599d2d0654e608b513a88`.
It separately confirms all nineteen frozen input pins, four listed owned
members and nine external bindings, and the prospective manifest hash.

The completed scientific diagnostic remains narrowly scoped: original
plain D1 Asian contract and existing unconditional PCA map;1,089 training
plus512 separate validation targets, shared across all three ranks; one
weighted SVD; ranks2/4/8; no validation rank selection or clipping. The
weighted training residuals were0.131424,0.000503196 and6.11e-15, while
separate conditional-cube validation RMSE was0.210486,0.202082 and0.202072
dollars. Contraction and finite-grid Cauchy diagnostics passed. No directed
rounding, quadrature, Gaussian-tail, interpolation or original-price error
certificate was obtained. Financial contract and scientific specifications
did not change during metadata recovery.

The earlier run001 launcher preflight rejection is also retained. It
performed no payoffs/SVD/ATTEMPT. The sole scientific run002 used the
enforced project Python3.12.4/NumPy2.0.2 interpreter. Its source/proof,
frozen corpus, result values and receipts remain read-only. Financial
details and primary-source scope are in HANDOFF_run002.md; its erroneous
seal-verification sentence must not be relied on.

Read INTEGRAL_ERROR_OBLIGATIONS_run002.md. The three-rank stop rule is
reached, so this uncertified quantum loading route is closed for the
nominated representation. Coherent loader/inverse, sign/normalization,
rotation/synthesis, estimation and physical costs remain paid unknowns.
WholeF30 acceptance, a20percent quantum gain, matched timing, source
adoption, B4/B8 validation and quantum advantage remain unclaimed.
