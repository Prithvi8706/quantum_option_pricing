"""Dormant E11 first-stock squared-L2 rational-only assembly.
Separate full static reviews and externally hashed ROOT READY are required.
No scientific source import, series, sampler, native array or financial transfer.
"""
from __future__ import annotations
import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import sys
import time
import traceback
import types
import _pylong

ROOT = Path("C:/Users/prith/quantum_option_pricing")
RESEARCH = ROOT / "research/limitation_program_20261001"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 4096, 512 * 1024**2
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
MAX_REDUCED_RATIONAL_BITS, MAX_ANALYTIC_TEMP_BITS = 131072, 524288
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE, _OWN_INVENTORIES = {}, {}, {}
_ABSENT_RUNTIME, _STANDARD_RUNTIME_MEMBERS = set(), set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_HASH_WORK, _REFERENCES, _STARTED, _FULL_ADMISSION = 0, 0, None, False
_OUTPUT_CREATED_BY_THIS_RUN = False
_OUTPUT_DIRECTORY_IDENTITY = None
AUTHOR = ROOT / 'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v2.py'
METHOD_DOC = ROOT / 'research/limitation_program_20261001/E11_FIRST_STOCK_SQUARED_L2_PREFLIGHT_V2.md'
PREFLIGHT = ROOT / 'research/limitation_program_20261001/e11_first_stock_squared_l2_preflight_v2.json'
READY = ROOT / '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run002.json'
OUTPUT = ROOT / 'results/limitation_program_20261001/E11_first_stock_squared_L2_run001'
AUTHOR_INPUTS = {'.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json': 'ec04e57e4f8394233f0282fce6e8941e20fd3d306e360c1b0d6602b302f9ca3a',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_STATIC_QA_run001.json': '5a150e2ed81e2e0aafae8c36318538fd462174229e70dce64f9bff09816edb31',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json': 'c6db01fd9fa72f6dbf0f6bbcb0db5a53a4f392bbc440fa18cdf8f3d592849a28',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_READY_run001.json': '6a2e5bfd72df50053c50b4611691ac3666ca4d6ae8f5a034dd947d7fcee44aae',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '72a5e7d0c9ee78305e1ef90f5097e9f8dee79b7b863fde677c5cb00582c78476',
 '.context/E11_FIRST_STOCK_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': 'e0b3eee56de49a75b508ddfa9e12c6df0f9e243468e1132a06482dcbbcd677af',
 '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_AUTHOR_STATIC_QA_run001.json': '04d1c89e10769b1967837acd93d3e7a0a600174b2074af1c3f0e90c5a2c70057',
 '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json': '20b48e9d7a6efd0efcb2b941100cf9c1fe0b0adabf5a157356d61c9611d30258',
 '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.md': '07a9bed61bc530b345bd8f3a73a0330335b31d8825cdb4ef92dc954ae91acfc4',
 '.context/E11_FIRST_STOCK_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': '88b3ceec4935baf4db5ecfb04643a9c4199e9c2974f20e1e42b51c64919762a5',
 '.context/E11_FIRST_STOCK_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': '0fae7a8f6a3c2c91654321f5040416f203424c330cbf82501efd8e7e48c508c3',
 '.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run001.json': '890395879ad2bcc7370bbcd365d57691874d240d163c3777152a17ef31aee598',
 '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json': 'fd80e86f7b05cc9ce245eef8a4359ec5f1d72b395d6e996e81283ec7d7c72dd9',
 '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': '27ff2133381c0600e70f951af50aaf6d8f2e0841dc5828916eec7a44b9362a39',
 '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_AUTHOR_METADATA_QA_run001.json': '3f65e52914e20156cc5ddf0e85607b36ce5168a93c3d5eee97400682fcddcc46',
 '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
 '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.md': 'a9f69d1990e553a4fd7804f249427b4df2540f1046778dd508c2d0e5082171bb',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_FINITE_ADMISSION_AUTHORING_ACCEPTANCE_run001.json': '230dba7471b50ec3172c44ee08e087a665d7032ecbcf6deb52d22ee39f4b1aa2',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_METHOD_REVIEW_run001.json': '00959a11c7bf00568c6af0fcb115d2ba3aef3c60aa4dc83bd56c5eba9071a7cc',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json': '3df88b2a7da02bfc406797f33a24a92e0f6d3dc1e4ea943586924bafa73d3ca2',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '00ad0ec5b6171bbeba31859898fa6a2dbeff67fa4bdb34a08f8c82aba6ed1911',
 '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_INDEPENDENT_FAILURE_FIELD_PEER_run001.json': '3cfc5a95b5b4d2a4d1dff6d50c0f214bb0cc78ef96248974a0e39600a1172802',
 '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_ROOT_FREEZE_run001.json': 'a0d5e217b4e0dfab0e6c097bb74b3333143054108bd3de89f1dd0aabf043c7ea',
 '.context/E11_FIRST_STOCK_V1_PRE_ADMISSION_LAUNCH_ROOT_CUSTODY_run001.json': '090b5733b31fe6e6c3480135d7feca7d1afaf42eeb9e05bad489599c2c0b8d96',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_CACHE_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'aea25182e67f8f108eba30b064b4c99f5440bda9df0f841c4dc58bc08498889f',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_AUTHOR_METADATA_QA_run001.json': 'e7d066531ca347962c4c4abd65eb3ddb4934185ddb8a6c2ded0784af317b4d75',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_INDEPENDENT_METHOD_PEER_run001.json': 'c6b1e4a55f0188816b31fbdda2a0c304efe4be94ecd832fe9c562c29df6d504e',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.json': '6f477c915777cd4ba42874bc39bbee4c1ff19410315a104504ac82a10bb57618',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.md': '870c1f677b36375a5dfee6cc9b86b687c3637480651cc0bf30e5d60048e49688',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_ROOT_METHOD_REVIEW_run001.json': 'f20164bc132655af205216d32863e160c62eef33022221a3f2747ec0b5439080',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.json': '74b97d5a79daff3f16f995a1d93eeb273e68e36b1c0fe286fe1746ba776e25a9',
 '.context/E11_first_stock_ROOT_saved_result_verifier_run001.py': 'cbcefc41c614619a2ab3e5380cfc2b847291961972c4df2cdaee5269efaab1fa',
 '.context/E11_first_stock_squared_L2_actual_run002.log': '8c84a83bbdecd823690e282653735c72c829213c54d90598c25f1d0f053f37f1',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a',
 'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md': 'b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637',
 'research/advantage_frontier_20260923/barrier_oracle_depth.py': '1e0e225131c668f133ef05a5de3f78fbad4fb5307a2fc8c452d99d14c8dda929',
 'research/controlled_source_completion/finance.py': '75f107e041a2b7fa7e1a6dfce471369549af96a18ae7852d212ca0e2b442f77b',
 'research/controlled_source_completion/ir.py': '3a4af54bd2e439ef060b747ea8f26a0897ce9e4a119509b57fb018d936d5d223',
 'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V3.md': 'a3de6c6ce10b1f1c7275b88defbb83ff2fc14be8857c53ec5169edbf92c18ee1',
 'research/limitation_program_20261001/E11_FIRST_STOCK_SQUARED_L2_PREFLIGHT_V1.md': 'b5d441b2ff2238e403e178c7da4e24e7c251ccb4b00deddb9efa41781992a5f9',
 'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v3.json': '730b8fa539759594248d810320566aad137ab16555ceb6a362cd9595180c0a5d',
 'research/limitation_program_20261001/e11_first_stock_squared_l2_preflight_v1.json': '5ef08878d82a1df6ad3baf6e8ff0078179fe76620cf37700584d9d96976f9e0e',
 'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v3.py': '12e2b2cdfe26c64d7abc7ecc55b5730d3dc9c86a5a84a63b2f96c3b7b2028d9b',
 'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v1.py': '099358102732798bc5e142d51ccf0136ebf20ba6b13bc8fab3846d6b2982686d',
 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_stock_exponential_envelopes.json': '6e293022c0b2682a0c2c2abe1aa672b954423831ed4503f8732fa95f01cb9b8e',
 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json': '525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a',
 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/target.json': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b',
 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/manifest.json': '165ff337315efeca8a658b1db46b172178598150f2c6b760a45bf22233f1a600',
 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c',
 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60'}
METHOD_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json'
METHOD_MD_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.md'
SUPPLEMENT_KEY = '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json'
METHOD_PEER_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json'
METHOD_ROOT_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_METHOD_REVIEW_run001.json'
OLD_LOG_READY_KEY = '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_READY_run001.json'
CURRENT_REVIEW_PATHS = ['.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run002.json', '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run002.json', '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run002.json']
AUTHOR_QA_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run002.json'
EXACT_STARTUP = {'PYTHONOPTIMIZE_and_integer_digit_override_absent_not_cleared': True,
 'Python_version': [3, 12, 4],
 'authority': 'Exact already admitted native invocation_check/runtime_scopes and literal '
              'ROOT/BASE/LAUNCHER assignments, not observed current runtime discovery.',
 'base_executable': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python.exe',
 'base_executable_SHA256': 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b',
 'base_prefix_and_no_site_prefix': 'C:/Users/prith/AppData/Local/Programs/Python/Python312',
 'declared_absent_standard_zip': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python312.zip',
 'default_decimal_digits': 4300,
 'exact_launch_flags': ['-I', '-S', '-B'],
 'launcher': 'C:/Users/prith/quantum_option_pricing/.context/frontier_t0_env/Scripts/python.exe',
 'launcher_SHA256': '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5',
 'lexical_and_physical_excluded_site_path': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/Lib/site-packages',
 'one_post_origin_decimal_serializer_limit': 20000,
 'optimization': 0,
 'ordered_exact_sys_path': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip',
                            'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\DLLs',
                            'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib',
                            'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312'],
 'workspace_cwd': 'C:/Users/prith/quantum_option_pricing'}
