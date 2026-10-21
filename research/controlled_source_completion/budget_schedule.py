"""Pack independent clean leaves into waves under an explicit logical-qubit cap."""

from collections import Counter

from research.controlled_priority_completion.parallel_source import entries, make_schedule


def make_budget_schedule(source, qubit_cap):
    """First-fit packing in decreasing depth order, independently at each DAG level."""
    schedule = make_schedule(source)
    metadata = entries(source)
    w = source["word_width"]
    retained = (source["values"] + len(source["outputs"])) * w
    capacity = qubit_cap - retained
    groups = []
    for wave in schedule["groups"]:
        batches = []
        for index in wave["call_indices"]:
            call = source["forward_calls"][index]
            r = metadata[call["leaf"]]["resources"]
            scratch = r["qubits"] - len(call["out"]) * w
            if scratch > capacity:
                raise ValueError("qubit cap cannot fit a single required leaf")
            batch = next((b for b in batches if b["scratch"] + scratch <= capacity), None)
            if batch is None:
                batch = dict(indices=[], scratch=0)
                batches.append(batch)
            batch["indices"].append(index)
            batch["scratch"] += scratch
        for batch in batches:
            calls = [source["forward_calls"][i] for i in batch["indices"]]
            copy_depth = max(Counter(a for c in calls for a in c["args"]).values(), default=0)
            rs = [metadata[c["leaf"]]["resources"] for c in calls]
            groups.append(dict(wave=wave["wave"], call_indices=batch["indices"],
                               private_scratch_qubits=batch["scratch"], copy_rounds=copy_depth,
                               t_depth=max(r["t_depth"] for r in rs),
                               clifford_t_depth=max(r["clifford_t_depth"] for r in rs)
                               + 2 * copy_depth))
    scratch = max(g["private_scratch_qubits"] for g in groups)
    output_depth = max(Counter(source["outputs"].values()).values(), default=0)
    schedule["groups"] = groups
    schedule["parallel_limit"] = None
    schedule["qubit_cap"] = qubit_cap
    schedule["packing"] = "First fit by decreasing leaf T-depth within each dependency wave"
    schedule["resources"].update(
        logical_qubits=retained + scratch, max_reused_scratch_qubits=scratch,
        t_depth=2 * sum(g["t_depth"] for g in groups),
        clifford_t_depth=2 * sum(g["clifford_t_depth"] for g in groups) + output_depth,
        t_depth_schedule="Memory-capped wave batches; shared-control copies paid separately",
    )
    return schedule
