"""New independent audit of only the completed V11 saved minimum75 leaf. No producer/helper imports or emitter."""

from array import array

from collections import deque

import argparse

import ast

import ctypes

from ctypes import wintypes

from datetime import datetime, timezone

import hashlib

from fractions import Fraction

from importlib.util import cache_from_source

import json

import os

from pathlib import Path

import sys

import time

import types

import traceback

ROOT = Path(__file__).resolve().parents[2]

RESEARCH = ROOT / "research/limitation_program_20261001"

PROGRAM = ROOT / "results/limitation_program_20261001"

LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"

AUDIT_NAME = "A13_recovery_audit_run006"

AUDIT = PROGRAM / AUDIT_NAME

AUDIT_SHA = "32c0cc8658bf2a2c89c86a5e685b4316d11a4a0e8b05b6c132fc2b0e78871b84"

AUDIT_COUNTS = [63, 1208, 2842]

AUDIT_READY = ROOT / ".context/A13_RECOVERY_AUDIT_V6_ROOT_READY_run001.json"

AUDIT_READY_SHA = "f3a0b5b792b8f231dac763ab0f86f7e84bbde6e114c456036a526ff1a173f46c"

PROTOCOL_SHA = "3ab2759c557563270a4a0242675f4d41123013df1f23f70d861b30b408db59e9"

AUDIT_AUTHORS = {
    ("audit_exp_frontier_recovery_v6.py"): (
        "54d841982c1a6f26b5a57814440609d5916dfad21cc3409ab57bee492ecc6c1b"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V6.md"): (
        "e0e433417a5fc5e8d06e50ac0371c65c9f26ad3ebdc070121008ed4287e0f47e"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v6.json"): (
        "17b95075d6c124db2dae7c35ca976048699d4c0fc0c843f606f00ab10ef00a67"
    ),
}

REQUIRED_SNAPSHOTS = {
    ("A13_BERNSTEIN_EQUIVALENCE_PREFLIGHT_V5.md"): (
        "e7ff698ea67c3ea28776c7da92078871426e3faa2ad6de210d272792ad1cd4a3"
    ),
    ("A13_EXP_FRONTIER_PREFLIGHT.md"): (
        "f5b4404650c1ee9bd3a8ef2557d67e1340dda0fc059d94126e19fcfc046d7f7b"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V4.md"): (
        "75b962da0239f371f34bc4c675243fba29b504038a68975a6b347fa0596af3f5"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V5.md"): (
        "06ddca7b99dba0d44c5dcc7de7f27d5c26ea82691cf8bdccfe91a2d969ceae18"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V6.md"): (
        "e0e433417a5fc5e8d06e50ac0371c65c9f26ad3ebdc070121008ed4287e0f47e"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_DP_OPTIMIZATION_PREFLIGHT_V4.md"): (
        "86e0185742c7ae425372675806dad6da772e0303ca0d1d8fab1d8a59eb7c717c"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md"): (
        "2d86febd3e35963e051113da6490b5e8ed352b7be10c79e6d8187cdf8950b747"
    ),
    ("A13_METADATA_PROFILE_ROOT_READY_run002.json"): (
        "641a2a6b3abcbe24c5c3374a35cc3fd973b773a4a4313a5e4d3bc2940c83d168"
    ),
    ("A13_METADATA_VALIDATION_PROFILE_PREFLIGHT_V2.md"): (
        "f07512a9714e611fdac659b4c3d83be4d6aa98daa92d4fabc1e0def9a43565b2"
    ),
    ("A13_RECOVERY_AUDIT_V6_ROOT_READY_run001.json"): (
        "f3a0b5b792b8f231dac763ab0f86f7e84bbde6e114c456036a526ff1a173f46c"
    ),
    ("a13_bernstein_equivalence_preflight_v5.json"): (
        "165426876e38662577fb1e1f1f816f664188245b46ec85bdf8c508e958c5880b"
    ),
    ("a13_exp_frontier_preflight.json"): (
        "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v4.json"): (
        "8b1bf237dd2739fdbfe59c5af4cd2bf776dc29ce198d02dcf8c900bedae1e1ea"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v5.json"): (
        "c8d592ab4e6beb52b59bc4c3275ab9a33e7e898c94ef56a8a733be821f6d6693"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v6.json"): (
        "17b95075d6c124db2dae7c35ca976048699d4c0fc0c843f606f00ab10ef00a67"
    ),
    ("a13_exp_frontier_recovery_dp_optimization_preflight_v4.json"): (
        "5a98e3e210b3e4911b7b00042504f22a1ba406fe97e0b5e286904c741d2d53fd"
    ),
    ("a13_exp_frontier_recovery_preflight.json"): (
        "c36d9c97266144a73373c1dd55922585a2271206d0a5cc1ddf0f42ddaa9ce291"
    ),
    ("a13_metadata_validation_profile_preflight_v2.json"): (
        "8e612119a7af4eff12107b4d4a44b26891180b8406d4f59f901ada354cc74b84"
    ),
    ("audit_exp_frontier_recovery_v4.py"): (
        "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
    ),
    ("audit_exp_frontier_recovery_v5.py"): (
        "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
    ),
    ("audit_exp_frontier_recovery_v6.py"): (
        "54d841982c1a6f26b5a57814440609d5916dfad21cc3409ab57bee492ecc6c1b"
    ),
    ("bernstein_integer_kernel_v5.py"): (
        "695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048"
    ),
    ("experiment_exp_frontier_recovery.py"): (
        "9a83c9ed87df61415af94b1ee15840c97714f48c90bebcf2c1d0b1367d79b8d9"
    ),
    ("profile_a13_metadata_validation_v2.py"): (
        "f033e7e551bad139e56fa9c350c3ce17f7a34bda85e156f4c091e1c366e51402"
    ),
    ("verify_a13_bernstein_equivalence_v5.py"): (
        "005b266056e791f06001f073858028096ff49f415f89cdc2f79b7de62ecca3ad"
    ),
}

GRID = tuple((degree, segments) for degree in (4, 6, 8, 10, 12) for segments in (1, 2, 4, 8))

CPU, ADMISSION, WALL = 180, 150, 600

MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2

MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3

MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3

FAILURE_NAMES = (
    ("FAILED_UNSEALED.json"),
    ("failed_unsealed.json"),
    ("failure.json"),
    ("run_failure.json"),
    ("prepare_failure.json"),
)

_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}

_PATH_CACHE, _HASH_CACHE = {}, {}

_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()

_CODE_CACHE_EXPECTED = {}

_BASE_SCOPE, _EXCLUDED_SCOPE = None, None

_STANDARD_RUNTIME_MEMBERS = set()

_HASH_WORK = _REFERENCES = 0

_STARTED = None

_SOURCE_INTERPRETER = None

MATERIAL = PROGRAM / "A13_run002"

METADATA_SOURCE = PROGRAM / "A13_recovery_run001"

FINAL_ROOT = PROGRAM / "A13_recovery_audit_ROOT_verification_run006"

FINAL_ROOT_READY = ROOT / ".context/A13_RECOVERY_AUDIT_ROOT_INTEGRITY_V6_ROOT_READY_run006.json"

FINAL_ROOT_READY_SHA = "378f5252b3ffc906f70f14e522f0525e8b72bad07262e339206dc4f2f4ffb5f2"

FINAL_ROOT_SHA = "b43d4f3f76061129af57f03b72d61d79b9a313795c543c804c5966d326989bab"

FINAL_ROOT_COUNTS = [8, 1241, 2842]

CORE_DERIVATION_SHA = "84b789dfd37ab68c4f94cd6ccde7723f7dd0a585b329878fb5c137956d2681c3"

ALPHA = [1, 16777216]

ALLOWANCE = [
    4073883417731182862847997641774456332891573449254683949318947788511038490778395976239348623,
    68351585149469122636640694597425667667286544715412888638305331450311031224980497600734786781970432,
]

BASELINES = {"B4x12": [520720662, 555774, 550141], "B8x52": [4267435214, 663704, 4460479]}

SITES = {"B4x12": [48, 30], "B8x52": [416, 234]}

ALLOCATION_PACKETS = [
    [
        "A13_fixed_alpha_allocation_run001",
        "4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f",
        [19, 1008, 2842],
        "a13-fixed-alpha-allocation-producer-terminal-manifest-v1",
        "receipt",
    ],
    [
        "A13_fixed_alpha_allocation_audit_run001",
        "829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358",
        [20, 1029, 2842],
        "a13-fixed-alpha-allocation-auditor-terminal-manifest-v1",
        "receipt",
    ],
    [
        "A13_fixed_alpha_allocation_root_verification_run002",
        "39930d414dde63f1ed087423de1877d565a509038a87a68bc478c7ccb9c365bf",
        [5, 1060, 2842],
        "root-exp-frontier-allocation-integrity-manifest-v2",
        "ROOT",
    ],
]

MAX_SCALAR_BITS = 2048

MAX_RESULT_BITS = 8192

MAX_NATIVE_CELLS = 240

MAX_IR_NODES = 64

_FAILED_MATERIAL_MEMBERS = set()

_FAILED_MATERIAL_BYTES = None

PRIOR_SELECTION = PROGRAM / "A13_certified_candidate_selection_run001"

PRIOR_SELECTION_FREEZE = (
    ROOT / ".context/A13_CERTIFIED_SELECTION_V1_FAILED_OWNED_FROZEN_run001.json"
)

PRIOR_SELECTION_FREEZE_SHA = "9538230d4e268e8d57123e272b75f52b01d922c0433da9fceb5c427fdfb6f63d"

PRIOR_SELECTION_READY = ROOT / ".context/A13_CERTIFIED_CANDIDATE_SELECTION_ROOT_READY_run001.json"

PRIOR_SELECTION_READY_SHA = "b105057da6040d17d0804320ff2c80081f75ca41fd3a85b4d898d6484c83f45a"

PRIOR_SELECTION_LOG = ROOT / ".context/a13_certified_selection_run001.log"

PRIOR_SELECTION_LOG_SHA = "e67e023ff8d5f5029400709f50255594e06c2692f85e42b3a6221978eab5f4af"

PRIOR_SELECTION_AUTHORS = {
    "select_a13_certified_candidates_v1.py": (
        "4b18973647539c539c6ca7fb92d7bb328df316858b2710677f4d9a895641a7f3"
    ),
    "A13_CERTIFIED_CANDIDATE_SELECTION_PREFLIGHT_V1.md": (
        "558404e9db891ac243546788e8c53732026011ce309deb6c790eb2e1674e7b4d"
    ),
    "a13_certified_candidate_selection_preflight_v1.json": (
        "71a21f6af54f3f1900439899050a17eded15a7f03840b8d8a24780ae8c96e60b"
    ),
}

_SELECTION_FAILED_MEMBERS = set()

PRIOR_INVENTORY = PROGRAM / "A13_d4_s4_native_contract_inventory_run001"

PRIOR_INVENTORY_WITNESS = (
    ROOT / ".context/A13_D4_S4_NATIVE_INVENTORY_V1_PREFIT_FAILURE_WITNESS_run001.json"
)

PRIOR_INVENTORY_WITNESS_SHA = "28e2a90043b4ce9fb943bd7ae81b28008010e8395a34938c8f1c4c5755fdf502"

PRIOR_INVENTORY_READY = ROOT / ".context/A13_D4_S4_NATIVE_CONTRACT_INVENTORY_ROOT_READY_run001.json"

PRIOR_INVENTORY_READY_SHA = "4da4681c4e8e27725c14ae58c87c83e409a5f2ae60c32f733e0dbebdbb20f4e6"

PRIOR_INVENTORY_LOG = ROOT / ".context/a13_d4_s4_native_contract_inventory_run001.log"

PRIOR_INVENTORY_LOG_SHA = "b5863e9ca7fe621eebef0a381aad0126332639afaacbf85683166d46b8f47e5e"

PRIOR_INVENTORY_AUTHORS = {
    "contract_a13_d4_s4_native_inventory_v1.py": "11cb6c88511101bd19ab348eb5dd6c031274c350a5dea3f97a9e154dacae3d51",
    "A13_D4_S4_NATIVE_CONTRACT_INVENTORY_PREFLIGHT_V1.md": "2667c373f70e166c6319678c8acf8aa4242af759b5029df0a919255a2b72cf4f",
    "a13_d4_s4_native_contract_inventory_preflight_v1.json": "192589cad03a24b2cccbef49a20d19151f112c72bbb8c16a94eff8ed96a03593",
}

HELD_AUDIT_V1_AUTHORS = {'audit_a13_d4_s4_first_signed_leaf_v1.py': 'e360545200826bbb0286b7dcc1024bf175fc38e473014f256bb44733cd8bffce', 'A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_PREFLIGHT_V1.md': '5ff11bbbfd56adae6756c8fc196012381d889650513aa7034321e9d7a1c54aa4', 'a13_d4_s4_first_signed_leaf_independent_audit_preflight_v1.json': '2b8281a3b3501c8337f1fe05d780edbbcd41b468c66211e5341060df98131147'}

HELD_AUDIT_V1_REPORTS = {'.context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_AUTHOR_STATIC_QA_next_run001.json': 'b48c34bf4e6814818b5bb549a505b739a48c151d30894f4f8b3e91a56281509f', '.context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_FULL_INPUT_AUTHOR_STATIC_QA_next_run001.json': '7f5d2e810fcf19c4fa6060bb70463cc6e56235bbb945d9a482ce0ba519fc7356', '.context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_ROOT_STATIC_HOLD_run001.json': '9095d1a10aa3c676f12562b10c732c4b37499991e7ac79a79bdcb160fb6e79f7', '.context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_STATIC_HOLD_run001.json': 'd11e2629a9838cffbd4384d68059a46cefb4c3590cc64b492a0b5e6bd4e71a18'}

HELD_AUDIT_V1_READY_KEY = ".context/A13_D4_S4_FIRST_SIGNED_LEAF_AUDIT_ROOT_READY_run001.json"

HELD_AUDIT_V1_OUTPUT_KEY = "results/limitation_program_20261001/A13_d4_s4_first_signed_leaf_audit_run001"

ROW_ID = "d4_s4"

SELECTOR = PROGRAM / "A13_certified_candidate_selection_run002"

SELECTOR_SHA = "81e4403e7cacf6396da6559d4bf94332522f0d2c2fa63d7b81fddd5d2658544e"

SELECTOR_COUNTS = [14, 1521, 2842]

SELECTOR_READY = ROOT / ".context/A13_CERTIFIED_CANDIDATE_SELECTION_ROOT_READY_run002.json"

SELECTOR_READY_SHA = "681b95ef4129b3c1a2f5e22071dca1439f293c50befad3c2a95cddacb2870445"

SELECTOR_RESULT_REVIEW = ROOT / ".context/A13_CERTIFIED_SELECTION_V2_ROOT_RESULT_REVIEW_run001.json"

SELECTOR_RESULT_REVIEW_SHA = "c6912bce8108d05668020895882e4985db35f610f869a120ed2ea9c501d4d9a0"

SELECTOR_AUTHORS = {
    "select_a13_certified_candidates_v2.py": "a99b3bcb04c76239f6c7f3a1a76bccba864c795f6473334796eb857e597adc27",
    "A13_CERTIFIED_CANDIDATE_SELECTION_PREFLIGHT_V2.md": "28caf7ff51c4641e3a2565d96ad4b6a6d37c3dacec3889d84299f444cc40aa55",
    "a13_certified_candidate_selection_preflight_v2.json": "f9505fe30ae015287e291e68836cbe744c62f30308c4cce1f28f3a4f3e6edcd5",
}

W, Q = 72, 1 << 40

FIXED_PLAN = {
    "nodes": [
        {"value": 0, "op": "local", "args": []},
        {"value": 1, "op": "coefficient", "args": [], "degree": 0},
        {"value": 2, "op": "coefficient", "args": [], "degree": 1},
        {"value": 3, "op": "coefficient", "args": [], "degree": 2},
        {"value": 4, "op": "coefficient", "args": [], "degree": 3},
        {"value": 5, "op": "coefficient", "args": [], "degree": 4},
        {"value": 6, "op": "mul", "args": [0, 2]},
        {"value": 7, "op": "add", "args": [1, 6]},
        {"value": 8, "op": "mul", "args": [0, 4]},
        {"value": 9, "op": "add", "args": [3, 8]},
        {"value": 10, "op": "mul", "args": [0, 0]},
        {"value": 11, "op": "mul", "args": [10, 9]},
        {"value": 12, "op": "add", "args": [7, 11]},
        {"value": 13, "op": "mul", "args": [10, 10]},
        {"value": 14, "op": "mul", "args": [13, 5]},
        {"value": 15, "op": "add", "args": [12, 14]},
    ],
    "output": 15,
    "odd_term_carried_without_zero_pad": True,
    "unused_candidate_power_emitted": False,
}

PRODUCER = PROGRAM / "A13_d4_s4_native_contract_inventory_run002"

PRODUCER_SHA = "a5b51dde9ac50bb742fa571d35182128f361d99e0b9d11cc427e505029c14eae"

PRODUCER_COUNTS = [31, 1547, 2842]

PRODUCER_READY = ROOT / ".context/A13_D4_S4_NATIVE_CONTRACT_INVENTORY_ROOT_READY_run002.json"

PRODUCER_READY_SHA = "4a4bdba7d452d55e5b65056a7bf3bf2b9ffbfbc1d09309cdbaf7e022232c2d11"

PRODUCER_AUTHORS = {
    "contract_a13_d4_s4_native_inventory_v2.py": "f3089b26850efdd401ec4f4ac9e85049f7897dc60aec111fa8a886bcd56d8aac",
    "A13_D4_S4_NATIVE_CONTRACT_INVENTORY_PREFLIGHT_V2.md": "5c4bf2928194caa8274f752b696478f115b62cfe7eac2b0892f12b7c2e778ea9",
    "a13_d4_s4_native_contract_inventory_preflight_v2.json": "f66b44ee38872b6d2d41febedea307d43f0855be7f41a5a32e6c3218b3a85937",
}

MUL_VALUES = (6, 8, 10, 11, 13, 14)

PRODUCER_RESULT_REVIEW = (
    ROOT
    / ".context/A13_D4_S4_NATIVE_CONTRACT_INVENTORY_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"
)

PRODUCER_RESULT_REVIEW_SHA = "97a12e075d711af47ebd414ee3ab69b9519711b061837eafb04c5478d94141a1"

NATIVE_AUDIT = PROGRAM / "A13_d4_s4_native_independent_audit_run001"

NATIVE_AUDIT_SHA = "c6583d3a46da731dc26cf5fa2e1b1056ef951543f81c8247f289ad717b31e70b"

NATIVE_AUDIT_COUNTS = [37, 1584, 2842]

NATIVE_AUDIT_READY = ROOT / ".context/A13_D4_S4_NATIVE_INDEPENDENT_AUDIT_ROOT_READY_run001.json"

NATIVE_AUDIT_READY_SHA = "81f1e6f56a7a374c7c48c14f4f456ad53781ffa0e8bba21343021a46b5471c64"

NATIVE_AUDIT_AUTHORS = {
    "audit_a13_d4_s4_native_inventory_v1.py": "0aa73e58bf13f3c3fe34eebbb69e5ff5a65bdd369381a47d6288decc1c12a537",
    "A13_D4_S4_NATIVE_INDEPENDENT_AUDIT_PREFLIGHT_V1.md": "b3313b72de08a03b7e202fff6cfc6a23e443e1f161ceca8550f6dbedf3d427c8",
    "a13_d4_s4_native_independent_audit_preflight_v1.json": "fca269bf20450065c61613480738afd59fa9da1ad6f6df78ec16ca0def5d340e",
}