COMMON_EXPECTATIONS = {'ROOT_finite_planning_acceptance_SHA256': '230dba7471b50ec3172c44ee08e087a665d7032ecbcf6deb52d22ee39f4b1aa2',
 'ROOT_finite_planning_acceptance_path': '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_FINITE_ADMISSION_AUTHORING_ACCEPTANCE_run001.json',
 'accepted_method_and_review_expected_SHA256': {'.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json': 'ec04e57e4f8394233f0282fce6e8941e20fd3d306e360c1b0d6602b302f9ca3a',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_STATIC_QA_run001.json': '5a150e2ed81e2e0aafae8c36318538fd462174229e70dce64f9bff09816edb31',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json': 'c6db01fd9fa72f6dbf0f6bbcb0db5a53a4f392bbc440fa18cdf8f3d592849a28',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_READY_run001.json': '6a2e5bfd72df50053c50b4611691ac3666ca4d6ae8f5a034dd947d7fcee44aae',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '72a5e7d0c9ee78305e1ef90f5097e9f8dee79b7b863fde677c5cb00582c78476',
                                                '.context/E11_FIRST_STOCK_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': 'e0b3eee56de49a75b508ddfa9e12c6df0f9e243468e1132a06482dcbbcd677af',
                                                '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_AUTHOR_STATIC_QA_run001.json': '04d1c89e10769b1967837acd93d3e7a0a600174b2074af1c3f0e90c5a2c70057',
                                                '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json': '20b48e9d7a6efd0efcb2b941100cf9c1fe0b0adabf5a157356d61c9611d30258',
                                                '.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.md': '07a9bed61bc530b345bd8f3a73a0330335b31d8825cdb4ef92dc954ae91acfc4',
                                                '.context/E11_FIRST_STOCK_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': '88b3ceec4935baf4db5ecfb04643a9c4199e9c2974f20e1e42b51c64919762a5',
                                                '.context/E11_FIRST_STOCK_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': '0fae7a8f6a3c2c91654321f5040416f203424c330cbf82501efd8e7e48c508c3',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run001.json': '890395879ad2bcc7370bbcd365d57691874d240d163c3777152a17ef31aee598',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json': 'fd80e86f7b05cc9ce245eef8a4359ec5f1d72b395d6e996e81283ec7d7c72dd9',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': '27ff2133381c0600e70f951af50aaf6d8f2e0841dc5828916eec7a44b9362a39',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_AUTHOR_METADATA_QA_run001.json': '3f65e52914e20156cc5ddf0e85607b36ce5168a93c3d5eee97400682fcddcc46',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.md': 'a9f69d1990e553a4fd7804f249427b4df2540f1046778dd508c2d0e5082171bb',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_FINITE_ADMISSION_AUTHORING_ACCEPTANCE_run001.json': '230dba7471b50ec3172c44ee08e087a665d7032ecbcf6deb52d22ee39f4b1aa2',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_METHOD_REVIEW_run001.json': '00959a11c7bf00568c6af0fcb115d2ba3aef3c60aa4dc83bd56c5eba9071a7cc',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json': '3df88b2a7da02bfc406797f33a24a92e0f6d3dc1e4ea943586924bafa73d3ca2',
                                                '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '00ad0ec5b6171bbeba31859898fa6a2dbeff67fa4bdb34a08f8c82aba6ed1911',
                                                '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_INDEPENDENT_FAILURE_FIELD_PEER_run001.json': '3cfc5a95b5b4d2a4d1dff6d50c0f214bb0cc78ef96248974a0e39600a1172802',
                                                '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_ROOT_FREEZE_run001.json': 'a0d5e217b4e0dfab0e6c097bb74b3333143054108bd3de89f1dd0aabf043c7ea',
                                                '.context/E11_FIRST_STOCK_V1_PRE_ADMISSION_LAUNCH_ROOT_CUSTODY_run001.json': '090b5733b31fe6e6c3480135d7feca7d1afaf42eeb9e05bad489599c2c0b8d96',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_CACHE_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'aea25182e67f8f108eba30b064b4c99f5440bda9df0f841c4dc58bc08498889f',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_AUTHOR_METADATA_QA_run001.json': 'e7d066531ca347962c4c4abd65eb3ddb4934185ddb8a6c2ded0784af317b4d75',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_INDEPENDENT_METHOD_PEER_run001.json': 'c6b1e4a55f0188816b31fbdda2a0c304efe4be94ecd832fe9c562c29df6d504e',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.json': '6f477c915777cd4ba42874bc39bbee4c1ff19410315a104504ac82a10bb57618',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.md': '870c1f677b36375a5dfee6cc9b86b687c3637480651cc0bf30e5d60048e49688',
                                                '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_ROOT_METHOD_REVIEW_run001.json': 'f20164bc132655af205216d32863e160c62eef33022221a3f2747ec0b5439080',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.json': '74b97d5a79daff3f16f995a1d93eeb273e68e36b1c0fe286fe1746ba776e25a9',
                                                '.context/E11_first_stock_ROOT_saved_result_verifier_run001.py': 'cbcefc41c614619a2ab3e5380cfc2b847291961972c4df2cdaee5269efaab1fa',
                                                '.context/E11_first_stock_squared_L2_actual_run002.log': '8c84a83bbdecd823690e282653735c72c829213c54d90598c25f1d0f053f37f1',
                                                'docs/limitation_audit_20261001/implementation_plan/roadmap.json': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a',
                                                'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md': 'b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637',
                                                'research/advantage_frontier_20260923/barrier_oracle_depth.py': '1e0e225131c668f133ef05a5de3f78fbad4fb5307a2fc8c452d99d14c8dda929',
                                                'research/controlled_source_completion/finance.py': '75f107e041a2b7fa7e1a6dfce471369549af96a18ae7852d212ca0e2b442f77b',
                                                'research/controlled_source_completion/ir.py': '3a4af54bd2e439ef060b747ea8f26a0897ce9e4a119509b57fb018d936d5d223',
                                                'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V3.md': 'a3de6c6ce10b1f1c7275b88defbb83ff2fc14be8857c53ec5169edbf92c18ee1',
                                                'research/limitation_program_20261001/E11_FIRST_STOCK_SQUARED_L2_PREFLIGHT_V1.md': 'b5d441b2ff2238e403e178c7da4e24e7c251ccb4b00deddb9efa41781992a5f9',
                                                'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v3.json': '730b8fa539759594248d810320566aad137ab16555ceb6a362cd9595180c0a5d',
                                                'research/limitation_program_20261001/e11_first_stock_squared_l2_preflight_v1.json': '5ef08878d82a1df6ad3baf6e8ff0078179fe76620cf37700584d9d96976f9e0e',
                                                'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v3.py': '12e2b2cdfe26c64d7abc7ecc55b5730d3dc9c86a5a84a63b2f96c3b7b2028d9b',
                                                'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v1.py': '099358102732798bc5e142d51ccf0136ebf20ba6b13bc8fab3846d6b2982686d',
                                                'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_stock_exponential_envelopes.json': '6e293022c0b2682a0c2c2abe1aa672b954423831ed4503f8732fa95f01cb9b8e',
                                                'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json': '525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a',
                                                'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
                                                'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/target.json': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b',
                                                'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/manifest.json': '165ff337315efeca8a658b1db46b172178598150f2c6b760a45bf22233f1a600',
                                                'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c',
                                                'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60'},
 'active_and_archived_finite_role_graph': {'active10': ['A01_run011',
                                                        'A02_BM_native_financial_bridge_audit_run002',
                                                        'A02_BM_native_financial_bridge_root_verification_run001',
                                                        'A02_BM_native_financial_bridge_run002',
                                                        'A10_coefficient_run001',
                                                        'C06_pair_audit_run001',
                                                        'C06_pair_run001',
                                                        'E11_scalar_midpoint_L2_numerical_run002',
                                                        'E11_native_coordinate_squared_L2_run001',
                                                        'E11_first_log_prefix_squared_L2_run001'],
                                           'all18_snapshot_canonical_JSON_SHA256': {'A01_run011': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                                    'A01_run014': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                                    'A02_BM_native_financial_bridge_audit_run002': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                    'A02_BM_native_financial_bridge_root_verification_run001': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                    'A02_BM_native_financial_bridge_run002': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                    'A02_quantile_financial_audit_run001': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                    'A02_quantile_law_audit_run001': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                    'A10_coefficient_run001': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                    'C06_pair_audit_run001': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                                    'C06_pair_run001': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                                    'C07_barrier_audit_run001': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                    'C07_barrier_run001': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                                    'C07_barrier_run002': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                                    'C07_bound_date1_run001': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                    'E10_continuous_moment_only_run002': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                    'E11_first_log_prefix_squared_L2_run001': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                                                                    'E11_native_coordinate_squared_L2_run001': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                    'E11_scalar_midpoint_L2_numerical_run002': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c'},
                                           'all18_snapshot_dicts_not18_runtime_success_permissions': True,
                                           'all_archive_nested_runtime_maps_preserved_not_admitted_as_current_runtime': True,
                                           'archive8': ['A01_run014',
                                                        'A02_quantile_financial_audit_run001',
                                                        'A02_quantile_law_audit_run001',
                                                        'E10_continuous_moment_only_run002',
                                                        'C07_barrier_audit_run001',
                                                        'C07_barrier_run001',
                                                        'C07_barrier_run002',
                                                        'C07_bound_date1_run001'],
                                           'completed_first_log_new_owner_only_after_ROOT_verification': True,
                                           'full_snapshot_authority': {'JSON_pointer': ['complete_original_cited_owner_snapshots'],
                                                                       'expected_SHA256': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
                                                                       'path': '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json'},
                                           'original17_objects_unchanged': True,
                                           'original_raw_missing_None_and_A10_bare_keys_external_owned_layouts_unchanged': True,
                                           'owner_summaries': {'A01_run011': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                              'literal_expected_manifest_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03',
                                                                              'manifest_path': 'results/limitation_program_20261001/A01_run011/manifest.json',
                                                                              'owned_bytes': 8745921,
                                                                              'owned_files': 13,
                                                                              'role': 'inherited '
                                                                                      'active '
                                                                                      'original '
                                                                                      'proof/custody'},
                                                               'A01_run014': {'full_original_snapshot_canonical_JSON_SHA256': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                              'literal_expected_manifest_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8',
                                                                              'manifest_path': 'results/limitation_program_20261001/A01_run014/manifest.json',
                                                                              'owned_bytes': 37429139,
                                                                              'owned_files': 16,
                                                                              'role': 'unchanged '
                                                                                      'archived '
                                                                                      'opaque '
                                                                                      'custody/citation '
                                                                                      'only'},
                                                               'A02_BM_native_financial_bridge_audit_run002': {'full_original_snapshot_canonical_JSON_SHA256': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                                               'literal_expected_manifest_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0',
                                                                                                               'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/manifest.json',
                                                                                                               'owned_bytes': 44651234,
                                                                                                               'owned_files': 24,
                                                                                                               'role': 'inherited '
                                                                                                                       'active '
                                                                                                                       'original '
                                                                                                                       'proof/custody'},
                                                               'A02_BM_native_financial_bridge_root_verification_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                                                           'literal_expected_manifest_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab',
                                                                                                                           'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_root_verification_run001/manifest.json',
                                                                                                                           'owned_bytes': 579999,
                                                                                                                           'owned_files': 3,
                                                                                                                           'role': 'inherited '
                                                                                                                                   'active '
                                                                                                                                   'original '
                                                                                                                                   'proof/custody'},
                                                               'A02_BM_native_financial_bridge_run002': {'full_original_snapshot_canonical_JSON_SHA256': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                                         'literal_expected_manifest_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162',
                                                                                                         'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/manifest.json',
                                                                                                         'owned_bytes': 113209386,
                                                                                                         'owned_files': 29,
                                                                                                         'role': 'inherited '
                                                                                                                 'active '
                                                                                                                 'original '
                                                                                                                 'proof/custody'},
                                                               'A02_quantile_financial_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                                       'literal_expected_manifest_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323',
                                                                                                       'manifest_path': 'results/limitation_program_20261001/A02_quantile_financial_audit_run001/manifest.json',
                                                                                                       'owned_bytes': 1107202,
                                                                                                       'owned_files': 9,
                                                                                                       'role': 'unchanged '
                                                                                                               'archived '
                                                                                                               'opaque '
                                                                                                               'custody/citation '
                                                                                                               'only'},
                                                               'A02_quantile_law_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                                 'literal_expected_manifest_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572',
                                                                                                 'manifest_path': 'results/limitation_program_20261001/A02_quantile_law_audit_run001/manifest.json',
                                                                                                 'owned_bytes': 379157,
                                                                                                 'owned_files': 8,
                                                                                                 'role': 'unchanged '
                                                                                                         'archived '
                                                                                                         'opaque '
                                                                                                         'custody/citation '
                                                                                                         'only'},
                                                               'A10_coefficient_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                          'literal_expected_manifest_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40',
                                                                                          'manifest_path': 'results/limitation_program_20261001/A10_coefficient_run001/manifest.json',
                                                                                          'owned_bytes': 107197203,
                                                                                          'owned_files': 557,
                                                                                          'role': 'inherited '
                                                                                                  'active '
                                                                                                  'original '
                                                                                                  'proof/custody'},
                                                               'C06_pair_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                                         'literal_expected_manifest_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14',
                                                                                         'manifest_path': 'results/limitation_program_20261001/C06_pair_audit_run001/manifest.json',
                                                                                         'owned_bytes': 1109330,
                                                                                         'owned_files': 11,
                                                                                         'role': 'inherited '
                                                                                                 'active '
                                                                                                 'original '
                                                                                                 'proof/custody'},
                                                               'C06_pair_run001': {'full_original_snapshot_canonical_JSON_SHA256': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                                   'literal_expected_manifest_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a',
                                                                                   'manifest_path': 'results/limitation_program_20261001/C06_pair_run001/manifest.json',
                                                                                   'owned_bytes': 738350,
                                                                                   'owned_files': 11,
                                                                                   'role': 'inherited '
                                                                                           'active '
                                                                                           'original '
                                                                                           'proof/custody'},
                                                               'C07_barrier_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                            'literal_expected_manifest_SHA256': '29fe018792317eef189a9e6ceae00bf80c13b81fafd89ef0f4c3f48933dd98c9',
                                                                                            'manifest_path': 'results/limitation_program_20261001/C07_barrier_audit_run001/manifest.json',
                                                                                            'owned_bytes': 51656,
                                                                                            'owned_files': 11,
                                                                                            'role': 'unchanged '
                                                                                                    'archived '
                                                                                                    'opaque '
                                                                                                    'custody/citation '
                                                                                                    'only'},
                                                               'C07_barrier_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                                      'literal_expected_manifest_SHA256': 'e30e10549a76d2baa07d44429badaf8e69f85b10041478def0f673b228c3a7b9',
                                                                                      'manifest_path': 'results/limitation_program_20261001/C07_barrier_run001/manifest.json',
                                                                                      'owned_bytes': 64258,
                                                                                      'owned_files': 9,
                                                                                      'role': 'unchanged '
                                                                                              'archived '
                                                                                              'opaque '
                                                                                              'custody/citation '
                                                                                              'only'},
                                                               'C07_barrier_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                                      'literal_expected_manifest_SHA256': '3ce81f47db7fcd054d33a7391fb4600303f1f8afac545367c473172e740b6c9b',
                                                                                      'manifest_path': 'results/limitation_program_20261001/C07_barrier_run002/manifest.json',
                                                                                      'owned_bytes': 75701,
                                                                                      'owned_files': 11,
                                                                                      'role': 'unchanged '
                                                                                              'archived '
                                                                                              'opaque '
                                                                                              'custody/citation '
                                                                                              'only'},
                                                               'C07_bound_date1_run001': {'full_original_snapshot_canonical_JSON_SHA256': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                          'literal_expected_manifest_SHA256': '9f7e676d7b7eb1c14b8ae8815b756da4491b50530fbdf9722b9861712de60dd6',
                                                                                          'manifest_path': 'results/limitation_program_20261001/C07_bound_date1_run001/manifest.json',
                                                                                          'owned_bytes': 126462,
                                                                                          'owned_files': 15,
                                                                                          'role': 'unchanged '
                                                                                                  'archived '
                                                                                                  'opaque '
                                                                                                  'custody/citation '
                                                                                                  'only'},
                                                               'E10_continuous_moment_only_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                                     'literal_expected_manifest_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668',
                                                                                                     'manifest_path': 'results/limitation_program_20261001/E10_continuous_moment_only_run002/manifest.json',
                                                                                                     'owned_bytes': 7876736,
                                                                                                     'owned_files': 18,
                                                                                                     'role': 'unchanged '
                                                                                                             'archived '
                                                                                                             'opaque '
                                                                                                             'custody/citation '
                                                                                                             'only'},
                                                               'E11_first_log_prefix_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                                                                                          'literal_expected_manifest_SHA256': '165ff337315efeca8a658b1db46b172178598150f2c6b760a45bf22233f1a600',
                                                                                                          'manifest_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/manifest.json',
                                                                                                          'owned_bytes': 35880313,
                                                                                                          'owned_files': 27,
                                                                                                          'role': 'new '
                                                                                                                  'active '
                                                                                                                  'scoped '
                                                                                                                  'completed '
                                                                                                                  'first-log '
                                                                                                                  'numerical '
                                                                                                                  'input '
                                                                                                                  'only'},
                                                               'E11_native_coordinate_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                                           'literal_expected_manifest_SHA256': 'bb1f08a600712e34d1fa4b3c77f0ea04147c5368c8f92dc4f9a21ed3e293df95',
                                                                                                           'manifest_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/manifest.json',
                                                                                                           'owned_bytes': 68640627,
                                                                                                           'owned_files': 47,
                                                                                                           'role': 'inherited '
                                                                                                                   'active '
                                                                                                                   'original '
                                                                                                                   'proof/custody'},
                                                               'E11_scalar_midpoint_L2_numerical_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c',
                                                                                                           'literal_expected_manifest_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170',
                                                                                                           'manifest_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/manifest.json',
                                                                                                           'owned_bytes': 7729234,
                                                                                                           'owned_files': 20,
                                                                                                           'role': 'inherited '
                                                                                                                   'active '
                                                                                                                   'original '
                                                                                                                   'proof/custody'}},
                                           'three_original_equal_SHA_archive_aliases': [{'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6',
                                                                                         'original_key': 'research/controlled_source_completion/nonrestoring_sqrt.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/nonrestoring_sqrt.py'},
                                                                                        {'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b',
                                                                                         'original_key': 'research/journal_sprint/reversible_fixed_point.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible_fixed_point.py'},
                                                                                        {'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a',
                                                                                         'original_key': 'research/antithetic_feasibility/reversible.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}]},
 'current_authoring_acceptance_SHA256': 'aea25182e67f8f108eba30b064b4c99f5440bda9df0f841c4dc58bc08498889f',
 'current_authoring_acceptance_path': '.context/E11_FIRST_STOCK_V2_ADMISSION_CACHE_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json',
 'current_static_review_paths': ['.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run002.json',
                                 '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run002.json',
                                 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run002.json'],
 'exact_startup_literals': {'PYTHONOPTIMIZE_and_integer_digit_override_absent_not_cleared': True,
                            'Python_version': [3, 12, 4],
                            'authority': 'Exact already admitted native '
                                         'invocation_check/runtime_scopes and '
                                         'literal ROOT/BASE/LAUNCHER '
                                         'assignments, not observed current '
                                         'runtime discovery.',
                            'base_executable': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python.exe',
                            'base_executable_SHA256': 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b',
                            'base_prefix_and_no_site_prefix': 'C:/Users/prith/AppData/Local/Programs/Python/Python312',
                            'declared_absent_standard_zip': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python312.zip',
                            'default_decimal_digits': 4300,
                            'exact_launch_flags': ['-I', '-S', '-B'],
                            'launcher': 'C:/Users/prith/quantum_option_pricing/.context/frontier_t0_env/Scripts/python.exe',
                            'launcher_SHA256': '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5',
                            'lexical_and_physical_excluded_site_path': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/Lib/site-packages',
                            'one_post_origin_decimal_serializer_limit': 20000,
                            'optimization': 0,
                            'ordered_exact_sys_path': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\DLLs',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312'],
                            'workspace_cwd': 'C:/Users/prith/quantum_option_pricing'},
 'finite_protocol': {'control_categories': 4,
                     'control_evaluation_now': False,
                     'control_metadata_variants': 13,
                     'fixed_M': 256,
                     'fixed_even_Gaussian_moment_order': 32,
                     'four_positive_first_fixed_reject_control_categories': [{'category': 'exact_first_stock_source_scope',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_SOURCE_SCOPE',
                                                                              'fixed_bad_metadata_variants': [{'stock': 4022},
                                                                                                              {'raw_log': 3543},
                                                                                                              {'asset_zero_based': 1},
                                                                                                              {'contractual_date_one_based': 2}]},
                                                                             {'category': 'units_and_initial_spot_once',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_UNITS_SPOT',
                                                                              'fixed_bad_metadata_variants': [{'units': 'dimensionless_squared'},
                                                                                                              {'extra_spot_multiplier': 100},
                                                                                                              {'initial_ln100_already_in_log': False}]},
                                                                             {'category': 'fixed_unconditional_tail_proof',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_TAIL_PROOF',
                                                                              'fixed_bad_metadata_variants': [{'moment_half_order': 15},
                                                                                                              {'lower_tail_paid': False},
                                                                                                              {'upper_tail_paid': False},
                                                                                                              {'native_pair_independence_assumed': True}]},
                                                                             {'category': 'uncombined_own_profile_authority',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_PROFILE_AUTHORITY',
                                                                              'fixed_bad_metadata_variants': [{'primary90_e0_from_profile': 'independent130'},
                                                                                                              {'independent130_alpha_from_profile': 'primary90'}]}],
                     'new_exp_CDF_series_precision_passes': 0,
                     'new_moment_or_precision_or_threshold_search': False,
                     'numerical_fixture_or_new_global_test_credit': 0,
                     'profile_numerical_guards_each': ['b_le_8_times_saved_ln2_lower',
                                                       'mu_lower_minus_a_strict_positive',
                                                       'b_minus_mu_upper_minus_2v_strict_positive'],
                     'profiles': ['primary90', 'independent130'],
                     'reconciliation': 'Check existing primary rational '
                                       'identities with a distinct expanded '
                                       'order, no third stock bound returned',
                     'returned_prospective_stock_bounds': 2,
                     'source_native_projection_interval_choice': 'Exactly '
                                                                 'inherited '
                                                                 'selected raw '
                                                                 'prefix '
                                                                 'interval, no '
                                                                 'fit or '
                                                                 'adaptive '
                                                                 'cutoff',
                     'unrelated_IO_KeyError_budget_or_assertion_rejection_credit': False},
 'first_failure_stop_no_retry_or_partial_success': True,
 'first_stock_projection_Gaussian_moment_theorem': {'C16_unevaluated_exact_product_factors': [1,
                                                                                              3,
                                                                                              5,
                                                                                              7,
                                                                                              9,
                                                                                              11,
                                                                                              13,
                                                                                              15,
                                                                                              17,
                                                                                              19,
                                                                                              21,
                                                                                              23,
                                                                                              25,
                                                                                              27,
                                                                                              29,
                                                                                              31],
                                                    'Gaussian_moment_identity': 'For '
                                                                                'a '
                                                                                'centered '
                                                                                'continuous '
                                                                                'N(0,v), '
                                                                                'E '
                                                                                'W^32=(31)!!*v^16=C16*v^16, '
                                                                                'by '
                                                                                'Gaussian '
                                                                                'integration-by-parts '
                                                                                'recurrence; '
                                                                                'no '
                                                                                'moment '
                                                                                'of '
                                                                                'digital '
                                                                                'coordinates '
                                                                                'is '
                                                                                'used.',
                                                    'M_fixed': 256,
                                                    'M_guard_unevaluated': 'b '
                                                                           '<= '
                                                                           '8*own_saved_ln2_lower '
                                                                           'implies '
                                                                           'exp(b)<=2^8=M',
                                                    'Q': 1099511627776,
                                                    'continuous_exponential_tilt_identity': 'E[exp(2L)1{L>b}]=exp(2mu+2v)*P(N(mu+2v,v)>b); '
                                                                                            'complete '
                                                                                            'square '
                                                                                            'in '
                                                                                            'the '
                                                                                            'unconditional '
                                                                                            'continuous '
                                                                                            'Gaussian '
                                                                                            'density.',
                                                    'continuous_normal_law': 'Only '
                                                                             'original '
                                                                             'continuous '
                                                                             'ideal '
                                                                             'Z0,Z1 '
                                                                             'are '
                                                                             'independent '
                                                                             'standard '
                                                                             'normals. '
                                                                             'Native '
                                                                             'shared '
                                                                             'finite '
                                                                             'pair '
                                                                             'is '
                                                                             'never '
                                                                             'assumed '
                                                                             'independent. '
                                                                             'L '
                                                                             'has '
                                                                             'mean '
                                                                             'mu=ln100-1/800 '
                                                                             'and '
                                                                             'variance '
                                                                             'v=3/400.',
                                                    'core_projection_bound': 'P '
                                                                             'fixes '
                                                                             'L_N '
                                                                             'because '
                                                                             'all '
                                                                             'native '
                                                                             'L_N '
                                                                             'belong '
                                                                             'to '
                                                                             '[a,b]; '
                                                                             '|L_N-P(L)|<=|L_N-L|. '
                                                                             'On '
                                                                             '[a,b], '
                                                                             'exp '
                                                                             'is '
                                                                             'M-Lipschitz.',
                                                    'd_lower_unevaluated': 'mu_lower-a',
                                                    'd_upper_tilted_unevaluated': 'b-mu_upper-2*v',
                                                    'even_moment_order': 32,
                                                    'exact_tilt_mass': 'exp(2mu+2v)=10000*exp(1/80)<=10000*80/79, '
                                                                       'using '
                                                                       'exp(x)<=1/(1-x) '
                                                                       'for '
                                                                       '0<=x<1; '
                                                                       'analytic '
                                                                       'inequality '
                                                                       'only, '
                                                                       'no '
                                                                       'series '
                                                                       'evaluated.',
                                                    'exactly_two_own_profile_bounds': 'Evaluate '
                                                                                      'this '
                                                                                      'rational '
                                                                                      'formula '
                                                                                      'once '
                                                                                      'using '
                                                                                      'primary90 '
                                                                                      'original '
                                                                                      'inputs '
                                                                                      'and '
                                                                                      'once '
                                                                                      'using '
                                                                                      'independent130 '
                                                                                      'own '
                                                                                      'original '
                                                                                      'inputs; '
                                                                                      'do '
                                                                                      'not '
                                                                                      'select '
                                                                                      'a '
                                                                                      'minimum, '
                                                                                      'require '
                                                                                      'nesting, '
                                                                                      'mix '
                                                                                      'adapters, '
                                                                                      'or '
                                                                                      'return '
                                                                                      'a '
                                                                                      'third '
                                                                                      'candidate.',
                                                    'ideal_reference': 'L=ln100-1/800+sqrt(3/1000)Z0+sqrt(9/2000)Z1; '
                                                                       'S=exp(L)',
                                                    'interval_authority_JSON_pointer': ['cases',
                                                                                        'B4x12',
                                                                                        'prefixes',
                                                                                        0,
                                                                                        'actual_raw_log_bounds',
                                                                                        0],
                                                    'interval_authority_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                    'interval_authority_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
                                                    'lower_projection_tail_pointwise': 'On '
                                                                                       'L<a, '
                                                                                       '0<=exp(a)-exp(L)<=exp(a)<=M; '
                                                                                       'lower '
                                                                                       'squared-tail '
                                                                                       'contribution '
                                                                                       '<=M^2*P(L<a).',
                                                    'lower_tail_bound_unevaluated': 'T_lower=M^2*C16*v^16/(mu_lower-a)^32',
                                                    'moment_half_order': 16,
                                                    'mu_lower_unevaluated': '5063438167381/Q '
                                                                            '- '
                                                                            'e0 '
                                                                            '- '
                                                                            '1/800',
                                                    'mu_upper_unevaluated': '5063438167381/Q '
                                                                            '+ '
                                                                            'e0 '
                                                                            '- '
                                                                            '1/800',
                                                    'native_all_input_interval_raw': [4155861047200,
                                                                                      5968266508490],
                                                    'native_clip_inactive_for_all_inputs_at_this_site_only': True,
                                                    'native_exponential_allowance_unevaluated': 'A=alpha*M+beta '
                                                                                                'from '
                                                                                                'original '
                                                                                                'full-clipped-domain '
                                                                                                'absolute '
                                                                                                'envelope '
                                                                                                '|S_N-exp(L_N)|<=alpha*exp(L_N)+beta; '
                                                                                                'original '
                                                                                                'clip '
                                                                                                'inactive '
                                                                                                'at '
                                                                                                'site',
                                                    'native_initial_log_literal_raw': 5063438167381,
                                                    'new_numerical_moments_products_tail_allowances_bounds': None,
                                                    'new_proof_guard_values': None,
                                                    'pointwise_three_term_proof': '|S_N-exp(L)|<=A+M*|L_N-L|+|exp(P(L))-exp(L)|; '
                                                                                  'square '
                                                                                  'with '
                                                                                  'pointwise '
                                                                                  'Cauchy '
                                                                                  'for '
                                                                                  'three '
                                                                                  'terms, '
                                                                                  'then '
                                                                                  'take '
                                                                                  'expectation.',
                                                    'projection': 'P(x)=min(max(x,a),b), '
                                                                  'a=raw_lower/Q, '
                                                                  'b=raw_upper/Q; '
                                                                  'mathematical '
                                                                  'comparison '
                                                                  'only, no '
                                                                  'source/policy '
                                                                  'change',
                                                    'prospective_stock_squared_L2_formula': 'B_stock=3*((alpha*M+beta)^2+M^2*B_log+T_lower+T_upper)',
                                                    'selected_scope': {'asset_zero_based': 0,
                                                                       'case': 'B4x12',
                                                                       'clipped_log': 3579,
                                                                       'contractual_date_one_based': 1,
                                                                       'raw_log': 3542,
                                                                       'saved_date_zero_based': 0,
                                                                       'stock': 4021,
                                                                       'units': 'dollars_squared'},
                                                    'upper_projection_tail_pointwise': 'On '
                                                                                       'L>b, '
                                                                                       '0<=exp(L)-exp(b)<=exp(L); '
                                                                                       'upper '
                                                                                       'squared-tail '
                                                                                       'contribution '
                                                                                       '<=E '
                                                                                       'exp(2L)1{L>b}.',
                                                    'upper_tail_bound_unevaluated': 'T_upper=(10000*80/79)*C16*v^16/(b-mu_upper-2v)^32',
                                                    'v_exact': [3, 400]},
 'full_METHOD_JSON_copy_count': 1,
 'future_actual_stock_bounds': {'independent130': None, 'primary90': None},
 'historical_cache_partitions': {'completed_first_log_V3': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-1.pyc',
                                                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-2.pyc',
                                                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.pyc'],
                                                            'existing_expected_SHA256': {}},
                                 'completed_native_author': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc',
                                                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-2.pyc',
                                                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.pyc'],
                                                             'existing_expected_SHA256': {}},
                                 'completed_scalar_V2': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc',
                                                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc',
                                                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc'],
                                                         'existing_expected_SHA256': {}},
                                 'failed_first_stock_V1': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.opt-1.pyc',
                                                                            'research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.opt-2.pyc',
                                                                            'research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.pyc'],
                                                           'existing_expected_SHA256': {}},
                                 'failed_scalar_V1': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc',
                                                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc',
                                                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'],
                                                      'existing_expected_SHA256': {}}},
 'historical_first_log_V3_source_has_current_execution_permission': False,
 'native_reference_toy_array_count': 0,
 'original_caps': {'CPU_admission_creation_wall': [180, 150, 600],
                   'current_stdlib_runtime_files_bytes': [4096, 536870912],
                   'owned_files_bytes': [64, 134217728],
                   'references_unique_bytes_hash_work': [100000,
                                                         8589934592,
                                                         25769803776],
                   'serialized_integer_reduced_rational_analytic_temporary_bits': [65536,
                                                                                   131072,
                                                                                   524288]},
 'original_cfg_expected': {'bytes_cap': 8388608,
                           'expected_SHA256': 'aaeeb031a76b70ae1ac53b6557056f554273db4b313678c36c7ccd2c483e7e37',
                           'path': '.context/frontier_t0_env/pyvenv.cfg'},
 'output': 'results/limitation_program_20261001/E11_first_stock_squared_L2_run001',
 'planned_manifest_inclusive_owned_files': 27,
 'planned_owned_filenames': ['executed_controller.py',
                             'executed_preflight.md',
                             'executed_policy.json',
                             'executed_ROOT_READY.json',
                             'reviewed_next_stock_method.md',
                             'reviewed_next_stock_method.json',
                             'reviewed_independent_method_peer.json',
                             'reviewed_ROOT_method.json',
                             'protocol.json',
                             'run_started.json',
                             'interpreter.json',
                             'loaded_module_origins.json',
                             'active_and_archived_role_graph.json',
                             'literal_prior_stock_component_adapters.json',
                             'fresh_full_input_union_before_assembly.json',
                             'source_first_stock_witness.json',
                             'primary_first_stock_components.json',
                             'primary_first_stock_squared_L2.json',
                             'independent_first_stock_components.json',
                             'independent_first_stock_squared_L2.json',
                             'independent_primary_proof_check.json',
                             'four_fixed_reject_controls.json',
                             'qualification_and_remaining_gaps.json',
                             'fresh_full_input_union_after_assembly.json',
                             'summary.json',
                             'completion_outcome.json',
                             'manifest.json'],
 'runtime_invocation': ['C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Scripts\\python.exe',
                        '-I',
                        '-S',
                        '-B',
                        'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_first_stock_squared_l2_v2.py',
                        '--ready-sha256',
                        'EXTERNALLY_PINNED_CURRENT_V2_READY_SHA256'],
 'selected_original_log_contract': {'actual_common_literal': 60222732077,
                                    'actual_drift_signed_literal': -1374389535,
                                    'actual_idio_literal': 73757482253,
                                    'actual_initial_literal': 5063438167381,
                                    'addition_rounding_zero_requires_original_all_partial_no_wrap': True,
                                    'asset_zero_based': 0,
                                    'case': 'B4x12',
                                    'contractual_date_one_based': 1,
                                    'fraction_bits': 40,
                                    'ideal_reference_exact_literal_parameters': {'S0': [100,
                                                                                        1],
                                                                                 'T': [1,
                                                                                       1],
                                                                                 'drift': [-1,
                                                                                           800],
                                                                                 'r': [3,
                                                                                       100],
                                                                                 'rho': [2,
                                                                                         5],
                                                                                 'sigma': [3,
                                                                                           10],
                                                                                 't': [1,
                                                                                       12]},
                                    'legacy_binary64_real_parameters_equal_exact_decimal_claimed': False,
                                    'newly_evaluated_or_synthesized_target': False,
                                    'ordered_native_normal_values': [94, 125],
                                    'ordered_original_normal_indices': [0, 1],
                                    'original_prefix_witness': {'asset': 0,
                                                                'constants': [[-1374389535,
                                                                               1],
                                                                              [5063438167381,
                                                                               1]],
                                                                'date': 0,
                                                                'every_driver_multiplicity': 1,
                                                                'original_normal_indices': [0,
                                                                                            1],
                                                                'raw_log': 3542,
                                                                'stock': 4021},
                                    'original_shared_pair_scope': {'cosines': [{'address': 67,
                                                                                'floors': 7,
                                                                                'input': 6,
                                                                                'local': 71,
                                                                                'lookup_outputs': [72,
                                                                                                   73,
                                                                                                   74,
                                                                                                   75,
                                                                                                   76,
                                                                                                   77,
                                                                                                   78,
                                                                                                   79],
                                                                                'output': 93},
                                                                               {'address': 99,
                                                                                'floors': 7,
                                                                                'input': 61,
                                                                                'local': 102,
                                                                                'lookup_outputs': [103,
                                                                                                   104,
                                                                                                   105,
                                                                                                   106,
                                                                                                   107,
                                                                                                   108,
                                                                                                   109,
                                                                                                   110],
                                                                                'output': 124}],
                                                                   'log': {'address': 23,
                                                                           'floors': 8,
                                                                           'input': 15,
                                                                           'local': 27,
                                                                           'lookup_outputs': [28,
                                                                                              29,
                                                                                              30,
                                                                                              31,
                                                                                              32,
                                                                                              33,
                                                                                              34,
                                                                                              35,
                                                                                              36],
                                                                           'output': 52},
                                                                   'normal_values': [94,
                                                                                     125],
                                                                   'original_shared_pair_preserved': True,
                                                                   'radius': 58,
                                                                   'raw_uniform_values': [0,
                                                                                          1]},
                                    'raw_preclip_log_value': 3542,
                                    'saved_date_zero_based': 0,
                                    'signed_cmul_floors': 2,
                                    'source_seven_node_slice_saved_metadata': [{'args': [94],
                                                                                'op': 'cmul',
                                                                                'out': [3492],
                                                                                'params': {'c': 60222732077}},
                                                                               {'args': [125],
                                                                                'op': 'cmul',
                                                                                'out': [3493],
                                                                                'params': {'c': 73757482253}},
                                                                               {'args': [3492,
                                                                                         3493],
                                                                                'op': 'add',
                                                                                'out': [3494],
                                                                                'params': {}},
                                                                               {'args': [],
                                                                                'op': 'const',
                                                                                'out': [3495],
                                                                                'params': {'value': 4722366482868270824161}},
                                                                               {'args': [3494,
                                                                                         3495],
                                                                                'op': 'add',
                                                                                'out': [3496],
                                                                                'params': {}},
                                                                               {'args': [],
                                                                                'op': 'const',
                                                                                'out': [3541],
                                                                                'params': {'value': 5063438167381}},
                                                                               {'args': [3496,
                                                                                         3541],
                                                                                'op': 'add',
                                                                                'out': [3542],
                                                                                'params': {}}],
                                    'stock_consumer_not_claimed': 4021,
                                    'target_literal_SHA256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
                                    'target_path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json',
                                    'time_exact_literal': [1, 12],
                                    'width': 72},
 'selected_original_stock_site': {'actual_original_support_signature': '2a35ab41d964c6abc9a3a6243a93f1be141b31da20672c50cdfe0d452239311e',
                                  'clipped': 3579,
                                  'exponent': 3979,
                                  'high': 9145480617430,
                                  'inverse_ln2': 1586259972792,
                                  'ln2': 762123384786,
                                  'low': -12193974156573,
                                  'polynomial': 4020,
                                  'raw_log': 3542,
                                  'remainder': 3982,
                                  'stock': 4021,
                                  'values': [16,
                                             3978,
                                             3979,
                                             3980,
                                             3981,
                                             3982,
                                             3983,
                                             3984,
                                             3985,
                                             3986,
                                             3987,
                                             3988,
                                             3989,
                                             3990,
                                             3991,
                                             3992,
                                             3993,
                                             3994,
                                             3995,
                                             3996,
                                             3997,
                                             3998,
                                             3999,
                                             4000,
                                             4001,
                                             4002,
                                             4003,
                                             4004,
                                             4005,
                                             4006,
                                             4007,
                                             4008,
                                             4009,
                                             4010,
                                             4011,
                                             4012,
                                             4013,
                                             4014,
                                             4015,
                                             4016,
                                             4017,
                                             4018,
                                             4019,
                                             4020,
                                             4021]},
 'serializer_expected_source_and_cache_partition': {'absent_three_variant_cache_paths': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.pyc',
                                                                                         'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-1.pyc',
                                                                                         'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-2.pyc'],
                                                    'existing_cache_expected_SHA256': {},
                                                    'import_before_initial_runtime_and_loaded_origin_admission': True,
                                                    'module': '_pylong',
                                                    'postadmission_origin_or_cache_discovery_authorized': False,
                                                    'scientific_arithmetic_or_representation_policy_change': False,
                                                    'source_SHA256': 'bcae0d4cc2d4d3fd9b40bb06b512eb8dd785f755edd1f9038613d4460ca4c6c1',
                                                    'source_path': 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\_pylong.py'},
 'source_contract_canonical_JSON_SHA256': '2d0ab1412b9e04cabaf030540c5ad884236ad7e6754f5acf44fb23efbd309540',
 'stock_source_45node_closure_canonical_JSON_SHA256': 'a284d0fa82eee4c8f40e7de2cadd9f2867b122d9bf24e604c3e90e55f68edbf1',
 'two_literal_profile_adapter_contract': {'independent130': {'B_log_original_literal_pair': [2428158210523221716611869059561284163506426632206382933227882749799107497844497983493965778077859665221003848479909443502356283144309763445667792023072878245744752236936706476755951355252171098226395633180998333416396336106714275667874841716872377533973362164422306514278219297714838302666989189183695256703701608221630931547883699856199822898192517375275381325725885420659120650636522924098635555012513935156871817454254946932191744197140849579927797658793344456153044262066893575491316898749520247694131272008480484279767442621311639247906829230752566809805133006122638828228870494291445884186293021900488583473809333911893695999791478916008054562105198374155378886604081879712491148543043767842545408363141653398723997338202229669865800275898817433527911904806662136305852498339695196210493003428178533842259395795527764866221522384929346609169752763847410100021900211807612222242377686666678799320498627233759536718291110326114419560051244617985404989154265033792342989447457763132027823749179017384608895015113531159623561782481108005357554216247019645899050523,
                                                                                             1513733228466844074031275717429922960187834973955384601995536522750016224414668727819206116519306201179573042460674520346942702696629351302643155826634064290672325608545738612667826017895680334158654790028613891981326576843599902103891630952814511173327529997748425925496065487194844289996932339143900081966349579181053527389213998289763844397764192911821096266306307504423212647986687390974299915254681199374147253096002018965665012434635135952694797887226841083837066248297522135663165086552559028923067229727245617133616118090428699689301851612632033088052755892767180543198941489242025484577036517070180690342893617402169278129137856839223966607852369548571543075007653621750787446809392176100547184066983840358432973683897920428422230036262075573229148857864832716125527510362375539991393222476383567811375726121835388823028241346307366055443781189365504221014616251877476187866875683293332963037770069373358608728988510788498971777052572870846793872720761611264090303077011502812390444993549203038354883176703281322899110004024395674513226847632315312959749352534835200],
                                                             'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
                                                             'B_log_saved_record_expected_SHA256': '7ba5fb90631a413504b3196824f8ef69649e44477bd13c4cbca20cc565941cae',
                                                             'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/independent_log_prefix_squared_L2.json',
                                                             'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
                                                             'alpha_beta_original_record_expected_SHA256': '6e293022c0b2682a0c2c2abe1aa672b954423831ed4503f8732fa95f01cb9b8e',
                                                             'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_stock_exponential_envelopes.json',
                                                             'alpha_original_field': ['B4x12',
                                                                                      'alpha_upper'],
                                                             'alpha_original_literal_pair': [247002706270630918565331540008958163692589137852088424583460925597448157152683677894942918643332625323316582822253875275,
                                                                                             22181357552966518876627313473144669627491496603006532601363836644916970462445004984319795248833116624779129687691228574631793262592],
                                                             'beta_original_field': ['B4x12',
                                                                                     'beta_upper'],
                                                             'beta_original_literal_pair': [1,
                                                                                            1099511627776],
                                                             'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                                                               'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                                                               'coordinate_squared_B_literal_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84',
                                                                                                               'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json',
                                                                                                               'coordinate_squared_B_uncombined_literal': [45526575641624206065960088254647963011088397925424336288233050317860197460879324658749414611574392425861283022019968244562699896140455970821288493126573624826536536912610825770883742372490773981523979696246736685050999662274328929778131746172668001901691046834836586721194202082479121970699430337226697752568947187457296404138334397844423679815518881938375176693001373653480415842115399914944778807835058160148015764442345734677926164113677443351799296560705736910653276695736495021885524820312187058296068869310952956910819322154696725305584723965789462683039126727683916922786468244659518851588647486421853725162918802134315547820918795106049611857838088118685068522360897370538324399193149950569315794375412868603490602486645544192130229308142902137397386041398706454720528355157101284743157437656955492159236359877173948345445727319099126101823284957663395902942816481504672717487603102511793763726345482303724630928183512057385898650074369193079140521157948972608871495778625773102762931608632772763752420208898616246237860960043233083858239,
                                                                                                                                                           1064311162290314829993317570393594139098783759755472316751688907376604267686819057685722084483472694979913873600803721210261653601613069280337194220754598433785378364203070858496756245943431492169577928446243218733206784282860496472857713784849350212282348295966506207303324069383995279555657006575860272992372853027356973988113815245928293961331789704506862768806632883623539099201848989216833061560609366169844682079158783936810813014476063528488006048240464997985884687969145967483292119744767282112030435416265811730561355136342763978551994132702756478800100718262968364118613782877026044387867417640192327089432833159010812111753923769185578544857826757126549955911889493341782728564597276328179501589306777896495754952403978573163919346168330904035486839477729792271453485959504398136183338911862175782922917093258127209534688205322695296676276395441012752256514277180818595823615644362363091088759329682368039258062181761762722268836977250742748313007631976499454204739038094317076899400791760670433509355026879994577025079039421948666755153920000],
                                                                                                               'fields': {'additive_rounding_zero_only_after_no_wrap': True,
                                                                                                                          'common_literal_error_upper': [276166322630920802395230294070446372783075414029508302638124289962937731639648392341357814793924321396020554846440862515,
                                                                                                                                                         1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888],
                                                                                                                          'drift_literal_error': [7,
                                                                                                                                                  27487790694400],
                                                                                                                          'every_original_driver_once': True,
                                                                                                                          'every_stored_partial_sum_and_product_safe': True,
                                                                                                                          'idio_literal_error_upper': [156576429583424880029055937563110731415892319528210216364286123675151694157011596510784577608392178182727361521908420199,
                                                                                                                                                       709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                          'initial_literal_error_upper': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                                                                                                                          346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                                                                                                                          'true_common_enclosure': [[38877535641111535490325048879373881033237089667338836564302146726369221970178317277329260034200117344446008391755317237212265486745,
                                                                                                                                                     709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                                                    [77755071282223070980650097758747762066474179334677673128604293452738443940356634554658520068400234688892016783510634474424530973491,
                                                                                                                                                     1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888]],
                                                                                                                          'true_idio_enclosure': [[47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343833,
                                                                                                                                                   709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                                                  [47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343835,
                                                                                                                                                   709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944]],
                                                                                                                          'true_initial_enclosure': [[51074463243831589481644883618341444951183233404609790581927792645537908406073896346061752896907334970354529391308639775166059120735,
                                                                                                                                                      11090678776483259438313656736572334813745748301503266300681918322458485231222502492159897624416558312389564843845614287315896631296],
                                                                                                                                                     [1596076976369737171301402613073170154724476043894055955685243520173059637689809260814429778028354217823579043478394992973939347523,
                                                                                                                                                      346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728]]},
                                                                                                               'literal_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                                                                               'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json'},
                                                             'e0_original_field': ['B4x12',
                                                                                   'initial_literal_error_upper'],
                                                             'e0_original_literal_pair': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                                                          346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                                                             'e0_original_record_expected_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                             'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json',
                                                             'future_first_stock_squared_bound': None,
                                                             'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                                                              'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                                                              'mu_lower_minus_a_strict_positive': None},
                                                             'ln2_lower_original_field': ['exact_component_allowances',
                                                                                          'ln2_lower'],
                                                             'ln2_lower_original_literal_pair': [1889261008865840820845434144940756618726999344670259515995750754217821754500788139444939524188547339025585587602769247784879116306451410162687618926710924446943916199137723684941981681870055380792574043291861815817772683212125601991704013718366662977212533772715036747350128426675744178435868437524651465387808022185045717540672567957277642069441780888858051055534388844360342398807653805619980652864503681208434677961274301606889689060873958402013731503561912296584004582336707583167425957420682771042753827882862458159391895363893023780996566350849344303354407122266002809532662847818704615735400368470916489232620845467336296959876015254942962044676870458651995798514099816581832619706240631245441372803345552299783611172312186961514646923930769255231,
                                                                                                 2725627488435628481496863175516455096268428871729528261974136657897740576702135939247829423093197483020632924981445528712795654376699704931913098750094045475418234376750483233635429338640072811018588732010250132338523030120871129556706434130706601892323570904539447104103180959965009284063038974813443414272999699177340229319053742082159247821787254916183238108504018824427371176008091776833205564916200995241120217565045507036810006744635670740696031073014129582349551099313579709502048339831984281555128954829589841559252686271983451367307069838038458075841476737790053476210649922039653098169050211612672671518989555517522647432276621598282684754503894614556632435948513203616062757277391012459709406205277046040823461804052649041636834455710597120000],
                                                             'ln2_lower_original_record_expected_SHA256': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c',
                                                             'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json',
                                                             'profile': 'independent130'},
                                          'primary90': {'B_log_original_literal_pair': [8512947868103270312620178638577675641787226919214228390530540381034131465897304040781846302011961304683661376217863894953653714626337944010446722728460538706926595232008107602575959975484595860579894434422595857037680642776863378528725175958732706908884736896816233339222173517891896741153446551808050780878902912055518946683907564816233968640153853973297161216675566384159352979311963775610947610269712162731115111068282500641705615023150474720728493520613362903823017476623356456346506182833482073871210080440284457552935309761648687916830904137003262193567398209116027802650614357784102225851623479377033752444067913586656279260339319807583904153617578284670222196187068661423744113098974350950521477755319342951839540876201609502733051489887920720037787943025286596377416669772603979,
                                                                                        5307039716072348696780168043740813464254609720802369423615294422907314307532518321538000940854478613980872020981793264427883045912368569694412757615556272398241982644161294516303803767354132880993538021210644731634689200578055163749524840592464477041507439945512096728776437943453406084685270822889988767868681493195952982792018927866877152888635594824290311697822256357585190810004684089502253539393496036233330075699157469101665700736452449271068553649074774557957281301950960647319203684623658366702735103742598936202023206199332036084265486135044737289634458202359168772559818555896159232721394619758320074879224794515146455685801330982081012412819934289386060886436186831160504046273104674577722520394081048768080809242859607520397670454818010531687899611661207230488036051164023784210432000],
                                                        'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
                                                        'B_log_saved_record_expected_SHA256': '2a1833c8685add43b3854180b0e919ae63d6e1f4f00b15e0b4a979dab55d7a29',
                                                        'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/primary_log_prefix_squared_L2.json',
                                                        'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
                                                        'alpha_beta_original_record_expected_SHA256': '525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a',
                                                        'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json',
                                                        'alpha_original_field': ['cases',
                                                                                 'B4x12',
                                                                                 'alpha_upper'],
                                                        'alpha_original_literal_pair': [45367232165459914923385662946667222531831256343543066774787104815382220620136265,
                                                                                        4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794752],
                                                        'beta_original_field': ['cases',
                                                                                'B4x12',
                                                                                'beta_upper'],
                                                        'beta_original_literal_pair': [1,
                                                                                       1099511627776],
                                                        'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                                                          'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                                                          'coordinate_squared_B_literal_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2',
                                                                                                          'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json',
                                                                                                          'coordinate_squared_B_uncombined_literal': [6384515858493324899204650816690602383243896628762144024838388575192784288263607574124475579311362107174259757315894678092932691144004996317684757239491577738663479089538830715373626887086762482848504764370894874601009690359513645879614296781215736265714976320857346435131493617915612198522808202631593695291899931649672368386146234734570417339446416702867410231806773950424091090661434442689891841358379288364117360578041218553229275135046496308953688840643190076858815826553021255552734203751723861582615543903022215132454667522895236911653076632975961585083926964508397813772669857423849359689257596440325535868533564587618339196330539161884615914792034482603801651059720606527409707394353927004650599038825068815554312722513304368639406353833221401969503097551111,
                                                                                                                                                      149255932348255029840930948694338021615758146182516215147903290154068608446638153532202662774179879721055219787468365833860973589471728563011692324832415929957895190975456274701802682993794698953733072940370655372202170774929412649893781138342842707674374706002694455090309162290064574705282811923418527693442615475576702226367774728084108794656911985978714181318614520136612078178581015897518667459585847855253021122272037703116390174668376951309260296787554752552811293610708797592730899712395924372711170571650703269509976322305071112951079966178662768362870326736403383874217502741289202539189610610979453036539824285013214071642625704529170206938597092797681220024236618836869254858053825329456771958456653563065069111119133549684255094573363094756306151650558476288000],
                                                                                                          'fields': {'addition_rounding_paid': 0,
                                                                                                                     'common_literal_error_upper': [25361871260938488729228877533401678061248213015932440747215362596598621650241007,
                                                                                                                                                    130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064],
                                                                                                                     'drift_literal_error_upper': [7,
                                                                                                                                                   27487790694400],
                                                                                                                     'every_signed144_scaled_normal_product_safe': True,
                                                                                                                     'every_stored72_raw_partial_sum_safe': True,
                                                                                                                     'exact_common_coefficient_enclosure': [[3570337775001464811484133992278442479448757806641386405762450668688115075446873113027781367,
                                                                                                                                                             65185151242703554760590262029100101153646988597309960020356494379340201592426774597868716032],
                                                                                                                                                            [7140675550002929622968267984556884958897515613282772811524901337376230150893746226055562735,
                                                                                                                                                             130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064]],
                                                                                                                     'exact_drift': [-1,
                                                                                                                                     800],
                                                                                                                     'exact_idio_coefficient_enclosure': [[1093188219767175304906489994055034964269771883937280948777703827016588627670840331443227841,
                                                                                                                                                           16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                                                                                                          [2186376439534350609812979988110069928539543767874561897555407654033177255341680662886455683,
                                                                                                                                                           32592575621351777380295131014550050576823494298654980010178247189670100796213387298934358016]],
                                                                                                                     'idio_literal_error_upper': [3594818524360149261960544761045424477895504472498124242279759015017946963915583,
                                                                                                                                                  16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                                                                     'initial_log_spot_error_upper': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                                                                                                                                      1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
                                                                                                                     'signed_scaled_normal_floors_per_increment': 2},
                                                                                                          'literal_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                                                                          'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json'},
                                                        'e0_original_field': ['cases',
                                                                              'B4x12',
                                                                              'initial_log_spot_error_upper'],
                                                        'e0_original_literal_pair': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                                                                     1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
                                                        'e0_original_record_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                        'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
                                                        'future_first_stock_squared_bound': None,
                                                        'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                                                         'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                                                         'mu_lower_minus_a_strict_positive': None},
                                                        'ln2_lower_original_field': ['exact_component_allowances',
                                                                                     'ln2_lower'],
                                                        'ln2_lower_original_literal_pair': [1345774352498033414297429742984977384893258835982351961807386333796539728241594400081593475302051821027762048040776563903683902961983263656168213352737876304347045903684241668673381438784885331058207914470224642777024991198545607304922005382825701321879479404077792934389096593003863039049325619009954841406946245966015575618504966501594756534721968950545959386285176356420712421910845677985146290754463549779541316458725767992186966218654989675307831921168545792,
                                                                                            1941541984504468570495415124249969943153260291510923173492279628121237271490888121892502719969273800531384118146530070969072470417266968221171879127013717035856262982263162712777774605998471461725924173989544832278147776356165895694754126642321144762871931919153281705662822212334308489675713211589863160815276266657731584868034417075674451499087564989252906843588748800087924882276955544589775699716444612993024606968249415334365911711858047546545182122278495875],
                                                        'ln2_lower_original_record_expected_SHA256': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60',
                                                        'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json',
                                                        'profile': 'primary90'}},
 'two_profile_adapter_commitments': {'independent130': '0466acccc3e557f0a46f1de1b9e7ff9288f0bbb29d369cca6129b798be4a4787',
                                     'primary90': '94402a3d233afaa4939a5f336b4f795f429e83d2c118441c1dcf66b080932025'}}
FLAGS = {'G2_transfer': False,
 'adoption': False,
 'cost_comparison': False,
 'cost_transfer': False,
 'digital_pair_independence': False,
 'estimator_schedule_emitted': False,
 'financial_adoption': False,
 'fits_or_pilots': False,
 'fixture_credit': 0,
 'full_E11_completed': False,
 'full_G2': False,
 'full_price_certificate': False,
 'gate_emission': False,
 'item': 'E11',
 'local_only': True,
 'native_arrays_generated_or_replayed': False,
 'native_financial_path_or_policy_L2_verified': False,
 'native_source_clipping_inserted': False,
 'new_global_fixture_credit': 0,
 'new_test_credit': 0,
 'new_transcendental_series': False,
 'old_numerical_helpers_or_evaluators_called': False,
 'one_first_stock_squared_L2_only': True,
 'physical_certificate': False,
 'prices_or_paths_sampled': False,
 'quantum_advantage': False,
 'source_emission': False,
 'source_substitution_authorized': False}
ROLE_GRAPH = {'active10': ['A01_run011',
              'A02_BM_native_financial_bridge_audit_run002',
              'A02_BM_native_financial_bridge_root_verification_run001',
              'A02_BM_native_financial_bridge_run002',
              'A10_coefficient_run001',
              'C06_pair_audit_run001',
              'C06_pair_run001',
              'E11_scalar_midpoint_L2_numerical_run002',
              'E11_native_coordinate_squared_L2_run001',
              'E11_first_log_prefix_squared_L2_run001'],
 'all18_snapshot_canonical_JSON_SHA256': {'A01_run011': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                          'A01_run014': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                          'A02_BM_native_financial_bridge_audit_run002': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                          'A02_BM_native_financial_bridge_root_verification_run001': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                          'A02_BM_native_financial_bridge_run002': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                          'A02_quantile_financial_audit_run001': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                          'A02_quantile_law_audit_run001': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                          'A10_coefficient_run001': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                          'C06_pair_audit_run001': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                          'C06_pair_run001': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                          'C07_barrier_audit_run001': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                          'C07_barrier_run001': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                          'C07_barrier_run002': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                          'C07_bound_date1_run001': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                          'E10_continuous_moment_only_run002': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                          'E11_first_log_prefix_squared_L2_run001': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                          'E11_native_coordinate_squared_L2_run001': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                          'E11_scalar_midpoint_L2_numerical_run002': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c'},
 'all18_snapshot_dicts_not18_runtime_success_permissions': True,
 'all_archive_nested_runtime_maps_preserved_not_admitted_as_current_runtime': True,
 'archive8': ['A01_run014',
              'A02_quantile_financial_audit_run001',
              'A02_quantile_law_audit_run001',
              'E10_continuous_moment_only_run002',
              'C07_barrier_audit_run001',
              'C07_barrier_run001',
              'C07_barrier_run002',
              'C07_bound_date1_run001'],
 'completed_first_log_new_owner_only_after_ROOT_verification': True,
 'full_snapshot_authority': {'JSON_pointer': ['complete_original_cited_owner_snapshots'],
                             'expected_SHA256': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
                             'path': '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json'},
 'original17_objects_unchanged': True,
 'original_raw_missing_None_and_A10_bare_keys_external_owned_layouts_unchanged': True,
 'owner_summaries': {'A01_run011': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                    'literal_expected_manifest_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03',
                                    'manifest_path': 'results/limitation_program_20261001/A01_run011/manifest.json',
                                    'owned_bytes': 8745921,
                                    'owned_files': 13,
                                    'role': 'inherited active original proof/custody'},
                     'A01_run014': {'full_original_snapshot_canonical_JSON_SHA256': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                    'literal_expected_manifest_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8',
                                    'manifest_path': 'results/limitation_program_20261001/A01_run014/manifest.json',
                                    'owned_bytes': 37429139,
                                    'owned_files': 16,
                                    'role': 'unchanged archived opaque custody/citation only'},
                     'A02_BM_native_financial_bridge_audit_run002': {'full_original_snapshot_canonical_JSON_SHA256': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                     'literal_expected_manifest_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0',
                                                                     'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/manifest.json',
                                                                     'owned_bytes': 44651234,
                                                                     'owned_files': 24,
                                                                     'role': 'inherited active '
                                                                             'original '
                                                                             'proof/custody'},
                     'A02_BM_native_financial_bridge_root_verification_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                 'literal_expected_manifest_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab',
                                                                                 'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_root_verification_run001/manifest.json',
                                                                                 'owned_bytes': 579999,
                                                                                 'owned_files': 3,
                                                                                 'role': 'inherited '
                                                                                         'active '
                                                                                         'original '
                                                                                         'proof/custody'},
                     'A02_BM_native_financial_bridge_run002': {'full_original_snapshot_canonical_JSON_SHA256': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                               'literal_expected_manifest_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162',
                                                               'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/manifest.json',
                                                               'owned_bytes': 113209386,
                                                               'owned_files': 29,
                                                               'role': 'inherited active original '
                                                                       'proof/custody'},
                     'A02_quantile_financial_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                             'literal_expected_manifest_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323',
                                                             'manifest_path': 'results/limitation_program_20261001/A02_quantile_financial_audit_run001/manifest.json',
                                                             'owned_bytes': 1107202,
                                                             'owned_files': 9,
                                                             'role': 'unchanged archived opaque '
                                                                     'custody/citation only'},
                     'A02_quantile_law_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                       'literal_expected_manifest_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572',
                                                       'manifest_path': 'results/limitation_program_20261001/A02_quantile_law_audit_run001/manifest.json',
                                                       'owned_bytes': 379157,
                                                       'owned_files': 8,
                                                       'role': 'unchanged archived opaque '
                                                               'custody/citation only'},
                     'A10_coefficient_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                'literal_expected_manifest_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40',
                                                'manifest_path': 'results/limitation_program_20261001/A10_coefficient_run001/manifest.json',
                                                'owned_bytes': 107197203,
                                                'owned_files': 557,
                                                'role': 'inherited active original proof/custody'},
                     'C06_pair_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                               'literal_expected_manifest_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14',
                                               'manifest_path': 'results/limitation_program_20261001/C06_pair_audit_run001/manifest.json',
                                               'owned_bytes': 1109330,
                                               'owned_files': 11,
                                               'role': 'inherited active original proof/custody'},
                     'C06_pair_run001': {'full_original_snapshot_canonical_JSON_SHA256': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                         'literal_expected_manifest_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a',
                                         'manifest_path': 'results/limitation_program_20261001/C06_pair_run001/manifest.json',
                                         'owned_bytes': 738350,
                                         'owned_files': 11,
                                         'role': 'inherited active original proof/custody'},
                     'C07_barrier_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                  'literal_expected_manifest_SHA256': '29fe018792317eef189a9e6ceae00bf80c13b81fafd89ef0f4c3f48933dd98c9',
                                                  'manifest_path': 'results/limitation_program_20261001/C07_barrier_audit_run001/manifest.json',
                                                  'owned_bytes': 51656,
                                                  'owned_files': 11,
                                                  'role': 'unchanged archived opaque '
                                                          'custody/citation only'},
                     'C07_barrier_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                            'literal_expected_manifest_SHA256': 'e30e10549a76d2baa07d44429badaf8e69f85b10041478def0f673b228c3a7b9',
                                            'manifest_path': 'results/limitation_program_20261001/C07_barrier_run001/manifest.json',
                                            'owned_bytes': 64258,
                                            'owned_files': 9,
                                            'role': 'unchanged archived opaque custody/citation '
                                                    'only'},
                     'C07_barrier_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                            'literal_expected_manifest_SHA256': '3ce81f47db7fcd054d33a7391fb4600303f1f8afac545367c473172e740b6c9b',
                                            'manifest_path': 'results/limitation_program_20261001/C07_barrier_run002/manifest.json',
                                            'owned_bytes': 75701,
                                            'owned_files': 11,
                                            'role': 'unchanged archived opaque custody/citation '
                                                    'only'},
                     'C07_bound_date1_run001': {'full_original_snapshot_canonical_JSON_SHA256': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                'literal_expected_manifest_SHA256': '9f7e676d7b7eb1c14b8ae8815b756da4491b50530fbdf9722b9861712de60dd6',
                                                'manifest_path': 'results/limitation_program_20261001/C07_bound_date1_run001/manifest.json',
                                                'owned_bytes': 126462,
                                                'owned_files': 15,
                                                'role': 'unchanged archived opaque '
                                                        'custody/citation only'},
                     'E10_continuous_moment_only_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                           'literal_expected_manifest_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668',
                                                           'manifest_path': 'results/limitation_program_20261001/E10_continuous_moment_only_run002/manifest.json',
                                                           'owned_bytes': 7876736,
                                                           'owned_files': 18,
                                                           'role': 'unchanged archived opaque '
                                                                   'custody/citation only'},
                     'E11_first_log_prefix_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                                                'literal_expected_manifest_SHA256': '165ff337315efeca8a658b1db46b172178598150f2c6b760a45bf22233f1a600',
                                                                'manifest_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/manifest.json',
                                                                'owned_bytes': 35880313,
                                                                'owned_files': 27,
                                                                'role': 'new active scoped '
                                                                        'completed first-log '
                                                                        'numerical input only'},
                     'E11_native_coordinate_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                 'literal_expected_manifest_SHA256': 'bb1f08a600712e34d1fa4b3c77f0ea04147c5368c8f92dc4f9a21ed3e293df95',
                                                                 'manifest_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/manifest.json',
                                                                 'owned_bytes': 68640627,
                                                                 'owned_files': 47,
                                                                 'role': 'inherited active '
                                                                         'original proof/custody'},
                     'E11_scalar_midpoint_L2_numerical_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c',
                                                                 'literal_expected_manifest_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170',
                                                                 'manifest_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/manifest.json',
                                                                 'owned_bytes': 7729234,
                                                                 'owned_files': 20,
                                                                 'role': 'inherited active '
                                                                         'original proof/custody'}},
 'three_original_equal_SHA_archive_aliases': [{'current_original_path_integrity_asserted': False,
                                               'expected_hash_waived': False,
                                               'expected_sha256': '69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6',
                                               'original_key': 'research/controlled_source_completion/nonrestoring_sqrt.py',
                                               'original_map': 'frozen_inputs',
                                               'original_owner': 'A01_run011',
                                               'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/nonrestoring_sqrt.py'},
                                              {'current_original_path_integrity_asserted': False,
                                               'expected_hash_waived': False,
                                               'expected_sha256': '52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b',
                                               'original_key': 'research/journal_sprint/reversible_fixed_point.py',
                                               'original_map': 'frozen_inputs',
                                               'original_owner': 'A01_run011',
                                               'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible_fixed_point.py'},
                                              {'current_original_path_integrity_asserted': False,
                                               'expected_hash_waived': False,
                                               'expected_sha256': '5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a',
                                               'original_key': 'research/antithetic_feasibility/reversible.py',
                                               'original_map': 'frozen_inputs',
                                               'original_owner': 'A01_run011',
                                               'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}]}
ACTIVE_OWNERS = ['A01_run011',
 'A02_BM_native_financial_bridge_audit_run002',
 'A02_BM_native_financial_bridge_root_verification_run001',
 'A02_BM_native_financial_bridge_run002',
 'A10_coefficient_run001',
 'C06_pair_audit_run001',
 'C06_pair_run001',
 'E11_scalar_midpoint_L2_numerical_run002',
 'E11_native_coordinate_squared_L2_run001',
 'E11_first_log_prefix_squared_L2_run001']
ARCHIVE_CITATIONS = ['A01_run014',
 'A02_quantile_financial_audit_run001',
 'A02_quantile_law_audit_run001',
 'E10_continuous_moment_only_run002',
 'C07_barrier_audit_run001',
 'C07_barrier_run001',
 'C07_barrier_run002',
 'C07_bound_date1_run001']
PROFILE_CONTRACT = {'independent130': {'B_log_original_literal_pair': [2428158210523221716611869059561284163506426632206382933227882749799107497844497983493965778077859665221003848479909443502356283144309763445667792023072878245744752236936706476755951355252171098226395633180998333416396336106714275667874841716872377533973362164422306514278219297714838302666989189183695256703701608221630931547883699856199822898192517375275381325725885420659120650636522924098635555012513935156871817454254946932191744197140849579927797658793344456153044262066893575491316898749520247694131272008480484279767442621311639247906829230752566809805133006122638828228870494291445884186293021900488583473809333911893695999791478916008054562105198374155378886604081879712491148543043767842545408363141653398723997338202229669865800275898817433527911904806662136305852498339695196210493003428178533842259395795527764866221522384929346609169752763847410100021900211807612222242377686666678799320498627233759536718291110326114419560051244617985404989154265033792342989447457763132027823749179017384608895015113531159623561782481108005357554216247019645899050523,
                                                    1513733228466844074031275717429922960187834973955384601995536522750016224414668727819206116519306201179573042460674520346942702696629351302643155826634064290672325608545738612667826017895680334158654790028613891981326576843599902103891630952814511173327529997748425925496065487194844289996932339143900081966349579181053527389213998289763844397764192911821096266306307504423212647986687390974299915254681199374147253096002018965665012434635135952694797887226841083837066248297522135663165086552559028923067229727245617133616118090428699689301851612632033088052755892767180543198941489242025484577036517070180690342893617402169278129137856839223966607852369548571543075007653621750787446809392176100547184066983840358432973683897920428422230036262075573229148857864832716125527510362375539991393222476383567811375726121835388823028241346307366055443781189365504221014616251877476187866875683293332963037770069373358608728988510788498971777052572870846793872720761611264090303077011502812390444993549203038354883176703281322899110004024395674513226847632315312959749352534835200],
                    'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
                    'B_log_saved_record_expected_SHA256': '7ba5fb90631a413504b3196824f8ef69649e44477bd13c4cbca20cc565941cae',
                    'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/independent_log_prefix_squared_L2.json',
                    'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
                    'alpha_beta_original_record_expected_SHA256': '6e293022c0b2682a0c2c2abe1aa672b954423831ed4503f8732fa95f01cb9b8e',
                    'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_stock_exponential_envelopes.json',
                    'alpha_original_field': ['B4x12', 'alpha_upper'],
                    'alpha_original_literal_pair': [247002706270630918565331540008958163692589137852088424583460925597448157152683677894942918643332625323316582822253875275,
                                                    22181357552966518876627313473144669627491496603006532601363836644916970462445004984319795248833116624779129687691228574631793262592],
                    'beta_original_field': ['B4x12', 'beta_upper'],
                    'beta_original_literal_pair': [1, 1099511627776],
                    'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                      'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                      'coordinate_squared_B_literal_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84',
                                                                      'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json',
                                                                      'coordinate_squared_B_uncombined_literal': [45526575641624206065960088254647963011088397925424336288233050317860197460879324658749414611574392425861283022019968244562699896140455970821288493126573624826536536912610825770883742372490773981523979696246736685050999662274328929778131746172668001901691046834836586721194202082479121970699430337226697752568947187457296404138334397844423679815518881938375176693001373653480415842115399914944778807835058160148015764442345734677926164113677443351799296560705736910653276695736495021885524820312187058296068869310952956910819322154696725305584723965789462683039126727683916922786468244659518851588647486421853725162918802134315547820918795106049611857838088118685068522360897370538324399193149950569315794375412868603490602486645544192130229308142902137397386041398706454720528355157101284743157437656955492159236359877173948345445727319099126101823284957663395902942816481504672717487603102511793763726345482303724630928183512057385898650074369193079140521157948972608871495778625773102762931608632772763752420208898616246237860960043233083858239,
                                                                                                                  1064311162290314829993317570393594139098783759755472316751688907376604267686819057685722084483472694979913873600803721210261653601613069280337194220754598433785378364203070858496756245943431492169577928446243218733206784282860496472857713784849350212282348295966506207303324069383995279555657006575860272992372853027356973988113815245928293961331789704506862768806632883623539099201848989216833061560609366169844682079158783936810813014476063528488006048240464997985884687969145967483292119744767282112030435416265811730561355136342763978551994132702756478800100718262968364118613782877026044387867417640192327089432833159010812111753923769185578544857826757126549955911889493341782728564597276328179501589306777896495754952403978573163919346168330904035486839477729792271453485959504398136183338911862175782922917093258127209534688205322695296676276395441012752256514277180818595823615644362363091088759329682368039258062181761762722268836977250742748313007631976499454204739038094317076899400791760670433509355026879994577025079039421948666755153920000],
                                                                      'fields': {'additive_rounding_zero_only_after_no_wrap': True,
                                                                                 'common_literal_error_upper': [276166322630920802395230294070446372783075414029508302638124289962937731639648392341357814793924321396020554846440862515,
                                                                                                                1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888],
                                                                                 'drift_literal_error': [7,
                                                                                                         27487790694400],
                                                                                 'every_original_driver_once': True,
                                                                                 'every_stored_partial_sum_and_product_safe': True,
                                                                                 'idio_literal_error_upper': [156576429583424880029055937563110731415892319528210216364286123675151694157011596510784577608392178182727361521908420199,
                                                                                                              709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                 'initial_literal_error_upper': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                                                                                 346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                                                                                 'true_common_enclosure': [[38877535641111535490325048879373881033237089667338836564302146726369221970178317277329260034200117344446008391755317237212265486745,
                                                                                                            709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                           [77755071282223070980650097758747762066474179334677673128604293452738443940356634554658520068400234688892016783510634474424530973491,
                                                                                                            1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888]],
                                                                                 'true_idio_enclosure': [[47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343833,
                                                                                                          709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                         [47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343835,
                                                                                                          709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944]],
                                                                                 'true_initial_enclosure': [[51074463243831589481644883618341444951183233404609790581927792645537908406073896346061752896907334970354529391308639775166059120735,
                                                                                                             11090678776483259438313656736572334813745748301503266300681918322458485231222502492159897624416558312389564843845614287315896631296],
                                                                                                            [1596076976369737171301402613073170154724476043894055955685243520173059637689809260814429778028354217823579043478394992973939347523,
                                                                                                             346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728]]},
                                                                      'literal_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                                      'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json'},
                    'e0_original_field': ['B4x12', 'initial_literal_error_upper'],
                    'e0_original_literal_pair': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                 346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                    'e0_original_record_expected_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                    'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json',
                    'future_first_stock_squared_bound': None,
                    'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                     'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                     'mu_lower_minus_a_strict_positive': None},
                    'ln2_lower_original_field': ['exact_component_allowances', 'ln2_lower'],
                    'ln2_lower_original_literal_pair': [1889261008865840820845434144940756618726999344670259515995750754217821754500788139444939524188547339025585587602769247784879116306451410162687618926710924446943916199137723684941981681870055380792574043291861815817772683212125601991704013718366662977212533772715036747350128426675744178435868437524651465387808022185045717540672567957277642069441780888858051055534388844360342398807653805619980652864503681208434677961274301606889689060873958402013731503561912296584004582336707583167425957420682771042753827882862458159391895363893023780996566350849344303354407122266002809532662847818704615735400368470916489232620845467336296959876015254942962044676870458651995798514099816581832619706240631245441372803345552299783611172312186961514646923930769255231,
                                                        2725627488435628481496863175516455096268428871729528261974136657897740576702135939247829423093197483020632924981445528712795654376699704931913098750094045475418234376750483233635429338640072811018588732010250132338523030120871129556706434130706601892323570904539447104103180959965009284063038974813443414272999699177340229319053742082159247821787254916183238108504018824427371176008091776833205564916200995241120217565045507036810006744635670740696031073014129582349551099313579709502048339831984281555128954829589841559252686271983451367307069838038458075841476737790053476210649922039653098169050211612672671518989555517522647432276621598282684754503894614556632435948513203616062757277391012459709406205277046040823461804052649041636834455710597120000],
                    'ln2_lower_original_record_expected_SHA256': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c',
                    'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json',
                    'profile': 'independent130'},
 'primary90': {'B_log_original_literal_pair': [8512947868103270312620178638577675641787226919214228390530540381034131465897304040781846302011961304683661376217863894953653714626337944010446722728460538706926595232008107602575959975484595860579894434422595857037680642776863378528725175958732706908884736896816233339222173517891896741153446551808050780878902912055518946683907564816233968640153853973297161216675566384159352979311963775610947610269712162731115111068282500641705615023150474720728493520613362903823017476623356456346506182833482073871210080440284457552935309761648687916830904137003262193567398209116027802650614357784102225851623479377033752444067913586656279260339319807583904153617578284670222196187068661423744113098974350950521477755319342951839540876201609502733051489887920720037787943025286596377416669772603979,
                                               5307039716072348696780168043740813464254609720802369423615294422907314307532518321538000940854478613980872020981793264427883045912368569694412757615556272398241982644161294516303803767354132880993538021210644731634689200578055163749524840592464477041507439945512096728776437943453406084685270822889988767868681493195952982792018927866877152888635594824290311697822256357585190810004684089502253539393496036233330075699157469101665700736452449271068553649074774557957281301950960647319203684623658366702735103742598936202023206199332036084265486135044737289634458202359168772559818555896159232721394619758320074879224794515146455685801330982081012412819934289386060886436186831160504046273104674577722520394081048768080809242859607520397670454818010531687899611661207230488036051164023784210432000],
               'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
               'B_log_saved_record_expected_SHA256': '2a1833c8685add43b3854180b0e919ae63d6e1f4f00b15e0b4a979dab55d7a29',
               'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/primary_log_prefix_squared_L2.json',
               'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
               'alpha_beta_original_record_expected_SHA256': '525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a',
               'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json',
               'alpha_original_field': ['cases', 'B4x12', 'alpha_upper'],
               'alpha_original_literal_pair': [45367232165459914923385662946667222531831256343543066774787104815382220620136265,
                                               4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794752],
               'beta_original_field': ['cases', 'B4x12', 'beta_upper'],
               'beta_original_literal_pair': [1, 1099511627776],
               'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                 'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                 'coordinate_squared_B_literal_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2',
                                                                 'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json',
                                                                 'coordinate_squared_B_uncombined_literal': [6384515858493324899204650816690602383243896628762144024838388575192784288263607574124475579311362107174259757315894678092932691144004996317684757239491577738663479089538830715373626887086762482848504764370894874601009690359513645879614296781215736265714976320857346435131493617915612198522808202631593695291899931649672368386146234734570417339446416702867410231806773950424091090661434442689891841358379288364117360578041218553229275135046496308953688840643190076858815826553021255552734203751723861582615543903022215132454667522895236911653076632975961585083926964508397813772669857423849359689257596440325535868533564587618339196330539161884615914792034482603801651059720606527409707394353927004650599038825068815554312722513304368639406353833221401969503097551111,
                                                                                                             149255932348255029840930948694338021615758146182516215147903290154068608446638153532202662774179879721055219787468365833860973589471728563011692324832415929957895190975456274701802682993794698953733072940370655372202170774929412649893781138342842707674374706002694455090309162290064574705282811923418527693442615475576702226367774728084108794656911985978714181318614520136612078178581015897518667459585847855253021122272037703116390174668376951309260296787554752552811293610708797592730899712395924372711170571650703269509976322305071112951079966178662768362870326736403383874217502741289202539189610610979453036539824285013214071642625704529170206938597092797681220024236618836869254858053825329456771958456653563065069111119133549684255094573363094756306151650558476288000],
                                                                 'fields': {'addition_rounding_paid': 0,
                                                                            'common_literal_error_upper': [25361871260938488729228877533401678061248213015932440747215362596598621650241007,
                                                                                                           130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064],
                                                                            'drift_literal_error_upper': [7,
                                                                                                          27487790694400],
                                                                            'every_signed144_scaled_normal_product_safe': True,
                                                                            'every_stored72_raw_partial_sum_safe': True,
                                                                            'exact_common_coefficient_enclosure': [[3570337775001464811484133992278442479448757806641386405762450668688115075446873113027781367,
                                                                                                                    65185151242703554760590262029100101153646988597309960020356494379340201592426774597868716032],
                                                                                                                   [7140675550002929622968267984556884958897515613282772811524901337376230150893746226055562735,
                                                                                                                    130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064]],
                                                                            'exact_drift': [-1,
                                                                                            800],
                                                                            'exact_idio_coefficient_enclosure': [[1093188219767175304906489994055034964269771883937280948777703827016588627670840331443227841,
                                                                                                                  16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                                                                 [2186376439534350609812979988110069928539543767874561897555407654033177255341680662886455683,
                                                                                                                  32592575621351777380295131014550050576823494298654980010178247189670100796213387298934358016]],
                                                                            'idio_literal_error_upper': [3594818524360149261960544761045424477895504472498124242279759015017946963915583,
                                                                                                         16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                            'initial_log_spot_error_upper': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                                                                                             1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
                                                                            'signed_scaled_normal_floors_per_increment': 2},
                                                                 'literal_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                                 'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json'},
               'e0_original_field': ['cases', 'B4x12', 'initial_log_spot_error_upper'],
               'e0_original_literal_pair': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                            1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
               'e0_original_record_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
               'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
               'future_first_stock_squared_bound': None,
               'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                'mu_lower_minus_a_strict_positive': None},
               'ln2_lower_original_field': ['exact_component_allowances', 'ln2_lower'],
               'ln2_lower_original_literal_pair': [1345774352498033414297429742984977384893258835982351961807386333796539728241594400081593475302051821027762048040776563903683902961983263656168213352737876304347045903684241668673381438784885331058207914470224642777024991198545607304922005382825701321879479404077792934389096593003863039049325619009954841406946245966015575618504966501594756534721968950545959386285176356420712421910845677985146290754463549779541316458725767992186966218654989675307831921168545792,
                                                   1941541984504468570495415124249969943153260291510923173492279628121237271490888121892502719969273800531384118146530070969072470417266968221171879127013717035856262982263162712777774605998471461725924173989544832278147776356165895694754126642321144762871931919153281705662822212334308489675713211589863160815276266657731584868034417075674451499087564989252906843588748800087924882276955544589775699716444612993024606968249415334365911711858047546545182122278495875],
               'ln2_lower_original_record_expected_SHA256': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60',
               'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json',
               'profile': 'primary90'}}
SELECTED_LOG = {'actual_common_literal': 60222732077,
 'actual_drift_signed_literal': -1374389535,
 'actual_idio_literal': 73757482253,
 'actual_initial_literal': 5063438167381,
 'addition_rounding_zero_requires_original_all_partial_no_wrap': True,
 'asset_zero_based': 0,
 'case': 'B4x12',
 'contractual_date_one_based': 1,
 'fraction_bits': 40,
 'ideal_reference_exact_literal_parameters': {'S0': [100, 1],
                                              'T': [1, 1],
                                              'drift': [-1, 800],
                                              'r': [3, 100],
                                              'rho': [2, 5],
                                              'sigma': [3, 10],
                                              't': [1, 12]},
 'legacy_binary64_real_parameters_equal_exact_decimal_claimed': False,
 'newly_evaluated_or_synthesized_target': False,
 'ordered_native_normal_values': [94, 125],
 'ordered_original_normal_indices': [0, 1],
 'original_prefix_witness': {'asset': 0,
                             'constants': [[-1374389535, 1], [5063438167381, 1]],
                             'date': 0,
                             'every_driver_multiplicity': 1,
                             'original_normal_indices': [0, 1],
                             'raw_log': 3542,
                             'stock': 4021},
 'original_shared_pair_scope': {'cosines': [{'address': 67,
                                             'floors': 7,
                                             'input': 6,
                                             'local': 71,
                                             'lookup_outputs': [72, 73, 74, 75, 76, 77, 78, 79],
                                             'output': 93},
                                            {'address': 99,
                                             'floors': 7,
                                             'input': 61,
                                             'local': 102,
                                             'lookup_outputs': [103,
                                                                104,
                                                                105,
                                                                106,
                                                                107,
                                                                108,
                                                                109,
                                                                110],
                                             'output': 124}],
                                'log': {'address': 23,
                                        'floors': 8,
                                        'input': 15,
                                        'local': 27,
                                        'lookup_outputs': [28, 29, 30, 31, 32, 33, 34, 35, 36],
                                        'output': 52},
                                'normal_values': [94, 125],
                                'original_shared_pair_preserved': True,
                                'radius': 58,
                                'raw_uniform_values': [0, 1]},
 'raw_preclip_log_value': 3542,
 'saved_date_zero_based': 0,
 'signed_cmul_floors': 2,
 'source_seven_node_slice_saved_metadata': [{'args': [94],
                                             'op': 'cmul',
                                             'out': [3492],
                                             'params': {'c': 60222732077}},
                                            {'args': [125],
                                             'op': 'cmul',
                                             'out': [3493],
                                             'params': {'c': 73757482253}},
                                            {'args': [3492, 3493],
                                             'op': 'add',
                                             'out': [3494],
                                             'params': {}},
                                            {'args': [],
                                             'op': 'const',
                                             'out': [3495],
                                             'params': {'value': 4722366482868270824161}},
                                            {'args': [3494, 3495],
                                             'op': 'add',
                                             'out': [3496],
                                             'params': {}},
                                            {'args': [],
                                             'op': 'const',
                                             'out': [3541],
                                             'params': {'value': 5063438167381}},
                                            {'args': [3496, 3541],
                                             'op': 'add',
                                             'out': [3542],
                                             'params': {}}],
 'stock_consumer_not_claimed': 4021,
 'target_literal_SHA256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
 'target_path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json',
 'time_exact_literal': [1, 12],
 'width': 72}
SELECTED_SITE = {'actual_original_support_signature': '2a35ab41d964c6abc9a3a6243a93f1be141b31da20672c50cdfe0d452239311e',
 'clipped': 3579,
 'exponent': 3979,
 'high': 9145480617430,
 'inverse_ln2': 1586259972792,
 'ln2': 762123384786,
 'low': -12193974156573,
 'polynomial': 4020,
 'raw_log': 3542,
 'remainder': 3982,
 'stock': 4021,
 'values': [16,
            3978,
            3979,
            3980,
            3981,
            3982,
            3983,
            3984,
            3985,
            3986,
            3987,
            3988,
            3989,
            3990,
            3991,
            3992,
            3993,
            3994,
            3995,
            3996,
            3997,
            3998,
            3999,
            4000,
            4001,
            4002,
            4003,
            4004,
            4005,
            4006,
            4007,
            4008,
            4009,
            4010,
            4011,
            4012,
            4013,
            4014,
            4015,
            4016,
            4017,
            4018,
            4019,
            4020,
            4021]}
THEOREM = {'C16_unevaluated_exact_product_factors': [1,
                                           3,
                                           5,
                                           7,
                                           9,
                                           11,
                                           13,
                                           15,
                                           17,
                                           19,
                                           21,
                                           23,
                                           25,
                                           27,
                                           29,
                                           31],
 'Gaussian_moment_identity': 'For a centered continuous N(0,v), E W^32=(31)!!*v^16=C16*v^16, by '
                             'Gaussian integration-by-parts recurrence; no moment of digital '
                             'coordinates is used.',
 'M_fixed': 256,
 'M_guard_unevaluated': 'b <= 8*own_saved_ln2_lower implies exp(b)<=2^8=M',
 'Q': 1099511627776,
 'continuous_exponential_tilt_identity': 'E[exp(2L)1{L>b}]=exp(2mu+2v)*P(N(mu+2v,v)>b); complete '
                                         'square in the unconditional continuous Gaussian density.',
 'continuous_normal_law': 'Only original continuous ideal Z0,Z1 are independent standard normals. '
                          'Native shared finite pair is never assumed independent. L has mean '
                          'mu=ln100-1/800 and variance v=3/400.',
 'core_projection_bound': 'P fixes L_N because all native L_N belong to [a,b]; '
                          '|L_N-P(L)|<=|L_N-L|. On [a,b], exp is M-Lipschitz.',
 'd_lower_unevaluated': 'mu_lower-a',
 'd_upper_tilted_unevaluated': 'b-mu_upper-2*v',
 'even_moment_order': 32,
 'exact_tilt_mass': 'exp(2mu+2v)=10000*exp(1/80)<=10000*80/79, using exp(x)<=1/(1-x) for 0<=x<1; '
                    'analytic inequality only, no series evaluated.',
 'exactly_two_own_profile_bounds': 'Evaluate this rational formula once using primary90 original '
                                   'inputs and once using independent130 own original inputs; do '
                                   'not select a minimum, require nesting, mix adapters, or return '
                                   'a third candidate.',
 'ideal_reference': 'L=ln100-1/800+sqrt(3/1000)Z0+sqrt(9/2000)Z1; S=exp(L)',
 'interval_authority_JSON_pointer': ['cases', 'B4x12', 'prefixes', 0, 'actual_raw_log_bounds', 0],
 'interval_authority_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
 'interval_authority_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
 'lower_projection_tail_pointwise': 'On L<a, 0<=exp(a)-exp(L)<=exp(a)<=M; lower squared-tail '
                                    'contribution <=M^2*P(L<a).',
 'lower_tail_bound_unevaluated': 'T_lower=M^2*C16*v^16/(mu_lower-a)^32',
 'moment_half_order': 16,
 'mu_lower_unevaluated': '5063438167381/Q - e0 - 1/800',
 'mu_upper_unevaluated': '5063438167381/Q + e0 - 1/800',
 'native_all_input_interval_raw': [4155861047200, 5968266508490],
 'native_clip_inactive_for_all_inputs_at_this_site_only': True,
 'native_exponential_allowance_unevaluated': 'A=alpha*M+beta from original full-clipped-domain '
                                             'absolute envelope '
                                             '|S_N-exp(L_N)|<=alpha*exp(L_N)+beta; original clip '
                                             'inactive at site',
 'native_initial_log_literal_raw': 5063438167381,
 'new_numerical_moments_products_tail_allowances_bounds': None,
 'new_proof_guard_values': None,
 'pointwise_three_term_proof': '|S_N-exp(L)|<=A+M*|L_N-L|+|exp(P(L))-exp(L)|; square with '
                               'pointwise Cauchy for three terms, then take expectation.',
 'projection': 'P(x)=min(max(x,a),b), a=raw_lower/Q, b=raw_upper/Q; mathematical comparison only, '
               'no source/policy change',
 'prospective_stock_squared_L2_formula': 'B_stock=3*((alpha*M+beta)^2+M^2*B_log+T_lower+T_upper)',
 'selected_scope': {'asset_zero_based': 0,
                    'case': 'B4x12',
                    'clipped_log': 3579,
                    'contractual_date_one_based': 1,
                    'raw_log': 3542,
                    'saved_date_zero_based': 0,
                    'stock': 4021,
                    'units': 'dollars_squared'},
 'upper_projection_tail_pointwise': 'On L>b, 0<=exp(L)-exp(b)<=exp(L); upper squared-tail '
                                    'contribution <=E exp(2L)1{L>b}.',
 'upper_tail_bound_unevaluated': 'T_upper=(10000*80/79)*C16*v^16/(b-mu_upper-2v)^32',
 'v_exact': [3, 400]}
PLANNED_FILES = ['executed_controller.py',
 'executed_preflight.md',
 'executed_policy.json',
 'executed_ROOT_READY.json',
 'reviewed_next_stock_method.md',
 'reviewed_next_stock_method.json',
 'reviewed_independent_method_peer.json',
 'reviewed_ROOT_method.json',
 'protocol.json',
 'run_started.json',
 'interpreter.json',
 'loaded_module_origins.json',
 'active_and_archived_role_graph.json',
 'literal_prior_stock_component_adapters.json',
 'fresh_full_input_union_before_assembly.json',
 'source_first_stock_witness.json',
 'primary_first_stock_components.json',
 'primary_first_stock_squared_L2.json',
 'independent_first_stock_components.json',
 'independent_first_stock_squared_L2.json',
 'independent_primary_proof_check.json',
 'four_fixed_reject_controls.json',
 'qualification_and_remaining_gaps.json',
 'fresh_full_input_union_after_assembly.json',
 'summary.json',
 'completion_outcome.json',
 'manifest.json']
READY_FIELDS = ['G2_transfer',
 'ROOT_finite_planning_acceptance_SHA256',
 'ROOT_finite_planning_acceptance_path',
 'absent_new_code_cache_paths',
 'accepted_method_and_review_expected_SHA256',
 'active_and_archived_finite_role_graph',
 'adoption',
 'author_method_SHA256',
 'cost_comparison',
 'cost_transfer',
 'current_authoring_acceptance_SHA256',
 'current_authoring_acceptance_path',
 'current_static_review_paths',
 'digital_pair_independence',
 'estimator_schedule_emitted',
 'exact_startup_literals',
 'existing_new_code_cache_SHA256',
 'financial_adoption',
 'finite_protocol',
 'first_failure_stop_no_retry_or_partial_success',
 'first_stock_projection_Gaussian_moment_theorem',
 'first_stock_rational_assembly_authorized',
 'fits_or_pilots',
 'fixture_credit',
 'full_E11_completed',
 'full_G2',
 'full_METHOD_JSON_copy_count',
 'full_price_certificate',
 'future_actual_stock_bounds',
 'gate_emission',
 'historical_cache_partitions',
 'historical_first_log_V3_source_has_current_execution_permission',
 'item',
 'local_only',
 'native_arrays_generated_or_replayed',
 'native_financial_path_or_policy_L2_verified',
 'native_reference_toy_array_count',
 'native_source_clipping_inserted',
 'new_global_fixture_credit',
 'new_test_credit',
 'new_transcendental_series',
 'old_numerical_helpers_or_evaluators_called',
 'one_first_stock_squared_L2_only',
 'original_caps',
 'original_cfg_expected',
 'output',
 'physical_certificate',
 'planned_manifest_inclusive_owned_files',
 'planned_owned_filenames',
 'prices_or_paths_sampled',
 'quantum_advantage',
 'ready',
 'root_and_independent_static_reviews_passed',
 'runtime_invocation',
 'schema',
 'selected_original_log_contract',
 'selected_original_stock_site',
 'serializer_expected_source_and_cache_partition',
 'source_contract_canonical_JSON_SHA256',
 'source_emission',
 'source_substitution_authorized',
 'static_review_expected_SHA256',
 'stock_source_45node_closure_canonical_JSON_SHA256',
 'two_literal_profile_adapter_contract',
 'two_profile_adapter_commitments']
POLICY_FIELDS = ['G2_transfer',
 'ROOT_READY',
 'ROOT_READY_schema',
 'ROOT_finite_planning_acceptance_SHA256',
 'ROOT_finite_planning_acceptance_path',
 'accepted_method_and_review_expected_SHA256',
 'active_and_archived_finite_role_graph',
 'adoption',
 'author_SHA256',
 'cost_comparison',
 'cost_transfer',
 'current_authoring_acceptance_SHA256',
 'current_authoring_acceptance_path',
 'current_definition_AST_SHA256',
 'current_static_review_paths',
 'digital_pair_independence',
 'estimator_schedule_emitted',
 'exact_startup_literals',
 'financial_adoption',
 'finite_protocol',
 'first_failure_stop_no_retry_or_partial_success',
 'first_stock_projection_Gaussian_moment_theorem',
 'first_stock_rational_assembly_authorized',
 'fits_or_pilots',
 'fixture_credit',
 'full_E11_completed',
 'full_G2',
 'full_METHOD_JSON_copy_count',
 'full_price_certificate',
 'future_actual_stock_bounds',
 'gate_emission',
 'historical_cache_partitions',
 'historical_first_log_V3_source_has_current_execution_permission',
 'item',
 'local_only',
 'method_SHA256',
 'native_arrays_generated_or_replayed',
 'native_financial_path_or_policy_L2_verified',
 'native_reference_toy_array_count',
 'native_source_clipping_inserted',
 'new_global_fixture_credit',
 'new_test_credit',
 'new_transcendental_series',
 'old_numerical_helpers_or_evaluators_called',
 'one_first_stock_squared_L2_only',
 'original_caps',
 'original_cfg_expected',
 'output',
 'physical_certificate',
 'planned_manifest_inclusive_owned_files',
 'planned_owned_filenames',
 'prices_or_paths_sampled',
 'quantum_advantage',
 'runtime_invocation',
 'schema',
 'selected_original_log_contract',
 'selected_original_stock_site',
 'serializer_expected_source_and_cache_partition',
 'source_contract_canonical_JSON_SHA256',
 'source_emission',
 'source_substitution_authorized',
 'stock_source_45node_closure_canonical_JSON_SHA256',
 'two_literal_profile_adapter_contract',
 'two_profile_adapter_commitments']
HISTORICAL_CACHE_PARTITIONS = {'completed_first_log_V3': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-1.pyc',
                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-2.pyc',
                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.pyc'],
                            'existing_expected_SHA256': {}},
 'completed_native_author': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc',
                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-2.pyc',
                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.pyc'],
                             'existing_expected_SHA256': {}},
 'completed_scalar_V2': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc',
                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc',
                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc'],
                         'existing_expected_SHA256': {}},
 'failed_first_stock_V1': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.opt-1.pyc',
                                            'research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.opt-2.pyc',
                                            'research/limitation_program_20261001/__pycache__/experiment_e11_first_stock_squared_l2_v1.cpython-312.pyc'],
                           'existing_expected_SHA256': {}},
 'failed_scalar_V1': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc',
                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc',
                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'],
                      'existing_expected_SHA256': {}}}
