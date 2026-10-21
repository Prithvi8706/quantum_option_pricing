"""Prospective shared OPERATIONAL receipt machinery only; no science on import."""

from __future__ import annotations

import argparse
import ast
import copy as ast_copy
from collections import Counter
from fractions import Fraction
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
V6_AUDIT_AUTHOR_NAMES = (
    "audit_arithmetic_free_basket_signal_v6.py",
    "A20_COMPARATOR_PHASE_INDEPENDENT_AUDIT_PREFLIGHT_V6.md",
    "a20_comparator_phase_independent_audit_preflight_v6.json",
)
AUTHOR_NAMES = V5_AUTHOR_NAMES + V6_AUTHOR_NAMES + V6_AUDIT_AUTHOR_NAMES
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


V6_AUDIT_READY = ROOT / ".context/A20_signal_audit_ROOT_READY_run005.json"
V6_PRODUCER_MANIFEST_SHA = None
V6_PRODUCER_COMPLETE_COUNTS = None
V6_PRODUCER_PROTOCOL_SHA = None
V6_PRODUCER_RUNTIME_COUNT = None
V6_PRODUCER_READY_SHA = "db0c8560db19a6ed08724505e2db9eea7868c088c9048685deed832d881d2e8d"
V6_PRODUCER_AUTHOR_PINS = {
    "experiment_arithmetic_free_basket_signal_v6.py": (
        "49cdcfaba5b6b7a41eba31776483b2ca6c549852f4ac188e11bd48a114c5e660"
    ),
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V6.md": (
        "ab9de65795a05040397ebc3c1c0b3f7dc9ff0c8923ba541ee6b59868e37c8fa1"
    ),
    "a20_comparator_phase_implementation_preflight_v6.json": (
        "6947a49240e3e5065e4cc01da37640f2a883e4d1b5bf91f3c6d2ad733bf9c1ca"
    ),
}
V5_INDEPENDENT_PROOF_AST_SHA = "242c52d8efddf53408df77f293d84e69d6902c0a2c1e5e18b890e485904a5aba"

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
        require(
            role == "audit" and mode in ("prepare", "run"), "Fixed independent A20 audit role/mode"
        )
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
            self.canonical(self.ready_path) == V6_AUDIT_READY,
            "Exact new producer-only V6 ROOT release route",
        )
        require(
            self.ready["schema"] == "A20-comparator-phase-independent-audit-READY-v6"
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
            "Exactly new auditor trio plus producer V6 trio and six immutable V5 dependencies",
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
        require(
            all(
                authors[(RESEARCH / name).relative_to(ROOT).as_posix()] == pin
                for name, pin in V6_PRODUCER_AUTHOR_PINS.items()
            ),
            "Every original V6 producer author expectation unchanged",
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
        self.audit_proof_guard = independent_proof_ast_guard(self)
        self.admit_new_v6_producer()
        self.verify()

    def admit_new_v6_producer(self):
        require(
            V6_PRODUCER_MANIFEST_SHA is not None
            and V6_PRODUCER_COMPLETE_COUNTS is not None
            and V6_PRODUCER_PROTOCOL_SHA is not None
            and V6_PRODUCER_RUNTIME_COUNT is not None,
            "Conditional author packet needs externally completed ROOT producer expectations",
        )
        policy = self.read(RESEARCH / V6_AUDIT_AUTHOR_NAMES[2])
        require(
            policy["schema"] == "A20-comparator-phase-independent-audit-preflight-v6"
            and self.ready["independent_restricted_component_audit_reviewed"] is True
            and policy["budgets_each_prepare_run"]
            == {
                "hard_process_CPU_seconds": CPU,
                "work_admission_CPU_seconds": WORK,
                "creation_wall_seconds": WALL,
            }
            and policy["V5_independent_proof_AST_SHA256"] == V5_INDEPENDENT_PROOF_AST_SHA,
            "Separate new auditor method, exact independent proof and unchanged budgets",
        )
        for key, expected in (
            ("producer_manifest_sha256", V6_PRODUCER_MANIFEST_SHA),
            ("producer_complete_counts", V6_PRODUCER_COMPLETE_COUNTS),
            ("producer_actual_protocol_sha256", V6_PRODUCER_PROTOCOL_SHA),
            ("producer_runtime_count", V6_PRODUCER_RUNTIME_COUNT),
            ("producer_ROOT_READY_sha256", V6_PRODUCER_READY_SHA),
        ):
            require(
                self.ready[key] == policy[key] == expected,
                "All new producer expectations come from prior ROOT review, never observation",
            )
        directory = PROGRAM / "A20_signal_semantics_run005"
        manifest_path = self.add(directory / "manifest.json", V6_PRODUCER_MANIFEST_SHA)
        manifest = self.read(manifest_path)
        require(
            manifest["schema"] == "A20-comparator-phase-component-manifest-v6"
            and manifest["role"] == "producer"
            and manifest["passed"] is True
            and manifest["completed"] is True
            and manifest["budget_censored"] is False
            and manifest["manifest_self_hash_excluded"] is True
            and manifest["operational_recovery_version"] == 6
            and manifest["immutable_recovery_history"] == self.recovery_history
            and manifest["lexical_operational_AST_guard"] == self.lexical_guard
            and manifest["old_run004_remains_failed_and_unapproved"] is True
            and manifest["new_test_credit"] == 0
            and [
                len(manifest[field])
                for field in ("files", "frozen_inputs", "external_runtime_inputs")
            ]
            == V6_PRODUCER_COMPLETE_COUNTS,
            "Actual complete new V6 producer is a scoped independent-audit input only",
        )
        owned = self.history_owned(directory, manifest["files"])
        require(manifest_path not in owned, "Producer manifest self excluded")
        members = owned | {manifest_path}
        require(
            self.inventory(directory) == members
            and not any(
                (directory / name).exists() or (directory / name).is_symlink()
                for name in FAILURE_NAMES
            ),
            "Exact complete successful producer owned/runtime inventory and no failed marker",
        )
        self.source_packets.append((directory, members))
        for field in ("frozen_inputs", "external_runtime_inputs"):
            require(type(manifest[field]) is dict, "Full producer expected input map")
            for key, expected in manifest[field].items():
                self.check()
                require(
                    (field == "frozen_inputs" and not Path(key).is_absolute())
                    or (field == "external_runtime_inputs" and Path(key).is_absolute()),
                    "Original new producer literal input-map spelling",
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
                    "Full new producer ROOT and external contracts retained without alias adapters",
                )
        producer_ready = self.read(self.add(V6_READY, V6_PRODUCER_READY_SHA))
        require(
            producer_ready["schema"] == "A20-comparator-phase-static-READY-v6"
            and producer_ready["role"] == "producer"
            and producer_ready["budget"] == [CPU, WORK, WALL]
            and producer_ready["author_sha256"]
            == {
                (RESEARCH / name).relative_to(ROOT).as_posix(): pin
                for name, pin in {**V5_AUTHOR_PINS, **V6_PRODUCER_AUTHOR_PINS}.items()
            },
            "Exact original V6 producer release and all nine source expectations",
        )
        protocol = self.read(self.add(directory / "protocol.json", V6_PRODUCER_PROTOCOL_SHA))
        require(
            protocol["schema"] == "A20-comparator-phase-prepared-protocol-v5"
            and protocol["role"] == "producer"
            and protocol["budget"] == [CPU, WORK, WALL]
            and protocol["root_READY_sha256"] == V6_PRODUCER_READY_SHA
            and protocol["operational_recovery_version"] == 6
            and protocol["immutable_recovery_history"] == self.recovery_history
            and protocol["lexical_operational_AST_guard"] == self.lexical_guard,
            "Exact actual ROOT-reviewed new prepared producer protocol retained",
        )
        require(
            all(
                manifest["files"].get(key) == expected
                for key, expected in protocol[
                    "prepared_owned_files_protocol_self_hash_excluded"
                ].items()
            )
            and all(
                manifest[field].get(key) == expected
                for field in ("frozen_inputs", "external_runtime_inputs")
                for key, expected in protocol[field].items()
            ),
            "All original prepared expected maps remain equal-SHA subsets of terminal maps",
        )
        runtime_paths, copies = protocol["runtime_paths"], protocol["runtime_live_to_snapshot"]
        require(
            len(runtime_paths) == len(set(runtime_paths)) == V6_PRODUCER_RUNTIME_COUNT
            and set(copies) == set(runtime_paths),
            "Complete original new producer runtime membership and copies",
        )
        for mapping in (
            copies,
            protocol["immutable_V2_history_live_to_snapshot"],
            protocol["immutable_V3_history_live_to_snapshot"],
            protocol["held_V4_live_to_snapshot"],
            protocol["other_agent_static_text_live_to_snapshot"],
        ):
            for live, saved in mapping.items():
                self.check()
                path, snapshot = self.recovery_path(live), self.recovery_path(saved)
                require(
                    lexically_under(snapshot, directory), "Complete producer snapshot confinement"
                )
                key = (
                    path.relative_to(ROOT).as_posix() if lexically_under(path, ROOT) else str(path)
                )
                expected = (
                    protocol["frozen_inputs"].get(key)
                    if lexically_under(path, ROOT)
                    else protocol["external_runtime_inputs"].get(key)
                )
                require(
                    expected is not None
                    and manifest["files"].get(snapshot.relative_to(directory).as_posix())
                    == expected,
                    "Every original producer live/snapshot witness has its unchanged expectation",
                )
                self.old_live_snapshot_witnesses.append((path, snapshot, expected))
        for spelling in protocol["runtime_absent"]:
            path = Path(spelling)
            require(
                path.is_absolute() and str(path) == spelling,
                "Every original producer source/cache/runtime absence spelling retained",
            )
            self.history_absent.add(path)
        self.verify_recovery_history()

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
            and self.ready["operational_syntax_transfer_and_independent_audit_reviewed"] is True
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
        current = ast.parse(self.read_bytes(RESEARCH / V6_AUDIT_AUTHOR_NAMES[0]))
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

        science_dump = execute_ast(ast.parse(self.read_bytes(RESEARCH / V6_AUTHOR_NAMES[0])))
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
        forbidden += (
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v6",
            "research.limitation_program_20261001.a20_signal_receipt_v5",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v5",
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
                "independent_proof_AST_guard": self.audit_proof_guard,
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
            "independent_proof_AST_guard": self.audit_proof_guard,
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


WIDTH = 72
FRACTION_BITS = 40
UNIT = 1 << FRACTION_BITS
WORD_MASK = (1 << WIDTH) - 1
REFERENCE_BITS = 53
REFERENCE_SIZE = 1 << REFERENCE_BITS
WIRE_LIMIT = 1024
RECIPE_GATE_LIMIT = 20000
VISIT_LIMIT = 64000000
ADMITTED_CHECK = None
VISITS = 0
BOUNDARIES = (
    0,
    1,
    2,
    (1 << 52) - 1,
    1 << 52,
    (1 << 52) + 1,
    REFERENCE_SIZE - 2,
    REFERENCE_SIZE - 1,
)
DIRTY_OUTPUTS = (0, WORD_MASK, sum(1 << j for j in range(0, WIDTH, 2)), 1 << 71)
SIGNED_BOUNDARIES = (
    (-(1 << 71), -(1 << 71)),
    (-(1 << 71), -1),
    (-(1 << 71), 0),
    (-(1 << 71), (1 << 71) - 1),
    (-1, -(1 << 71)),
    (-1, -1),
    (-1, 0),
    (0, -1),
    (0, 0),
    (0, 1),
    ((1 << 71) - 1, 0),
    ((1 << 71) - 1, (1 << 71) - 1),
)
SEVEN_T_SEQUENCE = (
    ("H", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "b"),
    ("T", "target"),
    ("H", "target"),
    ("CX", "a", "b"),
    ("T", "a"),
    ("Tdg", "b"),
    ("CX", "a", "b"),
)


def insist(condition, message):
    if not condition:
        raise ValueError(message)


def checkpoint():
    insist(ADMITTED_CHECK is not None, "No kernel before complete admission")
    ADMITTED_CHECK()


def gate_visit():
    global VISITS
    VISITS += 1
    insist(VISITS <= VISIT_LIMIT, "Fixed exact gate/state visit cap")
    checkpoint()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def object_sha(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def signed_word(value, width=WIDTH):
    insist(type(value) is int and 0 <= value < 1 << width, "Canonical modular word")
    return value if value < 1 << (width - 1) else value - (1 << width)


def phase_binding(columns, text):
    """Bind absolute phase one for the exact paid fifteen-row CCX macro."""
    checkpoint()
    insist(
        columns
        == [
            dict(input=i, output=i ^ (((i & 1) & ((i >> 1) & 1)) << 2), exact_nonzero_phase=1)
            for i in range(8)
        ],
        "All eight exact CCX permutation/absolute-phase columns",
    )
    tree = ast.parse(text.decode("utf-8-sig"))
    found = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    insist(len(found) == 1, "Unique pinned CCX definition")
    returns = [node for node in found[0].body if isinstance(node, ast.Return)]
    insist(len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal CCX return")
    rows = []
    for node in returns[0].value.elts:
        checkpoint()
        insist(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "gate"
            and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and all(isinstance(item, ast.Name) for item in node.args[1:]),
            "Literal exact-phase native chronology",
        )
        rows.append((node.args[0].value, *(item.id for item in node.args[1:])))
    insist(tuple(rows) == SEVEN_T_SEQUENCE, "Exact source-bound seven-T convention")
    return dict(proof_columns=8, exact_phase_one=True, macro=[list(row) for row in rows])


def independent_ccx_phase_columns(macro):
    """The eight complete columns in exact Q(sqrt2,i), with zero-other amplitudes."""
    ports = {"a": 0, "b": 1, "target": 2}
    zero = (Fraction(), Fraction(), Fraction(), Fraction())
    columns = []
    for basis in range(8):
        checkpoint()
        vector = {basis: (Fraction(1), Fraction(), Fraction(), Fraction())}
        for kind, *names in macro:
            checkpoint()
            wires = [ports[name] for name in names]
            next_vector = {}
            for state, amplitude in vector.items():
                gate_visit()
                a, b, c, d = amplitude
                if kind == "H":
                    half = (b, a / 2, d, c / 2)
                    low, high = state & ~(1 << wires[0]), state | (1 << wires[0])
                    sign = -1 if state & (1 << wires[0]) else 1
                    next_vector[low] = tuple(
                        x + y for x, y in zip(next_vector.get(low, zero), half)
                    )
                    next_vector[high] = tuple(
                        x + sign * y for x, y in zip(next_vector.get(high, zero), half)
                    )
                elif kind == "CX":
                    if state & (1 << wires[0]):
                        state ^= 1 << wires[1]
                    next_vector[state] = tuple(
                        x + y for x, y in zip(next_vector.get(state, zero), amplitude)
                    )
                else:
                    insist(kind in ("T", "Tdg"), "Only the exact source-bound CCX macro rows")
                    if state & (1 << wires[0]):
                        amplitude = (
                            (b - d, (a - c) / 2, b + d, (a + c) / 2)
                            if kind == "T"
                            else (b + d, (a + c) / 2, d - b, (c - a) / 2)
                        )
                    next_vector[state] = tuple(
                        x + y for x, y in zip(next_vector.get(state, zero), amplitude)
                    )
            vector = {state: value for state, value in next_vector.items() if value != zero}
            insist(len(vector) <= 8, "Fixed complete three-qubit macro dimension")
        output = basis ^ (((basis & 1) & ((basis >> 1) & 1)) << 2)
        insist(
            vector == {output: (Fraction(1), Fraction(), Fraction(), Fraction())},
            "Exact full CCX column: absolute phase+1 and every other amplitude zero",
        )
        columns.append(
            dict(
                input=basis,
                output=output,
                exact_nonzero_phase=1,
                all_other_output_amplitudes_exact_zero=True,
            )
        )
    return columns


class IndependentCircuit:
    """Fresh structural reconstruction from bit equations, without old builders."""

    def __init__(self):
        self.wires = 0
        self.rows = []

    def bank(self, size):
        checkpoint()
        insist(
            type(size) is int and 0 < size and self.wires + size <= WIRE_LIMIT,
            "Exact finite full-port bank allocation",
        )
        bank = tuple(range(self.wires, self.wires + size))
        self.wires += size
        return bank

    def append(self, kind, *ports):
        checkpoint()
        arity = {"X": 1, "CX": 2, "CCX": 3, "H": 1, "Z": 1, "CZ": 2}
        insist(
            kind in arity
            and len(ports) == arity[kind]
            and len(ports) == len(set(ports))
            and all(type(wire) is int and 0 <= wire < self.wires for wire in ports),
            "Every emitted native gate has allocated distinct ports",
        )
        insist(len(self.rows) < RECIPE_GATE_LIMIT, "Fixed per-recipe gate limit")
        self.rows.append([kind, *ports])

    def reverse(self, first, last):
        for row in reversed(self.rows[first:last]):
            self.append(*row)

    def publish(self, interfaces, ranges=None):
        ranges = {} if ranges is None else ranges
        ports = {key: list(bank) for key, bank in interfaces.items()}
        return {
            "schema": "A20-exact-native-gate-recipe-v2",
            "qubits": self.wires,
            "gates": self.rows,
            "interfaces": ports,
            "phase_ranges": ranges,
            "recipe_sha256": object_sha([self.wires, self.rows, ports, ranges]),
        }


def independent_add_rows(a, b, carry):
    """MAJ propagates majority; reversed UMA restores a/carry and adds into b."""
    insist(len(a) == len(b) and len(a) > 0, "Equal nonempty adder operands")
    rows = []
    triples = [(a[j], b[j], carry if j == 0 else a[j - 1]) for j in range(len(a))]
    for x, y, z in triples:
        rows.extend((["CX", x, y], ["CX", x, z], ["CCX", z, y, x]))
    for x, y, z in reversed(triples):
        rows.extend((["CCX", z, y, x], ["CX", x, z], ["CX", z, y]))
    return rows


def independent_comparison(circuit, a, b, flag):
    """Unsigned widened subtract, then sign bit XOR and exact uncomputation."""
    size = len(a)
    difference, extended = circuit.bank(size + 1), circuit.bank(size + 1)
    carry = circuit.bank(1)[0]
    start = len(circuit.rows)
    for source, target in zip(a, difference):
        circuit.append("CX", source, target)
    for source, target in zip(b, extended):
        circuit.append("CX", source, target)
    for row in reversed(independent_add_rows(extended, difference, carry)):
        circuit.append(*row)
    end = len(circuit.rows)
    circuit.append("CX", difference[-1], flag)
    circuit.reverse(start, end)


def independent_lookup(circuit, address, output, words):
    """All eight data rows, factored constant, explicit clean shared prefixes."""
    insist(
        len(address) == 3
        and len(words) == 8
        and all(type(word) is int and 0 <= word < REFERENCE_SIZE for word in words),
        "Restricted exact QROM data and address contract",
    )
    for bit, target in enumerate(output):
        if words[0] & (1 << bit):
            circuit.append("X", target)
    delta = [word ^ words[0] for word in words]
    if not any(delta):
        return
    stack = circuit.bank(2)

    def subtree(bit_index, prefix, offset):
        checkpoint()
        if not any(delta[offset : offset + (1 << (bit_index + 1))]):
            return
        if bit_index < 0:
            for j, wire in enumerate(output):
                if delta[offset] & (1 << j):
                    circuit.append("CX", prefix, wire)
            return
        flag, bit = stack[bit_index], address[bit_index]
        circuit.append("CCX", prefix, bit, flag)
        subtree(bit_index - 1, flag, offset + (1 << bit_index))
        circuit.append("CX", prefix, flag)
        subtree(bit_index - 1, flag, offset)
        circuit.append("CX", prefix, flag)
        circuit.append("CCX", prefix, bit, flag)

    subtree(1, address[2], 4)
    circuit.append("X", address[2])
    subtree(1, address[2], 0)
    circuit.append("X", address[2])


def independently_expected_recipes(words):
    """Recognize every source row, including controls, copies, H and inverses."""
    result = {}
    circuit = IndependentCircuit()
    a, b, out = circuit.bank(WIDTH), circuit.bank(WIDTH), circuit.bank(WIDTH)
    circuit.append("X", a[-1])
    circuit.append("X", b[-1])
    independent_comparison(circuit, a, b, out[0])
    circuit.append("X", a[-1])
    circuit.append("X", b[-1])
    result["native_signed_LT72"] = circuit.publish(dict(a=a, b=b, output=out))
    for controlled in (False, True):
        circuit = IndependentCircuit()
        address, out = circuit.bank(3), circuit.bank(WIDTH)
        independent_lookup(circuit, address, out, words)
        interfaces = dict(address=address, output=out)
        if controlled:
            original = circuit.rows
            circuit.rows = []
            control, scratch = circuit.bank(1)[0], circuit.bank(1)[0]
            interfaces["control"] = (control,)
            for kind, *ports in original:
                if kind == "X":
                    circuit.append("CX", control, *ports)
                elif kind == "CX":
                    circuit.append("CCX", control, *ports)
                else:
                    insist(kind == "CCX", "Only clean classical permutation lookup rows")
                    circuit.append("CCX", control, ports[0], scratch)
                    circuit.append("CCX", scratch, ports[1], ports[2])
                    circuit.append("CCX", control, ports[0], scratch)
        result[("controlled_" if controlled else "") + "QROM8_word72"] = circuit.publish(interfaces)
    result["controlled_one_stock53"] = independent_signal(None, WIDTH, REFERENCE_BITS)
    result["controlled_pair53"] = independent_signal(words, WIDTH, REFERENCE_BITS)
    return result, independent_signal(None, 3, 2)


def independent_signal(words, width, uniform_bits):
    circuit = IndependentCircuit()
    control, reference, stock = circuit.bank(1), circuit.bank(width), circuit.bank(width)
    predicate = circuit.bank(1)[0]
    ports = dict(control=control, reference=reference)
    if words is None:
        ports["stock"] = stock
    else:
        a0, a1, selector, selected = (
            circuit.bank(3),
            circuit.bank(3),
            circuit.bank(1),
            circuit.bank(3),
        )
        ports.update(address0=a0, address1=a1, selector=selector)
        circuit.append("H", selector[0])
        select_start = len(circuit.rows)
        for x, y, out in zip(a0, a1, selected):
            circuit.append("CX", x, out)
            circuit.append("CCX", selector[0], x, out)
            circuit.append("CCX", selector[0], y, out)
        select_end = len(circuit.rows)
        lookup_start = len(circuit.rows)
        independent_lookup(circuit, selected, stock, words)
        lookup_end = len(circuit.rows)
    transform_start = len(circuit.rows)
    for wire in reference[:uniform_bits]:
        circuit.append("H", wire)
    core_start = len(circuit.rows)
    compare_start = len(circuit.rows)
    circuit.append("X", reference[-1])
    circuit.append("X", stock[-1])
    independent_comparison(circuit, reference, stock, predicate)
    circuit.append("X", reference[-1])
    circuit.append("X", stock[-1])
    compare_end = len(circuit.rows)
    circuit.append("Z", control[0])
    circuit.append("CZ", control[0], predicate)
    circuit.reverse(compare_start, compare_end)
    core_end = len(circuit.rows)
    for wire in reference[:uniform_bits]:
        circuit.append("H", wire)
    transform_end = len(circuit.rows)
    ranges = dict(core=[core_start, core_end], reference_transform=[transform_start, transform_end])
    if words is not None:
        circuit.reverse(lookup_start, lookup_end)
        circuit.reverse(select_start, select_end)
        circuit.append("H", selector[0])
        ranges.update(selection=[select_start, select_end], lookup=[lookup_start, lookup_end])
    return circuit.publish(ports, ranges)


def independent_stock_sharing_signature(records):
    """Separate semantic comparison; keep original argument order for evaluation."""
    signature = []
    for record in records:
        checkpoint()
        arguments = tuple(record["args"])
        empty_parameters = type(record["params"]) is dict and len(record["params"]) == 0
        if record["op"] == "mul" and empty_parameters:
            insist(
                len(arguments) == 2 and all(type(number) is int for number in arguments),
                "Independent same-width parameter-free native mul commutation",
            )
            arguments = tuple(sorted(arguments))
        signature.append([record["op"], list(arguments), encoded(record["params"]), record["out"]])
    return encoded(signature)


def independently_prove_stock_sharing(templates):
    """Separate typed induction from both original source closures."""
    first, second = templates
    records0, records1 = first["normalized_nodes"], second["normalized_nodes"]
    insist(
        len(records0) == len(records1) == 45
        and first["output"] == second["output"] == 45
        and type(first["output"]) is type(second["output"]) is int
        and encoded(first["clamps"]) == encoded(second["clamps"]),
        "Independent fixed45-node source outputs and typed clamp equality",
    )
    rows, swaps = [], []
    comparisons = [[], []]
    for index in range(45):
        checkpoint()
        a, b = records0[index], records1[index]
        for column, record in enumerate((a, b)):
            insist(
                set(record) == {"op", "args", "params", "out"}
                and type(record["op"]) is str
                and type(record["params"]) is dict
                and type(record["args"]) is list
                and type(record["out"]) is int
                and record["out"] == index + 1
                and all(type(arg) is int and 0 <= arg < index + 1 for arg in record["args"]),
                "Independent typed predecessor IDs and full72/F40 source row",
            )
            args = record["args"].copy()
            if record["op"] == "mul" and not record["params"]:
                insist(len(args) == 2, "Independent recognized binary MUL")
                args.sort()
            comparisons[column].append(
                dict(op=record["op"], args=args, params=record["params"], out=record["out"])
            )
        same = encoded(a) == encoded(b)
        if not same:
            insist(
                a["op"] == b["op"] == "mul"
                and a["params"] == b["params"] == {}
                and len(a["args"]) == len(b["args"]) == 2
                and a["args"][0] == b["args"][1]
                and a["args"][1] == b["args"][0],
                "Independent only five empty-parameter same-width MUL reversals",
            )
            swaps.append(index)
        rows.append(
            dict(
                position_zero_based=index,
                output=a["out"],
                operation=a["op"],
                asset0_ordered_args=a["args"],
                asset1_ordered_args=b["args"],
                typed_parameters_sha256=object_sha(a["params"]),
                rule="identical_ordered_operation" if same else "full72_F40_MUL_commutativity",
                equal_predecessors_by_induction=True,
            )
        )
    insist(
        swaps == [10, 17, 21, 30, 34] and encoded(comparisons[0]) == encoded(comparisons[1]),
        "Independent complete typed induction with exactly fixed diagnosed swaps",
    )
    return {
        "schema": "A20-native72-F40-stock-function-sharing-proof-v1",
        "raw_template_identity": False,
        "raw_template_sha256": [t["template_sha256"] for t in templates],
        "semantic_signature_sha256": [object_sha(c) for c in comparisons],
        "node_count": 45,
        "swapped_positions_zero_based": swaps,
        "induction_rows": rows,
        "source_IR_MUL": "floor(signed72(a)*signed72(b)/2^40) mod2^72",
        "full_product_signed_bits": 144,
        "same_product_floor_mask_and_eager_guard_truth": True,
        "total_modular_function_equality_for_same_boundary_word": True,
        "partial_no_wrap_scalar_acceptance_equal": True,
        "raw_order_arrays_hashes_and_evaluation_preserved": True,
        "actual_asset_paths_equal_claim": False,
        "no_wrap_or_stock_support_proved_by_commutation": False,
        "old_MUL_gate_chronology_or_ordered_cost_equivalence": False,
        "full_source_cost_status": "NOT_FULL_SOURCE_COSTED",
        "new_test_credit": 0,
    }


def independent_mul_commutativity_qa():
    """Independent unsigned sign correction and Euclidean-floor oracle."""
    endpoints = (-(1 << 71), -(1 << 71) + 1, -UNIT - 1, -1, 0, 1, UNIT + 1, (1 << 71) - 1)
    modulus, product_modulus = 1 << 72, 1 << 144
    rows = []
    for a in endpoints:
        for b in endpoints:
            checkpoint()
            raw_a, raw_b = a % modulus, b % modulus
            sign_a, sign_b = raw_a >> 71, raw_b >> 71
            corrected = raw_a * raw_b - modulus * (sign_a * raw_b + sign_b * raw_a)
            corrected += product_modulus * sign_a * sign_b
            quotient, remainder = divmod(corrected, UNIT)
            reverse = raw_b * raw_a - modulus * (sign_b * raw_a + sign_a * raw_b)
            reverse += product_modulus * sign_b * sign_a
            decoded_a, decoded_b = raw_a - sign_a * modulus, raw_b - sign_b * modulus
            word = quotient % modulus
            window = (corrected % product_modulus // UNIT) % modulus
            insist(
                decoded_a == a
                and decoded_b == b
                and corrected == reverse == decoded_a * decoded_b
                and -(1 << 143) <= corrected < (1 << 143)
                and corrected == quotient * UNIT + remainder
                and 0 <= remainder < UNIT
                and word == window == (reverse // UNIT) % modulus,
                "Independent full144 symmetry, negative floor and retained72 window",
            )
            rows.append(
                dict(
                    a=a,
                    b=b,
                    full_signed_product=corrected,
                    floor_quotient=quotient,
                    word72=word,
                    retained144_window_word=window,
                    retained_no_wrap_guard=-(1 << 71) <= quotient < (1 << 71),
                )
            )
    insist(len(rows) == 64, "Independent exactly64 fixed reference pairs")
    return {
        "schema": "A20-native72-F40-MUL-commutativity-QA-v1",
        "pairs": rows,
        "fixed_scalar_pairs": 64,
        "new_MUL_gate_arrays": 0,
        "new_test_credit": 0,
        "full_source_cost_or_quantum_phase_proof": False,
    }


def independently_bind_stock(target, census):
    checkpoint()
    insist(
        type(target["width"]) is int
        and type(target["fraction_bits"]) is int
        and (target["width"], target["fraction_bits"]) == (WIDTH, FRACTION_BITS),
        "Original signed72/f40 source domain",
    )
    producer = {}
    for node in target["nodes"]:
        checkpoint()
        insist(
            type(node["op"]) is str
            and type(node["args"]) is list
            and type(node["out"]) is list
            and type(node["params"]) is dict,
            "Typed actual source node",
        )
        for value in node["out"]:
            insist(type(value) is int and value not in producer, "Unique actual SSA result")
            producer[value] = node
    templates = []
    for asset in (0, 1):
        occurrences = [
            row
            for row in census["builder_label_proof"]["exponentials"]
            if row["asset"] == asset and row["date"] == 0
        ]
        insist(len(occurrences) == 1, "One actual original occurrence per selected asset/date")
        occurrence = occurrences[0]
        anchor = occurrence["clipped_log"]
        order, seen = [], set()

        def collect(value):
            checkpoint()
            if value == anchor or value in seen:
                return
            insist(value in producer, "Actual scalar exponential dependency")
            node = producer[value]
            insist(
                node["op"] in {"const", "add", "sub", "mul", "cmul", "bits", "shift"}
                and node["out"] == [value],
                "Closed original scalar stock operations",
            )
            for arg in node["args"]:
                collect(arg)
            seen.add(value)
            order.append(node)
            insist(len(order) <= 64, "Fixed complete scalar closure")

        collect(occurrence["stock"])
        numbers, normalized = {anchor: 0}, []
        for node in order:
            checkpoint()
            key = node["out"][0]
            numbers[key] = len(numbers)
            normalized.append(
                dict(
                    op=node["op"],
                    args=[numbers[arg] for arg in node["args"]],
                    params=node["params"],
                    out=numbers[key],
                )
            )
        clips = [row for row in census["builder_label_proof"]["clips"] if row["out"] == anchor]
        insist(len(clips) == 1, "Exact selected original clamp")
        bounds = []
        for label in ("low", "high"):
            node = producer[clips[0][label]]
            insist(node["op"] == "const", "Native clamp literal")
            bounds.append(signed_word(node["params"]["value"]))
        templates.append(
            dict(
                asset=asset,
                date=0,
                clipped_log=anchor,
                stock=occurrence["stock"],
                clamps=bounds,
                normalized_nodes=normalized,
                output=numbers[occurrence["stock"]],
                template_sha256=object_sha(normalized),
            )
        )
    insist(
        independent_stock_sharing_signature(templates[0]["normalized_nodes"])
        == independent_stock_sharing_signature(templates[1]["normalized_nodes"])
        and encoded(templates[0]["clamps"]) == encoded(templates[1]["clamps"])
        and type(templates[0]["output"]) is type(templates[1]["output"]) is int
        and templates[0]["output"] == templates[1]["output"],
        "Typed scalar sharing; only empty-parameter native72/F40 MUL pairs commute",
    )
    return templates


def independent_stock_word(template, raw):
    insist(template["clamps"][0] <= raw <= template["clamps"][1], "Actual supported stock input")
    values = {0: raw}
    for row in template["normalized_nodes"]:
        checkpoint()
        op, p = row["op"], row["params"]
        args = [values[index] for index in row["args"]]
        if op == "const":
            value = signed_word(p["value"])
        elif op == "add":
            value = args[0] + args[1]
        elif op == "sub":
            value = args[0] - args[1]
        elif op in ("mul", "cmul"):
            multiplier = args[1] if op == "mul" else p["c"]
            insist(
                type(multiplier) is int and -(1 << 71) <= multiplier < 1 << 71,
                "Canonical signed CMUL/native operand",
            )
            product = args[0] * multiplier
            insist(-(1 << 143) <= product < 1 << 143, "Full signed144 product")
            value = product // UNIT
        elif op == "bits":
            shift, bits = p["shift"], p["width"]
            insist(
                type(shift) is int and type(bits) is int and 1 <= bits <= WIDTH,
                "Exact native bits window",
            )
            operand = args[0] if p.get("signed", False) else args[0] & WORD_MASK
            value = (operand >> shift if shift >= 0 else operand << -shift) & ((1 << bits) - 1)
            value = signed_word(value)
        else:
            insist(op == "shift" and -WIDTH < args[1] < WIDTH, "Actual native stock shift")
            value = args[0] << args[1] if args[1] >= 0 else args[0] >> -args[1]
        insist(
            type(value) is int and -(1 << 71) <= value < 1 << 71,
            "Every eagerly retained scalar node fits signed72 without wrap",
        )
        values[row["out"]] = value
    word = values[template["output"]]
    insist(0 <= word < REFERENCE_SIZE, "Source-bound exact nonnegative F below fixed MQ")
    return word


def write_word(state, wires, word):
    insist(type(word) is int and 0 <= word < 1 << len(wires), "Canonical interface word")
    for bit, wire in enumerate(wires):
        if word & (1 << bit):
            state |= 1 << wire
    return state


def read_word(state, wires):
    return sum(((state >> wire) & 1) << bit for bit, wire in enumerate(wires))


def initial_state(recipe, inputs):
    state = 0
    for name, value in inputs.items():
        state = write_word(state, recipe["interfaces"][name], value)
    return state


def basis_action(recipe, inputs, rows=None, reverse=False):
    """Actual array traversal, with absolute Z/CZ phase and all scratch checked."""
    initial = initial_state(recipe, inputs)
    state, phase = initial, 1
    rows = recipe["gates"] if rows is None else rows
    if reverse:
        rows = reversed(rows)
    for kind, *ports in rows:
        gate_visit()
        if kind in ("X", "CX", "CCX"):
            if all((state >> wire) & 1 for wire in ports[:-1]):
                state ^= 1 << ports[-1]
        else:
            insist(kind in ("Z", "CZ"), "Basis checker never drops or executes an H")
            if all((state >> wire) & 1 for wire in ports):
                phase *= -1
    occupied = {wire for bank in recipe["interfaces"].values() for wire in bank}
    insist(
        not state & sum(1 << wire for wire in range(recipe["qubits"]) if wire not in occupied),
        "Every private wire restored after actual basis traversal",
    )
    return state, initial, phase


def amplitude_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def sparse_operator(recipe, inputs):
    """Independent exact a+b*sqrt(2) representation using rational components."""
    initial = initial_state(recipe, inputs)
    vector = {initial: (Fraction(1), Fraction())}
    for kind, *ports in recipe["gates"]:
        checkpoint()
        next_vector = {}
        for state, amplitude in vector.items():
            gate_visit()
            if kind == "H":
                wire = ports[0]
                transformed = amplitude[1], amplitude[0] / 2
                zero, one = state & ~(1 << wire), state | (1 << wire)
                sign = -1 if state & (1 << wire) else 1
                next_vector[zero] = amplitude_add(
                    next_vector.get(zero, (Fraction(), Fraction())), transformed
                )
                next_vector[one] = amplitude_add(
                    next_vector.get(one, (Fraction(), Fraction())),
                    (sign * transformed[0], sign * transformed[1]),
                )
            else:
                if kind in ("X", "CX", "CCX"):
                    if all((state >> wire) & 1 for wire in ports[:-1]):
                        state ^= 1 << ports[-1]
                else:
                    insist(kind in ("Z", "CZ"), "Recognized exact phase op")
                    if all((state >> wire) & 1 for wire in ports):
                        amplitude = -amplitude[0], -amplitude[1]
                # Every admitted non-H row is an injective basis permutation
                # times an exact sign. Preserve its amplitude directly; only
                # H rows require additions from colliding output branches.
                insist(state not in next_vector, "Exact non-H basis action is injective")
                next_vector[state] = amplitude
        vector = {state: amp for state, amp in next_vector.items() if amp != (0, 0)}
        insist(len(vector) <= 8, "No full53/full72 statevector; fixed tiny sparse support")
    return vector, initial


def independently_count_resources(recipe):
    counts = Counter()
    ct, td = [0] * recipe["qubits"], [0] * recipe["qubits"]
    for kind, *ports in recipe["gates"]:
        checkpoint()
        counts[kind] += 1
        duration = 15 if kind == "CCX" else 3 if kind == "CZ" else 1
        end = max(ct[wire] for wire in ports) + duration
        tend = max(td[wire] for wire in ports) + (7 if kind == "CCX" else 0)
        for wire in ports:
            ct[wire], td[wire] = end, tend
    return dict(
        qubits=recipe["qubits"],
        source_gates=len(recipe["gates"]),
        native_counts={kind: counts[kind] for kind in ("X", "CX", "CCX", "H", "Z", "CZ")},
        exact_CCX_T_count=7 * counts["CCX"],
        expanded_Clifford_CX=counts["CX"] + 6 * counts["CCX"] + counts["CZ"],
        expanded_Clifford_H=counts["H"] + 2 * counts["CCX"] + 2 * counts["CZ"],
        expanded_Clifford_Z=counts["Z"],
        conservative_T_depth_upper=max(td, default=0),
        conservative_Clifford_T_depth_upper=max(ct, default=0),
        schedule_scope=(
            "conservative recipe-only dependency upper bounds; "
            "not measured full-source or physical schedule"
        ),
        all_lookup_copy_inverse_phase_and_preparation_gates_charged=True,
    )


def independent_universal_obligations():
    """Finite Boolean identities plus induction explain recognized whole-width recipes."""
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                checkpoint()
                x, y, z = a, b ^ a, c ^ a
                x ^= z & y
                insist(x == int(a + b + c >= 2), "MAJ computes exact carry")
                x ^= z & y
                z ^= x
                y ^= z
                insist(
                    (x, y, z) == (a, (a + b + c) % 2, c),
                    "UMA restores operand/carry and leaves exact sum bit",
                )
                rows.append(
                    dict(a=a, b=b, carry=c, majority=int(a + b + c >= 2), sum_bit=(a + b + c) % 2)
                )
    return {
        "recognized_actual_arrays_equal_independent_recipe": True,
        "local_MAJ_UMA_boolean_identities": rows,
        "whole_width_induction": (
            "MAJ ripples the carry through every operand bit; "
            "reversed UMA restores all a/carry bits "
            "and stores a+b modulo2^n in b. Its literal inverse subtracts. Copying unsigned n-bit "
            "a,b into n+1 zero words makes a-b lie in[-(2^n-1),2^n-1]; the top bit is exactly a<b. "
            "XOR-copy that bit then literal-invert the subtract/copies restores every scratch bit. "
            "Flipping both signed operand MSBs maps signed order to unsigned order and is undone."
        ),
        "QROM_induction": (
            "At each address prefix, CCX creates prefix*bit; CX(prefix,flag) switches to "
            "prefix*(1-bit); inverse CX/CCX restores zero. Leaf CX writes exactly the residual "
            "word, factored base X writes row0. The two top-MSB branches cover all8 addresses. "
            "Controlling X/CX directly and CCX with a fresh zero temporary implements each "
            "original permutation iff the external control is1, with exact temporary cleanup."
        ),
        "controlled_phase": "Z(c)CZ(c,p)=(-1)^(c*(1+p)); equals+1 for c0 or p1 and-1 for c1,p0",
        "reference_counting": (
            "For every integer0<=F<2^53, exactly F padded53-bit reference states satisfy r<F"
        ),
        "one_stock_zero_block": "2*F/2^53-1",
        "selector_zero_block": (
            "(F1+F2)/2^53-1; coherent selector amplitudes, not averaged probabilities"
        ),
        "uncontrolled_compute_uncompute_valid": (
            "Controls and selected input words do not change "
            "between exact comparator and its literal inverse"
        ),
        "absolute_phase_source_CCX_premise_required": True,
        "finite_diagnostics_are_not_substituted_for_universal_induction": True,
    }


def independent_component(source_result, target, census, support):
    """Every fixed semantic/basis/operator row is recomputed, never sampled."""
    templates = independently_bind_stock(target, census)
    insist(
        encoded(source_result["templates"]) == encoded(templates),
        "Independent exact JSON typed original ordered template binding",
    )
    sharing = independently_prove_stock_sharing(templates)
    commutativity = independent_mul_commutativity_qa()
    insist(
        encoded(sharing) == encoded(source_result["stock_function_sharing_proof"])
        and encoded(commutativity) == encoded(source_result["MUL_commutativity_QA"]),
        "Independent typed45-node induction and all64 commutativity reference pairs",
    )
    lo, hi = templates[0]["clamps"]
    knots = [lo, lo + 1, 0, UNIT, 4 * UNIT, 5 * UNIT, hi - 1, hi]
    insist(
        len(set(knots)) == 8 and all(lo <= raw <= hi for raw in knots), "Fixed eight stock knots"
    )
    insist(
        support["passed"] is True and support["actual_stock_templates_checked"] == 48,
        "Exact source-bound B4 support premise",
    )
    cells = support["range_reduction_cells"]
    insist(
        cells
        and all(
            0 <= row["stock_interval"][0] <= row["stock_interval"][1] < REFERENCE_SIZE
            for row in cells
        ),
        "Full preserved native stock support below fixed M",
    )
    words = [independent_stock_word(templates[0], raw) for raw in knots]
    insist(
        source_result["knots_raw"] == knots and source_result["native_words"] == words,
        "All eight original stock values independently recomputed",
    )
    recipes, tiny = independently_expected_recipes(words)
    insist(
        source_result["recipes"] == recipes and source_result["tiny_recipe"] == tiny,
        "All actual gate/wire/port/range/recipe-SHA rows exactly recognized",
    )
    insist(
        source_result["tiny_resource"] == independently_count_resources(tiny),
        "Separately counted tiny test recipe, never a native53/full-source schedule",
    )
    semantic = []
    for i, a in enumerate(words):
        for j, b in enumerate(words):
            checkpoint()
            total = a + b
            insist(total < 1 << 71, "Native positive sum72 no wrap")
            semantic.append(
                dict(
                    i=i,
                    j=j,
                    F1=a,
                    F2=b,
                    native_basket_raw=total // 2,
                    alive=total < 280 * UNIT,
                    positive=total >= 200 * UNIT + 2,
                    one_stock_count_first=a,
                    one_stock_count_second=b,
                    pair_signal_exact=[total - REFERENCE_SIZE, REFERENCE_SIZE],
                )
            )
    minimum = min(row["stock_interval"][0] for row in cells)
    maximum = max(row["stock_interval"][1] for row in cells)
    boundary_rows = []
    for name, center, offsets in (
        ("barrier", 280 * UNIT, (-1, 0, 1)),
        ("strike", 200 * UNIT, (-1, 0, 1, 2, 3)),
    ):
        for offset in offsets:
            total = center + offset
            a, b = total // 2, total - total // 2
            insist(
                minimum <= a <= maximum and minimum <= b <= maximum,
                "Fixed native interface boundary inside saved envelope, no preimage claim",
            )
            insist(
                (total // 2 < 140 * UNIT) == (total < 280 * UNIT)
                and (total // 2 > 100 * UNIT) == (total >= 200 * UNIT + 2),
                "Exact native strict-barrier/positive-strike ties",
            )
            boundary_rows.append(
                dict(
                    label=name,
                    offset=offset,
                    sum=total,
                    F1=a,
                    F2=b,
                    alive=total // 2 < 140 * UNIT,
                    positive=total // 2 > 100 * UNIT,
                )
            )
    for a, b in ((90 * UNIT, 90 * UNIT), (50 * UNIT, 162 * UNIT)):
        insist(
            minimum <= a <= maximum and minimum <= b <= maximum,
            "Fixed equal-product diagnostic support",
        )
        boundary_rows.append(
            dict(
                label="equal_product",
                F1=a,
                F2=b,
                native_basket_raw=(a + b) // 2,
                alive=(a + b) // 2 < 140 * UNIT,
                positive=(a + b) // 2 > 100 * UNIT,
            )
        )
    insist(
        source_result["rows"] == semantic and source_result["boundary_cases"] == boundary_rows,
        "All64 and10 raw semantic rows, no ideal substitutions",
    )
    checks = []
    for family in ("QROM8_word72", "controlled_QROM8_word72"):
        recipe = recipes[family]
        for address in range(8):
            for dirty in DIRTY_OUTPUTS:
                for control in (0, 1) if "control" in recipe["interfaces"] else (1,):
                    inputs = dict(address=address, output=dirty)
                    if "control" in recipe["interfaces"]:
                        inputs["control"] = control
                    state, initial, phase = basis_action(recipe, inputs)
                    output = read_word(state, recipe["interfaces"]["output"])
                    insist(
                        output == dirty ^ (words[address] if control else 0)
                        and read_word(state, recipe["interfaces"]["address"]) == address
                        and phase == 1,
                        "All dirty QROM controlled/noncontrolled outputs/phase",
                    )
                    restored, _, inverse_phase = basis_action(
                        recipe, dict(inputs, output=output), reverse=True
                    )
                    insist(
                        restored == initial and inverse_phase == 1, "Actual literal QROM inverse"
                    )
                    checks.append(
                        dict(family=family, address=address, dirty=dirty, control=control)
                    )
    recipe = recipes["native_signed_LT72"]
    for a, b in tuple((a, b) for a in BOUNDARIES for b in BOUNDARIES) + SIGNED_BOUNDARIES:
        for dirty in DIRTY_OUTPUTS:
            inputs = dict(a=a & WORD_MASK, b=b & WORD_MASK, output=dirty)
            state, initial, phase = basis_action(recipe, inputs)
            output = read_word(state, recipe["interfaces"]["output"])
            insist(
                output == dirty ^ int(a < b)
                and read_word(state, recipe["interfaces"]["a"]) == (a & WORD_MASK)
                and read_word(state, recipe["interfaces"]["b"]) == (b & WORD_MASK)
                and phase == 1,
                "Full signed72 comparator absolute phase/dirty-output ABI",
            )
            restored, _, inverse_phase = basis_action(
                recipe, dict(inputs, output=output), reverse=True
            )
            insist(restored == initial and inverse_phase == 1, "Literal comparator inverse")
            checks.append(dict(family="native_signed_LT72", a=a, b=b, dirty=dirty))
    recipe = recipes["controlled_one_stock53"]
    first, last = recipe["phase_ranges"]["core"]
    for stock in BOUNDARIES:
        for reference in BOUNDARIES:
            for control in (0, 1):
                state, initial, phase = basis_action(
                    recipe,
                    dict(control=control, reference=reference, stock=stock),
                    rows=recipe["gates"][first:last],
                )
                insist(
                    state == initial and phase == (1 if control == 0 or reference < stock else -1),
                    "Actual53-reference native controlled phase, ties and all scratch",
                )
                checks.append(dict(family="native53_phase", F=stock, r=reference, control=control))
    for stock in range(4):
        for reference in range(4):
            for control in (0, 1):
                vector, initial = sparse_operator(
                    tiny, dict(control=control, reference=reference, stock=stock)
                )
                expected_states = set()
                reference_mask = sum(1 << wire for wire in tiny["interfaces"]["reference"])
                for output in range(4):
                    expected = (
                        Fraction(int(output == reference))
                        if control == 0
                        else sum(
                            (
                                Fraction(1 if r < stock else -1, 4)
                                * (-1) ** (((reference ^ output) & r).bit_count())
                                for r in range(4)
                            ),
                            Fraction(),
                        )
                    )
                    state = (initial & ~reference_mask) | write_word(
                        0, tiny["interfaces"]["reference"], output
                    )
                    insist(
                        vector.get(state, (Fraction(), Fraction())) == (expected, 0),
                        "Independent complete tiny Walsh/counting operator "
                        "with absolute control phase",
                    )
                    if expected:
                        expected_states.add(state)
                insist(
                    set(vector) == expected_states, "All tiny inputs and private wires preserved"
                )
                checks.append(
                    dict(family="tiny_complete_operator", F=stock, r=reference, control=control)
                )
    recipe = recipes["controlled_pair53"]
    reference_wires = set(recipe["interfaces"]["reference"])
    removed = [
        j for j, row in enumerate(recipe["gates"]) if row[0] == "H" and row[1] in reference_wires
    ]
    insist(len(removed) == 106, "Both actual53-H layers retained and charged")
    removed_set = set(removed)
    test_view = dict(
        recipe, gates=[row for j, row in enumerate(recipe["gates"]) if j not in removed_set]
    )
    for i, a in enumerate(words):
        for j, b in enumerate(words):
            for reference in BOUNDARIES:
                for control in (0, 1):
                    for selector in (0, 1):
                        vector, initial = sparse_operator(
                            test_view,
                            dict(
                                address0=i,
                                address1=j,
                                reference=reference,
                                control=control,
                                selector=selector,
                            ),
                        )
                        phases = [1 if control == 0 or reference < word else -1 for word in (a, b)]
                        expected_states = set()
                        for output in (0, 1):
                            state = initial ^ (
                                (selector ^ output) << recipe["interfaces"]["selector"][0]
                            )
                            expected = Fraction(
                                phases[0] + phases[1]
                                if output == selector
                                else phases[0] - phases[1],
                                2,
                            )
                            insist(
                                vector.get(state, (Fraction(), Fraction())) == (expected, 0),
                                "Actual pair selected lookup/phase/inverse/H all-wire tiny view",
                            )
                            if expected:
                                expected_states.add(state)
                        insist(
                            set(vector) == expected_states,
                            "All native pair input and scratch restoration",
                        )
                        checks.append(
                            dict(
                                family="native53_pair_phase",
                                i=i,
                                j=j,
                                r=reference,
                                control=control,
                                selector=selector,
                            )
                        )
    insist(
        len(checks) == 2608 and checks == source_result["checks"],
        "Exact independent2608 fixed component checks",
    )
    resources = {name: independently_count_resources(recipe) for name, recipe in recipes.items()}
    insist(
        resources == source_result["resources"],
        "Every actual control/lookup/copy/inverse/H/phase cost independently counted",
    )
    view = dict(
        source_recipe_sha256=recipe["recipe_sha256"],
        removed_reference_H_indices=removed,
        removed_gates_counted_in_actual_cost=True,
        not_a_full53_statevector=True,
    )
    insist(
        source_result["native_pair_phase_test_view"] == view,
        "Only the declared106-H test-view deletion",
    )
    count_proof = dict(
        uniform_reference_bits=53,
        uniform_states=REFERENCE_SIZE,
        positive_phase_states_for_F="exactly F",
        one_stock_signal="(2F-MQ)/MQ",
        pair_signal="(F1+F2-MQ)/MQ",
        guaranteed_integer_half_threshold_gap=[1, 2 * REFERENCE_SIZE],
        no_53bit_statevector=True,
    )
    insist(
        source_result["exact_counting_proof"] == count_proof, "Exact whole-reference counting proof"
    )
    insist(
        source_result["offline_native_scalar_evaluations"] == 8
        and source_result["offline_pair_truth_records"] == 64,
        "All paid offline source words/pairs retained",
    )
    return dict(
        templates=templates,
        stock_function_sharing_proof=sharing,
        MUL_commutativity_QA=commutativity,
        native_words=words,
        knots_raw=knots,
        independent_semantic_rows=semantic,
        independent_boundary_cases=boundary_rows,
        independent_component_checks=checks,
        independent_resources=resources,
        universal_obligations=independent_universal_obligations(),
        counting_proof=count_proof,
        native_pair_phase_test_view=view,
        exact_gate_state_visits=VISITS,
        complete_source_cost_or_adoption=False,
        no_new_fixture_credit=True,
    )


SELECTED_PREMISES = {
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


def read_source_groups(receipt, directory):
    checkpoint()
    binding = receipt.read(directory / "source_binding.json")
    truth = receipt.read(directory / "native_truth.json")
    gates = receipt.read(directory / "gate_recipes.json")
    checks = receipt.read(directory / "component_checks.json")
    counting = receipt.read(directory / "exact_counting_proof.json")
    resources = receipt.read(directory / "resource_ledger.json")
    sharing = receipt.read(directory / "stock_function_sharing.json")
    insist(
        binding["schema"] == "A20-restricted-native-stock-source-binding-v2"
        and binding["selected_expected_sha256"] == receipt.ready["selected_prerequisite_sha256"]
        and binding["offline_truth_construction_charged"] is True
        and binding["general_q32_reachability_or_law_claim"] is False,
        "Exact producer source-binding scope and unchanged expected pins",
    )
    insist(
        truth["boundary_words_are_interface_only_not_proven_reachable"] is True,
        "No restricted interface-to-path reachability transfer",
    )
    insist(
        gates["schema"] == "A20-exact-paid-gate-recipes-v2"
        and gates["one_component_construction"] is True
        and gates["original_word_width"] == 72
        and gates["original_fractional_bits"] == 40
        and gates["native_reference_bits"] == 53
        and gates["reference_upper19_zero_promised"] is True
        and gates["reference_and_selector_block_output_garbage_allowed"] is True
        and gates["stock_address_and_internal_scratch_restored"] is True
        and gates["full_pricing_source_emitted"] is False,
        "Native signal ABI and full-source nonclaim",
    )
    families = {
        "QROM8_word72": 32,
        "controlled_QROM8_word72": 64,
        "native_signed_LT72": 304,
        "native53_phase": 128,
        "tiny_complete_operator": 32,
        "native53_pair_phase": 2048,
    }
    insist(
        checks["total_internal_checks"] == 2608
        and checks["new_test_credit"] == 0
        and checks["internal_checks_are_not_distinct_pytest_or_financial_fixtures"] is True
        and checks["native53_pair_tests_are_H_removed_reference_test_view"] is True
        and checks["family_counts"] == families
        and dict(Counter(row["family"] for row in checks["checks"])) == families
        and type(checks["exact_gate_state_visits"]) is int
        and 0 < checks["exact_gate_state_visits"] <= VISIT_LIMIT,
        "All fixed source checks retained with honest zero fixture credit",
    )
    insist(
        counting["reference_upper19_zero_promised"] is True
        and counting["strict_F_domain"] == [0, REFERENCE_SIZE - 1]
        and counting["control_zero_full_identity"] is True
        and counting["threshold_transform_or_full_pricing_oracle_supplied"] is False,
        "Counting premise, control phase and threshold scope",
    )
    insist(
        resources["offline_native_evaluations"] == 8
        and resources["offline_pair_truth_records"] == 64
        and resources["constructed_recipe_count_including_tiny"] == 6
        and resources["native_CCX_absolute_phase_and_seven_T_paid"] is True
        and resources["QROM_address_selection_copy_cleanup_and_H_Z_CZ_paid"] is True
        and resources["depths_are_conservative_recipe_upper_bounds_not_full_source_schedules"]
        is True
        and resources["classical_offline_build_storage_and_load_amortization_not_assumed_free"]
        is True,
        "Exact charged component cost scope",
    )
    for name in (
        "component_work_CPU_seconds_including_emission_and_checks",
        "component_work_wall_seconds_including_emission_and_checks",
    ):
        observation = resources[name]
        insist(
            type(observation) in (int, float)
            and 0 <= observation
            and observation < (180 if "CPU" in name else 600),
            "Finite recorded producer component observation, no measured-price timing",
        )
    expected_scope = {
        "status": "NOT_FULL_SOURCE_COSTED",
        "general_full72_or_q32_oracle_supplied": False,
        "threshold_transform_supplied": False,
        "new_financial_bias_allocation": None,
        "arithmetic_removal_or_adoption": False,
    }
    insist(
        resources["whole_source_comparison"] == expected_scope,
        "No arithmetic removal, financial or full-source cost approval",
    )
    count_keys = (
        "uniform_reference_bits",
        "uniform_states",
        "positive_phase_states_for_F",
        "one_stock_signal",
        "pair_signal",
        "guaranteed_integer_half_threshold_gap",
        "no_53bit_statevector",
    )
    return {
        "templates": binding["templates"],
        "stock_function_sharing_proof": sharing["proof"],
        "MUL_commutativity_QA": sharing["commutativity_QA"],
        "knots_raw": binding["knots_raw"],
        "native_words": binding["native_words"],
        "offline_native_scalar_evaluations": binding["offline_native_scalar_evaluations"],
        "rows": truth["rows"],
        "boundary_cases": truth["boundary_cases"],
        "offline_pair_truth_records": truth["offline_pair_truth_records"],
        "recipes": gates["recipes"],
        "tiny_recipe": gates["tiny_recipe"],
        "checks": checks["checks"],
        "native_pair_phase_test_view": checks["native_pair_phase_test_view"],
        "resources": resources["resources"],
        "tiny_resource": resources["tiny_resource"],
        "exact_counting_proof": {name: counting[name] for name in count_keys},
    }


def run_independent_audit(receipt, protocol, program, research):
    global ADMITTED_CHECK, VISITS
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    receipt.check(admission=True)
    ADMITTED_CHECK, VISITS = receipt.check, 0
    source = program / "A20_signal_semantics_run005"
    for name in ("summary.json", "completion_outcome.json"):
        terminal = receipt.read(source / name)
        insist(
            terminal["schema"] == "A20-comparator-phase-component-summary-v5"
            and terminal["role"] == "producer"
            and terminal["component_semantics_verified"] is True
            and terminal["independent_audit_still_required"] is True
            and terminal["restricted_pair_truth_rows"] == 64
            and terminal["interface_boundary_cases"] == 10
            and terminal["general_full72_or_q32_oracle"] is False
            and terminal["threshold_QSP_transform"] is False
            and terminal["complete_financial_bias_allocation"] is None
            and terminal["new_gate_replay_credit"] == 0
            and terminal["new_financial_replay_credit"] == 0
            and terminal["quantum_advantage"] is False,
            "Source component success is a bounded access result, no source-finance approval",
        )
    groups = read_source_groups(receipt, source)
    phase = phase_binding(
        receipt.read(program / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"),
        receipt.read_bytes(research / "temporary_and_fulladder.py"),
    )
    insist(
        receipt.read(source / "phase_premise.json") == phase,
        "Independent literal exact-phase macro and sealed eight-column premise",
    )
    full_phase_columns = independent_ccx_phase_columns(phase["macro"])
    work_cpu, work_wall = time.process_time(), time.monotonic()
    result = independent_component(
        groups,
        receipt.read(program / "A10_coefficient_run001/B4x12/min-depth/target.json"),
        receipt.read(program / "E22_census_run002/B4x12_predicate_census.json"),
        receipt.read(program / "E03_support_audit_run002/B4x12_audit.json"),
    )
    elapsed_cpu, elapsed_wall = time.process_time() - work_cpu, time.monotonic() - work_wall
    receipt.check(admission=True)
    receipt.write(
        "independent_source_binding.json",
        {
            "templates": result["templates"],
            "knots_raw": result["knots_raw"],
            "native_words": result["native_words"],
            "offline_native_scalar_evaluations": 8,
            "all_actual_original_dependency_order_and_literals_bound": True,
            "general_q32_reachability_or_law_claim": False,
        },
    )
    receipt.write(
        "independent_stock_function_sharing.json",
        {
            "proof": result["stock_function_sharing_proof"],
            "commutativity_QA": result["MUL_commutativity_QA"],
        },
    )
    receipt.write(
        "independent_native_truth.json",
        {
            "rows": result["independent_semantic_rows"],
            "boundary_cases": result["independent_boundary_cases"],
            "offline_pair_truth_records": 64,
        },
    )
    receipt.write(
        "independent_component_checks.json",
        {
            "checks": result["independent_component_checks"],
            "internal_component_checks": 2608,
            "exact_gate_state_visits": result["exact_gate_state_visits"],
            "native_pair_phase_test_view": result["native_pair_phase_test_view"],
            "full_native_arrays_recognized_and_reexecuted": True,
            "all_private_wires_and_inputs_preserved": True,
            "absolute_controlled_phase_checked": True,
            "finite_checks_not_whole_q32_or_financial_fixtures": True,
            "new_test_credit": 0,
        },
    )
    receipt.write(
        "independent_counting_and_structural_proof.json",
        {
            "exact_counting_proof": result["counting_proof"],
            "universal_obligations": result["universal_obligations"],
            "phase_premise": phase,
            "independent_exact_CCX_full_operator_columns": full_phase_columns,
            "integer_half_gap_applies_to_affine_pair_signal_only": True,
            "no_threshold_polynomial_or_QSP_transform_approval": True,
        },
    )
    receipt.write(
        "independent_resource_ledger.json",
        {
            "resources": result["independent_resources"],
            "tiny_resource": independently_count_resources(groups["tiny_recipe"]),
            "whole_source_comparison": {
                "status": "NOT_FULL_SOURCE_COSTED",
                "general_full72_or_q32_oracle_supplied": False,
                "threshold_transform_supplied": False,
                "new_financial_bias_allocation": None,
                "arithmetic_removal_or_adoption": False,
            },
            "independent_work_CPU_seconds": elapsed_cpu,
            "independent_work_wall_seconds": elapsed_wall,
            "depths_are_conservative_recipe_upper_bounds_not_measured_full_source": True,
            "every_control_lookup_copy_inverse_and_preparation_gate_counted": True,
        },
    )
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    summary = {
        "schema": "A20-comparator-phase-independent-audit-summary-v6",
        "role": "audit",
        "completed": True,
        "passed": True,
        "budget_censored": False,
        "component_semantics_verified": True,
        "independent_audit": True,
        "source_manifest_sha256": receipt.ready["producer_manifest_sha256"],
        "source_author_pair": {
            key: pin
            for key, pin in receipt.ready["author_sha256"].items()
            if Path(key).name
            in (
                "experiment_arithmetic_free_basket_signal_v6.py",
                "arithmetic_free_basket_signal_v5.py",
            )
        },
        "independent_source_template_reconstruction": True,
        "independent_recipe_reconstruction_and_actual_array_traversal": True,
        "universal_structural_and_absolute_phase_premises_verified": True,
        "internal_component_checks": 2608,
        "separate_MUL_commutativity_scalar_pairs": 64,
        "typed_stock_function_induction_nodes": 45,
        "raw_template_identity": False,
        "offline_native_scalar_evaluations": 8,
        "restricted_pair_truth_rows": 64,
        "interface_boundary_cases": 10,
        "general_full72_or_q32_oracle": False,
        "threshold_QSP_transform": False,
        "complete_financial_bias_allocation": None,
        "full_G2": False,
        "new_test_credit": 0,
        "new_gate_replay_credit": 0,
        "new_financial_replay_credit": 0,
        "adoption": False,
        "quantum_advantage": False,
        "original_scientific_precision_and_strict_ties_retained": True,
        "physical_runtime": None,
        "process_CPU_seconds_at_preseal_checkpoint": time.process_time(),
        "creation_clock_wall_seconds_at_preseal_checkpoint": time.monotonic() - receipt.started,
    }
    receipt.seal(summary)


def independent_proof_ast_guard(receipt):
    """Compare admitted text only; no historical code import or parsed AST execution."""
    receipt.check()
    original = ast.parse(receipt.read_bytes(RESEARCH / "audit_arithmetic_free_basket_signal_v5.py"))
    current = ast.parse(receipt.read_bytes(RESEARCH / V6_AUDIT_AUTHOR_NAMES[0]))
    original_proofs = [
        node
        for node in original.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        and node.name not in ("main", "run_independent_audit")
    ]
    require(len(original_proofs) == 29, "All original independent proof definitions retained")
    current_proofs = []
    for prior in original_proofs:
        receipt.check()
        matches = [
            node
            for node in current.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == prior.name
        ]
        require(
            len(matches) == 1
            and ast.dump(matches[0], include_attributes=False)
            == ast.dump(prior, include_attributes=False),
            "Every whole original independent proof definition has exact unchanged AST",
        )
        current_proofs.append(matches[0])
    proof_dump = ast.dump(
        ast.Module(body=current_proofs, type_ignores=[]), include_attributes=False
    )
    require(
        hashlib.sha256(proof_dump.encode()).hexdigest() == V5_INDEPENDENT_PROOF_AST_SHA,
        "Fixed ordered29 independent proof AST pin",
    )
    for prior in original.body:
        if not isinstance(prior, ast.Assign):
            continue
        receipt.check()
        names = [target.id for target in prior.targets if isinstance(target, ast.Name)]
        require(len(names) == 1, "Original independent scientific constant assignment")
        matches = [
            node
            for node in current.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == names[0] for target in node.targets
            )
        ]
        require(
            len(matches) == 1
            and ast.dump(matches[0], include_attributes=False)
            == ast.dump(prior, include_attributes=False),
            "All independent literals, limits, input corpora and initial counters exact",
        )
    replacements = {
        "A20_signal_semantics_run005": "A20_signal_semantics_run004",
        "A20-comparator-phase-independent-audit-summary-v6": (
            "A20-comparator-phase-independent-audit-summary-v5"
        ),
        "experiment_arithmetic_free_basket_signal_v6.py": (
            "experiment_arithmetic_free_basket_signal_v5.py"
        ),
    }

    class Inverse(ast.NodeTransformer):
        def __init__(self):
            self.counts = {key: 0 for key in replacements}

        def visit_Constant(self, node):
            if type(node.value) is str and node.value in replacements:
                self.counts[node.value] += 1
                return ast.copy_location(ast.Constant(value=replacements[node.value]), node)
            return node

    def wrapper(module):
        matches = [
            node
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name == "run_independent_audit"
        ]
        require(len(matches) == 1, "One complete independent audit orchestration definition")
        return matches[0]

    inverse = Inverse()
    restored = inverse.visit(ast_copy.deepcopy(wrapper(current)))
    wrapper_dump = ast.dump(restored, include_attributes=False)
    require(
        all(value == 1 for value in inverse.counts.values())
        and wrapper_dump == ast.dump(wrapper(original), include_attributes=False)
        and hashlib.sha256(wrapper_dump.encode()).hexdigest()
        == "3aa5c2e81c01892e35631f66483ebac664fa2ddcc16e1c305fba989f9b326f49",
        "Whole original audit wrapper inverse exact with only three operational literals",
    )
    receipt.check()
    return {
        "schema": "A20-v6-independent-proof-AST-guard-v1",
        "whole_original_independent_proof_definitions": 29,
        "ordered_independent_proof_AST_SHA256": V5_INDEPENDENT_PROOF_AST_SHA,
        "wrapper_inverse_AST_SHA256": (
            "3aa5c2e81c01892e35631f66483ebac664fa2ddcc16e1c305fba989f9b326f49"
        ),
        "wrapper_operational_literal_counts": inverse.counts,
        "all_scientific_corpora_precision_costs_counters_unchanged": True,
        "no_historical_source_import_or_AST_execution": True,
        "new_test_credit": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--ready", required=True)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    arguments = parser.parse_args()
    receipt = None
    try:
        receipt = Receipt("audit", arguments.ready, arguments.ready_sha256, arguments.mode)
        insist(
            all(
                receipt.ready["selected_prerequisite_sha256"].get(key) == pin
                for key, pin in SELECTED_PREMISES.items()
            ),
            "Unchanged original independent helper/census/exact-phase expected source pins",
        )
        if arguments.mode == "prepare":
            insist(arguments.protocol_sha256 is None, "No protocol pin before fresh audit prepare")
            print("PREPARED_PROTOCOL_SHA256=" + receipt.prepare())
        else:
            insist(
                arguments.protocol_sha256 is not None,
                "Actual new independently reviewed prepared audit protocol pin required",
            )
            protocol = receipt.admit_run(arguments.protocol_sha256)
            insist(
                protocol["operational_recovery_version"] == 6
                and protocol["immutable_recovery_history"] == receipt.recovery_history
                and protocol["lexical_operational_AST_guard"] == receipt.lexical_guard
                and protocol["independent_proof_AST_guard"] == receipt.audit_proof_guard,
                "Exact separately released prepared auditor source and immutable history proof",
            )
            run_independent_audit(receipt, protocol, PROGRAM, RESEARCH)
            print("A20 independent restricted component audit PASS; zero program fixture credit")
        return 0
    except BaseException as error:
        if receipt is not None:
            receipt.fail(error)
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
