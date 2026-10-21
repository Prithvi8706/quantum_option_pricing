"""Prospective second independently audited ordered signed38x40 multiplication leaf.

One fixed v8 standalone complete78/F40/dirty72 XOR leaf, not full source.
New construction and full independent checks require separate ROOT release.
"""


from array import array

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


AUTHOR = RESEARCH / 'prototype_a13_d4_s4_second_signed_leaf_min78_v2.py'
HELPER = RESEARCH / 'build_a13_d4_s4_second_signed_leaf_min78_v2.py'


METHOD_DOC = RESEARCH / 'A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_PREFLIGHT_V2.md'


PREFLIGHT = RESEARCH / 'a13_d4_s4_second_signed_leaf_min78_preflight_v2.json'


READY = ROOT / '.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_ROOT_READY_run002.json'


OUTPUT = ROOT / 'results/limitation_program_20261001/A13_d4_s4_second_signed_leaf_min78_run002'


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


INVENTORY_MODULE = 'research.limitation_program_20261001.prototype_a13_d4_s4_second_signed_leaf_min78_v2'


RUNTIME_INVOCATION = ["-B", "-m", INVENTORY_MODULE]


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



# New lowering and full eleven current owners; original nine metadata scopes stay literal.
LEAF_LOWERING_ROW_ID = 'A13_D4_S4_V8_SIGNED38X40_COMPLETE_PRODUCT78_SIGN38_TO72_V1'
BASELINE112_SHA = '67e3f264ef222f92b33537d4b3db1e397ccc712ed075364960231b8892e0cfed'
BASELINE112_COUNTS = [58, 1638, 2842]
BASELINE112_READY_SHA = 'd440ad7e684cb2491bd9ab6627f9061ee3a531beca1d36c110722bd771758790'
BASELINE112_AUTHORS = {'A13_D4_S4_FIRST_SIGNED_LEAF_IMPLEMENTATION_PREFLIGHT_V2.md': '451cb858fba32e9ca870be44fad8ee5a98cb04b5c317e900c39339d800176b13',
 'a13_d4_s4_first_signed_leaf_implementation_preflight_v2.json': '3c5b50dfd7b2efc96d4806b14a66e8f99dd18ca5b906ca1b8611adaf522bb8bb',
 'build_a13_d4_s4_first_signed_leaf_v2.py': '3d2bdc68aa39457faeb13900d3d83f666d5f92c49446ed7a2adec087912aa764',
 'prototype_a13_d4_s4_first_signed_leaf_v2.py': '02d2616422149e1e3de3b997c2396eba1309adce23472db2486d0228cf12f058'}
BASELINE112_RESULT_SHA = '5eab9fffdf29a0b68f8acba30d4882a388410b78c8d2ab5e07237162b409f4f8'
BASELINE112_AUDIT_SHA = 'e35e5e2b3b9b5833fd973f354c9f78303b66685d9d560a1f283be333de269326'
BASELINE112_AUDIT_COUNTS = [15, 1716, 2842]
BASELINE112_AUDIT_READY_SHA = '0535ca704201f1c1587c9b49908c35c7f2121c108bf320803dd454bae9efacbc'
BASELINE112_AUDIT_AUTHORS = {'A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_PREFLIGHT_V2.md': '9fd435b226da391315c1fc645a6cb8a02cda1e8e7d4d000e27cd837e36ddca48',
 'a13_d4_s4_first_signed_leaf_independent_audit_preflight_v2.json': '3cd28c170a37b252bfeadeeffda0b3bd11ce8f9fd341b31ab290e61e1a1ed87a',
 'audit_a13_d4_s4_first_signed_leaf_v2.py': '3da298fa3032693d823034410dadfa638cf1af422ccd04faae6c66534d24df5e'}
BASELINE112_AUDIT_RESULT_SHA = '0417e2f1a4c89a2e6ebeb48330e1d10dc77fae396a5184917343cc11c714f10f'
MIN80_COMPLETED11 = [['A13_recovery_run001',
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
  'a13-d4-s4-first-signed-leaf-independent-audit-manifest-v2']]
MIN80_PROSPECTUS_PINS = {'.context/A13_SIGNED_PRODUCT_WIDTH_SIGN_EXTENSION_INDEPENDENT_STATIC_REVIEW_run001.json': '5922ed6235c28dd764f29f1023d6bda2b749fb08d5afb3956dab025c44b29bf2',
 '.context/A13_SIGNED_PRODUCT_WIDTH_WITH_EXPLICIT_OUTPUT_SIGN_EXTENSION_PROSPECTUS_run001.json': 'c520f72be274ef5d63e432695309cd010b86fd3098d256ef08326d492ea828fa',
 '.context/A13_SIGNED_PRODUCT_WIDTH_WITH_EXPLICIT_OUTPUT_SIGN_EXTENSION_PROSPECTUS_run001.md': 'b787aa47e1b48aedc3b459a068cd755454661953b345feaa1afa272dade84127'}
MIN80_METHOD_REVIEW_KEY = '.context/A13_SIGNED_PRODUCT_WIDTH_SIGN_EXTENSION_INDEPENDENT_STATIC_REVIEW_run001.json'
BASELINE112 = PROGRAM / "A13_d4_s4_first_signed_leaf_run002"
BASELINE112_AUDIT = PROGRAM / "A13_d4_s4_first_signed_leaf_audit_run002"
BASELINE112_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ROOT_READY_run002.json"
BASELINE112_AUDIT_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_AUDIT_ROOT_READY_run002.json"
BASELINE112_RESULT = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"
BASELINE112_AUDIT_RESULT = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_AUDIT_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"


# Current twelve-owner scope; original nine/eleven literal history remains independent.
MIN78_COMPLETED12 = [['A13_recovery_run001',
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
MIN78_PROSPECTUS_PINS = {'.context/A13_V8_SIGNED38X40_MINIMUM78_AUTHOR_METADATA_QA_run001.json': '5153b4c6270af969b0e3f1ebb47538e7a5f576a16f4f0f5196e18d78739a26e0',
 '.context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.json': '3c035895661a2fb41f82656814123ca12acc88c87cbfd484488df6418a3fad30',
 '.context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.md': 'ed4bc634f34180be1f495cd54c4e8ca3f3516705d9571da6b484ef67c8a50687',
 '.context/A13_V8_SIGNED38X40_MINIMUM78_ROOT_PROSPECTIVE_METHOD_REVIEW_run001.json': '4905c9f4d83840f9d52f1e170e8a5dc157c9203e95ecd19e9a99fc44339dece1'}
MIN78_ROOT_METHOD_REVIEW_KEY = '.context/A13_V8_SIGNED38X40_MINIMUM78_ROOT_PROSPECTIVE_METHOD_REVIEW_run001.json'
COMPLETED80 = PROGRAM / "A13_d4_s4_first_signed_leaf_min80_run001"
COMPLETED80_AUTHORITY = {'ROOT_READY_SHA256': '42a92d6c63f244a1e6ae568415e8523c3eaad69a21dcd7d2fbf01737f30fe201',
 'ROOT_READY_path': '.context/A13_D4_S4_FIRST_SIGNED_LEAF_MIN80_ROOT_READY_run001.json',
 'ROOT_receipt_SHA256': 'b97356dd3dc51049351da54a754ee516561c3d74c5ab8524a8a64b234dfb13a7',
 'ROOT_receipt_path': '.context/A13_D4_S4_FIRST_SIGNED_LEAF_MIN80_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json',
 'complete_counts': [59, 1741, 2842],
 'completed_AUTHOR_SHA256': {'A13_D4_S4_FIRST_SIGNED_LEAF_MIN80_PREFLIGHT_V1.md': '0093cfc38c24fcc8b93e7f5e87f2d6819448ef4ca9ed5cf21bf72418d64f4d58',
                             'a13_d4_s4_first_signed_leaf_min80_preflight_v1.json': '8464d6a8e938e4f7bdaef0add101690c4b6d694aea7913d3796143c6078d841b',
                             'build_a13_d4_s4_first_signed_leaf_min80_v1.py': 'bd178f53783359b54494b8a2e776bbfa444f24ab6dfe77a2502a210bf35d939f',
                             'prototype_a13_d4_s4_first_signed_leaf_min80_v1.py': '09977778197c82d4548e5ae1d8d51995fcf8b8e3f01c6f5a62ce2f9d2c39357e'},
 'externally_ROOT_declared_not_observed_refresh': True,
 'inclusive_owned_files': 60,
 'manifest_SHA256': 'a5f6d39d8ae4cef0f4a968f0fb872c80e8028873a8e7c9aa9fb6be43f0c2f42f',
 'manifest_path': 'results/limitation_program_20261001/A13_d4_s4_first_signed_leaf_min80_run001/manifest.json'}


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
    found, total = set(), 0
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(canonical(candidate).is_relative_to(directory), "No owned directory escape")
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(Path(root) / name)
            require(actual.is_relative_to(directory) and actual not in found, "Unique owned path")
            require(actual.is_file(), "Regular actual owned entry")
            found.add(actual)
            total += actual.stat().st_size
            require(len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, "Finite owned inventory")
    return found


def own_runtime():
    global _STANDARD_RUNTIME_MEMBERS
    require(
        canonical(sys.executable) == canonical(LAUNCHER)
        and sys.dont_write_bytecode is True
        and canonical(Path.cwd()) == ROOT,
        "Exact pinned launcher/cwd and startup -B",
    )
    require(
        not any(os.environ.get(key) for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")),
        "No inherited runtime search/cache overrides",
    )
    require(canonical(sys.prefix) == ROOT / ".context/frontier_t0_env", "Pinned isolated prefix")
    cfg = Path(sys.prefix) / "pyvenv.cfg"
    add(cfg, digest(cfg))
    require(
        "include-system-site-packages = false" in cfg.read_text(encoding="utf-8").lower(),
        "Base site packages disabled",
    )
    base = canonical(sys.base_prefix)
    permitted = {
        ROOT,
        RESEARCH,
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
        canonical(base / "Lib"),
        canonical(base / "DLLs"),
    }
    for entry in sys.path:
        lexical = Path(os.path.abspath(str(ROOT if not entry else entry)))
        require(
            not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)
            and not any(
                lexical.resolve(strict=False).is_relative_to(scope) for scope in _EXCLUDED_SCOPE
            ),
            "No excluded search path even when absent",
        )
        if not lexical.exists():
            expected_zip = base / (
                "python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"
            )
            require(
                lexical == expected_zip and lexical.resolve(strict=False) == expected_zip,
                "Only the exact absent standard interpreter zip search entry",
            )
            _ABSENT_RUNTIME.add(lexical)
            continue
        path = canonical(ROOT if not entry else entry)
        require(
            path in permitted or (path.is_file() and path.parent == base and path.suffix == ".zip"),
            "Finite actual runtime search path",
        )
        if path.is_file():
            add(path, digest(path))
    candidates = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = candidates
    total = 0
    for path in sorted(candidates):
        require(path.is_file(), "Regular complete runtime member")
        total += path.stat().st_size
        require(
            len(candidates) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Fixed24k runtime files/2GiB",
        )
        add(path, digest(path))
    loaded_origins()
    return {
        "files": len(candidates),
        "bytes": total,
        "base_site_packages_pruned_and_rejected": True,
    }


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


def fresh_union():
    runtime_scopes()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(canonical(lexical, fresh=True) == actual, "Every lexical alias freshly confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, expected in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == expected, "Equal-SHA complete union")
            union[path] = expected
    for path, value in tuple(_OBSERVED.items()):
        budget()
        require(path not in union or union[path] == value, "Observed never replaces expected")
        union[path] = value
    total = 0
    for path, expected in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        total += actual.stat().st_size
        require(len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES, "Complete union caps")
        require(
            digest(actual, fresh=True, already_resolved=True) == expected, "Full fresh actual SHA"
        )
    for directory, members in _OWN_INVENTORIES.items():
        budget()
        require(inventory(directory) == members, "All original own inventories unchanged")
        no_failure(directory)
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete runtime membership unchanged",
    )
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Absent standard zip and new-code caches still absent",
    )
    return {"unique_paths": len(union), "unique_bytes": total, "full_fresh_resolve_and_SHA": True}


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


def save(name, value):
    budget()
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
    require(target.stat().st_size == new_bytes, "Exactly admitted output bytes")
    budget()


def copy(path, name):
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


def current_packet():
    directory = canonical(AUDIT)
    manifest = bind(directory / "manifest.json", AUDIT_SHA)
    data = read(manifest)
    no_failure(directory)
    require(
        data.get("schema") == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and data.get("passed") is True
        and data.get("completed") is True
        and data.get("budget_censored") is False
        and data.get("manifest_self_hash_excluded") is True
        and data.get("original_expected_hashes_waived") is False
        and data.get("manifest_inclusive_retention_checked") is True
        and data.get("manifest_inclusive_owned_count") == 64,
        "Only actual completed current V6 all20 scientific-audit receipt",
    )
    require(
        [len(data[field]) for field in (("files"), ("frozen_inputs"), ("external_runtime_inputs"))]
        == AUDIT_COUNTS,
        "Complete current63/1208/2842 maps, no reduced index",
    )
    owned = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        require(type(data[field]) is dict, "Typed complete current maps")
        for key, expected in data[field].items():
            budget()
            if field == "external_runtime_inputs":
                require(
                    type(key) is str and Path(key).is_absolute(),
                    ("Exact absolute external spelling"),
                )
                path = Path(key)
            else:
                exact_relative(key)
                path = directory / key if field == "files" else ROOT / key
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory)
                    and actual not in owned
                    and actual.relative_to(directory).as_posix() == key,
                    "Exact receipt-relative current owned key and physical confinement",
                )
                owned.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    ("Exact source ROOT-relative expectation"),
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    ("Exact source external expectation"),
                )
    require(
        inventory(directory) == owned and len(owned) == 64,
        ("Complete current64 actual owned inventory"),
    )
    _OWN_INVENTORIES[directory] = owned
    require(
        {
            key.split(("/"), 1)[1]: pin
            for key, pin in data[("files")].items()
            if key.startswith(("executed_code/"))
        }
        == REQUIRED_SNAPSHOTS,
        "All25 original snapshot names and hashes unchanged",
    )
    require(
        {key for key in data[("files")] if key.startswith(("rows/"))}
        == {f"rows/d{d}_s{s}.json.gz" for d, s in GRID},
        "Exactly20 fresh canonical compressed row names",
    )
    require(
        data[("files")].get(("protocol.json")) == PROTOCOL_SHA,
        ("Externally preserved prepared protocol expected SHA"),
    )
    require(
        data["historical_global_LIVE_integrity"]
        == {
            ("passed"): False,
            ("mismatch_references"): 36,
            ("distinct_paths"): 9,
            ("expected_hashes_waived"): False,
        },
        "Historical LIVE mismatch remains unapproved and unwaived",
    )
    return data


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
                # An absent potential cache is checked now, not promoted into expected input scope.
                # Independently declared absent caches remain in _ABSENT_RUNTIME and both unions.


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
    if not OUTPUT.is_dir():
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
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"new_scientific_outcome_uncertified":true,"full_G2":false,"adoption":false,"quantum_advantage":false}\n'
            )
    except OSError:
        pass


