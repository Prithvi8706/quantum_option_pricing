"""Fixed local metadata verification of the executed prefix47 v3 receipt."""

from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/limitation_program_20261001/A03_prefix47_omission_audit_run002"
OUTPUT = ROOT / "results/limitation_program_20261001/A03_prefix47_root_verification_run001"
EXPECTED = "e683efa7396df78062fcf7faa71fba8cafad6630852c5998b961508717cabe3e"
CPU, WALL = 300, 900


def main():
    started = time.process_time(), time.monotonic()

    def budget():
        assert time.process_time() - started[0] < CPU, "Metadata CPU censor"
        assert time.monotonic() - started[1] < WALL, "Metadata wall censor"

    def digest(path):
        budget()
        value = hashlib.sha256()
        with path.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                budget()
                value.update(block)
        budget()
        return value.hexdigest()

    def read(name):
        return json.loads((SOURCE / name).read_text(encoding="utf-8"))

    assert not OUTPUT.exists(), "Fresh verification receipt only"
    manifest_path = SOURCE / "manifest.json"
    assert digest(manifest_path) == EXPECTED
    manifest = read("manifest.json")
    assert manifest["manifest_self_hash_excluded"] is True
    assert not any(
        (SOURCE / x).exists()
        for x in ("FAILED_UNSEALED.json", "failed_unsealed.json", "failure.json")
    )
    owned, frozen = manifest["files"], manifest["frozen_inputs"]
    assert len(owned) == 12 and len(frozen) <= 100000
    assert set(owned) == {
        p.relative_to(ROOT).as_posix()
        for p in SOURCE.rglob("*")
        if p.is_file() and p != manifest_path
    }
    requirements = {}
    byte_total = 0
    for field in (owned, frozen, {manifest_path.relative_to(ROOT).as_posix(): EXPECTED}):
        for name, expected in field.items():
            budget()
            lexical = ROOT / name
            actual = lexical.resolve(strict=True)
            assert actual.is_relative_to(ROOT) and actual.is_file()
            assert len(expected) == 64 and all(c in "0123456789abcdef" for c in expected)
            if name in owned:
                assert actual.is_relative_to(SOURCE)
            if actual in requirements:
                assert requirements[actual] == expected, "Conflicting expected SHA"
            else:
                requirements[actual] = expected
                byte_total += actual.stat().st_size
                assert byte_total <= 8 * 1024**3
    assert len(requirements) <= 100000
    for actual, expected in requirements.items():
        assert digest(actual) == expected, "Owned/frozen SHA mismatch: " + str(actual)
    summary, protocol = read("summary.json"), read("protocol.json")
    assert summary["passed"] and not summary["budget_censored"]
    assert summary["independent_ideal47_omission_applicability_passed"]
    assert summary["actual_absent_RY_slots"] == 47
    assert summary["new_test_credit"] == summary["old_fixture_recredit"] == 0
    assert summary["original_scientific_scope_limits_passed"]
    assert summary["scientific_source_AST_slot_symbolic_CPU_seconds"] < 60
    assert summary["scientific_source_AST_slot_symbolic_wall_seconds"] < 120
    assert summary["total_CPU_admission_wall_seconds"] == [180, 150, 600]
    assert protocol["frozen_inputs"] == frozen
    certificate = read("ideal_omission_symbolic_certificate.json")
    witnesses = certificate["actual_absent_slot_witnesses"]
    assert len(witnesses) == 47
    for row in witnesses:
        mask = row["Walsh_mask"]
        assert mask > 0 and mask.bit_count() % 2 == 0
        assert mask.bit_count() == row["mask_Hamming_weight"]
        assert row["exact_ideal_beta_zero"] and not row["actual_binary64_or_QASM_accuracy_proved"]
    assert summary["remaining_conditional_nodes_without_angle_certificates"] == 1020
    assert not summary["full_loader_phase_or_accuracy_certified"]
    assert not summary["original_binary64_target_symmetry_certified"]
    assert not summary["serialized_literalzero_accuracy_certified"]
    assert not summary["financial_law_adopted"]
    budget()
    OUTPUT.mkdir()
    report = dict(
        passed=True,
        local_only=True,
        source_manifest_sha256=EXPECTED,
        own_references=len(owned),
        frozen_references=len(frozen),
        distinct_verified_files=len(requirements),
        SHA_mismatches=0,
        ideal47_scope_and_zero_credit_reconciled=True,
        full_loader_and_financial_G2_remain_open=True,
        new_test_credit=0,
        metadata_only_CPU_wall_limits=[CPU, WALL],
        actual_CPU_seconds=time.process_time() - started[0],
        actual_wall_seconds=time.monotonic() - started[1],
    )
    report_path = OUTPUT / "summary.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    inputs = {p.relative_to(ROOT).as_posix(): h for p, h in requirements.items()}
    inputs[Path(__file__).relative_to(ROOT).as_posix()] = digest(Path(__file__))
    result = dict(
        files={report_path.relative_to(ROOT).as_posix(): digest(report_path)},
        frozen_inputs=inputs,
        manifest_self_hash_excluded=True,
        terminal_record=report_path.relative_to(ROOT).as_posix(),
    )
    (OUTPUT / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
