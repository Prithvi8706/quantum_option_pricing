"""Finite, confidence-spending IQAE adapters with exact toy observations.

These adapters use the original ratio2/modified ratio3 branch-selection ideas,
but do not claim to reproduce either paper's native repeated-look controller.
All successful delivered intervals have simultaneous ideal-observation coverage.
A safety cap produces an explicit non-delivery, not a certified estimate.
"""

from fractions import Fraction
from math import ceil
import random

import mpmath as mp

from research.limitation_program_20261001 import audit_barrier_band as audit


ROOT = audit.ROOT
RESULTS = audit.RESULTS
EPSILON = Fraction(9, 128000)
ALPHA = Fraction(3, 1000)
MAX_ROUNDS = 20
MAX_LOOKS_PER_ROUND = 8
MAX_PAID_SOURCE_PAIRS = 983024
MAX_POWER_SEARCH_EVENTS = 100000
INVERSE_BISECTIONS = 80
IV_DIGITS = 110
SETTINGS = tuple(
    {"family": family, "first_batch_shots": shots}
    for family in ("original-IQAE-adapter", "modified-IQAE-adapter")
    for shots in (16, 32, 64, 128)
)
TOY_LAWS = (
    {
        "name": "coin-Y0-or16",
        "Y_dollars": [0, 16],
        "probabilities_exact": [[1, 2], [1, 2]],
        "mean_Y_dollars_exact": [8, 1],
        "amplitude_exact": [1, 8],
    },
    {
        "name": "coin-Y0-or32",
        "Y_dollars": [0, 32],
        "probabilities_exact": [[1, 2], [1, 2]],
        "mean_Y_dollars_exact": [16, 1],
        "amplitude_exact": [1, 4],
    },
)
PROOF = {
    "coverage": (
        "Before each fresh batch choose its power, integer size and failure allocation"
        " from past observations. Given that history, observations are independent"
        " Bernoulli(p_k). Hoeffding's two-sided failure is at most2*exp(-2*N*r^2)."
        " The radius is rounded upward from sqrt(log(2/delta)/(2*N)). Each new"
        " look uses fresh counts, so conditional fixed-batch coverage is valid."
        " Intersect outward converted intervals with prior knowledge. On simultaneous"
        " coverage every interval contains theta; a delivered amplitude interval"
        " of width<=2*epsilon yields its midpoint within epsilon."
    ),
    "spending": (
        "The original adapter allocates alpha/20 per round; at most20 rounds are"
        " admitted. The modified adapter allocates(2*alpha/3)*K/Kcap per round."
        " Distinct modified round powers increase by at least3 and never exceed"
        " fixed Kcap, so sumK<=3*Kcap/2 on every history, giving sumalpha_round<=alpha."
        " Within each round delta_look=alpha_round/[l*(l+1)] for l>=1. Its total"
        " is at mostalpha_round by telescoping. The conditional union bound"
        " therefore covers every admitted adaptive look, including stopping."
    ),
    "branch": (
        "Store theta/pi in[0,1/2]. Select odd K only when the scaled prior interval"
        " lies in one closed half-unit quadrant. On even quadrants sin^2(pi*t)"
        " increases; on odd quadrants it decreases. mp.iv sine enclosures and"
        " monotone rational bisection convert the binomial interval outward."
        " Endpoints0/1 map exactly. No branch is discarded using observed truth."
    ),
    "paid_budget": (
        "A shot costs k original Grover blocks plus one terminal original F/selector"
        " forward and literal-inverse cleanup pair. Before acquiring a batch, check"
        " N*(k+1) against the remaining983024 paid-source-pair cap. No acquisition"
        " is admitted over the cap. Finite round/look/search caps retain non-delivery."
        " Coverage of delivered intervals does not certify delivery for every"
        " financial amplitude within that budget."
    ),
    "exact_toys": (
        "For rational amplitude a, p_k=(1-T_{2k+1}(1-2a))/2, by the standard"
        " Grover rotation and Chebyshev identity. Exact rational doubling computes"
        " this probability. Bernoulli draws compare uniform integers with its"
        " rational numerator (rejection if needed); counts are exact-binomial"
        " model observations, not quantum circuit jobs or financial samples."
    ),
}


def angle_probability(theta_over_pi):
    value = Fraction(theta_over_pi)
    if value == 0:
        return Fraction(0), Fraction(0)
    if value == Fraction(1, 2):
        return Fraction(1), Fraction(1)
    old = mp.iv.dps
    mp.iv.dps = IV_DIGITS
    try:
        return audit.endpoints(mp.iv.sin(mp.iv.pi * audit.iv(value)) ** 2)
    finally:
        mp.iv.dps = old