MIN78_HELD_V1_AUTHORITY = {'author_method_SHA256': {'prototype_a13_d4_s4_second_signed_leaf_min78_v1.py': 'eefa45a0502e80b05e0ca8df3d4bafab114023528fef0f869eb98bedc4905d20', 'build_a13_d4_s4_second_signed_leaf_min78_v1.py': 'c73ef20ec17e795419f760e24d7fbf42deb6e7713d773b9c00c854e0f4f1b323', 'A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_PREFLIGHT_V1.md': 'a633e4ef1452f7ce13633d304b4896c5e27a37372f8c64090a21e09481c2266b', 'a13_d4_s4_second_signed_leaf_min78_preflight_v1.json': 'f6344bd43ce51ebc3c679373f7d762158118444545da5e1e49d7a104721f0c9a'}, 'static_QA_expected_SHA256': {'.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_AUTHOR_STATIC_QA_run001.json': '2717c4140b49bda19156d41dc7942957c0ea0338e01ace4d0e3aa6d1ac67debe', '.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_AUTHOR_STATIC_QA_SUPPLEMENT_run001.json': 'f6a66244da60863da7061b06bd4211acc6de6e0bd52ae2660570e0ece2ab46f2', '.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_AUTHOR_STATIC_AST_INVERSE_run001.json': 'fa70b4459b0d3a7f0d6f61c4d0015c8795c154ae3ce09fce927f3def18480739'}, 'independent_HOLD_path': '.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_INDEPENDENT_STATIC_PEER_run001.json', 'independent_HOLD_SHA256': '004cd299481cf1eddc7664d18481fd650ea5c514374ac09187912c687c365f66', 'ROOT_READY_absent': '.context/A13_D4_S4_SECOND_SIGNED_LEAF_MIN78_ROOT_READY_run001.json', 'output_absent': 'results/limitation_program_20261001/A13_d4_s4_second_signed_leaf_min78_run001', 'all6_original_cache_routes': ['research/limitation_program_20261001/__pycache__/build_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/build_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/build_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.pyc', 'research/limitation_program_20261001/__pycache__/prototype_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/prototype_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/prototype_a13_d4_s4_second_signed_leaf_min78_v1.cpython-312.pyc'], 'held_expected_legacy_runtime_invocation': ['-B', '-m', 'research.limitation_program_20261001.prototype_a13_d4_s4_first_signed_leaf_min80_v1'], 'historical_route_executed_or_authorized': False}


def minimum78_retain_held_v1_route(ready, policy):
    require(ready["minimum78_held_V1_authority"] == policy["minimum78_held_V1_authority"]
            == MIN78_HELD_V1_AUTHORITY, "Exact unexecuted V1 author/HOLD authority, no approval")
    for name, pin in MIN78_HELD_V1_AUTHORITY["author_method_SHA256"].items():
        bind(RESEARCH / name, pin)
    for key, pin in MIN78_HELD_V1_AUTHORITY["static_QA_expected_SHA256"].items():
        bind(ROOT / key, pin)
    bind(ROOT / MIN78_HELD_V1_AUTHORITY["independent_HOLD_path"],
         MIN78_HELD_V1_AUTHORITY["independent_HOLD_SHA256"])
    minimum78_full_optimization_cache_guard(
        [RESEARCH / "prototype_a13_d4_s4_second_signed_leaf_min78_v1.py",
         RESEARCH / "build_a13_d4_s4_second_signed_leaf_min78_v1.py"],
        ready["held_min78_V1_all_optimization_existing_cache_SHA256"],
        ready["held_min78_V1_all_optimization_absent_cache_paths"])
    for key in (MIN78_HELD_V1_AUTHORITY["ROOT_READY_absent"],
                MIN78_HELD_V1_AUTHORITY["output_absent"]):
        p = ROOT / key
        require(not p.exists() and not p.is_symlink() and p.resolve(strict=False) == p,
                "Held original V1 READY/output remain physically absent")
        _ABSENT_RUNTIME.add(p)
    budget()


