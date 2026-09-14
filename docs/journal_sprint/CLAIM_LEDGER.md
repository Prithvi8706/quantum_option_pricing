# Historical claims: quarantine ledger

Neither manuscript has been submitted or published. Original files remain
unchanged and are copied, hashed and indexed in
`results/journal_sprint/historical_audit_v2/evidence_snapshot/`.

| Historical statement | Disposition for the next manuscript |
|---|---|
| $0.203 is an irreducible three-qubit discretization floor | Withdraw. CSV delta is deviation from a precomputed QAE price, not isolated deterministic discretization error. |
| epsilon_target=0.01 means a one-cent price target | Withdraw. It is an amplitude-probability tolerance; apply the actual contract-dependent price transformation. |
| The p=0 mean Black-Scholes error is $0.203 | Replace only with a properly labeled recomputation: about $0.303837 for the 50-contract expanded CSV. That still does not isolate a discretization floor. |
| Oracle-query count is physical circuit depth or total shot-weighted cost | Withdraw. Report shots, Grover calls, A-equivalent calls, compiled depths/gates and setup separately. |
| Synthetic depolarizing p is calibrated IBM pricing performance | Withdraw unless supported by actual calibration and matched pricing-circuit tests. |
| A single-Ry hardware run validates the full pricing pipeline | Restrict to its actual state-preparation sanity check. |
| Paper B's 100-trial dimension sweep is reconciled/canonical | Quarantine. Checked-in script uses 10 trials; DOCX retains -1.14/-0.65-era statements; raw 100-trial evidence has not been located. Neither slope set is approved for reuse. |
| Both papers are submission-ready | Withdraw pending this reengineering and independent review. |

Producing-code provenance is incomplete. Last Git commit for a file is recorded
but does not establish which revision generated a historical run. Snapshot v1
missed the actual precomputation script due to a path error; v2 adds
`app/precompute_qae.py` and `src/quantum.py`. Both snapshots are retained.

Source trace: `app/precompute_qae.py` stores `quantum_call`'s result in `price`;
`src/noise_experiments.py` uses that field as the expanded sweep reference. The
audit recomputes continuous Black-Scholes independently without executing pickle
contents. The stored delta identity is checked row by row.

The DOCX and old LaTeX drafts are historical, not silently rewritten or destroyed.
This ledger and the repository warning supersede their protected/canonical status.
The next actual manuscript must remove or substantiate every quarantined claim.
