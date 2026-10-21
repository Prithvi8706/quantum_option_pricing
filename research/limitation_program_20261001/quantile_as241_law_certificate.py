"""Transfer an all-input AS241 quantile error into an ideal GBM price-law bound.

The deterministic signed-restored AS241 law differs from the accepted paired
Box-Muller source. Financial arithmetic remains exact continuous GBM here.
"""

from fractions import Fraction


UNIFORM_BITS = 32
FRACTION_BITS = 40
NATIVE_WIDTH = 72
TARGET = Fraction(1, 100000000)
ALLOWANCE = Fraction(1, 1000)
DENSITY_UPPER = Fraction(2, 5)
VARIATION_DOLLARS = Fraction(80)
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
TERMS = {
    "spot_dollars_exact": Fraction(100),
    "volatility_exact": Fraction(3, 10),
    "correlation_exact": Fraction(2, 5),
    "rate_exact": Fraction(3, 100),
    "maturity_years_exact": Fraction(1),
    "strike_dollars_exact": Fraction(100),
    "barrier_dollars_exact": Fraction(140),
}
PROOF = {
    "pointwise_cdf_sandwich": (
        "Let U be uniform on the q32 midpoints, X=Phi_inverse(U), and Z be the "
        "deterministic signed-restored AS241 result at the same input. If "
        "|Z-X|<=E at EVERY input, then {X<=x-E} subset {Z<=x} subset {X<=x+E}. "
        "Thus Fgrid(x-E)<=Fnew(x)<=Fgrid(x+E). This argument does not require "
        "the new outputs to be monotone in their input or distinct."
    ),
    "midpoint_grid_cdf": (
        "With N=2^32, Fgrid(x) counts midpoints (k+1/2)/N<=Phi(x), divided "
        "by N. The nearest-grid counting error is at most1/(2N), including "
        "a threshold exactly equal to a midpoint. Left CDF limits obey the "
        "same bound because Phi is continuous. No previous rounded-floor "
        "quantile law or its1ulp error is added."
    ),
    "gaussian_density": (
        "Machin's identity and the alternating atan series give "
        "pi>16*(1/5-1/(3*5^3))-4/239>25/8. Hence "
        "phi(x)<=1/sqrt(2*pi)<2/5. Integrating over an interval of length E "
        "bounds |Phi(x+E)-Phi(x)| by(2/5)E for every real x."
    ),
    "kolmogorov_bound": (
        "Combining the sandwich, midpoint counting and density bound gives "
        "sup_x |Fnew(x)-Phi(x)|<=2^-33+(2/5)E. Atoms and equal outputs are "
        "permitted. The comparison law is the continuous scalar Gaussian."
    ),
    "coordinate_variation": (
        "In the ORIGINAL equal-volatility GBM, one common or idiosyncratic "
        "normal increment has positive coefficients in every affected later "
        "stock. Each positive-weight basket and Asian average is nondecreasing. "
        "Fixing all other coordinates, strict barrier survival is a lower "
        "half-line, empty, or full. The discounted positive Asian payoff "
        "increases on survival and drops to zero at its finite endpoint. "
        "Survival gives the date/asset average<140, so discounted payoff<40 "
        "and its coordinate total variation<=80. This remains true with the "
        "other coordinates held at arbitrary finite discrete values."
    ),
    "cdf_to_bounded_variation": (
        "For the right-continuous strict-knockout coordinate payoff f, its "
        "signed Stieltjes variation measure has total mass<=TV(f). A "
        "half-line indicator's expectation differs by at most KS. Closed "
        "upper half-lines [x,infinity) use1-F(x-); closed lower half-lines "
        "useF(x), so discrete ties are retained. Integrating "
        "the indicator representation gives |Enew[f]-Egaussian[f]|<=TV*KS. "
        "Left CDF differences are also bounded by KS since Phi is continuous. "
        "One-sided finite limits exist and constants cancel between laws."
    ),
    "independent_product": (
        "Use independent q32 raw words for the NEW scalar AS241 law. Replace "
        "one of d=(assets+1)*dates independent Gaussian coordinates at a time. "
        "The uniform coordinate variation bound survives every mixture of "
        "continuous and discrete remaining coordinates. Bounded payoff "
        "permits iterated integration, and triangle inequality gives "
        "ideal-GBM price-law bias<=80*d*(2^-33+(2/5)E) discounted dollars."
    ),
    "scope": (
        "E uses the successful NEW central arithmetic and ordinary-tail "
        "native log/sqrt/input-sensitivity certificate. The mathematical "
        "all-input law includes those scalar arithmetic errors once. No "
        "native financial exp/clipping/path/barrier error, coherent divider "
        "or loader, gate cost, full-price accuracy or quantum advantage is "
        "certified. The accepted paired Box-Muller source is unchanged."
    ),
}


