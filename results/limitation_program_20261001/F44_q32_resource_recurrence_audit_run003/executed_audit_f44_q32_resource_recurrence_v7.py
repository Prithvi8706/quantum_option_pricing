"""Local fixed resource recurrence audit; prospective policy cannot grant execution."""
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
AUTHOR = RESEARCH / 'audit_f44_q32_resource_recurrence_v7.py'
METHOD_DOC = RESEARCH / 'F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V7.md'
PREFLIGHT = RESEARCH / 'f44_q32_resource_recurrence_audit_preflight_v7.json'
READY = ROOT / '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run005.json'
OUTPUT = ROOT / 'results/limitation_program_20261001/F44_q32_resource_recurrence_audit_run003'
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
CURRENT_MODULE = 'research.limitation_program_20261001.audit_f44_q32_resource_recurrence_v7'
CPU, ADMISSION, WALL = 600, 270, 900
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
FAILURE_NAMES = ("FAILED_UNSEALED.json", "failed_unsealed.json", "failure.json", "run_failure.json", "prepare_failure.json")
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_FAILED_INVENTORIES, _CODE_CACHE_EXPECTED = {}, {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_PLAN = None
_SCIENCE_ADMITTED = False
_OUTPUT_CREATED_BY_THIS_RUN = False
_RUNTIME_CORRECTION = None
_ROUTE_CORRECTION = None
RUNTIME_CORRECTION_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_ORIGINAL13_RUNTIME_MEMBERSHIP_CORRECTION_run002.json'
ROUTE_CORRECTION_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json'
ROUTE_CORRECTION_SHA = '36747dd106ccc6a8cfd8363d76835f2ac6f3029b8d15bb8699de3439cada04a5'
_PACKAGE_TREES = (ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath",
                  ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath-1.3.0.dist-info")
REFERENCE_NAMES = ("c130_native_row", "c130_schedule_interval", "c130_resources", "prep_resource_interval", "prep_actual_resources")
REFERENCE_FILENAME = "<current-f44-resource-reference-five-exact-definitions>"
STARTUP_EXPECTED = {'.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc': {'SHA256': 'd8536aedd91ba3763b64147357c5e8c0a270b6a8031a59130c10d10351ce879e', 'bytes': 1137}, '.context/frontier_t0_env/Lib/site-packages/__pycache__/_numba_cuda_redirector.cpython-312.pyc': {'SHA256': 'a440fa4055a99394bebc66cb280485004252f138d989b2d51fee17e9b3f213a1', 'bytes': 3609}, '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.pth': {'SHA256': '85a35d0fa0411036458d81dc56ae69bda1059d83882b7e2fe1bc3a5874213421', 'bytes': 176}, '.context/frontier_t0_env/Lib/site-packages/_cuda_bindings_redirector.py': {'SHA256': '25ed97b37208b2dba48d5732aa44899fa218c85d2c33148743ead8cc60d34fce', 'bytes': 854}, '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.pth': {'SHA256': '526df5910c1cc887b69adb485d6a42cef3a1af0185fcd0640cb8a97f8bc3d77e', 'bytes': 174}, '.context/frontier_t0_env/Lib/site-packages/_numba_cuda_redirector.py': {'SHA256': '854bdc54e933b3b1804d88454a4e51c2ecfdd59f6871e5957b97e5a344570d85', 'bytes': 2893}}
STARTUP_CACHE_KEYS = ('.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc', '.context/frontier_t0_env/Lib/site-packages/__pycache__/_numba_cuda_redirector.cpython-312.pyc')
INTERPRETER_PINS = {'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python.exe': 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b', 'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Scripts\\python.exe': '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5'}
METHOD_ADMISSION_PINS = {'.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '5419ad4d1d417b4ad65269ecdafcc5553b2ecd01582f2d568de678065b00b381', '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_PLANNING_AUTHOR_QA_run001.json': 'cdd47e4d5d344ac2a2727e6632928cd70a44ace74e010d1044d977d1a370aa74', '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_PLANNING_SUPPLEMENT_run001.json': '9b92a4a151b56348abb3d235b4c7b54a8eae10d0f8e34206d14029227a6ec1ed', '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_PLANNING_SUPPLEMENT_run001.md': 'b7b7416429163cf840e627108c4b9ab9d796e86faeb91389d04e7dffc8d6674f', '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': '9ac5b9db61c36997e3e91b7600e5d8e7e445f6eef89f683ee7e36f13bf1dc34d', '.context/F44_Q32_SHARED_QROM_FUSED_RESOURCE_RECURRENCE_INDEPENDENT_SYMBOLIC_METHOD_PEER_next_run001.json': '5c07db7abf7e4428a3f852697a07fe7ca53f31be7c8b4ebc8f807ad23cb05e83', '.context/F44_Q32_SHARED_QROM_FUSED_RESOURCE_RECURRENCE_METHOD_PROSPECTUS_run001.json': 'b32be58539d409b957db4592ff4aeca1b3f79bfd9bb2a378998a61e4064c0e18', '.context/F44_Q32_SHARED_QROM_FUSED_RESOURCE_RECURRENCE_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'b6f71bbee142e7652b885e762dc3359212a071170ee30e49993923c58ea9943e', '.context/F44_Q32_RESOURCE_RECURRENCE_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': '664be4ccee4c6000277a38ec69e479a4e681e2457479514f919530e336ce2ba3', '.context/F44_RESOURCE_RECURRENCE_CONTROLLER_AUTHOR_STATIC_FAILURE_HISTORY_run001.json': '5cd4d71f41a105cca7c00441cc164f8f81cf1a0f26719badd0b8eb751af85b19', '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_SCIENTIFIC_LIFECYCLE_STATIC_PEER_v14_run001.json': '61ec89e84d89d64029b585437156263d03f0a9a2c9b7afe7c2db0cc046db2243', '.context/F44_Q32_SHARED_QROM_FUSED_RESOURCE_RECURRENCE_METHOD_PROSPECTUS_run001.md': 'c5e0189c1a1db4e26343be5dbc97d912fa49f9875b91dcae302fad6a6c9969e2', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run001.json': 'e8d18991b9d61e3c65c6203dec9a21f6367b6bf6e983a9da272f3d61f20ff3de', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_SOURCE_METADATA_QA_v14_run001.json': 'bd5e96f333cc7c394c5d1ffb1d67a81e0943b44dabf424e37796d59f8f6b65dc', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run001.json': '46591ceacba1786ec36f8b25de3b7bb372427f95b9181726c5322161349e8d6a', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_REVIEW_RELEASE_ASSEMBLY_INDEPENDENT_PEER_v14_run001.json': 'f4cb014f61d0140a57c091076127e6d57922b939a9fda15b0702e6bc3c7121fe', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_UNKNOWN_RUNTIME_SOURCE_EXPECTATION_INDEPENDENT_HOLD_v14_run001.json': '87ae01536111ca73beb10247db99d24d2adc19072adc1bc959b097a34ad5d0a6', '.context/F44_Q32_RESOURCE_RECURRENCE_ORIGINAL_RUNTIME_MEMBERSHIP_CORRECTION_run001.json': '528196826f5bbed009e7a9fa1b4361b05386ac0be2f668788cc40708cd4dc47b', '.context/F44_resource_recurrence_ROOT_release_run001.py': '8c1e4c7f8bddbf6ba342e8457e012a32f3a6c8a2859fd3fe2c3d01d183ca23b1', '.context/F44_resource_recurrence_ROOT_static_review_run001.py': '3e97115503e78cface63ff5f57f0996ac9b856962274aa56695ab060d56f5525', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V1.md': 'b71fc0fc7609e96e1df0961b231404a7314eee06f86a9ac4e304a7935f6628cb', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v1.py': 'f763a73289c70c3e8da798d51328023ba751e7f59610f161435fe1b9aad9b731', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v1.json': 'f4f41c6ce4d77d52abe9360100e0c60ad562f2058516795d66cbae10cff7e4a3', '.context/F44_Q32_RESOURCE_RECURRENCE_V2_FIXED_RUNTIME_AND_ROUTE_ROOT_AUTHORING_CORRECTION_run001.json': 'a456c8e9dadee4f3f4432bfd2ae5c4c246b2b403be1ce592a2a2107ac8a35a3b', '.context/F44_Q32_ORIGINAL13_ADJACENT_RUNTIME_EXPECTATION_EVIDENCE_run001.json': '706ccea0dbee6edf29f99acb6f8fd506a60bba2b44bf2ec8e4b90a437446eec0', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run002.json': '696182100efcba2d102963f0dcfd7e906e257f87b3faf328e31e95541837cec3', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run002.json': '66f7a1c7616c64dc1b7a7cb524660956d21e352a434376c3c6ca5b914bfd9560', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run001.json': '06a9f25c00a9a74fa7a70d1c65d1b39d986ca1249ac877d6ca8389c940528019', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_STATIC_REVIEW_run002.json': 'c6a18e2084c371287ccbfa9e0cce804443ba9ed22fe29559260c93dd5d8c8c3a', '.context/F44_RESOURCE_RECURRENCE_PREOUTPUT_RUNTIME_FAILURE_OUTPUT_PATH_ROOT_CORRECTION_run001.json': '1a87b43b5c1a48e74509a7c4b35376613a515b2fd61904e16cdcb3fd3661ab7b', '.context/F44_RESOURCE_RECURRENCE_PREOUTPUT_RUNTIME_MEMBERSHIP_FAILURE_ROOT_FREEZE_run001.json': '7373a22f6ee4a397d0f11ac27db3e3d036e24e64560444f5861193f786de997a', '.context/F44_resource_recurrence_audit_actual_run002.log': '8e5686840dabc07778545ad2e660921fb20d7c6b4d6db02354d9e68e0a762eb7', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V2.md': '37a29bb022af142d7803f2d5d6b7d5db3e6552c76828d4c2f0823246203998a7', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v2.py': '33638cd7cd3d260fca58b2efc8719288f209557651aa2f93417287ddf68c2e52', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v2.json': '87e56282900dda07ab03dec5a3aac1b508cbd074723e163b4cefc30c704bbcc9', '.context/F44_Q32_RESOURCE_RECURRENCE_V3_ORIGINAL13_RUNTIME_AND_ROUTE_ROOT_AUTHORING_CORRECTION_run001.json': '88a00f40c2c38f19f81a6b26a7cb3b2df5abd8697b5fa18884dfe49c997030a2', '.context/F44_Q32_RESOURCE_RECURRENCE_ORIGINAL13_RUNTIME_MEMBERSHIP_CORRECTION_run002.json': '9cf41770b473061be40999e74e807609777b582ef6c26904cd6761170426b5b1', '.context/F44_Q32_RESOURCE_RECURRENCE_V3_ORIGINAL13_RUNTIME_AND_AUTHORING_INDEPENDENT_METADATA_PEER_v14_run001.json': '568de0a57207806f366bb11483d5cfc52a76ec719d2fe9b5059dae2972ae1417', '.context/F44_RESOURCE_RECURRENCE_FAILED_RUNTIME_MEMBERSHIP_READONLY_DIAGNOSTIC_run001.json': '3b046266d3b48364ead676640b21e706d6199c46c0cbff8eb86d2cd96cda2b1a', '.context/F44_RESOURCE_RECURRENCE_PREOUTPUT_CLI_ARGUMENT_FAILURE_ROOT_FREEZE_run001.json': '3476ddd903be3df51b09010830c33db2c429dfade48c4f4494a66f74338c18fb', '.context/F44_resource_recurrence_audit_actual_run001.log': 'b764a2a8037538cca8253b840b7075522de702fc9f094f8564a00ccc89de9dd2', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_FUNCTION_ROLE_SUPPLEMENT_run002.json': '14fd524385f7fec4c361c35329c064e061db51851994c3ffba6b14423e840df2', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_AST_DIFF_run002.json': 'e2315c4a43253b8a68fb91b3ac0f42d8105606b0f7dfe9df74b9b677c44b083b', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_AST_DIFF_run003.json': '6b7259b5d28d30c1c09f132610fd12b3737ce58d015d1e61df7740539ef2ddc8', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_FUNCTION_ROLE_SUPPLEMENT_run003.json': 'ae3a0093dee01dfcd5310dcd4ca112d8d58359560dbc7d1ae48af323450132fa', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run003.json': '08a4185bd68f09005eb3c11dab5d3f1dbb2d68d5d0d3057ffabcb5f8e8d33f55', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run003.json': '15dc0010c1d078ac6942d53c8f3d80d3fef441f7fd02052eea858d06577de3ba', '.context/F44_Q32_RESOURCE_RECURRENCE_V3_HISTORICAL_CACHE_LIFECYCLE_ROOT_HOLD_run001.json': '724bfe3f9b33eb3ac10776ffe8956d695b119504669fe766d018ebbb90687f1c', '.context/F44_resource_recurrence_ROOT_review_release_run003.py': 'c780b67fc68cbf29c1642560a60d666936781c44e44b693819916a98a3d380a1', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V3.md': '2456ff7c20a4476141a248b809504cf1d0879d79a89399043e1ae543315f9aca', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v3.py': '9fada4b35f057f672689933cb1987a33217ae8fabe5b9030b7aa86f34a65bb8a', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v3.json': '9c449d6e634f51bb1bc41cedb2adfe03325218349a98093cf7296b280f19d068', '.context/F44_Q32_RESOURCE_RECURRENCE_V4_COMPLETE_HISTORICAL_CACHE_ROOT_AUTHORING_CORRECTION_run001.json': 'bf7a09c015152423dc9d2e9f7f9f45de9f1b950619596f92d870c41330eee7c3', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_RELEASE_V3_ASSEMBLY_INDEPENDENT_HOLD_v14_run001.json': 'ce0f73a99ce85c034fb0b67820f7b17eef1ca0a12b93f570c57935b8486aa4bf', '.context/F44_Q32_RESOURCE_RECURRENCE_V4_COMPLETE_HISTORICAL_CACHE_AUTHORING_INDEPENDENT_METADATA_PEER_v14_run001.json': 'd9c37213f764536b926740e0159af7ec1a47e4525cd70df9a9732b7f193a6a23', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run004.json': 'fb9edff0340185a214a8ba3164b0ce49089fab3b5189149c5430ba5b80fbf0f0', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run004.json': 'b966a81a62a98808730f174d7cd686ac50827aa8c6e70b91556eb12eb797ac67', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run002.json': '0d064c2bb47b005019fecf4092baea7231956aa46d90b05e25235c4ecf3be001', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_STATIC_REVIEW_run004.json': '17397b2414fa7b90ab79da52a9d3ef5fd247135643fe94348c54d52867ead042', '.context/F44_RESOURCE_RECURRENCE_V4_WRAPPER_CPU_CENSORED_ROOT_FREEZE_run001.json': 'd5beef7bda2adb42ac224acec27f9fe89ee7a821692af03aff51391b1d7e9463', '.context/F44_V4_FIXED_ARITY_CLOCK_RECURRENCE_STATIC_OPTIMIZATION_REVIEW_v14_run001.json': '2777d5ce3e6f602565cf061b3ea32c3ab66134d2b18b115956037f7fd01e1acc', '.context/F44_resource_recurrence_audit_actual_run003.log': 'a23f111759564739e40890f83a7f73004b58d2dd404fcd95a3ea223568d4ecdf', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V4.md': '548092e522e3049d1a65ab5b547e69b40872876e5b400f7bc2ae8eb29ad848d0', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v4.py': '05e925fa800e023402775889d2cb5fe9db838d1446c015b52309a638ab51386e', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v4.json': '72d7ac14379eca4caadc41bfe690df2575048f3c99f0dee49284c784be1d1275', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_INDEPENDENT_METHOD_PEER_run001.json': 'c62a538c66c2f3a875e3a1c1b580853e1257bea72cf0ec0c6a023b0f57a2187d', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_METHOD_AUTHOR_METADATA_QA_run001.json': '940ae75dd433a7affe6d25638c136d29649daae286d15542b2721ab1753407b4', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_METHOD_PROSPECTUS_run001.json': '0e64be4efe87c4bc79933dd72647fe2690b81a68118318779dcb444e9cdde299', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_METHOD_PROSPECTUS_run001.md': 'aad01035f0de5d525a38d46b2512d01fada0ea96c6c111437f5d7bf13faaad4d', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_ROOT_METHOD_REVIEW_run001.json': '412992fd613e85653ed4809f1c67714542dc5ffae56bac11c719a11ae8792a8f', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'cedf660fba03f1bb1c4fd39b56a143dcea6c606fe27837493ba12b8b19c74ecd', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_FUNCTION_ROLE_SUPPLEMENT_run004.json': '634cb6f68062d8bd1ca7789afba3121210780cdd4259bbc9b2b46ca1a255db50', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_AST_DIFF_run004.json': 'a0d3e15b168a7130bfd73efaf2f064e5c28b8f1044f8565b2a0a5538744e4d6d', '.context/F44_V5_max_plus_ROOT_controller_authoring_acceptance_run001.py': 'ad4a82430f6634f62010cf515278336112dcfb75e6c385254c574583dbbf0b4c', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_AST_DIFF_run005.json': '7ed7b194d9705a7db53dda20fa59fea97f37b74cc076629952eee000ba49bc0c', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_FUNCTION_ROLE_SUPPLEMENT_run005.json': 'a606a42cf097b1be9bc2b214fdb848a4f1138e90338d90ae7316925f0c0649db', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run005.json': 'f2515e03b06025d7e3c458237cbcb1d64f44af5b5ccf9088834d44eb4b64d220', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run005.json': 'ef7b983d4ce89d5263b923c069efc836eed4c1b15593935ff823e3d444bdb94b', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_ROOT_ACTUAL_SOURCE_REVIEW_ATTESTATION_run001.json': 'dd15575e5558d87c7f13030728f52224d1843cba196fd6f8d28364669c2fe5f1', '.context/F44_Q32_RESOURCE_RECURRENCE_V5_ROOT_LIFECYCLE_HOLD_run001.json': '0d663505e7a20222502d8ee972133f1ddd95afad3b3b8a5f703af93d1c57ae7b', '.context/F44_V6_decimal_admission_ROOT_METHOD_review_run001.py': '9c25f366775b7077136c472ec4709cd23c8b574c3d703095c0b25aca1bf1fea2', '.context/F44_resource_recurrence_ROOT_review_release_run005.py': 'b21048207000c4586c853297d01e11ccf5c528e17bf9887654c83fecf4949ccf', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V5.md': '6964a1108406a83822a2fcdca6c4fa62ac13708cb9999c52e2ed3874918db354', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v5.py': '6f4e03d790f591487b020cd2387f52483754a56c367ed086bcdbaa17eab273b7', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v5.json': 'c5508d9583a3e569b5c73f24dd4d84d3213a94f3fc025b27de8e1f425798d14c', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': 'ccb285448e200865b955d5bf347e173d9a6ac811baa923697d0f4d9c981824ce', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_METHOD_AUTHOR_METADATA_QA_run001.json': '45e946b96452fe1c816b3fa4ff060ac16d721488a4ae6d080388e29c6bf382aa', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_METHOD_SUPPLEMENT_run001.json': 'ce306e99dc1a4cdd802d565e43fb2a735bb83371dd8c1e78e3165b79a4b52184', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_METHOD_SUPPLEMENT_run001.md': 'c8db33b0e399a8e75bcd4160031bf617a8169165193dac9478d9884e0f5107bf', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_ROOT_METHOD_REVIEW_run001.json': 'f68cc4a08d56614c64c52d82a18241345215bc70cb213004c084d600dcfd3dc4', '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': '36747dd106ccc6a8cfd8363d76835f2ac6f3029b8d15bb8699de3439cada04a5', '.context/F44_resource_recurrence_V5_atomic_author_full_QA_run001.py': 'd44272b761ccff782709b737c3636e85fa4a4be57620c31d52dd68e124a6ddad', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_AST_DIFF_run006.json': '5c05ba08c1cbd03931ece86b2f4e3adba91c5fb355ec5e8b3d0163f5e29f444e', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_FUNCTION_ROLE_SUPPLEMENT_run006.json': 'e5bd72250066bb2fc045452e3669e4941800684e488382160e6089bcf2ce26e4', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run006.json': '2703f81941da9eed8c5916211f21b46cb560e699fe8a79486e60bf8b12a8a092', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run006.json': 'a83f2c7220fe19678f33e3d24652f13955025943397b7ea07584ebd9c5c71770', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run004.json': 'ad2fb1c21524068fecb082480689c1830c65736eb802c40b5c8d0328472a2e17', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_STATIC_REVIEW_run006.json': '0bc459b7c97a466bcf50862f8a9bf7f0cf3263f39369d104f52d338331ac6236', '.context/F44_RESOURCE_RECURRENCE_V6_WRAPPER_REFERENCE_CPU_CENSORED_CUSTODY_PROPOSAL_run001.json': '468cad69ea40016b7fba097fdc947d93b5ae39af292204647b77ac462cbb1a93', '.context/F44_RESOURCE_RECURRENCE_V6_WRAPPER_REFERENCE_CPU_CENSORED_INDEPENDENT_SAVED_FIELD_PEER_run001.json': '39e8031882d06c7fd1eb12e71a531a3c4fae0855b57fb2fee4e89120122ced57', '.context/F44_RESOURCE_RECURRENCE_V6_WRAPPER_REFERENCE_CPU_CENSORED_ROOT_FREEZE_run001.json': 'a2d8994d5d5d7e682a2a0ac0d6c0e6b1984bb660c7339b633f39e5e679898955', '.context/F44_V6_wrapper_reference_CPU_censored_ROOT_failure_freeze_run001.py': 'da6cb681690926d48d20840766da79dec044f494b62de8a95c255496de63becb', '.context/F44_resource_recurrence_V6_actual_ROOT_saved_result_review_run001.py': '2533f6f7d7cdb07fe3eb5f09c6e6d27481469111a45c7142d4138a0fe5870255', '.context/F44_resource_recurrence_V6_actual_run001.log': '1f5e6aba1adb6dc5678dd2c5cce3f10e267341c637e55389ac5aa5323a8491d7', 'research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V6.md': '6edf31d9f808bfe12bec0553d73a041df33989b4f0fef82a312e7c11b1cbb892', 'research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v6.py': '440ee922662e3f4958a038f1b422da3c0ae24d9b71f98c9e75c43e93acd6f690', 'research/limitation_program_20261001/f44_q32_resource_recurrence_audit_preflight_v6.json': 'b6d46d72605ce0a6d99d9e6f9e594d25a505b254807172fb1b5fd42d93fe0d24', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_INDEPENDENT_METHOD_PEER_run001.json': '4032923458d2186c0a088cb1967fbff09fd146275ee6de914c095e6764c088cd', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_METHOD_AUTHOR_METADATA_QA_run001.json': '6062fb2308a7e6f77f6b504e3dff40afc0e669cb940059856beb252fdf24e1e0', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_METHOD_SUPPLEMENT_run001.json': 'b2167738ded45b24295ce2dfb653bb47973bc0a10cfc304ff5f8a0ee41f0f4d9', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_METHOD_SUPPLEMENT_run001.md': '754a8ff702dc753a5906724705ab5514be16590dea6d7e840161a6f04c0db2f2', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_ROOT_METHOD_REVIEW_run001.json': 'b7d2c4fc623e1505527b21ad18f86ea6d07b053ebef0e4575f9ef4db6e40f7ab', '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': '672a780255b86f18ecb1e49e420db922944deb287d142b35894b9c2970fc72bc', '.context/F44_resource_recurrence_V6_atomic_author_full_QA_run001.py': '5b08f890eb796a506aadfaef8a3eb6142d18d4e3932fd5a2d936c62fa01c53af', '.context/F44_resource_recurrence_V2_atomic_author_full_QA_run001.py': '8df4b3504d0147abf310df82ccd70f89ac54046853c6ee513aacf7cb245f886a'}
ADMISSION_PLAN_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_FINITE_ADMISSION_PLANNING_SUPPLEMENT_run001.json'
REQUIRED_CURRENT_REVIEW_PATHS = ('.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_AUTHOR_STATIC_QA_run007.json', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_INDEPENDENT_STATIC_PEER_run007.json', '.context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_STATIC_REVIEW_run007.json')
ORIGINAL_OWNER_NAMES = ('A14_cosine_feasibility_audit_run003', 'A14_cosine_feasibility_run001', 'A14_taylor_f44_stage_C_audit_run001', 'A14_taylor_f44_stage_C_grid_axis_run003', 'A14_taylor_f44_stage_C_grid_clamp_run002', 'A14_taylor_f44_stage_C_grid_shared_qrom_run001', 'A14_taylor_f44_stage_C_root_verification_run001', 'A14_taylor_f44_stage_C_run003', 'A14_taylor_f44_stage_K_audit_run001', 'A14_taylor_f44_stage_K_root_verification_run001', 'A14_taylor_f44_stage_K_run001', 'F44_QROM64X8_comparison_run001', 'F44_q32_preparation_compact40_wrapper_run002')
FIXED_OWNED_FILES = ('executed_audit_f44_q32_resource_recurrence_v7.py', 'executed_F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V7.md', 'executed_f44_q32_resource_recurrence_audit_preflight_v7.json', 'executed_F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run005.json', 'original_manifest_A14_cosine_feasibility_audit_run003.json', 'original_manifest_A14_cosine_feasibility_run001.json', 'original_manifest_A14_taylor_f44_stage_C_audit_run001.json', 'original_manifest_A14_taylor_f44_stage_C_grid_axis_run003.json', 'original_manifest_A14_taylor_f44_stage_C_grid_clamp_run002.json', 'original_manifest_A14_taylor_f44_stage_C_grid_shared_qrom_run001.json', 'original_manifest_A14_taylor_f44_stage_C_root_verification_run001.json', 'original_manifest_A14_taylor_f44_stage_C_run003.json', 'original_manifest_A14_taylor_f44_stage_K_audit_run001.json', 'original_manifest_A14_taylor_f44_stage_K_root_verification_run001.json', 'original_manifest_A14_taylor_f44_stage_K_run001.json', 'original_manifest_F44_QROM64X8_comparison_run001.json', 'original_manifest_F44_q32_preparation_compact40_wrapper_run002.json', 'failed_composition_V1_freeze.json', 'failed_composition_V1_diagnosis.json', 'failed_composition_V2_freeze.json', 'failed_composition_V2_diagnosis.json', 'interpreter.json', 'protocol.json', 'run_started.json', 'complete_owner_maps_and_inventories.json', 'history_cache_and_nonpromotion_roles.json', 'fixed_resource_parity_corpus.json', 'conditional_recurrence_induction_and_macro_authority.json', 'toy_exact_X_CX_CCX_H_empty_unused_wire_parity.json', 'toy_local128_boundary_parity.json', 'toy_all_empty_H_only_parity.json', 'saved_shared_QROM_component_full_parity.json', 'saved_preparation_wrapper_full_parity.json', 'all_projected_checkpoints_and_new_interleaving.json', 'three_exact_structural_controls.json', 'fresh_full_input_union_before_resources.json', 'fresh_full_input_union_after_resources.json', 'qualification_and_remaining_gaps.json', 'summary.json', 'completion_outcome.json', 'manifest.json')
C130_CCX_MACRO = (('H', 2), ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 2), ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 1), ('T', 2), ('H', 2), ('CX', 0, 1), ('T', 0), ('TD', 1), ('CX', 0, 1))

_PRIOR_ROUTE_CORRECTION = None
_MAXPLUS_METHOD = None
_F44_V4_HISTORY = None
_FAILED_V4_INVENTORY = {}
_OUTPUT_IDENTITY = None
_PHASE_OBSERVATIONS = []
PRIOR_ROUTE_CORRECTION_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V4_COMPLETE_HISTORICAL_CACHE_ROOT_AUTHORING_CORRECTION_run001.json'
MAXPLUS_METHOD_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_METHOD_PROSPECTUS_run001.json'
MAXPLUS_METHOD_SHA = '0e64be4efe87c4bc79933dd72647fe2690b81a68118318779dcb444e9cdde299'
PHASE_FIXTURES = ('toy_exact_X_CX_CCX_H_empty_unused_wire', 'toy_local128_boundary', 'toy_all_empty_H_only', 'saved_shared_QROM_component', 'saved_preparation_wrapper')
PHASE_NAMES = ('original_reference', 'equivalent_native_transition', 'parity_and_render_join')

_DECIMAL_POLICY_ADMITTED = False
_DECIMAL_METHOD = None
DECIMAL_METHOD_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V6_DECIMAL_ADMISSION_METHOD_SUPPLEMENT_run001.json'
DECIMAL_METHOD_SHA = 'ce306e99dc1a4cdd802d565e43fb2a735bb83371dd8c1e78e3165b79a4b52184'

_FIXED_BUDGET_METHOD = None
_FIXED_BUDGET_AUTHORITY = None
_F44_V6_HISTORY = None
_FAILED_V6_INVENTORY = {}
BUDGET_METHOD_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_METHOD_SUPPLEMENT_run001.json'
BUDGET_METHOD_SHA = 'b2167738ded45b24295ce2dfb653bb47973bc0a10cfc304ff5f8a0ee41f0f4d9'
BUDGET_AUTHORING_PATH = '.context/F44_Q32_RESOURCE_RECURRENCE_V7_FIXED_BUDGET_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json'
BUDGET_AUTHORING_SHA = '672a780255b86f18ecb1e49e420db922944deb287d142b35894b9c2970fc72bc'


# Exact original generic and archival metadata guards only.
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

AXIS_NAME = "A14_taylor_f44_stage_C_grid_axis_run003"

AXIS_HELPER = RESEARCH / "f44_cosine_caller_grid_axis_source_v1.py"

HELD_CLAMP_V1_AUTHORS = {'experiment_f44_cosine_caller_grid_clamp_v1.py': '6830c5310afff26258a036d0bfe5420683a8ae181dc56b529cf0a73ae933657e', 'f44_cosine_caller_grid_clamp_source_v1.py': '5519a388357c7d7d11d1b007144a99c46581a62dfa04c22086a6a38f3244f3d9', 'F44_COSINE_CALLER_GRID_CLAMP_PREFLIGHT_V1.md': 'a90f9411932aa00212f4559f612ace81fdf0031e457cd9a1ea5a5d31f84238c3', 'f44_cosine_caller_grid_clamp_preflight_v1.json': '33fda25ba221e003e4305d80e9e538a8ccd6fa64a3998d570b603fb6c4e2792c'}

HELD_CLAMP_V1_REPORTS = {'.context/F44_COSINE_CALLER_GRID_CLAMP_AUTHOR_STATIC_QA_next_run002.json': 'c839ba6f4200cf8e07bed37656b71bad6fc587cd28df59758f872d278a2bd418', '.context/F44_COSINE_CALLER_GRID_CLAMP_ROOT_STATIC_HOLD_run001.json': '7e7b1fb337b96ca95f3efb7d392dd96f393ae26fcdd803c89d22fc7f446400dd', '.context/F44_COSINE_CALLER_GRID_CLAMP_INDEPENDENT_STATIC_HOLD_run001.json': '5f5fb2eb32e6fac52a3d5db48405a341b6bf1be4209cca0b5af51a7aa43fd243'}

HELD_CLAMP_V1_READY_KEY = ".context/A14_F44_COSINE_CALLER_GRID_CLAMP_ROOT_READY_run001.json"

HELD_CLAMP_V1_OUTPUT_KEY = "results/limitation_program_20261001/A14_taylor_f44_stage_C_grid_clamp_run001"

LEGACY_CLAMP_HELPER = RESEARCH / "f44_cosine_caller_grid_clamp_source_v1.py"

CLAMP_PREREQUISITE_OWNERS = {'A14_cosine_feasibility_audit_run003': ['52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f',
                                         [17, 752, 2842]],
 'A14_cosine_feasibility_run001': ['bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b',
                                   [24, 672, 2842]],
 'A14_taylor_f44_stage_C_audit_run001': ['3de0e4a36928a630481ff12ba727e2fdc50512b6bd60b2cc2e94edbeb95d42ee',
                                         [17, 890, 2842]],
 'A14_taylor_f44_stage_C_grid_axis_run003': ['a6999915ecf45d96fc2ab89b16cc9b6499dd63cc807d6166a789b73bf1439bc2',
                                             [20, 954, 2842]],
 'A14_taylor_f44_stage_C_root_verification_run001': ['18da7c127f649014945cd4a3cc07360053a6394ac48f70851a40d786850a618d',
                                                     [8, 916, 2842]],
 'A14_taylor_f44_stage_C_run003': ['7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa',
                                   [34, 851, 2842]],
 'A14_taylor_f44_stage_K_audit_run001': ['2c253beba55b1271dec594db8231c8bdbfcaffbf4d797dedb840eda72568f5be',
                                         [10, 796, 2842]],
 'A14_taylor_f44_stage_K_root_verification_run001': ['24e316217afd614b577fe53921f54b7ad7c346737ec6e21c93500a795a1517d9',
                                                     [8, 811, 2842]],
 'A14_taylor_f44_stage_K_run001': ['b03c8a7cb62655301b9a231eb987f38e5ec496f612206ff6701143f6cefb8b88',
                                   [17, 774, 2842]]}

ORIGINAL_CLAMP_V2_POLICY_KEY = 'research/limitation_program_20261001/f44_cosine_caller_grid_clamp_preflight_v2.json'

ORIGINAL_CLAMP_V2_POLICY_SHA = '2913f50f4a72c184944f4f704fc7676684c79b2667f2da6e0e8e206b851a8d65'

WRAPPER_V1_AUTHORS = {'F44_Q32_PREPARATION_COMPACT40_WRAPPER_PREFLIGHT_V1.md': 'bd3cc5c2f59635b856d9ba81e636a6f8d9197a46ebba1e82147298b499c36a48',
 'experiment_f44_q32_preparation_compact40_wrapper_v1.py': '4bdb91b191610c7954a3723e950f2f5514c30cbba7f63e441ebd2815235bb67b',
 'f44_q32_preparation_compact40_wrapper_preflight_v1.json': 'bb3d0c8a978a92fe186fd2bf3f551723e768ff35581e3324f51c37e088586a0f',
 'f44_q32_preparation_compact40_wrapper_source_v1.py': '355839d8bdf63772bd7d480d555810a67fc621f155c0a3bb858be280c3cc4606'}

WRAPPER_V1_METADATA = {'.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_AUTHOR_STATIC_QA_run001.json': '9d8de8ad199e579f9e955fa9aa9416eddf1efae556b2bd0e28c32b20e98c20ac',
 '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_INDEPENDENT_SCIENTIFIC_STATIC_SUPPLEMENT_next_run001.json': 'f1b005d1850d136ce39bbf4214e5679219982d1814756e15f62612c33aa1de6f',
 '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_INDEPENDENT_STATIC_HOLD_next_run001.json': 'adc3e359ec23c9ac11372e20f0692ae70426ec2dfb8df31cd2327c8ff87a72bc'}

WRAPPER_V1_READY_KEY = '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_ROOT_READY_run001.json'

WRAPPER_V1_OUTPUT_KEY = 'results/limitation_program_20261001/F44_q32_preparation_compact40_wrapper_run001'

WRAPPER_V1_HOLD_KEY = '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_INDEPENDENT_STATIC_HOLD_next_run001.json'

WRAPPER_V1_SUPPLEMENT_KEY = '.context/F44_Q32_PREPARATION_COMPACT40_WRAPPER_INDEPENDENT_SCIENTIFIC_STATIC_SUPPLEMENT_next_run001.json'

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
        root_path = Path(root)
        for name in dirs:
            candidate = root_path / name
            require(canonical(candidate).is_relative_to(directory), "No owned directory escape")
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(root_path / name)
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

def fixed_original_runtime_scope():
    """Exact original saved scope before enumeration; no live expected discovery."""
    require(_RUNTIME_CORRECTION is not None, "Direct externally pinned runtime correction admitted first")
    scope = _RUNTIME_CORRECTION["fixed_runtime_scope"]
    require(str(ROOT) == scope["ROOT"] and str(RESEARCH) == scope["RESEARCH"]
            and canonical(Path.cwd(), fresh=True) == ROOT
            and canonical(sys.executable, fresh=True) == Path(scope["LAUNCHER"])
            and canonical(sys._base_executable, fresh=True) == Path(scope["BASE_executable"])
            and canonical(sys.base_prefix, fresh=True) == Path(scope["BASE"])
            and canonical(sys.prefix, fresh=True) == Path(scope["PREFIX"])
            and _BASE_SCOPE == Path(scope["BASE"]), "All original root/base/prefix/launcher literals exact")
    require(sys.path == scope["exact_original_sys_path"]
            and _EXCLUDED_SCOPE == (Path(scope["excluded_base_site_packages"]),) * 2,
            "Exact original ordered search and lexical/physical excluded base packages")
    require(tuple(_PACKAGE_TREES) == tuple(Path(key) for key in scope["selected_mpmath_trees"])
            and sorted(str(ROOT / key) for key in STARTUP_CACHE_KEYS)
            == sorted(scope["explicit_startup_cache_absolute_paths"])
            and sorted(str(ROOT / key) for key in STARTUP_EXPECTED)
            == sorted(scope["exact_original_six_startup_absolute_paths"])
            and tuple(scope["recursive_trees"]) == tuple(str(path) for path in (
                _BASE_SCOPE / "Lib", _BASE_SCOPE / "DLLs", Path(scope["PREFIX"]) / "Scripts") + _PACKAGE_TREES)
            and tuple(scope["adjacent_directories"]) == tuple(str(path) for path in (
                _BASE_SCOPE, Path(scope["PREFIX"]), Path(scope["PREFIX"]) / "Lib/site-packages")),
            "Original five trees/three adjacent directories/selected packages/six startup records/two caches")
    require(sys.dont_write_bytecode is True and sys.flags.optimize == 0
            and "PYTHONOPTIMIZE" not in os.environ
            and not any(os.environ.get(key) for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")),
            "Original startup and runtime override predicates unchanged")
    zip_policy = _RUNTIME_CORRECTION["optional_zip_authority"]
    require(zip_policy["permitted_present_zip_expected_SHA256"] == {}, "No present runtime zip authorized")
    for key in zip_policy["exact_original_absent_standard_paths"]:
        path = Path(key)
        require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                "New or redirected standard zip rejected before any read/hash/add")
        _ABSENT_RUNTIME.add(path)
    return scope


def own_runtime():
    """Closed original3062 membership before any candidate observation is hashed."""
    global _STANDARD_RUNTIME_MEMBERS, _HASH_WORK
    scope = fixed_original_runtime_scope()
    expected = _RUNTIME_CORRECTION["current_runtime_candidate_expected_SHA256"]
    candidates = standard_runtime_members()
    require(type(expected) is dict and len(expected) == 3062
            and candidates == {Path(key) for key in expected},
            "Complete current runtime candidates equal original closed3062 keys before hashes/add")
    total = 0
    for path in sorted(candidates):
        budget()
        key = key_for(path)
        mapping = _FROZEN if path.is_relative_to(ROOT) else _EXTERNAL
        require(path.is_file() and key in mapping and mapping[key] == expected[str(path)],
                "Every candidate has pre-existing original admitted expectation before its digest")
        total += path.stat().st_size
        require(len(candidates) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
                "Original fixed24k runtime files/2GiB")
        require(digest(path, fresh=True) == expected[str(path)], "Actual candidate equals original expected SHA")
    require(total == _RUNTIME_CORRECTION["current_runtime_candidate_saved_bytes_metadata"],
            "Complete original candidate bytes remain exact")
    _STANDARD_RUNTIME_MEMBERS = candidates
    cfg_policy = _RUNTIME_CORRECTION["cfg_authority_before_read_or_add"]
    cfg = canonical(Path(scope["PREFIX"]) / "pyvenv.cfg", fresh=True)
    require(str(cfg) == cfg_policy["absolute_path"] and key_for(cfg) == cfg_policy["original_declared_key"]
            and key_for(cfg) in _FROZEN and _FROZEN[key_for(cfg)] == cfg_policy["original_expected_SHA256"]
            == expected[str(cfg)], "Cfg source already has its original literal pin before cfg read")
    before = fingerprint(cfg)
    require(before[2] <= 8 << 20, "Finite original cfg plaintext read")
    with cfg.open("rb") as stream:
        cfg_bytes = stream.read(before[2] + 1)
    _HASH_WORK += len(cfg_bytes)
    require(_HASH_WORK <= MAX_HASH_WORK and len(cfg_bytes) == before[2] and fingerprint(cfg) == before
            and hashlib.sha256(cfg_bytes).hexdigest() == cfg_policy["original_expected_SHA256"]
            and canonical(cfg, fresh=True) == cfg, "Stable cfg bytes equal original expected authority")
    require("include-system-site-packages = false" in cfg_bytes.decode("utf-8").lower(),
            "Original separately expected venv config excludes base site packages")
    loaded_origins()
    return {"files": len(candidates), "bytes": total, "base_site_packages_pruned_and_rejected": True,
            "closed_original_expected_candidate_membership": True, "observed_expected_promotion": False}

def standard_runtime_members():
    base = canonical(sys.base_prefix)
    candidates = set()
    excluded = base / "Lib/site-packages"
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts") + _PACKAGE_TREES:
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            root_path = Path(root)
            dirs[:] = [name for name in dirs if root_path / name != excluded]
            for name in dirs:
                require(not (root_path / name).is_symlink(), "No runtime directory alias")
                canonical(root_path / name)
            for name in names:
                candidates.add(canonical(root_path / name))
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

def fresh_union():
    runtime_scopes()
    fixed_original_runtime_scope()
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
        if path.is_relative_to(OUTPUT):
            continue
        require(path in union and union[path] == value, "Every input observation already has equal original expected authority")
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
        _STANDARD_RUNTIME_MEMBERS == {Path(key) for key in _RUNTIME_CORRECTION["current_runtime_candidate_expected_SHA256"]}
        and standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
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
    output_custody_guard()
    no_failure(OUTPUT)
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
    output_custody_guard()
    no_failure(OUTPUT)

def save(name, value):
    output_custody_guard()
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
    output_custody_guard()
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
    if not _OUTPUT_CREATED_BY_THIS_RUN:
        return
    try:
        output_custody_guard()
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
                "phase_CPU_wall_observations": _PHASE_OBSERVATIONS,
                **flags(),
            },
        )
    except BaseException:
        pass
    try:
        output_custody_guard()
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,'
                b'"hard_budget_state_uncertified":true,"new_test_credit":0,'
                b'"Stage_C_release_authorized":false,"full_G2":false,"adoption":false}\n'
            )
    except BaseException:
        pass

