# A2a: binding-cell bias certificate by splitting out the lower-clip event (R1)

22 October 2026. C03 row A2a (deterministic bias reserve) at the binding cell B8x52, ε = $0.001.
**Rigour: R1.** Two exact or outward paths agree. This is **not R2**: there was no preregistration, sealed run, saved
verifier, ROOT receipt or human peer review. AI-assisted.

## Result

| Case | Certified run002 bias (finite source to continuous price) | Clip-split bias (this record) | 0.55ε target | Meets |
|---|---:|---:|---:|---|
| **B8x52** | 1.2396e-3 | **≤ 6703058386012589 / 2^64 = 3.63374e-4** | 5.5e-4 | **yes**, with 1.87e-4 spare |
| B4x12 | 2.0506e-4 | ≤ 111365570979513 / 2^63 = 1.20743e-5 | 5.5e-4 | yes |

- **Eligibility.** The binding cell is now eligible at $0.001 on a certified deterministic bias, with the source
  unchanged. The 4.73e-4 that C03 recorded as modelled (the "lower the clamp by 3 binades" route) is replaced by
  3.634e-4 at R1.
- **What no longer needs doing for eligibility:**
  - the A02 bridge rerun with stock classes 30 → 33;
  - the A07/A13 interval re-proofs.

  The clamp literal, exponent classes and circuit are untouched.
- **Clip-event probability (B8x52):**
  - P_fin(C) ≤ 10^-29 (primary, Bernstein);
  - P_fin(C) ≤ 1.42e-67 (independent, Bennett);
  - 104 clipable sites: all 8 stocks at dates 40-52;
  - Bernstein exponent ≥ 72.27 at every site (73.18 at elapsed date 40 down to 72.268 at date 52; review A2A-R10).
- **B4x12.** No site can clip: every all-input native log lower bound is at or above the clamp. So the run002 leak term
  ell was pure slack there.

## Statement

Let Y_N be the native discounted payoff under the finite input law. Let Y be the continuous-GBM reference, so that the
run002 target is |E Y_N − E Y|. For each case:

    |E Y_N − E Y| <= H_price + zeta0 + 40 * min(1, P_fin(C) + Σ_j min(1, g0_j + A_j))

- **H_price** is the pinned primary hybrid price bound (unchanged; identity re-checked).
- **zeta0** is the run002 smooth-payoff chain with the leak max(β, ell) replaced by β = 2^-40.
- **g0_j** is the run002 Gaussian closed-band bound on the band [(140 − β)/b_j, (140 + β + 2^-40)/a_j].
- **A_j** is the unchanged whole-pair law allowance.
- **C** is the event that some native stock site takes its lower clamp.

## Proof

1. **Pointwise split.** Under the hybrid law H, both payoffs lie in [0, 40] (run002 smooth-payoff record,
   `fixed_both_payoffs_safe_cap`). Hence

       |Y_N − Y_I| <= 40·1_C + zeta0·1_{C^c, no switch} + 40·1_{C^c, switch}.

   H is the native radius R̂ at midpoint quantile atoms with the ideal midpoint angle. It is a function of the same
   raw uniforms, so E_H Y_N = E_fin Y_N. Taking expectations, adding H_price (the bound on |E Y − E_H Y_I|) and using
   zeta0 ≤ 40 gives the statement once steps 2-4 hold.
2. **On C^c the leak is β.**
   - The run002 stock envelope (`stock_exponential_envelopes.json`) gives, for an unclipped site,
     S_N ≤ (1 + α)·e^{x_N} + β. With |x_N − x_I| ≤ λ_j (`raw_log_prefix_envelopes.json`), this gives
     S_N ≤ b_j S_I + β. Here b_j = (1 + α)e^{λ_j}.
   - The run002 leak ell = (1 + α)e^{L} + β is the same envelope evaluated at the clamp, and is used only because a
     clipped site's native value is native exp(L).
   - The basket coefficient is exact (1/na). So on C^c, B_N ≤ b_j B_H + β, and the lower side is unchanged.
   - Opposite strict barrier decisions therefore force B_H into the closed band band0_j. The mean-stock error on
     both-survivor paths becomes 140·max(1 − a_j, b_j − 1) + β. Those are exactly the run002 derivations
     (`bridge_method_obligations` → `clipping_and_band`, `survival_and_smooth`) with ell → β.