def exact(value):
    if isinstance(value, (list, tuple)):
        if len(value) != 2 or any(type(item) is not int for item in value) or value[1] <= 0:
            raise ValueError("Exact rational pair required")
        return Fraction(*value)
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    raise ValueError("Exact rational value required")


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def gaussian_density_proof():
    pi_lower = 16 * (Fraction(1, 5) - Fraction(1, 3 * 5**3)) - Fraction(4, 239)
    if not pi_lower > Fraction(25, 8):
        raise ArithmeticError("Fixed exact Machin density bound failed")
    return {
        "Machin_alternating_lower_bound_exact": pair(pi_lower),
        "pi_strict_lower_guard_exact": [25, 8],
        "Gaussian_density_strict_upper_exact": [2, 5],
        "numerical_Gaussian_evaluations": 0,
    }


def validate_model(model):
    if model.get("case") not in CASES:
        raise ValueError("Original supported contract required")
    if (model.get("assets"), model.get("dates")) != CASES[model["case"]]:
        raise ValueError("Original contract dimensions changed")
    if any(exact(model[name]) != value for name, value in TERMS.items()):
        raise ValueError("Original economic parameters changed")
    if (
        model.get("equal_asset_volatility") is not True
        or model.get("basket") != "positive equal-weight arithmetic spot basket"
        or model.get("continuous_driver_law")
        != "independent common and idiosyncratic Brownian drivers"
        or model.get("digital_paired_outputs_claimed_independent_gaussian") is not False
    ):
        raise ValueError("Original ideal GBM monotonicity/independence assumptions required")
    return (model["assets"] + 1) * model["dates"]


