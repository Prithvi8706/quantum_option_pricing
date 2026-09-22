"""Verify a committed checkout with an isolated interpreter and retain receipts."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def replay(checkout, python, output):
    checkout, python, output = checkout.resolve(), python.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    initial_status = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=checkout, text=True
    )
    if initial_status:
        raise ValueError("Replay must start from a clean committed checkout")
    env = dict(os.environ, PYTHONNOUSERSITE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    prefix = [str(python), "-m"]
    commands = [
        (
            "environment",
            [
                str(python),
                "-c",
                "import site,sys,numpy,scipy,qiskit; "
                "assert site.ENABLE_USER_SITE is False; "
                "print(sys.version); print(sys.prefix); "
                "print(numpy.__version__,scipy.__version__,qiskit.__version__); "
                "print(qiskit.__file__)",
            ],
        ),
        (
            "tests",
            prefix
            + [
                "pytest",
                "research/antithetic_feasibility",
                "research/compound_feasibility",
                "research/controlled_residual_feasibility",
                "research/controlled_source_completion/test_completion.py",
                "research/controlled_completion_followup",
                "-q",
            ],
        ),
        (
            "archive_and_gate_audit",
            prefix + ["research.controlled_completion_followup.audit_artifacts"],
        ),
        ("arithmetic_replay", prefix + ["research.controlled_completion_followup.arithmetic_run"]),
        ("financial_bridge", prefix + ["research.controlled_completion_followup.financial_bridge"]),
        (
            "ft_model",
            prefix
            + [
                "research.controlled_completion_followup.ft_model",
                "--ledger",
                "results/controlled_completion_followup/arithmetic_v1/cost_v3_phase64/ledger.json",
            ],
        ),
    ]
    receipt = dict(
        commit=head,
        checkout=str(checkout),
        interpreter=str(python),
        initial_git_status=initial_status,
        steps=[],
        all_passed=False,
        scope="Fresh isolated environment; tests, preserved evidence, "
        "emitted-gate replay and deterministic financial/FT calculations. "
        "No quantum hardware or full pricing QPE execution.",
    )
    for name, command in commands:
        start = time.perf_counter()
        result = subprocess.run(
            command,
            cwd=checkout,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # Logs are new receipts, not modifications of byte-hashed historical logs.
        log = "\n".join(line.rstrip() for line in result.stdout.splitlines()).rstrip() + "\n"
        target = output / (name + ".txt")
        target.write_text(log, encoding="utf-8")
        row = dict(
            name=name,
            command=command,
            returncode=result.returncode,
            seconds=time.perf_counter() - start,
            log=target.name,
            log_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        )
        receipt["steps"].append(row)
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(row), flush=True)
        if result.returncode:
            raise RuntimeError("Checkout verification failed: " + name)
    receipt["all_passed"] = True
    receipt["final_git_status"] = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=checkout, text=True
    )
    receipt["final_status_note"] = (
        "Recompilation intentionally updates new result paths/timing diagnostics "
        "inside this isolated checkout. The original workspace evidence is preserved."
    )
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    replay(args.checkout, args.python, args.output)
