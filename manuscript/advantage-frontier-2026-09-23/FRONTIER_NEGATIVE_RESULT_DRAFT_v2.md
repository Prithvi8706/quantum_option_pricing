# No certified tenfold: a scoped negative result and frontier for quantum pricing of a knock-out basket

**Draft manuscript v2, branch N of plan110 (N2 revision).** 12 October 2026. Affiliation: VIT Vellore.
This is an **AI-assisted draft**. It does not assert author names, human approval, review
outcome or submission. Version 1 (`FRONTIER_NEGATIVE_RESULT_DRAFT.md`, unchanged) had the
wave-2 adversarial review in `results/plan110_n1/review/REVIEW.md`, which listed 7 major and
14 minor defects. This version addresses each of them; the changelog at the end maps every
defect to its fix. This revision has not been re-checked by a reviewer, and it has not had
the user's sign-off that `research/plan110_n1/N1_CARD.md` requires.

**Number rule.** Every number below comes from an N1 result file (wave 1 of branch N), from
the N2 review files, or is a product or ratio of such numbers computed by the drafter, review
or fixer scripts. Each number carries a label and a direction:

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
| [DN] | `results/plan110_n1/drafter/draft_numbers.json` | v1 drafter, `draft_numbers.py` (copies and identity checks only; one known defective field, Appendix B) |
| [AD] | `results/plan110_n1/drafter/addendum.json` | v1 drafter, `draft_addendum.py` (cross-workstream products) |
| [NC] | `results/plan110_n1/review/number_check.json` | N2 review, `check_draft.py` (78 checks, `derived_for_review`) |
| [DC] | `results/plan110_n1/review/dirsel_confirm.json` | N2 review, `confirm_dirsel.py` (per-cell cross-products) |
| [FX] | `results/plan110_n1/fixer/fixer_numbers.json` | this revision, `research/plan110_n1/fixer/fixer_numbers.py` |
| [FX2] | `results/plan110_n1/fixer/fixer_numbers_2.json` | this revision, `research/plan110_n1/fixer/fixer_numbers_2.py` |
| [BD] | `research/plan110_w0/ws_small/README.md` §A1, numbers in `results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json` | W0 bias desk (R0) |
| [SPC] | `manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md` §0.4-0.5 | Stage C specification (bias labels) |
| [W0C] | `research/plan110_w0/W0_CARD.md` | conventions (W0) |
| [REG] | `results/plan110_w0/register/run001/REGISTER.md` and `register.json` | 110-item register (W0, R0) |
| [DP1] | `docs/program_plan_20261010/DP1_MEMO.md` (with its 12 October errata block) | DP1 decision memo |

**Provenance.** All N1, review and fixer scripts whose numbers appear here ran under
`.context/frontier_t0_env/Scripts/python.exe -I -S -B` (Python 3.12.4, standard library
only). The measured classical timings (T_C from Stage C items C2/C5, and the H16 worker grid)
come from the Stage C / H16 harness in the same environment, which uses numpy and numba and
is run without `-I` ([W0C]; `research/plan110_w0/ws_small/README.md`).

---

## Abstract

We ask whether any quantum amplitude-estimation design can price one fixed, discretely
monitored basket knock-out call, in a 4-asset × 12-date case (B4x12) and an 8-asset ×
52-date case (B8x52), with at least ten times lower complete latency than the strongest classical
method we tested, to $0.01 or $0.001 per $100 notional. We compare a quantum machine of 1e7
logical data qubits (magic-state factories not counted), 100 ns logical layers and 1e12 T
states per second against one measured 16-core CPU.

**The two sides are not held to the same confidence standard.** The quantum side must meet a
worst-case 99% guarantee. The classical side uses the practice confidence intervals of
Stage C (Student-t over 16 RQMC scrambles), which are not a guaranteed 99%. This asymmetry is
the primary convention the user chose. Holding the classical side to the symmetric,
distribution-free 99% standard slows it by about 37× (36.9×) at the binding cell, which is
the largest single convention lever in this paper (mod from meas inputs, q+) [HW].

We write the requirement as one ratio, M = k / k_10x:
- k is the estimator constant achieved (controlled Grover calls per σ/e);
- k_10x is the largest constant that still gives a tenfold win, given an idealized
  oracle-call depth floor and the measured classical time.

M ≤ 1 means tenfold is reached. The binding cell is B8x52 at $0.001. It is admitted on a
modelled, uncertified tightening of the stock clamp (deterministic bias $0.00047, inside the
0.55ε reserve), so the statistical share stays at e = 0.45ε (§2). M at the binding cell (all
mod) [HT], [HW], [DC], [FX]:

| Estimator class | M, primary (practice CIs) | M, symmetric distribution-free classical |
|---|---:|---:|
| Certified today | **801.5** (400.7 with direction-select) | 21.7 (10.9 with direction-select) |
| Best explicit worst-case constant (every conditional credit granted) | **232.0** | **6.29** (11.2 without the U1 mean credit) |
| Window/QSP amplitude estimation, which has no usable explicit worst-case constant | **8.62** (failure 0.01) / 10.26 (failure 0.003, like for like) | 0.23 (failure 0.01) |

N1 recomputed the estimator constants, classical times and M arithmetic exactly. The oracle
term is the smaller of two independent idealized floors, W0's (R0) and N1's (R1), which
differ by about 1.55×. With N1's floor alone, M is 1,258 / 364 / 13.5 [HT].

**Claim:** "No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52 knock-out task under the stated conventions."

Scope: this construction family (coherent fixed-point oracle plus bounded amplitude
estimation), the fixed task, and the strongest tested classical method. "Certified
constants" refers to the estimator constant; oracle costs are modelled idealized floors.
"Complete latency" here counts the Grover iterates only, not readout, reset, the inverse QFT,
decoding tail or classical post-processing (§8).

This is an achievability statement, not a query lower bound. The rigorous black-box lower
bound on k is only about 1.7-1.85.

**As a checkable threshold** (mod, derived) [FX]: at the binding cell and the primary
conventions, a design reaches tenfold with the best explicit constant only if one controlled
Grover iterate takes at most 9.9 reaction layers **and** at most 9.9e5 T gates; with
today's certified constant the limits are 2.9 layers and 2.9e5 T. The idealized all-free
oracle floor is 114 layers, so it would have to be beaten by a further 11.5× (explicit) or
40× (certified).

**The negative is robust only at the primary practice-CI convention.**
- Under the symmetric distribution-free convention, explicit M is 6.29 (11.2 without U1) with
  no oracle idealization. One oracle idealization (the all-free floor) plus this convention
  gives M = 0.31. For the certified class the same pair gives 1.08, or 0.54 with
  direction-select, whose call-cost condition is already met in this paper's cost model but
  is not certified for a compiled circuit. The window class, which has no usable explicit
  constant, reaches 0.23 under this convention alone.
- At the primary convention, one oracle idealization plus one quantum lane against one
  classical core gives M = 1.125, or 0.97 with direction-select.

