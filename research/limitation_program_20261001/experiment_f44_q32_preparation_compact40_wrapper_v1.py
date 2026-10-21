"""Unexecuted H32 and compact40 wrapper experiment, frozen clamp002 only.
Original runtime/history/guard helpers retained; ROOT owns release and sole actual.
No target imports, H/numeric/gate/resource execution occurred while authoring.
"""

import argparse
import ast
from array import array
import importlib.util
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
from fractions import Fraction
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "experiment_f44_q32_preparation_compact40_wrapper_v1.py"
METHOD_DOC = RESEARCH / "F44_Q32_PREPARATION_COMPACT40_WRAPPER_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "f44_q32_preparation_compact40_wrapper_preflight_v1.json"
READY = ROOT / ".context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "F44_q32_preparation_compact40_wrapper_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE_NAME = "A14_taylor_f44_stage_C_run003"
AUDIT_NAME = "A14_taylor_f44_stage_C_audit_run001"
SOURCE, AUDIT = PROGRAM / SOURCE_NAME, PROGRAM / AUDIT_NAME
SOURCE_SHA = "7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa"
# ROOT supplied this verified terminal expectation; never populated from a scan.
ROOT_DECLARED_AUDIT_SHA = "3de0e4a36928a630481ff12ba727e2fdc50512b6bd60b2cc2e94edbeb95d42ee"
SOURCE_COUNTS, AUDIT_COUNTS = [34, 851, 2842], [17, 890, 2842]
SOURCE_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json"
SOURCE_READY_SHA = "b781c1c80bc2ee381c9e35b3b83f9c4cadd0fc141c2e88ab214b73f5de2c67c0"
AUDIT_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_AUDIT_ROOT_READY_run001.json"
AUDIT_READY_SHA = "499c77ac13357e93bc1707ae27e6542429edd983879cb2b023da8243dca554df"
ACTUAL_AUDIT_ROOT = (
    ROOT / ".context/A14_F44_STAGE_C_AUDIT_ACTUAL_OWNED_ROOT_VERIFICATION_run001.json"
)
ACTUAL_AUDIT_ROOT_SHA = "b8af47d51348433f194a161c5eaa620c64c194d4b0ce37f9cd85a42e5cf2cd4d"
ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38"
CPU, ADMISSION, WALL = 300, 270, 900
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
OWNERS = {
    "A14_cosine_feasibility_run001": [
        "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b",
        [24, 672, 2842],
    ],
    "A14_cosine_feasibility_audit_run003": [
        "52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f",
        [17, 752, 2842],
    ],
    "A14_taylor_f44_stage_K_run001": [
        "b03c8a7cb62655301b9a231eb987f38e5ec496f612206ff6701143f6cefb8b88",
        [17, 774, 2842],
    ],
    "A14_taylor_f44_stage_K_audit_run001": [
        "2c253beba55b1271dec594db8231c8bdbfcaffbf4d797dedb840eda72568f5be",
        [10, 796, 2842],
    ],
    "A14_taylor_f44_stage_K_root_verification_run001": [
        "24e316217afd614b577fe53921f54b7ad7c346737ec6e21c93500a795a1517d9",
        [8, 811, 2842],
    ],
    SOURCE_NAME: [SOURCE_SHA, SOURCE_COUNTS],
    AUDIT_NAME: [ROOT_DECLARED_AUDIT_SHA, AUDIT_COUNTS],
}
SOURCE_AUTHORS = {
    "experiment_f44_cosine_stage_c_v3.py": (
        "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v3.json": (
        "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41"
    ),
    "f44_cosine_stage_c_source.py": (
        "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"
    ),
    "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": (
        "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141"
    ),
}
AUDIT_AUTHORS = {
    "audit_f44_cosine_stage_c_v1.py": (
        "548d444fdd61e97a7d249bcb2e271ae1489617d065d125114f2e1ec6d62a2167"
    ),
    "A14_F44_COSINE_STAGE_C_INDEPENDENT_AUDIT_PREFLIGHT_V1.md": (
        "d37ca22d3595823fb53787d54613293ebab86b9ba406f3c72a6b0f293e7ef5c2"
    ),
    "a14_f44_cosine_stage_c_independent_audit_preflight_v1.json": (
        "abafdfd42a1f4fa0d2f26926b42fc5142adee9740e6d2df2292a3a36f608185d"
    ),
}
INTERPRETER_PINS = {
    str(LAUNCHER): "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5",
    "C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python.exe": (
        "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
    ),
}
HISTORICAL_CACHE_RELEASES = (
    (
        ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json",
        "ce6e00b8cb2f53e05383d14e20e003e36207cd65096b232bb47df157782df3ba",
        ("experiment_taylor_f44_stage_k.py", "taylor_f44_stage_k_source.py"),
    ),
    (
        ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json",
        "67bf1f1a944f8aafd94f5eafdd418210ff053bf84a3586fd5c2b85c4b67a304a",
        ("audit_taylor_f44_stage_k.py",),
    ),
    (
        ".context/A14_TAYLOR_F44_STAGE_K_INTEGRITY_ROOT_READY_run001.json",
        "6d873e903c3f6e85ef488c8a9c2d4f635370a0af3191f3c65cc66537617f19c9",
        ("verify_taylor_f44_stage_k_root_v1.py",),
    ),
)
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_PACKAGE_TREES = (
    ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath",
    ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath-1.3.0.dist-info",
)

BUILDER = RESEARCH / "f44_cosine_stage_c_source.py"

BUILDER_SHA = "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"

BUILDER_NOTE = RESEARCH / "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md"

BUILDER_NOTE_SHA = "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141"

PRIOR_FAILED = PROGRAM / "A14_taylor_f44_stage_C_run001"

PRIOR_FAILURE_FREEZE = ROOT / ".context/A14_F44_STAGE_C_FAILED_OWNED_FROZEN_run001.json"

PRIOR_FAILURE_FREEZE_SHA = "60b2d2aa068169f19f72052738227588ea5ad2837498fbe0009db1d4a5c17c75"

PRIOR_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run001.json"

PRIOR_READY_SHA = "2a6806788c576085aafd2ff3fed1a03908e33fcddffef8c1d5d2b1c866b047de"

PRIOR_LOG = ROOT / ".context/a14_f44_stage_c_run001.log"

PRIOR_LOG_SHA = "da9d69f12a2cd1a8cef93ce0e112bf79410b659fad6289d8ae7b75bac14ada69"

PRIOR_AUTHORS = {
    "experiment_f44_cosine_stage_c_v1.py": (
        "c4f1bcbce2fd8ab729667c2a28c6dc44c857a6cf6feb02e308d52f2e19751caf"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V1.md": (
        "fa1a8d58c88ff379f7dc0b87733dc75e653ea617f4e93fe92c9f9e5f05a22620"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v1.json": (
        "3b34f4745c6459de8e6eb0f257383dc4e1c7e783b68aa6700711a8f72956564f"
    ),
    "f44_cosine_stage_c_source.py": BUILDER_SHA,
    "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": BUILDER_NOTE_SHA,
}

_PRIOR_FAILED_MEMBERS = set()

PRIOR_V2_OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_run002"

PRIOR_V2_WITNESS = ROOT / ".context/A14_F44_STAGE_C_V2_PREFIT_FAILURE_WITNESS_run002.json"

PRIOR_V2_WITNESS_SHA = "1de19d91d1359ffce383ffd917bc20f803c466d1b35a731c271f18a3b33b5be6"

PRIOR_V2_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run002.json"

PRIOR_V2_READY_SHA = "b53f15f958c9da2b966c965a58bbbe0f4839a61c92ff4452b5ed759a608ee2bc"

PRIOR_V2_LOG = ROOT / ".context/a14_f44_stage_c_run002.log"

PRIOR_V2_LOG_SHA = "a893e7feec700c44f5a686199dfd6ae3ad42687c29e7e11173bcd65e3821bad7"

PRIOR_V2_AUTHORS = {
    "experiment_f44_cosine_stage_c_v2.py": (
        "0a8e72bfa675b07ecaf948024d51ae5fb91381fd67fc0e9ec8d565635bcfff1c"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "f1cc8f98add202206d30cd082d75a2672039551124af4170d98402d47be9a1c0"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v2.json": (
        "40cd6de37e0aa811a8078be12f701d3df317a24732e2ef1ca276aa53beb14ecb"
    ),
}


FINAL_ROOT_NAME = "A14_taylor_f44_stage_C_root_verification_run001"
FINAL_ROOT_SHA = "18da7c127f649014945cd4a3cc07360053a6394ac48f70851a40d786850a618d"
FINAL_ROOT_COUNTS = [8, 916, 2842]
FINAL_ROOT_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_INTEGRITY_ROOT_READY_run001.json"
FINAL_ROOT_READY_SHA = "2b50451df6f1b948b51bf3d337c574d96e95c1981cd53930fdd88c49f48e4029"
FINAL_ROOT_AUTHORS = {
    "verify_f44_cosine_stage_c_root_v1.py": (
        "3cc9b714b9a3adcb7a32e20dc38a215276361faa7a721c5d4d87ac0feabc76ae"
    ),
    "F44_COSINE_STAGE_C_ROOT_INTEGRITY_PREFLIGHT_V1.md": (
        "66806ac48df395058ec99f6455f5d235400b7479b7ba9642315fdfaa55cf49c3"
    ),
    "f44_cosine_stage_c_root_integrity_preflight_v1.json": (
        "ead3ed99d8a15673c01b191a0fe0db4938005b5993524dcc094e947dffccf810"
    ),
}
OWNERS[FINAL_ROOT_NAME] = [FINAL_ROOT_SHA, FINAL_ROOT_COUNTS]
GRID_HELPER = RESEARCH / "f44_q32_preparation_compact40_wrapper_source_v1.py"
GRID_MODULE = "_f44_q32_preparation_compact40_wrapper_builder_v1"
GRID_ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38_CALLER_GRID_NO_AXIS_NO_INPUT_CLAMP"
GRID_CONTRACT_ID = "Q32_MIDPOINT_MOD256_128_M_OR_WRAP3Q4"
MAX_NATIVE_ROWS = 2000000
NATIVE_SOURCE = PROGRAM / "A14_taylor_f44_stage_K_run001"
PRIMARY = SOURCE
_SCIENCE_ADMITTED = False


# Finite original expected startup and immutable axis history; no observed pins.
STARTUP_EXPECTED = {'.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc': {'SHA256': 'd8536aedd91ba3763b64147357c5e8c0a270b6a8031a59130c10d10351ce879e',
                                                                                                      'bytes': 1137},
 '.context/frontier_t0_env/Lib/site-packages/__pycache__/_numba_cuda_redirector.cpython-312.pyc': {'SHA256': 'a440fa4055a99394bebc66cb280485004252f138d989b2d51fee17e9b3f213a1',
                                                                                                   'bytes': 3609},
 '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.pth': {'SHA256': '85a35d0fa0411036458d81dc56ae69bda1059d83882b7e2fe1bc3a5874213421',
                                                                              'bytes': 176},
 '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.py': {'SHA256': '25ed97b37208b2dba48d5732aa44899fa218c85d2c33148743ead8cc60d34fce',
                                                                             'bytes': 854},
 '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.pth': {'SHA256': '526df5910c1cc887b69adb485d6a42cef3a1af0185fcd0640cb8a97f8bc3d77e',
                                                                           'bytes': 174},
 '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.py': {'SHA256': '854bdc54e933b3b1804d88454a4e51c2ecfdd59f6871e5957b97e5a344570d85',
                                                                          'bytes': 2893}}
STARTUP_CACHE_KEYS = ('.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc',
 '.context/frontier_t0_env/Lib/site-packages/__pycache__/_numba_cuda_redirector.cpython-312.pyc')
AXIS_V2_WITNESS_KEY = '.context/F44_GRID_AXIS_V2_PREFIT_FAILURE_WITNESS_run002.json'
AXIS_V2_WITNESS_SHA = '2c9405566371af9bce19ff40385dc2f46f60a2dd2fe521165e0949058c9d5469'
AXIS_V2_READY_KEY = '.context/A14_F44_COSINE_CALLER_GRID_AXIS_ROOT_READY_run002.json'
AXIS_V2_READY_SHA = 'a6ef0c231f9ae624fa8753d69f7d17ac281e9ba2f420f522614295019607b4fc'
AXIS_V2_LOG_KEY = '.context/f44_caller_grid_axis_run002.log'
AXIS_V2_LOG_SHA = '65f800475f5607a380e3df64247b40cc043e3a3cf29a57245412c944c7ba8f4a'
AXIS_V2_OUTPUT_KEY = 'results/limitation_program_20261001/A14_taylor_f44_stage_C_grid_axis_run002'
AXIS_V2_AUTHORS = {'experiment_f44_cosine_caller_grid_axis_v2.py': '1575a24cdb54efc53dd33120ca17da6727d66e35abea4f79fc9ffc3e1b62f102',
 'F44_COSINE_CALLER_GRID_AXIS_PREFLIGHT_V2.md': '3e74a22ca039e6c529bd6533844747faf32b9de3f2d6100ec9c41a26eeca818a',
 'f44_cosine_caller_grid_axis_preflight_v2.json': '6bb667186d11d39d228d1e75a319dd336d083b09472c1877134bab4334333dd3',
 'f44_cosine_caller_grid_axis_source_v1.py': '8df89fa37fff14760c4f44b2900d20062999b076698a1d08d45f5b714ac65cdf'}
AXIS_V2_REVIEWS = {'.context/F44_COSINE_CALLER_GRID_AXIS_INDEPENDENT_STATIC_PEER_next_run002.json': '4e435c6080488141968087c83a07d040aae98923ed8376a802adce2fd2c76522',
 '.context/F44_COSINE_CALLER_GRID_AXIS_ROOT_STATIC_REVIEW_run002.json': '3eeae8062286c5a8ffdddff7c948e3c7515ef0afe9beb73c5edba657235568cf'}
AXIS_V2_ABSENT_CACHES = ['research/limitation_program_20261001/__pycache__/experiment_f44_cosine_caller_grid_axis_v2.cpython-312.pyc',
 'research/limitation_program_20261001/__pycache__/experiment_f44_cosine_caller_grid_axis_v2.cpython-312.opt-1.pyc',
 'research/limitation_program_20261001/__pycache__/experiment_f44_cosine_caller_grid_axis_v2.cpython-312.opt-2.pyc',
 'research/limitation_program_20261001/__pycache__/f44_cosine_caller_grid_axis_source_v1.cpython-312.pyc',
 'research/limitation_program_20261001/__pycache__/f44_cosine_caller_grid_axis_source_v1.cpython-312.opt-1.pyc',
 'research/limitation_program_20261001/__pycache__/f44_cosine_caller_grid_axis_source_v1.cpython-312.opt-2.pyc']
AXIS_V1_AUTHORS = {'F44_COSINE_CALLER_GRID_AXIS_PREFLIGHT_V1.md': 'ebac9881efd8c6ac7ea92fad6f9aee4f2aaf7311a7833ea78f6c0dfe90584e02',
 'experiment_f44_cosine_caller_grid_axis_v1.py': '1f038d7cf9ec9326ef0f242809c8691730b98ad0790416b15b29c07c20727abb',
 'f44_cosine_caller_grid_axis_preflight_v1.json': '27154e7a7e15ff5566d6ce68033e2a430e1f5267832ce184967e26bbad7bd6cc',
 'f44_cosine_caller_grid_axis_source_v1.py': '8df89fa37fff14760c4f44b2900d20062999b076698a1d08d45f5b714ac65cdf'}
AXIS_V1_HOLD_KEY = '.context/F44_COSINE_CALLER_GRID_AXIS_INDEPENDENT_STATIC_PEER_next_run001.json'
AXIS_V1_HOLD_SHA = '5feb26197cf766bebdd66020a032ee53ed95c7bbc69fee6a125d90d1b60589f7'
STARTUP_DIAGNOSIS_KEY = '.context/F44_GRID_AXIS_V2_STARTUP_EXPECTED_JOIN_STATIC_DIAGNOSIS_next_run001.json'
STARTUP_DIAGNOSIS_SHA = '258b5d54dd1826b2e52de593f41e924094c3679e4eabd075d7ef52b75d8bc683'
_OUTPUT_NATIVE_EXPECTED = {}
GRID_DESIGN_PINS = {
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.md": (
        "49ffa09b50230de03e97e98922ebe6a16cdf5f427136dc04156ceff494482c65"
    ),
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.json": (
        "aa7c8a986de52be213054481f5e46a2f36aa60c418117101828aafbfef57d0cc"
    ),
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_INDEPENDENT_STATIC_PEER_run001.json": (
        "3290f0a883512b4932fbc8ec8092d1c1c4b8df69a0e463d47d89e9622ffab423"
    ),
}

AXIS_NAME = "A14_taylor_f44_stage_C_grid_axis_run003"
AXIS_SOURCE = PROGRAM / AXIS_NAME
AXIS_SHA = "a6999915ecf45d96fc2ab89b16cc9b6499dd63cc807d6166a789b73bf1439bc2"
AXIS_COUNTS = [20, 954, 2842]
AXIS_READY = ROOT / ".context/A14_F44_COSINE_CALLER_GRID_AXIS_ROOT_READY_run003.json"
AXIS_READY_SHA = "e67e1f78e7e19888aeb8e3bb44f66527bab06c71ae42e1cfef81f99b0072362e"
AXIS_RESULT = ROOT / ".context/F44_COSINE_CALLER_GRID_AXIS_ACTUAL_RESULT_ROOT_VERIFICATION_run003.json"
AXIS_RESULT_SHA = "2bd3ca4c545327a94dd0ae335cd58de3d11d307b8faea604215e70958e48398f"
AXIS_HELPER = RESEARCH / "f44_cosine_caller_grid_axis_source_v1.py"
AXIS_AUTHORS = {'experiment_f44_cosine_caller_grid_axis_v3.py': '4026253281fcec10f01216929717738e9bb6b46a9a15c1630b041f7912c311fb',
 'F44_COSINE_CALLER_GRID_AXIS_PREFLIGHT_V3.md': '81707b87db9fe8252457382c16b13a7a222a21f492e5bc2beb2874287cd0f6e0',
 'f44_cosine_caller_grid_axis_preflight_v3.json': '9ef4e724f9a8a5e920e888f2b9d18fb04016c048b60e2f367437b0168b9b8c6f',
 'f44_cosine_caller_grid_axis_source_v1.py': '8df89fa37fff14760c4f44b2900d20062999b076698a1d08d45f5b714ac65cdf'}
AXIS_OWNED_EXPECTED = {'actual_axis_only_array_delta.json': '12a95f10f56d6502c8ca3ec7ac72a762959cab36e9030ab33f6560f3ba1589db',
 'actual_component_resources.json': '3603921354527ba6d61a8d4a2ab90687c606208c302be77057deb15b7b5388db',
 'caller_grid_binding.json': 'a5a6e781bbfdb23d0ad08a66ccf301381b3537d255c5500aa273c0e329123beb',
 'completion_outcome.json': '3e243afdab9681746111ad475c9c61a51856e20b2df2d0cfee92fc56d5c6d292',
 'cosine.gates.bin': '37f516fe86668d5e7b95f4d88435241f01e03fed83ab61395bbb602e5359abf1',
 'executed_A14_F44_COSINE_CALLER_GRID_AXIS_ROOT_READY_run003.json': 'e67e1f78e7e19888aeb8e3bb44f66527bab06c71ae42e1cfef81f99b0072362e',
 'executed_F44_COSINE_CALLER_GRID_AXIS_PREFLIGHT_V3.md': '81707b87db9fe8252457382c16b13a7a222a21f492e5bc2beb2874287cd0f6e0',
 'executed_experiment_f44_cosine_caller_grid_axis_v3.py': '4026253281fcec10f01216929717738e9bb6b46a9a15c1630b041f7912c311fb',
 'executed_f44_cosine_caller_grid_axis_preflight_v3.json': '9ef4e724f9a8a5e920e888f2b9d18fb04016c048b60e2f367437b0168b9b8c6f',
 'executed_f44_cosine_caller_grid_axis_source_v1.py': '8df89fa37fff14760c4f44b2900d20062999b076698a1d08d45f5b714ac65cdf',
 'fixed_grid_diagnostics.json': '3fb39af30ba0d4bb992ad02c1445e11ea7e6d03bb2e6ff4679dd33f340925ecc',
 'helper_text_delta_guard.json': '9d8c2bda136c469a538dcff4ed39fc73863b92bba5cf92e3619d5eb5da5b944d',
 'independent_absolute_phase_proof.json': 'aa79ff9c6e8818b6fa9d16d4f51d98dfe238439cfd9a9281e2c83805a5727007',
 'independent_whole_array_consumer.json': 'f5970ae304ff3313e76f6bc982b7e6d2abb9ec720c967bf8a935338c400c0470',
 'native_gate_array.json': '04db850d3b75392dd3deecc359e60689ddd023a5dac69af4cd5bbc413eb484b2',
 'prototype_descriptor.json': 'f383824133236df12f45825a7d783c98110a58fe6d4aaa8f9ef17f932c046abd',
 'retained_original_metadata_reconciliation.json': '5812f6110a4b8a12ae4ecc93bb01e57ab58ff757063b3b31437306128783a193',
 'retained_original_whole_source_accounting.json': '00d12e3997e8ca84e63626ca2f338f8d7cd599b197048532c85157d79216ac7b',
 'run_started.json': '84f82c935ae93e6b2823e53dffcc64df4978a132b6ecd66dc2621ceeb069e175',
 'summary.json': '3e243afdab9681746111ad475c9c61a51856e20b2df2d0cfee92fc56d5c6d292'}
CLAMP_OLD_PREFIX = '    zero, one, minus = (c.helper("CONST", params={"raw": raw}) for raw in (0, Q, -Q))\n    sign = c.helper("SIGN", [c.input])\n    below = c.helper("SIGNED_LT", [c.input, one])\n    upper = c.helper("SELECT", [below, c.input, one])\n    clamped = c.helper("SELECT", [sign, zero, upper])\n    is_Q = c.helper("EQ", [clamped, one])\n    eager = c.helper("SELECT", [is_Q, zero, clamped])'
CLAMP_NEW_PREFIX = '    one, minus = (c.helper("CONST", params={"raw": raw}) for raw in (Q, -Q))\n    # Under the separately admitted full72 D promise, both roles equal the input.\n    clamped, eager = c.input, c.input'
OWNERS[AXIS_NAME] = [AXIS_SHA, AXIS_COUNTS]