NATIVE_AUDIT_RESULT = ROOT / ".context/A13_D4_S4_NATIVE_INDEPENDENT_AUDIT_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json"

NATIVE_AUDIT_RESULT_SHA = "387926b180770fa08a2308bf107e88bf42b1d3439a3bfd0c7b2e630a86fa9cb1"

NATIVE_CONTRACT_SHA = "8555d8c619da44260149158fbc55ae6cb2e20de08dcd940200b2f71e135cd2f3"

HELD_DESIGN_AUTHORS = {
    "a13_d4_s4_contracted_mul_design_v1.py": "15af41694def4c14fa51945f430c23fa70db54858425a5812b88626fde54acfa",
    "A13_D4_S4_FIRST_CONTRACTED_MUL_DESIGN_V1.md": "28de45f1414552d132e16e55df9c458390ae9bec63a002e54153a91270143834",
    "a13_d4_s4_first_contracted_mul_design_v1.json": "81022169b2b307ce6e382dd44d547c0a844ec9b0d5de668af90a6142e7013607",
}

HELD_DESIGN_PEER = ROOT / ".context/A13_D4_S4_FIRST_CONTRACTED_MUL_DESIGN_INDEPENDENT_STATIC_PEER_run001.json"

HELD_DESIGN_PEER_SHA = "2b935b8e3a41716807380464aa86c8c5bf787fa2bc2fb458725e1ee263195c4d"

NATIVE_BITS, NATIVE_FRACTION, RESIDUE_BITS = 72, 40, 112

ACTIVE_WIDTHS = [38, 42]

LEAF_MAX_ROWS, LEAF_MAX_WIRES = 1_000_000, 32768

FIRST_VALUE, FIRST_ARGS = 6, [0, 2]

COMPLETED_OWNER_EXPECTATIONS = [
    ["A13_recovery_run001", "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9", [16, 909, 2842], "receipt"],
    ["A13_recovery_audit_run006", "32c0cc8658bf2a2c89c86a5e685b4316d11a4a0e8b05b6c132fc2b0e78871b84", [63, 1208, 2842], "receipt"],
    ["A13_recovery_audit_ROOT_verification_run006", "b43d4f3f76061129af57f03b72d61d79b9a313795c543c804c5966d326989bab", [8, 1241, 2842], "receipt"],
    ["A13_fixed_alpha_allocation_run001", "4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f", [19, 1008, 2842], "receipt"],
    ["A13_fixed_alpha_allocation_audit_run001", "829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358", [20, 1029, 2842], "receipt"],
    ["A13_fixed_alpha_allocation_root_verification_run002", "39930d414dde63f1ed087423de1877d565a509038a87a68bc478c7ccb9c365bf", [5, 1060, 2842], "ROOT"],
    ["A13_certified_candidate_selection_run002", "81e4403e7cacf6396da6559d4bf94332522f0d2c2fa63d7b81fddd5d2658544e", [14, 1521, 2842], "receipt"],
    ["A13_d4_s4_native_contract_inventory_run002", "a5b51dde9ac50bb742fa571d35182128f361d99e0b9d11cc427e505029c14eae", [31, 1547, 2842], "receipt"],
    ["A13_d4_s4_native_independent_audit_run001", "c6583d3a46da731dc26cf5fa2e1b1056ef951543f81c8247f289ad717b31e70b", [37, 1584, 2842], "receipt"],
]

EXPECTED_CCX_PHASE_MACRO = (
    ("H", 2), ("CX", 1, 2), ("TD", 2), ("CX", 0, 2), ("T", 2),
    ("CX", 1, 2), ("TD", 2), ("CX", 0, 2), ("T", 1), ("T", 2),
    ("H", 2), ("CX", 0, 1), ("T", 0), ("TD", 1), ("CX", 0, 1),
)

HELD_V1_AUTHORS = {'prototype_a13_d4_s4_first_signed_leaf_v1.py': 'f04584bf19cd99b0797fde22f3d98f00cbecfd2b4727fe6ef24b167302c5ea5b', 'build_a13_d4_s4_first_signed_leaf_v1.py': '3d2bdc68aa39457faeb13900d3d83f666d5f92c49446ed7a2adec087912aa764', 'A13_D4_S4_FIRST_SIGNED_LEAF_IMPLEMENTATION_PREFLIGHT_V1.md': 'cfba46ddfa571a7d306e9c776356078281e31ab8a4b631e9de656a069c9126c1', 'a13_d4_s4_first_signed_leaf_implementation_preflight_v1.json': '4cba71e49a5d4c87c7dd640d690ba916711cd1910f64f6c56005cecc8545a47e'}

HELD_V1_QA = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_AUTHOR_STATIC_QA_run001.json"

HELD_V1_QA_SHA = "fe2ace5c78370788309a206a7d61aee04cf52f0619db7ad2d769c67381da0350"

HELD_V1_PEER = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_STATIC_PEER_run001.json"

HELD_V1_PEER_SHA = "f8d3b8ef6eb0368db5c2b491f612aa0f77296204a60d8007591536e6e0ded33b"

HELD_V1_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ROOT_READY_run001.json"

HELD_V1_OUTPUT = PROGRAM / "A13_d4_s4_first_signed_leaf_run001"

HELD_V1_INPUTS = tuple((RESEARCH / name, pin) for name, pin in HELD_V1_AUTHORS.items()) + (
    (HELD_V1_QA, HELD_V1_QA_SHA), (HELD_V1_PEER, HELD_V1_PEER_SHA))

LEAF = PROGRAM / "A13_d4_s4_first_signed_leaf_run002"

LEAF_SHA = "67e3f264ef222f92b33537d4b3db1e397ccc712ed075364960231b8892e0cfed"

LEAF_COUNTS = [58, 1638, 2842]

LEAF_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ROOT_READY_run002.json"

LEAF_READY_SHA = "d440ad7e684cb2491bd9ab6627f9061ee3a531beca1d36c110722bd771758790"

LEAF_AUTHORS = {'prototype_a13_d4_s4_first_signed_leaf_v2.py': '02d2616422149e1e3de3b997c2396eba1309adce23472db2486d0228cf12f058', 'build_a13_d4_s4_first_signed_leaf_v2.py': '3d2bdc68aa39457faeb13900d3d83f666d5f92c49446ed7a2adec087912aa764', 'A13_D4_S4_FIRST_SIGNED_LEAF_IMPLEMENTATION_PREFLIGHT_V2.md': '451cb858fba32e9ca870be44fad8ee5a98cb04b5c317e900c39339d800176b13', 'a13_d4_s4_first_signed_leaf_implementation_preflight_v2.json': '3c5b50dfd7b2efc96d4806b14a66e8f99dd18ca5b906ca1b8611adaf522bb8bb'}

LEAF_RESULT = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"

LEAF_RESULT_SHA = "5eab9fffdf29a0b68f8acba30d4882a388410b78c8d2ab5e07237162b409f4f8"

LEAF_ARRAY_SHA = "5a37a245ecfded029138314b1d85a2caf6b308e56b27656b7f2eedd80f54f769"

ALL10_OWNER_EXPECTATIONS = COMPLETED_OWNER_EXPECTATIONS + [[LEAF.name, LEAF_SHA, LEAF_COUNTS, "receipt"]]

BASELINE112_AUDIT = PROGRAM / "A13_d4_s4_first_signed_leaf_audit_run002"

BASELINE112_AUDIT_SHA = 'e35e5e2b3b9b5833fd973f354c9f78303b66685d9d560a1f283be333de269326'

BASELINE112_AUDIT_COUNTS = [15, 1716, 2842]

BASELINE112_AUDIT_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_AUDIT_ROOT_READY_run002.json"

BASELINE112_AUDIT_READY_SHA = '0535ca704201f1c1587c9b49908c35c7f2121c108bf320803dd454bae9efacbc'

BASELINE112_AUDIT_AUTHORS = {'A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_PREFLIGHT_V2.md': '9fd435b226da391315c1fc645a6cb8a02cda1e8e7d4d000e27cd837e36ddca48',
 'a13_d4_s4_first_signed_leaf_independent_audit_preflight_v2.json': '3cd28c170a37b252bfeadeeffda0b3bd11ce8f9fd341b31ab290e61e1a1ed87a',
 'audit_a13_d4_s4_first_signed_leaf_v2.py': '3da298fa3032693d823034410dadfa638cf1af422ccd04faae6c66534d24df5e'}

BASELINE112_AUDIT_RESULT = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"

BASELINE112_AUDIT_RESULT_SHA = '0417e2f1a4c89a2e6ebeb48330e1d10dc77fae396a5184917343cc11c714f10f'

V11_METHOD_KEY = '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_METHOD_PROSPECTUS_run001.json'

V11_METHOD_SHA = '74ed5fe6a16e7766f304d880eeae24a12ec025aeed370d2e86a0aba37645c238'

V11_ACCEPTANCE_KEY = '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_ROOT_AUTHORING_ACCEPTANCE_run001.json'

V11_ACCEPTANCE_SHA = '5f1bae591eb6cce9bf143bb0b1b2872c066226fa6beac2fac4529cab3bc35c8c'

V11_CLARIFICATION_KEY = '.context/A13_V11_MIN75_EXTERNAL_AUDIT_STARTUP_RUNTIME_OPERATIONAL_CLARIFICATION_run001.json'

V11_CLARIFICATION_SHA = 'ff9f2ecb4dd8063a75c36ae9fc820a9c2895709bdd77b6b20b08c0a02c5ec45a'

V11_FIXED_INPUT_PINS = {'.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json': 'e6ffd93761a5421db3b7746ffd4ff0cce0ec0711ae1bf286d3448a2c2e9e5d9c',
 '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_ROOT_READY_run001.json': '4fbc699ec2aaf02009c71de62261434a786e1d4928dc7bd5fd54d68cf26d07dd',
 '.context/A13_V11_EXTERNAL_AUDIT_METHOD_AUTHOR_METADATA_HELPER_FAILURE_HISTORY_run001.json': 'd2b2422039c4a716922ce2a7025cd56edb6fe751732789922a702f1fed0ceca1',
 '.context/A13_V11_MIN75_EXTERNAL_AUDIT_STARTUP_RUNTIME_OPERATIONAL_CLARIFICATION_run001.json': 'ff9f2ecb4dd8063a75c36ae9fc820a9c2895709bdd77b6b20b08c0a02c5ec45a',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_INDEPENDENT_SYMBOLIC_LIFECYCLE_METHOD_PEER_v14_run001.json': 'de294f6be031841946755ddf5a72f02b6cfc747c23305f42a8d6f03d67e17fd1',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_METHOD_AUTHOR_METADATA_QA_run001.json': '2fc3aef4b3f5d984b51ad1e0764f5c2ee03bd7babd1fb9ec8c953defdf7742b6',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_METHOD_PROSPECTUS_run001.json': '74ed5fe6a16e7766f304d880eeae24a12ec025aeed370d2e86a0aba37645c238',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_METHOD_PROSPECTUS_run001.md': 'b5a07b0d467c950d06d7e9b45b8053aa787bbd56fb9376a1676f8efe26127c77',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_ROOT_AUTHORING_ACCEPTANCE_run001.json': '5f1bae591eb6cce9bf143bb0b1b2872c066226fa6beac2fac4529cab3bc35c8c',
 '.context/A13_V11_MIN75_EXTERNAL_INDEPENDENT_AUDIT_ROOT_METHOD_REVIEW_run001.json': '4125bd94cf8bc6b9e0e65dfbfb11fb02a2228344fa2e8f093ecda64336bd89ec',
 '.context/A13_V11_MIN75_ROOT_CLI_LAUNCH_FAILURE_PRESERVATION_run001.json': '4c1577a3ac53b0f42cfc39ac582456c6e1c8c659337af9d09dac57f2bd284e07',
 '.context/A13_d4_s4_v11_signed_leaf_min75_actual_run001.log': '1a2a5d87e984a034bd6ed9a41f0cc2c56247a9508555dd226a3eaf64993138c7',
 '.context/A13_d4_s4_v11_signed_leaf_min75_actual_run002.log': '2ef9fe6356d9bf30040ca718b0033aaba34f0c2fcbb763f4074324b6ba3dfe25',
 'research/limitation_program_20261001/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_INDEPENDENT_AUDIT_PREFLIGHT_V3.md': 'b1838fe5e9cca4c6a9a6c8f5541907f4be1e4ef2b3b674aa692b828746f95790',
 'research/limitation_program_20261001/A13_D4_S4_V11_SIGNED_LEAF_MIN75_PREFLIGHT_V1.md': '9402552c74de529c2e1a247bb6350f2a9f562282e72d696f355bce45a2c2b5b1',
 'research/limitation_program_20261001/a13_d4_s4_second_signed_leaf_min78_independent_audit_preflight_v3.json': '6e9d64a2f9ab4d7b724c60c72cd21bbdb8373246cc8ad85e05369bb069c5dd8a',
 'research/limitation_program_20261001/a13_d4_s4_v11_signed_leaf_min75_preflight_v1.json': '136eb2fc59efc9b6d688df533a9c98e2e640f86c7fca63f75037b39f5edf3776',
 'research/limitation_program_20261001/audit_a13_d4_s4_second_signed_leaf_min78_v3.py': '0fc14ce5a8cb29cf33452debd7a819996365da792ac604380f5eb4da03aa0886',
 'research/limitation_program_20261001/build_a13_d4_s4_v11_signed_leaf_min75_v1.py': '79def43eaa414ac8041ffdb462d08efa18081ce544c65b1e9e66b129ab46a09b',
 'research/limitation_program_20261001/prototype_a13_d4_s4_v11_signed_leaf_min75_v1.py': 'cfd1fa6c3e878770bcf2d3e8b991419032bc22b4002b713b91e24dcfd0fd11f2',
 'results/limitation_program_20261001/A13_d4_s4_v11_signed_leaf_min75_run001/manifest.json': '1bc7698bb5b98bd1ac0a66278b2ac018c29411b92a818d9456f23db1d62bb9da'}

V11_CURRENT_REVIEW_ROUTES = ['.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_INDEPENDENT_AUDIT_AUTHOR_STATIC_QA_run001.json',
 '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_INDEPENDENT_AUDIT_INDEPENDENT_STATIC_PEER_run001.json',
 '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_INDEPENDENT_AUDIT_ROOT_STATIC_REVIEW_run001.json']