def fixed_integer_policy():
    global _DECIMAL_POLICY_ADMITTED
    budget()
    require(
        _DECIMAL_POLICY_ADMITTED is False
        and "PYTHONINTMAXSTRDIGITS" not in os.environ
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
    _DECIMAL_POLICY_ADMITTED = True
    budget()

def guard_serialization_integers(value):
    """A bounded representation guard; it neither rounds nor changes a value."""
    budget()
    require(
        type(_DECIMAL_POLICY_ADMITTED) is bool
        and "PYTHONINTMAXSTRDIGITS" not in os.environ
        and "int_max_str_digits" not in sys._xoptions
        and sys.flags.int_max_str_digits == sys.int_info.default_max_str_digits == 4300
        and sys.get_int_max_str_digits() == (INTEGER_DECIMAL_DIGITS if _DECIMAL_POLICY_ADMITTED else 4300),
        "Exact default4300 metadata or admitted20000 representation stage, never a bypass",
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
        and witness["limits_CPU_admission_wall"] == [300, 270, 900]
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
        and historical["limits_CPU_admission_wall"] == [300, 270, 900]
        and historical["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in CLAMP_PREREQUISITE_OWNERS.items() if name != AXIS_NAME}
        and historical["completed_owner_complete_counts"]
        == {name: item[1] for name, item in CLAMP_PREREQUISITE_OWNERS.items() if name != AXIS_NAME}
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

def admit_original_clamp_V1_history(ready):
    """Old current labels are consumed only in their exact historical policy namespace."""
    original_policy = read(bind(ROOT / ORIGINAL_CLAMP_V2_POLICY_KEY, ORIGINAL_CLAMP_V2_POLICY_SHA))
    admit_held_clamp_V1(ready, original_policy)

def admit_unexecuted_wrapper_V1(ready, policy=None):
    """Fixed V1 authors/reviews/absence and externally declared complete cache partition."""
    for field, expected in (
        ("wrapper_V1_author_expected_SHA256", WRAPPER_V1_AUTHORS),
        ("wrapper_V1_metadata_expected_SHA256", WRAPPER_V1_METADATA),
        ("wrapper_V1_READY_absent_path", WRAPPER_V1_READY_KEY),
        ("wrapper_V1_output_absent_path", WRAPPER_V1_OUTPUT_KEY),
    ):
        require(ready[field] == expected, "Exact immutable wrapper V1 history field: " + field)
        if policy is not None:
            require(policy[field] == expected, "Same new policy literal wrapper V1 scope: " + field)
    for name, expected in WRAPPER_V1_AUTHORS.items():
        bind(RESEARCH / name, expected)
    records = {key: read(bind(ROOT / key, expected)) for key, expected in WRAPPER_V1_METADATA.items()}
    hold = records[WRAPPER_V1_HOLD_KEY]
    supplement = records[WRAPPER_V1_SUPPLEMENT_KEY]
    require(hold["schema"] == "f44-q32-preparation-wrapper-independent-static-hold-v1"
            and hold["status"] == "HOLD" and hold["passed"] is False
            and hold["author_method_SHA256"] == WRAPPER_V1_AUTHORS
            and hold["READY_and_output_absent"] is True
            and hold["metadata_only_hold"] is True
            and hold["scientific_or_diagnostic_failure_claimed"] is False
            and hold["target_imports_or_evaluation"] is False
            and [item["id"] for item in hold["blockers"]]
            == ["ORIGINAL_AXIS_OWNER_SCOPE", "HELD_CLAMP_CLAIM_SCOPE"],
            "V1 remains an unexecuted metadata HOLD, never a promoted science failure")
    require(supplement["schema"] == "f44-q32-preparation-wrapper-independent-scientific-static-supplement-v1"
            and supplement["passed"] is True
            and supplement["metadata_hold_still_authoritative"] is True
            and supplement["execution_or_READY_authorized"] is False
            and supplement["author_method_SHA256"] == WRAPPER_V1_AUTHORS
            and supplement["hold_SHA256"] == WRAPPER_V1_METADATA[WRAPPER_V1_HOLD_KEY]
            and supplement["remaining_lifecycle_blockers_only"] == hold["blockers"]
            and supplement["no_target_import_scientific_evaluation_array_H_phase_controls_resource_or_probe"] is True,
            "Conditional static scientific supplement preserves both metadata blockers")
    axis_code_caches(
        [RESEARCH / "experiment_f44_q32_preparation_compact40_wrapper_v1.py",
         RESEARCH / "f44_q32_preparation_compact40_wrapper_source_v1.py"],
        ready["wrapper_V1_existing_code_cache_SHA256"],
        ready["wrapper_V1_absent_code_cache_paths"],
    )
    for key in (WRAPPER_V1_READY_KEY, WRAPPER_V1_OUTPUT_KEY):
        path = ROOT / key
        require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                "Original unexecuted wrapper V1 READY and output stay physically absent")
        _ABSENT_RUNTIME.add(path)
    budget()

# New resource-only functions. This file is an editable authoring draft, not SCI authority.

class F44ResourceRecurrenceReject(ValueError):
    """Only fixed metadata-validator rejections, never budget or I/O failure."""


def flags():
    return {
        "resource_recurrence_parity_only": True,
        "resource_recurrence_execution_authorized": False,
        "new_scientific_evaluation": True,
        "gate_emission_authorized": False,
        "financial_gate_emission_authorized": False,
        "source_or_gate_emission_authorized": False,
        "native_array_generation_or_gate_replay_authorized": False,
        "fixed_internal_resource_toy_records_under_ROOT_SCI_only": True,
        "historical_helper_execution_authorized": False,
        "inner_QROM_reemission_authorized": False,
        "saved_shared_QROM_preparation_template_execution_authorized": False,
        "caller_typed_native_component_execution_authorized": False,
        "preparation_wrapper_execution_authorized": False,
        "actual_coherent32_preparation_array_audited": False,
        "whole_financial_source_emitted": False,
        "completed_composition_result": False,
        "source_substitution_authorized": False,
        "financial_adoption": False, "full_G2": False, "adoption": False,
        "cost_transfer": False, "quantum_advantage": False,
        "fixture_credit": 0, "new_test_credit": 0,
        "new_credited_gate_replays": 0, "new_price_samples": 0,
        "generic_StageC_resource_gate_passed": False,
        "generic_StageC_row_status": "REJECTED", "local_only": True,
    }


def validate_clock_contract(layout):
    expected = {
        name: {"T_clock_ID": name + "_T", "full_clock_ID": name + "_FULL",
               "storage": "full_q_separate_lists", "reset": reset}
        for name, reset in (("D", "at_E"), ("P", "never"),
                            ("S", "every_original_interval_including_empty"))
    }
    if layout != expected:
        raise F44ResourceRecurrenceReject("RESOURCE_CLOCK_NAMESPACES_SEPARATE")
    ids = [item[key] for item in layout.values() for key in ("T_clock_ID", "full_clock_ID")]
    if len(ids) != 6 or len(set(ids)) != 6:
        raise F44ResourceRecurrenceReject("RESOURCE_CLOCK_NAMESPACES_SEPARATE")
    return True


def validate_success_candidate(candidate):
    known = _PLAN["current_dynamic_READY_role_graph"]["admit_fixed_resource_oracle"]["fixed_whitelist"]
    valid = (candidate.get("name") in known
             and candidate.get("manifest_expected_SHA256") == known.get(candidate.get("name"))
             and candidate.get("completed") is True and candidate.get("passed") is True
             and candidate.get("budget_censored") is False
             and candidate.get("manifest_self_hash_excluded") is True
             and candidate.get("failure_marker") is None
             and candidate.get("complete_original_maps_inventory_admitted") is True)
    if not valid:
        raise F44ResourceRecurrenceReject("SUCCESS_SEALED_RESOURCE_ORACLE_REQUIRED")
    return True


def validate_dirty_interval_plan(plan):
    for wanted in plan["required"]:
        matching = [item for item in plan["actual"]
                    if item.get("direction") == wanted["direction"]
                    and item.get("op") == wanted["op"]]
        if len(matching) != 1 or matching[0]["rows"] != wanted["rows"]:
            raise F44ResourceRecurrenceReject("COMPLETE_DIRTY_OUTPUT72_INTERVAL_REQUIRED")
        if wanted["rows"][1] - wanted["rows"][0] != 72:
            raise F44ResourceRecurrenceReject("COMPLETE_DIRTY_OUTPUT72_INTERVAL_REQUIRED")
    if plan["original_paid_output_inventory"] != {"source_gates": 72, "cx": 72, "x": 0, "ccx": 0}:
        raise F44ResourceRecurrenceReject("COMPLETE_DIRTY_OUTPUT72_INTERVAL_REQUIRED")
    return True


def original_intervals(descriptor, paid_descriptor=None, mode="wrapper"):
    """Pure metadata validation; list membership is direction authority, including empty E."""
    N, q = descriptor["gate_rows"], descriptor["qubits"]
    require(type(N) is int and 0 <= N <= 2000000 and type(q) is int and 0 < q <= 16384,
            "Exact bounded immutable resource metadata")
    if mode == "wrapper":
        E = descriptor["arithmetic_forward_rows"][1]
        require(descriptor["arithmetic_forward_rows"] == [0, E]
                and descriptor["actual_arithmetic_inverse_rows"] == [E, N] and N == 2 * E,
                "Saved complete prepared A/literal-inverse boundary")
        H = tuple(descriptor["n32"])
        require(all(type(w) is int and 0 <= w < q for w in H), "Exact original H wires")
        forward = [dict(descriptor["events"][0]), dict(descriptor["events"][1])]
        required = []
        for wrapper in descriptor["wrappers"]:
            branch = wrapper["branch"]
            require(wrapper["complete_paid_component_rows"][1] - wrapper["complete_paid_component_rows"][0]
                    == paid_descriptor["gate_rows"]
                    and wrapper["copy_rows"][1] - wrapper["copy_rows"][0] == 40
                    and wrapper["uncopy_rows"][1] - wrapper["uncopy_rows"][0] == 40,
                    "Each original wrapper pays its own complete paid component and COPY40/UNCOPY40 ABI")
            forward.append({"op": "COPY40_" + branch, "rows": wrapper["copy_rows"]})
            offset = wrapper["complete_paid_component_rows"][0]
            old_end = paid_descriptor["forward_rows"][1]
            old_reverse = paid_descriptor["literal_global_inverse_rows"][0]
            for saved in paid_descriptor["trace"]:
                forward.append({"op": branch + ":" + saved["op"],
                                "rows": [offset + x for x in saved["rows"]]})
            dirty = {"op": branch + ":DIRTY_XOR72", "rows": [offset + old_end, offset + old_reverse]}
            forward.append(dirty)
            required.append({**dirty, "direction": "forward"})
            for saved in reversed(paid_descriptor["trace"]):
                begin, finish = saved["rows"]
                forward.append({"op": branch + ":inverse:" + saved["op"],
                                "rows": [offset + old_reverse + old_end - finish,
                                         offset + old_reverse + old_end - begin]})
            forward.append({"op": "UNCOPY40_" + branch, "rows": wrapper["uncopy_rows"]})
        inverse = [{"op": "whole-inverse:" + item["op"],
                    "rows": [N - item["rows"][1], N - item["rows"][0]]}
                   for item in reversed(forward)]
        output = None
    elif mode == "component":
        E, H = N, ()
        end = descriptor["forward_rows"][1]
        reverse = descriptor["literal_global_inverse_rows"][0]
        require(descriptor["forward_rows"] == [0, end]
                and descriptor["literal_global_inverse_rows"] == [reverse, N] and N == reverse + end,
                "Saved component complete forward/copy/private-inverse native ABI")
        forward = [{"op": event["op"], "rows": list(event["rows"])} for event in descriptor["trace"]]
        output = {"op": "output_XOR_actual_event", "rows": [end, reverse]}
        inverse = [{"op": event["op"], "rows": [reverse + end - event["rows"][1],
                                                  reverse + end - event["rows"][0]]}
                   for event in reversed(descriptor["trace"])]
        required = [{**output, "direction": "component"}]
    else:
        raise ValueError("Exact frozen resource mode required")
    cursor = 0
    sequence = forward + ([output] if output else []) + (inverse if mode == "component" else [])
    for item in sequence:
        begin, end = item["rows"]
        require(type(begin) is int and type(end) is int and begin == cursor <= end <= E,
                "Original complete serial cover without dropped empty events")
        cursor = end
    require(cursor == E, "All exact forward/component rows covered")
    if mode == "wrapper":
        cursor = E
        for item in inverse:
            require(item["rows"][0] == cursor <= item["rows"][1] <= N,
                    "Original mirrored inverse serial cover")
            cursor = item["rows"][1]
        require(cursor == N, "Complete exact prepared inverse cover")
    serial = []
    if mode == "wrapper":
        for direction, entries in (("forward", forward), ("inverse", inverse)):
            for index, item in enumerate(entries):
                serial.append({**item, "direction": direction, "ordinal": index})
    else:
        for index, item in enumerate(sequence):
            serial.append({**item, "direction": "component", "ordinal": index})
    dirty_plan = {"required": required, "actual": serial,
                  "original_paid_output_inventory": {"source_gates": 72, "cx": 72, "x": 0, "ccx": 0}}
    validate_dirty_interval_plan(dirty_plan)
    return {"mode": mode, "N": N, "E": E, "q": q, "H": H, "forward": forward,
            "inverse": inverse, "output": output, "serial": serial, "dirty_plan": dirty_plan}


def profile_state(label, q, begin, end, before=(), after=(), family="prep"):
    budget()
    require(0 <= begin <= end <= 2000000 and 0 < q <= 16384, "Bounded new full-q profile")
    return {"label": label, "family": family, "begin": begin, "end": end,
            "before": tuple(before), "after": tuple(after), "t": [0] * q, "full": [0] * q,
            "counts": [0, 0, 0], "H": 0, "old_checkpoints": [], "new_fences": []}


def profile_checkpoint(state, kind, payload=None, new=False):
    budget()
    label = [kind, payload]
    state["new_fences" if new else "old_checkpoints"].append(label)


def profile_event(state, op, wires):
    """Fixed unary/CX paid event; native CCX uses its separately proved transition."""
    clocks, full = state["t"], state["full"]
    if op == "CX":
        u, v = wires
        next_t = max(clocks[u], clocks[v])
        next_full = max(full[u], full[v]) + 1
        clocks[u] = clocks[v] = next_t
        full[u] = full[v] = next_full
    else:
        (u,) = wires
        clocks[u] += int(op in ("T", "TD"))
        full[u] += 1


def profile_H(state, wires, placement):
    for wire in wires:
        profile_checkpoint(state, placement, wire)
        profile_event(state, "H", (wire,))
        state["H"] += 1


def profile_result(state):
    if state["family"] == "component":
        profile_checkpoint(state, "end")
    profile_checkpoint(state, "NEW_finalization", new=True)
    X, CX, CCX = state["counts"]
    result = {"x": X, "cx": CX, "ccx": CCX, "preparation_h": state["H"],
            "native_rows": state["end"] - state["begin"],
            "source_gates": state["end"] - state["begin"] + state["H"],
            "t_count": 7 * CCX, "t_depth": max(state["t"]),
            "clifford_t_depth": max(state["full"]), "clifford_cx": CX + 6 * CCX,
            "clifford_h": state["H"] + 2 * CCX, "native_interval": [state["begin"], state["end"]]}
    del state["t"], state["full"]
    return result


def prep_renderer(q, directions, pair, serial_forward, serial_inverse):
    def sums(events):
        keys = ("x", "cx", "ccx", "preparation_h", "native_rows", "source_gates", "t_count",
                "t_depth", "clifford_t_depth", "clifford_cx", "clifford_h")
        return {key: sum(item[key] for item in events) for key in keys}
    forward_sums, inverse_sums = sums(serial_forward), sums(serial_inverse)
    count_keys = ("x", "cx", "ccx", "preparation_h", "native_rows", "source_gates", "t_count",
                  "clifford_cx", "clifford_h")
    require(all(forward_sums[k] == directions[0][k] and inverse_sums[k] == directions[1][k]
                for k in count_keys), "Complete ASAP/serial row and H count parity")
    return {"schema": "f44-whole-template-A-and-inverse-actual-resource-ledger-v1", "qubits": q,
            "actual_whole_A_ASAP": directions[0], "actual_whole_A_inverse_ASAP": directions[1],
            "actual_whole_A_then_inverse_ASAP": pair,
            "matched_serial_event_chronology": {"forward": serial_forward, "inverse": serial_inverse,
                "forward_sums": forward_sums, "inverse_sums": inverse_sums},
            "all_preparation_copy_encoder_component_private_inverse_work_charged": True,
            "original_whole_source_capped_schedule_evaluated": False,
            "historical144CX_outer_obligation_discounted": False,
            "whole_source_cost_or_savings_forecast": None, "classical_comparison_or_advantage": None}


def component_interval(result):
    return {"rows": result["native_interval"], **{key: result[key] for key in
            ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")}}


def component_renderer(q, whole, serial, plan):
    result = {key: value for key, value in component_interval(whole).items() if key != "rows"}
    result.update(qubits=q, clifford_cx=result["cx"] + 6 * result["ccx"], clifford_h=2 * result["ccx"],
        schedule="all-to-all ASAP full actual chronological exact7T expansion",
        entire_clean_prototype_not_leaf_sum_estimate=True, outer_caller_copies_excluded=True)
    count = len(plan["forward"])
    forward = [{"op": item["op"], **component_interval(value)} for item, value in
               zip(plan["forward"], serial[:count], strict=True)]
    output = component_interval(serial[count])
    inverse = [{"op": item["op"], **component_interval(value)} for item, value in
               zip(plan["inverse"], serial[count + 1:], strict=True)]
    all_events = forward + [output] + inverse
    keys = ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")
    sums = {key: sum(event[key] for event in all_events) for key in keys}
    require(all(sums[key] == result[key] for key in keys[:5]), "Exact component count inventories")
    require(output["source_gates"] == output["cx"] == 72 and output["x"] == output["ccx"] == 0,
            "Complete saved component dirty-output72 actual resources")
    result["matched_serial_event_chronology"] = {
        "forward_actual_events": forward, "output_XOR_actual_event": output,
        "inverse_actual_events": inverse, "sums": sums,
        "schedule": "serialize complete helper/leaf events; exact actual7T ASAP within each event",
        "matched_serial_whole_source_comparison_only": True,
        "distinct_from_standalone_ASAP_depth": True, "outer_caller_argument_copies_excluded": True}
    return result


def toy_plan(index):
    """Fixed preparation diagnostics; no component ABI or dirty72 obligation applies."""
    saved = _PLAN["fixed_toy_serial_interval_metadata_no_gate_generation"][index]
    serial = [{**item, "ordinal": ordinal} for direction in ("forward", "inverse")
              for ordinal, item in enumerate(saved[direction])]
    return {"mode": "toy", "q": 4, "H": (0, 1), "E": saved["E"], "N": saved["N"],
            "forward": saved["forward"], "inverse": saved["inverse"], "serial": serial,
            "toy": saved["toy"]}


def fixed_toy_words(index):
    require(_SCIENCE_ADMITTED, "Fixed diagnostic words only inside sole ROOT SCI")
    row_triplet = ((1, 0, 0, 0), (2, 0, 1, 0), (3, 0, 1, 2))
    forward = row_triplet if index == 0 else row_triplet * 43 if index == 1 else ()
    require(index in (0, 1, 2), "Only three fixed resource diagnostics")
    return tuple(value for row in forward + tuple(reversed(forward)) for value in row)


def start_profile(label, plan, begin, end, before=(), after=(), family="prep"):
    state = profile_state(label, plan["q"], begin, end, before, after, family)
    profile_checkpoint(state, "entry")
    profile_H(state, before, "before_H")
    return state


def finish_profile(state, records):
    profile_H(state, state["after"], "after_H")
    result = profile_result(state)
    records[state["label"]] = {"resource": result, "old_checkpoints": state["old_checkpoints"],
                               "new_fences": state["new_fences"]}
    return result


def fused_resources(words, plan, decoder):
    """One exact decoder call and three equivalent transitions per row; independent full-q clocks."""
    require(_SCIENCE_ADMITTED, "Recurrence only after complete sole ROOT admission")
    validate_fixed_macro_and_decoder(decoder)
    N, E, q, H = plan["N"], plan["E"], plan["q"], plan["H"]
    require(len(words) % 4 == 0 and len(words) // 4 == N and 0 <= E <= N <= 2000000,
            "Exact fixed complete word and boundary inventory")
    family = "component" if plan["mode"] == "component" else "prep"
    records, directions, serial_results = {}, [], []
    D = start_profile("D_forward", plan, 0, E, before=H, family=family)
    P = start_profile("P_pair", plan, 0, N, before=H, after=tuple(reversed(H)), family=family)
    serial_forward, serial_inverse = [], []
    if family == "prep":
        state = start_profile("S_H_before", plan, 0, 0, before=H)
        serial_forward.append({"op": "H32", **finish_profile(state, records)})
    decoded, equivalent_paid_events, native_transition_calls, cursor = 0, 0, 0, 0
    groups = (("component", plan["serial"]),) if family == "component" else (
        ("forward", [item for item in plan["serial"] if item["direction"] == "forward"]),
        ("inverse", [item for item in plan["serial"] if item["direction"] == "inverse"]))
    for group_index, (direction, items) in enumerate(groups):
        if group_index:
            require(cursor == E, "D reset after every forward-list event, including E empties")
            profile_checkpoint(D, "NEW_half_boundary", new=True)
            directions.append(finish_profile(D, records))
            D = start_profile("D_inverse", plan, E, N, after=tuple(reversed(H)))
        for item in items:
            begin, end = item["rows"]
            require(begin == cursor <= end <= (N if direction != "forward" else E),
                    "Every original list member retains ordered empty/native cover")
            label = "S_" + direction + "_" + str(item["ordinal"])
            S = start_profile(label, plan, begin, end, family=family)
            require(len({id(state[key]) for state in (D, P, S) for key in ("t", "full")}) == 6
                    and all(len(state[key]) == q for state in (D, P, S) for key in ("t", "full")),
                    "Actual six distinct full-q clocks including unused zero wires")
            D_t, D_full = D["t"], D["full"]
            P_t, P_full = P["t"], P["full"]
            S_t, S_full = S["t"], S["full"]
            for index in range(begin, end):
                for state in (D, P, S):
                    if (index - state["begin"]) % 128 == 0:
                        profile_checkpoint(state, "local128", index - state["begin"])
                opcode, operands = decoder(words, index, q)
                decoded += 1
                for state in (D, P, S):
                    state["counts"][opcode - 1] += 1
                equivalent_paid_events += 15 if opcode == 3 else 1
                native_clock_transition(D_t, D_full, opcode, operands)
                native_clock_transition(P_t, P_full, opcode, operands)
                native_clock_transition(S_t, S_full, opcode, operands)
                native_transition_calls += 3
                cursor = index + 1
            profile_checkpoint(S, "NEW_serial_boundary", new=True)
            value = finish_profile(S, records)
            serial_results.append(value)
            if family == "prep":
                (serial_forward if direction == "forward" else serial_inverse).append({"op": item["op"], **value})
            cursor = end
    require(cursor == N and decoded == N, "Each admitted native row decoded once and transitioned independently in D/P/S")
    directions.append(finish_profile(D, records))
    if family == "component":
        # This empty diagnostic is not an original c130_resources invocation or parity oracle.
        D_empty = start_profile("D_inverse_empty_diagnostic", plan, N, N, family="component")
        directions.append(finish_profile(D_empty, records))
    pair = finish_profile(P, records)
    if family == "prep":
        state = start_profile("S_H_after", plan, N, N, after=tuple(reversed(H)))
        serial_inverse.append({"op": "H32_inverse", **finish_profile(state, records)})
        rendered = prep_renderer(q, directions, pair, serial_forward, serial_inverse)
    else:
        rendered = component_renderer(q, pair, serial_results, plan)
    return {"complete_resource_dictionary": rendered, "profiles": records,
            "native_rows_decoded_once": decoded, "equivalent_paid_macro_events_accounted_once": equivalent_paid_events,
            "equivalent_native_transition_calls": native_transition_calls,
            "literal_paid_macro_event_iterations_in_fused_path": 0,
            "explicit_original_H_event_transition_calls": sum(value["resource"]["preparation_h"] for value in records.values()),
            "explicit_H_count_role": "All actual independent D/P/S and extra labelled serial H profile events; distinct from native transitions",
            "global_profile_order": "D then P then S for each shared row; list-authoritative half transition",
            "CPU_wall_and_stage_failure_order_equivalence_claimed": False}


def validate_fixed_macro_and_decoder(decoder):
    """Validate the exact positional grammar once before each complete hot traversal."""
    require(_SCIENCE_ADMITTED, "Macro grammar only after sole ROOT SCI admission")
    require(C130_CCX_MACRO == (('H', 2), ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 2),
            ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 1), ('T', 2),
            ('H', 2), ('CX', 0, 1), ('T', 0), ('TD', 1), ('CX', 0, 1)),
            "One original ordered 15-event paid CCX macro, no operand permutation")
    for event in C130_CCX_MACRO:
        require(type(event) is tuple and event[0] in ("X", "H", "T", "TD", "CX")
                and len(event) == (3 if event[0] == "CX" else 2)
                and len(set(event[1:])) == len(event) - 1
                and all(type(position) is int and 0 <= position < 3 for position in event[1:]),
                "Exact supported fixed arity and injective native operand positions")
    require(decoder.__name__ == "c130_native_row" and decoder.__code__.co_filename == REFERENCE_FILENAME
            and decoder.__globals__["C130_CCX_MACRO"] is C130_CCX_MACRO,
            "Decoder comes from the unchanged exact-five isolated namespace")


def native_clock_transition(clocks, full, opcode, operands):
    """Exact single validated native-row transition; no inner callback or paid-event loop."""
    if opcode == 3:
        u, v, w = operands
        next_t = max(clocks[u] + 3, clocks[v] + 4, clocks[w] + 4)
        g = max(full[u] + 8, full[v] + 10, full[w] + 11)
        clocks[u] = clocks[v] = clocks[w] = next_t
        full[u] = full[v] = g
        full[w] = g - 1
    elif opcode == 2:
        u, v = operands
        next_t = max(clocks[u], clocks[v])
        next_full = max(full[u], full[v]) + 1
        clocks[u] = clocks[v] = next_t
        full[u] = full[v] = next_full
    else:
        (u,) = operands
        full[u] += 1


def phase_begin(fixture, phase):
    require(_SCIENCE_ADMITTED and fixture in PHASE_FIXTURES and phase in PHASE_NAMES,
            "Only the fixed admitted outer fixture phases may observe process clocks")
    budget()
    row = {"fixture": fixture, "phase": phase, "begin_process_CPU": time.process_time(),
           "begin_process_wall": time.monotonic() - _STARTED, "end_process_CPU_or_null": None,
           "end_process_wall_or_null": None, "phase_completed": False}
    _PHASE_OBSERVATIONS.append(row)
    require(len(_PHASE_OBSERVATIONS) <= 15, "Exactly three phases for each of five fixtures, no extra replay")
    print("F44_V5_PHASE_BEGIN " + json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
    return row


def phase_finish(row):
    require(_SCIENCE_ADMITTED and row in _PHASE_OBSERVATIONS and row["phase_completed"] is False,
            "Finish one previously admitted outer phase")
    row["end_process_CPU_or_null"] = time.process_time()
    row["end_process_wall_or_null"] = time.monotonic() - _STARTED
    row["phase_completed"] = True
    print("F44_V5_PHASE_END " + json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
    budget()


def output_custody_guard():
    require(_DECIMAL_POLICY_ADMITTED is True and _OUTPUT_CREATED_BY_THIS_RUN and _OUTPUT_IDENTITY is not None
            and OUTPUT.is_dir() and not OUTPUT.is_symlink() and OUTPUT.resolve(strict=True) == OUTPUT,
            "Only this invocation's exclusive output may receive evidence or failure writes")
    info = OUTPUT.stat()
    require((info.st_dev, info.st_ino) == _OUTPUT_IDENTITY and not getattr(info, "st_reparse_tag", 0),
            "Created output directory identity remains exact")


def check_v4_failed_history():
    require(_F44_V4_HISTORY is not None, "Failed V4 custody bound before any origin/runtime admission")
    directory = ROOT / _F44_V4_HISTORY["failed_output_path"]
    require(inventory(directory) == set(_FAILED_V4_INVENTORY), "All34 opaque failed V4 members unchanged")
    total = 0
    for path, item in _FAILED_V4_INVENTORY.items():
        budget()
        require(path.stat().st_size == item["bytes"] and digest(path, fresh=True) == item["expected_SHA256"],
                "Every failed V4 byte pin repeats without scientific/oracle credit")
        total += item["bytes"]
    require(len(_FAILED_V4_INVENTORY) == _F44_V4_HISTORY["failed_output_inclusive_files"] == 34
            and total == _F44_V4_HISTORY["failed_output_inclusive_bytes"] == 57761911
            and (directory / "FAILED_UNSEALED.json").is_file(), "Exact failed inventory, bytes and marker")
    for name in _F44_V4_HISTORY["missing_completion_and_failure_records"]:
        exact_absence(key_for(directory / name))


def admit_v4_failed_history():
    global _F44_V4_HISTORY
    _F44_V4_HISTORY = read(ROOT / _ROUTE_CORRECTION["failedV4_ROOT_freeze_path"])
    require(_F44_V4_HISTORY == _MAXPLUS_METHOD["V4_failure_history"]["complete_original_ROOT_failed_custody_object"]
            and _F44_V4_HISTORY["schema"] == "root-f44-v4-wrapper-CPU-censored-failed-custody-v1"
            and _F44_V4_HISTORY["passed"] is True and _F44_V4_HISTORY["failure_custody_only"] is True
            and _F44_V4_HISTORY["READY_or_SCI_execution_authorized"] is False,
            "Exact pinned failed V4 object, never a fourteenth SUCCESS or runtime authority")
    for field in ("current_source_MD_policy_READY_expected_SHA256", "current_static_review_expected_SHA256"):
        for key, expected in _F44_V4_HISTORY[field].items():
            require(METHOD_ADMISSION_PINS[key] == expected, "Original failed V4 source/review expectations")
            bind(ROOT / key, expected)
    require(METHOD_ADMISSION_PINS[_F44_V4_HISTORY["actual_log_path"]] == _F44_V4_HISTORY["actual_log_expected_SHA256"],
            "Opaque failed V4 log is externally expected, not a science oracle")
    bind(ROOT / _F44_V4_HISTORY["actual_log_path"], _F44_V4_HISTORY["actual_log_expected_SHA256"])
    directory = ROOT / _F44_V4_HISTORY["failed_output_path"]
    for name, item in _F44_V4_HISTORY["failed_output_inclusive_inventory_expected_SHA256_bytes"].items():
        path = bind(directory / name, item["expected_SHA256"])
        require(path.parent == directory and path.stat().st_size == item["bytes"], "Exact opaque failed V4 member")
        _FAILED_V4_INVENTORY[path] = item
    check_v4_failed_history()


def reference_namespace():
    """Only five exact function definitions, in a current isolated namespace after admission."""
    require(_SCIENCE_ADMITTED, "No reference definition execution before sole ROOT SCI")
    texts = _PLAN["complete_exact_reference_function_texts"]
    source = "\n\n".join(texts[name] for name in REFERENCE_NAMES) + "\n"
    tree = ast.parse(source, filename=REFERENCE_FILENAME)
    require(len(tree.body) == 5 and all(isinstance(node, ast.FunctionDef) for node in tree.body),
            "Isolated reference namespace has exactly five definitions")
    pins = _PLAN["source_reference_literal"]["definition_AST_pins"]
    for node in tree.body:
        observed = hashlib.sha256(ast.dump(node, include_attributes=False).encode("utf-8")).hexdigest()
        require(observed == pins[node.name]["AST_SHA256"], "Unchanged original reference function AST")
    calls = {}
    for node in tree.body:
        lines = sorted(call.lineno - node.lineno for call in ast.walk(node)
                       if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "budget")
        expected = ("entry", "before_H", "local128", "after_H") if node.name == "prep_resource_interval" else (
            ("entry", "local128", "end") if node.name == "c130_schedule_interval" else (
                ("outer_entry", "outer_end") if node.name == "c130_resources" else ()))
        require(len(lines) == len(expected), "Exact original bounded budget callsite inventory")
        calls[node.name] = dict(zip(lines, expected, strict=True))
    context = {"queue": [], "next": 0, "active": None, "projections": {}, "outer": []}

    def callback():
        budget()
        caller = sys._getframe(1)
        name, line = caller.f_code.co_name, caller.f_lineno - caller.f_code.co_firstlineno
        require(caller.f_code.co_filename == REFERENCE_FILENAME and name in calls and line in calls[name],
                "Every reference budget call has the exact isolated original AST callsite")
        kind = calls[name][line]
        if kind.startswith("outer_"):
            context["outer"].append([kind, None])
            return
        if kind == "entry":
            require(context["next"] < len(context["queue"]), "Fixed reference invocation table not exceeded")
            item = context["queue"][context["next"]]
            context["next"] += 1
            require(name == item["function"]
                    and caller.f_locals["begin"] == item["begin"] and caller.f_locals["end"] == item["end"]
                    and caller.f_locals["qubits"] == item["q"]
                    and tuple(caller.f_locals.get("before_H", ())) == item["before"]
                    and tuple(caller.f_locals.get("after_H", ())) == item["after"],
                    "Original reference call agrees with complete bounded invocation metadata")
            context["active"] = item
            context["projections"][item["label"]] = []
        item = context["active"]
        require(item is not None and item["function"] == name, "Original bounded active leaf context")
        if kind == "local128":
            index = caller.f_locals["index"]
            require(type(index) is int and item["begin"] <= index < item["end"]
                    and (index - item["begin"]) % 128 == 0, "Original local128 callsite coordinates")
            payload = index - item["begin"]
        elif kind in ("before_H", "after_H"):
            payload = caller.f_locals["wire"]
            require(type(payload) is int and 0 <= payload < item["q"]
                    and payload in item["before" if kind == "before_H" else "after"],
                    "Original H callsite belongs to its exact admitted sequence")
        else:
            payload = None
        context["projections"][item["label"]].append([kind, payload])

    namespace = {"require": require, "budget": callback, "C130_CCX_MACRO": C130_CCX_MACRO,
                 "__builtins__": __builtins__}
    exec(compile(tree, REFERENCE_FILENAME, "exec", dont_inherit=True, optimize=0), namespace)
    require(set(namespace) == set(REFERENCE_NAMES) | {"require", "budget", "C130_CCX_MACRO", "__builtins__"},
            "Exact isolated current bindings; no historical module namespace")
    return namespace, context


def reference_invocations(plan):
    family = "c130_schedule_interval" if plan["mode"] == "component" else "prep_resource_interval"
    def item(label, begin, end, before=(), after=()):
        return {"function": family, "label": label, "begin": begin, "end": end,
                "q": plan["q"], "before": tuple(before), "after": tuple(after)}
    N, E, H = plan["N"], plan["E"], plan["H"]
    if plan["mode"] == "component":
        return [item("P_pair", 0, N)] + [item("S_component_" + str(event["ordinal"]), *event["rows"])
                                       for event in plan["serial"]]
    return [item("D_forward", 0, E, before=H), item("D_inverse", E, N, after=tuple(reversed(H))),
            item("P_pair", 0, N, before=H, after=tuple(reversed(H))), item("S_H_before", 0, 0, before=H)] + [
        item("S_" + event["direction"] + "_" + str(event["ordinal"]), *event["rows"])
        for event in plan["serial"]] + [item("S_H_after", N, N, after=tuple(reversed(H)))]


def reference_resources(words, plan, descriptor=None, paid_descriptor=None):
    namespace, context = reference_namespace()
    context["queue"] = reference_invocations(plan)
    if plan["mode"] == "component":
        result = namespace["c130_resources"](words, descriptor)
    elif plan["mode"] == "wrapper":
        result = namespace["prep_actual_resources"](words, descriptor, paid_descriptor)
    else:
        values = []
        for item in context["queue"]:
            value = namespace["prep_resource_interval"](words, item["q"], item["begin"], item["end"],
                before_H=item["before"], after_H=item["after"])
            values.append(value)
        first_inverse = 4 + len(plan["forward"])
        forward = [{"op": "H32", **values[3]}] + [
            {"op": event["op"], **value} for event, value in zip(plan["forward"], values[4:first_inverse], strict=True)]
        inverse = [{"op": event["op"], **value} for event, value in zip(plan["inverse"], values[first_inverse:-1], strict=True)]
        inverse.append({"op": "H32_inverse", **values[-1]})
        result = prep_renderer(plan["q"], values[:2], values[2], forward, inverse)
    require(context["next"] == len(context["queue"]), "Every exact original reference leaf call accounted")
    require(context["outer"] == ([["outer_entry", None], ["outer_end", None]] if plan["mode"] == "component" else []),
            "Original outer component resource guards retained separately")
    return {"complete_resource_dictionary": result, "projected_original_budget_calls": context["projections"],
            "outer_original_budget_calls": context["outer"], "reference_invocations": context["queue"]}


def complete_parity(words, plan, descriptor=None, paid_descriptor=None, saved_resource=None, fixture_label=None):
    require(_SCIENCE_ADMITTED and fixture_label in PHASE_FIXTURES, "One of five fixed admitted parity fixtures")
    phases = []
    phase = phase_begin(fixture_label, "original_reference")
    phases.append(phase)
    reference = reference_resources(words, plan, descriptor, paid_descriptor)
    phase_finish(phase)
    phase = phase_begin(fixture_label, "equivalent_native_transition")
    phases.append(phase)
    decoder_namespace, _ = reference_namespace()
    fused = fused_resources(words, plan, decoder_namespace["c130_native_row"])
    phase_finish(phase)
    phase = phase_begin(fixture_label, "parity_and_render_join")
    phases.append(phase)
    require(fused["complete_resource_dictionary"] == reference["complete_resource_dictionary"],
            "Exact complete original dictionary equality without normalized/depth-only comparison")
    if saved_resource is not None:
        saved_schedule = (saved_resource["same_ASAP_and_complete_serial_event_accounting"]
                          if plan["mode"] == "component" else saved_resource)
        require(reference["complete_resource_dictionary"] == saved_schedule,
                "Full resource result equals admitted original SUCCESS oracle dictionary")
        full_saved_render = ({**saved_resource, "same_ASAP_and_complete_serial_event_accounting":
                              fused["complete_resource_dictionary"]} if plan["mode"] == "component"
                             else fused["complete_resource_dictionary"])
        require(full_saved_render == saved_resource,
                "Entire saved SUCCESS ledger including immutable archival metadata equals full rendering")
    else:
        full_saved_render = None
    for label, projection in reference["projected_original_budget_calls"].items():
        require(fused["profiles"][label]["old_checkpoints"] == projection,
                "Every original per-profile entry/local128/H/end budget projection identical")
    diagnostics = [label for label in fused["profiles"] if label not in reference["projected_original_budget_calls"]]
    require(set(diagnostics) == ({"D_forward", "D_inverse_empty_diagnostic"} if plan["mode"] == "component" else set()),
            "Only component duplicate D/empty direction diagnostics excluded from original invocation claim")
    phase_finish(phase)
    return {"phase_CPU_wall_observations": phases, "passed": True, "complete_dictionary_parity": True, "saved_SUCCESS_oracle_parity": saved_resource is not None,
            "reference": reference, "fused": fused, "extra_component_diagnostic_profiles": diagnostics,
            "complete_saved_SUCCESS_ledger_rendering": full_saved_render,
            "saved_ledger_archival_permissions_are_current_authority": False,
            "guard_projection_identity": True, "guard_interleaving_time_or_failure_equivalence": False,
            "runtime_feasibility_or_speedup_claimed": False, **flags()}


def exact_absence(key):
    budget()
    path = ROOT / key
    require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
            "Exact inherited/current absent physical path without alias")
    _ABSENT_RUNTIME.add(path)


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
            "Stdlib-only resource audit; all numerical/historical scientific imports forbidden")
    require(not any(name.startswith("research.")
                    and name not in {__name__, "research.limitation_program_20261001"}
                    for name in sys.modules), "No scientific helper namespace imported")
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(not any(lexical.is_relative_to(scope) or lexical.resolve(strict=False).is_relative_to(scope)
                            for scope in _EXCLUDED_SCOPE), "Excluded base-package origin or alias")
            if not lexical.is_file():
                base_lib = Path(sys.base_prefix) / "Lib"
                require(attribute == "__cached__" and not lexical.exists() and not lexical.is_symlink()
                        and lexical.resolve(strict=False) == lexical
                        and (lexical in _ABSENT_RUNTIME or lexical.is_relative_to(base_lib)
                             and not lexical.is_relative_to(base_lib / "site-packages")),
                        "Only exactly absent declared or standard-Lib loaded caches")
                _ABSENT_RUNTIME.add(lexical)
                continue
            actual = canonical(lexical, fresh=True)
            if actual.is_relative_to(RESEARCH):
                require(actual == AUTHOR or actual in _CODE_CACHE_EXPECTED,
                        "Only current resource audit source is an executable scientific origin")
            mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
            key = key_for(actual)
            require(key in mapping, "Current author/reviews/startup expectations precede loaded-origin check")
            require(digest(actual, fresh=True, already_resolved=True) == mapping[key],
                    "Every loaded origin/cache fresh bytes equal its prior expectation")


def admit_v6_failed_history():
    global _F44_V6_HISTORY
    contract = _FIXED_BUDGET_METHOD["mandatory_failedV6_custody_guard"]
    require(METHOD_ADMISSION_PINS[contract["ROOT_freeze_path"]] == contract["ROOT_freeze_expected_SHA256"]
            and METHOD_ADMISSION_PINS[contract["independent_field_peer_path"]] == contract["independent_field_peer_expected_SHA256"],
            "Externally expected ROOT freeze and separate failure-field peer before admission")
    _F44_V6_HISTORY = read(bind(ROOT / contract["ROOT_freeze_path"], contract["ROOT_freeze_expected_SHA256"]))
    peer = read(bind(ROOT / contract["independent_field_peer_path"], contract["independent_field_peer_expected_SHA256"]))
    require(peer["passed"] is True and peer["blockers"] == []
            and peer["reviewed_ROOT_failure_freeze_path"] == contract["ROOT_freeze_path"]
            and peer["reviewed_ROOT_failure_freeze_SHA256"] == contract["ROOT_freeze_expected_SHA256"]
            and peer["SCI_or_READY_authorized"] is False
            and _F44_V6_HISTORY["schema"] == "root-f44-v6-wrapper-reference-CPU-censored-failed-custody-v1"
            and _F44_V6_HISTORY["passed"] is True and _F44_V6_HISTORY["failure_custody_only"] is True
            and _F44_V6_HISTORY["controller_authoring_authorized"] is False
            and _F44_V6_HISTORY["READY_or_SCI_execution_authorized"] is False
            and _F44_V6_HISTORY["actual_exit_code"] == 1
            and _F44_V6_HISTORY["fixture_credit"] == _F44_V6_HISTORY["new_test_credit"] == 0
            and _F44_V6_HISTORY["original_unchanged_CPU_admission_creation_wall"] == [300, 270, 900]
            and _F44_V6_HISTORY["terminal_CPU_seconds"] is _F44_V6_HISTORY["terminal_wall_seconds"] is None
            and _F44_V6_HISTORY["failed_output_path"] == contract["failed_output_path"]
            and hashlib.sha256(json.dumps(_F44_V6_HISTORY[contract["full_inventory_field"]],
                sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
            == contract["full_expected_owned_inventory_canonical_SHA256"],
            "Exact full V6 failure custody only, never source/runtime/oracle/current grant authority")
    for field in ("current_source_MD_policy_READY_expected_SHA256", "current_static_review_expected_SHA256"):
        for key, expected in _F44_V6_HISTORY[field].items():
            require(METHOD_ADMISSION_PINS[key] == expected, "Every original V6 failed source/review expected pin")
            bind(ROOT / key, expected)
    require(_F44_V6_HISTORY["actual_log_path"] == contract["actual_log_path"]
            and _F44_V6_HISTORY["actual_log_expected_SHA256"] == contract["actual_log_expected_SHA256"]
            == METHOD_ADMISSION_PINS[contract["actual_log_path"]]
            and _F44_V6_HISTORY["missing_completion_and_failure_records"] == contract["missing_completion_and_failure_records"],
            "Original opaque UTF16 log and exact missing old seals, without terminal-clock inference")
    bind(ROOT / contract["actual_log_path"], contract["actual_log_expected_SHA256"])
    directory = ROOT / contract["failed_output_path"]
    for name, item in _F44_V6_HISTORY[contract["full_inventory_field"]].items():
        path = bind(directory / name, item["expected_SHA256"])
        require(path.parent == directory and path.stat().st_size == item["bytes"] and path not in _FAILED_V6_INVENTORY,
                "Exact externally frozen opaque V6 member, no observed SHA expectation promotion")
        _FAILED_V6_INVENTORY[path] = item
    check_v6_failed_history()


def check_v6_failed_history():
    require(_F44_V6_HISTORY is not None, "Failed V6 bound before first startup/origin and both unions")
    contract = _FIXED_BUDGET_METHOD["mandatory_failedV6_custody_guard"]
    directory = ROOT / contract["failed_output_path"]
    require(inventory(directory) == set(_FAILED_V6_INVENTORY), "All34 opaque failed V6 members unchanged")
    total = 0
    for path, item in _FAILED_V6_INVENTORY.items():
        budget()
        require(path.stat().st_size == item["bytes"] and digest(path, fresh=True) == item["expected_SHA256"],
                "Every failed V6 byte pin repeats, with no completion/fixture/oracle credit")
        total += item["bytes"]
    require(len(_FAILED_V6_INVENTORY) == _F44_V6_HISTORY["failed_output_inclusive_files"] == 34
            and total == _F44_V6_HISTORY["failed_output_inclusive_bytes"] == 57825596
            and contract["inclusive_files_bytes"] == [34, 57825596], "Exact original failed V6 count/bytes")
    marker = read(directory / "FAILED_UNSEALED.json")
    require(marker == {"failed": True, "passed": False, "completed": False, "budget_censored": None,
                      "hard_budget_state_uncertified": True, "new_test_credit": 0,
                      "Stage_C_release_authorized": False, "full_G2": False, "adoption": False},
            "Full unsealed marker preserves literal null censor state and zero result credit")
    for name in _F44_V6_HISTORY["missing_completion_and_failure_records"]:
        exact_absence(key_for(directory / name))


def bootstrap(ready_sha):
    global _PLAN, _RUNTIME_CORRECTION, _ROUTE_CORRECTION, _PRIOR_ROUTE_CORRECTION, _MAXPLUS_METHOD, _DECIMAL_METHOD, _FIXED_BUDGET_METHOD, _FIXED_BUDGET_AUTHORITY
    ready = read(bind(READY, ready_sha))
    require(ready["schema"] == "root-f44-resource-recurrence-audit-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True
            and ready["resource_recurrence_execution_authorized"] is True,
            "Separate external ROOT resource-only execution grant")
    own = ready["author_method_SHA256"]
    require(type(own) is dict and set(own) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
            "Exactly three current resource authors; no historical four-author bootstrap")
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    reviews = ready["static_review_expected_SHA256"]
    require(type(reviews) is dict and len(reviews) == 3
            and set(reviews) == set(REQUIRED_CURRENT_REVIEW_PATHS),
            "Exactly current author QA, independent full peer, and ROOT full release review")
    for key, expected in reviews.items():
        review = read(bind(ROOT / key, expected))
        require(review["passed"] is True and review["blockers"] == []
                and review["author_method_SHA256"] == own
                and review["science_static_passed"] is True and review["lifecycle_static_passed"] is True,
                "All directly bound current reviews affirm exact current trio and full obligations")
    for key, expected in METHOD_ADMISSION_PINS.items():
        bind(ROOT / key, expected)
    _ROUTE_CORRECTION = read(ROOT / ROUTE_CORRECTION_PATH)
    _PRIOR_ROUTE_CORRECTION = read(ROOT / PRIOR_ROUTE_CORRECTION_PATH)
    _MAXPLUS_METHOD = read(ROOT / MAXPLUS_METHOD_PATH)
    _DECIMAL_METHOD = read(ROOT / DECIMAL_METHOD_PATH)
    original_v5_acceptance = read(ROOT / '.context/F44_Q32_RESOURCE_RECURRENCE_V5_MAX_PLUS_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json')
    _RUNTIME_CORRECTION = read(ROOT / RUNTIME_CORRECTION_PATH)
    _FIXED_BUDGET_METHOD = read(ROOT / BUDGET_METHOD_PATH)
    _FIXED_BUDGET_AUTHORITY = read(ROOT / BUDGET_AUTHORING_PATH)
    require(_FIXED_BUDGET_METHOD["passed"] is True and _FIXED_BUDGET_METHOD["blockers"] == []
            and _FIXED_BUDGET_METHOD["controller_authoring_authorized"] is False
            and _FIXED_BUDGET_METHOD["READY_or_SCI_execution_authorized"] is False
            and _FIXED_BUDGET_AUTHORITY["passed"] is True and _FIXED_BUDGET_AUTHORITY["blockers"] == []
            and _FIXED_BUDGET_AUTHORITY["science_static_passed"] is True
            and _FIXED_BUDGET_AUTHORITY["lifecycle_static_passed"] is True
            and _FIXED_BUDGET_AUTHORITY["controller_authoring_authorized"] is True
            and _FIXED_BUDGET_AUTHORITY["READY_or_SCI_execution_authorized"] is False
            and _FIXED_BUDGET_AUTHORITY["fixed_budget_METHOD_path"] == BUDGET_METHOD_PATH
            and _FIXED_BUDGET_AUTHORITY["fixed_budget_METHOD_expected_SHA256"] == BUDGET_METHOD_SHA
            and METHOD_ADMISSION_PINS[BUDGET_METHOD_PATH] == BUDGET_METHOD_SHA
            and METHOD_ADMISSION_PINS[BUDGET_AUTHORING_PATH] == BUDGET_AUTHORING_SHA
            and _FIXED_BUDGET_AUTHORITY["prospective_fixed_budget_contract"] == _FIXED_BUDGET_METHOD["prospective_fixed_budget_contract"]
            and all(METHOD_ADMISSION_PINS[key] == expected for key, expected in
                    _FIXED_BUDGET_AUTHORITY["accepted_METHOD_MD_QA_ROOT_independent_expected_SHA256"].items()),
            "Direct new V7 fixed-budget authoring authority; no historical READY or authoring grant transfers")
    routes = _FIXED_BUDGET_AUTHORITY["exact_future_routes"]
    require(_ROUTE_CORRECTION["passed"] is True and _ROUTE_CORRECTION["blockers"] == []
            and _ROUTE_CORRECTION["controller_authoring_authorized"] is True
            and _ROUTE_CORRECTION["READY_or_SCI_execution_authorized"] is False
            and [routes[key] for key in ("source", "MD", "policy")] == [key_for(AUTHOR), key_for(METHOD_DOC), key_for(PREFLIGHT)]
            and routes["current3_static_reviews"] == list(REQUIRED_CURRENT_REVIEW_PATHS)
            and routes["READY"] == key_for(READY) and routes["output"] == key_for(OUTPUT)
            and _FIXED_BUDGET_AUTHORITY["exact_manifest_inclusive41_owned_ledger"] == list(FIXED_OWNED_FILES)
            and _DECIMAL_METHOD["future_routes"] == _ROUTE_CORRECTION["exact_future_routes"]
            and _FIXED_BUDGET_METHOD["future_routes"] == routes
            and _MAXPLUS_METHOD["future_routes"] == original_v5_acceptance["exact_future_routes"]
            and _DECIMAL_METHOD["decimal_admission_state_contract"] == _ROUTE_CORRECTION["decimal_admission_state_contract"]
            and _MAXPLUS_METHOD["phase_CPU_wall_observation_contract"] == _ROUTE_CORRECTION["phase_CPU_wall_observation_contract"],
            "Explicit current V7 routes and separately retained historical V6/V5 routes; authoring never grants SCI")
    require(_RUNTIME_CORRECTION["passed"] is True and _RUNTIME_CORRECTION["blockers"] == []
            and _RUNTIME_CORRECTION["current_runtime_candidate_path_count"] == 3062
            and hashlib.sha256(json.dumps(_RUNTIME_CORRECTION["current_runtime_candidate_expected_SHA256"],
                sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
            == _ROUTE_CORRECTION["closed_original_runtime_authority"]["candidate_expected_map_canonical_JSON_SHA256"],
            "Closed3062 runtime pin map equals complete original13 declared-map projection")
    _PLAN = read(ROOT / ADMISSION_PLAN_PATH)
    policy = read(PREFLIGHT)
    require(policy["schema"] == "f44-resource-recurrence-audit-preflight-v7"
            and policy["author_SHA256"] == own[AUTHOR.name] and policy["method_SHA256"] == own[METHOD_DOC.name]
            and policy["resource_recurrence_execution_authorized"] is False,
            "Current policy records prospective permission false; ROOT separately grants true")
    historical_caps = _FIXED_BUDGET_METHOD["historical_caps_literal"]
    current_caps = dict(_PLAN["original_caps_literal"])
    current_caps["CPU_admission_creation_wall"] = [CPU, ADMISSION, WALL]
    require(_PLAN["original_caps_literal"] == historical_caps == _FIXED_BUDGET_AUTHORITY["historical_caps_literal"]
            and historical_caps["CPU_admission_creation_wall"] == [300, 270, 900]
            and current_caps == _FIXED_BUDGET_METHOD["prospective_current_caps_literal"]
            == _FIXED_BUDGET_AUTHORITY["prospective_current_caps_literal"]
            and current_caps["CPU_admission_creation_wall"] == [600, 270, 900]
            and {key: value for key, value in current_caps.items() if key != "CPU_admission_creation_wall"}
            == {key: value for key, value in historical_caps.items() if key != "CPU_admission_creation_wall"},
            "Separate historical300 and prospective600 caps; original admission270/wall900 and every other cap exact")
    fixed_budget_authority = {
        "METHOD_path": BUDGET_METHOD_PATH, "METHOD_expected_SHA256": BUDGET_METHOD_SHA,
        "ROOT_authoring_acceptance_path": BUDGET_AUTHORING_PATH,
        "ROOT_authoring_acceptance_expected_SHA256": BUDGET_AUTHORING_SHA,
        "historical_limits_CPU_admission_wall": [300, 270, 900],
        "prospective_limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
        "only_numeric_module_constant_change": {"name": "CPU", "old_literal": 300, "prospective_literal": 600},
        "no_charge_reset_or_exemption": True,
    }
    require(_FIXED_BUDGET_METHOD["prospective_fixed_budget_contract"]["only_numeric_module_constant_change"]
            == fixed_budget_authority["only_numeric_module_constant_change"]
            and _FIXED_BUDGET_METHOD["prospective_fixed_budget_contract"]["no_global_or_phase_clock_reset_no_charge_exemption_no_different_admission_wall_limit"] is True,
            "Exactly one prospective numeric constant change without reset, exemption or completion forecast")
    shared = {
        "output": key_for(OUTPUT), "runtime_invocation": ["-B", "-m", CURRENT_MODULE],
        "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], "current_resource_parity_FLAGS": flags(),
        "caps_literal": current_caps,
        "current_fixed_budget_authority": fixed_budget_authority,
        "startup_original_expected_files": STARTUP_EXPECTED,
        "startup_only_additional_runtime_cache_paths": list(STARTUP_CACHE_KEYS),
        "method_and_admission_expected_SHA256": METHOD_ADMISSION_PINS,
        "historical_authority_expected_SHA256": _PLAN["historical_authority_expected_SHA256"],
        "all13_original_owner_snapshots": _PLAN["all13_original_owner_snapshots_literal"],
        "historical_scope_owner_counts": _PLAN["historical_scope_owner_counts_literal"],
        "fixed_manifest_inclusive_owned_files": list(FIXED_OWNED_FILES),
        "V6_decimal_admission_authoring_acceptance_expected_SHA256": ROUTE_CORRECTION_SHA,
        "fixed_max_plus_METHOD_expected_SHA256": MAXPLUS_METHOD_SHA,
        "fixed_decimal_admission_METHOD_expected_SHA256": DECIMAL_METHOD_SHA,
        "decimal_admission_state_contract": _DECIMAL_METHOD["decimal_admission_state_contract"],
        "phase_CPU_wall_observation_contract": _ROUTE_CORRECTION["phase_CPU_wall_observation_contract"],
        "honest_fused_metadata_contract": _ROUTE_CORRECTION["honest_fused_metadata_contract"],
        "failed_V4_custody_expected_SHA256": _ROUTE_CORRECTION["failedV4_ROOT_freeze_expected_SHA256"],
        "fixed_original_runtime_scope": _RUNTIME_CORRECTION["fixed_runtime_scope"],
        "fixed_original_runtime_candidate_expected_SHA256": _RUNTIME_CORRECTION["current_runtime_candidate_expected_SHA256"],
        "fixed_original_cfg_authority": _RUNTIME_CORRECTION["cfg_authority_before_read_or_add"],
        "fixed_original_optional_zip_authority": _RUNTIME_CORRECTION["optional_zip_authority"],
    }
    require(all(ready[key] == policy[key] == expected for key, expected in shared.items()),
            "Exact new finite role graph, all literal original maps/scopes, caps and 41-file ledger")
    require(ready["interpreter_expected_SHA256"] == policy["interpreter_expected_SHA256"] == INTERPRETER_PINS,
            "Both ORIGINAL interpreter byte pins, no observed expectation promotion")
    for key, expected in INTERPRETER_PINS.items():
        bind(Path(key), expected)
    require(ready["current_all_optimization_present_cache_SHA256"] == policy["current_all_optimization_present_cache_SHA256"]
            == {}
            and ready["current_all_optimization_absent_cache_paths"] == policy["current_all_optimization_absent_cache_paths"]
            == _FIXED_BUDGET_AUTHORITY["current_source_all_optimization_absent_cache_paths"],
            "Exactly current three optimization variants before first loaded-origin check")
    axis_code_caches([AUTHOR], ready["current_all_optimization_present_cache_SHA256"],
                     ready["current_all_optimization_absent_cache_paths"])
    axis_code_caches([RESEARCH / "audit_f44_q32_resource_recurrence_v1.py"],
                     _PLAN["current_all3_cache_partition_prospective"]["present_expected_SHA256"],
                     _PLAN["current_all3_cache_partition_prospective"]["absent_paths"])
    archival_v2_ready = read(ROOT / ".context/F44_Q32_RESOURCE_RECURRENCE_AUDIT_ROOT_READY_run001.json")
    require(archival_v2_ready["schema"] == "root-f44-resource-recurrence-audit-READY-v1"
            and archival_v2_ready["author_method_SHA256"] == {
                name: METHOD_ADMISSION_PINS["research/limitation_program_20261001/" + name]
                for name in ("audit_f44_q32_resource_recurrence_v2.py",
                             "F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V2.md",
                             "f44_q32_resource_recurrence_audit_preflight_v2.json")}
            and archival_v2_ready["current_all_optimization_present_cache_SHA256"]
            == _PRIOR_ROUTE_CORRECTION["mandatory_historical_cache_guard_contracts_before_origin_and_both_unions"][0]["existing_expected_SHA256"]
            and archival_v2_ready["current_all_optimization_absent_cache_paths"]
            == _PRIOR_ROUTE_CORRECTION["mandatory_historical_cache_guard_contracts_before_origin_and_both_unions"][0]["exact_original_absent_path_list"],
            "Exact externally pinned old V2 READY trio and original cache partition; its grant is archival")
    axis_code_caches([RESEARCH / "audit_f44_q32_resource_recurrence_v2.py"],
                     archival_v2_ready["current_all_optimization_present_cache_SHA256"],
                     archival_v2_ready["current_all_optimization_absent_cache_paths"])
    archival_v3_policy = read(RESEARCH / "f44_q32_resource_recurrence_audit_preflight_v3.json")
    require(archival_v3_policy["schema"] == "f44-resource-recurrence-audit-preflight-v3"
            and archival_v3_policy["resource_recurrence_execution_authorized"] is False
            and archival_v3_policy["author_SHA256"]
            == METHOD_ADMISSION_PINS["research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v3.py"]
            and archival_v3_policy["method_SHA256"]
            == METHOD_ADMISSION_PINS["research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V3.md"]
            and archival_v3_policy["current_all_optimization_present_cache_SHA256"]
            == _PRIOR_ROUTE_CORRECTION["mandatory_historical_cache_guard_contracts_before_origin_and_both_unions"][1]["existing_expected_SHA256"]
            and archival_v3_policy["current_all_optimization_absent_cache_paths"]
            == _PRIOR_ROUTE_CORRECTION["mandatory_historical_cache_guard_contracts_before_origin_and_both_unions"][1]["exact_original_absent_path_list"],
            "Exact externally pinned held V3 policy and original cache partition; no V3 READY existed")
    axis_code_caches([RESEARCH / "audit_f44_q32_resource_recurrence_v3.py"],
                     archival_v3_policy["current_all_optimization_present_cache_SHA256"],
                     archival_v3_policy["current_all_optimization_absent_cache_paths"])
    old_v4_contract = _ROUTE_CORRECTION["mandatory_actual_oldV4_cache_guard"]["contract"]
    old_v4_ready = read(ROOT / old_v4_contract["record_path"])
    require(METHOD_ADMISSION_PINS[old_v4_contract["record_path"]] == old_v4_contract["record_expected_SHA256"]
            and METHOD_ADMISSION_PINS[old_v4_contract["source_path"]] == old_v4_contract["source_expected_SHA256"]
            and old_v4_ready["schema"] == old_v4_contract["record_schema"]
            and old_v4_ready["author_method_SHA256"] == {
                name: METHOD_ADMISSION_PINS["research/limitation_program_20261001/" + name]
                for name in ("audit_f44_q32_resource_recurrence_v4.py",
                             "F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V4.md",
                             "f44_q32_resource_recurrence_audit_preflight_v4.json")}
            and old_v4_ready["current_all_optimization_present_cache_SHA256"] == old_v4_contract["existing_expected_SHA256"]
            and old_v4_ready["current_all_optimization_absent_cache_paths"] == old_v4_contract["exact_original_absent_path_list"],
            "Exact old V4 READY/trio/cache object only as failed archival custody, no grant transfer")
    axis_code_caches([ROOT / old_v4_contract["source_path"]],
                     old_v4_ready["current_all_optimization_present_cache_SHA256"],
                     old_v4_ready["current_all_optimization_absent_cache_paths"])
    admit_v4_failed_history()
    held_v5_contract = _ROUTE_CORRECTION["mandatory_actual_heldV5_policy_cache_guard"]
    held_v5_policy = read(ROOT / held_v5_contract["record_path"])
    require(METHOD_ADMISSION_PINS[held_v5_contract["record_path"]] == held_v5_contract["record_expected_SHA256"]
            and METHOD_ADMISSION_PINS[held_v5_contract["source_path"]] == held_v5_contract["source_expected_SHA256"]
            and held_v5_policy["schema"] == held_v5_contract["record_schema"]
            and held_v5_policy["resource_recurrence_execution_authorized"] is False
            and held_v5_policy["author_SHA256"] == METHOD_ADMISSION_PINS["research/limitation_program_20261001/audit_f44_q32_resource_recurrence_v5.py"]
            and held_v5_policy["method_SHA256"] == METHOD_ADMISSION_PINS["research/limitation_program_20261001/F44_Q32_RESOURCE_RECURRENCE_AUDIT_PREFLIGHT_V5.md"]
            and held_v5_policy["current_all_optimization_present_cache_SHA256"] == held_v5_contract["existing_expected_SHA256"]
            and held_v5_policy["current_all_optimization_absent_cache_paths"] == held_v5_contract["exact_original_absent_path_list"],
            "Exact held V5 policy/source/MD/cache partition; no V5 READY ever existed")
    axis_code_caches([ROOT / held_v5_contract["source_path"]],
                     held_v5_policy["current_all_optimization_present_cache_SHA256"],
                     held_v5_policy["current_all_optimization_absent_cache_paths"])
    old_v6_contract = _FIXED_BUDGET_METHOD["mandatory_actual_oldV6_READY_cache_guard"]
    old_v6_ready = read(ROOT / old_v6_contract["record_path"])
    require(METHOD_ADMISSION_PINS[old_v6_contract["record_path"]] == old_v6_contract["record_expected_SHA256"]
            and METHOD_ADMISSION_PINS[old_v6_contract["source_path"]] == old_v6_contract["source_expected_SHA256"]
            and old_v6_ready["schema"] == old_v6_contract["record_schema"]
            and old_v6_ready["author_method_SHA256"] == {
                Path(key).name: expected for key, expected in old_v6_contract["source_MD_policy_expected_SHA256"].items()}
            and old_v6_ready["limits_CPU_admission_wall"] == [300, 270, 900]
            and old_v6_ready["caps_literal"] == historical_caps
            and old_v6_ready["current_all_optimization_present_cache_SHA256"] == old_v6_contract["existing_expected_SHA256"]
            and old_v6_ready["current_all_optimization_absent_cache_paths"] == old_v6_contract["exact_original_absent_path_list"],
            "Exact actual old V6 READY/trio and original ordered three caches; old grant is failed custody only")
    axis_code_caches([ROOT / old_v6_contract["source_path"]],
                     old_v6_ready["current_all_optimization_present_cache_SHA256"],
                     old_v6_ready["current_all_optimization_absent_cache_paths"])
    admit_v6_failed_history()
    bootstrap_startup_expected()
    for key, expected in _PLAN["historical_authority_expected_SHA256"].items():
        bind(ROOT / key, expected)
    return ready, policy


def admit_original_owners():
    manifests, records = {}, _PLAN["all13_original_owner_snapshots_literal"]
    require(set(records) == set(ORIGINAL_OWNER_NAMES) and len(records) == 13,
            "Exactly original thirteen owners; no current A13/V11/V14 or later receipt admission")
    for name, record in records.items():
        budget(admission=True)
        manifest_path = bind(ROOT / record["manifest_path"], record["manifest_expected_SHA256"])
        directory = manifest_path.parent
        no_failure(directory)
        manifest = read(manifest_path)
        field = record["owned_map_schema"]
        require(field in ("files", "owned_files") and (field == "owned_files") == (name == "F44_QROM64X8_comparison_run001")
                and manifest["completed"] is True and manifest["passed"] is True
                and manifest["budget_censored"] is False and manifest["manifest_self_hash_excluded"] is True,
                "Completed sealed original map schema; failure markers reject before oracle use")
        fields = (field, "frozen_inputs", "external_runtime_inputs")
        require([len(manifest[key]) for key in fields] == record["complete_counts"]
                and {key: manifest[key] for key in fields} == record["complete_original_declared_maps"],
                "ALL complete original maps compare literally, never filtered or renamed")
        members = set()
        for item in record["complete_original_physical_owned_inventory"]:
            actual = bind(ROOT / item["root_relative_path"], item["expected_SHA256"])
            require(actual.is_relative_to(directory) and actual not in members
                    and actual.stat().st_size == item["bytes"],
                    "Exact original physical owned map key/SHA/bytes without schema normalization")
            if actual == manifest_path:
                require(item["original_map_key"] == "manifest.json"
                        and item["expected_SHA256"] == record["manifest_expected_SHA256"],
                        "Original inventory manifest has external pin, never selfhash owned-map lookup")
            else:
                require(manifest[field][item["original_map_key"]] == item["expected_SHA256"],
                        "Each original nonmanifest physical member equals original owned-map expectation")
            members.add(actual)
        require(inventory(directory) == members and len(members) == record["complete_counts"][0] + 1,
                "Complete recursive owned inventory plus original manifest")
        _OWN_INVENTORIES[directory] = members
        for key, expected in manifest["frozen_inputs"].items():
            require(type(key) is str and "\\" not in key and ".." not in Path(key).parts
                    and not Path(key).is_absolute() and (ROOT / key).relative_to(ROOT).as_posix() == key,
                    "Exact original ROOT-relative input spelling")
            bind(ROOT / key, expected)
        for key, expected in manifest["external_runtime_inputs"].items():
            require(Path(key).is_absolute(), "Exact external absolute original runtime path")
            bind(Path(key), expected)
        for key, startup in STARTUP_EXPECTED.items():
            require(manifest["frozen_inputs"].get(key) == startup["SHA256"],
                    "Each original owner binds all six original startup expectations")
        manifests[name] = manifest
    return manifests


def check_failed_composition_histories():
    for version, record in _PLAN["both_failed_complete_literal_histories"].items():
        budget()
        freeze = record["original_freeze_literal"]
        directory = ROOT / freeze["route"]
        expected = _FAILED_INVENTORIES[directory]
        require(inventory(directory) == set(expected), "All failed opaque owned members unchanged")
        for path, item in expected.items():
            stat = path.stat()
            require(stat.st_size == item["bytes"] and stat.st_mtime_ns == item["st_mtime_ns"]
                    and stat.st_ctime_ns == item["st_ctime_ns"], "Original failed opaque SHA/byte/time snapshot unchanged")
        require((directory / "FAILED_UNSEALED.json").is_file()
                and len(expected) == freeze["owned_file_count"]
                and sum(path.stat().st_size for path in expected) == freeze["owned_bytes"],
                "Failed inventories are preservation history, never SUCCESS owners or resource oracles")
        for item in record["missing_completion_records"]:
            exact_absence(item["root_relative_path"])
    check_code_caches()


def admit_failed_composition_histories():
    require(set(_PLAN["both_failed_complete_literal_histories"]) == {"V1", "V2"}, "Exactly both failed composition packets")
    for version, record in _PLAN["both_failed_complete_literal_histories"].items():
        freeze = read(bind(ROOT / record["freeze_path"], record["freeze_expected_SHA256"]))
        diagnosis = read(bind(ROOT / record["diagnosis_path"], record["diagnosis_expected_SHA256"]))
        require(freeze == record["original_freeze_literal"] and diagnosis == record["original_diagnosis_literal"]
                and freeze["passed"] is True and freeze["blockers"] == [],
                "Exact immutable failed preservation and diagnosis literals, not scientific PASS")
        archived = read(bind(ROOT / freeze["ROOT_READY_path"], freeze["ROOT_READY_SHA256"]))
        require(archived == record["archival_ROOT_READY_literal"], "Entire archival READY retained in separate namespace")
        own = record["original_author_SHA256"]
        require(archived["author_method_SHA256"] == own, "Original failed four-author namespace only")
        for name, expected in own.items():
            bind(RESEARCH / name, expected)
        archived_policy = read(RESEARCH / next(name for name in own if name.endswith(".json")))
        require(archived_policy == record["archival_policy_literal"], "Entire original policy literal without permission cloning")
        members = {}
        for item in freeze["complete_recursive_owned_inventory"].values():
            actual = bind(ROOT / item["root_relative_path"], item["SHA256"])
            require(actual.is_relative_to(ROOT / freeze["route"]) and actual not in members,
                    "All failed54 owned files are opaque fixed preservation references")
            members[actual] = item
        _FAILED_INVENTORIES[ROOT / freeze["route"]] = members
        cache = record["archival_current_cache_partition"]
        axis_code_caches([RESEARCH / name for name in own if name.endswith(".py")],
                         cache["present_expected_SHA256"], cache["absent_paths"])
    # Old guards consume only their original archived READY/policy namespace.
    archived = _PLAN["both_failed_complete_literal_histories"]["V2"]
    ready, policy = archived["archival_ROOT_READY_literal"], archived["archival_policy_literal"]
    admit_prior_failure(ready, policy)
    admit_axis_preoutput_history(ready, policy)
    admit_original_clamp_V1_history(ready)
    admit_unexecuted_wrapper_V1(ready, policy)
    check_failed_composition_histories()


def admit_archived_runtime_declarations(policy):
    """Finite author-selected ORIGINAL full-map declarations; no archived execution grant consumed."""
    for record in policy["archived_runtime_declarations"]:
        archive = read(bind(ROOT / record["path"], record["expected_SHA256"]))
        require(archive == record["entire_original_literal"], "Complete original archival runtime namespace")
        sources = [RESEARCH / name for name in archive["author_method_SHA256"] if name.endswith(".py")]
        for name, expected in archive["author_method_SHA256"].items():
            bind(RESEARCH / name, expected)
        checker = axis_code_caches if record["cache_variants"] == 3 else code_caches
        checker(sources, archive["existing_new_code_cache_SHA256"], archive["absent_new_code_cache_paths"])


def complete_fresh_union():
    budget()
    loaded_origins()
    check_failed_composition_histories()
    check_v4_failed_history()
    check_v6_failed_history()
    result = fresh_union()
    check_failed_composition_histories()
    check_v4_failed_history()
    check_v6_failed_history()
    loaded_origins()
    budget()
    return {**result, "current_reviews_direct_union_members": True,
            "both_failed_full_inventories_checked_before_and_after": True,
            "failed_V4_complete34_custody_before_and_after_union": True,
            "failed_V6_complete34_custody_before_and_after_union": True}


def read_saved_native(record):
    global _HASH_WORK
    require(_SCIENCE_ADMITTED and sys.byteorder == "little", "Read only saved admitted native resources on pinned little endian")
    path = canonical(ROOT / record["root_relative_path"], fresh=True)
    before = fingerprint(path)
    require(before[2] == record["bytes"] and before[2] % 16 == 0 and before[2] // 16 <= 2000000,
            "Original saved complete Nx4 signed32 word bytes")
    words, state, total = array("i"), hashlib.sha256(), 0
    require(words.itemsize == 4, "Exact native signed32 ABI")
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            budget()
            total += len(block)
            _HASH_WORK += len(block)
            require(_HASH_WORK <= MAX_HASH_WORK, "Saved native read charged to fixed24GiB hash-work cap")
            require(total <= before[2] and len(block) % 4 == 0, "Bounded aligned complete saved words")
            state.update(block)
            words.frombytes(block)
    require(total == before[2] and fingerprint(path) == before and state.hexdigest() == record["expected_SHA256"],
            "Fresh saved native byte expectation never inferred from current observation")
    return words


def saved_fixture_metadata(name):
    literal = _PLAN["fixed_saved_success_fixture_descriptors_full_resources_and_saved_phase_literals"][name]
    fixture = literal["original_METHOD_fixture_literal"]
    manifest = read(ROOT / fixture["manifest_path"])
    no_failure(ROOT / fixture["manifest_path"].rsplit("/", 1)[0])
    candidate = {"name": name, "manifest_expected_SHA256": fixture["manifest_expected_SHA256"],
                 "completed": manifest["completed"], "passed": manifest["passed"],
                 "budget_censored": manifest["budget_censored"], "manifest_self_hash_excluded": manifest["manifest_self_hash_excluded"],
                 "failure_marker": None, "complete_original_maps_inventory_admitted": True}
    validate_success_candidate(candidate)
    descriptor = read(ROOT / fixture["descriptor"]["root_relative_path"])
    resource = read(ROOT / fixture["saved_full_resource_ledger"]["root_relative_path"])
    phase = read(ROOT / literal["phase_path"])
    require(descriptor == literal["entire_original_descriptor_literal"]
            and resource == fixture["saved_resource_literal_dictionary"]
            and phase == literal["entire_original_phase_authority_literal"],
            "Saved descriptor/resources/phase are full original SUCCESS literals")
    require(phase["exact_absolute_phase_CCX"] is True and phase["basis_columns"] == 8
            and phase["events"] == 15 and phase["T_or_Tdg_count"] == 7
            and phase["H_count"] == 2 and phase["CX_count"] == 6
            and phase["relative_or_unknown_global_phase_accepted"] is False,
            "Original complete absolute phase certificate prerequisite; no new phase execution")
    return fixture, descriptor, resource


def fixed_controls(component_plan):
    specs = _PLAN["control_validator_specs"]
    validate_clock_contract(specs["RESOURCE_CLOCK_NAMESPACES_SEPARATE"]["positive_layout_literal"])
    validate_dirty_interval_plan(component_plan["dirty_plan"])
    bad_dirty = {**component_plan["dirty_plan"], "actual": [item for item in component_plan["dirty_plan"]["actual"]
        if item["op"] != "output_XOR_actual_event"]}
    mutations = (
        ("RESOURCE_CLOCK_NAMESPACES_SEPARATE", validate_clock_contract,
         specs["RESOURCE_CLOCK_NAMESPACES_SEPARATE"]["fixed_mutated_layout_literal"]),
        ("COMPLETE_DIRTY_OUTPUT72_INTERVAL_REQUIRED", validate_dirty_interval_plan, bad_dirty),
        ("SUCCESS_SEALED_RESOURCE_ORACLE_REQUIRED", validate_success_candidate,
         specs["SUCCESS_SEALED_RESOURCE_ORACLE_REQUIRED"]["fixed_mutated_candidate"]))
    records = []
    for tag, validator, value in mutations:
        budget()
        try:
            validator(value)
        except F44ResourceRecurrenceReject as error:
            require(type(error) is F44ResourceRecurrenceReject and str(error) == tag,
                    "Only exact dedicated structural control rejection counts")
            records.append({"tag": tag, "rejected": True, "error_type": type(error).__name__,
                            "mutation_metadata_only": True, "scientific_evaluator_called": False})
        else:
            raise ValueError("Prescribed structural control did not reject: " + tag)
    return {"passed": True, "controls": records, "count": 3, "budget_IO_or_unrelated_exception_counted": False, **flags()}


def run(ready_sha):
    global _SCIENCE_ADMITTED, _OUTPUT_CREATED_BY_THIS_RUN, _OUTPUT_IDENTITY
    require(not OUTPUT.exists() and not OUTPUT.is_symlink() and OUTPUT.resolve(strict=False) == OUTPUT,
            "Fresh fixed resource audit output; sole attempt and no fallback route")
    ready, policy = bootstrap(ready_sha)
    manifests = admit_original_owners()
    admit_failed_composition_histories()
    admit_archived_runtime_declarations(policy)
    runtime = own_runtime()
    loaded_origins()
    require(sys.version_info[:3] == (3, 12, 4) and sys.byteorder == "little"
            and array("i").itemsize == 4 and sys.flags.optimize == 0
            and "PYTHONOPTIMIZE" not in os.environ, "Original exact Python/startup representation")
    fixed_integer_policy()
    budget(admission=True)
    OUTPUT.mkdir()
    _OUTPUT_CREATED_BY_THIS_RUN = True
    output_info = OUTPUT.stat()
    _OUTPUT_IDENTITY = (output_info.st_dev, output_info.st_ino)
    output_custody_guard()
    save("run_started.json", {"schema": "f44-resource-recurrence-start-v1", "ROOT_READY_SHA256": ready_sha,
         "sole_attempt": True, "creation_clock_basis": "Win64 FILETIME process creation", **flags()})
    for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
        copy(path, "executed_" + path.name)
    for name, record in _PLAN["all13_original_owner_snapshots_literal"].items():
        copy(ROOT / record["manifest_path"], "original_manifest_" + name + ".json")
    for version, history in _PLAN["both_failed_complete_literal_histories"].items():
        copy(ROOT / history["freeze_path"], "failed_composition_" + version + "_freeze.json")
        copy(ROOT / history["diagnosis_path"], "failed_composition_" + version + "_diagnosis.json")
    save("interpreter.json", {"schema": "f44-resource-recurrence-interpreter-v1", "version": sys.version,
        "launcher": str(canonical(sys.executable)), "base_prefix": str(canonical(sys.base_prefix)),
        "interpreter_expected_SHA256": INTERPRETER_PINS, "runtime": runtime,
        "dont_write_bytecode": sys.dont_write_bytecode, "decimal_digit_limit": sys.get_int_max_str_digits()})
    save("protocol.json", {"schema": "f44-resource-recurrence-protocol-v1", "caps": policy["caps_literal"],
        "current_fixed_budget_authority": policy["current_fixed_budget_authority"],
        "historical_caps_immutable": _FIXED_BUDGET_METHOD["historical_caps_literal"],
        "fixed_41_manifest_inclusive_owned_files": policy["fixed_manifest_inclusive_owned_files"],
        "ROOT_execution_grant": ready["resource_recurrence_execution_authorized"],
        "policy_execution_grant": policy["resource_recurrence_execution_authorized"], **flags()})
    save("complete_owner_maps_and_inventories.json", {"schema": "f44-resource-original13-owners-v1",
        "all13_original_owner_snapshots": _PLAN["all13_original_owner_snapshots_literal"],
        "historical_scope_owner_counts": _PLAN["historical_scope_owner_counts_literal"],
        "all_complete_maps_literal_and_full_inventories_admitted": True, "later_owner_admission": False})
    save("history_cache_and_nonpromotion_roles.json", {"schema": "f44-resource-history-role-graph-v1",
        "both_failed_complete_literal_histories": _PLAN["both_failed_complete_literal_histories"],
        "original_V1_prospective_DYNAMIC_READY_role_graph_archival": _PLAN["current_dynamic_READY_role_graph"],
        "current_V7_ready_route_and_direct_review_paths": {"READY": key_for(READY),
            "reviews": list(REQUIRED_CURRENT_REVIEW_PATHS), "fixed_budget_authoring_SHA256": BUDGET_AUTHORING_SHA,
            "historical_V6_route_correction_SHA256": ROUTE_CORRECTION_SHA},
        "failed_V4_full_custody_object": _F44_V4_HISTORY,
        "failed_V6_full_custody_object": _F44_V6_HISTORY,
        "old_V6_original_cache_partition": _FIXED_BUDGET_METHOD["mandatory_actual_oldV6_READY_cache_guard"],
        "current_fixed_budget_authority": policy["current_fixed_budget_authority"],
        "V6_failed_partial_resource_return_is_not_an_oracle": True,
        "old_V4_original_cache_partition": _ROUTE_CORRECTION["mandatory_actual_oldV4_cache_guard"],
        "V4_failed_partial_resource_return_is_not_an_oracle": True,
        "current_review_direct_bindings": ready["static_review_expected_SHA256"],
        "archived_runtime_declarations": policy["archived_runtime_declarations"],
        "failed_partial_sources_proofs_or_resource_results_reused": False,
        "archival_permissions_current": False})
    save("fixed_resource_parity_corpus.json", {"schema": "f44-resource-fixed-corpus-v1",
        "saved_two_SUCCESS_fixtures": _PLAN["fixed_saved_success_fixture_descriptors_full_resources_and_saved_phase_literals"],
        "three_fixed_preparation_resource_toy_interval_plans": _PLAN["fixed_toy_serial_interval_metadata_no_gate_generation"],
        "toy_component72_ABI_required": False, "fixed_controls": _PLAN["control_validator_specs"],
        "extra_case_native_source_or_price_generation": False, **flags()})
    save("conditional_recurrence_induction_and_macro_authority.json", {
        "schema": "f44-resource-conditional-induction-v1", "method_admission_expected_SHA256": METHOD_ADMISSION_PINS,
        "five_original_reference_function_AST_pins": _PLAN["source_reference_literal"]["definition_AST_pins"],
        "exact_original_macro": C130_CCX_MACRO,
        "accepted_max_plus_METHOD_SHA256": MAXPLUS_METHOD_SHA,
        "symbolic_full16_trace": _MAXPLUS_METHOD["symbolic_proof"],
        "honest_fused_metadata_contract": _ROUTE_CORRECTION["honest_fused_metadata_contract"],
        "initial_clocks": "Distinct full-q zero lists; before-H belongs to the individual original profile",
        "transition": "Each exact decoded native row applies one equivalent fixed transition independently to D/P/S: CCX T=max(a+3,b+4,c+4), full=(g,g,g-1), g=max(A+8,B+10,C+11); unary/CX remain exact. Original reference alone iterates the paid15 events",
        "boundary": "Original list membership keeps every empty interval and reset; forward E empties precede the D reset, inverse E empties follow it; P never resets",
        "conditional_conclusion": "When both complete, each corresponding clock/count/whole original dictionary and projected old guard sequence agrees by induction",
        "completion_CPU_speedup_global_guard_order_or_failure_equivalence_proved": False,
        "new_phase_proof_or_financial_result": False, **flags()})
    before = complete_fresh_union()
    save("fresh_full_input_union_before_resources.json", before)
    budget(admission=True)
    _SCIENCE_ADMITTED = True
    parity_names = []
    toy_outputs = ("toy_exact_X_CX_CCX_H_empty_unused_wire_parity.json", "toy_local128_boundary_parity.json",
                   "toy_all_empty_H_only_parity.json")
    for index, name in enumerate(toy_outputs):
        plan, words = toy_plan(index), fixed_toy_words(index)
        save(name, complete_parity(words, plan, fixture_label=PHASE_FIXTURES[index]))
        parity_names.append(name)
        del words
    component_name = "A14_taylor_f44_stage_C_grid_shared_qrom_run001"
    fixture, component_descriptor, component_resource = saved_fixture_metadata(component_name)
    component_plan = original_intervals(component_descriptor, mode="component")
    words = read_saved_native(fixture["array"])
    save("saved_shared_QROM_component_full_parity.json",
         complete_parity(words, component_plan, component_descriptor, saved_resource=component_resource, fixture_label="saved_shared_QROM_component"))
    parity_names.append("saved_shared_QROM_component_full_parity.json")
    del words
    wrapper_name = "F44_q32_preparation_compact40_wrapper_run002"
    fixture, wrapper_descriptor, wrapper_resource = saved_fixture_metadata(wrapper_name)
    paid_record = _PLAN["all13_original_owner_snapshots_literal"]["A14_taylor_f44_stage_C_grid_clamp_run002"]
    paid_map = paid_record["complete_original_declared_maps"]["files"]
    paid_path = ROOT / paid_record["manifest_path"].rsplit("/", 1)[0] / "prototype_descriptor.json"
    paid_descriptor = read(bind(paid_path, paid_map["prototype_descriptor.json"]))
    wrapper_plan = original_intervals(wrapper_descriptor, paid_descriptor)
    words = read_saved_native(fixture["array"])
    save("saved_preparation_wrapper_full_parity.json",
         complete_parity(words, wrapper_plan, wrapper_descriptor, paid_descriptor, wrapper_resource, fixture_label="saved_preparation_wrapper"))
    parity_names.append("saved_preparation_wrapper_full_parity.json")
    del words
    save("three_exact_structural_controls.json", fixed_controls(component_plan))
    parity_pins = {name: digest(OUTPUT / name, fresh=True) for name in parity_names}
    save("all_projected_checkpoints_and_new_interleaving.json", {
        "schema": "f44-resource-budget-projection-aggregate-v1", "five_full_parity_record_SHA256": parity_pins,
        "full_per_profile_original_projections_retained_in_each_pinned_record": True,
        "new_D_P_S_interleaving_half_serial_finalization_fences_separately_labelled": True,
        "component_D_duplicate_and_empty_diagnostic_not_original_invocations": True,
        "global_order_time_speedup_or_CPU_failure_equivalence_claimed": False})
    after = complete_fresh_union()
    save("fresh_full_input_union_after_resources.json", after)
    save("qualification_and_remaining_gaps.json", {"schema": "f44-resource-qualification-v1",
        "result_scope": "Exact resource recurrence parity on three fixed resource toys and two ORIGINAL saved SUCCESS sources only",
        "failed_V1_V2_partial_material_reused_or_promoted": False,
        "failed_V4_partial_resource_or_CPU_return_promoted": False,
        "failed_V6_partial_resource_or_CPU_return_promoted": False,
        "fixed_max_plus_design_completion_or_speedup_forecast": None,
        "completed_new_shared_QROM_preparation_composition": False,
        "runtime_or_saved_cost_transfer_speedup_whole_price_fullG2_advantage": None,
        "remaining": ["New composition source would require a separate reviewed builder, corpus and READY",
                      "Current wall/CPU observation is not a speedup comparison or completion theorem",
                      "No full financial source, original rejected StageC reversal, fixture credit, or quantum advantage"], **flags()})
    summary = {"schema": "f44-resource-recurrence-summary-v1", "passed": True, "completed": True,
        "budget_censored": False, "two_success_fixtures": 2, "fixed_preparation_resource_toys": 3,
        "metadata_controls": 3, "full_saved_dictionary_parity": True, "profile_guard_projection_parity": True,
        "both_full_uncached_input_unions_completed": True, "CPU_seconds": time.process_time(),
        "creation_wall_seconds": time.monotonic() - _STARTED, "cost_savings_or_advantage": None, **flags()}
    save("summary.json", summary)
    save("completion_outcome.json", summary)
    expected_files = set(policy["fixed_manifest_inclusive_owned_files"])
    require(expected_files == set(FIXED_OWNED_FILES) and len(expected_files) == 41,
            "Source and policy agree with exact frozen manifest-inclusive41 emitter ledger")
    members = inventory(OUTPUT)
    require(members == {OUTPUT / name for name in expected_files if name != "manifest.json"},
            "All and only forty prescribed pre-manifest outputs")
    owned = {path.name: digest(path, fresh=True) for path in sorted(members)}
    manifest = {"schema": "f44-resource-recurrence-audit-manifest-v1", "files": owned,
        "frozen_inputs": dict(_FROZEN), "external_runtime_inputs": dict(_EXTERNAL),
        "ROOT_READY_SHA256": ready_sha, "author_method_SHA256": ready["author_method_SHA256"],
        "static_review_expected_SHA256": ready["static_review_expected_SHA256"],
        "manifest_self_hash_excluded": True, "passed": True, "completed": True, "budget_censored": False,
        "complete_original_owner_maps_counts": {name: record["complete_counts"] for name, record in
            _PLAN["all13_original_owner_snapshots_literal"].items()},
        "qualification": "Current resource audit only; all historical emission permissions archival and current execution false except sole ROOT resource grant",
        **flags()}
    complete_manifest(manifest, owned, sum(path.stat().st_size for path in members))
    budget()
    output_custody_guard()
    no_failure(OUTPUT)


def main():
    global _STARTED
    _STARTED = process_started()
    parser = argparse.ArgumentParser(description="Local fixed resource-recurrence parity audit; separate ROOT READY required")
    parser.add_argument("--root-ready-sha256", required=True)
    args = parser.parse_args()
    runtime_scopes()
    require(canonical(__file__, fresh=True) == AUTHOR
            and not OUTPUT.exists() and not OUTPUT.is_symlink() and OUTPUT.resolve(strict=False) == OUTPUT,
            "One fresh exclusively released resource route; preexisting receipt never receives failure writes")
    try:
        run(args.root_ready_sha256)
    except BaseException as error:
        if _OUTPUT_CREATED_BY_THIS_RUN:
            retain_failure(error)
        raise


if __name__ == "__main__":
    main()
