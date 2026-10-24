# U1: a certified upper bound on the digital mean at the binding cell (R1)

22 October 2026. This is register item U1: the mean credit that the window estimator class uses. The cell is
B8x52 at ε = $0.001.

**Rigour: R1.** A fixed-n sample was drawn, and the bound was computed along two independent exact or outward paths
that agree. This is **not R2**: there was no preregistration, sealed run, saved verifier, ROOT receipt or human peer
review. AI-assisted.

## Result

**With probability ≥ 1 − δ_U, where δ_U = 10^-4, over a classical sample fixed before any quantum run:**

    E[g] = E[Y_N]  ≤  m_cert = 3.28803895004885611880573890944030163553… USD (exact rational in u1_certificate.json)

| Piece | Value | Label |
|---|---:|---|
| Sample mean of the raw continuous payoff (n = 2^23 = 8,388,608, fixed in advance) | 3.279600201 | meas |
| Float slack added to the mean | 1e-9 | assm (generous) |
| One-sided empirical-Bernstein half-width at δ_U = 1e-4, range R = 40 | 0.008075375 | cert (outward arithmetic) |
| UCB on E[Y], the continuous-GBM price | 3.287675577 | cert, conditional on the PRNG being iid |
| A2a bias bound \|E Y_N − E Y\| (finite source to continuous price) | 3.63374e-4 | cert R1 (`results/claim_debts_20261022/a2a/run001`) |
| **m_cert** | **3.288038950** | cert R1 |

**What this means for the window class.** Its k = 8.762 is now covered by a certified premise.
- P2 used m = 3.3268214. That was the uncertified RQMC price 3.2816194 plus L1 = 0.045202052, which was borrowed from
  B4x12 and is not a B8x52 certificate.
- m_cert sits **0.0388 below** that value.
- The error rule √(m(S−m))·Δ + SΔ²/4 + 2^-39 increases in m on [0, S/2]. Any certified upper bound at or below P2's
  m therefore keeps P2's call count valid.

| Mean bound used | Δ | N calls | k | M (binding cell, primary) |
|---|---:|---:|---:|---:|
| P2's m (now covered by m_cert) | 4.14077e-5 | 100,924 | **8.7618** | **26.08** |
| m_cert itself (tighter) | 4.16284e-5 | 100,389 | 8.7153 | 25.94 |

M = k·10·(σ/e)·D_eff·t_layer/T_C, with σ/e = 11518.65676754799, D_eff = 2296.03168, t_layer = 1e-7 and
T_C = 8.886479314695709. I recommend keeping the headline at k = 8.762 (M 26.1). Re-deriving the headline on m_cert
would move it by only 0.5%, and it is not needed.

**Failure share.** δ_U = 1e-4 is a new event in the C03 failure union. It is taken from the 0.007 that C03 allocated to
physical failure, so that share becomes 0.0069. The window estimator keeps its 0.003. That moves the H18 condition by
about 1.4%: the physical share drops from 0.007 to 0.0069.

## Statement and proof

Notation:
- Y = e^{-rT}(A − 100)^+·1{max_j B_j < 140} is the continuous-GBM payoff, with 8 assets and 52 dates.
- Y_N is the native payoff under the circuit's finite input law.
- g is the digital payoff node, so E[g] = E[Y_N]. This is the E02 amplitude law: p = E[Yraw]/2^46.

1. **Bias.** E[Y_N] ≤ E[Y] + |E Y_N − E Y| ≤ E[Y] + 6703058386012589/2^64, by the A2a clip-split certificate.
2. **Range.** On survival, A ≤ max_j B_j < 140, so 0 ≤ Y ≤ 40e^{-rT} ≤ 40. This is analytic, and the sample min and
   max (0 and 30.40) agree.
3. **One-sided empirical Bernstein** (Maurer & Pontil 2009, Thm 4, scaled to [0, R]). For iid Y_1..Y_n with unbiased
   sample variance V_n, with probability ≥ 1 − δ,

       E[Y] ≤ Ȳ + sqrt(2 V_n ln(2/δ) / n) + 7 R ln(2/δ) / (3(n − 1)).

   - n = 2^23 was fixed in the script before sampling. There was no pilot and no stopping rule.
   - Ȳ and V_n are formed as exact rationals from the saved `math.fsum` totals. Every transcendental is rounded
     outward: Decimal ln and sqrt at 60 digits, rounded up at 1e-40.
4. **Combine.** m_cert = UCB + A2a ≤ S/2 = 19.41. That is the condition under which the √(m(S−m)) rule applies.

**Sample.**
- `eb_sample.py` simulates the contract directly, from cumulative common and idiosyncratic Brownian increments, with
  numpy PCG64 seed [2026102231, 8, 52].