We name the levers that would overturn the result: an explicit worst-case constant for
window/QSP estimation; an oracle near the idealized floor; a different comparison
convention; and a control-variate residual oracle whose payoff span has not been measured.
That last escape is open, not closed (§6, §7).

---

## 1. Introduction and scope

The project's foundation document,
[WHY_NO_ADVANTAGE.md](WHY_NO_ADVANTAGE.md), explains why six constructions failed to
produce a significant advantage. Those six constructions span three option contracts and
were built with one toolchain (register item C12). The sixth of them, Failure 6, is the
discretely monitored knock-out basket that Stage C measured
([STAGE_C_STATUS.md](STAGE_C_STATUS.md)). This draft turns that construction into a scoped
frontier statement.

The question is no longer whether one compiled circuit misses its budget. It is whether
**any** design in this construction family can reach tenfold once each of three ingredients
is pushed to its idealized limit:
- the oracle call;
- the estimator constant;
- the hardware.

The **scope** of the claim is the conjunction of three things (N1 card):
1. **This construction family.** A coherent fixed-point oracle for the payoff, wrapped in
   bounded amplitude estimation. The evidence covers oracles that cost at least the idealized
   floor (§4.1), which is a modelled construction, not a lower bound on every oracle. Stated
   as a checkable threshold (§3), the claim covers every design in this family whose Grover
   iterate at the binding cell costs more than about 10 reaction layers or more than about
   1e6 T (best explicit constant), or more than about 3 layers or 3e5 T (today's certified
   constant).
2. **The fixed task.** One discounted price of the contract in §2, for the two cases.
3. **The strongest tested classical method.** Preintegration plus RQMC on a 16-core CPU,
   with practice confidence intervals.

The claim does not say that quantum advantage in option pricing is impossible. It does not
cover other tasks, other access models, residual (control-variate) oracles or untested
classical challengers (§6-§8).

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
- The output is one price within ε ∈ {$0.10, $0.03, $0.01, $0.001}, with 99% confidence:
  worst-case 99% on the quantum side, practice confidence intervals on the classical side
  (see the table).
- Only ε = $0.01 and $0.001 are decision cells. The larger ε values are dominated by
  classical fixed overhead.

**Conventions.** These were fixed in [W0C] on 11 October 2026. The primary value is used
for the claim; every other value is a sensitivity column.

| Convention | Primary | Sensitivity columns |
|---|---|---|
| Parallelism matching | One quantum machine against one 16-core classical machine. Quantum lanes are allowed only inside the width budget | 1 lane vs 1 core; L lanes vs 16 cores |
| Classical confidence | Practice confidence intervals, as in Stage C (Student-t over 16 RQMC scrambles; not a guaranteed 99%). This is the convention that departs from symmetry: the quantum side carries a worst-case 99% guarantee | Distribution-free 99%, symmetric with the quantum worst-case guarantee. This is the stricter classical standard; it is q+ only because it slows the classical side |
| Width budget W | 1e7 logical **data** qubits ([W0C]); magic-state factories are outside W (q+) | 1e6, 1e8, unlimited |
| Magic-state supply | 1e12 accepted T states per second | 1e11, 1e13 |
| Logical layer time | 100 ns | 10 ns, 1 µs, 10 µs |
| Statistical split | e = 0.45 ε on both sides. The classical side is also held to 0.45ε although it carries no deterministic-bias reserve (labelled QF in [SPC] §0.4-0.5) | e = ε |
| B8x52 at $0.001 | Eligible on a modelled, uncertified clamp tightening: lowering the stock clamp 3 binades gives bias $0.000473 = 0.47ε ≤ 0.55ε [BD]. The primary therefore keeps e = 0.45ε (mod, q+). It needs an A02 bridge rerun and A07/A13 re-proofs | Strict zero-bias reading, e = ε: explicit 104.4, certified 400.7. Ineligible under the current certified bias bound of $0.00124: the binding cell moves to B4x12 $0.001, explicit 318.0 (q−) |

The **classical time T_C** is the minimum measured "primary" wall time over Stage C items
C2 (preintegration, RQMC) and C5 (`oss_bb`, `oss`), with a monotone envelope across ε
[RC]. Taking the minimum over noisy candidates is labelled classical-favourable in [SPC]
§0.5, so T_C is **meas, q−** here. In the decision cells it is [HT]:

| Cell | T_C |
|---|---:|
| B4x12 $0.01 | 0.1244 s |
| B4x12 $0.001 | 2.688 s |
| B8x52 $0.01 | 0.5535 s |
| B8x52 $0.001 | **22.529 s** |

At the binding cell, the H16 rerun's 16-worker time is 23.46 s, 4.1% higher (meas) [HW].
With it, explicit M would be 222.8 instead of 232.0 (mod) [FX]. The effect on M is at most
about 4%.

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
| T_C | 22.529 s | meas, q− (min over candidates) | [HT] |
| σ/e | 11,518.7 = 5.18340 / (0.45 × $0.001) | mod (σ measured), 0; the cell itself is admitted on an uncertified clamp tightening (q+, §2) | [HT], [FX] |
| D_max(k=1) | 1,955.9 layers | mod, 0 | [DN], [FX] |
| D_eff, W0 floor (used; R0) | 2,296 layers, supply-bound | mod, q+ | [HT] |
| D_eff, N1 floor (R1; not used here) | 3,605 layers, supply-bound | mod, q+ | [HT] |
| k_10x | 0.852 | mod, 0 | [DN] |
| k: certified today / best explicit / window (failure 0.01) / window (failure 0.003) | 682.7 / 197.6 / 7.34 / 8.74 | mod | [HT] |
| **M: certified / explicit / window (0.01) / window (0.003)** | **801.5 / 232.0 / 8.62 / 10.26** | mod, 0 | [HT] |

Three features of the ledger matter for everything that follows.

1. **Even k = 1 fails.** k_10x is below 1 (0.852): even an estimator with k = 1, below the
   rigorous black-box floor of about 1.85 for B8x52 (§4.2), would miss tenfold at the
   primary conventions.
2. **The explicit miss splits into supply and everything else** [HC §2], [DN], [FX].
   M = 232.0 = 74.8 × 3.10.
   - At unlimited supply (equivalently 1e13 T/s, where the iterate is reaction-bound at the
     740-layer Box-Muller floor) M would be **74.8**. This is the product of every non-supply
     term. Reaching tenfold then needs a 1.34 ns layer instead of 100 ns.
   - At 1e12 T/s, supply adds a further factor of **3.10**: one call is supply-limited at
     2,296 layers instead of 740.

   So faster layers alone do not help at this cell. At 10 ns the binding-cell M stays
   232.0, because the call remains supply-bound [HT]. The 10 ns column improves only the
   B4x12 cells, to a minimum of 197.8.
