# P2: a certified worst-case constant for window amplitude estimation (derivation)

This note writes out the argument implemented in `research/frontier_probe_20261021/p2_window_constant.py` (parts
1-2) and `p2b_parts34.py` (parts 3-4). The R2 adversarial review re-derived each step and found no critical or
major error (`results/frontier_probe_20261021/review/p2_review.jsonl`, 21 rows).

**Conventions** (WS-k, v3 §4.2):
- one call is one controlled Grover iterate;
- direction-select lets N calls realise the exponents n = −N..N;
- Q has eigenphases ±φ, φ = 2θ, a = sin²θ.

## 1. Estimator

1. **Prepare the window state.** Prepare |w⟩ = Σ_{|n|≤N} w_n |n⟩ / ‖w‖ in a register of G = 2^g ≥ 2N+1 points.
   - The magnitude uses a subset-sum step set {1, 2, 4, …, remainder} with total N, so exactly N calls realise
     every |n| ≤ N.
2. **Apply the offset and the powers.** Apply the known phase e^{inτ}, with τ = 2πl/(GK) and l uniform on
   {0..K−1}; this is classical randomness and query-free. Then apply controlled Q^n.
3. **Read out.** Apply the inverse QFT over Z_G and read j. Set φ̂ = 2πj/G − τ and â = sin²(φ̂/2).

For an eigenvector with phase φ, outcome j has probability F(φ + τ − 2πj/G)/G, where F(u) = W(u)²/‖w‖² and
W(u) = Σ_n w_n e^{inu} (real, because w is symmetric). This is exact because G ≥ 2N+1.

A|0⟩ is a superposition of the two eigenvectors (±φ). The outcome law is a mixture of the two branches, and â
is even and 2π-periodic in φ̂. So the success event |φ̂ − (±φ)| ≤ Δ gives the same â bound for either branch,
including a near 0 or 1.

The amplitude error is |â − a| ≤ √(a(1−a))·Δ + Δ²/4. In dollars this is √(m(S−m))·Δ + SΔ²/4 when
m ≤ m_U ≤ S/2 (the U1 credit), plus the 2^-39 readout term.

## 2. Part 3: the success probability for every phase

Averaging over l turns the readout into a lattice sum with step h = 2π/(GK):

P(φ) = (h/2π) Σ_{u ∈ φ + hZ, |u| ≤ Δ} F(u).

A lattice sum differs from ∫_{−Δ}^{Δ} F by at most h·(TV(F) + sup F). Two Cauchy-Schwarz bounds give
sup F ≤ 2N+1 and |F′| ≤ 2N(2N+1). Hence, for every φ,

P(φ) ≥ λ0 − (2N+1)(1+4c)/(GK),  where λ0 = (1/2π)∫_{−Δ}^{Δ} F and c = NΔ.

With K = 2^40 the loss is below 1e-11.

## 3. Parts 1-2: a lower bound on λ0, uniform in N ≥ N0

**Window.** φ_γ(x) = I0(β√(1−x²)) − γ on [−1, 1], with γ ∈ [0, 1]. The taps are w_n = φ_γ(n/N) for |n| < N
and w_{±N} = (1−γ)/2.

**Split.** Write φ_γ = φ_1 + (1−γ)·1_{[−1,1]}, where φ_1 = I0(β√(1−x²)) − 1 is continuous and satisfies
φ_1(±1) = 0. The transforms are:
- Φ_γ(η) = ∫ φ_γ e^{−iηx} = 2 sinh(√(β²−η²))/√(β²−η²) − 2γ sin η/η, with sinh → sin for |η| > β;
- Φ_1 = Φ_γ at γ = 1.

**Poisson summation.** It is valid because φ_1 is continuous and Φ_1 = O(η⁻²). Together with the exact DTFT of
the half-weight rectangle, sin(Nω)·cot(ω/2), it gives

W(ω) = N Φ_γ(Nω) + R(ω),  R(ω) = N Σ_{k≠0} Φ_1(N(ω+2πk)) + (1−γ) sin(Nω)·(cot(ω/2) − 2/ω).