V11_CURRENT13 = [['A13_recovery_run001',
  'e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9',
  [16, 909, 2842],
  'receipt',
  'a13-exp-frontier-recovery-terminal-manifest-v1'],
 ['A13_recovery_audit_run006',
  '32c0cc8658bf2a2c89c86a5e685b4316d11a4a0e8b05b6c132fc2b0e78871b84',
  [63, 1208, 2842],
  'receipt',
  'a13-exp-frontier-recovery-independent-audit-manifest-v1'],
 ['A13_recovery_audit_ROOT_verification_run006',
  'b43d4f3f76061129af57f03b72d61d79b9a313795c543c804c5966d326989bab',
  [8, 1241, 2842],
  'receipt',
  'a13-recovery-audit-root-integrity-manifest-v6'],
 ['A13_fixed_alpha_allocation_run001',
  '4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f',
  [19, 1008, 2842],
  'receipt',
  'a13-fixed-alpha-allocation-producer-terminal-manifest-v1'],
 ['A13_fixed_alpha_allocation_audit_run001',
  '829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358',
  [20, 1029, 2842],
  'receipt',
  'a13-fixed-alpha-allocation-auditor-terminal-manifest-v1'],
 ['A13_fixed_alpha_allocation_root_verification_run002',
  '39930d414dde63f1ed087423de1877d565a509038a87a68bc478c7ccb9c365bf',
  [5, 1060, 2842],
  'ROOT',
  'root-exp-frontier-allocation-integrity-manifest-v2'],
 ['A13_certified_candidate_selection_run002',
  '81e4403e7cacf6396da6559d4bf94332522f0d2c2fa63d7b81fddd5d2658544e',
  [14, 1521, 2842],
  'receipt',
  'a13-certified-candidate-selection-manifest-v2'],
 ['A13_d4_s4_native_contract_inventory_run002',
  'a5b51dde9ac50bb742fa571d35182128f361d99e0b9d11cc427e505029c14eae',
  [31, 1547, 2842],
  'receipt',
  'a13-d4-s4-native-contract-inventory-manifest-v2'],
 ['A13_d4_s4_native_independent_audit_run001',
  'c6583d3a46da731dc26cf5fa2e1b1056ef951543f81c8247f289ad717b31e70b',
  [37, 1584, 2842],
  'receipt',
  'a13-d4-s4-native-independent-audit-manifest-v1'],
 ['A13_d4_s4_first_signed_leaf_run002',
  '67e3f264ef222f92b33537d4b3db1e397ccc712ed075364960231b8892e0cfed',
  [58, 1638, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-manifest-v2'],
 ['A13_d4_s4_first_signed_leaf_audit_run002',
  'e35e5e2b3b9b5833fd973f354c9f78303b66685d9d560a1f283be333de269326',
  [15, 1716, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-independent-audit-manifest-v2'],
 ['A13_d4_s4_first_signed_leaf_min80_run001',
  'a5f6d39d8ae4cef0f4a968f0fb872c80e8028873a8e7c9aa9fb6be43f0c2f42f',
  [59, 1741, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-min80-manifest-v1'],
 ['A13_d4_s4_v11_signed_leaf_min75_run001',
  '1bc7698bb5b98bd1ac0a66278b2ac018c29411b92a818d9456f23db1d62bb9da',
  [61, 1819, 2842],
  'receipt',
  'a13-d4-s4-v11-signed-leaf-min75-manifest-v1']]

V11_ORIGINAL12 = [['A13_recovery_run001',
  'e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9',
  [16, 909, 2842],
  'receipt',
  'a13-exp-frontier-recovery-terminal-manifest-v1'],
 ['A13_recovery_audit_run006',
  '32c0cc8658bf2a2c89c86a5e685b4316d11a4a0e8b05b6c132fc2b0e78871b84',
  [63, 1208, 2842],
  'receipt',
  'a13-exp-frontier-recovery-independent-audit-manifest-v1'],
 ['A13_recovery_audit_ROOT_verification_run006',
  'b43d4f3f76061129af57f03b72d61d79b9a313795c543c804c5966d326989bab',
  [8, 1241, 2842],
  'receipt',
  'a13-recovery-audit-root-integrity-manifest-v6'],
 ['A13_fixed_alpha_allocation_run001',
  '4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f',
  [19, 1008, 2842],
  'receipt',
  'a13-fixed-alpha-allocation-producer-terminal-manifest-v1'],
 ['A13_fixed_alpha_allocation_audit_run001',
  '829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358',
  [20, 1029, 2842],
  'receipt',
  'a13-fixed-alpha-allocation-auditor-terminal-manifest-v1'],
 ['A13_fixed_alpha_allocation_root_verification_run002',
  '39930d414dde63f1ed087423de1877d565a509038a87a68bc478c7ccb9c365bf',
  [5, 1060, 2842],
  'ROOT',
  'root-exp-frontier-allocation-integrity-manifest-v2'],
 ['A13_certified_candidate_selection_run002',
  '81e4403e7cacf6396da6559d4bf94332522f0d2c2fa63d7b81fddd5d2658544e',
  [14, 1521, 2842],
  'receipt',
  'a13-certified-candidate-selection-manifest-v2'],
 ['A13_d4_s4_native_contract_inventory_run002',
  'a5b51dde9ac50bb742fa571d35182128f361d99e0b9d11cc427e505029c14eae',
  [31, 1547, 2842],
  'receipt',
  'a13-d4-s4-native-contract-inventory-manifest-v2'],
 ['A13_d4_s4_native_independent_audit_run001',
  'c6583d3a46da731dc26cf5fa2e1b1056ef951543f81c8247f289ad717b31e70b',
  [37, 1584, 2842],
  'receipt',
  'a13-d4-s4-native-independent-audit-manifest-v1'],
 ['A13_d4_s4_first_signed_leaf_run002',
  '67e3f264ef222f92b33537d4b3db1e397ccc712ed075364960231b8892e0cfed',
  [58, 1638, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-manifest-v2'],
 ['A13_d4_s4_first_signed_leaf_audit_run002',
  'e35e5e2b3b9b5833fd973f354c9f78303b66685d9d560a1f283be333de269326',
  [15, 1716, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-independent-audit-manifest-v2'],
 ['A13_d4_s4_first_signed_leaf_min80_run001',
  'a5f6d39d8ae4cef0f4a968f0fb872c80e8028873a8e7c9aa9fb6be43f0c2f42f',
  [59, 1741, 2842],
  'receipt',
  'a13-d4-s4-first-signed-leaf-min80-manifest-v1']]

V11_LEAF_SHA = '1bc7698bb5b98bd1ac0a66278b2ac018c29411b92a818d9456f23db1d62bb9da'

V11_LEAF_COUNTS = [61, 1819, 2842]

V11_LEAF_READY_SHA = '4fbc699ec2aaf02009c71de62261434a786e1d4928dc7bd5fd54d68cf26d07dd'

V11_LEAF_RESULT_SHA = 'e6ffd93761a5421db3b7746ffd4ff0cce0ec0711ae1bf286d3448a2c2e9e5d9c'

V11_ARRAY_SHA = 'f923f7ed030f5886fd4c8b1f75baf7689bc2408828ded1e109b21f0c91dacc7c'

V11_DESCRIPTOR_SHA = 'd4743a3b849d6b52992ee6cbc05b5034c429cba08c1872389ecfb234f8853d4d'

V11_CASES_SHA = 'd3e33d7dde61e7e09c491d6d0fd3c1722233661ccf9cda57004b9fdfaa91a4cc'

V11_BINDING_SHA = '5dffa4c00e20f555c55ef7789521faa7adba79edafd90a69f572f185b1b5a96d'

V11_ROW_ID = 'A13_D4_S4_V11_SIGNED34X41_COMPLETE_PRODUCT75_SIGN35_TO72_V1'

V11_VALUE = 11

V11_ARGS = [10, 9]

V11_ACTIVE_WIDTHS = [34, 41]

V11_PLANNED_OWNED = ['executed_audit_a13_d4_s4_v11_signed_leaf_min75_v1.py',
 'executed_A13_D4_S4_V11_SIGNED_LEAF_MIN75_INDEPENDENT_AUDIT_PREFLIGHT_V1.md',
 'executed_a13_d4_s4_v11_signed_leaf_min75_independent_audit_preflight_v1.json',
 'executed_A13_D4_S4_V11_SIGNED_LEAF_MIN75_AUDIT_ROOT_READY_run001.json',
 'run_started.json',
 'independent_saved_all_rows_and_signed75_semantics.json',
 'independent_fixed64_native_cases.json',
 'independent_actual_forward_inverse_all_wire_batch.json',
 'independent900_unsigned_toys_and_four_controls.json',
 'independent_cyclic8_absolute_phase.json',
 'independent_dict_dependency_actual_resources.json',
 'independent_unmatched_v11_comparator_scope.json',
 'independent_original_report_comparison.json',
 'independent_full_ordered_ABI_and_source_scope.json',
 'independent_owner_scope_metadata.json',
 'summary.json',
 'completion_outcome.json',
 'manifest.json']

V11_INTERPRETER_KEY = 'results/limitation_program_20261001/A13_recovery_audit_run006/interpreter.json'

V11_INTERPRETER_SHA = 'd5c93a15909831bb9db474efb47ed2d4e36f91c3a7cb722f52a2b91743a3710c'

V11_STARTUP6 = [{'bytes_metadata_only': 1137,
  'expected_SHA256': 'd8536aedd91ba3763b64147357c5e8c0a270b6a8031a59130c10d10351ce879e',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\__pycache__\\_cuda_bindings_redirector.cpython-312.pyc',
  'role': 'startup redirector existing bytecode'},
 {'bytes_metadata_only': 3609,
  'expected_SHA256': 'a440fa4055a99394bebc66cb280485004252f138d989b2d51fee17e9b3f213a1',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/__pycache__/_numba_cuda_redirector.cpython-312.pyc',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\__pycache__\\_numba_cuda_redirector.cpython-312.pyc',
  'role': 'startup redirector existing bytecode'},
 {'bytes_metadata_only': 176,
  'expected_SHA256': '85a35d0fa0411036458d81dc56ae69bda1059d83882b7e2fe1bc3a5874213421',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.pth',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\_cuda_bindings_redirector.pth',
  'role': '.pth bootstrap declaration'},
 {'bytes_metadata_only': 854,
  'expected_SHA256': '25ed97b37208b2dba48d5732aa44899fa218c85d2c33148743ead8cc60d34fce',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.py',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\_cuda_bindings_redirector.py',
  'role': 'startup redirector source'},
 {'bytes_metadata_only': 174,
  'expected_SHA256': '526df5910c1cc887b69adb485d6a42cef3a1af0185fcd0640cb8a97f8bc3d77e',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.pth',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\_numba_cuda_redirector.pth',
  'role': '.pth bootstrap declaration'},
 {'bytes_metadata_only': 2893,
  'expected_SHA256': '854bdc54e933b3b1804d88454a4e51c2ecfdd59f6871e5957b97e5a344570d85',
  'original_frozen_inputs_key': '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.py',
  'original_saved_absolute_path': 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Lib\\site-packages\\_numba_cuda_redirector.py',
  'role': 'startup redirector source'}]

V11_STDLIB2842_CANONICAL_SHA = 'd68ae51a74eb7da5ba68308626a630dbf5860135ee22a0e5f1677e34d5cd7bfa'

V11_SAVED3057_CANONICAL_SHA = 'c9ee43f7da3224147c00018e6a3f4cea45ad9e794a232a1966332c66e94f2ce7'

_V11_OWNERS = None

_V11_POLICY = None

_V11_READY = None

_V11_METHOD = None

_V11_OUTPUT_IDENTITY = None

AUTHOR = RESEARCH / 'audit_a13_d4_s4_v11_signed_leaf_min75_v1.py'

METHOD_DOC = RESEARCH / 'A13_D4_S4_V11_SIGNED_LEAF_MIN75_INDEPENDENT_AUDIT_PREFLIGHT_V1.md'

PREFLIGHT = RESEARCH / 'a13_d4_s4_v11_signed_leaf_min75_independent_audit_preflight_v1.json'

READY = ROOT / '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_AUDIT_ROOT_READY_run001.json'

OUTPUT = PROGRAM / 'A13_d4_s4_v11_signed_leaf_min75_audit_run001'

INVENTORY_MODULE = 'research.limitation_program_20261001.audit_a13_d4_s4_v11_signed_leaf_min75_v1'

RUNTIME_INVOCATION = ['-B', '-m', INVENTORY_MODULE]

V11_LEAF = ROOT / 'results/limitation_program_20261001/A13_d4_s4_v11_signed_leaf_min75_run001'

V11_LEAF_READY = ROOT / '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_ROOT_READY_run001.json'

V11_LEAF_RESULT = ROOT / '.context/A13_D4_S4_V11_SIGNED_LEAF_MIN75_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json'

V11_PRODUCER_POLICY = RESEARCH / 'a13_d4_s4_v11_signed_leaf_min75_preflight_v1.json'

V11_PRODUCER_INVOCATION = ['-B', '-m', 'research.limitation_program_20261001.prototype_a13_d4_s4_v11_signed_leaf_min75_v1']

def require(condition, message):
    if not condition:
        raise ValueError(message)

def process_started():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(
            kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]
        ),
        "Actual process creation clock",
    )
    ticks = (stamps[0].dwHighDateTime << 32) | stamps[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Actual UTC creation precedes observation")
    # GetCurrentProcess is a pseudo-handle, never an owned handle to close.
    return time.monotonic() - age_ns / 1_000_000_000

def budget(admission=False):
    require(time.process_time() < (ADMISSION if admission else CPU), "Process CPU guard")
    require(time.monotonic() - _STARTED < WALL, "Creation-derived wall guard")

def runtime_scopes():
    global _BASE_SCOPE, _EXCLUDED_SCOPE
    budget()
    lexical = Path(os.path.abspath(sys.base_prefix))
    actual = lexical.resolve(strict=True)
    require(actual == lexical, "Actual base prefix has no alias")
    excluded = lexical / "Lib/site-packages"
    physical_excluded = excluded.resolve(strict=False)
    scopes = (actual, (excluded, physical_excluded))
    if _BASE_SCOPE is not None:
        require(scopes == (_BASE_SCOPE, _EXCLUDED_SCOPE), "Actual runtime scopes unchanged")
    _BASE_SCOPE, _EXCLUDED_SCOPE = scopes
    budget()

def canonical(path, fresh=False):
    budget()
    path = Path(path)
    require(not path.drive or path.is_absolute(), "No ambiguous drive-relative input")
    lexical = Path(os.path.abspath(str(path)))
    require(
        not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base packages lexical path",
    )
    key = str(lexical)
    if not fresh and key in _PATH_CACHE:
        cached, identity = _PATH_CACHE[key]
        if fingerprint(lexical) == identity:
            budget()
            return cached
    actual = lexical.resolve(strict=True)
    require(
        not any(actual.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base package alias",
    )
    require(actual == lexical, "No lexical-to-physical input alias")
    require(
        key not in _PATH_CACHE or _PATH_CACHE[key][0] == actual,
        "Previously confined lexical input did not redirect",
    )
    _PATH_CACHE[key] = (actual, fingerprint(lexical))
    budget()
    return actual

def fingerprint(path):
    stat = path.stat()
    return tuple(
        getattr(stat, name, None)
        for name in (
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

def digest(path, fresh=False, already_resolved=False):
    global _HASH_WORK
    budget()
    path = path if already_resolved else canonical(path, fresh=fresh)
    require(path.is_file(), "Actual regular SHA input")
    before, total, state = fingerprint(path), 0, hashlib.sha256()
    if not fresh and path in _HASH_CACHE and _HASH_CACHE[path][0] == before:
        budget()
        return _HASH_CACHE[path][1]
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK, "Fixed24GiB hashing-work cap")
            require(total <= before[2], "Input grew while hashing")
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable actual byte hash")
    result = state.hexdigest()
    require(
        path not in _OBSERVED or _OBSERVED[path] == result, "Previously observed bytes unchanged"
    )
    _OBSERVED.setdefault(path, result)
    _HASH_CACHE[path] = (before, result)
    budget()
    return result

def add(path, expected):
    global _REFERENCES
    budget()
    _REFERENCES += 1
    require(_REFERENCES <= MAX_REFERENCES, "Fixed100k map-reference cap")
    require(
        type(expected) is str
        and len(expected) == 64
        and all(char in "0123456789abcdef" for char in expected),
        "Exact expected SHA",
    )
    actual = canonical(path)
    require(actual.is_file(), "Regular preserved input")
    if actual.is_relative_to(ROOT):
        key, mapping = actual.relative_to(ROOT).as_posix(), _FROZEN
    else:
        require(actual.is_relative_to(_BASE_SCOPE), "Actual external base runtime")
        key, mapping = str(actual), _EXTERNAL
    require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA expectations")
    mapping[key] = expected
    return actual

def read(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= 128 * 1024**2, "Bounded regular JSON input")
    chunks, total, state = [], 0, hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK and total <= before[2], "Bounded JSON reads")
            chunks.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable JSON bytes")
    expected = (
        _FROZEN.get(path.relative_to(ROOT).as_posix())
        if path.is_relative_to(ROOT)
        else _EXTERNAL.get(str(path))
    )
    observed = state.hexdigest()
    require(expected is not None and observed == expected, "JSON belongs to exact admitted SHA")
    require(path not in _OBSERVED or _OBSERVED[path] == observed, "Stable observed JSON SHA")
    _OBSERVED[path] = observed
    _HASH_CACHE[path] = (before, observed)
    budget()
    result = json.loads(b"".join(chunks))
    budget()
    return result

def no_failure(directory):
    require(
        not any((directory / name).exists() for name in FAILURE_NAMES),
        "Authoritative failure marker prohibits admission",
    )

def inventory(directory):
    if directory == OUTPUT:
        v11_output_custody()
    found, total = set(), 0
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(canonical(candidate).is_relative_to(directory), "No owned directory escape")
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(Path(root) / name, fresh=True)
            require(actual.is_relative_to(directory) and actual not in found, "Unique owned path")
            require(actual.is_file(), "Regular actual owned entry")
            found.add(actual)
            total += actual.stat().st_size
            require(len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, "Finite owned inventory")
    if directory == OUTPUT:
        v11_output_custody()
    return found

def standard_runtime_members():
    base = canonical(sys.base_prefix)
    candidates = set()
    excluded = base / "Lib/site-packages"
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts"):
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            dirs[:] = [name for name in dirs if Path(root) / name != excluded]
            for name in dirs:
                require(not (Path(root) / name).is_symlink(), "No runtime directory alias")
                canonical(Path(root) / name)
            for name in names:
                candidates.add(canonical(Path(root) / name))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite complete runtime membership")
    for directory in (
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
    ):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite adjacent runtime membership")
    return candidates

def key_for(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)

def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual) == expected, "Actual admitted expected bytes")
    return actual

def code_caches(sources, pins, absent_keys):
    """External presence/absence admission; source execution never reads these caches."""
    budget()
    paths = {
        key_for(Path(cache_from_source(str(source)))): Path(cache_from_source(str(source)))
        for source in sources
    }
    present = {key for key, path in paths.items() if path.exists()}
    require(
        type(pins) is dict
        and set(pins) == present
        and type(absent_keys) is list
        and absent_keys == sorted(set(paths) - present),
        "Exact external cache presence and absence declaration",
    )
    for key in present:
        path = bind(paths[key], pins[key])
        _CODE_CACHE_EXPECTED[path] = pins[key]
    for key in absent_keys:
        path = paths[key]
        require(not path.exists() and not path.is_symlink(), "No absent cache or dangling alias")
        _ABSENT_RUNTIME.add(path)
    budget()

def check_code_caches():
    budget()
    for path, expected in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == expected, "Declared existing cache bytes unchanged")
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Declared absent caches and standard zip remain absent",
    )
    budget()

def complete_manifest(value, owned, nonmanifest_bytes):
    """Check exact UTF8 JSON bytes and file count including the prospective manifest."""
    budget()
    v11_output_custody()
    require(len(owned) + 1 <= MAX_OWN_FILES, "Manifest-inclusive owned file cap")
    value["manifest_inclusive_owned_file_count"] = len(owned) + 1
    value["owned_nonmanifest_bytes"] = nonmanifest_bytes
    value["manifest_inclusive_retention_checked_before_sealing"] = True
    manifest_bytes = 1  # save() appends exactly one newline.
    for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(value):
        budget()
        manifest_bytes += len(fragment.encode("utf-8"))
        require(nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES, "Manifest-inclusive128MiB cap")
    save("manifest.json", value)
    require(
        (OUTPUT / "manifest.json").stat().st_size == manifest_bytes, "Exact encoded manifest size"
    )
    actual = inventory(OUTPUT)
    require(
        actual == {OUTPUT / name for name in owned} | {OUTPUT / "manifest.json"}
        and len(actual) == len(owned) + 1 <= MAX_OWN_FILES,
        "Complete final manifest-inclusive inventory",
    )
    total = 0
    for path in actual:
        budget()
        total += path.stat().st_size
    require(
        total == nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES,
        "Complete final owned byte cap",
    )
    budget()

def v11_output_custody():
    """Keep every owned write and seal inside the one held output directory."""
    require(_V11_OUTPUT_IDENTITY is not None and OUTPUT.is_dir() and not OUTPUT.is_symlink(),
            "Only the created current output directory owns writes")
    require(OUTPUT.resolve(strict=True) == OUTPUT, "Output and all ancestors retain exact physical route")
    info = OUTPUT.stat()
    require(not (getattr(info, "st_file_attributes", 0) & 1024)
            and (info.st_dev, info.st_ino) == _V11_OUTPUT_IDENTITY,
            "Current output identity unchanged and no reparse redirect")
    return OUTPUT

def save(name, value):
    budget()
    v11_output_custody()
    target = OUTPUT / name
    require(target.parent == OUTPUT and not target.exists(), "Exclusive metadata output")
    pieces, new_bytes = [], 0
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(value):
        budget()
        part = fragment.encode("utf-8")
        new_bytes += len(part)
        require(new_bytes <= MAX_OWN_BYTES, "Bounded prospective UTF8 serialization")
        pieces.append(part)
    pieces.append(b"\n")
    new_bytes += 1
    members = inventory(OUTPUT)
    current_bytes = 0
    for member in members:
        budget()
        current_bytes += member.stat().st_size
    require(
        len(members) + 1 + (name != "manifest.json") <= MAX_OWN_FILES
        and current_bytes + new_bytes <= MAX_OWN_BYTES,
        "Inclusive owned byte/file cap with a final manifest slot",
    )
    with target.open("xb") as stream:
        for piece in pieces:
            budget()
            stream.write(piece)
    v11_output_custody()
    require(target.resolve(strict=True) == target and not target.is_symlink(), "Written output retains exact physical route")
    require(target.stat().st_size == new_bytes, "Exactly admitted output bytes")
    budget()

def copy(path, name):
    v11_output_custody()
    source = canonical(path)
    before, expected = fingerprint(source), digest(source)
    target = OUTPUT / name
    members = inventory(OUTPUT)
    require(target.parent == OUTPUT and not target.exists(), "New fixed copied output")
    require(
        len(members) + 2 <= MAX_OWN_FILES
        and sum(member.stat().st_size for member in members) + before[2] <= MAX_OWN_BYTES,
        "Admitted copied bytes with a manifest slot",
    )
    total = 0
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(65536):
            budget()
            total += len(block)
            require(total <= before[2], "Copied source cannot grow")
            outgoing.write(block)
    require(total == before[2] and fingerprint(source) == before, "Stable complete source copy")
    require(digest(target) == expected, "Exact preserved copied source bytes")
    v11_output_custody()

def exact_relative(key):
    require(
        type(key) is str
        and key
        and not Path(key).is_absolute()
        and not Path(key).drive
        and "\\" not in key
        and all(part not in ("", ".", "..") for part in key.split("/"))
        and Path(key).as_posix() == key,
        "Exact original slash-relative spelling without adaptation",
    )

def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(("."), 1)[0] in forbidden for name in sys.modules),
        ("No numerical or scientific imports"),
    )
    require(
        not any(
            name.startswith(("research."))
            and name not in {__name__, ("research.limitation_program_20261001")}
            for name in sys.modules
        ),
        "No scientific source, auditor, kernel or historical helper imports",
    )
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not lexical.is_relative_to(_EXCLUDED_SCOPE[0])
                and not lexical.resolve(strict=False).is_relative_to(_EXCLUDED_SCOPE[1]),
                "No excluded loaded runtime source/cache",
            )
            if lexical.is_file():
                actual = canonical(lexical, fresh=True)
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                require(key in mapping, "No unknown loaded source or present cache after admission")
                require(
                    digest(actual, fresh=True) == mapping[key],
                    ("Loaded bytes retain original expected SHA"),
                )
            else:
                require(
                    attribute == "__cached__"
                    and not lexical.exists()
                    and not lexical.is_symlink()
                    and lexical.resolve(strict=False) == lexical,
                    "Only exact absent loaded cache route, never missing source or dangling alias",
                )

def source_protocol_checks(manifest):
    global _SOURCE_INTERPRETER
    protocol = read(bind(AUDIT / "protocol.json", PROTOCOL_SHA))
    require(
        protocol["schema"] == "a13-exp-frontier-recovery-independent-audit-protocol-v1"
        and protocol["operational_recovery_audit_version"] == 6
        and protocol["V6_ROOT_READY_SHA256"] == AUDIT_READY_SHA
        and protocol["output"] == AUDIT.relative_to(ROOT).as_posix()
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and protocol["independent_digits"] == 130
        and protocol["primary_digits"] == 90
        and protocol["fixed_grid"] == [list(row) for row in GRID]
        and protocol["threads"] == 1
        and protocol["gate_emission_authorized"] is False
        and protocol["new_fixture_credit"] == 0
        and protocol["candidate_G2_absolute_stock_error_allocation"] is None
        and protocol["candidate_G2_barrier_band_allocation"] is None,
        "Exact originally frozen V6 scientific scope and clocks, read as metadata only",
    )
    require(
        [len(protocol[field]) for field in (("frozen_inputs"), ("external_runtime_inputs"))]
        == [1198, 2842],
        "Complete original prospective source maps retained",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        require(type(protocol[field]) is dict, "Typed prospective full expected maps")
        for key, expected in protocol[field].items():
            budget()
            require(
                manifest[field].get(key) == expected,
                ("Every prospective source SHA expectation remains equal and strict"),
            )
    for name, expected in AUDIT_AUTHORS.items():
        require(
            manifest[("frozen_inputs")].get((RESEARCH / name).relative_to(ROOT).as_posix())
            == expected
            and REQUIRED_SNAPSHOTS[name] == expected,
            "Original executed trio and exact retained snapshots agree",
        )
    _SOURCE_INTERPRETER = read(AUDIT / "interpreter.json")
    require(
        _SOURCE_INTERPRETER == protocol[("interpreter")],
        ("Original full prepared interpreter record unchanged"),
    )
    require(
        _SOURCE_INTERPRETER["executable"] == str(LAUNCHER)
        and _SOURCE_INTERPRETER["base_executable"] == str(_BASE_SCOPE / "python.exe")
        and _SOURCE_INTERPRETER["base_prefix"] == str(_BASE_SCOPE)
        and _SOURCE_INTERPRETER["venv_prefix"] == str(ROOT / ".context/frontier_t0_env")
        and _SOURCE_INTERPRETER["sys_path"] == sys.path
        and _SOURCE_INTERPRETER["startup_bytecode_disabled"] is True
        and _SOURCE_INTERPRETER["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and _SOURCE_INTERPRETER["base_site_packages_import_rejected"] is True,
        "Exact original base/prefix/search/source-runtime scope, no scientific import",
    )
    for spelling in _SOURCE_INTERPRETER["absent_standard_runtime_paths"]:
        path = Path(spelling)
        require(
            path.is_absolute()
            and not path.exists()
            and not path.is_symlink()
            and path.resolve(strict=False) == path,
            "Original declared runtime absence remains exact",
        )
        _ABSENT_RUNTIME.add(path)
    for record in read(AUDIT / "loaded_module_origins.json"):
        budget()
        require(
            type(record) is dict
            and record["kind"] in ("source", "cache")
            and type(record["module"]) is str,
            "Saved original loaded origins are metadata only",
        )
        bind(Path(record["path"]), record["sha256"])
    return protocol

def saved_runtime_membership():
    """Rewalk original file roots, including opaque numerical sources, without imports."""
    require(_SOURCE_INTERPRETER is not None, "Full source runtime metadata admitted first")
    record = _SOURCE_INTERPRETER["runtime_inventory"]
    declared = record["actual_file_paths"]
    require(
        type(declared) is list and len(declared) == len(set(declared)) == record["files"] == 3057,
        "Complete original3057 unique runtime file inventory",
    )
    found = set()
    for spelling in record["roots"]:
        budget()
        root = canonical(spelling)
        if root.is_file():
            found.add(root)
        else:
            require(root.is_dir(), "Saved runtime root remains regular file or directory")
            for directory, dirs, names in os.walk(root, followlinks=False):
                budget()
                parent = canonical(directory)
                dirs[:] = [name for name in dirs if parent / name != _EXCLUDED_SCOPE[0]]
                for name in dirs:
                    child = parent / name
                    require(
                        not child.is_symlink() and canonical(child).is_relative_to(root),
                        ("Original runtime directory has no alias or escape"),
                    )
                for name in names:
                    found.add(canonical(parent / name))
                    require(
                        len(found) <= MAX_RUNTIME_FILES, ("Bounded complete saved runtime rewalk")
                    )
    expected_paths = {Path(path) for path in declared}
    require(found == expected_paths, "Complete actual original runtime membership unchanged")
    total = 0
    for path in found:
        budget()
        require(path.is_file(), "Saved runtime path stays a regular file")
        key = key_for(path)
        mapping = _FROZEN if path.is_relative_to(ROOT) else _EXTERNAL
        require(key in mapping, "Every saved runtime member has an original admitted expected SHA")
        total += path.stat().st_size
    require(
        total == record[("bytes")] and total <= MAX_RUNTIME_BYTES,
        ("Original runtime byte count and caps unchanged"),
    )
    adjacent = {str(path) for path in _BASE_SCOPE.iterdir() if path.is_file()}
    require(
        adjacent == set(_SOURCE_INTERPRETER[("external_adjacent_files")]),
        ("Original full base adjacent membership unchanged"),
    )
    prefix = ROOT / ".context/frontier_t0_env"
    prefix_members = sorted(
        [path.name, ("file") if path.is_file() else ("directory")] for path in prefix.iterdir()
    )
    require(
        prefix_members == _SOURCE_INTERPRETER[("venv_root_directory_membership")],
        ("Original venv root membership unchanged"),
    )
    hooks = {str(path) for path in (prefix / "Lib/site-packages").glob("*.pth")}
    require(
        hooks
        == {
            path
            for path in _SOURCE_INTERPRETER[("bootstrap_hook_and_loaded_venv_paths")]
            if path.endswith((".pth"))
        },
        "No new or removed startup hook",
    )
    return {
        ("saved_runtime_files"): len(found),
        ("saved_runtime_bytes"): total,
        ("numerical_package_sources_hashed_not_imported"): True,
    }

def source_clocks(document):
    budget()
    require(
        document["budget"]["process_CPU_seconds"] >= 0
        and document["budget"]["process_CPU_seconds"] < 300
        and document["budget"]["wall_seconds"] >= 0
        and document["budget"]["wall_seconds"] < 900,
        "Retained source clock snapshots fit original limits; not a final OS-exit observation",
    )

def reconcile_metadata(manifest):
    summary = read(AUDIT / "summary.json")
    require(
        summary["schema"] == "a13-exp-frontier-recovery-independent-audit-summary-v1"
        and summary["operational_recovery_audit_version"] == 6
        and summary["V6_ROOT_READY_SHA256"] == AUDIT_READY_SHA,
        "Exact current all20 scientific summary metadata",
    )
    for key in (
        "completed",
        "passed",
        "independent_audit_passed",
        "metadata_source_passed",
        "scientific_screen_complete",
        "all20_uniformly_certified",
        "all_untrusted_claimed_rows_independently_recertified",
        "every_claimed_primary80_uniform_bound_authorized_by_independent130",
        "independent112_uniform_witnesses_retained_separately",
        "exact_finite_fitting_transcript_and_single_tie_even_quantization_checked",
        "all_claimed_native_intermediate72_product144_and_shift_guards_independently_recomputed",
        (
            "all_claimed_selector_QROM_argument_output_copies_banks_"
            "and_cleanup_costs_independently_reconstructed"
        ),
        "global_financial_forward_and_inverse_clean_function_invocations_paid",
        "symbolic_resources_not_actual_source_or_capped_schedule",
        "original_failure_remains_authoritative_zero_credit",
    ):
        require(summary[key] is True, "Retained scoped all20 certification claim: " + key)
    for key in (
        "rejection",
        "budget_censored",
        "failed_original_source_mathematical_PASS",
        "partial_v5_rows_promoted",
        "old_censored_proof_rows_promoted_or_reused",
        "scientific_producer_or_helper_imports",
        "source_expected_hashes_waived",
        "gate_emission_authorized",
        "full_G2",
        "adoption",
        "cost_transfer",
        "feasible_architecture_or_realized_cost_improvement_claim",
    ):
        require(summary[key] is False, "Retained scientific scope prohibition: " + key)
    for key in (
        "new_test_credit",
        "new_gate_replays",
        "new_price_samples",
        "retained_rejected_rows",
        "prior_failed_recovery_audit_credit",
        "prior_failed_recovery_audit_v2_credit",
        "prior_failed_recovery_audit_v3_credit",
        "prior_failed_recovery_audit_v4_credit",
        "prior_failed_recovery_audit_v5_credit",
    ):
        require(summary[key] == 0, "Zero new or prior-failure credit: " + key)
    require(
        summary["fixed_architecture_rows"] == summary["certified_estimate_rows"] == 20
        and summary["candidate_G2_absolute_stock_error_allocation"] is None
        and summary["candidate_G2_barrier_band_allocation"] is None,
        "Exactly all20 finite certificates without G2 allocation or feasibility",
    )
    source_clocks(summary)
    index = read(AUDIT / "fixed_inventory_authorization.json")
    require(
        index["all20_rows_and_rejections_retained"] is True
        and index["original_baseline_retained_separately"] is True
        and index["fixed_row_statuses"] == summary["fixed_row_statuses"],
        "Complete source row-status metadata equals exact summary",
    )
    expected_statuses = [
        {
            ("degree"): d,
            ("segments"): s,
            ("row_id"): f"d{d}_s{s}",
            ("status"): ("CERTIFIED_ESTIMATE"),
        }
        for d, s in GRID
    ]
    require(
        index[("fixed_row_statuses")] == expected_statuses,
        ("Exactly20 ordered certified fixed architecture statuses"),
    )
    rows = index["independent_row_artifacts"]
    require(type(rows) is list and len(rows) == 20, "Exactly20 original artifact descriptors")
    for descriptor, (degree, segments) in zip(rows, GRID, strict=True):
        budget()
        route = f"rows/d{degree}_s{segments}.json.gz"
        require(
            descriptor["actual_row_file"] == route
            and descriptor["row_id"] == f"d{degree}_s{segments}"
            and descriptor["degree"] == degree
            and descriptor["segments"] == segments
            and descriptor["status"] == "CERTIFIED_ESTIMATE"
            and descriptor["artifact_encoding"] == "canonical-gzip-json-v1"
            and descriptor["compact_sorted_JSON"] is True
            and descriptor["compression_level"] == 1
            and descriptor["gzip_filename"] == ""
            and descriptor["gzip_mtime"] == 0
            and descriptor["compressed_SHA256"] == manifest["files"][route]
            and descriptor["compressed_bytes"] == (AUDIT / route).stat().st_size,
            "Exact named freshly generated row descriptor and opaque compressed-byte expectation",
        )
        require(
            type(descriptor["uncompressed_JSON_SHA256"]) is str
            and len(descriptor["uncompressed_JSON_SHA256"]) == 64
            and all(c in "0123456789abcdef" for c in descriptor["uncompressed_JSON_SHA256"])
            and type(descriptor[("uncompressed_bytes")]) is int
            and descriptor[("uncompressed_bytes")] > 0,
            "Saved uncompressed descriptor is typed metadata, never a decompression claim",
        )
    outcome = read(AUDIT / "completion_outcome.json")
    require(
        outcome["phase"] == "run"
        and outcome["summary_file"] == "summary.json"
        and outcome["limits_CPU_admission_wall"] == [300, 270, 900],
        "Original exact completed run terminal and immutable clocks",
    )
    for key in (
        ("completed"),
        ("passed"),
        ("independent_audit_passed"),
        ("metadata_source_passed"),
        ("scientific_screen_complete"),
    ):
        require(outcome[key] is True, "Actual completed terminal metadata")
    for key in (
        ("budget_censored"),
        ("rejection"),
        ("full_G2"),
        ("adoption"),
        ("cost_transfer"),
        ("gate_emission_authorized"),
    ):
        require(outcome[key] is False, "Terminal retains exploratory scope and no failure")
    require(outcome["new_test_credit"] == 0, "Terminal supplies zero new programme credit")
    source_clocks(outcome)
    return {
        "current_scoped_all20_certification_metadata_reconciled": True,
        "saved_precision": {"primary": 90, "independent": 130, "separate_witness_order": 112},
        "fixed_certified_statuses": expected_statuses,
        "complete25_snapshot_count": 25,
        "complete20_opaque_row_count": 20,
        "current_owned_count_including_manifest": 64,
        "source_complete_counts": AUDIT_COUNTS,
        "proof_payload_decompressed_or_recomputed": False,
        "saved_uncompressed_descriptor_verified_as_actual_payload": False,
        "retained_source_summary_budget": summary["budget"],
        "retained_source_outcome_budget": outcome["budget"],
        **flags(),
    }

def retain_failure(error):
    try:
        v11_output_custody()
    except BaseException:
        return
    try:
        budget()
        save(
            "failure.json",
            {
                "passed": False,
                "completed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                **flags(),
            },
        )
    except BaseException:
        pass
    try:
        v11_output_custody()
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"new_scientific_outcome_uncertified":true,"full_G2":false,"adoption":false,"quantum_advantage":false}\n'
            )
        v11_output_custody()
    except BaseException:
        pass

def packet(name, pin, counts, schema, owned_contract, terminal_header=True):
    directory = canonical(PROGRAM / name)
    manifest = bind(directory / "manifest.json", pin)
    data = read(manifest)
    require(
        data["schema"] == schema and data["manifest_self_hash_excluded"] is True,
        "Exact externally pinned owner schema and self-excluded manifest",
    )
    require(
        [len(data[k]) for k in ("files", "frozen_inputs", "external_runtime_inputs")] == counts,
        "Complete original owner maps without reduced index",
    )
    if terminal_header:
        require(
            data["completed"] is True
            and data["passed"] is True
            and data["budget_censored"] is False,
            "Actual completed owner, never partial success",
        )
    no_failure(directory)
    members = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        mapping = data[field]
        require(type(mapping) is dict, "Typed complete owner map")
        for key, expected in mapping.items():
            budget()
            if field == "external_runtime_inputs":
                require(type(key) is str and Path(key).is_absolute(), "Exact absolute external key")
                path = Path(key)
            else:
                exact_relative(key)
                path = (
                    directory / key
                    if field == "files" and owned_contract == "receipt"
                    else ROOT / key
                )
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory) and actual not in members,
                    "Complete unique physically confined owner member",
                )
                required = (
                    actual.relative_to(directory).as_posix()
                    if owned_contract == "receipt"
                    else actual.relative_to(ROOT).as_posix()
                )
                require(required == key, "Exact original owner spelling")
                members.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact ROOT-relative original input expectation",
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Exact original absolute external expectation",
                )
    require(
        inventory(directory) == members and len(members) == counts[0] + 1,
        "Full physical owner membership plus manifest",
    )
    _OWN_INVENTORIES[directory] = members
    return data