def validate_native_error(certificate, fresh):
    """Reconcile all saved transform classes and fresh-tail arithmetic rows."""
    if certificate.get("certified") is not True or certificate.get("budget_censored") is not False:
        raise ValueError("Successful uncensored all-input native transform proof required")
    true_flags = (
        "actual_q32_native_transform_error_included",
        "exact_transform_hypothesis_replaced_by_mathematical_native_arithmetic",
    )
    false_flags = (
        "native_financial_path_arithmetic_certified",
        "coherent_loader_implemented_or_adopted",
        "accepted_Box_Muller_baseline_changed",
        "full_G2_closed",
    )
    if any(certificate.get(name) is not True for name in true_flags) or any(
        certificate.get(name) is not False for name in false_flags
    ):
        raise ValueError("Native scalar-law and financial implementation scopes differ")
    if certificate.get("actual_coherent_leaf_or_quantum_gate_cost") is not None:
        raise ValueError("Quantum implementation cost must remain open")
    transform = certificate["transform"]
    normalization = transform["normalization"]
    if (
        normalization.get("all_q32_tail_words_covered") is not True
        or normalization.get("enumerated_q32_words_as_completeness_proof") != 0
        or transform.get("continuous_uniform_midpoint_coupling_error_included") is not False
        or transform.get("radial_cutoff_or_bad_event_used") is not False
    ):
        raise ValueError("All-input same-midpoint proof without Box-Muller coupling required")
    cover = transform["cell_exponent_cover"]
    wanted = {(cell, exponent) for cell in range(32) for exponent in range(-33, -3)}
    actual = [(row["table_cell"], row["exponent"]) for row in cover]
    if len(actual) != 960 or len(set(actual)) != 960 or set(actual) != wanted:
        raise ValueError("Exact32-cell/30-exponent native log cover required")
    rows = fresh["rows"]
    if (
        fresh.get("fixed_rows") != 1024
        or fresh.get("completed_rows") != 1024
        or len(rows) != 1024
        or [row["cell_index"] for row in rows] != list(range(1024))
    ):
        raise ValueError("Complete original1024-cell fresh sensitivity ledger required")
    rho = exact(transform["native_transform_error_upper_exact"])
    if rho < 0:
        raise ValueError("Nonnegative all-input transform error required")
    totals = []
    for row in rows:
        real = exact(row["saved_real_approximation_error_upper_exact"])
        arithmetic = exact(row["fresh_native_rational_error_upper_exact"])
        total = exact(row["actual_native_tail_quantile_error_upper_exact"])
        if (
            min(real, arithmetic) < 0
            or total != real + arithmetic
            or exact(row["argument_perturbation_upper_exact"]) != rho
            or row.get("previous_conditional_floor_arithmetic_error_added") is not False
            or row.get("actual_sqrt_floor_and_shift_error_only_in_rho") is not True
        ):
            raise ValueError("Fresh input sensitivity must replace prior hypothetical-floor error")
        totals.append(total)
    tail = exact(certificate["actual_native_tail_quantile_error_upper_exact"])
    central = exact(certificate["central_quantile_error_upper_exact"])
    combined = exact(certificate["combined_mathematical_native_quantile_error_upper_exact"])
    if min(tail, central) < 0 or tail != max(totals) or combined != max(tail, central):
        raise ValueError("Exact all-input quantile maximum does not reconcile")
    if exact(certificate["required_uniform_quantile_error_exact"]) != TARGET or combined > TARGET:
        raise ValueError("Frozen1e-8 all-input quantile target required")
    return combined


def law_bound(model, quantile_error):
    """Conditional theorem; the producer binds its premise to the native receipt."""
    dimension = validate_model(model)
    error = exact(quantile_error)
    if not 0 <= error <= TARGET:
        raise ValueError("Successful nonnegative1e-8 quantile premise required")
    midpoint = Fraction(1, 1 << (UNIFORM_BITS + 1))
    displacement = DENSITY_UPPER * error
    ks = midpoint + displacement
    dollars = VARIATION_DOLLARS * dimension * ks
    return {
        "case": model["case"],
        "new_law": "independent q32 midpoint inputs, mathematical-native signed-restored AS241",
        "uniform_bits": UNIFORM_BITS,
        "fraction_bits": FRACTION_BITS,
        "native_width": NATIVE_WIDTH,
        "normal_coordinates": dimension,
        "uniform_quantile_error_upper_exact": pair(error),
        "new_law_monotonicity_required": False,
        "grid_KS_error_upper_exact": pair(midpoint),
        "quantile_displacement_KS_error_upper_exact": pair(displacement),
        "scalar_Gaussian_KS_error_upper_exact": pair(ks),
        "coordinate_total_variation_upper_dollars_exact": pair(VARIATION_DOLLARS),
        "ideal_GBM_new_law_price_bias_upper_dollars_exact": pair(dollars),
        "separate_exploratory_law_allowance_dollars_exact": pair(ALLOWANCE),
        "new_law_bias_fits_separate_exploratory_allowance": dollars <= ALLOWANCE,
        "Gaussian_density_proof": gaussian_density_proof(),
        "previous_exact_floor_quantile_law_ULP_added": False,
        "quantile_native_scalar_arithmetic_already_in_E": True,
        "independent_raw_uniform_coordinates_required": True,
        "original_continuous_ideal_GBM_payoff_used": True,
        "accepted_Box_Muller_law_certified": False,
        "accepted_Box_Muller_baseline_changed": False,
        "native_financial_exp_clipping_or_path_certified": False,
        "coherent_divider_or_loader_adopted": False,
        "actual_quantum_gate_cost": None,
        "native_financial_price_error_bound": None,
        "complete_original_price_certified": False,
        "full_G2_closed": False,
        "quantum_advantage_established": False,
        "second_discount_applied": False,
        "proof": PROOF,
    }