def inverse_probability(probability):
    probability = Fraction(probability)
    if not 0 <= probability <= 1:
        raise ValueError("Inverse probability outside[0,1]")
    special = {
        Fraction(0): Fraction(0),
        Fraction(1, 4): Fraction(1, 6),
        Fraction(1, 2): Fraction(1, 4),
        Fraction(3, 4): Fraction(1, 3),
        Fraction(1): Fraction(1, 2),
    }
    if probability in special:
        return (special[probability],) * 2
    lower, upper = Fraction(0), Fraction(1, 2)
    for _ in range(INVERSE_BISECTIONS):
        middle = (lower + upper) / 2
        lo, hi = angle_probability(middle)
        if hi < probability:
            lower = middle
        elif lo > probability:
            upper = middle
        else:
            # An unresolved comparison preserves the current outward bracket.
            break
    return lower, upper


def hoeffding_interval(hits, shots, failure):
    if type(hits) is not int or type(shots) is not int or not 0 <= hits <= shots or shots < 1:
        raise ValueError("Exact integer batch counts required")
    failure = Fraction(failure)
    if not 0 < failure < 1:
        raise ValueError("Positive allocated failure required")
    old = mp.iv.dps
    mp.iv.dps = IV_DIGITS
    try:
        radius = audit.endpoints(mp.iv.sqrt(mp.iv.log(2 / audit.iv(failure)) / (2 * shots)))[1]
    finally:
        mp.iv.dps = old
    radius = Fraction(ceil(radius * (1 << 64)), 1 << 64)
    empirical = Fraction(hits, shots)
    return max(Fraction(0), empirical - radius), min(Fraction(1), empirical + radius), radius