def rational(value):
    budget()
    require(
        type(value) is list and len(value) == 2 and all(type(v) is int for v in value),
        "Canonical exact rational integer pair, never floats or booleans",
    )
    require(
        value[1] > 0 and all(abs(v).bit_length() <= MAX_SCALAR_BITS for v in value),
        "Positive denominator and prospective2048-bit saved scalar cap",
    )
    result = Fraction(value[0], value[1])
    require([result.numerator, result.denominator] == value, "Original reduced rational schema")
    budget()
    return result

def pair(value):
    budget()
    result = [value.numerator, value.denominator]
    require(
        all(abs(v).bit_length() <= MAX_RESULT_BITS for v in result),
        "Finite8192-bit derived pair fits original4300-digit JSON policy",
    )
    return result

def failed_material_witness(initial=False):
    global _FAILED_MATERIAL_MEMBERS, _FAILED_MATERIAL_BYTES
    record = read(METADATA_SOURCE / "material_inventory.json")
    require(
        record["schema"] == "a13-exp-frontier-untrusted-material-inventory-v1"
        and record["material_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and record["original_terminal_failure_authoritative"] is True
        and record["original_manifest_absent"] is True
        and record["exact_file_count"] == 42
        and record["original_file_bytes"] == 243935317,
        "Full original42 failed-owned bytes remain failed, not adopted",
    )
    mapping = record["files"]
    require(type(mapping) is dict and len(mapping) == 42, "Exact failed material inventory")
    members, total = set(), 0
    for key, entry in mapping.items():
        budget()
        exact_relative(key)
        path = MATERIAL / key
        require(
            entry["ROOT_relative_path"] == path.relative_to(ROOT).as_posix()
            and _FROZEN.get(entry["ROOT_relative_path"]) == entry["sha256"],
            "Failed input inherits original prospective expected SHA, no observed substitution",
        )
        actual = canonical(path)
        require(
            actual.is_relative_to(MATERIAL)
            and actual not in members
            and actual.is_file()
            and type(entry["bytes"]) is int
            and entry["bytes"] >= 0
            and actual.stat().st_size == entry["bytes"],
            "Complete failed-owned physical member",
        )
        members.add(actual)
        total += entry["bytes"]
    require(
        inventory(MATERIAL) == members
        and total == 243935317
        and (MATERIAL / "FAILED_UNSEALED.json").is_file()
        and not (MATERIAL / "manifest.json").exists()
        and not (MATERIAL / "manifest.json").is_symlink(),
        "Original authoritative failure and complete42 inventory remain unchanged",
    )
    if initial:
        _FAILED_MATERIAL_MEMBERS, _FAILED_MATERIAL_BYTES = members, total
    else:
        require(
            members == _FAILED_MATERIAL_MEMBERS and total == _FAILED_MATERIAL_BYTES,
            "Both union-side original failure inventories identical",
        )
    return {
        "files": len(members),
        "bytes": total,
        "authoritative_failed": True,
        "new_scientific_credit": 0,
    }

def selection_failure_witnesses():
    budget()
    require(
        inventory(PRIOR_SELECTION) == _SELECTION_FAILED_MEMBERS
        and len(_SELECTION_FAILED_MEMBERS) == 7
        and sum(fingerprint(path)[2] for path in _SELECTION_FAILED_MEMBERS) == 115343
        and (PRIOR_SELECTION / "FAILED_UNSEALED.json").is_file()
        and not (PRIOR_SELECTION / "manifest.json").exists()
        and not (PRIOR_SELECTION / "manifest.json").is_symlink(),
        "Original seven-file selector V1 stays failed, immutable and unapproved",
    )
    budget()

def admit_prior_selection_failure(ready, policy):
    expectations = {
        "prior_selector_failed_owned_freeze_SHA256": PRIOR_SELECTION_FREEZE_SHA,
        "prior_selector_READY_SHA256": PRIOR_SELECTION_READY_SHA,
        "prior_selector_log_SHA256": PRIOR_SELECTION_LOG_SHA,
        "prior_selector_author_SHA256": PRIOR_SELECTION_AUTHORS,
    }
    require(
        all(ready[key] == policy[key] == value for key, value in expectations.items()),
        "Externally frozen prior selector failure expectations without refresh",
    )
    record = read(bind(PRIOR_SELECTION_FREEZE, PRIOR_SELECTION_FREEZE_SHA))
    require(
        record["schema"] == "root-a13-certified-selection-v1-failed-owned-freeze-v1"
        and record["route"] == PRIOR_SELECTION.relative_to(ROOT).as_posix()
        and record["owned_file_count"] == 7
        and record["owned_bytes"] == 115343
        and record["manifest_absent"] is True
        and record["all_partial_results_unapproved"] is True
        and record["terminal_CPU_wall_uncertified"] is True
        and record["rational_selection_complete"] is False
        and record["fixture_credit"] == 0
        and record["observed_owned_expectations_do_not_replace_original_expected_hashes"] is True
        and record["READY_path"] == PRIOR_SELECTION_READY.relative_to(ROOT).as_posix()
        and record["READY_SHA256"] == PRIOR_SELECTION_READY_SHA
        and record["log_path"] == PRIOR_SELECTION_LOG.relative_to(ROOT).as_posix()
        and record["log_SHA256"] == PRIOR_SELECTION_LOG_SHA,
        "Exact ROOT-only frozen prior observed failure, no science approval",
    )
    mapping = record["owned_files"]
    require(
        type(mapping) is dict and len(mapping) == 7, "Complete prior observed-owned expected map"
    )
    for key, expected in mapping.items():
        exact_relative(key)
        path = bind(PRIOR_SELECTION / key, expected)
        require(
            path.is_relative_to(PRIOR_SELECTION)
            and path.relative_to(PRIOR_SELECTION).as_posix() == key
            and path not in _SELECTION_FAILED_MEMBERS,
            "Unique exact receipt-relative failed-owned membership",
        )
        _SELECTION_FAILED_MEMBERS.add(path)
    prior_ready = read(bind(PRIOR_SELECTION_READY, PRIOR_SELECTION_READY_SHA))
    require(
        prior_ready["schema"] == "root-a13-certified-candidate-selection-READY-v1"
        and prior_ready["author_method_SHA256"] == PRIOR_SELECTION_AUTHORS
        and prior_ready["output"] == PRIOR_SELECTION.relative_to(ROOT).as_posix(),
        "Every original executed author and original READY expectation retained",
    )
    for name, expected in PRIOR_SELECTION_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_SELECTION_LOG, PRIOR_SELECTION_LOG_SHA)
    code_caches(
        [RESEARCH / "select_a13_certified_candidates_v1.py"],
        prior_ready["existing_new_code_cache_SHA256"],
        prior_ready["absent_new_code_cache_paths"],
    )
    marker = read(PRIOR_SELECTION / "FAILED_UNSEALED.json")
    failure = read(PRIOR_SELECTION / "failure.json")
    require(
        marker["passed"] is False
        and marker["completed"] is False
        and marker["hard_budget_state_uncertified"] is True
        and failure["passed"] is False
        and failure["completed"] is False,
        "Authoritative prior failure is never promoted by new selection",
    )
    selection_failure_witnesses()

