"""Archive installed package pins and dependency consistency, without credentials."""

import argparse
import importlib.metadata
from pathlib import Path
import platform
import shutil
import subprocess
import sys

from .storage import finish_run, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    packages = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    check = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
    write_json(
        args.output / "environment.json",
        {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": packages,
            "pip_check_exit_code": check.returncode,
            "pip_check": check.stdout + check.stderr,
        },
    )
    with (args.output / "installed-pins.txt").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(f"{name}=={version}" for name, version in sorted(packages.items())))
        stream.write("\n")
    shutil.copy2(__file__, args.output / "environment_snapshot.py")
    if check.returncode:
        raise RuntimeError("dependency consistency check failed; evidence retained")
    finish_run(args.output)
    print(f"Archived {len(packages)} packages; pip check passed")


if __name__ == "__main__":
    main()