def chebyshev_pair(degree, argument):
    """Exact(T_n,T_{n+1}) by doubling; logarithmically many rational operations."""
    argument = Fraction(argument)
    if type(degree) is not int or degree < 0:
        raise ValueError("Nonnegative Chebyshev degree required")
    if degree == 0:
        return Fraction(1), argument
    first, second = chebyshev_pair(degree // 2, argument)
    even, odd = 2 * first**2 - 1, 2 * first * second - argument
    return (odd, 2 * second**2 - 1) if degree % 2 else (even, odd)


def exact_grover_probability(amplitude, power):
    amplitude = Fraction(amplitude)
    if not 0 <= amplitude <= 1 or type(power) is not int or power < 0:
        raise ValueError("Exact amplitude and nonnegative integer power required")
    polynomial = chebyshev_pair(2 * power + 1, 1 - 2 * amplitude)[0]
    value = (1 - polynomial) / 2
    audit.require(0 <= value <= 1, "Exact Grover probability outside unit interval")
    return value


class ExactToyObserver:
    def __init__(self, amplitude, seed):
        self.amplitude = Fraction(amplitude)
        self.rng = random.Random(seed)
        self.probabilities = {}

    def __call__(self, power, shots):
        if power not in self.probabilities:
            self.probabilities[power] = exact_grover_probability(self.amplitude, power)
        probability = self.probabilities[power]
        if probability in (0, 1):
            return shots * int(probability)
        numerator, denominator = probability.numerator, probability.denominator
        bits = (denominator - 1).bit_length()
        hits = 0
        for _ in range(shots):
            draw = self.rng.getrandbits(bits)
            while draw >= denominator:
                draw = self.rng.getrandbits(bits)
            hits += int(draw < numerator)
        return hits


def power_cap():
    old = mp.iv.dps
    mp.iv.dps = IV_DIGITS
    try:
        return audit.endpoints(mp.iv.pi / (4 * audit.iv(EPSILON)))[0].__floor__()
    finally:
        mp.iv.dps = old


def controller(observe, setting):
    if setting not in SETTINGS:
        raise ValueError("One of the eight frozen controller settings required")
    ratio = 2 if setting["family"] == "original-IQAE-adapter" else 3
    kcap = power_cap()
    lower, upper = Fraction(0), Fraction(1, 2)
    K, quadrant, round_number, look = 1, 0, 1, 1
    total_Q, total_shots, paid, search_events = 0, 0, 0, 0
    log, allocated_rounds = [], []
    status, reason = "censored", "round-cap"
    while round_number <= MAX_ROUNDS:
        round_failure = ALPHA / MAX_ROUNDS if ratio == 2 else Fraction(2, 3) * ALPHA * K / kcap
        if look == 1:
            allocated_rounds.append(round_failure)
        shots = setting["first_batch_shots"] * (1 << (look - 1))
        power = (K - 1) // 2
        if paid + shots * (power + 1) > MAX_PAID_SOURCE_PAIRS:
            reason = "paid-source-pair-cap-before-acquisition"
            break
        failure = round_failure / (look * (look + 1))
        hits = observe(power, shots)
        pl, pu, radius = hoeffding_interval(hits, shots, failure)
        if quadrant % 2:
            pl, pu = 1 - pu, 1 - pl
        local_lo = inverse_probability(pl)[0]
        local_hi = inverse_probability(pu)[1]
        lower = max(lower, (Fraction(quadrant, 2) + local_lo) / K)
        upper = min(upper, (Fraction(quadrant, 2) + local_hi) / K)
        total_Q += power * shots
        total_shots += shots
        paid += (power + 1) * shots
        log.append(
            dict(
                round=round_number,
                look=look,
                K=K,
                power=power,
                quadrant=quadrant,
                shots=shots,
                hits=hits,
                failure_exact=audit.pair(failure),
                hoeffding_radius_upper_exact=audit.pair(radius),
                theta_over_pi_interval_exact=list(map(audit.pair, (lower, upper))),
            )
        )
        if lower > upper:
            reason = "inconsistent-confidence-intersection"
            break
        amplitude = (
            max(Fraction(0), angle_probability(lower)[0]),
            min(Fraction(1), angle_probability(upper)[1]),
        )
        if amplitude[1] - amplitude[0] <= 2 * EPSILON:
            status, reason = "delivered", "outward-amplitude-interval-within-tolerance"
            break
        if lower == upper:
            reason = "unresolved-outward-amplitude-rounding"
            break
        proposed = min(kcap, (Fraction(1, 2) / (upper - lower)).__floor__())
        if proposed % 2 == 0:
            proposed -= 1
        next_K, next_quadrant = None, None
        while proposed >= ratio * K:
            if search_events >= MAX_POWER_SEARCH_EVENTS:
                break
            search_events += 1
            left, right = proposed * lower, proposed * upper
            half = (2 * left).__floor__()
            if right <= Fraction(half + 1, 2):
                next_K, next_quadrant = proposed, half
                break
            proposed -= 2
        if search_events >= MAX_POWER_SEARCH_EVENTS and next_K is None:
            reason = "power-search-event-cap"
            break
        if next_K is not None:
            K, quadrant = next_K, next_quadrant
            round_number, look = round_number + 1, 1
        else:
            look += 1
            if look > MAX_LOOKS_PER_ROUND:
                reason = "look-cap"
                break
    audit.require(
        sum(allocated_rounds, Fraction(0)) <= ALPHA, "Adaptive failure allocation exceeded"
    )
    audit.require(paid <= MAX_PAID_SOURCE_PAIRS, "Prospective paid budget exceeded")
    delivered = status == "delivered"
    return dict(
        status=status,
        stop_reason=reason,
        setting=setting,
        transcript=log,
        admitted_rounds=len(allocated_rounds),
        admitted_batches=len(log),
        total_Q_calls=total_Q,
        total_terminal_F_selector_clean_pairs=total_shots,
        paid_source_pairs=paid,
        longest_single_shot_Q_chain=max((row["power"] for row in log), default=0),
        power_search_events=search_events,
        failure_allocation_upper_exact=audit.pair(sum(allocated_rounds, Fraction(0))),
        amplitude_interval_exact=list(map(audit.pair, amplitude)) if delivered else None,
        dollar_interval_exact=[audit.pair(64 * value) for value in amplitude]
        if delivered
        else None,
        delivered_midpoint_amplitude_error_at_most_exact=audit.pair(EPSILON) if delivered else None,
        simultaneous_ideal_failure_upper_exact=audit.pair(ALPHA),
        uniform_financial_delivery_within_budget_proved=False,
        censored_result_is_certified_estimate=False,
        paper_native_controller_reproduced=False,
    )


def conditional_financial_cost(row, wrapper, baseline):
    shots, Q = row["total_terminal_F_selector_clean_pairs"], row["total_Q_calls"]
    terminal_T = wrapper["financial_resources"]["t_count"] + sum(
        value["t_count"] for value in wrapper["selector_costs"].values()
    )
    terminal_depth = wrapper["financial_resources"]["t_depth"] + sum(
        value["t_depth"] for value in wrapper["selector_costs"].values()
    )
    result = dict(
        conditional_on_same_original_ideal_digital_source=True,
        financial_forwards=Q + shots,
        financial_literal_inverses=Q + shots,
        selector_forwards=Q + shots,
        selector_literal_inverses=Q + shots,
        original_pinned_active_Grover_reflections=Q,
        terminal_flag_measurements=shots,
        uniform_preparation_H=shots * len(wrapper["random_wires"]),
        control_X_preparations=shots,
        control_X_cleanup=shots,
        required_random_reset_bits=shots * len(wrapper["random_wires"]),
        source_and_selector_clean_after_terminal_literal_inverse=True,
        adaptive_feedback_updates=row["admitted_batches"],
        total_physical_readout_reset_feedback_seconds=None,
        logical_qubits=wrapper["resources"]["logical_qubits"],
        logical_T_count=Q * wrapper["resources"]["t_count"] + shots * terminal_T,
        logical_serial_unitary_T_depth=Q * wrapper["resources"]["t_depth"] + shots * terminal_depth,
        finance_measurements_or_gate_replays_executed=0,
        actual_financial_controller_cost_measured=False,
        finance_eligibility=(
            "Requires actual digital-source observation/controller delivery "
            "and independent coverage/cost audit"
        ),
    )
    result["toy_delivered_and_conditional_logical_T_work_below_canonical"] = (
        row["status"] == "delivered"
        and result["logical_T_count"] < baseline["full_T_count"]
        and result["logical_serial_unitary_T_depth"] < baseline["full_T_depth"]
    )
    result["full_G2_or_physical_certificate"] = False
    return result