3. **The thresholds a design must beat** (mod, derived) [FX], [NC] `derived_for_review`.
   Because M = k · D_eff / D_max(k=1), M ≤ 1 needs D_eff ≤ D_max(k=1) / k. With
   D_eff = max(reaction depth, T / (1e12 T/s × 100 ns)), a design must meet **both** limits
   below on one controlled Grover iterate at the binding cell:

   | Estimator class (k at the binding cell) | Max reaction layers per iterate | Max T per iterate | Idealized all-free floor (114 layers, W0) is above the limit by |
   |---|---:|---:|---:|
   | Best explicit (197.6) | 9.90 | 9.9e5 | 11.5× |
   | Certified today (682.7) | 2.86 | 2.9e5 | 39.8× |
   | Certified schedule with direction-select (341.4) | 5.73 | 5.7e5 | 19.9× |
   | Window, failure 0.01 (7.34) | 266 | 2.7e7 | below the limit (M = 0.43) |

   The N1 all-free floor is 163 layers, 16.5× above the explicit limit [FX]. Under the
   symmetric distribution-free classical convention every limit rises by 36.9×: 365 layers
   and 3.7e7 T (explicit), 106 layers and 1.1e7 T (certified) [FX2]. The all-free floor
   (114) then lies inside the explicit limit, which is the M = 0.31 of §5.3.

---

## 4. Results

### 4.1 The oracle floor, and why supply binds

**Method** (N1, [RC], [FS]; all mod, q+). The N1 floor is an analytic formula sheet built
from cited literature constructions. It shares no code with W0's WS-floor. The citations
below were not re-fetched in N1 (lit, not re-fetched); their bibliographic details and the
uses made of them (4-T AND, free Cliffords, QROM) are standard.

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

The 52-53% Box-Muller share is N1's value; W0 reported the loader as 36-56% of its floor
(§9.1 item 12).

**Comparison with W0.** The two floors differ by more than 10% in 165 of 180 convention
pairs [RC].

- **At the primary conventions, N1 is less favourable:** 563 against 364 (B4x12), and
  3,605 against 2,296 (B8x52), ratios 1.547× and 1.570×. The main cause is that N1 places a
  carry-propagate adder after every Estrin level and uses 72-bit words.
- **N1 is more favourable in 33 pairs.** These include B8x52 at unlimited or 1e8 width:
  1,875 against 2,296.
- **Rule.** The decision uses the more quantum-favourable floor in every pair [RC]. Taking
  the minimum excludes the q− direction of the floor choice.
- **Effect.** The quoted 801.5 / 232.0 / 8.62 therefore use W0's floor, which is rigour R0.
  With N1's floor alone (R1), the binding-cell M values are 1,258 (certified), 364.2
  (explicit) and 13.5 (window, 0.01) [HT]. What R1 establishes is that both independent
  floors give M ≫ 30 at the primary conventions; it supports the verdict, not the exact
  quoted values.

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
2. **The U1 mean certificate**, m ≤ price + L1. The price is an uncertified classical RQMC
   orientation value (assm), and the B8x52 L1 is borrowed from B4x12. The quantum run thus
   consumes a classical price, which is circular for a stand-alone quantum estimate.
3. **Non-dyadic M.** This needs a QFT over Z_M. BHMT Theorem 12 holds for any integer M.

Partial combinations [EC]:
- 323-353 without the mean certificate (353.0 at the binding cell);
- 195-341 with dyadic M.

**Direction-select control, about ×2** (mod, q+) [EC] §2b.
- **The argument.** Replacing Q^j by Q^(j−c) in BHMT's construction multiplies each
  eigen-branch by a global phase only, and the branches are orthogonal on the unmeasured
  register. The outcome distribution, and so Theorem 12, is unchanged. A shot then costs
  M/2 calls instead of M − 1. The N2 review re-derived this identity and found it correct.
- **The call-cost condition is satisfied in this paper's cost model.** A direction-select
  iterate, [S_χ controlled on 0]·A S₀ A†·[S_χ controlled on 1], must cost no more than one
  controlled Grover iterate. That holds when only the reflections are controlled, which is
  exactly what the floor sheet assumes (§4.1). It is **not yet certified for a compiled
  circuit**.
- **The window chains already use it.** The window/QSP constants below use the convention
  that N calls cover exponents −N..N, which is the same direction-select call cost [EC], [ES].
- **Effect.**
  - Certified-schedule k: 293-533 (491,520 calls at $0.01); 341.4 at the binding cell.
  - Best k: 98-171.
  - Primary M at the binding cell: 801.5 → 400.7 (certified) and 232.0 → 200.4
    (explicit) [ES].
  - So within this paper's cost model the certified class is **400.7-801.5** at the primary
    conventions.

**Window/QSP estimation: k ≈ 7-26, with no usable explicit worst-case constant** (mod, q+)
[EC] §2c. The DPSS window constant is c = 4.168 at δ = 0.003 and 3.502 at δ = 0.01. These are
WS-k's N = 400 values. N1 recomputed c by power iteration, a different algorithm from W0's,
only at N = 50, 100 and 200, matching WS-k to 1e-12 at N = 100 and 200; it did not recompute
N = 400. The constants are also extrapolated from N ≤ 400 to the N ≈ 1e3-3e5 the task uses
(effect under 1% per [EC]).

| Setting | k (all cells) | B4x12 / B8x52 at $0.001 |
|---|---|---|
| δ = 0.003, no credits | 23.5-25.7 | |
| δ = 0.003, with U1/U2 | 8.25-8.77 | 8.25 / 8.74 |
| δ = 0.01, with U1/U2 (the DP1 row) | 6.93-7.37 | 6.93 / 7.34 |

The primary sources fall short of an explicit worst-case constant (lit) [EC] §4:
- Berry et al. (arXiv:2209.13581) App. D is approximate throughout.
- Patel et al. (arXiv:2403.18927) Thm 3 is asymptotic, with N₀ unspecified.
- Patel Thm 2 is explicit but average-case. A random known register offset makes it
  worst-case (N1 argument), but at k = 6.8e5-9.3e5, about 1e5 times too large [ES].
- Rall & Fuller (arXiv:2207.08628) give fits at a = 0.5 and 95%, not a worst-case 99%
  constant.

**Other explicit theorems are worse than canonical** (lit, q−) [EC] §2b. Grinko et al.
(arXiv:1912.05559) Thm 1 gives k = 2,997-5,755 (a WS-k file value quoted through [EC]), and
Fukuzawa et al. (arXiv:2208.14612) Lemma 3.7 gives about the same. No Bayesian or likelihood
design (E25) has a worst-case coverage theorem with an explicit constant in the sources
checked.

**Counting lower bound** (mod, rigorous; q+) [EC] §1, [ES], [FX].
- **The hard family.** A_θ = R_y(2θ) has θ-independent eigenvectors. This meets the
  premise of Mande & de Wolf (arXiv:2305.04908v3) Claim 5.3, and gives (1 − δ)K ≤ 2N + 2
  with one free copy of A|0⟩.
