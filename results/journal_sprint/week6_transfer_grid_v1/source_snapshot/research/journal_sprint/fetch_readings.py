"""Download primary full-text readings for a local, inspectable research ledger."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import hashlib

import requests
from bs4 import BeautifulSoup

SOURCES = {
    "bae": "https://arxiv.org/html/2412.04394v5",
    "biqae": "https://arxiv.org/html/2507.23074v2",
    "noisy_mle": "https://ar5iv.labs.arxiv.org/html/2006.16223",
    "iqae_bias": "https://arxiv.org/html/2311.16560v2",
    "geometric": "https://arxiv.org/html/2609.02715v1",
    "quantum_qmc": "https://arxiv.org/html/2609.03625v1",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/primary_readings_v1")
    parser.add_argument("--only", choices=list(SOURCES))
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)

    def fetch(item):
        key, url = item
        response = requests.get(url, timeout=45)
        result = {
            "key": key,
            "url": url,
            "resolved_url": response.url,
            "status": response.status_code,
        }
        if response.status_code == 200:
            (output / f"{key}.html").write_bytes(response.content)
            soup = BeautifulSoup(response.content, "html.parser")
            for math_tag in soup.find_all("math"):
                math_tag.replace_with(" " + math_tag.get("alttext", math_tag.get_text()) + " ")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            body = soup.find("article") or soup.find("main") or soup
            text = "\n".join(
                line.strip() for line in body.get_text("\n").splitlines() if line.strip()
            )
            (output / f"{key}.txt").write_text(text, encoding="utf-8")
            result.update(characters=len(text), sha256=hashlib.sha256(response.content).hexdigest())
        print(result, flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        selected = {args.only: SOURCES[args.only]} if args.only else SOURCES
        results = list(pool.map(fetch, selected.items()))
    (output / "retrieval.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
