# U2: mean-aware bounded-AE schedule (design prospectus only)

**Status.** This is design and prospectus work only. The limitation program is at USER_REQUESTED_STOP_CHECKPOINT after scope #43, and nothing beyond #43 is authorized.

This note does not run SCI, any controller, a ROOT launcher, a saved verifier or a reporter. It writes nothing under `.context/`, `results/limitation_program_20261001/`, `docs/limitation_program_20261001/` or `docs/limitation_audit_20261001/`.

All numbers below come from two sources only:
- the saved E07 schedule formula, evaluated as pure-constant arithmetic on declared budgets;
- values read from saved, verified records.

No price, moment, mean certificate or bias is evaluated.

Helpers (new files; each output was created with exclusive create):
- `research/parallel_E11_unblock_20261010/U2/mean_aware_schedule_arithmetic.py`, sha256 `b1f24a29b563532dfa88243072e1d1f641975608138e3da2ea9e3c359b205316`. Output: `mean_aware_schedule_arithmetic_run001.json`, sha256 `cac54669f497d1a1dc9be17fec666d8768b124a65ea96833fb925f3098491928`.
- `research/parallel_E11_unblock_20261010/U2/tight_span_variant_arithmetic.py`, sha256 `4ba6fc570090932341aabd622192cc6b8cd012c9c1cf6bc54e05ae36df59af6d`. Output: `tight_span_variant_arithmetic_run001.json`, sha256 `6de53a169c953e267545161c36879468bf0535507c3862b2d229a682e080618a`.

Both helpers ran under system CPython 3.9.13 with `-I -S -B`. Both load the frozen E07 `executed_code` snapshot by file path after checking its hash, and write no bytecode. Neither records AST or compile metadata, so the pinned 3.12.4 environment was not required.

## 0. Answer in brief

1. **The earlier thresholds are confirmed only as two-decimal roundings.** The exact sufficient conditions for halving M (and the call count) on the saved span-64 wrapper, at a 0.45·ε statistical share, are m ≤ 19.159773, 5.267484, 10.242691 and 6.086186 USD at ε = 1/10, 3/100, 1/100 and 1/1000. Three of the four rounded values (19.16, 5.27, 6.09) are slightly *above* the true threshold. So the earlier sentence "halving needs m <= 19.16 / 5.27 / 10.24 / 6.09" is correct as a rounding but not as a sufficient condition at 1/10, 3/100 and 1/1000. Use the truncated values instead.
2. **A mean bound m leaves the normalization unchanged.** The span stays 64 USD, as the 46-bit Hadamard selector requires. The bound only replaces the worst case sqrt(a(1-a)) <= 1/2 with sqrt(a(1-a)) <= sqrt((m/64)(1-m/64)), which is valid for m <= 32. Repetitions (15) and failure (≤ 0.0029685) are unchanged. Calls go from 15(M−1) to 15(M/2−1).
3. **m must bound the digital mean E[g]** (`p = E[Yraw]/2^46`), not the continuous price. With the #43 conditional L1 bridge, a continuous-price certificate m_f is enough when m_f ≤ m* − 0.045202052 USD.
4. **Correction to PLAN_43 §2 ("U1 ... the only plausible route to a reduction").** A *support-tight normalization* needs no mean certificate. It compares a 47-bit selector against 3·Yraw, which gives span 128/3 USD and uses only the audited E03 support. That alone halves M at ε = 1/10 and 1/100 under the unchanged schedule formula. It does not halve M at 3/100 or 1/1000, where a mean bound is still needed, but a looser one (§4). This is a new-wrapper design, not a saved result.
5. **Rotation synthesis.** At ε = 1/10, 3/100 and 1/100, every IQFT rotation a halved schedule needs is already certified in `E02_IQFT_run001/rotations.json`. At ε = 1/1000, both the baseline (19 bits) and the halved schedule (18 bits) need rotations that do not exist yet (pi/131072, pi/262144, and pi/524288 for the baseline).

## 1. Exact construction of the saved E07 schedule

Producing code: `results/limitation_program_20261001/E07_schedule_run001/executed_code/financial_bounded_schedule.py`, sha256 `4452c331...f149c`. This equals the frozen `research/limitation_program_20261001/financial_bounded_schedule.py` pin in E07 `protocol.json`. The schedule is built in five steps, all exact:

- **Pi enclosure.** `pi_interval(80)`: Machin's formula 16·atan(1/5) − 4·atan(1/239), with 80 alternating rational terms each, gives the enclosure [π_lo, π_hi] (`schedule.json /pi_enclosure_exact`).
- **QPE size M.** M is the least power of two with `span·(π_hi/M + π_hi²/M²) <= δ`, where span = 64 and δ is the statistical dollar share. An adjacency check rejects the result if π_lo would already accept M/2.
- **Elementary failure.** `1 − 8/π_hi²`, rounded up on the 2^-40 grid, gives 104140535669/2^40.
- **Repetitions.** The repetition count is the least odd number whose exact binomial majority tail is ≤ the failure allowance 3/1000. For this elementary failure that is **15**. The resulting ideal failure is ≈ 0.0029684634.
- **Calls.** Controlled Grover calls = 15·(M−1), and the longest chain is M−1.

The interpretation is BHMT Theorem 12 with k = 1 (`protocol.json /primary_theorem`). With probability ≥ 8/π², the amplitude error is at most

    |a~ − a| <= 2π·sqrt(a(1−a))/M + π²/M².

The saved formula `span*(pi/M + pi**2/M**2)` is this bound times span, after **sqrt(a(1−a)) <= 1/2**. The E07 schedule enters the worst case at exactly that point.

The downstream E02 ledger (`E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json`) adds a classical readout allowance of 2^-39 USD (`ideal_error_plus_readout_upper_exact`). The same ledger fixes the amplitude law `p = E[Yraw]/2**46 = E[already discounted native dollar Y]/64`.

**Reproduction.** My helper re-ran `certified_schedule(9/2000, 3/1000, 64)` from the snapshot. M, repetitions, calls, ideal error, ideal failure and elementary failure equal the saved `schedule.json` exactly: M = 65536, 15 shots, 983,025 calls.

## 2. Mean-aware derivation (exact formulas)

### 2.1 Assumptions

- **A1 (amplitude law).** a = E[g]/64, where g = Yraw·2^-40 is the native, already-discounted digital payoff under the circuit's finite Hadamard input law. This is the E02 binding.
- **A2 (certified mean bound).** A certified m satisfies E[g] <= m <= 32. The certificate is deterministic, or carries its own failure allocation, and it is fixed **before** any quantum run. It is not estimated from the same run.
- **A3 (theorem).** Theorem 12 (k = 1) holds for every a in [0,1]. sqrt(a(1−a)) is increasing on [0, 1/2], so a <= m/64 <= 1/2 gives sqrt(a(1−a)) <= sqrt((m/64)(1−m/64)).
- **A4 (unchanged parts).** Statistical share δ = (9/20)·ε, as in CONTRACT C05 and the E24 adopted share. Failure allowance 3/1000. Readout allowance 2^-39 USD. Median decode is unchanged.

### 2.2 Dollar error and the halving threshold

Multiplying by span 64 gives 64·sqrt(a(1−a)) = sqrt(E[g](64 − E[g])) <= sqrt(m(64−m)). The mean-aware dollar error is

    e(m, M) = 2π·sqrt(m(64−m))/M + 64π²/M² + 2^-39.

The worst case m = 32 recovers 64(π/M + π²/M²) + 2^-39 exactly.

**Normalization.** Unchanged. The span 64 = 2^46/2^40 is forced by a Hadamard-uniform selector on the 2^-40 grid: the span must be a power of two at least sup g = 42680645928225/2^40 ≈ 38.818. A bound on the *mean* does not change the *support*, so it cannot change the span. Section 4 treats a different normalization that uses the support.