HELD_CLAMP_V1_AUTHORS = {'experiment_f44_cosine_caller_grid_clamp_v1.py': '6830c5310afff26258a036d0bfe5420683a8ae181dc56b529cf0a73ae933657e', 'f44_cosine_caller_grid_clamp_source_v1.py': '5519a388357c7d7d11d1b007144a99c46581a62dfa04c22086a6a38f3244f3d9', 'F44_COSINE_CALLER_GRID_CLAMP_PREFLIGHT_V1.md': 'a90f9411932aa00212f4559f612ace81fdf0031e457cd9a1ea5a5d31f84238c3', 'f44_cosine_caller_grid_clamp_preflight_v1.json': '33fda25ba221e003e4305d80e9e538a8ccd6fa64a3998d570b603fb6c4e2792c'}
HELD_CLAMP_V1_REPORTS = {'.context/F44_COSINE_CALLER_GRID_CLAMP_AUTHOR_STATIC_QA_next_run002.json': 'c839ba6f4200cf8e07bed37656b71bad6fc587cd28df59758f872d278a2bd418', '.context/F44_COSINE_CALLER_GRID_CLAMP_ROOT_STATIC_HOLD_run001.json': '7e7b1fb337b96ca95f3efb7d392dd96f393ae26fcdd803c89d22fc7f446400dd', '.context/F44_COSINE_CALLER_GRID_CLAMP_INDEPENDENT_STATIC_HOLD_run001.json': '5f5fb2eb32e6fac52a3d5db48405a341b6bf1be4209cca0b5af51a7aa43fd243'}
HELD_CLAMP_V1_READY_KEY = ".context/A14_F44_COSINE_CALLER_GRID_CLAMP_ROOT_READY_run001.json"
HELD_CLAMP_V1_OUTPUT_KEY = "results/limitation_program_20261001/A14_taylor_f44_stage_C_grid_clamp_run001"

CLAMP_NAME = 'A14_taylor_f44_stage_C_grid_clamp_run002'
CLAMP_SHA = '386140b9aa1f297ba8712831cb11a13a57a9b227cb18093685e619797201b6de'
CLAMP_COUNTS = [22, 992, 2842]
CLAMP_READY_SHA = '0189efea6ddc3e5027c6fffe06606f3799f62ee067d71d6362ce10a4249e8d0b'
CLAMP_ROOT_RESULT_SHA = '10cb9be70bb885e7f0c8982095c08f07c0526bd5f5deb56a45c11d1ac8abf0de'
CLAMP_AUTHORS = {'F44_COSINE_CALLER_GRID_CLAMP_PREFLIGHT_V2.md': 'dee489fe7e1849ddc474c099d279c442dbdb8332431a8900906ffd9bef2cb7b3', 'experiment_f44_cosine_caller_grid_clamp_v2.py': '7a709d6bfd92364a0805ef9f40582c675cc74b193615d1c3cc8cbd106d72df77', 'f44_cosine_caller_grid_clamp_preflight_v2.json': '2913f50f4a72c184944f4f704fc7676684c79b2667f2da6e0e8e206b851a8d65', 'f44_cosine_caller_grid_clamp_source_v1.py': '5519a388357c7d7d11d1b007144a99c46581a62dfa04c22086a6a38f3244f3d9'}
CLAMP_OWNED = {'actual_clamp_array_delta.json': '3d4978877cedf337491e6b7c5c69f0623665a6cf0eedf62db8575d090d06333a', 'actual_component_resources.json': '87e7ee539543d9ae7ee88d47c0b335bd16eb2c6e22911968f22a2ec4d145c47a', 'caller_grid_binding.json': '06a44302f68026086ad7f84e277d2d476e558a3d3273f97668965ac7febe775d', 'completion_outcome.json': 'dcd30dd25256ed0ecfd1ebe01e06dfd0f73a927afdc4d735585862ff7ccfe0c2', 'cosine.gates.bin': '26f1f9ebcab1c956ba508a95ec0fcc5950d8c85762db7c4e064f90dd4bcbc6a9', 'executed_A14_F44_COSINE_CALLER_GRID_CLAMP_ROOT_READY_run002.json': '0189efea6ddc3e5027c6fffe06606f3799f62ee067d71d6362ce10a4249e8d0b', 'executed_F44_COSINE_CALLER_GRID_CLAMP_PREFLIGHT_V2.md': 'dee489fe7e1849ddc474c099d279c442dbdb8332431a8900906ffd9bef2cb7b3', 'executed_experiment_f44_cosine_caller_grid_clamp_v2.py': '7a709d6bfd92364a0805ef9f40582c675cc74b193615d1c3cc8cbd106d72df77', 'executed_f44_cosine_caller_grid_clamp_preflight_v2.json': '2913f50f4a72c184944f4f704fc7676684c79b2667f2da6e0e8e206b851a8d65', 'executed_f44_cosine_caller_grid_clamp_source_v1.py': '5519a388357c7d7d11d1b007144a99c46581a62dfa04c22086a6a38f3244f3d9', 'fixed_grid_diagnostics.json': 'c1ec431faa079d3af3666d62b7e66d967fb79d100cb23e84d33f5c416838a6ab', 'helper_text_delta_guard.json': 'be1e7cb8bbc76b049b8cf16c3eb44b32cfa184119b324ad8f53bc7a1c934471d', 'independent_absolute_phase_proof.json': 'aa79ff9c6e8818b6fa9d16d4f51d98dfe238439cfd9a9281e2c83805a5727007', 'independent_whole_array_consumer.json': 'c4ea7ccd557563dbed2f30675dcbf8a6fa267e5cbd448042be36f810c88569e2', 'native_gate_array.json': '43a0874809f7f5e64c4c66d9d617f436c222d5f4c26ef1ba740ae0937a4a687e', 'prototype_descriptor.json': 'd50cc85ccdb5cf2b1a9afa5b337d3a15e21fefb93b7ed26cf62ec08feaf665b0', 'retained_original_metadata_reconciliation.json': '03273dd63ac70fb8e6ffbd9473e9504220a27d2d62db13ac6d95f2ad9d76b552', 'retained_original_whole_source_accounting.json': '774b0ed0108046d860900a249151cd8bf54a2892391c85a7821ead65dc2105f1', 'run_started.json': '75847b06de7940fda9e56b0d832200c5ef90770e60515f8c50fdac3130d734f1', 'standalone_axis_clamp_resource_comparison.json': '79ed4ba8b22460d20506da3fa228a0ea7de0cfa0dac5f3699b3be3945e75759d', 'summary.json': 'dcd30dd25256ed0ecfd1ebe01e06dfd0f73a927afdc4d735585862ff7ccfe0c2', 'universal_input_clamp_identity.json': 'd4a65f5a72063724dd9a41eb2ef61afd066bbbbbf1c8ee38bc4f0345932af4fe'}
PREP_DESIGN_PINS = {'.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_PROSPECTIVE_DESIGN_run001.md': 'a382efe6a1427daadd2ff0dcf7516c8cdc3d47d094fc5740a2373931a1ea9380', '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_PROSPECTIVE_DESIGN_run001.json': '0b55d2d9a4f13f210b310e1def59cc1158d29a7d0c27af4e4a546f94ef6a2fba', '.context/F44_Q32_PREPARATION_COMPACT40_COHORT_ADDENDUM_run001.md': '601f76d241525f93c3c62a475e90c351ec44b37aee653dc26bb1748e6c94fc60'}
PREP_DESIGN_JSON_KEY = '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_PROSPECTIVE_DESIGN_run001.json'
PREP_ADDENDUM_KEY = '.context/F44_Q32_PREPARATION_COMPACT40_COHORT_ADDENDUM_run001.md'
PREP_CASE_PINS = {'B4x12': {'target': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json', 'original_declared_SHA256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'}, 'source': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/source.json', 'original_declared_SHA256': 'd40db71a1946f49e40683b6686579bc572f668de03f5968ccc5911189760e21f'}, 'schedule': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/schedule_capped.json', 'original_declared_SHA256': 'bfdf78765965f619285118268bc2a761ac2b0aac2a5b32d5a521dd8a77ba222e'}}, 'B8x52': {'target': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/target.json', 'original_declared_SHA256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'}, 'source': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/source.json', 'original_declared_SHA256': 'b1a920b5cf3f20775ab042f43368bc2fc578bfeef7488c00d8d9ce4ad26a6ef8'}, 'schedule': {'path': 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/schedule_capped.json', 'original_declared_SHA256': '1a94a9ef56d9d982fa54a97289710129e119fea24c92ce6e835784028d555c71'}}}
PREP_COHORT_FIELDS = {'inputs': [128, 25769803904, 42949673088, 60129542272, 77309411456, 94489280640, 111669149824, 128849019008, 146028888192, 163208757376, 180388626560, 197568495744, 214748364928, 231928234112, 249108103296, 274877906816, 274877907072, 300647710848, 317827580032, 335007449216, 352187318400, 369367187584, 386547056768, 403726925952, 420906795136, 438086664320, 455266533504, 472446402688, 489626271872, 506806141056, 523986010240, 549755813760, 549755814016, 575525617792, 592705486976, 609885356160, 627065225344, 644245094528, 661424963712, 678604832896, 695784702080, 712964571264, 730144440448, 747324309632, 764504178816, 781684048000, 798863917184, 824633720704, 824633720960, 850403524736, 867583393920, 884763263104, 901943132288, 919123001472, 936302870656, 953482739840, 970662609024, 987842478208, 1005022347392, 1022202216576, 1039382085760, 1056561954944, 1073741824128, 1099511627648], 'input_case_count': 64, 'dirty_patterns': [0, 4722366482869645213695], 'logical_case_count': 128, 'logical_forward_calls': 128, 'logical_reverse_calls': 128, 'physical_whole_array_sweeps': 2, 'program_fixture_credit': 0}
PREP_ROW_ID = 'F44_Q32_H32_TWO_COMPACT40_TWO_PAID_CLAMP002_WRAPPERS_V1'
CLAMP = PROGRAM / CLAMP_NAME
CLAMP_READY = ROOT / ".context/A14_F44_COSINE_CALLER_GRID_CLAMP_ROOT_READY_run002.json"
CLAMP_ROOT_RESULT = ROOT / ".context/F44_COSINE_CALLER_GRID_CLAMP_ACTUAL_RESULT_ROOT_VERIFICATION_run002.json"
LEGACY_CLAMP_HELPER = RESEARCH / "f44_cosine_caller_grid_clamp_source_v1.py"
OWNERS[CLAMP_NAME] = [CLAMP_SHA, CLAMP_COUNTS]
_OUTPUT_METADATA_EXPECTED = {}

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
    guard_serialization_integers(result)
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


def bootstrap_startup_expected():
    """Admit six ORIGINAL expected startup bytes before any loaded-origin check."""
    for key, record in STARTUP_EXPECTED.items():
        budget()
        lexical = ROOT / key
        actual = canonical(lexical, fresh=True)
        require(actual == lexical and actual.is_file(), "Exact finite startup physical origin")
        add(actual, record["SHA256"])
        require(fingerprint(actual)[2] == record["bytes"], "Original fixed startup byte length")
        require(
            digest(actual, fresh=True, already_resolved=True) == record["SHA256"],
            "Fresh complete startup bytes equal ORIGINAL frozen expectations",
        )
    budget()


def axis_code_caches(sources, pins, absent_keys):
    """Axis-only finite three-variant declarations; retain original default guard."""
    budget()
    variants = {
        key_for(Path(cache_from_source(str(source), optimization=optimization))):
        Path(cache_from_source(str(source), optimization=optimization))
        for source in sources
        for optimization in ("", "1", "2")
    }
    present = {key for key, path in variants.items() if path.exists()}
    require(
        len(variants) == 3 * len(sources)
        and type(pins) is dict
        and set(pins) == present
        and type(absent_keys) is list
        and len(absent_keys) == len(set(absent_keys))
        and set(absent_keys) == set(variants) - present,
        "Exactly all declared normal/opt1/opt2 axis caches, no omitted variant",
    )
    for key in sorted(present):
        actual = canonical(variants[key], fresh=True)
        add(actual, pins[key])
        require(
            digest(actual, fresh=True, already_resolved=True) == pins[key],
            "Fresh complete externally expected axis cache bytes",
        )
        _CODE_CACHE_EXPECTED[actual] = pins[key]
    for key in absent_keys:
        path = variants[key]
        require(not path.exists() and not path.is_symlink(), "Exact absent axis cache variant")
        _ABSENT_RUNTIME.add(path)
    default = {
        key_for(Path(cache_from_source(str(source))))
        for source in sources
    }
    code_caches(
        sources,
        {key: pins[key] for key in default & present},
        sorted(default - present),
    )
    budget()


def axis_preoutput_failure_witnesses():
    budget()
    directory = ROOT / AXIS_V2_OUTPUT_KEY
    require(
        not directory.exists()
        and not directory.is_symlink()
        and directory.resolve(strict=False) == directory,
        "Executed axis V2 output stays wholly absent without physical alias",
    )
    budget()


def admit_axis_preoutput_history(ready, policy):
    for field, expected in (
        ("axis_V2_prefit_failure_witness_SHA256", AXIS_V2_WITNESS_SHA),
        ("axis_V2_READY_expected_SHA256", AXIS_V2_READY_SHA),
        ("axis_V2_log_expected_SHA256", AXIS_V2_LOG_SHA),
        ("axis_V2_author_expected_SHA256", AXIS_V2_AUTHORS),
        ("axis_V2_static_review_expected_SHA256", AXIS_V2_REVIEWS),
        ("axis_V2_absent_new_code_cache_paths", AXIS_V2_ABSENT_CACHES),
        ("V1_quartet_expected_SHA256_immutable_unexecuted", AXIS_V1_AUTHORS),
        ("V1_independent_hold_report_expected_SHA256", AXIS_V1_HOLD_SHA),
        ("startup_static_diagnosis_expected_SHA256", STARTUP_DIAGNOSIS_SHA),
    ):
        require(ready[field] == policy[field] == expected, "Exact original axis history expectation")
    witness = read(bind(ROOT / AXIS_V2_WITNESS_KEY, AXIS_V2_WITNESS_SHA))
    require(
        witness["schema"] == "root-f44-grid-axis-v2-prefit-failure-witness-v1"
        and witness["metadata_only"] is True
        and witness["passed"] is False
        and witness["actual_failed_before_output_creation"] is True
        and witness["scientific_admission_or_helper_emission_started"] is False
        and witness["output_route_absent"] is True
        and witness["owned_output_files"] == {}
        and witness["output_route"] == AXIS_V2_OUTPUT_KEY
        and witness["original_READY_expected_SHA256"] == AXIS_V2_READY_SHA
        and witness["original_log_SHA256"] == AXIS_V2_LOG_SHA
        and witness["original_author_expected_SHA256"] == AXIS_V2_AUTHORS
        and witness["original_static_review_expected_SHA256"] == AXIS_V2_REVIEWS
        and witness["existing_new_code_cache_SHA256"] == {}
        and witness["absent_new_code_cache_paths"] == AXIS_V2_ABSENT_CACHES
        and witness["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and witness["terminal_process_exit_code"] == 1
        and witness["terminal_CPU_wall_uncertified"] is True
        and witness["terminal_CPU_seconds"] is None
        and witness["terminal_wall_seconds"] is None
        and witness["exact_offending_loaded_origin"] is None
        and witness["failure_origin_unlogged_and_not_inferred"] is True
        and witness["original_expected_hashes_runtime_guards_or_caps_waived"] is False
        and witness["new_fixture_credit"] == 0,
        "Actual axis V2 startup failure stays metadata-only with unknown offending origin",
    )
    historical = read(bind(ROOT / AXIS_V2_READY_KEY, AXIS_V2_READY_SHA))
    require(
        historical["schema"] == "root-f44-caller-grid-axis-READY-v2"
        and historical["author_method_SHA256"] == AXIS_V2_AUTHORS
        and historical["output"] == AXIS_V2_OUTPUT_KEY
        and historical["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and historical["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in OWNERS.items() if name != AXIS_NAME}
        and historical["completed_owner_complete_counts"]
        == {name: item[1] for name, item in OWNERS.items() if name != AXIS_NAME}
        and historical["existing_new_code_cache_SHA256"] == {}
        and historical["absent_new_code_cache_paths"] == AXIS_V2_ABSENT_CACHES
        and historical["V1_quartet_expected_SHA256_immutable_unexecuted"] == AXIS_V1_AUTHORS
        and historical["V1_independent_hold_report_expected_SHA256"] == AXIS_V1_HOLD_SHA,
        "Original executed axis V2 complete release and six cache absences stay fixed",
    )
    for name, expected in AXIS_V2_AUTHORS.items():
        bind(RESEARCH / name, expected)
    for name, expected in AXIS_V1_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(ROOT / AXIS_V2_LOG_KEY, AXIS_V2_LOG_SHA)
    for key, expected in AXIS_V2_REVIEWS.items():
        bind(ROOT / key, expected)
    bind(ROOT / AXIS_V1_HOLD_KEY, AXIS_V1_HOLD_SHA)
    bind(ROOT / STARTUP_DIAGNOSIS_KEY, STARTUP_DIAGNOSIS_SHA)
    axis_code_caches(
        [RESEARCH / "experiment_f44_cosine_caller_grid_axis_v2.py", AXIS_HELPER],
        historical["existing_new_code_cache_SHA256"],
        historical["absent_new_code_cache_paths"],
    )
    axis_preoutput_failure_witnesses()


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
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts") + _PACKAGE_TREES:
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
    for key in STARTUP_CACHE_KEYS:
        candidates.add(canonical(ROOT / key))
        require(len(candidates) <= MAX_RUNTIME_FILES, "Finite explicit startup cache membership")
    return candidates


def key_for(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual) == expected, "Actual admitted expected bytes")
    return actual


def packet(name, pin, counts):
    directory = canonical(PROGRAM / name)
    manifest = bind(directory / "manifest.json", pin)
    data = read(manifest)
    no_failure(directory)
    require(
        data.get("passed") is True
        and data.get("completed") is True
        and data.get("budget_censored") is False
        and data.get("manifest_self_hash_excluded") is True,
        "Actual completed uncensored scoped source/audit, not candidate eligibility",
    )
    require(
        [len(data[field]) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
        == counts,
        "Complete original maps",
    )
    owned = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        require(type(data[field]) is dict, "Typed complete original input maps")
        for key, expected in data[field].items():
            budget()
            require(type(key) is str, "Literal original key")
            if field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Scoped external original key")
                path = Path(key)
            else:
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in Path(key).parts,
                    "Exact slash-relative old key",
                )
                root_owned = key.startswith(directory.relative_to(ROOT).as_posix() + "/")
                path = ROOT / key if field == "frozen_inputs" or root_owned else directory / key
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory)
                    and actual not in owned
                    and actual.relative_to(ROOT if root_owned else directory).as_posix() == key,
                    "Exact no-alias original own membership",
                )
                owned.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact original ROOT membership",
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Exact external original membership",
                )
    require(inventory(directory) == owned, "Exact complete prior inventory")
    _OWN_INVENTORIES[directory] = owned
    return data


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
    prior_failure_witnesses()
    axis_preoutput_failure_witnesses()
    held_clamp_V1_absences()
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
    guard_serialization_integers(value)
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
    guard_serialization_integers(value)
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
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,'
                b'"hard_budget_state_uncertified":true,"new_test_credit":0,'
                b'"Stage_C_release_authorized":false,"full_G2":false,"adoption":false}\n'
            )
    except OSError:
        pass


def fixed_integer_policy():
    budget()
    require(
        "PYTHONINTMAXSTRDIGITS" not in os.environ
        and "int_max_str_digits" not in sys._xoptions
        and sys.flags.int_max_str_digits
        == sys.get_int_max_str_digits()
        == sys.int_info.default_max_str_digits
        == 4300,
        "Pinned default decimal conversion policy before one explicit bounded change",
    )
    sys.set_int_max_str_digits(INTEGER_DECIMAL_DIGITS)
    require(
        sys.get_int_max_str_digits() == INTEGER_DECIMAL_DIGITS, "Exactly fixed20000 decimal digits"
    )
    budget()


def guard_serialization_integers(value):
    """A bounded representation guard; it neither rounds nor changes a value."""
    budget()
    require(
        sys.get_int_max_str_digits() == INTEGER_DECIMAL_DIGITS,
        "Fixed finite decimal policy unchanged",
    )
    pending, count, maximum_bits = [value], 0, 0
    while pending:
        budget()
        item = pending.pop()
        count += 1
        require(count <= MAX_SERIALIZATION_VALUES, "Evidence-value traversal bounded by128MiB")
        if type(item) is int:
            bits = item.bit_length()
            require(bits <= INTEGER_SERIALIZATION_BITS, "Each serialized integer at most65536 bits")
            maximum_bits = max(maximum_bits, bits)
        elif isinstance(item, dict):
            for key, member in item.items():
                budget()
                pending.append(key)
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, "Bounded serializer frontier")
        elif isinstance(item, (list, tuple)):
            for member in item:
                budget()
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, "Bounded serializer frontier")
    budget()
    return {"visited_values": count, "maximum_integer_bits": maximum_bits}


def prior_failure_witnesses():
    budget()
    require(
        inventory(PRIOR_FAILED) == _PRIOR_FAILED_MEMBERS
        and (PRIOR_FAILED / "FAILED_UNSEALED.json").is_file()
        and not (PRIOR_FAILED / "manifest.json").exists()
        and not (PRIOR_FAILED / "manifest.json").is_symlink(),
        "Original13-file partial Stage C run remains immutable, failed and unapproved",
    )
    require(
        sum(fingerprint(path)[2] for path in _PRIOR_FAILED_MEMBERS) == 11426616,
        "Original failed-owned byte count unchanged",
    )
    require(
        not PRIOR_V2_OUTPUT.exists()
        and not PRIOR_V2_OUTPUT.is_symlink()
        and PRIOR_V2_OUTPUT.resolve(strict=False) == PRIOR_V2_OUTPUT,
        "Actual V2 startup failure stays before output creation and without physical alias",
    )
    budget()


