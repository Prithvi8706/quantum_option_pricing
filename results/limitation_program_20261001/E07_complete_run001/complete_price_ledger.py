"""Exact rational error obligations for one monitored B4 price.

Unknown bounds remain unknown. A certificate for the digital mean cannot
certify the original continuous financial expectation by itself.
"""

from __future__ import annotations

from fractions import Fraction


def rational(value):
    if value is None:
        return None
    if isinstance(value, float) or isinstance(value, bool):
        raise ValueError("use exact rational values, never binary floating budgets")
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            raise ValueError("rational numerator/denominator required")
        value = Fraction(*value)
    else:
        value = Fraction(value)
    if value < 0:
        raise ValueError("error and failure bounds cannot be negative")
    return value


def encoded(value):
    value = rational(value)
    return None if value is None else [value.numerator, value.denominator]


def assess(ledger):
    """Check sums exactly and require a certificate for every nonreserved term."""
    epsilon, alpha = rational(ledger["epsilon_dollars"]), rational(ledger["failure_cap"])
    if epsilon is None or epsilon <= 0 or alpha is None or not 0 < alpha < 1:
        raise ValueError("positive price tolerance and probability cap required")
    terms = ledger["dollar_terms"]
    failures = ledger["failure_terms"]
    if len({x["name"] for x in terms}) != len(terms) or len({x["name"] for x in failures}) != len(
        failures
    ):
        raise ValueError("duplicate error obligation")
    for term in terms + failures:
        if rational(term["bound"]) is not None and not term.get("certificate"):
            raise ValueError("a numerical bound needs its own certificate")
    dollar_sum = sum((rational(x["bound"]) or Fraction(0) for x in terms), Fraction(0))
    failure_sum = sum((rational(x["bound"]) or Fraction(0) for x in failures), Fraction(0))
    allowances = [rational(x["allowance"]) for x in failures]
    if any(x is None for x in allowances):
        raise ValueError("failure allowances must be explicit")
    allocated = sum(allowances, Fraction(0))
    if allocated > alpha:
        raise ValueError("joint failure allocation exceeds the complete-price cap")
    for term, allowance in zip(failures, allowances, strict=True):
        bound = rational(term["bound"])
        if bound is not None and bound > allowance:
            raise ValueError("certificate exceeds its own failure allowance")
    missing = [x["name"] for x in terms + failures if x["bound"] is None]
    complete = not missing and dollar_sum <= epsilon and failure_sum <= alpha
    return dict(
        complete_price_certified=complete,
        open_obligations=missing,
        known_dollar_bound_sum=encoded(dollar_sum),
        known_failure_bound_sum=encoded(failure_sum),
        allocated_failure_sum=encoded(allocated),
        remaining_dollar_headroom=encoded(epsilon - dollar_sum) if dollar_sum <= epsilon else None,
        known_bounds_fit=dollar_sum <= epsilon and failure_sum <= alpha,
        missing_bounds_are_zero=False,
    )


def adaptive_failure_allocation(stages, total):
    """Validate a declared finite controller with exact stage failure bounds."""
    total = rational(total)
    if total is None or not 0 < total < 1 or not stages:
        raise ValueError("finite stages and a probability budget required")
    if len({row["name"] for row in stages}) != len(stages):
        raise ValueError("duplicate adaptive stage")
    values = [rational(row["failure_upper"]) for row in stages]
    if any(value is None for value in values):
        raise ValueError("every adaptive stage needs a confidence certificate")
    if sum(values, Fraction(0)) > total:
        raise ValueError("adaptive stage failures exceed their shared budget")
    return encoded(sum(values, Fraction(0)))


def make_b4_ledger(estimator, source_binding, support_binding, epsilon=Fraction(1, 100)):
    """Attach a bounded digital schedule without inventing financial biases."""
    epsilon = rational(epsilon)
    statistical = Fraction(9, 20) * epsilon
    if rational(estimator["statistical_error_dollars_exact"]) != statistical:
        raise ValueError("estimator does not match the selected dollar allowance")
    failure = rational(estimator["ideal_failure_upper_exact"])
    if failure is None or failure > Fraction(3, 1000):
        raise ValueError("estimator lacks its exact finite confidence bound")
    certificate = estimator["certificate"]
    exact_contract = source_binding["fixed_contract_certificate"]
    zero = [0, 1]
    dollar_terms = [
        dict(
            name="finite_input_law_and_joint_Box_Muller",
            bound=None,
            certificate=None,
            prerequisite="C06: joint finite-pair coupling",
        ),
        dict(
            name="clipped_log_tail",
            bound=None,
            certificate=None,
            prerequisite="C06: tail and clipping dollar bridge",
        ),
        dict(
            name="native_arithmetic_and_polynomial",
            bound=None,
            certificate=None,
            prerequisite="C06/C07: path enclosure and barrier boundary band",
        ),
        dict(
            name="monitoring_policy",
            bound=zero,
            certificate=exact_contract,
            reason="The contract fixes monitoring dates; no policy approximation was introduced",
        ),
        dict(
            name="surrogate",
            bound=zero,
            certificate=exact_contract,
            reason="The source evaluates the original digitized payoff",
        ),
        dict(
            name="random_preparation",
            bound=zero,
            certificate=exact_contract,
            reason="Exact Hadamards prepare the original finite product input law",
        ),
        dict(name="statistical_digital_mean", bound=encoded(statistical), certificate=certificate),
    ]
    failure_terms = [
        dict(
            name="ideal_estimator",
            allowance=[3, 1000],
            bound=encoded(failure),
            certificate=certificate,
        ),
        dict(
            name="QPE_rotation_synthesis",
            allowance=[1, 1000],
            bound=None,
            certificate=None,
            prerequisite="Emit synthesized IQFT rotations with whole-circuit error bound",
        ),
        dict(
            name="physical_execution",
            allowance=[3, 1000],
            bound=None,
            certificate=None,
            prerequisite="H17/H18: complete execution failure allocation",
        ),
        dict(
            name="certificate_acquisition",
            allowance=[3, 1000],
            bound=zero,
            certificate=support_binding["certificate"],
            reason=(
                "This moment-free estimator uses deterministic all-input support "
                "and no statistical certificate acquisition"
            ),
        ),
    ]
    ledger = dict(
        schema="rational-complete-price-obligations-v1",
        task="B4x12 original monitored arithmetic-basket knock-out call",
        epsilon_dollars=encoded(epsilon),
        failure_cap=[1, 100],
        source=source_binding,
        support=support_binding,
        output_includes_discount=True,
        further_discount_factor_applied=[1, 1],
        dollar_terms=dollar_terms,
        failure_terms=failure_terms,
        ideal_digital_mean_certified=True,
        full_price_confidence_claim=False,
        adaptive_quantum_stages=0,
    )
    ledger["assessment"] = assess(ledger)
    return ledger