**Decay of Φ_1.** For |η| > β, write s = √(η²−β²). By the mean value theorem on sin t/t (whose derivative is
at most 1/t + 1/t²), and with η − s = β²/(η+s):

|Φ_1(η)| ≤ 2β²(1 + 1/s) / ((η+s)s) ≤ β²κ/η²,  κ = (1 + 1/s_min) / (1 − β²/η_min²),  η_min = Nπ.

For |η| ≥ η1 = 2β this gives |Φ_1| ≤ A1/η² with A1 = 1.23761·β²·(1 + 2/(√3·η1)), since
2/((1+√3/2)(√3/2)) = 1.2376043.

**Aliasing.** For |ω| ≤ π and k ≠ 0, |N(ω+2πk)| ≥ Nπ(2|k|−1), and Σ_{k≥1}(2k−1)⁻² = π²/8. Hence
N Σ_{k≠0} |Φ_1| ≤ β²κ/(4N).

**The rectangle term.** cot(x/2) − 2/x has a Laurent series whose coefficients all have one sign, so
|cot(ω/2) − 2/ω|/|ω| increases on (0, π]. Its maximum, at π, is 2/π². Therefore

|R(ω)| ≤ β²κ/(4N) + (1−γ)(2/π²)|ω| ≤ C_R := β²κ/(4N) + (1−γ)·2/π.

**Energy expansion.** Σ w_n² = (1/2π)∫_{−π}^{π} W² and the in-band energy (1/2π)∫_{−Δ}^{Δ} W² are each expanded
as a main term plus a cross term plus an R² term:
- **Main terms:** at most N·I_tot/2π and at least N·I_c/2π. Here I_tot = ∫_ℝ Φ_γ² = 2π∫φ_γ² and
  I_c = ∫_{−c}^{c} Φ_γ².
- **Cross term over [−π, π]:** at most
  X = (1/π)·[β²κ/(4N)·L1Φ + (1−γ)(2/π²)·L1ηΦ/N], where L1Φ ≥ ∫_{|η|≤Nπ}|Φ_γ| and L1ηΦ ≥ ∫_{|η|≤Nπ}|η||Φ_γ|.
  - L1Φ = U1 + (1−γ)·4(1 + ln Nπ), with U1 = 2(η1·Φ_1(0) + A1/η1).
  - L1ηΦ = V1 + (1−γ)·8N, with V1 = 2(η1²Φ_1(0)/2 + A1·ln(Nπ/η1)). The 8N term is exact:
    ∫_{|η|≤Nπ} 2|sin η| = 8N.
- **Cross term in band:** at most X_band = (1/π)·[β²κ/(4N) + (1−γ)(2/π²)(c/N)]·2c·Φ_γ(0), using
  |Φ_γ| ≤ Φ_γ(0) because φ_γ ≥ 0.
- **R² term:** at most C_R² over [−π, π]. In band it is dropped, which is valid because it is nonnegative.

Therefore

**λ0(N, c/N) ≥ (N·I_c/2π − X_band) / (N·I_tot/2π + X + C_R²).**

**Monotonicity.** Dividing through by N, each correction term (X_band/N, X/N, C_R²/N) decreases in N for N ≥ 800.
So the right-hand side increases in N, and a bound certified at N0 = 800 holds for every N ≥ 800. The review
checked this numerically over 200 log-spaced N up to 1e7.

**Certified evaluation.**
- **I_tot** is an exact rational series. Write φ_γ = Σ_k c_k(1−x²)^k with c_0 = 1−γ and
  c_k = (β²/4)^k/(k!)², and use ∫(1−x²)^m = 2^{2m+1}(m!)²/(2m+1)!. The series is truncated at k = 60 with a
  rational tail bound, and π is enclosed as [3.14159265358979323, …324].
- **I_c** uses a 50-digit decimal midpoint rule with error at most (2c)·h²·4Φ_γ(0)²/24. This rests on
  |Φ^(k)| ≤ ∫|x|^k φ_γ ≤ Φ_γ(0), so |(Φ²)″| ≤ 4Φ_γ(0)².

