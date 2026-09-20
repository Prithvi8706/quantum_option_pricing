"""Explicitly scoped D1/D2 market and route menu; no silent problem pivot."""

CASES = [
    dict(id="D1", split="development", assets=1, dates=2, sigma=0.2, strike=95.0, correlation=0.3),
    dict(
        id="D2", split="development", assets=2, dates=2, sigma=0.25, strike=105.0, correlation=0.4
    ),
]
MENU = [("reflection", d) for d in (16, 32, 64, 128)] + [("ripple", 24), ("fourier", 24)]


def verify_targets(results):
    cases = results["comparisons"]
    if [c["case"] for c in cases] != CASES:
        raise ValueError("financial target or case menu changed")
    for case in cases:
        plan = case["arithmetic_plan"]
        if any(
            plan[k] != v
            for k, v in {"normal_bits": 10, "fraction_bits": 20, "width": 40, "degree": 24}.items()
        ):
            raise ValueError("precision menu changed")
        if [(r["mode"], r["degree"]) for r in case["alternatives"]] != MENU:
            raise ValueError("route or degree menu changed")
        if case["production_choice"] is not None or case["confirmation"] is not False:
            raise ValueError("unsupported case promotion")
    if results["candidate_status"] != "standby" or results["confirmation_admitted"] is not False:
        raise ValueError("unsupported candidate promotion")
    if results["quantum_over_classical_advantage_established"] is not False:
        raise ValueError("unsupported advantage claim")
    return {"cases": 2, "configurations": 12, "target_scope": "frozen development menu"}
