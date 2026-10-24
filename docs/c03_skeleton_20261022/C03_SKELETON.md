# C03 skeleton: the complete-price error and confidence allowance (binding cell, window class)

22 October 2026. This is register item C03, with H18. Its trigger fired: the plausible-tier miss is 23.1, which is
≤ 30 (`results/frontier_probe_20261021/headline/run004`). Its rule says "freeze the skeleton with explicit 'unknown'
rows". This is an **R0 desk record**: nothing here certifies a row that was not already certified elsewhere. It
assumes the best explicit estimator class (the certified Kaiser window, P2 run002) at the binding cell B8x52 $0.001,
ε = $0.001, under the primary conventions.

**Status key:**
- **cert:** a certificate exists in the repo;
- **mod:** modelled, no certificate;
- **assm:** assumed;
- **unknown:** no allocation or number exists yet.

## A. Dollar error budget (total ≤ ε = 1.0e-3)

| Row | Component | Allocation | Status | Evidence / owner item |
|---|---|---:|---|---|
| A1 | Statistical estimator error e (window AE, parts 1-4 of the open problem) | 4.5e-4 (0.45ε) | **cert**, conditional on U1/U2 and the direction-select call cost | `results/frontier_probe_20261021/p2/run002`; `docs/frontier_probe_20261021/P2_DERIVATION.md` |
| A1a | Readout term inside the Δ rule | 2^-39 ≈ 1.8e-12 | assm (placeholder) | WS-k Δ rule; U2 |
| A2 | Deterministic bias reserve | 5.5e-4 (0.55ε) | n/a | — |
| A2a | Stock lower-clamp leak after the 3-binade tightening, plus the arithmetic envelope (whole modelled bias) | 4.73e-4 | **mod** (admission rests on it) | [BD] `results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json`; needs the A02 bridge rerun and A07/A13 re-proofs |
| A2b | Box-Muller q32 loader law error | inside A2a's model? | **unknown** split | A05 ("done for scope" for the current loader) |
| A2c | U2 support-tight wrapper readout bound | 2^-39 placeholder | **unknown** | U2 (E11 design notes; frozen scope) |
| A2d | Unallocated bias spare | 7.7e-5 | n/a | 0.55ε − 4.73e-4 |
| A3 | Classical post-processing (â = sin²(φ̂/2), dollar scaling) | ≤ 1e-12 in binary64 | mod | inside A1a |

## B. Failure budget (total ≤ 0.01, union bound)

| Row | Event | Allocation | Status | Evidence / owner item |
|---|---|---:|---|---|
| B1 | Window estimator misses (λ0 < 1 − δ), including part 3 (< 1e-11) and part 4 (≤ 1.9e-6 of the 4e-6 reserved) | 0.003 | **cert** | P2 run002 |
| B2 | U1 mean certificate fails (true mean > price + L1) | **unknown** | assm: the price is an uncertified RQMC orientation value; the B8x52 L1 is borrowed from B4x12 | U1 (frozen scope); C11 |
| B3 | Source / financial-bridge events (clamp or law-bridge failure probabilities, if any are probabilistic) | **unknown** | mod | A02 bridge; E07 |
| B4 | Physical (logical) failures over the whole computation | **unknown** | — | H18 (below) |
| B5 | Direction-select and controlled powers of Q | 0 | exact in the cost model (Clifford+T) | v3 §4.2 (call-cost condition) |
| | **Certified so far** | **0.003 of 0.01** | | |
| | **To allocate across B2-B4** | **0.007** | **unknown** | E07 (its 4 open obligations) |

## C. H18 necessary condition (desk, mod)

At the binding cell the certified window uses N = 100,924 controlled Grover iterates.
- Each iterate is D_eff = 2,296 supply-bound layers at 1e12 T/s and 100 ns, so T per iterate is 2.30e8.
- The whole estimate is **2.32e13 T gates** and **2.32e8 logical layers**, about 23.2 s of quantum time against
  T_C = 10.03 s, which is M = 23.1. After the review, the QF T_C is 10.84 s, so M = 21.4.
- With the 1e7-qubit width, that is **2.32e15 qubit-layers**.

Any physical-failure share s from B4 then requires:

| Share s of the 0.01 | Logical failure per T gate | Logical failure per qubit-layer |
|---:|---:|---:|
| 0.001 | ≤ 4.3e-17 | ≤ 4.3e-19 |
| 0.003 | ≤ 1.3e-16 | ≤ 1.3e-18 |
| 0.006 | ≤ 2.6e-16 | ≤ 2.6e-18 |

These are necessary conditions for the complete-price certificate, not a hardware model. They are orders of
magnitude below demonstrated logical error rates. They belong in the paper's hardware section (v3 §4.3) as the H18
row. H18's register rule ("recompute only when G3 fixes the estimator count") is met, because P2 fixes the count.

## D. What would complete C03

Each of the following needs authorization; none was done here:
1. **Certify B2 or drop U1.** Without U1, explicit window M is 41.3 at the primary conventions and 1.22 under the
   symmetric convention. A better option exists: **replace U1 by the quantum-only first stage**
   (`results/frontier_probe_20261021/p2/run003_self_mean`). That stage's failure share (1e-4) sits inside B1's 0.003
   with certified constants, so row B2 disappears. The cost is k 9.058 instead of 8.762 (primary M 23.9, symmetric
   0.707).
2. **Certify A2a.** That means the A02 bridge rerun and the A07/A13 re-proofs. It is the binding cell's eligibility
   debt, unchanged from v3.
3. **Allocate B3 and B4** explicitly, and certify A2b and A2c.

Until then, the complete-price claim at the binding cell is a **0.003-certified estimator inside a 0.01 budget whose
other 0.007 is unallocated**. The paper should say this in §8.