HISTORICAL_SOURCE_PATHS = {'completed_first_log_V3': 'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v3.py',
 'completed_native_author': 'research/limitation_program_20261001/experiment_e11_native_coordinate_squared_l2_v1.py',
 'completed_scalar_V2': 'research/limitation_program_20261001/experiment_e11_scalar_midpoint_l2_v2.py',
 'failed_first_stock_V1': 'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v1.py',
 'failed_scalar_V1': 'research/limitation_program_20261001/experiment_e11_scalar_midpoint_l2_v1.py'}
SERIALIZATION_RUNTIME = {'absent_three_variant_cache_paths': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.pyc',
                                      'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-1.pyc',
                                      'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-2.pyc'],
 'existing_cache_expected_SHA256': {},
 'import_before_initial_runtime_and_loaded_origin_admission': True,
 'module': '_pylong',
 'postadmission_origin_or_cache_discovery_authorized': False,
 'scientific_arithmetic_or_representation_policy_change': False,
 'source_SHA256': 'bcae0d4cc2d4d3fd9b40bb06b512eb8dd785f755edd1f9038613d4460ca4c6c1',
 'source_path': 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\_pylong.py'}
FAILED_E11_V1_HISTORY = {'ROOT_READY_SHA256': '855f25478139081cccaa804fc5a889fe4dcbdeeffed39e3d1f234ac365a3c6c9',
 'ROOT_READY_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run001.json',
 'ROOT_freeze_SHA256': 'c50342018999b1338a9ecc8ab5e6128a110b8d1076c5ce3021a6dac93e60dea6',
 'ROOT_freeze_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_FAILED_UNSEALED_ROOT_FREEZE_run001.json',
 'author_method_SHA256': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b',
                          'e11_scalar_midpoint_l2_numerical_preflight_v1.json': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27',
                          'experiment_e11_scalar_midpoint_l2_v1.py': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6'},
 'cache_partition': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc',
                                      'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc',
                                      'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'],
                     'existing_expected_SHA256': {}},
 'complete_failed_owned_inventory': {'FAILED_UNSEALED.json': {'SHA256': '06220039aa4d77b9fd8ad352a17240ffa874a7a36fff96188ee592e816139f43',
                                                              'bytes': 160},
                                     'all30_primary_and_independent_bin_records.json': {'SHA256': '7a90fc82caedf10db30e64236bf3639c48dd330b0bd202464ec249ac3f244bc8',
                                                                                        'bytes': 1029646},
                                     'all_bin_sum_and_telescoping_comparisons.json': {'SHA256': 'd2a07815a797522bdf45e020054d1c2948f2017caffeaa3b6c30133b05571a77',
                                                                                      'bytes': 121843},
                                     'complete_historical_owner_maps_and_inventories.json': {'SHA256': '38082221aefea36cf230fde4a5302734131f01452aa3e8db5c60133584cdebce',
                                                                                             'bytes': 1140113},
                                     'exact_real_analytic_proof_and_scope.json': {'SHA256': '229b26f1c68d6ba9e6bdb917c31fef3ed096a5861103b6029d9fe8539d5959ac',
                                                                                  'bytes': 3370},
                                     'executed_E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': {'SHA256': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b',
                                                                                                   'bytes': 15449},
                                     'executed_E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run001.json': {'SHA256': '855f25478139081cccaa804fc5a889fe4dcbdeeffed39e3d1f234ac365a3c6c9',
                                                                                                          'bytes': 569265},
                                     'executed_e11_scalar_midpoint_l2_numerical_preflight_v1.json': {'SHA256': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27',
                                                                                                     'bytes': 567832},
                                     'executed_experiment_e11_scalar_midpoint_l2_v1.py': {'SHA256': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6',
                                                                                          'bytes': 1654285},
                                     'failure.json': {'SHA256': 'a8547fb69b52d4e6158fcbafc84c87cca21986f156215cd94a22421625f44099',
                                                      'bytes': 1880},
                                     'fixed_canonical_argument_corpus.json': {'SHA256': '98c8d4d3494d7e03f4a1e21407d5ebd408ffd7573887fd91daead5fc8ea91a64',
                                                                              'bytes': 13441},
                                     'fresh_input_union_before_scalar_numerics.json': {'SHA256': '6c72160c0ec959d64505ea9e094f81a637e15389816b0f6d18047dd835e83016',
                                                                                       'bytes': 8522},
                                     'independent_log_endpoint_ledger.json': {'SHA256': '6269a7bb56b776dd782ad4e417162a54f66314899497d8476cd585db058b02f6',
                                                                              'bytes': 500884},
                                     'independent_production_squared_L2_allowance.json': {'SHA256': 'e6058f8f4ac815c3a908f9fbf8d99b69dd126cb7febd4cf211ab2812aa774cc8',
                                                                                          'bytes': 5442},
                                     'primary_log_endpoint_ledger.json': {'SHA256': 'dfbfd35ec2de6922af4f86df34817b91aece77554f30428396c9040cd1471223',
                                                                          'bytes': 312396},
                                     'primary_production_squared_L2_allowance.json': {'SHA256': 'afa1c0313c1dc63ea0a3a52a0442c5897b57660a2d069a773254eb714fdc0af1',
                                                                                      'bytes': 4316},
                                     'protocol.json': {'SHA256': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27',
                                                       'bytes': 567832},
                                     'run_started.json': {'SHA256': '522093ef710d65913cdf1bf38f967c57c583f04af4125b7e2f8b0ae41992d40e',
                                                          'bytes': 903},
                                     'three_precise_negative_diagnostic_controls.json': {'SHA256': '0885318fc20876378c982a9b6af4a3d53b30bebeb216611aa4198a4b45a2f654',
                                                                                         'bytes': 5237}},
 'failed_not_scientific_certificate_or_new_owner': True,
 'manifest_and_summary_and_second_union_absent': ['manifest.json',
                                                  'summary.json',
                                                  'fresh_input_union_after_scalar_numerics.json'],
 'output': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run001',
 'static_review_expected_SHA256': {'.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_AUTHOR_STATIC_QA_run001.json': '695cadc7fb64708bdd43bda53221299ff7c07c34474e866e6c8232b3d8623f55',
                                   '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_INDEPENDENT_STATIC_PEER_next_run001.json': 'eb3e0c49cdcb19f2c4d5cf8f8a927caa6078c5dc92c344534091e8435a3bf4de',
                                   '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_STATIC_REVIEW_run001.json': 'ca768374525412a7ffe3ee82e358ade56d98613d0599eb217b58dd65d52ad2d1'}}
