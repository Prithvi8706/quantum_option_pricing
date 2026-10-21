"""Dormant E11 first-preclip-log squared-L2 rational-only assembly.
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
AUTHOR = RESEARCH / "experiment_e11_first_log_prefix_squared_l2_v2.py"
METHOD_DOC = RESEARCH / "E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V2.md"
PREFLIGHT = RESEARCH / "e11_first_log_prefix_squared_l2_preflight_v2.json"
READY = ROOT / ".context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001"
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
AUTHOR_INPUTS = {'.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '638c4b186ef566d5a332103b32081a98f89ca33f4466361fcc339cb0c3a82d69',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_AUTHOR_STATIC_QA_run001.json': '65481a5a53d71848ca795dd10fcf48f1d14adc5bb2f67fafe56bf30cdf2c8545',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json': '2b71cb95bf2af76ad2835d3f2bbb8334e44fed28979d01e9b7cb4f4e24456d10',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.md': '83c2eebda4a60c2f14a306933acdfb3147710953dfccebe6c01cd2219491ca63',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_OPERATIONAL_CLARIFICATION_INDEPENDENT_PEER_run001.json': 'b50ffe7d80d2847917e92da3bf8d133476213f6197cbaf39855e131cd71ee12d',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_OPERATIONAL_CLARIFICATION_run001.json': '651c8908f9cb0d09ad96c6bbc63bdaf9a140584778b7f10e8cdfb37daf64979f',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': '38d469da3136ca60663b4a1c5f630c2e0ecefcbbf175da8ea783b10657ff8b04',
 '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_SUPPLEMENT_AUTHOR_AUDIT_NOTES_v14_run001.json': 'c9f276e225a8055ad621ff81218e11928b23edbcf7326ad18cee1b3175112dc1',
 '.context/E11_FIRST_LOG_PREFIX_INDEPENDENT_METHOD_PEER_METADATA_HELPER_HISTORY_run001.json': 'ef2b4b127ae9e51c37327b1104b80b31c11fa21f04374dab5ccf0898db19407b',
 '.context/E11_FIRST_LOG_PREFIX_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'ce9e3c7ac493485233e68a462d1c9e95de5f88a9d35fb8f4df8b2276df66f997',
 '.context/E11_FIRST_LOG_PREFIX_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run002.json': '380b3c9031220fce9328cd3bfb997fc455cfe7c4c8c07e5f0dc7e646c01832bd',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_TRIO_METADATA_CREATION_run001.json': 'c80033b92992b86c9e61805f5d8fca0741a650b705075a417891dc7aaa22e31d',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_HELD_AUTHOR_STATIC_QA_run001.json': '02fd0372f1bcd6a3b03612c3d947f536e6bcc5d6935421bac6763cc66aa8b513',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_INDEPENDENT_STATIC_HOLD_HISTORY_run001.json': 'db76ea24ba05d410fc4406b4cdc1a7a0a71cfdaec56750dd1ef20150f519f00f',
 '.context/E11_FIRST_LOG_PREFIX_V2_BOUND_READS_AND_OUTPUT_CUSTODY_ROOT_AUTHORING_CORRECTION_run001.json': 'b1ff1496fb948d9e7591d2dcbd7e5c6d497a970bb0730d56a1511db59ab68503',
 '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json': '136be8c070c5925d4a8ceac215788c3e2051b42289d9ca4e99b180ad7b6648c1',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_AUTHOR_METADATA_QA_run001.json': '272476c3620b72a187f7084b4100da6425640db804cc18aafb8d6dc036526913',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': 'f4623f2ef2c9c64d8bb1affe957a7b0d6e909fde82d61a5a74ea2f03c0b37a0f',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.json': '74b97d5a79daff3f16f995a1d93eeb273e68e36b1c0fe286fe1746ba776e25a9',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.md': 'eb18393f45ac3cb2a9ca602090c8137d9ff60e9fcd61a68187a9cadd599fa33b',
 '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'a2d597896b1b35e33ea4f9f83a58e3a70a040042ab58bdf4c69546cf7156aea9',
 '.context/E11_first_log_controller_body_v1_draft.txt': 'e071e8de267a380a2b9e4a24eca970b11e291f8ceed4e9274b1335f72e163788',
 '.context/E11_first_log_preflight_v1_draft.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
 '.context/author_E11_first_log_controller_trio_v1_run001.py': 'e8f47a1126b2dd4cf26e5265c7eceb6a1055cef182afcfd4498c24fdaffab24c',
 'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V1.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
 'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v1.json': 'f97bbafe661aed9b3f4e1f59cedc352774c5dbc2be046066581662232716670b',
 'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v1.py': '68ce90a9801d7395b110af4c20021ae9c8d7b707aad2f35f4bd7ae77408ce4c4',
 'research/limitation_program_20261001/experiment_e11_native_coordinate_squared_l2_v1.py': 'a60e773dbb23ff37fb3b631c53f270ee78ebcdf3963cc84165a8e13023f7b295'}
METHOD_KEY = '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.json'
METHOD_MD_KEY = '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.md'
SUPPLEMENT_KEY = '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json'
METHOD_PEER_KEY = '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json'
METHOD_ROOT_KEY = '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json'
NATIVE_READY_KEY = '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json'
COMPLETED_E11_READY_KEY = '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run002.json'
COMPLETED_E11_READY_SHA = '9a9d00407a8a6f763e9142d95d97e06dcadde3f2d0a73dfa9fcf167ced6f2c65'
CURRENT_REVIEW_PATHS = ['.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_STATIC_QA_run001.json',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json',
 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json']
AUTHOR_QA_KEY = '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_STATIC_QA_run001.json'
EXACT_STARTUP = {'PYTHONOPTIMIZE_and_integer_digit_override_absent_not_cleared': True,
 'Python_version': [3, 12, 4],
 'authority': 'Exact already admitted native invocation_check/runtime_scopes and literal ROOT/BASE/LAUNCHER '
              'assignments, not observed current runtime discovery.',
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
SELECTED_CONTRACT = {'actual_common_literal': 60222732077,
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
                                             'lookup_outputs': [103, 104, 105, 106, 107, 108, 109, 110],
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
                                            {'args': [3492, 3493], 'op': 'add', 'out': [3494], 'params': {}},
                                            {'args': [],
                                             'op': 'const',
                                             'out': [3495],
                                             'params': {'value': 4722366482868270824161}},
                                            {'args': [3494, 3495], 'op': 'add', 'out': [3496], 'params': {}},
                                            {'args': [],
                                             'op': 'const',
                                             'out': [3541],
                                             'params': {'value': 5063438167381}},
                                            {'args': [3496, 3541], 'op': 'add', 'out': [3542], 'params': {}}],
 'stock_consumer_not_claimed': 4021,
 'target_literal_SHA256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
 'target_path': 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json',
 'time_exact_literal': [1, 12],
 'width': 72}
CONTRACT_OBJECT_SHA = '2d0ab1412b9e04cabaf030540c5ad884236ad7e6754f5acf44fb23efbd309540'
FINITE_PROTOCOL = {'all_setup_admission_hash_math_control_and_serialization_CPU_charged': True,
 'candidate': 'B4_asset0_contractual_date1_preclip_raw_log3542_ONLY',
 'fixed_controls': ['REJECT_WEAK_PRICE_AS_STRONG_L1',
                    'REJECT_DIGITAL_PAIR_INDEPENDENCE_OR_ZERO_CROSS_TERM',
                    'REJECT_MISSING_FLOOR_OR_LITERAL_ERROR',
                    'REJECT_CHANGED_SOURCE_VALUE_PAIR_TARGET_OR_LAW'],
 'fresh_full_unions_before_and_after_required_before_future_release': 2,
 'independent': 'saved E11 independent plus A02 independently130 literals',
 'new_fixture_or_sample_or_cutoff_or_precision_candidates': 0,
 'primary': 'saved E11 primary plus A02 primary90 literals',
 'rational_assemblies': 2,
 'stop_rule': 'First provenance/premise/source-signed-safety/units/control/cap failure => scoped HOLD; no '
              'refresh/adaptation/cap raise',
 'third_numerical_candidate_or_envelope': False}
THEOREM = {'continuous_coordinate_second_moments_required_exact': [1, 1],
 'continuous_tail_discarded': False,
 'dollar_payoff_norm_or_policy_residual_claimed': False,
 'finite_pair_independence_or_zero_covariance_required': False,
 'five_terms': ['aN*(ZN0-Z0)',
                'bN*(ZN1-Z1)',
                '(aN-a)*Z0',
                '(bN-b)*Z1',
                'literal constants plus TWO signed-floor errors'],
 'ideal': 'L=ln100-1/800+(3/10)*sqrt((2/5)/12)*Z0+(3/10)*sqrt((3/5)/12)*Z1',
 'kappa': 'e0+ed+2/Q',
 'native': 'LN=lN+dN+floor_Q(aN*ZN0)+floor_Q(bN*ZN1)',
 'pointwise_Cauchy_term_count': 5,
 'rational_squared_formula_unevaluated': '5*((aN^2+bN^2)*B+ea^2+eb^2+(e0+ed+2/Q)^2)',
 'units': 'dimensionless_log_price_squared_at_one_original_source_intermediate'}
ROLE_GRAPH = {'active9': ['A01_run011',
             'A02_BM_native_financial_bridge_audit_run002',
             'A02_BM_native_financial_bridge_root_verification_run001',
             'A02_BM_native_financial_bridge_run002',
             'A10_coefficient_run001',
             'C06_pair_audit_run001',
             'C06_pair_run001',
             'E11_scalar_midpoint_L2_numerical_run002',
             'E11_native_coordinate_squared_L2_run001'],
 'active_new_native_coordinate_owner': 'E11_native_coordinate_squared_L2_run001',
 'active_original8': ['A01_run011',
                      'A02_BM_native_financial_bridge_audit_run002',
                      'A02_BM_native_financial_bridge_root_verification_run001',
                      'A02_BM_native_financial_bridge_run002',
                      'A10_coefficient_run001',
                      'C06_pair_audit_run001',
                      'C06_pair_run001',
                      'E11_scalar_midpoint_L2_numerical_run002'],
 'alias_role_owner_map_key_SHA_and_archived_route_preserved': True,
 'all17_success_or_current_runtime_promotion': False,
 'archive_C07_scope_and_failed_history4': ['C07_barrier_audit_run001',
                                           'C07_barrier_run001',
                                           'C07_barrier_run002',
                                           'C07_bound_date1_run001'],
 'archive_original4': ['A01_run014',
                       'A02_quantile_financial_audit_run001',
                       'A02_quantile_law_audit_run001',
                       'E10_continuous_moment_only_run002'],
 'archived_equal_SHA_source_aliases_exact': [{'current_original_path_integrity_asserted': False,
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
                                              'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}],
 'no_current_dirty_original_integrity_claim_or_hash_waiver': True,
 'owner_snapshot_SUMMARIES_no_large_map_duplicate': {'A01_run011': {'all_original_maps_preserved_exact': True,
                                                                    'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                    'complete_original_snapshot_canonical_JSON_SHA256': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                    'literal_manifest_expected_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03',
                                                                    'original_field_presence': {'external_runtime_inputs': False,
                                                                                                'files': True,
                                                                                                'frozen_inputs': True},
                                                                    'original_files_key_layout': 'ROOT_RELATIVE',
                                                                    'original_map_counts': [13, 623, None],
                                                                    'owned_inventory_bytes': 8745921,
                                                                    'owned_inventory_count': 13,
                                                                    'role': 'active_original_parent',
                                                                    'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                              'A01_run011']},
                                                     'A01_run014': {'all_original_maps_preserved_exact': True,
                                                                    'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                    'complete_original_snapshot_canonical_JSON_SHA256': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                    'literal_manifest_expected_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8',
                                                                    'original_field_presence': {'external_runtime_inputs': False,
                                                                                                'files': True,
                                                                                                'frozen_inputs': True},
                                                                    'original_files_key_layout': 'ROOT_RELATIVE',
                                                                    'original_map_counts': [16, 1221, None],
                                                                    'owned_inventory_bytes': 37429139,
                                                                    'owned_inventory_count': 16,
                                                                    'role': 'original_archive_only',
                                                                    'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                              'A01_run014']},
                                                     'A02_BM_native_financial_bridge_audit_run002': {'all_original_maps_preserved_exact': True,
                                                                                                     'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                     'complete_original_snapshot_canonical_JSON_SHA256': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                                     'literal_manifest_expected_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0',
                                                                                                     'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                 'files': True,
                                                                                                                                 'frozen_inputs': True},
                                                                                                     'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                     'original_map_counts': [23,
                                                                                                                             399,
                                                                                                                             2842],
                                                                                                     'owned_inventory_bytes': 44651234,
                                                                                                     'owned_inventory_count': 24,
                                                                                                     'role': 'active_original_parent',
                                                                                                     'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                               'A02_BM_native_financial_bridge_audit_run002']},
                                                     'A02_BM_native_financial_bridge_root_verification_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                 'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                 'complete_original_snapshot_canonical_JSON_SHA256': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                                                 'literal_manifest_expected_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab',
                                                                                                                 'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                             'files': True,
                                                                                                                                             'frozen_inputs': True},
                                                                                                                 'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                 'original_map_counts': [2,
                                                                                                                                         421,
                                                                                                                                         2842],
                                                                                                                 'owned_inventory_bytes': 579999,
                                                                                                                 'owned_inventory_count': 3,
                                                                                                                 'role': 'active_original_parent',
                                                                                                                 'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                           'A02_BM_native_financial_bridge_root_verification_run001']},
                                                     'A02_BM_native_financial_bridge_run002': {'all_original_maps_preserved_exact': True,
                                                                                               'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                               'complete_original_snapshot_canonical_JSON_SHA256': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                               'literal_manifest_expected_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162',
                                                                                               'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                           'files': True,
                                                                                                                           'frozen_inputs': True},
                                                                                               'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                               'original_map_counts': [28,
                                                                                                                       375,
                                                                                                                       2842],
                                                                                               'owned_inventory_bytes': 113209386,
                                                                                               'owned_inventory_count': 29,
                                                                                               'role': 'active_original_parent',
                                                                                               'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                         'A02_BM_native_financial_bridge_run002']},
                                                     'A02_quantile_financial_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                             'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                             'complete_original_snapshot_canonical_JSON_SHA256': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                             'literal_manifest_expected_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323',
                                                                                             'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                         'files': True,
                                                                                                                         'frozen_inputs': True},
                                                                                             'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                             'original_map_counts': [8,
                                                                                                                     2730,
                                                                                                                     None],
                                                                                             'owned_inventory_bytes': 1107202,
                                                                                             'owned_inventory_count': 9,
                                                                                             'role': 'original_archive_only',
                                                                                             'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                       'A02_quantile_financial_audit_run001']},
                                                     'A02_quantile_law_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                       'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                       'complete_original_snapshot_canonical_JSON_SHA256': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                       'literal_manifest_expected_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572',
                                                                                       'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                   'files': True,
                                                                                                                   'frozen_inputs': True},
                                                                                       'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                       'original_map_counts': [7,
                                                                                                               962,
                                                                                                               None],
                                                                                       'owned_inventory_bytes': 379157,
                                                                                       'owned_inventory_count': 8,
                                                                                       'role': 'original_archive_only',
                                                                                       'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                 'A02_quantile_law_audit_run001']},
                                                     'A10_coefficient_run001': {'all_original_maps_preserved_exact': True,
                                                                                'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                'complete_original_snapshot_canonical_JSON_SHA256': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                'literal_manifest_expected_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40',
                                                                                'original_field_presence': {'external_runtime_inputs': False,
                                                                                                            'files': False,
                                                                                                            'frozen_inputs': False},
                                                                                'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                'original_map_counts': [None,
                                                                                                        None,
                                                                                                        None],
                                                                                'owned_inventory_bytes': 107197203,
                                                                                'owned_inventory_count': 557,
                                                                                'role': 'active_original_parent',
                                                                                'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                          'A10_coefficient_run001']},
                                                     'C06_pair_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                               'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                               'complete_original_snapshot_canonical_JSON_SHA256': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                               'literal_manifest_expected_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14',
                                                                               'original_field_presence': {'external_runtime_inputs': False,
                                                                                                           'files': True,
                                                                                                           'frozen_inputs': True},
                                                                               'original_files_key_layout': 'ROOT_RELATIVE',
                                                                               'original_map_counts': [10,
                                                                                                       111,
                                                                                                       None],
                                                                               'owned_inventory_bytes': 1109330,
                                                                               'owned_inventory_count': 11,
                                                                               'role': 'active_original_parent',
                                                                               'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                         'C06_pair_audit_run001']},
                                                     'C06_pair_run001': {'all_original_maps_preserved_exact': True,
                                                                         'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                         'complete_original_snapshot_canonical_JSON_SHA256': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                         'literal_manifest_expected_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a',
                                                                         'original_field_presence': {'external_runtime_inputs': False,
                                                                                                     'files': True,
                                                                                                     'frozen_inputs': True},
                                                                         'original_files_key_layout': 'ROOT_RELATIVE',
                                                                         'original_map_counts': [10,
                                                                                                 24,
                                                                                                 None],
                                                                         'owned_inventory_bytes': 738350,
                                                                         'owned_inventory_count': 11,
                                                                         'role': 'active_original_parent',
                                                                         'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                   'C06_pair_run001']},
                                                     'C07_barrier_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                  'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                  'complete_original_snapshot_canonical_JSON_SHA256': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                  'literal_manifest_expected_SHA256': '29fe018792317eef189a9e6ceae00bf80c13b81fafd89ef0f4c3f48933dd98c9',
                                                                                  'original_field_presence': {'external_runtime_inputs': False,
                                                                                                              'files': True,
                                                                                                              'frozen_inputs': True},
                                                                                  'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                  'original_map_counts': [10,
                                                                                                          33,
                                                                                                          None],
                                                                                  'owned_inventory_bytes': 51656,
                                                                                  'owned_inventory_count': 11,
                                                                                  'role': 'C07_scope_or_failed_history_citation_only',
                                                                                  'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                            'C07_barrier_audit_run001']},
                                                     'C07_barrier_run001': {'all_original_maps_preserved_exact': True,
                                                                            'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                            'complete_original_snapshot_canonical_JSON_SHA256': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                            'literal_manifest_expected_SHA256': 'e30e10549a76d2baa07d44429badaf8e69f85b10041478def0f673b228c3a7b9',
                                                                            'original_field_presence': {'external_runtime_inputs': False,
                                                                                                        'files': True,
                                                                                                        'frozen_inputs': True},
                                                                            'original_files_key_layout': 'ROOT_RELATIVE',
                                                                            'original_map_counts': [8,
                                                                                                    8,
                                                                                                    None],
                                                                            'owned_inventory_bytes': 64258,
                                                                            'owned_inventory_count': 9,
                                                                            'role': 'C07_scope_or_failed_history_citation_only',
                                                                            'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                      'C07_barrier_run001']},
                                                     'C07_barrier_run002': {'all_original_maps_preserved_exact': True,
                                                                            'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                            'complete_original_snapshot_canonical_JSON_SHA256': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                            'literal_manifest_expected_SHA256': '3ce81f47db7fcd054d33a7391fb4600303f1f8afac545367c473172e740b6c9b',
                                                                            'original_field_presence': {'external_runtime_inputs': False,
                                                                                                        'files': True,
                                                                                                        'frozen_inputs': True},
                                                                            'original_files_key_layout': 'ROOT_RELATIVE',
                                                                            'original_map_counts': [10,
                                                                                                    8,
                                                                                                    None],
                                                                            'owned_inventory_bytes': 75701,
                                                                            'owned_inventory_count': 11,
                                                                            'role': 'C07_scope_or_failed_history_citation_only',
                                                                            'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                      'C07_barrier_run002']},
                                                     'C07_bound_date1_run001': {'all_original_maps_preserved_exact': True,
                                                                                'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                'complete_original_snapshot_canonical_JSON_SHA256': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                'literal_manifest_expected_SHA256': '9f7e676d7b7eb1c14b8ae8815b756da4491b50530fbdf9722b9861712de60dd6',
                                                                                'original_field_presence': {'external_runtime_inputs': False,
                                                                                                            'files': True,
                                                                                                            'frozen_inputs': True},
                                                                                'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                'original_map_counts': [14,
                                                                                                        88,
                                                                                                        None],
                                                                                'owned_inventory_bytes': 126462,
                                                                                'owned_inventory_count': 15,
                                                                                'role': 'C07_scope_or_failed_history_citation_only',
                                                                                'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                          'C07_bound_date1_run001']},
                                                     'E10_continuous_moment_only_run002': {'all_original_maps_preserved_exact': True,
                                                                                           'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                           'complete_original_snapshot_canonical_JSON_SHA256': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                           'literal_manifest_expected_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668',
                                                                                           'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                       'files': True,
                                                                                                                       'frozen_inputs': True},
                                                                                           'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                           'original_map_counts': [17,
                                                                                                                   109,
                                                                                                                   2842],
                                                                                           'owned_inventory_bytes': 7876736,
                                                                                           'owned_inventory_count': 18,
                                                                                           'role': 'original_archive_only',
                                                                                           'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                     'E10_continuous_moment_only_run002']},
                                                     'E11_native_coordinate_squared_L2_run001': {'all_original_maps_preserved_exact': True,
                                                                                                 'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                 'complete_original_snapshot_canonical_JSON_SHA256': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                                 'literal_manifest_expected_SHA256': 'bb1f08a600712e34d1fa4b3c77f0ea04147c5368c8f92dc4f9a21ed3e293df95',
                                                                                                 'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                             'files': True,
                                                                                                                             'frozen_inputs': True},
                                                                                                 'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                 'original_map_counts': [46,
                                                                                                                         1897,
                                                                                                                         2842],
                                                                                                 'owned_inventory_bytes': 68640627,
                                                                                                 'owned_inventory_count': 47,
                                                                                                 'role': 'active_new_native_coordinate_certificate',
                                                                                                 'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                           'E11_native_coordinate_squared_L2_run001']},
                                                     'E11_scalar_midpoint_L2_numerical_run002': {'all_original_maps_preserved_exact': True,
                                                                                                 'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                 'complete_original_snapshot_canonical_JSON_SHA256': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c',
                                                                                                 'literal_manifest_expected_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170',
                                                                                                 'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                             'files': True,
                                                                                                                             'frozen_inputs': True},
                                                                                                 'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                 'original_map_counts': [19,
                                                                                                                         174,
                                                                                                                         2842],
                                                                                                 'owned_inventory_bytes': 7729234,
                                                                                                 'owned_inventory_count': 20,
                                                                                                 'role': 'active_original_parent',
                                                                                                 'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                           'E11_scalar_midpoint_L2_numerical_run002']}}}
ACTIVE_OWNERS = ['A01_run011',
 'A02_BM_native_financial_bridge_audit_run002',
 'A02_BM_native_financial_bridge_root_verification_run001',
 'A02_BM_native_financial_bridge_run002',
 'A10_coefficient_run001',
 'C06_pair_audit_run001',
 'C06_pair_run001',
 'E11_scalar_midpoint_L2_numerical_run002',
 'E11_native_coordinate_squared_L2_run001']
ARCHIVE_CITATIONS = ['A01_run014',
 'A02_quantile_financial_audit_run001',
 'A02_quantile_law_audit_run001',
 'E10_continuous_moment_only_run002',
 'C07_barrier_audit_run001',
 'C07_barrier_run001',
 'C07_barrier_run002',
 'C07_bound_date1_run001']
PROFILE_CONTRACT = {'independent130': {'B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                    'METHOD_JSON_pointer': ['literal_uncombined_first_prefix_adapters', 'independent130'],
                    'all_literals_and_profile_kept_uncombined': True,
                    'complete_uncombined_adapter_canonical_JSON_SHA256': 'd56abc5f75d0eefb6cc2562ca810fd55d19b19ba8f4992776ce3838fe724d394',
                    'literal_error_role_to_original_field': {'e0': 'initial_literal_error_upper',
                                                             'ea': 'common_literal_error_upper',
                                                             'eb': 'idio_literal_error_upper',
                                                             'ed': 'drift_literal_error'},
                    'original_coordinate_B_expected_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84',
                    'original_coordinate_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json',
                    'original_envelope_expected_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                    'original_envelope_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json'},
 'primary90': {'B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
               'METHOD_JSON_pointer': ['literal_uncombined_first_prefix_adapters', 'primary90'],
               'all_literals_and_profile_kept_uncombined': True,
               'complete_uncombined_adapter_canonical_JSON_SHA256': '10656218733e1d57511dd11f99750da60917a1f1d3ecadb0192aea0a3c48a5ba',
               'literal_error_role_to_original_field': {'e0': 'initial_log_spot_error_upper',
                                                        'ea': 'common_literal_error_upper',
                                                        'eb': 'idio_literal_error_upper',
                                                        'ed': 'drift_literal_error_upper'},
               'original_coordinate_B_expected_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2',
               'original_coordinate_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json',
               'original_envelope_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
               'original_envelope_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json'}}
ORIGINAL_CAPS = {'CPU_admission_creation_wall': [180, 150, 600],
 'current_stdlib_runtime_files_bytes': [4096, 536870912],
 'owned_files_bytes': [64, 134217728],
 'references_unique_bytes_hash_work': [100000, 8589934592, 25769803776],
 'serialized_integer_reduced_rational_analytic_temporary_bits': [65536, 131072, 524288]}
PLANNED_FILES = ['manifest.json',
 'protocol.json',
 'run_started.json',
 'interpreter.json',
 'loaded_module_origins.json',
 'completion_outcome.json',
 'summary.json',
 'executed_controller.py',
 'executed_preflight.md',
 'executed_policy.json',
 'executed_ROOT_READY.json',
 'reviewed_next_method.md',
 'reviewed_next_method.json',
 'reviewed_independent_method_peer.json',
 'reviewed_ROOT_method.json',
 'source_first_log_prefix_witness.json',
 'active_and_archived_role_graph.json',
 'literal_prior_component_adapters.json',
 'primary_log_prefix_components.json',
 'primary_log_prefix_squared_L2.json',
 'independent_log_prefix_components.json',
 'independent_log_prefix_squared_L2.json',
 'independent_primary_proof_check.json',
 'four_fixed_reject_controls.json',
 'qualification_and_remaining_gaps.json',
 'fresh_full_input_union_before_assembly.json',
 'fresh_full_input_union_after_assembly.json']
HISTORICAL_CACHE_PARTITIONS = {'completed_native_author': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc',
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
                      'existing_expected_SHA256': {}}}
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
CONTROL_SPECS = [{'code': 'REJECT_WEAK_PRICE_AS_STRONG_L1',
  'fixed_bad_metadata_variants': [{'weak_price_bias_total_used_as_same_coupling_strong_L1': True}],
  'predicate': 'Strong_L1 authority is absent for the old whole-price bias; this stage accepts only '
               'native-coordinate squared B and one preclip log output, never the weak price total'},
 {'code': 'REJECT_DIGITAL_PAIR_INDEPENDENCE_OR_ZERO_CROSS_TERM',
  'fixed_bad_metadata_variants': [{'digital_pair_independence_assumed': True},
                                  {'cross_terms_set_zero_by_digital_independence': True}],
  'predicate': 'Original pair94/125 is shared; five-term pointwise Cauchy and continuous coordinate second '
               'moments are required; no digital independence or zero-covariance simplification'},
 {'code': 'REJECT_MISSING_FLOOR_OR_LITERAL_ERROR',
  'fixed_bad_metadata_variants': [{'omitted_signed_cmul_floor_value': 3492},
                                  {'omitted_signed_cmul_floor_value': 3493},
                                  {'omitted_error_component': 'ea'},
                                  {'omitted_error_component': 'eb'},
                                  {'omitted_error_component': 'e0'},
                                  {'omitted_error_component': 'ed'}],
  'predicate': 'Both floor IDs3492,3493 and all four literal errors ea,eb,e0,ed must be present; kappa '
               'retains e0+ed+2tau; original signed144 and every stored72 partial no-wrap premises remain '
               'mandatory'},
 {'code': 'REJECT_CHANGED_SOURCE_VALUE_PAIR_TARGET_OR_LAW',
  'fixed_bad_metadata_variants': [{'raw_preclip_log_value': 3541},
                                  {'ordered_native_normal_values': [125, 94]},
                                  {'target_literal_SHA256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'},
                                  {'ideal_reference_model': 'C4_H8_compound_predictor'}],
  'predicate': 'Exact B4x12 asset0 contractual date1/raw3542 seven-node slice, normal '
               'indices0,1/values94,125, original B4 target SHA and exact-decimal A02 ideal model must '
               'match'}]
COMMON_EXPECTATIONS = {'accepted_method_and_review_expected_SHA256': {'.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '638c4b186ef566d5a332103b32081a98f89ca33f4466361fcc339cb0c3a82d69',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_AUTHOR_STATIC_QA_run001.json': '65481a5a53d71848ca795dd10fcf48f1d14adc5bb2f67fafe56bf30cdf2c8545',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.json': '2b71cb95bf2af76ad2835d3f2bbb8334e44fed28979d01e9b7cb4f4e24456d10',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_METHOD_SUPPLEMENT_run001.md': '83c2eebda4a60c2f14a306933acdfb3147710953dfccebe6c01cd2219491ca63',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_OPERATIONAL_CLARIFICATION_INDEPENDENT_PEER_run001.json': 'b50ffe7d80d2847917e92da3bf8d133476213f6197cbaf39855e131cd71ee12d',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_OPERATIONAL_CLARIFICATION_run001.json': '651c8908f9cb0d09ad96c6bbc63bdaf9a140584778b7f10e8cdfb37daf64979f',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': '38d469da3136ca60663b4a1c5f630c2e0ecefcbbf175da8ea783b10657ff8b04',
                                                '.context/E11_FIRST_LOG_PREFIX_FINITE_ADMISSION_SUPPLEMENT_AUTHOR_AUDIT_NOTES_v14_run001.json': 'c9f276e225a8055ad621ff81218e11928b23edbcf7326ad18cee1b3175112dc1',
                                                '.context/E11_FIRST_LOG_PREFIX_INDEPENDENT_METHOD_PEER_METADATA_HELPER_HISTORY_run001.json': 'ef2b4b127ae9e51c37327b1104b80b31c11fa21f04374dab5ccf0898db19407b',
                                                '.context/E11_FIRST_LOG_PREFIX_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'ce9e3c7ac493485233e68a462d1c9e95de5f88a9d35fb8f4df8b2276df66f997',
                                                '.context/E11_FIRST_LOG_PREFIX_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run002.json': '380b3c9031220fce9328cd3bfb997fc455cfe7c4c8c07e5f0dc7e646c01832bd',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_TRIO_METADATA_CREATION_run001.json': 'c80033b92992b86c9e61805f5d8fca0741a650b705075a417891dc7aaa22e31d',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_HELD_AUTHOR_STATIC_QA_run001.json': '02fd0372f1bcd6a3b03612c3d947f536e6bcc5d6935421bac6763cc66aa8b513',
                                                '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_INDEPENDENT_STATIC_HOLD_HISTORY_run001.json': 'db76ea24ba05d410fc4406b4cdc1a7a0a71cfdaec56750dd1ef20150f519f00f',
                                                '.context/E11_FIRST_LOG_PREFIX_V2_BOUND_READS_AND_OUTPUT_CUSTODY_ROOT_AUTHORING_CORRECTION_run001.json': 'b1ff1496fb948d9e7591d2dcbd7e5c6d497a970bb0730d56a1511db59ab68503',
                                                '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json': '136be8c070c5925d4a8ceac215788c3e2051b42289d9ca4e99b180ad7b6648c1',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_AUTHOR_METADATA_QA_run001.json': '272476c3620b72a187f7084b4100da6425640db804cc18aafb8d6dc036526913',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': 'f4623f2ef2c9c64d8bb1affe957a7b0d6e909fde82d61a5a74ea2f03c0b37a0f',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.json': '74b97d5a79daff3f16f995a1d93eeb273e68e36b1c0fe286fe1746ba776e25a9',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_PROSPECTUS_run001.md': 'eb18393f45ac3cb2a9ca602090c8137d9ff60e9fcd61a68187a9cadd599fa33b',
                                                '.context/E11_NEXT_FINANCIAL_PATH_POLICY_L2_FIRST_LOG_PREFIX_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'a2d597896b1b35e33ea4f9f83a58e3a70a040042ab58bdf4c69546cf7156aea9',
                                                '.context/E11_first_log_controller_body_v1_draft.txt': 'e071e8de267a380a2b9e4a24eca970b11e291f8ceed4e9274b1335f72e163788',
                                                '.context/E11_first_log_preflight_v1_draft.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
                                                '.context/author_E11_first_log_controller_trio_v1_run001.py': 'e8f47a1126b2dd4cf26e5265c7eceb6a1055cef182afcfd4498c24fdaffab24c',
                                                'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V1.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
                                                'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v1.json': 'f97bbafe661aed9b3f4e1f59cedc352774c5dbc2be046066581662232716670b',
                                                'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v1.py': '68ce90a9801d7395b110af4c20021ae9c8d7b707aad2f35f4bd7ae77408ce4c4',
                                                'research/limitation_program_20261001/experiment_e11_native_coordinate_squared_l2_v1.py': 'a60e773dbb23ff37fb3b631c53f270ee78ebcdf3963cc84165a8e13023f7b295'},
 'active_and_archived_finite_role_graph': {'active9': ['A01_run011',
                                                       'A02_BM_native_financial_bridge_audit_run002',
                                                       'A02_BM_native_financial_bridge_root_verification_run001',
                                                       'A02_BM_native_financial_bridge_run002',
                                                       'A10_coefficient_run001',
                                                       'C06_pair_audit_run001',
                                                       'C06_pair_run001',
                                                       'E11_scalar_midpoint_L2_numerical_run002',
                                                       'E11_native_coordinate_squared_L2_run001'],
                                           'active_new_native_coordinate_owner': 'E11_native_coordinate_squared_L2_run001',
                                           'active_original8': ['A01_run011',
                                                                'A02_BM_native_financial_bridge_audit_run002',
                                                                'A02_BM_native_financial_bridge_root_verification_run001',
                                                                'A02_BM_native_financial_bridge_run002',
                                                                'A10_coefficient_run001',
                                                                'C06_pair_audit_run001',
                                                                'C06_pair_run001',
                                                                'E11_scalar_midpoint_L2_numerical_run002'],
                                           'alias_role_owner_map_key_SHA_and_archived_route_preserved': True,
                                           'all17_success_or_current_runtime_promotion': False,
                                           'archive_C07_scope_and_failed_history4': ['C07_barrier_audit_run001',
                                                                                     'C07_barrier_run001',
                                                                                     'C07_barrier_run002',
                                                                                     'C07_bound_date1_run001'],
                                           'archive_original4': ['A01_run014',
                                                                 'A02_quantile_financial_audit_run001',
                                                                 'A02_quantile_law_audit_run001',
                                                                 'E10_continuous_moment_only_run002'],
                                           'archived_equal_SHA_source_aliases_exact': [{'current_original_path_integrity_asserted': False,
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
                                                                                        'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}],
                                           'no_current_dirty_original_integrity_claim_or_hash_waiver': True,
                                           'owner_snapshot_SUMMARIES_no_large_map_duplicate': {'A01_run011': {'all_original_maps_preserved_exact': True,
                                                                                                              'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                              'complete_original_snapshot_canonical_JSON_SHA256': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4',
                                                                                                              'literal_manifest_expected_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03',
                                                                                                              'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                          'files': True,
                                                                                                                                          'frozen_inputs': True},
                                                                                                              'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                              'original_map_counts': [13,
                                                                                                                                      623,
                                                                                                                                      None],
                                                                                                              'owned_inventory_bytes': 8745921,
                                                                                                              'owned_inventory_count': 13,
                                                                                                              'role': 'active_original_parent',
                                                                                                              'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                        'A01_run011']},
                                                                                               'A01_run014': {'all_original_maps_preserved_exact': True,
                                                                                                              'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                              'complete_original_snapshot_canonical_JSON_SHA256': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da',
                                                                                                              'literal_manifest_expected_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8',
                                                                                                              'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                          'files': True,
                                                                                                                                          'frozen_inputs': True},
                                                                                                              'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                              'original_map_counts': [16,
                                                                                                                                      1221,
                                                                                                                                      None],
                                                                                                              'owned_inventory_bytes': 37429139,
                                                                                                              'owned_inventory_count': 16,
                                                                                                              'role': 'original_archive_only',
                                                                                                              'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                        'A01_run014']},
                                                                                               'A02_BM_native_financial_bridge_audit_run002': {'all_original_maps_preserved_exact': True,
                                                                                                                                               'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                               'complete_original_snapshot_canonical_JSON_SHA256': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7',
                                                                                                                                               'literal_manifest_expected_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0',
                                                                                                                                               'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                           'files': True,
                                                                                                                                                                           'frozen_inputs': True},
                                                                                                                                               'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                                               'original_map_counts': [23,
                                                                                                                                                                       399,
                                                                                                                                                                       2842],
                                                                                                                                               'owned_inventory_bytes': 44651234,
                                                                                                                                               'owned_inventory_count': 24,
                                                                                                                                               'role': 'active_original_parent',
                                                                                                                                               'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                         'A02_BM_native_financial_bridge_audit_run002']},
                                                                                               'A02_BM_native_financial_bridge_root_verification_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                                                           'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                                           'complete_original_snapshot_canonical_JSON_SHA256': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36',
                                                                                                                                                           'literal_manifest_expected_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab',
                                                                                                                                                           'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                                       'files': True,
                                                                                                                                                                                       'frozen_inputs': True},
                                                                                                                                                           'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                                                           'original_map_counts': [2,
                                                                                                                                                                                   421,
                                                                                                                                                                                   2842],
                                                                                                                                                           'owned_inventory_bytes': 579999,
                                                                                                                                                           'owned_inventory_count': 3,
                                                                                                                                                           'role': 'active_original_parent',
                                                                                                                                                           'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                                     'A02_BM_native_financial_bridge_root_verification_run001']},
                                                                                               'A02_BM_native_financial_bridge_run002': {'all_original_maps_preserved_exact': True,
                                                                                                                                         'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                         'complete_original_snapshot_canonical_JSON_SHA256': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073',
                                                                                                                                         'literal_manifest_expected_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162',
                                                                                                                                         'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                     'files': True,
                                                                                                                                                                     'frozen_inputs': True},
                                                                                                                                         'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                                         'original_map_counts': [28,
                                                                                                                                                                 375,
                                                                                                                                                                 2842],
                                                                                                                                         'owned_inventory_bytes': 113209386,
                                                                                                                                         'owned_inventory_count': 29,
                                                                                                                                         'role': 'active_original_parent',
                                                                                                                                         'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                   'A02_BM_native_financial_bridge_run002']},
                                                                                               'A02_quantile_financial_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                                       'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                       'complete_original_snapshot_canonical_JSON_SHA256': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828',
                                                                                                                                       'literal_manifest_expected_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323',
                                                                                                                                       'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                                   'files': True,
                                                                                                                                                                   'frozen_inputs': True},
                                                                                                                                       'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                                       'original_map_counts': [8,
                                                                                                                                                               2730,
                                                                                                                                                               None],
                                                                                                                                       'owned_inventory_bytes': 1107202,
                                                                                                                                       'owned_inventory_count': 9,
                                                                                                                                       'role': 'original_archive_only',
                                                                                                                                       'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                 'A02_quantile_financial_audit_run001']},
                                                                                               'A02_quantile_law_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                                 'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                 'complete_original_snapshot_canonical_JSON_SHA256': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4',
                                                                                                                                 'literal_manifest_expected_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572',
                                                                                                                                 'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                             'files': True,
                                                                                                                                                             'frozen_inputs': True},
                                                                                                                                 'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                                 'original_map_counts': [7,
                                                                                                                                                         962,
                                                                                                                                                         None],
                                                                                                                                 'owned_inventory_bytes': 379157,
                                                                                                                                 'owned_inventory_count': 8,
                                                                                                                                 'role': 'original_archive_only',
                                                                                                                                 'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                           'A02_quantile_law_audit_run001']},
                                                                                               'A10_coefficient_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                          'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                          'complete_original_snapshot_canonical_JSON_SHA256': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b',
                                                                                                                          'literal_manifest_expected_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40',
                                                                                                                          'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                      'files': False,
                                                                                                                                                      'frozen_inputs': False},
                                                                                                                          'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                          'original_map_counts': [None,
                                                                                                                                                  None,
                                                                                                                                                  None],
                                                                                                                          'owned_inventory_bytes': 107197203,
                                                                                                                          'owned_inventory_count': 557,
                                                                                                                          'role': 'active_original_parent',
                                                                                                                          'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                    'A10_coefficient_run001']},
                                                                                               'C06_pair_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                         'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                         'complete_original_snapshot_canonical_JSON_SHA256': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7',
                                                                                                                         'literal_manifest_expected_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14',
                                                                                                                         'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                     'files': True,
                                                                                                                                                     'frozen_inputs': True},
                                                                                                                         'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                         'original_map_counts': [10,
                                                                                                                                                 111,
                                                                                                                                                 None],
                                                                                                                         'owned_inventory_bytes': 1109330,
                                                                                                                         'owned_inventory_count': 11,
                                                                                                                         'role': 'active_original_parent',
                                                                                                                         'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                   'C06_pair_audit_run001']},
                                                                                               'C06_pair_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                   'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                   'complete_original_snapshot_canonical_JSON_SHA256': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25',
                                                                                                                   'literal_manifest_expected_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a',
                                                                                                                   'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                               'files': True,
                                                                                                                                               'frozen_inputs': True},
                                                                                                                   'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                   'original_map_counts': [10,
                                                                                                                                           24,
                                                                                                                                           None],
                                                                                                                   'owned_inventory_bytes': 738350,
                                                                                                                   'owned_inventory_count': 11,
                                                                                                                   'role': 'active_original_parent',
                                                                                                                   'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                             'C06_pair_run001']},
                                                                                               'C07_barrier_audit_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                            'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                            'complete_original_snapshot_canonical_JSON_SHA256': '5445fc1862e97867c3d6939cbd31216a1017b040bf094d6058b3106394df6ddb',
                                                                                                                            'literal_manifest_expected_SHA256': '29fe018792317eef189a9e6ceae00bf80c13b81fafd89ef0f4c3f48933dd98c9',
                                                                                                                            'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                        'files': True,
                                                                                                                                                        'frozen_inputs': True},
                                                                                                                            'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                            'original_map_counts': [10,
                                                                                                                                                    33,
                                                                                                                                                    None],
                                                                                                                            'owned_inventory_bytes': 51656,
                                                                                                                            'owned_inventory_count': 11,
                                                                                                                            'role': 'C07_scope_or_failed_history_citation_only',
                                                                                                                            'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                      'C07_barrier_audit_run001']},
                                                                                               'C07_barrier_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                      'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                      'complete_original_snapshot_canonical_JSON_SHA256': 'e9d74c619c4d09da370613c25ffac7e3264b46798e245155bc700cbd2573ed58',
                                                                                                                      'literal_manifest_expected_SHA256': 'e30e10549a76d2baa07d44429badaf8e69f85b10041478def0f673b228c3a7b9',
                                                                                                                      'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                  'files': True,
                                                                                                                                                  'frozen_inputs': True},
                                                                                                                      'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                      'original_map_counts': [8,
                                                                                                                                              8,
                                                                                                                                              None],
                                                                                                                      'owned_inventory_bytes': 64258,
                                                                                                                      'owned_inventory_count': 9,
                                                                                                                      'role': 'C07_scope_or_failed_history_citation_only',
                                                                                                                      'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                'C07_barrier_run001']},
                                                                                               'C07_barrier_run002': {'all_original_maps_preserved_exact': True,
                                                                                                                      'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                      'complete_original_snapshot_canonical_JSON_SHA256': 'dc351f55e0c6aa4a9d16504621b3f9edb2c5654cbd16a706f8beb8e1a8261511',
                                                                                                                      'literal_manifest_expected_SHA256': '3ce81f47db7fcd054d33a7391fb4600303f1f8afac545367c473172e740b6c9b',
                                                                                                                      'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                  'files': True,
                                                                                                                                                  'frozen_inputs': True},
                                                                                                                      'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                      'original_map_counts': [10,
                                                                                                                                              8,
                                                                                                                                              None],
                                                                                                                      'owned_inventory_bytes': 75701,
                                                                                                                      'owned_inventory_count': 11,
                                                                                                                      'role': 'C07_scope_or_failed_history_citation_only',
                                                                                                                      'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                'C07_barrier_run002']},
                                                                                               'C07_bound_date1_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                          'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                          'complete_original_snapshot_canonical_JSON_SHA256': '313fbc2fa8cea77e1a52ebc80268ad7329375cdf169ac93cd9e2f2e8a043aac7',
                                                                                                                          'literal_manifest_expected_SHA256': '9f7e676d7b7eb1c14b8ae8815b756da4491b50530fbdf9722b9861712de60dd6',
                                                                                                                          'original_field_presence': {'external_runtime_inputs': False,
                                                                                                                                                      'files': True,
                                                                                                                                                      'frozen_inputs': True},
                                                                                                                          'original_files_key_layout': 'ROOT_RELATIVE',
                                                                                                                          'original_map_counts': [14,
                                                                                                                                                  88,
                                                                                                                                                  None],
                                                                                                                          'owned_inventory_bytes': 126462,
                                                                                                                          'owned_inventory_count': 15,
                                                                                                                          'role': 'C07_scope_or_failed_history_citation_only',
                                                                                                                          'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                    'C07_bound_date1_run001']},
                                                                                               'E10_continuous_moment_only_run002': {'all_original_maps_preserved_exact': True,
                                                                                                                                     'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                     'complete_original_snapshot_canonical_JSON_SHA256': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231',
                                                                                                                                     'literal_manifest_expected_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668',
                                                                                                                                     'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                 'files': True,
                                                                                                                                                                 'frozen_inputs': True},
                                                                                                                                     'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                                     'original_map_counts': [17,
                                                                                                                                                             109,
                                                                                                                                                             2842],
                                                                                                                                     'owned_inventory_bytes': 7876736,
                                                                                                                                     'owned_inventory_count': 18,
                                                                                                                                     'role': 'original_archive_only',
                                                                                                                                     'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                               'E10_continuous_moment_only_run002']},
                                                                                               'E11_native_coordinate_squared_L2_run001': {'all_original_maps_preserved_exact': True,
                                                                                                                                           'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                           'complete_original_snapshot_canonical_JSON_SHA256': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476',
                                                                                                                                           'literal_manifest_expected_SHA256': 'bb1f08a600712e34d1fa4b3c77f0ea04147c5368c8f92dc4f9a21ed3e293df95',
                                                                                                                                           'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                       'files': True,
                                                                                                                                                                       'frozen_inputs': True},
                                                                                                                                           'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                                           'original_map_counts': [46,
                                                                                                                                                                   1897,
                                                                                                                                                                   2842],
                                                                                                                                           'owned_inventory_bytes': 68640627,
                                                                                                                                           'owned_inventory_count': 47,
                                                                                                                                           'role': 'active_new_native_coordinate_certificate',
                                                                                                                                           'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                     'E11_native_coordinate_squared_L2_run001']},
                                                                                               'E11_scalar_midpoint_L2_numerical_run002': {'all_original_maps_preserved_exact': True,
                                                                                                                                           'archive_nested_maps_current_runtime_or_success_admitted': False,
                                                                                                                                           'complete_original_snapshot_canonical_JSON_SHA256': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c',
                                                                                                                                           'literal_manifest_expected_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170',
                                                                                                                                           'original_field_presence': {'external_runtime_inputs': True,
                                                                                                                                                                       'files': True,
                                                                                                                                                                       'frozen_inputs': True},
                                                                                                                                           'original_files_key_layout': 'RECEIPT_RELATIVE',
                                                                                                                                           'original_map_counts': [19,
                                                                                                                                                                   174,
                                                                                                                                                                   2842],
                                                                                                                                           'owned_inventory_bytes': 7729234,
                                                                                                                                           'owned_inventory_count': 20,
                                                                                                                                           'role': 'active_original_parent',
                                                                                                                                           'snapshot_JSON_pointer': ['complete_original_cited_owner_snapshots',
                                                                                                                                                                     'E11_scalar_midpoint_L2_numerical_run002']}}},
 'current_authoring_acceptance_SHA256': 'b1ff1496fb948d9e7591d2dcbd7e5c6d497a970bb0730d56a1511db59ab68503',
 'current_authoring_acceptance_path': '.context/E11_FIRST_LOG_PREFIX_V2_BOUND_READS_AND_OUTPUT_CUSTODY_ROOT_AUTHORING_CORRECTION_run001.json',
 'current_static_review_paths': ['.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_STATIC_QA_run001.json',
                                 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_INDEPENDENT_STATIC_PEER_run001.json',
                                 '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json'],
 'exact_startup_literals': {'PYTHONOPTIMIZE_and_integer_digit_override_absent_not_cleared': True,
                            'Python_version': [3, 12, 4],
                            'authority': 'Exact already admitted native invocation_check/runtime_scopes and '
                                         'literal ROOT/BASE/LAUNCHER assignments, not observed current '
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
 'finite_protocol': {'all_setup_admission_hash_math_control_and_serialization_CPU_charged': True,
                     'candidate': 'B4_asset0_contractual_date1_preclip_raw_log3542_ONLY',
                     'fixed_controls': ['REJECT_WEAK_PRICE_AS_STRONG_L1',
                                        'REJECT_DIGITAL_PAIR_INDEPENDENCE_OR_ZERO_CROSS_TERM',
                                        'REJECT_MISSING_FLOOR_OR_LITERAL_ERROR',
                                        'REJECT_CHANGED_SOURCE_VALUE_PAIR_TARGET_OR_LAW'],
                     'fresh_full_unions_before_and_after_required_before_future_release': 2,
                     'independent': 'saved E11 independent plus A02 independently130 literals',
                     'new_fixture_or_sample_or_cutoff_or_precision_candidates': 0,
                     'primary': 'saved E11 primary plus A02 primary90 literals',
                     'rational_assemblies': 2,
                     'stop_rule': 'First provenance/premise/source-signed-safety/units/control/cap failure '
                                  '=> scoped HOLD; no refresh/adaptation/cap raise',
                     'third_numerical_candidate_or_envelope': False},
 'first_failure_stop_no_retry_or_partial_success': True,
 'five_term_single_log_prefix_theorem': {'continuous_coordinate_second_moments_required_exact': [1, 1],
                                         'continuous_tail_discarded': False,
                                         'dollar_payoff_norm_or_policy_residual_claimed': False,
                                         'finite_pair_independence_or_zero_covariance_required': False,
                                         'five_terms': ['aN*(ZN0-Z0)',
                                                        'bN*(ZN1-Z1)',
                                                        '(aN-a)*Z0',
                                                        '(bN-b)*Z1',
                                                        'literal constants plus TWO signed-floor errors'],
                                         'ideal': 'L=ln100-1/800+(3/10)*sqrt((2/5)/12)*Z0+(3/10)*sqrt((3/5)/12)*Z1',
                                         'kappa': 'e0+ed+2/Q',
                                         'native': 'LN=lN+dN+floor_Q(aN*ZN0)+floor_Q(bN*ZN1)',
                                         'pointwise_Cauchy_term_count': 5,
                                         'rational_squared_formula_unevaluated': '5*((aN^2+bN^2)*B+ea^2+eb^2+(e0+ed+2/Q)^2)',
                                         'units': 'dimensionless_log_price_squared_at_one_original_source_intermediate'},
 'full_METHOD_JSON_copy_count': 1,
 'future_actual_log_bound': None,
 'historical_V1_acceptance_has_current_authoring_authority': False,
 'historical_cache_partitions': {'completed_native_author': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc',
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
 'historical_first_log_V1_source_has_current_execution_permission': False,
 'native_reference_toy_array_count': 0,
 'original_caps': {'CPU_admission_creation_wall': [180, 150, 600],
                   'current_stdlib_runtime_files_bytes': [4096, 536870912],
                   'owned_files_bytes': [64, 134217728],
                   'references_unique_bytes_hash_work': [100000, 8589934592, 25769803776],
                   'serialized_integer_reduced_rational_analytic_temporary_bits': [65536, 131072, 524288]},
 'output': 'results/limitation_program_20261001/E11_first_log_prefix_squared_L2_run001',
 'planned_manifest_inclusive_owned_files': 27,
 'planned_owned_filenames': ['manifest.json',
                             'protocol.json',
                             'run_started.json',
                             'interpreter.json',
                             'loaded_module_origins.json',
                             'completion_outcome.json',
                             'summary.json',
                             'executed_controller.py',
                             'executed_preflight.md',
                             'executed_policy.json',
                             'executed_ROOT_READY.json',
                             'reviewed_next_method.md',
                             'reviewed_next_method.json',
                             'reviewed_independent_method_peer.json',
                             'reviewed_ROOT_method.json',
                             'source_first_log_prefix_witness.json',
                             'active_and_archived_role_graph.json',
                             'literal_prior_component_adapters.json',
                             'primary_log_prefix_components.json',
                             'primary_log_prefix_squared_L2.json',
                             'independent_log_prefix_components.json',
                             'independent_log_prefix_squared_L2.json',
                             'independent_primary_proof_check.json',
                             'four_fixed_reject_controls.json',
                             'qualification_and_remaining_gaps.json',
                             'fresh_full_input_union_before_assembly.json',
                             'fresh_full_input_union_after_assembly.json'],
 'preserved_first_log_V1_author_creator_and_HOLD_expected_SHA256': {'.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_AUTHOR_TRIO_METADATA_CREATION_run001.json': 'c80033b92992b86c9e61805f5d8fca0741a650b705075a417891dc7aaa22e31d',
                                                                    '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_HELD_AUTHOR_STATIC_QA_run001.json': '02fd0372f1bcd6a3b03612c3d947f536e6bcc5d6935421bac6763cc66aa8b513',
                                                                    '.context/E11_FIRST_LOG_PREFIX_SQUARED_L2_V1_INDEPENDENT_STATIC_HOLD_HISTORY_run001.json': 'db76ea24ba05d410fc4406b4cdc1a7a0a71cfdaec56750dd1ef20150f519f00f',
                                                                    '.context/E11_first_log_controller_body_v1_draft.txt': 'e071e8de267a380a2b9e4a24eca970b11e291f8ceed4e9274b1335f72e163788',
                                                                    '.context/E11_first_log_preflight_v1_draft.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
                                                                    '.context/author_E11_first_log_controller_trio_v1_run001.py': 'e8f47a1126b2dd4cf26e5265c7eceb6a1055cef182afcfd4498c24fdaffab24c',
                                                                    'research/limitation_program_20261001/E11_FIRST_LOG_PREFIX_SQUARED_L2_PREFLIGHT_V1.md': '49c733e778bbfaef4f4d5b63517aaab790d83df5b933252bc4aee174a34d3f54',
                                                                    'research/limitation_program_20261001/e11_first_log_prefix_squared_l2_preflight_v1.json': 'f97bbafe661aed9b3f4e1f59cedc352774c5dbc2be046066581662232716670b',
                                                                    'research/limitation_program_20261001/experiment_e11_first_log_prefix_squared_l2_v1.py': '68ce90a9801d7395b110af4c20021ae9c8d7b707aad2f35f4bd7ae77408ce4c4'},
 'prior_foundational_ROOT_authoring_acceptance_SHA256': '380b3c9031220fce9328cd3bfb997fc455cfe7c4c8c07e5f0dc7e646c01832bd',
 'prior_foundational_ROOT_authoring_acceptance_path': '.context/E11_FIRST_LOG_PREFIX_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run002.json',
 'runtime_invocation': ['-I',
                        '-S',
                        '-B',
                        'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_first_log_prefix_squared_l2_v2.py',
                        '--ready-sha256',
                        'EXTERNAL_ROOT_READY_SHA256'],
 'selected_original_contract': {'actual_common_literal': 60222732077,
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
                                                            'constants': [[-1374389535, 1],
                                                                          [5063438167381, 1]],
                                                            'date': 0,
                                                            'every_driver_multiplicity': 1,
                                                            'original_normal_indices': [0, 1],
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
                                'width': 72},
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
 'tightened_current_bootstrap_order': ['Charge setup and imports against original process-created budgets; '
                                       'check externally declared exact invocation, paths, startup flags and '
                                       'default4300 policy.',
                                       'Read externally SHA-pinned bounded ROOT READY and prospective '
                                       'policy; bind exactly3 new author bytes/AST and exhaustive current '
                                       'default-opt1-opt2 cache partition.',
                                       'Bind exact original METHOD, admission supplement, all accepted '
                                       'METHOD/admission reviews, this clarification and its independent '
                                       'peer, ROOT authoring acceptanceV2, and exactly3 future current '
                                       'source-QA/independent/root-static records from externally fixed '
                                       'expected maps. Reject missing or additional review routes, wrong '
                                       'pins or malformed scope without deriving expectations from observed '
                                       'bytes.',
                                       'Bind full original native2842 external runtime expected map, the two '
                                       'pinned interpreters and upfront _pylong source/three-cache '
                                       'partition; compile/loaded-function source guard and validate finite '
                                       'stdlib membership.',
                                       'Perform the first strict loaded-origin guard only after every '
                                       'current author/cache/runtime/review binding above; reject unknown, '
                                       'numerical, site or old scientific origins.',
                                       'Apply the one reviewed20000 saved-pair serializer decimal limit '
                                       'after initial admissions/origins; representation caps remain '
                                       'unchanged.',
                                       'Bind remaining exact active9/archive8/alias/failed-history roles, '
                                       'then first complete fresh uncached input/owned/runtime/absence union '
                                       'before either assembly.',
                                       'Exactly two uncombined90/130 first-log squared assemblies, '
                                       'independent reconciliation and four fixed rejection categories; no '
                                       'third candidate, series, sampling or arrays.',
                                       'Second complete fresh uncached union rechecks all exact current '
                                       'reviews and original input/history/runtime/cache bindings before '
                                       'exclusive terminal seal.'],
 'two_literal_profile_adapter_contract': {'independent130': {'B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                             'METHOD_JSON_pointer': ['literal_uncombined_first_prefix_adapters',
                                                                                     'independent130'],
                                                             'all_literals_and_profile_kept_uncombined': True,
                                                             'complete_uncombined_adapter_canonical_JSON_SHA256': 'd56abc5f75d0eefb6cc2562ca810fd55d19b19ba8f4992776ce3838fe724d394',
                                                             'literal_error_role_to_original_field': {'e0': 'initial_literal_error_upper',
                                                                                                      'ea': 'common_literal_error_upper',
                                                                                                      'eb': 'idio_literal_error_upper',
                                                                                                      'ed': 'drift_literal_error'},
                                                             'original_coordinate_B_expected_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84',
                                                             'original_coordinate_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json',
                                                             'original_envelope_expected_SHA256': '18cb2c79139845907452ee05fc68ea8b4a0a82fcdd035ef8652aec3b871afa08',
                                                             'original_envelope_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_raw_log_prefix_envelopes.json'},
                                          'primary90': {'B_field': 'continuous_to_original_native_coordinate_squared_L2_upper',
                                                        'METHOD_JSON_pointer': ['literal_uncombined_first_prefix_adapters',
                                                                                'primary90'],
                                                        'all_literals_and_profile_kept_uncombined': True,
                                                        'complete_uncombined_adapter_canonical_JSON_SHA256': '10656218733e1d57511dd11f99750da60917a1f1d3ecadb0192aea0a3c48a5ba',
                                                        'literal_error_role_to_original_field': {'e0': 'initial_log_spot_error_upper',
                                                                                                 'ea': 'common_literal_error_upper',
                                                                                                 'eb': 'idio_literal_error_upper',
                                                                                                 'ed': 'drift_literal_error_upper'},
                                                        'original_coordinate_B_expected_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2',
                                                        'original_coordinate_B_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json',
                                                        'original_envelope_expected_SHA256': '4b9a6c0cb574ed2c8008f4802957d4949fbc8922c5ec79861cf6bcd838a93373',
                                                        'original_envelope_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/raw_log_prefix_envelopes.json'}}}


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

def invocation_check():
    require(sys.version_info[:3] == (3, 12, 4) and sys.flags.isolated == 1
            and sys.flags.no_site == 1 and sys.dont_write_bytecode
            and sys.flags.optimize == 0 and "PYTHONOPTIMIZE" not in os.environ,
            "Pinned Python3.12.4 isolated -I -S -B direct-script invocation")
    require(canonical(Path.cwd(), fresh=True) == ROOT, "Exact original workspace cwd")
    require(canonical(sys.executable, fresh=True) == LAUNCHER
            and canonical(sys.base_prefix, fresh=True) == BASE
            and canonical(sys.prefix, fresh=True) == BASE,
            "No-site exact launcher/base/prefix")
    require(sys.path == [str(BASE / "python312.zip"), str(BASE / "DLLs"),
                         str(BASE / "Lib"), str(BASE)], "Exact isolated stdlib search path")
    absent_zip = BASE / "python312.zip"
    require(not absent_zip.exists() and not absent_zip.is_symlink(), "Exact absent standard zip")
    _ABSENT_RUNTIME.add(absent_zip)
    require(not any(name == "site" or name.startswith("research.") for name in sys.modules),
            "No site or scientific module loaded")
    bind(LAUNCHER, LAUNCHER_SHA)
    bind(BASE / "python.exe", BASE_SHA)

def bind(path, expected):
    actual = add(path, expected)
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

def code_cache_policy(ready):
    paths = {exact_key("research/limitation_program_20261001/__pycache__/"
                       + AUTHOR.stem + ".cpython-312" + suffix + ".pyc")
             for suffix in ("", ".opt-1", ".opt-2")}
    expected = ready["existing_new_code_cache_SHA256"]
    absent = ready["absent_new_code_cache_paths"]
    present = {path for path in paths if path.exists()}
    require(type(expected) is dict and type(absent) is list
            and len(absent) == len(set(absent))
            and {exact_key(key) for key in expected} == present
            and {exact_key(key) for key in absent} == paths - present,
            "Exact externally declared normal/opt1/opt2 current author cache partition")
    for key, pin in expected.items():
        path = bind(exact_key(key), pin)
        _CODE_CACHE_EXPECTED[path] = pin
    for key in absent:
        path = exact_key(key)
        require(not path.exists() and not path.is_symlink(), "Exact declared absent author cache")
        _ABSENT_RUNTIME.add(path)

def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        save("failure.json", {"passed": False, "completed": False, "error_type": type(error).__name__,
                              "error": str(error), "traceback": traceback.format_exc(), **flags()})
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,'
                         b'"hard_budget_state_uncertified":true,"fixture_credit":0,"digital_moment_transfer":false}\n')
    except OSError:
        pass

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

def bootstrap_json(path, expected):
    """Bounded raw JSON before the declared decimal-serializer change."""
    global _HASH_WORK
    budget()
    actual = bind(path, expected)
    before = fingerprint(actual)
    require(before[2] <= MAX_OWN_BYTES, "Bounded bootstrap JSON")
    raw = actual.read_bytes()
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2], "Bootstrap read/hash work charged")
    require(fingerprint(actual) == before and hashlib.sha256(raw).hexdigest() == expected,
            "Bootstrap JSON equals external expected bytes")
    result = json.loads(raw)
    budget()
    return result

def source_code_guard():
    global _HASH_WORK
    actual = canonical(AUTHOR, fresh=True)
    before = fingerprint(actual)
    require(before[2] <= 8 << 20, "Bounded frozen source compilation")
    raw = actual.read_bytes()
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2] and fingerprint(actual) == before,
            "Stable source compilation read/hash work charged")
    require(len(raw) <= 8 << 20 and hashlib.sha256(raw).hexdigest()
            == _FROZEN[actual.relative_to(ROOT).as_posix()], "Exact bounded new source compilation")
    tree = ast.parse(raw)
    declared = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    compiled = compile(raw, str(AUTHOR), "exec", dont_inherit=True, optimize=0)
    codes = {c.co_name: c for c in compiled.co_consts
             if isinstance(c, types.CodeType) and c.co_name in declared}
    require(set(codes) == declared, "Every declared new source function compiled without execution")
    for name in sorted(declared):
        budget()
        function = globals()[name]
        require(isinstance(function, types.FunctionType) and function.__globals__ is globals()
                and function.__code__ == codes[name], "Every loaded function equals frozen current source")

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

def known_runtime_admission(original_e11_manifest):
    """Retain original full expected stdlib pins before strict bootstrap origins."""
    global _STANDARD_RUNTIME_MEMBERS
    expected = original_e11_manifest["external_runtime_inputs"]
    require(type(expected) is dict and len(expected) == 2842, "Exact original E11 external runtime map")
    for key, pin in expected.items():
        require(Path(key).is_absolute(), "Original external runtime spelling")
        bind(Path(key), pin)
    members = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = members
    required = {Path(key) for key in expected} | {LAUNCHER}
    require(members == required, "Complete original isolated runtime membership, no observed expectations")
    size = 0
    for path in sorted(members):
        budget()
        size += path.stat().st_size
    require(len(members) <= MAX_RUNTIME_FILES and size <= MAX_RUNTIME_BYTES,
            "Original finite stdlib runtime budgets")
    return {"files": len(members), "bytes": size, "original_full_expected_SHA_before_origins": True,
            "isolated_no_site": True, "numerical_packages_loaded": False}

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


def current_review_admission(ready, authors):
    require(type(ready["static_review_expected_SHA256"]) is dict
            and set(ready["static_review_expected_SHA256"]) == set(CURRENT_REVIEW_PATHS),
            "Exactly current author QA, independent SCI/lifecycle peer and ROOT static review")
    records = {}
    for key in CURRENT_REVIEW_PATHS:
        pin = ready["static_review_expected_SHA256"][key]
        record = bootstrap_json(ROOT / key, pin)
        require(record["passed"] is True and record.get("blockers", []) == []
                and record["author_method_SHA256"] == authors,
                "Every current direct static review passed for exact new trio")
        if key == AUTHOR_QA_KEY:
            require(record["target_imported_or_executed"] is False
                    and record["scientific_evaluation_performed"] is False,
                    "Current author QA is source/metadata only")
        records[key] = {"expected_SHA256": pin, "direct_current_input_member": key in _FROZEN}
    require(all(row["direct_current_input_member"] for row in records.values()),
            "All current reviews bound before first origin guard")
    return records


def checked_method_graph(method, supplement):
    require(object_sha(method["selected_single_log_prefix_contract"]) == CONTRACT_OBJECT_SHA
            and method["selected_single_log_prefix_contract"] == SELECTED_CONTRACT,
            "Exact original seven-node contract, no new source or law")
    require(method["finite_protocol_unevaluated"] == FINITE_PROTOCOL
            and method["prospective_single_log_prefix_theorem"] == THEOREM,
            "Exactly two uncombined assemblies and dependent-safe five terms")
    require(supplement["active_and_archived_finite_role_graph"] == ROLE_GRAPH
            and supplement["two_literal_profile_adapter_contract"] == PROFILE_CONTRACT,
            "Exact active9/archive8/aliases and original90/130 literal fields")
    require(method["prospective_fixed_inclusive_owned_ledger"] == PLANNED_FILES
            and len(PLANNED_FILES) == 27
            and method["original_caps_prospective_unchanged"] == ORIGINAL_CAPS,
            "Exact27 ledger and original charged budgets")
    snapshots = method["complete_original_cited_owner_snapshots"]
    require(set(snapshots) == set(ROLE_GRAPH["owner_snapshot_SUMMARIES_no_large_map_duplicate"]),
            "Exactly17 original snapshot dictionaries, active9 and archival8")
    for name, summary in ROLE_GRAPH["owner_snapshot_SUMMARIES_no_large_map_duplicate"].items():
        require(object_sha(snapshots[name]) == summary["complete_original_snapshot_canonical_JSON_SHA256"],
                "All original wrappers/map/key/field-presence objects unchanged")
    for profile in ("primary90", "independent130"):
        require(object_sha(method["literal_uncombined_first_prefix_adapters"][profile])
                == PROFILE_CONTRACT[profile]["complete_uncombined_adapter_canonical_JSON_SHA256"],
                "Each full saved adapter uncombined and literal")


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


def admit_history_roles(method, ready):
    history_roles = method["prospective_proof_and_citation_roles"]["old_E11_failed_completed_cache_and_serialization_roles_unchanged_archival"]
    require(history_roles["failed_E11_V1_opaque_history"] == FAILED_E11_V1_HISTORY,
            "Complete immutable failed19 history retained")
    native_ready = read(ROOT / NATIVE_READY_KEY)
    scalar_ready = read(bind(ROOT / COMPLETED_E11_READY_KEY, COMPLETED_E11_READY_SHA))
    for label, source, old in (
        ("completed_native_author", RESEARCH / "experiment_e11_native_coordinate_squared_l2_v1.py", native_ready),
        ("completed_scalar_V2", RESEARCH / "experiment_e11_scalar_midpoint_l2_v2.py", scalar_ready),
    ):
        expected = HISTORICAL_CACHE_PARTITIONS[label]
        require({"existing_expected_SHA256": old["existing_new_code_cache_SHA256"],
                 "absent_paths": old["absent_new_code_cache_paths"]} == expected,
                "Historical completed cache namespace remains original")
        historical_code_cache_partition(source, expected)
    require(ready["historical_cache_partitions"] == HISTORICAL_CACHE_PARTITIONS,
            "All three old cache namespaces externally declared, no old grant clone")
    retain_failed_e11_v1()
    for name, pin in FAILED_E11_V1_HISTORY["author_method_SHA256"].items():
        bind(RESEARCH / name, pin)
    for key, pin in FAILED_E11_V1_HISTORY["static_review_expected_SHA256"].items():
        bind(ROOT / key, pin)
    return {"completed_native_and_scalar_READY_role": "historical exact cache and source custody only",
            "failed19_original_READY_author_review_and_missing_seals_preserved": True,
            "checker003_saved_record_only_no_reexecution": True, "checker002_no_completion": True}


def first_log_admission(ready_sha):
    global _FULL_ADMISSION
    startup_decimal_policy()
    ready = bootstrap_json(READY, ready_sha)
    require(ready["schema"] == "root-e11-first-log-prefix-squared-L2-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True
            and ready["first_log_prefix_rational_assembly_authorized"] is True
            and ready["output"] == OUTPUT.relative_to(ROOT).as_posix(), "Separate first-log-only ROOT release")
    authors = ready["author_method_SHA256"]
    require(type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
            "Exactly new first-log author trio")
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = bootstrap_json(PREFLIGHT, authors[PREFLIGHT.name])
    require(policy["schema"] == "e11-first-log-prefix-squared-L2-preflight-v1"
            and policy["author_SHA256"] == authors[AUTHOR.name] and policy["method_SHA256"] == authors[METHOD_DOC.name]
            and policy["first_log_prefix_rational_assembly_authorized"] is False,
            "Dormant policy baseline with distinct external ROOT grant")
    for key, value in COMMON_EXPECTATIONS.items():
        require(policy[key] == ready[key] == value, "Exact current roles/caps/literals/finite graph")
    for key, value in flags().items():
        require(policy[key] == ready[key] == value, "No financial or old scientific permission clone")
    exact_startup_literals(ready, policy, ready_sha)
    code_cache_policy(ready)
    require(ready["accepted_method_and_review_expected_SHA256"] == AUTHOR_INPUTS,
            "Exact external current METHOD/admission/clarification/acceptanceV2 map")
    for key, pin in AUTHOR_INPUTS.items():
        bind(ROOT / key, pin)
    current_reviews = current_review_admission(ready, authors)
    method = bootstrap_json(ROOT / METHOD_KEY, AUTHOR_INPUTS[METHOD_KEY])
    supplement = bootstrap_json(ROOT / SUPPLEMENT_KEY, AUTHOR_INPUTS[SUPPLEMENT_KEY])
    native_snapshot = method["complete_original_cited_owner_snapshots"]["E11_native_coordinate_squared_L2_run001"]
    native_manifest = bootstrap_json(ROOT / native_snapshot["manifest_path"], native_snapshot["literal_expected_manifest_SHA256"])
    require(native_manifest["passed"] is native_manifest["completed"] is True
            and native_manifest["budget_censored"] is False,
            "Completed native-coordinate prerequisite, never a current execution grant")
    runtime = known_runtime_admission(native_manifest)
    serialization_runtime_admission()
    source_code_guard()
    require(policy["current_definition_AST_SHA256"] == definition_AST_pins(),
            "Complete current source definition AST map before origins")
    require(type(E11FirstLogPrefixReject) is type and E11FirstLogPrefixReject.__bases__ == (ValueError,)
            and E11FirstLogPrefixReject.__module__ == __name__, "Dedicated current exception class")
    strict_loaded_origins()
    fixed_integer_policy()
    checked_method_graph(method, supplement)
    for field in ("selected_original_owned_artifact_pins", "selected_original_readonly_source_pins"):
        for key, pin in method[field].items():
            bind(ROOT / key, pin)
    owners = {}
    snapshots = method["complete_original_cited_owner_snapshots"]
    for name in ACTIVE_OWNERS:
        full_active_owner(name, snapshots[name], ROLE_GRAPH["archived_equal_SHA_source_aliases_exact"])
        owners[name] = ROLE_GRAPH["owner_snapshot_SUMMARIES_no_large_map_duplicate"][name]
    archival = {name: archive_owned_custody(name, snapshots[name]) for name in ARCHIVE_CITATIONS}
    histories = admit_history_roles(method, ready)
    strict_loaded_origins()
    _FULL_ADMISSION = True
    return ready, policy, method, supplement, owners, archival, histories, runtime, current_reviews


def definition_AST_pins():
    require(AUTHOR.relative_to(ROOT).as_posix() in _FROZEN, "Current source admitted before AST witness")
    actual = canonical(AUTHOR, fresh=True)
    before = fingerprint(actual)
    require(actual.is_file() and before[2] <= 8 << 20, "Pre-read bounded current plaintext AST source")
    with actual.open("rb") as stream:
        raw = stream.read(before[2] + 1)
    global _HASH_WORK
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and fingerprint(actual) == before and len(raw) == before[2]
            and hashlib.sha256(raw).hexdigest()
            == _FROZEN[AUTHOR.relative_to(ROOT).as_posix()], "Exact source AST witness read")
    tree = ast.parse(raw)
    return {node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


def fresh_first_log_union():
    """Expected inputs only; current owned evidence hashes never synthesize input authority."""
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical, fresh=True) == actual, "Every lexical input stays confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == pin, "Exact expected overlap; unresolved conflict HOLD")
            union[path] = pin
    for path, pin in _OBSERVED.items():
        if path.is_relative_to(OUTPUT):
            continue
        require(path in union and union[path] == pin, "Observed input must already have external expectation")
    require(len(union) <= MAX_REFERENCES, "Finite full expected role union")
    size = 0
    for path, pin in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES and digest(actual, fresh=True, already_resolved=True) == pin,
                "Complete uncached physical/stat/SHA input union")
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, "All17 owned and failed19 inventories unchanged")
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS, "Strict original2842 runtime membership unchanged")
    require(not any(path.exists() or path.is_symlink() or path.resolve(strict=False) != path
                    for path in _ABSENT_RUNTIME), "All declared exact absences retained")
    for path, pin in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == pin, "Every declared present source cache unchanged")
    require(all(key in _FROZEN for key in CURRENT_REVIEW_PATHS) and all(key in _FROZEN for key in AUTHOR_INPUTS),
            "Every exact current review/method remains direct union authority")
    strict_loaded_origins()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_physical_resolve_stat_SHA": True,
            "active9": ACTIVE_OWNERS, "archive8_opaque_custody_only": ARCHIVE_CITATIONS,
            "current_reviews_direct_expected_members": CURRENT_REVIEW_PATHS,
            "owned_generated_evidence_excluded_from_input_expectations": True,
            "absent_paths": sorted(str(path) for path in _ABSENT_RUNTIME),
            "owned_inventory_identity_SHA256": {str(directory): object_sha(sorted(str(path) for path in members))
                                                for directory, members in _OWN_INVENTORIES.items()}}


class E11FirstLogPrefixReject(ValueError):
    pass


def valid_first_log_scope(scope):
    if scope["weak_price_bias_total_used_as_same_coupling_strong_L1"] is not False:
        raise E11FirstLogPrefixReject("REJECT_WEAK_PRICE_AS_STRONG_L1")
    if scope["digital_pair_independence_assumed"] is not False or scope["cross_terms_set_zero_by_digital_independence"] is not False:
        raise E11FirstLogPrefixReject("REJECT_DIGITAL_PAIR_INDEPENDENCE_OR_ZERO_CROSS_TERM")
    if (scope["signed_cmul_floor_values"] != [3492, 3493] or scope["literal_error_components"] != ["ea", "eb", "e0", "ed"]
            or scope["floor_error_coefficient"] != 2 or scope["signed144_product_safety"] is not True
            or scope["all_stored72_partial_safety"] is not True):
        raise E11FirstLogPrefixReject("REJECT_MISSING_FLOOR_OR_LITERAL_ERROR")
    exact = {"case": "B4x12", "asset_zero_based": 0, "contractual_date_one_based": 1,
             "raw_preclip_log_value": 3542, "ordered_native_normal_values": [94, 125],
             "ordered_original_normal_indices": [0, 1], "target_literal_SHA256": SELECTED_CONTRACT["target_literal_SHA256"],
             "ideal_reference_model": "A02_B4x12_exact_decimal_shared_original_gaussian",
             "source_seven_node_slice": SELECTED_CONTRACT["source_seven_node_slice_saved_metadata"]}
    if any(scope[key] != value for key, value in exact.items()):
        raise E11FirstLogPrefixReject("REJECT_CHANGED_SOURCE_VALUE_PAIR_TARGET_OR_LAW")
    return True


def source_first_log_witness(method):
    contract = method["selected_single_log_prefix_contract"]
    target = read(ROOT / contract["target_path"])
    require(target["width"] == 72 and target["fraction_bits"] == 40, "Original signed72/F40 source")
    selected = []
    wanted = {node["out"][0] for node in contract["source_seven_node_slice_saved_metadata"]}
    for node in target["nodes"]:
        budget()
        if any(value in wanted for value in node["out"]):
            selected.append(node)
    require(selected == contract["source_seven_node_slice_saved_metadata"], "Exact original seven stored source nodes")
    witnesses = {}
    for key, row in method["original_source_AST_witnesses_readonly"].items():
        source_key, name = key.split("::")
        path = canonical(ROOT / source_key, fresh=True)
        require(source_key in _FROZEN, "Original plaintext witness requires prior externally expected pin")
        before = fingerprint(path)
        require(path.is_file() and before[2] <= 8 << 20, "Pre-read bounded original plaintext source witness")
        with path.open("rb") as stream:
            raw = stream.read(before[2] + 1)
        global _HASH_WORK
        _HASH_WORK += len(raw)
        require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2] and fingerprint(path) == before
                and hashlib.sha256(raw).hexdigest() == _FROZEN[source_key],
                "Original source AST witnessed from fixed plaintext only")
        text = raw.decode("utf-8")
        definitions = {node.name: node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef)}
        node = definitions[name]
        require(ast.get_source_segment(text, node) == row["definition_text_readonly"]
                and hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest() == row["normalized_AST_SHA256"],
                "Original signed cmul floor/add/no-clip source definition exact")
        witnesses[key] = row["normalized_AST_SHA256"]
    roles = method["all_original_sampler_pair_and_financial_role_bindings"]["B4x12"]
    prefix = [item for item in roles["financial_roles"]["prefix_witnesses"]
              if item["asset"] == 0 and item["date"] == 0]
    require(prefix == [contract["original_prefix_witness"]], "Date convention and raw3542 exact original prefix")
    require(roles["joint_pair_scopes"][0] == contract["original_shared_pair_scope"],
            "Original shared pair and94/125 source normal identities preserved")
    scope = {"weak_price_bias_total_used_as_same_coupling_strong_L1": False,
             "digital_pair_independence_assumed": False, "cross_terms_set_zero_by_digital_independence": False,
             "signed_cmul_floor_values": [3492, 3493], "literal_error_components": ["ea", "eb", "e0", "ed"],
             "floor_error_coefficient": 2, "signed144_product_safety": True, "all_stored72_partial_safety": True,
             "case": "B4x12", "asset_zero_based": 0, "contractual_date_one_based": 1,
             "raw_preclip_log_value": 3542, "ordered_native_normal_values": [94, 125],
             "ordered_original_normal_indices": [0, 1], "target_literal_SHA256": contract["target_literal_SHA256"],
             "ideal_reference_model": "A02_B4x12_exact_decimal_shared_original_gaussian",
             "source_seven_node_slice": selected}
    valid_first_log_scope(scope)
    return scope, {"selected_contract": contract, "original_AST_pins_plaintext_only": witnesses,
                   "source_joins_only_no_source_evaluator_called": True, "stock4021_not_certified": True}


def literal_first_log_inputs(method):
    values = {}
    for profile in ("primary90", "independent130"):
        adapter = method["literal_uncombined_first_prefix_adapters"][profile]
        record = read(ROOT / adapter["coordinate_squared_B_path"])
        require(record[adapter["coordinate_squared_B_field"]] == adapter["coordinate_squared_B_uncombined_literal"],
                "Completed original continuous-to-native coordinate B, profile kept uncombined")
        envelope = read(ROOT / adapter["path"])
        case = envelope["cases"]["B4x12"] if profile == "primary90" else envelope["B4x12"]
        require(all(case[key] == value for key, value in adapter["fields"].items()),
                "Each full selected A02 adapter field equals its original saved literal")
        native_field_names = (["actual_common_literal", "actual_idio_literal", "actual_drift_literal", "actual_initial_literal"]
                              if profile == "primary90" else ["actual_common_raw", "actual_idio_raw", "actual_drift_raw", "actual_initial_raw"])
        require([case[key] for key in native_field_names]
                == [SELECTED_CONTRACT[key] for key in ("actual_common_literal", "actual_idio_literal", "actual_drift_signed_literal", "actual_initial_literal")],
                "Native coefficient/constants source joins exact")
        if profile == "primary90":
            require(case["every_signed144_scaled_normal_product_safe"] is True
                    and case["every_stored72_raw_partial_sum_safe"] is True
                    and case["signed_scaled_normal_floors_per_increment"] == 2
                    and case["addition_rounding_paid"] == 0, "Signed144 and all72 partials safe, both floors paid")
        else:
            require(case["every_stored_partial_sum_and_product_safe"] is True
                    and case["additive_rounding_zero_only_after_no_wrap"] is True
                    and case["every_original_driver_once"] is True, "Independent original signed safety and multiplicity")
        mapping = PROFILE_CONTRACT[profile]["literal_error_role_to_original_field"]
        values[profile] = {"B": adapter["coordinate_squared_B_uncombined_literal"],
                           **{role: case[key] for role, key in mapping.items()}}
    return values


def primary_log_components(inputs):
    original = inputs["primary90"]
    c = {key: checked_ratio(original[key]) for key in ("B", "ea", "eb", "e0", "ed")}
    require(all(value >= 0 for value in c.values()), "Positive saved primary component allowances")
    c.update(aN=Fraction(60222732077, 1 << 40), bN=Fraction(73757482253, 1 << 40), tau=Fraction(1, 1 << 40))
    c["kappa"] = plus(plus(c["e0"], c["ed"]), times(Fraction(2), c["tau"]))
    return c


def primary_log_squared(c):
    coefficients = plus(times(c["aN"], c["aN"]), times(c["bN"], c["bN"]))
    coordinate = times(coefficients, c["B"])
    literals = plus(times(c["ea"], c["ea"]), times(c["eb"], c["eb"]))
    constant = times(c["kappa"], c["kappa"])
    result = times(Fraction(5), plus(plus(coordinate, literals), constant))
    return {"schema": "e11-first-log-prefix-squared-L2-bound-v1", "profile": "primary90",
            "dimensionless_squared_log_error_upper": pair_literal(result),
            "existing_primary_stage_ledger": {"native_weighted_coordinate": pair_literal(coordinate),
                "continuous_coefficient_literal_errors_squared": pair_literal(literals),
                "constants_and_two_floors_squared": pair_literal(constant)},
            "pointwise_Cauchy_terms": 5, "continuous_coordinate_second_moments": [1, 1],
            "digital_pair_independence_assumed": False, "continuous_tail_discarded": False,
            "exact_raw_log_value": 3542, "full_financial_output_certified": False}


def independent_log_components(inputs):
    original = inputs["independent130"]
    c = {key: checked_ratio(original[key]) for key in ("ed", "e0", "eb", "ea", "B")}
    require(all(value >= 0 for value in c.values()), "Independent own130 saved positive allowances")
    c["tau"] = Fraction(1, 1099511627776)
    c["bN"] = Fraction(73757482253, 1099511627776)
    c["aN"] = Fraction(60222732077, 1099511627776)
    c["kappa"] = plus(times(c["tau"], Fraction(2)), plus(c["ed"], c["e0"]))
    return c


def independent_log_squared(c):
    native_b = times(times(c["bN"], c["bN"]), c["B"])
    native_a = times(c["B"], times(c["aN"], c["aN"]))
    coefficient_b = times(c["eb"], c["eb"])
    coefficient_a = times(c["ea"], c["ea"])
    constant = times(c["kappa"], c["kappa"])
    result = times(plus(plus(plus(native_b, native_a), coefficient_b), plus(coefficient_a, constant)), Fraction(5))
    return {"schema": "e11-first-log-prefix-squared-L2-bound-v1", "profile": "independent130",
            "dimensionless_squared_log_error_upper": pair_literal(result),
            "existing_independent_stage_ledger": {"native_b_coordinate": pair_literal(native_b),
                "native_a_coordinate": pair_literal(native_a), "coefficient_b_squared": pair_literal(coefficient_b),
                "coefficient_a_squared": pair_literal(coefficient_a), "constants_and_two_floors_squared": pair_literal(constant)},
            "pointwise_Cauchy_terms": 5, "continuous_coordinate_second_moments": [1, 1],
            "digital_pair_independence_assumed": False, "continuous_tail_discarded": False,
            "exact_raw_log_value": 3542, "full_financial_output_certified": False}


def encoded_log_components(c):
    return {"exact_rational_components": {key: pair_literal(value) for key, value in c.items()},
            "two_signed_cmul_floor_errors_paid": True, "all_original_signed144_products_and_stored72_partials_required": True,
            "addition_rounding_zero_after_no_wrap_only": True, "original_shared94_125_pair_not_independent": True}


def independently_reconcile_log_primary(inputs, c, result):
    """Check identities of existing primary records; no third numerical candidate."""
    require(all(c[key] == checked_ratio(inputs["primary90"][key]) for key in ("B", "ea", "eb", "e0", "ed")),
            "Primary identity uses its own original saved adapter only")
    require(c["aN"] == Fraction(60222732077, 1099511627776)
            and c["bN"] == Fraction(73757482253, 1099511627776)
            and c["tau"] == Fraction(1, 1099511627776), "Native coefficient and floor-unit identities")
    require(c["kappa"] == plus(times(c["tau"], Fraction(2)), plus(c["ed"], c["e0"])),
            "Constants and both exact signed-floor allowances paid")
    stages = {key: checked_ratio(value) for key, value in result["existing_primary_stage_ledger"].items()}
    require(stages["native_weighted_coordinate"] == plus(times(c["B"], times(c["bN"], c["bN"])),
                                                           times(times(c["aN"], c["aN"]), c["B"]))
            and stages["continuous_coefficient_literal_errors_squared"] == plus(times(c["eb"], c["eb"]), times(c["ea"], c["ea"]))
            and stages["constants_and_two_floors_squared"] == times(c["kappa"], c["kappa"]),
            "Distinct expanded identities reconcile existing primary stages")
    require(checked_ratio(result["dimensionless_squared_log_error_upper"])
            == plus(plus(times(Fraction(5), stages["constants_and_two_floors_squared"]),
                         times(stages["continuous_coefficient_literal_errors_squared"], Fraction(5))),
                    times(Fraction(5), stages["native_weighted_coordinate"])),
            "Pointwise five-term Cauchy identity, no new envelope returned")
    return {"passed": True, "existing_primary_expression_reconciled_by_distinct_expanded_order": True,
            "total_envelope_assemblies": 2, "third_candidate_or_bound_returned": False,
            "independent130_own_literals_kept_separate": True, "outward_profile_nesting_required": False}


def four_first_log_controls(positive):
    require(valid_first_log_scope(positive) is True, "Positive exact metadata validator before fixed mutations")
    results = []
    for category in CONTROL_SPECS:
        mutations = []
        for mutation in category["fixed_bad_metadata_variants"]:
            budget()
            bad = dict(positive)
            if "omitted_signed_cmul_floor_value" in mutation:
                bad["signed_cmul_floor_values"] = [value for value in positive["signed_cmul_floor_values"]
                                                  if value != mutation["omitted_signed_cmul_floor_value"]]
            elif "omitted_error_component" in mutation:
                bad["literal_error_components"] = [value for value in positive["literal_error_components"]
                                                   if value != mutation["omitted_error_component"]]
            else:
                bad.update(mutation)
            try:
                valid_first_log_scope(bad)
            except E11FirstLogPrefixReject as error:
                require(type(error) is E11FirstLogPrefixReject and str(error) == category["code"],
                        "Only exact dedicated intended first-log semantic rejection counts")
            else:
                require(False, "Fixed invalid first-log metadata was accepted")
            mutations.append({"fixed_mutation": mutation, "exact_structural_rejection": True})
        results.append({"code": category["code"], "fixed_variants": mutations, "passed": True})
    require(len(results) == 4 and sum(len(row["fixed_variants"]) for row in results) == 13,
            "Exactly four registered categories and13 fixed metadata variants")
    return {"passed": True, "category_count": 4, "metadata_variants": 13, "categories": results,
            "budget_unrelated_or_IO_error_credit": False, "new_numerical_candidate_or_fixture": False}


def flags():
    return {"item": "E11", "one_preclip_log_squared_L2_only": True, "full_E11_completed": False,
            "native_financial_path_or_policy_L2_verified": False, "full_price_certificate": False,
            "G2_transfer": False, "full_G2": False, "adoption": False, "financial_adoption": False,
            "cost_comparison": False, "cost_transfer": False, "quantum_advantage": False,
            "physical_certificate": False, "estimator_schedule_emitted": False,
            "source_emission": False, "gate_emission": False, "source_substitution_authorized": False,
            "prices_or_paths_sampled": False, "fits_or_pilots": False, "new_transcendental_series": False,
            "native_arrays_generated_or_replayed": False, "old_numerical_helpers_or_evaluators_called": False,
            "digital_pair_independence": False, "native_source_clipping_inserted": False,
            "fixture_credit": 0, "new_test_credit": 0, "new_global_fixture_credit": 0, "local_only": True}


def main():
    global _STARTED, _OUTPUT_CREATED_BY_THIS_RUN
    _STARTED = process_started()
    runtime_scopes()
    invocation_check()
    startup_decimal_policy()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists() and not OUTPUT.is_symlink(),
            "One exclusive first-log output route")
    try:
        ready, policy, method, supplement, owners, archive, histories, runtime, current_reviews = first_log_admission(args.ready_sha256)
        first = fresh_first_log_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        _OUTPUT_CREATED_BY_THIS_RUN = True
        copies = {"executed_controller.py": AUTHOR, "executed_preflight.md": METHOD_DOC,
                  "executed_policy.json": PREFLIGHT, "executed_ROOT_READY.json": READY,
                  "reviewed_next_method.md": ROOT / METHOD_MD_KEY, "reviewed_next_method.json": ROOT / METHOD_KEY,
                  "reviewed_independent_method_peer.json": ROOT / METHOD_PEER_KEY,
                  "reviewed_ROOT_method.json": ROOT / METHOD_ROOT_KEY}
        for name, path in copies.items():
            copy(path, name)
        save("protocol.json", policy)
        save("run_started.json", {"created_UTC": time.time_ns(), "PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        save("interpreter.json", {"runtime": runtime, "literal_startup": EXACT_STARTUP})
        save("loaded_module_origins.json", {"fresh_known_only_present_origins": True,
             "upfront_serializer": SERIALIZATION_RUNTIME, "all_current_reviews_bound_before_first_origin": current_reviews,
             "current_cache_partition": {"present": ready["existing_new_code_cache_SHA256"], "absent": ready["absent_new_code_cache_paths"]}})
        save("active_and_archived_role_graph.json", {"active9": owners, "archive8": archive,
             "aliases": ROLE_GRAPH["archived_equal_SHA_source_aliases_exact"], "historical_roles": histories,
             "one_METHOD_snapshot_authority": {"path": METHOD_KEY, "SHA256": AUTHOR_INPUTS[METHOD_KEY]},
             "all17_compact_summaries_not_full_snapshot_duplicates": True})
        save("literal_prior_component_adapters.json", PROFILE_CONTRACT)
        save("fresh_full_input_union_before_assembly.json", first)
        positive, witness = source_first_log_witness(method)
        save("source_first_log_prefix_witness.json", witness)
        inputs = literal_first_log_inputs(method)
        primary = primary_log_components(inputs)
        primary_bound = primary_log_squared(primary)
        save("primary_log_prefix_components.json", encoded_log_components(primary))
        save("primary_log_prefix_squared_L2.json", primary_bound)
        independent = independent_log_components(inputs)
        independent_bound = independent_log_squared(independent)
        save("independent_log_prefix_components.json", encoded_log_components(independent))
        save("independent_log_prefix_squared_L2.json", independent_bound)
        reconciliation = independently_reconcile_log_primary(inputs, primary, primary_bound)
        save("independent_primary_proof_check.json", reconciliation)
        controls = four_first_log_controls(positive)
        save("four_fixed_reject_controls.json", controls)
        save("qualification_and_remaining_gaps.json", {"selected_preclip_log_only": True, "dimensionless_squared_log_units": True,
             "original_weak_price_bias_not_strong_L1": True, "hybrid_native_and_C07_date1_range_lemma_only_scoped": True,
             "all_date_exp_clip_stock_basket_barrier_payoff_policy_L2_open": True,
             "remaining_original_split_obligations": method["remaining_split_obligations"], **flags()})
        second = fresh_first_log_union()
        save("fresh_full_input_union_after_assembly.json", second)
        summary = {"schema": "e11-first-log-prefix-squared-L2-summary-v1", "passed": True, "completed": True,
             "budget_censored": False, "numerical_envelope_assemblies": 2, "primary_bound": primary_bound,
             "independent_bound": independent_bound, "reconciliation": reconciliation, "four_fixed_controls": controls,
             "selected_source_contract_SHA256": CONTRACT_OBJECT_SHA, "both_complete_fresh_input_unions": [first, second],
             "planned_manifest_inclusive_owned_files": 27, "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
             "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        members = inventory(OUTPUT)
        require({path.name for path in members} == set(PLANNED_FILES) - {"manifest.json"}, "Exactly fixed27 inclusive ledger before seal")
        files, total = {}, 0
        for path in sorted(members):
            budget()
            total += path.stat().st_size
            require(total <= MAX_OWN_BYTES and len(files) < MAX_OWN_FILES - 1, "Final manifest reserve")
            files[path.name] = digest(path, fresh=True)
        complete_manifest({"schema": "e11-first-log-prefix-squared-L2-manifest-v1", "files": files,
             "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL, "manifest_self_hash_excluded": True,
             "passed": True, "completed": True, "budget_censored": False, "both_complete_fresh_input_unions": [first, second],
             "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}, files, total)
        budget()
        print(json.dumps({"passed": True, "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True), **flags()}), flush=True)
    except BaseException as error:
        if _OUTPUT_CREATED_BY_THIS_RUN:
            retain_failure(error)
        raise


if __name__ == "__main__":
    main()
