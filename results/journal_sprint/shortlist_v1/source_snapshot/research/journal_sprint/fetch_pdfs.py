"""Preserve complete primary PDFs and page-delimited text for reading."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

import requests

IDS = {
    "bae": "2412.04394v5",
    "biqae": "2507.23074v2",
    "noisy_mle": "2006.16223",
    "iqae_bias": "2311.16560v2",
    "geometric": "2609.02715v1",
    "quantum_qmc": "2609.03625v1",
}


def main():
    path = Path("results/journal_sprint/primary_pdfs_v1")
    path.mkdir(parents=True, exist_ok=False)

    def fetch(item):
        name, identifier = item
        url = "https://arxiv.org/pdf/" + identifier
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        if not response.content.startswith(b"%PDF"):
            raise ValueError("Not PDF: " + url)
        pdf = path / (name + ".pdf")
        pdf.write_bytes(response.content)
        text_path = path / (name + ".txt")
        subprocess.run([shutil.which("pdftotext"), "-layout", str(pdf), str(text_path)], check=True)
        text = text_path.read_text(encoding="utf-8")
        result = {
            "name": name,
            "url": url,
            "resolved_url": response.url,
            "sha256": hashlib.sha256(response.content).hexdigest(),
            "pages": text.count("\f"),
            "characters": len(text),
        }
        print(result, flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        result = list(pool.map(fetch, IDS.items()))
    (path / "retrieval.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