HISTORICAL_READY_PATHS = {'completed_first_log_V3': '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_READY_run001.json',
 'completed_native_author': '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json',
 'completed_scalar_V2': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run002.json',
 'failed_first_stock_V1': '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json'}
HELD_HISTORY_EXPECTED = {'.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_TRIO_METADATA_CREATION_run001.json': 'c80033b92992b86c9e61805f5d8fca0741a650b705075a417891dc7aaa22e31d',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_TRIO_METADATA_CREATION_run002.json': '06655978c4797aa3732892720200383264ec40294cf7583528961695290f62cd',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_HELD_AUTHOR_STATIC_QA_run001.json': '02fd0372f1bcd6a3b03612c3d947f536e6bcc5d6935421bac6763cc66aa8b513',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_INDEPENDENT_STATIC_HOLD_HISTORY_run001.json': 'db76ea24ba05d410fc4406b4cdc1a7a0a71cfdaec56750dd1ef20150f519f00f',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V2_HELD_AUTHOR_STATIC_QA_run001.json': '1ee84df22f3f0626d6eeb455f3607632e0c378cb3268ba0af08fd6a7e9b3f5f8',
 '.context/E11_first_log_controller_body_v1_draft.txt': 'e071e8de267a380a2b9e4a24eca970b11e291f8ceed4e9274b1335f72e163788',
 '.context/E11_first_log_preflight_v1_draft.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
 '.context/author_E11_first_log_controller_trio_v1_run001.py': 'e8f47a1126b2dd4cf26e5265c7eceb6a1055cef182afcfd4498c24fdaffab24c',
 '.context/author_E11_first_log_controller_trio_v2_run001.py': '58437094363e2bbe0c56bb76c0b2276c1e039118ed51a7fd33b842d8d072b21c',
 '.context/freeze_E11_first_log_V2_author_HOLD_static_QA_run001.py': '307dae354fa8435b87bc28ee8a5e4a17cae5e806813a1b13b344c5854d158136',
 '.context/freeze_E11_first_log_V2_author_static_QA_run001.py': 'f3d99f596b09440359190435e485ba22523cb27ddf4da2099cdb72012c8e74a9',
 'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V1.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
 'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V2.md': '312a6648091a041226a1f44a014a9fcf33944d291d83d7af8e69dacdcb4a8c50',
 'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v1.json': 'f97bbafe661aed9b3f4e1f59cedc352774c5dbc2be046066581662232716670b',
 'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v2.json': 'c7d0482eff611734755396b1fef9801f9c62a479f3041690b2f8f79f271e30bb',
 'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v1.py': '68ce90a9801d7395b110af4c20021ae9c8d7b707aad2f35f4bd7ae77408ce4c4',
 'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v2.py': '0b9b213a927c9b002fc3e69b1fce53a64bb6b5e1d169535ac4a5b1a2f031cfa2'}
POSITIVE_SCOPE = {'M': 256,
 'asset_zero_based': 0,
 'case': 'B4x12',
 'clipped_log': 3579,
 'contractual_date_one_based': 1,
 'even_moment_order': 32,
 'extra_spot_multiplier': 1,
 'independent130_alpha_from_profile': 'independent130',
 'initial_ln100_already_in_log': True,
 'lower_tail_paid': True,
 'moment_half_order': 16,
 'native_pair_independence_assumed': False,
 'primary90_e0_from_profile': 'primary90',
 'raw_log': 3542,
 'saved_date_zero_based': 0,
 'stock': 4021,
 'units': 'dollars_squared',
 'upper_tail_paid': True}
CONTROL_SPECS = [{'category': 'exact_first_stock_source_scope',
  'dedicated_reject_code': 'E11_FIRST_STOCK_SOURCE_SCOPE',
  'fixed_bad_metadata_variants': [{'stock': 4022},
                                  {'raw_log': 3543},
                                  {'asset_zero_based': 1},
                                  {'contractual_date_one_based': 2}]},
 {'category': 'units_and_initial_spot_once',
  'dedicated_reject_code': 'E11_FIRST_STOCK_UNITS_SPOT',
  'fixed_bad_metadata_variants': [{'units': 'dimensionless_squared'},
                                  {'extra_spot_multiplier': 100},
                                  {'initial_ln100_already_in_log': False}]},
 {'category': 'fixed_unconditional_tail_proof',
  'dedicated_reject_code': 'E11_FIRST_STOCK_TAIL_PROOF',
  'fixed_bad_metadata_variants': [{'moment_half_order': 15},
                                  {'lower_tail_paid': False},
                                  {'upper_tail_paid': False},
                                  {'native_pair_independence_assumed': True}]},
 {'category': 'uncombined_own_profile_authority',
  'dedicated_reject_code': 'E11_FIRST_STOCK_PROFILE_AUTHORITY',
  'fixed_bad_metadata_variants': [{'primary90_e0_from_profile': 'independent130'},
                                  {'independent130_alpha_from_profile': 'primary90'}]}]
CFG_EXPECTED = {'bytes_cap': 8388608,
 'expected_SHA256': 'aaeeb031a76b70ae1ac53b6557056f554273db4b313678c36c7ccd2c483e7e37',
 'path': '.context/frontier_t0_env/pyvenv.cfg'}
RUNTIME_EXTERNAL_MAP_SHA256 = 'd68ae51a74eb7da5ba68308626a630dbf5860135ee22a0e5f1677e34d5cd7bfa'
NATIVE_SNAPSHOT_COMMITMENT = '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476'
STOCK_NODE_CLOSURE_SHA256 = 'a284d0fa82eee4c8f40e7de2cadd9f2867b122d9bf24e604c3e90e55f68edbf1'
STOCK_ENVELOPE_CASE_SHA256 = {'independent130': '675b0822ac868d39c255c3b4730079cfd4aeeb45356d92e2b10407cbfd8c7e8c',
 'primary90': '40c582bdef1cb16b1e20a68d7273b43f8c5c33f02fcc4af37f8ae4696678230e'}
CACHE_METHOD_KEY = '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.json'
CACHE_METHOD_AUTHORITY = {'.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_AUTHOR_METADATA_QA_run001.json': 'e7d066531ca347962c4c4abd65eb3ddb4934185ddb8a6c2ded0784af317b4d75',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_INDEPENDENT_METHOD_PEER_run001.json': 'c6b1e4a55f0188816b31fbdda2a0c304efe4be94ecd832fe9c562c29df6d504e',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.json': '6f477c915777cd4ba42874bc39bbee4c1ff19410315a104504ac82a10bb57618',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_PROSPECTUS_run001.md': '870c1f677b36375a5dfee6cc9b86b687c3637480651cc0bf30e5d60048e49688',
 '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_ROOT_METHOD_REVIEW_run001.json': 'f20164bc132655af205216d32863e160c62eef33022221a3f2747ec0b5439080'}
CURRENT_V2_ROUTES = {'AUTHOR_QA': '.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run002.json',
 'MD': 'research/limitation_program_20261001/E11_FIRST_STOCK_SQUARED_L2_PREFLIGHT_V2.md',
 'OUTPUT': 'results/limitation_program_20261001/E11_first_stock_squared_L2_run001',
 'READY': '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run002.json',
 'ROOT_METHOD_review': '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_ROOT_METHOD_REVIEW_run001.json',
 'ROOT_controller_authoring_acceptance': '.context/E11_FIRST_STOCK_V2_ADMISSION_CACHE_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json',
 'ROOT_source_review': '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run002.json',
 'independent_METHOD_peer': '.context/E11_FIRST_STOCK_V2_ADMISSION_EXPECTED_HASH_CACHE_METHOD_INDEPENDENT_METHOD_PEER_run001.json',
 'independent_source_peer': '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run002.json',
 'policy': 'research/limitation_program_20261001/e11_first_stock_squared_l2_preflight_v2.json',
 'source': 'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v2.py'}