def admit_prior_failure(ready, policy):
    require(
        ready["prior_failed_owned_freeze_SHA256"]
        == policy["prior_failed_owned_freeze_SHA256"]
        == PRIOR_FAILURE_FREEZE_SHA,
        "Externally frozen exact previous failure map",
    )
    record = read(bind(PRIOR_FAILURE_FREEZE, PRIOR_FAILURE_FREEZE_SHA))
    require(
        record["schema"] == "root-a14-f44-stage-c-failed-owned-freeze-v1"
        and record["metadata_freeze_only"] is True
        and record["passed"] is False
        and record["original_failure_is_authoritative"] is True
        and record["hard_budget_state_uncertified"] is True
        and record["all_expected_SHA_waivers"] == 0,
        "Previous failure freeze is metadata only",
    )
    require(
        record["failure_route"] == PRIOR_FAILED.relative_to(ROOT).as_posix()
        and record["owned_file_count"] == 13
        and record["owned_bytes"] == 11426616
        and record["original_READY_expected_sha256"] == PRIOR_READY_SHA
        and record["original_log_sha256"] == PRIOR_LOG_SHA,
        "Exact prior route/counts/READY/raw log",
    )
    members = record["observed_owned_files"]
    require(
        type(members) is dict and len(members) == 13, "All13 immutable prior owned observations"
    )
    for key, expected in members.items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and (ROOT / key).relative_to(ROOT).as_posix() == key
            and ".." not in Path(key).parts,
            "Exact prior ROOT-relative owned spelling",
        )
        member = bind(ROOT / key, expected)
        require(
            member.is_relative_to(PRIOR_FAILED)
            and member not in _PRIOR_FAILED_MEMBERS
            and member.name != "manifest.json",
            "Unique physically confined prior failed-owned member",
        )
        _PRIOR_FAILED_MEMBERS.add(member)
    historical = read(bind(PRIOR_READY, PRIOR_READY_SHA))
    require(
        historical["schema"] == "root-a14-f44-cosine-stage-c-READY-v1"
        and historical["author_method_SHA256"] == PRIOR_AUTHORS
        and historical["output"] == PRIOR_FAILED.relative_to(ROOT).as_posix(),
        "All five exact original author bytes remain fixed",
    )
    for name, expected in PRIOR_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_LOG, PRIOR_LOG_SHA)
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v1.py", BUILDER],
        historical["existing_new_code_cache_SHA256"],
        historical["absent_new_code_cache_paths"],
    )
    failure, marker = (
        read(PRIOR_FAILED / "failure.json"),
        read(PRIOR_FAILED / "FAILED_UNSEALED.json"),
    )
    require(
        failure["passed"] is False
        and failure["completed"] is False
        and failure["error_type"] == "ValueError"
        and "4300 digits" in failure["error"]
        and marker["passed"] is False
        and marker["completed"] is False
        and marker["hard_budget_state_uncertified"] is True
        and marker["budget_censored"] is None,
        "Exact previous decimal-serialization failure remains authoritative",
    )
    for key, expected in (
        ("prior_V2_prefit_failure_witness_SHA256", PRIOR_V2_WITNESS_SHA),
        ("prior_V2_READY_SHA256", PRIOR_V2_READY_SHA),
        ("prior_V2_log_SHA256", PRIOR_V2_LOG_SHA),
    ):
        require(
            ready[key] == policy[key] == expected,
            "Exact externally expected V2 startup failure metadata history",
        )
    require(
        ready["prior_V2_three_author_SHA256"]
        == policy["prior_V2_three_author_SHA256"]
        == PRIOR_V2_AUTHORS,
        "All three original V2 author expectations remain fixed",
    )
    witness = read(bind(PRIOR_V2_WITNESS, PRIOR_V2_WITNESS_SHA))
    require(
        witness["schema"] == "root-a14-stage-c-v2-prefit-failure-witness-v1"
        and witness["passed"] is False
        and witness["metadata_only"] is True
        and witness["actual_V2_failed_before_output_mkdir"] is True
        and witness["scientific_execution_started"] is False
        and witness["bounded_decimal_policy_set_by_V2_before_failure"] is False
        and witness["original_READY_expected_sha256"] == PRIOR_V2_READY_SHA
        and witness["original_log_expected_sha256"] == PRIOR_V2_LOG_SHA
        and witness["author_expected_SHA256"] == PRIOR_V2_AUTHORS
        and witness["output_route"] == PRIOR_V2_OUTPUT.relative_to(ROOT).as_posix()
        and witness["original_run001_failure_unchanged"] is True
        and witness["startup_flag_observed"]
        == witness["startup_effective_digit_limit_observed"]
        == witness["startup_documented_default_observed"]
        == 4300
        and witness["startup_environment_override_absent"] is True
        and witness["startup_xoption_override_absent"] is True
        and witness["new_fixture_credit"] == 0,
        "V2 startup guard failure has no scientific or bounded-policy result",
    )
    historical_V2 = read(bind(PRIOR_V2_READY, PRIOR_V2_READY_SHA))
    require(
        historical_V2["schema"] == "root-a14-f44-cosine-stage-c-READY-v2"
        and historical_V2["author_method_SHA256"]
        == {
            **PRIOR_V2_AUTHORS,
            BUILDER.name: BUILDER_SHA,
            BUILDER_NOTE.name: BUILDER_NOTE_SHA,
        }
        and historical_V2["output"] == PRIOR_V2_OUTPUT.relative_to(ROOT).as_posix()
        and historical_V2["limits_CPU_admission_wall"] == [300, 270, 900]
        and historical_V2["integer_decimal_digit_limit"] == INTEGER_DECIMAL_DIGITS
        and historical_V2["integer_serialization_bit_cap"] == INTEGER_SERIALIZATION_BITS,
        "Exact V2 author trio, shared builder and bounded representation plan preserved",
    )
    for name, expected in PRIOR_V2_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_V2_LOG, PRIOR_V2_LOG_SHA)
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v2.py", BUILDER],
        historical_V2["existing_new_code_cache_SHA256"],
        historical_V2["absent_new_code_cache_paths"],
    )
    prior_failure_witnesses()


def component_scope(record, schema):
    require(
        record["schema"] == schema
        and record["passed"] is True
        and record["completed"] is True
        and record["budget_censored"] is False
        and record["limits_CPU_admission_wall"] == [300, 270, 900],
        "Actual uncensored fixed component process; no new science",
    )
    for key in (
        "full_G2",
        "adoption",
        "cost_transfer",
        "quantum_advantage",
        "global_financial_gate_emission_authorized",
    ):
        require(record[key] is False, "Original component does not authorize financial promotion")
    for key in ("new_test_credit", "new_credited_gate_replays", "new_price_samples"):
        require(type(record[key]) is int and record[key] == 0, "No fixture or price credit")
    require(
        record["original_scientific_receipts_unchanged"] is True
        and record["previous_A14_rejected_rows_unchanged"] is True,
        "Original scope remains explicit",
    )


def reconcile_metadata():
    source_summary, source_outcome = (
        read(SOURCE / "summary.json"),
        read(SOURCE / "completion_outcome.json"),
    )
    audit_summary, audit_outcome = (
        read(AUDIT / "summary.json"),
        read(AUDIT / "completion_outcome.json"),
    )
    for record in (source_summary, source_outcome):
        component_scope(record, "a14-f44-stage-c-primary90-summary-v3")
        require(
            record["primary_digits"] == 90
            and record["coefficient_count"] == 448
            and record["center_count"] == 64
            and record["actual_native_replay_counts"] == [64, 16]
            and record["actual_prototype_completed"] is True,
            "Same completed primary90 component scope",
        )
    for record in (audit_summary, audit_outcome):
        component_scope(record, "a14-f44-stage-c-independent130-summary-v1")
        require(
            record["producer_manifest_SHA256"] == SOURCE_SHA
            and record["producer_complete_counts"] == SOURCE_COUNTS
            and record["independent_digits"] == 130
            and record["logical_forward_reverse_checks"] == [64, 16]
            and record["physical_forward_reverse_sweeps"] == [2, 2]
            and record["all448_true_coefficients_and64_centers_authorized"] is True
            and record["all64_uniform_and_native_segments_independently_authorized"] is True
            and record["complete_saved_array_structure_absolute_phase_and_resources_audited"]
            is True
            and record["resource_gate_passed"] is False
            and record["component_candidate_eligible"] is False
            and record["row_status"] == "REJECTED",
            "Exact saved independent130 authorization and rejection",
        )
    require(
        source_outcome["failed"] is False and audit_outcome["failed"] is False,
        "Both authoritative successful outcomes",
    )
    row = read(SOURCE / "fixed_frontier_row.json")
    require(
        source_summary["row"] == source_outcome["row"] == row
        and row["row_id"] == ROW_ID
        and row["status"] == "REJECTED"
        and row["resource_gate_passed"] is False
        and row["candidate_eligible"] is False
        and row["native_rows"] == 436366
        and row["native_qubits"] == 10364,
        "Unchanged actual source resource rejection",
    )
    binding = read(SOURCE / "original_source_binding.json")
    own_binding = read(AUDIT / "independent_source_binding_audit.json")
    require(
        own_binding["passed"] is True and own_binding["complete_source_binding"] == binding,
        "Full saved original source-binding metadata agrees",
    )
    literals, own_literals = (
        read(SOURCE / "primary90_literals.json"),
        read(AUDIT / "independent130_literal_audit.json"),
    )
    require(
        literals["coefficient_count"] == own_literals["coefficient_count"] == 448
        and literals["center_count"] == own_literals["center_count"] == 64
        and literals["table_literal_count"] == 512
        and own_literals["passed"] is True
        and own_literals["digits"] == 130
        and own_literals["oracle_bits"] == 512
        and own_literals["Machin_terms"] == 200
        and own_literals["trig_terms"] == 224
        and own_literals["fixed_words_unchanged"] is True
        and len(literals["table"]) == 64
        and all(len(bank) == 8 for bank in literals["table"]),
        "Literal inventory metadata only; exact oracle pairs remain opaque",
    )
    require(
        len(literals["coefficient_rows"]) == len(own_literals["rows"]) == 448
        and len(literals["center_rows"]) == 64,
        "Every saved coefficient and center record",
    )
    for primary, independent in zip(
        literals["coefficient_rows"], own_literals["rows"], strict=True
    ):
        budget()
        require(
            [primary[key] for key in ("segment", "degree", "raw")]
            == [independent[key] for key in ("segment", "degree", "raw")]
            and independent["all_containment_half_ULP_checks_passed"] is True,
            "Every saved literal identity and prior authorized status agrees; "
            "no interval evaluation",
        )
    native, own_native = (
        read(SOURCE / "all64_native_certificate.json"),
        read(AUDIT / "independent_native_audit.json"),
    )
    require(
        native["all64_native_promises_passed"] is True
        and own_native["passed"] is True
        and native["segment_rows"] == own_native["segment_rows"]
        and len(native["segment_rows"]) == 64,
        "All64 saved native records equal; no recurrence evaluation",
    )
    uniform, own_uniform = (
        read(SOURCE / "uniform_certificate.json"),
        read(AUDIT / "independent_uniform_audit.json"),
    )
    require(
        uniform["uniform_component_gate_passed"] is True
        and own_uniform["passed"] is True
        and own_uniform["all64_closed_segments"] is True
        and len(own_uniform["rows"]) == 64
        and uniform["original_E_old"] == own_uniform["original_E_old"]
        and own_uniform["no_financial_allowance_transfer"] is True,
        "Saved uniform scope and original allowance identity; no bound arithmetic",
    )
    resources, own_resources = (
        read(SOURCE / "actual_prototype_resources.json"),
        read(AUDIT / "independent_actual_resources.json"),
    )
    cost, own_cost = (
        read(SOURCE / "whole_source_resource_comparison.json"),
        read(AUDIT / "independent_whole_source_cost_audit.json"),
    )
    require(
        resources == own_resources
        and cost["actual_clean_prototype_resource"] == resources
        and own_cost["passed"] is True
        and cost["cases"] == own_cost["cases"]
        and cost["matched_serial_clean_function_resource"]
        == own_cost["matched_serial_clean_function_resource"]
        and cost["all_resource_gates_passed"] is own_cost["all_resource_gates_passed"] is False
        and own_cost["actual_capped_changed_financial_schedule_realized"] is False,
        "Exact saved ASAP/serial and complete-source cost agreement; no resource recount",
    )
    array, gates = (
        read(SOURCE / "native_gate_array.json"),
        read(AUDIT / "independent_gate_array_audit.json"),
    )
    require(
        array["rows"] == gates["all_actual_rows_consumed"] == 436366
        and gates["all_actual_allocations_consumed"] == 10364
        and array["gate_SHA256"]
        == _FROZEN[(SOURCE / array["gate_file"]).relative_to(ROOT).as_posix()]
        and gates["actual_global_inverse_checked_row_for_row"] is True
        and gates["universal_full72_clean_XOR_conditional"] is True
        and gates["builder_or_MatchingCircuit_called"] is False,
        "Saved array consumer metadata and exact binary pin; bytes only hashed here",
    )
    phase = read(AUDIT / "independent_absolute_phase_audit.json")
    require(
        phase["exact_absolute_phase_CCX"] is True
        and phase["relative_or_unknown_global_phase_accepted"] is False,
        "Prior exact phase audit retained; no phase calculation",
    )
    diagnostics, own_diagnostics = (
        read(SOURCE / "fixed_native_diagnostics.json"),
        read(AUDIT / "independent_bit_sliced_diagnostics.json"),
    )
    require(
        diagnostics["full_map_case_count"] == own_diagnostics["full_map_case_count"] == 32
        and diagnostics["standalone_round_tie_case_count"]
        == own_diagnostics["standalone_round_tie_case_count"]
        == 8
        and diagnostics["whole_prototype_total_replays"]
        == own_diagnostics["logical_whole_prototype_total_replays"]
        == 64
        and diagnostics["standalone_round_leaf_total_replays"]
        == own_diagnostics["logical_standalone_round_total_replays"]
        == 16
        and own_diagnostics["entire_allocated_state_forward_and_reverse_compared"] is True
        and own_diagnostics["physical_prototype_sweeps"]
        == own_diagnostics["physical_ROUND_sweeps"]
        == 2
        and own_diagnostics["case_or_corpus_expansion"] is False,
        "Same saved fixed diagnostics; no replay or scalar oracle",
    )
    return dict(
        source_manifest_SHA256=SOURCE_SHA,
        audit_manifest_SHA256=ROOT_DECLARED_AUDIT_SHA,
        source_complete_counts=SOURCE_COUNTS,
        audit_complete_counts=AUDIT_COUNTS,
        saved_source_binding_literals_native_uniform_scope_agrees=True,
        saved_actual_ASAP_serial_and_whole_source_resource_metadata_equal=True,
        saved_phase_and_fixed_diagnostic_metadata_reconciled=True,
        universal_helper_proof_remains_conditional_on_original_full72_leaf_and_all64_range_premises=True,
        source_public_Q_endpoint_map_not_original_equivalence=True,
        **flags(),
    )


def save_gate_array(circuit):
    budget()
    require(0 < circuit.rows <= MAX_NATIVE_ROWS, "ONE complete bounded clean prototype")
    target = OUTPUT / "preparation_wrapper.gates.bin"
    members = inventory(OUTPUT)
    bytes_total = circuit.rows * 16
    require(
        not target.exists()
        and len(members) + 2 <= MAX_OWN_FILES
        and sum(path.stat().st_size for path in members) + bytes_total <= MAX_OWN_BYTES,
        "Actual gate bytes admitted with final manifest slot",
    )
    with target.open("xb") as stream:
        for offset in range(0, len(circuit.gates), 16384):
            budget()
            stream.write(circuit.gates[offset : offset + 16384].tobytes())
    require(target.stat().st_size == bytes_total, "Complete actual saved gate payload")
    return {
        "gate_file": target.name,
        "gate_SHA256": digest(target, fresh=True),
        "rows": circuit.rows,
        "bytes": bytes_total,
        "row_format": "little-endian int32 Nx4 X/CX/CCX",
    }


def audit_native_payload(path, rows, qubits, numpy_header=False):
    require(
        type(rows) is int and 0 < rows <= 2000000 and type(qubits) is int and 0 < qubits <= 16384,
        "Finite complete native payload contract",
    )
    data = independent_input_bytes(path)
    offset = 0
    if numpy_header:
        require(
            data[:6] == b"\x93NUMPY" and data[6:8] in (b"\x01\x00", b"\x02\x00"),
            "Only exact native NPY1/2 envelopes",
        )
        header_bytes = 2 if data[6] == 1 else 4
        header_length = int.from_bytes(data[8 : 8 + header_bytes], "little")
        offset = 8 + header_bytes + header_length
        require(header_length <= 4096 and offset <= len(data), "Bounded complete NPY header")
        header = ast.literal_eval(data[8 + header_bytes : offset].decode("latin1"))
        require(
            header == {"descr": "<i4", "fortran_order": False, "shape": (rows, 4)},
            "Exact little-endian int32 row-major array, no dtype conversion",
        )
    require(
        sys.byteorder == "little" and array("i").itemsize == 4 and len(data) - offset == 16 * rows,
        "All and only complete native rows",
    )
    words = array("i")
    words.frombytes(data[offset:])
    for index in range(rows):
        if index % 128 == 0:
            budget(admission=True)
        kind, a, b, c = words[4 * index : 4 * index + 4]
        operands = (a, b, c)[:kind]
        require(
            kind in (1, 2, 3)
            and len(set(operands)) == kind
            and all(0 <= wire < qubits for wire in operands)
            and all(x == 0 for x in (a, b, c)[kind:]),
            "Every full native opcode/wire/padding value independent validation",
        )
    budget(admission=True)
    return words


def audit_admitted_leaves(binding):
    leaves = {}
    for operation in ("ADD", "SUB"):
        profile = binding["cases"]["B4x12"]["selected_primitive_profiles"][operation]
        second = binding["cases"]["B8x52"]["selected_primitive_profiles"][operation]
        require(
            profile == second and not profile.get("resource_rejected"),
            "One identical independently authorized original BK72 leaf",
        )
        entries = read(ROOT / profile["descriptor_path"])
        require(type(entries) is list, "Actual full original descriptor list")
        selected = [
            entry
            for entry in entries
            if (entry["op"], entry["width"], entry["variant"])
            == (operation.lower(), 72, "brent-kung")
        ]
        require(len(selected) == 1, "One exact generic full72 native leaf")
        descriptor = selected[0]
        require(
            descriptor["args"] == [list(range(72)), list(range(72, 144))]
            and descriptor["outs"] == [list(range(144, 216))]
            and descriptor["resources"] == profile["resources"]
            and descriptor["spec"]["lowering"] == "clean-xor-prefix-add-sub-v1"
            and not descriptor["spec"].get("input_contract"),
            "Exact admitted unrestricted ADD/SUB clean ABI",
        )
        path = canonical(ROOT / profile["gate_path"])
        require(
            _FROZEN[key_for(path)] == profile["gate_sha256"], "Original saved raw expected leaf SHA"
        )
        leaves[operation] = {
            "descriptor": descriptor,
            "gate_SHA256": profile["gate_sha256"],
            "words": audit_native_payload(
                path,
                descriptor["resources"]["source_gates"],
                descriptor["resources"]["qubits"],
                True,
            ),
        }
    descriptors, arrays = (
        read(NATIVE_SOURCE / "primitive_descriptors.json"),
        read(NATIVE_SOURCE / "native_gate_arrays.json"),
    )
    for operation, key in (("MUL", "multiplier"), ("ROUND", "rounder")):
        descriptor, record = descriptors[key], arrays[key]
        arity = 2 if operation == "MUL" else 1
        require(
            descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
            and descriptor["spec"]["width"] == 72
            and descriptor["args"] == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
            and descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))]
            and descriptor["input_preserved"] is True
            and descriptor["dirty_output_XOR"] is True
            and descriptor["private_workspace_zero_entry_exit"] is True,
            "Full72 previously independently proved K clean ports",
        )
        if operation == "MUL":
            require(
                descriptor["spec"]["fraction_bits"] == 44
                and descriptor["spec"]["product_width"] == 116
                and descriptor["spec"]["active_operand_bits"] == [52, 38]
                and descriptor["spec"]["input_contract"] == {"signed_operand_bits": [52, 38]}
                and descriptor["full_signed_semantic_product_bits"] == 144
                and descriptor["generic_active_signed_product_bits"] == 90,
                "Exact newly paid signed52x38/F44 K multiplier domain",
            )
        else:
            require(
                descriptor["spec"]["input_fraction_bits"] == 44
                and descriptor["spec"]["output_fraction_bits"] == 40
                and descriptor["spec"]["input_contract"] == {},
                "Universal signed ties-even K rounder",
            )
        path = canonical(NATIVE_SOURCE / record["gate_file"])
        require(
            _FROZEN[key_for(path)] == record["gate_SHA256"]
            and record["rows"] == descriptor["gate_rows"],
            "Actual K independent descriptor/full-binary expected binding",
        )
        leaves[operation] = {
            "descriptor": descriptor,
            "gate_SHA256": record["gate_SHA256"],
            "words": audit_native_payload(path, record["rows"], descriptor["qubits"]),
        }
    return leaves


C130_CCX_MACRO = (
    ("H", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 1),
    ("T", 2),
    ("H", 2),
    ("CX", 0, 1),
    ("T", 0),
    ("TD", 1),
    ("CX", 0, 1),
)


class C130SavedRows:
    """An actual-row proof cursor, never an emitter or a circuit builder."""

    def __init__(self, words, qubits, start=0, finish=None):
        budget()
        require(type(qubits) is int and 0 < qubits <= 16384, "Bounded actual allocated wires")
        require(
            len(words) % 4 == 0 and 0 < len(words) // 4 <= 2000000,
            "Complete bounded native Nx4 payload",
        )
        self.words, self.qubits, self.cursor = words, qubits, start
        self.finish = len(words) // 4 if finish is None else finish
        require(0 <= start <= self.finish <= len(words) // 4, "Actual-row cursor interval")

    def consume(self, wires):
        if self.cursor % 128 == 0:
            budget()
        require(
            1 <= len(wires) <= 3
            and len(set(wires)) == len(wires)
            and all(type(w) is int and 0 <= w < self.qubits for w in wires),
            "Canonical consumed native operands",
        )
        require(self.cursor < self.finish, "No implicit row, truncation or overrun")
        at = 4 * self.cursor
        require(
            self.words[at] == len(wires)
            and all(self.words[at + 1 + j] == wires[j] for j in range(len(wires)))
            and all(self.words[at + 1 + j] == 0 for j in range(len(wires), 3)),
            "Actual saved row satisfies independent local proof step",
        )
        self.cursor += 1

    def inverse_of(self, begin, end):
        require(0 <= begin <= end <= self.cursor, "Inverse refers only to consumed original rows")
        for index in range(end - 1, begin - 1, -1):
            at = 4 * index
            kind = self.words[at]
            require(kind in (1, 2, 3), "Canonical original inverse opcode")
            self.consume(tuple(self.words[at + 1 + j] for j in range(kind)))


def c130_full_bank(bank):
    require(
        type(bank) is list
        and len(bank) == 72
        and all(type(wire) is int for wire in bank)
        and bank == list(range(bank[0], bank[0] + 72)),
        "Canonical contiguous full72 bank",
    )
    return tuple(bank)


def c130_leaf_size(descriptor):
    result = descriptor["qubits"] if "qubits" in descriptor else descriptor["resources"]["qubits"]
    require(type(result) is int and 0 < result <= 16384, "Finite admitted native leaf capacity")
    return result


def c130_helper_body(cursor, operation, arguments, outputs, scratch, parameters):
    """Independent row obligations plus Boolean identities for each actual helper.

    Borrow identity: b_next=(~a & b) XOR (equal(a,b) & b_prev);
    terms are disjoint. Signed order follows by biasing both sign bits.
    SELECT=no XOR (flag AND (yes XOR no)). EQ is an AND of 72
    complemented differences. QROM implements all64 six-bit minterms;
    caller proof separately supplies zero high66 address bits.
    """
    if operation == "CONST":
        require(
            not arguments and len(outputs) == 1 and set(parameters) == {"raw"},
            "Fixed constant helper interface",
        )
        value = parameters["raw"]
        require(type(value) is int and -(1 << 71) <= value < (1 << 71), "Signed72 exact constant")
        for bit in range(72):
            if (value >> bit) & 1:
                cursor.consume((outputs[0][bit],))
    elif operation == "SHIFT4":
        require(len(arguments) == len(outputs) == 1 and not parameters, "Fixed left-shift helper")
        for source_bit in range(68):
            cursor.consume((arguments[0][source_bit], outputs[0][source_bit + 4]))
    elif operation == "ADDRESS34":
        require(len(arguments) == len(outputs) == 1 and not parameters, "Fixed right-shift helper")
        for output_bit in range(38):
            cursor.consume((arguments[0][output_bit + 34], outputs[0][output_bit]))
    elif operation == "SIGN":
        require(len(arguments) == len(outputs) == 1 and not parameters, "One signed flag")
        cursor.consume((arguments[0][71], outputs[0][0]))
    elif operation == "NOT":
        require(len(arguments) == len(outputs) == 1 and not parameters, "One Boolean complement")
        cursor.consume((outputs[0][0],))
        cursor.consume((arguments[0][0], outputs[0][0]))
    elif operation == "AND":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters, "One Boolean conjunction"
        )
        cursor.consume((arguments[0][0], arguments[1][0], outputs[0][0]))
    elif operation == "SELECT":
        require(
            len(arguments) == 3 and len(outputs) == 1 and not parameters and len(scratch) >= 72,
            "Full72 Boolean-controlled selection",
        )
        flag, yes, no = arguments
        for bit, delta in enumerate(scratch[:72]):
            cursor.consume((no[bit], outputs[0][bit]))
            cursor.consume((yes[bit], delta))
            cursor.consume((no[bit], delta))
            cursor.consume((flag[0], delta, outputs[0][bit]))
    elif operation == "EQ":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters and len(scratch) >= 143,
            "All72 equality operands and full prefix history",
        )
        a, b = arguments
        equality_bits, prefixes = scratch[:72], scratch[72:143]
        for bit, history in enumerate(equality_bits):
            cursor.consume((a[bit], history))
            cursor.consume((b[bit], history))
            cursor.consume((history,))
        cursor.consume((equality_bits[0], equality_bits[1], prefixes[0]))
        for bit in range(2, 72):
            cursor.consume((prefixes[bit - 2], equality_bits[bit], prefixes[bit - 1]))
        cursor.consume((prefixes[-1], outputs[0][0]))
    elif operation == "SIGNED_LT":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters and len(scratch) >= 217,
            "Complete signed72 subtraction-borrow comparison",
        )
        a, b = arguments
        equal_bits, complements, borrows = scratch[:72], scratch[72:144], scratch[144:217]
        cursor.consume((a[71],))
        cursor.consume((b[71],))
        for bit in range(72):
            cursor.consume((equal_bits[bit],))
            cursor.consume((a[bit], equal_bits[bit]))
            cursor.consume((b[bit], equal_bits[bit]))
            cursor.consume((complements[bit],))
            cursor.consume((a[bit], complements[bit]))
            cursor.consume((complements[bit], b[bit], borrows[bit + 1]))
            cursor.consume((equal_bits[bit], borrows[bit], borrows[bit + 1]))
        cursor.consume((borrows[72], outputs[0][0]))
        cursor.consume((a[71],))
        cursor.consume((b[71],))
    elif operation == "QROM64x8":
        require(
            len(arguments) == 1
            and len(outputs) == 8
            and set(parameters) == {"table"}
            and len(scratch) >= 5,
            "All64 eight-output signed72 QROM interface",
        )
        table, address = parameters["table"], arguments[0]
        require(
            type(table) is list
            and len(table) == 64
            and all(type(row) is list and len(row) == 8 for row in table),
            "Complete512 lookup literals",
        )
        for code in range(64):
            budget()
            inverted = tuple(bit for bit in range(6) if not ((code >> bit) & 1))
            for bit in inverted:
                cursor.consume((address[bit],))
            cursor.consume((address[0], address[1], scratch[0]))
            for bit in range(2, 6):
                cursor.consume((scratch[bit - 2], address[bit], scratch[bit - 1]))
            for column in range(8):
                value = table[code][column]
                require(
                    type(value) is int and -(1 << 71) <= value < (1 << 71),
                    "Every actual signed72 QROM literal",
                )
                for bit in range(72):
                    if (value >> bit) & 1:
                        cursor.consume((scratch[4], outputs[column][bit]))
            for bit in range(5, 1, -1):
                cursor.consume((scratch[bit - 2], address[bit], scratch[bit - 1]))
            cursor.consume((address[0], address[1], scratch[0]))
            for bit in reversed(inverted):
                cursor.consume((address[bit],))
    else:
        require(False, "Unrecognized native helper; no generic fallback")


