# Fixed polar-safe h=1/128 four-target accuracy check (scope #44), prospectus DRAFT

**This is a design draft. It is NOT a preregistration.** It was written on
2026-10-10 by a parallel design subagent (task U4), outside the program
lifecycle. It sits under `docs/parallel_E11_unblock_20261010/` and nothing
in `.context/`, `results/limitation_program_20261001/` or
`docs/limitation_program_20261001/` refers to it. It carries no SHA pin,
stat8 fingerprint, review or authorization. The program is at
USER_REQUESTED_STOP_CHECKPOINT after scope #43, and the #43 ROOT receipt
records `beyond44_SCI_authorized=false`. Scope #44 needs explicit user
authorization (lifecycle step 0 below). Before any lifecycle use, an author
must re-transcribe this text into a fresh `.context/` prospectus. That author
then owns the transcription and must disclose this draft as its origin.

No new scientific bound was evaluated for this draft, and no saved limb
operand was decoded. The only arithmetic done was on exact pure constants
(the four budgets, the 11/2000 headroom, B_band's closed form, 97/100, 40).
The magnitudes quoted below (~0.04648, ~0.045202, ~1.6262, ~38.818) are
copied from already-saved, already-disclosed sources: the #43 prospectus
disclosure, the #43 verified results page and the task's verified
background. They were not recomputed.

## Fixed route (inherited from #42/#43, not re-tuned)

Same coupling and parameters as #42 and #43: lambda=2^-18, h=1/128, H=140,
Q=2^40, kernel M=4608, the outward sqrt128 grid, the product-60 coupling and
the safe event E. The two own profiles, primary90 and independent130, are
kept separate. There is no cross-profile minimum, selection or aggregate
field.

    Y_N = native node 5697 = select(5644, 5696, 13)
    Y   = exp(-3/100)*(A-100)^+ * 1{ideal strict-140 survival}
    bias_pi := |E[Y_N] - E[Y]|   under profile pi's own certificates

#44 adds no new probability statement. It only compares, as exact
rationals, three already-sealed upper bounds per profile against fixed
pure-constant budgets.

## Statement to be checked (per own profile pi, separately)

The three valid upper bounds on bias_pi are:

    bias_pi <= m_pi                     (#42 conditional mean certificate)
    bias_pi <= E|Y_N-Y| <= L1_pi         (Jensen; #43 L1 certificate)
    bias_pi <= ||Y_N-Y||_2 <= sqrt(L2SQ_pi) <= RMS_pi    (Jensen; #43 L2 certificate)

All three are conditional on the #42/#43 premises (P1-P10 of the #43
prospectus). The Jensen steps need Y_N and Y on one probability space whose
marginals are the native digital law and the ideal law. That is the #42
coupling premise; #44 inherits it and does not re-prove it (obligation O1).

Fixed targets and budgets (exact, read from saved files, never chosen in
#44):

| k | epsilon_k (USD) | half-bias budget b_k = epsilon_k/2 | b_k^2 |
|---|---|---|---|
| 1 | 1/10 | 1/20 | 1/400 |
| 2 | 3/100 | 3/200 | 9/40000 |
| 3 | 1/100 | 1/200 | 1/40000 |
| 4 | 1/1000 | 1/2000 | 1/4000000 |
| H | 1/100 (E07 ledger only) | headroom 11/2000 | 121/4000000 |

The headroom row H applies only at epsilon=1/100. There, the saved E07
ledger splits 1/100 = 9/2000 (bounded-AE statistical share) + 11/2000
(`remaining_dollar_headroom`). That 11/2000 is shared with all three open
E07 dollar terms (`finite_input_law_and_joint_Box_Muller`,
`clipped_log_tail`, `native_arithmetic_and_polynomial`). Row H is reported
separately from row 3. It never replaces b_3, and it is never applied to
epsilon != 1/100.

## Saved fields compared (JSON pointers)

Profile files (per own profile; `{P}` = `primary` / `independent`):

- #42: `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_uniform_error_test_run001/{P}_fixed_polar_safe_h128_uniform_error_feasibility.json`
- #43: `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/{P}_fixed_polar_safe_h128_payoff_squared_L2_bridge.json`

All rationals use schema `canonical-nonnegative-rational-base2p32-v1`
(little-endian base-2^32 numerator/denominator limbs, sign "positive").
#44 compares them only as reduced exact rationals.

**Classifying operands** (the only fields whose value decides a row):

| Symbol | File | JSON pointer |
|---|---|---|
| m_pi | #42 | `/conditional_full_payoff_mean_bias_upper` |
| L1_pi | #43 | `/payoff_L1_upper` |
| L2SQ_pi | #43 | `/payoff_squared_L2_upper_L2SQ` |

**Gate fields** (all must hold, or the negative branch applies):

| File | JSON pointer | Required |
|---|---|---|
| #42 | `/profile` | `primary90` / `independent130`, matching the #43 file |
| #42 | `/schema` | `e11-B4x12-fixed-polar-safe-h128-pointwise-feasibility-limb-profile-v1` |
| #42 | `/outcome` | `conditional_payoff_mean_certificate` |
| #42 | `/all12_fixed_basket_criterion_passed` | `true` |
| #42 | `/all12_simultaneous_on_same_fixed_safe_event` | `true` |
| #42 | `/full_payoff_mean_certificate_adopted` | `true` |
| #43 | `/profile` | same as #42 |
| #43 | `/schema` | `e11-B4x12-fixed-polar-safe-h128-payoff-squared-L2-bridge-limb-profile-v1` |
| #43 | `/outcome` | `conditional_payoff_squared_L2_certificate` |
| #43 | `/payoff_squared_L2_certificate_adopted` | `true` |
| #43 | `/all_rational_checks_passed` | `true` |
| #43 | `/rational_checks/R1` ... `/rational_checks/R7` | all `true` |
| #43 | `/inherited42_all12_fixed_basket_criterion_passed`, `/inherited42_all12_simultaneous_on_same_fixed_safe_event` | `true` |
| #43 | `/inherited42_profile_file/expected_SHA256` | equals SHA256 of the own #42 profile file (369f1635... / 5447209f...) |

**Consistency operands** (re-derived; never classifying):

| Symbol | File | JSON pointer |
|---|---|---|
| E_s | #42 and #43 copy | `/conditional_smooth_survival_payoff_error_upper`; `/inherited42_conditional_smooth_survival_payoff_error_upper` |
| p | #42 and #43 copy | `/conditional_mismatch_probability_upper`; `/inherited42_conditional_mismatch_probability_upper` |
| m copy | #43 | `/inherited42_conditional_full_payoff_mean_bias_upper` |
| B_band | #42, #43 | `/components/fixed_ideal_band_probability_upper` |
| polar_bad | #42, #43 | `/components/polar_bad_event_probability_upper` |
| U, eta, tau | #42, #43 | `/components/own_discount_U`, `/components/own_discount_literal_error_eta`, `/components/native_discount_floor_tau` |
| C_J | #43 | `/components/payoff_jump_constant_C_J` |
| RMS (display cross-check only) | #43 | `/payoff_RMS_sqrt128_upper`, `/payoff_RMS_sqrt128_witness/outward_order_and_strict_sqrt_grid_gap_passed` |

**Budget sources** (pure constants, read and checked, not chosen):

| Constant | File | JSON pointer |
|---|---|---|
| four epsilon_k | `.context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json` | `/four_original_targets_dollars` = [[1,10],[3,100],[1,100],[1,1000]] |
| four b_k | same | `/bias_budgets_dollars` = [[1,20],[3,200],[1,200],[1,2000]] |
| headroom | `results/limitation_program_20261001/E07_schedule_run001/complete_price_ledger.json` | `/assessment/remaining_dollar_headroom` = [11,2000], `/epsilon_dollars` = [1,100], `/assessment/known_dollar_bound_sum` = [9,2000] |
| statistical share | `results/limitation_program_20261001/E07_schedule_run001/schedule.json` | `/statistical_error_dollars_exact` = [9,2000] |

## Exact comparison rule (fixed in advance; no tunable parameter)

For each own profile pi and each row k in {1,2,3,4,H}, with budget b
(b_k, or 11/2000 for H), comparisons are exact cross-multiplications of
reduced nonnegative rationals:

    MEAN_k(pi) = "compatible"   iff  m_pi    <= b
    L1_k(pi)   = "compatible"   iff  L1_pi   <= b
    L2_k(pi)   = "compatible"   iff  L2SQ_pi <= b^2      (exact; never via the RMS display)
    otherwise the row is "certificate_route_ruled_out".

- **Equality.** Equality counts as compatible. The quantity being bounded
  satisfies bias <= bound = b, so equality is not a failure. (In the any-h
  four-target scope, equality was "inconclusive". That convention applied
  to a necessary-condition threshold, not to an upper bound. #44 uses the
  upper-bound reading and says so.)
- **Per-row output.** For each pi and k, #44 emits the three row
  classifications. It also emits a per-profile route summary:

      ROUTE_k(pi) = "conditional_route_compatible_necessary_not_sufficient"
                    if any of MEAN_k, L1_k, L2_k is compatible,
                    else "certificate_route_ruled_out".

  The OR is fixed before evaluation and is deterministic. It does not
  select between profiles. Because L1 <= m (T4) and L1 <= sqrt(L2SQ) (T5)
  are exact identities on the saved fields, the OR always equals the L1
  row. The three rows are kept for transparency.
- **Ruled out.** "certificate_route_ruled_out" means only that this fixed
  conditional certificate route (lambda=2^-18, h=1/128, jump constants 40
  and C_J) cannot certify that budget. It is not a lower bound on bias and
  says nothing about the price, other routes or other loaders.
- **Compatible.** "compatible" means only that this one conditional
  coupling-bias certificate fits inside that half-budget. It is not
  epsilon-accuracy. The statistical share, IQFT synthesis, physical
  failure, confidence, and binding to E07 ledger rows remain open (O2-O5).
- **No aggregation.** No cross-profile minimum, maximum, "both" or "either"
  field is emitted.

## Exact consistency checks (per own profile; any failure -> negative branch)

- **T1 (binding).** #43 `/inherited42_profile_file/expected_SHA256` ==
  SHA256(own #42 profile file). Both `/profile` fields are equal.
- **T2 (copy equality).** #43 `/inherited42_conditional_full_payoff_mean_bias_upper`,
  `/inherited42_conditional_mismatch_probability_upper` and
  `/inherited42_conditional_smooth_survival_payoff_error_upper` are
  limb-identical to the #42 originals.
- **T3 (inherited identities).** m == E_s + 40*p (R3). p == min(1,
  polar_bad + B_band) with polar_bad == 15/65536 (R2).
  B_band == (1/1176)*(1+1/963379197) == 481689599/566466967836. C_J ==
  40*(U+eta)+tau. E_s <= C_J <= 40 (R4).
- **T4 (mean dominates L1).** m - L1 == p*(E_s + 40 - C_J) >= 0. This is an
  exact identity: m - L1 = E_s + 40p - E_s(1-p) - C_J p.
- **T5 (L2 dominates L1).** L2SQ - L1^2 == p*(1-p)*(C_J - E_s)^2 >= 0. This
  is the exact two-point variance identity for the LP weights
  (1-p, p) on (E_s, C_J).
- **T6 (RMS display consistency).** RMS^2 >= L2SQ, and the saved sqrt128
  witness flag is true. If RMS <= b then L2SQ <= b^2 must also hold.
- **T7 (budget constants).** b_k == epsilon_k/2 for all four rows.
  9/2000 + 11/2000 == 1/100. The read budget arrays equal the literals
  above.
- **T8 (forced-outcome witnesses, see lemmas).** p >= B_band.
  B_band > 1/1176. U >= 97/100. m >= 40*B_band. L1 >= C_J*B_band.
  L2SQ >= C_J^2*B_band.

## Forced-outcome lemmas (symbolic; exact pure constants only)

Write d = exp(-3/100).

- **S0.** By R2, B_band = (1/1176)(1 + 1/963379197) > 1/1176. Also
  p = min(1, 15/65536 + B_band) >= B_band, since B_band <= 1.
- **S1 (mean route).** m = E_s + 40p >= 40p >= 40*B_band > 40/1176 = 5/147.
  Then 5/147 > 3/200 (1000 > 441), and 5/147 > 11/2000 > 1/200 > 1/2000
  (10000 > 1617). So MEAN_2, MEAN_3, MEAN_4 and MEAN_H are forced to
  "ruled_out". 5/147 < 1/20 (100 < 147), so MEAN_1 is **not** forced.
- **S2 (L1 route).** L1 = E_s(1-p) + C_J p >= C_J*B_band. Also
  C_J = 40(U+eta)+tau >= 40U >= 40d >= 40*(97/100) = 194/5. This uses
  eta, tau >= 0, U >= d (the own enclosure; #43 premise P2) and
  e^{-x} >= 1-x. Hence L1 > (194/5)/1176 = 97/2940 ~ 0.03299. Then
  97/2940 > 3/200 (19400 > 8820) and 97/2940 > 11/2000 (194000 > 32340).
  So L1_2, L1_3, L1_4 and L1_H are forced to "ruled_out". 97/2940 < 1/20
  (1940 < 2940), so L1_1 is **not** forced. Design magnitude (disclosed,
  not recomputed): C_J*B_band ~ 38.818/1176 ~ 0.0330.
- **S3 (L2 route).** L2SQ = E_s^2(1-p) + C_J^2 p >= C_J^2*B_band >
  (194/5)^2/1176 = 9409/7350 > 1 > 1/400 = b_1^2. So L2 rows 1-4 and H are
  **all** forced to "ruled_out", including epsilon=1/10. This is expected.
  The RMS of the coupling difference is a much weaker bias bound than L1
  (T5), because the band event carries jumps of size ~C_J.

So for each profile, 13 of the 15 classifying rows (5 rows x 3 bounds) are
fixed by pure constants applied to identities that #43 already verified.
Only MEAN_1 and L1_1 depend on a saved operand's actual value.

## Expected outcome (stated before any #44 run; identical for both profiles)

| Row | b | MEAN | L1 | L2 | ROUTE |
|---|---|---|---|---|---|
| 1: epsilon=1/10 | 1/20 | compatible (expected; m ~ 0.04648) | compatible (expected; L1 <= 0.045202052 outward display) | ruled_out (forced, S3) | conditional_route_compatible_necessary_not_sufficient |
| 2: epsilon=3/100 | 3/200 | ruled_out (forced, S1) | ruled_out (forced, S2) | ruled_out (forced, S3) | certificate_route_ruled_out |
| 3: epsilon=1/100 | 1/200 | ruled_out (forced) | ruled_out (forced) | ruled_out (forced) | certificate_route_ruled_out |
| 4: epsilon=1/1000 | 1/2000 | ruled_out (forced) | ruled_out (forced) | ruled_out (forced) | certificate_route_ruled_out |
| H: E07 headroom, epsilon=1/100 only | 11/2000 | ruled_out (forced) | ruled_out (forced) | ruled_out (forced) | certificate_route_ruled_out |

On this route, the result is compatible only with epsilon=1/10, and only
through the mean and L1 rows. It is ruled out for 3/100, 1/100 and 1/1000.
The structural reason is the band term: C_J*B_band ~ 0.033 > 3/200, and
40*B_band = 5/147*(1+1/963379197) ~ 0.0340 > 3/200.

The epsilon=1/10 margin is small. From the disclosed magnitudes,
1/20 - m ~ 0.0035 (about 7% of the half-budget) and 1/20 - L1 ~ 0.0048.

**Outcome predictability (disclosure).** The expected outcome is
effectively known before any run:

- L1_1 compatibility already follows from the verified #43 outward display
  L1 <= 0.045202052 < 0.05. That display is reporting-only, so the #44 rule
  must still compare limbs.
- MEAN_1 follows from the decoded #42 magnitudes disclosed in the #43
  prospectus: E_s ~ 3.3126e-3 and p ~ 1.0792e-3, so m ~ 0.04648.

#44 therefore adds saved-checked custody, not new information. See the
expected-value section.

## Five metadata controls (artificial; positive first; inherited convention)

Each control mutates the #44 rule on artificial operands and must be
rejected.

- **CROSS_PROFILE_MINIMUM**: classify with min(m_primary, m_independent),
  or emit any cross-profile aggregate.
- **EQUALITY_BOUNDARY**: an operand exactly equal to b (artificial
  m == 3/200) is classified "ruled_out", or a strict "<" rule is used.
- **L2_UNITS**: L2SQ compared to b instead of b^2, or the RMS display used
  as the classifying operand.
- **HEADROOM_SCOPE**: 11/2000 applied to epsilon != 1/100, or substituted
  for b_3 = 1/200, or treated as available to the E11 term alone.
- **POLICY_ADOPTION**: a compatible row emits
  `accuracy_policy_adopted=true`, `price_accuracy_certified=true` or any
  estimator or schedule change.

As in #43, `positive_first=true`: the unmutated rule on artificial operands
runs first and must reproduce a preregistered classification vector.

## Rejected alternatives

- **New sharper bound** (relative barrier transport, exact
  P(E^c) = 1-(1-2 lambda)^30, dropping +tau). That is a new scientific bound
  and not a comparison. Relative barrier transport is projected at mean
  ~ 0.019 in the earlier design notes (`wf1/PLAN_43.md` section 5,
  unverified projection), which is still > 3/200.
- **Re-tuning h or lambda** to fit a budget. Forbidden as post hoc.
- **Variance or second-moment transfer for an MSE-style criterion.**
  Blocked by P11: no certified continuous B4x12 second moment exists, and
  E10 covers C4/H8 only.
- **Treating RMS <= b as the bias criterion.** Kept only as the L2 row. It
  is dominated by L1 (T5) and is not the governing bias quantity.
- **Classifying "inconclusive" on equality**, as the any-h necessary
  conditions did. Not adopted, because these are upper certificates.
- **Comparing against the A02 native financial-bridge B4 bias**
  (~0.000214 USD in the STATUS.md A02 row). That is a different route and
  loader. #44 makes no cross-route comparison and no claim about that row.

## Premises (path, SHA256 as read 2026-10-10)

Sealed #43 run
(`results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/`):

- `primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json`: `c488f82b5fe04f578b33f2a060b99e6da387263b0da49cb2651691f1a23d32d6`
- `independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json`: `663e25dd2fc990185400972b7f1c3be0fe04cb87a780dd7adfd35e2b61584910`
- `manifest.json`: `2f3162d8647888e424a01caadc0eff70cb481167a291a23462789eff380fa3f9` (pinned by the #43 ROOT receipt)
- `summary.json`: `5003fa2451d9c7717aefc846f7d476e43c98619bbef23b89ed3d0b51513ef500`
- `same_profile_reconciliation.json`: `2959479c37e5dbb98c34c3d1812f7e3c33a781b34eb9ff82c8afb9d57155871d`
- `executed_controller.py` (= #43 SOURCE `research/limitation_program_20261001/experiment_e11_b4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_v1.py`): `870214680675e618eb64c45c38074e4f83ccac6911564cf04f237a3bddf3af58`

Sealed #42 run
(`results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_uniform_error_test_run001/`):

- `primary_fixed_polar_safe_h128_uniform_error_feasibility.json`: `369f16352cd77be2a621f14d2810f24c58227248ffbebf004cf8b8208b639dc4`
- `independent_fixed_polar_safe_h128_uniform_error_feasibility.json`: `5447209f05c17e99c89bb893793a5d62506de1dd6bfc1078eb1cba3e54484704`
- `manifest.json`: `e3b748925b525e0bb1154e438016b005bf30b7bf73461d0133034e763f937901`
- `summary.json`: `82203b9d9c31ce0ccdc23df4d4c4ab360c237e212bd2b5fdb23ad88fce37dd2c`
- `same_profile_reconciliation.json`: `59b799899dcc2196b83cc54d53b78a42143ed43de3cc1fd2610eea2b2595d2db`

ROOT receipts and prospectus:

- #43 ROOT saved verification `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json`: `87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7`
- #42 ROOT saved verification `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_UNIFORM_ERROR_TEST_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json`: `c5f1bf3f358e537274bac297581d5e9e7f1c246072059b04886d607f4cea3e33`
- #43 prospectus MD `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_BRIDGE_run001.md`: `6a70fc53f245ec8ee4f6dc2c87d3ba893126167c281707b22181c00ed84ca818`
- #43 prospectus JSON `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_BRIDGE_run001.json`: `9c363bd7aae3e165d530ab1c11a53181ebb26a5e63d7fc16a9eaec3337237e94`
- #43 independent prospectus peer `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_INDEPENDENT_PROSPECTUS_PEER_run001.json`: `2f123d526863fed8cc7c5edd9b908741b1d031ae23b21eaeaccf038f41439be2`
- Four-target ROOT conditional review `.context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json`: `de6d09fe50db48939e335d2a9aa4db112a3371a12d66fa7177b76bf5eae10e25`
- Any-h four-target ROOT result verification `.context/E11_B4X12_ANY_H_FOUR_TARGET_CERTIFICATE_STRENGTH_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json`: `da012791afcb7cf2d9fa1a062435cad899a1c9191073801c0f86be69e6b25ceb`

Estimator ledger (E07):

- `results/limitation_program_20261001/E07_schedule_run001/schedule.json`: `4fdd33add8e18f83680bcda21f38fb0bb67cc1017323717b89a52165cb59b335`
- `.../summary.json`: `ac53dda516a97d8e535d1eced5f549f83116834bb2d3333ee653a45bd27a2ddf`
- `.../complete_price_ledger.json`: `bc07fa6f834160d60d2db8875a25088fcff6cd9b18ffb131150566bb52d28dcb`

Docs (context only):

- `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md`: `c43d0f35483491de3b3057c0803ac24011767f57b9fb40e63e902d82ec4cdc90`
- `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md`: `512e879c42b206b0d79897850b39d3fcc167cc0e7188abf901bbdfa6ed639b04`
- `docs/limitation_program_20261001/E11_ANY_H_FOUR_TARGET_FEASIBILITY_RESULTS_20261008.md`: `ec90df235b10b2e3d8a7533870f5e78b46d61030bc8d8b582fce44fa39495f7e`
- `docs/limitation_program_20261001/CHECKPOINT_20261009_PAYOFF_L2.md`: `dfaba4cd6ec29bf6862800134976df4d8e6c6f4858f7458aeeb593cca890b7b4`
- `docs/limitation_program_20261001/STATUS.md` (E10/E11/A02 rows): `0e8dbe484afe274c7a723dc8a823c4eaa520198364950c158a69745bedf22d88`
- `manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md`: `b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637` (equals the pin in the four-target review)
- `results/limitation_program_20261001/progress.json`: `22beb45e8050e56ac7e91f2a3c354c04851cc38fce426d1a7b6615d488c57198` (phase "USER_REQUESTED_STOP_CHECKPOINT:43 ...")

Earlier session design notes (re-verified in substance above, not trusted
as authority):

- `C:/Users/prith/AppData/Local/Temp/claude/C--Users-prith-quantum-option-pricing/3cc032fb-36f0-4c77-b733-779e62fbfea3/scratchpad/wf1/PLAN_43.md`: `3d44ee1ddb19dcb23bc3418b2a9cc96b49014dc69b0e59c01b1f3f5859f3d405` (equals the #43 JSON design-pass pin)
- `.../wf1/moment_estimator_inventory.json`: `e3712e9b164a86ce0086f4b4c070c512e724d797ff851ad5c2a75ce8ed8b5b29`

Re-verification of PLAN_43 section 2(d):

- Its claim that only epsilon=1/10 fits is confirmed by S1/S2, with the
  exact constants 5/147 and 97/2940.
- Its figure "C_J*B_band = 0.0330" is consistent with the symbolic lower
  bound 97/2940 ~ 0.03299.
- Its statement that the L2 route is weaker (b >= 1.275) is confirmed by
  S3.

Not re-verified: the PLAN's estimator break-even figures in 2(a)-(c). #44
does not use them.

The reporter must re-pin at authoring time, because the working tree is
dirty. HEAD `04637210b5db6e6554cd12583e50aecac10dee0e`, primitives.py
`02b983af3f5afb538f5448aad372e214f6a3740a0c19fb017d633e302a278daf`,
checkpoint run026 `8d3de5286c9fdef9ff840007d8dce0f5f35abd60f1619fb9e794eeb4cefe5bc8`,
progress run038 `6ee0aaa16a6381706805f39aa1275c3995222ac721a84e75b185b4a4a1274544`,
AUDIT43 `d61f29aae451be96337b73bf2284b6725c665be944ddbf8fbb07e0ce11f432c4`.

## New obligations (for the peer) and open obligations

- **Q1 (new, for peer acceptance).** Upper-bound comparison semantics:
  bias <= bound <= b means compatible, including equality. Bound > b means
  the route is ruled out only, never a bias lower bound.
- **Q2 (new, for peer acceptance).** The Jensen chain
  |E Y_N - E Y| <= E|Y_N-Y| <= ||Y_N-Y||_2 on the #42 coupling, so that L1
  and L2 rows are valid bias rows.
- **Q3 (new, for peer acceptance).** Lemmas S0-S3, including U >= d >= 97/100
  and the identities T4/T5.
- **O1 (inherited, open).** The coupling marginals equal the native digital
  law and the ideal law (#42 P1). #44 does not re-prove this.
- **O2 (open).** Binding the E11 coupling term to the E07 `dollar_terms`
  rows is not done. Which of `finite_input_law_and_joint_Box_Muller`,
  `clipped_log_tail` and `native_arithmetic_and_polynomial` the term
  discharges is not established.
- **O3 (open).** No saved bounded-AE schedule exists for epsilon in
  {1/10, 3/100, 1/1000}. E07 covers only 1/100. So even ROUTE_1
  "compatible" has no statistical partner.
- **O4 (open).** QPE/IQFT rotation synthesis and the physical-execution
  failure allowances (E07 `failure_terms` 1-2) remain None.
- **O5 (open).** The conditionality of #42/#43 (P1-P10, and the single
  shared native graph for controller lines 305/314) is inherited, not
  re-audited.
- **P11 (missing, out of scope).** No certified continuous B4x12 second
  moment exists.

## Negative branch and failure action

- **Negative branch.** If any gate field or T1-T8 check fails for a
  profile, the SOURCE still seals all 13 files. That profile's rows are
  `no_conditional_certificate_available`, which is neither compatible nor
  ruled out, and the outcome is `negative_four_target_check_feasibility`.
  There is no fallback, re-tuning or substitution of the other profile.
- **SCI failure.** Writes FAILED_UNSEALED and gets ROOT failure custody,
  credit 0, no retry and no reseal. Repair is only through a distinct v2
  SOURCE with a new peer/ROOT cycle.
- **Metadata helper failure.** An assert before the write keeps the helper,
  and the next attempt is runNNN+1 (`preserved_prepublication_metadata_failure`).

## Caps (unchanged from #42/#43)

- default4300;
- CPU 180 s, admission 150 s, wall 600 s;
- RSS 157286400 bytes;
- 131072-bit reduced and 524288-bit temporary frontiers;
- <= 4096 limbs, emitted JSON integers <= 256 bits;
- an exact 13-file inclusive ledger and 128 MiB of output;
- five artificial metadata controls, positive first.

#44 needs no sqrt, no arrays and no limb arithmetic beyond products of
already-reduced rationals with small constants. The squares b_k^2 and the
T5 product are the largest terms.

## Disclosure

- Drafted by parallel design subagent U4 on 2026-10-10, read-only on all
  pinned paths.
- The magnitudes quoted are copies of: the #43 prospectus design-pass
  disclosure (E_s, p, C_J, L1, L2SQ), the verified #43 results-page
  outward displays, and the task's verified background for the #42 mean
  (~0.04648).
- No limb was decoded, and no saved operand was compared against any
  budget.
- The only computation was a pure-constant Fraction check of the S0-S3
  constants and orderings, using the system interpreter with -I -S -B.
- No controller, launcher, verifier or reporter was run.
- U4 must not serve as the #44 independent prospectus peer, SOURCE peer,
  FIELD peer or overall auditor.

## Expected value of running #44 (design judgment)

**Low information gain.** The value is custody and accounting. 13 of 15
rows per profile are forced by pure constants on already-verified
identities. The other 2 classifying rows (MEAN_1, L1_1) are implied by
already-disclosed or verified displays. The L2 rows are all forced.

#44 would turn the statement "the fixed polar-safe E11 route certifies the
coupling bias only within the epsilon=1/10 half-budget" into a
saved-checked scope (count 43 -> 44). It does not change E11's status
(partial), estimator work (E07 bounded AE never reads a moment), fixture
credit or whole-limitation credit (0).

**Cheaper alternative.** Record lemmas S0-S3 as an annotation to the #43
results. This counts for nothing in the saved-checked tally, but it costs
no lifecycle.

**More informative next scope** (from PLAN_43 section 2, not re-verified
here): U1, a certified continuous B4 price upper bound plus a new
mean-aware bounded-AE schedule. It is the only listed route that could
change estimator work, by at most 2x at epsilon=1/100.

## Lifecycle #44 would need if the user authorizes it (mapped from #42/#43)

- **Name stem:** `E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK`;
  lowercase `fixed_polar_safe_h128_four_target_check`.
- **Output directory:** `results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_four_target_accuracy_check_run001/`.
- **Interpreter:** `.context/frontier_t0_env/Scripts/python.exe -I -S -B`,
  default4300, no scientific imports.
- **Writes:** every write uses exclusive create.
- **Roles:** A = prospectus author, S = SOURCE author, C = checker author,
  P = independent peers, R = reporter.

| # | Step | Files to create | Role | Gate |
|---|---|---|---|---|
| 0 | User authorization | n/a | user | Explicit yes to lift the #43 stop for #44 metadata work. A separate explicit yes for SCI. New receipts set `beyond45_SCI_authorized=false`. |
| 1 | Prospectus | `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_run001.{md,json}`, helper `.context/E11_fixed_polar_safe_h128_four_target_check_metadata_author_run001.py` | A (discloses this U4 draft) | Symbolic only. Pointer table, comparison rule, T1-T8, S0-S3, five controls, expected-outcome table, premise pins (SHA256 + stat8), caps, failure_action. `separate_ROOT_and_independent_full_proof_review_required_before_SOURCE_authoring=true`. No operand evaluated. |
| 2 | Operand-role inventory | `.context/E11_fixed_polar_safe_h128_four_target_check_operand_roles_metadata_inventory_run001.py`, `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_OPERAND_ROLE_INVENTORY_run001.{md,json}` | A or a disclosed inventory author | Field shape only. Maps every pointer above in all four profile files plus the budget sources. Pins the #42/#43 manifests and ROOT receipts. No limb decoding. |
| 3 | Independent prospectus peer | `.context/review_E11_fixed_polar_safe_h128_four_target_check_PROSPECTUS_METADATA_run001.py`, `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_INDEPENDENT_PROSPECTUS_PEER_run001.json` | P (not A, not U4) | Must explicitly accept Q1, Q2 and Q3, the equality convention and the headroom-scope restriction. `passed`, `science_static_passed` and `lifecycle_static_passed` true, `blockers []`. |
| 4 | ROOT conditional review | `.context/ROOT_E11_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_CONDITIONAL_REVIEW_run001.json` | ROOT | Requires the peer pass. `bounded_actual_SOURCE_authoring_permitted=true`. SOURCE, READY, SCI and result stay false. |
| 5 | Scientific body drafts | `.context/E11_fixed_polar_safe_h128_four_target_check_scientific_bodies_DRAFT_run001.txt`, `..._saved_profile_identity_DRAFT_run001.txt` | S (+ C for identity) | Changes `interface_witness` and `compose` only. compose: gates, then T1-T8, then rows MEAN/L1/L2 x {1,2,3,4,H}, then ROUTE. A failed gate gives the negative branch. |
| 6 | SOURCE DRAFT + author QA | `.context/prepare_E11_fixed_polar_safe_h128_four_target_check_SOURCE_METADATA_run001.py`, `.context/E11_fixed_polar_safe_h128_four_target_check_SOURCE_DRAFT_run001.py`, `_changed3_HEADER_DRAFT_run001.txt`, `_INPUT_ADAPTER_DRAFT_run001.json`, `_PREFLIGHT_DRAFT_run001.md`, `.context/E11_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_SOURCE_DRAFT_AUTHOR_QA_run001.json` | S | Foundation is the #43 SOURCE 87021468. Harness definitions are AST+text identical; `interface_witness`, `compose` and `main` change; gate False. Selected inputs: 4 profile JSONs, 2 manifests, 2 summaries, 2 reconciliations, 2 ROOT receipts (`ordinary_json`), the four-target ROOT review, the E07 ledger and schedule, and the #44 prospectus/peer/ROOT review. The executed #43 controller is `plaintext_AST_only` if selected. |
| 7 | ROOT publication of actual SOURCE | `.context/publish_E11_fixed_polar_safe_h128_four_target_check_ACTUAL_SOURCE_METADATA_run001.py`; `research/limitation_program_20261001/experiment_e11_b4x12_fixed_polar_safe_h128_four_target_check_v1.py`; `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_{PLAN,INPUT_ADAPTER,PREFLIGHT,AUTHOR_STATIC_QA,AUTHOR_AST_DELTA}_run001.*` | ROOT | Full plaintext read first. Only the gate and docstring differ from the DRAFT. READY and OUTPUT absent. |
| 8 | SCI launcher (inert) | `.context/ROOT_E11_fixed_polar_safe_h128_four_target_check_SCI_launcher_run001.py` | ROOT | `--ready-sha256` required. Pins the SOURCE SHA. Log `xb`, terminal `x`. |
| 9 | Disabled saved-verifier DRAFT | `.context/author_E11_fixed_polar_safe_h128_four_target_check_saved_checker_metadata_run001.py`, `.context/E11_fixed_polar_safe_h128_four_target_check_ROOT_saved_verifier_DRAFT_run001.py`, `_changed2_HEADER_DRAFT_run001.txt`, `.context/E11_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_DISABLED_SAVED_CHECKER_AUTHOR_METADATA_QA_run001.json` | C (not S) | Re-derives T1-T8 and all 15 row classifications per profile from saved limbs. Checks the None branch. Gate False, pins None. |
| 10 | Independent SOURCE static peer | `.context/review_E11_fixed_polar_safe_h128_four_target_check_CURRENT_SOURCE_METADATA_run001.py`, `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_INDEPENDENT_STATIC_PEER_run001.json` | P (not S, not C) | Static only, no function calls. |
| 11 | Release DRAFT + QA | `.context/author_ROOT_E11_fixed_polar_safe_h128_four_target_check_RELEASE_DRAFT_METADATA_run001.py`, `.context/ROOT_E11_fixed_polar_safe_h128_four_target_check_source_review_release_DRAFT_run001.py`, `_changed_MAIN_HEADER_DRAFT_run001.txt`, `.context/ROOT_E11_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_DISABLED_RELEASE_DRAFT_AUTHOR_QA_run001.json` | disclosed metadata author | `ROOT_RELEASE_EXECUTION_AUTHORIZED=False`. |
| 12 | ROOT release | `.context/ROOT_E11_fixed_polar_safe_h128_four_target_check_source_review_release_run001.py`, `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_ROOT_STATIC_REVIEW_run001.json`, `..._ROOT_READY_run001.json` | ROOT | Requires QA and peer pass. Only the release gate differs from the DRAFT. |
| 13 | SCI (sole execution) | 13-file output dir: 4 executed copies, `run_started`, `selected_premise_authority`, `fixed_polar_safe_h128_four_target_source_premise_witness.json`, `five_metadata_controls`, `{primary,independent}_fixed_polar_safe_h128_four_target_accuracy_check.json`, `same_profile_reconciliation`, `summary`, `manifest`. Also `.context/E11_B4x12_fixed_polar_safe_h128_four_target_check_actual_run001.log` and `..._ROOT_TERMINAL_OBSERVATION_run001.json` | ROOT | Requires the separate user SCI yes. Caps as above; five controls, positive first. |
| 14 | Final checker binding | `.context/E11_fixed_polar_safe_h128_four_target_check_ROOT_saved_verifier_run001.py`, `.context/E11_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_FINAL_SAVED_VERIFIER_BINDING_run001.json` | ROOT | Run under pinned CPython 3.12.4 (frontier_t0_env), not system 3.9 (#43 run001 precedent). Exit 0, sealed 13. Only the gate, LOG_SHA, MF_SHA and PINS assignments change. |
| 15 | Independent FIELD peer | `.context/review_E11_fixed_polar_safe_h128_four_target_check_FINAL_FIELD_METADATA_run001.py`, `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_SAVED_VERIFIER_INDEPENDENT_FIELD_PEER_run001.json` | P (not C, not S) | Does not run the checker. |
| 16 | ROOT saved verification | `.context/E11_B4X12_FIXED_POLAR_SAFE_H128_FOUR_TARGET_CHECK_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json` | ROOT | Requires the FIELD pass. Typed diagnostics only. `USER_REQUESTED_STOP_CHECKPOINT=true`, `beyond45_SCI_authorized=false`, `accuracy_policy_adopted=false`. |
| 17 | Reporter DRAFT | `.context/author_checkpoint44_reporting_DRAFT_metadata_run001.py`, `.context/ROOT_checkpoint_four_target_44_DRAFT_run001.py`, header, QA | R | SCOPES=[44]. Baseline: checkpoint run026 8d3de528, progress run038 6ee0aaa1, AUDIT43 d61f29aa, doc pins, HEAD and primitives re-pinned at authoring time. |
| 18 | Reporter enable + execution | `.context/ROOT_checkpoint_four_target_44_verified_run001.py`, binding. Updates `progress.json`, `STATUS.md`, `OVERNIGHT_PROGRESS_20261007.md`, `IMPLEMENTATION_PLAN.md`. New `docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_FOUR_TARGET_RESULTS_<date>.md`, checkpoint marker `CHECKPOINT_<date>_FOUR_TARGET.md`, `.context/OVERNIGHT_PROGRAM_PROGRESS_20261007_run039.json`, `.context/OVERNIGHT_CONTINUATION_CHECKPOINT_20261007_run027.json` | ROOT executes | Verified count 43 -> 44. The 110 categories are unchanged, E11 stays partial, and fixture, whole-limitation and accuracy credit stay 0. |
| 19 | Independent overall audit, then stop | `.context/review_VERIFIED44_stop_checkpoint_METADATA_run001.py`, `.context/OVERNIGHT_VERIFIED44_INDEPENDENT_PROGRESS_CURRENT_CAPTURE_run001.json`, `..._AUDIT_run001.json` | P (not R, not S/C) | Only scope 44 is appended; old records preserved. Stop. |

## Assumptions

- **A1.** The half-bias convention b = epsilon/2 and the four epsilons are
  exactly those saved in the four-target ROOT review. #44 neither re-derives
  nor justifies the 1/2 split.
- **A2.** The 11/2000 headroom is the E07 epsilon=1/100 ledger quantity and
  is meaningful only for that target.
- **A3.** "Bias" means the absolute difference of the native and ideal
  means under the #42 coupling. The #42 m and the #43 L1/L2 bound this
  quantity for the full payoff Y_N vs Y.
- **A4.** The saved profile files, manifests and ROOT receipts are unchanged
  since the SHA256 values above were read. The future prospectus must
  re-pin them with stat8.
- **A5.** Profiles are identical to displayed digits (per the #43
  disclosure). #44 nonetheless evaluates each independently.

## Non-claims

This draft, and #44 if run, claim none of the following:

- a measured or lower-bounded bias;
- price accuracy at any epsilon;
- an adopted accuracy or price policy;
- confidence or runtime;
- an estimator saving or schedule change;
- a moment or variance transfer;
- E07 ledger discharge;
- candidate G2;
- physical delivery;
- quantum advantage.

"Compatible at epsilon=1/10" is necessary-not-sufficient and conditional.
"Ruled out" applies to this fixed certificate route only. This draft is not
a preregistration, review, receipt or authorization.