- It does **not** use the Stage C factor, preintegration kernel, or range bound. That makes it independent of the C09
  machinery.
- Wall time 127 s and CPU time 125 s, single process.
- The machine was not idle during the run: another session's python process was busy. This does not affect
  correctness, because the sample is not a timing measurement.

**Cross-check (mod).** The saved C09 preintegrated sample (n = 80,419,536) at the same δ_U, with R = 17.30, gives a
UCB of 3.28251 and m = 3.28287. The two are consistent. This value is **not** used:
- the preintegrated range 17.30 comes from a float-evaluated analytic bound in P1;
- the kernel's equality with E[Y|y] holds only in float64.

## Independent recompute

`u1_independent.py` uses only integers and Fractions:
- ln(2·10^4) by the atanh series with an explicit remainder;
- square roots by `isqrt` at 2^-200, rounded up;
- Δ from the closed-form quadratic root instead of P2's bisection.

Results:
- m_cert agrees to 9.7e-41.
- The call counts agree exactly: 100,924 at P2's m, which also equals P2 run002's saved N, and 100,389 at m_cert.
- `agree = true`.

## Files

| File | sha256 |
|---|---|
| `research/claim_debts_20261022/u1/eb_sample.py` | 445fab47acb58a35b2788cfa7208811c33ae95a6d465b91b16d22de683159dd0 |
| `research/claim_debts_20261022/u1/u1_certificate.py` | 713db0df38ff86753063ec86462d7aac44de2ffa8648d57019dd7cbb822d7ee8 |
| `research/claim_debts_20261022/u1/u1_independent.py` | 06a772f62c892e2d6e35c6ab59c2cdb118b5e7a0d068ff616fa58488315b7035 |
| `research/claim_debts_20261022/u1/summarize.py` | 239b04541a26cc335d7a28a06fba8b40c1d6e45924d64ba43f0df83dfbe363af |
| `results/claim_debts_20261022/u1/run001/eb_sample.json` | 373d66263ac53a0d04483640323c1566f26c7fce1add6e888659f4e6a50531b8 |
| `results/claim_debts_20261022/u1/run001/u1_certificate.json` | a965d569ea8183e2305a2740f25ce66119235dc8bec59f2abc57cebc026a1408 |
| `results/claim_debts_20261022/u1/run001/u1_independent.json` | 652c6428878aebeb026dc7961c5165bd23f334321c55067f7f746f23922e04d5 |
| `results/claim_debts_20261022/u1/run001/summary.json` | all_checks_pass = true |

How each script runs:
- `eb_sample.py` ran in the Stage C env **without** `-I -S` (it needs numpy):
  `../../../.context/frontier_t0_env/Scripts/python.exe -B research/claim_debts_20261022/u1/eb_sample.py run001`.
- The three other scripts ran with `-I -S -B` from the worktree root.

## Premises (read only)

| Premise | sha256 |
|---|---|
| `results/claim_debts_20261022/a2a/run001/summary.json` (A2a bias, R1) | 5608ee4dbb83f862bdbe4143b238baae7502528ce62448ea2146aa35e5037555 |
| `results/frontier_probe_20261021/p2/run002/p2_window.json` (c = 4.179, N = 100,924) | 0447dd06e08262f53cd52d32d3c16c24e21c56044b45339619321719aced1094 |
| `research/frontier_probe_20261021/p2_window_constant.py` (`delta_phi` copied unchanged) | 59a010a89f1aa56d60e6ff6e965d4d66754e1d5619a7a65bd253af8db59e58f3 |
| `results/frontier_classical_20261001/sigma_dev/sigma_dev.json` (σ_q) | 9d3c4e361ec0a9f4d24fbebea7e1d6adb40e39326cf67d5fd44cca6a4fa27677 |
| `results/frontier_classical_20261001/c1/c1_summary.json` (P2's price) | 5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123 |
| `results/c10_challengers_20261022/c09/B8x52_0.001_run001/c09_g4.json` (cross-check only) | 8ce019bf6592de155c5fc33be79391c5ab6cd54a444c41422be2e9cc8aec5552 |

## Assumptions and what remains for R2

**Assumptions.**
- The PRNG stream is treated as iid N(0,1) draws. This is the usual Monte Carlo premise, labelled assm.
- Float64 rounding in the simulated payoff is covered by a 1e-9 USD slack. That slack is generous, but it is not
  derived.
- The A2a premises carry over unchanged, including its three facts that run002 does not state as outputs.

**Still needed for R2:**
- preregistration of n, seed and δ_U before sampling;
- a sealed run with a saved verifier and receipt;
- human peer review of the statement, especially the binding E[g] = E[Y_N] (U2 note O2) and the C03 failure-share
  change;
- an R2 A2a.
