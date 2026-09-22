"""Inventory the private reading cache without publishing third-party full texts."""

import hashlib
import json
from pathlib import Path


def main():
    root = Path("docs/research_investigation/2026-09-22/sources")
    sources = {
        "kernel_nested": "https://proceedings.mlr.press/v267/chen25av.html",
        "nonlinear_": "https://arxiv.org/abs/2502.05094",
        "repeated_icml": "https://icml.cc/virtual/2026/poster/63263",
        "repeated_": "https://arxiv.org/abs/2602.08120",
        "spde_": "https://arxiv.org/abs/2606.31076",
        "wang_kan": "https://arxiv.org/abs/2312.15871",
    }
    rows = []
    for file in sorted(root.iterdir()):
        if file.suffix not in (".txt", ".pdf", ".html", ".png"):
            continue
        url = next(url for prefix, url in sources.items() if file.name.startswith(prefix))
        rows.append(
            dict(
                local_filename=file.name,
                bytes=file.stat().st_size,
                sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                source=url,
            )
        )
    (root / "PROVENANCE.json").write_text(
        json.dumps(
            dict(
                reading_date="2026-09-22",
                artifacts=rows,
                publication="Full third-party downloads stay local; links and hashes only.",
                instructions="Retrieve papers at the primary links. Extracted text depends "
                "on the extraction tool; this inventory preserves the original "
                "local evidence rather than promising identical extraction bytes.",
            ),
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
