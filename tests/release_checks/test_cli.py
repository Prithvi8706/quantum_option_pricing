import subprocess
import sys
from research.release_checks.audit import ROOT


def test_table_cli_refuses_overwrite(tmp_path):
    path = tmp_path / "table.csv"
    path.write_bytes(b"user data")
    result = subprocess.run(
        [sys.executable, "-m", "research.release_checks.tables", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert path.read_bytes() == b"user data"


def test_audit_cli_refuses_overwrite(tmp_path):
    path = tmp_path / "audit.json"
    path.write_bytes(b"user data")
    result = subprocess.run(
        [sys.executable, "-m", "research.release_checks.audit", "--output", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert path.read_bytes() == b"user data"