**Minimal M given m.** M(m) is the least power of two with e(m, M) <= δ, which is equivalent to

    M >= [A + sqrt(A² + 4·δ'·64π²)] / (2δ'),  A = 2π·sqrt(m(64−m)),  δ' = δ − 2^-39.

Calls = 15·(M(m) − 1). Repetitions are independent of m, because the 8/π² success bound does not depend on a.

**Threshold for M → M/2^j.** Write M' = M/2^j and R = (δ − 2^-39 − 64π²/M'²)·M'/(2π). Then e(m, M') <= δ iff

    m <= m*(M') = 32 − sqrt(1024 − R²)    (when 0 < R < 32).

Every number is certified with π_hi and an inward integer-sqrt enclosure. The helper then re-checks `e(m*_inward, M') <= δ` with an outward sqrt.

### 2.3 Results (pure-constant schedule arithmetic)

Only the ε = 1/100 baseline is a saved schedule. The other baselines are the same formula at δ = 0.45·ε and are **not** saved or preregistered schedules.

| ε (USD) | δ = 0.45ε | baseline M (bits) | baseline calls | halved M | halved calls | sufficient m* for halving (USD, truncated) | earlier claim | m* for quartering |
|---|---|---|---|---|---|---|---|---|
| 1/10 | 9/200 | 8192 (13) | 122,865 | 4096 | 61,425 | **19.159773760** | 19.16 (rounds up: not sufficient as stated) | 3.534308482 |
| 3/100 | 27/2000 | 16384 (14) | 245,745 | 8192 | 122,865 | **5.267484706** | 5.27 (rounds up) | 1.226955321 |
| 1/100 | 9/2000 | 65536 (16), saved | 983,025 | 32768 | 491,505 | **10.242691368** | 10.24 (sufficient) | 2.226638005 |
| 1/1000 | 9/20000 | 524288 (19) | 7,864,305 | 262144 | 3,932,145 | **6.086186020** | 6.09 (rounds up) | 1.407644120 |

Reading the table:
- Readout sensitivity is at most 6e-8 USD on m* (`readout_free_m_star_inward` in the JSON).
- Repetitions are 15 in every row.
- Worst-case M/2 never fits, which confirms that each baseline is minimal.
- An eighth of M would need m* ≈ 0.83, 0.30, 0.54 and 0.35 USD.

**Correction of the earlier quartering remark.** PLAN_43 said quartering "would need m below the uncertified price of about 3.52". That is accurate only at ε = 1/10 (m* = 3.5343), and even there m* exceeds the uncertified RQMC orientation price by just 0.0154 USD. The orientation price is 3.5188852273893136 (`results/frontier_classical_20261001/c1/c1_summary.json`, uncertified), which is less than the 0.045 bridge. At the other three targets, quartering needs m* ≈ 1.2–2.2 USD, well below that orientation price. Under the orientation, quartering is therefore not reachable at any target, and halving is the most a mean bound can give.

### 2.4 What m must certify (bridge from a continuous-price certificate)

The estimator reads E[g], the digital payoff under the finite input law. Consider a future certificate of the form E[Y] <= m_f, where Y is the ideal continuous discounted strict-140 payoff. Scope #43 gives, per own profile, the conditional bound E|Y_N − Y| <= L1 with outward display 0.045202052. Here Y_N is the native full-payoff node under the #42 coupling. Then

    E[g] = E[Y_N] <= E[Y] + E|Y_N − Y| <= m_f + 0.045202052.

So halving requires m_f <= m* − 0.045202052 USD, which is 19.114571708, 5.222282654, 10.197489316 and 6.040983968 at the four targets. The outward 1e-9 display is a valid upper bound for this sufficient direction. A future scope should still use the exact saved rational `payoff_L1_upper`, not the display.

Using the bridge here spends **no** dollar headroom: it only shifts the a-priori m. The ledger's open dollar terms (finite input law, clipped tail, native arithmetic) stay as they are.

For orientation only (uncertified, not a bound), the required m_f is roughly 5.4x, 1.5x, 2.9x and 1.7x the RQMC price. The 3/100 target therefore needs a mean certificate within about 50% of the true price.

## 3. Work adoption of a mean-aware schedule would need

Each item is a separate, new, preregistered scope; none is part of #43.

1. **Mean certificate (prerequisite; this is U1).** A certified upper bound on E[g], or on E[Y] plus a bridge whose law binding is checked (item 2). Examples: an outward vanilla or Jensen domination of the knock-out basket, or a direct digital-domain bound. No candidate is evaluated here.
2. **Law and node binding.** Prove that the #42 coupling's Y_N is the *same node* (native payoff 5697) as the E02 wrapper's comparator input. Also prove that the coupling's marginal on the Q32 cell midpoints equals the circuit's Hadamard input law: 1920 original uniform bits, and the selector bits must be independent. The E07 ledger lists `finite_input_law_and_joint_Box_Muller` as open, so this binding is not yet established. #42 and #43 are labelled *conditional*, and that label carries through.
3. **New schedule certificate.** Add a variant of `certified_schedule` with an `m` input: `e(m,M) = 2π·sqrt(m(64−m))/M + 64π²/M² (+ readout)`. It needs exact-Fraction sqrt enclosures (an outward sqrt for the error, an inward sqrt for the threshold), a required m <= 32 guard, and the same adjacency check with π_lo. Repetitions are unchanged. Its tests should cover reproducing the E07 row at m = 32, monotonicity in m, and rejecting m > 32 or a float m. The output format needs a new name, and the record must state that the error is *conditional on the m certificate*.
4. **IQFT and rotation synthesis.**
   - **ε ∈ {1/10, 3/100, 1/100}.** The halved schedules need 12, 13 and 15 bits, so rotations up to pi/4096, pi/8192 and pi/32768. All are in `E02_IQFT_run001/rotations.json` (pi/8 … pi/65536), with max operator error ≈ 2.63e-18. That is far below the per-rotation requirement 1/(45000·(t−1)(t−2)), which is 1/4,950,000, 1/5,940,000 and 1/8,190,000 for t = 12, 13, 15; this requirement pattern is checked against the E02 (t = 16) and E24 (t = 15) ledgers.
   - **ε = 1/100 operations ledger.** For the circuit, the E24 13/20 row already emits a 15-bit, 15-shot IQFT operations ledger (`E24_grid_run001/B4x12/13_of_20/iqft_operations.json`): 4095 Rz, full T-count 255,951,625,444,980 against 511,911,060,861,915 at 16 bits. Its dollar error row (13/2000) must **not** be relabelled. A new ledger row must carry 9/2000, conditional on m.
   - **ε = 1/10 and 3/100.** No saved B4 schedule or IQFT operations ledger exists at 12, 13 or 14 bits, so new emission is needed. The rotation certificates can be reused.
   - **ε = 1/1000.** New synthesis of pi/131072 and pi/262144 is needed for 18 bits, plus pi/524288 for the 19-bit baseline. E24 already records `pi_1_131072` as missing for 17 bits.
5. **E07/E02 ledger.** Add a new `complete_price_ledger` row. The statistical term becomes 0.45ε, *conditional on* the m certificate, which is a new certificate premise. If the m certificate carries a probability, its failure goes into the failure union. `QPE_rotation_synthesis` and `physical_execution` stay open.
6. **Wrapper binding.** No circuit change is needed for the mean-aware schedule itself: same wrapper `E02_financial_run002/B4x12/iterate.json`, span 64 and decode. It is enough to re-bind the existing wrapper to the new schedule with fewer QPE bits and to re-emit the QPE register width. The support-tight variant in §4 *does* change the wrapper.
7. **Lifecycle.** The usual prospectus, independent peer review, ROOT_READY, sealed run, saved verifier and ROOT receipt, for each of items 1, 3, 4 and 5 that becomes a scope.

## 4. Normalization alternative: support-tight span (no mean certificate)

Replace the comparator `sel46 < Yraw` with `sel_b < c·Yraw`, where c is an integer, b is the selector width, and c·sup Yraw <= 2^b. The exact integer multiply-by-c is shift-add, and the comparator is still exact with Hadamard selector preparation. Then

    a' = c·E[Yraw]/2^b = E[g]/S',  S' = 2^(b−40)/c,  price = S'·a~'.

Every quantity is exact. The schedule formula with S' in place of 64 is pure-constant arithmetic, and the only scientific premise is the already-audited E03 support (`E03_support_run001/summary.json` sha256 `bb114ee7...`, audit `E03_support_audit_run002`).

Results (`tight_span_variant_arithmetic_run001.json`; the c = 1, b = 46 row reproduces §2.3 exactly):

| (c, b) | S' (USD) | ε = 1/10: M/2 without m? | ε = 3/100: m* for M/2 | ε = 1/100: M/2 without m? | ε = 1/1000: m* for M/2 |
|---|---|---|---|---|---|
| (1, 46), saved wrapper | 64 | no (m ≤ 19.1597) | 5.267484706 | no (m ≤ 10.2426) | 6.086186020 |
| (3, 47) | 42.666666 | **yes** | 9.267075890 | **yes** | 11.202584787 |
| (13, 49) | 39.384615 | **yes** | 10.846501010 | **yes** | 13.750321594 |
| (105, 52) | 39.009523 | **yes** | 11.084873557 | **yes** | 14.217430905 |
| (211, 53) | 38.824644 | **yes** | 11.208921058 | **yes** | 14.476904699 |

With (3, 47), M/4 needs m <= 5.811476 at ε = 1/10 and m <= 3.514349 at ε = 1/100. Neither is reachable under the orientation price once the bridge is added.

Interpretation:
- A one-bit-wider selector plus ×3 removes the mean-certificate dependency for halving at ε = 1/10 and 1/100.
- At 3/100 and 1/1000, it raises the mean threshold that halving needs by roughly 1.8–2.4x, which loosens U1.
- This changes the **wrapper**. Adoption needs:
  - a newly emitted predicate: a constant multiplier and its uncompute, plus a b-bit comparator and b Hadamard selector bits;
  - new source-graph and marking checks, and an all-input support re-check for c·Yraw <= 2^b;
  - a re-derived readout allowance (2^-39 is only a placeholder here);
  - a new schedule, IQFT ledger and E07 ledger.

  Per-call cost rises by one multiplier. I did not evaluate that cost; it is expected to be small next to the 520,750,804 T per source iterate, but that is unproved.
- E24's 13/20 share already halves at ε = 1/100, but only by cutting headroom to 7/2000, which is below the 1/200 half-bias budget. Both mean-aware halving and support-tight halving keep the 11/2000 headroom.

## 5. Premises (path, sha256)

| Premise | SHA256 |
|---|---|
| results/limitation_program_20261001/E07_schedule_run001/schedule.json | 4fdd33add8e18f83680bcda21f38fb0bb67cc1017323717b89a52165cb59b335 |
| …/E07_schedule_run001/summary.json | ac53dda516a97d8e535d1eced5f549f83116834bb2d3333ee653a45bd27a2ddf |
| …/E07_schedule_run001/protocol.json | 0894809f2feb4c3f88fc866b1895e6ddc25af17c3aa15d926594e193dd1672dd |
| …/E07_schedule_run001/manifest.json | fbdac6d588e1b893f7731c940c85002de6bcdd5c2a2514469fcb137c72052d75 |
| …/E07_schedule_run001/complete_price_ledger.json | bc07fa6f834160d60d2db8875a25088fcff6cd9b18ffb131150566bb52d28dcb |
| …/E07_schedule_run001/executed_code/financial_bounded_schedule.py | 4452c3319e9b7c33b96276aeefe137905d41c4638e42037d264fd6bdd26f149c |
| …/E07_schedule_run001/executed_code/test_financial_bounded_schedule.py | 4a2f3c5c2bafd944cb5f441bfd2aa9682a21239e76e16951116b28f0425aac37 |
| results/limitation_program_20261001/E02_IQFT_run001/rotations.json | 429a1bc35d7a9a365abbe1ff56c6ae10eb02e5167eb1c5b9bc1d3eeafb56effc |
| …/E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json | d2eb29c7c92d6eda32879e5e040a8e5280432fa42417f7c60c1d2ac2db3ba405 |
| …/E02_IQFT_run001/B4x12/iqft_operations.json | 7bd30a31a023a20b0a93e828f213c7f50fe07ebd840ee67098a22c698ebaf905 |
| results/limitation_program_20261001/E24_grid_run001/summary.json | 5504c21d022bc61e0b2d436f391884ad5c82224796d787171004b4811da7f730 |
| …/E24_grid_run001/B4x12/13_of_20/digital_estimator_row.json | 8039d3a47f2909d7d9ed9d3e02ab1a6b5d0516372d1545312db37363855dc214 |
| …/E24_grid_run001/B4x12/13_of_20/iqft_operations.json | 10059560a2e94ee6c6c1aaa88793dc31d453ca2c218ded5d297a3cb357228f34 |
| …/E24_grid_run001/B4x12/13_of_20/schedule.json | 6164d39e37c9db62e0bb30be57d148861394b890c07d19b11bd9c324ff4a8f60 |
| results/limitation_program_20261001/E03_support_run001/summary.json | bb114ee72a837cd379987b73b9d40b7c3b9ebf6129340598cffd2551ca1c9524 |
| results/limitation_program_20261001/E03_support_audit_run002/summary.json | 43209c88565a1281f4c643b075add354078c3511a33ef0fa9caa08688b83cd47 |
| docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md (#42) | c43d0f35483491de3b3057c0803ac24011767f57b9fb40e63e902d82ec4cdc90 |
| docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md (#43) | 512e879c42b206b0d79897850b39d3fcc167cc0e7188abf901bbdfa6ed639b04 |
| .context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json (#43 ROOT) | 87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7 |
| results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json | c488f82b5fe04f578b33f2a060b99e6da387263b0da49cb2651691f1a23d32d6 |
| …/independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json | 663e25dd2fc990185400972b7f1c3be0fe04cb87a780dd7adfd35e2b61584910 |
| .context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run002.md (coupling and Q32 midpoints) | 04b491906b3dfadfb790fee41f7bca8dfc98991a7929770c785ad1ced3c0cc59 |
| .context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json (four targets and half-bias budgets) | de6d09fe50db48939e335d2a9aa4db112a3371a12d66fa7177b76bf5eae10e25 |
| manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md | b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637 |
| docs/limitation_audit_20261001/implementation_plan/CONTRACT.md (C05: 0.45ε share) | c90588139c60a1cf820c26c4051c16661309d714e2947a3257a5773c3e8e2ce2 |
| docs/limitation_program_20261001/STATUS.md (E10 scope C4/H8 only) | 0e8dbe484afe274c7a723dc8a823c4eaa520198364950c158a69745bedf22d88 |
| results/frontier_classical_20261001/c1/c1_summary.json (uncertified orientation price) | 5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123 |
| scratchpad wf1/PLAN_43.md (earlier note, re-verified here) | 3d44ee1ddb19dcb23bc3418b2a9cc96b49014dc69b0e59c01b1f3f5859f3d405 |
| scratchpad wf1/moment_estimator_inventory.json | e3712e9b164a86ce0086f4b4c070c512e724d797ff851ad5c2a75ce8ed8b5b29 |

## 6. Open obligations

- **O1.** No certified upper bound on E[g] or E[Y] for B4x12 exists. All halving claims are conditional on one existing (U1).
- **O2.** Bind the #42 coupling's Y_N to the E02 comparator input (node and finite Hadamard input law). The #42 and #43 bridges are conditional records.
- **O3.** Use the exact `payoff_L1_upper` rational, not the 1e-9 display, in any future certificate.
- **O4.** A new exact schedule function with an m input, with tests and preregistration. Only the ε = 1/100 baseline is saved; the 1/10, 3/100 and 1/1000 baselines here are unsaved formula evaluations.
- **O5.** IQFT operation ledgers at 12, 13 and 14 bits (new emission). Rotation synthesis of pi/131072, pi/262144 and pi/524288 for ε = 1/1000.
- **O6.** A new E07 ledger row in which the statistical term is conditional on the m certificate, with any m-certificate failure added to the union. The `QPE_rotation_synthesis` and `physical_execution` terms remain open.
- **O7.** The support-tight variant (§4) needs a new wrapper, a support re-check of c·Yraw, a readout re-derivation and a cost delta. None of these was evaluated.
- **O8.** Earlier PLAN_43 wording to correct in any future write-up:
  - the thresholds are roundings, three of them upward;
  - "only plausible route" is superseded by §4;
  - the quartering remark holds only approximately, and only at ε = 1/10.

## 7. Non-claims

This note claims none of the following:
- **Bias:** no measured bias.
- **Accuracy policy:** no accuracy policy or price-accuracy success.
- **Estimator saving:** no adopted estimator saving. Halved call counts are conditional design arithmetic.
- **Moments:** no moment or variance transfer, since no certified continuous B4x12 second moment exists.
- **Program status:** no G2, no physical delivery or runtime, and no quantum advantage. Nothing changes E11's "partial" status or any program record.
- **Comparison:** no new comparison against classical methods.

The RQMC price is quoted only as uncertified orientation.