def c130_expected_roles():
    """Algebra of the specified total integer function; no wire allocation."""
    raw, zero, one, minus = ("input",), ("const", 0), ("const", 1 << 40), ("const", -(1 << 40))
    clamp = ("select", ("negative", raw), zero, ("select", ("lt", raw, one), raw, one))
    eager = ("select", ("eq", clamp, one), zero, clamp)
    address = ("shr34", eager)
    rescaled, center = ("shl4", eager), ("table", address, 0)
    coefficients = [("table", address, column) for column in range(1, 8)]
    local = ("sub", rescaled, center)
    value = ("table", address, 7)
    horner = []
    for degree in range(5, -1, -1):
        product = ("mul44", value, local)
        following = ("add", product, coefficients[degree])
        horner.append(
            {
                "degree": degree,
                "accumulator": value,
                "local": local,
                "product": product,
                "coefficient": coefficients[degree],
                "sum": following,
            }
        )
        value = following
    rounded = ("round4", value)
    low = ("select", ("lt", rounded, minus), minus, rounded)
    projected = ("select", ("lt", one, low), one, low)
    value, axes = projected, []
    for point, exact in (
        (0, one),
        (1 << 38, zero),
        (1 << 39, minus),
        (3 << 38, zero),
        (1 << 40, one),
    ):
        flag = ("eq", clamp, ("const", point))
        following = ("select", flag, exact, value)
        axes.append(
            {
                "turn": point,
                "point": ("const", point),
                "flag": flag,
                "before": value,
                "after": following,
            }
        )
        value = following
    return {
        "clamped": clamp,
        "eager_Q_to_zero": eager,
        "address": address,
        "rescaled": rescaled,
        "center": center,
        "coefficients": coefficients,
        "local": local,
        "Horner": horner,
        "round_input": horner[-1]["sum"],
        "rounded": rounded,
        "projected": projected,
        "axes": axes,
        "final": value,
    }


def c130_expected_expression():
    return c130_expected_roles()["final"]


def c130_bind_internal_roles(internal, expressions):
    expected = c130_expected_roles()
    require(
        set(internal) == set(expected), "All named descriptor roles have exact independent meanings"
    )

    def meaning(bank):
        key = c130_full_bank(bank)
        require(
            key in expressions, "Internal role points only to an actual consumed full72 SSA bank"
        )
        return expressions[key]

    for name in expected:
        budget()
        if name == "coefficients":
            require(
                type(internal[name]) is list
                and len(internal[name]) == 7
                and [meaning(bank) for bank in internal[name]] == expected[name],
                "Every seven actual coefficient bank has its correct QROM column",
            )
        elif name in ("Horner", "axes"):
            require(
                type(internal[name]) is list and len(internal[name]) == len(expected[name]),
                "Complete fixed Horner and axis stage metadata",
            )
            literal = "degree" if name == "Horner" else "turn"
            for actual, target in zip(internal[name], expected[name], strict=True):
                require(
                    set(actual) == set(target)
                    and type(actual[literal]) is int
                    and actual[literal] == target[literal],
                    "Exact frozen stage index",
                )
                require(
                    all(meaning(actual[key]) == target[key] for key in target if key != literal),
                    "Every actual internal stage pointer has its independently specified algebra",
                )
        else:
            require(
                meaning(internal[name]) == expected[name],
                "Exact named actual internal bank semantics",
            )


def c130_expression(operation, args, parameters, outputs):
    if operation == "CONST":
        return [("const", parameters["raw"])]
    tags = {
        "SIGN": "negative",
        "SIGNED_LT": "lt",
        "SELECT": "select",
        "EQ": "eq",
        "SHIFT4": "shl4",
        "ADDRESS34": "shr34",
        "SUB": "sub",
        "ADD": "add",
        "MUL": "mul44",
        "ROUND": "round4",
        "NOT": "not",
        "AND": "and",
    }
    if operation == "QROM64x8":
        require(outputs == 8, "Complete eight-output table expression")
        return [("table", args[0], column) for column in range(8)]
    require(operation in tags and outputs == 1, "Recognized single-result semantic expression")
    return [(tags[operation], *args)]


