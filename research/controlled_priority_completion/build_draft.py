"""Render the companion Markdown with local Markdown 3.7 and headless Edge.

Document tools are separate from the pinned scientific environment. No network
assets, journal submission or author details are inserted by this build.
"""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--browser", default=("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / ".context/controlled_document_tools"))
    import markdown

    assert importlib.metadata.version("Markdown") == "3.7"
    directory = root / "manuscript/controlled-compound-2026-09-22"
    source = directory / "main.md"
    text = source.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html = (
        """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Auditable digital-oracle resources for controlled compound Asian-basket pricing</title>
<style>
@page { size: A4; margin: 19mm 17mm; }
body { font-family: Georgia, serif; font-size: 10.5pt; line-height: 1.45; color: #111; }
h1 { font-size: 20pt; line-height: 1.2; } h2 { font-size: 14pt; margin-top: 1.3em; }
h3 { font-size: 12pt; } h1,h2,h3 { break-after: avoid; }
p { orphans: 3; widows: 3; } table { border-collapse: collapse; width: 100%; font-size: 8.7pt; }
th,td { border-bottom: 1px solid #999; padding: 5px 4px; text-align: left; }
tr { break-inside: avoid; } thead { display: table-header-group; }
pre { white-space: pre-wrap; font-size: 9pt; border-left: 2px solid #aaa; padding-left: 10px; }
code { overflow-wrap: anywhere; } a { color: #173f64; }
</style></head><body>"""
        + body
        + "</body></html>"
    )
    html_path, pdf_path = directory / "main.html", directory / "main.pdf"
    html_path.write_text(html, encoding="utf-8")
    command = [
        args.browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--user-data-dir=" + str(root / ".context/controlled_pdf_profile"),
        "--print-to-pdf=" + str(pdf_path),
        html_path.as_uri(),
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert completed.returncode == 0 and pdf_path.is_file(), completed.stderr
    assert pdf_path.read_bytes().startswith(b"%PDF")
    receipt = dict(
        markdown_version=markdown.__version__,
        command=command,
        returncode=completed.returncode,
        files={
            p.name: dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in (source, html_path, pdf_path)
        },
    )
    (directory / "build_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["files"], indent=2))


if __name__ == "__main__":
    main()
