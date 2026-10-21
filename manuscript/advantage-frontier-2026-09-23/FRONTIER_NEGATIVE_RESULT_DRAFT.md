# No certified tenfold: a scoped negative result and frontier for quantum pricing of a knock-out basket

**Draft manuscript, branch N of plan110 (N2).** 12 October 2026. Affiliation: VIT Vellore.
This is an **AI-assisted draft**. It does not assert author names, human approval, review
outcome or submission. It has not yet had the wave-2 adversarial review or the user's
sign-off that `research/plan110_n1/N1_CARD.md` requires.

**Number rule.** Every number below comes from an N1 result file (wave 1 of branch N) or is
a product or ratio of such numbers computed by the two drafter scripts. Each number carries
a label and a direction:

- labels: **meas** (measured), **mod** (modelled), **assm** (assumed), **lit** (literature,
  with citation);
- directions: **q+** (quantum-favourable), **q−** (against quantum), **0** (neutral).

Where an N1 value differs from the W0 value, the N1 value is used and the difference is
listed in §9. Where the three N1 workstreams disagree with each other, both values are given
and the disagreement is listed in §9.

Source keys (paths relative to the repository root):

| Key | File | Producer |
|---|---|---|
| [HT] | `results/plan110_n1/headline/headline_table.json` | N1-headline, `headline_m.py` |
| [RC] | `results/plan110_n1/headline/receipt.md` | N1-headline receipt |
| [KF] | `results/plan110_n1/headline/keff.json` | N1-headline, `e07_keff.py` |
| [FS] | `results/plan110_n1/headline/floor_sheet.json` | N1-headline, `floor_sheet.py` |
| [ES] | `results/plan110_n1/estimator/estimator_recompute.json` | N1-estimator, `recompute_estimator.py` |
| [EC] | `research/plan110_n1/estimator/estimator_card.md` | N1-estimator card |
| [HW] | `results/plan110_n1/hwclassical/hw_classical_card_v2.json` | N1-hwclassical, `hw_classical_v2.py` |
| [HC] | `research/plan110_n1/hwclassical/hw_classical_card.md` | N1-hwclassical card |
| [DN] | `results/plan110_n1/drafter/draft_numbers.json` | this draft, `draft_numbers.py` (copies and identity checks only) |
| [AD] | `results/plan110_n1/drafter/addendum.json` | this draft, `draft_addendum.py` (cross-workstream products) |
| [W0C] | `research/plan110_w0/W0_CARD.md` | conventions (W0) |
| [REG] | `results/plan110_w0/register/run001/REGISTER.md` | 110-item register (W0, R0) |

All scripts whose numbers appear here ran under `.context/frontier_t0_env/Scripts/python.exe
-I -S -B` (Python 3.12.4, standard library only).

---

## Abstract

We ask whether any quantum amplitude-estimation design can price one fixed, discretely
monitored basket knock-out call, in a 4-asset × 12-date case (B4x12) and an 8-asset ×
52-date case (B8x52), with at least ten times lower complete latency than the strongest
classical method we tested, to $0.01 or $0.001 per $100 notional at 99% confidence. We
compare a quantum machine of 1e7 logical qubits, 100 ns logical layers and 1e12 T states
per second against one measured 16-core CPU.

We write the requirement as one ratio, M = k / k_10x:
- k is the estimator constant achieved (controlled Grover calls per σ/e);
- k_10x is the largest constant that still gives a tenfold win, given an idealized
  oracle-call depth floor and the measured classical time.

M ≤ 1 means tenfold is reached. In the most quantum-favourable eligible cell (B8x52 at
$0.001), M has three values, one per estimator class:

| Estimator class | M |
|---|---:|
| Certified today | **801.5** |
| Best explicit worst-case constant (every conditional credit granted) | **232.0** |
| Window/QSP amplitude estimation, which has no usable explicit worst-case constant | **8.62** |

All three are modelled, and two R1 recomputes along different paths confirm them.

**Claim:** "No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52 knock-out task under the stated conventions."

This is an achievability statement, not a query lower bound. The rigorous black-box lower
bound on k is only about 1.7-1.85.

The result is fragile in a specific way: one idealized change on each side of the
comparison is enough to reach tenfold.
- The idealized all-free oracle plus a distribution-free classical confidence convention
  gives M = 0.31.
- The all-free oracle plus one quantum lane against one classical core gives M = 1.125.
  This becomes 0.97 if a newly identified, conditional direction-select credit is granted.

We name the levers that would overturn the result:
- an explicit worst-case constant for window/QSP estimation;
- an oracle near the idealized floor;
- a relaxed convention.

We also list the escapes that are closed.

---

## 1. Introduction and scope

The project's foundation document,
[WHY_NO_ADVANTAGE.md](WHY_NO_ADVANTAGE.md), explains why six constructions failed to
produce a significant advantage. Those six constructions span three option contracts and
were built with one toolchain (register item C12). This draft closes the last open
contract, the discretely monitored knock-out basket that Stage C measured
([STAGE_C_STATUS.md](STAGE_C_STATUS.md)), and turns it into a frontier statement.