def c130_gate_binding(words, descriptor, table, leaves):
    budget()
    require(
        set(leaves) == {"ADD", "SUB", "MUL", "ROUND"},
        "Exactly four externally admitted clean leaves",
    )
    require(
        type(table) is list
        and len(table) == 64
        and all(
            type(row) is list
            and len(row) == 8
            and all(type(value) is int and -(1 << 71) <= value < (1 << 71) for value in row)
            and row[0] == (2 * index + 1) * (1 << 37)
            for index, row in enumerate(table)
        ),
        "All512 exact signed72 table literals and all64 independent F44 centers",
    )
    require(
        descriptor["schema"] == "a14-f44-stage-c-clean-cosine-prototype-v1"
        and descriptor["row_id"] == "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38",
        "One fixed saved clean cosine descriptor",
    )
    rows, wires = len(words) // 4, descriptor["qubits"]
    require(
        descriptor["gate_rows"] == rows
        and descriptor["args"] == [list(range(72))]
        and descriptor["outs"] == [list(range(72, 144))],
        "Actual full72 raw/dirty-output ports",
    )
    workspace = descriptor["shared_private_workspace"]
    capacity = max(c130_leaf_size(leaf["descriptor"]) for leaf in leaves.values())
    require(
        workspace == list(range(144, 144 + capacity))
        and capacity >= 653
        and descriptor["full72_private_leaf_capacity"] == capacity,
        "One exact full reusable private bank",
    )
    next_wire, position = 144 + capacity, 0
    expressions = {tuple(range(72)): ("input",)}
    forward_end = descriptor["forward_rows"][1]
    require(descriptor["forward_rows"] == [0, forward_end], "Forward begins at actual row0")
    cursor = C130SavedRows(words, wires, finish=forward_end)
    for event in descriptor["trace"]:
        budget()
        operation, arguments, outputs = event["op"], event["args"], event["outs"]
        require(
            event["rows"][0] == position == cursor.cursor
            and event["full_private_bank_reused"] is True,
            "Every forward row belongs to one exact contiguous event",
        )
        argument_keys = [c130_full_bank(bank) for bank in arguments]
        require(
            all(bank in expressions for bank in argument_keys),
            "Every argument is prior input/SSA, never dirty output",
        )
        for output in outputs:
            c130_full_bank(output)
            require(
                output == list(range(next_wire, next_wire + 72)),
                "Each result is a fresh monotone full72 SSA bank",
            )
            next_wire += 72
        arity, out_count = len(arguments), len(outputs)
        require(
            72 * (arity + out_count) <= capacity and event["inner_argument_copy_CX"] == 144 * arity,
            "Full copied arguments and private outputs fit the common bank",
        )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        parameters = event.get("params", {})
        if operation in leaves:
            leaf, body_begin = leaves[operation], cursor.cursor
            leaf_descriptor, leaf_words = leaf["descriptor"], leaf["words"]
            size = c130_leaf_size(leaf_descriptor)
            require(
                arity == (1 if operation == "ROUND" else 2)
                and out_count == 1
                and leaf_descriptor["args"]
                == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
                and leaf_descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))],
                "Every complete native clean-leaf full72 ABI",
            )
            require(
                event["leaf_gate_SHA256"] == leaf["gate_SHA256"] and len(leaf_words) % 4 == 0,
                "Leaf occurrence binds the independently admitted exact raw body",
            )
            remap = list(workspace[:size])
            remap[72 * arity : 72 * (arity + 1)] = outputs[0]
            require(
                len(set(remap)) == size, "Native remap is injective, including fresh output bank"
            )
            for index in range(len(leaf_words) // 4):
                if index % 128 == 0:
                    budget()
                at, opcode = 4 * index, leaf_words[4 * index]
                require(
                    opcode in (1, 2, 3)
                    and all(leaf_words[at + 1 + j] == 0 for j in range(opcode, 3)),
                    "Complete canonical admitted primitive body",
                )
                operands = tuple(leaf_words[at + 1 + j] for j in range(opcode))
                require(
                    len(set(operands)) == opcode and all(0 <= wire < size for wire in operands),
                    "Every native operand is valid before remapping",
                )
                cursor.consume(tuple(remap[wire] for wire in operands))
            require(
                event["actual_leaf_rows"] == [body_begin, cursor.cursor],
                "Complete remapped saved primitive interval",
            )
        else:
            body_begin = cursor.cursor
            private_arguments = [workspace[72 * j : 72 * (j + 1)] for j in range(arity)]
            private_outputs = [
                workspace[72 * (arity + j) : 72 * (arity + j + 1)] for j in range(out_count)
            ]
            if operation == "QROM64x8":
                require(
                    parameters == {"table": table},
                    "Every QROM literal equals the externally admitted complete table",
                )
            c130_helper_body(
                cursor,
                operation,
                private_arguments,
                private_outputs,
                workspace[72 * (arity + out_count) :],
                parameters,
            )
            body_end = cursor.cursor
            require(
                event["compute_rows"] == [body_begin, body_end], "Complete consumed helper body"
            )
            for source, target in zip(private_outputs, outputs, strict=True):
                for bit in range(72):
                    cursor.consume((source[bit], target[bit]))
            copy_end = cursor.cursor
            require(event["copy_rows"] == [body_end, copy_end], "Every actual full72 result copy")
            cursor.inverse_of(body_begin, body_end)
            require(
                event["inverse_rows"] == [copy_end, cursor.cursor],
                "Literal complete helper uncomputation",
            )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        position = cursor.cursor
        require(event["rows"][1] == position, "No unconsumed helper/leaf row")
        meanings = c130_expression(
            operation, [expressions[bank] for bank in argument_keys], parameters, out_count
        )
        for output, meaning in zip(outputs, meanings, strict=True):
            expressions[tuple(output)] = meaning
    require(
        position == forward_end
        and next_wire == wires
        and descriptor["SSA_full72_banks"] == len(expressions) + 1,
        "Every allocated SSA/private wire and complete forward row consumed",
    )
    c130_bind_internal_roles(descriptor["internal"], expressions)
    middle_end = forward_end + 72
    require(
        descriptor["output_XOR_rows"] == [forward_end, middle_end]
        and descriptor["literal_global_inverse_rows"] == [middle_end, rows]
        and rows == middle_end + forward_end,
        "Whole clean F/72XOR/F^-1 shape",
    )
    cursor.finish = rows
    result_bank = []
    for bit in range(72):
        offset = 4 * cursor.cursor
        source = words[offset + 1]
        cursor.consume((source, 72 + bit))
        result_bank.append(source)
    require(
        tuple(result_bank) in expressions
        and expressions[tuple(result_bank)] == c130_expected_expression(),
        "Actual descriptor-driven SSA expression is the independently specified "
        "total integer function",
    )
    cursor.inverse_of(0, forward_end)
    require(
        cursor.cursor == rows
        and descriptor["input_preserved"] is True
        and descriptor["dirty_output_XOR"] is True
        and descriptor["private_and_SSA_zero_entry_exit"] is True
        and descriptor["input_full72_signed_clamp_0_to_Q"] is True
        and descriptor["outer_caller_copies_excluded"] is True
        and descriptor["prototype_native_rows_cap"] == 2000000
        and descriptor["prototype_native_wire_cap"] == 16384
        and descriptor["replay_guard_rows"] == 128
        and descriptor["full_financial_or_G2_certificate"] is False
        and descriptor["new_test_credit"] == 0,
        "Whole72 dirty-XOR clean composition and component-only scope",
    )
    budget()
    return {
        "all_actual_rows_consumed": rows,
        "all_actual_allocations_consumed": wires,
        "descriptor_driven_SSA_function_checked": True,
        "actual_global_inverse_checked_row_for_row": True,
        "all_internal_role_pointers_semantically_bound": True,
        "builder_or_MatchingCircuit_called": False,
        "second_array_generated": False,
        "universal_full72_clean_XOR_conditional": True,
        "required_external_premises": [
            "Independent BK72 ADD/SUB full72 clean-map certificates",
            "Independent K signed52x38 MUL and full72 ROUND certificates",
            "Independent all64 eager caller signed/no-wrap/address/low-bit proofs",
        ],
        "program_fixture_credit": 0,
        "financial_G2_or_adoption": False,
    }


def c130_integer_reference(raw, table):
    """Separate integer specification, including negative floor/tie behavior."""
    require(type(raw) is int and 0 <= raw < (1 << 72), "Unsigned full72 reference word")
    value = raw - (1 << 72) if raw & (1 << 71) else raw
    coordinate = max(0, min(1 << 40, value))
    exact_axes = {0: 1 << 40, 1 << 38: 0, 1 << 39: -(1 << 40), 3 << 38: 0, 1 << 40: 1 << 40}
    if coordinate in exact_axes:
        return exact_axes[coordinate] % (1 << 72)
    row = table[coordinate // (1 << 34)]
    delta = 16 * coordinate - row[0]
    result = row[7]
    for index in (6, 5, 4, 3, 2, 1):
        result = (result * delta) // (1 << 44) + row[index]
    quotient, remainder = divmod(result, 16)
    if remainder > 8 or (remainder == 8 and quotient % 2 == 1):
        quotient += 1
    return max(-(1 << 40), min(1 << 40, quotient)) % (1 << 72)


def c130_native_row(words, index, qubits):
    at = 4 * index
    opcode = words[at]
    require(
        type(opcode) is int and opcode in (1, 2, 3), "Actual native opcode is canonical integer"
    )
    operands = tuple(words[at + 1 + position] for position in range(opcode))
    require(
        len(set(operands)) == opcode
        and all(type(wire) is int and 0 <= wire < qubits for wire in operands)
        and all(words[at + 1 + position] == 0 for position in range(opcode, 3)),
        "All actual operands and padding are checked before every replay or schedule use",
    )
    return opcode, operands


def c130_compare_slices(actual, initial, expected_outputs, lane_count):
    require(
        len(expected_outputs) == lane_count and len(actual) == len(initial),
        "Complete logical case-state dimensions",
    )
    for wire in range(len(actual)):
        if wire % 128 == 0:
            budget()
        expected = initial[wire]
        if 72 <= wire < 144:
            bit = wire - 72
            for lane, value in enumerate(expected_outputs):
                expected ^= ((value >> bit) & 1) << lane
        require(
            actual[wire] == expected,
            "Every logical case compares every allocated wire, including all zero history",
        )


def c130_schedule_interval(words, qubits, begin, end):
    budget()
    require(
        len(words) % 4 == 0
        and 0 < len(words) // 4 <= 2000000
        and type(qubits) is int
        and 0 < qubits <= 16384
        and type(begin) is int
        and type(end) is int
        and 0 <= begin <= end <= len(words) // 4,
        "Actual bounded schedule interval",
    )
    t_clock, full_clock, counts = [0] * qubits, [0] * qubits, [0, 0, 0]
    for index in range(begin, end):
        if (index - begin) % 128 == 0:
            budget()
        opcode, actual = c130_native_row(words, index, qubits)
        counts[opcode - 1] += 1
        expanded = (
            C130_CCX_MACRO if opcode == 3 else (("CX", 0, 1),) if opcode == 2 else (("X", 0),)
        )
        for event in expanded:
            affected = tuple(actual[position] for position in event[1:])
            next_t = max(t_clock[wire] for wire in affected) + (1 if event[0] in ("T", "TD") else 0)
            next_full = max(full_clock[wire] for wire in affected) + 1
            for wire in affected:
                t_clock[wire], full_clock[wire] = next_t, next_full
    budget()
    return {
        "rows": [begin, end],
        "source_gates": end - begin,
        "x": counts[0],
        "cx": counts[1],
        "ccx": counts[2],
        "t_count": 7 * counts[2],
        "t_depth": max(t_clock),
        "clifford_t_depth": max(full_clock),
    }


def c130_resources(words, descriptor):
    budget()
    rows, qubits = len(words) // 4, descriptor["qubits"]
    require(
        rows == descriptor["gate_rows"] and rows <= 2000000, "Complete actual saved resource source"
    )
    full = c130_schedule_interval(words, qubits, 0, rows)
    result = {key: value for key, value in full.items() if key != "rows"}
    result.update(
        qubits=qubits,
        clifford_cx=result["cx"] + 6 * result["ccx"],
        clifford_h=2 * result["ccx"],
        schedule="all-to-all ASAP full actual chronological exact7T expansion",
        entire_clean_prototype_not_leaf_sum_estimate=True,
        outer_caller_copies_excluded=True,
    )
    forward_end, reverse_begin = (
        descriptor["forward_rows"][1],
        descriptor["literal_global_inverse_rows"][0],
    )
    forward, inverse, position = [], [], 0
    for event in descriptor["trace"]:
        begin, end = event["rows"]
        require(
            begin == position and begin <= end <= forward_end,
            "Exact contiguous event serial chronology",
        )
        forward.append({"op": event["op"], **c130_schedule_interval(words, qubits, begin, end)})
        position = end
    require(position == forward_end, "Every forward row belongs to one actual serial event")
    output = c130_schedule_interval(words, qubits, forward_end, reverse_begin)
    require(
        output["source_gates"] == output["cx"] == 72 and output["x"] == output["ccx"] == 0,
        "All72 actual dirty-output copy rows paid",
    )
    for event in reversed(descriptor["trace"]):
        begin, end = event["rows"]
        actual_begin, actual_end = (
            reverse_begin + forward_end - end,
            reverse_begin + forward_end - begin,
        )
        inverse.append(
            {"op": event["op"], **c130_schedule_interval(words, qubits, actual_begin, actual_end)}
        )
    all_events = forward + [output] + inverse
    sums = {
        key: sum(event[key] for event in all_events)
        for key in ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")
    }
    require(
        all(sums[key] == result[key] for key in ("source_gates", "x", "cx", "ccx", "t_count")),
        "Both complete scheduling conventions consume exactly the same actual row inventory",
    )
    result["matched_serial_event_chronology"] = {
        "forward_actual_events": forward,
        "output_XOR_actual_event": output,
        "inverse_actual_events": inverse,
        "sums": sums,
        "schedule": "serialize complete helper/leaf events; exact actual7T ASAP within each event",
        "matched_serial_whole_source_comparison_only": True,
        "distinct_from_standalone_ASAP_depth": True,
        "outer_caller_argument_copies_excluded": True,
    }
    budget()
    return result


def c130_phase_shift(vector, exponent):
    result = [0, 0, 0, 0]
    for degree, coefficient in enumerate(vector):
        power = (degree + exponent) % 8
        result[power % 4] += coefficient if power < 4 else -coefficient
    return tuple(result)


def c130_phase_add(mapping, state, vector, sign=1):
    previous = mapping.get(state, (0, 0, 0, 0))
    mapping[state] = tuple(previous[index] + sign * vector[index] for index in range(4))


def c130_ccx_absolute_phase():
    """Exact Z[zeta8]/(zeta8^4+1) coefficients; two Hadamards divide by2.

    Eight input basis columns verify the full operator, including its absolute
    phase. These are proof cases, not the frozen native diagnostic corpus.
    """
    budget()
    require(len(C130_CCX_MACRO) == 15, "One fixed exact15-event macro")
    for basis in range(8):
        budget()
        amplitudes, hadamards = {basis: (1, 0, 0, 0)}, 0
        for event in C130_CCX_MACRO:
            name, operands = event[0], event[1:]
            updated = {}
            if name == "H":
                hadamards += 1
            for state, vector in amplitudes.items():
                if name == "CX":
                    out = state ^ (1 << operands[1]) if state & (1 << operands[0]) else state
                    c130_phase_add(updated, out, vector)
                elif name in ("T", "TD"):
                    shifted = (
                        c130_phase_shift(vector, 1 if name == "T" else -1)
                        if state & (1 << operands[0])
                        else vector
                    )
                    c130_phase_add(updated, state, shifted)
                else:
                    require(name == "H" and len(operands) == 1, "Exact macro event alphabet")
                    bit = operands[0]
                    zero = state & ~(1 << bit)
                    one = zero | (1 << bit)
                    c130_phase_add(updated, zero, vector)
                    c130_phase_add(updated, one, vector, -1 if state & (1 << bit) else 1)
            amplitudes = {state: vector for state, vector in updated.items() if any(vector)}
        expected = basis ^ 4 if basis & 1 and basis & 2 else basis
        require(
            hadamards == 2 and amplitudes == {expected: (2, 0, 0, 0)},
            "Actual15-event macro equals exact CCX with positive absolute unit amplitude",
        )
    budget()
    return {
        "exact_absolute_phase_CCX": True,
        "basis_columns": 8,
        "events": 15,
        "T_or_Tdg_count": 7,
        "CX_count": 6,
        "H_count": 2,
        "cyclotomic_integer_proof": "zeta8^4=-1; common two-H denominator2",
        "relative_or_unknown_global_phase_accepted": False,
        "program_fixture_credit": 0,
    }


def grid_bind_internal_roles(internal, expressions):
    expected = grid_expected_roles()
    require(
        set(internal) == set(expected), "All named descriptor roles have exact independent meanings"
    )

    def meaning(bank):
        key = c130_full_bank(bank)
        require(
            key in expressions, "Internal role points only to an actual consumed full72 SSA bank"
        )
        return expressions[key]

    for name in expected:
        budget()
        if name == "coefficients":
            require(
                type(internal[name]) is list
                and len(internal[name]) == 7
                and [meaning(bank) for bank in internal[name]] == expected[name],
                "Every seven actual coefficient bank has its correct QROM column",
            )
        elif name in ("Horner", "axes"):
            require(
                type(internal[name]) is list and len(internal[name]) == len(expected[name]),
                "Complete fixed Horner and axis stage metadata",
            )
            literal = "degree" if name == "Horner" else "turn"
            for actual, target in zip(internal[name], expected[name], strict=True):
                require(
                    set(actual) == set(target)
                    and type(actual[literal]) is int
                    and actual[literal] == target[literal],
                    "Exact frozen stage index",
                )
                require(
                    all(meaning(actual[key]) == target[key] for key in target if key != literal),
                    "Every actual internal stage pointer has its independently specified algebra",
                )
        else:
            require(
                meaning(internal[name]) == expected[name],
                "Exact named actual internal bank semantics",
            )


def grid_gate_binding(words, descriptor, table, leaves):
    budget()
    require(
        set(leaves) == {"ADD", "SUB", "MUL", "ROUND"},
        "Exactly four externally admitted clean leaves",
    )
    require(
        type(table) is list
        and len(table) == 64
        and all(
            type(row) is list
            and len(row) == 8
            and all(type(value) is int and -(1 << 71) <= value < (1 << 71) for value in row)
            and row[0] == (2 * index + 1) * (1 << 37)
            for index, row in enumerate(table)
        ),
        "All512 exact signed72 table literals and all64 independent F44 centers",
    )
    require(
        descriptor["schema"] == "f44-caller-grid-no-axis-no-input-clamp-clean-prototype-v1"
        and descriptor["row_id"] == GRID_ROW_ID,
        "One fixed saved clean cosine descriptor",
    )
    require(
        descriptor["caller_grid_contract_id"] == GRID_CONTRACT_ID
        and descriptor["certificate_scope"] == "PROMISED_CALLER_GRID_ONLY"
        and descriptor["axis_tail_omitted"] is True
        and descriptor["generic_full72_equivalence_claimed"] is False
        and descriptor["actual_coherent32_preparation_array_audited"] is False,
        "Only separately pinned caller-grid certificate, no generic72 or prepared array claim",
    )
    rows, wires = len(words) // 4, descriptor["qubits"]
    require(
        descriptor["gate_rows"] == rows
        and descriptor["args"] == [list(range(72))]
        and descriptor["outs"] == [list(range(72, 144))],
        "Actual full72 raw/dirty-output ports",
    )
    workspace = descriptor["shared_private_workspace"]
    capacity = max(c130_leaf_size(leaf["descriptor"]) for leaf in leaves.values())
    require(
        workspace == list(range(144, 144 + capacity))
        and capacity >= 653
        and descriptor["full72_private_leaf_capacity"] == capacity,
        "One exact full reusable private bank",
    )
    next_wire, position = 144 + capacity, 0
    expressions = {tuple(range(72)): ("input",)}
    forward_end = descriptor["forward_rows"][1]
    require(descriptor["forward_rows"] == [0, forward_end], "Forward begins at actual row0")
    cursor = C130SavedRows(words, wires, finish=forward_end)
    for event in descriptor["trace"]:
        budget()
        operation, arguments, outputs = event["op"], event["args"], event["outs"]
        require(
            event["rows"][0] == position == cursor.cursor
            and event["full_private_bank_reused"] is True,
            "Every forward row belongs to one exact contiguous event",
        )
        argument_keys = [c130_full_bank(bank) for bank in arguments]
        require(
            all(bank in expressions for bank in argument_keys),
            "Every argument is prior input/SSA, never dirty output",
        )
        for output in outputs:
            c130_full_bank(output)
            require(
                output == list(range(next_wire, next_wire + 72)),
                "Each result is a fresh monotone full72 SSA bank",
            )
            next_wire += 72
        arity, out_count = len(arguments), len(outputs)
        require(
            72 * (arity + out_count) <= capacity and event["inner_argument_copy_CX"] == 144 * arity,
            "Full copied arguments and private outputs fit the common bank",
        )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        parameters = event.get("params", {})
        if operation in leaves:
            leaf, body_begin = leaves[operation], cursor.cursor
            leaf_descriptor, leaf_words = leaf["descriptor"], leaf["words"]
            size = c130_leaf_size(leaf_descriptor)
            require(
                arity == (1 if operation == "ROUND" else 2)
                and out_count == 1
                and leaf_descriptor["args"]
                == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
                and leaf_descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))],
                "Every complete native clean-leaf full72 ABI",
            )
            require(
                event["leaf_gate_SHA256"] == leaf["gate_SHA256"] and len(leaf_words) % 4 == 0,
                "Leaf occurrence binds the independently admitted exact raw body",
            )
            remap = list(workspace[:size])
            remap[72 * arity : 72 * (arity + 1)] = outputs[0]
            require(
                len(set(remap)) == size, "Native remap is injective, including fresh output bank"
            )
            for index in range(len(leaf_words) // 4):
                if index % 128 == 0:
                    budget()
                at, opcode = 4 * index, leaf_words[4 * index]
                require(
                    opcode in (1, 2, 3)
                    and all(leaf_words[at + 1 + j] == 0 for j in range(opcode, 3)),
                    "Complete canonical admitted primitive body",
                )
                operands = tuple(leaf_words[at + 1 + j] for j in range(opcode))
                require(
                    len(set(operands)) == opcode and all(0 <= wire < size for wire in operands),
                    "Every native operand is valid before remapping",
                )
                cursor.consume(tuple(remap[wire] for wire in operands))
            require(
                event["actual_leaf_rows"] == [body_begin, cursor.cursor],
                "Complete remapped saved primitive interval",
            )
        else:
            body_begin = cursor.cursor
            private_arguments = [workspace[72 * j : 72 * (j + 1)] for j in range(arity)]
            private_outputs = [
                workspace[72 * (arity + j) : 72 * (arity + j + 1)] for j in range(out_count)
            ]
            if operation == "QROM64x8":
                require(
                    parameters == {"table": table},
                    "Every QROM literal equals the externally admitted complete table",
                )
            c130_helper_body(
                cursor,
                operation,
                private_arguments,
                private_outputs,
                workspace[72 * (arity + out_count) :],
                parameters,
            )
            body_end = cursor.cursor
            require(
                event["compute_rows"] == [body_begin, body_end], "Complete consumed helper body"
            )
            for source, target in zip(private_outputs, outputs, strict=True):
                for bit in range(72):
                    cursor.consume((source[bit], target[bit]))
            copy_end = cursor.cursor
            require(event["copy_rows"] == [body_end, copy_end], "Every actual full72 result copy")
            cursor.inverse_of(body_begin, body_end)
            require(
                event["inverse_rows"] == [copy_end, cursor.cursor],
                "Literal complete helper uncomputation",
            )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        position = cursor.cursor
        require(event["rows"][1] == position, "No unconsumed helper/leaf row")
        meanings = c130_expression(
            operation, [expressions[bank] for bank in argument_keys], parameters, out_count
        )
        for output, meaning in zip(outputs, meanings, strict=True):
            expressions[tuple(output)] = meaning
    require(
        position == forward_end
        and next_wire == wires
        and descriptor["SSA_full72_banks"] == len(expressions) + 1,
        "Every allocated SSA/private wire and complete forward row consumed",
    )
    grid_bind_internal_roles(descriptor["internal"], expressions)
    middle_end = forward_end + 72
    require(
        descriptor["output_XOR_rows"] == [forward_end, middle_end]
        and descriptor["literal_global_inverse_rows"] == [middle_end, rows]
        and rows == middle_end + forward_end,
        "Whole clean F/72XOR/F^-1 shape",
    )
    cursor.finish = rows
    result_bank = []
    for bit in range(72):
        offset = 4 * cursor.cursor
        source = words[offset + 1]
        cursor.consume((source, 72 + bit))
        result_bank.append(source)
    require(
        tuple(result_bank) in expressions
        and expressions[tuple(result_bank)] == grid_expected_expression(),
        "Actual descriptor-driven SSA expression is the independently specified "
        "total integer function",
    )
    cursor.inverse_of(0, forward_end)
    require(
        cursor.cursor == rows
        and descriptor["input_preserved"] is True
        and descriptor["dirty_output_XOR"] is True
        and descriptor["private_and_SSA_zero_entry_exit"] is True
        and descriptor["input_full72_signed_clamp_0_to_Q"] is False
        and descriptor["input_clamp_and_eager_Q_gate_events_omitted"] is True
        and descriptor["outer_caller_copies_excluded"] is True
        and descriptor["prototype_native_rows_cap"] == 2000000
        and descriptor["prototype_native_wire_cap"] == 16384
        and descriptor["replay_guard_rows"] == 128
        and descriptor["full_financial_or_G2_certificate"] is False
        and descriptor["new_test_credit"] == 0,
        "Whole72 dirty-XOR clean composition and component-only scope",
    )
    budget()
    return {
        "all_actual_rows_consumed": rows,
        "all_actual_allocations_consumed": wires,
        "descriptor_driven_SSA_function_checked": True,
        "actual_global_inverse_checked_row_for_row": True,
        "all_internal_role_pointers_semantically_bound": True,
        "builder_or_MatchingCircuit_called": False,
        "second_array_generated": False,
        "caller_grid_full72_interface_clean_XOR_conditional": True,
        "required_external_premises": [
            "Independent BK72 ADD/SUB full72 clean-map certificates",
            "Independent K signed52x38 MUL and full72 ROUND certificates",
            "Independent all64 eager caller signed/no-wrap/address/low-bit proofs",
            "Prepared Q32 grid at full72 component input; a future whole-source "
            "40-active/32-zero argument bridge must be emitted and audited separately",
        ],
        "program_fixture_credit": 0,
        "financial_G2_or_adoption": False,
    }


def grid_slice_initial(qubits, cases):
    require(
        type(qubits) is int and 144 <= qubits <= 16384 and len(cases) == 128,
        "Fixed finite bit-slice lanes",
    )
    state = [0] * qubits
    for lane, (value, dirty) in enumerate(cases):
        budget()
        for bit in range(72):
            state[bit] |= ((value >> bit) & 1) << lane
            state[72 + bit] |= ((dirty >> bit) & 1) << lane
    return state


def grid_bit_sweep(words, state, lane_count, inverse=False):
    budget()
    require(
        len(words) % 4 == 0
        and 0 < len(words) // 4 <= 2000000
        and 144 <= len(state) <= 16384
        and lane_count == 128
        and type(inverse) is bool,
        "Complete bounded bit-slice sweep",
    )
    full = (1 << lane_count) - 1
    for wire, value in enumerate(state):
        if wire % 128 == 0:
            budget()
        require(
            type(value) is int and 0 <= value <= full,
            "Every allocated wire contains exactly the admitted lane bits",
        )
    indices = range(len(words) // 4 - 1, -1, -1) if inverse else range(len(words) // 4)
    for step, index in enumerate(indices):
        if step % 128 == 0:
            budget()
        opcode, operands = c130_native_row(words, index, len(state))
        if opcode == 1:
            state[operands[0]] ^= full
        elif opcode == 2:
            state[operands[1]] ^= state[operands[0]]
        else:
            state[operands[2]] ^= state[operands[0]] & state[operands[1]]
    budget()


def flags():
    return dict(
        caller_typed_component_only=True,
        caller_grid_entry_promise_required=True,
        actual_coherent32_preparation_array_audited=False,
        whole_source_40_active_to72_zero_padded_bridge_audited=False,
        generic_full72_map_equivalence_claimed=False,
        whole_financial_source_emitted=False,
        new_test_credit=0,
        new_credited_gate_replays=0,
        new_price_samples=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        quantum_advantage=False,
        global_financial_gate_emission_authorized=False,
        original_scientific_receipts_unchanged=True,
        previous_A14_rejected_rows_unchanged=True,
        generic_StageC_resource_gate_passed=False,
        generic_StageC_row_status="REJECTED",
        new_QROM_release_authorized=False,
        input_clamp_and_eager_Q_gate_events_omitted=True,
        whole_source_capped_depth_transfer=False,
    )


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
            "Stdlib-only component; no numerical package or historical scientific imports")
    require(not any(name.startswith("research.")
                    and name not in {__name__, "research.limitation_program_20261001"}
                    for name in sys.modules), "No imported historical builder/producer/auditor")
    if GRID_MODULE in sys.modules:
        require(_SCIENCE_ADMITTED, "New helper only after full admission")
        require(canonical(sys.modules[GRID_MODULE].__file__, fresh=True) == GRID_HELPER,
                "Only new externally pinned helper origin")
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(not lexical.is_relative_to(_EXCLUDED_SCOPE[0])
                    and not lexical.resolve(strict=False).is_relative_to(_EXCLUDED_SCOPE[1]),
                    "No excluded runtime origin or cache")
            if not lexical.is_file():
                base_lib = Path(sys.base_prefix) / "Lib"
                require(attribute == "__cached__" and not lexical.exists() and not lexical.is_symlink()
                        and lexical.resolve(strict=False) == lexical,
                        "Missing loaded sources rejected; only a physically absent loaded cache")
                require(lexical in _ABSENT_RUNTIME
                        or (lexical.is_relative_to(base_lib)
                            and not lexical.is_relative_to(base_lib / "site-packages")),
                        "Absent loaded cache is declared or inside current standard Lib")
                _ABSENT_RUNTIME.add(lexical)
                continue
            actual = canonical(lexical, fresh=True)
            if actual.is_relative_to(RESEARCH):
                require(actual in {AUTHOR, GRID_HELPER} or actual in _CODE_CACHE_EXPECTED,
                        "Historical scientific sources are reference bytes only")
            key = key_for(actual)
            mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
            require(key in mapping, "All loaded origins have an expectation BEFORE the first check")
            require(digest(actual, fresh=True, already_resolved=True) == mapping[key],
                    "Every fresh loaded source/cache equals its prior frozen expectation")


def admission(ready_sha):
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-f44-q32-preparation-compact40-wrapper-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "Separate ROOT scientific component release required",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in OWNERS.items()}
        and ready["completed_owner_complete_counts"]
        == {name: item[1] for name, item in OWNERS.items()},
        "All ten externally fixed complete owners; exact fresh route and StageC caps",
    )
    require(
        ready["caller_typed_native_component_execution_authorized"] is True
        and ready["caller_grid_entry_promise_required"] is True
        and ready["actual_coherent32_preparation_array_audited"] is False
        and ready["financial_adoption"] is False
        and ready["fixture_credit"] == 0,
        "Only conditional prepared-grid component, no whole-source or generic72 release",
    )
    own = ready["author_method_SHA256"]
    require(
        set(own) == {AUTHOR.name, GRID_HELPER.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly four separately frozen new authors",
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "f44-q32-preparation-compact40-wrapper-preflight-v1"
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["completed_owner_manifest_SHA256"] == ready["completed_owner_manifest_SHA256"]
        and policy["completed_owner_complete_counts"] == ready["completed_owner_complete_counts"]
        and policy["integer_decimal_digit_limit"] == INTEGER_DECIMAL_DIGITS
        and policy["integer_serialization_bit_cap"] == INTEGER_SERIALIZATION_BITS
        and policy["author_SHA256"] == own[AUTHOR.name]
        and policy["helper_SHA256"] == own[GRID_HELPER.name]
        and policy["method_SHA256"] == own[METHOD_DOC.name]
        and policy["grid_input_cases_dirty_patterns_logical_lanes"] == [64, 2, 128]
        and policy["physical_whole_array_sweeps"] == 2
        and policy["whole_source_capped_depth_transfer"] is False,
        "Exact fixed component scope and bounded representation",
    )
    require(
        ready["interpreter_expected_SHA256"] == INTERPRETER_PINS, "Both original fixed interpreters"
    )
    manifests = {name: packet(name, pin, counts) for name, (pin, counts) in OWNERS.items()}
    require(
        ready["startup_original_expected_files"]
        == policy["startup_original_expected_files"] == STARTUP_EXPECTED
        and ready["startup_only_additional_runtime_cache_paths"]
        == policy["startup_only_additional_runtime_cache_paths"] == list(STARTUP_CACHE_KEYS),
        "Only finite original expected startup source/pth/cache bootstrap is authorized",
    )
    for name, manifest in manifests.items():
        for key, record in STARTUP_EXPECTED.items():
            budget(admission=True)
            require(
                manifest["frozen_inputs"].get(key) == record["SHA256"],
                "Each of ALL ten original owners binds each startup expected byte SHA",
            )
    for name in (SOURCE_NAME, AUDIT_NAME):
        component_scope(
            manifests[name],
            "a14-f44-stage-c-primary90-manifest-v3"
            if name == SOURCE_NAME
            else "a14-f44-stage-c-independent130-manifest-v1",
        )
    require(
        manifests[AUDIT_NAME]["producer_manifest_SHA256"] == SOURCE_SHA
        and manifests[AUDIT_NAME]["producer_complete_counts"] == SOURCE_COUNTS
        and manifests[AUDIT_NAME]["row_status"] == "REJECTED",
        "Same completed generic Stage C resource rejection",
    )
    final = manifests[FINAL_ROOT_NAME]
    require(
        final["schema"] == "a14-f44-stage-c-root-integrity-manifest-v1"
        and final["source_manifest_SHA256"] == SOURCE_SHA
        and final["audit_manifest_SHA256"] == ROOT_DECLARED_AUDIT_SHA
        and final["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in OWNERS.items() if name not in (FINAL_ROOT_NAME, AXIS_NAME, CLAMP_NAME)}
        and final["completed_owner_complete_counts"]
        == {name: item[1] for name, item in OWNERS.items() if name not in (FINAL_ROOT_NAME, AXIS_NAME, CLAMP_NAME)},
        "Original final ROOT whole-map integrity scope, not new array approval",
    )
    source_ready = read(bind(SOURCE_READY, SOURCE_READY_SHA))
    audit_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    final_ready = read(bind(FINAL_ROOT_READY, FINAL_ROOT_READY_SHA))
    require(
        source_ready["schema"] == "root-a14-f44-cosine-stage-c-READY-v3"
        and source_ready["author_method_SHA256"] == SOURCE_AUTHORS
        and source_ready["output"] == SOURCE.relative_to(ROOT).as_posix(),
        "Immutable generic producer release",
    )
    require(
        audit_ready["schema"] == "root-a14-f44-cosine-stage-c-audit-READY-v1"
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS
        and audit_ready["producer_manifest_SHA256"] == SOURCE_SHA
        and audit_ready["producer_complete_counts"] == SOURCE_COUNTS
        and audit_ready["output"] == AUDIT.relative_to(ROOT).as_posix(),
        "Immutable independent130 release",
    )
    require(
        final_ready["schema"] == "root-a14-f44-stage-c-integrity-READY-v1"
        and final_ready["author_method_SHA256"] == FINAL_ROOT_AUTHORS
        and final_ready["limits_CPU_admission_wall"] == [180, 150, 600]
        and final_ready["output"] == (PROGRAM / FINAL_ROOT_NAME).relative_to(ROOT).as_posix(),
        "Exact historical ROOT release; its caps are not the new scientific caps",
    )
    originals = {
        name: item[0]
        for name, item in OWNERS.items()
        if name not in (SOURCE_NAME, AUDIT_NAME, FINAL_ROOT_NAME, AXIS_NAME, CLAMP_NAME)
    }
    original_counts = {
        name: item[1]
        for name, item in OWNERS.items()
        if name not in (SOURCE_NAME, AUDIT_NAME, FINAL_ROOT_NAME, AXIS_NAME, CLAMP_NAME)
    }
    for release in (source_ready, audit_ready):
        require(
            release["completed_prerequisite_manifest_SHA256"] == originals
            and release["completed_prerequisite_complete_counts"] == original_counts,
            "All original five native/numerical premise owners retained",
        )
    for authors in (SOURCE_AUTHORS, AUDIT_AUTHORS, FINAL_ROOT_AUTHORS):
        for name, expected in authors.items():
            bind(RESEARCH / name, expected)
    for release, sources in (
        (source_ready, [RESEARCH / "experiment_f44_cosine_stage_c_v3.py", BUILDER]),
        (audit_ready, [RESEARCH / "audit_f44_cosine_stage_c_v1.py"]),
        (final_ready, [RESEARCH / "verify_f44_cosine_stage_c_root_v1.py"]),
    ):
        code_caches(
            sources,
            release["existing_new_code_cache_SHA256"],
            release["absent_new_code_cache_paths"],
        )
    for key, pin, sources in HISTORICAL_CACHE_RELEASES:
        release = read(bind(ROOT / key, pin))
        code_caches(
            [RESEARCH / name for name in sources],
            release["existing_new_code_cache_SHA256"],
            release["absent_new_code_cache_paths"],
        )
    axis_code_caches(
        [AUTHOR, GRID_HELPER],
        ready["existing_new_code_cache_SHA256"],
        ready["absent_new_code_cache_paths"],
    )
    admit_prior_failure(ready, policy)
    admit_axis_preoutput_history(ready, policy)
    bind(ACTUAL_AUDIT_ROOT, ACTUAL_AUDIT_ROOT_SHA)
    for key, expected in GRID_DESIGN_PINS.items():
        bind(ROOT / key, expected)
    require(
        policy["grid_design_expected_SHA256"] == GRID_DESIGN_PINS,
        "Same peer-reviewed conditional grid design",
    )
    design = read(ROOT / ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.json")
    legacy_path = ROOT / design["original_evidence"]["A10_original_flat_manifest"]["path"]
    require(
        _FROZEN[key_for(legacy_path)]
        == design["original_evidence"]["A10_original_flat_manifest"]["SHA256"],
        "Original A10 flat manifest remains an admitted provenance reference",
    )
    legacy = read(legacy_path)
    directory = ROOT / design["original_evidence"]["original_executed_code_directory"]
    for name, expected in design["original_evidence"][
        "original_executed_code_owned_SHA256"
    ].items():
        require(
            legacy["executed_code\\" + name] == expected,
            "Selected historical ABI text has original manifest membership",
        )
        bind(directory / name, expected)
    for key, expected in ready["static_review_expected_SHA256"].items():
        require(
            key.startswith(".context/") and ".." not in Path(key).parts, "ROOT-local static review"
        )
        bind(ROOT / key, expected)
    return ready, policy


def independent_input_bytes(path):
    global _HASH_WORK
    budget()
    actual = canonical(path)
    key = key_for(actual)
    expected = _FROZEN.get(key) if actual.is_relative_to(ROOT) else _EXTERNAL.get(key)
    if actual.is_relative_to(OUTPUT):
        require(
            actual == OUTPUT / "preparation_wrapper.gates.bin",
            "Only current owned complete native array may be interpreted",
        )
        expected = _OUTPUT_NATIVE_EXPECTED.get(actual)
    require(
        expected is not None and digest(actual) == expected,
        "Admitted original or own full native bytes",
    )
    before = fingerprint(actual)
    require(0 < before[2] <= MAX_OWN_BYTES, "Bounded native or original text input")
    parts, total = [], 0
    with actual.open("rb") as stream:
        while block := stream.read(65536):
            budget()
            total += len(block)
            _HASH_WORK += len(block)
            require(
                total <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                "All interpretation read bytes charged",
            )
            parts.append(block)
    result = b"".join(parts)
    require(
        total == before[2]
        and fingerprint(actual) == before
        and hashlib.sha256(result).hexdigest() == expected,
        "Stable whole admitted native input",
    )
    return result


def helper_text_delta_guard():
    old_text = independent_input_bytes(AXIS_HELPER).decode("utf-8")
    new_text = independent_input_bytes(GRID_HELPER).decode("utf-8")
    old, new = ast.parse(old_text), ast.parse(new_text)
    old_defs = {node.name: node for node in old.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    new_defs = {node.name: node for node in new.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    names = ("require", "Circuit", "leaf_size", "Prototype", "helper_compute")
    require(set(old_defs) == set(new_defs) == set(names) | {"build_caller_grid_cosine"},
            "Exactly the original five retained definitions and one changed builder")
    for name in names:
        require(ast.dump(old_defs[name], include_attributes=False)
                == ast.dump(new_defs[name], include_attributes=False),
                "Every retained emitter/native/helper definition exact frozen axis AST")
    before = ast.get_source_segment(old_text, old_defs["build_caller_grid_cosine"])
    after = ast.get_source_segment(new_text, new_defs["build_caller_grid_cosine"])
    require(after.count(CLAMP_NEW_PREFIX) == 1 and before.count(CLAMP_OLD_PREFIX) == 1,
            "Only fixed initial clamp-prefix substitution")
    restored = after.replace(CLAMP_NEW_PREFIX, CLAMP_OLD_PREFIX)
    require(restored.count('"schema": "f44-caller-grid-no-axis-no-input-clamp-clean-prototype-v1"') == 1,
            "Only the new promised-map descriptor schema")
    restored = restored.replace('"schema": "f44-caller-grid-no-axis-no-input-clamp-clean-prototype-v1"',
                                '"schema": "f44-caller-grid-no-axis-clean-prototype-v1"')
    new_flag = '"input_full72_signed_clamp_0_to_Q": False,\n        "input_clamp_and_eager_Q_gate_events_omitted": True,'
    require(restored.count(new_flag) == 1, "Only explicit clamp-event omission metadata")
    restored = restored.replace(new_flag, '"input_full72_signed_clamp_0_to_Q": True,')
    require(ast.dump(ast.parse(restored), include_attributes=False)
            == ast.dump(ast.parse(before), include_attributes=False),
            "Complete builder inverse delta restores frozen axis AST")
    return {"retained_definition_AST_exact": list(names),
            "entire_builder_inverse_prefix_and_descriptor_delta_AST_exact": True,
            "zero_CONST_and_six_input_clamp_eager_events_only_removed": True,
            "new_helper_expected_SHA256": _FROZEN[key_for(GRID_HELPER)],
            "scientific_functions_evaluated_by_text_guard": False, **flags()}


def caller_binding_inventory():
    binding = read(SOURCE / "original_source_binding.json")
    records = {}
    for case, expected in (("B4x12", (30, 60)), ("B8x52", (234, 468))):
        budget(admission=True)
        saved = binding["cases"][case]
        target, source, schedule = (
            read(ROOT / saved[k]) for k in ("target_path", "source_path", "schedule_path")
        )
        require(
            target["width"] == source["word_width"] == 72
            and target["fraction_bits"] == source["fraction_bits"] == 40,
            "Same full72 original native target",
        )
        require(
            schedule["format"] == "compact-clean-xor-capped-wave-schedule-v7"
            and schedule["input_contract"]
            == "Nonnegative raw bit patterns within each declared input bit width",
            "Explicit original preparation contract, not a variable-name inference",
        )
        require(
            len(target["nodes"]) <= 100000 and len(source["forward_calls"]) <= 100000,
            "Bounded complete original structural inventory",
        )
        locations = {value: node for node in target["nodes"] for value in node["out"]}
        calls = {value: call for call in source["forward_calls"] for value in call["out"]}
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            source["inputs"] == inputs and len(inputs) == expected[1],
            "All original input allocations and pair roles",
        )
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        require(len(noninputs) == len(source["forward_calls"]), "Every original call retained")
        for index, (node, call) in enumerate(zip(noninputs, source["forward_calls"], strict=True)):
            if index % 128 == 0:
                budget(admission=True)
            require(
                node["args"] == call["args"] and node["out"] == call["out"],
                "Whole actual ordered call/SSA mapping",
            )
        arguments = []
        require(len(saved["pair_scopes"]) == expected[0], "Every complete original joint pair")
        for index, pair in enumerate(saved["pair_scopes"]):
            budget(admission=True)
            raw_u, raw_v = pair["raw_uniform_values"]
            require(
                pair["raw_uniform_values"]
                == [inputs[2 * index]["out"][0], inputs[2 * index + 1]["out"][0]],
                "Complete ordered prepared q32 input pairing",
            )
            for raw in (raw_u, raw_v):
                node = locations[raw]
                require(
                    node["op"] == "input"
                    and node["params"]["bits"] == 32
                    and node["params"]["preparation"] == "uniform"
                    and schedule["widths"][raw] == 32,
                    "Native retained32 preparation promise and zero-padding obligation",
                )
            midpoint, wrapped = [item["input"] for item in pair["cosines"]]
            arguments.extend((midpoint, wrapped))
            node = locations[midpoint]
            shifts = [value for value in node["args"] if locations[value]["op"] == "bits"]
            constants = [value for value in node["args"] if locations[value]["op"] == "const"]
            require(
                node["op"] == "add" and len(shifts) == len(constants) == 1,
                "Exact original midpoint chain",
            )
            shift = locations[shifts[0]]
            require(
                shift["args"] == [raw_v]
                and shift["params"] == {"shift": -8, "width": 72, "signed": False}
                and locations[constants[0]]["params"] == {"value": 128},
                "Unsigned raw32 left8 plus literal midpoint128",
            )
            wrap = locations[wrapped]
            require(
                wrap["op"] == "bits"
                and wrap["params"] == {"shift": 0, "width": 40, "signed": False}
                and len(wrap["args"]) == 1,
                "Original sole low40 wrap",
            )
            summed = locations[wrap["args"][0]]
            other = [value for value in summed["args"] if value != midpoint]
            require(
                summed["op"] == "add"
                and midpoint in summed["args"]
                and len(other) == 1
                and locations[other[0]]["op"] == "const"
                and locations[other[0]]["params"] == {"value": 824633720832},
                "Same midpoint plus exact3Qquarter; no independent sine draw",
            )
            require(
                schedule["widths"][midpoint] == schedule["widths"][wrapped] == 40
                and schedule["widths"][wrap["args"][0]] == 41,
                "Original native m/sum/w storage obligations unchanged",
            )
            for value in (shifts[0], constants[0], midpoint, other[0], wrap["args"][0], wrapped):
                node, call = locations[value], calls[value]
                require(
                    node["args"] == call["args"]
                    and node["out"] == call["out"]
                    and call["argument_copy_cx"] == {0: 0, 1: 144, 2: 288}[len(node["args"])],
                    "Every original conversion call/copy record unchanged",
                )
        require(
            arguments == saved["cosine_argument_values"] and len(arguments) == expected[1],
            "All original cosine m/w callers bound",
        )
        records[case] = {
            "all_joint_pairs": expected[0],
            "all_cosine_callers": expected[1],
            "full_actual_caller_ABI_joined": True,
            "all_argument_ancestors_and_original_storage_retained": True,
        }
    return {
        "cases": records,
        "caller_grid_contract_id": GRID_CONTRACT_ID,
        "entry_promise_required": True,
        "actual_coherent32_preparation_array_audited": False,
        "symbolic_grid": "256*n+128 with0<=n<2^32; wrapped branch is a permutation",
        "axis_equalities_constant_false_on_prepared_grid": True,
        **flags(),
    }


def grid_expected_roles():
    """Independent promised-domain algebra; omitted roles alias the actual input."""
    raw, one, minus = ("input",), ("const", 1 << 40), ("const", -(1 << 40))
    address = ("shr34", raw)
    rescaled, center = ("shl4", raw), ("table", address, 0)
    coefficients = [("table", address, column) for column in range(1, 8)]
    local, value = ("sub", rescaled, center), ("table", address, 7)
    horner = []
    for degree in range(5, -1, -1):
        product = ("mul44", value, local)
        following = ("add", product, coefficients[degree])
        horner.append({"degree": degree, "accumulator": value, "local": local,
                       "product": product, "coefficient": coefficients[degree], "sum": following})
        value = following
    rounded = ("round4", value)
    low = ("select", ("lt", rounded, minus), minus, rounded)
    projected = ("select", ("lt", one, low), one, low)
    return {"clamped": raw, "eager_Q_to_zero": raw, "address": address,
            "rescaled": rescaled, "center": center, "coefficients": coefficients,
            "local": local, "Horner": horner, "round_input": horner[-1]["sum"],
            "rounded": rounded, "projected": projected, "axes": [], "final": projected}


def grid_expected_expression():
    return grid_expected_roles()["final"]


def grid_fixed_inputs():
    # Exactly64 input values fixed before emission. No tests or calculations run on import.
    values = []
    for segment in range(64):
        if segment in (0, 16, 32, 48):
            value = segment * (1 << 34) + 128
        elif segment in (15, 31, 47, 63):
            value = (segment + 1) * (1 << 34) - 128
        else:
            value = segment * (1 << 34) + (1 << 33) + 128
        require(
            128 <= value <= (1 << 40) - 128 and value % 256 == 128 and value >> 34 == segment,
            "Every fixed case belongs to the full prepared grid and exact designated segment",
        )
        values.append(value)
    require(len(values) == len(set(values)) == 64, "Exactly64 distinct complete-grid inputs")
    return tuple(values)


def grid_fixed_diagnostics(words, descriptor, table):
    values, mask = grid_fixed_inputs(), (1 << 72) - 1
    cases = [(value, dirty) for value in values for dirty in (0, mask)]
    require(len(cases) == 128, "Exactly64 complete-grid inputs times two full72 dirty patterns")
    initial = grid_slice_initial(descriptor["qubits"], cases)
    current = list(initial)
    expected = [c130_integer_reference(value, table) for value, _ in cases]
    grid_bit_sweep(words, current, 128)
    c130_compare_slices(current, initial, expected, 128)
    grid_bit_sweep(words, current, 128, inverse=True)
    require(current == initial, "Every allocated wire restores for all128 actual reverse lanes")
    return {
        "input_case_count": 64,
        "dirty_patterns": [0, mask],
        "logical_forward_calls": 128,
        "logical_reverse_calls": 128,
        "physical_whole_array_sweeps": 2,
        "logical_case_count": 128,
        "inputs": list(values),
        "full72_input_dirty_output_private_and_SSA_forward_reverse_compared": True,
        "same_fixed_case_formula_no_adaptive_expansion": True,
        "producer_reference_or_generic_replay_called": False,
        "new_standalone_round_corpus": False,
        "program_fixture_credit": 0,
        **flags(),
    }


def actual_axis_only_array_delta(words, descriptor):
    """Consume the immutable axis array via an explicit wire/SSA alias map; no emission."""
    original = read(AXIS_SOURCE / "prototype_descriptor.json")
    record = read(AXIS_SOURCE / "native_gate_array.json")
    require(original["schema"] == "f44-caller-grid-no-axis-clean-prototype-v1"
            and original["internal"]["axes"] == []
            and len(original["trace"]) >= 9
            and [event["op"] for event in original["trace"][:9]]
            == ["CONST", "CONST", "CONST", "SIGN", "SIGNED_LT", "SELECT", "SELECT", "EQ", "SELECT"],
            "Exactly three saved constants and six original initial clamp/eager events")
    prefix = original["trace"][:9]
    zero, one, minus, sign, below, upper, clamped, is_q, eager = [event["outs"][0] for event in prefix]
    require([event["params"] for event in prefix[:3]] == [{"raw": 0}, {"raw": 1 << 40}, {"raw": -(1 << 40)}]
            and [event["args"] for event in prefix[3:]]
            == [[list(range(72))], [list(range(72)), one], [below, list(range(72)), one],
                [sign, zero, upper], [clamped, one], [is_q, zero, clamped]]
            and original["internal"]["clamped"] == clamped
            and original["internal"]["eager_Q_to_zero"] == eager,
            "All removed events/parameters/ports have the exact universal identity proof")
    require(original["shared_private_workspace"] == descriptor["shared_private_workspace"]
            and original["args"] == descriptor["args"] == [list(range(72))]
            and original["outs"] == descriptor["outs"] == [list(range(72, 144))],
            "Same public ports and complete shared bank, no adjacent compact wires")
    require(record["rows"] == original["gate_rows"]
            and record["row_format"] == "little-endian int32 Nx4 X/CX/CCX",
            "Externally pinned complete saved axis array")
    baseline = audit_native_payload(AXIS_SOURCE / record["gate_file"], record["rows"], original["qubits"])
    private_end = 144 + len(original["shared_private_workspace"])
    mapping = {wire: wire for wire in range(private_end)}
    for bank in (clamped, eager):
        for bit, wire in enumerate(bank):
            mapping[wire] = bit
    removed = {0, 3, 4, 5, 6, 7, 8}
    kept = [event for index, event in enumerate(original["trace"]) if index not in removed]
    require(len(kept) == len(descriptor["trace"]), "Only seven specified events removed")

    def remap_bank(bank):
        c130_full_bank(bank)
        require(all(wire in mapping for wire in bank), "Only retained live banks or two proved input aliases")
        return [mapping[wire] for wire in bank]

    def compare_row(old_index, new_index):
        if new_index % 128 == 0:
            budget()
        old_opcode, old_operands = c130_native_row(baseline, old_index, original["qubits"])
        new_opcode, new_operands = c130_native_row(words, new_index, descriptor["qubits"])
        require(all(wire in mapping for wire in old_operands), "Every retained old wire has an explicit live map")
        require(new_opcode == old_opcode and new_operands == tuple(mapping[wire] for wire in old_operands),
                "Every retained actual saved row equals exact mapped immutable axis row")

    next_wire, next_row, retained_forward, retained_reverse = private_end, 0, 0, 0
    old_forward = original["forward_rows"][1]
    new_forward = descriptor["forward_rows"][1]
    require(original["forward_rows"] == [0, old_forward]
            and descriptor["forward_rows"] == [0, new_forward], "Both actual forward row intervals start0")
    for old, new in zip(kept, descriptor["trace"], strict=True):
        budget()
        for old_bank, new_bank in zip(old["outs"], new["outs"], strict=True):
            require(c130_full_bank(new_bank) == tuple(range(next_wire, next_wire + 72)),
                    "Each retained new output gets exactly one fresh monotone full72 bank")
            for old_wire, new_wire in zip(old_bank, new_bank, strict=True):
                require(old_wire not in mapping, "Each retained old SSA bank uniquely allocated")
                mapping[old_wire] = new_wire
            next_wire += 72
        old_begin, old_end = old["rows"]
        require(new["rows"][0] == next_row and new["rows"][1] - next_row == old_end - old_begin,
                "Contiguous retained new events have exactly original complete row lengths")
        normalized = dict(old)
        normalized["args"] = [remap_bank(bank) for bank in old["args"]]
        normalized["outs"] = [remap_bank(bank) for bank in old["outs"]]
        for field in ("rows", "actual_leaf_rows", "compute_rows", "copy_rows", "inverse_rows"):
            if field in old:
                normalized[field] = [value - old_begin + next_row for value in old[field]]
        require(normalized == new, "Every retained trace field, literal, leaf SHA, copy and inverse exact")
        for offset in range(old_end - old_begin):
            old_index, new_index = old_begin + offset, next_row + offset
            compare_row(old_index, new_index)
            retained_forward += 1
            compare_row(old_forward + 72 + old_forward - 1 - old_index,
                        new_forward + 72 + new_forward - 1 - new_index)
            retained_reverse += 1
        next_row = new["rows"][1]
    require(next_row == retained_forward == retained_reverse == new_forward
            and next_wire == descriptor["qubits"], "Every retained forward/reverse row and new allocation mapped")
    require(original["gate_rows"] == 2 * old_forward + 72
            and descriptor["gate_rows"] == 2 * new_forward + 72
            and original["output_XOR_rows"] == [old_forward, old_forward + 72]
            and descriptor["output_XOR_rows"] == [new_forward, new_forward + 72]
            and original["literal_global_inverse_rows"] == [old_forward + 72, original["gate_rows"]]
            and descriptor["literal_global_inverse_rows"] == [new_forward + 72, descriptor["gate_rows"]],
            "Both whole F/dirty72XOR/F^-1 layouts complete")
    for bit in range(72):
        compare_row(old_forward + bit, new_forward + bit)
    alias_wires = set(clamped) | set(eager)
    ordinary = {wire: target for wire, target in mapping.items() if wire not in alias_wires}
    require(len(set(ordinary.values())) == len(ordinary)
            and set(ordinary.values()) == set(range(descriptor["qubits"])),
            "All actual new wires uniquely covered; only two explicitly proved banks alias input")
    deleted_unread = set(zero) | set(sign) | set(below) | set(upper) | set(is_q)
    require(not deleted_unread.intersection(mapping), "All other deleted SSA banks have no retained use")

    def remap_internal(value):
        if isinstance(value, list) and len(value) == 72 and all(type(wire) is int for wire in value):
            return remap_bank(value)
        if isinstance(value, list):
            return [remap_internal(member) for member in value]
        if isinstance(value, dict):
            return {key: remap_internal(member) for key, member in value.items()}
        return value

    require(remap_internal(original["internal"]) == descriptor["internal"],
            "Every internal role/Horner/output pointer exact mapped axis role, with two input aliases")
    omitted_rows = sum(original["trace"][index]["rows"][1] - original["trace"][index]["rows"][0]
                       for index in removed)
    require(old_forward - new_forward == omitted_rows
            and original["qubits"] - descriptor["qubits"] == 7 * 72,
            "Actual only seven private SSA outputs and their complete forward/inverse intervals omitted")
    return {"baseline_axis_manifest_SHA256": AXIS_SHA,
            "baseline_axis_gate_SHA256": record["gate_SHA256"],
            "all_retained_forward_rows": retained_forward, "all_retained_reverse_rows": retained_reverse,
            "all_output_XOR_rows": 72, "actual_new_allocated_wires": descriptor["qubits"],
            "old_wire_to_new_wire_map": {str(wire): target for wire, target in sorted(mapping.items())},
            "two_removed_roles_alias_original_full72_input": [clamped, eager],
            "other_deleted_banks_no_retained_use": [zero, sign, below, upper, is_q],
            "only_unused_zero_CONST_plus_six_initial_input_events_removed": True,
            "all_retained_actual_trace_fields_and_internal_pointers_checked": True,
            "all_retained_actual_forward_copy_and_literal_reverse_rows_mapped": True,
            "baseline_array_regenerated_or_replayed": False, "second_comparison_array_generated": False,
            "new_whole_array_independent_consumer_required_separately": True, **flags()}


def load_grid_helper():
    global _SCIENCE_ADMITTED
    require(
        not _SCIENCE_ADMITTED and GRID_MODULE not in sys.modules,
        "Only one new helper after complete admission",
    )
    check_code_caches()
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete current runtime before sole new scientific helper import",
    )
    loaded_origins()
    budget(admission=True)
    _SCIENCE_ADMITTED = True
    spec = importlib.util.spec_from_file_location(GRID_MODULE, GRID_HELPER)
    require(
        spec is not None and spec.loader is not None and canonical(spec.origin) == GRID_HELPER,
        "Exact admitted helper loader",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[GRID_MODULE] = module
    spec.loader.exec_module(module)
    require(
        module.ROW_ID == PREP_ROW_ID
        and module.MACRO == C130_CCX_MACRO
        and module.MAX_ROWS == 2000000
        and module.MAX_QUBITS == 16384
        and module.REPLAY_GUARD_ROWS == 128,
        "Same paid absolute7T expansion and finite guards",
    )
    loaded_origins()
    check_code_caches()
    budget(admission=True)
    return module


def bootstrap_preparation_author_expectations(ready_sha):
    """External author pins precede own_runtime's first strict loaded-origin check."""
    ready = read(bind(READY, ready_sha))
    require(ready["schema"] == "root-f44-q32-preparation-compact40-wrapper-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True,
            "External reviewed READY before finite author-origin bootstrap")
    own = ready["author_method_SHA256"]
    require(set(own) == {AUTHOR.name, GRID_HELPER.name, METHOD_DOC.name, PREFLIGHT.name},
            "Exactly four external author expectations, never startup observed promotion")
    for name, pin in own.items():
        bind(RESEARCH / name, pin)
    axis_code_caches([AUTHOR, GRID_HELPER], ready["existing_new_code_cache_SHA256"],
                     ready["absent_new_code_cache_paths"])


def admit_completed_axis(ready, policy):
    axis = read(AXIS_SOURCE / "manifest.json")
    require(axis["schema"] == "f44-caller-grid-axis-component-manifest-v3"
            and axis["passed"] is True and axis["completed"] is True
            and axis["budget_censored"] is False and axis["files"] == AXIS_OWNED_EXPECTED
            and axis["completed_owner_manifest_SHA256"]
            == {name: item[0] for name, item in OWNERS.items() if name != AXIS_NAME}
            and axis["completed_owner_complete_counts"]
            == {name: item[1] for name, item in OWNERS.items() if name != AXIS_NAME},
            "Exact completed conditional axis manifest and all eight original owner relations")
    release = read(bind(AXIS_READY, AXIS_READY_SHA))
    require(release["schema"] == "root-f44-caller-grid-axis-READY-v3"
            and release["author_method_SHA256"] == AXIS_AUTHORS
            and release["output"] == AXIS_SOURCE.relative_to(ROOT).as_posix()
            and release["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL],
            "Original executed axis READY immutable and scope unchanged")
    for name, expected in AXIS_AUTHORS.items():
        bind(RESEARCH / name, expected)
    axis_code_caches([RESEARCH / "experiment_f44_cosine_caller_grid_axis_v3.py", AXIS_HELPER],
                     release["existing_new_code_cache_SHA256"], release["absent_new_code_cache_paths"])
    result = read(bind(AXIS_RESULT, AXIS_RESULT_SHA))
    require(result["passed"] is True and result["manifest_SHA256"] == AXIS_SHA
            and result["complete_counts"] == AXIS_COUNTS and result["inclusive_owned_files"] == 21
            and result["all_owned_hashes_inventory_and_result_metadata_verified"] is True
            and result["generic_resource_REJECTED_unchanged"] is True
            and result["actual_coherent_preparation_outer_bridge_or_whole_financial_source_audited"] is False,
            "Externally supplied actual axis PASS never implies preparation/bridge/whole-source PASS")
    summary = read(AXIS_SOURCE / "summary.json")
    require(summary["passed"] is True and summary["completed"] is True
            and summary["certificate_scope"] == "PROMISED_CALLER_GRID_ONLY"
            and summary["logical_forward_reverse_calls"] == [128, 128]
            and summary["physical_whole_array_sweeps"] == 2
            and summary["actual_coherent32_preparation_array_audited"] is False
            and summary["whole_source_40_active_to72_zero_padded_bridge_audited"] is False
            and summary["generic_StageC_row_status"] == "REJECTED"
            and summary["generic_StageC_resource_gate_passed"] is False,
            "Actual saved array premise retains all unresolved source integration/cost qualifications")
    require(ready["axis_component_manifest_SHA256"] == policy["axis_component_manifest_SHA256"] == AXIS_SHA
            and ready["axis_component_complete_counts"] == policy["axis_component_complete_counts"] == AXIS_COUNTS
            and ready["axis_component_READY_SHA256"] == policy["axis_component_READY_SHA256"] == AXIS_READY_SHA
            and ready["axis_component_author_expected_SHA256"]
            == policy["axis_component_author_expected_SHA256"] == AXIS_AUTHORS
            and ready["axis_component_ROOT_result_SHA256"]
            == policy["axis_component_ROOT_result_SHA256"] == AXIS_RESULT_SHA
            and ready["axis_component_owned_expected_SHA256"]
            == policy["axis_component_owned_expected_SHA256"] == AXIS_OWNED_EXPECTED,
            "New release/policy exact completed axis array premise and full owned expected map")
    budget(admission=True)


def clamp_domain_identity_proof(caller):
    """Universal integer inequalities, tied to original caller promises; no sample proof."""
    require(caller["caller_grid_contract_id"] == GRID_CONTRACT_ID
            and caller["cases"]["B4x12"]["all_cosine_callers"] == 60
            and caller["cases"]["B8x52"]["all_cosine_callers"] == 468
            and caller["entry_promise_required"] is True
            and caller["actual_coherent32_preparation_array_audited"] is False,
            "Every original midpoint/wrapped caller bound to the conditional D promise")
    q, lower, upper = 1 << 40, 128, (1 << 40) - 128
    require(0 < lower <= upper < q < 1 << 71, "Every promised raw input signed72 positive and below Q")
    require(all(point % 256 == 0 for point in (0, q // 4, q // 2, 3 * q // 4, q)),
            "All five axes lie in residue0, disjoint from every promised residue128")
    return {"caller_grid_contract_id": GRID_CONTRACT_ID,
            "universal_quantifier": "Every integer n in [0,2^32) at full72 input x=256*n+128",
            "exact_raw_input_hull": [lower, upper], "signed72_no_overflow": True,
            "SIGN_negative_constant": 0, "SIGNED_LT_input_Q_constant": 1,
            "upper_SELECT_equals_input": True, "clamped_SELECT_equals_input": True,
            "clamped_EQ_Q_constant": 0, "eager_SELECT_equals_input": True,
            "five_axis_equalities_false_by_residue": True,
            "only_unused_zero_CONST_and_six_input_events_removed": True,
            "same_original_table_hulls_and_all64_native_promises_required": True,
            "full72_zero_private_entry_and_arbitrary_dirty72_output_required": True,
            "coherent_superposition_extension": "Each promised basis state has the same phase-correct clean XOR; linearity applies on the admitted promised subspace",
            "actual_coherent_preparation_and_compact40_padding_bridge_audited": False,
            "generic72_equivalence_or_whole_source_cost_transfer": False, **flags()}


def clamp_standalone_cost_comparison(resources, descriptor):
    old = read(AXIS_SOURCE / "actual_component_resources.json")
    original = read(AXIS_SOURCE / "prototype_descriptor.json")
    return {"schema": "f44-grid-clamp-standalone-saved-axis-resource-comparison-v1",
            "baseline_axis_manifest_SHA256": AXIS_SHA,
            "actual_saved_axis_rows": original["gate_rows"], "actual_new_clamp_rows": descriptor["gate_rows"],
            "actual_saved_axis_qubits": original["qubits"], "actual_new_clamp_qubits": descriptor["qubits"],
            "saved_axis_complete_resources": old["same_ASAP_and_complete_serial_event_accounting"],
            "new_actual_whole_component_complete_resources": resources,
            "classical_runtime_ratio_or_winner": None,
            "standalone_to_whole_capped_source_transfer": False,
            "outer_full72_argument_copies_CX_per_forward_still_separate": 144,
            "whole_source_native_preparation_padding_call_binding_and_scheduling_open": True,
            "generic_resource_REJECTED_unchanged": True, **flags()}


def held_clamp_V1_absences():
    """Static HOLD never becomes a scientific failure or a released attempt."""
    for key in (HELD_CLAMP_V1_READY_KEY, HELD_CLAMP_V1_OUTPUT_KEY):
        budget()
        path = ROOT / key
        require(not path.exists() and not path.is_symlink()
                and path.resolve(strict=False) == path,
                "Original held clamp V1 READY/output remain wholly absent without alias")
    budget()


def admit_held_clamp_V1(ready, policy):
    require(ready["held_clamp_V1_author_expected_SHA256"]
            == policy["held_clamp_V1_author_expected_SHA256"] == HELD_CLAMP_V1_AUTHORS
            and ready["held_clamp_V1_report_expected_SHA256"]
            == policy["held_clamp_V1_report_expected_SHA256"] == HELD_CLAMP_V1_REPORTS
            and ready["held_clamp_V1_READY_absent_path"]
            == policy["held_clamp_V1_READY_absent_path"] == HELD_CLAMP_V1_READY_KEY
            and ready["held_clamp_V1_output_absent_path"]
            == policy["held_clamp_V1_output_absent_path"] == HELD_CLAMP_V1_OUTPUT_KEY,
            "Exact immutable unexecuted V1 quartet/QA/two holds and absent route")
    for name, expected in HELD_CLAMP_V1_AUTHORS.items():
        bind(RESEARCH / name, expected)
    records = {key: read(bind(ROOT / key, expected))
               for key, expected in HELD_CLAMP_V1_REPORTS.items()}
    for key in (
        ".context/F44_COSINE_CALLER_GRID_CLAMP_ROOT_STATIC_HOLD_run001.json",
        ".context/F44_COSINE_CALLER_GRID_CLAMP_INDEPENDENT_STATIC_HOLD_run001.json",
    ):
        record = records[key]
        require(record["status"] == "HOLD" and record["passed"] is False
                and record["author_files_SHA256"] == HELD_CLAMP_V1_AUTHORS
                and record["new_READY_and_output_absent"] is True
                and record["complete_scientific_static_peer_review_claimed"] is False
                and record["scientific_method_or_diagnostic_failure_claimed"] is False
                and record["fixture_credit"] == 0,
                "Metadata-only original holds, never numerical failure or science promotion")
    axis_code_caches(
        [RESEARCH / "experiment_f44_cosine_caller_grid_clamp_v1.py", LEGACY_CLAMP_HELPER],
        ready["held_clamp_V1_existing_code_cache_SHA256"],
        ready["held_clamp_V1_absent_code_cache_paths"],
    )
    for key in (HELD_CLAMP_V1_READY_KEY, HELD_CLAMP_V1_OUTPUT_KEY):
        _ABSENT_RUNTIME.add(ROOT / key)
    held_clamp_V1_absences()
    require(policy["current_initial_input_clamp_events_omitted"] is True
            and policy["current_postROUND_projection_retained"] is True
            and policy["current_loaded_origins_AST_equal_original_axis_V3"] is False
            and policy["current_clamp_loaded_origins_AST_equal_held_clamp_V1"] is True
            and policy["V2_science_helper_corpus_and_caps_exact_held_clamp_V1"] is True,
            "Current component claims separated from original scalar and axis-history claims")
    budget(admission=True)


class PreparationReject(ValueError):
    pass


def prep_require(condition, tag):
    if not condition:
        raise PreparationReject(tag)


def prep_read_owned(name):
    global _HASH_WORK
    budget()
    path = canonical(OUTPUT / name, fresh=True)
    require(path.parent == OUTPUT and name in _OUTPUT_METADATA_EXPECTED,
            "Only a registered current-owned metadata artifact")
    expected = _OUTPUT_METADATA_EXPECTED[name]
    before = fingerprint(path)
    require(0 < before[2] <= MAX_OWN_BYTES, "Bounded whole owned metadata")
    parts, total, state = [], 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(65536):
            budget()
            total += len(block)
            _HASH_WORK += len(block)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                    "All owned interpretation reads charged")
            parts.append(block)
            state.update(block)
    require(total == before[2] and fingerprint(path) == before and state.hexdigest() == expected,
            "Stable whole saved artifact, no in-memory producer substitution")
    value = json.loads(b"".join(parts))
    guard_serialization_integers(value)
    return value


def prep_save_owned(name, value):
    save(name, value)
    _OUTPUT_METADATA_EXPECTED[name] = digest(OUTPUT / name, fresh=True)


def prep_clamp_admission(ready, policy):
    """Literal completed dependency only; no concurrent shared-QROM version."""
    for field, expected in (
        ("clamp_component_manifest_SHA256", CLAMP_SHA),
        ("clamp_component_complete_counts", CLAMP_COUNTS),
        ("clamp_component_READY_SHA256", CLAMP_READY_SHA),
        ("clamp_component_ROOT_result_SHA256", CLAMP_ROOT_RESULT_SHA),
        ("clamp_component_author_expected_SHA256", CLAMP_AUTHORS),
        ("clamp_component_owned_expected_SHA256", CLAMP_OWNED),
        ("preparation_design_expected_SHA256", PREP_DESIGN_PINS),
        ("preparation_original_case_paths_and_pins", PREP_CASE_PINS),
        ("original_fixed_grid_diagnostics_SHA256", CLAMP_OWNED["fixed_grid_diagnostics.json"]),
        ("original_fixed_grid_diagnostics_declared_fields", PREP_COHORT_FIELDS),
    ):
        require(ready[field] == policy[field] == expected, "Exact frozen preparation dependency: " + field)
    release = read(bind(CLAMP_READY, CLAMP_READY_SHA))
    require(release["schema"] == "root-f44-caller-grid-clamp-READY-v2"
            and release["author_method_SHA256"] == CLAMP_AUTHORS
            and release["output"] == CLAMP.relative_to(ROOT).as_posix(),
            "Immutable original clamp002 READY, not a new implementation")
    for name, expected in CLAMP_AUTHORS.items():
        bind(RESEARCH / name, expected)
    axis_code_caches(
        [RESEARCH / "experiment_f44_cosine_caller_grid_clamp_v2.py", LEGACY_CLAMP_HELPER],
        release["existing_new_code_cache_SHA256"], release["absent_new_code_cache_paths"],
    )
    manifest = read(CLAMP / "manifest.json")
    require(manifest["schema"] == "f44-caller-grid-clamp-component-manifest-v2"
            and manifest["files"] == CLAMP_OWNED
            and manifest["ROOT_READY_SHA256"] == CLAMP_READY_SHA
            and manifest["actual_coherent32_preparation_array_audited"] is False
            and manifest["whole_source_40_active_to72_zero_padded_bridge_audited"] is False
            and manifest["whole_financial_source_emitted"] is False,
            "Original complete paid component retains preparation/source qualifications")
    result = read(bind(CLAMP_ROOT_RESULT, CLAMP_ROOT_RESULT_SHA))
    require(result["passed"] is True and result["manifest_SHA256"] == CLAMP_SHA
            and result["complete_counts"] == CLAMP_COUNTS
            and result["actual_coherent_preparation_outer_bridge_or_whole_financial_source_audited"] is False,
            "Saved ROOT metadata verification does not establish the new experiment")
    for key, expected in PREP_DESIGN_PINS.items():
        bind(ROOT / key, expected)
    require(policy["cohort_authority"] == "complete original clamp002 fixed_grid_diagnostics.json inputs"
            and ready["cohort_authority"] == policy["cohort_authority"]
            and ready["preparation_wrapper_execution_authorized"] is True
            and policy["center_cohort_unexecuted_and_superseded"] is True
            and policy["fixed_negative_control_count"] == 5
            and policy["native_array_rows_qubits_guard_rows"] == [2000000, 16384, 128],
            "New bounded source scope and explicit unexecuted cohort correction")
    budget(admission=True)


def prep_caller_audit():
    original = caller_binding_inventory()
    binding = read(SOURCE / "original_source_binding.json")
    design = read(ROOT / PREP_DESIGN_JSON_KEY)
    cases = {}
    for case, counts in (("B4x12", (30, 60)), ("B8x52", (234, 468))):
        saved = binding["cases"][case]
        expected = PREP_CASE_PINS[case]
        for label in ("target", "source", "schedule"):
            require(saved[label + "_path"] == expected[label]["path"]
                    and saved[label + "_sha256"] == expected[label]["original_declared_SHA256"]
                    and _FROZEN[saved[label + "_path"]] == saved[label + "_sha256"],
                    "All six exact original caller/source/schedule declarations")
        schedule = read(ROOT / saved["schedule_path"])
        source = read(ROOT / saved["source_path"])
        copied = design["original_binding"]["source_pointer_metadata"][case]
        require(copied["complete_cosine_argument_values_copied_metadata_only"]
                == saved["cosine_argument_values"] and len(saved["pair_scopes"]) == counts[0],
                "Complete ordered original caller list, no inferred final polynomial inputs")
        pointers = {}
        raw_wires = set()
        for index, pair in enumerate(saved["pair_scopes"]):
            budget(admission=True)
            ids = dict(raw_u=pair["raw_uniform_values"][0], raw_v=pair["raw_uniform_values"][1],
                       m=pair["cosines"][0]["input"], w=pair["cosines"][1]["input"])
            row = {}
            for role, value in ids.items():
                width, offset = schedule["widths"][value], schedule["offsets"][value]
                require(type(width) is int and type(offset) is int and offset >= 0
                        and width == (32 if role.startswith("raw_") else 40),
                        "Exact original compact declared bit width and nonnegative offset")
                stored = copied["complete_stored_pair_pointer_metadata"][str(index)][role]
                require(stored == {"SSA_value": value, "stored_width": width, "stored_offset": offset},
                        "Every stored pointer rederived from the complete pinned original schedule")
                row[role] = {**stored, "declared_wire_list": list(range(offset, offset + width))}
                if role.startswith("raw_"):
                    wires = set(row[role]["declared_wire_list"])
                    require(not raw_wires.intersection(wires), "Every original raw input has a disjoint bank")
                    raw_wires.update(wires)
            pointers[str(index)] = row
        require(len(pointers) == counts[0] and len(source["inputs"]) == counts[1]
                and len(copied["complete_stored_pair_pointer_metadata"]) == counts[0],
                "Every original pair/raw uniform and compact m/w pointer consumed")
        cases[case] = {"all_pairs": counts[0], "all_arguments": counts[1],
                       "cosine_argument_values": saved["cosine_argument_values"],
                       "complete_pair_pointers": pointers,
                       "first_argument_values": [pair["input"] for pair in saved["pair_scopes"][0]["cosines"]],
                       "exact_paths_and_pins": expected,
                       "original_source_meaning": source["meaning"]}
    require(all(cases[case]["first_argument_values"] == [6, 61] for case in cases),
            "m6/w61 are arguments; final MUL72/92 must never replace them")
    return {"schema": "f44-preparation-complete-original-pointer-audit-v1", "cases": cases,
            "original_caller_binding": original, "actual_original_financial_source_instantiation": False,
            "m_and_w_share_original_raw_v": True, "new_fixture_credit": 0}


def prep_metadata_guard(descriptor, caller):
    prep_require(descriptor["schema"] == "f44-q32-two-compact40-two-clamp002-wrapper-prototype-v1",
                 "PROTOTYPE_SCHEMA")
    prep_require(descriptor["wrap_top_bit_gate_order"] == ["CX_original_x_to_y", "X_y", "X_x"],
                 "WRAP_ORDER")
    prep_require(descriptor["compact_source_lists"] == {"m": descriptor["m40"], "w": descriptor["w40"]}
                 and all(len(descriptor["compact_source_lists"][key]) == 40 for key in ("m", "w")),
                 "COMPACT_SOURCE_40_ONLY")
    expected = {case: caller["cases"][case]["first_argument_values"] for case in ("B4x12", "B8x52")}
    prep_require(descriptor["original_first_argument_values"] == expected
                 == {"B4x12": [6, 61], "B8x52": [6, 61]}, "ORIGINAL_SSA_INPUT")
    prep_require(descriptor["composition_chronology"] == [
        "H32", "ENCODE_M", "ENCODE_W", "WRAP_M", "WRAP_W", "WRAP_W_inverse",
        "WRAP_M_inverse", "ENCODE_W_inverse", "ENCODE_M_inverse", "H32_inverse"], "A_INVERSE_ORDER")


def prep_H_consumer(forward, inverse, n32):
    """Independent exact two-column consumer for a separate H-capable format."""
    columns = [[["0", "1/2"], ["0", "1/2"]], [["0", "1/2"], ["0", "-1/2"]]]
    for artifact, direction in ((forward, "forward"), (inverse, "inverse")):
        prep_require(artifact["schema"] == "f44-separate-positive-H32-records-v1"
                     and artifact["direction"] == direction
                     and artifact["native_Nx4_reinterpreted"] is False
                     and artifact["exact_field"] == "Q(sqrt(2)); sqrt(2) is the positive real root"
                     and artifact["matrix_columns_Qsqrt2_pairs"] == columns, "H_COLUMNS")
        ordered = list(n32) if direction == "forward" else list(reversed(n32))
        prep_require(len(n32) == len(set(n32)) == 32
                     and artifact["targets_in_logical_little_endian_order"] == n32
                     and artifact["records"] == [{"op": "H", "target": wire} for wire in ordered]
                     and artifact["zero_entry_source_required"] is True
                     and artifact["sampled_uniformity_claim"] is False, "H_TARGETS_AND_INVERSE")
    matrix = [[tuple(Fraction(x) for x in columns[col][row]) for col in range(2)] for row in range(2)]
    for left in range(2):
        for right in range(2):
            budget()
            real, root = Fraction(0), Fraction(0)
            for inner in range(2):
                a, b = matrix[left][inner]
                c, d = matrix[inner][right]
                real += a * c + 2 * b * d
                root += a * d + b * c
            require((real, root) == (Fraction(int(left == right)), Fraction(0)),
                    "Both exact real H columns compose to I with positive normalization")
    require(matrix[0][1] == matrix[1][0], "Literal real H is self-adjoint")
    return {"schema": "f44-H32-exact-two-column-tensor-proof-v1", "two_columns_checked": 2,
            "positive_sqrt2_absolute_convention": True, "H_dagger_equals_H_and_H_squared_I": True,
            "forward_and_literal_inverse_records_consumed": [32, 32],
            "all_32_targets_injective_and_bound": True,
            "tensor_element": "<n|H32|e>=2^-16*(-1)^(sum_j e_j*n_j)",
            "zero32_source_uniform_amplitude": "positive 2^-16 on every q32 basis value",
            "zero32_source_uniform_probability": "2^-32", "zero_entry_premise_required": True,
            "universal_tensor_rule": "disjoint one-qubit exact operators compose as a tensor product",
            "arbitrary_reference_operator_extension": "same verified operator tensor identity on reference",
            "arbitrary_entangled_input_claimed_uniform": False, "samples_establish_uniformity": False,
            "native_Nx4_H_opcode_added": False, "program_fixture_credit": 0}


def prep_whole_array_consumer(words, descriptor, paid_words, paid_descriptor, caller):
    prep_metadata_guard(descriptor, caller)
    budget()
    require(descriptor["row_id"] == PREP_ROW_ID
            and descriptor["native_format"] == "little-endian int32 Nx4 X/CX/CCX"
            and descriptor["prototype_native_rows_cap"] == 2000000
            and descriptor["prototype_native_wire_cap"] == 16384,
            "One fixed complete bounded native preparation/wrapper allocation")
    position = 0
    for field, width in (("n32", 32), ("m40", 40), ("m_adjacent32_sentinels", 32),
                         ("w40", 40), ("w_adjacent32_sentinels", 32), ("dirty_m72", 72),
                         ("dirty_w72", 72), ("argument72", 72),
                         ("private_and_retained_SSA", paid_descriptor["qubits"] - 144)):
        require(descriptor[field] == list(range(position, position + width)),
                "Independent complete allocation, including distinct adjacent sentinel banks")
        position += width
    require(position == descriptor["qubits"] <= 16384, "All allocated wires independently consumed")
    cursor = C130SavedRows(words, descriptor["qubits"])
    n, m, w = descriptor["n32"], descriptor["m40"], descriptor["w40"]
    events = descriptor["events"]
    require(len(events) == 4 and len(descriptor["wrappers"]) == 2, "Exactly two encoders/two wrappers")
    begin = cursor.cursor
    cursor.consume((m[7],))
    for bit in range(32):
        cursor.consume((n[bit], m[bit + 8]))
    require(events[0] == {"op": "ENCODE_M", "rows": [begin, cursor.cursor]}, "Whole midpoint encoder")
    begin = cursor.cursor
    for bit in range(40):
        cursor.consume((m[bit], w[bit]))
    cursor.consume((w[38], w[39]))
    cursor.consume((w[39],))
    cursor.consume((w[38],))
    require(events[1] == {"op": "ENCODE_W", "rows": [begin, cursor.cursor]},
            "Actual wrapped encoder uses original x before either X")
    sentinel_set = set(descriptor["m_adjacent32_sentinels"] + descriptor["w_adjacent32_sentinels"])
    for index, (branch, source, output) in enumerate((("m", m, descriptor["dirty_m72"]),
                                                     ("w", w, descriptor["dirty_w72"]))):
        wrapper = descriptor["wrappers"][index]
        argument, private = descriptor["argument72"], descriptor["private_and_retained_SSA"]
        mapping = argument + output + private
        require(wrapper["branch"] == branch and wrapper["source40"] == source
                and wrapper["argument72"] == argument and wrapper["dirty_output72"] == output
                and wrapper["private_and_retained_SSA"] == private
                and wrapper["whole_old_wire_to_new_wire"] == mapping
                and len(mapping) == len(set(mapping)) == paid_descriptor["qubits"]
                and not set(mapping).intersection(source + list(sentinel_set)),
                "All original public/private/retained-SSA wires map injectively without source aliases")
        begin = cursor.cursor
        for bit in range(40):
            cursor.consume((source[bit], argument[bit]))
        body = cursor.cursor
        require(wrapper["copy_rows"] == [begin, body], "Exactly forty declared source copies")
        for old_index in range(paid_descriptor["gate_rows"]):
            if old_index % 128 == 0:
                budget()
            _, operands = c130_native_row(paid_words, old_index, paid_descriptor["qubits"])
            cursor.consume(tuple(mapping[wire] for wire in operands))
        body_end = cursor.cursor
        require(wrapper["complete_paid_component_rows"] == [body, body_end],
                "Every paid component forward/XOR/whole-inverse row retained in order")
        for bit in range(39, -1, -1):
            cursor.consume((source[bit], argument[bit]))
        require(wrapper["uncopy_rows"] == [body_end, cursor.cursor]
                and wrapper["rows"] == [begin, cursor.cursor]
                and events[index + 2] == {"op": "WRAP_" + branch.upper(), "rows": [begin, cursor.cursor]},
                "Exact same forty uncopy pairs, complete serialized wrapper chronology")
    end = cursor.cursor
    require(descriptor["arithmetic_forward_rows"] == [0, end]
            and descriptor["actual_arithmetic_inverse_rows"] == [end, len(words) // 4]
            and descriptor["gate_rows"] == len(words) // 4 == 2 * end,
            "One complete forward and actual literal inverse, no implicit dependent outputs")
    cursor.inverse_of(0, end)
    require(cursor.cursor == descriptor["gate_rows"]
            and descriptor["zero_entry_uniform_source_required"] is True
            and descriptor["dirty_outputs_full72_arbitrary"] is True
            and descriptor["high32_argument_padding_zero_entry"] is True
            and descriptor["whole_financial_source_emitted"] is False
            and descriptor["fixture_credit"] == 0,
            "Whole allocation, every actual inverse row and template-only scope consumed")
    return {"all_actual_rows_consumed": cursor.cursor, "all_allocated_wires_consumed": position,
            "two_complete_paid_clamp_remaps_consumed": True, "exact40_copy_and_uncopy": True,
            "high32_padding_zero_from_fresh_bank": True, "adjacent32_sentinels_never_read": True,
            "full72_dirty_outputs_and_complete_private_SSA_retained": True,
            "wrapped_original_x_gate_order_verified": True, "actual_literal_whole_inverse_consumed": True,
            "H_inverse_after_all_arithmetic_dependents": True, "second_native_array_generated": False,
            "full_original_financial_source_emitted_or_accepted": False, "program_fixture_credit": 0}


def prep_universal_composition(descriptor, h_proof, paid_proof, row_proof, phase):
    require(h_proof["H_dagger_equals_H_and_H_squared_I"] is True
            and h_proof["all_32_targets_injective_and_bound"] is True
            and paid_proof["caller_grid_full72_interface_clean_XOR_conditional"] is True
            and row_proof["two_complete_paid_clamp_remaps_consumed"] is True
            and row_proof["actual_literal_whole_inverse_consumed"] is True
            and phase["exact_absolute_phase_CCX"] is True, "All exact operator premises join")
    for top in range(4):
        budget()
        x, y = top & 1, top >> 1
        transformed = (1 ^ x) + 2 * (1 ^ y ^ x)
        require(transformed == (top + 3) % 4, "All four original top-bit cases; low30 untouched")
    require(descriptor["composition_chronology"][-1] == "H32_inverse",
            "Input preparation reversed only after dependent outputs and encoders")
    return {"schema": "f44-preparation-wrapper-universal-operator-composition-v1",
            "n_quantifier": "every unsigned32 n", "dirty_quantifier": "every two arbitrary full72 outputs",
            "midpoint": "256*n+128", "wrap": "256*((n+3*2^30) mod 2^32)+128",
            "same_draw_correlated_midpoint_wrap": True,
            "promised_domain": "128<=m,w<=2^40-128; residue128 mod256; zero high32",
            "zero_entry_preparation_uniformity": "exact H tensor product; equal positive amplitudes",
            "wrapper_operator": "|s,d,0B,0P> -> |s,d xor C(zeroextend72(s)),0B,0P>, phase1",
            "reference_entanglement": "universal exact absolute basis-map identities extend by linearity tensor I_R",
            "arbitrary_entangled_H_input_claimed_uniform": False,
            "whole_template_A_dagger_A_identity": True,
            "whole_financial_dependents_must_also_be_uncomputed_before_H_dagger": True,
            "uniformity_or_phase_inferred_from_samples": False,
            "original_leaf_all64_range_and_source_guards_remain_required": True,
            "whole_financial_source_or_G2_certificate": False}


def prep_fixed_negative_controls(descriptor, caller, h_forward, h_inverse):
    results = []

    def control(tag, action):
        budget()
        try:
            action()
        except PreparationReject as error:
            require(str(error) == tag, "Only the specifically declared structural failure is expected")
            results.append({"tag": tag, "rejected": True})
        else:
            raise ValueError("Declared negative control incorrectly accepted: " + tag)
        budget()

    changed_H = json.loads(json.dumps(h_forward))
    changed_H["matrix_columns_Qsqrt2_pairs"][0][0][1] = "-1/2"
    control("H_COLUMNS", lambda: prep_H_consumer(changed_H, h_inverse, descriptor["n32"]))
    bad = dict(descriptor)
    bad["wrap_top_bit_gate_order"] = ["X_x", "CX_updated_x_to_y", "X_y"]
    control("WRAP_ORDER", lambda: prep_metadata_guard(bad, caller))
    bad_copy = dict(descriptor)
    bad_copy["compact_source_lists"] = {"m": descriptor["m40"] + descriptor["m_adjacent32_sentinels"],
                                         "w": descriptor["w40"]}
    control("COMPACT_SOURCE_40_ONLY", lambda: prep_metadata_guard(bad_copy, caller))
    bad_ids = dict(descriptor)
    bad_ids["original_first_argument_values"] = {"B4x12": [72, 92], "B8x52": [72, 92]}
    control("ORIGINAL_SSA_INPUT", lambda: prep_metadata_guard(bad_ids, caller))
    bad_inverse = dict(descriptor)
    bad_inverse["composition_chronology"] = ["H32", "ENCODE_M", "ENCODE_W", "WRAP_M", "WRAP_W",
                                             "H32_inverse", "WRAP_W_inverse", "WRAP_M_inverse",
                                             "ENCODE_W_inverse", "ENCODE_M_inverse"]
    control("A_INVERSE_ORDER", lambda: prep_metadata_guard(bad_inverse, caller))
    require(len(results) == 5, "Exactly five fixed structural controls; budget failures do not pass")
    return {"fixed_count": 5, "controls": results, "alternate_gate_array_emitted": False,
            "budget_exception_is_expected_rejection": False, "fixture_credit": 0}


def prep_sweep(words, state, begin, end):
    budget()
    require(0 <= begin <= end <= len(words) // 4 and 0 < len(words) // 4 <= 2000000
            and 0 < len(state) <= 16384, "Complete fixed arithmetic interval")
    full = (1 << 128) - 1
    require(all(type(value) is int and 0 <= value <= full for value in state), "Exactly128 logical lane bits")
    for index in range(begin, end):
        if (index - begin) % 128 == 0:
            budget()
        opcode, operands = c130_native_row(words, index, len(state))
        if opcode == 1:
            state[operands[0]] ^= full
        elif opcode == 2:
            state[operands[1]] ^= state[operands[0]]
        else:
            state[operands[2]] ^= state[operands[0]] & state[operands[1]]


def prep_fixed_diagnostics(words, descriptor, table):
    saved = read(CLAMP / "fixed_grid_diagnostics.json")
    xs = saved["inputs"]
    require(len(xs) == len(set(xs)) == 64 and xs == PREP_COHORT_FIELDS["inputs"]
            and all(saved[field] == expected for field, expected in PREP_COHORT_FIELDS.items()),
            "Exact64 original saved boundary-sensitive integers and fixed logical scope")
    mask = (1 << 72) - 1
    cases = []
    for raw in xs:
        require(type(raw) is int and 128 <= raw <= (1 << 40) - 128 and raw % 256 == 128,
                "Original saved complete prepared grid case")
        n = (raw - 128) >> 8
        require(0 <= n < 1 << 32 and 256 * n + 128 == raw, "Exact inverse original midpoint interpretation")
        for dirty in (0, mask):
            cases.append((n, raw, (raw + 3 * (1 << 38)) % (1 << 40), dirty))
    initial = [0] * descriptor["qubits"]
    expected = list(initial)
    for lane, (n, m, w, dirty) in enumerate(cases):
        budget()
        for field, value in (("n32", n), ("dirty_m72", dirty), ("dirty_w72", dirty)):
            for bit, wire in enumerate(descriptor[field]):
                initial[wire] |= ((value >> bit) & 1) << lane
        for field in ("m_adjacent32_sentinels", "w_adjacent32_sentinels"):
            for bit, wire in enumerate(descriptor[field]):
                initial[wire] |= ((lane + bit) % 2) << lane
    expected = list(initial)
    for lane, (_, m, w, _) in enumerate(cases):
        for field, value, xor in (("m40", m, False), ("w40", w, False),
                                  ("dirty_m72", c130_integer_reference(m, table), True),
                                  ("dirty_w72", c130_integer_reference(w, table), True)):
            budget()
            for bit, wire in enumerate(descriptor[field]):
                value_bit = ((value >> bit) & 1) << lane
                if xor:
                    expected[wire] ^= value_bit
                else:
                    expected[wire] |= value_bit
    actual = list(initial)
    begin, end = descriptor["arithmetic_forward_rows"]
    prep_sweep(words, actual, begin, end)
    require(actual == expected, "Every n/m/w/dirty/private/SSA/sentinel wire equals independent expected result")
    begin, end = descriptor["actual_arithmetic_inverse_rows"]
    prep_sweep(words, actual, begin, end)
    require(actual == initial, "Every actual literal inverse lane restores every allocated wire")
    return {"original_saved_cohort_path": (CLAMP / "fixed_grid_diagnostics.json").relative_to(ROOT).as_posix(),
            "original_saved_cohort_SHA256": CLAMP_OWNED["fixed_grid_diagnostics.json"],
            "exact_saved_inputs": xs, "logical_composed_forward_calls": 128,
            "logical_composed_actual_inverse_calls": 128, "physical_whole_array_sweeps": 2,
            "two_full_component_calls_in_each_composed_direction": True,
            "paired_arbitrary_full72_dirty_diagnostics": [0, mask],
            "all_allocated_wires_and_adjacent_sentinels_compared": True,
            "H_basis_simulation_used_as_uniformity_proof": False, "fixture_credit": 0}


def prep_resource_interval(words, qubits, begin, end, before_H=(), after_H=()):
    budget()
    require(0 <= begin <= end <= len(words) // 4 <= 2000000 and 0 < qubits <= 16384,
            "Every actual chronological resource interval bounded")
    t_clock, full_clock = [0] * qubits, [0] * qubits
    counts = {"x": 0, "cx": 0, "ccx": 0, "preparation_h": 0}

    def event(op, wires):
        require(wires and len(set(wires)) == len(wires)
                and all(type(wire) is int and 0 <= wire < qubits for wire in wires), "Actual resource event wires")
        next_t = max(t_clock[wire] for wire in wires) + int(op in ("T", "TD"))
        next_full = max(full_clock[wire] for wire in wires) + 1
        for wire in wires:
            t_clock[wire], full_clock[wire] = next_t, next_full

    for wire in before_H:
        budget()
        event("H", (wire,))
        counts["preparation_h"] += 1
    for index in range(begin, end):
        if (index - begin) % 128 == 0:
            budget()
        opcode, operands = c130_native_row(words, index, qubits)
        counts[("x", "cx", "ccx")[opcode - 1]] += 1
        expansion = C130_CCX_MACRO if opcode == 3 else (("CX", 0, 1),) if opcode == 2 else (("X", 0),)
        for expanded in expansion:
            event(expanded[0], tuple(operands[j] for j in expanded[1:]))
    for wire in after_H:
        budget()
        event("H", (wire,))
        counts["preparation_h"] += 1
    return {**counts, "native_rows": end - begin,
            "source_gates": end - begin + counts["preparation_h"],
            "t_count": 7 * counts["ccx"], "t_depth": max(t_clock),
            "clifford_t_depth": max(full_clock), "clifford_cx": counts["cx"] + 6 * counts["ccx"],
            "clifford_h": counts["preparation_h"] + 2 * counts["ccx"], "native_interval": [begin, end]}


def prep_actual_resources(words, descriptor, paid_descriptor):
    qubits = descriptor["qubits"]
    end = descriptor["arithmetic_forward_rows"][1]
    rows = descriptor["gate_rows"]
    H = descriptor["n32"]
    asap_A = prep_resource_interval(words, qubits, 0, end, before_H=H)
    asap_inverse = prep_resource_interval(words, qubits, end, rows, after_H=tuple(reversed(H)))
    asap_cycle = prep_resource_interval(words, qubits, 0, rows, before_H=H, after_H=tuple(reversed(H)))
    forward_intervals = [dict(descriptor["events"][0]), dict(descriptor["events"][1])]
    for wrapper in descriptor["wrappers"]:
        branch = wrapper["branch"]
        forward_intervals.append({"op": "COPY40_" + branch, "rows": wrapper["copy_rows"]})
        offset = wrapper["complete_paid_component_rows"][0]
        old_end = paid_descriptor["forward_rows"][1]
        old_reverse = paid_descriptor["literal_global_inverse_rows"][0]
        for saved in paid_descriptor["trace"]:
            forward_intervals.append({"op": branch + ":" + saved["op"],
                                      "rows": [offset + x for x in saved["rows"]]})
        forward_intervals.append({"op": branch + ":DIRTY_XOR72",
                                  "rows": [offset + old_end, offset + old_reverse]})
        for saved in reversed(paid_descriptor["trace"]):
            begin, finish = saved["rows"]
            forward_intervals.append({"op": branch + ":inverse:" + saved["op"],
                                      "rows": [offset + old_reverse + old_end - finish,
                                               offset + old_reverse + old_end - begin]})
        forward_intervals.append({"op": "UNCOPY40_" + branch, "rows": wrapper["uncopy_rows"]})
    position = 0
    for interval in forward_intervals:
        require(interval["rows"][0] == position <= interval["rows"][1] <= end,
                "All complete original helper/leaf/copy events preserve actual serial chronology")
        position = interval["rows"][1]
    require(position == end, "Every composed forward row accounted exactly once")
    inverse_intervals = [{"op": "whole-inverse:" + item["op"],
                          "rows": [end + end - item["rows"][1], end + end - item["rows"][0]]}
                         for item in reversed(forward_intervals)]
    serial_A = [{"op": "H32", **prep_resource_interval(words, qubits, 0, 0, before_H=H)}]
    for item in forward_intervals:
        serial_A.append({"op": item["op"], **prep_resource_interval(words, qubits, *item["rows"])})
    serial_inverse = []
    for item in inverse_intervals:
        serial_inverse.append({"op": item["op"], **prep_resource_interval(words, qubits, *item["rows"])})
    serial_inverse.append({"op": "H32_inverse", **prep_resource_interval(words, qubits, rows, rows,
                                                                        after_H=tuple(reversed(H)))})

    def sums(events):
        keys = ("x", "cx", "ccx", "preparation_h", "native_rows", "source_gates", "t_count",
                "t_depth", "clifford_t_depth", "clifford_cx", "clifford_h")
        return {key: sum(item[key] for item in events) for key in keys}

    whole_A, whole_inverse = sums(serial_A), sums(serial_inverse)
    for result, actual in ((whole_A, asap_A), (whole_inverse, asap_inverse)):
        require(all(result[key] == actual[key] for key in ("x", "cx", "ccx", "preparation_h",
                                                          "native_rows", "source_gates", "t_count",
                                                          "clifford_cx", "clifford_h")),
                "Complete ASAP and serial conventions consume identical actual record inventories")
    return {"schema": "f44-whole-template-A-and-inverse-actual-resource-ledger-v1", "qubits": qubits,
            "actual_whole_A_ASAP": asap_A, "actual_whole_A_inverse_ASAP": asap_inverse,
            "actual_whole_A_then_inverse_ASAP": asap_cycle,
            "matched_serial_event_chronology": {"forward": serial_A, "inverse": serial_inverse,
                                                 "forward_sums": whole_A, "inverse_sums": whole_inverse},
            "all_preparation_copy_encoder_component_private_inverse_work_charged": True,
            "original_whole_source_capped_schedule_evaluated": False,
            "historical144CX_outer_obligation_discounted": False,
            "whole_source_cost_or_savings_forecast": None, "classical_comparison_or_advantage": None}


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists() and not OUTPUT.is_symlink(),
            "One fresh exclusively released preparation/wrapper route")
    try:
        require(sys.version_info[:3] == (3, 12, 4) and sys.byteorder == "little"
                and array("i").itemsize == 4 and sys.flags.optimize == 0
                and "PYTHONOPTIMIZE" not in os.environ, "Original exact Python/startup representation")
        for spelling, expected in INTERPRETER_PINS.items():
            bind(Path(spelling), expected)
        fixed_integer_policy()
        bootstrap_startup_expected()
        bootstrap_preparation_author_expectations(args.ready_sha256)
        runtime = own_runtime()
        ready, policy = admission(args.ready_sha256)
        admit_completed_axis(ready, policy)
        admit_held_clamp_V1(ready, policy)
        prep_clamp_admission(ready, policy)
        loaded_origins()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, GRID_HELPER, METHOD_DOC, PREFLIGHT, READY, ROOT / PREP_ADDENDUM_KEY):
            copy(path, "executed_" + path.name)
        save("run_started.json", {"created_UTC": datetime.now(timezone.utc).isoformat(),
                                   "PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                                   "new_template_result_yet_established": False, **flags()})
        save("retained_original_metadata_reconciliation.json", reconcile_metadata())
        save("retained_original_whole_source_accounting.json", {
            "original_comparison": read(SOURCE / "whole_source_resource_comparison.json"),
            "original_independent_comparison": read(AUDIT / "independent_whole_source_cost_audit.json"),
            "original_storage_copy_inverse_baseline_obligations_retained": True,
            "new_whole_source_comparator_or_capped_schedule_evaluated": False, **flags()})
        caller = prep_caller_audit()
        save("complete_original_caller_pointer_audit.json", caller)
        table = read(SOURCE / "primary90_literals.json")["table"]
        leaves = audit_admitted_leaves(read(SOURCE / "original_source_binding.json"))
        paid_descriptor = read(CLAMP / "prototype_descriptor.json")
        native = read(CLAMP / "native_gate_array.json")
        require(native["gate_file"] == "cosine.gates.bin" and native["rows"] == paid_descriptor["gate_rows"]
                and native["gate_SHA256"] == CLAMP_OWNED["cosine.gates.bin"]
                and native["row_format"] == "little-endian int32 Nx4 X/CX/CCX", "Exact saved paid component")
        paid_words = audit_native_payload(CLAMP / native["gate_file"], native["rows"], paid_descriptor["qubits"])
        paid_proof = grid_gate_binding(paid_words, paid_descriptor, table, leaves)
        save("independent_saved_paid_component_consumer.json", paid_proof)
        builder = load_grid_helper()
        first_arguments = {case: caller["cases"][case]["first_argument_values"] for case in ("B4x12", "B8x52")}
        circuit, descriptor, h_forward, h_inverse = builder.build_preparation_wrapper(
            paid_words, paid_descriptor, budget, first_arguments)
        prep_save_owned("prototype_descriptor.json", descriptor)
        prep_save_owned("H32_preparation.json", h_forward)
        prep_save_owned("H32_inverse.json", h_inverse)
        record = save_gate_array(circuit)
        _OUTPUT_NATIVE_EXPECTED[canonical(OUTPUT / record["gate_file"])] = record["gate_SHA256"]
        save("native_gate_array.json", record)
        descriptor = prep_read_owned("prototype_descriptor.json")
        h_forward, h_inverse = prep_read_owned("H32_preparation.json"), prep_read_owned("H32_inverse.json")
        words = audit_native_payload(OUTPUT / record["gate_file"], descriptor["gate_rows"], descriptor["qubits"])
        h_proof = prep_H_consumer(h_forward, h_inverse, descriptor["n32"])
        save("independent_H32_exact_consumer.json", h_proof)
        row_proof = prep_whole_array_consumer(words, descriptor, paid_words, paid_descriptor, caller)
        save("independent_complete_wrapper_row_consumer.json", row_proof)
        phase = c130_ccx_absolute_phase()
        save("fresh_independent_absolute_CCX_phase.json", phase)
        save("universal_preparation_wrapper_operator_proof.json",
             prep_universal_composition(descriptor, h_proof, paid_proof, row_proof, phase))
        save("five_fixed_structural_negative_controls.json",
             prep_fixed_negative_controls(descriptor, caller, h_forward, h_inverse))
        save("original_cohort_full_wire_diagnostics.json", prep_fixed_diagnostics(words, descriptor, table))
        save("actual_whole_template_resources.json", prep_actual_resources(words, descriptor, paid_descriptor))
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = {"schema": "f44-q32-preparation-compact40-wrapper-summary-v1", "passed": True,
                   "completed": True, "budget_censored": False, "row_id": PREP_ROW_ID,
                   "certificate_scope": "EMITTED_SINGLE_Q32_TEMPLATE_TWO_COMPACT40_PAID_CLAMP002_WRAPPERS_ONLY",
                   "actual_single_H32_template_and_compact_wrapper_audited": True,
                   "actual_whole_template_A_inverse_and_absolute_phase_checked": True,
                   "actual_all_original_caller_pointer_metadata_audited": True,
                   "actual_original_full_financial_preparation_instantiated": False,
                   "logical_composed_forward_reverse_calls": [128, 128], "physical_sweeps": 2,
                   "two_paid_components_per_composed_direction": True,
                   "original_cohort_SHA256": CLAMP_OWNED["fixed_grid_diagnostics.json"],
                   "completed_owner_manifest_SHA256": {name: item[0] for name, item in OWNERS.items()},
                   "completed_owner_complete_counts": {name: item[1] for name, item in OWNERS.items()},
                   "both_full_uncached_input_unions": [first, second], "current_runtime": runtime,
                   "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()}
        save("summary.json", summary)
        save("completion_outcome.json", summary)
        owned = inventory(OUTPUT)
        files = {path.name: digest(path, fresh=True) for path in sorted(owned)}
        manifest = {**summary, "schema": "f44-q32-preparation-compact40-wrapper-manifest-v1",
                    "manifest_self_hash_excluded": True, "files": files, "frozen_inputs": _FROZEN,
                    "external_runtime_inputs": _EXTERNAL, "ROOT_READY_SHA256": args.ready_sha256,
                    "clamp_dependency_manifest_SHA256": CLAMP_SHA,
                    "terminal_budget_observation": {"process_CPU_seconds": time.process_time(),
                                                    "wall_seconds": time.monotonic() - _STARTED}}
        complete_manifest(manifest, files, sum(path.stat().st_size for path in owned))
        budget()
        print(json.dumps({"passed": True, "completed": True, "CPU": time.process_time(),
                          "wall": time.monotonic() - _STARTED, "certificate_scope": summary["certificate_scope"],
                          **flags()}, sort_keys=True))
        return 0
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
