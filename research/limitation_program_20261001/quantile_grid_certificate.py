"""A conditional price-law certificate for a different ideal Gaussian grid.

This is an independent-scalar inverse-CDF midpoint law. It is not the accepted
paired Box-Muller source, and no reversible inverse-CDF implementation is claimed.
"""

from fractions import Fraction

from research.limitation_program_20261001.barrier_band_certificate import exact, pair


PROOF = {
    "coordinate_monotonicity": (
        "Fix every normal except one common or idiosyncratic increment. In the "
        "original equal-volatility GBM, increasing that increment increases "
        "every affected stock at subsequent monitoring dates, because its "
        "coefficient is nonnegative. Unaffected stocks and earlier dates are "
        "constant. Each monitored positive-weight basket and the arithmetic "
        "Asian average are therefore nondecreasing in that coordinate."
    ),
    "one_threshold": (
        "If an unaffected monitoring date already violates the barrier the "
        "payoff is identically zero. Otherwise the intersection of all strict "
        "survival half-lines is itself a half-line, possibly empty or full. "
        "Within it the discounted call payoff is nonnegative and nondecreasing; "
        "at its finite endpoint it drops to zero. Original strict survival "
        "and digital ties are respected."
    ),
    "total_variation": (
        "Survival at every contractual date bounds the date/asset average "
        "below H. Hence the discounted payoff is at most C=(H-K)exp(-rT)<40. "
        "Its coordinate variation is at most2C: at most C of monotone increase "
        "and at most C of knockout jump. Composition with the increasing "
        "normal quantile preserves this bound on the uniform coordinate."
    ),
    "midpoint_quadrature": (
        "For a bounded-variation f and cell width w, let m be the midpoint. "
        "The left-half integral of abs(f(u)-f(m)) is at most (w/2) times "
        "variation on the left half, and similarly for the right half. "
        "Thus abs(integral_cell f-w*f(m))<=w*variation_cell/2. Summing cells "
        "gives at most w*TV(f)/2, including midpoint jumps. Define u=0,1 "
        "by one-sided limits; endpoint values have measure zero."
    ),
    "product_telescope": (
        "Replace one independent continuous uniform coordinate at a time by "
        "the same midpoint grid. The variation bound is uniform in all fixed "
        "remaining coordinates, whether continuous or already discrete. "
        "Integrating each difference and applying triangle inequality gives "
        "price-law error <=number_of_normals*40/2^q discounted dollars."
    ),
    "transfer_boundary": (
        "The proof requires exact independent scalar normal quantiles and "
        "exact continuous GBM/path/payoff arithmetic. Rounded inverse-CDF, "
        "native exp/clipping, barrier predicates and coherent loading need "
        "separate certificates. It does not certify the existing paired "
        "Box-Muller graph or provide a compiled circuit/runtime advantage."
    ),
}


def law_bound(model, uniform_bits=32, headroom=Fraction(11, 2000)):
    if type(uniform_bits) is not int or not 1 <= uniform_bits <= 64:
        raise ValueError("Integer ideal-grid precision between1 and64 required")
    expected = {"B4x12": (4, 12), "B8x52": (8, 52)}
    if model.get("case") not in expected:
        raise ValueError("Original supported contract required")
    assets, dates = expected[model["case"]]
    if (model["assets"], model["dates"]) != (assets, dates):
        raise ValueError("Contract dimensions mismatch")
    if (
        model.get("equal_asset_volatility") is not True
        or model.get("basket") != "positive equal-weight arithmetic spot basket"
        or model.get("continuous_driver_law")
        != "independent common and idiosyncratic Brownian drivers"
        or model.get("digital_paired_outputs_claimed_independent_gaussian") is not False
    ):
        raise ValueError("Original monotonicity and independent-scalar law assumptions required")
    terms = {
        "barrier_dollars_exact": Fraction(140),
        "strike_dollars_exact": Fraction(100),
        "rate_exact": Fraction(3, 100),
        "maturity_years_exact": Fraction(1),
        "volatility_exact": Fraction(3, 10),
        "correlation_exact": Fraction(2, 5),
    }
    if any(exact(model[name]) != value for name, value in terms.items()):
        raise ValueError("Original GBM model mismatch")
    allowance = exact(headroom)
    if allowance <= 0:
        raise ValueError("Positive exact allowance required")
    dimension = (assets + 1) * dates
    bound = Fraction(dimension * 40, 1 << uniform_bits)
    return dict(
        case=model["case"],
        ideal_law="independent Phi_inverse((raw+1/2)/2^q) scalar normals",
        normal_coordinates=dimension,
        uniform_bits=uniform_bits,
        coordinate_total_variation_upper_dollars_exact=[80, 1],
        all_date_continuous_payoff_grid_law_error_upper_dollars_exact=pair(bound),
        headroom_exact=pair(allowance),
        ideal_grid_law_term_fits_headroom=bound <= allowance,
        continuous_ideal_grid_law_certificate=True,
        accepted_Box_Muller_law_certified=False,
        native_rounded_inverse_CDF_or_path_certified=False,
        coherent_loader_implemented=False,
        complete_original_price_certified=False,
        second_discount_applied=False,
        proof=PROOF,
    )