The question is no longer whether one compiled circuit misses its budget. It is whether
**any** design in this construction family can reach tenfold once each of three ingredients
is pushed to its idealized limit:
- the oracle call;
- the estimator constant;
- the hardware.

The **scope** of the claim is the conjunction of three things (N1 card):
1. **This construction family.** A coherent fixed-point oracle for the payoff, wrapped in
   bounded amplitude estimation.
2. **The fixed task.** One discounted price of the contract in §2, for the two cases.
3. **The strongest tested classical method.** Preintegration plus RQMC on a 16-core CPU,
   with practice confidence intervals.

The claim does not say that quantum advantage in option pricing is impossible. It does not
cover other tasks, other access models or untested classical challengers (§8).

---

## 2. The task and its conventions

**Contract.** An equal-weight basket knock-out call, with S0 = K = 100, barrier H = 140,
σ = 0.3, ρ = 0.4, r = 0.03 and T = 1. It is discretely monitored on 12 dates over 4 assets
(B4x12) and on 52 dates over 8 assets (B8x52). These are the Stage C development cases
(STAGE_C_STATUS.md glossary).

**Payoff and error.**
- The payoff support is audited at [0, 38.818] (E03, as used in [EC] §1).
- The quantum-side payoff standard deviation is σ_q = 5.66357 for B4x12 and 5.18340 for
  B8x52 (meas, 0) [EC].
- The output is one price within ε ∈ {$0.10, $0.03, $0.01, $0.001}, with 99% confidence.
- Only ε = $0.01 and $0.001 are decision cells. The larger ε values are dominated by
  classical fixed overhead.

**Conventions.** These were fixed in [W0C] on 11 October 2026. The primary value is used
for the claim; every other value is a sensitivity column.

| Convention | Primary | Sensitivity columns |
|---|---|---|
| Parallelism matching | One quantum machine against one 16-core classical machine. Quantum lanes are allowed only inside the width budget | 1 lane vs 1 core; L lanes vs 16 cores |
| Classical confidence | Practice confidence intervals, as in Stage C | Distribution-free 99%, symmetric with the quantum worst-case guarantee |
| Width budget W | 1e7 logical qubits | 1e6, 1e8, unlimited |
| Magic-state supply | 1e12 accepted T states per second | 1e11, 1e13 |
| Logical layer time | 100 ns | 10 ns, 1 µs, 10 µs |
| Statistical split | e = 0.45 ε | e = ε (zero deterministic bias) |
| B8x52 at $0.001 | Eligible at zero deterministic bias (q+) | Ineligible under the current $0.00124 bias bound |

The **classical time T_C** is the minimum measured "primary" wall time over Stage C items
C2 (preintegration, RQMC) and C5 (`oss_bb`, `oss`), with a monotone envelope across ε
[RC]. In the decision cells it is (meas, 0) [HT]:

| Cell | T_C |
|---|---:|
| B4x12 $0.01 | 0.1244 s |
| B4x12 $0.001 | 2.688 s |
| B8x52 $0.01 | 0.5535 s |
| B8x52 $0.001 | **22.529 s** |

---

## 3. The inequality and the gap ledger

Let D_eff be the effective depth of one controlled Grover iterate, in reaction layers:

> D_eff = max(reaction depth, T per iterate / (supply × t_layer))

The largest per-call depth that still gives a tenfold win, written for k = 1, is

> D_max(k=1) = T_C / (10 · (σ/e) · t_layer).

The largest estimator constant that still gives tenfold is k_10x = D_max(k=1) / D_eff, and

> **M = k / k_10x.**  M ≤ 1 means a 10× complete-latency win.

This is the depth form of the single inequality in WHY_NO_ADVANTAGE.md §2.4. It now
separates the oracle (D_eff), the estimator (k) and the hardware (t_layer and supply).

**Gap ledger at the binding cell, B8x52 at $0.001, primary conventions:**

| Quantity | Value | Label | Source |
|---|---:|---|---|
| T_C | 22.529 s | meas, 0 | [HT] |
| σ/e | 11,518.7 | mod (σ measured), 0 | [HT] |
| D_max(k=1) | 1,955.9 layers | mod, 0 | [DN] |
| D_eff, W0 floor (used) | 2,296 layers, supply-bound | mod, q+ | [HT] |
| D_eff, N1 floor (not used here) | 3,605 layers, supply-bound | mod, q+ | [HT] |
| k_10x | 0.852 | mod, 0 | [DN] |
| k: certified today / best explicit / window (failure 0.01) / window (failure 0.003) | 682.7 / 197.6 / 7.34 / 8.74 | mod | [HT] |
| **M: certified / explicit / window (0.01) / window (0.003)** | **801.5 / 232.0 / 8.62 / 10.26** | mod, 0 | [HT] |

