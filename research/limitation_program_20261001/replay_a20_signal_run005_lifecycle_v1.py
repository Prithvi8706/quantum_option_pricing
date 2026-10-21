"""Prospective shared OPERATIONAL receipt machinery only; no science on import."""

from __future__ import annotations

import argparse
import ast
import copy as ast_copy
from collections import Counter  # noqa: F401 -- retain exact V6 metadata namespace AST
import ctypes
from ctypes import wintypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
CPU, WORK, WALL = 180, 150, 600
V5_AUTHOR_NAMES = (
    "arithmetic_free_basket_signal_v5.py",
    "a20_signal_receipt_v5.py",
    "experiment_arithmetic_free_basket_signal_v5.py",
    "audit_arithmetic_free_basket_signal_v5.py",
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V5.md",
    "a20_comparator_phase_implementation_preflight_v5.json",
)
V6_AUTHOR_NAMES = (
    "experiment_arithmetic_free_basket_signal_v6.py",
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V6.md",
    "a20_comparator_phase_implementation_preflight_v6.json",
)
AUTHOR_NAMES = V5_AUTHOR_NAMES + V6_AUTHOR_NAMES
MAX_REFERENCES = 100000
_LEXICAL_PARTS_CACHE = {}
LIFECYCLE_FUNCTION_COUNTS = {
    "admit_v4_hold_and_external_history": 2,
    "admit_packet": 1,
    "canonical": 5,
    "add": 1,
    "read_bytes": 1,
    "owner_memberships": 1,
    "inventory": 2,
    "runtime_paths": 13,
    "verify_loaded": 1,
    "reserve_owned": 1,
    "write": 1,
    "admit_run": 1,
}


V6_READY = ROOT / ".context/A20_signal_producer_ROOT_READY_run005.json"
V5_READY = ROOT / ".context/A20_signal_producer_ROOT_READY_run004.json"
V5_READY_SHA = "d5f65f8f710882783f042f070c161abebd15b44e5142f4e0baf3883a81498284"
V5_FAILED = PROGRAM / "A20_signal_semantics_run004"
V5_FREEZE = ROOT / ".context/A20_signal_run004_FAILED_OWNED_FROZEN_run001.json"
V5_FREEZE_SHA = "130f5e83d4ddb4a03a5921dfed47d86596795e2b82b97b1a0595238fb4179eb3"
V5_PROTOCOL_SHA = "5b30e876fb4c39144001812dab74c874804f53420c49a6946edd5605972a318e"
V5_LOG = ROOT / ".context/a20_signal_run004.log"
V5_LOG_SHA = "35528e1d08ae389768bb89c4c714e610e139cffe5814dedcb47ddebefb672e13"
V5_FAILURE_MARKER_SHA = "3aa5ecb0bd421846bc945790f0e6a0621b2f87d7c325e328768d14db30869322"
PROFILE_SOURCE = RESEARCH / "profile_a20_signal_run004_metadata_v2.py"
PROFILE_SOURCE_SHA = "d98a2a52a25b8d7ba98ca2307d5003d659186b3195e9dc12dc7f610f7830c7c4"
LIFECYCLE_INVERSE_AST_SHA = "d12c2827803d450f9077e71083f560b146d73eb9a6931fb28031e6be9b5277e2"
V5_EXECUTE_AST_SHA = "9b5cbe9601231c0a7b434ee34275ee47ecd1463187e8d3f35783b8666f83adba"
PAIR_ROOT_WITNESS = (
    ROOT / ".context/A20_SIGNAL_METADATA_PROFILE_V2_COMPLETED_PAIR_ROOT_VERIFICATION_run001.json"
)
PAIR_ROOT_WITNESS_SHA = "fea813097cd0a48dd542f2cd16610a92446791385b3138f5c05e878e8a481048"
V5_AUTHOR_PINS = {
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V5.md": (
        "4d98b1d5f1042f53c069c61b5bffac4a17333dc64afb9a7b0133d5e8cd010458"
    ),
    "a20_comparator_phase_implementation_preflight_v5.json": (
        "095a108aa9e0beb293eaf0067d2d3a193c60983344b6b4d3cba4ec5c14738445"
    ),
    "a20_signal_receipt_v5.py": "c130a7eed0688faba014a36300bc01c6eadf162426b1f2a6e911096aa9a1fd8c",
    "arithmetic_free_basket_signal_v5.py": (
        "98a6fe0295e71da76ef6499ae52193cf00f86c120aa63d44edfd8b70e24551f5"
    ),
    "audit_arithmetic_free_basket_signal_v5.py": (
        "e1b63dcb68250763d545a6f0b3074ddce31b1221c839b8df0d4831ff7a507a67"
    ),
    "experiment_arithmetic_free_basket_signal_v5.py": (
        "586b9b3e021b90a819b0b3efa8907c473b9054eb60bdf65305a4a7db40d471bc"
    ),
}
PRIOR_PROFILE_REFERENCES = {
    "OLD": {
        "output": (
            "results/limitation_program_20261001/A20_signal_run004_metadata_profile_old_run001"
        ),
        "owned_freeze_path": (
            ".context/A20_SIGNAL_OLD_METADATA_PROFILE_FAILED_OWNED_FROZEN_run001.json"
        ),
        "owned_freeze_SHA256": "f8aaa9750b27741e0bb33e29be1f0078902e409cd0ad6b9a7117962cf4279f42",
        "owned_freeze_schema": "root-a20-old-metadata-profile-failed-owned-freeze-v1",
        "owned_count": 9,
        "READY_path": ".context/A20_signal_run004_METADATA_PROFILE_OLD_ROOT_READY_run001.json",
        "READY_SHA256": "704ed9de48c63bfbfb5fd8aaa58c49f587ccdb530af814c663a680cde6823b55",
        "log_path": ".context/a20_signal_metadata_profile_old_run001.log",
        "log_SHA256": "e28649b8f7d24ac810e3bbfe2767ae2344dbd62e68b5cce071ad6dd244ce68a8",
        "marker_SHA256": "2157d817aa2725fd1aa22ad0a3b1f3a7099578045cca514fb5dc808768025033",
        "observed_measured_status_key": "completed_measured_union",
        "completed_measured_union": False,
        "failure_stage": (
            "measured_union/context.digest/Receipt.check Fixed A20 process CPU/wall guard"
        ),
        "all_saved_observations_unapproved": True,
    },
    "OPT": {
        "output": (
            "results/limitation_program_20261001/A20_signal_run004_metadata_profile_opt_run002"
        ),
        "owned_freeze_path": (
            ".context/A20_SIGNAL_OPT_METADATA_PROFILE_FAILED_OWNED_FROZEN_run002.json"
        ),
        "owned_freeze_SHA256": "43e18e8f704e1c6e65184efe8cf92f9c237e7f2164c7b12db9a7448d0e29cd5e",
        "owned_freeze_schema": "root-a20-opt-metadata-profile-failed-owned-freeze-v1",
        "owned_count": 11,
        "READY_path": ".context/A20_signal_run004_METADATA_PROFILE_OPT_ROOT_READY_run002.json",
        "READY_SHA256": "3cd1dfd62c4b5b3a87805b19af2a2a376630740c0ea8148601f08ed7fd84272c",
        "log_path": ".context/a20_signal_metadata_profile_opt_run002.log",
        "log_SHA256": "eb9c50c3c1626b999b4052af7b00f3ae7ffc9b4db2e58ec1f02f0a4eb362a7e2",
        "marker_SHA256": "2157d817aa2725fd1aa22ad0a3b1f3a7099578045cca514fb5dc808768025033",
        "observed_measured_status_key": "completed_measured_union_observed_not_approved",
        "completed_measured_union": True,
        "failure_stage": "second full fresh integrity union / Process CPU guard",
        "all_saved_observations_unapproved": True,
    },
}
COMPLETED_METADATA_PACKETS = [
    [
        "A20_signal_run004_terminal_failure_capture_run001",
        "943669cfd00806e16aac728f452bf4a7addadb98da03095dc1ed90daf81dfdc0",
        [15, 5975, 2842],
        "a20-run004-failure-capture-manifest-v1",
    ],
    [
        "A20_signal_run004_metadata_profile_old_run003",
        "6439dcfe9838c80d8326d288db0fe9229200fdb0234e83452d07693c9fb8bb93",
        [14, 6024, 2842],
        "a20-run004-metadata-profile-manifest-v2",
    ],
    [
        "A20_signal_run004_metadata_profile_opt_run004",
        "451876d96b3dd3aa0899d986f6fb04745ed662c456ebba18684f37ee9bb9a34b",
        [14, 6024, 2842],
        "a20-run004-metadata-profile-manifest-v2",
    ],
]
HISTORY_READY_CACHE_DECLARATIONS = [
    [
        ".context/A20_signal_run004_FAILURE_CAPTURE_ROOT_READY_run001.json",
        "4a073df214072745d88429b998f3c654f801226e5666ce03e0d3ba6dbbf63069",
        "capture_a20_signal_run004_failure_v1.py",
    ],
    [
        ".context/A20_signal_run004_METADATA_PROFILE_OLD_ROOT_READY_run001.json",
        "704ed9de48c63bfbfb5fd8aaa58c49f587ccdb530af814c663a680cde6823b55",
        "profile_a20_signal_run004_metadata_v1.py",
    ],
    [
        ".context/A20_signal_run004_METADATA_PROFILE_OPT_ROOT_READY_run002.json",
        "3cd1dfd62c4b5b3a87805b19af2a2a376630740c0ea8148601f08ed7fd84272c",
        "profile_a20_signal_run004_metadata_v1.py",
    ],
    [
        ".context/A20_signal_run004_METADATA_PROFILE_OLD_ROOT_READY_run003.json",
        "d662663ca124933b36d39c7b53347f8060f0493927685a426178306307ed312b",
        "profile_a20_signal_run004_metadata_v2.py",
    ],
    [
        ".context/A20_signal_run004_METADATA_PROFILE_OPT_ROOT_READY_run004.json",
        "9c47971ae0718ec56ca90e2f8f1889db5de599df68b34c16eff80a39459224c3",
        "profile_a20_signal_run004_metadata_v2.py",
    ],
]
LEXICAL_HELPER_AND_CORPUS_AST_SHA = (
    "7aba01b1e19f978e81b1fac021582462947bed447a5d5fe2f2d0a7a8f0b622ef"
)

