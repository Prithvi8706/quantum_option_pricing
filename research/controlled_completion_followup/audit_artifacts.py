"""Read-only reconciliation of historical evidence and the new arithmetic backend."""

import hashlib
import json
from pathlib import Path

import numpy as np

from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.run import dump

REPO = Path(__file__).resolve().parents[2]
OLD = REPO / "results/controlled_source_completion"
NEW = REPO / "results/controlled_completion_followup/arithmetic_v1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    archive = json.loads((OLD / "validation_v2/artifact_manifest.json").read_text())
    for record in archive["artifacts"]:
        path = REPO / record["path"].replace("\\", "/")
        assert path.stat().st_size == record["bytes"] and digest(path) == record["sha256"]
    for record in archive["source_snapshot"]:
        path = OLD / "validation_v2/snapshot" / record["path"].replace("\\", "/")
        assert digest(path) == record["sha256"]
    cache, rows = {}, []
    for tag in ("C4_f24", "H8_f24", "C4_f40", "H8_f40", "phase_f64"):
        directory = NEW / "compile_v2" / tag
        source = json.loads((directory / "source.json").read_text())
        before = json.loads((OLD / "compile_v2" / tag / "target.json").read_text())
        after = json.loads((directory / "target.json").read_text())
        assert before == after, "Arithmetic redesign must not change the target law"
        library = resolve_library(source)
        count = np.zeros(3, dtype=np.int64)
        for call in source["forward_calls"]:
            key = (library, call["leaf"])
            if key not in cache:
                entry = json.loads((library / (call["leaf"] + ".json")).read_text())
                path = library / entry["gate_file"]
                assert digest(path) == entry["sha256"]
                gates = np.load(path, mmap_mode="r")
                assert np.all((gates[:, 0] >= 1) & (gates[:, 0] <= 3))
                for kind in (1, 2, 3):
                    wires = gates[gates[:, 0] == kind, 1 : 1 + kind]
                    assert np.all((wires >= 0) & (wires < entry["resources"]["qubits"]))
                    for i in range(kind):
                        for j in range(i):
                            assert np.all(wires[:, i] != wires[:, j])
                counts = np.bincount(gates[:, 0], minlength=4)[1:4]
                r = entry["resources"]
                assert counts.tolist() == [r["x"], r["cx"], r["ccx"]]
                assert 7 * int(counts[2]) == r["t_count"]
                cache[key] = counts
            count += cache[key]
            count[1] += call["argument_copy_cx"]
        count *= 2
        count[1] += len(source["outputs"]) * source["word_width"]
        r = source["resources"]
        assert count.tolist() == [r["x"], r["cx"], r["ccx"]]
        assert 7 * int(count[2]) == r["t_count"]
        rows.append(
            dict(
                tag=tag,
                target_unchanged=True,
                gates_reconciled=True,
                source_sha256=digest(directory / "source.json"),
                target_sha256=digest(directory / "target.json"),
            )
        )
    result = dict(
        historical_artifacts_unchanged=len(archive["artifacts"]),
        historical_snapshot_files_verified=len(archive["source_snapshot"]),
        unique_new_leaf_files=len(cache),
        sources=rows,
        scope="Byte preservation, identical digital targets, emitted gate hashes, "
        "wire validity, clean hierarchy counts. Financial and physical "
        "certification are separate.",
    )
    dump(NEW / "audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