Two features of the ledger matter for everything that follows.

1. **Even k = 1 fails.** k_10x is below 1 (0.852): even an estimator with k = 1, below the
   rigorous black-box floor of about 1.85 for B8x52 (§5.3), would miss tenfold at the
   primary conventions.
2. **The explicit miss has two hardware factors** [HC §2], [DN]. M = 232.0 splits as
   74.8 × 3.10:
   - **74.8 is layer time.** At the idealized Box-Muller floor of 740 layers, the
     required layer time is 1.34 ns instead of 100 ns.
   - **3.10 is magic-state supply.** At 1e12 T/s one call is supply-limited at 2,296
     layers instead of 740.

   So faster layers alone do not help at this cell. At 10 ns the binding-cell M stays
   232.0, because the call remains supply-bound [HT]. The 10 ns column improves only the
   B4x12 cells, to a minimum of 197.8.

---

## 4. Results

### 4.1 The oracle floor, and why supply binds

**Method** (N1, [RC], [FS]; all mod, q+). The N1 floor is an analytic formula sheet built
from cited literature constructions. It shares no code with W0's WS-floor.

- **Gate costs.**
  - A logical AND costs 4 T and one reaction layer (Jones, PRA 87, 022328 (2013); Gidney,
    Quantum 2, 74 (2018)).
  - Clifford gates take no time (Fowler, arXiv:1210.4626).
- **Arithmetic.**
  - Adders are Kogge-Stone; multi-operand sums use Dadda 3:2 trees.
  - Multiplications are truncated fused multiply-adds; constant multiplications use
    canonical signed digits.
  - Coefficient lookup is QROM (Babbush et al., PRX 8, 041015 (2018)).
  - Functions are piecewise Chebyshev polynomials evaluated by Estrin's scheme, sized to
    a 2^-41 error bound.
- **One Grover iterate** is one uncompute, one compute and the S0 reflection. Only the
  reflections are controlled.
- **Width.** Under the width budget, every stage either keeps or cleans its garbage, and
  all keep/clean combinations are enumerated.

**Floor values** (mod, q+) [FS], [DN]:

| | B4x12 | B8x52 |
|---|---:|---:|
| Compute critical path | 270 layers | 278 layers |
| T per compute | 2.26e7 | 1.87e8 |
| Box-Muller share of the compute path (144 layers) | 53% | 52% |
| Grover iterate at W = 1e7, 1e12 T/s, 100 ns | 563 layers, reaction-bound | 1,409 layers and 3.61e8 T: **supply-bound**, D_eff = 3,605 |
| Same at unlimited width | 563 layers | 585 layers and 1.88e8 T: supply-bound, D_eff = 1,875 (5.03e7 qubits) |
| Compute path with all-free oracle (free loader and exponential, 48-bit words) | 59 layers | 67 layers |

**Comparison with W0.** The two floors differ by more than 10% in 165 of 180 convention
pairs [RC].

- **At the primary conventions, N1 is less favourable:** 563 against 364 (B4x12), and
  3,605 against 2,296 (B8x52). The main cause is that N1 places a carry-propagate adder
  after every Estrin level and uses 72-bit words.
- **N1 is more favourable in 33 pairs.** These include B8x52 at unlimited or 1e8 width:
  1,875 against 2,296.
- **Rule.** The decision uses the more quantum-favourable floor in every pair [RC].
- **Effect.** The claim therefore uses the smaller of two independent floors. With N1's
  floor alone, the binding-cell M values rise to 1,258 (certified), 364.2 (explicit) and
  13.5 (window, 0.01) [HT].

**Supply binds before depth for B8x52.** At 1e12 T/s and 100 ns, the B8x52 iterate cannot
issue its T gates fast enough on either floor. That is why the 3.10 supply factor in §3
exists. The required rate is 3.3e14 T/s at the explicit constant [HW] (§4.3).

### 4.2 The estimator constant bracket and its access model

**Access model** [EC] §1.
- **What the estimator may touch.** It has black-box access to the state-preparation
  unitary A, where A|0⟩ = √(1−a)|ψ₀⟩|0⟩ + √a|ψ₁⟩|1⟩ and the mean is μ = S·a. It may use
  controlled Q = −A S₀ A† S_χ, Q⁻¹, or a direction-select between them, plus query-free
  operations.
- **What it must guarantee.** |μ̂ − μ| ≤ e with probability at least 1 − δ, for every
  payoff law on [0, S].
- **Cost unit.** One controlled Grover iterate.
- **Failure allocation.** The estimator's share is δ = 0.003, the E07 allocation, unless
  stated otherwise.

**Certified today** (mod, exact; σ meas; 0) [KF], [EC] §2a.
- The schedule is canonical BHMT Theorem 12 with 15 medians, span 64 and dyadic M.
- N1 reproduces the saved certificate exactly: M = 65,536 and 15 medians give **983,025
  controlled Grover calls** at ε = $0.01.