def prior_inventory_failure_witness():
    budget()
    require(
        canonical(PRIOR_INVENTORY.parent) == PROGRAM
        and PRIOR_INVENTORY.resolve(strict=False) == PRIOR_INVENTORY
        and not PRIOR_INVENTORY.exists()
        and not PRIOR_INVENTORY.is_symlink(),
        "Original pre-output inventory failure route remains physically wholly absent",
    )
    for path, expected in (
        (PRIOR_INVENTORY_WITNESS, PRIOR_INVENTORY_WITNESS_SHA),
        (PRIOR_INVENTORY_READY, PRIOR_INVENTORY_READY_SHA),
        (PRIOR_INVENTORY_LOG, PRIOR_INVENTORY_LOG_SHA),
        *((RESEARCH / name, expected) for name, expected in PRIOR_INVENTORY_AUTHORS.items()),
    ):
        require(
            digest(path, fresh=True) == expected,
            "Every original pre-output failure byte retains its ROOT expected SHA",
        )
    witness = read(PRIOR_INVENTORY_WITNESS)
    require(
        witness
        == {
            "schema": "root-a13-d4-s4-native-inventory-v1-prefit-failure-witness-v1",
            "actual_failed_before_output_creation": True,
            "all_scientific_results_unapproved": True,
            "failure_observed": "Exact original base/prefix/search/source-runtime scope, no scientific import",
            "invocation": "-I -S -B research/limitation_program_20261001/contract_a13_d4_s4_native_inventory_v1.py --ready-sha256 "
            + PRIOR_INVENTORY_READY_SHA,
            "metadata_only": True,
            "native_inventory_scientific_execution_started": False,
            "new_fixture_credit": 0,
            "original_READY_expected_SHA256": PRIOR_INVENTORY_READY_SHA,
            "original_READY_path": PRIOR_INVENTORY_READY.relative_to(ROOT).as_posix(),
            "original_author_expected_SHA256": PRIOR_INVENTORY_AUTHORS,
            "original_expected_hashes_or_runtime_scope_waived": False,
            "original_log_SHA256": PRIOR_INVENTORY_LOG_SHA,
            "original_log_path": PRIOR_INVENTORY_LOG.relative_to(ROOT).as_posix(),
            "output_route": PRIOR_INVENTORY.relative_to(ROOT).as_posix(),
            "output_route_absent": True,
            "passed": False,
            "terminal_CPU_wall_uncertified": True,
        },
        "Exact ROOT-only pre-output failure record with no partial scientific approval",
    )
    budget()

def admit_prior_inventory_failure(ready, policy):
    expectations = {
        "prior_inventory_failure_witness_SHA256": PRIOR_INVENTORY_WITNESS_SHA,
        "prior_inventory_READY_SHA256": PRIOR_INVENTORY_READY_SHA,
        "prior_inventory_log_SHA256": PRIOR_INVENTORY_LOG_SHA,
        "prior_inventory_author_SHA256": PRIOR_INVENTORY_AUTHORS,
        "prior_inventory_output_route_absent": True,
        "runtime_invocation": V11_PRODUCER_INVOCATION,
        "original_runtime_scope_and_expected_SHA_checks_waived": False,
    }
    require(
        all(ready[key] == policy[key] == expected for key, expected in expectations.items()),
        "Externally frozen failed V1 bytes and exact compatible V2 launch without waiver",
    )
    for path, expected in (
        (PRIOR_INVENTORY_WITNESS, PRIOR_INVENTORY_WITNESS_SHA),
        (PRIOR_INVENTORY_READY, PRIOR_INVENTORY_READY_SHA),
        (PRIOR_INVENTORY_LOG, PRIOR_INVENTORY_LOG_SHA),
        *((RESEARCH / name, expected) for name, expected in PRIOR_INVENTORY_AUTHORS.items()),
    ):
        bind(path, expected)
    prior_ready = read(PRIOR_INVENTORY_READY)
    require(
        prior_ready["schema"] == "root-a13-d4-s4-native-contract-inventory-READY-v1"
        and prior_ready["author_method_SHA256"] == PRIOR_INVENTORY_AUTHORS
        and prior_ready["output"] == PRIOR_INVENTORY.relative_to(ROOT).as_posix()
        and prior_ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and prior_ready["audit_manifest_SHA256"] == AUDIT_SHA
        and prior_ready["audit_complete_counts"] == AUDIT_COUNTS
        and prior_ready["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and prior_ready["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and prior_ready["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Original executed V1 release and all its expected source premises are immutable",
    )
    code_caches(
        [RESEARCH / "contract_a13_d4_s4_native_inventory_v1.py"],
        prior_ready["existing_new_code_cache_SHA256"],
        prior_ready["absent_new_code_cache_paths"],
    )
    _ABSENT_RUNTIME.add(PRIOR_INVENTORY)
    prior_inventory_failure_witness()

def held_v1_witness():
    for path, expected in HELD_V1_INPUTS:
        budget()
        key = path.relative_to(ROOT).as_posix()
        require(key in _FROZEN and _FROZEN[key] == expected,
                "Held V1 input uses independently fixed original expected SHA")
        require(digest(path, fresh=True) == expected, "All six held V1 bytes freshly unchanged")
    for path in (HELD_V1_READY, HELD_V1_OUTPUT):
        budget()
        require(not path.exists() and not path.is_symlink()
                and path.resolve(strict=False) == path,
                "Held V1 had no READY, output, execution or substitute route")
    qa, peer = read(HELD_V1_QA), read(HELD_V1_PEER)
    require(qa["schema"] == "a13-first-signed-leaf-author-static-qa-v1"
            and qa["author_only_unexecuted"] is True
            and qa["exact_author_packet"] == HELD_V1_AUTHORS
            and qa["new_READY_absent"] is True and qa["new_output_route_absent"] is True,
            "Original V1 author-only QA is retained, never a completed run")
    require(peer["schema"] == "a13-d4-s4-first-signed-leaf-independent-static-peer-v1"
            and peer["status"] == "HOLD" and peer["passed"] is False
            and peer["exact_author_quartet"] == HELD_V1_AUTHORS
            and len(peer["blockers"]) == 1,
            "Original independent V1 HOLD remains authoritative and unexecuted")
    return {"schema": "a13-first-signed-leaf-held-v1-witness-v1",
            "author_SHA256": HELD_V1_AUTHORS, "QA_SHA256": HELD_V1_QA_SHA,
            "independent_HOLD_SHA256": HELD_V1_PEER_SHA,
            "original_READY_and_output_absent": True,
            "original_scientific_result_or_resources": None, "fixture_credit": 0}

def admit_held_v1(ready, policy):
    fixed = {"held_unexecuted_V1_author_SHA256": HELD_V1_AUTHORS,
             "held_unexecuted_V1_QA_SHA256": HELD_V1_QA_SHA,
             "held_unexecuted_V1_independent_HOLD_SHA256": HELD_V1_PEER_SHA,
             "held_unexecuted_V1_READY_absent": HELD_V1_READY.relative_to(ROOT).as_posix(),
             "held_unexecuted_V1_output_absent": HELD_V1_OUTPUT.relative_to(ROOT).as_posix(),
             "fresh_loaded_source_and_present_cache_checks": True,
             "unknown_present_loaded_origin_rejected": True,
             "postadmission_observed_expected_promotion": False,
             "runtime_optimization_level": 0,
             "PYTHONOPTIMIZE_environment_absent": True}
    require(all(ready[key] == policy[key] == expected for key, expected in fixed.items()),
            "Separate guard-only V2 release and immutable V1 HOLD history")
    for path, expected in HELD_V1_INPUTS:
        bind(path, expected)
    code_caches([RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_v1.py",
                 RESEARCH / "build_a13_d4_s4_first_signed_leaf_v1.py"],
                ready["held_V1_existing_code_cache_SHA256"],
                ready["held_V1_absent_code_cache_paths"])
    held_v1_witness()

def held_audit_V1_absences():
    for key in (HELD_AUDIT_V1_READY_KEY, HELD_AUDIT_V1_OUTPUT_KEY):
        budget()
        path = ROOT / key
        require(not path.exists() and not path.is_symlink()
                and path.resolve(strict=False) == path,
                "Unexecuted held independent-audit V1 READY/output remain wholly absent without alias")
    budget()

def admit_held_audit_V1(ready, policy):
    fixed = {
        "held_audit_V1_author_expected_SHA256": HELD_AUDIT_V1_AUTHORS,
        "held_audit_V1_report_expected_SHA256": HELD_AUDIT_V1_REPORTS,
        "held_audit_V1_READY_absent_path": HELD_AUDIT_V1_READY_KEY,
        "held_audit_V1_output_absent_path": HELD_AUDIT_V1_OUTPUT_KEY,
        "V2_independent_science_cases_phase_resources_and_caps_exact_V1": True,
        "V2_original_selector_five_expected_fields_restored": True,
        "V2_current_selector_permission_is_saved_independent_audit_only": True,
    }
    require(all(ready[key] == policy[key] == expected for key, expected in fixed.items()),
            "Narrow V2 admission correction and bounded immutable unexecuted audit V1 history")
    for name, expected in HELD_AUDIT_V1_AUTHORS.items():
        bind(RESEARCH / name, expected)
    records = {key: read(bind(ROOT / key, expected))
               for key, expected in HELD_AUDIT_V1_REPORTS.items()}
    root_hold = records[".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_ROOT_STATIC_HOLD_run001.json"]
    require(root_hold["schema"] == "root-a13-completed-leaf-audit-static-hold-v1"
            and root_hold["status"] == "HOLD" and root_hold["passed"] is False
            and root_hold["author_method_SHA256"] == HELD_AUDIT_V1_AUTHORS
            and root_hold["new_READY_and_output_absent"] is True
            and root_hold["scientific_method_or_diagnostic_failure_claimed"] is False
            and root_hold["fixture_credit"] == 0 and len(root_hold["blockers"]) == 2,
            "Original ROOT hold is unexecuted metadata-only, never a scientific failure")
    peer_hold = records[".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_STATIC_HOLD_run001.json"]
    require(peer_hold["status"] == "HOLD" and peer_hold["passed"] is False
            and len(peer_hold["blockers"]) == 2,
            "Original independent static admission hold remains authoritative")
    code_caches([RESEARCH / "audit_a13_d4_s4_first_signed_leaf_v1.py"],
                ready["held_audit_V1_existing_code_cache_SHA256"],
                ready["held_audit_V1_absent_code_cache_paths"])
    for key in (HELD_AUDIT_V1_READY_KEY, HELD_AUDIT_V1_OUTPUT_KEY):
        _ABSENT_RUNTIME.add(ROOT / key)
    held_audit_V1_absences()
    budget(admission=True)

def fit_round_metadata(fit, degree):
    rounds = fit["exchange_rounds"]
    require(
        type(rounds) is list and len(rounds) == 32,
        "Exactly32 original exchange record objects, not an integer count",
    )
    previous_nodes = None
    for number, record in enumerate(rounds, 1):
        budget()
        require(
            type(record) is dict
            and set(record)
            == {
                "round",
                "solve_nodes",
                "solved_coefficients",
                "solved_alternating_error",
                "candidate_stationary_brackets",
                "candidate_extrema",
                "candidate_residuals",
                "exact_exchange_bottleneck",
                "exact_two_pass_bottleneck_then_sum_lex",
                "selected_next_node_indices",
                "selected_next_nodes",
            }
            and type(record["round"]) is int
            and record["round"] == number
            and type(record["solve_nodes"]) is list
            and len(record["solve_nodes"]) == degree + 2
            and type(record["solved_coefficients"]) is list
            and len(record["solved_coefficients"]) == degree + 1
            and type(record["selected_next_nodes"]) is list
            and len(record["selected_next_nodes"]) == degree + 2
            and type(record["selected_next_node_indices"]) is list
            and len(record["selected_next_node_indices"]) == degree + 2
            and record["exact_two_pass_bottleneck_then_sum_lex"] is True,
            "Complete original ordered solve/exchange metadata remains exact",
        )
        require(
            previous_nodes is None or record["solve_nodes"] == previous_nodes,
            "Every original next solve uses the previous selected nodes, no hidden round",
        )
        previous_nodes = record["selected_next_nodes"]
    require(
        type(fit["coefficients_before_quantization"]) is list
        and len(fit["coefficients_before_quantization"]) == degree + 1
        and fit["coefficients_before_quantization"] == rounds[-1]["solved_coefficients"]
        and fit["coefficients_from_round32_solve"] is True
        and fit["extra33rd_solve"] is False
        and fit["root_search_fitting_evidence_only"] is True,
        "Original final32-solve coefficient anchor and authorized raw quantization unchanged",
    )

def independent_removal(target, source, sites, started):
    nodes = {node["out"][0]: node for node in target["nodes"]}
    endpoints = {site["polynomial"] for site in sites}
    boundaries = {site["remainder"] for site in sites}
    closure, pending = set(), list(endpoints)
    while pending:
        check(started)
        value = pending.pop()
        if value in boundaries or value in closure:
            continue
        node = nodes[value]
        require(
            node["op"] in ("const", "add", "mul") and len(node["out"]) == 1,
            "Actual original active polynomial closure",
        )
        closure.add(value)
        pending.extend(node["args"])
    replaceable_consumers = {site["stock"] for site in sites}
    retained = set()
    for value, node in nodes.items():
        check(started)
        if value not in closure and value not in replaceable_consumers:
            retained.update(argument for argument in node["args"] if argument in closure)
    changed = True
    while changed:
        check(started)
        changed = False
        for value in tuple(retained):
            for argument in nodes[value]["args"]:
                if argument in closure and argument not in retained:
                    retained.add(argument)
                    changed = True
    removable = closure - retained
    indices = [
        index for index, call in enumerate(source["forward_calls"]) if call["out"][0] in removable
    ]
    require(len(indices) == len(removable), "One actual removable forward call per SSA value")
    return dict(
        active_polynomial_value_ids=sorted(closure),
        retained_shared_or_dead_ancestor_value_ids=sorted(retained),
        removed_value_ids=sorted(removable),
        removed_forward_call_indices=indices,
        eager_unused_values_outside_closure_retained=True,
    )

def check(started):
    budget()

def v11_admitted_source_bytes(path):
    global _HASH_WORK
    budget()
    actual = canonical(path, fresh=True)
    expected = _FROZEN.get(actual.relative_to(ROOT).as_posix())
    require(expected is not None, "Text AST source admitted from exact original expected map first")
    before = fingerprint(actual)
    require(before[2] <= 8 << 20 and actual.is_file(), "Finite source text AST admission")
    chunks, size = [], 0
    with actual.open("rb") as stream:
        while chunk := stream.read(65536):
            budget()
            size += len(chunk)
            _HASH_WORK += len(chunk)
            require(
                size <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                "Complete charged bounded source text read",
            )
            chunks.append(chunk)
    raw = b"".join(chunks)
    require(
        size == before[2]
        and fingerprint(actual) == before
        and hashlib.sha256(raw).hexdigest() == expected
        and canonical(path, fresh=True) == actual,
        "Fresh original source bytes before nonexecuting AST parse",
    )
    budget()
    return raw

def admitted_text_AST(path):
    raw = v11_admitted_source_bytes(path)
    tree = ast.parse(raw)
    budget()
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

def copied_metadata_provenance():
    own = admitted_text_AST(AUTHOR)
    old_selector = admitted_text_AST(RESEARCH / "select_a13_certified_candidates_v2.py")
    old_audit = admitted_text_AST(RESEARCH / "audit_exp_frontier_recovery_v6.py")
    for name, expected in (
        ("fit_round_metadata", old_selector["fit_round_metadata"]),
        ("independent_removal", old_audit["independent_removal"]),
    ):
        require(
            ast.dump(own[name], include_attributes=False)
            == ast.dump(expected, include_attributes=False),
            "Exact unexecuted original metadata/closure helper text, no source import",
        )
    budget()

def current_controller_code_guard():
    """Compare loaded functions with exact admitted source compilation without executing it."""
    path = canonical(AUTHOR, fresh=True)
    raw = v11_admitted_source_bytes(path)
    tree = ast.parse(raw)
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    expected = compile(raw, str(AUTHOR), "exec", dont_inherit=True, optimize=sys.flags.optimize)
    codes = {code.co_name: code for code in expected.co_consts
             if isinstance(code, types.CodeType) and code.co_name in names}
    require(set(codes) == names, "Exactly declared source functions, no namespace substitution")
    for name in sorted(names):
        budget()
        function = globals()[name]
        require(isinstance(function, types.FunctionType) and function.__globals__ is globals()
                and function.__code__ == codes[name], "Every loaded controller function equals source code")
    budget()

def runtime_invocation_guard(ready_sha):
    require(
        __name__ == "__main__"
        and __package__ == "research.limitation_program_20261001"
        and __spec__ is not None
        and __spec__.name == INVENTORY_MODULE
        and canonical(__spec__.origin) == AUTHOR
        and sys.orig_argv[1:] == RUNTIME_INVOCATION + ["--ready-sha256", ready_sha]
        and sys.flags.isolated == 0
        and sys.flags.no_site == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is False
        and sys.flags.optimize == 0
        and "PYTHONOPTIMIZE" not in os.environ
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True
        and canonical(Path.cwd()) == ROOT
        and sys.path[0] == str(ROOT),
        "Exact original-runtime-compatible -B -m invocation from workspace root",
    )

def flags():
    return {
        "v11_ordered_standalone_signed_leaf_only": True,
        "independent_completed_leaf_audit_only": True,
        "completed_v11_minimum75_saved_array_only": True,
        "new_native_or_toy_gate_arrays_constructed": 0,
        "original_native_inventory_and_independent_audit_are_frozen_inputs": True,
        "new_scientific_evaluation": True,
        "scientific_imports_or_proof_decompression": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "candidate_G2_absolute_stock_error_allocation": None,
        "candidate_G2_barrier_band_allocation": None,
        "candidate_feasibility": False,
        "actual_emitted_source_or_capped_schedule": False,
        "actual_gate_schedule_or_cost_verified": False,
        "gate_emission_authorized": False,
        "financial_gate_emission_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "old_failed_source_mathematical_PASS": False,
        "old_V5_and_partial_A20_failures_approved": False,
        "historical_global_LIVE_integrity_approved": False,
        "nested_historical_manifests_admitted_as_success": False,
        "held_A13_null_allocation_fields_changed": False,
        "local_only": True,
    }

def v11_full_optimization_cache_guard(sources, pins, absent_keys):
    """External complete default/opt1/opt2 cache partition before bootstrap and both unions."""
    budget()
    routes = {key_for(Path(cache_from_source(str(source), optimization=opt))):
              Path(cache_from_source(str(source), optimization=opt))
              for source in sources for opt in ("", "1", "2")}
    present = {key for key, path in routes.items() if path.exists()}
    require(type(pins) is dict and set(pins) == present and type(absent_keys) is list
            and absent_keys == sorted(set(routes) - present),
            "Exact externally frozen all-optimization cache partition; no observation promotion")
    for key in present:
        path = bind(routes[key], pins[key])
        _CODE_CACHE_EXPECTED[path] = pins[key]
    for key in absent_keys:
        path = routes[key]
        require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                "Exact absent all-optimization cache routes without dangling aliases")
        _ABSENT_RUNTIME.add(path)
    budget()

class HighSignCopyReject(ValueError):  # noqa: N818 - fixed ROOT diagnostic name
    """Only the fixed high-sign output-copy validator raises this diagnostic."""

def v11_read_rows(descriptor):
    global _HASH_WORK
    path = canonical(V11_LEAF / "native_gate_rows.i32", fresh=True)
    expected = _FROZEN[key_for(path)]
    before = fingerprint(path)
    require(0 < descriptor["gate_rows"] <= LEAF_MAX_ROWS
            and before[2] == descriptor["gate_rows"] * 16 <= MAX_OWN_BYTES,
            "Whole externally expected native Nx4 payload, no generated comparison array")
    raw_parts, total, state = [], 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(65536):
            budget()
            total += len(block)
            _HASH_WORK += len(block)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "All actual native read work charged")
            raw_parts.append(block)
            state.update(block)
    require(total == before[2] and fingerprint(path) == before and state.hexdigest() == expected
            and canonical(V11_LEAF / "native_gate_rows.i32", fresh=True) == path,
            "Stable complete saved producer array equals externally supplied expected SHA")
    require(sys.byteorder == "little" and array("i").itemsize == 4, "Pinned actual little-endian int32 ABI")
    rows = array("i")
    rows.frombytes(b"".join(raw_parts))
    require(len(rows) == descriptor["gate_rows"] * 4, "Every native word retained")
    return rows