- **Values at δ = 0.01** (support class, Q-access plus one copy of A|0⟩): at the primary
  split, k_LB = 1.691-1.696 for B4x12 and 1.848-1.853 for B8x52 (over both splits,
  1.687-1.696 and 1.843-1.853).
- **Weaker access or narrower classes.** Under A/A† access the bound halves to 0.85 / 0.93.
  For a mean-bounded class it falls to 0.15-0.16 at the primary split (0.14-0.16 over both
  splits); the lowest value in any cell or access model is 0.074 [EC].
- **What it does not bind.** White-box estimators that use the known source code.

So between the rigorous floor of about 1.85 and the best explicit constant of about 198 lies
a gap of about two orders of magnitude, and it is not established that this gap is real.
This is the reason the claim is worded as achievability (§7).

**Lanes at W = 1e7** (mod, q+) [EC] §3, [ES].
- **Only one lane of the primary-width design fits.** The primary floor designs are 5.28M
  qubits wide (B4x12) and 10M wide (B8x52). The B4x12 lane credit below uses three lanes of
  the narrower W = 1e6 design.
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

*Direction note.* The H16 grid timed only `preint`, while T_C may in principle come from a
C5 method. In all four decision cells T_C is `preint` ([HT] `T_C` → `raw_best`), so applying
the measured H16 ratio to the Stage C T_C is like for like there, and the result is
unaffected.

**Classical confidence, C09** (mod from meas inputs; q+ because it slows the classical
side) [HW], [HC] §4.
- **What the convention is.** The primary classical side uses practice confidence
  intervals; the quantum k is a worst-case 99% guarantee over a bounded range. The
  distribution-free column is the *stricter* classical standard, and it is the one that is
  symmetric with the quantum side. It is the user's chosen primary that departs from
  symmetry.
- **The distribution-free route.** It uses a two-sided empirical Bernstein bound (Maurer &
  Pontil 2009, Thm 4; lit, not re-fetched in N1) at δ = 0.01 and payoff range $40 (assm). It
  uses iid preintegration with the measured σ_preint of 1.248 (B4) and 1.146 (B8), and the
  measured per-point cost of 1.15 µs and 10.4 µs at 16 workers.
- **Factor over the practice time:**

| Cell | Factor |
|---|---:|
| B4x12 $0.001 | 40.3 |
| B8x52 $0.001 | **36.9** |
| B4x12 $0.01 | 10.6 |
| B8x52 $0.01 | 18.9 |

- **Where the 36.9× comes from** (binding cell; mod, derived) [FX], [NC]. It is mostly the
  loss of RQMC's convergence rate: an iid CLT run needs 4.30e7 points against 1.43e6 RQMC
  points in the practice run, **30.2×**. The empirical-Bernstein tail then needs 8.02e7
  points, a further **1.86×** over CLT. The iid per-point cost (10.4 µs) is 0.66× the
  practice wall time per point (15.8 µs, which includes fixed overhead). The product
  30.2 × 1.86 × 0.66 = 36.9.
- **Resulting M at the binding cell:**

| Floor | Certified | Certified with direction-select | Best explicit | Best explicit without U1 | Window (0.01) |
|---|---:|---:|---:|---:|---:|
| Box-Muller | 21.7 | 10.9 | **6.29** | 11.2 | 0.23 |
| All-free | 1.08 | 0.54 | **0.31** | 0.56 | 0.012 |

- **The orientation price under the symmetric convention** (mod, derived) [NC], [FX]. The
  explicit k leans on U1, whose price is an uncertified classical RQMC value. A symmetric
  distribution-free comparison should not let the quantum side lean on an uncertified
  classical estimate. Without U1 the binding-cell k is 353.0, so M_distfree is **11.2**
  (Box-Muller) and **0.56** (all-free). The conclusion does not change: two departures
  still suffice.
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
faster than every verified anchor. The three 2026 anchors (arXiv:2603.16203, 2605.04892,
2510.26078) rest on the N1-hwclassical fetch log alone; the N2 reviewer could not check them
independently.

| Anchor | Value | 100 ns is faster by |
|---|---:|---:|
| Liu et al. (arXiv:2603.16203): decode-to-feedback pipeline, no qubits | 446 ns | 4.5× |
| Yang et al. (arXiv:2605.04892): the only demonstrated complete readout-to-feedback loop among the sources checked, d = 3 | 550 ns | 5.5× |
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
row. All values mod [HT], [ES], [AD], [DC].

| Estimator class | k at the binding cell | **M, primary** | Status of the constant |
|---|---:|---:|---|
| Certified today (E07 schedule) | 682.7 | **801.5** | Certified |
| Certified schedule with direction-select | 341.4 | 400.7 | Call-cost condition satisfied in this paper's cost model; not certified for a compiled circuit |
| Best explicit (U1 + U2 + non-dyadic M) | 197.6 | **232.0** | Three conditional credits |
| Best explicit at a consistent failure of 0.01 | 144.9 | 170.1 | As above; 11 medians |
| Best explicit with direction-select | n/a | 200.4 | As above, plus the direction-select condition |
| Window/QSP, failure 0.01 (the DP1 row) | 7.34 | **8.62** | No usable explicit worst-case constant |
| Window/QSP, failure 0.003 (like for like) | 8.74 | 10.26 | As above |

**Readings of the primary conventions** (mod) [HT], [ES], [FX]:

| Reading | Certified | Best explicit | Window (0.01) |
|---|---:|---:|---:|
| As quoted: W0 floor (R0), e = 0.45ε | 801.5 | 232.0 | 8.62 |
| N1 floor alone (R1) | 1,258 | 364.2 | 13.5 |
| Strict zero-bias reading of the binding cell (e = ε) | 400.7 | 104.4 | 3.88 |
| Direction-select (condition met in this cost model) | 400.7 | 200.4 | 8.62 (already uses it) |
| Binding cell ineligible (B4x12 $0.001 binds; q−) | 1,065 | 318.0 | 11.8 |

**Verdict at R1:** the claim holds under the primary conventions. N1 reproduced k, T_C, σ/e
and the M arithmetic exactly; the oracle term is the smaller of the two independent floors.
Under every reading above, the certified class stays at M ≥ 400.7 and the best explicit
class at M ≥ 104.4 (76.6 at failure 0.01 under the zero-bias reading [HT]), both above the
30× threshold that justifies R1. The window class misses by 3.9-13.5× across these readings,
and it has no explicit constant.

### 5.2 One departure at a time

Each row changes one convention or idealization, and each is quantum-favourable unless
marked q−. These are the explicit-best minima from [HT], except the C09 rows from [HW] and
the no-U1 row from [FX].