def flags():
    return {
        "second_v8_ordered_standalone_signed_leaf_only": True,
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
        "gate_emission_authorized": True,
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


def allocation_binding():
    source = PROGRAM / ALLOCATION_PACKETS[0][0]
    auditor = PROGRAM / ALLOCATION_PACKETS[1][0]
    root_owner = PROGRAM / ALLOCATION_PACKETS[2][0]
    primary = read(source / "summary.json")
    audit = read(auditor / "summary.json")
    root = read(root_owner / "summary.json")
    authorization = read(auditor / "primary_allocation_authorization.json")
    polynomial = read(source / "uniform_poly_allowance.json")
    require(
        primary["schema"] == "a13-fixed-alpha-allocation-producer-summary-v1"
        and audit["schema"] == "a13-fixed-alpha-allocation-auditor-summary-v1"
        and root["schema"] == "root-exp-frontier-fixed-alpha-fresh-integrity-v2",
        "Exact original primary90/independent130/ROOT allocation summaries",
    )
    for document in (primary, audit, root):
        require(
            document["completed"] is True
            and document["passed"] is True
            and document["budget_censored"] is False
            and document["conditional_allocation_release_eligible"] is True
            and document["alpha"] == ALPHA
            and document["conditional_E_allow_lower"] == ALLOWANCE,
            "Same externally approved fixed-alpha and exact primary-owned positive allowance",
        )
    require(
        audit["independent_allocation_audit_passed"] is True
        and audit["actual_source_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and root["actual_primary90_and_independent130_terminal_PASS"] is True
        and root["primary_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and root["audit_manifest_sha256"] == ALLOCATION_PACKETS[1][1],
        "Actual independent certification and ROOT input binding",
    )
    require(
        authorization["independent130_authorizes_complete_primary90_result"] is True
        and authorization["conditional_allocation_release_eligible"] is True
        and authorization["source_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and authorization["approved_primary_E_allow_lower"] == ALLOWANCE
        and authorization["new_fixture_credit"] == 0,
        "Exact primary lower allowance independently authorized, no own-lower substitution",
    )
    require(
        polynomial["schema"] == "a13-fixed-alpha-native-poly-allowance-v1"
        and polynomial["interval_digits"] == 90
        and polynomial["alpha"] == ALPHA
        and polynomial["E_allow_lower"] == ALLOWANCE
        and polynomial["all_nonempty_allowances_strict_positive"] is True
        and polynomial["allowance_is_outward_lower_not_polynomial_error_upper"] is True
        and polynomial["candidate_quantization_all_internal_floors_and_full_realization_must_fit"]
        is True
        and polynomial["final_shift_floor_paid_separately"] == [1, 1 << 40],
        "Primary scalar premise separates polynomial, reduction and final shift budgets",
    )
    allowance = rational(ALLOWANCE)
    require(
        0 < allowance <= rational(authorization["independent_own_release_lower"]),
        "Strict positive primary lower bound never replaced by tighter independent result",
    )
    for document in (primary, audit):
        require(
            document["both_financial_residual_fit"] is True
            and document["all_nonempty_allowances_strict_positive"] is True,
            "Both unchanged original contracts retain allocation premise",
        )
        for key in (
            "full_G2",
            "adoption",
            "cost_transfer",
            "quantum_advantage",
            "actual_candidate_G2_feasibility_established",
        ):
            require(
                document[key] is False, "Original allocation is conditional, not changed-source G2"
            )
    return allowance


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


def check(started):
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
        "runtime_invocation": RUNTIME_INVOCATION,
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


def admission(ready_sha):
    require(
        not os.environ.get("PYTHONINTMAXSTRDIGITS")
        and "int_max_str_digits" not in sys._xoptions
        and sys.get_int_max_str_digits() == 4300,
        "Original bounded4300-digit conversion policy, no environment or -X override",
    )
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a13-d4-s4-second-signed-leaf-min78-READY-v2"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["local_only"] is True,
        "Separate prospective reviewed local selection release",
    )
    require(
        FINAL_ROOT_SHA is not None and FINAL_ROOT_COUNTS is not None,
        "Externally completed final ROOT receipt must be non-null before freeze",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["audit_manifest_SHA256"] == AUDIT_SHA
        and ready["audit_complete_counts"] == AUDIT_COUNTS
        and ready["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and ready["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and ready["metadata_source_manifest_SHA256"]
        == "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9"
        and ready["fixed_alpha_allocation_packets"] == ALLOCATION_PACKETS
        and ready["fixed_alpha"] == ALPHA
        and ready["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Exact externally declared six full-owner packets, same fixed allowance and caps",
    )
    require(ready["gate_emission_authorized"] is True, "Only separately released standalone gate emission")
    for key in (
        "financial_adoption",
        "full_G2",
        "cost_transfer",
        "quantum_advantage",
    ):
        require(
            ready[key] is False,
            "Only exact rational selection, no emission/adoption/advantage release",
        )
    require(ready["fixture_credit"] == 0, "No additional test credit")
    authors = ready["author_method_SHA256"]
    require(
        type(authors) is dict and set(authors) == {AUTHOR.name, HELPER.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly four externally frozen new controller/helper/method/policy bytes",
    )
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a13-d4-s4-second-signed-leaf-min78-preflight-v2"
        and policy["author_SHA256"] == authors[AUTHOR.name]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["fixed_row_id"] == ROW_ID
        and policy["audit_manifest_SHA256"] == AUDIT_SHA
        and policy["audit_complete_counts"] == AUDIT_COUNTS
        and policy["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and policy["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and policy["fixed_alpha_allocation_packets"] == ALLOCATION_PACKETS
        and policy["fixed_alpha"] == ALPHA
        and policy["approved_primary_E_allow_lower"] == ALLOWANCE
        and policy["fixed_class_segment_slots"] == 240
        and policy["maximum_native_cell_metadata"] == MAX_NATIVE_CELLS
        and policy["rational_scalar_result_bit_caps"] == [MAX_SCALAR_BITS, MAX_RESULT_BITS],
        "Exact prospective fixed rule and finite metadata/rational bounds",
    )
    admit_prior_inventory_failure(ready, policy)
    admit_prior_selection_failure(ready, policy)
    manifest = current_packet()
    source_protocol_checks(manifest)
    reconcile_metadata(manifest)
    packet(
        "A13_recovery_run001",
        "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9",
        [16, 909, 2842],
        "a13-exp-frontier-recovery-terminal-manifest-v1",
        "receipt",
    )
    final = packet(
        FINAL_ROOT.name,
        FINAL_ROOT_SHA,
        FINAL_ROOT_COUNTS,
        "a13-recovery-audit-root-integrity-manifest-v6",
        "receipt",
    )
    require(
        final["audit_manifest_SHA256"] == AUDIT_SHA
        and final["audit_complete_counts"] == AUDIT_COUNTS
        and final["current_scoped_all20_certification_integrity_verified"] is True,
        "Actual final ROOT integrity of exact independent all20 receipt",
    )
    root_summary = read(FINAL_ROOT / "summary.json")
    require(
        root_summary["schema"] == "a13-recovery-audit-root-integrity-summary-v6"
        and root_summary["completed"] is True
        and root_summary["passed"] is True
        and root_summary["budget_censored"] is False
        and root_summary["audit_manifest_SHA256"] == AUDIT_SHA
        and root_summary["current_scoped_all20_certification_integrity_verified"] is True,
        "Completed final ROOT terminal, never old failure or foreign continuation substitution",
    )
    for args in ALLOCATION_PACKETS:
        packet(*args, terminal_header=args[0] != ALLOCATION_PACKETS[2][0])
    allocation_binding()
    audit_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    require(
        audit_ready["schema"] == "root-a13-recovery-audit-READY-v6"
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS,
        "Original independent audit release retains exact original author bytes",
    )
    code_caches(
        [RESEARCH / "audit_exp_frontier_recovery_v6.py"],
        audit_ready["existing_new_code_cache_SHA256"],
        audit_ready["absent_new_code_cache_paths"],
    )
    old_root_ready = read(bind(FINAL_ROOT_READY, FINAL_ROOT_READY_SHA))
    require(
        old_root_ready["schema"] == "root-a13-recovery-audit-integrity-READY-v6"
        and old_root_ready["audit_manifest_SHA256"] == AUDIT_SHA,
        "Externally pinned actual final ROOT original release",
    )
    code_caches(
        [RESEARCH / "verify_a13_recovery_audit_root_v6.py"],
        old_root_ready["existing_new_code_cache_SHA256"],
        old_root_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [AUTHOR, HELPER], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    executables = {canonical(LAUNCHER), canonical(Path(sys._base_executable))}
    pinned = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        actual = canonical(spelling)
        require(
            actual in executables and actual not in pinned,
            "Only actual distinct executable expected pins",
        )
        pinned.add(actual)
        bind(actual, expected)
    require(
        len(executables) == 2 and pinned == executables,
        "Both actual external interpreter expected pins",
    )
    failed_material_witness(initial=True)
    admit_completed_selector(ready, policy)
    return manifest


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


"""Author-only exact native-contract functions; no author-time evaluation."""


def admit_completed_selector(ready, policy):
    expectations = {
        "completed_selector_manifest_SHA256": SELECTOR_SHA,
        "completed_selector_complete_counts": SELECTOR_COUNTS,
        "completed_selector_READY_SHA256": SELECTOR_READY_SHA,
        "completed_selector_author_SHA256": SELECTOR_AUTHORS,
        "completed_selector_ROOT_result_review_SHA256": SELECTOR_RESULT_REVIEW_SHA,
        "fixed_row_id": ROW_ID,
        "fixed_class_segment_slots": 240,
    }
    require(
        all(ready[key] == policy[key] == value for key, value in expectations.items()),
        "All separately externally expected sole-selector premises fixed before arithmetic",
    )
    require(
        ready["new_scientific_evaluation"] is True
        and ready["independent_native_contract_audit_approved"] is True
        and policy["new_second_standalone_signed_leaf"] is True
        and policy["new_fitting_quantization_or_exponential_evaluation"] is False,
        "Separate release covers only fixed native interval induction and contract inventory",
    )
    manifest = packet(
        SELECTOR.name,
        SELECTOR_SHA,
        SELECTOR_COUNTS,
        "a13-certified-candidate-selection-manifest-v2",
        "receipt",
    )
    require(
        manifest["new_scientific_evaluation"] is False
        and manifest["candidate_feasibility"] is False
        and manifest["gate_emission_authorized"] is False
        and manifest["financial_gate_emission_authorized"] is False
        and manifest["full_G2"] is False
        and manifest["adoption"] is False
        and manifest["cost_transfer"] is False
        and manifest["new_test_credit"] == 0,
        "Completed selector grants metadata shortlist only, never leaf permission or credit",
    )
    old_ready = read(bind(SELECTOR_READY, SELECTOR_READY_SHA))
    require(
        old_ready["schema"] == "root-a13-certified-candidate-selection-READY-v2"
        and old_ready["author_method_SHA256"] == SELECTOR_AUTHORS
        and old_ready["output"] == SELECTOR.relative_to(ROOT).as_posix(),
        "Exact independently completed selector author/release bytes",
    )
    for name, expected in SELECTOR_AUTHORS.items():
        budget()
        require(
            manifest["frozen_inputs"][(RESEARCH / name).relative_to(ROOT).as_posix()] == expected,
            "Original complete selector expected source map retained",
        )
        bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "select_a13_certified_candidates_v2.py"],
        old_ready["existing_new_code_cache_SHA256"],
        old_ready["absent_new_code_cache_paths"],
    )
    bind(SELECTOR_RESULT_REVIEW, SELECTOR_RESULT_REVIEW_SHA)
    selector_result_witness()


def selector_result_witness():
    summary = read(SELECTOR / "summary.json")
    report = read(SELECTOR / "all20_candidate_selection.json")
    review = read(SELECTOR_RESULT_REVIEW)
    require(
        summary["schema"] == "a13-certified-candidate-selection-summary-v2"
        and summary["completed"] is True
        and summary["passed"] is True
        and summary["budget_censored"] is False
        and summary["shortlist_row_ids"] == [ROW_ID]
        and summary["audit_manifest_SHA256"] == AUDIT_SHA
        and summary["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and summary["fixed_alpha"] == ALPHA
        and summary["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Externally completed sole-row shortlist and original lower allowance unchanged",
    )
    require(
        report["schema"] == "a13-certified-exact-rational-candidate-selection-v1"
        and report["row_count"] == 20
        and report["native_cell_count"] == 4500
        and report["shortlist_row_ids"] == report["nondominated_ordered_row_ids"] == [ROW_ID]
        and report["fixed_alpha"] == ALPHA
        and report["approved_primary_E_allow_lower"] == ALLOWANCE
        and len(report["eligible_row_ids"]) == 18
        and report["candidate_G2_absolute_stock_error_allocation"] is None
        and report["candidate_G2_barrier_band_allocation"] is None
        and report["gate_emission_authorized"] is False,
        "Complete original fixed selection is an expected input, never re-ranked",
    )
    require(
        review["schema"] == "root-a13-selection-v2-result-reconciliation-v1"
        and review["passed"] is True
        and review["manifest_expected_SHA256"] == SELECTOR_SHA
        and review["shortlist_row_ids"] == [ROW_ID]
        and review["rows"] == 20
        and review["all_cells"] == 4500
        and review["occupied_cells"] == 4200
        and review["eligible_row_ids"] == report["eligible_row_ids"]
        and review["full_input_map_runtime_rewalk_performed"] is False
        and review["scientific_proofs_or_gate_costs_recomputed"] is False
        and review["gate_emission_or_financial_adoption_authorized"] is False
        and review["fixture_credit"] == 0,
        "ROOT result reconciliation remains scoped metadata, no transferred live integrity or gate permission",
    )
    for document in (summary, report):
        require(
            all(
                document[key] is False
                for key in (
                    "full_G2",
                    "adoption",
                    "cost_transfer",
                    "quantum_advantage",
                    "gate_emission_authorized",
                    "financial_gate_emission_authorized",
                    "candidate_feasibility",
                )
            )
            and document["new_test_credit"] == 0,
            "All old selector no-adoption/financial/no-credit fields unchanged",
        )
    selected = [row for row in report["rows"] if row["row_id"] == ROW_ID]
    require(
        len(report["rows"]) == 20
        and len(selected) == 1
        and selected[0]["shortlisted_for_future_contract_consideration"] is True
        and selected[0]["error_and_native_eligible_for_contract_consideration"] is True
        and selected[0]["all_native_metadata_promises_valid"] is True
        and selected[0]["rejections"] == [],
        "One exact selected scientific premise, never another search architecture",
    )
    return selected[0]


def admitted_text_AST(path):
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


def producer_result_witness():
    budget()
    summary, outcome = read(PRODUCER / "summary.json"), read(PRODUCER / "completion_outcome.json")
    require(outcome == {**summary, "failed": False}, "Exact complete producer terminal pair")
    require(
        summary["schema"] == "a13-d4-s4-native-contract-inventory-summary-v2"
        and summary["completed"] is summary["passed"] is True
        and summary["budget_censored"] is False
        and summary["row_id"] == ROW_ID
        and summary["fixed_cell_slots"] == 240
        and summary["ordered_shared_MUL_count"] == 6
        and summary["native_integer_domain_contract_inventory_passed"] is True
        and summary[
            "whole_source_operation_storage_selector_coefficient_copies_inverse_obligations_enumerated"
        ]
        is True
        and summary["all7_completed_owner_maps_and_owned_inventories_retained"] is True
        and summary["prior_inventory_pre_output_failure_retained_without_promotion"] is True
        and summary["original_capped_baselines_retained"] == BASELINES
        and summary["completed_selector_manifest_SHA256"] == SELECTOR_SHA
        and summary["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and summary["runtime_invocation"]
        == [
            "-B",
            "-m",
            "research.limitation_program_20261001.contract_a13_d4_s4_native_inventory_v2",
        ],
        "Only externally frozen completed native producer, no partial substitution",
    )
    for key in (
        "full_G2",
        "adoption",
        "cost_transfer",
        "quantum_advantage",
        "gate_emission_authorized",
        "financial_gate_emission_authorized",
        "candidate_feasibility",
        "actual_gate_schedule_or_cost_verified",
    ):
        require(summary[key] is False, "Producer inventory grants no gate/cost/financial adoption")
    require(
        summary["new_test_credit"]
        == summary["new_credited_gate_replays"]
        == summary["new_price_samples"]
        == 0,
        "No transferred fixture credit",
    )
    review = read(PRODUCER_RESULT_REVIEW)
    require(
        review["schema"] == "root-a13-d4-s4-native-contract-inventory-actual-owned-result-review-v2"
        and review["passed"] is True
        and review["manifest_SHA256"] == PRODUCER_SHA
        and review["complete_counts"] == PRODUCER_COUNTS
        and review["inclusive_owned_files"] == 32
        and review["all_new_owned_hashes_and_complete_inventory_verified"] is True
        and review[
            "result_summary_outcome_cells_six_ordered_contracts_source_obligations_scope_metadata_reconciled"
        ]
        is True
        and review["full_new_runtime_input_rewalk_repeated_by_this_ROOT_owned_review"] is False
        and review[
            "new_independent_integer_range_width_or_payment_recomputation_by_this_ROOT_owned_review"
        ]
        is False
        and review["independent_scientific_inventory_audit_still_required"] is True
        and review["financial_G2_cost_adoption_gate_or_fixture_credit"] is False,
        "ROOT result review remains owned/result metadata, not an independent scientific proof",
    )
    require(
        review["cell_slots_occupied"]
        == [summary["fixed_cell_slots"], summary["occupied_cell_slots"]]
        and review["both_full_uncached_input_union_metadata"]
        == summary["both_full_uncached_input_unions"],
        "Scoped ROOT review agrees with exact producer metadata",
    )
    budget()
    return summary


def audit_admission(ready_sha):
    require(
        PRODUCER_SHA is not None and PRODUCER_COUNTS is not None,
        "Externally completed inventory pins before release",
    )
    original_manifest = admission(ready_sha)
    ready, policy = read(READY), read(PREFLIGHT)
    expectations = {
        "producer_manifest_SHA256": PRODUCER_SHA,
        "producer_complete_counts": PRODUCER_COUNTS,
        "producer_READY_SHA256": PRODUCER_READY_SHA,
        "producer_author_SHA256": PRODUCER_AUTHORS,
        "producer_ROOT_result_review_SHA256": PRODUCER_RESULT_REVIEW_SHA,
        "independent_native_contract_audit_approved": True,
    }
    require(
        all(ready[key] == policy[key] == expected for key, expected in expectations.items()),
        "Separate independent audit release binds original actual producer expectations",
    )
    producer = packet(
        PRODUCER.name,
        PRODUCER_SHA,
        PRODUCER_COUNTS,
        "a13-d4-s4-native-contract-inventory-manifest-v2",
        "receipt",
    )
    require(
        producer["manifest_inclusive_retention_checked_before_sealing"] is True
        and producer["manifest_inclusive_owned_file_count"] == PRODUCER_COUNTS[0] + 1
        and producer["row_id"] == ROW_ID
        and producer["completed_selector_manifest_SHA256"] == SELECTOR_SHA
        and producer["completed_selector_complete_counts"] == SELECTOR_COUNTS,
        "Full actual producer retention and original selector identity",
    )
    old_ready = read(bind(PRODUCER_READY, PRODUCER_READY_SHA))
    require(
        old_ready["schema"] == "root-a13-d4-s4-native-contract-inventory-READY-v2"
        and old_ready["author_method_SHA256"] == PRODUCER_AUTHORS
        and old_ready["output"] == PRODUCER.relative_to(ROOT).as_posix()
        and old_ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and old_ready["independent_peer_report_SHA256"]
        == "fa41d1d350658b8d919fc60566fa4c832352863d29d38c596da41c81b2f7ff71",
        "Unchanged independently reviewed producer release",
    )
    for name, expected in PRODUCER_AUTHORS.items():
        require(
            producer["frozen_inputs"][(RESEARCH / name).relative_to(ROOT).as_posix()] == expected,
            "Every original producer author expected input retained",
        )
        bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "contract_a13_d4_s4_native_inventory_v2.py"],
        old_ready["existing_new_code_cache_SHA256"],
        old_ready["absent_new_code_cache_paths"],
    )
    bind(PRODUCER_RESULT_REVIEW, PRODUCER_RESULT_REVIEW_SHA)
    producer_result_witness()
    return original_manifest


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
ACTIVE_WIDTHS = [38, 40]
LEAF_MAX_ROWS, LEAF_MAX_WIRES = 1_000_000, 32768
FIRST_VALUE, FIRST_ARGS = 8, [0, 4]
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


def native_audit_witness():
    summary = read(NATIVE_AUDIT / "summary.json")
    outcome = read(NATIVE_AUDIT / "completion_outcome.json")
    review = read(NATIVE_AUDIT_RESULT)
    require(outcome == {**summary, "failed": False}, "Exact completed independent audit pair")
    require(
        summary["schema"] == "a13-d4-s4-native-independent-audit-summary-v1"
        and summary["completed"] is summary["passed"] is True
        and summary["budget_censored"] is False
        and summary["producer_manifest_SHA256"] == PRODUCER_SHA
        and summary["producer_complete_counts"] == PRODUCER_COUNTS
        and summary["all8_completed_owner_maps_and_owned_inventories_retained"] is True
        and summary["all240_native_cells_and_six_ordered_hulls_independently_audited"] is True
        and summary["fixed_cell_slots"] == 240
        and summary["occupied_cell_slots"] == 224
        and summary["ordered_shared_MUL_count"] == 6,
        "Actual independent native induction, not a primary-only width claim",
    )
    require(
        review["schema"] == "root-a13-d4-s4-native-independent-audit-actual-owned-result-review-v1"
        and review["passed"] is True
        and review["manifest_SHA256"] == NATIVE_AUDIT_SHA
        and review["complete_counts"] == NATIVE_AUDIT_COUNTS
        and review["inclusive_owned_files"] == 38
        and review["all_new_owned_hashes_and_complete_inventory_verified"] is True
        and review["all_six_complete_independent_scientific_members_equal_original_producer"] is True
        and review["independent_all240_integer_cell_and_six_minimum_width_audit_completed"] is True
        and review["actual_leaf_ABI_phase_cost_source_G2_adoption_or_advantage_transfer"] is False
        and review["fixture_credit"] == 0,
        "Independent audited contract only; actual leaf proof remains new work",
    )
    for key in ("full_G2", "adoption", "cost_transfer", "quantum_advantage",
                "gate_emission_authorized", "financial_gate_emission_authorized"):
        require(summary[key] is False, "Original independent audit grants no leaf release")
    path = NATIVE_AUDIT / "independent_six_ordered_MUL_contracts.json"
    require(_FROZEN[path.relative_to(ROOT).as_posix()] == NATIVE_CONTRACT_SHA,
            "Original independent-owned contract expected hash")
    contracts = read(path)
    require(contracts["schema"] == "a13-d4-s4-six-ordered-MUL-contracts-v1"
            and len(contracts["contracts"]) == 6
            and contracts["gate_leaf_authoring_or_execution_authorized"] is False,
            "All six original contracts remain independent premises")
    matches = [x for x in contracts["contracts"] if x["value"] == FIRST_VALUE]
    require(len(matches) == 1, "One exact second ordered v8 contract")
    contract = matches[0]
    require(contract["ordered_args"] == FIRST_ARGS
            and contract["complete_ordered_ABI_signature"]["ordered_active_signed_widths"] == ACTIVE_WIDTHS
            and contract["runtime_operand_swap_or_width_switch"] is False
            and contract["hull_covers_both_cases_every_reachable_segment_class"] is True,
            "Audited ordered38x40, no sampling, swapping or runtime dispatch")
    budget()
    return contract


HELD_V1_AUTHORS = {'prototype_a13_d4_s4_first_signed_leaf_v1.py': 'f04584bf19cd99b0797fde22f3d98f00cbecfd2b4727fe6ef24b167302c5ea5b', 'build_a13_d4_s4_first_signed_leaf_v1.py': '3d2bdc68aa39457faeb13900d3d83f666d5f92c49446ed7a2adec087912aa764', 'A13_D4_S4_FIRST_SIGNED_LEAF_IMPLEMENTATION_PREFLIGHT_V1.md': 'cfba46ddfa571a7d306e9c776356078281e31ab8a4b631e9de656a069c9126c1', 'a13_d4_s4_first_signed_leaf_implementation_preflight_v1.json': '4cba71e49a5d4c87c7dd640d690ba916711cd1910f64f6c56005cecc8545a47e'}
HELD_V1_QA = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_AUTHOR_STATIC_QA_run001.json"
HELD_V1_QA_SHA = "fe2ace5c78370788309a206a7d61aee04cf52f0619db7ad2d769c67381da0350"
HELD_V1_PEER = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_INDEPENDENT_STATIC_PEER_run001.json"
HELD_V1_PEER_SHA = "f8d3b8ef6eb0368db5c2b491f612aa0f77296204a60d8007591536e6e0ded33b"
HELD_V1_READY = ROOT / ".context/A13_D4_S4_FIRST_SIGNED_LEAF_ROOT_READY_run001.json"
HELD_V1_OUTPUT = PROGRAM / "A13_d4_s4_first_signed_leaf_run001"
HELD_V1_INPUTS = tuple((RESEARCH / name, pin) for name, pin in HELD_V1_AUTHORS.items()) + (
    (HELD_V1_QA, HELD_V1_QA_SHA), (HELD_V1_PEER, HELD_V1_PEER_SHA))


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


def second_leaf_admission(ready_sha):
    require("PYTHONINTMAXSTRDIGITS" not in os.environ
            and "int_max_str_digits" not in sys._xoptions
            and sys.flags.int_max_str_digits == sys.get_int_max_str_digits()
            == sys.int_info.default_max_str_digits == 4300,
            "Pinned4300 startup/effective/default digit policy without any overrides")
    original = audit_admission(ready_sha)
    ready, policy = read(READY), read(PREFLIGHT)
    fixed = {
        "native_audit_manifest_SHA256": NATIVE_AUDIT_SHA,
        "native_audit_complete_counts": NATIVE_AUDIT_COUNTS,
        "native_audit_READY_SHA256": NATIVE_AUDIT_READY_SHA,
        "native_audit_author_SHA256": NATIVE_AUDIT_AUTHORS,
        "native_audit_ROOT_result_review_SHA256": NATIVE_AUDIT_RESULT_SHA,
        "native_contract_original_expected_SHA256": NATIVE_CONTRACT_SHA,
        "ordered_active_signed_widths": ACTIVE_WIDTHS,
        "word_fraction_product_residue_bits": [72, 40, 144, 78],
        "selected_value": FIRST_VALUE,
        "ordered_args": FIRST_ARGS,
        "native_logical_forward_inverse_cases": [64, 64],
        "native_physical_forward_inverse_sweeps": [1, 1],
        "scalar_toy_widths": [1, 4],
        "scalar_toy_native_fraction_residue_bits": [8, 4, 12],
        "scalar_toy_ordered_pairs": 900,
        "negative_scalar_or_promise_controls": 4,
        "native_alternative_arrays": 0,
        "completed_owner_packet_literals": COMPLETED_OWNER_EXPECTATIONS,
        "leaf_abort_rows_wires": [LEAF_MAX_ROWS, LEAF_MAX_WIRES],
    }
    require(all(ready[k] == policy[k] == v for k, v in fixed.items()),
            "Independent completed audit and fixed standalone preregistration")
    require(ready["standalone_signed_leaf_approved"] is True
            and policy["new_second_standalone_signed_leaf"] is True
            and policy["new_integer_native_range_induction"] is False
            and policy["source_substitution_authorized"] is False
            and ready["gate_emission_scope"] == 'one_standalone_ordered_v8_signed38x40_complete_product78_explicit_sign38_to72_leaf',
            "One new leaf only, no repeated native inventory or financial source release")
    audit = packet(NATIVE_AUDIT.name, NATIVE_AUDIT_SHA, NATIVE_AUDIT_COUNTS,
                   "a13-d4-s4-native-independent-audit-manifest-v1", "receipt")
    old_ready = read(bind(NATIVE_AUDIT_READY, NATIVE_AUDIT_READY_SHA))
    require(old_ready["schema"] == "root-a13-d4-s4-native-independent-audit-READY-v1"
            and old_ready["author_method_SHA256"] == NATIVE_AUDIT_AUTHORS,
            "Original independent audit release remains immutable")
    for filename, expected in NATIVE_AUDIT_AUTHORS.items():
        require(audit["frozen_inputs"][(RESEARCH / filename).relative_to(ROOT).as_posix()] == expected,
                "All original audit authors keep original expected bytes")
        bind(RESEARCH / filename, expected)
    code_caches([RESEARCH / "audit_a13_d4_s4_native_inventory_v1.py"],
                old_ready["existing_new_code_cache_SHA256"], old_ready["absent_new_code_cache_paths"])
    bind(NATIVE_AUDIT_RESULT, NATIVE_AUDIT_RESULT_SHA)
    for filename, expected in HELD_DESIGN_AUTHORS.items():
        bind(RESEARCH / filename, expected)
    bind(HELD_DESIGN_PEER, HELD_DESIGN_PEER_SHA)
    code_caches([RESEARCH / "a13_d4_s4_contracted_mul_design_v1.py"],
                ready["held_design_existing_code_cache_SHA256"],
                ready["held_design_absent_code_cache_paths"])
    contract = native_audit_witness()
    require(ready["complete_ordered_ABI_signature"] == policy["complete_ordered_ABI_signature"]
            == contract["complete_ordered_ABI_signature"], "Entire audited ABI, not just two widths")
    require(policy["helper_SHA256"] == ready["author_method_SHA256"][HELPER.name]
            and policy["helper_namespace_AST_SHA256"] == ready["helper_namespace_AST_SHA256"],
            "Externally frozen exact new helper source and AST namespace")
    admit_held_v1(ready, policy)
    return original, contract


def execute_new_helper_namespace():
    global _HASH_WORK
    actual = canonical(HELPER, fresh=True)
    expected = _FROZEN[actual.relative_to(ROOT).as_posix()]
    before = fingerprint(actual)
    require(before[2] <= 1 << 20, "Bounded new helper source")
    raw = actual.read_bytes()
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2]
            and fingerprint(actual) == before and hashlib.sha256(raw).hexdigest() == expected,
            "New helper uses fresh exact source bytes, no existing pyc execution")
    tree = ast.parse(raw)
    require(hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()
            == read(PREFLIGHT)["helper_namespace_AST_SHA256"], "Fixed entire helper AST")
    namespace = {"__name__": "released_second_v8_signed_leaf_helper", "__file__": str(HELPER)}
    budget()
    exec(compile(tree, str(HELPER), "exec", dont_inherit=True), namespace)
    budget()
    require(namespace["W"] == 72 and namespace["F"] == 40 and namespace["RESIDUE_BITS"] == 78
            and namespace["LOWERING_ROW_ID"] == LEAF_LOWERING_ROW_ID
            and namespace["EXPECTED_ORDERED_ACTIVE_WIDTHS"] == ACTIVE_WIDTHS
            and namespace["CCX_PHASE_MACRO"] == EXPECTED_CCX_PHASE_MACRO,
            "One pinned new helper namespace only, no original module imports")
    return namespace


def current_controller_code_guard():
    """Compare loaded functions with exact admitted source compilation without executing it."""
    global _HASH_WORK
    path = canonical(AUTHOR, fresh=True)
    before = fingerprint(path)
    require(before[2] <= 8 << 20, "Bounded loaded-controller source guard")
    raw = path.read_bytes()
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2]
            and fingerprint(path) == before
            and hashlib.sha256(raw).hexdigest() == _FROZEN[path.relative_to(ROOT).as_posix()],
            "Loaded-controller guard compiles exact admitted source bytes")
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


def save_and_read_actual_rows(gates):
    global _HASH_WORK
    require(sys.byteorder == "little" and gates.typecode == "i" and gates.itemsize == 4
            and len(gates) % 4 == 0 and len(gates) // 4 <= LEAF_MAX_ROWS,
            "Native complete little-endian signed-int32 Nx4 array")
    path = OUTPUT / "native_gate_rows.i32"
    size = len(gates) * 4
    current = inventory(OUTPUT)
    require(not path.exists() and len(current) + 2 <= MAX_OWN_FILES
            and sum(p.stat().st_size for p in current) + size <= MAX_OWN_BYTES,
            "Binary native array reserves final manifest and all owned bytes")
    view = memoryview(gates).cast("B")
    with path.open("xb") as stream:
        for start in range(0, size, 1 << 20):
            budget()
            piece = view[start:start + (1 << 20)]
            require(stream.write(piece) == len(piece), "Exact native binary writes")
    del view
    expected = digest(path, fresh=True)
    before = fingerprint(path)
    actual, state, total = array("i"), hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            budget()
            _HASH_WORK += len(block)
            total += len(block)
            require(_HASH_WORK <= MAX_HASH_WORK and total <= size and len(block) % 16 == 0,
                    "Complete stable bounded array reread")
            state.update(block)
            actual.frombytes(block)
    require(total == size == before[2] and fingerprint(path) == before
            and state.hexdigest() == expected and actual.typecode == "i" and actual.itemsize == 4,
            "Independent consumer receives actual saved array, not builder object")
    budget()
    return actual, expected


def independent_whole_row_proof(rows, descriptor):
    """Consume every actual row using a checked cursor and independent allocation ledger."""
    require(len(rows) % 4 == 0 and 0 < len(rows) // 4 <= LEAF_MAX_ROWS,
            "Complete finite actual gate row words")
    position, allocated = 0, 216
    def emit(*wires):
        nonlocal position
        budget()
        require(1 <= len(wires) <= 3 and len(set(wires)) == len(wires)
                and all(type(w) is int and 0 <= w < allocated for w in wires),
                "Independent distinct allocated native gate wires")
        expected = (len(wires), *wires, *([0] * (3 - len(wires))))
        require(tuple(rows[position * 4:position * 4 + 4]) == expected,
                "Every actual native row matches independently derived recurrence")
        position += 1
    def allocate(n):
        nonlocal allocated
        budget()
        require(allocated + n <= LEAF_MAX_WIRES, "Independent allocated-wire cap")
        wires = list(range(allocated, allocated + n))
        allocated += n
        return wires
    columns = [[] for _ in range(78)]
    expected_partials, correction = [], 0
    # A signed coefficient is -1 only at its active sign bit; this is not helper.signed_planes.
    for bbit in range(40):
        for abit in range(38):
            budget()
            column = abit + bbit
            if column >= 78:
                continue
            sign_a, sign_b = (-1 if abit == 37 else 1), (-1 if bbit == 39 else 1)
            complemented = sign_a * sign_b < 0
            wire = allocate(1)[0]
            if complemented:
                emit(wire)
                correction -= pow(2, column)
            emit(abit, 72 + bbit, wire)
            columns[column].append(wire)
            expected_partials.append({"a_bit": abit, "b_bit": bbit, "column": column,
                                      "negative": complemented, "wire": wire})
    correction %= pow(2, 78)
    expected_fixed = []
    for column in range(78):
        budget()
        if correction // pow(2, column) % 2:
            wire = allocate(1)[0]
            emit(wire)
            columns[column].append(wire)
            expected_fixed.append({"column": column, "wire": wire})
    expected_layers = []
    while any(len(values) >= 3 for values in columns):
        later = [[] for _ in range(78)]
        triples = []
        for column in range(78):
            budget()
            values = columns[column]
            full = len(values) // 3
            for triple in range(full):
                x, y, z = values[3 * triple:3 * triple + 3]
                summation = allocate(1)[0]
                emit(x, summation); emit(y, summation)
                carry = None
                if column != 77:
                    carry = allocate(1)[0]
                    emit(x, y, carry); emit(summation, z, carry)
                    later[column + 1].append(carry)
                emit(z, summation)
                later[column].append(summation)
                triples.append({"column": column, "inputs": [x, y, z],
                                "sum": summation, "carry": carry})
            later[column].extend(values[3 * full:])
        columns = later
        expected_layers.append(triples)
    left, right, product = allocate(78), allocate(78), allocate(78)
    for column in range(78):
        if len(columns[column]) >= 1:
            emit(columns[column][0], left[column])
        if len(columns[column]) == 2:
            emit(columns[column][1], right[column])
    propagate, carry = allocate(78), allocate(79)
    for bit in range(78):
        emit(left[bit], propagate[bit]); emit(right[bit], propagate[bit])
        emit(left[bit], right[bit], carry[bit + 1])
        if bit != 0:
            emit(propagate[bit], carry[bit], carry[bit + 1])
        emit(propagate[bit], product[bit])
        if bit != 0:
            emit(carry[bit], product[bit])
    compute_end = position
    for bit in range(72):
        emit(product[40 + bit if bit < 38 else 77], 144 + bit)
    for offset in range(compute_end - 1, -1, -1):
        budget()
        original = tuple(rows[4 * offset:4 * offset + 4])
        require(tuple(rows[4 * position:4 * position + 4]) == original,
                "Entire actual inverse is literal reversed compute; no omitted private wire")
        position += 1
    require(position == len(rows) // 4 and allocated == descriptor["qubits"],
            "Every actual row and every allocated wire consumed exactly")
    expected_recipe = {"partials": expected_partials, "correction": correction,
                       "fixed": expected_fixed, "CSA_layers": expected_layers,
                       "final_columns": columns, "left": left, "right": right,
                       "product": product, "propagate": propagate, "carry": carry,
                       "output_source_bits": list(range(40, 78)) + [77] * 34}
    require(descriptor["recipe"] == expected_recipe
            and descriptor["args"] == [list(range(72)), list(range(72, 144))]
            and descriptor["outs"] == [list(range(144, 216))]
            and descriptor["compute_gate_rows"] == [0, compute_end]
            and descriptor["copy_gate_rows"] == [compute_end, compute_end + 72]
            and descriptor["inverse_gate_rows"] == [compute_end + 72, position]
            and descriptor["gate_rows"] == position,
            "Full recipe, ports and compute/copy/inverse boundaries independently reconstructed")
    require(descriptor["row_id"] == LEAF_LOWERING_ROW_ID and descriptor["source_row_id"] == ROW_ID and descriptor["value"] == FIRST_VALUE
            and descriptor["ordered_args"] == FIRST_ARGS
            and descriptor["spec"]["active_operand_bits"] == ACTIVE_WIDTHS
            and descriptor["spec"]["product_width"] == 78
            and descriptor["dirty_output_XOR"] is True
            and descriptor["private_workspace_zero_entry_exit"] is True
            and descriptor["low_product_columns_discarded_before_carry"] is False,
            "Standalone full72 signed144/floor40 promises and complete low carry")
    require(descriptor["op"] == "mul" and descriptor["params"] == {}
            and descriptor["schema"] == "a13-d4-s4-second-ordered-signed-leaf-min78-explicit-sign-descriptor-v1"
            and descriptor["spec"] == {
                "width": 72, "fraction_bits": 40, "product_width": 78,
                "active_operand_bits": [38, 40],
                "input_contract": {"signed_operand_bits": [38, 40]},
                "variant": "retained-CSA-ripple-product78-sign38-to72-v1"}
            and descriptor["full_signed_semantic_product_bits"] == 144
            and descriptor["product_modulus_bits"] == 78
            and descriptor["input_preserved"] is True
            and descriptor["actual_cost_or_source_transfer_claim"] is False,
            "Complete original full72/F40 input/output ABI and standalone descriptor")
    return {"passed": True, "actual_rows_consumed": position, "allocated_wires": allocated,
            "compute_copy_inverse_rows": [compute_end, 72, compute_end],
            "independent_signed_coefficients_and_complement_correction": True,
            "all_CSA_disjoint_majority_and_full78_ripple_structurally_matched": True,
            "full72_copy_and_all_private_literal_inverse": True,
            "producer_builder_or_plane_method_called": False,
            "all34_high_output_CX_sources_equal_computed_product77": True,
            "universal_signed_floor_sign_extension": minimum78_universal_floor_sign_extension_proof(descriptor)}


def validate_typed_word(raw, width):
    require(type(raw) is int and 0 <= raw < (1 << 72), "Concrete unsigned full72 word")
    active_sign = (raw >> (width - 1)) & 1
    required_upper = (1 << (72 - width)) - 1 if active_sign else 0
    require(raw >> width == required_upper, "Full72 active signed sign-extension promise")


def native_corpus_and_oracles():
    """Evaluate only preregistered formulas after ROOT admission; duplicates are retained."""
    wa, wb = ACTIVE_WIDTHS
    amin, amax = -(1 << (wa - 1)), (1 << (wa - 1)) - 1
    bmin, bmax = -(1 << (wb - 1)), (1 << (wb - 1)) - 1
    pa = 1 << 20; pb = 1 << 20
    candidates = [(0, 0), (0, bmin), (amin, 0), (-1, -1), (-1, bmax),
                  (amax, -1), (amin, bmin), (amin, bmax), (amax, bmin), (amax, bmax),
                  (pa, pb), (pa - 1, pb + 1), (pa + 1, pb - 1),
                  (-pa, pb), (-pa - 1, pb + 1), (-pa + 1, pb - 1)]
    mask = (1 << 72) - 1
    alternating = sum(1 << bit for bit in range(0, 72, 2))
    dirty = [0, mask, alternating, mask ^ alternating]
    cases = []
    for pair_id, (a, b) in enumerate(candidates):
        budget()
        require(amin <= a <= amax and bmin <= b <= bmax,
                "Every fixed NEW v8 pair satisfies its promise; no clipping or substitution")
        raw_a, raw_b = a & mask, b & mask
        validate_typed_word(raw_a, wa); validate_typed_word(raw_b, wb)
        direct = (a * b // (1 << 40)) & mask
        # A second unsigned72 oracle uses explicit full-word sign correction, not active planes.
        sa, sb = raw_a // (1 << 71), raw_b // (1 << 71)
        full_unsigned = raw_a * raw_b
        signed_residue = (full_unsigned - sa * (1 << 72) * raw_b
                          - sb * (1 << 72) * raw_a + sa * sb * (1 << 144)) % (1 << 144)
        independent = (signed_residue // (1 << 40)) & mask
        require(direct == independent, "Independent direct signed and unsigned-correction scalar oracles")
        for dirty_id, word in enumerate(dirty):
            cases.append({"id": f"pair{pair_id:02d}_dirty{dirty_id}", "signed_a": a, "signed_b": b,
                          "raw_a": raw_a, "raw_b": raw_b, "dirty": word,
                          "expected_output": word ^ direct})
    require(len(cases) == 64, "All fixed16 pairs times4 dirty targets, including duplicates")
    return cases


def independent_native_batch(rows, qubits, cases):
    require(len(cases) == 64 and 216 <= qubits <= LEAF_MAX_WIRES, "One fixed64-case native batch")
    state = [0] * qubits
    expected = [0] * qubits
    for index, case in enumerate(cases):
        budget()
        for bank, word in ((0, case["raw_a"]), (72, case["raw_b"]), (144, case["dirty"])):
            for bit in range(72):
                state[bank + bit] |= ((word >> bit) & 1) << index
        for bank, word in ((0, case["raw_a"]), (72, case["raw_b"]), (144, case["expected_output"])):
            for bit in range(72):
                expected[bank + bit] |= ((word >> bit) & 1) << index
    initial = state.copy()
    for reverse in (False, True):
        sequence = range(len(rows) // 4 - 1, -1, -1) if reverse else range(len(rows) // 4)
        for index in sequence:
            budget()
            kind, x, y, z = rows[4 * index:4 * index + 4]
            if kind == 1:
                state[x] ^= (1 << 64) - 1
            elif kind == 2:
                state[y] ^= state[x]
            else:
                require(kind == 3, "Only actual X/CX/CCX array rows")
                state[z] ^= state[x] & state[y]
        require(state == (initial if reverse else expected),
                "All allocated wires: full inputs, arbitrary dirty XOR and complete zero private workspace")
    return {"passed": True, "logical_forward_cases": 64, "logical_inverse_cases": 64,
            "physical_full_forward_sweeps": 1, "physical_full_inverse_sweeps": 1,
            "all_allocated_wires_compared_including_unused_carries": True,
            "finite_batch_is_not_universal_ABI_proof": True, "fixture_credit": 0}


def independent_toy_and_negative_controls():
    count = 0
    for wa in range(1, 5):
        for wb in range(1, 5):
            for a in range(1 << wa):
                for b in range(1 << wb):
                    budget()
                    signed_a = a if a < (1 << (wa - 1)) else a - (1 << wa)
                    signed_b = b if b < (1 << (wb - 1)) else b - (1 << wb)
                    oracle = (signed_a * signed_b // 16) % 256
                    weighted, complemented, correction = 0, 0, 0
                    for j in range(wa):
                        for i in range(wb):
                            weight = (1 << (j + i)) * (-1 if j == wa - 1 else 1) * (-1 if i == wb - 1 else 1)
                            term = ((a >> j) & 1) * ((b >> i) & 1)
                            weighted += weight * term
                            if weight < 0:
                                complemented += -weight * (1 - term); correction += weight
                            else:
                                complemented += weight * term
                    product_bits = wa + wb
                    residue = (complemented + correction) % (1 << product_bits)
                    computed_product_sign = (residue >> (product_bits - 1)) & 1
                    if product_bits > 4:
                        quotient_bits = product_bits - 4
                        delivered = residue // 16
                        if computed_product_sign:
                            delivered += 256 - (1 << quotient_bits)
                    else:
                        # L<=F: floor(P/16) is0 or-1. Zero product has computed sign0.
                        delivered = 255 if computed_product_sign else 0
                    require(weighted == signed_a * signed_b
                            and -(1 << (product_bits - 1)) <= weighted < (1 << (product_bits - 1))
                            and delivered == oracle,
                            "Complete toy product-L carries and computed-sign extension including L<=F")
                    count += 1
    require(count == 900, "Exactly900 fixed ordered scalar toy pairs, no toy gate arrays")
    mask = (1 << 72) - 1
    a, b = -1, 1
    correct = (a * b // (1 << 40)) & mask
    short = ((a * b) % (1 << sum(ACTIVE_WIDTHS))) // (1 << 40)
    require(short != correct, "Fixed bad-short-modulus method is rejected")
    a, b = (1 << 21) - 1, (1 << 20) + 1
    high = sum(1 << (j + i) for j in range(38) for i in range(40)
               if j + i >= 40 and (a >> j) & 1 and (b >> i) & 1)
    correct_carry = (a * b) // (1 << 40)
    require(high // (1 << 40) != correct_carry, "Fixed dropped-low-carry method is rejected")
    invalid_a, invalid_b = (1 << ACTIVE_WIDTHS[0]) - 1, 1
    validate_typed_word(invalid_b, ACTIVE_WIDTHS[1])
    rejected = False
    try:
        validate_typed_word(invalid_a, ACTIVE_WIDTHS[0])
    except ValueError as error:
        require(str(error) == "Full72 active signed sign-extension promise",
                "Only exact typed-promise failure, never budget censor/control credit")
        rejected = True
    require(rejected, "Invalid sign extension is never a valid logical case")
    # Fourth preregistered control: two corrupt metadata plans, no alternate gate array.
    fixed_product = -1 * 1
    fixed_correct = (fixed_product // (1 << 40)) & mask
    fixed_residue = fixed_product % (1 << 78)
    low38 = fixed_residue // (1 << 40)
    computed_sign = (fixed_residue >> 77) & 1
    extended = low38 + computed_sign * ((1 << 72) - (1 << 38))
    require(extended == fixed_correct and low38 != fixed_correct
            and (extended ^ (1 << 38)) != fixed_correct,
            "At fixed -1 times1, missing high extension and flipped high bit both fail full72 map")
    positive_plan = independent_product78_output_sources(list(range(40, 78)) + [77] * 34)
    corrupt_plan = positive_plan.copy()
    corrupt_plan[38] = None
    rejection_records = []
    for label, plan in (("omitted-high34", positive_plan[:38]),
                        ("corrupted-first-high-sign-copy", corrupt_plan)):
        budget()
        try:
            independent_product78_output_sources(plan)
        except HighSignCopyReject as error:
            require(str(error) == "MIN78_HIGH_SIGN_COPY_PLAN", "Only dedicated high-copy rejection")
            rejection_records.append({"mutation": label, "exact_structural_rejection": True})
        else:
            raise ValueError("Fixed malformed high-sign-copy control unexpectedly accepted")
    require(len(rejection_records) == 2, "Both fixed variants of fourth control rejected")
    return {"passed": True, "scalar_toy_ordered_pairs": count, "toy_native_fraction_residue_bits": [8, 4, 12],
            "toy_actual_product_bits": "L=wa+wb, all low columns and carries retained",
            "toy_L_less_equal_F_branch_computed_product_sign_to_all8": True,
            "operand_sign_XOR_is_not_sign_authority_at_zero": True,
            "controls": [
                {"name": "bad-short-modulus", "a": -1, "b": 1, "bad_output": short,
                 "correct_output": correct, "bad_method_rejected": True},
                {"name": "dropped-low-carry", "a": a, "b": b,
                 "bad_output": high // (1 << 40), "correct_output": correct_carry, "bad_method_rejected": True},
                {"name": "invalid-sign-extension", "raw_a": invalid_a, "raw_b": invalid_b,
                 "promise_rejected_before_any_logical_case": True},
                {"name": "omitted-or-corrupted-output-high-sign-copies", "a": -1, "b": 1,
                 "correct_output": fixed_correct, "bad_omitted_output": low38,
                 "bad_corrupted_output": extended ^ (1 << 38),
                 "structural_rejections": rejection_records, "bad_method_rejected": True}],
            "alternative_native_or_toy_gate_arrays_constructed": 0,
            "expected_control_rejections_are_not_actual_run_failures": True, "fixture_credit": 0}


def independent_absolute_ccx_phase():
    """Exact integer ring Z[z]/(z^4+1) with denominator2^k; no floating approximation."""
    def multiply_z(v, power):
        result = [0, 0, 0, 0]
        for degree, coefficient in enumerate(v):
            index = degree + power
            quotient, residue = divmod(index, 4)
            result[residue] += (-1 if quotient & 1 else 1) * coefficient
        return tuple(result)
    def half_sqrt_two(v):
        # 1/sqrt2=(z-z^3)/2 at z=exp(i*pi/4); caller increments denominator exponent.
        left, right = multiply_z(v, 1), multiply_z(v, 3)
        return tuple(a - b for a, b in zip(left, right, strict=True))
    columns = []
    for basis in range(8):
        budget()
        state = [(0, 0, 0, 0)] * 8
        state[basis] = (1, 0, 0, 0)
        denominator_exponent = 0
        for event in EXPECTED_CCX_PHASE_MACRO:
            budget()
            kind, wires = event[0], event[1:]
            if kind == "CX":
                control, target = wires
                following = [(0, 0, 0, 0)] * 8
                for index in range(8):
                    dest = index ^ (1 << target) if index & (1 << control) else index
                    following[dest] = state[index]
                state = following
            elif kind in ("T", "TD"):
                target = wires[0]
                state = [multiply_z(v, 1 if kind == "T" else -1)
                         if index & (1 << target) else v for index, v in enumerate(state)]
            else:
                require(kind == "H", "Exact original15-event seven-T macro")
                target = wires[0]
                following = [(0, 0, 0, 0)] * 8
                for index in range(8):
                    if index & (1 << target):
                        continue
                    other = index | (1 << target)
                    u, v = state[index], state[other]
                    following[index] = half_sqrt_two(tuple(x + y for x, y in zip(u, v, strict=True)))
                    following[other] = half_sqrt_two(tuple(x - y for x, y in zip(u, v, strict=True)))
                state = following; denominator_exponent += 1
        expected_basis = basis ^ 4 if basis & 1 and basis & 2 else basis
        expected = [(0, 0, 0, 0)] * 8
        expected[expected_basis] = (1 << denominator_exponent, 0, 0, 0)
        require(state == expected, "All eight CCX columns equal ideal permutation with absolute global phase1")
        columns.append({"input_basis": basis, "output_basis": expected_basis,
                        "denominator_exponent": denominator_exponent,
                        "cyclotomic_integer_column": state})
    require(sum(e[0] in ("T", "TD") for e in EXPECTED_CCX_PHASE_MACRO) == 7,
            "Exactly seven paid T/TD events per ideal CCX")
    return {"passed": True, "basis_columns": columns, "absolute_unit_global_phase": True,
            "relative_phase_or_approximate_CCX_used": False, "exact_ring": "Z[z]/(z^4+1), z=exp(i*pi/4)",
            "universal_promised_span_and_reference_entanglement_follow_by_linearity": True,
            "producer_or_old_phase_fixture_called": False, "fixture_credit": 0}


def independent_standalone_resources(rows, qubits):
    count = [0, 0, 0, 0]
    t_layers, all_layers = [0] * qubits, [0] * qubits
    events = 0
    for offset in range(0, len(rows), 4):
        budget()
        kind, a, b, c = rows[offset:offset + 4]
        require(kind in (1, 2, 3), "Every native resource row accounted")
        count[kind] += 1
        if kind == 3:
            mapping = (a, b, c)
            macro = [(event[0], tuple(mapping[wire] for wire in event[1:]))
                     for event in EXPECTED_CCX_PHASE_MACRO]
        else:
            macro = [("X", (a,))] if kind == 1 else [("CX", (a, b))]
        for event, touched in macro:
            budget()
            require(len(set(touched)) == len(touched) and all(0 <= wire < qubits for wire in touched),
                    "Complete actual macro resource operand domain")
            paid_t = int(event in ("T", "TD"))
            t_depth = max(t_layers[wire] for wire in touched) + paid_t
            all_depth = max(all_layers[wire] for wire in touched) + 1
            for wire in touched:
                t_layers[wire], all_layers[wire] = t_depth, all_depth
            events += 1
    return {"schema": "a13-first-signed-leaf-actual-standalone-resources-v1",
            "native_gate_rows": len(rows) // 4, "X": count[1], "CX": count[2], "CCX": count[3],
            "T": 7 * count[3], "Clifford_T_macro_events": events,
            "ASAP_T_depth": max(t_layers), "ASAP_Clifford_T_depth": max(all_layers),
            "allocated_qubits": qubits, "includes_forward_full72_dirty_XOR_and_complete_inverse": True,
            "caller_argument_copies_included": False, "caller_copy_obligation_remains": True,
            "whole_clean_function_source_capped_schedule_or_original_G2_cost": False,
            "old_cost_estimate_or_profile_used": False, "fixture_credit": 0}


def reread_new_owned_json(filename, expected):
    """A within-run output hash binds actual producer bytes for the distinct consumer."""
    global _HASH_WORK
    path = canonical(OUTPUT / filename, fresh=True)
    require(path.parent == OUTPUT, "Only new standalone owned JSON")
    before = fingerprint(path)
    require(before[2] <= 8 << 20, "Bounded new scientific descriptor JSON")
    raw = path.read_bytes()
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2]
            and fingerprint(path) == before and hashlib.sha256(raw).hexdigest() == expected,
            "Fresh actual saved scientific JSON without changing original expectations")
    budget()
    return json.loads(raw)


def repeated_metadata_witnesses():
    for witness in (failed_material_witness, selection_failure_witnesses,
                    prior_inventory_failure_witness, selector_result_witness,
                    producer_result_witness, native_audit_witness, held_v1_witness):
        budget()
        witness()


class HighSignCopyReject(ValueError):
    """Dedicated fixed structural-control failure, never a budget exception."""

def independent_product78_output_sources(plan):
    expected = list(range(40, 78)) + [77] * 34
    if plan != expected:
        raise HighSignCopyReject("MIN78_HIGH_SIGN_COPY_PLAN")
    return expected

def minimum78_universal_floor_sign_extension_proof(descriptor):
    require(descriptor["spec"]["active_operand_bits"] == [38, 40]
            and descriptor["spec"]["product_width"] == 78
            and descriptor["output_sign_extension"]
            == {"retained_quotient_bits": 38, "computed_product_sign_bit": 77,
                "high_output_bits": list(range(38, 72))},
            "Fixed v8 minimum78 descriptor and explicit computed-product sign-copy obligation")
    independent_product78_output_sources(descriptor["recipe"]["output_source_bits"])
    require((1 << (38 + 40 - 2)) < (1 << 77), "Every active signed product fits signed78")
    require((1 << (38 + 40 - 2)) > (1 << 76) - 1,
            "Positive min-times-min endpoint requires complete signed78, not signed77")
    return {
        "schema": "a13-v8-minimum78-universal-floor40-sign38-to72-theorem-v1",
        "passed": True,
        "promised_span": "all distinct full72 sign extensions of ordered signed38 and signed40; arbitrary dirty72; private zero; arbitrary reference entanglement",
        "signed_range_argument": "Absolute product<=2^(38+40-2)=2^76<2^77; exact product fits signed78. Positive min-times-min is2^76, outside signed77.",
        "full_residue_argument": "All signed coefficients, negative complemented planes, correction modulo2^78, every low column and full CSA/ripple carry give R=P mod2^78.",
        "nonnegative_case": "For P>=0, R=P and floor(R/2^40)=floor(P/2^40) fits signed38 with computed sign0, including zero.",
        "negative_case": "For P<0, R=P+2^78; floor(R/2^40)=floor(P/2^40)+2^38. Computed product bit77 is1. All34 high copies contribute2^72-2^38, yielding floor(P/2^40) modulo2^72 including negative nonmultiples.",
        "clean_phase_composition": "Each checked output CX preserves computed product/sign and XORs an arbitrary dirty target. Literal reversed compute restores all private zero and both full72 inputs. Fresh exact absolute-phase CCX plus X/CX gives the exact basis operator; linearity tensor reference identity proves arbitrary entanglement on the promise.",
        "no_truncation_toward_zero_or_operand_sign_XOR_shortcut": True,
        "finite_native_and_toy_cases_are_not_the_universal_proof": True,
        "remaining_leaves_repeated_ports_caller_fullsource_G2_adoption_still_open": True,
        "fixture_credit": 0,
    }

def minimum78_unmatched_cost_statement():
    """A metadata scope statement, never a forecast or v6/v8 comparison."""
    return {"schema": "a13-v8-min78-unmatched-resource-comparator-scope-null-v1",
            "selected_value": 8, "ordered_args": [0, 4], "ordered_active_signed_widths": [38, 40],
            "matched_executed_v8_wide_baseline": None, "matched_resource_comparison": None,
            "savings": None, "v6_resource_transfer": False, "cost_forecast": None,
            "second_matching_native_array_emitted": False, "fixture_credit": 0}

def minimum80_completed112_witnesses():
    for prefix, owner, manifest_pin, counts, ready_path, ready_pin, authors, result_path, result_pin in (
        ("completed112", BASELINE112, BASELINE112_SHA, BASELINE112_COUNTS,
         BASELINE112_READY, BASELINE112_READY_SHA, BASELINE112_AUTHORS,
         BASELINE112_RESULT, BASELINE112_RESULT_SHA),
        ("completed112_audit", BASELINE112_AUDIT, BASELINE112_AUDIT_SHA, BASELINE112_AUDIT_COUNTS,
         BASELINE112_AUDIT_READY, BASELINE112_AUDIT_READY_SHA, BASELINE112_AUDIT_AUTHORS,
         BASELINE112_AUDIT_RESULT, BASELINE112_AUDIT_RESULT_SHA),
    ):
        budget()
        require(_FROZEN[key_for(owner / "manifest.json")] == manifest_pin,
                "Original completed112 manifest authority already admitted")
        manifest = read(owner / "manifest.json")
        require([len(manifest[k]) for k in ("files", "frozen_inputs", "external_runtime_inputs")] == counts
                and manifest["passed"] is True and manifest["completed"] is True
                and manifest["budget_censored"] is False,
                "Both complete original112 owner maps and terminal status unchanged")
        release = read(bind(ready_path, ready_pin))
        require(release["author_method_SHA256"] == authors
                and release["output"] == owner.relative_to(ROOT).as_posix()
                and release["root_and_independent_static_reviews_passed"] is True
                and release["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL],
                "Exact saved112 release metadata, never a new scientific permission")
        for name, pin in authors.items():
            bind(RESEARCH / name, pin)
        for key, pin in release["static_review_expected_SHA256"].items():
            require(key.startswith(".context/") and ".." not in Path(key).parts,
                    "Original local reviewed112 author metadata")
            bind(ROOT / key, pin)
        sources = ([RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_v2.py",
                    RESEARCH / "build_a13_d4_s4_first_signed_leaf_v2.py"]
                   if prefix == "completed112" else [RESEARCH / "audit_a13_d4_s4_first_signed_leaf_v2.py"])
        code_caches(sources, release["existing_new_code_cache_SHA256"], release["absent_new_code_cache_paths"])
        result = read(bind(result_path, result_pin))
        require(result["passed"] is True and result["manifest_SHA256"] == manifest_pin
                and result["complete_counts"] == counts
                and result["inclusive_owned_files"] == counts[0] + 1,
                "Completed original112 externally declared ROOT metadata result authority")
    producer = read(BASELINE112 / "manifest.json")
    audit = read(BASELINE112_AUDIT / "manifest.json")
    require(audit["completed_leaf_manifest_SHA256"] == BASELINE112_SHA
            and audit["completed_leaf_complete_counts"] == BASELINE112_COUNTS
            and audit["all10_completed_owner_packet_literals"]
            == COMPLETED_OWNER_EXPECTATIONS + [[BASELINE112.name, BASELINE112_SHA, BASELINE112_COUNTS, "receipt"]]
            and producer["native_audit_manifest_SHA256"] == NATIVE_AUDIT_SHA,
            "Original auditor has exactly its original ten premises, never current11 promotion")
    require(read(BASELINE112 / "native_descriptor.json")["product_modulus_bits"] == 112
            and read(BASELINE112 / "first_leaf_source_contract_binding.json")["exact_ordered_contract"]
            == read(NATIVE_AUDIT / "independent_six_ordered_MUL_contracts.json")["contracts"][0],
            "Original product112 descriptor and complete ordered contract remain unchanged")
    producer_release = read(BASELINE112_READY)
    current_release = read(READY)
    for field in ("held_V1_existing_code_cache_SHA256", "held_V1_absent_code_cache_paths",
                  "held_design_existing_code_cache_SHA256", "held_design_absent_code_cache_paths"):
        require(current_release[field] == producer_release[field],
                "Original completed112 held-source cache authority unchanged")
    audit_release = read(BASELINE112_AUDIT_READY)
    for name, pin in audit_release["held_audit_V1_author_expected_SHA256"].items():
        bind(RESEARCH / name, pin)
    for key, pin in audit_release["held_audit_V1_report_expected_SHA256"].items():
        bind(ROOT / key, pin)
    code_caches([RESEARCH / "audit_a13_d4_s4_first_signed_leaf_v1.py"],
                audit_release["held_audit_V1_existing_code_cache_SHA256"],
                audit_release["held_audit_V1_absent_code_cache_paths"])
    for field in ("held_audit_V1_READY_absent_path", "held_audit_V1_output_absent_path"):
        path = ROOT / audit_release[field]
        require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                "Original independent auditor heldV1 never executed or received a route")
        _ABSENT_RUNTIME.add(path)
    for key, pin in MIN80_PROSPECTUS_PINS.items():
        bind(ROOT / key, pin)
    method_review = read(ROOT / MIN80_METHOD_REVIEW_KEY)
    require(method_review["passed"] is True and method_review["blockers"] == []
            and method_review["mathematical_design_passed"] is True
            and method_review["science_or_controls_executed"] is False
            and method_review["new_READY_created"] is False,
            "Prospectus is mathematical authority only, never prior execution approval")
    budget()

def minimum78_full_optimization_cache_guard(sources, pins, absent_keys):
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


def minimum78_completed80_metadata_witnesses():
    budget()
    current = read(READY)
    old = read(bind(ROOT / COMPLETED80_AUTHORITY["ROOT_READY_path"],
                    COMPLETED80_AUTHORITY["ROOT_READY_SHA256"]))
    policy = read(bind(RESEARCH / "a13_d4_s4_first_signed_leaf_min80_preflight_v1.json",
                       COMPLETED80_AUTHORITY["completed_AUTHOR_SHA256"]["a13_d4_s4_first_signed_leaf_min80_preflight_v1.json"]))
    require(old["schema"] == "root-a13-d4-s4-first-signed-leaf-min80-READY-v1"
            and old["author_method_SHA256"] == COMPLETED80_AUTHORITY["completed_AUTHOR_SHA256"]
            and old["output"] == COMPLETED80.relative_to(ROOT).as_posix()
            and old["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and old["root_and_independent_static_reviews_passed"] is True
            and old["minimum80_complete_owner_packet_literals"] == MIN80_COMPLETED11
            and policy["minimum80_complete_owner_packet_literals"] == MIN80_COMPLETED11
            and old["minimum80_lowering_row_id"] == policy["minimum80_lowering_row_id"]
            == "A13_D4_S4_V6_SIGNED38X42_COMPLETE_PRODUCT80_SIGN40_TO72_V1"
            and old["minimum80_product_and_output_widths"] == [80, 40, 72]
            and old["minimum80_lowering_execution_authorized"] is True,
            "Immutable min80 archival eleven-owner release, never current v8 permissions")
    for name, pin in COMPLETED80_AUTHORITY["completed_AUTHOR_SHA256"].items():
        bind(RESEARCH / name, pin)
    for name, pin in old["static_review_expected_SHA256"].items():
        require(name.startswith(".context/") and ".." not in Path(name).parts,
                "Exact archived min80 local static reviews")
        bind(ROOT / name, pin)
    code_caches([RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_min80_v1.py",
                 RESEARCH / "build_a13_d4_s4_first_signed_leaf_min80_v1.py"],
                old["existing_new_code_cache_SHA256"], old["absent_new_code_cache_paths"])
    minimum78_full_optimization_cache_guard(
        [RESEARCH / "prototype_a13_d4_s4_first_signed_leaf_min80_v1.py",
         RESEARCH / "build_a13_d4_s4_first_signed_leaf_min80_v1.py"],
        current["completed80_all_optimization_existing_cache_SHA256"],
        current["completed80_all_optimization_absent_cache_paths"])
    result = read(bind(ROOT / COMPLETED80_AUTHORITY["ROOT_receipt_path"],
                       COMPLETED80_AUTHORITY["ROOT_receipt_SHA256"]))
    require(result["passed"] is True
            and result["manifest_SHA256"] == COMPLETED80_AUTHORITY["manifest_SHA256"]
            and result["complete_counts"] == COMPLETED80_AUTHORITY["complete_counts"]
            and result["inclusive_owned_files"] == 60,
            "Externally declared ROOT-completed min80 producer metadata only")
    completed = read(COMPLETED80 / "manifest.json")
    require(completed["schema"] == "a13-d4-s4-first-signed-leaf-min80-manifest-v1"
            and completed["completed"] is completed["passed"] is True
            and completed["budget_censored"] is False
            and [len(completed[k]) for k in ("files", "frozen_inputs", "external_runtime_inputs")]
            == COMPLETED80_AUTHORITY["complete_counts"]
            and completed["manifest_inclusive_owned_file_count"] == 60,
            "Completed min80 original three maps/inclusive owned inventory unchanged")
    for field in ("held_V1_existing_code_cache_SHA256", "held_V1_absent_code_cache_paths",
                  "held_design_existing_code_cache_SHA256", "held_design_absent_code_cache_paths"):
        require(current[field] == old[field], "No historical held-source cache refresh")
    for name, pin in MIN78_PROSPECTUS_PINS.items():
        bind(ROOT / name, pin)
    prospective = read(ROOT / MIN78_ROOT_METHOD_REVIEW_KEY)
    require(prospective["passed"] is True and prospective["blockers"] == []
            and prospective["authoring_one_NEW_v8_quartet_and_static_QA_authorized"] is True
            and prospective["science_or_READY_execution_authorized"] is False,
            "v8 ROOT prospectus approval is authoring-only, never actual permission")
    design = read(ROOT / ".context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.json")
    snapshots = design["prospective_current12_owner_snapshots"]
    require(set(snapshots) == {row[0] for row in MIN78_COMPLETED12},
            "Exactly fixed twelve completed owners; pending external min80 auditor unadmitted")
    for name, pin, counts, ownership, schema in MIN78_COMPLETED12:
        saved = snapshots[name]
        owner = canonical(PROGRAM / name)
        actual = read(bind(owner / "manifest.json", pin))
        require(saved["manifest_expected_SHA256"] == pin and saved["complete_counts"] == counts
                and saved["complete_original_declared_maps"]
                == {k: actual[k] for k in ("files", "frozen_inputs", "external_runtime_inputs")}
                and inventory(owner) == _OWN_INVENTORIES[owner],
                "Every complete original literal map and physical owned inventory retained")
        for item in saved["complete_original_physical_owned_inventory"]:
            path = ROOT / item["root_relative_path"]
            require(path in _OWN_INVENTORIES[owner] and path.stat().st_size == item["bytes"]
                    and _FROZEN[key_for(path)] == item["expected_SHA256"],
                    "Every original owned receipt member and manifest remains exact")
    budget()


def minimum78_admission(ready, policy):
    for prefix, manifest_pin, counts, ready_pin, authors, result_pin in (
        ("completed112", BASELINE112_SHA, BASELINE112_COUNTS, BASELINE112_READY_SHA,
         BASELINE112_AUTHORS, BASELINE112_RESULT_SHA),
        ("completed112_audit", BASELINE112_AUDIT_SHA, BASELINE112_AUDIT_COUNTS,
         BASELINE112_AUDIT_READY_SHA, BASELINE112_AUDIT_AUTHORS, BASELINE112_AUDIT_RESULT_SHA),
    ):
        for suffix, expected in (("manifest_SHA256", manifest_pin), ("complete_counts", counts),
                                 ("READY_SHA256", ready_pin), ("author_expected_SHA256", authors),
                                 ("ROOT_result_SHA256", result_pin)):
            key = prefix + "_" + suffix
            require(ready[key] == policy[key] == expected, "Exact archived112 source metadata: " + key)
    require(ready["minimum78_lowering_execution_authorized"] is True
            and ready["minimum78_lowering_row_id"] == policy["minimum78_lowering_row_id"] == LEAF_LOWERING_ROW_ID
            and ready["minimum78_complete_owner_packet_literals"]
            == policy["minimum78_complete_owner_packet_literals"] == MIN78_COMPLETED12
            and ready["minimum78_prospectus_expected_SHA256"]
            == policy["minimum78_prospectus_expected_SHA256"] == MIN78_PROSPECTUS_PINS
            and ready["minimum78_completed80_metadata_authority"]
            == policy["minimum78_completed80_metadata_authority"] == COMPLETED80_AUTHORITY
            and ready["minimum78_product_and_output_widths"]
            == policy["minimum78_product_and_output_widths"] == [78, 40, 72]
            and ready["minimum78_selected_value_args"] == policy["minimum78_selected_value_args"] == [8, [0, 4]]
            and ready["planned_manifest_inclusive_owned_files"] == policy["planned_manifest_inclusive_owned_files"] == 62
            and policy["new_actual_results"] is None and policy["new_actual_resource_comparison"] is None
            and policy["matched_v8_wide_baseline"] is None
            and policy["pending_external_min80_audit"] == {"completed_owner_admitted": False, "manifest_SHA256": None, "ROOT_receipt_SHA256": None},
            "New separately authorized v8 minimum78 scope; no old permission or cost transfer")
    require(not any(k.startswith("minimum80_") for k in ready)
            and not any(k.startswith("minimum80_") for k in policy),
            "Archived min80 permissions never cloned into current v8 fields")
    for name, pin, counts, ownership, schema in MIN78_COMPLETED12:
        if name in (BASELINE112.name, BASELINE112_AUDIT.name, COMPLETED80.name):
            packet(name, pin, counts, schema, ownership)
        else:
            directory = canonical(PROGRAM / name)
            require(directory in _OWN_INVENTORIES,
                    "Original nine owner maps/inventories already admitted unchanged")
            manifest = read(bind(directory / "manifest.json", pin))
            require([len(manifest[k]) for k in ("files", "frozen_inputs", "external_runtime_inputs")] == counts,
                    "Original nine complete declared map counts retained")
    minimum80_completed112_witnesses()
    minimum78_completed80_metadata_witnesses()
    design = read(ROOT / ".context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.json")
    require(policy["all_current12_full_original_declared_maps_and_owned_inventories"]
            == design["prospective_current12_owner_snapshots"]
            and policy["archival_completed80_READY_original_scope11_only"]
            == design["archival_min80_ROOT_READY_scope11_only"],
            "Current full literal snapshots and archival eleven-owner READY remain exactly prospective")
    minimum78_full_optimization_cache_guard([AUTHOR, HELPER],
        ready["new_all_optimization_existing_cache_SHA256"],
        ready["new_all_optimization_absent_cache_paths"])
    budget(admission=True)


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists(),
            "One new standalone second v8 signed leaf route")
    try:
        runtime_invocation_guard(args.ready_sha256)
        _, contract = second_leaf_admission(args.ready_sha256)
        minimum78_admission(read(READY), read(PREFLIGHT))
        minimum78_retain_held_v1_route(read(READY), read(PREFLIGHT))
        current_controller_code_guard()
        copied_metadata_provenance()
        runtime = own_runtime()
        loaded_origins()
        check_code_caches()
        saved_before = saved_runtime_membership()
        repeated_metadata_witnesses()
        minimum80_completed112_witnesses()
        minimum78_completed80_metadata_witnesses()
        first = fresh_union()
        require(saved_runtime_membership() == saved_before,
                "Entire saved runtime across first fresh union")
        repeated_metadata_witnesses()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, HELPER, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        for prefix, paths in (
            ("prior_selector_failed_", (PRIOR_SELECTION_FREEZE, PRIOR_SELECTION_READY,
                PRIOR_SELECTION_LOG, *(RESEARCH / n for n in PRIOR_SELECTION_AUTHORS))),
            ("prior_selector_completed_", (SELECTOR_READY, SELECTOR_RESULT_REVIEW,
                *(RESEARCH / n for n in SELECTOR_AUTHORS))),
            ("prior_inventory_prefit_failed_", (PRIOR_INVENTORY_WITNESS, PRIOR_INVENTORY_READY,
                PRIOR_INVENTORY_LOG, *(RESEARCH / n for n in PRIOR_INVENTORY_AUTHORS))),
            ("completed_native_producer_", (PRODUCER / "manifest.json", PRODUCER_READY,
                PRODUCER_RESULT_REVIEW, *(RESEARCH / n for n in PRODUCER_AUTHORS))),
            ("completed_independent_native_audit_", (NATIVE_AUDIT / "manifest.json",
                NATIVE_AUDIT_READY, NATIVE_AUDIT_RESULT, *(RESEARCH / n for n in NATIVE_AUDIT_AUTHORS))),
            ("held_first_leaf_design_", (*(RESEARCH / n for n in HELD_DESIGN_AUTHORS), HELD_DESIGN_PEER)),
        ):
            for path in paths:
                copy(path, prefix + path.name)
        for path, _ in HELD_V1_INPUTS:
            copy(path, "held_unexecuted_V1_" + path.name)
        for name in (".context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.md",
                     ".context/A13_V8_SIGNED38X40_MINIMUM78_FLOOR40_SIGN38_TO72_PROSPECTUS_run001.json"):
            copy(ROOT / name, "prospective_method_" + Path(name).name)
        save("held_unexecuted_V1_history.json", held_v1_witness())
        save("run_started.json", {"created_UTC": datetime.now(timezone.utc).isoformat(),
            "PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        namespace = execute_new_helper_namespace()
        binding = {
            "inventory_manifest_SHA256": PRODUCER_SHA,
            "inventory_complete_counts": PRODUCER_COUNTS,
            "independent_inventory_verification_SHA256": NATIVE_AUDIT_RESULT_SHA,
            "native_audit_manifest_SHA256": NATIVE_AUDIT_SHA,
            "native_audit_complete_counts": NATIVE_AUDIT_COUNTS,
            "separate_second_standalone_leaf_ROOT_release": True,
            "row_id": ROW_ID, "complete_maps_and_owned_inventories_verified": True,
            "all240_native_slots_verified": True,
            "minimum78_output_sign_extension_lowering_release": True,
            "lowering_row_id": LEAF_LOWERING_ROW_ID,
        }
        leaf, descriptor = namespace["build_second_leaf"](binding, contract, budget)
        budget()
        rows, actual_array_sha = save_and_read_actual_rows(leaf.gates)
        save("native_descriptor.json", descriptor)
        descriptor_sha = digest(OUTPUT / "native_descriptor.json", fresh=True)
        actual_descriptor = reread_new_owned_json("native_descriptor.json", descriptor_sha)
        consumer = independent_whole_row_proof(rows, actual_descriptor)
        save("independent_whole_array_structural_proof.json", consumer)
        cases = native_corpus_and_oracles()
        save("fixed64_native_cases.json", {"schema": "a13-second-v8-min78-fixed-native-cases-v1",
            "case_count": 64, "cases": cases, "duplicates_retained": True})
        batch = independent_native_batch(rows, actual_descriptor["qubits"], cases)
        save("independent_native_forward_inverse_batch.json", batch)
        toys = independent_toy_and_negative_controls()
        save("independent900_scalar_toys_and_four_controls.json", toys)
        save("paid_CCX_macro.json", {"macro": namespace["CCX_PHASE_MACRO"]})
        macro_sha = digest(OUTPUT / "paid_CCX_macro.json", fresh=True)
        actual_macro = reread_new_owned_json("paid_CCX_macro.json", macro_sha)
        require(tuple(tuple(e) for e in actual_macro["macro"]) == EXPECTED_CCX_PHASE_MACRO,
                "Actual saved paid macro matches independent phase and resource method")
        phase = independent_absolute_ccx_phase()
        save("independent_exact_absolute_CCX_phase.json", phase)
        resources = independent_standalone_resources(rows, actual_descriptor["qubits"])
        save("independent_actual_standalone_resources.json", resources)
        save("actual_minimum78_unmatched_v8_resource_scope.json", minimum78_unmatched_cost_statement())
        save("second_leaf_source_contract_binding.json", {
            "schema": "a13-second-v8-min78-original-audited-contract-binding-v1",
            "producer_manifest_SHA256": PRODUCER_SHA,
            "native_audit_manifest_SHA256": NATIVE_AUDIT_SHA,
            "native_contract_original_expected_SHA256": NATIVE_CONTRACT_SHA,
            "exact_ordered_contract": contract,
            "actual_array_SHA256": actual_array_sha, "actual_descriptor_SHA256": descriptor_sha,
            "universal_complete_product78_floor40_and_explicit_computed_sign38_to72_proof": True,
            "whole_array_independent_structural_proof_passed": consumer["passed"],
            "absolute_unit_phase_every_CCX_column_passed": phase["passed"],
            "full72_dirty_XOR_input_preservation_zero_workspace_literal_inverse": True,
            "all_other_MULs_not_emitted_by_this_v8_packet_and_full_source_still_open": True,
            "caller_copy_storage_selector_inverse_and_allowance_obligations_remain": True,
            "original_capped_baselines_unchanged": BASELINES,
            "financial_G2_cost_source_adoption_transfer": False, "fixture_credit": 0})
        loaded_origins()
        check_code_caches()
        require(saved_runtime_membership() == saved_before,
                "Entire original saved runtime before terminal union")
        repeated_metadata_witnesses()
        minimum80_completed112_witnesses()
        minimum78_completed80_metadata_witnesses()
        second = fresh_union()
        require(saved_runtime_membership() == saved_before,
                "Entire saved runtime across second full fresh union")
        repeated_metadata_witnesses()
        summary = {
            "schema": "a13-d4-s4-second-signed-leaf-min78-summary-v2",
            "completed": True, "passed": True, "budget_censored": False,
            "row_id": LEAF_LOWERING_ROW_ID, "source_row_id": ROW_ID, "value": FIRST_VALUE, "ordered_args": FIRST_ARGS,
            "ordered_active_signed_widths": ACTIVE_WIDTHS,
            "word_fraction_product_residue_bits": [72, 40, 144, 78],
            "all12_completed_owner_maps_and_owned_inventories_retained": True,
            "all_old_failed_and_prefit_history_retained_without_promotion": True,
            "actual_saved_native_array_SHA256": actual_array_sha,
            "within_run_distinct_method_whole_array_consumer_passed": True,
            "fresh_exact8_basis_absolute_unit_phase_passed": True,
            "fixed_native_batch": batch,
            "fixed_scalar_toy_pair_count": 900, "fixed_expected_rejected_controls": 4,
            "standalone_leaf_resources": resources,
            "leaf_is_not_full_source_or_capped_schedule": True,
            "external_independent_completed_leaf_audit_still_required": True,
            "both_full_uncached_input_unions": [first, second],
            "current_runtime": runtime, "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "budget": {"process_CPU_seconds": time.process_time(),
                       "wall_seconds": time.monotonic() - _STARTED}, **flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES,
                    "Inclusive owned manifest reserve")
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        require(len(owned) + 1 == 62, "Exactly declared62 inclusive files; no scope expansion")
        complete_manifest({"schema": "a13-d4-s4-second-signed-leaf-min78-manifest-v2",
            "files": owned, "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL,
            "manifest_self_hash_excluded": True, "completed": True, "passed": True,
            "budget_censored": False, "native_audit_manifest_SHA256": NATIVE_AUDIT_SHA,
            "native_audit_complete_counts": NATIVE_AUDIT_COUNTS,
            "both_full_uncached_input_unions": [first, second],
            "terminal_budget_observation": {"process_CPU_seconds": time.process_time(),
                                           "wall_seconds": time.monotonic() - _STARTED},
            **flags()}, owned, total)
        budget()
        print(json.dumps({"passed": True,
            "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
            "second_v8_standalone_signed_leaf_only": True, **flags()}), flush=True)
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