3. **Band probability.** P_H(B_H ∈ band0_j) ≤ g0_j + A_j.
   - The run002 continuous anti-concentration and whole-pair transport lemmas apply to any closed band with these
     endpoint forms. Their TV ≤ 4 argument is endpoint-generic. The band is positive and ordered; this follows from run002's guard a_j ≤ 1 ≤ b_j (`experiment_box_muller_native_financial_bridge_v2.py:2889`) and β = 2^-40, and is not asserted separately by the scripts (review A2A-R04).
   - Primary path: log(U/L) ≤ U/L − 1, and sqrt(2π var) uses a Machin π lower bound.
   - Independent path: an exact log in decimal intervals.
   - Self-check: with ell restored, the primary path reproduces every run002 g_j outward (g_cert ≤ g ≤ g_cert(1 + 1e-5)).
     It also reproduces zeta exactly, and the run002 total identity exactly.
4. **P_fin(C).**
   - C ⊆ ∪ over clipable sites (i, j) of {x_I,ij ≤ L + λ_j}. A site is clipable when its all-input native raw log
     lower bound is below the clamp raw value −12193974156573.
   - x_I,ij = log 100 + jμ + Σ_k Y_k, with μ = −3/(200·nt) and Y_k = R̂_k(a_k cos θ_k + b_k sin θ_k) over the whole
     source pairs k.
   - The coefficients are the exact √(9/(250nt)) (common) and √(27/(500nt)) (own idiosyncratic), or 0.
   - Under H the pairs are independent, and within a pair R̂ (from u1) is independent of θ (from u2).
   - θ is uniform on N = 2^32 equispaced midpoints (the +3/4-wrapped grid is a permutation). Since Σ_k e^{imθ_k} = 0
     unless N | m:
     - E Y_k = 0;
     - E Y_k² = E[R̂²]·(a_k² + b_k²)/2 exactly;
     - |Y_k| ≤ B·√2·max(a, b), with B = 6.7637 the pinned all-input internal radius bound.
   - So V_j = (E[R̂²]/2)·j·9/(100nt).
   - Second moment:
     - primary: E[R̂²] ≤ 2 + D_S·B², from the KS distance D_S = 1.296e-10 on [0, B²];
     - independent: E[R̂²] ≤ 2 + η, from |R̂_k² − S_k| ≤ η = 2.64e-11 and the midpoint rule for convex −2 ln u.
   - Tail: one-sided Bernstein (primary) or Bennett (independent) with s_j = log 100 + jμ − L − λ_j ≈ 15.68, plus a
     union bound over the clipable sites.

## Numbers (B8x52)

| Term | run002 | Clip split |
|---|---:|---:|
| H_price | 1.16799e-4 | 1.16799e-4 (unchanged) |
| zeta | 1.48531e-5 | 4.53233e-8 |
| P_H(any switch) | 2.76976e-5 | 6.16322e-6 |
| P_fin(C) | (inside the band) | ≤ 1e-29 |
| **Total** | **1.23956e-3** | **3.63374e-4** |

The desk "ideal_clip_split_ell_to_lsb" value (3.63374e-4, modelled) is reproduced. The 3.4e-16 difference comes from
outward rounding.

## Files

All runs used `../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B` from the worktree root. The isolated
3.12.4 env lives in the main repository root, not in the worktree.

| File | sha256 |
|---|---|
| `research/claim_debts_20261022/a2a/clip_split_certificate.py` (primary) | 0e31d0c9fc79b6f71ab29ef1813c3076dcddf3107f9c16ca9759a6658ac62a7f |
| `research/claim_debts_20261022/a2a/independent_recompute.py` | c34cccfcb9043fdb781a8f26735620a45315ad03e9cbb99533d75203eb8e2bb6 |
| `research/claim_debts_20261022/a2a/summarize.py` | 7204d9aff2c1eee50d410dc9a3bb6ac3f1afaef2b64129efc610e8e95a937ed8 |
| `results/claim_debts_20261022/a2a/run001/certificate.json` | 75c682324a539021c0231cdbd5e1e61dc4b6a7c4d9cb77b18f23ab6d6429585d |
| `results/claim_debts_20261022/a2a/run001/independent.json` | 4a05126d89cf6ddee3972f51309c623f36e0af8b911f431e5406fd2403220a63 |
| `results/claim_debts_20261022/a2a/run001/summary.json` | all_checks_pass = true; paths agree to a relative 9.4e-13 |

