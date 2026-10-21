# Fixed polar-safe payoff squared-L2 bridge

Scope43 composes saved #42 own-profile fields only; lambda=2^-18 and h=1/128 stay fixed by #42 and nothing is retuned. Y_N is the native full payoff node and Y the ideal discounted strict-140 survival payoff under the #42 coupling. For each own profile separately (no cross-profile minimum) the saved identities E_s=U*avg+40*eta+tau, p=min(1,60*lambda+B_band) and mean=E_s+40*p are re-derived exactly and the jump constant is C_J=40*(U+eta)+tau. Only when all seven exact checks R1-R7 pass does the profile record E[(Y_N-Y)^2]<=L2SQ=E_s^2+(C_J^2-E_s^2)*p, the cross-check E_s^2+1600*p, E|Y_N-Y|<=E_s*(1-p)+C_J*p and an outward sqrt128 RMS. L2SQ is the exact maximum of the LP relaxation over the disjoint event split, not the sharpest bound for this coupling. A failed inherited criterion or check seals a negative fixed-bridge feasibility record with all four fields None and no fallback.

Per own profile (fixed outward 1e-9 displays copied verbatim as typed strings from the ROOT reporting metadata; reporting only, not certificate operands, not recalculated here):

- `primary90`: outcome `conditional_payoff_squared_L2_certificate`; E[(Y_N-Y)^2] <= 1.626207727 USD^2, RMS <= 1.275228500 USD, E|Y_N-Y| <= 0.045202052 USD.
- `independent130`: outcome `conditional_payoff_squared_L2_certificate`; E[(Y_N-Y)^2] <= 1.626207727 USD^2, RMS <= 1.275228500 USD, E|Y_N-Y| <= 0.045202052 USD.

Saved ROOT reporting facts (profiles remain separate):

