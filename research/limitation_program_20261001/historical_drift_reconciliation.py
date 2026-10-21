"""Read-only reconstruction of nine old Stage C inventory bytes and provenance.

Recovered old bytes never replace live code or old receipt hashes. A recovered
historical snapshot and a matching live external dependency are distinct claims.
"""

from __future__ import annotations

import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results/limitation_program_20261001"
RECEIPTS = ("A18_run001", "A18_B4_run001", "A01_run015", "A01_run016")
STEMS = (
    "c1_rates",
    "c2_timing",
    "c4_coverage",
    "c5_smoothers",
    "c7_c8_cases",
    "decision",
    "fit",
    "kernels",
    "scrambles",
)
PATHS = tuple("research/frontier_classical_20261001/" + name + ".py" for name in STEMS)
TRANSFORMS = ("identity", "normalize_CRLF_to_LF", "materialize_LF_as_CRLF")
MAX_COMMITS = 256
MAX_ARCHIVE_CANDIDATES = 1000
INVENTORY_EVIDENCE = {
    "A18_run001": (
        "executed_code/experiment_checkpoint.py",
        'for p in ROOT.joinpath("research").rglob("*.py"):',
    ),
    "A18_B4_run001": (
        "executed_code/experiment_checkpoint_B4.py",
        'frozen = dict(prior["frozen_inputs"])',
    ),
    "A01_run015": (
        "executed_reconcile_checkpoint_v2.py",
        'for path, expected in protocol["frozen_inputs"].items():',
    ),
    "A01_run016": (
        "reconcile_checkpoint_B4.py",
        'frozen = dict(protocol["frozen_inputs"])',
    ),
}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hash_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def relative(path, root=ROOT):
    return Path(path).resolve().relative_to(root.resolve()).as_posix()


def local(root, name):
    path = (root / name).resolve()
    require(path.is_relative_to(root.resolve()), "Path escaped local workspace")
    return path


def git(root, *args):
    completed = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    require(completed.returncode == 0, "Read-only local Git command failed: " + args[0])
    return completed.stdout


def transformed(payload, transform):
    if transform == "identity":
        return payload
    normalized = payload.replace(b"\r\n", b"\n")
    if transform == "normalize_CRLF_to_LF":
        return normalized
    if transform == "materialize_LF_as_CRLF":
        return normalized.replace(b"\n", b"\r\n")
    raise ValueError("Undeclared byte transformation")


def matching_transform(payload, expected):
    for transform in TRANSFORMS:
        if hash_bytes(transformed(payload, transform)) == expected:
            return transform
    return None


def verify_git_object(payload, oid, object_format):
    require(object_format in ("sha1", "sha256"), "Unsupported local Git object format")
    header = b"blob " + str(len(payload)).encode("ascii") + b"\0"
    actual = hashlib.new(object_format, header + payload).hexdigest()
    require(actual == oid, "Local Git blob identity failed")


def roots_for(directory):
    protocol, manifest = read(directory / "protocol.json"), read(directory / "manifest.json")
    rows = []
    for dependency in protocol.get("executed_dependencies", []):
        original = dependency.get("original", dependency.get("source"))
        rows.append(
            dict(
                original=original,
                snapshot=dependency["snapshot"],
                sha256=dependency["sha256"],
                binding="explicit protocol executed_dependencies",
            )
        )
    if directory.name == "A01_run015":
        rows.append(
            dict(
                original="research/limitation_program_20261001/reconcile_checkpoint_v2.py",
                snapshot="executed_reconcile_checkpoint_v2.py",
                binding="own-script archived by prepare and manifest",
            )
        )
    if directory.name == "A01_run016":
        rows.append(
            dict(
                original="research/limitation_program_20261001/reconcile_checkpoint_B4.py",
                snapshot="reconcile_checkpoint_B4.py",
                binding="own-script archived by prepare and manifest",
            )
        )
    for row in rows:
        if "sha256" not in row:
            row["sha256"] = manifest["frozen_inputs"][row["original"]]
    return rows


def project_import_closure(root, roots):
    """Literal local-import closure only; no module is imported or executed."""
    overrides = {row["original"]: local(root, row["snapshot_workspace_path"]) for row in roots}
    todo, found, dynamic = list(overrides), {}, []
    while todo:
        original = todo.pop()
        if original in found:
            continue
        path = overrides.get(original, local(root, original))
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source)
        found[original] = path
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if node.level:
                    parent = original[:-3].replace("/", ".").split(".")[:-1]
                    module = ".".join(
                        parent[: len(parent) - node.level + 1] + ([module] if module else [])
                    )
                modules.append(module)
                modules.extend(
                    module + "." + alias.name for alias in node.names if alias.name != "*"
                )
            elif isinstance(node, ast.Call):
                name = ast.unparse(node.func)
                if name in ("__import__", "importlib.import_module", "exec", "eval"):
                    dynamic.append(dict(source=original, line=node.lineno, call=name))
        for module in modules:
            if module.startswith("research."):
                direct = module.replace(".", "/") + ".py"
                package = module.replace(".", "/") + "/__init__.py"
                for candidate in (direct, package):
                    if local(root, candidate).is_file():
                        todo.append(candidate)
    return found, dynamic


