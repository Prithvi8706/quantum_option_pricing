from research.release_checks.audit import build_report


def test_release_overlay_checks_evidence_but_does_not_promote_science():
    report = build_report()
    assert report['artifact_checks_passed']
    assert len(report['archives']) == 4
    assert all(r['exact_json'] for r in report['replays'])
    assert report['finite_diagnostics']['grid_inputs'] == 292
    assert not report['scientific_status']['submission_ready']
    assert not report['full_circuit_reconstruction_performed']