- π is enclosed with BBP in [KF] and with an Euler series in [ES]; the median tail is an
  exact convolution.
- Certified k = **585.8-1,066.7** over all cells at e = 0.45 ε.

**Best explicit worst-case 99% constant: k = 186.6-198.2** (mod, q+) [EC] §2b. This needs
three conditional credits, none of which is certified yet:
1. **The U2 support-tight wrapper** (span 8192/211 = 38.82). The audited support exists;
   the wrapper circuit and its readout bound do not.
2. **The U1 mean certificate**, m ≤ price + L1. The price is an uncertified RQMC value
   (assm), and the B8x52 L1 is borrowed from B4x12.
3. **Non-dyadic M.** This needs a QFT over Z_M. BHMT Theorem 12 holds for any integer M.

Partial combinations [EC]:
- 323-353 without the mean certificate;
- 195-341 with dyadic M.

**New conditional credit: direction-select control, about ×2** (mod, q+) [EC] §2b.
- **The argument.** Replacing Q^j by Q^(j−c) in BHMT's construction multiplies each
  eigen-branch by a global phase only. The outcome distribution, and so Theorem 12, is
  unchanged. A shot then costs M/2 calls instead of M − 1.
- **The one missing certificate** is a call cost: a direction-select iterate must cost no
  more than one controlled Grover iterate. That cost is assumed here.
- **Effect.**
  - Certified-schedule k: 293-533 (491,520 calls at $0.01).
  - Best k: 98-171.
  - Primary M at the binding cell: 801.5 → 400.7 (certified) and 232.0 → 200.4
    (explicit) [ES].

**Window/QSP estimation: k ≈ 7-26, with no usable explicit worst-case constant** (mod, q+)
[EC] §2c. The DPSS window constant is c = 4.168 at δ = 0.003 and 3.502 at δ = 0.01. N1
confirmed it to 1e-12 by power iteration, a different algorithm from W0's.

| Setting | k |
|---|---|
| δ = 0.003, no credits | 23.5-25.7 |
| δ = 0.003, with U1/U2 | 8.25-8.74 |
| δ = 0.01, with U1/U2 (the DP1 row) | 6.93-7.34 |

The primary sources fall short of an explicit worst-case constant (lit) [EC] §4:
- Berry et al. (arXiv:2209.13581) App. D is approximate throughout.
- Patel et al. (arXiv:2403.18927) Thm 3 is asymptotic, with N₀ unspecified.
- Patel Thm 2 is explicit but average-case. A random known register offset makes it
  worst-case (N1 argument), but at k = 6.8e5-9.3e5, about 1e5 times too large [ES].
- Rall & Fuller (arXiv:2207.08628) give fits at a = 0.5 and 95%, not a worst-case 99%
  constant.

**Other explicit theorems are worse than canonical** (lit, q−) [EC] §2b. Grinko et al.
(arXiv:1912.05559) Thm 1 gives k = 2,997-5,755, and Fukuzawa et al. (arXiv:2208.14612)
Lemma 3.7 gives about the same. No Bayesian or likelihood design (E25) has a worst-case
coverage theorem with an explicit constant in the sources checked.

**Counting lower bound** (mod, rigorous; q+) [EC] §1, [DN].
- **The hard family.** A_θ = R_y(2θ) has θ-independent eigenvectors. This meets the
  premise of Mande & de Wolf (arXiv:2305.04908v3) Claim 5.3, and gives (1 − δ)K ≤ 2N + 2
  with one free copy of A|0⟩.
- **Values at δ = 0.01** (support class, Q-access): k_LB = 1.687-1.696 for B4x12 and
  1.843-1.853 for B8x52.
- **Weaker access or narrower classes.** Under A/A† access the bound halves to 0.85 / 0.93.
  For a mean-bounded class it falls to 0.15-0.16.
- **What it does not bind.** White-box estimators that use the known source code.

So between the rigorous floor of about 1.85 and the best explicit constant of about 198 lies
a gap of about two orders of magnitude, and it is not established that this gap is real.
This is the reason the claim is worded as achievability (§7).

**Lanes at W = 1e7** (mod, q+) [EC] §3, [ES].
- **Only one primary floor design fits.** The designs are 5.28M qubits wide (B4x12) and
  10M wide (B8x52).
- **Lane credit with the 1e12 T/s supply shared:**
  - 1.00× for B8x52;
  - 1.29× for B4x12, capped by total T ÷ supply;
  - with unlimited supply, B4x12 reaches 3.36× and B8x52 stays at 1.00×.
- **Window chains are one coherent chain**, so they get no lane credit.
- **Consequence.** The binding cell gets no lane credit under any modelled supply.

### 4.3 Classical parallelism, classical confidence, and hardware coverage

**Classical parallelism, H16** (meas) [HT], [HC] §4. The speedup from 1 to 16 workers on
the Intel Core Ultra 7 155H is:

| Cell | Speedup |
|---|---:|
| B4x12 $0.01 | 6.44× |
| B4x12 $0.001 | 9.36× |
| B8x52 $0.01 | 7.38× |
| B8x52 $0.001 | 10.24× |

The parallel efficiency is 0.40-0.64, and the 16-worker times reproduce Stage C within
4-10%. Matching one quantum lane against one core therefore helps quantum by 6.4-10.2×, not
16×. The minimum explicit M becomes 22.7 (mod, q+).

**Classical confidence, C09** (mod from meas inputs; the column is q+ because it slows the
classical side) [HW], [HC] §4.
- **Why the convention matters.** The quantum k is already a worst-case 99% guarantee over
  a bounded range. A symmetric convention therefore slows only the classical side.
- **The distribution-free route.** It uses a two-sided empirical Bernstein bound (Maurer &
  Pontil 2009, Thm 4) at δ = 0.01 and payoff range $40 (assm). It uses iid preintegration
  with the measured σ_preint of 1.248 (B4) and 1.146 (B8), and the measured per-point cost
  of 1.15 µs and 10.4 µs at 16 workers.
- **Factor over the practice time:**

| Cell | Factor |
|---|---:|
| B4x12 $0.001 | 40.3 |
| B8x52 $0.001 | **36.9** |
| B4x12 $0.01 | 10.6 |
| B8x52 $0.01 | 18.9 |

- **Resulting M at the binding cell:**

| Floor | Certified | Best explicit |
|---|---:|---:|
| Box-Muller | 21.7 | **6.29** |
| All-free | 1.08 | **0.31** |

- **Why the factor is not netted against quantum.** The triage note's "quantum needs
  10-20× more calls" is already inside W0's span-normalised k. Subtracting it again would
  count it twice.

**Coverage, C10** (0; strengthens the negative) [HC] §4.
- **Label.** The comparator is the strongest *tested* method.
- **Untested challengers:**
  - GPU code;
  - PDE, finite-difference and sparse-grid solvers;
  - multilevel and multi-index MC/QMC;
  - control variates;
  - importance sampling;
  - compiled kernels;
  - surrogates.
- **Why leaving them out is conservative.** A faster eligible challenger lowers T_C, which
  lowers k_10x and raises M. The negative is monotone in the classical side.

**Hardware coverage** (lit; the convention is q+) [HW], [HC] §1-3. The 100 ns layer is
faster than every verified anchor:

| Anchor | Value | 100 ns is faster by |
|---|---:|---:|
| Liu et al. (arXiv:2603.16203): decode-to-feedback pipeline, no qubits | 446 ns | 4.5× |
| Yang et al. (arXiv:2605.04892): the only demonstrated complete readout-to-feedback loop, d = 3 | 550 ns | 5.5× |
| Willow d = 7 QEC cycle (arXiv:2408.13687) | 1.1 µs | 11× |
| Projected d = 25 cycle (arXiv:2505.15917) | 1 µs | 10× |
| Projected application-scale reaction time | 10 µs | 100× |
| Projected application-scale CCZ period | 25 µs | 250× |

What the binding cell would need for tenfold (mod) [HW]:

| Estimator and floor | Layer time | T rate | Width |
|---|---:|---:|---:|
| Explicit constant (197.6) | 1.34 ns | 3.3e14 T/s, 326× the budget | 1e7 qubits |
| Certified (682.7) | 0.39 ns | 1.1e15 T/s | 1e7 qubits |
| Window (7.3) | 36 ns | 1.2e13 T/s | 1e7 qubits |
| Explicit constant, all-free floor | 8.8 ns | 1.3e13 T/s | 1.85e6 qubits |

Rate and width anchors (lit, derived):
- about 2.4e5 CCZ/s (arXiv:2505.15917);
- about 3e4 T/s (arXiv:2510.26078);
- 48 demonstrated logical qubits (arXiv:2312.03982).

---

## 5. The decision table

### 5.1 Primary M

Minimum M over eligible, non-overhead cells. The binding cell is B8x52 at $0.001 in every
row. All values mod [HT], [ES], [AD].

| Estimator class | k at the binding cell | **M, primary** | Status of the constant |
|---|---:|---:|---|
| Certified today (E07 schedule) | 682.7 | **801.5** | Certified |
| Certified schedule with direction-select | n/a | 400.7 | Call cost assumed |
| Best explicit (U1 + U2 + non-dyadic M) | 197.6 | **232.0** | Three conditional credits |
| Best explicit at a consistent failure of 0.01 | 144.9 | 170.1 | As above; 11 medians |
| Best explicit with direction-select | n/a | 200.4 | As above, plus the assumed call cost |
| Window/QSP, failure 0.01 (the DP1 row) | 7.34 | **8.62** | No usable explicit worst-case constant |
| Window/QSP, failure 0.003 (like for like) | 8.74 | 10.26 | As above |

