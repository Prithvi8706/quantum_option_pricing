"""Lossless evidence packaging/extraction, never rewriting producer manifests."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile


ROOT = Path(__file__).resolve().parents[2]
ARCHIVES = (
    "week10_stress_v1", "week10_stress_v2", "week10_stress_v3",
    "rescue_encoding_v1", "rescue_encoding_v2", "rescue_pilot_cs_v1",
    "encoding_decision_v1", "encoding_decision_v2", "allocation_v1", "shortlist_v1",
    "w11_baseline_pilot_v1", "w11_references_v1", "w11_main_v1",
)
DEFAULT = ROOT / "results/journal_sprint/week10_11_evidence_v1"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def member_path(name):
    p = PurePosixPath(name)
    if (not name or "\\" in name or ":" in name or p.is_absolute()
            or ".." in p.parts or "." in name.split("/") or "" in name.split("/")
            or len(p.parts) < 2):
        raise ValueError("unsafe bundle member")
    return p


def build(source_root, prefix, archives=ARCHIVES):
    source_root, prefix = Path(source_root).resolve(), Path(prefix)
    archive_path, index_path = prefix.with_suffix(".zip"), prefix.with_suffix(".json")
    if archive_path.exists() or index_path.exists():
        raise FileExistsError("bundle output already exists")
    if (not archives or len(set(archives)) != len(archives)
            or any(not name or name in (".", "..") or "/" in name or "\\" in name
                   or ":" in name for name in archives)):
        raise ValueError("simple unique archive names required")
    sources = []
    for name in archives:
        folder = source_root / name
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError("missing or symlinked archive")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise ValueError("symlinked evidence")
            if path.is_file():
                relative = path.relative_to(source_root).as_posix()
                member_path(relative)
                sources.append((relative, path))
    if not sources:
        raise ValueError("empty bundle")
    prefix.parent.mkdir(parents=True, exist_ok=True)
    entries = {}
    with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_DEFLATED) as output:
        for relative, path in sources:
            data = path.read_bytes()
            entries[relative] = dict(sha256=digest(data), size=len(data))
            output.writestr(relative, data)
    index = dict(version=1, archives=list(archives), entries=entries,
                 zip_sha256=digest(archive_path.read_bytes()),
                 note="Lossless original evidence and failed attempts; not regenerated results")
    with index_path.open("x", encoding="utf-8") as stream:
        json.dump(index, stream, indent=2)
        stream.write("\n")
    return dict(files=len(entries), uncompressed_bytes=sum(e["size"] for e in entries.values()),
                zip_bytes=archive_path.stat().st_size, zip_sha256=index["zip_sha256"])


def validate(prefix):
    prefix = Path(prefix)
    index = json.loads(prefix.with_suffix(".json").read_text(encoding="utf-8"))
    archive_path = prefix.with_suffix(".zip")
    if digest(archive_path.read_bytes()) != index["zip_sha256"]:
        raise ValueError("bundle checksum mismatch")
    if index.get("version") != 1 or not index.get("entries"):
        raise ValueError("unsupported or empty bundle")
    names = index["archives"]
    if (not names or len(set(names)) != len(names)
            or any(not isinstance(n, str) or not n or n in (".", "..")
                   or "/" in n or "\\" in n or ":" in n for n in names)):
        raise ValueError("unsafe archive names")
    total = 0
    with zipfile.ZipFile(archive_path) as source:
        members = source.infolist()
        if (len(members) != len(index["entries"])
                or {p.filename for p in members} != set(index["entries"])):
            raise ValueError("bundle inventory mismatch")
        for info in members:
            p = member_path(info.filename)
            expected = index["entries"][info.filename]
            total += info.file_size
            if (p.parts[0] not in names or info.is_dir()
                    or stat.S_ISLNK(info.external_attr >> 16)
                    or info.file_size != expected["size"]
                    or info.file_size > 50*1024**2 or total > 1024**3):
                raise ValueError("invalid member type, size or root")
            if digest(source.read(info)) != expected["sha256"]:
                raise ValueError("member checksum mismatch")
    if {member_path(n).parts[0] for n in index["entries"]} != set(names):
        raise ValueError("empty or missing archive root")
    return index


def extract(prefix, output):
    """Validate all bytes before writing; refuse any existing archive destination.

    An I/O failure can leave new partial directories. They are not treated as
    complete; originals are never overwritten. Retry into a fresh output root.
    """
    index = validate(prefix)
    output = Path(output).resolve()
    for name in index["archives"]:
        if (output / name).exists() or (output / name).is_symlink():
            raise FileExistsError(f"archive destination exists: {name}")
    output.mkdir(parents=True, exist_ok=True)
    # Reserve each destination exclusively before extracting any file.
    for name in index["archives"]:
        (output / name).mkdir(exist_ok=False)
    with zipfile.ZipFile(Path(prefix).with_suffix(".zip")) as source:
        for name in index["entries"]:
            target = output.joinpath(*member_path(name).parts)
            if output not in target.resolve().parents:
                raise ValueError("destination escaped output root")
            target.parent.mkdir(parents=True, exist_ok=True)
            data = source.read(name)
            if digest(data) != index["entries"][name]["sha256"]:
                raise ValueError("bundle changed during extraction")
            with target.open("xb") as stream:
                stream.write(data)
    return dict(extracted=len(index["entries"]), archives=index["archives"],
                producer_manifests_changed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("build", "verify", "extract"))
    parser.add_argument("--bundle", type=Path, default=DEFAULT)
    parser.add_argument("--source-root", type=Path, default=ROOT / "results/journal_sprint")
    parser.add_argument("--output", type=Path, default=ROOT / "results/journal_sprint")
    args = parser.parse_args()
    if args.action == "build":
        result = build(args.source_root, args.bundle)
    elif args.action == "extract":
        result = extract(args.bundle, args.output)
    else:
        index = validate(args.bundle)
        result = dict(verified=True, files=len(index["entries"]), archives=index["archives"])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