ORIGINAL_PINS = {
    "A20_ARITHMETIC_FREE_LOADING_PROSPECTUS.md": (
        "19f08143e9be0aadac7f88f15a344ad9218ad359877c9e52aa6fc99715b5b291"
    ),
    "a20_arithmetic_free_loading_prospectus.json": (
        "c3d9b9301463069afe0813f726131f9f2af4a5ec0b7a7e5bf8c18950aae1f3f0"
    ),
}
HISTORICAL_V2_PINS = {
    "research/limitation_program_20261001/arithmetic_free_basket_signal_v2.py": (
        "4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a"
    ),
    "research/limitation_program_20261001/a20_signal_receipt_v2.py": (
        "25fcef657d3699a54f5ee7daf0783ccf5948359604dd10e293b545739f2498bd"
    ),
    "research/limitation_program_20261001/experiment_arithmetic_free_basket_signal_v2.py": (
        "ca96c32e9d53e49da5e24b5d96df017d4f65b7ab913a3b74441d3e6d8645f4ed"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_v2.py": (
        "64327303b9658ecb920829241b1df9c42120773a2b3df3747e6d97af1ffd3c7d"
    ),
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "3efd3f0850348f4a0c8759de84fca3632f029cca81c49e5689cb7f74512d4546"
    ),
    "research/limitation_program_20261001/a20_comparator_phase_implementation_preflight_v2.json": (
        "66eb828afe1ce31ff4b9d0be97f7ef889f9c9cc696ee7372ce2193fae507bbb5"
    ),
    ".context/A20_signal_producer_ROOT_READY_run001.json": (
        "08af3d467e1f9e235eb38943b4875999104ec110e92ab5a97cc7a15cb9beb4af"
    ),
    ".context/a20_signal_prepare_run001.log": (
        "6bbcb3b3bebc40221d3cef2b99b2d453090b4e34ae1f07b4bcd2bc511b5da394"
    ),
}
HISTORICAL_V2_ABSENT_ROUTES = (
    "A20_signal_semantics_run001",
    "A20_signal_semantics_audit_run001",
)
HISTORICAL_V3_PINS = {
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "2a75285047b52ec7a1a9717e047c5c45419c6bc14acc4e5d32e57cd50cbfa7ee"
    ),
    "research/limitation_program_20261001/a20_comparator_phase_implementation_preflight_v3.json": (
        "694ad7f6e1aca0346938c43a83bfd721b669d7787edf3d1f6c1814f292f3b36c"
    ),
    "research/limitation_program_20261001/a20_signal_receipt_v3.py": (
        "79e70710f9c742fda57dff73704b66f791ee7905a88b0ab0128a2054aaebd6f2"
    ),
    "research/limitation_program_20261001/arithmetic_free_basket_signal_v3.py": (
        "4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_v3.py": (
        "5d0babd08382923458dd303309777085163e917b3c41e74ebae6c48c5762e187"
    ),
    "research/limitation_program_20261001/experiment_arithmetic_free_basket_signal_v3.py": (
        "eb7b523da38975278cd7e5d5c1a0993d67f04cc8b056f1897c5b1d08e9d9af62"
    ),
    ".context/A20_signal_producer_ROOT_READY_run002.json": (
        "fceee79c50b097a4de6da9ab67f450dac1f77431d447972d71214b869befd6ae"
    ),
    ".context/a20_signal_prepare_run002.log": (
        "2394d1e4b659b9c8cf10638e557460de1a01b290694af1919c25eb8145539ff2"
    ),
}
HISTORICAL_V3_ABSENT_ROUTES = (
    "A20_signal_semantics_run002",
    "A20_signal_semantics_audit_run002",
)
HELD_V4_AUTHOR_PINS = {
    "research/limitation_program_20261001/arithmetic_free_basket_signal_v4.py": (
        "4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a"
    ),
    "research/limitation_program_20261001/a20_signal_receipt_v4.py": (
        "81b3002343dce65736ff3d46df00e871464d29124675e3632ed967a5a6556b50"
    ),
    "research/limitation_program_20261001/experiment_arithmetic_free_basket_signal_v4.py": (
        "5730ca2a353c5beffbacd01c0f7e28fa6944fb4570d16d1bfc9fdcb2c3474344"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_v4.py": (
        "f4ab02ce6119e433564bcdf915c82a48f30a57aa0cc6f89ca02c9043a7b3d625"
    ),
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V4.md": (
        "bd4aec08b82a4474e96f0e33b21d812d1186d4fbdecb490aa8550f87696f7bbb"
    ),
    "research/limitation_program_20261001/a20_comparator_phase_implementation_preflight_v4.json": (
        "0f8d6efc2df7168b86d3679981211de7238443b29444d0c59aaca9481623ed01"
    ),
}
OTHER_AGENT_STATIC_TEXT_PINS = {
    "research/limitation_program_20261001/arithmetic_free_basket_signal_continuation_v6.py": (
        "d2f8361086ba411415d0527fe96870b61b39c77b77f989b1d3b9abf67121661b"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_continuation_v6.py": (
        "cb526bebdec30e71a05c155b03f343320cec00d33e9b47945fb51a4084469f3b"
    ),
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V6.md": (
        "4847562140646b95d702a9d820b523cb083e984dcb5264f921d8aff59d825c84"
    ),
    "docs/limitation_program_20261001/continuation_20261004/A14/A20_COMMUTATIVITY_REVIEW_v5.md": (
        "cc141ffe56e5666f1b8a303e3171653feda577922b237cfb23493aa241c88b57"
    ),
    (
        "docs/limitation_program_20261001/continuation_20261004/A13/"
        "A20_V5_ORDERED_COST_BOUNDARY_SUPPLEMENT.md"
    ): ("c7a326a02752306d6a61ae821351298ef083070cd6d73fbc2540848fadd6596c"),
    (
        "research/limitation_program_20261001/continuation_20261004/A14/"
        "A20_MUL_METADATA_REVIEW_v5b.json"
    ): ("0e3f461b75a069580aff670110f9269165b5a709e4c59e4b0061c699462f67d7"),
    (
        "research/limitation_program_20261001/continuation_20261004/A14/"
        "A20_V6_INDEPENDENT_STATIC_REVIEW_run001.json"
    ): ("fe09d4de4c97f53bcbeeb6bf771226e7c4914aec73eefb00e0c7c197bf384a68"),
    "docs/limitation_program_20261001/continuation_20261004/A20_V6_OPERATIONAL_ERRATUM.md": (
        "450993fc8b8922d43a989acb34960377abacc1393e758c152353ccc58f36a005"
    ),
}
EXTERNAL_HISTORY_MANIFEST_PINS = {
    "results/limitation_program_20261001/A20_continuation_20261004_failure_capture_run001": (
        "512a5418c01a4841de7457692bf98052f8c501475b2d4ae0be51badd3a3531ad"
    ),
    "results/limitation_program_20261001/A20_continuation_20261004_template_diagnostic_run001": (
        "5935f7871819a283dd395a6b09b6bd4cd4f40860d9d57aba95336bf901532d19"
    ),
    (
        "results/limitation_program_20261001/"
        "A20_continuation_20261004_ROOT_template_integrity_run001"
    ): ("07825749932b1ea9c760b26ba8b09682bd1c73bdc6ecacbcaf8628793fb73cf4"),
}
INTERPRETER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
SHA = re.compile(r"[0-9a-f]{64}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


LEXICAL_PATHS = (
    ".",
    "foo",
    "foo/bar",
    "foo/../bar",
    "../foo",
    "C:",
    "C:foo",
    "C:/",
    "C:/foo",
    "c:/FOO/bar",
    "C:/foobar",
    "D:/foo",
    "//server/share/",
    "//server/share/foo",
    "/foo",
    "C:/Straße/x",
    "C:/STRASSE/x",
    "C:/foo/../bar",
    "C:/İ/x",
    "C:/i̇/x",
    "C:/ΟΣ/x",
    "C:/ος/x",
    "C:Σ",
    "C:σ",
    "C:ς",
)

LEXICAL_PARENTS = (
    ".",
    "foo",
    "foo/..",
    "..",
    "C:",
    "C:/",
    "c:/foo",
    "C:/foobar",
    "D:/",
    "//server/share/",
    "/foo",
    "C:/STRASSE",
    "C:/İ",
    "C:/ΟΣ",
    "C:Σ",
    "C:σ",
    "C:ς",
)


def lexical_parts(path):
    """Immutable Windows syntax only; never a physical-resolution cache."""
    require(isinstance(path, (Path, PureWindowsPath)), "Only Windows path objects")
    key = str(path)
    if key not in _LEXICAL_PARTS_CACHE:
        require(len(_LEXICAL_PARTS_CACHE) < MAX_REFERENCES, "Bounded lexical syntax cache")
        _LEXICAL_PARTS_CACHE[key] = (
            path.anchor.lower(),
            tuple((part.lower() for part in path.parts)),
        )
    return _LEXICAL_PARTS_CACHE[key]


def lexically_under(path, parent):
    """Exact Path.is_relative_to syntax predicate; aliases still resolve separately."""
    if path.drive and (not path.root) or (parent.drive and (not parent.root)):
        return path.is_relative_to(parent)
    anchor, parts = lexical_parts(path)
    root_anchor, root_parts = lexical_parts(parent)
    return (
        anchor == root_anchor
        and len(parts) >= len(root_parts)
        and (parts[: len(root_parts)] == root_parts)
    )


class Receipt:
    def __init__(self, role, ready_path, ready_sha, mode):
        require(role == "producer" and mode in ("prepare", "run"), "Fixed A20 role/mode")
        self.role, self.mode = role, mode
        self.output = PROGRAM / (
            "A20_signal_semantics_run005"
            if role == "producer"
            else "A20_signal_semantics_audit_run005"
        )
        self.started = self.creation_clock()
        self.frozen, self.external, self.observed, self.cache, self.physical = {}, {}, {}, {}, {}
        self.hash_work, self.references, self.mutated = 0, 0, False
        self.runtime_absent = []
        self.source_packets = []
        self.history_absent = set()
        self.history_present_caches = {}
        self.old_live_snapshot_witnesses = []
        self.recovery_history = None
        self.lexical_guard = None
        self.failed_history_packets = []
        self.owned_usage = None
        self.owned_expected = set()
        self.base = Path(os.path.abspath(sys.base_prefix))
        self.excluded = self.base / "Lib/site-packages"
        self.check()
        require(self.base.resolve(strict=True) == self.base, "Exact base runtime path")
        self.excluded_actual = self.excluded.resolve(strict=False)
        require(
            sys.version_info[:2] == (3, 12) and sys.dont_write_bytecode,
            "Pinned Python3.12 -B before module import",
        )
        require(
            Path(sys.executable).resolve(strict=True) == INTERPRETER,
            "Pinned isolated research interpreter",
        )
        require(Path.cwd().resolve(strict=True) == ROOT, "Fixed ROOT working directory")
        require(
            all(
                not os.environ.get(name) for name in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")
            ),
            "No inherited external runtime overrides",
        )
        self.import_policy()
        self.ready_path = Path(ready_path)
        self.add(self.ready_path, ready_sha)
        self.ready = self.read(self.ready_path)
        require(
            self.canonical(self.ready_path) == V6_READY,
            "Exact new producer-only V6 ROOT release route",
        )
        require(
            self.ready["schema"] == "A20-comparator-phase-static-READY-v6"
            and self.ready["ready"] is True
            and self.ready["role"] == role,
            "Actual role-specific ROOT READY",
        )
        require(
            self.ready["budget"] == [CPU, WORK, WALL]
            and self.ready["science_executed_during_authoring"] is False,
            "Prospective fixed budgets and author scope",
        )
        require(
            self.ready["output"] == self.output.relative_to(ROOT).as_posix(),
            "Exact fresh fixed receipt",
        )
        self.add(INTERPRETER, self.ready["interpreter_sha256"])
        base_interpreter = self.canonical(Path(sys._base_executable))
        require(
            base_interpreter == self.base / "python.exe",
            "Exact base-prefix interpreter behind the pinned launcher",
        )
        self.add(base_interpreter, self.ready["base_interpreter_sha256"])
        authors = self.ready["author_sha256"]
        require(
            set(authors)
            == {str((RESEARCH / name).relative_to(ROOT).as_posix()) for name in AUTHOR_NAMES},
            "Exactly new V6 trio plus all six immutable V5 dependencies pinned",
        )
        for key, expected in authors.items():
            self.add(ROOT / key, expected)
        require(
            all(
                authors[(RESEARCH / name).relative_to(ROOT).as_posix()] == pin
                for name, pin in V5_AUTHOR_PINS.items()
            ),
            "All original V5 author expectations remain unchanged",
        )
        self.admit_v2_history()
        self.admit_v3_history()
        self.admit_v4_hold_and_external_history()
        for name, expected in ORIGINAL_PINS.items():
            self.add(RESEARCH / name, expected)
        old = self.read(RESEARCH / "a20_arithmetic_free_loading_prospectus.json")
        selected = self.ready["selected_prerequisite_sha256"]
        require(
            all(
                selected.get(key) == expected
                for key, expected in old["selected_original_expected_sha256"].items()
            ),
            "Original selected expected SHA never replaced",
        )
        for key, expected in selected.items():
            require(
                (ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical selected ROOT spelling"
            )
            self.add(ROOT / key, expected)
        memberships = self.owner_memberships(self.ready["selected_owner_manifest_sha256"])
        require(
            all(
                (key, expected) in memberships
                for key, expected in selected.items()
                if not key.endswith("/manifest.json")
            ),
            "Every selected premise has exact sealed owner membership",
        )
        self.admit_recovery_history()
        self.lexical_guard = self.operational_ast_guard()
        self.verify()

    def recovery_path(self, key):
        require(type(key) is str, "Exact recovery input spelling")
        path = Path(key)
        if path.is_absolute():
            require(str(path) == key, "Original exact absolute runtime spelling")
            return path
        require(
            "\\" not in key
            and ".." not in path.parts
            and (ROOT / key).relative_to(ROOT).as_posix() == key,
            "Original exact ROOT-relative spelling",
        )
        return ROOT / key

    def history_owned(self, directory, mapping):
        require(type(mapping) is dict, "Complete fixed historical owned map")
        members = set()
        for key, expected in mapping.items():
            self.check()
            require(
                type(key) is str
                and "\\" not in key
                and not Path(key).is_absolute()
                and ".." not in Path(key).parts,
                "Strict receipt-relative historical owned spelling",
            )
            member = self.add(directory / key, expected)
            require(
                lexically_under(member, directory)
                and member.relative_to(directory).as_posix() == key
                and member not in members,
                "Unique complete physically confined historical owned member",
            )
            members.add(member)
        return members

    def complete_metadata_packet(self, name, pin, counts, schema):
        directory = PROGRAM / name
        manifest = self.add(directory / "manifest.json", pin)
        data = self.read(manifest)
        require(
            data["schema"] == schema
            and data["passed"] is True
            and data["completed"] is True
            and data["budget_censored"] is False
            and data["manifest_self_hash_excluded"] is True
            and data["metadata_integrity_only"] is True
            and data["original_scientific_attempt_passed"] is False
            and data["original_failed_unsealed_authoritative"] is True
            and data["new_test_credit"] == 0
            and data["adoption"] is False
            and data["full_G2"] is False
            and data["cost_transfer"] is False
            and data["quantum_advantage"] is False,
            "Completed metadata diagnostic supplies no old scientific or financial approval",
        )
        require(
            [len(data[field]) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
            == counts,
            "All externally fixed complete metadata owner-map counts",
        )
        owned = self.history_owned(directory, data["files"])
        require(manifest not in owned, "Metadata manifest self excluded")
        members = owned | {manifest}
        require(self.inventory(directory) == members, "Complete actual metadata owner inventory")
        self.source_packets.append((directory, members))
        for field in ("frozen_inputs", "external_runtime_inputs"):
            require(type(data[field]) is dict, "Complete historical expected input map")
            for key, expected in data[field].items():
                self.check()
                require(
                    (field == "frozen_inputs" and not Path(key).is_absolute())
                    or (field == "external_runtime_inputs" and Path(key).is_absolute()),
                    "Original field-specific relative versus absolute spelling",
                )
                path = self.recovery_path(key)
                actual = self.add(path, expected)
                require(
                    (
                        field == "frozen_inputs"
                        and lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key
                    )
                    or (
                        field == "external_runtime_inputs"
                        and not lexically_under(actual, ROOT)
                        and str(actual) == key
                    ),
                    "Literal frozen ROOT versus external absolute owner-map contract",
                )
        return data

    def history_cache_declaration(self, source, data):
        self.check()
        cache = Path(importlib.util.cache_from_source(str(source)))
        key = cache.relative_to(ROOT).as_posix()
        present = {key} if cache.exists() else set()
        pins = data["existing_new_code_cache_SHA256"]
        absent = data["absent_new_code_cache_paths"]
        require(
            type(pins) is dict
            and set(pins) == present
            and type(absent) is list
            and absent == sorted({key} - present),
            "Exact inherited ROOT cache presence and absence declaration",
        )
        for spelling, expected in pins.items():
            actual = self.add(ROOT / spelling, expected)
            require(actual == cache, "Exact declared historical cache path")
            require(
                actual not in self.history_present_caches
                or self.history_present_caches[actual] == expected,
                "Equal-SHA inherited cache declarations",
            )
            self.history_present_caches[actual] = expected
        for spelling in absent:
            path = ROOT / spelling
            require(
                path == cache
                and not path.exists()
                and not path.is_symlink()
                and path.resolve(strict=False) == path,
                "Exact physically absent inherited cache path",
            )
            self.history_absent.add(path)

    def admit_recovery_history(self):
        policy = self.read(RESEARCH / V6_AUTHOR_NAMES[2])
        require(
            policy["schema"] == "A20-comparator-phase-operational-recovery-preflight-v6"
            and self.ready["root_and_independent_static_reviews_passed"] is True
            and self.ready["operational_syntax_transfer_and_scientific_retry_reviewed"] is True
            and self.ready["completed_metadata_packets"]
            == policy["completed_metadata_packets"]
            == COMPLETED_METADATA_PACKETS
            and self.ready["pair_ROOT_metadata_witness_SHA256"]
            == policy["pair_ROOT_metadata_witness_SHA256"]
            == PAIR_ROOT_WITNESS_SHA
            and self.ready["original_failed_owned_freeze_SHA256"]
            == policy["original_failed_owned_freeze_SHA256"]
            == V5_FREEZE_SHA
            and policy["lifecycle_function_counts"] == LIFECYCLE_FUNCTION_COUNTS
            and policy["lifecycle_inverse_AST_SHA256"] == LIFECYCLE_INVERSE_AST_SHA
            and policy["V5_execute_AST_SHA256"] == V5_EXECUTE_AST_SHA
            and policy["V5_author_expected_SHA256"] == V5_AUTHOR_PINS,
            "Separate reviewed new V6 transfer with exact fixed completed metadata premises",
        )
        require(
            all(
                self.ready[key] is False
                for key in (
                    "full_G2",
                    "adoption",
                    "cost_transfer",
                    "quantum_advantage",
                    "complete_financial_source_emission_authorized",
                )
            )
            and self.ready["new_test_credit"] == 0,
            "New restricted component release carries no pricing/adoption/advantage permission",
        )
        for record in COMPLETED_METADATA_PACKETS:
            self.complete_metadata_packet(*record)
        self.add(PROFILE_SOURCE, PROFILE_SOURCE_SHA)
        original_freeze = self.read(self.add(V5_FREEZE, V5_FREEZE_SHA))
        require(
            original_freeze["schema"] == "A20-run004-post-failure-observed-owned-freeze-v1"
            and original_freeze["scope"] == "INTEGRITY_ONLY_FAILED_UNSEALED_NOT_SCIENTIFIC_APPROVAL"
            and original_freeze["source_directory"] == V5_FAILED.relative_to(ROOT).as_posix()
            and original_freeze["owned_files"] == 2945
            and original_freeze["owned_bytes"] == 116156575
            and original_freeze["original_prepared_protocol_expected_sha256"] == V5_PROTOCOL_SHA
            and original_freeze["failure_marker_expected_sha256"] == V5_FAILURE_MARKER_SHA
            and original_freeze["raw_failure_log_expected_sha256"] == V5_LOG_SHA
            and original_freeze["original_prepared_expectations_unchanged"] is True,
            "Complete externally fixed run004 failure scope and original expected release",
        )
        observed = original_freeze["observed_after_authoritative_failure_files"]
        require(
            len(observed) == 2945
            and observed["protocol.json"] == V5_PROTOCOL_SHA
            and observed["FAILED_UNSEALED.json"] == V5_FAILURE_MARKER_SHA
            and "manifest.json" not in observed,
            "All fixed observed failed bytes remain separate from original expectations",
        )
        failed_members = self.history_owned(V5_FAILED, observed)
        require(
            self.inventory(V5_FAILED) == failed_members
            and sum(self.stamp(path)[2] for path in failed_members) == 116156575,
            "Exact complete unchanged run004 owned inventory and bytes",
        )
        self.failed_history_packets.append((V5_FAILED, failed_members))
        original_ready = self.read(self.add(V5_READY, V5_READY_SHA))
        require(
            original_ready["schema"] == "A20-comparator-phase-static-READY-v5"
            and original_ready["role"] == "producer"
            and original_ready["budget"] == [CPU, WORK, WALL]
            and original_ready["author_sha256"]
            == {
                (RESEARCH / name).relative_to(ROOT).as_posix(): pin
                for name, pin in V5_AUTHOR_PINS.items()
            },
            "Original six V5 expectations and producer-only release preserved as failed history",
        )
        self.add(V5_LOG, V5_LOG_SHA)
        old_protocol = self.read(V5_FAILED / "protocol.json")
        require(
            old_protocol["schema"] == "A20-comparator-phase-prepared-protocol-v5"
            and old_protocol["root_READY_sha256"] == V5_READY_SHA
            and old_protocol["budget"] == [CPU, WORK, WALL]
            and [
                len(old_protocol[field])
                for field in (
                    "frozen_inputs",
                    "external_runtime_inputs",
                    "prepared_owned_files_protocol_self_hash_excluded",
                )
            ]
            == [5950, 2842, 2932],
            "Exact complete original prepared expected maps retained without replacement",
        )
        for key, expected in old_protocol[
            "prepared_owned_files_protocol_self_hash_excluded"
        ].items():
            self.check()
            require(
                key != "protocol.json" and observed.get(key) == expected,
                "Every original prepared-owned expectation remains identical",
            )
        for field in ("frozen_inputs", "external_runtime_inputs"):
            for key, expected in old_protocol[field].items():
                self.check()
                require(
                    (field == "frozen_inputs" and not Path(key).is_absolute())
                    or (field == "external_runtime_inputs" and Path(key).is_absolute()),
                    "All original prepared input keys retain their literal field contract",
                )
                actual = self.add(self.recovery_path(key), expected)
                require(
                    (
                        field == "frozen_inputs"
                        and lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key
                    )
                    or (
                        field == "external_runtime_inputs"
                        and not lexically_under(actual, ROOT)
                        and str(actual) == key
                    ),
                    "Original prepared ROOT-relative and absolute expectations are exact",
                )
        for spelling in old_protocol["runtime_absent"]:
            path = Path(spelling)
            require(
                path.is_absolute() and str(path) == spelling,
                "Exact original runtime absence spelling",
            )
            self.history_absent.add(path)
        runtime_paths = old_protocol["runtime_paths"]
        copies = old_protocol["runtime_live_to_snapshot"]
        require(
            len(runtime_paths) == 2892
            and len(set(runtime_paths)) == 2892
            and set(copies) == set(runtime_paths),
            "All original live runtime and snapshot witnesses retained",
        )
        for mapping in (
            copies,
            old_protocol["immutable_V2_history_live_to_snapshot"],
            old_protocol["immutable_V3_history_live_to_snapshot"],
            old_protocol["held_V4_live_to_snapshot"],
            old_protocol["other_agent_static_text_live_to_snapshot"],
        ):
            for live, saved in mapping.items():
                self.check()
                path, snapshot = self.recovery_path(live), self.recovery_path(saved)
                require(lexically_under(snapshot, V5_FAILED), "Original snapshot remains confined")
                key = (
                    path.relative_to(ROOT).as_posix() if lexically_under(path, ROOT) else str(path)
                )
                expected = (
                    old_protocol["frozen_inputs"].get(key)
                    if lexically_under(path, ROOT)
                    else old_protocol["external_runtime_inputs"].get(key)
                )
                require(
                    expected is not None
                    and observed.get(snapshot.relative_to(V5_FAILED).as_posix()) == expected,
                    "Original live and snapshot expectations remain equal, "
                    "never observed substitutions",
                )
                self.old_live_snapshot_witnesses.append((path, snapshot, expected))
        marker = self.read(V5_FAILED / "FAILED_UNSEALED.json")
        require(
            marker["passed"] is False
            and marker["authoritative_failure"] is True
            and marker["budget_censored"] is None
            and marker["hard_budget_state_uncertified"] is True
            and marker["new_test_credit"] == 0
            and marker["adoption"] is False,
            "Run004 remains authoritative failure with uncertified terminal clocks",
        )
        for mode in ("OLD", "OPT"):
            reference = PRIOR_PROFILE_REFERENCES[mode]
            freeze = self.read(
                self.add(ROOT / reference["owned_freeze_path"], reference["owned_freeze_SHA256"])
            )
            require(
                freeze["schema"] == reference["owned_freeze_schema"]
                and freeze["failed_route"] == reference["output"]
                and freeze["failure_stage"] == reference["failure_stage"]
                and freeze["original_READY_expected_sha256"] == reference["READY_SHA256"]
                and freeze["original_failure_log_sha256"] == reference["log_SHA256"]
                and freeze[reference["observed_measured_status_key"]]
                is reference["completed_measured_union"]
                and freeze["passed"] is False
                and freeze["new_fixture_credit"] == 0
                and freeze["original_scientific_run_passed"] is False
                and freeze["original_terminal_CPU_wall_uncertified"] is True,
                "Both original V1 profiles remain failed without ratios or scientific approval",
            )
            directory = ROOT / reference["output"]
            mapping = freeze["observed_owned_files"]
            require(
                len(mapping) == reference["owned_count"]
                and "manifest.json" not in mapping
                and mapping["FAILED_UNSEALED.json"] == reference["marker_SHA256"],
                "Complete original nine/eleven failed-owned profile maps",
            )
            members = self.history_owned(directory, mapping)
            require(
                self.inventory(directory) == members, "Complete actual failed profile inventory"
            )
            self.failed_history_packets.append((directory, members))
            self.add(ROOT / reference["READY_path"], reference["READY_SHA256"])
            self.add(ROOT / reference["log_path"], reference["log_SHA256"])
        for key, expected, name in HISTORY_READY_CACHE_DECLARATIONS:
            data = self.read(self.add(ROOT / key, expected))
            self.history_cache_declaration(RESEARCH / name, data)
        pair = self.read(self.add(PAIR_ROOT_WITNESS, PAIR_ROOT_WITNESS_SHA))
        require(
            pair["schema"] == "root-a20-v2-completed-pair-verification-v1"
            and pair["passed"] is True
            and pair["original_science_passed"] is False
            and pair["scientific_retry_authorized"] is False
            and pair["quantum_advantage"] is False
            and pair["fixture_credit"] == 0
            and pair["new_full_input_union_performed_by_ROOT"] is False
            and pair["single_sequential_pair_not_statistical_timing_claim"] is True
            and pair["source_packets_each_record_two_complete_fresh_unions"] is True
            and pair["packets"]
            == [
                {
                    "route": name,
                    "manifest_SHA256": pin,
                    "counts": counts,
                    "owned_inclusive_verified": counts[0] + 1,
                }
                for name, pin, counts, _schema in COMPLETED_METADATA_PACKETS[1:]
            ],
            "ROOT pair witness is scoped metadata comparison, not inherited science permission",
        )
        summaries = [
            self.read(PROGRAM / record[0] / "summary.json")
            for record in COMPLETED_METADATA_PACKETS[1:]
        ]
        require(
            summaries[0]["mode"] == "OLD"
            and summaries[1]["mode"] == "OPT"
            and summaries[0]["ordered_workload_SHA256"]
            == summaries[1]["ordered_workload_SHA256"]
            == pair["workload_SHA256"]
            and summaries[0]["measured_union"]["ordered_result_SHA256"]
            == summaries[1]["measured_union"]["ordered_result_SHA256"]
            == pair["result_SHA256"]
            and all(
                data["measured_union"]["unique_paths"] == 8809
                and data["measured_union"]["unique_bytes"] == 364163396
                and data["measured_union"]["actual_full_SHA_bytes"] == 364163396
                and data["measured_union"]["actual_stat_and_hash_cache_reuse"] is False
                and len(data["two_full_uncached_integrity_unions"]) == 2
                for data in summaries
            ),
            "Completed single pair has the same complete workload/result and fresh obligations",
        )
        self.recovery_history = {
            "schema": "A20-v6-immutable-operational-recovery-history-v1",
            "complete_metadata_packets": COMPLETED_METADATA_PACKETS,
            "original_failed_owned_freeze_SHA256": V5_FREEZE_SHA,
            "original_READY_expected_SHA256": V5_READY_SHA,
            "original_prepared_protocol_expected_SHA256": V5_PROTOCOL_SHA,
            "original_raw_log_expected_SHA256": V5_LOG_SHA,
            "both_V1_failed_profile_references": PRIOR_PROFILE_REFERENCES,
            "pair_ROOT_metadata_witness_SHA256": PAIR_ROOT_WITNESS_SHA,
            "historical_READY_cache_declarations": HISTORY_READY_CACHE_DECLARATIONS,
            "old_science_and_partial_summaries_approved": False,
            "profiles_predicted_science_speedup": False,
            "new_test_credit": 0,
        }
        self.verify_recovery_history()

    def verify_recovery_history(self):
        self.check()
        require(
            not any(
                path.exists() or path.is_symlink() or path.resolve(strict=False) != path
                for path in self.history_absent
            ),
            "All original runtime and inherited metadata cache absences remain physically exact",
        )
        for path, expected in self.history_present_caches.items():
            self.check()
            require(
                self.digest(path, True) == expected, "Every inherited present cache freshly hashed"
            )
        for live, saved, expected in self.old_live_snapshot_witnesses:
            self.check()
            for path in (live, saved):
                actual = self.canonical(path, fresh=True)
                key = (
                    actual.relative_to(ROOT).as_posix()
                    if lexically_under(actual, ROOT)
                    else str(actual)
                )
                mapping = self.frozen if lexically_under(actual, ROOT) else self.external
                require(
                    mapping.get(key) == expected,
                    "All original live/copy expected identities retained",
                )
        for directory, members in self.failed_history_packets:
            self.check()
            require(
                self.inventory(directory) == members
                and (directory / "FAILED_UNSEALED.json").is_file()
                and not (directory / "manifest.json").exists()
                and not (directory / "manifest.json").is_symlink(),
                "Every unchanged original failed inventory remains authoritative and unsealed",
            )
        self.check()

    def operational_ast_guard(self):
        self.check()
        current = ast.parse(self.read_bytes(RESEARCH / V6_AUTHOR_NAMES[0]))
        baseline = ast.parse(self.read_bytes(RESEARCH / "a20_signal_receipt_v5.py"))
        profile = ast.parse(self.read_bytes(PROFILE_SOURCE))

        def methods(module):
            classes = [
                node
                for node in module.body
                if isinstance(node, ast.ClassDef) and node.name == "Receipt"
            ]
            require(len(classes) == 1, "Exactly one admitted operational Receipt class")
            return {
                node.name: node for node in classes[0].body if isinstance(node, ast.FunctionDef)
            }

        original, actual = methods(baseline), methods(current)

        class Inverse(ast.NodeTransformer):
            def __init__(self):
                self.count = 0

            def visit_Call(self, node):
                self.generic_visit(node)
                if isinstance(node.func, ast.Name) and node.func.id == "lexically_under":
                    require(
                        len(node.args) == 2 and not node.keywords,
                        "Only exact lexical adapter inverse",
                    )
                    self.count += 1
                    return ast.copy_location(
                        ast.Call(
                            func=ast.Attribute(
                                value=node.args[0], attr="is_relative_to", ctx=ast.Load()
                            ),
                            args=[node.args[1]],
                            keywords=[],
                        ),
                        node,
                    )
                return node

        records, restored, count = [], [], 0
        for name, fixed_count in LIFECYCLE_FUNCTION_COUNTS.items():
            self.check()
            inverse = Inverse()
            node = inverse.visit(ast_copy.deepcopy(actual[name]))
            require(
                inverse.count == fixed_count
                and ast.dump(node, include_attributes=False)
                == ast.dump(original[name], include_attributes=False),
                "Each original metadata method has only its exact whitelisted syntax substitutions",
            )
            records.append(
                {"method": name, "predicate_count": fixed_count, "inverse_AST_exact": True}
            )
            restored.append(node)
            count += inverse.count
        normalized = hashlib.sha256(
            ast.dump(ast.Module(body=restored, type_ignores=[]), include_attributes=False).encode()
        ).hexdigest()
        require(
            count == 30 and normalized == LIFECYCLE_INVERSE_AST_SHA,
            "Exact original twelve-method inverse AST pin",
        )

        def lexical_ast(module):
            constants = [
                node
                for node in module.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name)
                    and target.id in ("LEXICAL_PATHS", "LEXICAL_PARENTS")
                    for target in node.targets
                )
            ]
            functions = [
                node
                for node in module.body
                if isinstance(node, ast.FunctionDef)
                and node.name in ("lexical_parts", "lexically_under")
            ]
            require(
                len(constants) == 2 and len(functions) == 2,
                "Exact two helpers and fixed syntax corpus",
            )
            return ast.dump(
                ast.Module(body=constants + functions, type_ignores=[]), include_attributes=False
            )

        helper_dump = lexical_ast(current)
        require(
            helper_dump == lexical_ast(profile)
            and hashlib.sha256(helper_dump.encode()).hexdigest()
            == LEXICAL_HELPER_AND_CORPUS_AST_SHA,
            "Same proven helpers, drive-relative fallback and exact 425 corpus literals",
        )
        producer = ast.parse(
            self.read_bytes(RESEARCH / "experiment_arithmetic_free_basket_signal_v5.py")
        )

        def execute_ast(module):
            nodes = [
                node
                for node in module.body
                if isinstance(node, ast.FunctionDef) and node.name == "execute"
            ]
            require(len(nodes) == 1, "Exactly one whole original scientific execution function")
            return ast.dump(nodes[0], include_attributes=False)

        science_dump = execute_ast(current)
        require(
            science_dump == execute_ast(producer)
            and hashlib.sha256(science_dump.encode()).hexdigest() == V5_EXECUTE_AST_SHA,
            "All scientific orchestration, loops, costs and counters remain exact original V5 AST",
        )
        self.check()
        return {
            "schema": "A20-v6-operational-syntax-AST-guard-v1",
            "methods": records,
            "inverse_AST_SHA256": normalized,
            "total_predicates": count,
            "helper_and_corpus_AST_SHA256": LEXICAL_HELPER_AND_CORPUS_AST_SHA,
            "V5_execute_AST_SHA256": V5_EXECUTE_AST_SHA,
            "V5_builder_expected_SHA256": V5_AUTHOR_PINS["arithmetic_free_basket_signal_v5.py"],
            "single_syntax_cache_fixed_bound": MAX_REFERENCES,
            "no_source_module_import_or_AST_execution": True,
            "new_test_credit": 0,
        }

    def lexical_parity(self):
        records = []
        for raw in LEXICAL_PATHS:
            for parent_raw in LEXICAL_PARENTS:
                self.check()
                path, parent = PureWindowsPath(raw), PureWindowsPath(parent_raw)
                expected, actual = path.is_relative_to(parent), lexically_under(path, parent)
                require(actual == expected, "Exact same fixed Windows syntax parity")
                records.append(
                    {"path": raw, "parent": parent_raw, "matches": True, "result": actual}
                )
        require(len(records) == 425, "Exact original 25-by-17 metadata corpus")
        return records

    def admit_v2_history(self):
        """Bind the actual pre-mkdir admission failure without promoting it."""
        for key, expected in HISTORICAL_V2_PINS.items():
            self.add(ROOT / key, expected)
        ready = self.read(ROOT / ".context/A20_signal_producer_ROOT_READY_run001.json")
        require(
            ready["schema"] == "A20-comparator-phase-static-READY-v2"
            and ready["role"] == "producer"
            and ready["ready"] is True
            and ready["budget"] == [CPU, WORK, WALL]
            and ready["output"] == "results/limitation_program_20261001/A20_signal_semantics_run001"
            and ready["author_sha256"]
            == {key: pin for key, pin in HISTORICAL_V2_PINS.items() if key.startswith("research/")},
            "Exact immutable V2 release and six historical expected authors",
        )
        log = self.read_bytes(ROOT / ".context/a20_signal_prepare_run001.log")
        require(
            log.startswith(b"\xef\xbb\xbf")
            and "ValueError: Exact selected owned member spelling" in log.decode("utf-8-sig"),
            "Exact raw UTF8-BOM original admission failure log",
        )
        self.verify_v2_absence()
        policy = self.read(RESEARCH / "a20_comparator_phase_implementation_preflight_v5.json")
        require(
            policy["immutable_V2_admission_history_expected_sha256"] == HISTORICAL_V2_PINS,
            "Prospective V5 method preserves every immutable V2 history pin",
        )
        self.history = {
            "schema": "A20-V2-pre-mkdir-admission-failure-history-v1",
            "historical_expected_sha256": HISTORICAL_V2_PINS,
            "failed_before_receipt_mkdir": True,
            "error": "ValueError: Exact selected owned member spelling",
            "historical_output_routes_absent": list(HISTORICAL_V2_ABSENT_ROUTES),
            "old_scientific_work_performed": False,
            "old_native_gate_emissions": 0,
            "original_CPU_seconds": None,
            "original_wall_seconds": None,
            "original_hard_budget_state_certified": False,
            "scientific_budget_censor_claim": None,
            "new_test_credit": 0,
            "failure_not_promoted_or_repaired": True,
        }

    def verify_v2_absence(self):
        self.check()
        require(
            not any(
                (PROGRAM / name).exists() or (PROGRAM / name).is_symlink()
                for name in HISTORICAL_V2_ABSENT_ROUTES
            ),
            "Historical V2 failed before its routes were created; no old retry",
        )

    def admit_v3_history(self):
        """Preserve the actual missing namespace-init admission failure unchanged."""
        for key, expected in HISTORICAL_V3_PINS.items():
            self.add(ROOT / key, expected)
        ready = self.read(ROOT / ".context/A20_signal_producer_ROOT_READY_run002.json")
        require(
            ready["schema"] == "A20-comparator-phase-static-READY-v3"
            and ready["role"] == "producer"
            and ready["ready"] is True
            and ready["budget"] == [CPU, WORK, WALL]
            and ready["output"] == "results/limitation_program_20261001/A20_signal_semantics_run002"
            and ready["author_sha256"]
            == {key: pin for key, pin in HISTORICAL_V3_PINS.items() if key.startswith("research/")}
            and ready["immutable_V2_history_SHA256"] == HISTORICAL_V2_PINS,
            "Exact immutable V3 release, six historical authors and original V2 pins",
        )
        log = self.read_bytes(ROOT / ".context/a20_signal_prepare_run002.log")
        require(
            log.startswith(b"\xef\xbb\xbf")
            and "FileNotFoundError: [WinError 2]" in log.decode("utf-8-sig")
            and r"limitation_program_20261001\\__init__.py" in log.decode("utf-8-sig"),
            "Exact raw UTF8-BOM missing namespace-init admission failure log",
        )
        self.verify_v3_absence()
        policy = self.read(RESEARCH / "a20_comparator_phase_implementation_preflight_v5.json")
        require(
            policy["immutable_V3_admission_history_expected_sha256"] == HISTORICAL_V3_PINS,
            "Prospective V5 method preserves every immutable V3 history pin",
        )
        self.history_v3 = {
            "schema": "A20-V3-pre-mkdir-admission-failure-history-v1",
            "historical_expected_sha256": HISTORICAL_V3_PINS,
            "failed_before_receipt_mkdir": True,
            "error_type": "FileNotFoundError",
            "error": "Missing namespace-package research/limitation_program_20261001/__init__.py",
            "historical_output_routes_absent": list(HISTORICAL_V3_ABSENT_ROUTES),
            "old_scientific_work_performed": False,
            "old_native_gate_emissions": 0,
            "original_CPU_seconds": None,
            "original_wall_seconds": None,
            "original_hard_budget_state_certified": False,
            "scientific_budget_censor_claim": None,
            "new_test_credit": 0,
            "failure_not_promoted_or_repaired": True,
        }

    def verify_v3_absence(self):
        self.check()
        require(
            not any(
                (PROGRAM / name).exists() or (PROGRAM / name).is_symlink()
                for name in HISTORICAL_V3_ABSENT_ROUTES
            ),
            "Historical V3 failed before its routes were created; no old retry or alias",
        )

    def admit_v4_hold_and_external_history(self):
        """Metadata-only fixed history admission; no foreign scientific work is called."""
        for key, expected in {**HELD_V4_AUTHOR_PINS, **OTHER_AGENT_STATIC_TEXT_PINS}.items():
            self.add(ROOT / key, expected)
        self.verify_v4_hold_absence()
        policy = self.read(RESEARCH / "a20_comparator_phase_implementation_preflight_v5.json")
        require(
            policy["held_V4_author_expected_sha256"] == HELD_V4_AUTHOR_PINS
            and policy["other_agent_static_text_expected_sha256"] == OTHER_AGENT_STATIC_TEXT_PINS
            and (
                policy["external_history_manifest_expected_sha256"]
                == EXTERNAL_HISTORY_MANIFEST_PINS
            ),
            "Exact prospective held-draft, static-text and external-history pin shapes",
        )
        admitted = {}
        for name, expected in EXTERNAL_HISTORY_MANIFEST_PINS.items():
            directory = self.canonical(ROOT / name)
            manifest_path = self.add(directory / "manifest.json", expected)
            manifest = self.read(manifest_path)
            require(
                manifest.get("passed") is True
                and manifest.get("manifest_self_hash_excluded") is True
                and (manifest.get("new_test_credit", manifest.get("new_fixture_credit")) == 0),
                "Historical metadata packets pass only their own zero-credit scope",
            )
            files = manifest["files"]
            owned = {manifest_path}
            for member, pin in files.items():
                path = self.add(directory / member, pin)
                require(
                    lexically_under(path, directory)
                    and path.relative_to(directory).as_posix() == member
                    and (path not in owned),
                    "Strict complete historical owned map with exact physical confinement",
                )
                owned.add(path)
            require(
                self.inventory(directory) == owned, "Exact historical metadata packet inventory"
            )
            self.source_packets.append((directory, owned))
            admitted[directory.name] = manifest
        capture_dir = PROGRAM / "A20_continuation_20261004_failure_capture_run001"
        capture = admitted[capture_dir.name]
        require(
            capture.get("integrity_only") is True and capture.get("original_source_failed") is True,
            "Original failure capture is integrity-only and does not approve science",
        )
        failed_dir = PROGRAM / "A20_continuation_20261004_producer_run002"
        failed_owned = self.read(capture_dir / "failed_source_owned_inventory.json")
        require(len(failed_owned) == 2900, "Exactly2900 immutable failed-owned members")
        failed_paths = set()
        for member, pin in failed_owned.items():
            path = self.add(failed_dir / member, pin)
            require(
                lexically_under(path, failed_dir)
                and path.relative_to(failed_dir).as_posix() == member
                and (path not in failed_paths),
                "Exact failed source owned membership and expected SHA",
            )
            failed_paths.add(path)
        require(
            self.inventory(failed_dir) == failed_paths,
            "Complete actual failed source retained inventory",
        )
        self.failed_history_packets.append((failed_dir, failed_paths))
        failure = self.read(failed_dir / "failure.json")
        marker = self.read(failed_dir / "FAILED_UNSEALED.json")
        require(
            failure.get("passed") is False
            and failure.get("message") == "Exact shared stock template; no unproved deduplication"
            and (failure.get("new_test_credit") == 0)
            and (failure.get("adoption") is False)
            and (marker.get("authoritative_failure") is True)
            and (marker.get("passed") is False)
            and (marker.get("hard_budget_state_uncertified") is True),
            "Authoritative original scientific failure is immutable and unapproved",
        )
        expected_maps = self.read(capture_dir / "failed_prepared_expected_maps.json")
        failed_protocol = self.read(failed_dir / "protocol.json")
        require(
            failed_protocol["frozen_inputs"] == expected_maps["frozen_inputs"]
            and failed_protocol["external_runtime_inputs"]
            == expected_maps["external_runtime_inputs"]
            and (
                failed_protocol["prepared_owned_files_protocol_self_hash_excluded"]
                == expected_maps["prepared_owned"]
            )
            and (len(expected_maps["prepared_owned"]) == 2896)
            and all(
                (
                    failed_owned.get(key) == pin
                    for key, pin in expected_maps["prepared_owned"].items()
                )
            ),
            "Original prepared expectations retained exactly without live-map or runtime promotion",
        )
        capture_check = self.read(capture_dir / "verification.json")
        require(
            capture_check.get("passed") is True
            and capture_check.get("integrity_only") is True
            and (capture_check.get("original_scientific_attempt_passed") is False)
            and (capture_check.get("original_failed_unsealed_authoritative") is True)
            and (capture_check.get("component_checks_completed") == 0)
            and (capture_check.get("gate_recipes_emitted") == 0),
            "Capture does not supply completed component checks or gate recipes",
        )
        diagnostic_dir = PROGRAM / "A20_continuation_20261004_template_diagnostic_run001"
        diagnostic = admitted[diagnostic_dir.name]
        require(
            diagnostic.get("schema") == "a20-two-closure-diagnostic-manifest-v1"
            and diagnostic.get("scientific_component_approval") is False,
            "Diagnostic scope is structural closure metadata only",
        )
        diagnostic_nine = {
            diagnostic_dir.relative_to(ROOT).as_posix()
            + "/manifest.json": EXTERNAL_HISTORY_MANIFEST_PINS[
                diagnostic_dir.relative_to(ROOT).as_posix()
            ]
        }
        for member, pin in diagnostic["files"].items():
            diagnostic_nine[(diagnostic_dir / member).relative_to(ROOT).as_posix()] = pin
        for member, pin in diagnostic["frozen_inputs"].items():
            require(
                (ROOT / member).relative_to(ROOT).as_posix() == member,
                "Strict diagnostic frozen ROOT spelling",
            )
            self.add(ROOT / member, pin)
            diagnostic_nine[member] = pin
        require(len(diagnostic_nine) == 9, "Exact nine-path diagnostic metadata integrity scope")
        diagnostic_summary = self.read(diagnostic_dir / "summary.json")
        require(
            diagnostic_summary.get("passed") is True
            and diagnostic_summary.get("exact_shared_template_premise") is False
            and (diagnostic_summary.get("scientific_component_approval") is False)
            and (diagnostic_summary.get("clamp_signed_literals_equal") is True)
            and (
                [row["position_zero_based"] for row in diagnostic_summary["node_differences"]]
                == [10, 17, 21, 30, 34]
            ),
            "Original raw-DAG rejection and five diagnosed swaps retained",
        )
        integrity_dir = PROGRAM / "A20_continuation_20261004_ROOT_template_integrity_run001"
        integrity = admitted[integrity_dir.name]
        require(
            integrity.get("integrity_only") is True
            and integrity["frozen_inputs"]
            == {str(Path(key)): pin for key, pin in diagnostic_nine.items()},
            "Exact pinned ROOT metadata Windows-key shape; no general modern-map normalization",
        )
        integrity_check = self.read(integrity_dir / "verification.json")
        require(
            integrity_check.get("passed") is True
            and integrity_check.get("completed") is True
            and (
                integrity_check.get("source_manifest_sha256")
                == EXTERNAL_HISTORY_MANIFEST_PINS[diagnostic_dir.relative_to(ROOT).as_posix()]
            )
            and (integrity_check.get("full_G2") is False)
            and (integrity_check.get("financial_source_adoption") is False),
            "ROOT diagnostic integrity is metadata-only, without scientific or financial transfer",
        )
        self.held_v4_history = {
            "schema": "A20-held-unexecuted-V4-author-history-v1",
            "expected_sha256": HELD_V4_AUTHOR_PINS,
            "science_executed": False,
            "ROOT_READY_issued": False,
            "prepare_attempted": False,
            "new_test_credit": 0,
            "reason": "Other-agent raw template mismatch prevented operational-only release",
        }
        self.external_history = {
            "schema": "A20-fixed-external-history-scope-v1",
            "manifest_expected_sha256": EXTERNAL_HISTORY_MANIFEST_PINS,
            "other_agent_static_text_expected_sha256": OTHER_AGENT_STATIC_TEXT_PINS,
            "original_failed_owned_files": 2900,
            "original_prepared_owned_files": 2896,
            "original_failed_unsealed_authoritative": True,
            "diagnostic_raw_template_identity_rejected": True,
            "diagnosed_swapped_positions_zero_based": [10, 17, 21, 30, 34],
            "general_historical_live_map_or_full_runtime_promotion": False,
            "static_foreign_methods_grant_component_PASS": False,
            "new_test_credit": 0,
            "adoption": False,
        }

    def verify_v4_hold_absence(self):
        self.check()
        routes = ("A20_signal_semantics_run003", "A20_signal_semantics_audit_run003")
        ready_routes = (
            "A20_signal_producer_ROOT_READY_run003.json",
            "A20_signal_audit_ROOT_READY_run003.json",
        )
        require(
            not any((PROGRAM / name).exists() or (PROGRAM / name).is_symlink() for name in routes)
            and not any(
                (ROOT / ".context" / name).exists() or (ROOT / ".context" / name).is_symlink()
                for name in ready_routes
            ),
            "Held V4 remains unexecuted without ROOT release",
        )

    def admit_packet(self, directory, expected_manifest):
        directory = self.canonical(directory)
        require(
            directory.is_dir()
            and (not any(((directory / name).exists() for name in FAILURE_NAMES))),
            "No failed/unsealed source packet",
        )
        manifest_path = self.add(directory / "manifest.json", expected_manifest)
        manifest = self.read(manifest_path)
        require(
            manifest.get("schema") == "A20-comparator-phase-component-manifest-v5"
            and manifest.get("role") == "producer"
            and (manifest.get("passed") is True)
            and (manifest.get("completed") is True)
            and (manifest.get("budget_censored") is False)
            and (manifest.get("manifest_self_hash_excluded") is True),
            "Actual complete uncensored producer packet",
        )
        owned = set()
        for key, expected in manifest["files"].items():
            self.check()
            path = self.add(directory / key, expected)
            require(
                lexically_under(path, directory)
                and path.relative_to(directory).as_posix() == key
                and (path not in owned)
                and (path != manifest_path),
                "Unique canonical producer-owned member",
            )
            owned.add(path)
        require(
            self.inventory(directory) == owned | {manifest_path},
            "Exact producer actual owned inventory",
        )
        self.source_packets.append((directory, owned | {manifest_path}))
        for key, expected in manifest["frozen_inputs"].items():
            require((ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical source frozen key")
            self.add(ROOT / key, expected)
        for key, expected in manifest["external_runtime_inputs"].items():
            require(
                Path(key).is_absolute() and str(Path(key)) == key,
                "Canonical scoped source external key",
            )
            self.add(Path(key), expected)
        self.verify()
        for name in ("summary.json", "completion_outcome.json"):
            data = self.read(directory / name)
            require(
                data.get("passed") is True
                and data.get("completed") is True
                and (data.get("budget_censored") is False)
                and (data.get("new_test_credit") == 0)
                and (data.get("internal_component_checks") == 2608)
                and (data.get("full_G2") is False)
                and (data.get("adoption") is False),
                "Actual source outcome, scope and zero credit",
            )
        return manifest

    @staticmethod
    def creation_clock():
        require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.argtypes, kernel.GetCurrentProcess.restype = [], wintypes.HANDLE
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [
            ctypes.POINTER(wintypes.FILETIME)
        ] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        values = [wintypes.FILETIME() for _ in range(4)]
        require(
            kernel.GetProcessTimes(
                kernel.GetCurrentProcess(), *(ctypes.byref(value) for value in values)
            ),
            "Actual process creation clock",
        )
        ticks = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
        age = time.time_ns() - (ticks - 116444736000000000) * 100
        require(age >= 0, "Actual creation precedes observation")
        return time.monotonic() - age / 1e9

    def check(self, admission=False):
        require(
            time.process_time() < (WORK if admission else CPU)
            and time.monotonic() - self.started < WALL,
            "Fixed A20 process CPU/wall guard",
        )

    @staticmethod
    def stamp(path):
        value = path.stat()
        return tuple(
            getattr(value, key, None)
            for key in (
                "st_dev",
                "st_ino",
                "st_size",
                "st_mtime_ns",
                "st_ctime_ns",
                "st_mode",
                "st_file_attributes",
                "st_reparse_tag",
            )
        )

    def canonical(self, path, fresh=False):
        self.check()
        lexical = Path(os.path.abspath(path))
        require(
            not lexically_under(lexical, self.excluded)
            and (not lexically_under(lexical, self.excluded_actual)),
            "Excluded base site lexical origin",
        )
        stamp = self.stamp(lexical)
        if not fresh and lexical in self.physical and (self.physical[lexical][0] == stamp):
            return self.physical[lexical][1]
        actual = lexical.resolve(strict=True)
        require(
            actual == lexical and (not lexically_under(actual, self.excluded_actual)),
            "No alias/reparse/excluded origin",
        )
        require(
            lexically_under(actual, ROOT) or lexically_under(actual, self.base),
            "Exact ROOT or scoped base runtime",
        )
        self.physical[lexical] = (stamp, actual)
        return actual

    def digest(self, path, fresh=False):
        path = self.canonical(path, fresh)
        stamp = self.stamp(path)
        if not fresh and path in self.cache and self.cache[path][0] == stamp:
            return self.cache[path][1]
        require(path.is_file() and stamp[2] <= 128 * 1024**2, "Bounded regular file")
        state, total = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while chunk := stream.read(1 << 20):
                self.check()
                self.hash_work += len(chunk)
                total += len(chunk)
                require(
                    self.hash_work <= 24 * 1024**3 and total <= stamp[2], "Bounded stable hash work"
                )
                state.update(chunk)
        require(total == stamp[2] and self.stamp(path) == stamp, "Actual stable full byte SHA")
        digest = state.hexdigest()
        require(
            path not in self.observed or self.observed[path] == digest,
            "Previously observed actual bytes unchanged",
        )
        self.observed[path], self.cache[path] = digest, (stamp, digest)
        return digest

    def add(self, path, expected):
        self.references += 1
        require(
            self.references <= 100000 and isinstance(expected, str) and SHA.fullmatch(expected),
            "Fixed exact expected reference",
        )
        path = self.canonical(path)
        mapping, key = (
            (self.frozen, path.relative_to(ROOT).as_posix())
            if lexically_under(path, ROOT)
            else (self.external, str(path))
        )
        require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA guards")
        mapping[key] = expected
        return path

    def read_bytes(self, path):
        path = self.canonical(path)
        expected = (
            self.frozen.get(path.relative_to(ROOT).as_posix())
            if lexically_under(path, ROOT)
            else self.external.get(str(path))
        )
        require(expected is not None and self.digest(path) == expected, "Read exact admitted bytes")
        before = self.stamp(path)
        require(before[2] <= 32 * 1024**2, "Bounded JSON/source bytes")
        with path.open("rb") as stream:
            chunks = []
            total = 0
            while chunk := stream.read(1 << 20):
                self.check()
                self.hash_work += len(chunk)
                total += len(chunk)
                require(
                    self.hash_work <= 24 * 1024**3 and total <= before[2],
                    "Charged stable bounded parsing bytes",
                )
                chunks.append(chunk)
        data = b"".join(chunks)
        require(
            total == before[2]
            and self.stamp(path) == before
            and (hashlib.sha256(data).hexdigest() == expected),
            "Same exact parsed bytes",
        )
        self.check()
        return data

    def read(self, path):
        result = json.loads(self.read_bytes(path))
        self.check()
        return result

    def owner_memberships(self, owners):
        memberships = set()
        selected = self.ready["selected_prerequisite_sha256"]
        for key, expected in owners.items():
            path = self.add(ROOT / key, expected)
            require(path.name == "manifest.json", "Selected immutable owner manifest")
            packet = self.read(path)
            legacy_flat = "files" not in packet
            require(
                not any(((path.parent / name).exists() for name in FAILURE_NAMES)),
                "No failed premise owner",
            )
            if legacy_flat:
                require(
                    key
                    == "results/limitation_program_20261001/A10_coefficient_run001/manifest.json"
                    and expected
                    == "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40"
                    and all(
                        (
                            isinstance(value, str) and SHA.fullmatch(value)
                            for value in packet.values()
                        )
                    ),
                    "Only exact original A10 flat owner format",
                )
                packet = {"files": packet}
            require(isinstance(packet.get("files"), dict), "Owner files map")
            for field in ("files", "frozen_inputs"):
                for name, sha in packet.get(field, {}).items():
                    self.check()
                    self.references += 1
                    require(
                        self.references <= 100000, "Bounded selected owner membership references"
                    )
                    if field == "files":
                        spelling = name.replace("\\", "/") if legacy_flat else name
                        lexical = (
                            ROOT / spelling
                            if spelling.startswith(path.parent.relative_to(ROOT).as_posix() + "/")
                            else path.parent / spelling
                        )
                        selected_key = Path(os.path.abspath(lexical)).relative_to(ROOT).as_posix()
                        if selected_key not in selected:
                            continue
                        actual = lexical
                        actual = self.canonical(actual)
                        require(
                            lexically_under(actual, path.parent), "Owned member confined to receipt"
                        )
                        require(
                            spelling
                            in (
                                actual.relative_to(ROOT).as_posix(),
                                actual.relative_to(path.parent).as_posix(),
                            ),
                            "Exact selected owned member spelling",
                        )
                    else:
                        if name not in selected:
                            continue
                        actual = self.canonical(ROOT / name)
                        require(
                            actual.relative_to(ROOT).as_posix() == name,
                            "Canonical frozen owner key",
                        )
                    require(isinstance(sha, str) and SHA.fullmatch(sha), "Owner exact SHA")
                    memberships.add((actual.relative_to(ROOT).as_posix(), sha))
        return memberships

    def verify(self, fresh=False):
        if fresh:
            self.verify_recovery_history()
            self.verify_v2_absence()
            self.verify_v3_absence()
            self.verify_v4_hold_absence()
            self.verify_packet_inventory()
        union = {ROOT / key: value for key, value in self.frozen.items()}
        for key, value in self.external.items():
            require(
                Path(key) not in union or union[Path(key)] == value, "Canonical union equal SHA"
            )
            union[Path(key)] = value
        for path, value in self.observed.items():
            require(
                path not in union or union[path] == value,
                "Actual observations join immutable union",
            )
            union[path] = value
        size = 0
        for path in union:
            self.check()
            size += self.stamp(path)[2]
            require(size <= 8 * 1024**3, "Fixed8GiB unique input cap")
        for path, expected in sorted(union.items()):
            self.check()
            require(self.digest(path, fresh) == expected, "Full exact union verification")
        if fresh:
            self.verify_packet_inventory()
            self.verify_recovery_history()
        return len(union)

    def verify_packet_inventory(self):
        for directory, expected in self.source_packets:
            self.check()
            require(
                not any((directory / name).exists() for name in FAILURE_NAMES)
                and self.inventory(directory) == expected,
                "Admitted source remains complete without new failure or unexpected owned members",
            )

        for directory, expected in self.failed_history_packets:
            self.check()
            require(
                self.inventory(directory) == expected
                and (directory / "FAILED_UNSEALED.json").is_file()
                and not (directory / "manifest.json").exists(),
                "Complete original failed inventory and authoritative failure remain unchanged",
            )

    def inventory(self, directory):
        files, runtime_size, component_size, runtime_count, component_count = (set(), 0, 0, 0, 0)
        for base, directories, names in os.walk(directory, followlinks=False):
            self.check()
            for name in directories:
                path = self.canonical(Path(base) / name)
                require(
                    lexically_under(path, directory) and (not path.is_symlink()),
                    "Confined non-link owned directories",
                )
            for name in names:
                path = self.canonical(Path(base) / name)
                require(
                    lexically_under(path, directory) and path not in files and path.is_file(),
                    "Unique confined owned file",
                )
                files.add(path)
                relative = path.relative_to(directory)
                if relative.parts[0] == "runtime_snapshot":
                    require(
                        len(relative.parts) == 2
                        and relative.name.isdecimal()
                        and (str(int(relative.name)) == relative.name),
                        "Exact runtime snapshot member shape",
                    )
                    runtime_count += 1
                    runtime_size += path.stat().st_size
                    require(
                        runtime_count <= 24000 and runtime_size <= 2 * 1024**3,
                        "Separate complete runtime snapshot evidence cap",
                    )
                else:
                    component_count += 1
                    component_size += path.stat().st_size
                    require(
                        component_count <= 64 and component_size <= 128 * 1024**2,
                        "Separate fixed component evidence cap",
                    )
                require(len(files) <= 24064, "Combined prospectively declared owned cap")
        return files

    def runtime_paths(self):
        self.import_policy()
        prefix = Path(sys.prefix).resolve(strict=True)
        require(prefix == ROOT / ".context/frontier_t0_env", "Actual isolated prefix")
        self.check()
        config = (prefix / "pyvenv.cfg").read_text(encoding="utf-8")
        self.check()
        require("include-system-site-packages = false" in config.lower(), "No system-site runtime")
        roots = [self.base / "Lib", self.base / "DLLs", prefix / "Scripts"]
        found = set()
        absent = set()
        site = prefix / "Lib/site-packages"
        for root in (prefix, site):
            for path in root.iterdir():
                self.check()
                if path.is_file() and (
                    root == prefix or path.suffix in (".pth", ".py", ".pyc", ".pyd")
                ):
                    found.add(self.canonical(path))
                elif path.is_dir() and (
                    path.name == "__pycache__"
                    or (root == prefix and (path / "__init__.py").exists())
                    or path.name in ("sitecustomize", "usercustomize")
                ):
                    roots.append(self.canonical(path))
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if not name:
                    continue
                lexical = Path(os.path.abspath(name))
                require(
                    not lexically_under(lexical, self.excluded)
                    and (not lexically_under(lexical.resolve(strict=False), self.excluded_actual)),
                    "Excluded module/cache origin even if absent",
                )
                if lexically_under(lexical, site):
                    relative = lexical.relative_to(site)
                    if len(relative.parts) > 1:
                        package = site / relative.parts[0]
                        if package.is_dir():
                            roots.append(self.canonical(package))
        for name in AUTHOR_NAMES:
            source = RESEARCH / name
            if source.suffix == ".py":
                found.add(self.canonical(source))
                cache = Path(importlib.util.cache_from_source(str(source)))
                if cache.exists():
                    found.add(self.canonical(cache))
                else:
                    absent.add(str(cache))

        def optional_init_member(path):
            self.check()
            require(
                path == Path(os.path.abspath(path))
                and (not path.is_symlink())
                and (path.resolve(strict=False) == path),
                "Exact package-init source/cache route including absent or dangling aliases",
            )
            if path.exists():
                require(path.is_file(), "Existing package-init source/cache is regular")
                found.add(self.canonical(path))
            else:
                absent.add(str(path))

        for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
            self.canonical(source.parent)
            optional_init_member(source)
            optional_init_member(source.with_suffix(".pyc"))
            for optimization in ("", "1", "2"):
                optional_init_member(
                    Path(importlib.util.cache_from_source(str(source), optimization=optimization))
                )
            cache_directory = source.parent / "__pycache__"
            require(
                not cache_directory.is_symlink()
                and cache_directory.resolve(strict=False) == cache_directory,
                "Exact package-init cache directory including absent aliases",
            )
            if cache_directory.exists():
                require(cache_directory.is_dir(), "Package-init cache parent is a directory")
                self.canonical(cache_directory)
                for cache in cache_directory.glob("__init__*.pyc"):
                    optional_init_member(cache)
        for root in roots:
            require(root.is_dir(), "Declared runtime tree")
            for base, directories, names in os.walk(root, topdown=True, followlinks=False):
                self.check()
                directories[:] = [
                    name for name in directories if Path(base) / name != self.excluded
                ]
                for name in directories:
                    directory = self.canonical(Path(base) / name)
                    require(
                        lexically_under(directory, root) and (not directory.is_symlink()),
                        "Every runtime directory including empty aliases is confined",
                    )
                for name in names:
                    found.add(self.canonical(Path(base) / name))
        for root in (prefix, self.base):
            for path in root.iterdir():
                self.check()
                if path.is_file():
                    found.add(self.canonical(path))
        allowed_search = {
            ROOT,
            prefix,
            site,
            self.base,
            self.base / "Lib",
            self.base / "DLLs",
            self.base / "python312.zip",
        }
        for name in sys.path:
            lexical = Path(os.path.abspath(name or ROOT))
            require(
                lexical in allowed_search and (not lexically_under(lexical, self.excluded)),
                "Declared finite sys.path",
            )
            if lexical.is_file():
                found.add(self.canonical(lexical))
            elif not lexical.exists():
                absent.add(str(lexical))
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if not name:
                    continue
                lexical = Path(os.path.abspath(name))
                require(
                    not lexically_under(lexical, self.excluded)
                    and (not lexically_under(lexical.resolve(strict=False), self.excluded_actual)),
                    "Excluded module/cache origin even if absent",
                )
                if lexical.exists():
                    actual = self.canonical(lexical)
                    require(
                        lexically_under(actual, self.base)
                        or lexically_under(actual, prefix)
                        or lexically_under(actual, RESEARCH)
                        or (
                            actual
                            in (
                                ROOT / "research/__init__.py",
                                ROOT / "research/__init__.pyc",
                                ROOT / "research/__pycache__/__init__.cpython-312.pyc",
                            )
                        ),
                        "Bounded loaded origin",
                    )
                    found.add(actual)
                elif (
                    lexically_under(lexical, self.base)
                    or lexically_under(lexical, prefix)
                    or lexically_under(lexical, RESEARCH)
                    or (
                        lexical
                        in (
                            ROOT / "research/__init__.pyc",
                            ROOT / "research/__pycache__/__init__.cpython-312.pyc",
                        )
                    )
                ):
                    absent.add(str(lexical))
                else:
                    require(False, "Unexpected absent loaded origin")
        size = 0
        for path in found:
            self.check()
            size += self.stamp(path)[2]
            require(len(found) <= 24000 and size <= 2 * 1024**3, "Fixed full reachable runtime cap")
        self.runtime_absent = sorted(absent)
        return sorted(found)

    def verify_loaded(self, protocol):
        self.import_policy()
        require(
            [str(path) for path in self.runtime_paths()] == protocol["runtime_paths"]
            and self.runtime_absent == protocol["runtime_absent"],
            "Complete runtime and absence inventory unchanged",
        )
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if name and Path(name).exists():
                    path = self.canonical(name)
                    expected = (
                        self.frozen.get(path.relative_to(ROOT).as_posix())
                        if lexically_under(path, ROOT)
                        else self.external.get(str(path))
                    )
                    require(
                        expected is not None and self.digest(path) == expected,
                        "Every actual loaded origin/cache has captured exact bytes",
                    )

    def import_policy(self):
        forbidden = ("numpy", "numba", "scipy", "mpmath", "pytest", "qiskit", "cirq", "psutil")
        forbidden += (
            "research.limitation_program_20261001.arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.a20_signal_receipt_v2",
        )
        forbidden += (
            "research.limitation_program_20261001.arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.a20_signal_receipt_v3",
        )
        forbidden += (
            "research.limitation_program_20261001.arithmetic_free_basket_signal_v4",
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v4",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v4",
            "research.limitation_program_20261001.a20_signal_receipt_v4",
        )
        if self.role == "audit":
            forbidden += (
                "research.limitation_program_20261001.arithmetic_free_basket_signal_v5",
                "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v5",
            )
        require(
            not any(
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in forbidden
            ),
            "Stdlib-only component and independent auditor import policy",
        )

    def reserve_owned(self, path, size):
        """Enforce all prospective owned caps before opening a new file."""
        self.check()
        require(type(size) is int and 0 <= size <= 128 * 1024**2, "Bounded prospective owned file")
        require(
            lexically_under(path, self.output)
            and path.resolve(strict=False) == path
            and (not path.exists()),
            "Confined canonical exclusive owned target",
        )
        if self.owned_usage is None:
            usage = [0, 0, 0, 0]
            current = self.inventory(self.output)
            require(
                current == self.owned_expected,
                "Only the explicitly admitted inventory initializes owned capacity",
            )
            for existing in current:
                self.check()
                kind = 0 if existing.relative_to(self.output).parts[0] == "runtime_snapshot" else 2
                usage[kind] += 1
                usage[kind + 1] += self.stamp(existing)[2]
            self.owned_usage = usage
        relative = path.relative_to(self.output)
        runtime = relative.parts[0] == "runtime_snapshot"
        if runtime:
            require(
                len(relative.parts) == 2
                and relative.name.isdecimal()
                and (str(int(relative.name)) == relative.name),
                "Exact new runtime snapshot member shape",
            )
        index = 0 if runtime else 2
        updated = self.owned_usage.copy()
        updated[index] += 1
        updated[index + 1] += size
        require(
            updated[0] <= 24000
            and updated[1] <= 2 * 1024**3
            and (updated[2] <= 64)
            and (updated[3] <= 128 * 1024**2)
            and (updated[0] + updated[2] <= 24064),
            "Prospective runtime, component and combined owned caps before mutation",
        )
        self.owned_usage = updated
        self.owned_expected.add(path)

    def write(self, name, value):
        self.check()
        data = json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode() + b"\n"
        self.check()
        require(len(data) <= 32 * 1024**2, "Bounded new JSON artifact")
        path = self.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        require(
            lexically_under(path.resolve(strict=False), self.output), "Confined exclusive output"
        )
        self.reserve_owned(path, len(data))
        with path.open("xb") as stream:
            for offset in range(0, len(data), 1 << 20):
                self.check()
                stream.write(data[offset : offset + (1 << 20)])
        self.check()
        require(
            self.digest(path, True) == hashlib.sha256(data).hexdigest(),
            "Fresh output-byte verification",
        )
        return path

    def prepare(self):
        require(not self.output.exists(), "Fresh exclusive receipt; no retry")
        runtime = self.runtime_paths()
        runtime_absent = self.runtime_absent.copy()
        self.check(admission=True)
        self.output.mkdir()
        self.mutated = True
        self.write("lexical_operational_AST_guard.json", self.lexical_guard)
        self.write("lexical_predicate_equivalence.json", self.lexical_parity())
        copies = {}
        for index, path in enumerate(runtime):
            self.check(admission=True)
            expected = self.digest(path, True)
            self.add(path, expected)
            target = self.output / "runtime_snapshot" / str(index)
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, self.stamp(path)[2])
            with path.open("rb") as source, target.open("xb") as sink:
                while chunk := source.read(1 << 20):
                    self.check(admission=True)
                    self.hash_work += len(chunk)
                    require(self.hash_work <= 24 * 1024**3, "Charged runtime copy/read work")
                    sink.write(chunk)
            require(
                self.digest(target, True) == expected and self.digest(path, True) == expected,
                "Actual snapshot matches live runtime expected bytes",
            )
            self.add(target, expected)
            copies[str(path)] = target.relative_to(ROOT).as_posix()
        for name in AUTHOR_NAMES:
            source = RESEARCH / name
            data = self.read_bytes(source)
            target = self.output / "executed_dependencies" / name
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, len(data))
            with target.open("xb") as sink:
                sink.write(data)
            self.add(target, self.frozen[source.relative_to(ROOT).as_posix()])
        history_copies = {}
        for key, expected in {
            **HISTORICAL_V2_PINS,
            **HISTORICAL_V3_PINS,
            **HELD_V4_AUTHOR_PINS,
            **OTHER_AGENT_STATIC_TEXT_PINS,
        }.items():
            self.check(admission=True)
            source = ROOT / key
            data = self.read_bytes(source)
            target = self.output / "admission_history" / source.name
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, len(data))
            with target.open("xb") as sink:
                sink.write(data)
            self.add(target, expected)
            history_copies[key] = target.relative_to(ROOT).as_posix()
        v2_copies = {key: history_copies[key] for key in HISTORICAL_V2_PINS}
        v3_copies = {key: history_copies[key] for key in HISTORICAL_V3_PINS}
        v4_copies = {key: history_copies[key] for key in HELD_V4_AUTHOR_PINS}
        text_copies = {key: history_copies[key] for key in OTHER_AGENT_STATIC_TEXT_PINS}
        self.write("V2_admission_history.json", {**self.history, "exact_byte_copies": v2_copies})
        self.write("V3_admission_history.json", {**self.history_v3, "exact_byte_copies": v3_copies})
        self.write(
            "held_V4_author_history.json", {**self.held_v4_history, "exact_byte_copies": v4_copies}
        )
        self.write(
            "external_history_scope.json",
            {**self.external_history, "exact_static_text_copies": text_copies},
        )
        require(
            self.inventory(self.output) == self.owned_expected,
            "Exact freshly created prepared owned inventory",
        )
        self.verify(True)
        require(
            self.runtime_paths() == runtime and self.runtime_absent == runtime_absent,
            "Complete prepared runtime presence and exact absence remain unchanged",
        )
        self.check(admission=True)
        prepared_owned = {
            path.relative_to(self.output).as_posix(): self.digest(path)
            for path in sorted(self.owned_expected)
        }
        path = self.write(
            "protocol.json",
            {
                "schema": "A20-comparator-phase-prepared-protocol-v5",
                "role": self.role,
                "budget": [CPU, WORK, WALL],
                "root_READY_sha256": self.digest(self.ready_path),
                "frozen_inputs": self.frozen,
                "external_runtime_inputs": self.external,
                "runtime_live_to_snapshot": copies,
                "runtime_paths": [str(path) for path in runtime],
                "runtime_absent": self.runtime_absent,
                "immutable_V2_admission_failure_history": self.history,
                "immutable_V2_history_live_to_snapshot": v2_copies,
                "immutable_V3_admission_failure_history": self.history_v3,
                "immutable_V3_history_live_to_snapshot": v3_copies,
                "held_V4_author_history": self.held_v4_history,
                "held_V4_live_to_snapshot": v4_copies,
                "external_history_scope": self.external_history,
                "other_agent_static_text_live_to_snapshot": text_copies,
                "prepared_owned_files_protocol_self_hash_excluded": prepared_owned,
                "operational_recovery_version": 6,
                "immutable_recovery_history": self.recovery_history,
                "lexical_operational_AST_guard": self.lexical_guard,
                "component_gate_emission_permitted_after_run_admission": True,
                "full_pricing_source_emission": False,
                "internal_checks_not_financial_fixtures": True,
            },
        )
        require(
            self.inventory(self.output) == self.owned_expected,
            "Exact complete prepared owned inventory after protocol write",
        )
        self.check()
        return self.digest(path, True)

    def admit_run(self, protocol_sha):
        require(
            self.output.is_dir()
            and (
                not any(
                    (
                        (self.output / name).exists()
                        for name in ("manifest.json", "completion_outcome.json", "RUN_STARTED.json")
                        + FAILURE_NAMES
                    )
                )
            ),
            "One run of complete prepared receipt",
        )
        protocol_path = self.output / "protocol.json"
        self.add(protocol_path, protocol_sha)
        protocol = self.read(protocol_path)
        require(
            protocol["schema"] == "A20-comparator-phase-prepared-protocol-v5"
            and protocol["role"] == self.role
            and (protocol["root_READY_sha256"] == self.digest(self.ready_path))
            and (protocol["immutable_V2_admission_failure_history"] == self.history)
            and (protocol["immutable_V3_admission_failure_history"] == self.history_v3)
            and (protocol["held_V4_author_history"] == self.held_v4_history)
            and (protocol["external_history_scope"] == self.external_history),
            "Same prepared protocol/root READY",
        )
        prepared_owned = set()
        for key, expected in protocol["prepared_owned_files_protocol_self_hash_excluded"].items():
            path = self.add(self.output / key, expected)
            require(
                lexically_under(path, self.output)
                and path.relative_to(self.output).as_posix() == key
                and (path != protocol_path)
                and (path not in prepared_owned),
                "Unique canonical prepared owned member",
            )
            prepared_owned.add(path)
        require(
            self.inventory(self.output) == prepared_owned | {protocol_path},
            "Exactly prepared owned inventory before exclusive run admission",
        )
        self.owned_expected = prepared_owned | {protocol_path}
        self.mutated = True
        self.write(
            "RUN_STARTED.json",
            {
                "role": self.role,
                "prepared_protocol_sha256": protocol_sha,
                "exclusive_no_retry": True,
                "process_CPU_seconds": time.process_time(),
                "creation_wall_seconds": time.monotonic() - self.started,
            },
        )
        for key, expected in protocol["frozen_inputs"].items():
            require((ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical prepared ROOT key")
            self.add(ROOT / key, expected)
        for key, expected in protocol["external_runtime_inputs"].items():
            self.add(Path(key), expected)
        require(
            [str(path) for path in self.runtime_paths()] == protocol["runtime_paths"],
            "Complete actual runtime inventory unchanged",
        )
        require(
            self.runtime_absent == protocol["runtime_absent"],
            "Exact previously absent bytecode/zip origins still absent",
        )
        self.verify(True)
        self.check(admission=True)
        self.mutated = True
        return protocol

    def seal(self, summary):
        self.write("summary.json", summary)
        self.write("completion_outcome.json", {**summary, "authoritative_terminal_outcome": True})
        count = self.verify(True)
        self.check()
        owned = self.inventory(self.output)
        require(
            owned == self.owned_expected, "Exactly admitted and newly created terminal owned files"
        )
        files = {
            path.relative_to(self.output).as_posix(): self.digest(path, True)
            for path in sorted(owned)
        }
        self.check()
        manifest = {
            "schema": "A20-comparator-phase-component-manifest-v6",
            "role": self.role,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "files": files,
            "frozen_inputs": self.frozen,
            "external_runtime_inputs": self.external,
            "manifest_self_hash_excluded": True,
            "fresh_union_paths": count,
            "all_original_scientific_scopes_retained": True,
            "operational_recovery_version": 6,
            "immutable_recovery_history": self.recovery_history,
            "lexical_operational_AST_guard": self.lexical_guard,
            "old_run004_remains_failed_and_unapproved": True,
            "new_test_credit": 0,
        }
        self.write("manifest.json", manifest)
        require(
            self.inventory(self.output) == owned | {self.output / "manifest.json"},
            "Exact terminal owned inventory",
        )
        self.check()

    def fail(self, error):
        if not self.mutated or not self.output.exists():
            return
        manifest = self.output / "manifest.json"
        try:
            if manifest.exists():
                manifest.rename(self.output / "failed_manifest_attempt.json")
        except OSError:
            pass
        marker = (
            b'{"passed":false,"authoritative_failure":true,"budget_censored":null,'
            b'"hard_budget_state_uncertified":true,"new_test_credit":0,"adoption":false}\n'
        )
        try:
            with (self.output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(marker)
        except OSError:
            pass
        try:
            self.check()
            self.write(
                "failure.json",
                {
                    "passed": False,
                    "error_type": type(error).__name__,
                    "message": str(error)[:4096],
                    "budget": [CPU, WORK, WALL],
                    "new_test_credit": 0,
                    "adoption": False,
                },
            )
        except BaseException:
            pass


SELECTED = {
    "research/journal_sprint/reversible_fixed_point.py": (
        "52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b"
    ),
    "research/controlled_source_completion/exact_lookup.py": (
        "a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c"
    ),
    "results/limitation_program_20261001/E22_census_run002/B4x12_predicate_census.json": (
        "35b9cf84b23b10d871dbb64e5af1bdfe9c9ce58db811ac089f7729c6eebfabb3"
    ),
    "results/limitation_program_20261001/A17_quantile_divider_run001/exact_CCX_phase_proof.json": (
        "714698f92a1d94f61ec26f746e77f9a7aa936a41308a9b82e6e93495fa92a55c"
    ),
    "research/limitation_program_20261001/temporary_and_fulladder.py": (
        "34bb7f93d07b51de54c44d2fd8c124678d280db01066df848bb7eac43aa2dfeb"
    ),
}

TARGET = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/target.json"

CENSUS = PROGRAM / "E22_census_run002/B4x12_predicate_census.json"

SUPPORT = PROGRAM / "E03_support_audit_run002/B4x12_audit.json"

PHASE = PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"


# NEW DIAGNOSTIC WRAPPER ONLY. All original 37 Receipt methods above are exact.
DIAGNOSTIC_AUTHOR_NAMES = (
    "replay_a20_signal_run005_lifecycle_v1.py",
    "A20_SIGNAL_RUN005_LIFECYCLE_REPLAY_PREFLIGHT_V1.md",
    "a20_signal_run005_lifecycle_replay_preflight_v1.json",
)
DIAGNOSTIC_READY = ROOT / ".context/A20_SIGNAL_RUN005_LIFECYCLE_REPLAY_ROOT_READY_run001.json"
DIAGNOSTIC_OUTPUT = PROGRAM / "A20_signal_run005_lifecycle_replay_run001"
V6_CONTROLLER_SHA = "49cdcfaba5b6b7a41eba31776483b2ca6c549852f4ac188e11bd48a114c5e660"
V6_RECEIPT_AST_SHA = "d591bc2a7518069591fe95b336acb4b05698009a730e93f0f72b52613ab429b5"
V6_READY_SHA = "db0c8560db19a6ed08724505e2db9eea7868c088c9048685deed832d881d2e8d"
FAILED_005 = PROGRAM / "A20_signal_semantics_run005"
FAILED_005_FREEZE = ROOT / ".context/A20_signal_run005_FAILED_OWNED_FROZEN_run001.json"
FAILED_005_FREEZE_SHA = "0f427ba7d4a743b08c2cb24d67239b891bb5299c28ae4ce8ece26616f8a94716"
FAILED_005_PROTOCOL_SHA = "9374af35fd3daa3505adc063340187d4a36d2adad869367dc62c2cb855f05f57"
FAILED_005_LOG = ROOT / ".context/a20_signal_semantics_run005.log"
FAILED_005_LOG_SHA = "fd6d3dd292272506945938699e0ea2a5724c8a5bf190a9dc41c45d6ec374f76b"
FAILED_005_OWNED_COUNT = 2942
FAILED_005_OWNED_BYTES = 116034567
FAILED_005_PROTOCOL_COUNTS = [2938, 8992, 2842, 2893, 14]
MAX_STAGE_EVENTS = 128
MAX_STAGE_BYTES = 128 * 1024
BOOTSTRAP_HASH_WORK = BOOTSTRAP_REFERENCES = 0
DIAGNOSTIC_STARTED = None
STAGE_EVENTS = []
STAGE_BYTES = 0
FAILED_STAGE = None


class ReplayReceipt(Receipt):
    """Charge bootstrap reads from the first original constructor counter check."""

    @property
    def hash_work(self):
        return self._replay_hash_work + BOOTSTRAP_HASH_WORK

    @hash_work.setter
    def hash_work(self, value):
        if hasattr(self, "_replay_hash_work"):
            self._replay_hash_work = value - BOOTSTRAP_HASH_WORK
        else:
            require(value == 0, "Original hash-work counter starts at zero")
            self._replay_hash_work = 0

    @property
    def references(self):
        return self._replay_references + BOOTSTRAP_REFERENCES

    @references.setter
    def references(self, value):
        if hasattr(self, "_replay_references"):
            self._replay_references = value - BOOTSTRAP_REFERENCES
        else:
            require(value == 0, "Original reference counter starts at zero")
            self._replay_references = 0


def diagnostic_budget(admission=False):
    require(time.process_time() < (WORK if admission else CPU), "Fixed A20 process CPU/wall guard")
    require(time.monotonic() - DIAGNOSTIC_STARTED < WALL, "Fixed A20 process CPU/wall guard")


def no_scientific_modules():
    forbidden = ("numpy", "numba", "scipy", "mpmath", "pytest", "qiskit", "cirq", "psutil")
    require(
        not any(
            name == prefix or name.startswith(prefix + ".")
            for name in sys.modules
            for prefix in forbidden
        ),
        "Stdlib-only metadata diagnostic",
    )
    for name, module in tuple(sys.modules.items()):
        if name.startswith("research.limitation_program_20261001."):
            require(
                name
                == "research.limitation_program_20261001.replay_a20_signal_run005_lifecycle_v1",
                "No scientific or receipt dependency module loaded",
            )
        origin = getattr(module, "__file__", None)
        if origin:
            lexical = Path(os.path.abspath(origin))
            require(
                lexical
                not in {
                    RESEARCH / name
                    for name in V5_AUTHOR_NAMES + V6_AUTHOR_NAMES
                    if name.endswith(".py")
                },
                "All producer, builder, old receipt and old auditor sources are reference-only",
            )


def stage_record(name, state, receipt=None, error=None):
    global STAGE_BYTES
    record = {
        "schema": "a20-run005-metadata-lifecycle-stage-observation-v1",
        "sequence": len(STAGE_EVENTS),
        "stage": name,
        "state": state,
        "diagnostic_process_CPU_seconds": time.process_time(),
        "diagnostic_creation_wall_seconds": time.monotonic() - DIAGNOSTIC_STARTED,
        "original_run005_terminal_stage_CPU_wall": None,
        "metadata_only": True,
        "science_calls": 0,
        "new_test_credit": 0,
        "hash_work_bytes": BOOTSTRAP_HASH_WORK if receipt is None else receipt.hash_work,
        "references": BOOTSTRAP_REFERENCES if receipt is None else receipt.references,
        "frozen_keys": None if receipt is None else len(receipt.frozen),
        "external_keys": None if receipt is None else len(receipt.external),
        "observed_keys": None if receipt is None else len(receipt.observed),
    }
    if error is not None:
        record.update(error_type=type(error).__name__, message=str(error)[:4096])
    encoded = json.dumps(record, sort_keys=True, allow_nan=False)
    require(
        len(STAGE_EVENTS) < MAX_STAGE_EVENTS
        and STAGE_BYTES + len(encoded.encode()) + 1 <= MAX_STAGE_BYTES,
        "Fixed bounded stage instrumentation",
    )
    STAGE_EVENTS.append(record)
    STAGE_BYTES += len(encoded.encode()) + 1
    # ROOT captures these prospective observations in its exclusive launch log.
    # This is fixed stdout instrumentation, not an unchecked owned-file writer.
    print(encoded, flush=True)


def stage(name, call, receipt=None):
    global FAILED_STAGE
    stage_record(name, "before", receipt)
    try:
        no_scientific_modules()
        diagnostic_budget()
        result = call()
        no_scientific_modules()
        observed_receipt = result if isinstance(result, Receipt) else receipt
        stage_record(name, "after", observed_receipt)
        return result
    except BaseException as error:
        if FAILED_STAGE is None:
            FAILED_STAGE = name
        stage_record(name, "failed", receipt, error)
        raise


def bootstrap_read(path, expected):
    global BOOTSTRAP_HASH_WORK, BOOTSTRAP_REFERENCES
    diagnostic_budget()
    BOOTSTRAP_REFERENCES += 1
    require(
        BOOTSTRAP_REFERENCES <= MAX_REFERENCES and SHA.fullmatch(expected),
        "Exact bounded bootstrap expected reference",
    )
    lexical = Path(os.path.abspath(path))
    require(
        lexical == path and lexical.resolve(strict=True) == lexical and lexical.is_file(),
        "Exact physically resolved bootstrap member",
    )
    before = Receipt.stamp(path)
    require(before[2] <= 32 * 1024**2, "Bounded bootstrap source/READY")
    pieces, total = [], 0
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            diagnostic_budget()
            BOOTSTRAP_HASH_WORK += len(chunk)
            total += len(chunk)
            require(
                BOOTSTRAP_HASH_WORK <= 24 * 1024**3 and total <= before[2],
                "Charged stable bootstrap byte work",
            )
            pieces.append(chunk)
    data = b"".join(pieces)
    require(
        total == before[2]
        and Receipt.stamp(path) == before
        and hashlib.sha256(data).hexdigest() == expected,
        "Exact stable admitted bootstrap bytes",
    )
    diagnostic_budget()
    return data


def release_admission(path, pin):
    require(
        Path.cwd().resolve(strict=True) == ROOT
        and Path(os.path.abspath(path)) == DIAGNOSTIC_READY
        and SHA.fullmatch(pin),
        "Exact separately frozen new diagnostic ROOT READY",
    )
    ready = json.loads(bootstrap_read(DIAGNOSTIC_READY, pin))
    require(
        ready["schema"] == "A20-run005-metadata-lifecycle-replay-READY-v1"
        and ready["ready"] is True,
        "Released metadata-only diagnostic",
    )
    require(
        ready["root_and_independent_static_reviews_passed"] is True
        and ready["new_test_credit"] == 0
        and all(
            ready[key] is False
            for key in ("adoption", "cost_transfer", "full_G2", "quantum_advantage")
        ),
        "Separate ROOT and independent static release, zero scientific or cost promotion",
    )
    require(
        ready["budget"] == [CPU, WORK, WALL]
        and ready["output"] == DIAGNOSTIC_OUTPUT.relative_to(ROOT).as_posix(),
        "Same fixed caps and exclusive diagnostic route",
    )
    require(
        ready["science_executed_during_authoring"] is False
        and ready["scientific_execution_authorized"] is False
        and ready["local_only"] is True,
        "No scientific release or remote action",
    )
    require(
        ready["source_controller_expected_SHA256"] == V6_CONTROLLER_SHA
        and ready["original_failed_run005_freeze_expected_SHA256"] == FAILED_005_FREEZE_SHA
        and ready["original_protocol_expected_SHA256"] == FAILED_005_PROTOCOL_SHA
        and ready["original_READY_expected_SHA256"] == V6_READY_SHA,
        "Original pins retained, not observed-as-expected",
    )
    keys = {(RESEARCH / name).relative_to(ROOT).as_posix() for name in DIAGNOSTIC_AUTHOR_NAMES}
    require(
        set(ready["author_sha256"]) == keys,
        "Exactly the three separately frozen diagnostic authors",
    )
    for key, expected in ready["author_sha256"].items():
        bootstrap_read(ROOT / key, expected)
    require(
        not DIAGNOSTIC_OUTPUT.exists() and not DIAGNOSTIC_OUTPUT.is_symlink(),
        "Exclusive new diagnostic output, no retry",
    )
    return ready


def normalized_metadata_code(code):
    code_type = type(Receipt.check.__code__)

    def constant(value):
        if isinstance(value, code_type):
            return normalized_metadata_code(value)
        if isinstance(value, tuple):
            return tuple(constant(item) for item in value)
        return value

    return (
        code.co_argcount,
        code.co_posonlyargcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        code.co_code,
        tuple(constant(value) for value in code.co_consts),
        code.co_names,
        code.co_varnames,
        code.co_freevars,
        code.co_cellvars,
        code.co_exceptiontable,
    )


def loaded_reference_guard(current):
    # Compile to inspect code objects only. No compiled code or parsed AST executes.
    compiled = compile(
        current,
        str(RESEARCH / DIAGNOSTIC_AUTHOR_NAMES[0]),
        "exec",
        dont_inherit=True,
        optimize=sys.flags.optimize,
    )
    code_type = type(Receipt.check.__code__)
    classes = [
        value
        for value in compiled.co_consts
        if isinstance(value, code_type) and value.co_name == "Receipt"
    ]
    require(len(classes) == 1, "Exactly one compiled copied metadata class")
    methods = {
        value.co_name: value
        for value in classes[0].co_consts
        if isinstance(value, code_type)
    }
    require(len(methods) == 37, "Exactly37 original metadata code objects")
    for name, expected in methods.items():
        actual = getattr(Receipt, name).__code__
        inherited = getattr(ReplayReceipt, name).__code__
        require(
            inherited is actual
            and normalized_metadata_code(actual) == normalized_metadata_code(expected),
            "Every loaded metadata method and nested constant matches admitted source",
        )


def diagnostic_ast_guard(receipt):
    original = ast.parse(receipt.read_bytes(RESEARCH / V6_AUTHOR_NAMES[0]))
    current = ast.parse(receipt.read_bytes(RESEARCH / DIAGNOSTIC_AUTHOR_NAMES[0]))
    loaded_reference_guard(current)
    original_class = [
        n for n in original.body if isinstance(n, ast.ClassDef) and n.name == "Receipt"
    ]
    current_class = [n for n in current.body if isinstance(n, ast.ClassDef) and n.name == "Receipt"]
    require(
        len(original_class) == len(current_class) == 1,
        "Exactly one copied reference metadata Receipt",
    )
    expected_dump = ast.dump(original_class[0], include_attributes=False)
    require(
        ast.dump(current_class[0], include_attributes=False) == expected_dump
        and hashlib.sha256(expected_dump.encode()).hexdigest() == V6_RECEIPT_AST_SHA,
        "All 37 original metadata methods exact, including all guards/counters",
    )
    cutoff = next(
        i
        for i, n in enumerate(original.body)
        if isinstance(n, ast.FunctionDef) and n.name == "execute"
    )
    require(
        ast.dump(ast.Module(body=current.body[:cutoff], type_ignores=[]), include_attributes=False)
        == ast.dump(
            ast.Module(body=original.body[:cutoff], type_ignores=[]), include_attributes=False
        ),
        "Entire original pre-execute metadata namespace exact",
    )
    require(
        not any(isinstance(n, ast.FunctionDef) and n.name == "execute" for n in current.body),
        "No scientific execute function in diagnostic",
    )
    scopes = {}
    for function in [n for n in original_class[0].body if isinstance(n, ast.FunctionDef)] + [
        n for n in original.body if isinstance(n, ast.FunctionDef) and n.name == "execute"
    ]:
        if function.name in ("__init__", "prepare", "admit_run", "seal", "execute"):
            scopes[function.name] = [
                ast.unparse(n)
                for n in ast.walk(function)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr == "verify"
            ]
    require(
        scopes
        == {
            "__init__": ["self.verify()"],
            "prepare": ["self.verify(True)"],
            "admit_run": ["self.verify(True)"],
            "seal": ["self.verify(True)"],
            "execute": ["receipt.verify(True)", "receipt.verify(True)"],
        },
        "Named AST scopes prove actual fresh/cached call arguments",
    )
    return {
        "schema": "a20-run005-lifecycle-reference-AST-guard-v1",
        "all_37_Receipt_methods_exact": True,
        "all_37_loaded_metadata_code_objects_and_inheritance_exact": True,
        "copied_class_AST_SHA256": V6_RECEIPT_AST_SHA,
        "original_named_verify_calls": scopes,
        "four_scientific_run_fresh_positions": [
            "admit_run",
            "execute.pre_science",
            "execute.post_science",
            "seal",
        ],
        "new_test_credit": 0,
    }


def bind_diagnostic_release(receipt, ready, ready_sha):
    require(
        receipt.hash_work == receipt._replay_hash_work + BOOTSTRAP_HASH_WORK
        and receipt.references == receipt._replay_references + BOOTSTRAP_REFERENCES,
        "Bootstrap work included from first original constructor counter check",
    )
    require(
        receipt.hash_work <= 24 * 1024**3 and receipt.references <= MAX_REFERENCES,
        "Bootstrap work retained in original aggregate counters",
    )
    receipt.add(DIAGNOSTIC_READY, ready_sha)
    for key, expected in ready["author_sha256"].items():
        receipt.add(ROOT / key, expected)
    require(
        ready["interpreter_sha256"] == receipt.ready["interpreter_sha256"]
        and ready["base_interpreter_sha256"] == receipt.ready["base_interpreter_sha256"],
        "Same immutable pinned isolated and base interpreters",
    )
    source = RESEARCH / DIAGNOSTIC_AUTHOR_NAMES[0]
    cache = Path(importlib.util.cache_from_source(str(source)))
    declaration = ready["diagnostic_source_cache_state"]
    require(
        set(declaration) == {"path", "present", "expected_SHA256"}
        and declaration["path"] == cache.relative_to(ROOT).as_posix()
        and type(declaration["present"]) is bool,
        "Exact new source cache route declared before release",
    )
    require(
        cache == Path(os.path.abspath(cache))
        and not cache.is_symlink()
        and cache.resolve(strict=False) == cache,
        "Physical diagnostic cache route",
    )
    if declaration["present"]:
        require(
            cache.is_file()
            and isinstance(declaration["expected_SHA256"], str)
            and SHA.fullmatch(declaration["expected_SHA256"]),
            "Exact pre-existing diagnostic cache pin",
        )
        receipt.add(cache, declaration["expected_SHA256"])
        receipt.history_present_caches[cache] = declaration["expected_SHA256"]
    else:
        require(
            declaration["expected_SHA256"] is None and not cache.exists(),
            "Declared absent diagnostic cache remains absent",
        )
        receipt.history_absent.add(cache)
    return declaration


def admit_failed_run005(receipt):
    receipt.add(FAILED_005_FREEZE, FAILED_005_FREEZE_SHA)
    freeze = receipt.read(FAILED_005_FREEZE)
    require(
        freeze["schema"] == "root-a20-run005-post-failure-observed-owned-freeze-v1"
        and freeze["scope"] == "INTEGRITY_ONLY_FAILED_UNSEALED_NOT_SCIENTIFIC_APPROVAL",
        "Exact ROOT failure-only witness",
    )
    require(
        freeze["original_failure_is_authoritative"] is True
        and freeze["completed"] is False
        and freeze["passed"] is False
        and freeze["budget_censored"] is None
        and freeze["hard_budget_state_uncertified"] is True
        and freeze["exact_failure_stage_and_terminal_CPU_wall"] is None
        and freeze["scientific_function_evaluation_or_checks_completed_before_failure"] is None,
        "No original science or exact terminal inference",
    )
    require(
        freeze["original_READY_expected_SHA256"] == V6_READY_SHA
        and freeze["original_protocol_expected_SHA256"] == FAILED_005_PROTOCOL_SHA
        and freeze["limits_CPU_admission_wall"] == [CPU, WORK, WALL]
        and freeze["all_original_prepared_expected_files_unchanged"] is True
        and freeze["expected_SHA_waivers"] == 0,
        "All original caps and prepared expectations immutable",
    )
    require(
        freeze["owned_file_count"] == FAILED_005_OWNED_COUNT
        and freeze["owned_bytes"] == FAILED_005_OWNED_BYTES
        and len(freeze["observed_owned_files"]) == FAILED_005_OWNED_COUNT,
        "All 2942 failed owned members and retained bytes",
    )
    receipt.add(FAILED_005_LOG, FAILED_005_LOG_SHA)
    require(freeze["raw_log_SHA256"] == FAILED_005_LOG_SHA, "Unchanged original actual raw log")
    members, size = set(), 0
    for key, expected in freeze["observed_owned_files"].items():
        path = receipt.add(ROOT / key, expected)
        require(
            path.relative_to(ROOT).as_posix() == key
            and lexically_under(path, FAILED_005)
            and path not in members,
            "Full canonical failed-owned expected map",
        )
        members.add(path)
        size += receipt.stamp(path)[2]
        require(size <= FAILED_005_OWNED_BYTES, "Bounded failed retention")
    require(
        size == FAILED_005_OWNED_BYTES and receipt.inventory(FAILED_005) == members,
        "Exact whole failed inventory, no selected subset",
    )
    require(
        (FAILED_005 / "FAILED_UNSEALED.json") in members
        and not (FAILED_005 / "manifest.json").exists()
        and not (FAILED_005 / "summary.json").exists()
        and not (FAILED_005 / "completion_outcome.json").exists(),
        "Authoritative unsealed failure never promoted",
    )
    require(
        receipt.frozen[(FAILED_005 / "protocol.json").relative_to(ROOT).as_posix()]
        == FAILED_005_PROTOCOL_SHA,
        "Failure-owned protocol and independently fixed original protocol pin agree",
    )
    receipt.failed_history_packets.append((FAILED_005, members))
    protocol = receipt.read(FAILED_005 / "protocol.json")
    counts = [
        len(protocol[k])
        for k in (
            "prepared_owned_files_protocol_self_hash_excluded",
            "frozen_inputs",
            "external_runtime_inputs",
            "runtime_paths",
            "runtime_absent",
        )
    ]
    require(
        counts == FAILED_005_PROTOCOL_COUNTS
        and freeze["original_prepared_expected_files_count"] == counts[0],
        "All original2938/8992/2842/2893/14 contracts",
    )
    require(
        protocol["schema"] == "A20-comparator-phase-prepared-protocol-v5"
        and protocol["role"] == "producer"
        and protocol["root_READY_sha256"] == V6_READY_SHA
        and protocol["budget"] == [CPU, WORK, WALL]
        and protocol["operational_recovery_version"] == 6,
        "Original exact prepared role, ROOT release and caps, no new science authorization",
    )
    require(
        protocol["immutable_recovery_history"] == receipt.recovery_history
        and protocol["lexical_operational_AST_guard"] == receipt.lexical_guard
        and protocol["immutable_V2_admission_failure_history"] == receipt.history
        and protocol["immutable_V3_admission_failure_history"] == receipt.history_v3
        and protocol["held_V4_author_history"] == receipt.held_v4_history
        and protocol["external_history_scope"] == receipt.external_history,
        "Every original inherited history remains exact",
    )
    original_started = receipt.read(FAILED_005 / "RUN_STARTED.json")
    require(
        original_started["prepared_protocol_sha256"] == FAILED_005_PROTOCOL_SHA
        and original_started["exclusive_no_retry"] is True
        and original_started["role"] == "producer",
        "Exact saved partial admission marker only",
    )
    return protocol, freeze, members


def create_diagnostic_output(receipt):
    receipt.check(admission=True)
    require(
        not DIAGNOSTIC_OUTPUT.exists() and not DIAGNOSTIC_OUTPUT.is_symlink(),
        "Fresh exclusive metadata diagnostic route",
    )
    receipt.output = DIAGNOSTIC_OUTPUT
    receipt.owned_expected = set()
    receipt.owned_usage = None
    receipt.output.mkdir()
    receipt.mutated = True
    receipt.write(
        "RUN_STARTED.json",
        {
            "schema": "a20-run005-metadata-lifecycle-replay-started-v1",
            "role": "metadata-only",
            "exclusive_no_retry": True,
            "original_failed_run005_still_authoritative": True,
            "original_protocol_expected_SHA256": FAILED_005_PROTOCOL_SHA,
            "scientific_execution_authorized": False,
            "new_test_credit": 0,
        },
    )


def admit_prepared_owned(receipt, protocol, failed_members):
    prepared_owned = set()
    for key, expected in protocol["prepared_owned_files_protocol_self_hash_excluded"].items():
        path = receipt.add(FAILED_005 / key, expected)
        require(
            lexically_under(path, FAILED_005)
            and path.relative_to(FAILED_005).as_posix() == key
            and path != FAILED_005 / "protocol.json"
            and path not in prepared_owned,
            "Unique canonical original prepared owned member",
        )
        require(
            path in failed_members
            and receipt.frozen[path.relative_to(ROOT).as_posix()] == expected,
            "Every original prepared expectation agrees with complete frozen failed map",
        )
        prepared_owned.add(path)
    additions = {
        FAILED_005 / n
        for n in ("protocol.json", "RUN_STARTED.json", "FAILED_UNSEALED.json", "failure.json")
    }
    require(
        len(prepared_owned) == 2938
        and receipt.inventory(FAILED_005) == prepared_owned | additions == failed_members,
        "Exactly2938 prepared members plusfour actual immutable failed additions",
    )


def bind_original_protocol_maps(receipt, protocol):
    for key, expected in protocol["frozen_inputs"].items():
        require(
            (ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical original prepared ROOT key"
        )
        receipt.add(ROOT / key, expected)
    for key, expected in protocol["external_runtime_inputs"].items():
        receipt.add(Path(key), expected)
    witnessed = set()
    maps = [protocol["runtime_live_to_snapshot"]] + [
        protocol[k]
        for k in (
            "immutable_V2_history_live_to_snapshot",
            "immutable_V3_history_live_to_snapshot",
            "held_V4_live_to_snapshot",
            "other_agent_static_text_live_to_snapshot",
        )
    ]
    for mapping in maps:
        for live_key, saved_key in mapping.items():
            live = Path(live_key) if Path(live_key).is_absolute() else ROOT / live_key
            saved = ROOT / saved_key
            live = receipt.canonical(live)
            saved = receipt.canonical(saved)
            live_root_key = (
                live.relative_to(ROOT).as_posix() if lexically_under(live, ROOT) else str(live)
            )
            expected = (
                receipt.frozen.get(live_root_key)
                if lexically_under(live, ROOT)
                else receipt.external.get(live_root_key)
            )
            require(
                expected is not None
                and receipt.frozen.get(saved.relative_to(ROOT).as_posix()) == expected,
                "All saved runtime/history live-copy witnesses join unchanged expected maps",
            )
            triple = (live, saved, expected)
            if triple not in witnessed:
                receipt.old_live_snapshot_witnesses.append(triple)
                witnessed.add(triple)
    require(
        len(protocol["runtime_live_to_snapshot"]) == 2893,
        "Complete original runtime live/copy witness map",
    )
    for key in protocol["runtime_absent"]:
        path = Path(key)
        require(
            path == Path(os.path.abspath(path))
            and not path.exists()
            and not path.is_symlink()
            and path.resolve(strict=False) == path,
            "Every original prepared runtime absence retained",
        )
        receipt.history_absent.add(path)
    for live_key in protocol["runtime_paths"]:
        path = Path(live_key)
        if path.suffix == ".pyc":
            expected = (
                receipt.frozen.get(path.relative_to(ROOT).as_posix())
                if lexically_under(path, ROOT)
                else receipt.external.get(str(path))
            )
            require(expected is not None, "Original present cache has prior prepared expectation")
            receipt.history_present_caches[path] = expected


def current_runtime_projection(receipt, protocol, declaration):
    current = receipt.runtime_paths()
    original = {Path(key) for key in protocol["runtime_paths"]}
    source = RESEARCH / DIAGNOSTIC_AUTHOR_NAMES[0]
    cache = ROOT / declaration["path"]
    extension = {source} | ({cache} if declaration["present"] else set())
    require(
        set(current) == original | extension,
        "Complete unchanged original runtime plusonly new diagnostic source/cache",
    )
    expected_absent = set(protocol["runtime_absent"]) | (
        {str(cache)} if not declaration["present"] else set()
    )
    require(
        set(receipt.runtime_absent) == expected_absent,
        "Every original runtime absence plusdeclared new diagnostic absence exact",
    )
    result = dict(protocol)
    result["runtime_paths"] = [str(path) for path in current]
    result["runtime_absent"] = receipt.runtime_absent.copy()
    return result


def metadata_only_gap(receipt):
    receipt.check(admission=True)
    no_scientific_modules()
    return {
        "scientific_interval": "OMITTED_NO_SCIENCE",
        "builder_imports": 0,
        "builder_calls": 0,
        "component_checks_executed": 0,
        "metadata_replay_is_not_original_scientific_runtime": True,
    }


def seal_diagnostic(receipt, ready_sha, ast_guard, projection):
    summary = {
        "schema": "a20-run005-metadata-lifecycle-replay-summary-v1",
        "completed_metadata_prefix": True,
        "metadata_only": True,
        "original_scientific_run005_status": "FAILED_UNSEALED",
        "original_terminal_stage_CPU_wall": None,
        "scientific_execution_authorized": False,
        "scientific_outcome": None,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "cost_transfer": False,
        "adoption": False,
        "full_G2": False,
        "quantum_advantage": False,
        "fresh_call_positions": [
            "admit_run",
            "execute.pre_science",
            "execute.post_science",
            "seal",
        ],
        "scientific_interval": "OMITTED_NO_SCIENCE",
        "reference_AST_guard": ast_guard,
        "diagnostic_ROOT_READY_SHA256": ready_sha,
    }
    receipt.write("summary.json", summary)
    receipt.write(
        "completion_outcome.json",
        {**summary, "authoritative_metadata_terminal_outcome_pending_seal": True},
    )
    count = stage("seal.fresh_union", lambda: receipt.verify(True), receipt)
    receipt.check()
    owned = receipt.inventory(receipt.output)
    require(owned == receipt.owned_expected, "Exactly admitted newly created diagnostic files")
    files = {
        path.relative_to(receipt.output).as_posix(): receipt.digest(path, True)
        for path in sorted(owned)
    }
    receipt.check()
    manifest = {
        "schema": "a20-run005-metadata-lifecycle-replay-manifest-v1",
        "passed": True,
        "completed": True,
        "budget_censored": False,
        "metadata_only": True,
        "files": files,
        "frozen_inputs": receipt.frozen,
        "external_runtime_inputs": receipt.external,
        "manifest_self_hash_excluded": True,
        "fresh_union_paths": count,
        "ROOT_READY_SHA256": ready_sha,
        "original_failed_run005_freeze_expected_SHA256": FAILED_005_FREEZE_SHA,
        "original_protocol_expected_SHA256": FAILED_005_PROTOCOL_SHA,
        "original_run005_unchanged_unapproved": True,
        "original_terminal_stage_CPU_wall": None,
        "reference_AST_guard": ast_guard,
        "diagnostic_stage_stdout_is_ROOT_retained_separate_log": True,
        "stage_observations_before_manifest": STAGE_EVENTS,
        "all_original_fresh_unions_retained": 4,
        "hash_work_bytes_at_preseal": receipt.hash_work,
        "references_at_preseal": receipt.references,
        "extended_runtime_counts": [
            len(projection["runtime_paths"]),
            len(projection["runtime_absent"]),
        ],
        "scientific_execution_authorized": False,
        "scientific_outcome": None,
        "new_test_credit": 0,
        "adoption": False,
        "cost_transfer": False,
        "full_G2": False,
        "quantum_advantage": False,
    }
    receipt.write("manifest.json", manifest)
    require(
        receipt.inventory(receipt.output) == owned | {receipt.output / "manifest.json"},
        "Exact exclusive terminal diagnostic inventory",
    )
    receipt.check()


def main():
    global DIAGNOSTIC_STARTED
    parser = argparse.ArgumentParser(
        description="Metadata-only frozen A20 run005 lifecycle replay; no scientific execution"
    )
    parser.add_argument("--ready", required=True)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    DIAGNOSTIC_STARTED = Receipt.creation_clock()
    receipt = None
    try:
        ready = stage(
            "diagnostic.release_admission", lambda: release_admission(args.ready, args.ready_sha256)
        )
        receipt = stage(
            "V6.constructor.ordinary_verify",
            lambda: ReplayReceipt("producer", V6_READY, V6_READY_SHA, "run"),
        )
        declaration = stage(
            "diagnostic.release_bind_and_original_counter_join",
            lambda: bind_diagnostic_release(receipt, ready, args.ready_sha256),
            receipt,
        )
        ast_guard = stage(
            "diagnostic.exact_reference_AST_guard", lambda: diagnostic_ast_guard(receipt), receipt
        )
        protocol, freeze, failed_members = stage(
            "admit_run.failed005_full_frozen_history", lambda: admit_failed_run005(receipt), receipt
        )
        stage("diagnostic.exclusive_output", lambda: create_diagnostic_output(receipt), receipt)
        stage(
            "admit_run.original_prepared_owned",
            lambda: admit_prepared_owned(receipt, protocol, failed_members),
            receipt,
        )
        stage(
            "admit_run.original_full_maps_and_all_witnesses",
            lambda: bind_original_protocol_maps(receipt, protocol),
            receipt,
        )
        projection = stage(
            "admit_run.complete_runtime_and_absence",
            lambda: current_runtime_projection(receipt, protocol, declaration),
            receipt,
        )
        stage("admit_run.fresh_union", lambda: receipt.verify(True), receipt)
        stage("admit_run.admission150_guard", lambda: receipt.check(admission=True), receipt)
        stage(
            "execute.pre_science.verify_loaded", lambda: receipt.verify_loaded(projection), receipt
        )
        stage("execute.pre_science.fresh_union", lambda: receipt.verify(True), receipt)
        stage(
            "execute.pre_science.admission150_guard", lambda: receipt.check(admission=True), receipt
        )
        stage(
            "execute.after_omitted_import.verify_loaded",
            lambda: receipt.verify_loaded(projection),
            receipt,
        )
        stage("execute.OMITTED_NO_SCIENCE", lambda: metadata_only_gap(receipt), receipt)
        stage(
            "execute.post_science.verify_loaded", lambda: receipt.verify_loaded(projection), receipt
        )
        stage("execute.post_science.fresh_union", lambda: receipt.verify(True), receipt)
        stage(
            "seal.original_full_owned_retention_and_fourth_union",
            lambda: seal_diagnostic(receipt, args.ready_sha256, ast_guard, projection),
            receipt,
        )
        stage_record("diagnostic.terminal", "PASS_METADATA_ONLY", receipt)
        receipt.check()
        return 0
    except BaseException as error:
        # Exact original fail() writes a fixed authoritative marker if output exists.
        # No diagnostic data-file write bypasses its original budget/counter guards.
        if receipt is not None:
            receipt.fail(error)
        stage_record(FAILED_STAGE or "diagnostic.terminal", "FAILED_UNSEALED", receipt, error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
