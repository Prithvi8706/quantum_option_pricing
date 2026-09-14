"""Download primary full-text readings for a local, inspectable research ledger."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import hashlib
from urllib.parse import urlparse

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

TITLE_PREFIXES = {
    "bae": "bayesian quantum amplitude estimation",
    "biqae": "harnessing bayesian statistics to accelerate iterative quantum amplitude estimation",
    "noisy_mle": "amplitude estimation via maximum likelihood",
    "iqae_bias": "on the bias in iterative quantum amplitude estimation",
    "geometric": "quantum amplitude estimation beyond power-of-two schedules",
    "quantum_qmc": "quantum quasi-monte carlo:",
}


def validated_article(key, response):
    expected, actual = urlparse(SOURCES[key]), urlparse(response.url)
    if (
        actual.scheme != "https"
        or actual.hostname != expected.hostname
        or actual.path.rstrip("/") != expected.path.rstrip("/")
    ):
        raise ValueError("response redirected away from the requested primary article")
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select_one("h1.ltx_title_document")
    article = soup.find("article")
    if (
        title is None
        or article is None
        or soup.select_one(".ltx_abstract") is None
        or len(article.get_text()) < 1000
        or not " ".join(title.get_text().lower().split()).startswith(TITLE_PREFIXES[key])
    ):
        raise ValueError("response is not the requested full-text article")
    return soup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/primary_readings_v1")
    parser.add_argument("--only", choices=list(SOURCES))
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)

    def fetch(item):
        key, url = item
        try:
            response = requests.get(url, timeout=45)
        except requests.RequestException as error:
            return {"key": key, "url": url, "retrieved": False, "error": str(error)}
        result = {
            "key": key,
            "url": url,
            "resolved_url": response.url,
            "status": response.status_code,
            "retrieved": False,
        }
        if response.status_code == 200:
            try:
                soup = validated_article(key, response)
            except ValueError as error:
                result["error"] = str(error)
                return result
            (output / f"{key}.html").write_bytes(response.content)
            for math_tag in soup.find_all("math"):
                math_tag.replace_with(" " + math_tag.get("alttext", math_tag.get_text()) + " ")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            body = soup.find("article") or soup.find("main") or soup
            text = "\n".join(
                line.strip() for line in body.get_text("\n").splitlines() if line.strip()
            )
            (output / f"{key}.txt").write_text(text, encoding="utf-8")
            result.update(
                retrieved=True,
                characters=len(text),
                sha256=hashlib.sha256(response.content).hexdigest(),
            )
        print(result, flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        selected = {args.only: SOURCES[args.only]} if args.only else SOURCES
        results = list(pool.map(fetch, selected.items()))
    (output / "retrieval.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
