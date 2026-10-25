"""Scope #44 R2 sealed run (orchestrator). See docs/r2_scope44/PREREGISTRATION.md.

Real run (the author only, after approving and committing the preregistration). It writes results/r2_scope44/RUN/
and the receipt .context/R2_SCOPE44_SEALED_RECEIPT_RUN.json:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/sealed_run.py --author-run RUN

Dry run (anyone; package QA only, NOT R2 evidence). It writes only under OUT and uses a different U1 seed, so it
reveals nothing about the real sample:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/sealed_run.py --dry-run OUT RUN
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = REPO / ".context/frontier_t0_env/Scripts/python.exe"
PREREG = REPO / "docs/r2_scope44/PREREGISTRATION.md"
MANIFEST = REPO / "research/r2_scope44/manifest.json"
STEPS_PY = REPO / "research/r2_scope44/steps.py"
REAL_BASE = REPO / "results/r2_scope44"
CONTEXT = REPO / ".context"
STEPS = [("p2", ["-I", "-S", "-B"]), ("a2a", ["-I", "-S", "-B"]), ("u1_sample", ["-I", "-B"]),
         ("u1_bound", ["-I", "-S", "-B"]), ("headline", ["-I", "-S", "-B"])]
SEED_TAG = {"real": b"r2-scope44-u1-seed-v1\n", "dry": b"r2-scope44-u1-DRY-RUN-seed-v1\n"}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def fail(msg):
    raise SystemExit(f"REFUSED: {msg}")


def gates(mode):
    """Checks made before anything runs. Returns the record of what was checked."""
    rec = {}
    if not sys.version.startswith("3.12.4") or Path(sys.executable).resolve() != PY.resolve():
        fail(f"interpreter must be {PY} (3.12.4); got {sys.executable} {sys.version.split()[0]}")
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        fail("run with -I -S -B")
    prereg, manifest = PREREG.read_bytes(), MANIFEST.read_bytes()
    rec["prereg_sha256"], rec["manifest_sha256"] = sha_bytes(prereg), sha_bytes(manifest)
    cited = re.findall(r"Manifest sha256: `([0-9a-f]{64})`", prereg.decode("utf-8"))
    if cited != [rec["manifest_sha256"]]:
        fail(f"PREREGISTRATION.md must cite the manifest sha256 exactly once ({rec['manifest_sha256']})")
    files = json.loads(manifest)["files"]
    bad = [p for p, h in files.items() if sha_bytes((REPO / p).read_bytes()) != h]
    if bad:
        fail(f"manifest hash mismatch: {bad}")
    rec["manifest_files"] = len(files)
    if mode == "real":
        text = prereg.decode("utf-8")
        block = text.split("## Approval", 1)[-1]
        if "<" in block.split("\n## ", 1)[0]:
            fail("the Approval block in PREREGISTRATION.md still has <placeholders>")
        tracked = [str(PREREG.relative_to(REPO)), str(MANIFEST.relative_to(REPO)), *files]
        for p in tracked:
            if git("ls-files", "--error-unmatch", p)[0] != 0:
                fail(f"not committed: {p}")
        if git("diff", "--quiet", "HEAD", "--", *tracked)[0] != 0:
            fail("preregistered files differ from HEAD; commit them first")
        rec["git_head"] = git("rev-parse", "HEAD")[1]
        rec["git_remote_branches_containing_head"] = git("branch", "-r", "--contains", rec["git_head"])[1].split()
        if not rec["git_remote_branches_containing_head"]:
            fail("push the preregistration commit first, so its timestamp is external")
        for old in REAL_BASE.glob("*/STARTED.json"):
            if json.loads(old.read_text(encoding="utf-8"))["prereg_sha256"] != rec["prereg_sha256"]:
                fail(f"{old.parent.name} ran under a different preregistration; a new one is a new scope")
            done = old.parent / "RECEIPT.json"
            if done.exists() and json.loads(done.read_text(encoding="utf-8"))["status"] == "PASS":
                fail(f"{old.parent.name} already passed; one sealed pass per preregistration")
    rec["seed_hex"] = sha_bytes(SEED_TAG[mode] + prereg + b"\n" + manifest)
    return rec


def files_with_hashes(root):
    return {str(p.relative_to(root)).replace("\\", "/"): sha_bytes(p.read_bytes())
            for p in sorted(root.rglob("*")) if p.is_file()}


def main(argv):
    if argv[:1] == ["--author-run"] and len(argv) == 2:
        mode, root, run = "real", REAL_BASE / argv[1], argv[1]
    elif argv[:1] == ["--dry-run"] and len(argv) == 3:
        mode, root, run = "dry", Path(argv[1]).resolve() / argv[2], argv[2]
        if CONTEXT.resolve() in root.parents or REAL_BASE.resolve() in root.parents:
            fail("a dry run may not write under .context/ or results/r2_scope44/")
    else:
        raise SystemExit(__doc__)
    rec = gates(mode)
    root.mkdir(parents=True, exist_ok=False)
    started = dict(schema="r2-scope44-started-v1", mode=mode, run=run, root=str(root),
                   created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=sys.version, **rec)
    (root / "STARTED.json").write_text(json.dumps(started, indent=1), encoding="utf-8")
    (root / "logs").mkdir()
    steps, status = [], "PASS"
    for name, flags in STEPS:
        t0 = time.perf_counter()
        r = subprocess.run([str(PY), *flags, str(STEPS_PY), name, str(root), rec["seed_hex"]], cwd=REPO,
                           capture_output=True, text=True)
        (root / "logs" / f"{name}.stdout.txt").write_text(r.stdout, encoding="utf-8")
        (root / "logs" / f"{name}.stderr.txt").write_text(r.stderr, encoding="utf-8")
        steps.append(dict(step=name, flags=flags, returncode=r.returncode, wall_s=time.perf_counter() - t0))
        print(name, "rc", r.returncode, f"{steps[-1]['wall_s']:.1f}s", flush=True)
        if r.returncode != 0:
            status = f"FAILED_AT_{name}"
            break
    outcome = None
    if status == "PASS":
        outcome = json.loads((root / "headline.json").read_text(encoding="utf-8"))["decision"]
    receipt = dict(schema="r2-scope44-sealed-receipt-v1", mode=mode, run=run, status=status, steps=steps,
                   decision=outcome, started=started, outputs_sha256=files_with_hashes(root),
                   completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   note=("A sealed receipt is one R2 step. R2 also needs the saved verifier (verify_sealed.py) and "
                         "the human result review in docs/r2_scope44/HUMAN_REVIEW_PACKET.md."
                         if mode == "real" else "DRY RUN: package QA only; not R2 evidence; different U1 seed."))
    body = json.dumps(receipt, indent=1).encode("utf-8")
    with open(root / "RECEIPT.json", "xb") as f:
        f.write(body)
    if mode == "real":
        with open(CONTEXT / f"R2_SCOPE44_SEALED_RECEIPT_{run}.json", "x", encoding="utf-8") as f:
            json.dump(dict(receipt_path=str((root / "RECEIPT.json").relative_to(REPO)).replace("\\", "/"),
                           receipt_sha256=sha_bytes(body), receipt=receipt), f, indent=1)
    print(status, json.dumps(outcome, indent=1) if outcome else "")


if __name__ == "__main__":
    main(sys.argv[1:])
