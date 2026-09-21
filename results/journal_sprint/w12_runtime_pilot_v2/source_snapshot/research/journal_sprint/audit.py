"""Preserve historical evidence and recompute reference mismatch, without pickle loading."""

import argparse
import csv
import shutil
import subprocess
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from scipy.special import ndtr

from .storage import ROOT, finish_run, sha256, start_run, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/historical_audit_v1")
    args = parser.parse_args()
    path = start_run(args.output, {"historical_inputs_read_only": True})
    selected = [ROOT / "README.md", ROOT / "ROADMAP.md"]
    selected += list((ROOT / "data").glob("*"))
    selected += list((ROOT / "outputs").rglob("*"))
    selected += [
        ROOT / "src" / name
        for name in ("noise_experiments.py", "plot_dimension_sweep.py", "quantum.py")
    ]
    selected.append(ROOT / "app/precompute_qae.py")
    manifest = []
    for source in selected:
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        target = path / "evidence_snapshot" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        revision = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(relative)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        tracked = (
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", str(relative)], cwd=ROOT, capture_output=True
            ).returncode
            == 0
        )
        manifest.append(
            {
                "path": str(relative),
                "sha256": sha256(source),
                "bytes": source.stat().st_size,
                "tracked": tracked,
                "last_git_revision": revision or None,
                "provenance_limit": "Last path commit is not proof of producing run",
            }
        )
    write_json(path / "evidence_manifest.json", manifest)
    docx_claims = {}
    for source in (ROOT / "outputs").glob("*.docx"):
        with zipfile.ZipFile(source) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
        paragraphs = [
            "".join(p.itertext())
            for p in document.iter(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
            )
        ]
        docx_claims[source.name] = [
            p
            for p in paragraphs
            if any(term in p for term in ("0.203", "1.14", "0.65", "0.98", "0.77", "100"))
        ]
    write_json(path / "manuscript_claim_excerpts.json", docx_claims)
    with (ROOT / "data/noise_sweep_expanded.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    print("Historical CSV columns:", list(rows[0]), flush=True)
    # Column interpretation is explicit, never silently inferred from position.
    records = []
    for row in rows:
        s, k, r, t, sigma = [float(row[key]) for key in ("S0", "K", "r", "T", "sigma")]
        d1 = (np.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
        bs = s * ndtr(d1) - k * np.exp(-r * t) * ndtr(d1 - sigma * np.sqrt(t))
        records.append(dict(row, independent_black_scholes=float(bs)))
    write_json(path / "reference_rows.json", records)
    finish_run(path)


if __name__ == "__main__":
    main()
