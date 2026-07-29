import re

from research.paper_a.environment import capture_environment

REQUIRED_PACKAGES = ("qiskit-terra", "qiskit-aer", "qiskit-algorithms",
                     "qiskit-finance", "numpy", "scipy")


def test_capture_returns_all_required_keys():
    env = capture_environment()
    assert set(env) == {"python_version", "packages", "git_commit",
                        "platform", "captured_at_utc"}


def test_capture_records_every_required_package():
    env = capture_environment()
    for name in REQUIRED_PACKAGES:
        assert name in env["packages"], f"{name} missing from environment lock"
        assert re.match(r"^\d+\.\d+", env["packages"][name])


def test_git_commit_is_a_full_sha():
    env = capture_environment()
    assert re.fullmatch(r"[0-9a-f]{40}", env["git_commit"])


def test_timestamp_is_utc_iso8601():
    env = capture_environment()
    assert env["captured_at_utc"].endswith("+00:00")


def test_capture_is_stable_except_for_timestamp():
    a, b = capture_environment(), capture_environment()
    a.pop("captured_at_utc")
    b.pop("captured_at_utc")
    assert a == b