## 4. Part 4: implementation error

Every non-oracle gate is either Clifford+T exact or a rotation synthesised to ε_r = 2^-40 (Ross-Selinger,
arXiv:1403.2975). The rotations are:
- at most 2^g in the preparation tree, plus binary64 angle rounding of at most 4e-15 rad each;
- 2(g+1) for the offset;
- g(g−1) for the inverse QFT.

Operator-norm errors add, and a probability moves by at most 2× the state error. So the failure probability
rises by at most 1.9e-6 at the largest N used (2.98e5). The run002 certificate reserves 4e-6, and every cell is
asserted against it.

The rotation T cost is about 3.4e7 per shot, against about 2.3e13 T for the shot's Grover iterates.

## 5. Result (run002) and checks

| | δ = 0.003 | δ = 0.01 |
|---|---:|---:|
| β (Kaiser, γ = 0) | 3.87 | 3.19 |
| c certified, all N ≥ 800, parts 1-4 | 4.179 | 3.510 |
| k at B8x52 $0.001 (U1/U2 + direction-select) | 8.762 | 7.359 |

**Independent checks.**
- The exact discrete λ0 (FFT, float) at the binding N = 100,924 gives 1−λ0 = 2.97059e-3 ≤ 3e-3.
- The review's brute force over N from 800 to 300,007 found no violation. The margin is about 2.4e-5 at large N.

**Coverage.** 20 k cells have N < 800: all are ε = 0.10, split e = ε, and overhead-dominated, so none enters a
reported minimum (`results/frontier_probe_20261021/coverage/run001/coverage.json`).

## 6. Replacing the U1 mean credit with a quantum-only first stage (22 Oct)

The √(m(S−m)) error rule needs an upper bound m_U ≥ m with m_U ≤ S/2. U1 supplies it from an uncertified classical
price plus L1. The same certified estimator can supply it instead.

**Stage 1.** Run the window estimator with failure δ1 and phase half-width D1, and no mean credit. Worst case over
a, |â − a| ≤ D1/2 + D1²/4. Set a_U = â + D1/2 + D1²/4. With probability ≥ 1 − δ1,
a ≤ a_U ≤ a + D1 + D1²/2.

**Stage 2.** Run the estimator with failure δ2 and the mean bound m_U = S·a_U. The union bound gives δ1 + δ2 = 0.003.

**Cost.** N = ⌈c(δ1)/D1⌉ + ⌈c(δ2)/D2(m_U)⌉, taken at the worst stage-1 outcome. Stage 1 is raised to N0 = 800 when it
would be smaller, so the certificate covers it.

**Certified constants** (γ = 0 Kaiser, parts 1-4, all N ≥ 800):
- c(1e-4) = 6.052 (β = 5.72) and c(2.9e-3) = 4.197 (β = 3.88);
- also c(3e-4) = 5.433, c(2.7e-3) = 4.236, c(1e-3) = 4.777 and c(2e-3) = 4.400.

**Binding cell.** The optimum is δ1 = 1e-4 and D1 = 0.0035:
- 1,730 + 102,602 = 104,332 calls, so **k = 9.058** (U1: 8.762);
- the worst-case mean bound is 3.418, against the true 3.282.

Output: `results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json`; M rows in `derived/run003_self_mean`.

**Review notes (r3, `results/frontier_probe_20261021/review/r3_review.jsonl`; minor, adopted as text).**
- **Cap the mean bound.** Define m_U := min(S·a_U, S/2), so that stage 2 is defined even when stage 1 fails.
- **Read the cost as a worst case over stage-1 successes.** 104,332 calls (k 9.058) holds with probability ≥ 1 − 1e-4.
  With probability ≤ 1e-4, stage 1 fails and the capped stage 2 can take up to 182,785 calls (k 15.87). The error
  guarantee is unaffected (union bound 0.003).
- **Reproduced.** The reviewer re-certified c(1e-4) = 6.052 and c(0.0029) = 4.197 (each fails at −0.001) and
  reproduced k = 9.0577.