def v11_native_gate(rows, index, qubits):
    at = 4 * index
    require(0 <= at <= len(rows) - 4, "Complete actual native row within saved array")
    kind = rows[at]
    require(kind in (1, 2, 3), "Saved opcode only X/CX/CCX")
    wires = tuple(rows[at + offset] for offset in range(1, kind + 1))
    require(len(set(wires)) == kind and all(0 <= wire < qubits for wire in wires)
            and all(rows[at + offset] == 0 for offset in range(kind + 1, 4)),
            "Every actual saved wire, distinct operand and padding checked")
    return kind, wires

def v11_unsigned_sign_identity(raw_a, raw_b, width_a, width_b, word_bits=72):
    """Full unsigned-word correction plus positive Euclidean remainder; no bit-plane oracle."""
    modulus = pow(2, word_bits)
    require(0 <= raw_a < modulus and 0 <= raw_b < modulus, "Unsigned full public words")
    active_a, active_b = raw_a % pow(2, width_a), raw_b % pow(2, width_b)
    sign_a, sign_b = active_a // pow(2, width_a - 1), active_b // pow(2, width_b - 1)
    signed_a, signed_b = active_a - sign_a * pow(2, width_a), active_b - sign_b * pow(2, width_b)
    require(raw_a == signed_a % modulus and raw_b == signed_b % modulus,
            "Exact full-word sign extensions of ordered active operands")
    full_sign_a, full_sign_b = raw_a // pow(2, word_bits - 1), raw_b // pow(2, word_bits - 1)
    product = raw_a * raw_b - full_sign_a * modulus * raw_b - full_sign_b * modulus * raw_a
    product += full_sign_a * full_sign_b * modulus * modulus
    require(product == signed_a * signed_b, "Unsigned full72 correction equals mathematical signed144 product")
    return signed_a, signed_b, product

def v11_saved_array_universal_proof(rows, descriptor, contract):
    """Independent deque-column consumer and analytic sign-edge correction; no emitter."""
    require(descriptor["schema"] == "a13-d4-s4-v11-ordered-signed-leaf-min75-explicit-sign-descriptor-v1"
            and descriptor["row_id"] == V11_ROW_ID and descriptor["source_row_id"] == "d4_s4" and descriptor["value"] == 11
            and descriptor["ordered_args"] == [10, 9] and descriptor["op"] == "mul"
            and descriptor["params"] == {} and descriptor["spec"] == {
                "width": 72, "fraction_bits": 40, "product_width": 75,
                "active_operand_bits": [34, 41], "input_contract": {"signed_operand_bits": [34, 41]},
                "variant": "retained-CSA-ripple-product75-sign35-to72-v1"},
            "Exact full ordered34x41/F40 signed144-to75 descriptor, no active-width dispatch")
    require(contract["value"] == 11 and contract["ordered_args"] == [10, 9]
            and contract["complete_ordered_ABI_signature"]["ordered_active_signed_widths"] == [34, 41]
            and contract["runtime_operand_swap_or_width_switch"] is False,
            "Exact independently certified V11 ordered source contract")
    require(216 <= descriptor["qubits"] <= LEAF_MAX_WIRES
            and len(rows) == 4 * descriptor["gate_rows"], "Bounded actual saved dimensions")
    position, next_wire = 0, 216

    def allocate(width):
        nonlocal next_wire
        budget()
        require(type(width) is int and width > 0 and next_wire + width <= LEAF_MAX_WIRES,
                "Fresh independent monotone allocation ledger")
        bank = list(range(next_wire, next_wire + width))
        next_wire += width
        return bank

    def consume(*wires):
        nonlocal position
        if position % 128 == 0:
            budget()
        kind, actual = v11_native_gate(rows, position, descriptor["qubits"])
        require(kind == len(wires) and actual == wires
                and all(wire < next_wire for wire in wires), "Every saved row matches separate derived recurrence")
        position += 1

    columns = [deque() for _ in range(75)]
    partials = []
    # Unsigned A*B - a_sign*2^34*B - b_sign*2^41*A + a_sign*b_sign*2^75.
    # Its bit coefficients are negative on the two sign edges, positive at their intersection.
    for bbit in range(41):
        for abit in range(34):
            budget()
            negative = (bbit == 40 and abit < 33) or (abit == 33 and bbit < 40)
            wire = allocate(1)[0]
            if negative:
                consume(wire)
            consume(abit, 72 + bbit, wire)
            column = abit + bbit
            columns[column].append(wire)
            partials.append({"a_bit": abit, "b_bit": bbit, "column": column,
                             "negative": negative, "wire": wire})
    # Closed-form sum of the two negative sign edges, independent of helper's plane sum.
    negative_weight = pow(2, 33) * (pow(2, 40) - 1) + pow(2, 40) * (pow(2, 33) - 1)
    correction = (-negative_weight) % pow(2, 75)
    fixed = []
    for column in range(75):
        budget()
        if divmod(correction, pow(2, column))[0] % 2:
            wire = allocate(1)[0]
            consume(wire)
            columns[column].append(wire)
            fixed.append({"column": column, "wire": wire})
    local_boolean_rows = []
    for encoded in range(8):
        x, y, z = encoded & 1, (encoded >> 1) & 1, (encoded >> 2) & 1
        p = x ^ y
        generate, propagated = x & y, p & z
        carry, summation = generate ^ propagated, p ^ z
        require(not (generate and propagated) and x + y + z == summation + 2 * carry,
                "Universal three-bit disjoint-majority integer identity")
        local_boolean_rows.append([x, y, z, summation, carry])
    layers = []
    while any(len(bucket) > 2 for bucket in columns):
        following = [deque() for _ in range(75)]
        layer = []
        for column, bucket in enumerate(columns):
            budget()
            while len(bucket) >= 3:
                x, y, z = bucket.popleft(), bucket.popleft(), bucket.popleft()
                summation = allocate(1)[0]
                consume(x, summation)
                consume(y, summation)
                carry = None
                if column < 74:
                    carry = allocate(1)[0]
                    consume(x, y, carry)
                    consume(summation, z, carry)
                    following[column + 1].append(carry)
                consume(z, summation)
                following[column].append(summation)
                layer.append({"column": column, "inputs": [x, y, z], "sum": summation, "carry": carry})
            following[column].extend(bucket)
        columns = following
        layers.append(layer)
    left, right, product = allocate(75), allocate(75), allocate(75)
    for bit, bucket in enumerate(columns):
        budget()
        values = list(bucket)
        if values:
            consume(values[0], left[bit])
        if len(values) == 2:
            consume(values[1], right[bit])
    propagate, carry = allocate(75), allocate(76)
    for bit in range(75):
        consume(left[bit], propagate[bit])
        consume(right[bit], propagate[bit])
        consume(left[bit], right[bit], carry[bit + 1])
        if bit > 0:
            consume(propagate[bit], carry[bit], carry[bit + 1])
        consume(propagate[bit], product[bit])
        if bit > 0:
            consume(carry[bit], product[bit])
    compute_end = position
    for bit in range(72):
        consume(product[40 + bit if bit < 35 else 74], 144 + bit)
    for original in range(compute_end - 1, -1, -1):
        if position % 128 == 0:
            budget()
        require(v11_native_gate(rows, position, descriptor["qubits"])
                == v11_native_gate(rows, original, descriptor["qubits"]),
                "Every actual inverse row is exactly reversed compute, including all private wires")
        position += 1
    recipe = {"partials": partials, "correction": correction, "fixed": fixed, "CSA_layers": layers,
              "final_columns": [list(bucket) for bucket in columns], "left": left, "right": right,
              "product": product, "propagate": propagate, "carry": carry,
              "output_source_bits": list(range(40, 75)) + [74] * 37}
    require(position == descriptor["gate_rows"] and next_wire == descriptor["qubits"]
            and descriptor["recipe"] == recipe and descriptor["args"] == [list(range(72)), list(range(72, 144))]
            and descriptor["outs"] == [list(range(144, 216))]
            and descriptor["compute_gate_rows"] == [0, compute_end]
            and descriptor["copy_gate_rows"] == [compute_end, compute_end + 72]
            and descriptor["inverse_gate_rows"] == [compute_end + 72, position],
            "All actual public ports, complete recipe, rows and allocations consumed")
    require(descriptor["private_workspace_zero_entry_exit"] is True
            and descriptor["dirty_output_XOR"] is True and descriptor["input_preserved"] is True
            and descriptor["low_product_columns_discarded_before_carry"] is False
            and descriptor["full_signed_semantic_product_bits"] == 144
            and descriptor["product_modulus_bits"] == 75
            and descriptor["constructed_only_under_separate_v11_leaf_ROOT_release"] is True
            and descriptor["actual_cost_or_source_transfer_claim"] is False,
            "Universal full72 clean XOR and exactly original signed144 arithmetic floor40 semantics")
    v11_high_sign_copy_plan(recipe["output_source_bits"])
    require(descriptor["output_sign_extension"] == {"retained_quotient_bits": 35,
            "computed_product_sign_bit": 74, "high_output_bits": list(range(35, 72))},
            "Every computed product sign copy is explicit in the saved descriptor")
    return {"passed": True, "actual_rows_consumed": position, "allocated_wires": next_wire,
            "compute_copy_inverse_rows": [compute_end, 72, compute_end],
            "analytic_sign_edge_negative_weight": negative_weight, "mod75_correction": correction,
            "all_low_columns_before_bit40_and_carries_retained": True,
            "local_disjoint_majority_boolean_rows": local_boolean_rows,
            "Euclidean_identity": "R=P mod2^75; q=floor(P/2^40); n=1 if P<0 else0; R//2^40=q+n*2^35; high37 computed-sign copies add n*(2^72-2^35), giving q mod2^72",
            "universal_signed75_fit_proof": "|P|<=2^(33+40)=2^73<2^74, including positive min-times-min; negative floor40 is arithmetic floor, zero has computed product sign0",
            "universal_coherent_extension": "Exact classical bijection, absolute CCX phase1 and clean private inverse imply the promised full72 typed coherent span tensor arbitrary reference identity",
            "signed_active_product_abs_bound": pow(2, 33 + 40),
            "signed144_contains_every_promised_product": True,
            "all_inputs_only_controls_dirty_output_only_full72_copy_private_inverse_clean": True,
            "producer_helper_plane_or_proof_function_called": False,
            "second_native_array_or_emitter_constructed": False, "fixture_credit": 0}

def v11_fresh64_cases():
    bounds_a = (-pow(2, 33), pow(2, 33) - 1)
    bounds_b = (-pow(2, 40), pow(2, 40) - 1)
    amin, amax = bounds_a
    bmin, bmax = bounds_b
    p = pow(2, 20)
    pairs = [(0, 0), (0, bmin), (amin, 0), (-1, -1), (-1, bmax), (amax, -1),
             (amin, bmin), (amin, bmax), (amax, bmin), (amax, bmax), (p, p),
             (p - 1, p + 1), (p + 1, p - 1), (-p, p), (-p - 1, p + 1), (-p + 1, p - 1)]
    mask, even = pow(2, 72) - 1, int("01" * 36, 2)
    cases = []
    for pair_id, (a, b) in enumerate(pairs):
        budget()
        require(amin <= a <= amax and bmin <= b <= bmax, "Every literal V11 pair obeys promise; no clipping or substitution")
        raw_a, raw_b = a % pow(2, 72), b % pow(2, 72)
        decoded_a, decoded_b, product = v11_unsigned_sign_identity(raw_a, raw_b, 34, 41)
        require((decoded_a, decoded_b) == (a, b), "Full-word correction agrees with fixed signed pair")
        quotient, remainder = divmod(product, pow(2, 40))
        require(0 <= remainder < pow(2, 40)
                and quotient % pow(2, 72) == divmod(product % pow(2, 144), pow(2, 40))[0] % pow(2, 72),
                "Negative and positive Euclidean floor-window identity")
        for dirty_id, dirty in enumerate((0, mask, even, mask - even)):
            cases.append({"id": f"pair{pair_id:02d}_dirty{dirty_id}", "signed_a": a, "signed_b": b,
                          "raw_a": raw_a, "raw_b": raw_b, "dirty": dirty,
                          "expected_output": dirty ^ (quotient % pow(2, 72))})
    require(len(cases) == 64, "Exactly original16 ordered formulas times four dirty full72 patterns")
    return cases

