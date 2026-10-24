# Current headline numbers (single source; 22 Oct 2026)

**Current run:** `results/frontier_probe_20261021/headline/run006/headline_table.json`.
- **Produced by:** `research/frontier_probe_20261021/headline_m_probe.py run006 results/c10_challengers_20261022/overrides_run006.json`.
- **Binding cell:** B8x52 $0.001 in every row.
- **Labels:** mod, from meas inputs. Quantum-favourable (QF) choices are used wherever a measurement was uncertain
  (Stage C spec section 0.5).
- **Review status:** reviewed by three AI R2 agents (P2; C10/C09; r3). There has been no human review.

## Inputs

| Input | Value | Source / label |
|---|---|---|
| Estimator, window certified (U1 + U2 + direction-select) | k = 8.762 | P2 run002 (c(0.003) = 4.179, parts 1-4); mod |
| Same, quantum-only mean (U2 + direction-select) | k = 9.058 | p2/run003_self_mean; mod |
| Oracle D_eff (W0 Box-Muller floor) | 2,296 layers | unchanged; mod, q+ |
| Classical T_C (B8x52 $0.001) | **8.89 s** (Stage C 22.53 s) | Same estimator, faster arithmetic. Speedup = QF fast speedup 2.078 × float32-GEMM gain 1.220 (paired; admitted by the ε/10 check). meas; the composition is assm |
| Symmetric distribution-free factor | **17.3** | C09b replicated RQMC, minimum over methods; meas. Re-measured with float32 itself: **17.5** (`f32_consistency/run001`; started at 15.5% CPU). Using 17.5, the QF end, the symmetric column below falls by about 1% (window 1.49) |
| One-core ratio | 9.62 | H16 fast, QF maximum; meas. Re-measured with float32: 9.56, so 9.62 stays the QF value |

## M (binding cell)

| Class | Primary | All-free | 1 lane vs 1 core | Symmetric | All-free + symmetric | Minimal departures to M ≤ 1 |
|---|---:|---:|---:|---:|---:|---:|
| Certified today | 2,032 | 100.9 | 211.2 | 117.1 | 5.82 | 3 |
| Canonical explicit | 588.1 | 29.2 | 61.1 | 33.9 | 1.68 | 3 |
| **Window certified, δ = 0.003** | **26.1** | **1.30** | 2.71 | **1.50** | 0.075 | **2** |
| Window certified, δ = 0.01 | 21.9 | 1.09 | 2.28 | 1.26 | 0.063 | 2 (failure 0.01 counts as one) |
| Window, quantum-only mean | 27.0 | 1.34 | 2.80 | 1.55 | 0.078 | 2 |
| Window, no U1/U2 | 76.8 | 3.81 | 7.98 | 4.43 | 0.22 | 2 |

The quantum-only mean row is the window row × 9.058 / 8.762 = 1.0338.

**P3** (`p3/run006`). For the window class, M ≤ 1 at the primary conventions needs D_eff ≤ **88 layers**. The
idealized all-free floor is 114 layers.

## Verdict

The NO-GO holds at the primary conventions with a **26×** margin. **No single favourable departure overturns it**
for any explicit class; the closest is the all-free oracle at 1.30. Two departures together do, for example
all-free + symmetric distribution-free at 0.075.

## History of the binding-cell explicit M

| Date | Stage | M |
|---|---|---:|
| 11 Oct | DP1 | 232 |
| 21 Oct | P2 window constant | 10.29 |
| 22 Oct | C10, unreviewed | 23.1 |
| 22 Oct | after review (run005) | 21.4 |
| 22 Oct | with float32 GEMM (run006) | 26.1 |

Older documents quote the numbers current when they were written. Their headers point here.

## Claim-grade debts (22 Oct, user-authorized; R1, not R2)

See [docs/claim_debts_20261022/CLAIM_DEBTS_STATUS.md](../claim_debts_20261022/CLAIM_DEBTS_STATUS.md).

- **Binding-cell bias:** 3.634e-4 ≤ 0.55ε, certified by the A2a clip-split certificate, so B8x52 $0.001 is eligible.
  The source is unchanged.
- **U1:** m = 3.28804, which covers P2's 3.32682, at failure 1e-4.
- **U2:** wrapper built, +11,578 T per iterate.
- **C03 complete-price ledger:** complete for both window classes. The physical share, 0.0069 or 0.007, is an
  explicit premise: ≤ 2.9e-16 logical failure per T at the floor, ≤ 2.8e-17 for the compiled iterate.
- **C11 compiled iterate:** window M 2,290 at floor conventions, 8,828 literal, ≥ 277 in every reading. The floor
  value of 26.1 stays the quantum-favourable reading.
- **Scope #44:** an independent recompute reproduces this table exactly. NO-GO holds under every single departure.
  The catalysed-CCZ supply convention gives 13.0, which does not flip it.