**Verdict at R1:** the claim holds under the primary conventions. Every class with an
explicit constant misses by more than 170×. The window class misses by 8.6-10.3×, and it
has no explicit constant.

### 5.2 One favourable departure at a time

These are the explicit-best minima from [HT], except the C09 rows from [HW].

| Departure | M | Direction |
|---|---:|---|
| Primary | 232.0 | n/a |
| All-free oracle (free loader and exponential, narrow words) | 11.5 | q+ |
| 1 lane vs 1 core (H16, meas) | 22.7 | q+ |
| Distribution-free classical, quantified from Stage C (36.9× at the binding cell) | **6.29** | q+ |
| Distribution-free classical ×5 / ×2 (assm, W0's C09 range) | 46.4 / 116.0 | q+ |
| Supply 1e13 T/s | 74.8 | q+ |
| e = ε (zero deterministic bias) | 104.4 | q+ |
| Estimator failure 0.01 | 170.1 | q+ |
| W = 1e8 or unlimited (N1 floor) | 189.5 | q+ |
| 10 ns layers (minimum at B4x12; B8x52 stays at 232.0) | 197.8 | q+ |
| B8x52 $0.001 ineligible (current bias bound) | 318.0 (B4x12) | q− |
| Supply 1e11 / W = 1e6 / 1 µs / 10 µs | 1,978 / 648 / 748 / 7,476 | q− |

For the window class [HT]:
- the all-free oracle alone gives 0.43 at failure 0.01, or 0.51 at 0.003;
- 1 lane vs 1 core alone gives 0.84 at failure 0.01, or 1.002 at 0.003.

### 5.3 Minimal stacked departures to M ≤ 1

**With W0's assumed C09 factors (×2/×5)** [HT], [RC], the explicit class needs **three**
departures:

| Departures | M |
|---|---:|
| All-free + 1 lane vs 1 core + distribution-free ×5 | 0.225 |
| All-free + e = ε + 1 lane vs 1 core (DP1's example; DP1 gave 0.51) | 0.506 |
| All-free + 1 lane vs 1 core + 10 ns | 0.714 |
| All-free + 1 lane vs 1 core + failure 0.01 | 0.825 |

The best pair is all-free + 1 lane vs 1 core, at **M = 1.125**. The certified class also
needs three: all-free + 1 lane + distribution-free ×5 gives 0.777. Its best pair gives
3.89.

**With the Stage-C-quantified C09 factor** [HW], **two** departures suffice for the
explicit class:
- all-free oracle + distribution-free classical gives **M = 0.31**;
- the certified class with the same pair gives 1.08, still just above 1.

**With the conditional direction-select credit** [AD] (derived here as products of [HT],
[ES] and [HW] values; mod, q+):

| Departures, with direction-select | M |
|---|---:|
| All-free + 1 lane vs 1 core, explicit class | **0.97** |
| All-free + distribution-free (Stage C), explicit class | 0.27 |
| All-free + distribution-free (Stage C), certified schedule | 0.54 |

**Reading.** The DP1 memo's "at least three stacked departures" holds only under W0's
assumed C09 range and without direction-select. With the N1 measurements, two idealized
departures are enough: one on the oracle (the all-free floor) and one on the comparison
convention. Neither departure is part of the primary conventions. The all-free oracle is an
idealization that no construction in this project approaches (§6). The claim is therefore
unchanged, but the manuscript must not describe the margin as "three departures".

---

## 6. The frontier: what would overturn the result

Each lever below is stated with the size of its effect at the binding cell.

1. **An explicit worst-case 99% constant for window/QSP amplitude estimation.**
   - This alone moves M from 232 to 8.62-10.26 [HT]. It does not reach 1 at the primary
     oracle floor.
   - The precise open problem [EC] §5 has five parts:
     1. For every amplitude, N ≤ c(δ)/Δ + c₀ calls with explicit c(δ) and c₀, valid for
        all N or for an explicit N₀ below the smallest N the task uses.
     2. A certified lower bound on the window concentration λ₀(N, Δ) ≥ 1 − δ at the N
        actually used. This could be an interval-arithmetic computation rather than new
        mathematics.
     3. A worst-case phase bound that includes the finite QFT grid.
     4. Every finite-size error inside δ.
     5. Alternatively, a proven worst-case coverage statement for QSP/ChebAE.
   - Target: c(0.003) ≈ 4.2, which means k ≈ 8.7 with the U1/U2 credits and about 26
     without.
   - We do not claim this problem is hard, only that no primary source we checked supplies
     the constant.
2. **An oracle near the idealized all-free floor.** This alone moves the explicit M from
   232 to 11.5 [HT].
   - Combined with lever 1, it gives the window-class M of 0.43-0.51 [HT].
   - The all-free floor assumes a free Gaussian loader, a free exponential and 48-bit
     words. Its compute path is 67 layers against 278 for the current law (B8x52 [FS]).
   - Box-Muller alone is about half of the current-law path (§4.1).
3. **A relaxed convention.**
   - A distribution-free classical convention gives M = 6.29 (explicit) [HW].
   - One lane against one core gives 22.7 [HT].
   - A supply of 1e13 T/s gives 74.8 [HT].
   - A 10 ns layer does nothing at the binding cell unless supply also rises (§3).
   - Any one of these, stacked with lever 2, reaches or nearly reaches M = 1 (§5.3).
4. **Smaller conditional credits.** They change M by less than 2× and do not overturn the
   result alone [ES], [HT]:
   - direction-select: 232 → 200;
   - estimator failure 0.01: 232 → 170;
   - lanes: 1.00× at B8x52, at most 1.29× at B4x12.

**What a hardware programme would have to show.** For the explicit constant at the
Box-Muller floor: a 1.34 ns logical layer, 3.3e14 accepted T states per second and 1e7
logical qubits, simultaneously [HW]. The best verified complete loop is 550 ns at d = 3.

---

## 7. Closed escapes

These routes were examined and closed for this task. They are cited so that a reader does
not reopen them without new evidence.

- **E22: log-domain QSP on the payoff predicates.** The register records 0 of 3,106 actual
  payoff predicates as eligible [REG] (W0 count, not recomputed in N1). It is closed as a
  negative.
- **F05: free coherent loading ("even with free loading").** The all-free oracle, which
  includes a free loader, still gives explicit M = 11.5 [HT].
- **F20: control variates as a σ credit ("even with a free control").**
  - A control reduces σ. But the bounded estimator's k is span-normalised, so a σ credit
    lowers the call count only for a σ-normalised estimator.
  - No explicit-constant source supplies a σ-normalised estimator. The DP1 table run001
    wrongly included this credit; run002 removed it (DP1 memo).
  - The counting bound (§4.2) also does not bind such white-box escapes. They remain
    outside the claim, not refuted.
- **F04: structured integration of a certified residual.** It closes with F20 [REG].
- **C14: the "2×" per-call depth reading.** Per-call depth is one Grover iterate, as used
  throughout. The DP1 memo (`docs/program_plan_20261010/DP1_MEMO.md`, WS-small) records
  the "2×" reading as wrong.
- **Lanes, E20.** No lane credit at the binding cell (§4.2).
- **Latency lines H14, H04 and H07** [HC] §3:
  - a GHz photonic clock is not a logical-layer time;
  - constant-round fault tolerance still pays at least one syndrome round plus decoding per
    layer, about 1 µs on superconducting hardware;
  - the projected cat-qubit cycle is 500 ns.

**Parked as a different task.** Twenty-five register items need a different output
contract, model or deliverable [REG]:
- E10, E14-E19;
- F09-F19;
- F21, F22;
- F26-F29;
- F32.

They include nested estimation, multilevel and Heston corrections, heavy tails, rough
volatility, Greeks, multi-output portfolios and quantum walks. They are outside the claim,
not refuted by it. Following register item C12, the earlier failures in
WHY_NO_ADVANTAGE.md are labelled **six constructions, three contracts, one toolchain**.
They are not six independent confirmations.

---

## 8. Limitations and scope

- **Achievability only.** Between the rigorous black-box floor (k ≈ 1.7-1.85) and the best
  explicit constant (about 198) there is about a 100× gap. The claim says only that no
  design with certified constants is known to close it under these conventions.
- **Conditional credits are granted, not certified.** The 232 row already assumes three
  uncertified credits (§4.2), so the certified-constant claim is in fact carried by a
  stronger margin (801.5). Granting the credits makes the negative more conservative,
  not less.
- **Two idealized floors.** The floor is idealized: Clifford gates and routing are free,
  and the leaf constants come from the literature. N1's independent floor is 1.55-1.57×
  less favourable than W0's at the primary conventions. Using the more favourable floor
  per pair keeps the claim conservative, but the two floors disagree by more than 10% in
  165 of 180 pairs [RC], so neither is a tight bound.
- **Rigour level.** The headline is R1 (an independent recompute plus a receipt).
  - The N1 card justifies R1 over R2 by the primary margin of at least 30×.
  - Under the Stage-C distribution-free sensitivity, the margin falls to 6.29, below that
    30× threshold [HC] §5.
  - The primary margin is unchanged, but a reviewer may reasonably ask for R2.
- **Classical side.** Classical T_C is measured on one laptop CPU (16 workers), with
  practice confidence intervals. The strongest tested method is not the strongest
  applicable method (C10), but untested challengers can only raise M.
- **The distribution-free factor** uses an assumed payoff range of $40 ($64 as a
  sensitivity) and an empirical Bernstein bound. A betting confidence sequence could lower
  it by up to about 12% [HC] §4.
- **Hardware anchors.** Two anchors remain repository citations not verified within the
  fetch cap:
  - the neutral-atom 0.5-4 ms layer time;
  - the active-volume reaction time of about 1 µs.
- **Scope.** One contract (two cases), one construction family, one access model. Nothing
  here transfers to other payoffs without recomputing every term of the ledger.

---

## 9. Discrepancies

### 9.1 N1 against W0 (the N1 value is used)

1. **Floors.** N1 and W0 differ by more than 10% in 165 of 180 pairs. The more favourable
   value is used per pair. N1 is more favourable at B8x52 with W ≥ 1e8: explicit M = 189.5
   instead of 232 [RC].
2. **Mixed failure allocation in WS-k.** The window row (8.62) uses failure 0.01, while
   the explicit row (197.6) and E07 use 0.003. Like for like, the values are 10.26
   (window, 0.003) or 170.1 (explicit, 0.01) [RC], [EC].
3. **C09 factor.** W0 assumed 2-5×. Stage C data give 10.6-40.3×, so the distribution-free
   explicit M is 6.29, not 46-116 [HC].
4. **Number of departures.** DP1 says at least three; two suffice (0.31, §5.3) [HC].
5. **Direction-select.** WS-k said "no theorem covers" it. BHMT Thm 12 does, so it is a new
   conditional credit of about ×2 [EC].
6. **Counting bound.** W0 quoted "about 1.7-1.85" without an access model. The values hold
   for Q-access plus one copy of A|0⟩, and fall to 0.85/0.93 under A/A† access [EC].
7. **"No explicit constant".** W0's "no explicit constant in any primary source" becomes "no
   *usable* explicit worst-case constant": Patel Thm 2 plus a random offset is explicit but
   about 1e5× too large [EC].
8. **WS-k lane figures** mix source widths with floor depths. The corrected credit is 1.00×
   for B8x52 and 1.29× for B4x12 [EC].
9. **Register H01/H02 wording.** It calls Liu's 446 ns a complete readout-to-feedback loop.
   It is a partial pipeline with no qubits; only Yang's 550 ns is complete [HC].
10. **W0 decision summary quirk.** At B4x12 $0.03 it prints the raw T_C of 0.12677 s, but
    its k_10x uses the envelope value of 0.12440 s. M is unaffected [RC].
11. **W = 1e6.** The N1 floor is infeasible for B8x52 (persistent registers alone take 3.4e6
    qubits), so W0's D_eff of 11,034 is used [RC].

### 9.2 Between N1 workstreams (both values reported)

12. **Minimal departures.**
    - N1-headline: "no set of two reaches M ≤ 1" (best pair 1.125). This used W0's assumed
      C09 ×2/×5.
    - N1-hwclassical: two departures give 0.31, using the Stage-C factor.
    - Both are correct under their own inputs. This draft adopts the Stage-C factor
      because it is computed from measured inputs, not assumed.
13. **Direction-select was not carried into the headline enumeration.** Applied to the best
    headline pair, it gives 0.97 [AD]. This is a cross-product that no single N1 file
    contains. The wave-2 reviewer should confirm it with a headline rerun before the margin
    is quoted.

---

## Appendix A. The 110-item register

All 110 items of the programme have a W0 record, with disposition, trigger and
reopen/kill rule, in [results/plan110_w0/register/run001/REGISTER.md](../../results/plan110_w0/register/run001/REGISTER.md)
(machine-readable: `register.json`).

| Tier | Meaning | Count [REG] |
|---|---|---:|
| T1 | Decision-critical, done in W0 | 4 |
| T2 | Credited levers | 8 |
| T3 | Deferred certification debts | 12 |
| T4 | Closed or folded into N1 | 26 |
| T5 | Dormant with triggers | 35 |
| T6 | Parked as a different task | 25 |

How the register maps onto this draft:
- **§4.1 (oracle floor):** A01 and its parameter items.
- **§4.2 (estimator):** E01, C11, E03, E04, E08, E20 and E25.
- **§4.3 (classical and hardware):** H01, H02, H14, H16, H17, C09 and C10.
- **§3 (the ledger):** F31 and C14.
- **§7 (closed escapes):** E22, C12, F04, F05 and F20.

The register's dispositions are W0 (R0). This draft changes none of them; §9.1 item 9
records the one wording correction N1 found (H01/H02).

## Appendix B. Reproduction

Run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`, in this order:

1. **N1-headline:** `research/plan110_n1/headline/e07_keff.py`, then `floor_sheet.py`, then
   `headline_m.py`.
2. **N1-estimator:** `research/plan110_n1/estimator/recompute_estimator.py`.
3. **N1-hwclassical:** `research/plan110_n1/hwclassical/hw_classical_v2.py`. The v1 script
   is superseded.
4. **This draft:**
   - `research/plan110_n1/drafter/draft_numbers.py` copies the quoted values and checks 10
     arithmetic identities, with a maximum relative error of 1.8e-16 [DN];
   - `research/plan110_n1/drafter/draft_addendum.py` forms the direction-select
     cross-products [AD].

Every output file records the SHA-256 of its inputs. Each script creates its outputs with
exclusive create and refuses to overwrite them.