def v11_fresh_forward_inverse(rows, descriptor, cases):
    qubits, lanes = descriptor["qubits"], len(cases)
    require(lanes == 64, "Fixed64-lane cohort, not exhaustive proof or new fixture credit")
    state, expected = [0] * qubits, [0] * qubits
    for lane, case in enumerate(cases):
        budget()
        for bit in range(72):
            for offset, key in ((0, "raw_a"), (72, "raw_b"), (144, "dirty")):
                state[offset + bit] |= (case[key] // pow(2, bit) % 2) * pow(2, lane)
            for offset, key in ((0, "raw_a"), (72, "raw_b"), (144, "expected_output")):
                expected[offset + bit] |= (case[key] // pow(2, bit) % 2) * pow(2, lane)
    initial, full_lane_mask = tuple(state), pow(2, lanes) - 1
    for reverse in (False, True):
        indexes = reversed(range(descriptor["gate_rows"])) if reverse else range(descriptor["gate_rows"])
        for index in indexes:
            if index % 128 == 0:
                budget()
            kind, wires = v11_native_gate(rows, index, qubits)
            if kind == 1:
                toggle = full_lane_mask
            elif kind == 2:
                toggle = state[wires[0]]
            else:
                toggle = state[wires[0]] & state[wires[1]]
            state[wires[-1]] ^= toggle
        require(tuple(state) == (initial if reverse else tuple(expected)),
                "All actual input, dirty output, private and unused carry wires compared after each full sweep")
    return {"passed": True, "logical_forward_cases": 64, "logical_inverse_cases": 64,
            "physical_full_forward_sweeps": 1, "physical_full_inverse_sweeps": 1,
            "all_allocated_wires_compared_including_unused_carries": True,
            "finite_batch_is_not_universal_ABI_proof": True, "fixture_credit": 0}

def v11_fresh_cyclic8_phase(macro):
    require(tuple(tuple(event) for event in macro) == EXPECTED_CCX_PHASE_MACRO,
            "Actual saved15-event paid seven-T macro exact independent fixed literal")

    def rotate(coefficients, exponent):
        result = [0] * 8
        for position, coefficient in enumerate(coefficients):
            result[(position + exponent) % 8] += coefficient
        return result

    def normalize(coefficients):
        return [coefficients[position] - coefficients[position + 4] for position in range(4)]

    columns = []
    for basis in range(8):
        budget()
        state = [[0] * 8 for _ in range(8)]
        state[basis][0] = 1
        exponent = 0
        for event in macro:
            budget()
            kind, wires = event[0], event[1:]
            if kind == "CX":
                following = [[0] * 8 for _ in range(8)]
                for row in range(8):
                    dest = row ^ pow(2, wires[1]) if row // pow(2, wires[0]) % 2 else row
                    following[dest] = state[row]
                state = following
            elif kind in ("T", "TD"):
                state = [rotate(value, 1 if kind == "T" else 7)
                         if row // pow(2, wires[0]) % 2 else value for row, value in enumerate(state)]
            else:
                require(kind == "H", "Only paid H/CX/T/TD events")
                following = [[0] * 8 for _ in range(8)]
                for row in range(8):
                    if row // pow(2, wires[0]) % 2:
                        continue
                    other = row + pow(2, wires[0])
                    added = [a + b for a, b in zip(state[row], state[other], strict=True)]
                    subtracted = [a - b for a, b in zip(state[row], state[other], strict=True)]
                    for target, value in ((row, added), (other, subtracted)):
                        left, right = rotate(value, 1), rotate(value, 3)
                        following[target] = [a - b for a, b in zip(left, right, strict=True)]
                exponent += 1
                state = following
        target = basis ^ 4 if basis % 4 == 3 else basis
        normalized = [normalize(value) for value in state]
        ideal = [[0] * 4 for _ in range(8)]
        ideal[target][0] = pow(2, exponent)
        require(normalized == ideal, "Every exact phase column equals ideal CCX with absolute amplitude1")
        columns.append({"input_basis": basis, "output_basis": target,
                        "denominator_exponent": exponent, "normalized_column": normalized})
    require(sum(event[0] in ("T", "TD") for event in macro) == 7, "Exactly seven paid T/TD")
    return {"passed": True, "all8_basis_columns": columns, "absolute_unit_global_phase": True,
            "representation": "8 cyclic integer coefficients mod z^8-1, reduced by z^4=-1; denominator2^Hcount",
            "faithful_antipodal_reduction_to_Phi8_basis": True,
            "producer_old_phase_proof_called": False, "fixture_credit": 0}

def v11_fresh_resource_dependencies(rows, qubits, macro):
    native = {1: 0, 2: 0, 3: 0}
    dependencies = {wire: (0, 0) for wire in range(qubits)}
    events = 0
    for index in range(len(rows) // 4):
        if index % 128 == 0:
            budget()
        kind, wires = v11_native_gate(rows, index, qubits)
        native[kind] += 1
        expanded = [("X", wires)] if kind == 1 else [("CX", wires)] if kind == 2 else [
            (event[0], tuple(wires[role] for role in event[1:])) for event in macro]
        for operation, touched in expanded:
            budget()
            require(len(set(touched)) == len(touched) and all(wire in dependencies for wire in touched),
                    "All actual expanded paid macro operands accounted")
            depth_t = max(dependencies[wire][0] for wire in touched) + (operation in ("T", "TD"))
            depth_all = max(dependencies[wire][1] for wire in touched) + 1
            for wire in touched:
                dependencies[wire] = (depth_t, depth_all)
            events += 1
    return {"schema": "a13-first-signed-leaf-actual-standalone-resources-v1",
            "native_gate_rows": len(rows) // 4, "X": native[1], "CX": native[2], "CCX": native[3],
            "T": 7 * native[3], "Clifford_T_macro_events": events,
            "ASAP_T_depth": max(depth[0] for depth in dependencies.values()),
            "ASAP_Clifford_T_depth": max(depth[1] for depth in dependencies.values()),
            "allocated_qubits": qubits, "includes_forward_full72_dirty_XOR_and_complete_inverse": True,
            "caller_argument_copies_included": False, "caller_copy_obligation_remains": True,
            "whole_clean_function_source_capped_schedule_or_original_G2_cost": False,
            "old_cost_estimate_or_profile_used": False, "fixture_credit": 0}

def v11_high_sign_copy_plan(plan):
    expected = list(range(40, 75)) + [74] * 37
    if plan != expected:
        raise HighSignCopyReject("MIN75_HIGH_SIGN_COPY_PLAN")
    return expected

def v11_fresh900_and_controls():
    count = 0
    for wa in range(1, 5):
        for wb in range(1, 5):
            for raw_a in range(pow(2, wa)):
                for raw_b in range(pow(2, wb)):
                    budget()
                    sa, sb = raw_a // pow(2, wa - 1), raw_b // pow(2, wb - 1)
                    product = raw_a * raw_b - sa * pow(2, wa) * raw_b - sb * pow(2, wb) * raw_a
                    product += sa * sb * pow(2, wa + wb)
                    decoded_a, decoded_b = raw_a - sa * pow(2, wa), raw_b - sb * pow(2, wb)
                    require(product == decoded_a * decoded_b, "Independent unsigned-active correction identity")
                    q, r = divmod(product, 16)
                    require(0 <= r < 16 and q % 256 == divmod(product % 4096, 16)[0],
                            "Independent exact toy signed12-residue/floor4/mod8 identity")
                    complement_sum = 0
                    for bbit in range(wb):
                        for abit in range(wa):
                            negative = (abit == wa - 1 and bbit < wb - 1) or (bbit == wb - 1 and abit < wa - 1)
                            bit = (raw_a // pow(2, abit) % 2) * (raw_b // pow(2, bbit) % 2)
                            complement_sum += (1 - bit if negative else bit) * pow(2, abit + bbit)
                    correction = -(pow(2, wa - 1) * (pow(2, wb - 1) - 1)
                                   + pow(2, wb - 1) * (pow(2, wa - 1) - 1))
                    require(complement_sum + correction == product, "Closed sign-edge correction independently matches every toy")
                    actual_bits = wa + wb
                    complete_residue = (complement_sum + correction) % pow(2, actual_bits)
                    computed_sign = complete_residue // pow(2, actual_bits - 1)
                    if actual_bits > 4:
                        short_window = complete_residue // 16
                        extended = (short_window + computed_sign * (256 - pow(2, actual_bits - 4))) % 256
                    else:
                        extended = 255 * computed_sign
                    require(extended == q % 256,
                            "Complete L residue, all low carries and explicit sign extension; L<=F gives0/-1")
                    require(product != 0 or computed_sign == 0, "Zero uses computed product sign, not operand sign XOR")
                    count += 1
    require(count == 900, "Exactly fixed width1..4 ordered toy raw patterns, no toy circuits")
    short = divmod((-1) % pow(2, 75), pow(2, 40))[0]
    correct = divmod(-1, pow(2, 40))[0] % pow(2, 72)
    require(short != correct, "Bad75-bit modulus cannot preserve full72 negative quotient")
    a, b = pow(2, 21) - 1, pow(2, 20) + 1
    a_bits = [a // pow(2, bit) % 2 for bit in range(34)]
    b_bits = [b // pow(2, bit) % 2 for bit in range(41)]
    high_only = sum(pow(2, ai + bi) * av * bv for ai, av in enumerate(a_bits)
                    for bi, bv in enumerate(b_bits) if ai + bi >= 40)
    bad_carry, correct_carry = divmod(high_only, pow(2, 40))[0], divmod(a * b, pow(2, 40))[0]
    require(bad_carry != correct_carry, "Bad omission of lower40 carries rejected")
    invalid_a, invalid_b = pow(2, 34) - 1, 1
    active_signed = invalid_a % pow(2, 34) - pow(2, 34)
    require(invalid_a != active_signed % pow(2, 72) and invalid_b == 1 % pow(2, 72),
            "Invalid active-sign upper-word extension rejected independently before a logical case")
    expected_plan = list(range(40, 75)) + [74] * 37
    structural_rejections = []
    for mutation in ("omitted-high37", "corrupted-first-high-sign-copy"):
        budget()
        bad_plan = expected_plan[:35] if mutation == "omitted-high37" else expected_plan.copy()
        if mutation == "corrupted-first-high-sign-copy":
            bad_plan[35] = None
        try:
            v11_high_sign_copy_plan(bad_plan)
        except HighSignCopyReject as error:
            require(type(error) is HighSignCopyReject and str(error) == "MIN75_HIGH_SIGN_COPY_PLAN",
                    "Only dedicated exact intended structural rejection counts")
        else:
            require(False, "Bad high-sign copy plan was accepted")
        structural_rejections.append({"mutation": mutation, "exact_structural_rejection": True})
    bad_corrupted = correct ^ pow(2, 35)
    require(bad_corrupted != correct and short != correct, "Fixed negative quotient loses a required high sign toggle")
    return {"passed": True, "scalar_toy_ordered_pairs": count, "toy_native_fraction_residue_bits": [8, 4, 12],
            "controls": [{"name": "bad-short-modulus", "a": -1, "b": 1, "bad_output": short,
                          "correct_output": correct, "bad_method_rejected": True},
                         {"name": "dropped-low-carry", "a": a, "b": b, "bad_output": bad_carry,
                          "correct_output": correct_carry, "bad_method_rejected": True},
                         {"name": "invalid-sign-extension", "raw_a": invalid_a, "raw_b": invalid_b,
                          "promise_rejected_before_any_logical_case": True},
                         {"name": "omitted-or-corrupted-output-high-sign-copies", "a": -1, "b": 1,
                          "bad_omitted_output": short, "bad_corrupted_output": bad_corrupted,
                          "correct_output": correct, "structural_rejections": structural_rejections,
                          "bad_method_rejected": True}],
            "toy_actual_product_bits": "L=wa+wb, all low columns and carries retained",
            "toy_L_less_equal_F_branch_computed_product_sign_to_all8": True,
            "operand_sign_XOR_is_not_sign_authority_at_zero": True,
            "alternative_native_or_toy_gate_arrays_constructed": 0,
            "expected_control_rejections_are_not_actual_run_failures": True, "fixture_credit": 0}

def v11_compare_original_reports(structural, cases, batch, toys, phase, resources):
    """Original primary reports become comparison inputs only after all own science succeeds."""
    old = read(V11_LEAF / "independent_whole_array_structural_proof.json")
    require(old["passed"] is True and old["actual_rows_consumed"] == structural["actual_rows_consumed"]
            and old["allocated_wires"] == structural["allocated_wires"]
            and old["compute_copy_inverse_rows"] == structural["compute_copy_inverse_rows"]
            and old["full72_copy_and_all_private_literal_inverse"] is True,
            "Saved producer proof is compared only for dimensions after independent every-row proof")
    old_cases = read(V11_LEAF / "fixed64_native_cases.json")
    require(old_cases["schema"] == "a13-v11-min75-fixed-native-cases-v1"
            and old_cases["case_count"] == 64 and old_cases["duplicates_retained"] is True
            and old_cases["cases"] == cases
            and _FROZEN[key_for(V11_LEAF / "fixed64_native_cases.json")]
            == V11_CASES_SHA,
            "All original64 fixed scalar/full72 dirty cases reconstructed with retained duplicate IDs")
    require(read(V11_LEAF / "independent_native_forward_inverse_batch.json") == batch,
            "Fresh actual forward and literal reverse compare every input/output/private allocated wire")
    require(read(V11_LEAF / "independent900_scalar_toys_and_four_controls.json") == toys,
            "All fresh900 scalar toys and four fixed controls reproduce original result fields")
    old_phase = read(V11_LEAF / "independent_exact_absolute_CCX_phase.json")
    require(old_phase["passed"] is True and old_phase["absolute_unit_global_phase"] is True
            and len(old_phase["basis_columns"]) == 8, "Eight saved absolute phase columns, no phase transfer")
    for old_column, own_column in zip(old_phase["basis_columns"], phase["all8_basis_columns"], strict=True):
        require(old_column["input_basis"] == own_column["input_basis"]
                and old_column["output_basis"] == own_column["output_basis"]
                and old_column["denominator_exponent"] == own_column["denominator_exponent"]
                and old_column["cyclotomic_integer_column"] == own_column["normalized_column"],
                "Every cyclic8/antipodal fresh absolute unit column matches independently saved representation")
    require(read(V11_LEAF / "independent_actual_standalone_resources.json") == resources,
            "Fresh per-wire dict macro dependencies reproduce every complete saved standalone resource field")
    summary = v11_completed_metadata_witness()
    require(summary["standalone_leaf_resources"] == resources and summary["fixed_native_batch"] == batch,
            "External completed producer summary binds actual dimensions and own results")
    return {"passed": True, "all64_cases_all900_toys_four_controls_match": True,
            "all8_absolute_phase_columns_match_after_fresh_cyclic8_reconstruction": True,
            "all_actual_standalone_resource_fields_match": True,
            "producer_proof_used_as_independent_theorem": False,
            "producer_or_helper_imported_executed_or_called": False,
            "no_full_source_financial_capped_cost_transfer": True, "fixture_credit": 0}

def v11_unmatched_comparator_scope():
    result = {"schema": "a13-v11-min75-unmatched-resource-comparator-scope-null-v1",
        "selected_value": 11, "ordered_args": [10, 9], "ordered_active_signed_widths": [34, 41],
        "matched_executed_v11_wide_baseline": None, "matched_resource_comparison": None,
        "savings": None, "cost_forecast": None, "v6_resource_transfer": False,
        "second_matching_native_array_emitted": False, "fixture_credit": 0}
    require(read(V11_LEAF / "actual_minimum75_unmatched_v11_resource_scope.json") == result,
            "No V6/min80 widebaseline transfer to V11; matching baseline remains unexecuted/null")
    return result


def v11_object_SHA(value):
    budget()
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def v11_method_and_current_reviews(ready, policy):
    require(ready["current_fixed_input_expected_SHA256"] == policy["current_fixed_input_expected_SHA256"] == V11_FIXED_INPUT_PINS,
            "Closed externally frozen METHOD/admission/clarification/template/source/result pin map")
    for key, pin in V11_FIXED_INPUT_PINS.items():
        bind(ROOT / key, pin)
    reviews = ready["static_review_expected_SHA256"]
    require(type(reviews) is dict and set(reviews) == set(V11_CURRENT_REVIEW_ROUTES),
            "Exactly3 current author-QA/independent/root-static records, no missing or extra route")
    for key, pin in reviews.items():
        record = read(bind(ROOT / key, pin))
        require(record["passed"] is True and record.get("blockers", []) == [], "Every frozen current review PASS")
        require(record["author_method_SHA256"] == ready["author_method_SHA256"], "Every current review joins exact new trio")
        require(_FROZEN[key] == pin, "Current review directly admitted before first own_runtime/origin check")
    method = read(ROOT / V11_METHOD_KEY)
    acceptance = read(ROOT / V11_ACCEPTANCE_KEY)
    clarification = read(ROOT / V11_CLARIFICATION_KEY)
    require(method["current13_complete_owner_packet_literals"] == V11_CURRENT13
            and method["original12_complete_owner_packet_literals"] == V11_ORIGINAL12
            and method["current13_inclusive_owned_files"] == 419 and method["current13_inclusive_owned_bytes"] == 129861281,
            "Exact original12 plus sole completed V11; no later owner or template scope")
    require(acceptance["authoring_only"] is True and acceptance["READY_or_SCI_execution_authorized"] is False
            and acceptance["approved_current_author_paths"] == [AUTHOR.relative_to(ROOT).as_posix(), METHOD_DOC.relative_to(ROOT).as_posix(), PREFLIGHT.relative_to(ROOT).as_posix()],
            "Frozen acceptance was authoring only, never current scientific execution permission")
    require(clarification["exact_original_six_startup_records"] == V11_STARTUP6
            and clarification["wrong_prose_label_is_expected_path_or_cache_scope_authority"] is False,
            "Concrete original six redirector records supersede inaccurate historical prose, no scope invention")
    return method

def v11_snapshot_owner_witnesses():
    require(_V11_METHOD is not None, "Pinned METHOD available before owner witness")
    total_files = total_bytes = 0
    for name, pin, counts, ownership, schema in V11_CURRENT13:
        budget()
        snapshot = _V11_METHOD["complete_current13_owner_snapshots"][name]
        directory = canonical(PROGRAM / name, fresh=True)
        actual = read(directory / "manifest.json")
        require(snapshot["manifest_path"] == (directory / "manifest.json").relative_to(ROOT).as_posix()
                and snapshot["manifest_expected_SHA256"] == pin and snapshot["complete_counts"] == counts
                and actual["schema"] == schema and snapshot["complete_original_declared_maps"]
                == {key: actual[key] for key in ("files", "frozen_inputs", "external_runtime_inputs")},
                "Full exact original wrappers/maps/schema/counts preserved, not whole unrelated supplement wrapper equality")
        entries = snapshot["complete_original_physical_owned_inventory"]
        expected_members = set()
        owner_bytes = 0
        for entry in entries:
            path = canonical(ROOT / entry["root_relative_path"], fresh=True)
            require(path.is_relative_to(directory) and key_for(path) in _FROZEN
                    and _FROZEN[key_for(path)] == entry["expected_SHA256"] and path.stat().st_size == entry["bytes"],
                    "Complete original physical owned SHA and size authority; no observed promotion")
            expected_members.add(path)
            owner_bytes += entry["bytes"]
        require(inventory(directory) == expected_members == _OWN_INVENTORIES[directory]
                and len(expected_members) == counts[0] + 1, "All419 owned bytes retain full inventories including external MF pin")
        total_files += len(expected_members)
        total_bytes += owner_bytes
    require(total_files == 419 and total_bytes == 129861281, "Exact current13 inclusive physical ownership")
    return {"current13_complete_owner_packet_literals": V11_CURRENT13, "original12": V11_ORIGINAL12,
            "inclusive_original_owned_files": total_files, "inclusive_original_owned_bytes": total_bytes,
            "complete_original_maps_and_inventories_retained": True, "later_owners_admitted": False}

def v11_startup_and_runtime_roles():
    require(_SOURCE_INTERPRETER is not None and read(ROOT / V11_INTERPRETER_KEY) == _SOURCE_INTERPRETER,
            "Exact original saved interpreter record, not current runtime discovery")
    require(_SOURCE_INTERPRETER["runtime_inventory"]["files"] == 3057
            and v11_object_SHA(_SOURCE_INTERPRETER["runtime_inventory"]) == V11_SAVED3057_CANONICAL_SHA,
            "Complete original saved3057 opaque runtime inventory role")
    source_manifest = read(AUDIT / "manifest.json")
    external = source_manifest["external_runtime_inputs"]
    require(len(external) == 2842 and v11_object_SHA(external) == V11_STDLIB2842_CANONICAL_SHA,
            "Original strict2842 external stdlib map, distinct from saved3057 membership")
    require(_SOURCE_INTERPRETER["bootstrap_hook_and_loaded_venv_paths"]
            == [row["original_saved_absolute_path"] for row in V11_STARTUP6], "Exact original six startup .pth/.py/.pyc paths")
    for row in V11_STARTUP6:
        path = ROOT / row["original_frozen_inputs_key"]
        require(str(path) == row["original_saved_absolute_path"]
                and source_manifest["frozen_inputs"][row["original_frozen_inputs_key"]] == row["expected_SHA256"],
                "Exact original startup key/path/expected SHA, never old inaccurate customization label")
        bind(path, row["expected_SHA256"])
        require(path.stat().st_size == row["bytes_metadata_only"], "Original startup record size")
    return external

def own_runtime():
    require(canonical(sys.executable) == canonical(LAUNCHER) and sys.dont_write_bytecode is True
            and canonical(Path.cwd()) == ROOT and canonical(sys.prefix) == ROOT / ".context/frontier_t0_env",
            "Pinned exact original-runtime-compatible launcher/cwd/prefix/startup-B")
    require(not any(os.environ.get(k) for k in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")), "No inherited runtime/search/cache override")
    external = v11_startup_and_runtime_roles()
    require(sys.path == _SOURCE_INTERPRETER["sys_path"], "Exact original prepared search list")
    candidates = standard_runtime_members()
    require({str(path) for path in candidates if not path.is_relative_to(ROOT)} == set(external),
            "Actual current external standard runtime membership equals original2842, no unknown file admitted")
    global _STANDARD_RUNTIME_MEMBERS
    _STANDARD_RUNTIME_MEMBERS = candidates
    total = 0
    for path in sorted(candidates):
        budget()
        key = key_for(path)
        mapping = _FROZEN if path.is_relative_to(ROOT) else _EXTERNAL
        require(key in mapping, "Every actual runtime member has prior original expected SHA; no digest-observed pin synthesis")
        total += path.stat().st_size
        require(len(candidates) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES, "Original current runtime caps")
        require(digest(path, fresh=True) == mapping[key], "Actual runtime bytes retain original declared expectation")
    cfg = ROOT / ".context/frontier_t0_env/pyvenv.cfg"
    require(key_for(cfg) in _FROZEN and "include-system-site-packages = false" in cfg.read_text(encoding="utf-8").lower(),
            "Original separately expected venv config excludes base site packages")
    loaded_origins()
    return {"files": len(candidates), "bytes": total, "base_site_packages_pruned_and_rejected": True,
            "original2842_external_and_saved3057_roles_distinct": True, "observed_expected_promotion": False}

def v11_completed_metadata_witness():
    summary = read(V11_LEAF / "summary.json")
    require(read(V11_LEAF / "completion_outcome.json") == {**summary, "failed": False}
            and summary["schema"] == "a13-d4-s4-v11-signed-leaf-min75-summary-v1"
            and summary["completed"] is summary["passed"] is True and summary["budget_censored"] is False
            and summary["row_id"] == V11_ROW_ID and summary["source_row_id"] == ROW_ID and summary["value"] == V11_VALUE
            and summary["ordered_args"] == V11_ARGS and summary["ordered_active_signed_widths"] == V11_ACTIVE_WIDTHS
            and summary["word_fraction_product_residue_bits"] == [72,40,144,75]
            and summary["all12_completed_owner_maps_and_owned_inventories_retained"] is True
            and summary["all_old_failed_and_prefit_history_retained_without_promotion"] is True
            and summary["external_independent_completed_leaf_audit_still_required"] is True,
            "Exact completed V11 metadata authority only, no borrowed independent proof")
    review = read(V11_LEAF_RESULT)
    require(review["schema"] == "root-a13-v11-signed-leaf-min75-actual-result-review-v1"
            and review["passed"] is True and review["manifest_SHA256"] == V11_LEAF_SHA and review["complete_counts"] == V11_LEAF_COUNTS
            and review["inclusive_owned_files"] == 62 and review["current_static_review_files_claimed_direct_SCI_union_members"] is False
            and review["full_source_capped_schedule_financial_G2_adoption_cost_or_advantage_transfer"] is False,
            "Original ROOT result authority and transitive review role preserved, not retroactive direct membership")
    require(summary["actual_saved_native_array_SHA256"] == V11_ARRAY_SHA == _FROZEN[key_for(V11_LEAF / "native_gate_rows.i32")]
            and _FROZEN[key_for(V11_LEAF / "native_descriptor.json")] == V11_DESCRIPTOR_SHA, "Original single saved array/descriptor SHA")
    for key in ("full_G2","adoption","cost_transfer","quantum_advantage","financial_gate_emission_authorized","candidate_feasibility"):
        require(summary[key] is False, "No financial/fullsource permission from saved V11 completion")
    return summary

def v11_original_ordered_contract():
    path = NATIVE_AUDIT / "independent_six_ordered_MUL_contracts.json"
    require(_FROZEN[key_for(path)] == NATIVE_CONTRACT_SHA, "Literal original six-contract authority SHA")
    contracts = read(path)
    require(contracts["schema"] == "a13-d4-s4-six-ordered-MUL-contracts-v1" and len(contracts["contracts"]) == 6
            and contracts["gate_leaf_authoring_or_execution_authorized"] is False, "Original six contracts grant no new gate emission")
    chosen = [row for row in contracts["contracts"] if row["value"] == 11]
    require(len(chosen) == 1, "Only original V11 source value selected")
    contract = chosen[0]
    require(contract["deduplicated_signature_index"] == 3 and contract["ordered_args"] == [10,9]
            and contract["complete_ordered_ABI_signature"]["ordered_active_signed_widths"] == [34,41]
            and contract["runtime_operand_swap_or_width_switch"] is False and contract == _V11_METHOD["complete_ordered_contract"],
            "Entire original index3/V11/[10,9]/signed34x41 ordered ABI/hull contract exact")
    binding = read(V11_LEAF / "v11_leaf_source_contract_binding.json")
    require(_FROZEN[key_for(V11_LEAF / "v11_leaf_source_contract_binding.json")] == V11_BINDING_SHA
            and binding["schema"] == "a13-v11-min75-original-audited-contract-binding-v1" and binding["exact_ordered_contract"] == contract
            and binding["producer_manifest_SHA256"] == PRODUCER_SHA and binding["native_audit_manifest_SHA256"] == NATIVE_AUDIT_SHA
            and binding["native_contract_original_expected_SHA256"] == NATIVE_CONTRACT_SHA
            and binding["actual_array_SHA256"] == V11_ARRAY_SHA and binding["actual_descriptor_SHA256"] == V11_DESCRIPTOR_SHA
            and binding["original_capped_baselines_unchanged"] == BASELINES and binding["financial_G2_cost_source_adoption_transfer"] is False,
            "Saved current V11 contract binding is metadata only; no whole-source savings transfer")
    return contract

def v11_original_history_admission(producer_ready, producer_policy):
    require(producer_ready["runtime_invocation"] == producer_policy["runtime_invocation"] == V11_PRODUCER_INVOCATION,
            "Historical producer invocation retained in its scope, not current auditor invocation")
    admit_prior_selection_failure(producer_ready, producer_policy)
    admit_prior_inventory_failure(producer_ready, producer_policy)
    admit_held_v1(producer_ready, producer_policy)
    old_ready = read(bind(BASELINE112_AUDIT_READY, BASELINE112_AUDIT_READY_SHA))
    old_policy = read(bind(RESEARCH / "a13_d4_s4_first_signed_leaf_independent_audit_preflight_v2.json",
                          BASELINE112_AUDIT_AUTHORS["a13_d4_s4_first_signed_leaf_independent_audit_preflight_v2.json"]))
    admit_held_audit_V1(old_ready, old_policy)
    for name, expected in HELD_DESIGN_AUTHORS.items():
        bind(RESEARCH / name, expected)
    code_caches([RESEARCH / "a13_d4_s4_contracted_mul_design_v1.py"], producer_ready["held_design_existing_code_cache_SHA256"], producer_ready["held_design_absent_code_cache_paths"])
    code_caches([RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_v1.py", RESEARCH / "build_a13_d4_s4_first_signed_leaf_v1.py"],
                producer_ready["held_V1_existing_code_cache_SHA256"], producer_ready["held_V1_absent_code_cache_paths"])
    v11_full_optimization_cache_guard([RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_min80_v1.py", RESEARCH / "build_a13_d4_s4_first_signed_leaf_min80_v1.py"],
                producer_ready["completed80_all_optimization_existing_cache_SHA256"], producer_ready["completed80_all_optimization_absent_cache_paths"])
    v11_full_optimization_cache_guard([RESEARCH / "prototype_a13_d4_s4_v11_signed_leaf_min75_v1.py", RESEARCH / "build_a13_d4_s4_v11_signed_leaf_min75_v1.py"],
                producer_ready["new_all_optimization_existing_cache_SHA256"], producer_ready["new_all_optimization_absent_cache_paths"])
    require({k: producer_ready[k] for k in _V11_METHOD["runtime_admission_plan"]["original_producer_cache_policy_full_fields"]}
            == _V11_METHOD["runtime_admission_plan"]["original_producer_cache_policy_full_fields"], "Whole original producer cache field authority unchanged")
    failed_material_witness(initial=True)

def v11_admission(ready_sha):
    global _V11_METHOD, _V11_POLICY, _V11_READY, _V11_OWNERS
    require("PYTHONINTMAXSTRDIGITS" not in os.environ and "int_max_str_digits" not in sys._xoptions
            and sys.get_int_max_str_digits() == 4300, "Original bounded decimal policy unchanged, no override")
    ready = read(bind(READY, ready_sha))
    require(ready["schema"] == "root-a13-d4-s4-v11-signed-leaf-min75-independent-audit-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True
            and ready["independent_completed_v11_audit_approved"] is True and ready["gate_emission_authorized"] is False,
            "Separate externally pinned current scientific audit grant, never inherited producer or METHOD permission")
    authors = ready["author_method_SHA256"]
    require(type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, "Exactly new auditor author trio")
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(policy["schema"] == "a13-d4-s4-v11-signed-leaf-min75-independent-audit-preflight-v1"
            and policy["author_SHA256"] == authors[AUTHOR.name] and policy["method_doc_SHA256"] == authors[METHOD_DOC.name]
            and policy["ROOT_READY_or_SCI_execution_authorized"] is False, "Prospective author-only policy, ROOT READY provides separate current grant")
    fixed = {"output": OUTPUT.relative_to(ROOT).as_posix(), "limits_CPU_admission_wall": [CPU,ADMISSION,WALL],
             "owned_caps_files_bytes": [MAX_OWN_FILES,MAX_OWN_BYTES], "runtime_caps_files_bytes": [MAX_RUNTIME_FILES,MAX_RUNTIME_BYTES],
             "bookkeeping_reference_unique_bytes_hash_work_caps": [MAX_REFERENCES,MAX_UNIQUE_BYTES,MAX_HASH_WORK],
             "current13_complete_owner_packet_literals": V11_CURRENT13, "original12_complete_owner_packet_literals": V11_ORIGINAL12,
             "planned_owned_filenames": V11_PLANNED_OWNED, "planned_exact_success_inclusive_owned_files":18,
             "planned_maximum_inclusive_owned_files":20, "current_review_routes":V11_CURRENT_REVIEW_ROUTES,
             "saved_v11_array_expected_SHA256":V11_ARRAY_SHA}
    require(all(ready[k] == policy[k] == value for k,value in fixed.items()), "Every current scope/cap/retention/route fixed before origins")
    require(ready["prospective_run_flags"] == policy["prospective_run_flags"] == flags(), "Every current run qualification flag fixed")
    v11_full_optimization_cache_guard([AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"])
    _V11_METHOD = v11_method_and_current_reviews(ready,policy)
    for name,pin,counts,ownership,schema in V11_CURRENT13:
        packet(name,pin,counts,schema,ownership,terminal_header=name != ALLOCATION_PACKETS[2][0])
    source_protocol_checks(read(AUDIT / "manifest.json"))
    external = v11_startup_and_runtime_roles()
    require(set(ready["interpreter_expected_SHA256"]) == {str(LAUNCHER), str(_BASE_SCOPE / "python.exe")}, "Only two actual pinned interpreter routes")
    require(ready["interpreter_expected_SHA256"] == policy["interpreter_expected_SHA256"] == _V11_METHOD["runtime_admission_plan"]["interpreter_expected_SHA256"], "Both original expected interpreter pins")
    for key,pin in ready["interpreter_expected_SHA256"].items():
        bind(Path(key),pin)
    for key,pin in external.items():
        require(_EXTERNAL[key] == pin, "All original2842 expected stdlib pins already directly admitted")
    producer_ready = read(V11_LEAF_READY); producer_policy = read(V11_PRODUCER_POLICY)
    require(producer_ready["minimum75_complete_owner_packet_literals"] == producer_policy["minimum75_complete_owner_packet_literals"] == V11_ORIGINAL12,
            "Historical producer original12 exact; no late min78, V14 or external min80 audit")
    for key,pin in producer_ready["static_review_expected_SHA256"].items():
        bind(ROOT/key,pin)
    v11_original_history_admission(producer_ready,producer_policy)
    copied_metadata_provenance()
    current_controller_code_guard()
    contract = v11_original_ordered_contract()
    require(ready["complete_ordered_ABI_signature"] == policy["complete_ordered_ABI_signature"] == contract["complete_ordered_ABI_signature"], "Full current ordered ABI exact")
    _V11_READY, _V11_POLICY = ready, policy
    _V11_OWNERS = v11_snapshot_owner_witnesses()
    v11_completed_metadata_witness()
    budget(admission=True)
    return contract

def v11_repeated_metadata_witnesses():
    budget()
    require(read(READY)["static_review_expected_SHA256"] == _V11_READY["static_review_expected_SHA256"], "Exact same current review map on both union sides")
    for key,pin in _V11_READY["static_review_expected_SHA256"].items():
        require(_FROZEN[key] == pin and digest(ROOT/key,fresh=True) == pin, "Every current review directly expected and fresh SHA unchanged")
    v11_snapshot_owner_witnesses()
    v11_completed_metadata_witness()
    v11_startup_and_runtime_roles()
    failed_material_witness()
    selection_failure_witnesses()
    prior_inventory_failure_witness()
    held_v1_witness()
    held_audit_V1_absences()
    check_code_caches()
    saved_runtime_membership()

def fresh_union():
    runtime_scopes()
    for lexical,(actual,_) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical,fresh=True)==actual, "Every lexical path freshly confined")
    union={}
    for mapping in (_FROZEN,_EXTERNAL):
        for key,pin in mapping.items():
            path=Path(key) if Path(key).is_absolute() else ROOT/key
            require(path not in union or union[path]==pin, "Equal original expectations in complete role union")
            union[path]=pin
    for path,pin in _OBSERVED.items():
        if path.is_relative_to(OUTPUT):
            # New owned output bytes are custody, never inherited input expectations.
            continue
        require(path in union and union[path]==pin, "Every input observation already has equal original expected authority")
    total=0
    for path,pin in sorted(union.items()):
        budget()
        actual=canonical(path,fresh=True);total+=actual.stat().st_size
        require(len(union)<=MAX_REFERENCES and total<=MAX_UNIQUE_BYTES and digest(actual,fresh=True,already_resolved=True)==pin, "Complete fresh uncached bytes SHA and caps")
    for directory,members in _OWN_INVENTORIES.items():
        require(inventory(directory)==members, "Every current original SUCCESS inventory unchanged")
        no_failure(directory)
    require(standard_runtime_members()==_STANDARD_RUNTIME_MEMBERS, "Complete actual current standard runtime membership unchanged")
    require(not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME), "All externally declared runtime/cache/history absences unchanged")
    v11_repeated_metadata_witnesses()
    loaded_origins()
    return {"unique_paths":len(union),"unique_bytes":total,"full_fresh_resolve_and_SHA":True,
            "current_reviews_direct_expected_membership":True,"startup6_saved3057_strict2842_roles_retained":True}

def main():
    global _STARTED, _V11_OUTPUT_IDENTITY
    _STARTED=process_started()
    runtime_scopes()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256",required=True)
    args=parser.parse_args()
    runtime_invocation_guard(args.ready_sha256)
    require(canonical(__file__)==AUTHOR and not OUTPUT.exists() and not OUTPUT.is_symlink(), "One exclusive new independent V11 output route")
    try:
        contract=v11_admission(args.ready_sha256)
        current_runtime=own_runtime()
        saved_runtime_membership()
        v11_repeated_metadata_witnesses()
        first=fresh_union()
        v11_repeated_metadata_witnesses()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        info = OUTPUT.stat()
        _V11_OUTPUT_IDENTITY = (info.st_dev, info.st_ino)
        v11_output_custody()
        for path in (AUTHOR,METHOD_DOC,PREFLIGHT,READY):
            copy(path,"executed_"+path.name)
        save("run_started.json",{"created_UTC":datetime.now(timezone.utc).isoformat(),"current_runtime":current_runtime,
             "limits_CPU_admission_wall":[CPU,ADMISSION,WALL],"completed_v11_manifest_SHA256":V11_LEAF_SHA,**flags()})
        descriptor=read(V11_LEAF/"native_descriptor.json")
        rows=v11_read_rows(descriptor)
        structural=v11_saved_array_universal_proof(rows,descriptor,contract)
        save("independent_saved_all_rows_and_signed75_semantics.json",structural)
        cases=v11_fresh64_cases()
        save("independent_fixed64_native_cases.json",{"schema":"a13-v11-min75-independent-audit-fixed-native-cases-v1","case_count":64,"duplicates_retained":True,"cases":cases})
        batch=v11_fresh_forward_inverse(rows,descriptor,cases)
        save("independent_actual_forward_inverse_all_wire_batch.json",batch)
        toys=v11_fresh900_and_controls()
        save("independent900_unsigned_toys_and_four_controls.json",toys)
        macro=read(V11_LEAF/"paid_CCX_macro.json")["macro"]
        phase=v11_fresh_cyclic8_phase(macro)
        save("independent_cyclic8_absolute_phase.json",phase)
        resources=v11_fresh_resource_dependencies(rows,descriptor["qubits"],macro)
        save("independent_dict_dependency_actual_resources.json",resources)
        comparison=v11_compare_original_reports(structural,cases,batch,toys,phase,resources)
        save("independent_original_report_comparison.json",comparison)
        comparator=v11_unmatched_comparator_scope()
        save("independent_unmatched_v11_comparator_scope.json",comparator)
        save("independent_full_ordered_ABI_and_source_scope.json",{"exact_original_contract":contract,"row_id":V11_ROW_ID,
             "full_signed144_floor40_mod72_and_dirty_XOR":True,"complete_product_sign_carry_low_high_bits":[75,74,76,35,37],
             "coherent_promised_span_tensor_arbitrary_reference_only":True,"caller_copies_QROM_selector_storage_inverse_allowance_all_remaining_MULs_fullsource_still_open":True,
             "matched_executed_v11_wide_baseline":None,"savings":None,"whole_source_or_financial_G2_adoption_cost_advantage":False,**flags()})
        save("independent_owner_scope_metadata.json",{**_V11_OWNERS,"six_exact_original_startup_records":V11_STARTUP6,
             "saved3057_runtime_record_SHA256":V11_INTERPRETER_SHA,"strict_external2842_map_SHA256":V11_STDLIB2842_CANONICAL_SHA,
             "operational_clarification_SHA256":V11_CLARIFICATION_SHA,"historical_producer_static_reviews_transitive_READY_not_retroactive_direct_membership":True})
        v11_repeated_metadata_witnesses()
        second=fresh_union()
        v11_repeated_metadata_witnesses()
        summary={"schema":"a13-d4-s4-v11-signed-leaf-min75-independent-audit-summary-v1","passed":True,"completed":True,"budget_censored":False,
             "row_id":V11_ROW_ID,"source_row_id":ROW_ID,"value":11,"ordered_args":[10,9],"ordered_active_signed_widths":[34,41],
             "word_fraction_product_residue_bits":[72,40,144,75],"completed_v11_manifest_SHA256":V11_LEAF_SHA,"completed_v11_counts":V11_LEAF_COUNTS,
             "actual_saved_native_array_SHA256":V11_ARRAY_SHA,"all_saved_rows_and_universal_ABI_checked":True,
             "native_forward_inverse_batch":batch,"900_scalar_toys_four_controls_passed":True,"fresh8_absolute_unit_phase_passed":True,
             "actual_standalone_resources":resources,"producer_science_compared_only_after_fresh_independent_results":True,
             "unmatched_v11_scope":comparator,"both_full_uncached_input_unions":[first,second],"limits_CPU_admission_wall":[CPU,ADMISSION,WALL],
             "terminal_budget_observation":{"process_CPU_seconds":time.process_time(),"wall_seconds":time.monotonic()-_STARTED},**flags()}
        budget();save("summary.json",summary);save("completion_outcome.json",{**summary,"failed":False})
        members=inventory(OUTPUT)
        require({path.name for path in members}==set(V11_PLANNED_OWNED)-{"manifest.json"} and len(members)==17,"Exactly18 inclusive preregistered new success names")
        files={};total=0
        for path in sorted(members):
            budget();total+=path.stat().st_size
            require(total<=MAX_OWN_BYTES and len(files)<MAX_OWN_FILES-1,"Manifest inclusive original retention caps")
            files[path.name]=digest(path,fresh=True)
        complete_manifest({"schema":"a13-d4-s4-v11-signed-leaf-min75-independent-audit-manifest-v1","files":files,"frozen_inputs":_FROZEN,"external_runtime_inputs":_EXTERNAL,
             "manifest_self_hash_excluded":True,"passed":True,"completed":True,"budget_censored":False,
             "completed_v11_manifest_SHA256":V11_LEAF_SHA,"current13_complete_owner_packet_literals":V11_CURRENT13,
             "both_full_uncached_input_unions":[first,second],"terminal_budget_observation":{"process_CPU_seconds":time.process_time(),"wall_seconds":time.monotonic()-_STARTED},**flags()},files,total)
        budget();print(json.dumps({"passed":True,"manifest_SHA256":digest(OUTPUT/"manifest.json",fresh=True),**flags()}),flush=True)
    except BaseException as error:
        retain_failure(error)
        raise

if __name__ == "__main__":
    main()
