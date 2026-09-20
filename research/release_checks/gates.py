"""Keep artifact readiness separate from unsupported scientific admission."""

GATES = {
    "human_novelty_review",
    "physical_execution_budget",
    "matched_quantum_classical_advantage",
    "fresh_confirmation",
    "human_submission_approval",
}


def scientific_status(gates):
    if set(gates) != GATES or any(type(v) is not bool for v in gates.values()):
        raise ValueError("complete boolean scientific gate inventory required")
    if any(gates.values()):
        raise ValueError("v1 has no evidence-backed promotion workflow; human review required")
    return {
        "submission_ready": False,
        "confirmation_admitted": False,
        "open_gates": sorted(GATES),
        "reason": "artifact checks cannot establish scientific admission",
    }