def metadata(root=ROOT):
    """Prepare inventory and Git tree identities before reading/searching old blobs."""
    root = Path(root).resolve()
    commits = (
        git(root, "rev-list", "--all", "--", "research/frontier_classical_20261001")
        .decode("ascii")
        .splitlines()
    )
    require(len(commits) <= MAX_COMMITS, "Prospective Git commit cap exceeded")
    objects = defaultdict(list)
    for commit in commits:
        listing = git(root, "ls-tree", "-r", commit, "--", *PATHS).decode("utf-8").splitlines()
        for line in listing:
            descriptor, name = line.split("\t", 1)
            _, kind, oid = descriptor.split()
            require(kind == "blob" and name in PATHS, "Unexpected local Git tree entry")
            objects[oid].append(dict(commit=commit, path=name))
    completed = subprocess.run(
        ["rg", "--files", "--hidden", "--no-ignore", "research", "results", "docs"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    require(completed.returncode in (0, 1), "Local archive filename inventory failed")
    filenames = {name + ".py" for name in STEMS}
    archives = []
    for name in completed.stdout.splitlines():
        path = local(root, name)
        rel = relative(path, root)
        if path.name in filenames and rel not in PATHS:
            archives.append(rel)
    require(len(archives) <= MAX_ARCHIVE_CANDIDATES, "Prospective archive filename cap exceeded")
    return dict(
        local_git_HEAD=git(root, "rev-parse", "HEAD").decode("ascii").strip(),
        object_format=git(root, "rev-parse", "--show-object-format").decode("ascii").strip(),
        commits=commits,
        git_blob_candidates=[
            dict(oid=oid, references=refs) for oid, refs in sorted(objects.items())
        ],
        archive_file_candidates=sorted(archives),
        old_blob_payloads_read_before_protocol=False,
        search_candidates_compared_to_old_sha_before_protocol=False,
    )


def reconcile(root, directory, frozen_metadata):
    root, directory = Path(root).resolve(), Path(directory).resolve()
    frozen = read(directory / "frozen_inputs.json")
    for name, expected in frozen.items():
        require(sha(local(root, name)) == expected, "Frozen reconciliation input changed: " + name)
    objects = {}
    object_dir = directory / "archived_git_blobs"
    object_dir.mkdir()
    for candidate in frozen_metadata["git_blob_candidates"]:
        oid = candidate["oid"]
        payload = git(root, "cat-file", "blob", oid)
        verify_git_object(payload, oid, frozen_metadata["object_format"])
        objects[oid] = payload
    provenance = []
    reference_rows = defaultdict(list)
    all_files_checked, all_snapshot_checked = 0, 0
    for name in RECEIPTS:
        historical = root / "results/limitation_program_20261001" / name
        manifest, protocol = read(historical / "manifest.json"), read(historical / "protocol.json")
        require(
            manifest["frozen_inputs"] == protocol["frozen_inputs"],
            "Manifest/protocol frozen map differs",
        )
        for path, expected in manifest["files"].items():
            require(
                sha(local(root, path)) == expected, "Historical receipt-owned file changed: " + path
            )
            all_files_checked += 1
        roots = roots_for(historical)
        evidence_name, evidence_statement = INVENTORY_EVIDENCE[name]
        evidence_path = historical / evidence_name
        evidence_lines = evidence_path.read_text(encoding="utf-8-sig").splitlines()
        evidence_line = [
            index + 1
            for index, line in enumerate(evidence_lines)
            if line.strip() == evidence_statement
        ]
        require(len(evidence_line) == 1, "Inventory-construction source evidence differs")
        for row in roots:
            snapshot = (historical / row["snapshot"]).resolve()
            require(snapshot.is_relative_to(historical), "Snapshot path outside original receipt")
            require(
                sha(snapshot) == row["sha256"] == manifest["frozen_inputs"][row["original"]],
                "Historical declared execution snapshot changed",
            )
            row["snapshot_workspace_path"] = relative(snapshot, root)
            all_snapshot_checked += 1
        closure, dynamic = project_import_closure(root, roots)
        for source, path in closure.items():
            if source in manifest["frozen_inputs"]:
                require(
                    sha(path) == manifest["frozen_inputs"][source],
                    "Literal executed project-import source changed: " + source,
                )
        changed_classical = []
        for path, expected in manifest["frozen_inputs"].items():
            if (
                path.startswith("research/frontier_classical_20261001/")
                and sha(local(root, path)) != expected
            ):
                changed_classical.append(path)
        require(set(changed_classical) == set(PATHS), "Declared nine-path drift scope changed")
        declared = {row["original"] for row in roots}
        for path in PATHS:
            reference_rows[path].append(
                dict(
                    receipt=name,
                    expected_sha256=manifest["frozen_inputs"][path],
                    manifest_sha256=sha(historical / "manifest.json"),
                    protocol_sha256=sha(historical / "protocol.json"),
                    declared_executed_snapshot=path in declared,
                    literal_project_import_reachable=path in closure,
                    legitimate_frozen_expectation_retained=True,
                    classification="blanket research inventory"
                    if name == "A18_run001"
                    else "inherited blanket research inventory",
                )
            )
        provenance.append(
            dict(
                receipt=name,
                declared_execution_roots=roots,
                literal_project_import_source_paths=sorted(closure),
                possible_dynamic_import_or_execution_calls=dynamic,
                runtime_import_trace_available=False,
                inventory_construction_evidence=dict(
                    archived_source=relative(evidence_path, root),
                    archived_source_sha256=sha(evidence_path),
                    line=evidence_line[0],
                    statement=evidence_statement,
                ),
                classification_scope=(
                    "Explicit snapshots plus literal imports and frozen producer inventory "
                    "construction; not a runtime non-execution proof"
                ),
            )
        )
    recovered_dir = directory / "recovered_original_inventory"
    recovered_dir.mkdir()
    rows, copied_oids = [], set()
    for path in PATHS:
        expected_set = {row["expected_sha256"] for row in reference_rows[path]}
        require(len(expected_set) == 1, "Historical Stage C expected versions differ")
        expected = expected_set.pop()
        match = None
        for archive in frozen_metadata["archive_file_candidates"]:
            if Path(archive).name == Path(path).name:
                payload = local(root, archive).read_bytes()
                if hash_bytes(payload) == expected:
                    match = (
                        payload,
                        dict(kind="existing archived file", path=archive, sha256=expected),
                        "identity",
                    )
                    break
        if match is None:
            for candidate in frozen_metadata["git_blob_candidates"]:
                references = [ref for ref in candidate["references"] if ref["path"] == path]
                if not references:
                    continue
                oid, payload = candidate["oid"], objects[candidate["oid"]]
                transform = matching_transform(payload, expected)
                if transform is not None:
                    object_path = object_dir / (oid + ".blob")
                    if oid not in copied_oids:
                        with object_path.open("xb") as handle:
                            handle.write(payload)
                        copied_oids.add(oid)
                    match = (
                        payload,
                        dict(
                            kind="local Git blob",
                            oid=oid,
                            object_format=frozen_metadata["object_format"],
                            raw_blob_sha256=hash_bytes(payload),
                            retained_raw_blob=relative(object_path, root),
                            commit_path_references=references,
                        ),
                        transform,
                    )
                    break
        recovered, evidence, transform = None, None, None
        if match is not None:
            payload, evidence, transform = match
            recovered = recovered_dir / Path(path).name
            with recovered.open("xb") as handle:
                handle.write(transformed(payload, transform))
            require(sha(recovered) == expected, "Recovered bytes do not match legitimate old SHA")
        actual = sha(local(root, path))
        rows.append(
            dict(
                path=path,
                expected_old_sha256=expected,
                live_current_sha256=actual,
                expected_live_matches=actual == expected,
                historical_old_bytes_recovered=recovered is not None,
                recovered_snapshot_path=relative(recovered, root) if recovered else None,
                recovered_snapshot_sha256=sha(recovered) if recovered else None,
                source_evidence=evidence,
                exact_byte_materialization=transform,
                references=reference_rows[path],
                expected_hash_waived=False,
                actor_or_reason_attributed=False,
            )
        )
    reconstructed = all(row["historical_old_bytes_recovered"] for row in rows)
    return dict(
        passed=reconstructed,
        local_only=True,
        affected_receipts=list(RECEIPTS),
        distinct_drift_paths=len(rows),
        old_expected_reference_count=sum(len(row["references"]) for row in rows),
        rows=rows,
        execution_provenance=provenance,
        original_receipt_owned_files_hash_checked=all_files_checked,
        original_declared_executed_snapshots_hash_checked=all_snapshot_checked,
        historical_snapshot_integrity=reconstructed,
        historical_snapshot_integrity_scope=(
            "Nine recovered old inventory byte strings, receipt-owned files and declared "
            "execution snapshots/literal project imports only"
        ),
        global_live_integrity=False,
        global_live_integrity_reason=(
            "Nine legitimate frozen live external expectations still differ; "
            "reconstruction never replaces or waives them"
        ),
        legitimate_expected_hashes_waived=False,
        old_receipts_or_live_sources_modified=False,
        full_program_external_dependency_or_quantum_array_scan_repeated=False,
        old_runtime_import_trace_available=False,
        actor_attribution=None,
        new_financial_or_quantum_executions=0,
        next=(
            "Keep both archived reconstruction and unresolved live external drift "
            "in the versioned full-program validator report"
        ),
    )