ORIGINAL_V1_FIXED_SHARED = {'ROOT_finite_planning_acceptance_SHA256': '230dba7471b50ec3172c44ee08e087a665d7032ecbcf6deb52d22ee39f4b1aa2',
 'ROOT_finite_planning_acceptance_path': '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_FINITE_ADMISSION_AUTHORING_ACCEPTANCE_run001.json',
 'active_and_archived_finite_role_graph': {'active10': ['A01_run011',
                                                        'A02_BM_native_financial_bridge_audit_run002',
                                                        'A02_BM_native_financial_bridge_root_verification_run001',
                                                        'A02_BM_native_financial_bridge_run002',
                                                        'A10_coefficient_run001',
                                                        'C06_pair_audit_run001',
                                                        'C06_pair_run001',
                                                        'E11_scalar_midpoint_L2_numerical_run002',
                                                        'E11_native_coordinate_squared_L2_run001',
                                                        'E11_first_log_prefix_squared_L2_run001'],
                                           'all18_snapshot_canonical_JSON_SHA256': {'A01_run011': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                                    'A01_run014': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                                    'A02_BM_native_financial_bridge_audit_run002': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                    'A02_BM_native_financial_bridge_root_verification_run001': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                    'A02_BM_native_financial_bridge_run002': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                    'A02_quantile_financial_audit_run001': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                    'A02_quantile_law_audit_run001': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                    'A10_coefficient_run001': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                    'C06_pair_audit_run001': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                                    'C06_pair_run001': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                                    'C07_barrier_audit_run001': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                    'C07_barrier_run001': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                                    'C07_barrier_run002': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                                    'C07_bound_date1_run001': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                    'E10_continuous_moment_only_run002': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                    'E11_first_log_prefix_squared_L2_run001': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                                                                    'E11_native_coordinate_squared_L2_run001': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                    'E11_scalar_midpoint_L2_numerical_run002': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c'},
                                           'all18_snapshot_dicts_not18_runtime_success_permissions': True,
                                           'all_archive_nested_runtime_maps_preserved_not_admitted_as_current_runtime': True,
                                           'archive8': ['A01_run014',
                                                        'A02_quantile_financial_audit_run001',
                                                        'A02_quantile_law_audit_run001',
                                                        'E10_continuous_moment_only_run002',
                                                        'C07_barrier_audit_run001',
                                                        'C07_barrier_run001',
                                                        'C07_barrier_run002',
                                                        'C07_bound_date1_run001'],
                                           'completed_first_log_new_owner_only_after_ROOT_verification': True,
                                           'full_snapshot_authority': {'JSON_pointer': ['complete_original_cited_owner_snapshots'],
                                                                       'expected_SHA256': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
                                                                       'path': '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json'},
                                           'original17_objects_unchanged': True,
                                           'original_raw_missing_None_and_A10_bare_keys_external_owned_layouts_unchanged': True,
                                           'owner_summaries': {'A01_run011': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                              'literal_expected_manifest_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03',
                                                                              'manifest_path': 'results/limitation_program_20261001/A01_run011/manifest.json',
                                                                              'owned_bytes': 8745921,
                                                                              'owned_files': 13,
                                                                              'role': 'inherited '
                                                                                      'active '
                                                                                      'original '
                                                                                      'proof/custody'},
                                                               'A01_run014': {'full_original_snapshot_canonical_JSON_SHA256': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                              'literal_expected_manifest_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8',
                                                                              'manifest_path': 'results/limitation_program_20261001/A01_run014/manifest.json',
                                                                              'owned_bytes': 37429139,
                                                                              'owned_files': 16,
                                                                              'role': 'unchanged '
                                                                                      'archived '
                                                                                      'opaque '
                                                                                      'custody/citation '
                                                                                      'only'},
                                                               'A02_BM_native_financial_bridge_audit_run002': {'full_original_snapshot_canonical_JSON_SHA256': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                                               'literal_expected_manifest_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0',
                                                                                                               'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/manifest.json',
                                                                                                               'owned_bytes': 44651234,
                                                                                                               'owned_files': 24,
                                                                                                               'role': 'inherited '
                                                                                                                       'active '
                                                                                                                       'original '
                                                                                                                       'proof/custody'},
                                                               'A02_BM_native_financial_bridge_root_verification_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                                                           'literal_expected_manifest_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab',
                                                                                                                           'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_root_verification_run001/manifest.json',
                                                                                                                           'owned_bytes': 579999,
                                                                                                                           'owned_files': 3,
                                                                                                                           'role': 'inherited '
                                                                                                                                   'active '
                                                                                                                                   'original '
                                                                                                                                   'proof/custody'},
                                                               'A02_BM_native_financial_bridge_run002': {'full_original_snapshot_canonical_JSON_SHA256': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                                         'literal_expected_manifest_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162',
                                                                                                         'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/manifest.json',
                                                                                                         'owned_bytes': 113209386,
                                                                                                         'owned_files': 29,
                                                                                                         'role': 'inherited '
                                                                                                                 'active '
                                                                                                                 'original '
                                                                                                                 'proof/custody'},
                                                               'A02_quantile_financial_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                                       'literal_expected_manifest_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323',
                                                                                                       'manifest_path': 'results/limitation_program_20261001/A02_quantile_financial_audit_run001/manifest.json',
                                                                                                       'owned_bytes': 1107202,
                                                                                                       'owned_files': 9,
                                                                                                       'role': 'unchanged '
                                                                                                               'archived '
                                                                                                               'opaque '
                                                                                                               'custody/citation '
                                                                                                               'only'},
                                                               'A02_quantile_law_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                                 'literal_expected_manifest_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572',
                                                                                                 'manifest_path': 'results/limitation_program_20261001/A02_quantile_law_audit_run001/manifest.json',
                                                                                                 'owned_bytes': 379157,
                                                                                                 'owned_files': 8,
                                                                                                 'role': 'unchanged '
                                                                                                         'archived '
                                                                                                         'opaque '
                                                                                                         'custody/citation '
                                                                                                         'only'},
                                                               'A10_coefficient_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                          'literal_expected_manifest_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40',
                                                                                          'manifest_path': 'results/limitation_program_20261001/A10_coefficient_run001/manifest.json',
                                                                                          'owned_bytes': 107197203,
                                                                                          'owned_files': 557,
                                                                                          'role': 'inherited '
                                                                                                  'active '
                                                                                                  'original '
                                                                                                  'proof/custody'},
                                                               'C06_pair_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                                         'literal_expected_manifest_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14',
                                                                                         'manifest_path': 'results/limitation_program_20261001/C06_pair_audit_run001/manifest.json',
                                                                                         'owned_bytes': 1109330,
                                                                                         'owned_files': 11,
                                                                                         'role': 'inherited '
                                                                                                 'active '
                                                                                                 'original '
                                                                                                 'proof/custody'},
                                                               'C06_pair_run001': {'full_original_snapshot_canonical_JSON_SHA256': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                                   'literal_expected_manifest_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a',
                                                                                   'manifest_path': 'results/limitation_program_20261001/C06_pair_run001/manifest.json',
                                                                                   'owned_bytes': 738350,
                                                                                   'owned_files': 11,
                                                                                   'role': 'inherited '
                                                                                           'active '
                                                                                           'original '
                                                                                           'proof/custody'},
                                                               'C07_barrier_audit_run001': {'full_original_snapshot_canonical_JSON_SHA256': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                            'literal_expected_manifest_SHA256': '29fe018792317eef189a9e6ceae00bf80c13b81fafd89ef0f4c3f48933dd98c9',
                                                                                            'manifest_path': 'results/limitation_program_20261001/C07_barrier_audit_run001/manifest.json',
                                                                                            'owned_bytes': 51656,
                                                                                            'owned_files': 11,
                                                                                            'role': 'unchanged '
                                                                                                    'archived '
                                                                                                    'opaque '
                                                                                                    'custody/citation '
                                                                                                    'only'},
                                                               'C07_barrier_run001': {'full_original_snapshot_canonical_JSON_SHA256': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                                      'literal_expected_manifest_SHA256': 'e30e10549a76d2baa07d44429badaf8e69f85b10041478def0f673b228c3a7b9',
                                                                                      'manifest_path': 'results/limitation_program_20261001/C07_barrier_run001/manifest.json',
                                                                                      'owned_bytes': 64258,
                                                                                      'owned_files': 9,
                                                                                      'role': 'unchanged '
                                                                                              'archived '
                                                                                              'opaque '
                                                                                              'custody/citation '
                                                                                              'only'},
                                                               'C07_barrier_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                                      'literal_expected_manifest_SHA256': '3ce81f47db7fcd054d33a7391fb4600303f1f8afac545367c473172e740b6c9b',
                                                                                      'manifest_path': 'results/limitation_program_20261001/C07_barrier_run002/manifest.json',
                                                                                      'owned_bytes': 75701,
                                                                                      'owned_files': 11,
                                                                                      'role': 'unchanged '
                                                                                              'archived '
                                                                                              'opaque '
                                                                                              'custody/citation '
                                                                                              'only'},
                                                               'C07_bound_date1_run001': {'full_original_snapshot_canonical_JSON_SHA256': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                          'literal_expected_manifest_SHA256': '9f7e676d7b7eb1c14b8ae8815b756da4491b50530fbdf9722b9861712de60dd6',
                                                                                          'manifest_path': 'results/limitation_program_20261001/C07_bound_date1_run001/manifest.json',
                                                                                          'owned_bytes': 126462,
                                                                                          'owned_files': 15,
                                                                                          'role': 'unchanged '
                                                                                                  'archived '
                                                                                                  'opaque '
                                                                                                  'custody/citation '
                                                                                                  'only'},
                                                               'E10_continuous_moment_only_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                                     'literal_expected_manifest_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668',
                                                                                                     'manifest_path': 'results/limitation_program_20261001/E10_continuous_moment_only_run002/manifest.json',
                                                                                                     'owned_bytes': 7876736,
                                                                                                     'owned_files': 18,
                                                                                                     'role': 'unchanged '
                                                                                                             'archived '
                                                                                                             'opaque '
                                                                                                             'custody/citation '
                                                                                                             'only'},
                                                               'E11_first_log_prefix_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '65231e645a8789bc96a615ef06713a6f7ec345ac0274687e8d8eb9554a608f55',
                                                                                                          'literal_expected_manifest_SHA256': '165ff337315efeca8a658b1db46b172178598150f2c6b760a45bf22233f1a600',
                                                                                                          'manifest_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/manifest.json',
                                                                                                          'owned_bytes': 35880313,
                                                                                                          'owned_files': 27,
                                                                                                          'role': 'new '
                                                                                                                  'active '
                                                                                                                  'scoped '
                                                                                                                  'completed '
                                                                                                                  'first-log '
                                                                                                                  'numerical '
                                                                                                                  'input '
                                                                                                                  'only'},
                                                               'E11_native_coordinate_squared_L2_run001': {'full_original_snapshot_canonical_JSON_SHA256': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                                           'literal_expected_manifest_SHA256': 'bb1f08a600712e34d1fa4b3c77f0ea04147c5368c8f92dc4f9a21ed3e293df95',
                                                                                                           'manifest_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/manifest.json',
                                                                                                           'owned_bytes': 68640627,
                                                                                                           'owned_files': 47,
                                                                                                           'role': 'inherited '
                                                                                                                   'active '
                                                                                                                   'original '
                                                                                                                   'proof/custody'},
                                                               'E11_scalar_midpoint_L2_numerical_run002': {'full_original_snapshot_canonical_JSON_SHA256': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c',
                                                                                                           'literal_expected_manifest_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170',
                                                                                                           'manifest_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/manifest.json',
                                                                                                           'owned_bytes': 7729234,
                                                                                                           'owned_files': 20,
                                                                                                           'role': 'inherited '
                                                                                                                   'active '
                                                                                                                   'original '
                                                                                                                   'proof/custody'}},
                                           'three_original_equal_SHA_archive_aliases': [{'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6',
                                                                                         'original_key': 'research/controlled_source_completion/nonrestoring_sqrt.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/nonrestoring_sqrt.py'},
                                                                                        {'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b',
                                                                                         'original_key': 'research/journal_sprint/reversible_fixed_point.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible_fixed_point.py'},
                                                                                        {'current_original_path_integrity_asserted': False,
                                                                                         'expected_hash_waived': False,
                                                                                         'expected_sha256': '5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a',
                                                                                         'original_key': 'research/antithetic_feasibility/reversible.py',
                                                                                         'original_map': 'frozen_inputs',
                                                                                         'original_owner': 'A01_run011',
                                                                                         'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}]},
 'current_static_review_paths': ['.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run001.json',
                                 '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json',
                                 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json'],
 'exact_startup_literals': {'PYTHONOPTIMIZE_and_integer_digit_override_absent_not_cleared': True,
                            'Python_version': [3, 12, 4],
                            'authority': 'Exact already admitted native '
                                         'invocation_check/runtime_scopes and '
                                         'literal ROOT/BASE/LAUNCHER '
                                         'assignments, not observed current '
                                         'runtime discovery.',
                            'base_executable': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python.exe',
                            'base_executable_SHA256': 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b',
                            'base_prefix_and_no_site_prefix': 'C:/Users/prith/AppData/Local/Programs/Python/Python312',
                            'declared_absent_standard_zip': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/python312.zip',
                            'default_decimal_digits': 4300,
                            'exact_launch_flags': ['-I', '-S', '-B'],
                            'launcher': 'C:/Users/prith/quantum_option_pricing/.context/frontier_t0_env/Scripts/python.exe',
                            'launcher_SHA256': '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5',
                            'lexical_and_physical_excluded_site_path': 'C:/Users/prith/AppData/Local/Programs/Python/Python312/Lib/site-packages',
                            'one_post_origin_decimal_serializer_limit': 20000,
                            'optimization': 0,
                            'ordered_exact_sys_path': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\DLLs',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib',
                                                       'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312'],
                            'workspace_cwd': 'C:/Users/prith/quantum_option_pricing'},
 'finite_protocol': {'control_categories': 4,
                     'control_evaluation_now': False,
                     'control_metadata_variants': 13,
                     'fixed_M': 256,
                     'fixed_even_Gaussian_moment_order': 32,
                     'four_positive_first_fixed_reject_control_categories': [{'category': 'exact_first_stock_source_scope',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_SOURCE_SCOPE',
                                                                              'fixed_bad_metadata_variants': [{'stock': 4022},
                                                                                                              {'raw_log': 3543},
                                                                                                              {'asset_zero_based': 1},
                                                                                                              {'contractual_date_one_based': 2}]},
                                                                             {'category': 'units_and_initial_spot_once',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_UNITS_SPOT',
                                                                              'fixed_bad_metadata_variants': [{'units': 'dimensionless_squared'},
                                                                                                              {'extra_spot_multiplier': 100},
                                                                                                              {'initial_ln100_already_in_log': False}]},
                                                                             {'category': 'fixed_unconditional_tail_proof',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_TAIL_PROOF',
                                                                              'fixed_bad_metadata_variants': [{'moment_half_order': 15},
                                                                                                              {'lower_tail_paid': False},
                                                                                                              {'upper_tail_paid': False},
                                                                                                              {'native_pair_independence_assumed': True}]},
                                                                             {'category': 'uncombined_own_profile_authority',
                                                                              'dedicated_reject_code': 'E11_FIRST_STOCK_PROFILE_AUTHORITY',
                                                                              'fixed_bad_metadata_variants': [{'primary90_e0_from_profile': 'independent130'},
                                                                                                              {'independent130_alpha_from_profile': 'primary90'}]}],
                     'new_exp_CDF_series_precision_passes': 0,
                     'new_moment_or_precision_or_threshold_search': False,
                     'numerical_fixture_or_new_global_test_credit': 0,
                     'profile_numerical_guards_each': ['b_le_8_times_saved_ln2_lower',
                                                       'mu_lower_minus_a_strict_positive',
                                                       'b_minus_mu_upper_minus_2v_strict_positive'],
                     'profiles': ['primary90', 'independent130'],
                     'reconciliation': 'Check existing primary rational '
                                       'identities with a distinct expanded '
                                       'order, no third stock bound returned',
                     'returned_prospective_stock_bounds': 2,
                     'source_native_projection_interval_choice': 'Exactly '
                                                                 'inherited '
                                                                 'selected raw '
                                                                 'prefix '
                                                                 'interval, no '
                                                                 'fit or '
                                                                 'adaptive '
                                                                 'cutoff',
                     'unrelated_IO_KeyError_budget_or_assertion_rejection_credit': False},
 'first_failure_stop_no_retry_or_partial_success': True,
 'first_stock_projection_Gaussian_moment_theorem': {'C16_unevaluated_exact_product_factors': [1,
                                                                                              3,
                                                                                              5,
                                                                                              7,
                                                                                              9,
                                                                                              11,
                                                                                              13,
                                                                                              15,
                                                                                              17,
                                                                                              19,
                                                                                              21,
                                                                                              23,
                                                                                              25,
                                                                                              27,
                                                                                              29,
                                                                                              31],
                                                    'Gaussian_moment_identity': 'For '
                                                                                'a '
                                                                                'centered '
                                                                                'continuous '
                                                                                'N(0,v), '
                                                                                'E '
                                                                                'W^32=(31)!!*v^16=C16*v^16, '
                                                                                'by '
                                                                                'Gaussian '
                                                                                'integration-by-parts '
                                                                                'recurrence; '
                                                                                'no '
                                                                                'moment '
                                                                                'of '
                                                                                'digital '
                                                                                'coordinates '
                                                                                'is '
                                                                                'used.',
                                                    'M_fixed': 256,
                                                    'M_guard_unevaluated': 'b '
                                                                           '<= '
                                                                           '8*own_saved_ln2_lower '
                                                                           'implies '
                                                                           'exp(b)<=2^8=M',
                                                    'Q': 1099511627776,
                                                    'continuous_exponential_tilt_identity': 'E[exp(2L)1{L>b}]=exp(2mu+2v)*P(N(mu+2v,v)>b); '
                                                                                            'complete '
                                                                                            'square '
                                                                                            'in '
                                                                                            'the '
                                                                                            'unconditional '
                                                                                            'continuous '
                                                                                            'Gaussian '
                                                                                            'density.',
                                                    'continuous_normal_law': 'Only '
                                                                             'original '
                                                                             'continuous '
                                                                             'ideal '
                                                                             'Z0,Z1 '
                                                                             'are '
                                                                             'independent '
                                                                             'standard '
                                                                             'normals. '
                                                                             'Native '
                                                                             'shared '
                                                                             'finite '
                                                                             'pair '
                                                                             'is '
                                                                             'never '
                                                                             'assumed '
                                                                             'independent. '
                                                                             'L '
                                                                             'has '
                                                                             'mean '
                                                                             'mu=ln100-1/800 '
                                                                             'and '
                                                                             'variance '
                                                                             'v=3/400.',
                                                    'core_projection_bound': 'P '
                                                                             'fixes '
                                                                             'L_N '
                                                                             'because '
                                                                             'all '
                                                                             'native '
                                                                             'L_N '
                                                                             'belong '
                                                                             'to '
                                                                             '[a,b]; '
                                                                             '|L_N-P(L)|<=|L_N-L|. '
                                                                             'On '
                                                                             '[a,b], '
                                                                             'exp '
                                                                             'is '
                                                                             'M-Lipschitz.',
                                                    'd_lower_unevaluated': 'mu_lower-a',
                                                    'd_upper_tilted_unevaluated': 'b-mu_upper-2*v',
                                                    'even_moment_order': 32,
                                                    'exact_tilt_mass': 'exp(2mu+2v)=10000*exp(1/80)<=10000*80/79, '
                                                                       'using '
                                                                       'exp(x)<=1/(1-x) '
                                                                       'for '
                                                                       '0<=x<1; '
                                                                       'analytic '
                                                                       'inequality '
                                                                       'only, '
                                                                       'no '
                                                                       'series '
                                                                       'evaluated.',
                                                    'exactly_two_own_profile_bounds': 'Evaluate '
                                                                                      'this '
                                                                                      'rational '
                                                                                      'formula '
                                                                                      'once '
                                                                                      'using '
                                                                                      'primary90 '
                                                                                      'original '
                                                                                      'inputs '
                                                                                      'and '
                                                                                      'once '
                                                                                      'using '
                                                                                      'independent130 '
                                                                                      'own '
                                                                                      'original '
                                                                                      'inputs; '
                                                                                      'do '
                                                                                      'not '
                                                                                      'select '
                                                                                      'a '
                                                                                      'minimum, '
                                                                                      'require '
                                                                                      'nesting, '
                                                                                      'mix '
                                                                                      'adapters, '
                                                                                      'or '
                                                                                      'return '
                                                                                      'a '
                                                                                      'third '
                                                                                      'candidate.',
                                                    'ideal_reference': 'L=ln100-1/800+sqrt(3/1000)Z0+sqrt(9/2000)Z1; '
                                                                       'S=exp(L)',
                                                    'interval_authority_JSON_pointer': ['cases',
                                                                                        'B4x12',
                                                                                        'prefixes',
                                                                                        0,
                                                                                        'actual_raw_log_bounds',
                                                                                        0],
                                                    'interval_authority_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                    'interval_authority_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
                                                    'lower_projection_tail_pointwise': 'On '
                                                                                       'L<a, '
                                                                                       '0<=exp(a)-exp(L)<=exp(a)<=M; '
                                                                                       'lower '
                                                                                       'squared-tail '
                                                                                       'contribution '
                                                                                       '<=M^2*P(L<a).',
                                                    'lower_tail_bound_unevaluated': 'T_lower=M^2*C16*v^16/(mu_lower-a)^32',
                                                    'moment_half_order': 16,
                                                    'mu_lower_unevaluated': '5063438167381/Q '
                                                                            '- '
                                                                            'e0 '
                                                                            '- '
                                                                            '1/800',
                                                    'mu_upper_unevaluated': '5063438167381/Q '
                                                                            '+ '
                                                                            'e0 '
                                                                            '- '
                                                                            '1/800',
                                                    'native_all_input_interval_raw': [4155861047200,
                                                                                      5968266508490],
                                                    'native_clip_inactive_for_all_inputs_at_this_site_only': True,
                                                    'native_exponential_allowance_unevaluated': 'A=alpha*M+beta '
                                                                                                'from '
                                                                                                'original '
                                                                                                'full-clipped-domain '
                                                                                                'absolute '
                                                                                                'envelope '
                                                                                                '|S_N-exp(L_N)|<=alpha*exp(L_N)+beta; '
                                                                                                'original '
                                                                                                'clip '
                                                                                                'inactive '
                                                                                                'at '
                                                                                                'site',
                                                    'native_initial_log_literal_raw': 5063438167381,
                                                    'new_numerical_moments_products_tail_allowances_bounds': None,
                                                    'new_proof_guard_values': None,
                                                    'pointwise_three_term_proof': '|S_N-exp(L)|<=A+M*|L_N-L|+|exp(P(L))-exp(L)|; '
                                                                                  'square '
                                                                                  'with '
                                                                                  'pointwise '
                                                                                  'Cauchy '
                                                                                  'for '
                                                                                  'three '
                                                                                  'terms, '
                                                                                  'then '
                                                                                  'take '
                                                                                  'expectation.',
                                                    'projection': 'P(x)=min(max(x,a),b), '
                                                                  'a=raw_lower/Q, '
                                                                  'b=raw_upper/Q; '
                                                                  'mathematical '
                                                                  'comparison '
                                                                  'only, no '
                                                                  'source/policy '
                                                                  'change',
                                                    'prospective_stock_squared_L2_formula': 'B_stock=3*((alpha*M+beta)^2+M^2*B_log+T_lower+T_upper)',
                                                    'selected_scope': {'asset_zero_based': 0,
                                                                       'case': 'B4x12',
                                                                       'clipped_log': 3579,
                                                                       'contractual_date_one_based': 1,
                                                                       'raw_log': 3542,
                                                                       'saved_date_zero_based': 0,
                                                                       'stock': 4021,
                                                                       'units': 'dollars_squared'},
                                                    'upper_projection_tail_pointwise': 'On '
                                                                                       'L>b, '
                                                                                       '0<=exp(L)-exp(b)<=exp(L); '
                                                                                       'upper '
                                                                                       'squared-tail '
                                                                                       'contribution '
                                                                                       '<=E '
                                                                                       'exp(2L)1{L>b}.',
                                                    'upper_tail_bound_unevaluated': 'T_upper=(10000*80/79)*C16*v^16/(b-mu_upper-2v)^32',
                                                    'v_exact': [3, 400]},
 'full_METHOD_JSON_copy_count': 1,
 'future_actual_stock_bounds': {'independent130': None, 'primary90': None},
 'historical_cache_partitions': {'completed_first_log_V3': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-1.pyc',
                                                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.opt-2.pyc',
                                                                             'research/limitation_program_20261001/__pycache__/experiment_e11_first_log_prefix_squared_l2_v3.cpython-312.pyc'],
                                                            'existing_expected_SHA256': {}},
                                 'completed_native_author': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc',
                                                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-2.pyc',
                                                                              'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.pyc'],
                                                             'existing_expected_SHA256': {}},
                                 'completed_scalar_V2': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc',
                                                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc',
                                                                          'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc'],
                                                         'existing_expected_SHA256': {}},
                                 'failed_scalar_V1': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc',
                                                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc',
                                                                       'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'],
                                                      'existing_expected_SHA256': {}}},
 'historical_first_log_V3_source_has_current_execution_permission': False,
 'native_reference_toy_array_count': 0,
 'original_caps': {'CPU_admission_creation_wall': [180, 150, 600],
                   'current_stdlib_runtime_files_bytes': [4096, 536870912],
                   'owned_files_bytes': [64, 134217728],
                   'references_unique_bytes_hash_work': [100000,
                                                         8589934592,
                                                         25769803776],
                   'serialized_integer_reduced_rational_analytic_temporary_bits': [65536,
                                                                                   131072,
                                                                                   524288]},
 'original_cfg_expected': {'bytes_cap': 8388608,
                           'expected_SHA256': 'aaeeb031a76b70ae1ac53b6557056f554273db4b313678c36c7ccd2c483e7e37',
                           'path': '.context/frontier_t0_env/pyvenv.cfg'},
 'output': 'results/limitation_program_20261001/E11_first_stock_squared_L2_run001',
 'planned_manifest_inclusive_owned_files': 27,
 'planned_owned_filenames': ['executed_controller.py',
                             'executed_preflight.md',
                             'executed_policy.json',
                             'executed_ROOT_READY.json',
                             'reviewed_next_stock_method.md',
                             'reviewed_next_stock_method.json',
                             'reviewed_independent_method_peer.json',
                             'reviewed_ROOT_method.json',
                             'protocol.json',
                             'run_started.json',
                             'interpreter.json',
                             'loaded_module_origins.json',
                             'active_and_archived_role_graph.json',
                             'literal_prior_stock_component_adapters.json',
                             'fresh_full_input_union_before_assembly.json',
                             'source_first_stock_witness.json',
                             'primary_first_stock_components.json',
                             'primary_first_stock_squared_L2.json',
                             'independent_first_stock_components.json',
                             'independent_first_stock_squared_L2.json',
                             'independent_primary_proof_check.json',
                             'four_fixed_reject_controls.json',
                             'qualification_and_remaining_gaps.json',
                             'fresh_full_input_union_after_assembly.json',
                             'summary.json',
                             'completion_outcome.json',
                             'manifest.json'],
 'runtime_invocation': ['C:/Users/prith/quantum_option_pricing/.context/frontier_t0_env/Scripts/python.exe',
                        '-I',
                        '-S',
                        '-B',
                        'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_first_stock_squared_l2_v1.py',
                        '--ready-sha256',
                        'EXTERNAL_ROOT_READY_SHA256'],
 'selected_original_log_contract': {'actual_common_literal': 60222732077,
                                    'actual_drift_signed_literal': -1374389535,
                                    'actual_idio_literal': 73757482253,
                                    'actual_initial_literal': 5063438167381,
                                    'addition_rounding_zero_requires_original_all_partial_no_wrap': True,
                                    'asset_zero_based': 0,
                                    'case': 'B4x12',
                                    'contractual_date_one_based': 1,
                                    'fraction_bits': 40,
                                    'ideal_reference_exact_literal_parameters': {'S0': [100,
                                                                                        1],
                                                                                 'T': [1,
                                                                                       1],
                                                                                 'drift': [-1,
                                                                                           800],
                                                                                 'r': [3,
                                                                                       100],
                                                                                 'rho': [2,
                                                                                         5],
                                                                                 'sigma': [3,
                                                                                           10],
                                                                                 't': [1,
                                                                                       12]},
                                    'legacy_binary64_real_parameters_equal_exact_decimal_claimed': False,
                                    'newly_evaluated_or_synthesized_target': False,
                                    'ordered_native_normal_values': [94, 125],
                                    'ordered_original_normal_indices': [0, 1],
                                    'original_prefix_witness': {'asset': 0,
                                                                'constants': [[-1374389535,
                                                                               1],
                                                                              [5063438167381,
                                                                               1]],
                                                                'date': 0,
                                                                'every_driver_multiplicity': 1,
                                                                'original_normal_indices': [0,
                                                                                            1],
                                                                'raw_log': 3542,
                                                                'stock': 4021},
                                    'original_shared_pair_scope': {'cosines': [{'address': 67,
                                                                                'floors': 7,
                                                                                'input': 6,
                                                                                'local': 71,
                                                                                'lookup_outputs': [72,
                                                                                                   73,
                                                                                                   74,
                                                                                                   75,
                                                                                                   76,
                                                                                                   77,
                                                                                                   78,
                                                                                                   79],
                                                                                'output': 93},
                                                                               {'address': 99,
                                                                                'floors': 7,
                                                                                'input': 61,
                                                                                'local': 102,
                                                                                'lookup_outputs': [103,
                                                                                                   104,
                                                                                                   105,
                                                                                                   106,
                                                                                                   107,
                                                                                                   108,
                                                                                                   109,
                                                                                                   110],
                                                                                'output': 124}],
                                                                   'log': {'address': 23,
                                                                           'floors': 8,
                                                                           'input': 15,
                                                                           'local': 27,
                                                                           'lookup_outputs': [28,
                                                                                              29,
                                                                                              30,
                                                                                              31,
                                                                                              32,
                                                                                              33,
                                                                                              34,
                                                                                              35,
                                                                                              36],
                                                                           'output': 52},
                                                                   'normal_values': [94,
                                                                                     125],
                                                                   'original_shared_pair_preserved': True,
                                                                   'radius': 58,
                                                                   'raw_uniform_values': [0,
                                                                                          1]},
                                    'raw_preclip_log_value': 3542,
                                    'saved_date_zero_based': 0,
                                    'signed_cmul_floors': 2,
                                    'source_seven_node_slice_saved_metadata': [{'args': [94],
                                                                                'op': 'cmul',
                                                                                'out': [3492],
                                                                                'params': {'c': 60222732077}},
                                                                               {'args': [125],
                                                                                'op': 'cmul',
                                                                                'out': [3493],
                                                                                'params': {'c': 73757482253}},
                                                                               {'args': [3492,
                                                                                         3493],
                                                                                'op': 'add',
                                                                                'out': [3494],
                                                                                'params': {}},
                                                                               {'args': [],
                                                                                'op': 'const',
                                                                                'out': [3495],
                                                                                'params': {'value': 4722366482868270824161}},
                                                                               {'args': [3494,
                                                                                         3495],
                                                                                'op': 'add',
                                                                                'out': [3496],
                                                                                'params': {}},
                                                                               {'args': [],
                                                                                'op': 'const',
                                                                                'out': [3541],
                                                                                'params': {'value': 5063438167381}},
                                                                               {'args': [3496,
                                                                                         3541],
                                                                                'op': 'add',
                                                                                'out': [3542],
                                                                                'params': {}}],
                                    'stock_consumer_not_claimed': 4021,
                                    'target_literal_SHA256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
                                    'target_path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json',
                                    'time_exact_literal': [1, 12],
                                    'width': 72},
 'selected_original_stock_site': {'actual_original_support_signature': '2a35ab41d964c6abc9a3a6243a93f1be141b31da20672c50cdfe0d452239311e',
                                  'clipped': 3579,
                                  'exponent': 3979,
                                  'high': 9145480617430,
                                  'inverse_ln2': 1586259972792,
                                  'ln2': 762123384786,
                                  'low': -12193974156573,
                                  'polynomial': 4020,
                                  'raw_log': 3542,
                                  'remainder': 3982,
                                  'stock': 4021,
                                  'values': [16,
                                             3978,
                                             3979,
                                             3980,
                                             3981,
                                             3982,
                                             3983,
                                             3984,
                                             3985,
                                             3986,
                                             3987,
                                             3988,
                                             3989,
                                             3990,
                                             3991,
                                             3992,
                                             3993,
                                             3994,
                                             3995,
                                             3996,
                                             3997,
                                             3998,
                                             3999,
                                             4000,
                                             4001,
                                             4002,
                                             4003,
                                             4004,
                                             4005,
                                             4006,
                                             4007,
                                             4008,
                                             4009,
                                             4010,
                                             4011,
                                             4012,
                                             4013,
                                             4014,
                                             4015,
                                             4016,
                                             4017,
                                             4018,
                                             4019,
                                             4020,
                                             4021]},
 'serializer_expected_source_and_cache_partition': {'absent_three_variant_cache_paths': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.pyc',
                                                                                         'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-1.pyc',
                                                                                         'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-2.pyc'],
                                                    'existing_cache_expected_SHA256': {},
                                                    'import_before_initial_runtime_and_loaded_origin_admission': True,
                                                    'module': '_pylong',
                                                    'postadmission_origin_or_cache_discovery_authorized': False,
                                                    'scientific_arithmetic_or_representation_policy_change': False,
                                                    'source_SHA256': 'bcae0d4cc2d4d3fd9b40bb06b512eb8dd785f755edd1f9038613d4460ca4c6c1',
                                                    'source_path': 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\_pylong.py'},
 'source_contract_canonical_JSON_SHA256': '2d0ab1412b9e04cabaf030540c5ad884236ad7e6754f5acf44fb23efbd309540',
 'stock_source_45node_closure_canonical_JSON_SHA256': 'a284d0fa82eee4c8f40e7de2cadd9f2867b122d9bf24e604c3e90e55f68edbf1',
 'two_literal_profile_adapter_contract': {'independent130': {'B_log_original_literal_pair': [2428158210523221716611869059561284163506426632206382933227882749799107497844497983493965778077859665221003848479909443502356283144309763445667792023072878245744752236936706476755951355252171098226395633180998333416396336106714275667874841716872377533973362164422306514278219297714838302666989189183695256703701608221630931547883699856199822898192517375275381325725885420659120650636522924098635555012513935156871817454254946932191744197140849579927797658793344456153044262066893575491316898749520247694131272008480484279767442621311639247906829230752566809805133006122638828228870494291445884186293021900488583473809333911893695999791478916008054562105198374155378886604081879712491148543043767842545408363141653398723997338202229669865800275898817433527911904806662136305852498339695196210493003428178533842259395795527764866221522384929346609169752763847410100021900211807612222242377686666678799320498627233759536718291110326114419560051244617985404989154265033792342989447457763132027823749179017384608895015113531159623561782481108005357554216247019645899050523,
                                                                                             1513733228466844074031275717429922960187834973955384601995536522750016224414668727819206116519306201179573042460674520346942702696629351302643155826634064290672325608545738612667826017895680334158654790028613891981326576843599902103891630952814511173327529997748425925496065487194844289996932339143900081966349579181053527389213998289763844397764192911821096266306307504423212647986687390974299915254681199374147253096002018965665012434635135952694797887226841083837066248297522135663165086552559028923067229727245617133616118090428699689301851612632033088052755892767180543198941489242025484577036517070180690342893617402169278129137856839223966607852369548571543075007653621750787446809392176100547184066983840358432973683897920428422230036262075573229148857864832716125527510362375539991393222476383567811375726121835388823028241346307366055443781189365504221014616251877476187866875683293332963037770069373358608728988510788498971777052572870846793872720761611264090303077011502812390444993549203038354883176703281322899110004024395674513226847632315312959749352534835200],
                                                             'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
                                                             'B_log_saved_record_expected_SHA256': '7ba5fb90631a413504b3196824f8ef69649e44477bd13c4cbca20cc565941cae',
                                                             'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/independent_log_prefix_squared_L2.json',
                                                             'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
                                                             'alpha_beta_original_record_expected_SHA256': '6e293022c0b2682a0c2c2abe1aa672b954423831ed4503f8732fa95f01cb9b8e',
                                                             'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_stock_exponential_envelopes.json',
                                                             'alpha_original_field': ['B4x12',
                                                                                      'alpha_upper'],
                                                             'alpha_original_literal_pair': [247002706270630918565331540008958163692589137852088424583460925597448157152683677894942918643332625323316582822253875275,
                                                                                             22181357552966518876627313473144669627491496603006532601363836644916970462445004984319795248833116624779129687691228574631793262592],
                                                             'beta_original_field': ['B4x12',
                                                                                     'beta_upper'],
                                                             'beta_original_literal_pair': [1,
                                                                                            1099511627776],
                                                             'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                                                               'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                                                               'coordinate_squared_B_literal_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84',
                                                                                                               'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json',
                                                                                                               'coordinate_squared_B_uncombined_literal': [45526575641624206065960088254647963011088397925424336288233050317860197460879324658749414611574392425861283022019968244562699896140455970821288493126573624826536536912610825770883742372490773981523979696246736685050999662274328929778131746172668001901691046834836586721194202082479121970699430337226697752568947187457296404138334397844423679815518881938375176693001373653480415842115399914944778807835058160148015764442345734677926164113677443351799296560705736910653276695736495021885524820312187058296068869310952956910819322154696725305584723965789462683039126727683916922786468244659518851588647486421853725162918802134315547820918795106049611857838088118685068522360897370538324399193149950569315794375412868603490602486645544192130229308142902137397386041398706454720528355157101284743157437656955492159236359877173948345445727319099126101823284957663395902942816481504672717487603102511793763726345482303724630928183512057385898650074369193079140521157948972608871495778625773102762931608632772763752420208898616246237860960043233083858239,
                                                                                                                                                           1064311162290314829993317570393594139098783759755472316751688907376604267686819057685722084483472694979913873600803721210261653601613069280337194220754598433785378364203070858496756245943431492169577928446243218733206784282860496472857713784849350212282348295966506207303324069383995279555657006575860272992372853027356973988113815245928293961331789704506862768806632883623539099201848989216833061560609366169844682079158783936810813014476063528488006048240464997985884687969145967483292119744767282112030435416265811730561355136342763978551994132702756478800100718262968364118613782877026044387867417640192327089432833159010812111753923769185578544857826757126549955911889493341782728564597276328179501589306777896495754952403978573163919346168330904035486839477729792271453485959504398136183338911862175782922917093258127209534688205322695296676276395441012752256514277180818595823615644362363091088759329682368039258062181761762722268836977250742748313007631976499454204739038094317076899400791760670433509355026879994577025079039421948666755153920000],
                                                                                                               'fields': {'additive_rounding_zero_only_after_no_wrap': True,
                                                                                                                          'common_literal_error_upper': [276166322630920802395230294070446372783075414029508302638124289962937731639648392341357814793924321396020554846440862515,
                                                                                                                                                         1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888],
                                                                                                                          'drift_literal_error': [7,
                                                                                                                                                  27487790694400],
                                                                                                                          'every_original_driver_once': True,
                                                                                                                          'every_stored_partial_sum_and_product_safe': True,
                                                                                                                          'idio_literal_error_upper': [156576429583424880029055937563110731415892319528210216364286123675151694157011596510784577608392178182727361521908420199,
                                                                                                                                                       709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                          'initial_literal_error_upper': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                                                                                                                          346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                                                                                                                          'true_common_enclosure': [[38877535641111535490325048879373881033237089667338836564302146726369221970178317277329260034200117344446008391755317237212265486745,
                                                                                                                                                     709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                                                    [77755071282223070980650097758747762066474179334677673128604293452738443940356634554658520068400234688892016783510634474424530973491,
                                                                                                                                                     1419606883389857208104148062281258856159455782592418086487285545274686109596480318996466895925319463985864300012238628776434768805888]],
                                                                                                                          'true_idio_enclosure': [[47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343833,
                                                                                                                                                   709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944],
                                                                                                                                                  [47615062388795067043711504546324594758292274589912294657316208604719517989833302425846834916550135782273491250268855199060730343835,
                                                                                                                                                   709803441694928604052074031140629428079727891296209043243642772637343054798240159498233447962659731992932150006119314388217384402944]],
                                                                                                                          'true_initial_enclosure': [[51074463243831589481644883618341444951183233404609790581927792645537908406073896346061752896907334970354529391308639775166059120735,
                                                                                                                                                      11090678776483259438313656736572334813745748301503266300681918322458485231222502492159897624416558312389564843845614287315896631296],
                                                                                                                                                     [1596076976369737171301402613073170154724476043894055955685243520173059637689809260814429778028354217823579043478394992973939347523,
                                                                                                                                                      346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728]]},
                                                                                                               'literal_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                                                                               'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json'},
                                                             'e0_original_field': ['B4x12',
                                                                                   'initial_literal_error_upper'],
                                                             'e0_original_literal_pair': [85425762457946856618229923647506612305082283325923484576059679573669303927067258488077892805477943696085462313996355,
                                                                                          346583711765101857447301773017885462929554634421977071896309947576827663475703202879996800763017447262173901370175446478621769728],
                                                             'e0_original_record_expected_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                             'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json',
                                                             'future_first_stock_squared_bound': None,
                                                             'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                                                              'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                                                              'mu_lower_minus_a_strict_positive': None},
                                                             'ln2_lower_original_field': ['exact_component_allowances',
                                                                                          'ln2_lower'],
                                                             'ln2_lower_original_literal_pair': [1889261008865840820845434144940756618726999344670259515995750754217821754500788139444939524188547339025585587602769247784879116306451410162687618926710924446943916199137723684941981681870055380792574043291861815817772683212125601991704013718366662977212533772715036747350128426675744178435868437524651465387808022185045717540672567957277642069441780888858051055534388844360342398807653805619980652864503681208434677961274301606889689060873958402013731503561912296584004582336707583167425957420682771042753827882862458159391895363893023780996566350849344303354407122266002809532662847818704615735400368470916489232620845467336296959876015254942962044676870458651995798514099816581832619706240631245441372803345552299783611172312186961514646923930769255231,
                                                                                                 2725627488435628481496863175516455096268428871729528261974136657897740576702135939247829423093197483020632924981445528712795654376699704931913098750094045475418234376750483233635429338640072811018588732010250132338523030120871129556706434130706601892323570904539447104103180959965009284063038974813443414272999699177340229319053742082159247821787254916183238108504018824427371176008091776833205564916200995241120217565045507036810006744635670740696031073014129582349551099313579709502048339831984281555128954829589841559252686271983451367307069838038458075841476737790053476210649922039653098169050211612672671518989555517522647432276621598282684754503894614556632435948513203616062757277391012459709406205277046040823461804052649041636834455710597120000],
                                                             'ln2_lower_original_record_expected_SHA256': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c',
                                                             'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json',
                                                             'profile': 'independent130'},
                                          'primary90': {'B_log_original_literal_pair': [8512947868103270312620178638577675641787226919214228390530540381034131465897304040781846302011961304683661376217863894953653714626337944010446722728460538706926595232008107602575959975484595860579894434422595857037680642776863378528725175958732706908884736896816233339222173517891896741153446551808050780878902912055518946683907564816233968640153853973297161216675566384159352979311963775610947610269712162731115111068282500641705615023150474720728493520613362903823017476623356456346506182833482073871210080440284457552935309761648687916830904137003262193567398209116027802650614357784102225851623479377033752444067913586656279260339319807583904153617578284670222196187068661423744113098974350950521477755319342951839540876201609502733051489887920720037787943025286596377416669772603979,
                                                                                        5307039716072348696780168043740813464254609720802369423615294422907314307532518321538000940854478613980872020981793264427883045912368569694412757615556272398241982644161294516303803767354132880993538021210644731634689200578055163749524840592464477041507439945512096728776437943453406084685270822889988767868681493195952982792018927866877152888635594824290311697822256357585190810004684089502253539393496036233330075699157469101665700736452449271068553649074774557957281301950960647319203684623658366702735103742598936202023206199332036084265486135044737289634458202359168772559818555896159232721394619758320074879224794515146455685801330982081012412819934289386060886436186831160504046273104674577722520394081048768080809242859607520397670454818010531687899611661207230488036051164023784210432000],
                                                        'B_log_original_saved_field': 'dimensionless_squared_log_error_upper',
                                                        'B_log_saved_record_expected_SHA256': '2a1833c8685add43b3854180b0e919ae63d6e1f4f00b15e0b4a979dab55d7a29',
                                                        'B_log_saved_record_path': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001/primary_log_prefix_squared_L2.json',
                                                        'all_original_inputs_uncombined_no_minimum_or_profile_nesting': True,
                                                        'alpha_beta_original_record_expected_SHA256': '525fe878d5897e697d5c3c4982cfe96dbf8dbd2512f407054805153d75f9a09a',
                                                        'alpha_beta_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/stock_exponential_envelopes.json',
                                                        'alpha_original_field': ['cases',
                                                                                 'B4x12',
                                                                                 'alpha_upper'],
                                                        'alpha_original_literal_pair': [45367232165459914923385662946667222531831256343543066774787104815382220620136265,
                                                                                        4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794752],
                                                        'beta_original_field': ['cases',
                                                                                'B4x12',
                                                                                'beta_upper'],
                                                        'beta_original_literal_pair': [1,
                                                                                       1099511627776],
                                                        'complete_previous_first_log_adapter_unchanged': {'case': 'B4x12',
                                                                                                          'coordinate_squared_B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                                                                          'coordinate_squared_B_literal_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2',
                                                                                                          'coordinate_squared_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json',
                                                                                                          'coordinate_squared_B_uncombined_literal': [6384515858493324899204650816690602383243896628762144024838388575192784288263607574124475579311362107174259757315894678092932691144004996317684757239491577738663479089538830715373626887086762482848504764370894874601009690359513645879614296781215736265714976320857346435131493617915612198522808202631593695291899931649672368386146234734570417339446416702867410231806773950424091090661434442689891841358379288364117360578041218553229275135046496308953688840643190076858815826553021255552734203751723861582615543903022215132454667522895236911653076632975961585083926964508397813772669857423849359689257596440325535868533564587618339196330539161884615914792034482603801651059720606527409707394353927004650599038825068815554312722513304368639406353833221401969503097551111,
                                                                                                                                                      149255932348255029840930948694338021615758146182516215147903290154068608446638153532202662774179879721055219787468365833860973589471728563011692324832415929957895190975456274701802682993794698953733072940370655372202170774929412649893781138342842707674374706002694455090309162290064574705282811923418527693442615475576702226367774728084108794656911985978714181318614520136612078178581015897518667459585847855253021122272037703116390174668376951309260296787554752552811293610708797592730899712395924372711170571650703269509976322305071112951079966178662768362870326736403383874217502741289202539189610610979453036539824285013214071642625704529170206938597092797681220024236618836869254858053825329456771958456653563065069111119133549684255094573363094756306151650558476288000],
                                                                                                          'fields': {'addition_rounding_paid': 0,
                                                                                                                     'common_literal_error_upper': [25361871260938488729228877533401678061248213015932440747215362596598621650241007,
                                                                                                                                                    130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064],
                                                                                                                     'drift_literal_error_upper': [7,
                                                                                                                                                   27487790694400],
                                                                                                                     'every_signed144_scaled_normal_product_safe': True,
                                                                                                                     'every_stored72_raw_partial_sum_safe': True,
                                                                                                                     'exact_common_coefficient_enclosure': [[3570337775001464811484133992278442479448757806641386405762450668688115075446873113027781367,
                                                                                                                                                             65185151242703554760590262029100101153646988597309960020356494379340201592426774597868716032],
                                                                                                                                                            [7140675550002929622968267984556884958897515613282772811524901337376230150893746226055562735,
                                                                                                                                                             130370302485407109521180524058200202307293977194619920040712988758680403184853549195737432064]],
                                                                                                                     'exact_drift': [-1,
                                                                                                                                     800],
                                                                                                                     'exact_idio_coefficient_enclosure': [[1093188219767175304906489994055034964269771883937280948777703827016588627670840331443227841,
                                                                                                                                                           16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                                                                                                          [2186376439534350609812979988110069928539543767874561897555407654033177255341680662886455683,
                                                                                                                                                           32592575621351777380295131014550050576823494298654980010178247189670100796213387298934358016]],
                                                                                                                     'idio_literal_error_upper': [3594818524360149261960544761045424477895504472498124242279759015017946963915583,
                                                                                                                                                  16296287810675888690147565507275025288411747149327490005089123594835050398106693649467179008],
                                                                                                                     'initial_log_spot_error_upper': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                                                                                                                                      1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
                                                                                                                     'signed_scaled_normal_floors_per_increment': 2},
                                                                                                          'literal_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                                                                          'path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json'},
                                                        'e0_original_field': ['cases',
                                                                              'B4x12',
                                                                              'initial_log_spot_error_upper'],
                                                        'e0_original_literal_pair': [251043752960007949707159381571869253780488898003998645625260105337093999684715,
                                                                                     1018517988167243043134222844204689080525734196832968125318070224677190649881668353091698688],
                                                        'e0_original_record_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                        'e0_original_record_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json',
                                                        'future_first_stock_squared_bound': None,
                                                        'future_profile_guard_results': {'b_le_8_times_saved_ln2_lower': None,
                                                                                         'b_minus_mu_upper_minus_2v_strict_positive': None,
                                                                                         'mu_lower_minus_a_strict_positive': None},
                                                        'ln2_lower_original_field': ['exact_component_allowances',
                                                                                     'ln2_lower'],
                                                        'ln2_lower_original_literal_pair': [1345774352498033414297429742984977384893258835982351961807386333796539728241594400081593475302051821027762048040776563903683902961983263656168213352737876304347045903684241668673381438784885331058207914470224642777024991198545607304922005382825701321879479404077792934389096593003863039049325619009954841406946245966015575618504966501594756534721968950545959386285176356420712421910845677985146290754463549779541316458725767992186966218654989675307831921168545792,
                                                                                            1941541984504468570495415124249969943153260291510923173492279628121237271490888121892502719969273800531384118146530070969072470417266968221171879127013717035856262982263162712777774605998471461725924173989544832278147776356165895694754126642321144762871931919153281705662822212334308489675713211589863160815276266657731584868034417075674451499087564989252906843588748800087924882276955544589775699716444612993024606968249415334365911711858047546545182122278495875],
                                                        'ln2_lower_original_record_expected_SHA256': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60',
                                                        'ln2_lower_original_record_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json',
                                                        'profile': 'primary90'}},
 'two_profile_adapter_commitments': {'independent130': '0466acccc3e557f0a46f1de1b9e7ff9288f0bbb29d369cca6129b798be4a4787',
                                     'primary90': '94402a3d233afaa4939a5f336b4f795f429e83d2c118441c1dcf66b080932025'}}
V2_METADATA_OVERRIDE_FIELDS = ['runtime_invocation',
 'current_static_review_paths',
 'current_authoring_acceptance_path',
 'current_authoring_acceptance_SHA256',
 'accepted_method_and_review_expected_SHA256',
 'historical_cache_partitions']
ORIGINAL_V1_ACCEPTANCE_KEY = '.context/E11_FIRST_STOCK_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json'
FAILED_STOCK_V1_EXPECTED = {'.context/E11_FIRST_STOCK_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json': '20b48e9d7a6efd0efcb2b941100cf9c1fe0b0adabf5a157356d61c9611d30258',
 '.context/E11_FIRST_STOCK_SQUARED_L2_AUTHOR_STATIC_QA_run001.json': '890395879ad2bcc7370bbcd365d57691874d240d163c3777152a17ef31aee598',
 '.context/E11_FIRST_STOCK_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json': 'fd80e86f7b05cc9ce245eef8a4359ec5f1d72b395d6e996e81283ec7d7c72dd9',
 '.context/E11_FIRST_STOCK_SQUARED_L2_METHOD_PROSPECTUS_run001.json': '5ca963150cb1b1e4e25adb00e2c1cbbc51d9e988c33d12763ba8fb5c3d0f1908',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json': '3df88b2a7da02bfc406797f33a24a92e0f6d3dc1e4ea943586924bafa73d3ca2',
 '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '00ad0ec5b6171bbeba31859898fa6a2dbeff67fa4bdb34a08f8c82aba6ed1911',
 '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_INDEPENDENT_FAILURE_FIELD_PEER_run001.json': '3cfc5a95b5b4d2a4d1dff6d50c0f214bb0cc78ef96248974a0e39600a1172802',
 '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_ROOT_FREEZE_run001.json': 'a0d5e217b4e0dfab0e6c097bb74b3333143054108bd3de89f1dd0aabf043c7ea',
 '.context/E11_FIRST_STOCK_V1_PRE_ADMISSION_LAUNCH_ROOT_CUSTODY_run001.json': '090b5733b31fe6e6c3480135d7feca7d1afaf42eeb9e05bad489599c2c0b8d96',
 '.context/E11_first_stock_ROOT_saved_result_verifier_run001.py': 'cbcefc41c614619a2ab3e5380cfc2b847291961972c4df2cdaee5269efaab1fa',
 '.context/E11_first_stock_squared_L2_actual_run002.log': '8c84a83bbdecd823690e282653735c72c829213c54d90598c25f1d0f053f37f1',
 'research/limitation_program_20261001/E11_FIRST_STOCK_SQUARED_L2_PREFLIGHT_V1.md': 'b5d441b2ff2238e403e178c7da4e24e7c251ccb4b00deddb9efa41781992a5f9',
 'research/limitation_program_20261001/e11_first_stock_squared_l2_preflight_v1.json': '5ef08878d82a1df6ad3baf6e8ff0078179fe76620cf37700584d9d96976f9e0e',
 'research/limitation_program_20261001/experiment_e11_first_stock_squared_l2_v1.py': '099358102732798bc5e142d51ccf0136ebf20ba6b13bc8fab3846d6b2982686d'}
FAILED_STOCK_V1_READY_KEY = '.context/E11_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json'
FAILED_STOCK_V1_FREEZE_KEY = '.context/E11_FIRST_STOCK_V1_PREOUTPUT_CPU_CENSORED_ROOT_FREEZE_run001.json'

def admit_first_stock_v1_preoutput_history():
    require(type(_FULL_ADMISSION) is bool and _FULL_ADMISSION is False,
            "Failed stock V1 cache custody before current origins and epoch closure")
    for key, pin in FAILED_STOCK_V1_EXPECTED.items(): bind(ROOT / key, pin)
    old = bootstrap_json(ROOT / FAILED_STOCK_V1_READY_KEY, FAILED_STOCK_V1_EXPECTED[FAILED_STOCK_V1_READY_KEY])
    failure = bootstrap_json(ROOT / FAILED_STOCK_V1_FREEZE_KEY, FAILED_STOCK_V1_EXPECTED[FAILED_STOCK_V1_FREEZE_KEY])
    require(failure["passed"] is True and failure["failure_custody_only"] is True
            and failure["certified_stock_numerical_result"] is failure["READY_or_SCI_execution_authorized"] is False
            and failure["owned_failed_output_files"] == failure["completion_or_partial_success_credit"] == 0
            and failure["output_directory_absent"] is True
            and failure["first_input_union_completed"] is failure["numerical_bound_guard_moment_tail_control_or_source_calculation_reached"] is False,
            "Immutable V1 preoutput CPU failure grants no mathematical result or owner")
    require(failure["actual_log_expected_SHA256"] == FAILED_STOCK_V1_EXPECTED[failure["actual_log_path"]]
            and failure["current_source_MD_policy_READY_review_expected_SHA256"]
            == {key: FAILED_STOCK_V1_EXPECTED[key] for key in failure["current_source_MD_policy_READY_review_expected_SHA256"]}
            and old["author_method_SHA256"] == failure["author_method_SHA256"]
            and old["static_review_expected_SHA256"] == failure["static_review_expected_SHA256"],
            "Exact preserved V1 source READY current3 and failed log field joins")
    partition = {"existing_expected_SHA256": old["existing_new_code_cache_SHA256"],
                 "absent_paths": old["absent_new_code_cache_paths"]}
    require(partition == failure["current_source_cache_partition"] == HISTORICAL_CACHE_PARTITIONS["failed_first_stock_V1"],
            "V1 actual READY three-cache authority, never observed promotion")
    historical_code_cache_partition(ROOT / HISTORICAL_SOURCE_PATHS["failed_first_stock_V1"], partition)
    require(failure["output_path"] == OUTPUT.relative_to(ROOT).as_posix()
            and not OUTPUT.exists() and not OUTPUT.is_symlink() and OUTPUT.resolve(strict=False) == OUTPUT,
            "V1 zero-owned shared output is absent only before this V2 exclusive creation")
    require(OUTPUT not in _ABSENT_RUNTIME, "Shared current output is never an absence obligation after creation")
    return {"failedV1_preoutput_no_result_or_success_owner": True,
            "oldV1_actual_three_cache_consumer_before_first_origins": True,
            "shared_output_absence_precreation_only": True, "old_execution_grant_inherited": False}

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

def exact_key(key):
    require(type(key) is str and key and not Path(key).is_absolute()
            and not Path(key).drive and "\\" not in key
            and all(part not in ("", ".", "..") for part in key.split("/"))
            and Path(key).as_posix() == key, "Exact original ROOT-relative spelling")
    return ROOT / key

def object_sha(value):
    budget()
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    require(len(data) <= MAX_OWN_BYTES, "Bounded literal metadata object")
    return hashlib.sha256(data).hexdigest()

def bind(path, expected):
    actual = add(path, expected)
    require(type(_FULL_ADMISSION) is bool, "Exact admission epoch bool")
    if _FULL_ADMISSION is False:
        actual = canonical(actual, fresh=True)
        require(not actual.is_relative_to(OUTPUT), "Admission bind never admits output authority")
        before = fingerprint(actual)
        result = digest(actual, fresh=False, already_resolved=True)
        require(result == expected and (actual not in _OBSERVED or _OBSERVED[actual] == expected)
                and fingerprint(actual) == before and canonical(actual, fresh=True) == actual,
                "Admission cached SHA equals external expected pin with stable fresh identity")
    else:
        require(digest(actual, fresh=True) == expected, "Full fresh original expected bytes")
    return actual

def standard_runtime_members():
    members = {LAUNCHER, BASE / "python.exe"}
    for path in BASE.iterdir():
        budget()
        if path.is_file():
            members.add(canonical(path))
    for tree in (BASE / "Lib", BASE / "DLLs"):
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            parent = Path(root)
            require(canonical(parent, fresh=True) == parent, "Exact current runtime directory")
            dirs[:] = [name for name in dirs if name.lower() != "site-packages"]
            for name in dirs:
                path = parent / name
                require(not path.is_symlink() and canonical(path, fresh=True) == path,
                        "No runtime alias silently skipped")
            for name in names:
                members.add(canonical(parent / name))
                require(len(members) <= MAX_RUNTIME_FILES, "Current isolated runtime count cap")
    return members

def historical_code_cache_partition(source, partition):
    paths = {exact_key("research/limitation_program_20261001/__pycache__/" + source.stem
                       + ".cpython-312" + suffix + ".pyc") for suffix in ("", ".opt-1", ".opt-2")}
    expected, absent = partition["existing_expected_SHA256"], partition["absent_paths"]
    present = {path for path in paths if path.exists()}
    require(type(expected) is dict and type(absent) is list and len(absent) == len(set(absent))
            and {exact_key(key) for key in expected} == present
            and {exact_key(key) for key in absent} == paths - present,
            "Original externally fixed historical three-variant cache partition")
    for key, pin in expected.items():
        path = bind(exact_key(key), pin)
        _CODE_CACHE_EXPECTED[path] = pin
    for key in absent:
        path = exact_key(key)
        require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                "Original absent cache has no physical alias")
        _ABSENT_RUNTIME.add(path)

def serialization_runtime_admission():
    contract = SERIALIZATION_RUNTIME
    source = Path(contract['source_path'])
    require(str(source) in _EXTERNAL and _EXTERNAL[str(source)] == contract['source_SHA256'], 'Serializer module has original admitted complete-runtime expected SHA')
    require(canonical(_pylong.__file__, fresh=True) == source and digest(source, fresh=True) == contract['source_SHA256'], 'Upfront standard serializer origin freshly equals original expected SHA')
    require(contract['existing_cache_expected_SHA256'] == {}, 'Externally declared serializer cache partition')
    for key in contract['absent_three_variant_cache_paths']:
        path = Path(key)
        require(not path.exists() and not path.is_symlink(), 'Every externally declared serializer cache variant absent before admission')
        _ABSENT_RUNTIME.add(path)

def retain_failed_e11_v1():
    history = FAILED_E11_V1_HISTORY
    freeze = read(bind(ROOT / history['ROOT_freeze_path'], history['ROOT_freeze_SHA256']))
    original_ready = read(bind(ROOT / history['ROOT_READY_path'], history['ROOT_READY_SHA256']))
    require(freeze['certified_scalar_result'] is False and freeze['manifest_absent'] is True and freeze['own_complete_inventory'] == history['complete_failed_owned_inventory'], 'Failed V1 is immutable opaque history, never a certificate')
    require(original_ready['author_method_SHA256'] == history['author_method_SHA256'] and original_ready['output'] == history['output'], 'Original failed V1 author and route authority retained')
    require(original_ready['static_review_expected_SHA256'] == history['static_review_expected_SHA256'], 'Original V1 review authority unchanged')
    partition = history['cache_partition']
    require(partition['existing_expected_SHA256'] == original_ready['existing_new_code_cache_SHA256'] and partition['absent_paths'] == original_ready['absent_new_code_cache_paths'], 'Original failed V1 cache authority only')
    historical_code_cache_partition(RESEARCH / 'experiment_e11_scalar_midpoint_l2_v1.py', partition)
    directory = ROOT / history['output']
    members = set()
    for name, row in history['complete_failed_owned_inventory'].items():
        require(Path(name).name == name and name not in history['manifest_and_summary_and_second_union_absent'], 'Only declared failed owned filenames')
        path = bind(directory / name, row['SHA256'])
        require(path.stat().st_size == row['bytes'], 'Complete original failed owned byte size')
        members.add(path)
    require(len(members) == 19 and inventory(directory) == members, 'Every original failed owned file and physical inventory retained')
    _OWN_INVENTORIES[directory] = members
    for name in history['manifest_and_summary_and_second_union_absent']:
        path = directory / name
        require(not path.exists() and not path.is_symlink(), 'Failed packet never acquires a completion seal')
        _ABSENT_RUNTIME.add(path)

def strict_loaded_origins():
    forbidden = {"numpy", "scipy", "mpmath", "sympy", "numba", "pytest", "pandas", "gmpy", "gmpy2"}
    require(not any(name.split(".", 1)[0] in forbidden or name.startswith("research.")
                    for name in sys.modules), "No numerical or old scientific module import")
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(not any(lexical.is_relative_to(s) or lexical.resolve(strict=False).is_relative_to(s)
                            for s in _EXCLUDED_SCOPE), "Excluded origin remains rejected")
            if lexical.is_file():
                actual = canonical(lexical, fresh=True)
                key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                require(key in mapping and digest(actual, fresh=True) == mapping[key],
                        "Every present loaded source/cache already has original expected SHA")
            else:
                require(attribute == "__cached__" and not lexical.exists() and not lexical.is_symlink()
                        and lexical.resolve(strict=False) == lexical,
                        "Only an immediate exact absent hypothetical cache; never missing source")
                source = getattr(module, "__file__", None)
                require(source is not None and str(source).endswith(".py")
                        and Path(cache_from_source(str(source), optimization="")) == lexical,
                        "Missing cache belongs exactly to its known loaded Python source")
                require(lexical in _ABSENT_RUNTIME or lexical.is_relative_to(BASE / "Lib"),
                        "No unknown author/cache route; absent stdlib cache is not promoted to dependency")

def full_active_owner(name, snapshot, archive_routes):
    """Retain every original field, key and owner; bind explicit role union only."""
    manifest = read(bind(ROOT / snapshot["manifest_path"], snapshot["literal_expected_manifest_SHA256"]))
    for field, row in snapshot["complete_original_declared_maps_with_field_presence"].items():
        require(row["original_field_present"] == (field in manifest)
                and row["complete_original_map"] == manifest.get(field), "Original map field presence and bytes")
    legacy = snapshot["complete_original_legacy_bare_owned_file_map"]
    require(legacy is None or (name == "A10_coefficient_run001" and legacy == manifest),
            "Original bare A10 layout, never fabricated files/frozen/runtime fields")
    directory = canonical((ROOT / snapshot["manifest_path"]).parent)
    aliases = {(r["original_owner"], r["original_map"], r["original_key"]): r for r in archive_routes}
    for field, row in snapshot["complete_original_declared_maps_with_field_presence"].items():
        if not row["original_field_present"]:
            continue
        for key, pin in row["complete_original_map"].items():
            budget()
            alias = aliases.get((name, field, key))
            if alias is not None:
                require(alias["expected_sha256"] == pin and alias["expected_hash_waived"] is False
                        and alias["current_original_path_integrity_asserted"] is False,
                        "Scoped equal-SHA archive does not assert current original integrity")
                path = ROOT / alias["verified_archived_path"]
            elif field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Original external map exact absolute key")
                path = Path(key)
            elif field == "files" and snapshot["original_files_key_layout"] == "RECEIPT_RELATIVE":
                path = directory / Path(key)
            else:
                path = ROOT / key
            bind(path, pin)
    if legacy is not None:
        for key, pin in legacy.items():
            budget()
            require(not Path(key).is_absolute() and ".." not in Path(key).parts,
                    "Exact original A10 receipt-relative backslash keys")
            bind(directory / Path(key), pin)
    members = set()
    for row in snapshot["complete_physical_receipt_inventory_expected_hashes_and_stat_only"]:
        budget()
        path = bind(ROOT / row["path"], row["expected_SHA256"])
        require(path.is_relative_to(directory) and path.stat().st_size == row["bytes_metadata_only"],
                "Complete physical original receipt member, including manifest")
        members.add(path)
    require(inventory(directory) == members, "Complete original owned physical inventory")
    _OWN_INVENTORIES[directory] = members
    for row in snapshot["original_declared_external_owned_artifacts"]:
        require(row["exists_metadata_only"] is True, "Original external-owned document remains explicit")
        bind(ROOT / row["path"], row["expected_SHA256"])
    return {"manifest_expected_SHA256": snapshot["literal_expected_manifest_SHA256"],
            "original_map_counts": snapshot["original_map_counts"], "original_files_key_layout": snapshot["original_files_key_layout"],
            "original_field_presence": {k: r["original_field_present"] for k, r in snapshot["complete_original_declared_maps_with_field_presence"].items()},
            "full_original_snapshot": snapshot, "no_recursive_nested_owner_success_or_runtime_promotion": True}

def archive_owned_custody(name, snapshot):
    """Opaque manifest/maps and exact explicit owned bytes; no archived recursive maps."""
    manifest = read(bind(ROOT / snapshot["manifest_path"], snapshot["literal_expected_manifest_SHA256"]))
    for field, original in snapshot["complete_original_declared_maps_with_field_presence"].items():
        require(original["original_field_present"] == (field in manifest)
                and original["complete_original_map"] == manifest.get(field),
                "Archive literal field presence/maps preserved without runtime promotion")
    legacy = snapshot["complete_original_legacy_bare_owned_file_map"]
    require(legacy is None or legacy == manifest, "Archived bare manifest remains original")
    directory = canonical((ROOT / snapshot["manifest_path"]).parent)
    members = set()
    for row in snapshot["complete_physical_receipt_inventory_expected_hashes_and_stat_only"]:
        path = bind(ROOT / row["path"], row["expected_SHA256"])
        require(path.is_relative_to(directory) and path.stat().st_size == row["bytes_metadata_only"]
                and path not in members, "Exact opaque original archived owned custody")
        members.add(path)
    require(inventory(directory) == members, "Exact archived physical inventory without a success assertion")
    _OWN_INVENTORIES[directory] = members
    for row in snapshot["original_declared_external_owned_artifacts"]:
        require(row["exists_metadata_only"] is True, "Explicit archival external-owned custody")
        bind(ROOT / row["path"], row["expected_SHA256"])
    return {"name": name, "manifest_expected_SHA256": snapshot["literal_expected_manifest_SHA256"],
            "original_maps_canonical_SHA256": object_sha(snapshot), "physical_owned_files": len(members),
            "role": "opaque citation/failure custody only; no archived recursive runtime or scientific success"}

def checked_ratio(pair):
    budget()
    require(type(pair) is list and len(pair) == 2 and all(type(v) is int for v in pair)
            and pair[1] > 0 and max(abs(v).bit_length() for v in pair) <= INTEGER_SERIALIZATION_BITS,
            "Bounded exact saved rational pair, no floats or implicit parameter replacement")
    value = Fraction(pair[0], pair[1])
    return rational_guard(value)

def rational_guard(value):
    budget()
    require(type(value) is Fraction and max(abs(value.numerator).bit_length(), value.denominator.bit_length())
            <= MAX_REDUCED_RATIONAL_BITS, "Fixed reduced-rational cap")
    return value

def plus(a, b):
    budget()
    require(max(abs(a.numerator).bit_length() + b.denominator.bit_length(),
                abs(b.numerator).bit_length() + a.denominator.bit_length()) + 1 <= MAX_ANALYTIC_TEMP_BITS
            and a.denominator.bit_length() + b.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS,
            "Finite numerator sum temporary cap before operation")
    return rational_guard(a + b)

def times(a, b):
    budget()
    require(abs(a.numerator).bit_length() + abs(b.numerator).bit_length() <= MAX_ANALYTIC_TEMP_BITS
            and a.denominator.bit_length() + b.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS,
            "Finite product temporary caps before operation")
    return rational_guard(a * b)

def pair_literal(value):
    rational_guard(value)
    require(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= INTEGER_SERIALIZATION_BITS,
            "Every saved exact rational within original serialization bit cap")
    return [value.numerator, value.denominator]

def startup_decimal_policy():
    require("PYTHONINTMAXSTRDIGITS" not in os.environ and "int_max_str_digits" not in sys._xoptions
            and sys.flags.int_max_str_digits == sys.get_int_max_str_digits()
            == sys.int_info.default_max_str_digits == 4300,
            "Externally accepted original default4300 policy before admissions")

def exact_startup_literals(ready, policy, ready_sha):
    require(ready["exact_startup_literals"] == policy["exact_startup_literals"] == EXACT_STARTUP,
            "Literal original launcher/base/search/exclusion/zip contract in policy and READY")
    require(str(ROOT).replace("\\", "/") == EXACT_STARTUP["workspace_cwd"]
            and str(LAUNCHER).replace("\\", "/") == EXACT_STARTUP["launcher"]
            and str(BASE).replace("\\", "/") == EXACT_STARTUP["base_prefix_and_no_site_prefix"]
            and sys.path == EXACT_STARTUP["ordered_exact_sys_path"], "Actual startup matches external literals")
    require(sys.orig_argv[1:] == ["-I", "-S", "-B", str(AUTHOR), "--ready-sha256", ready_sha],
            "Exact new direct-script route and external READY argument")

def stable_expected_bytes(path, expected, limit):
    """Read at most the predeclared size+1 before parsing admitted bytes."""
    global _HASH_WORK
    budget()
    actual = canonical(path, fresh=True)
    require(type(expected) is str and len(expected) == 64 and actual.is_file(), "Expected regular byte source")
    before = fingerprint(actual)
    require(0 <= before[2] <= limit, "Pre-read finite size cap")
    with actual.open("rb") as stream:
        raw = stream.read(before[2] + 1)
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2] and fingerprint(actual) == before
            and canonical(actual, fresh=True) == actual and hashlib.sha256(raw).hexdigest() == expected,
            "Charged bounded stable expected bytes before parse")
    require(actual not in _OBSERVED or _OBSERVED[actual] == expected, "Observed expected bytes stable")
    _OBSERVED[actual] = expected
    _HASH_CACHE[actual] = (before, expected)
    budget()
    return raw