Readers of certificate.json need `sys.set_int_max_str_digits(0)`, because some exact rationals have more than 4,300
digits.

## Premises (read only; cited by sha256)

| Premise | sha256 |
|---|---|
| `results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/closed_barrier_bands.json` | f8d5d6f3e2dcd58be9300cc1324eac959b3aec4666ad358d48f95a049bc80281 |
| `.../A02_BM_native_financial_bridge_run002/smooth_payoff_bounds.json` | c31be96d9e4980a40ab1037466bf43698f8a55567225b0a86db320b3ac0ebb62 |
| `.../A02_BM_native_financial_bridge_run002/complete_financial_bounds.json` | 1ed44ea428e5bdc92d83cab57f51ea0d102f680344335fafb95ff5cdc01e350f |
| `.../A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json` | 525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a |
| `.../A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json` | 4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373 |
| `.../A02_BM_native_financial_bridge_run002/summary.json` | 66a0843d3739f1963a868483b278bb6aefd0358e16156b178e6862b9594f6f5d |
| `results/limitation_program_20261001/A02_polar_cdf_bv_run003/log_radius_envelope.json` | 93dd1dac2698e869bc31c537b25a8fcc6f058987c314c8d1a4667feae0ccae84 |
| `.../A02_polar_cdf_bv_run003/ideal_hybrid_bounds.json` | 965017f89fd79abf4264abf66d11ab5df9d6ad7448f9513c9182801ee7529890 |

The derivation steps cited are in `research/limitation_program_20261001/experiment_box_muller_native_financial_bridge_v2.py`
(`closed_barrier_bands`, `smooth_payoff_bounds`, `stock_exponential_envelopes`, `raw_log_prefix_envelopes`,
`bridge_method_obligations`). The run002 bridge has its own independent audit (`A02_BM_native_financial_bridge_audit_run002`)
and is composed into `E07_original_BM_G2_composition_run001/B8x52_G2_composed_ledger.json`.

## Notes for the C03 owner

- **A2b (loader law) is inside A2a.** The run002 bridge's pay-once term covers `finite_input_law_and_joint_Box_Muller`,
  `clipped_log_tail` and `native_arithmetic_and_polynomial` (G2 composed ledger, `covers`). So no separate Box-Muller
  law row is needed.
- **Bias reserve.** 0.55ε = 5.5e-4, certified bias 3.634e-4 (R1), spare 1.866e-4. A2c (the U2 readout placeholder,
  2^-39) fits inside the spare.
- **No failure probability.** The bridge is a deterministic expectation bound. The clip event enters as a dollar
  term, not as a failure probability.

## Caveats and what R2 would need

- **Premise reuse.** The certificate inherits every run002 premise unchanged: stock, prefix and radius envelopes, the
  band transport lemma and the hybrid-law structure. It adds three facts used in the proof but not stated as a
  run002 output:
  - radius-angle independence inside a pair (distinct raw uniforms);
  - independence across whole pairs;
  - the exact moments of the midpoint angle grid.

  The first two are the whole-pair structure the run002 transport already uses (`hybrid_order`, `whole_pair_transport`).
- **Native clamp comparison.** The clamp test is taken as "native raw log < clamp raw". The union uses ≤ on the ideal
  side, which is a superset.
- **Remaining for R2:**
  - a preregistered prospectus;
  - an independent (human) peer review of steps 2 and 4;
  - a ROOT_READY / sealed run with saved verifier and receipt, under the limitation-program lifecycle;
  - recomposition of the E07 G2 ledger at ε = 1/1000 with this term.

  None was done here. No limitation-program file was edited.

## Review

An independent AI adversarial review (`results/claim_debts_20261022/review/a2a_review_summary.md`, 12 findings) found the certificate **sound with minor fixes and no major findings**. It reproduced both runs exactly. Both minor findings (A2A-R04, A2A-R10) are corrected above. There has still been no human review.