```json
[
  {
    "ROOT_pointer": [
      "profile_bridge_results"
    ],
    "typed_saved_value": [
      {
        "LP_relaxation_exact_maximum_not_sharpest_bound": true,
        "accuracy_policy_adopted": false,
        "actual_bias_lower_bound_estimator_G2_physical_or_advantage": false,
        "all_rational_checks_passed": true,
        "conditional_payoff_L1_bound_reference": {
          "JSON_pointer": "/payoff_L1_upper",
          "profile": "primary90"
        },
        "conditional_payoff_RMS_bound_reference": {
          "JSON_pointer": "/payoff_RMS_sqrt128_upper",
          "profile": "primary90"
        },
        "conditional_payoff_squared_L2_bound_reference": {
          "JSON_pointer": "/payoff_squared_L2_upper_L2SQ",
          "profile": "primary90"
        },
        "displays_reporting_only_not_certificate_operands": true,
        "estimator_saving_claimed": false,
        "fixed_outward_1e_9_reporting_displays": {
          "L1": {
            "display_unit": "1e-9 USD",
            "outward_display_units": 45202052,
            "readable_decimal_upper": "0.045202052"
          },
          "L2SQ": {
            "display_unit": "1e-9 USD^2",
            "outward_display_units": 1626207727,
            "readable_decimal_upper": "1.626207727"
          },
          "RMS": {
            "display_unit": "1e-9 USD",
            "outward_display_units": 1275228500,
            "readable_decimal_upper": "1.275228500"
          }
        },
        "inherited42_all12_fixed_basket_criterion_passed": true,
        "inherited42_all12_simultaneous_on_same_fixed_safe_event": true,
        "moment_or_variance_transfer_claimed": false,
        "negative_bridge_is_feasibility_not_accuracy_success": true,
        "no_adaptive_lambda_h_fallback_or_cross_profile_minimum": true,
        "outcome": "conditional_payoff_squared_L2_certificate",
        "payoff_squared_L2_certificate_adopted": true,
        "profile": "primary90",
        "rational_checks": {
          "R1": true,
          "R2": true,
          "R3": true,
          "R4": true,
          "R5": true,
          "R6": true,
          "R7": true
        },
        "saved42_operands_C_J_R1_R7_L2SQ_BASE_L1_and_sqrt128_rederived_exactly": true
      },
      {
        "LP_relaxation_exact_maximum_not_sharpest_bound": true,
        "accuracy_policy_adopted": false,
        "actual_bias_lower_bound_estimator_G2_physical_or_advantage": false,
        "all_rational_checks_passed": true,
        "conditional_payoff_L1_bound_reference": {
          "JSON_pointer": "/payoff_L1_upper",
          "profile": "independent130"
        },
        "conditional_payoff_RMS_bound_reference": {
          "JSON_pointer": "/payoff_RMS_sqrt128_upper",
          "profile": "independent130"
        },
        "conditional_payoff_squared_L2_bound_reference": {
          "JSON_pointer": "/payoff_squared_L2_upper_L2SQ",
          "profile": "independent130"
        },
        "displays_reporting_only_not_certificate_operands": true,
        "estimator_saving_claimed": false,
        "fixed_outward_1e_9_reporting_displays": {
          "L1": {
            "display_unit": "1e-9 USD",
            "outward_display_units": 45202052,
            "readable_decimal_upper": "0.045202052"
          },
          "L2SQ": {
            "display_unit": "1e-9 USD^2",
            "outward_display_units": 1626207727,
            "readable_decimal_upper": "1.626207727"
          },
          "RMS": {
            "display_unit": "1e-9 USD",
            "outward_display_units": 1275228500,
            "readable_decimal_upper": "1.275228500"
          }
        },
        "inherited42_all12_fixed_basket_criterion_passed": true,
        "inherited42_all12_simultaneous_on_same_fixed_safe_event": true,
        "moment_or_variance_transfer_claimed": false,
        "negative_bridge_is_feasibility_not_accuracy_success": true,
        "no_adaptive_lambda_h_fallback_or_cross_profile_minimum": true,
        "outcome": "conditional_payoff_squared_L2_certificate",
        "payoff_squared_L2_certificate_adopted": true,
        "profile": "independent130",
        "rational_checks": {
          "R1": true,
          "R2": true,
          "R3": true,
          "R4": true,
          "R5": true,
          "R6": true,
          "R7": true
        },
        "saved42_operands_C_J_R1_R7_L2SQ_BASE_L1_and_sqrt128_rederived_exactly": true
      }
    ]
  }
]
```

Non-claims: these are upper certificates on the native-versus-ideal payoff coupling. They are not a measured bias, price accuracy, an adopted price policy, a moment or variance transfer (no certified continuous B4x12 second moment exists), an estimator saving, confidence or runtime, candidate G2, physical delivery or quantum advantage. One saved-checked bounded component scope is recorded; fixture, whole-limitation and accuracy credit stay 0 and E11 stays partial.

Expected outcome, stated in the prospectus before the run: estimator work is unchanged, because the saved B4 schedule E07 is bounded amplitude estimation and never reads a moment; E11 stays partial and no accuracy policy is adopted.

Checker binding disclosure: ROOT first ran the final-checker binding helper under system CPython 3.9.13 by mistake ([binding run001](../../.context/E11_FIXED_POLAR_SAFE_H128_PAYOFF_L2_FINAL_SAVED_VERIFIER_BINDING_run001.json), 95 code-location pairs, a 3.9 artifact). The superseding [binding run002](../../.context/E11_FIXED_POLAR_SAFE_H128_PAYOFF_L2_FINAL_SAVED_VERIFIER_BINDING_run002.json) under the pinned CPython 3.12.4 records 60 pairs with the checker bytes, the four bound assignments and the eight authority pins unchanged. Both are preserved. The report author agent43_C also authored the scope43 saved checker; this page is not independent approval.

Evidence: [ROOT receipt](../../.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json), [manifest](../../results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/manifest.json), [stop checkpoint](CHECKPOINT_20261009_PAYOFF_L2.md). ROOT SHA256 `87d7dec30d03f326e13a16b8a2ebfea464c1e797a753986e0d2db3d10bd06ce7`.