def bootstrap_json(path, expected):
    actual = add(path, expected)
    return json.loads(stable_expected_bytes(actual, expected, MAX_OWN_BYTES))

def read(path):
    actual = canonical(path, fresh=True)
    mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
    key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
    require(key in mapping, "Expected JSON authority precedes byte read")
    result = json.loads(stable_expected_bytes(actual, mapping[key], MAX_OWN_BYTES))
    guard_serialization_integers(result)
    return result

def source_code_guard():
    key = AUTHOR.relative_to(ROOT).as_posix()
    require(key in _FROZEN, "Current source expected before compilation")
    raw = stable_expected_bytes(AUTHOR, _FROZEN[key], 8 << 20)
    tree = ast.parse(raw)
    definitions = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    functions = {name: node for name, node in definitions.items() if isinstance(node, ast.FunctionDef)}
    compiled = compile(raw, str(AUTHOR), "exec", dont_inherit=True, optimize=0)
    codes = {node.co_name: node for node in compiled.co_consts if isinstance(node, types.CodeType) and node.co_name in functions}
    require(set(codes) == set(functions), "Every current function compiled without executing module")
    for name in functions:
        budget()
        function = globals()[name]
        require(type(function) is types.FunctionType and function.__globals__ is globals()
                and function.__code__ == codes[name], "Current loaded function equals admitted compiled code")
    classes = {name: node for name, node in definitions.items() if isinstance(node, ast.ClassDef)}
    require(set(classes) == {"E11FirstStockReject"} and len(classes["E11FirstStockReject"].body) == 1
            and isinstance(classes["E11FirstStockReject"].body[0], ast.Pass)
            and classes["E11FirstStockReject"].decorator_list == [], "Dedicated current plain-pass exception AST")
    require(type(E11FirstStockReject) is type and E11FirstStockReject.__bases__ == (ValueError,)
            and E11FirstStockReject.__module__ == __name__ and E11FirstStockReject.__name__ == "E11FirstStockReject"
            and E11FirstStockReject.__qualname__ == "E11FirstStockReject", "Exact current exception identity")