| Departure | M | Direction |
|---|---:|---|
| Primary | 232.0 | n/a |
| All-free oracle (free loader and exponential, narrow words) | 11.5 | q+ (oracle idealization) |
| 1 lane vs 1 core (H16, meas) | 22.7 | q+ |
| Symmetric distribution-free classical, quantified from Stage C (36.9× at the binding cell). The stricter classical standard, not an idealization | **6.29** | q+ |
| Same, without the U1 mean credit | 11.2 | q+ |
| Distribution-free classical ×5 / ×2 (assm, W0's C09 range) | 46.4 / 116.0 | q+ |
| Supply 1e13 T/s | 74.8 | q+ |
| e = ε: the strict zero-bias reading of the binding cell (§2) | 104.4 | q+ |
| Estimator failure 0.01 | 170.1 | q+ |
| W = 1e8 or unlimited (N1 floor) | 189.5 | q+ |
| 10 ns layers (minimum at B4x12; B8x52 stays at 232.0) | 197.8 | q+ |
| B8x52 $0.001 ineligible (current certified bias bound) | 318.0 (B4x12) | q− |
| Supply 1e11 / W = 1e6 / 1 µs / 10 µs | 1,978 / 648 / 748 / 7,476 | q− |

For the window class [HT], [HW]:
- the all-free oracle alone gives 0.43 at failure 0.01, or 0.51 at 0.003;
- 1 lane vs 1 core alone gives 0.84 at failure 0.01, or 1.002 at 0.003;
- the symmetric distribution-free convention alone gives 0.23 at failure 0.01.

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

Under the strict zero-bias reading of the binding cell (§2), e = ε is part of the primary,
so all-free + 1 lane vs 1 core is a **pair** that gives 0.506 [HT], [DC]. Under that reading
two departures suffice even with W0's assumed C09 range.

**With the Stage-C-quantified C09 factor** [HW], **two** departures suffice for the
explicit class:
- all-free oracle + symmetric distribution-free classical gives **M = 0.31** (0.56 without
  U1);
- the certified class with the same pair gives 1.08, 8% above 1.

**With direction-select** (call-cost condition met in this paper's cost model, not certified
for a compiled circuit) [AD], confirmed per cell by derived arithmetic in [DC] (mod, q+):

| Departures, with direction-select | M |
|---|---:|
| All-free + 1 lane vs 1 core, explicit class | **0.97** |
| All-free + distribution-free (Stage C), explicit class | 0.27 |
| All-free + distribution-free (Stage C), certified schedule | 0.54 |

**Reading.** The DP1 memo's "at least three stacked departures" holds only under W0's
assumed C09 range, without direction-select, and with e = 0.45ε at the binding cell; the DP1
errata block corrects it [DP1]. With the N1 measurements, two departures are enough: one
oracle idealization (the all-free floor, which no construction in this project approaches,
§6) plus the symmetric distribution-free classical convention. That second departure is not
an idealization; it is the stricter classical standard, symmetric with the quantum
worst-case guarantee. Under it, even the certified class reaches 0.54-1.08 with the all-free
floor. The claim, which is stated at the primary practice-CI convention, is unchanged, but
the negative is robust only at that convention, and the manuscript does not describe the
margin as "three departures".

---

## 6. The frontier: what would overturn the result

Each lever below is stated with the size of its effect at the binding cell.

1. **An explicit worst-case 99% constant for window/QSP amplitude estimation.**
   - This alone moves M from 232 to 8.62-10.26 [HT]. It does not reach 1 at the primary
     oracle floor and convention, but it does under the symmetric convention (0.23) [HW].
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
2. **An oracle below the thresholds of §3.** One controlled Grover iterate at the binding
   cell must take at most 9.9 reaction layers and 9.9e5 T (explicit constant), or 2.9 layers
   and 2.9e5 T (certified) [FX].
   - The idealized all-free floor (114 layers, W0) moves the explicit M from 232 to 11.5
     [HT]; it would have to be beaten by a further 11.5×.
   - Combined with lever 1, it gives the window-class M of 0.43-0.51 [HT].
   - The all-free floor assumes a free Gaussian loader, a free exponential and 48-bit
     words. Its compute path is 67 layers against 278 for the current law (B8x52 [FS]). The
     bias effect of the 48-bit words was not checked (§8).
   - Box-Muller alone is about half of the current-law path (§4.1).
3. **A different comparison convention.**
   - The symmetric distribution-free classical convention gives M = 6.29 (explicit; 11.2
     without U1) [HW], [FX]. This is a stricter classical standard, not a relaxation.
   - One lane against one core gives 22.7 [HT].
   - A supply of 1e13 T/s gives 74.8 [HT].
   - A 10 ns layer does nothing at the binding cell unless supply also rises (§3).
   - Any one of these, stacked with lever 2's all-free floor, reaches or nearly reaches
     M = 1 (§5.3).
4. **Smaller conditional credits.** They change M by less than 2.5× and do not overturn the
   result alone [ES], [HT]:
   - direction-select: 232 → 200 (explicit), 801.5 → 400.7 (certified);
   - estimator failure 0.01: 232 → 170;
   - the strict zero-bias reading: 232 → 104.4;
   - lanes: 1.00× at B8x52, at most 1.29× at B4x12.
5. **A control-variate residual oracle that shrinks the payoff span (open; register F20,
   F04).** This escape was listed as closed in v1. It is not closed.
   - *Why it is not closed.* v1 treated a control only as a σ reduction, which helps only a
     σ-normalised estimator. But bounded amplitude estimation's k is span-normalised: its
     call count scales with the range S of the variable the oracle encodes. A residual
     oracle (payoff − control, with the control's mean known classically) changes S itself,
     so a smaller residual range lowers the call count directly, with no σ-normalised
     estimator needed. Neither N1 nor W0 measured the residual span. The register's hard cap
     of about 4.5× (σ 5.15 → 1.14, F20) bounds the σ ratio, not the span ratio.
   - *How large it would need to be* (mod, derived, first order) [FX]. To first order the
     needed span reduction S / S_res equals M at the floor and convention used, before the
     control's own coherent cost is charged: 232× at the Box-Muller floor (residual span
     ≤ $0.17 against the $38.82 support-tight span), 11.5× at the all-free floor (≤ $3.37),
     and 6.29× under the symmetric convention at the Box-Muller floor (≤ $6.18). The net
     gain is (S / S_res) ÷ (D_eff,res / D_eff), because evaluating the control coherently
     raises D_eff; the exact factor also depends on where the residual mean sits within its
     range, through the U1 mean bound.
   - *Reasons to expect a small gain, which are not measurements.* The register notes that
     no geometric control exists for the knock-out, and that coherent preintegration needs
     per-date root solves and normal-CDF evaluations (F20). The classical comparator already
     uses preintegration, so a control granted only to the quantum side is asymmetric.
   - *Register triggers.* F04's reopen rule ("if the other levers bring miss ≤ 4×") and F20's
     costing trigger ("only if the other levers reach miss ≤ 4×") are met by the stacked
     departures of §5.3 (for example 1.125 and 0.31), though not at the primary conventions
     alone.
   - *Scope.* A residual oracle encodes payoff − control, not the payoff, so it lies outside
     scope item 1 of the claim (§1). It is outside the claim, not refuted by it. The counting
     bound (§4.2) does not bind it either.
   - *What would settle it.* A measured residual range for a control with a classically
     certified mean, together with a coherent cost for the control, showing
     (S / S_res) · (D_eff / D_eff,res) ≥ M at the binding cell.

**What a hardware programme would have to show.** For the explicit constant at the
Box-Muller floor: a 1.34 ns logical layer, 3.3e14 accepted T states per second and 1e7
logical qubits, simultaneously [HW]. The best verified complete loop among the sources
checked is 550 ns at d = 3.

---

## 7. Closed escapes, bounded escapes, and escapes outside the claim

### 7.1 Closed for this task

These routes were examined and closed for this task. They are cited so that a reader does
not reopen them without new evidence.

- **E22: log-domain QSP on the payoff predicates.** The register records 0 of 3,106 actual
  payoff predicates as eligible [REG] (W0 count, not recomputed in N1). It is closed as a
  negative.
- **C14: the "2×" per-call depth reading.** Per-call depth is one Grover iterate, as used
  throughout. The DP1 memo (`docs/program_plan_20261010/DP1_MEMO.md`, WS-small) records
  the "2×" reading as wrong. (Register tier T1, decision-critical, done in W0.)
- **Lanes, E20.** No lane credit at the binding cell (§4.2).
- **Latency lines H14, H04 and H07** [HC] §3:
  - a GHz photonic clock is not a logical-layer time;
  - constant-round fault tolerance still pays at least one syndrome round plus decoding per
    layer, about 1 µs on superconducting hardware;
  - the projected cat-qubit cycle is 500 ns.

### 7.2 Bounded at the primary conventions

- **F05: free coherent loading ("even with free loading").** The all-free oracle, which
  includes a free loader, still gives explicit M = 11.5 [HT]. F05's own kill rule, "close as
  a standalone route if ≥ 10× miss remains", is therefore met at the primary conventions.
  The register file keeps F05 at T2 ("credited screen value / branch-A lever"); this draft
  does not edit the register, and it records F05 as *bounded by the all-free floor
  (M = 11.5)*, not closed. Under the symmetric distribution-free convention the same floor
  gives 0.31, so the bound holds only at the primary convention.

### 7.3 Outside the claim, not closed

- **F20: control variates, and F04: structured integration of a certified residual.** F20
  is T2 in the register, not closed. F04 is T4, but its stated closure basis is "closes on
  the F20 zero-depth credit", which is exactly the credit the DP1 table's run002 removed, so
  that basis no longer exists. The residual-span reduction these routes could give is not
  costed anywhere in N1 or W0. Both are treated as the open lever 5 of §6.
- **The σ-normalised estimator line.** In the sources checked (Kothari & O'Donnell,
  arXiv:2208.07544, not re-fetched in N1), no explicit-constant worst-case estimator is
  σ-normalised. The variance-aware estimators of Montanaro (2015) and Hamoudi (2021) were
  not checked. The DP1 table run001 wrongly included a σ credit; run002 removed it [DP1].

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
- **The oracle floor is modelled, not a lower bound.** "No design" is evidence about
  oracles that cost at least the idealized floor. Stated checkably (§3): a design reaches
  tenfold at the binding cell and primary conventions only if one controlled Grover iterate
  takes at most 9.9 reaction layers and 9.9e5 T (explicit) or 2.9 layers and 2.9e5 T
  (certified). Any design above either limit is covered by the claim.
- **The negative is robust only at the primary practice-CI convention.** The classical side
  uses practice confidence intervals; the quantum side a worst-case 99% guarantee. Under the
  symmetric distribution-free convention, explicit M is 6.29 (11.2 without U1), and with the
  all-free floor it is 0.31 [HW], [FX].
- **The certified class is robust only at the primary conventions.** Within this paper's
  cost model, where the direction-select condition is met, certified M is 400.7-801.5 at the
  primary conventions, and 0.54-1.08 with the all-free floor plus the symmetric classical
  convention [DC], [HW]. Without direction-select it is 1.08, only 8% above 1.
- **Conditional credits are granted, not certified.** The 232 row already assumes three
  uncertified credits (§4.2), so the certified-constant claim is in fact carried by a
  stronger margin (400.7-801.5). Granting the credits makes the negative more conservative,
  not less.
- **The orientation price.** The U1 credit uses an uncertified classical RQMC price and a
  B8x52 L1 borrowed from B4x12, and so the quantum run consumes a classical estimate. Without
  U1 the primary explicit M is 414.4 and the symmetric-convention M is 11.2 (Box-Muller) or
  0.56 (all-free) [FX].
- **The binding cell's eligibility is a re-certification debt.** B8x52 at $0.001 is admitted
  on a modelled clamp tightening (bias 0.47ε) that still needs an A02 bridge rerun and
  A07/A13 re-proofs [BD]. If it is ineligible, the binding cell is B4x12 at $0.001 and
  explicit M is 318.0 (q−). Under the strict zero-bias reading, explicit M is 104.4 and
  certified 400.7 (§5.1).
- **Two idealized floors.** The floor is idealized: Clifford gates and routing are free,
  and the leaf constants come from the literature. N1's independent floor is 1.55-1.57×
  less favourable than W0's at the primary conventions. Using the more favourable floor
  per pair keeps the claim conservative, but the two floors disagree by more than 10% in
  165 of 180 pairs [RC], so neither is a tight bound.
- **Rigour level.** The headline verdict is R1 (an independent recompute plus a receipt).
  - N1 recomputed the estimator constants, classical times and M arithmetic exactly. The
    oracle term is the smaller of W0's floor (R0) and N1's floor (R1); the quoted
    801.5 / 232.0 / 8.62 use W0's floor. With N1's floor alone they are
    1,258 / 364.2 / 13.5.
  - The N1 card justifies R1 over R2 by the primary margin of at least 30×, which holds
    under every reading of the primary (≥ 104.4 explicit, ≥ 400.7 certified).
  - Under the Stage-C distribution-free sensitivity, the margin falls to 6.29, below that
    30× threshold [HC] §5. A reviewer may reasonably ask for R2.
- **Undisclosed-in-v1 quantum-favourable conventions** (each strengthens the negative):
  - the classical side is held to the same 0.45ε statistical share as the quantum side,
    although it carries no 0.55ε deterministic-bias reserve ([SPC] §0.4-0.5 labels this QF);
  - the magic-state factory footprint is outside W, which [W0C] defines as logical *data*
    qubits;
  - the quantum latency counts only Grover iterates, not readout, reset, the inverse QFT,
    decoder tail or classical post-processing, although the claim says "complete latency";
  - the bias effect of the all-free floor's 48-bit words was not checked.
- **A quantum-unfavourable convention.** T_C is the minimum over noisy C2/C5 candidates,
  labelled CF in [SPC] §0.5. The binding-cell T_C of 22.53 s is 4.1% below the H16 rerun's
  23.46 s; with the latter, explicit M would be 222.8 [FX].
- **An escape outside the claim.** The control-variate residual-span lever (§6 lever 5) is
  not costed and not closed.
- **Classical side.** Classical T_C is measured on one laptop CPU (16 workers), with
  practice confidence intervals. The strongest tested method is not the strongest
  applicable method (C10), but untested challengers can only raise M.
- **The distribution-free factor** uses an assumed payoff range of $40 ($64 as a
  sensitivity) and an empirical Bernstein bound. A betting confidence sequence could lower
  it by up to about 12% [HC] §4.
- **Literature not re-fetched in N1.** Jones (2013), Gidney (2018), Fowler
  (arXiv:1210.4626), Babbush et al. (2018), Maurer & Pontil (2009) and Kothari & O'Donnell
  (arXiv:2208.07544). The three 2026 hardware anchors rest on the N1-hwclassical fetch log
  alone.
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
   instead of 232 [RC]. At the primary conventions N1 is 1.547× (B4x12) and 1.570× (B8x52)
   less favourable, so the quoted primary values use W0's R0 floor (§4.1).
2. **Mixed failure allocation in WS-k.** The window row (8.62) uses failure 0.01, while
   the explicit row (197.6) and E07 use 0.003. Like for like, the values are 10.26
   (window, 0.003) or 170.1 (explicit, 0.01) [RC], [EC].
3. **C09 factor.** W0 assumed 2-5×. Stage C data give 10.6-40.3×, so the distribution-free
   explicit M is 6.29, not 46-116 [HC].
4. **Number of departures.** DP1 says at least three; two suffice (0.31, §5.3) [HC]. The
   DP1 errata block now records this [DP1].
5. **Direction-select.** WS-k said "no theorem covers" it. BHMT Thm 12 does, so it is a new
   credit of about ×2 whose call-cost condition is met in this cost model [EC].
6. **Counting bound.** W0 quoted "about 1.7-1.85" without an access model. The values hold
   for Q-access plus one copy of A|0⟩, and fall to 0.85/0.93 under A/A† access [EC].
7. **"No explicit constant".** W0's "no explicit constant in any primary source" becomes "no
   *usable* explicit worst-case constant": Patel Thm 2 plus a random offset is explicit but
   about 1e5× too large [EC].
8. **WS-k lane figures** mix source widths with floor depths. The corrected credit is 1.00×
   for B8x52 and 1.29× for B4x12 [EC].
9. **Register H01/H02 wording.** It calls Liu's 446 ns a complete readout-to-feedback loop.
   It is a partial pipeline with no qubits; among the sources checked, only Yang's 550 ns is
   complete [HC].
10. **W0 decision summary quirk.** At B4x12 $0.03 it prints the raw T_C of 0.12677 s, but
    its k_10x uses the envelope value of 0.12440 s. M is unaffected [RC].
11. **W = 1e6.** The N1 floor is infeasible for B8x52 (persistent registers alone take 3.4e6
    qubits), so W0's D_eff of 11,034 is used [RC].
12. **Loader share.** DP1 gives the loader as 36-56% of W0's floor. N1's Box-Muller share of
    the compute critical path is 52-53% (mod) [RC]. The two shares are of different floors
    and are not directly comparable; this draft quotes the N1 value.
13. **B8x52 $0.001 "at zero bias".** DP1 and v1 described the binding cell as eligible at
    zero deterministic bias, but the table uses e = 0.45ε there. The cell is admitted on the
    modelled clamp tightening (bias $0.000473); the consistent zero-bias reading gives
    explicit M = 104.4 [BD], [HT], [DP1].

### 9.2 Between N1 workstreams (both values reported)

14. **Minimal departures.**
    - N1-headline: "no set of two reaches M ≤ 1" (best pair 1.125). This used W0's assumed
      C09 ×2/×5.
    - N1-hwclassical: two departures give 0.31, using the Stage-C factor.
    - Both are correct under their own inputs. This draft adopts the Stage-C factor
      because it is computed from measured inputs, not assumed.
15. **Direction-select was not carried into the headline enumeration.** Applied to the best
    headline pair, it gives 0.97 [AD]. This is a cross-product that no single N1 file
    contains. The N2 review confirmed it, per cell and along a different path, by derived
    arithmetic (0.9718, 0.2696 and 0.5392 to 1e-15; binding cell unchanged) [DC]. It was not
    confirmed by a headline rerun.

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
- **§7.1 (closed):** E22 (T4), C12 (T4, labelling) and C14 (T1).
- **§7.2 (bounded at the primary conventions):** F05 (T2 in the register).
- **§6 lever 5 and §7.3 (outside the claim, not closed):** F20 (T2) and F04 (T4).

The register's dispositions are W0 (R0). This draft does not edit the register file. It
reads three dispositions differently from the register, and records one wording correction:
- **F05** stays T2 in the register; this draft records its kill rule as met at the primary
  conventions (M = 11.5 ≥ 10) and treats it as bounded, not closed (§7.2).
- **F20** stays T2 in the register; this draft treats it as an open escape outside the
  claim (§6 lever 5).
- **F04** is T4 in the register, but its closure basis ("closes on the F20 zero-depth
  credit") no longer exists after run002; this draft treats it as open with F20 (§7.3).
- **H01/H02:** the wording correction in §9.1 item 9.

## Appendix B. Reproduction

Run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`, in this order:

1. **N1-headline:** `research/plan110_n1/headline/e07_keff.py`, then `floor_sheet.py`, then
   `headline_m.py`.
2. **N1-estimator:** `research/plan110_n1/estimator/recompute_estimator.py`.
3. **N1-hwclassical:** `research/plan110_n1/hwclassical/hw_classical_v2.py`. The v1 script
   is superseded.
4. **v1 drafter:**
   - `research/plan110_n1/drafter/draft_numbers.py` copies the quoted values and checks 10
     arithmetic identities, with a maximum relative error of 1.8e-16 [DN];
   - `research/plan110_n1/drafter/draft_addendum.py` forms the direction-select
     cross-products [AD].
   - **Known defective field in [DN].** `draft_numbers.json` → `certified_k_range_0.45eps`
     reads [532.5, 1066.7], which wrongly mixes in the non-dyadic conditional-credit rows.
     The certified range is 585.8-1,066.7; see the `correction_certified_k_range` row in
     `results/plan110_n1/drafter/rows.jsonl`. The file is kept unchanged (no overwrite).
5. **N2 review:** `research/plan110_n1/review/check_draft.py` [NC] and
   `research/plan110_n1/review/confirm_dirsel.py` [DC].
6. **This revision:** `research/plan110_n1/fixer/fixer_numbers.py` [FX], then
   `fixer_numbers_2.py` [FX2]. Rows are in `results/plan110_n1/fixer/rows.jsonl`, and the
   defect-to-fix map is `results/plan110_n1/fixer/fix_map.json`.

The measured classical inputs (Stage C C2/C5 timings and the H16 grid) come from the Stage C
/ H16 harness, which uses numpy and numba and is run without `-I`; they are inputs to these
scripts, not outputs of them.

Every output file records the SHA-256 of its inputs. Each script creates its outputs with
exclusive create and refuses to overwrite them.

---

## Changelog (v1 → v2)

Defect numbers are those of `results/plan110_n1/review/REVIEW.md`. New numbers are in [FX]
and [FX2] unless another source is named.

| Defect | Severity | Fix in v2 | Where |
|---|---|---|---|
| 1 | major | "Two R1 recomputes confirm them" replaced: N1 recomputed k, T_C, σ/e and the M arithmetic exactly; the oracle term is the smaller of W0's (R0) and N1's (R1) floors, about 1.55× apart; N1's floor alone gives 1,258 / 364 / 13.5. R1 supports the verdict, not the quoted values | Abstract; §4.1 "Effect"; §5.1 readings table and verdict; §8 "Rigour level"; §9.1 item 1 |
| 2 | major | Checkable thresholds stated: explicit ≤ 9.90 layers and ≤ 9.9e5 T per iterate; certified ≤ 2.86 layers and ≤ 2.9e5 T (5.73 / 5.7e5 with direction-select); window 266 layers; all-free floor 11.5× / 39.8× above. Scope item 1 reworded as "every design whose iterate exceeds either limit" ("or", since the limits are joint necessary conditions). Symmetric-convention limits added (365 / 106 layers) | Abstract; §1 scope item 1; §3 item 3; §6 lever 2; §8 |
| 3 | major | Binding cell described as admitted on a modelled, uncertified clamp tightening (bias $0.000473 = 0.47ε ≤ 0.55ε), primary keeps e = 0.45ε; strict zero-bias line 104.4 / 400.7 and pair 0.506; eligibility listed as a re-certification debt (ineligible: 318.0 at B4x12) | Abstract; §2 conventions table; §3 ledger σ/e label; §5.1 readings table; §5.2; §5.3; §8; §9.1 item 13 |
| 4 | major | Abstract now states up front that classical uses practice CIs and quantum a worst-case 99%, that the symmetric convention costs classical 36.9× at the binding cell, gives M under it (6.29, 11.2 without U1; 21.7 certified; 0.31 all-free) and says the negative is robust only at the primary practice-CI convention. The distribution-free column is relabelled as the stricter symmetric standard, not an "idealized change". §4.3 decomposition: 30.2× (CLT iid vs RQMC points) × 1.86× (EB over CLT) × 0.66 (per-point cost) = 36.9× | Abstract; §2 table; §4.3; §5.2; §5.3 "Reading"; §6 lever 3; §8 |
| 5 | major | Fragility sentence rewritten: one oracle idealization plus the symmetric classical convention gives 0.31; one oracle idealization plus one lane vs one core gives 1.125, or 0.97 with direction-select | Abstract |
| 6 | major | Direction-select changed from "assumed" to "satisfied in the paper's cost model; not yet certified for a compiled circuit"; certified class reported as 400.7-801.5 (primary) and 0.54-1.08 (all-free + symmetric classical); noted that the window chains already use the same call cost | Abstract; §4.2; §5.1 table; §5.3; §8 |
| 7 | major | §7 split into closed / bounded / outside-the-claim. F05 moved to "bounded by the all-free floor (M = 11.5)", register kept at T2; F20 and F04 moved to "outside the claim, not closed"; the control-variate residual-span lever moved to §6 as open lever 5 with the reasoning (span-normalised k, unmeasured residual span, first-order needed reductions 232× / 11.5× / 6.29×, register triggers met under stacked departures); σ-normalised sentence softened to "in the sources checked"; Appendix A lists the exceptions instead of "changes none" | §6 lever 5; §7; Appendix A; Abstract |
| 8 | minor | Orientation-price line added: without U1, k = 353.0, M_distfree 11.2 (Box-Muller) and 0.56 (all-free); primary 414.4; circularity noted | §4.2 credit 2; §4.3; §5.2; §8 |
| 9 | minor | q+ conventions disclosed: classical 0.45ε share without bias reserve; factories outside W ("logical data qubits"); latency counts Grover iterates only; 48-bit word bias unchecked | Abstract; §2 table; §6 lever 2; §8 |
| 10 | minor | T_C relabelled "meas, q− (min over candidates)"; H16 rerun 23.46 s (+4.1%) gives explicit M 222.8 | §2; §3 ledger; §8 |
| 11 | minor | "74.8 is layer time" replaced: at unlimited supply M would be 74.8, reaching tenfold then needs 1.34 ns layers, and at 1e12 T/s supply adds a further 3.10 | §3 item 2 |
| 12 | minor | Abstract window entry shows 8.62 (failure 0.01) / 10.26 (0.003, like for like) | Abstract table |
| 13 | minor | Window k ranges now 8.25-8.77 and 6.93-7.37 with the $0.001 values shown; mean-bounded counting bound 0.15-0.16 at the primary split (0.14-0.16 over both; lowest 0.074); support bound quoted at the primary split (1.691-1.696, 1.848-1.853) with the both-split range; window constant clause states that N1 recomputed c only at N ≤ 200 and that the N = 400 values are WS-k's, extrapolated to N ≈ 1e3-3e5 | §4.2 |
| 14 | minor | Provenance narrowed to N1/drafter/review/fixer scripts; measured timings attributed to the Stage C / H16 harness with numpy and numba | Front matter "Provenance"; Appendix B |
| 15 | minor | [DN] defective field `certified_k_range_0.45eps` disclosed with pointer to the drafter correction row | Source keys; Appendix B item 4 |
| 16 | minor | Floor-sheet citations and Maurer & Pontil marked "lit, not re-fetched in N1"; 2026 anchors marked as resting on the hwclassical fetch log; Yang qualified "among the sources checked" | §4.1; §4.3; §6; §8; §9.1 item 9 |
| 17 | minor | Direction note: the H16 grid timed only `preint`, and T_C is `preint` in all decision cells, so the 1-lane result is unaffected | §4.3 |
| 18 | minor | Lanes reworded: only one lane of the primary-width design fits; the B4x12 credit uses three lanes of the W = 1e6 design | §4.2 |
| 19 | minor | "This draft closes the last open contract" removed; §1 now says the knock-out basket Stage C measured is already Failure 6 of WHY_NO_ADVANTAGE.md, and that this draft turns that sixth construction into a scoped frontier statement | §1 |
| 20 | minor | Loader-share discrepancy (DP1 36-56% vs N1 52-53%) added | §4.1; §9.1 item 12 |
| 21 | minor | Scope line added directly after the verbatim claim: family, task, tested classical method; "certified constants" refers to the estimator constant; oracle costs are modelled idealized floors (plus the latency scope from defect 9) | Abstract |
| Review method note | n/a | §9.2 item 13 (now 15) says "confirmed by derived arithmetic" in [DC], not by a headline rerun | §9.2 item 15 |