def definition_AST_pins():
    key = AUTHOR.relative_to(ROOT).as_posix()
    require(key in _FROZEN, "Current source expected before AST witness")
    raw = stable_expected_bytes(AUTHOR, _FROZEN[key], 8 << 20)
    tree = ast.parse(raw)
    return {node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}

def code_cache_policy(ready):
    all_paths = sorted("research/limitation_program_20261001/__pycache__/" + AUTHOR.stem + ".cpython-312" + suffix + ".pyc"
                       for suffix in ("", ".opt-1", ".opt-2"))
    expected, absent = ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    require(type(expected) is dict and set(expected) <= set(all_paths) and type(absent) is list
            and absent == sorted(set(all_paths) - set(expected)), "Exact sorted current three-cache partition")
    for key in all_paths:
        path = exact_key(key)
        if key in expected:
            require(path.exists(), "Declared present current cache")
            _CODE_CACHE_EXPECTED[bind(path, expected[key])] = expected[key]
        else:
            require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
                    "Declared absent current cache remains exact physical route")
            _ABSENT_RUNTIME.add(path)

def invocation_check():
    require(sys.version_info[:3] == (3, 12, 4) and sys.flags.isolated == 1 and sys.flags.no_site == 1
            and sys.dont_write_bytecode and sys.flags.optimize == 0 and "PYTHONOPTIMIZE" not in os.environ,
            "Pinned Python3.12.4 isolated -I -S -B direct script")
    require(canonical(Path.cwd(), fresh=True) == ROOT and canonical(__file__, fresh=True) == AUTHOR,
            "Current absolute controller and workspace")
    require(canonical(sys.executable, fresh=True) == LAUNCHER and canonical(sys.base_prefix, fresh=True) == BASE
            and canonical(sys.prefix, fresh=True) == BASE, "Original no-site launcher/base/prefix")
    require(sys.path == EXACT_STARTUP["ordered_exact_sys_path"], "Original exact four-entry search path")
    path = BASE / "python312.zip"
    require(not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path, "Original absent zip")
    _ABSENT_RUNTIME.add(path)
    require("site" not in sys.modules and not any(name.startswith("research.") for name in sys.modules), "No site/source imports")

def current_review_admission(ready, authors):
    expected = ready["static_review_expected_SHA256"]
    require(type(expected) is dict and set(expected) == set(CURRENT_REVIEW_PATHS), "Exact current three static reviews")
    records = {}
    for key in CURRENT_REVIEW_PATHS:
        record = bootstrap_json(ROOT / key, expected[key])
        require(record["passed"] is record["science_static_passed"] is record["lifecycle_static_passed"] is True
                and record["blockers"] == [] and record["author_method_SHA256"] == authors,
                "Every current review covers exact trio/science/lifecycle before origins")
        if key == AUTHOR_QA_KEY:
            require(record["target_imported_or_executed"] is record["scientific_evaluation_performed"] is False,
                    "Author QA metadata and AST only")
        records[key] = {"expected_SHA256": expected[key], "direct_current_input_member": key in _FROZEN}
    require(all(row["direct_current_input_member"] for row in records.values()), "Current reviews direct before runtime")
    return records

def cfg_admission():
    key = CFG_EXPECTED["path"]
    pin = CFG_EXPECTED["expected_SHA256"]
    raw = stable_expected_bytes(add(ROOT / key, pin), pin, 8 << 20)
    text = raw.decode("utf-8")
    fields = {}
    for line in text.splitlines():
        if "=" in line:
            name, value = line.split("=", 1)
            require(name.strip().lower() not in fields, "No duplicate cfg key")
            fields[name.strip().lower()] = value.strip()
    require(fields.get("include-system-site-packages", "").lower() == "false", "Original isolated cfg")
    return {"path": key, "expected_SHA256": pin, "bounded_UTF8_false_site_cfg": True}

def known_runtime_admission(original_native_manifest):
    global _STANDARD_RUNTIME_MEMBERS
    expected = original_native_manifest["external_runtime_inputs"]
    require(type(expected) is dict and len(expected) == 2842 and object_sha(expected) == RUNTIME_EXTERNAL_MAP_SHA256,
            "Exact original complete2842 expected runtime map before enumeration")
    required = {Path(key) for key in expected} | {LAUNCHER}
    require(all(Path(key).is_absolute() for key in expected), "Original absolute external runtime spelling")
    members = standard_runtime_members()
    require(members == required and len(members) == 2843, "Original strict candidate set before current byte observations")
    _STANDARD_RUNTIME_MEMBERS = required
    bind(LAUNCHER, LAUNCHER_SHA)
    for key, pin in expected.items(): bind(Path(key), pin)
    require(expected[str(BASE / "python.exe")] == BASE_SHA, "Second original interpreter pin")
    size = 0
    for path in members:
        budget()
        size += path.stat().st_size
        require(size <= MAX_RUNTIME_BYTES, "Original512MiB runtime cap")
    return {"files": len(members), "bytes": size, "original2842_plus_launcher_exact": True,
            "candidate_equality_before_current_hashes": True, "no_site_or_numeric_packages": True}

def checked_stock_method_graph(method, supplement):
    require(method["selected_original_first_log_contract_unchanged"] == SELECTED_LOG
            and method["selected_original_first_stock_source_site"] == SELECTED_SITE
            and method["prospective_first_stock_projection_Gaussian_moment_theorem"] == THEOREM,
            "Exact original source and accepted projection/two-tail theorem")
    require(method["finite_protocol_unevaluated"] == COMMON_EXPECTATIONS["finite_protocol"]
            and method["two_separate_original_first_stock_profile_adapters"] == PROFILE_CONTRACT,
            "Own fixed two-profile adapters and two assemblies")
    original_shared = supplement["prospective_full_READY_policy_field_role_graph"]["fixed_shared_values"]
    require(original_shared == ORIGINAL_V1_FIXED_SHARED, "Every historical V1 shared value preserved exactly")
    for key, value in original_shared.items():
        if key not in V2_METADATA_OVERRIDE_FIELDS:
            require(COMMON_EXPECTATIONS[key] == value, "Original scientific owner cap shared field exact")
    require(supplement["prospective_exact27_inclusive_owned_ledger"] == PLANNED_FILES
            and method["prospective_fixed_inclusive_owned_ledger"] == PLANNED_FILES
            and method["original_caps_prospective_unchanged"] == COMMON_EXPECTATIONS["original_caps"], "Exact27 and unchanged caps")
    snapshots = method["complete_original_cited_owner_snapshots"]
    require(set(snapshots) == set(ACTIVE_OWNERS) | set(ARCHIVE_CITATIONS) and len(snapshots) == 18,
            "All18/active10/archive8 original owners only")
    require({name: object_sha(value) for name, value in snapshots.items()} == ROLE_GRAPH["all18_snapshot_canonical_JSON_SHA256"],
            "Original raw snapshots full canonical commitments")
    for profile, adapter in PROFILE_CONTRACT.items():
        require(object_sha(adapter) == COMMON_EXPECTATIONS["two_profile_adapter_commitments"][profile], "Own adapter full canonical pin")
    old_acceptance = read(ROOT / ORIGINAL_V1_ACCEPTANCE_KEY)
    require(old_acceptance["passed"] is old_acceptance["controller_authoring_authorized"] is True
            and old_acceptance["READY_or_SCI_execution_authorized"] is False
            and old_acceptance["exact_future_routes"] == supplement["future_routes"],
            "Original V1 authoring receipt historical only and unchanged")
    cache_method = read(ROOT / CACHE_METHOD_KEY)
    require(cache_method["future_routes"] == CURRENT_V2_ROUTES
            and cache_method["original18_snapshot_canonical_JSON_SHA256"] == ROLE_GRAPH["all18_snapshot_canonical_JSON_SHA256"]
            and cache_method["exact27_inclusive_owned_ledger"] == PLANNED_FILES
            and cache_method["original_caps_exact"] == COMMON_EXPECTATIONS["original_caps"],
            "V2 metadata correction preserves original owner science and caps")
    acceptance = read(ROOT / COMMON_EXPECTATIONS["current_authoring_acceptance_path"])
    require(acceptance["passed"] is acceptance["controller_authoring_authorized"] is True
            and acceptance["READY_or_SCI_execution_authorized"] is False
            and acceptance["exact_future_routes"] == CURRENT_V2_ROUTES
            and acceptance["accepted_method_MD_QA_independent_ROOT_expected_SHA256"] == CACHE_METHOD_AUTHORITY,
            "Current V2 authoring receipt independent of original V1 route metadata")

def admit_stock_history_roles(method, ready):
    require(ready["historical_cache_partitions"] == HISTORICAL_CACHE_PARTITIONS, "Original four plus failed stock V1 historical namespaces")
    require(HISTORICAL_READY_PATHS["completed_first_log_V3"] == OLD_LOG_READY_KEY, "Exact original log READY namespace")
    for label, key in HISTORICAL_READY_PATHS.items():
        require(key in _FROZEN, "Old READY has expected historical authority before read")
        old = read(ROOT / key)
        require({"existing_expected_SHA256": old["existing_new_code_cache_SHA256"],
                 "absent_paths": old["absent_new_code_cache_paths"]} == HISTORICAL_CACHE_PARTITIONS[label],
                "Own original historical READY/cache join, including completedfirstlogV3")
        historical_code_cache_partition(ROOT / HISTORICAL_SOURCE_PATHS[label], HISTORICAL_CACHE_PARTITIONS[label])
    retain_failed_e11_v1()
    for name, pin in FAILED_E11_V1_HISTORY["author_method_SHA256"].items(): bind(RESEARCH / name, pin)
    for key, pin in FAILED_E11_V1_HISTORY["static_review_expected_SHA256"].items(): bind(ROOT / key, pin)
    for key, pin in HELD_HISTORY_EXPECTED.items(): bind(ROOT / key, pin)
    require(HISTORICAL_CACHE_PARTITIONS["failed_scalar_V1"] == FAILED_E11_V1_HISTORY["cache_partition"], "Exact failed namespace")
    return {"all4_actual_historical_namespace_consumers": True, "completed_firstlog_V3_JOIN_original_READY": OLD_LOG_READY_KEY,
            "failed19_and_heldV1V2_preserved_only": True, "old_execution_grants_inherited": False, "failed_stockV1_actual_three_cache_repeated": True, "failed_stockV1_not_success_owner": True}

def first_stock_admission(ready_sha):
    global _FULL_ADMISSION
    require(type(_FULL_ADMISSION) is bool and _FULL_ADMISSION is False, "Single initialized admission epoch; no reentry")
    startup_decimal_policy()
    ready = bootstrap_json(READY, ready_sha)
    require(set(ready) == set(READY_FIELDS) and ready["schema"] == "root-e11-first-stock-squared-L2-READY-v1"
            and ready["ready"] is ready["root_and_independent_static_reviews_passed"] is ready["first_stock_rational_assembly_authorized"] is True,
            "Closed65-field separate one-stock ROOT grant")
    authors = ready["author_method_SHA256"]
    require(type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, "Exact current trio")
    for name, pin in authors.items(): add(RESEARCH / name, pin)
    policy = bootstrap_json(PREFLIGHT, authors[PREFLIGHT.name])
    require(set(policy) == set(POLICY_FIELDS) and policy["schema"] == "e11-first-stock-squared-L2-preflight-v1"
            and policy["first_stock_rational_assembly_authorized"] is False
            and policy["author_SHA256"] == authors[AUTHOR.name] and policy["method_SHA256"] == authors[METHOD_DOC.name]
            and policy["ROOT_READY"] == READY.relative_to(ROOT).as_posix()
            and policy["ROOT_READY_schema"] == ready["schema"], "Closed64-field dormant policy distinct from ROOT")
    for key, value in COMMON_EXPECTATIONS.items(): require(policy[key] == ready[key] == value, "Exact current shared field role")
    for key, value in FLAGS.items(): require(policy[key] == ready[key] == value, "All qualification permissions fixed")
    exact_startup_literals(ready, policy, ready_sha)
    code_cache_policy(ready)
    for key, pin in AUTHOR_INPUTS.items(): add(ROOT / key, pin)
    current_reviews = current_review_admission(ready, authors)
    for name, pin in authors.items(): bind(RESEARCH / name, pin)
    for key, pin in AUTHOR_INPUTS.items(): bind(ROOT / key, pin)
    cache_method = bootstrap_json(ROOT / CACHE_METHOD_KEY, AUTHOR_INPUTS[CACHE_METHOD_KEY])
    acceptance = bootstrap_json(ROOT / COMMON_EXPECTATIONS["current_authoring_acceptance_path"],
                                COMMON_EXPECTATIONS["current_authoring_acceptance_SHA256"])
    require(cache_method["passed"] is True and cache_method["blockers"] == []
            and cache_method["controller_authoring_authorized"] is cache_method["READY_or_SCI_execution_authorized"] is False
            and cache_method["future_routes"] == CURRENT_V2_ROUTES,
            "Exact accepted V2 METHOD is planning metadata only before runtime")
    require(acceptance["passed"] is acceptance["controller_authoring_authorized"] is True
            and acceptance["READY_or_SCI_execution_authorized"] is False
            and acceptance["accepted_method_MD_QA_independent_ROOT_expected_SHA256"] == CACHE_METHOD_AUTHORITY
            and acceptance["exact_future_routes"] == CURRENT_V2_ROUTES
            and acceptance["unchanged_caps"] == COMMON_EXPECTATIONS["original_caps"]
            and acceptance["exact_manifest_inclusive_owned_ledger"] == PLANNED_FILES,
            "Direct V2 authoring acceptance covers exact routes without a scientific grant")
    for key in (CURRENT_V2_ROUTES["independent_METHOD_peer"], CURRENT_V2_ROUTES["ROOT_METHOD_review"]):
        review = bootstrap_json(ROOT / key, AUTHOR_INPUTS[key])
        require(review["passed"] is review["science_static_passed"] is review["lifecycle_static_passed"] is True
                and review["blockers"] == [] and review["reviewed_METHOD_path"] == CACHE_METHOD_KEY
                and review["reviewed_METHOD_SHA256"] == AUTHOR_INPUTS[CACHE_METHOD_KEY],
                "Separate V2 METHOD reviews direct before runtime origins and digits")
    failed_stock_history = admit_first_stock_v1_preoutput_history()
    cfg = cfg_admission()
    method = bootstrap_json(ROOT / METHOD_KEY, AUTHOR_INPUTS[METHOD_KEY])
    supplement = bootstrap_json(ROOT / SUPPLEMENT_KEY, AUTHOR_INPUTS[SUPPLEMENT_KEY])
    native = method["complete_original_cited_owner_snapshots"]["E11_native_coordinate_squared_L2_run001"]
    require(object_sha(native) == NATIVE_SNAPSHOT_COMMITMENT, "Original native snapshot before runtime")
    native_manifest = bootstrap_json(ROOT / native["manifest_path"], native["literal_expected_manifest_SHA256"])
    require(native_manifest["passed"] is native_manifest["completed"] is True and native_manifest["budget_censored"] is False,
            "Scoped completed prerequisite no inherited grant")
    runtime = known_runtime_admission(native_manifest)
    serialization_runtime_admission()
    source_code_guard()
    require(policy["current_definition_AST_SHA256"] == definition_AST_pins(), "Every current function and class AST")
    strict_loaded_origins()
    fixed_integer_policy()
    checked_stock_method_graph(method, supplement)
    snapshots = method["complete_original_cited_owner_snapshots"]
    owners = {}
    for name in ACTIVE_OWNERS:
        full_active_owner(name, snapshots[name], ROLE_GRAPH["three_original_equal_SHA_archive_aliases"])
        owners[name] = ROLE_GRAPH["owner_summaries"][name]
    archive = {name: archive_owned_custody(name, snapshots[name]) for name in ARCHIVE_CITATIONS}
    histories = admit_stock_history_roles(method, ready)
    strict_loaded_origins()
    require(type(_FULL_ADMISSION) is bool and _FULL_ADMISSION is False, "Close one admission cache epoch before either union")
    _FULL_ADMISSION = True
    return ready, policy, method, supplement, owners, archive, histories, runtime, current_reviews, cfg

def fresh_first_stock_union():
    require(_FULL_ADMISSION is True, "Full current admission before either union")
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical, fresh=True) == actual, "Every lexical input stays confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(not path.is_relative_to(OUTPUT) and (path not in union or union[path] == pin), "Expected input only and exact overlap")
            union[path] = pin
    for path, pin in _OBSERVED.items():
        if path.is_relative_to(OUTPUT): continue
        require(path in union and union[path] == pin, "Every nonoutput observation already has equal original expected authority")
    require(len(union) <= MAX_REFERENCES, "Finite unique input references")
    size = 0
    for path, pin in sorted(union.items()):
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES and digest(actual, fresh=True, already_resolved=True) == pin, "Full uncached expected input union")
    for directory, members in _OWN_INVENTORIES.items(): require(inventory(directory) == members, "All18 and failed19 exact inventories")
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS, "Exact strict2842+launcher membership repeated")
    for label, partition in HISTORICAL_CACHE_PARTITIONS.items():
        historical_code_cache_partition(ROOT / HISTORICAL_SOURCE_PATHS[label], partition)
    require(not any(path.exists() or path.is_symlink() or path.resolve(strict=False) != path for path in _ABSENT_RUNTIME), "All exact absences repeated")
    for path, pin in _CODE_CACHE_EXPECTED.items(): require(digest(path, fresh=True) == pin, "All present declared caches exact")
    require(all(key in _FROZEN for key in CURRENT_REVIEW_PATHS) and all(key in _FROZEN for key in AUTHOR_INPUTS), "All current reviews/METHOD direct membership")
    cfg_admission()
    serialization_runtime_admission()
    source_code_guard()
    strict_loaded_origins()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_physical_resolve_stat_SHA": True,
            "active10": ACTIVE_OWNERS, "archive8_opaque_custody_only": ARCHIVE_CITATIONS,
            "current_reviews_direct_expected_members": CURRENT_REVIEW_PATHS,
            "all4_historical_three_cache_partitions_repeated": True, "owned_generated_evidence_excluded_from_input_expectations": True,
            "absent_paths": sorted(str(path) for path in _ABSENT_RUNTIME),
            "owned_inventory_identity_SHA256": {str(directory): object_sha(sorted(str(path) for path in members)) for directory, members in _OWN_INVENTORIES.items()}}

def output_directory_identity():
    require(OUTPUT.is_dir() and not OUTPUT.is_symlink() and OUTPUT.resolve(strict=True) == OUTPUT,
            "Owned output has exact physical route")
    stat = OUTPUT.stat()
    return (stat.st_dev, stat.st_ino, getattr(stat, "st_birthtime_ns", stat.st_ctime_ns),
            stat.st_mode, getattr(stat, "st_file_attributes", None), getattr(stat, "st_reparse_tag", None))

def owned_output_guard():
    require(_OUTPUT_CREATED_BY_THIS_RUN is True and _OUTPUT_DIRECTORY_IDENTITY is not None
            and output_directory_identity() == _OUTPUT_DIRECTORY_IDENTITY, "Only this invocation unchanged exclusive output")

def save(name, value):
    budget()
    owned_output_guard()
    require(name in PLANNED_FILES or name == "failure.json", "Finite registered metadata emitter")
    target = OUTPUT / name
    require(target.parent == OUTPUT and not target.exists() and not target.is_symlink(), "Exclusive metadata output")
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
    require(len(members) + 1 + (name != "manifest.json") <= MAX_OWN_FILES
            and current_bytes + new_bytes <= MAX_OWN_BYTES, "Inclusive file/byte cap with manifest reserve")
    owned_output_guard()
    with target.open("xb") as stream:
        for piece in pieces:
            budget()
            owned_output_guard()
            stream.write(piece)
    owned_output_guard()
    require(target.stat().st_size == new_bytes, "Exactly admitted output bytes")
    budget()

def copy(path, name):
    budget()
    owned_output_guard()
    require(name in PLANNED_FILES, "Finite registered copy emitter")
    source = canonical(path, fresh=True)
    key = source.relative_to(ROOT).as_posix() if source.is_relative_to(ROOT) else str(source)
    mapping = _FROZEN if source.is_relative_to(ROOT) else _EXTERNAL
    require(key in mapping, "Copied source already has original expected pin")
    before, expected = fingerprint(source), mapping[key]
    require(digest(source, fresh=True) == expected, "Copied original input exact")
    target = OUTPUT / name
    members = inventory(OUTPUT)
    require(target.parent == OUTPUT and not target.exists() and not target.is_symlink(), "New registered copied output")
    current_bytes = 0
    for member in members:
        budget()
        current_bytes += member.stat().st_size
    require(len(members) + 2 <= MAX_OWN_FILES and current_bytes + before[2] <= MAX_OWN_BYTES, "Copy including MF reserve")
    total = 0
    owned_output_guard()
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(65536):
            budget()
            owned_output_guard()
            total += len(block)
            require(total <= before[2], "Copied source cannot grow")
            outgoing.write(block)
    owned_output_guard()
    require(total == before[2] and fingerprint(source) == before and canonical(source, fresh=True) == source,
            "Stable complete confined original copy")
    require(digest(target, fresh=True) == expected, "Copied expected bytes exact, output observation only")

def complete_manifest(value, owned, nonmanifest_bytes):
    budget()
    owned_output_guard()
    require(set(owned) == set(PLANNED_FILES) - {"manifest.json"} and len(owned) == 26, "Exact26 preseal emitter ledger")
    value["manifest_inclusive_owned_file_count"] = 27
    value["owned_nonmanifest_bytes"] = nonmanifest_bytes
    value["manifest_inclusive_retention_checked_before_sealing"] = True
    value["completion_requires_absent_failure_and_censor_markers"] = True
    guard_serialization_integers(value)
    manifest_bytes = 1
    for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(value):
        budget()
        manifest_bytes += len(fragment.encode("utf-8"))
        require(nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES, "Manifest-inclusive128MiB cap")
    save("manifest.json", value)
    owned_output_guard()
    require((OUTPUT / "manifest.json").stat().st_size == manifest_bytes, "Exact manifest bytes")
    actual = inventory(OUTPUT)
    require(actual == {OUTPUT / name for name in PLANNED_FILES} and len(actual) == 27 <= MAX_OWN_FILES,
            "Exact27 complete manifest-inclusive physical inventory")
    total = 0
    for path in actual:
        budget()
        total += path.stat().st_size
    require(total == nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES, "Complete inclusive retention")
    require(not (OUTPUT / "failure.json").exists() and not (OUTPUT / "FAILED_UNSEALED.json").exists(), "No failure/censor marker")
    owned_output_guard()
    budget()

def retain_failure(error):
    """Failure invalidates completion, including a failure after a manifest exists."""
    try:
        owned_output_guard()
    except BaseException:
        return
    try:
        save("failure.json", {"passed": False, "completed": False, "error_type": type(error).__name__,
                              "error": str(error)[:4096], "traceback": traceback.format_exc()[-16384:], **flags()})
    except BaseException:
        pass
    try:
        owned_output_guard()
        marker = OUTPUT / "FAILED_UNSEALED.json"
        raw = b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"fixture_credit":0,"postseal_marker_invalidates_completion":true}\n'
        entries = list(OUTPUT.iterdir())
        require(len(entries) + 1 <= MAX_OWN_FILES and all(path.is_file() and not path.is_symlink() for path in entries), "Bounded failure marker inventory")
        require(sum(path.stat().st_size for path in entries) + len(raw) <= MAX_OWN_BYTES, "Failure marker stays original byte cap")
        owned_output_guard()
        with marker.open("xb") as stream:
            owned_output_guard()
            stream.write(raw)
    except BaseException:
        pass

class E11FirstStockReject(ValueError):
    pass

def valid_first_stock_scope(scope):
    if any(type(scope.get(key)) is not type(POSITIVE_SCOPE[key]) or scope.get(key) != POSITIVE_SCOPE[key]
           for key in ("case", "asset_zero_based", "contractual_date_one_based", "saved_date_zero_based", "raw_log", "clipped_log", "stock")):
        raise E11FirstStockReject("E11_FIRST_STOCK_SOURCE_SCOPE")
    if (type(scope.get("extra_spot_multiplier")) is not int or scope.get("extra_spot_multiplier") != 1
            or scope.get("units") != "dollars_squared" or scope.get("initial_ln100_already_in_log") is not True):
        raise E11FirstStockReject("E11_FIRST_STOCK_UNITS_SPOT")
    if (type(scope.get("M")) is not int or scope.get("M") != 256
            or type(scope.get("even_moment_order")) is not int or scope.get("even_moment_order") != 32
            or type(scope.get("moment_half_order")) is not int or scope.get("moment_half_order") != 16
            or scope.get("lower_tail_paid") is not True or scope.get("upper_tail_paid") is not True
            or scope.get("native_pair_independence_assumed") is not False):
        raise E11FirstStockReject("E11_FIRST_STOCK_TAIL_PROOF")
    if (scope.get("primary90_e0_from_profile") != "primary90"
            or scope.get("independent130_alpha_from_profile") != "independent130"):
        raise E11FirstStockReject("E11_FIRST_STOCK_PROFILE_AUTHORITY")
    return True

def metadata_pointer(value, parts):
    for part in parts:
        budget()
        value = value[part]
    return value

def source_first_stock_witness(method):
    target_key = SELECTED_LOG["target_path"]
    target = read(ROOT / target_key)
    require(digest(ROOT / target_key, fresh=True) == SELECTED_LOG["target_literal_SHA256"], "Original exact target witness")
    require(target["width"] == 72 and target["fraction_bits"] == 40, "Original signed72/F40 target")
    values = {value: row for row in target["nodes"] for value in row["out"]}
    closure = method["selected_original_stock_source_node_closure_readonly"]
    require(object_sha(closure) == STOCK_NODE_CLOSURE_SHA256 and len(closure) == 45, "Exactly45 original stock nodes")
    require(all(values[row["out"][0]] == row for row in closure), "Original fixed stock closure copied from saved target, no build/evaluate")
    require(method["selected_original_first_stock_source_site"] == SELECTED_SITE
            and values[4021]["args"] == [4020, 3979] and values[4021]["op"] == "shift", "Actual stock shift joins exponent and polynomial")
    selected_raw = [values[row["out"][0]] for row in SELECTED_LOG["source_seven_node_slice_saved_metadata"]]
    require(selected_raw == SELECTED_LOG["source_seven_node_slice_saved_metadata"], "Original raw3542 signed product/add witness")
    clamp = [values[value] for value in (3576, 3577, 3578, 3579)]
    require([row["op"] for row in clamp] == ["lt", "select", "lt", "select"]
            and [row["args"] for row in clamp] == [[3542, 3490], [3576, 3490, 3542], [3577, 3491], [3578, 3577, 3491]],
            "Original native clamp structure and no source insertion")
    require(SELECTED_SITE["low"] < THEOREM["native_all_input_interval_raw"][0]
            <= THEOREM["native_all_input_interval_raw"][1] < SELECTED_SITE["high"],
            "Unconditional native interval strictly inside original clamp at only this site")
    witnesses = {}
    for key, row in method["original_source_AST_witnesses_readonly"].items():
        source_key, name = key.split("::")
        require(source_key in _FROZEN, "Original plaintext source expected before AST read")
        raw = stable_expected_bytes(ROOT / source_key, _FROZEN[source_key], 8 << 20)
        text = raw.decode("utf-8")
        definitions = {node.name: node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef)}
        node = definitions[name]
        require(ast.get_source_segment(text, node) == row["definition_text_readonly"]
                and hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest() == row["normalized_AST_SHA256"],
                "Actual original build/exp/native shift definitions plaintext only")
        witnesses[key] = row["normalized_AST_SHA256"]
    require(method["selected_independent130_stock_scope"]["actual_original_support_signature"]
            == SELECTED_SITE["actual_original_support_signature"], "Own independent original source support signature")
    positive = dict(POSITIVE_SCOPE)
    valid_first_stock_scope(positive)
    return positive, {"selected_site": SELECTED_SITE, "original_raw_log_contract": SELECTED_LOG,
                      "stock45node_canonical_JSON_SHA256": STOCK_NODE_CLOSURE_SHA256,
                      "original_AST_pins_plaintext_only": witnesses,
                      "native_clamp_inactive_unconditionally_at_this_site_only": True,
                      "continuous_L_unbounded_both_tails_still_required": True,
                      "source_or_array_regenerated_or_evaluated": False}

def literal_first_stock_inputs(method):
    inputs = {}
    for profile, adapter in PROFILE_CONTRACT.items():
        require(adapter == method["two_separate_original_first_stock_profile_adapters"][profile]
                and adapter["profile"] == profile, "Exact own complete stock adapter")
        record = read(bind(ROOT / adapter["B_log_saved_record_path"], adapter["B_log_saved_record_expected_SHA256"]))
        require(record["profile"] == profile and record[adapter["B_log_original_saved_field"]] == adapter["B_log_original_literal_pair"],
                "Own completed first-log B, never coordinate predecessor")
        values = {"B_log": adapter["B_log_original_literal_pair"]}
        for role, prefix in (("e0", "e0"), ("alpha", "alpha"), ("beta", "beta"), ("ln2_lower", "ln2_lower")):
            path_role = "alpha_beta" if role in ("alpha", "beta") else role
            saved = read(bind(ROOT / adapter[path_role + "_original_record_path"], adapter[path_role + "_original_record_expected_SHA256"]))
            literal = metadata_pointer(saved, adapter[prefix + "_original_field"])
            require(literal == adapter[prefix + "_original_literal_pair"], "Each own original rational field pointer/literal")
            values[role] = literal
        prior = adapter["complete_previous_first_log_adapter_unchanged"]
        envelope = read(bind(ROOT / prior["path"], prior["literal_SHA256"]))
        case = envelope["cases"]["B4x12"] if profile == "primary90" else envelope["B4x12"]
        require(all(case[key] == value for key, value in prior["fields"].items()), "All original raw-prefix safety/source literal fields")
        if profile == "primary90":
            require(case["every_signed144_scaled_normal_product_safe"] is True
                    and case["every_stored72_raw_partial_sum_safe"] is True
                    and case["signed_scaled_normal_floors_per_increment"] == 2
                    and case["addition_rounding_paid"] == 0, "Primary signed144/stored72/raw-floor safety")
        else:
            require(case["every_stored_partial_sum_and_product_safe"] is True
                    and case["additive_rounding_zero_only_after_no_wrap"] is True
                    and case["every_original_driver_once"] is True, "Independent original signed safety and multiplicity")
        stock_saved = read(ROOT / adapter["alpha_beta_original_record_path"])
        stock_case = stock_saved["cases"]["B4x12"] if profile == "primary90" else stock_saved["B4x12"]
        require(object_sha(stock_case) == STOCK_ENVELOPE_CASE_SHA256[profile],
                "Own complete original full-clipped-domain stock proof, literal classes/floors/signed ranges unchanged")
        if profile == "primary90":
            require(stock_case["all_positive_stock_stored72_product144_shift_guards_passed"] is True
                    and stock_case["whole_clipped_integer_domain_covered"] is True
                    and stock_case["final_negative_shift_floor_charged_once"] is True,
                    "Primary original full-clipped-domain72/144/shift guards")
        else:
            require(stock_case["original_degree12_Estrin_no_AS_certificate_transfer"] is True
                    and stock_case["inverse_ln2_raw"] == SELECTED_SITE["inverse_ln2"]
                    and stock_case["ln2_raw"] == SELECTED_SITE["ln2"],
                    "Own independent retained native degree12 proof and original constants")
        inputs[profile] = values
    return inputs

def rational_compare(a, b):
    rational_guard(a)
    rational_guard(b)
    require(abs(a.numerator).bit_length() + b.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS
            and abs(b.numerator).bit_length() + a.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS,
            "Exact comparison cross-products bounded before comparison")
    return (a > b) - (a < b)

def reciprocal_positive(value):
    rational_guard(value)
    require(value.numerator > 0, "Strict positive guard before reciprocal")
    require(max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_ANALYTIC_TEMP_BITS,
            "Finite reciprocal representation before construction")
    return rational_guard(Fraction(value.denominator, value.numerator))

def fixed_power(value, exponent):
    require(type(exponent) is int and exponent in (2, 16, 32), "Only fixed prescribed powers")
    result = Fraction(1)
    for _ in range(exponent):
        budget()
        result = times(result, value)
    return result

def primary_stock_components(inputs):
    c = {key: checked_ratio(inputs["primary90"][key]) for key in ("B_log", "e0", "alpha", "beta", "ln2_lower")}
    require(all(value.numerator >= 0 for value in c.values()), "Own primary positive original allowances")
    c["M"], c["v"] = Fraction(256), Fraction(3, 400)
    c["a"], c["b"] = Fraction(4155861047200, 1099511627776), Fraction(5968266508490, 1099511627776)
    mu_native = Fraction(5063438167381, 1099511627776)
    c["mu_lower"] = plus(plus(mu_native, -c["e0"]), Fraction(-1, 800))
    c["mu_upper"] = plus(plus(mu_native, c["e0"]), Fraction(-1, 800))
    c["lower_distance"] = plus(c["mu_lower"], -c["a"])
    c["upper_distance"] = plus(plus(c["b"], -c["mu_upper"]), -times(Fraction(2), c["v"]))
    require(rational_compare(c["b"], times(Fraction(8), c["ln2_lower"])) <= 0
            and c["lower_distance"].numerator > 0 and c["upper_distance"].numerator > 0,
            "All three own primary proof guards before either reciprocal tail")
    c["A"] = plus(times(c["alpha"], c["M"]), c["beta"])
    c["C16"] = Fraction(1)
    for factor in THEOREM["C16_unevaluated_exact_product_factors"]:
        c["C16"] = times(c["C16"], Fraction(factor))
    c["central_moment32"] = times(c["C16"], fixed_power(c["v"], 16))
    c["lower_tail"] = times(times(fixed_power(c["M"], 2), c["central_moment32"]),
                             fixed_power(reciprocal_positive(c["lower_distance"]), 32))
    c["upper_tail"] = times(times(Fraction(800000, 79), c["central_moment32"]),
                             fixed_power(reciprocal_positive(c["upper_distance"]), 32))
    return c

def independent_stock_components(inputs):
    c = {key: checked_ratio(inputs["independent130"][key]) for key in ("ln2_lower", "beta", "alpha", "e0", "B_log")}
    require(all(value.numerator >= 0 for value in c.values()), "Own independent positive original allowances")
    c["v"], c["M"] = Fraction(3, 400), Fraction(256)
    c["b"], c["a"] = Fraction(5968266508490, 1099511627776), Fraction(4155861047200, 1099511627776)
    c["mu_upper"] = plus(c["e0"], plus(Fraction(-1, 800), Fraction(5063438167381, 1099511627776)))
    c["mu_lower"] = plus(Fraction(-1, 800), plus(Fraction(5063438167381, 1099511627776), -c["e0"]))
    c["upper_distance"] = plus(-times(c["v"], Fraction(2)), plus(-c["mu_upper"], c["b"]))
    c["lower_distance"] = plus(-c["a"], c["mu_lower"])
    require(c["upper_distance"].numerator > 0 and c["lower_distance"].numerator > 0
            and rational_compare(times(c["ln2_lower"], Fraction(8)), c["b"]) >= 0,
            "All three own independent guards before reciprocal tails")
    c["A"] = plus(c["beta"], times(c["M"], c["alpha"]))
    c["C16"] = Fraction(1)
    for factor in reversed(THEOREM["C16_unevaluated_exact_product_factors"]):
        c["C16"] = times(Fraction(factor), c["C16"])
    c["central_moment32"] = times(fixed_power(c["v"], 16), c["C16"])
    c["upper_tail"] = times(fixed_power(reciprocal_positive(c["upper_distance"]), 32),
                             times(c["central_moment32"], Fraction(800000, 79)))
    c["lower_tail"] = times(fixed_power(reciprocal_positive(c["lower_distance"]), 32),
                             times(c["central_moment32"], fixed_power(c["M"], 2)))
    return c

def primary_stock_squared(c):
    stages = {"native_exponential_allowance_squared": fixed_power(c["A"], 2),
              "log_transport_M_squared_B_log": times(fixed_power(c["M"], 2), c["B_log"]),
              "lower_projection_tail": c["lower_tail"], "upper_tilted_projection_tail": c["upper_tail"]}
    bound = times(Fraction(3), plus(plus(stages["native_exponential_allowance_squared"], stages["log_transport_M_squared_B_log"]),
                                   plus(stages["lower_projection_tail"], stages["upper_tilted_projection_tail"])))
    return {"schema": "e11-first-stock-squared-L2-bound-v1", "profile": "primary90",
            "dollars_squared_stock_error_upper": pair_literal(bound),
            "existing_primary_stage_ledger": {key: pair_literal(value) for key, value in stages.items()},
            "all_three_own_profile_guards_passed": True, "M": 256, "moment_order": 32,
            "both_unconditional_continuous_tails_paid": True, "native_pair_independence_assumed": False,
            "pointwise_Cauchy_terms": 3, "extra_spot_multiplier": 1, "exact_stock_value": 4021, **flags()}

def independent_stock_squared(c):
    stages = {"upper_tilted_projection_tail": c["upper_tail"], "lower_projection_tail": c["lower_tail"],
              "log_transport_M_squared_B_log": times(c["B_log"], times(c["M"], c["M"])),
              "native_exponential_allowance_squared": times(c["A"], c["A"])}
    bound = plus(plus(times(stages["upper_tilted_projection_tail"], Fraction(3)), times(Fraction(3), stages["lower_projection_tail"])),
                 plus(times(stages["log_transport_M_squared_B_log"], Fraction(3)), times(Fraction(3), stages["native_exponential_allowance_squared"])))
    return {"schema": "e11-first-stock-squared-L2-bound-v1", "profile": "independent130",
            "dollars_squared_stock_error_upper": pair_literal(bound),
            "existing_independent_stage_ledger": {key: pair_literal(value) for key, value in stages.items()},
            "all_three_own_profile_guards_passed": True, "M": 256, "moment_order": 32,
            "both_unconditional_continuous_tails_paid": True, "native_pair_independence_assumed": False,
            "pointwise_Cauchy_terms": 3, "extra_spot_multiplier": 1, "exact_stock_value": 4021, **flags()}

def encoded_stock_components(c):
    return {"exact_rational_components": {key: pair_literal(value) for key, value in c.items()},
            "all_three_own_profile_guards_before_reciprocals": True, "fixed_M256_moment32": True,
            "both_unconditional_continuous_tails_paid": True, "stock_units": "dollars_squared", **flags()}

def independently_reconcile_stock_primary(inputs, c, result):
    require(all(c[key] == checked_ratio(inputs["primary90"][key]) for key in ("B_log", "e0", "alpha", "beta", "ln2_lower")),
            "Existing primary uses only own original profile fields")
    stages = {key: checked_ratio(value) for key, value in result["existing_primary_stage_ledger"].items()}
    require(c["A"] == plus(c["beta"], times(c["M"], c["alpha"])) and c["M"] == Fraction(256) and c["v"] == Fraction(3, 400),
            "Own stock amplitude, variance and fixed threshold identities")
    expanded_amplitude = plus(plus(times(times(c["alpha"], c["alpha"]), times(c["M"], c["M"])),
                                  times(Fraction(2), times(times(c["alpha"], c["M"]), c["beta"]))), times(c["beta"], c["beta"]))
    require(stages["native_exponential_allowance_squared"] == expanded_amplitude
            and stages["log_transport_M_squared_B_log"] == times(c["M"], times(c["B_log"], c["M"]))
            and stages["lower_projection_tail"] == c["lower_tail"] and stages["upper_tilted_projection_tail"] == c["upper_tail"],
            "Distinct expanded order reconciles existing primary stages only")
    require(checked_ratio(result["dollars_squared_stock_error_upper"])
            == plus(plus(times(c["upper_tail"], Fraction(3)), times(c["lower_tail"], Fraction(3))),
                    plus(times(stages["log_transport_M_squared_B_log"], Fraction(3)), times(expanded_amplitude, Fraction(3)))),
            "Expanded existing-primary total identity no third bound returned")
    return {"passed": True, "existing_primary_expanded_identities_reconciled": True,
            "total_envelope_assemblies": 2, "third_candidate_or_bound_returned": False,
            "independent130_own_literals_kept_separate": True, "outward_profile_nesting_required": False}

def four_first_stock_controls(positive):
    require(valid_first_stock_scope(positive) is True, "Positive exact validator before every fixed mutation")
    results = []
    for category in CONTROL_SPECS:
        mutations = []
        for mutation in category["fixed_bad_metadata_variants"]:
            budget()
            bad = dict(positive)
            bad.update(mutation)
            try:
                valid_first_stock_scope(bad)
            except E11FirstStockReject as error:
                require(type(error) is E11FirstStockReject and str(error) == category["dedicated_reject_code"],
                        "Only exact dedicated current semantic category counts")
            else:
                require(False, "Invalid fixed metadata accepted")
            mutations.append({"fixed_mutation": mutation, "exact_structural_rejection": True})
        results.append({"code": category["dedicated_reject_code"], "fixed_variants": mutations, "passed": True})
    require(len(results) == 4 and sum(len(row["fixed_variants"]) for row in results) == 13, "Exactly four categories/13variants")
    return {"passed": True, "category_count": 4, "metadata_variants": 13, "categories": results,
            "unrelated_IO_KeyError_assertion_or_budget_error_credit": False, "new_numerical_candidate_or_fixture": False}

def flags():
    return dict(FLAGS)

def main():
    global _STARTED, _OUTPUT_CREATED_BY_THIS_RUN, _OUTPUT_DIRECTORY_IDENTITY
    try:
        _STARTED = process_started()
        runtime_scopes()
        invocation_check()
        startup_decimal_policy()
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--ready-sha256", required=True)
        args = parser.parse_args()
        require(type(args.ready_sha256) is str and len(args.ready_sha256) == 64
                and all(char in "0123456789abcdef" for char in args.ready_sha256), "Exact external64hex READY pin")
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(), "Unused exclusive stock output route")
        ready, policy, method, supplement, owners, archive, histories, runtime, reviews, cfg = first_stock_admission(args.ready_sha256)
        first = fresh_first_stock_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        _OUTPUT_DIRECTORY_IDENTITY = output_directory_identity()
        _OUTPUT_CREATED_BY_THIS_RUN = True
        owned_output_guard()
        copies = {"executed_controller.py": AUTHOR, "executed_preflight.md": METHOD_DOC,
                  "executed_policy.json": PREFLIGHT, "executed_ROOT_READY.json": READY,
                  "reviewed_next_stock_method.md": ROOT / METHOD_MD_KEY,
                  "reviewed_next_stock_method.json": ROOT / METHOD_KEY,
                  "reviewed_independent_method_peer.json": ROOT / METHOD_PEER_KEY,
                  "reviewed_ROOT_method.json": ROOT / METHOD_ROOT_KEY}
        for name, path in copies.items(): copy(path, name)
        save("protocol.json", policy)
        save("run_started.json", {"created_UTC": time.time_ns(), "PID": os.getpid(),
                                  "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        save("interpreter.json", {"runtime": runtime, "literal_startup": EXACT_STARTUP, "separate_expected_cfg": cfg})
        save("loaded_module_origins.json", {"fresh_known_only_present_origins": True, "upfront_serializer": SERIALIZATION_RUNTIME,
                                           "all_current_reviews_before_first_runtime_origin": reviews,
                                           "current_cache_partition": {"present": ready["existing_new_code_cache_SHA256"],
                                                                       "absent": ready["absent_new_code_cache_paths"]}})
        save("active_and_archived_role_graph.json", {"active10": owners, "archive8": archive,
                                                    "aliases": ROLE_GRAPH["three_original_equal_SHA_archive_aliases"],
                                                    "historical_roles": histories,
                                                    "one_METHOD_snapshot_authority": {"path": METHOD_KEY, "SHA256": AUTHOR_INPUTS[METHOD_KEY]},
                                                    "all18_compact_summaries_not_full_snapshot_duplicates": True})
        save("fresh_full_input_union_before_assembly.json", first)
        positive, witness = source_first_stock_witness(method)
        save("source_first_stock_witness.json", witness)
        inputs = literal_first_stock_inputs(method)
        save("literal_prior_stock_component_adapters.json", PROFILE_CONTRACT)
        primary = primary_stock_components(inputs)
        primary_bound = primary_stock_squared(primary)
        save("primary_first_stock_components.json", encoded_stock_components(primary))
        save("primary_first_stock_squared_L2.json", primary_bound)
        independent = independent_stock_components(inputs)
        independent_bound = independent_stock_squared(independent)
        save("independent_first_stock_components.json", encoded_stock_components(independent))
        save("independent_first_stock_squared_L2.json", independent_bound)
        reconciliation = independently_reconcile_stock_primary(inputs, primary, primary_bound)
        save("independent_primary_proof_check.json", reconciliation)
        controls = four_first_stock_controls(positive)
        save("four_fixed_reject_controls.json", controls)
        save("qualification_and_remaining_gaps.json", {"selected_stock4021_only": True, "dollars_squared_units": True,
                                                      "both_unconditional_continuous_tails_paid": True,
                                                      "no_extra_spot_multiplier": True, "all_other_assets_dates_path_policy_payoff_G2_open": True,
                                                      "remaining_original_split_obligations": method["remaining_obligations"], **flags()})
        second = fresh_first_stock_union()
        save("fresh_full_input_union_after_assembly.json", second)
        summary = {"schema": "e11-first-stock-squared-L2-summary-v1", "passed": True, "completed": True,
                   "budget_censored": False, "numerical_envelope_assemblies": 2,
                   "primary_bound": primary_bound, "independent_bound": independent_bound,
                   "reconciliation": reconciliation, "four_fixed_controls": controls,
                   "selected_source_contract_SHA256": COMMON_EXPECTATIONS["source_contract_canonical_JSON_SHA256"],
                   "both_complete_fresh_input_unions": [first, second], "planned_manifest_inclusive_owned_files": 27,
                   "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                   "completion_requires_absent_failure_and_censor_markers": True,
                   "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        members = inventory(OUTPUT)
        require({path.name for path in members} == set(PLANNED_FILES) - {"manifest.json"}, "Exact26 before seal")
        files, total = {}, 0
        for path in sorted(members):
            budget()
            total += path.stat().st_size
            require(total <= MAX_OWN_BYTES and len(files) < MAX_OWN_FILES - 1, "Final MF reserve")
            files[path.name] = digest(path, fresh=True)
        complete_manifest({"schema": "e11-first-stock-squared-L2-manifest-v1", "files": files,
                           "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL,
                           "manifest_self_hash_excluded": True, "passed": True, "completed": True, "budget_censored": False,
                           "both_complete_fresh_input_unions": [first, second],
                           "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}, files, total)
        budget()
        owned_output_guard()
        require(not (OUTPUT / "failure.json").exists() and not (OUTPUT / "FAILED_UNSEALED.json").exists(), "Terminal failure absence")
        manifest_sha = digest(OUTPUT / "manifest.json", fresh=True)
        budget()
        owned_output_guard()
        print(json.dumps({"passed": True, "manifest_SHA256": manifest_sha, **flags()}), flush=True)
    except BaseException as error:
        if _OUTPUT_CREATED_BY_THIS_RUN:
            retain_failure(error)
        raise

if __name__ == "__main__":
    main()
