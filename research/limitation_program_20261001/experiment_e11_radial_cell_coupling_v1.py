"""Dormant E11 radial-cell/ideal-midpoint squared-L2 controller. Separate own ROOT READY and full current three reviews are mandatory. No native, stock, series, sampling or numerical package execution."""
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
ROOT = Path('C:/Users/prith/quantum_option_pricing')
RESEARCH = ROOT / 'research/limitation_program_20261001'
AUTHOR = RESEARCH / 'experiment_e11_radial_cell_coupling_v1.py'
METHOD_DOC = RESEARCH / 'E11_RADIAL_CELL_COUPLING_PREFLIGHT_V1.md'
PREFLIGHT = RESEARCH / 'e11_radial_cell_coupling_preflight_v1.json'
READY = ROOT / '.context/E11_RADIAL_CELL_COUPLING_ROOT_READY_run001.json'
OUTPUT = ROOT / 'results/limitation_program_20261001/E11_radial_cell_coupling_run001'
BASE = Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
LAUNCHER = ROOT / '.context/frontier_t0_env/Scripts/python.exe'
LAUNCHER_SHA = '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5'
BASE_SHA = 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b'
CPU, ADMISSION, WALL = (180, 150, 600)
MAX_OWN_FILES, MAX_OWN_BYTES = (64, 128 * 1024 ** 2)
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = (4096, 512 * 1024 ** 2)
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = (100000, 8 * 1024 ** 3, 24 * 1024 ** 3)
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = (20000, 65536)
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
MAX_REDUCED_RATIONAL_BITS, MAX_ANALYTIC_TEMP_BITS = (131072, 524288)
_FROZEN, _EXTERNAL, _OBSERVED = ({}, {}, {})
_PATH_CACHE, _HASH_CACHE, _OWN_INVENTORIES = ({}, {}, {})
_ABSENT_RUNTIME, _STANDARD_RUNTIME_MEMBERS = (set(), set())
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = (None, None)
_HASH_WORK, _REFERENCES, _STARTED, _FULL_ADMISSION = (0, 0, None, False)
AUTHOR_INPUTS = {'.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': 'e7b4a988f5e50de4064f96d809177a22e0cb4a55388d42ba139697ac525307e3', '.context/E11_RADIAL_CELL_COUPLING_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'c552f2a95ac74a0815e6251737a5c68796260c981e83529366c13743d176d192', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json': '6ff35a0771cacaf0685d9943d27f86a6303c2ec1fb78ac8143edc1e9e735b92e', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.md': 'e1e9a5a9107483d1cb7c80f6f5e23098117bbaee7843f326ff97ead82182db25', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json': '65215242e73564d38c69afa0d62e9a1693d3bac30182f5f079b663d64d5b8042', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '4d58ff0a6aa1a0622000682879eec8c9d806206e230ee90d5679cd8845b954e7', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': 'be76c6299d743ba6b82dce19615c7ebb709f7f3f5bed1e06164b615af9d5989f', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.md': '076a3c8ac42884b550a29cb0114dfb23618e48ab3e54b9ef62830849d8a2f45a', '.context/E11_RADIAL_CELL_COUPLING_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json': 'cd288c2e58f04c8ea364075aaa5ede23b19ba7076e5b1534ec814ef723f46294'}
COMMON_EXPECTATIONS = {'G2_transfer': False, 'accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256': {'.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json': '65215242e73564d38c69afa0d62e9a1693d3bac30182f5f079b663d64d5b8042', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '4d58ff0a6aa1a0622000682879eec8c9d806206e230ee90d5679cd8845b954e7', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': 'be76c6299d743ba6b82dce19615c7ebb709f7f3f5bed1e06164b615af9d5989f', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.md': '076a3c8ac42884b550a29cb0114dfb23618e48ab3e54b9ef62830849d8a2f45a'}, 'accepted_symbolic_METHOD_MD_independent_ROOT_expected_SHA256': {'.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': 'e7b4a988f5e50de4064f96d809177a22e0cb4a55388d42ba139697ac525307e3', '.context/E11_RADIAL_CELL_COUPLING_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'c552f2a95ac74a0815e6251737a5c68796260c981e83529366c13743d176d192', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json': '6ff35a0771cacaf0685d9943d27f86a6303c2ec1fb78ac8143edc1e9e735b92e', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.md': 'e1e9a5a9107483d1cb7c80f6f5e23098117bbaee7843f326ff97ead82182db25'}, 'active_current_owner_names': ['E11_native_coordinate_squared_L2_run001', 'E11_scalar_midpoint_L2_numerical_run002'], 'adoption': False, 'cost_comparison': False, 'current_authoring_acceptance_SHA256': 'cd288c2e58f04c8ea364075aaa5ede23b19ba7076e5b1534ec814ef723f46294', 'current_authoring_acceptance_path': '.context/E11_RADIAL_CELL_COUPLING_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json', 'current_control_specs': [{'category': 'both_endpoint_cells', 'dedicated_tag': 'RADIAL_ENDPOINT_CELLS', 'fixed_bad_metadata_variants': [{'first_cell_paid': False}, {'last_cell_paid': False}]}, {'category': 'complete_aligned_dyadic_partition', 'dedicated_tag': 'RADIAL_WHOLE_CELL_PARTITION', 'fixed_bad_metadata_variants': [{'dyadic_indices': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}, {'dyadic_indices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}, {'whole_cell_alignment': False}]}, {'category': 'own_reciprocal_endpoint_provenance', 'dedicated_tag': 'RADIAL_LN2_ENDPOINT_ROLE', 'fixed_bad_metadata_variants': [{'reciprocal_endpoint_role': 'own_ledger_window_exact_upper'}, {'positive_ln2_enclosure_provenance': False}]}, {'category': 'radial_factor2_role', 'dedicated_tag': 'RADIAL_FACTOR2_ROLE', 'fixed_bad_metadata_variants': [{'coordinate_radial_factor': 1}, {'raw_radial_measure_role': 'old_factor2_midpoint_radial_stage'}]}, {'category': 'units_and_excluded_scopes', 'dedicated_tag': 'RADIAL_UNITS_SCOPE', 'fixed_bad_metadata_variants': [{'units': 'dollars_squared'}, {'new_native_coordinate_claim': True}, {'scalar_inverse_lipschitz_used': True}, {'downstream_financial_claim': True}]}], 'current_positive_scope': {'M': 4294967296, 'coordinate_radial_factor': 2, 'delta_pair_role': [1, 4294967296], 'downstream_financial_claim': False, 'dyadic_indices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'first_cell_paid': True, 'last_cell_paid': True, 'new_native_coordinate_claim': False, 'positive_ln2_enclosure_provenance': True, 'raw_radial_measure_role': 'unmultiplied_radial_squared_integral', 'reciprocal_endpoint_role': 'own_ledger_window_exact_lower', 'scalar_inverse_lipschitz_used': False, 'scope': 'E11_RADIAL_AND_IDEAL_MIDPOINT_ONLY', 'units': 'dimensionless_Gaussian_coordinate_squared', 'whole_cell_alignment': True}, 'current_static_review_paths': ['.context/E11_RADIAL_CELL_COUPLING_AUTHOR_STATIC_QA_run001.json', '.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_STATIC_PEER_run001.json', '.context/E11_RADIAL_CELL_COUPLING_ROOT_STATIC_REVIEW_run001.json'], 'default_decimal4300_no_setter': True, 'digital_pair_independence': False, 'estimator_schedule_emitted': False, 'exact12_copy_routes': {'executed_ROOT_READY.json': '.context/E11_RADIAL_CELL_COUPLING_ROOT_READY_run001.json', 'executed_controller.py': 'research/limitation_program_20261001/experiment_e11_radial_cell_coupling_v1.py', 'executed_policy.json': 'research/limitation_program_20261001/e11_radial_cell_coupling_preflight_v1.json', 'executed_preflight.md': 'research/limitation_program_20261001/E11_RADIAL_CELL_COUPLING_PREFLIGHT_V1.md', 'reviewed_ROOT_finite_review.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json', 'reviewed_ROOT_symbolic_review.json': '.context/E11_RADIAL_CELL_COUPLING_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json', 'reviewed_finite_method.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json', 'reviewed_finite_method.md': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.md', 'reviewed_finite_peer.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json', 'reviewed_symbolic_method.json': '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json', 'reviewed_symbolic_method.md': '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.md', 'reviewed_symbolic_peer.json': '.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json'}, 'exact29_inclusive_owned_ledger': ['executed_controller.py', 'executed_preflight.md', 'executed_policy.json', 'executed_ROOT_READY.json', 'reviewed_symbolic_method.json', 'reviewed_symbolic_method.md', 'reviewed_symbolic_peer.json', 'reviewed_ROOT_symbolic_review.json', 'reviewed_finite_method.json', 'reviewed_finite_method.md', 'reviewed_finite_peer.json', 'reviewed_ROOT_finite_review.json', 'run_started.json', 'interpreter.json', 'loaded_module_origins.json', 'original2_and_transitive12_scope.json', 'protocol.json', 'source_and_own_profile_adapters.json', 'five_radial_proof_controls.json', 'primary_radial_and_ideal_midpoint_bound.json', 'independent_radial_and_ideal_midpoint_bound.json', 'primary_same_profile_saved_comparison.json', 'independent_same_profile_saved_comparison.json', 'fresh_full_input_union_before_radial.json', 'fresh_full_input_union_after_radial.json', 'qualification_and_remaining_gaps.json', 'summary.json', 'completion_outcome.json', 'manifest.json'], 'expected_only_observations_output_excluded': True, 'finite_protocol': {'controls_categories_variants': [5, 13], 'midpoint_M': 4294967296, 'new_own_profile_radial_assemblies': 2, 'new_series_or_native_evaluations': 0, 'retries': 0, 'same_profile_old_saved_comparison_records': 2, 'whole_lower_band_terms': 31}, 'fits_or_pilots': False, 'fixture_credit': 0, 'full_E11_completed': False, 'full_original2_expected_registry_commitment': 'd056ae5e02ce07e604d2f2d4d35faf6845649a2a51a653b7a71dbe45cc058e89', 'full_price_certificate': False, 'gate_emission': False, 'item': 'E11', 'local_only': True, 'native12_transitive_citation_authority': {'each_full_snapshot_canonical_JSON_SHA256': {'A01_run011': 'e9d1cfaa6de54592a5fbc1ca9b4b2eb2813ae47351b7e5e2b794cc7a4b5fdaa4', 'A01_run014': '3a08cffa90ec2efba45fce55993216ff4a8ede31db83e8039e3a1ee00d26b8da', 'A02_BM_native_financial_bridge_audit_run002': '9b7b3956d1e58948dd8baea7d8b3fc738ee5b6ebedf371d3a3ba9a3493463fa7', 'A02_BM_native_financial_bridge_root_verification_run001': 'de6cde463a3d4df7b9247cbc455e3b5e651e0b00c57fade9e45630094ba0bb36', 'A02_BM_native_financial_bridge_run002': '2da2fe84d3a4eba45c8c818fa000ad7bf4f644509738489c680850f46d08f073', 'A02_quantile_financial_audit_run001': 'a22987c8bda0dcbd8ecbb5a442e3a840e2d6c04227ac41108bdfcd48a8cad828', 'A02_quantile_law_audit_run001': '1d72bba27529ecd4d4daff435b3b332956f4ccf0fc1f34ad727d596f124975b4', 'A10_coefficient_run001': 'bcfa30a62d3caa537b2cb485bed51fec1866c16895a0bbdc5422724ab0f0f37b', 'C06_pair_audit_run001': 'ba38b9be3319290278648495376e678cbb71ab4b1a06ac289f746714f27c3fa7', 'C06_pair_run001': '659d4ff845d18acab0187dc3d07f83b5786db7c9451320784c376aa85d25ad25', 'E10_continuous_moment_only_run002': 'a1d883c14a55d4924cf682688d7ed03ec2811c2eafa8386285c84fa25da7d231', 'E11_scalar_midpoint_L2_numerical_run002': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c'}, 'exact_original_owner_names': ['A01_run011', 'A01_run014', 'A02_BM_native_financial_bridge_audit_run002', 'A02_BM_native_financial_bridge_root_verification_run001', 'A02_BM_native_financial_bridge_run002', 'A02_quantile_financial_audit_run001', 'A02_quantile_law_audit_run001', 'A10_coefficient_run001', 'C06_pair_audit_run001', 'C06_pair_run001', 'E10_continuous_moment_only_run002', 'E11_scalar_midpoint_L2_numerical_run002'], 'expected_SHA256': '301a97276c10e6a4a23a663bffb0e4224ab83f5f37aeec377c71f20e2fef509c', 'field': ['cited_complete_original_packet_snapshots'], 'no_duplicate_original_full12_maps_or_native_arrays': True, 'not_automatically_new_runtime_or_success_owner_admission': True, 'original_active_archive_roles_unchanged': True, 'path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/reviewed_gap_map_method.json'}, 'native_arrays_generated_or_replayed': False, 'native_financial_path_or_policy_L2_verified': False, 'native_source_clipping_inserted': False, 'new_global_fixture_credit': 0, 'new_native_coordinate_certificate': False, 'new_transcendental_series': False, 'no_numeric_results_before_own_ROOT_READY': True, 'old_numerical_helpers_or_evaluators_called': False, 'original_caps': {'CPU_admission_creation_wall': [180, 150, 600], 'SOURCE_UTF8_bytes': 8388608, 'current_stdlib_runtime_files_bytes': [4096, 536870912], 'decimal_digits_default_only': 4300, 'owned_files_bytes': [64, 134217728], 'references_unique_bytes_hash_work': [100000, 8589934592, 25769803776], 'serialized_integer_reduced_rational_analytic_temporary_bits': [65536, 131072, 524288]}, 'original_history3_cache_roles': {'failed_scalar_V1': {'actual_original_cache_partition': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'], 'existing_expected_SHA256': {}}, 'old_execution_grant_inherited': False, 'original_READY_expected_SHA256': '855f25478139081cccaa804fc5a889fe4dcbdeeffed39e3d1f234ac365a3c6c9', 'original_READY_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run001.json', 'original_author_bare_key_to_declared_physical_path_roles': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md', 'original_expected_SHA256': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b'}, 'e11_scalar_midpoint_l2_numerical_preflight_v1.json': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\e11_scalar_midpoint_l2_numerical_preflight_v1.json', 'original_expected_SHA256': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27'}, 'experiment_e11_scalar_midpoint_l2_v1.py': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_scalar_midpoint_l2_v1.py', 'original_expected_SHA256': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6'}}, 'original_author_method_SHA256': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b', 'e11_scalar_midpoint_l2_numerical_preflight_v1.json': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27', 'experiment_e11_scalar_midpoint_l2_v1.py': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6'}, 'original_output': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run001', 'original_static_review_expected_SHA256': {'.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_AUTHOR_STATIC_QA_run001.json': '695cadc7fb64708bdd43bda53221299ff7c07c34474e866e6c8232b3d8623f55', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_INDEPENDENT_STATIC_PEER_next_run001.json': 'eb3e0c49cdcb19f2c4d5cf8f8a927caa6078c5dc92c344534091e8435a3bf4de', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_STATIC_REVIEW_run001.json': 'ca768374525412a7ffe3ee82e358ade56d98613d0599eb217b58dd65d52ad2d1'}}, 'native_V1': {'actual_original_cache_partition': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_native_coordinate_squared_l2_v1.cpython-312.pyc'], 'existing_expected_SHA256': {}}, 'old_execution_grant_inherited': False, 'original_READY_expected_SHA256': '136be8c070c5925d4a8ceac215788c3e2051b42289d9ca4e99b180ad7b6648c1', 'original_READY_path': '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json', 'original_author_bare_key_to_declared_physical_path_roles': {'E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md', 'original_expected_SHA256': '0218bd7d7a2ea047dfdcdf2bf402587e9ea7f70d79ca20a2f1eb0d04a172e4d5'}, 'e11_native_coordinate_squared_l2_preflight_v1.json': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\e11_native_coordinate_squared_l2_preflight_v1.json', 'original_expected_SHA256': '0f61e692116ee66cda0e6bfc3cbde926a87ca38a3bed8f2779064b1e74282678'}, 'experiment_e11_native_coordinate_squared_l2_v1.py': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_native_coordinate_squared_l2_v1.py', 'original_expected_SHA256': 'a60e773dbb23ff37fb3b631c53f270ee78ebcdf3963cc84165a8e13023f7b295'}}, 'original_author_method_SHA256': {'E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md': '0218bd7d7a2ea047dfdcdf2bf402587e9ea7f70d79ca20a2f1eb0d04a172e4d5', 'e11_native_coordinate_squared_l2_preflight_v1.json': '0f61e692116ee66cda0e6bfc3cbde926a87ca38a3bed8f2779064b1e74282678', 'experiment_e11_native_coordinate_squared_l2_v1.py': 'a60e773dbb23ff37fb3b631c53f270ee78ebcdf3963cc84165a8e13023f7b295'}, 'original_output': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001', 'original_static_review_expected_SHA256': {'.context/E11_NATIVE_COORDINATE_SQUARED_L2_INDEPENDENT_STATIC_PEER_next_run001.json': '8cb873a6531da25bfbe70490e743b21fa4cefe4c56044ecfc7177d5c61bfbdcc', '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json': '2a82f44cabd58afcacc9dd4b657219ad9e65e8a3a35a93f8bfd5ae2ec13d67eb'}}, 'scalar_V2': {'actual_original_cache_partition': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc'], 'existing_expected_SHA256': {}}, 'old_execution_grant_inherited': False, 'original_READY_expected_SHA256': '9a9d00407a8a6f763e9142d95d97e06dcadde3f2d0a73dfa9fcf167ced6f2c65', 'original_READY_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run002.json', 'original_author_bare_key_to_declared_physical_path_roles': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V2.md': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V2.md', 'original_expected_SHA256': 'c9055a5c36600cbf5912aa2dba918372277aafbcc4e1dbd28908d035b2347ba3'}, 'e11_scalar_midpoint_l2_numerical_preflight_v2.json': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\e11_scalar_midpoint_l2_numerical_preflight_v2.json', 'original_expected_SHA256': 'deb59afbd4bad7672dfe9d9ff8ae6a852de19bd385b3fd937290c3036fe8b715'}, 'experiment_e11_scalar_midpoint_l2_v2.py': {'original_declared_path': 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_scalar_midpoint_l2_v2.py', 'original_expected_SHA256': '37a3fc6d539f1afd41e4d2ce043a443e2b334f3042b938aae95811345d47a188'}}, 'original_author_method_SHA256': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V2.md': 'c9055a5c36600cbf5912aa2dba918372277aafbcc4e1dbd28908d035b2347ba3', 'e11_scalar_midpoint_l2_numerical_preflight_v2.json': 'deb59afbd4bad7672dfe9d9ff8ae6a852de19bd385b3fd937290c3036fe8b715', 'experiment_e11_scalar_midpoint_l2_v2.py': '37a3fc6d539f1afd41e4d2ce043a443e2b334f3042b938aae95811345d47a188'}, 'original_output': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002', 'original_static_review_expected_SHA256': {'.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_STATIC_REVIEW_run002.json': '465e1aeb28e7c04272c0444765dde2c07d8511e50565e5ce4417d12dfbdf136f', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_V2_AUTHOR_STATIC_QA_SUPPLEMENT_run001.json': 'c40ae5d0abd997cf88f6dd9542cf82703c954a06d24d44078002890d7d568363', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_V2_AUTHOR_STATIC_QA_run001.json': 'b645079132cc41ea237973ff7c362e137e13431a815ad340193d6a7fa16a9023', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_V2_INDEPENDENT_DELTA_PEER_run001.json': '33342b2b049c2b1b94aec1aeeedbef891c06d2a4d985720ee90fc79b978717e0'}}}, 'original_two_snapshot_authority': {'complete_original_snapshot_canonical_commitments': {'E11_native_coordinate_squared_L2_run001': '2212e6791fd01ccd8f9333b5e3ccf93df993178bdc0fb8d601f1cbc814197476', 'E11_scalar_midpoint_L2_numerical_run002': 'a71f6dc420f9b28ce9944c7ba052368c8269db34538e162d6329933b2eb8d20c'}, 'expected_SHA256': '6ff35a0771cacaf0685d9943d27f86a6303c2ec1fb78ac8143edc1e9e735b92e', 'field': 'complete_two_original_scientific_owner_snapshots', 'path': '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json'}, 'output': 'results/limitation_program_20261001/E11_radial_cell_coupling_run001', 'own_profile_input_roles': {'independent130': {'complete_literal_token_pair_equality_checked': True, 'exact_lower_ledger_pointer': ['endpoints', 2, 'window_exact', 0], 'exact_upper_ledger_pointer': ['endpoints', 2, 'window_exact', 1], 'lower_pointer': ['exact_component_allowances', 'ln2_lower'], 'no_original_endpoint_or_bound_value_copied_into_new_numeric_result': True, 'old_arithmetic_field': 'arithmetic_squared_L2_upper', 'old_coordinate_expected_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84', 'old_coordinate_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json', 'old_ideal_midpoint_field': 'ideal_midpoint_coordinate_squared_L2_upper', 'old_original_continuous_native_coordinate_field_NOT_new_result': 'continuous_to_original_native_coordinate_squared_L2_upper', 'ordinary4300_profile_record_token_census': [{'expected_SHA256': '6269a7bb56b776dd782ad4e417162a54f66314899497d8476cd585db058b02f6', 'integer_tokens': 805, 'maximum_integer_token_digits': 1987, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/independent_log_endpoint_ledger.json'}, {'expected_SHA256': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c', 'integer_tokens': 20, 'maximum_integer_token_digits': 766, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json'}, {'expected_SHA256': '71da4ec6f046ef77d8fdd7095178060b3a3b9194a45eebb399e523e8fa57cd84', 'integer_tokens': 8, 'maximum_integer_token_digits': 1054, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_coordinate_squared_L2_bound.json'}], 'original_component_expected_SHA256': '770027966cb8bba8cac32d77a40fd0b34e456f1a718ae34070b81280f4f1312c', 'original_component_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/independent_native_arithmetic_components.json', 'original_ln2_fixed_terms_history_only': 1024, 'original_ln2_ledger_expected_SHA256': '6269a7bb56b776dd782ad4e417162a54f66314899497d8476cd585db058b02f6', 'original_ln2_ledger_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/independent_log_endpoint_ledger.json', 'original_ln2_window_pointer': ['endpoints', 2, 'window_exact'], 'positive_enclosure_mathematical_authority': 'Original certified ln2 windows plus original native source input ordering; new numerical guard not run', 'profile_is_role_label_not_invented_coordinate_record_field': True, 'upper_pointer': ['exact_component_allowances', 'ln2_upper'], 'values_computed_or_substituted_now': False}, 'primary90': {'complete_literal_token_pair_equality_checked': True, 'exact_lower_ledger_pointer': ['endpoints', 2, 'window_exact', 0], 'exact_upper_ledger_pointer': ['endpoints', 2, 'window_exact', 1], 'lower_pointer': ['exact_component_allowances', 'ln2_lower'], 'no_original_endpoint_or_bound_value_copied_into_new_numeric_result': True, 'old_arithmetic_field': 'arithmetic_squared_L2_upper', 'old_coordinate_expected_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2', 'old_coordinate_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json', 'old_ideal_midpoint_field': 'ideal_midpoint_coordinate_squared_L2_upper', 'old_original_continuous_native_coordinate_field_NOT_new_result': 'continuous_to_original_native_coordinate_squared_L2_upper', 'ordinary4300_profile_record_token_census': [{'expected_SHA256': 'dfbfd35ec2de6922af4f86df34817b91aece77554f30428396c9040cd1471223', 'integer_tokens': 723, 'maximum_integer_token_digits': 1139, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/primary_log_endpoint_ledger.json'}, {'expected_SHA256': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60', 'integer_tokens': 25, 'maximum_integer_token_digits': 566, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json'}, {'expected_SHA256': 'd4240bd936acfbf7fff2b62750233ef7e1a7ed9f53a720a0d7e2ba362e7dcdd2', 'integer_tokens': 18, 'maximum_integer_token_digits': 775, 'numeric_values_used_for_new_math': False, 'path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_coordinate_squared_L2_bound.json'}], 'original_component_expected_SHA256': 'e8524a1e565f67b74dd91d9b6c7daf8d7be1ec585841d22f38c17f2e8752fb60', 'original_component_path': 'results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001/primary_native_arithmetic_components.json', 'original_ln2_fixed_terms_history_only': 256, 'original_ln2_ledger_expected_SHA256': 'dfbfd35ec2de6922af4f86df34817b91aece77554f30428396c9040cd1471223', 'original_ln2_ledger_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/primary_log_endpoint_ledger.json', 'original_ln2_window_pointer': ['endpoints', 2, 'window_exact'], 'positive_enclosure_mathematical_authority': 'Original certified ln2 windows plus original native source input ordering; new numerical guard not run', 'profile_is_role_label_not_invented_coordinate_record_field': True, 'upper_pointer': ['exact_component_allowances', 'ln2_upper'], 'values_computed_or_substituted_now': False}}, 'owner_scope_not_native12_new_success_or_stock18_19': True, 'physical_JSON_write_block_bytes': 65536, 'physical_certificate': False, 'prices_or_paths_sampled': False, 'quantum_advantage': False, 'radial_and_ideal_midpoint_squared_L2_only': True, 'runtime_authority_commitment': '83082c3b47c0145e6f593c40a19a3d09b06c5e8f13cd2f78fd0d77bddeb89140', 'runtime_invocation': ['-I', '-S', '-B', 'C:\\Users\\prith\\quantum_option_pricing\\research\\limitation_program_20261001\\experiment_e11_radial_cell_coupling_v1.py', '--ready-sha256', '<EXACT_EXTERNALLY_PINNED_CURRENT_ROOT_READY_SHA256>'], 'source_emission': False}
ACTIVE_OWNERS = ['E11_native_coordinate_squared_L2_run001', 'E11_scalar_midpoint_L2_numerical_run002']
ARCHIVE_CITATIONS = ['A01_run014', 'A02_quantile_financial_audit_run001', 'A02_quantile_law_audit_run001', 'E10_continuous_moment_only_run002']
PLANNED_FILES = ['executed_controller.py', 'executed_preflight.md', 'executed_policy.json', 'executed_ROOT_READY.json', 'reviewed_symbolic_method.json', 'reviewed_symbolic_method.md', 'reviewed_symbolic_peer.json', 'reviewed_ROOT_symbolic_review.json', 'reviewed_finite_method.json', 'reviewed_finite_method.md', 'reviewed_finite_peer.json', 'reviewed_ROOT_finite_review.json', 'run_started.json', 'interpreter.json', 'loaded_module_origins.json', 'original2_and_transitive12_scope.json', 'protocol.json', 'source_and_own_profile_adapters.json', 'five_radial_proof_controls.json', 'primary_radial_and_ideal_midpoint_bound.json', 'independent_radial_and_ideal_midpoint_bound.json', 'primary_same_profile_saved_comparison.json', 'independent_same_profile_saved_comparison.json', 'fresh_full_input_union_before_radial.json', 'fresh_full_input_union_after_radial.json', 'qualification_and_remaining_gaps.json', 'summary.json', 'completion_outcome.json', 'manifest.json']
REQUIRED_COMPONENTS = ['original_log_table_literal_and_native_Horner_floors', 'original_fixed_ln2_literal_and_all33_exponents', 'original_unclipped_minus2_nooverflow_and_unsigned46bit_isqrt_domain', 'original_sqrt_floor', 'all512_original_cosine_literals_and_native_Horner_floors', 'original_signed144product_stored72_and_product_floor']
SCIENTIFIC_SCOPE = {'source_law': 'original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'native_components': ['original_log_table_literal_and_native_Horner_floors', 'original_fixed_ln2_literal_and_all33_exponents', 'original_unclipped_minus2_nooverflow_and_unsigned46bit_isqrt_domain', 'original_sqrt_floor', 'all512_original_cosine_literals_and_native_Horner_floors', 'original_signed144product_stored72_and_product_floor'], 'quantity': 'squared_L2_Gaussian_coordinate', 'units': 'dimensionless_Gaussian_coordinate_squared', 'digital_pair_independence': False}
CURRENT_REVIEW_PATHS = ['.context/E11_RADIAL_CELL_COUPLING_AUTHOR_STATIC_QA_run001.json', '.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_STATIC_PEER_run001.json', '.context/E11_RADIAL_CELL_COUPLING_ROOT_STATIC_REVIEW_run001.json']
AUTHOR_QA_KEY = '.context/E11_RADIAL_CELL_COUPLING_AUTHOR_STATIC_QA_run001.json'
RADICAND_REVIEW_PINS = {'.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_ROOT_SYMBOLIC_REVIEW_run001.json': '4b841bd78a7827cf3b09ea5ec32da63a9c419ceb461f193e317ed9d1c213b06a', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_INDEPENDENT_STATIC_METHOD_PEER_run001.json': '7a6ec840faa1c1760ed80617f92c3faa66af1698600141bbf339fc208d69efac'}
COMPLETED_E11_READY_KEY = '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run002.json'
COMPLETED_E11_READY_SHA = '9a9d00407a8a6f763e9142d95d97e06dcadde3f2d0a73dfa9fcf167ced6f2c65'
COMPLETED_E11_CACHE_PARTITION = {'existing_expected_SHA256': {}, 'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc']}
GAP_KEY = '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_PROSPECTUS_run001.json'
GAP_MD_KEY = '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_PROSPECTUS_run001.md'
PREPARATION_KEY = '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_PREPARATION_run001.json'
PREPARATION_MD_KEY = '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_PREPARATION_run001.md'
PREPARATION_QA_KEY = '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_METADATA_QA_run001.json'
METHOD_PEER_KEY = '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_INDEPENDENT_METHOD_REVIEW_next_run001.json'
METHOD_ROOT_KEY = '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_ROOT_PROSPECTIVE_METHOD_REVIEW_run001.json'
E11_ROOT003_KEY = '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ACTUAL_RESULT_ROOT_VERIFICATION_run003.json'
E11_CHECKER003_PEER_KEY = '.context/E11_SCALAR_MIDPOINT_L2_ROOT_CHECKER003_INDEPENDENT_STATIC_DELTA_SUPPLEMENT_next_run001.json'
E11_MANIFEST_KEY = 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/manifest.json'
E11_MANIFEST_SHA = '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170'
SOURCE_BINDING_KEY = 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/native_source_binding.json'
SOURCE_BINDING_SHA = 'f6f10f434d1408fae49419ae1503f3bda2588eb47b9179ea292eb25949846a41'
NOOVERFLOW_KEY = 'results/limitation_program_20261001/C06_pair_audit_run001/all_Q32_native_nooverflow_audit.json'
NOOVERFLOW_SHA = '01e146b99fd6578331d50c9622ed1e70474941f706b9c66ce9abc8aa32a66cd7'
UPSTREAM_COORDINATE_KEY = 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/exact_real_analytic_proof_and_scope.json'
UPSTREAM_COORDINATE_SHA = '229b26f1c68d6ba9e6bdb917c31fef3ed096a5861103b6029d9fe8539d5959ac'
ROOT_DESCRIPTOR_SHA = '7d5b9840c1ddd5e6c12bb02cfde591a6be8bdeb18b1de75b93f527d3fde7d5d2'
ORIGINAL_CASES = [('B4x12', 30, 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json', 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'), ('B8x52', 234, 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/target.json', '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b')]
FAILED_E11_V1_HISTORY = {'ROOT_READY_SHA256': '855f25478139081cccaa804fc5a889fe4dcbdeeffed39e3d1f234ac365a3c6c9', 'ROOT_READY_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run001.json', 'ROOT_freeze_SHA256': 'c50342018999b1338a9ecc8ab5e6128a110b8d1076c5ce3021a6dac93e60dea6', 'ROOT_freeze_path': '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_FAILED_UNSEALED_ROOT_FREEZE_run001.json', 'author_method_SHA256': {'E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b', 'e11_scalar_midpoint_l2_numerical_preflight_v1.json': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27', 'experiment_e11_scalar_midpoint_l2_v1.py': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6'}, 'cache_partition': {'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v1.cpython-312.pyc'], 'existing_expected_SHA256': {}}, 'complete_failed_owned_inventory': {'FAILED_UNSEALED.json': {'SHA256': '06220039aa4d77b9fd8ad352a17240ffa874a7a36fff96188ee592e816139f43', 'bytes': 160}, 'all30_primary_and_independent_bin_records.json': {'SHA256': '7a90fc82caedf10db30e64236bf3639c48dd330b0bd202464ec249ac3f244bc8', 'bytes': 1029646}, 'all_bin_sum_and_telescoping_comparisons.json': {'SHA256': 'd2a07815a797522bdf45e020054d1c2948f2017caffeaa3b6c30133b05571a77', 'bytes': 121843}, 'complete_historical_owner_maps_and_inventories.json': {'SHA256': '38082221aefea36cf230fde4a5302734131f01452aa3e8db5c60133584cdebce', 'bytes': 1140113}, 'exact_real_analytic_proof_and_scope.json': {'SHA256': '229b26f1c68d6ba9e6bdb917c31fef3ed096a5861103b6029d9fe8539d5959ac', 'bytes': 3370}, 'executed_E11_SCALAR_MIDPOINT_L2_NUMERICAL_PREFLIGHT_V1.md': {'SHA256': '50c9f302f739f7e85d0c9f2ce5dd8e59636aa88122622677d66594b1df53f11b', 'bytes': 15449}, 'executed_E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run001.json': {'SHA256': '855f25478139081cccaa804fc5a889fe4dcbdeeffed39e3d1f234ac365a3c6c9', 'bytes': 569265}, 'executed_e11_scalar_midpoint_l2_numerical_preflight_v1.json': {'SHA256': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27', 'bytes': 567832}, 'executed_experiment_e11_scalar_midpoint_l2_v1.py': {'SHA256': 'a5acd62fd400c66b45b2946a20d366ff844ba67ea3d2fb7b205bb2cf828ddea6', 'bytes': 1654285}, 'failure.json': {'SHA256': 'a8547fb69b52d4e6158fcbafc84c87cca21986f156215cd94a22421625f44099', 'bytes': 1880}, 'fixed_canonical_argument_corpus.json': {'SHA256': '98c8d4d3494d7e03f4a1e21407d5ebd408ffd7573887fd91daead5fc8ea91a64', 'bytes': 13441}, 'fresh_input_union_before_scalar_numerics.json': {'SHA256': '6c72160c0ec959d64505ea9e094f81a637e15389816b0f6d18047dd835e83016', 'bytes': 8522}, 'independent_log_endpoint_ledger.json': {'SHA256': '6269a7bb56b776dd782ad4e417162a54f66314899497d8476cd585db058b02f6', 'bytes': 500884}, 'independent_production_squared_L2_allowance.json': {'SHA256': 'e6058f8f4ac815c3a908f9fbf8d99b69dd126cb7febd4cf211ab2812aa774cc8', 'bytes': 5442}, 'primary_log_endpoint_ledger.json': {'SHA256': 'dfbfd35ec2de6922af4f86df34817b91aece77554f30428396c9040cd1471223', 'bytes': 312396}, 'primary_production_squared_L2_allowance.json': {'SHA256': 'afa1c0313c1dc63ea0a3a52a0442c5897b57660a2d069a773254eb714fdc0af1', 'bytes': 4316}, 'protocol.json': {'SHA256': 'ddb66b7512edc0405dafc21a141d65f9c6f64f62d35f986d5ee64b2c6e507f27', 'bytes': 567832}, 'run_started.json': {'SHA256': '522093ef710d65913cdf1bf38f967c57c583f04af4125b7e2f8b0ae41992d40e', 'bytes': 903}, 'three_precise_negative_diagnostic_controls.json': {'SHA256': '0885318fc20876378c982a9b6af4a3d53b30bebeb216611aa4198a4b45a2f654', 'bytes': 5237}}, 'failed_not_scientific_certificate_or_new_owner': True, 'manifest_and_summary_and_second_union_absent': ['manifest.json', 'summary.json', 'fresh_input_union_after_scalar_numerics.json'], 'output': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run001', 'static_review_expected_SHA256': {'.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_AUTHOR_STATIC_QA_run001.json': '695cadc7fb64708bdd43bda53221299ff7c07c34474e866e6c8232b3d8623f55', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_INDEPENDENT_STATIC_PEER_next_run001.json': 'eb3e0c49cdcb19f2c4d5cf8f8a927caa6078c5dc92c344534091e8435a3bf4de', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_STATIC_REVIEW_run001.json': 'ca768374525412a7ffe3ee82e358ade56d98613d0599eb217b58dd65d52ad2d1'}}
SERIALIZATION_RUNTIME = {'absent_three_variant_cache_paths': ['C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.pyc', 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-1.pyc', 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\__pycache__\\_pylong.cpython-312.opt-2.pyc'], 'existing_cache_expected_SHA256': {}, 'import_before_initial_runtime_and_loaded_origin_admission': True, 'module': '_pylong', 'postadmission_origin_or_cache_discovery_authorized': False, 'scientific_arithmetic_or_representation_policy_change': False, 'source_SHA256': 'bcae0d4cc2d4d3fd9b40bb06b512eb8dd785f755edd1f9038613d4460ca4c6c1', 'source_path': 'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\_pylong.py'}
FINITE_METHOD = '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json'
SYMBOLIC_METHOD = '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json'
AUTHORGRANT = '.context/E11_RADIAL_CELL_COUPLING_ROOT_CONTROLLER_AUTHORING_ACCEPTANCE_run001.json'
FINITE_PINS = {'.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json': '65215242e73564d38c69afa0d62e9a1693d3bac30182f5f079b663d64d5b8042', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json': '4d58ff0a6aa1a0622000682879eec8c9d806206e230ee90d5679cd8845b954e7', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json': 'be76c6299d743ba6b82dce19615c7ebb709f7f3f5bed1e06164b615af9d5989f', '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.md': '076a3c8ac42884b550a29cb0114dfb23618e48ab3e54b9ef62830849d8a2f45a'}
SYMBOLIC_PINS = {'.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json': 'e7b4a988f5e50de4064f96d809177a22e0cb4a55388d42ba139697ac525307e3', '.context/E11_RADIAL_CELL_COUPLING_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json': 'c552f2a95ac74a0815e6251737a5c68796260c981e83529366c13743d176d192', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json': '6ff35a0771cacaf0685d9943d27f86a6303c2ec1fb78ac8143edc1e9e735b92e', '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.md': 'e1e9a5a9107483d1cb7c80f6f5e23098117bbaee7843f326ff97ead82182db25'}
COPY_ROUTES = {'executed_ROOT_READY.json': '.context/E11_RADIAL_CELL_COUPLING_ROOT_READY_run001.json', 'executed_controller.py': 'research/limitation_program_20261001/experiment_e11_radial_cell_coupling_v1.py', 'executed_policy.json': 'research/limitation_program_20261001/e11_radial_cell_coupling_preflight_v1.json', 'executed_preflight.md': 'research/limitation_program_20261001/E11_RADIAL_CELL_COUPLING_PREFLIGHT_V1.md', 'reviewed_ROOT_finite_review.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_ROOT_METHOD_REVIEW_run001.json', 'reviewed_ROOT_symbolic_review.json': '.context/E11_RADIAL_CELL_COUPLING_ROOT_SYMBOLIC_METHOD_REVIEW_run001.json', 'reviewed_finite_method.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.json', 'reviewed_finite_method.md': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_METHOD_run001.md', 'reviewed_finite_peer.json': '.context/E11_RADIAL_CELL_COUPLING_FINITE_ADMISSION_INDEPENDENT_METHOD_PEER_run001.json', 'reviewed_symbolic_method.json': '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.json', 'reviewed_symbolic_method.md': '.context/E11_RADIAL_CELL_COUPLING_SYMBOLIC_METHOD_PROPOSAL_run001.md', 'reviewed_symbolic_peer.json': '.context/E11_RADIAL_CELL_COUPLING_INDEPENDENT_SYMBOLIC_METHOD_PEER_run001.json'}
POLICY_KEYS = ['G2_transfer', 'ROOT_READY', 'ROOT_READY_schema', 'accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256', 'accepted_symbolic_METHOD_MD_independent_ROOT_expected_SHA256', 'active_current_owner_names', 'adoption', 'author_SHA256', 'cost_comparison', 'current_authoring_acceptance_SHA256', 'current_authoring_acceptance_path', 'current_control_specs', 'current_definition_AST_SHA256', 'current_positive_scope', 'current_static_review_paths', 'default_decimal4300_no_setter', 'digital_pair_independence', 'estimator_schedule_emitted', 'exact12_copy_routes', 'exact29_inclusive_owned_ledger', 'expected_only_observations_output_excluded', 'finite_protocol', 'fits_or_pilots', 'fixture_credit', 'full_E11_completed', 'full_original2_expected_registry_commitment', 'full_price_certificate', 'gate_emission', 'item', 'local_only', 'method_SHA256', 'native12_transitive_citation_authority', 'native_arrays_generated_or_replayed', 'native_financial_path_or_policy_L2_verified', 'native_source_clipping_inserted', 'new_global_fixture_credit', 'new_native_coordinate_certificate', 'new_transcendental_series', 'no_numeric_results_before_own_ROOT_READY', 'old_numerical_helpers_or_evaluators_called', 'original_caps', 'original_history3_cache_roles', 'original_two_snapshot_authority', 'output', 'own_profile_input_roles', 'owner_scope_not_native12_new_success_or_stock18_19', 'physical_JSON_write_block_bytes', 'physical_certificate', 'prices_or_paths_sampled', 'quantum_advantage', 'radial_and_ideal_midpoint_squared_L2_only', 'radial_ideal_midpoint_rational_assembly_authorized', 'runtime_authority_commitment', 'runtime_invocation', 'schema', 'source_emission']
READY_KEYS = ['G2_transfer', 'absent_new_code_cache_paths', 'accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256', 'accepted_symbolic_METHOD_MD_independent_ROOT_expected_SHA256', 'active_current_owner_names', 'adoption', 'author_method_SHA256', 'cost_comparison', 'current_authoring_acceptance_SHA256', 'current_authoring_acceptance_path', 'current_control_specs', 'current_positive_scope', 'current_static_review_paths', 'default_decimal4300_no_setter', 'digital_pair_independence', 'estimator_schedule_emitted', 'exact12_copy_routes', 'exact29_inclusive_owned_ledger', 'existing_new_code_cache_SHA256', 'expected_only_observations_output_excluded', 'finite_protocol', 'fits_or_pilots', 'fixture_credit', 'full_E11_completed', 'full_original2_expected_registry_commitment', 'full_price_certificate', 'gate_emission', 'item', 'local_only', 'native12_transitive_citation_authority', 'native_arrays_generated_or_replayed', 'native_financial_path_or_policy_L2_verified', 'native_source_clipping_inserted', 'new_global_fixture_credit', 'new_native_coordinate_certificate', 'new_transcendental_series', 'no_numeric_results_before_own_ROOT_READY', 'old_numerical_helpers_or_evaluators_called', 'original_caps', 'original_history3_cache_roles', 'original_two_snapshot_authority', 'output', 'own_profile_input_roles', 'owner_scope_not_native12_new_success_or_stock18_19', 'physical_JSON_write_block_bytes', 'physical_certificate', 'prices_or_paths_sampled', 'quantum_advantage', 'radial_and_ideal_midpoint_squared_L2_only', 'radial_ideal_midpoint_rational_assembly_authorized', 'ready', 'root_and_independent_static_reviews_passed', 'runtime_authority_commitment', 'runtime_invocation', 'schema', 'source_emission', 'static_review_expected_SHA256']
POLICY_SCHEMA = 'e11-radial-cell-coupling-preflight-v1'
READY_SCHEMA = 'root-e11-radial-cell-coupling-READY-v1'
NATIVE_CFG_SHA = 'aaeeb031a76b70ae1ac53b6557056f554273db4b313678c36c7ccd2c483e7e37'
NATIVE_OWNER = 'E11_native_coordinate_squared_L2_run001'
ORIGINAL2_SHA = 'bd1e8abf0da43232b90971b2584bd0b6e537d806444892c6086e6ae22ba86874'
PRIMARY_RECIPE = {'coordinate_radial_contribution': '2*raw_radial', 'ideal_midpoint_coordinate': '2*raw_radial+4*(22/7)^2*delta^2', 'lower_terms': 't_k=delta/(own_ln2_lower*2^(k+5)*(31-k)), k=0..30', 'order': 'k ascending0..30, left associated stage assembly; no independent inputs or function calls', 'own_input_role': 'primary90 only', 'raw_radial': '((first+lower)+upper)+last', 'stages': ['first=delta/(32*own_ln2_lower)', 'lower=left_sum(t_0,...,t_30)', 'upper=(31/4)*delta^2*own_ln2_upper', 'last=delta^2/(2*(1-delta))']}
INDEPENDENT_RECIPE = {'angular_identity_is_old_source_constant': '4*(22/7)^2=1936/49, the original independent angular coefficient', 'coordinate_radial_contribution': '2*raw_radial', 'finite_sum': 'S=sum_{j=1}^{31} 1/(j*2^(36-j))', 'ideal_midpoint_coordinate': '(delta/own_ln2_lower)*(1/16+2*S)+delta^2*((31/2)*own_ln2_upper+1/(1-delta)+1936/49)', 'index_identity_not_evaluated': 'j=31-k bijects k0..30 to j31..1; 36-j=k+5', 'order': 'j ascending1..31 reverses dyadic sum order; factor reciprocals and expanded ideal assembly; no primary evaluator', 'own_input_role': 'independent130 only', 'raw_radial': '(delta/own_ln2_lower)*(1/32+S)+delta^2*((31/4)*own_ln2_upper+1/(2-2*delta))'}
CURRENT_POSITIVE_SCOPE = {'M': 4294967296, 'coordinate_radial_factor': 2, 'delta_pair_role': [1, 4294967296], 'downstream_financial_claim': False, 'dyadic_indices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'first_cell_paid': True, 'last_cell_paid': True, 'new_native_coordinate_claim': False, 'positive_ln2_enclosure_provenance': True, 'raw_radial_measure_role': 'unmultiplied_radial_squared_integral', 'reciprocal_endpoint_role': 'own_ledger_window_exact_lower', 'scalar_inverse_lipschitz_used': False, 'scope': 'E11_RADIAL_AND_IDEAL_MIDPOINT_ONLY', 'units': 'dimensionless_Gaussian_coordinate_squared', 'whole_cell_alignment': True}
CURRENT_CONTROL_SPECS = [{'category': 'both_endpoint_cells', 'dedicated_tag': 'RADIAL_ENDPOINT_CELLS', 'fixed_bad_metadata_variants': [{'first_cell_paid': False}, {'last_cell_paid': False}]}, {'category': 'complete_aligned_dyadic_partition', 'dedicated_tag': 'RADIAL_WHOLE_CELL_PARTITION', 'fixed_bad_metadata_variants': [{'dyadic_indices': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}, {'dyadic_indices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}, {'whole_cell_alignment': False}]}, {'category': 'own_reciprocal_endpoint_provenance', 'dedicated_tag': 'RADIAL_LN2_ENDPOINT_ROLE', 'fixed_bad_metadata_variants': [{'reciprocal_endpoint_role': 'own_ledger_window_exact_upper'}, {'positive_ln2_enclosure_provenance': False}]}, {'category': 'radial_factor2_role', 'dedicated_tag': 'RADIAL_FACTOR2_ROLE', 'fixed_bad_metadata_variants': [{'coordinate_radial_factor': 1}, {'raw_radial_measure_role': 'old_factor2_midpoint_radial_stage'}]}, {'category': 'units_and_excluded_scopes', 'dedicated_tag': 'RADIAL_UNITS_SCOPE', 'fixed_bad_metadata_variants': [{'units': 'dollars_squared'}, {'new_native_coordinate_claim': True}, {'scalar_inverse_lipschitz_used': True}, {'downstream_financial_claim': True}]}]
VALIDATOR_PREDICATES = {'RADIAL_ENDPOINT_CELLS': {'positive_expected_values': {'first_cell_paid': True, 'last_cell_paid': True}, 'predicate': 'All named relevant positive-scope fields equal their exact positive values, with exact bool/int/string/list element types; no bool accepted as int', 'variant_keys': ['first_cell_paid', 'last_cell_paid']}, 'RADIAL_FACTOR2_ROLE': {'positive_expected_values': {'coordinate_radial_factor': 2, 'raw_radial_measure_role': 'unmultiplied_radial_squared_integral'}, 'predicate': 'All named relevant positive-scope fields equal their exact positive values, with exact bool/int/string/list element types; no bool accepted as int', 'variant_keys': ['coordinate_radial_factor', 'raw_radial_measure_role']}, 'RADIAL_LN2_ENDPOINT_ROLE': {'positive_expected_values': {'positive_ln2_enclosure_provenance': True, 'reciprocal_endpoint_role': 'own_ledger_window_exact_lower'}, 'predicate': 'All named relevant positive-scope fields equal their exact positive values, with exact bool/int/string/list element types; no bool accepted as int', 'variant_keys': ['positive_ln2_enclosure_provenance', 'reciprocal_endpoint_role']}, 'RADIAL_UNITS_SCOPE': {'positive_expected_values': {'M': 4294967296, 'delta_pair_role': [1, 4294967296], 'downstream_financial_claim': False, 'new_native_coordinate_claim': False, 'scalar_inverse_lipschitz_used': False, 'scope': 'E11_RADIAL_AND_IDEAL_MIDPOINT_ONLY', 'units': 'dimensionless_Gaussian_coordinate_squared'}, 'predicate': 'All named relevant positive-scope fields equal their exact positive values, with exact bool/int/string/list element types; no bool accepted as int', 'variant_keys': ['downstream_financial_claim', 'new_native_coordinate_claim', 'scalar_inverse_lipschitz_used', 'units']}, 'RADIAL_WHOLE_CELL_PARTITION': {'positive_expected_values': {'dyadic_indices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'whole_cell_alignment': True}, 'predicate': 'All named relevant positive-scope fields equal their exact positive values, with exact bool/int/string/list element types; no bool accepted as int', 'variant_keys': ['dyadic_indices', 'whole_cell_alignment']}}
RADIAL_FLAG_KEYS = ['G2_transfer', 'adoption', 'cost_comparison', 'default_decimal4300_no_setter', 'digital_pair_independence', 'estimator_schedule_emitted', 'expected_only_observations_output_excluded', 'fits_or_pilots', 'fixture_credit', 'full_E11_completed', 'full_price_certificate', 'gate_emission', 'local_only', 'native_arrays_generated_or_replayed', 'native_financial_path_or_policy_L2_verified', 'native_source_clipping_inserted', 'new_global_fixture_credit', 'new_native_coordinate_certificate', 'new_transcendental_series', 'no_numeric_results_before_own_ROOT_READY', 'old_numerical_helpers_or_evaluators_called', 'owner_scope_not_native12_new_success_or_stock18_19', 'physical_certificate', 'prices_or_paths_sampled', 'quantum_advantage', 'radial_and_ideal_midpoint_squared_L2_only', 'source_emission']
_OWNS_OUTPUT = False
_OWNED_OUTPUT_ID = None
_CURRENT_AST_MAP = {}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def process_started():
    require(os.name == 'nt' and ctypes.sizeof(ctypes.c_void_p) == 8, 'Pinned Win64')
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(kernel.GetProcessTimes(kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]), 'Actual process creation clock')
    ticks = stamps[0].dwHighDateTime << 32 | stamps[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, 'Actual UTC creation precedes observation')
    return time.monotonic() - age_ns / 1000000000

def budget(admission=False):
    require(time.process_time() < (ADMISSION if admission else CPU), 'Process CPU guard')
    require(time.monotonic() - _STARTED < WALL, 'Creation-derived wall guard')

def runtime_scopes():
    global _BASE_SCOPE, _EXCLUDED_SCOPE
    budget()
    lexical = Path(os.path.abspath(sys.base_prefix))
    actual = lexical.resolve(strict=True)
    require(actual == lexical, 'Actual base prefix has no alias')
    excluded = lexical / 'Lib/site-packages'
    physical_excluded = excluded.resolve(strict=False)
    scopes = (actual, (excluded, physical_excluded))
    if _BASE_SCOPE is not None:
        require(scopes == (_BASE_SCOPE, _EXCLUDED_SCOPE), 'Actual runtime scopes unchanged')
    _BASE_SCOPE, _EXCLUDED_SCOPE = scopes
    budget()

def canonical(path, fresh=False):
    budget()
    path = Path(path)
    require(not path.drive or path.is_absolute(), 'No ambiguous drive-relative input')
    lexical = Path(os.path.abspath(str(path)))
    require(not any((lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)), 'Excluded base packages lexical path')
    key = str(lexical)
    if not fresh and key in _PATH_CACHE:
        cached, identity = _PATH_CACHE[key]
        if fingerprint(lexical) == identity:
            budget()
            return cached
    actual = lexical.resolve(strict=True)
    require(not any((actual.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)), 'Excluded base package alias')
    require(actual == lexical, 'No lexical-to-physical input alias')
    require(key not in _PATH_CACHE or _PATH_CACHE[key][0] == actual, 'Previously confined lexical input did not redirect')
    _PATH_CACHE[key] = (actual, fingerprint(lexical))
    budget()
    return actual

def fingerprint(path):
    stat = path.stat()
    return tuple((getattr(stat, name, None) for name in ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_mode', 'st_file_attributes', 'st_reparse_tag')))

def digest(path, fresh=False, already_resolved=False):
    global _HASH_WORK
    budget()
    path = path if already_resolved else canonical(path, fresh=fresh)
    require(path.is_file(), 'Actual regular SHA input')
    before, total, state = (fingerprint(path), 0, hashlib.sha256())
    if not fresh and path in _HASH_CACHE and (_HASH_CACHE[path][0] == before):
        budget()
        return _HASH_CACHE[path][1]
    with path.open('rb') as stream:
        while (chunk := stream.read(1024 * 1024)):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK, 'Fixed24GiB hashing-work cap')
            require(total <= before[2], 'Input grew while hashing')
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, 'Stable actual byte hash')
    result = state.hexdigest()
    require(path not in _OBSERVED or _OBSERVED[path] == result, 'Previously observed bytes unchanged')
    _OBSERVED.setdefault(path, result)
    _HASH_CACHE[path] = (before, result)
    budget()
    return result

def add(path, expected):
    global _REFERENCES
    budget()
    _REFERENCES += 1
    require(_REFERENCES <= MAX_REFERENCES, 'Fixed100k map-reference cap')
    require(type(expected) is str and len(expected) == 64 and all((char in '0123456789abcdef' for char in expected)), 'Exact expected SHA')
    actual = canonical(path)
    require(actual.is_file(), 'Regular preserved input')
    if actual.is_relative_to(ROOT):
        key, mapping = (actual.relative_to(ROOT).as_posix(), _FROZEN)
    else:
        require(actual.is_relative_to(_BASE_SCOPE), 'Actual external base runtime')
        key, mapping = (str(actual), _EXTERNAL)
    require(key not in mapping or mapping[key] == expected, 'Canonical equal-SHA expectations')
    mapping[key] = expected
    return actual

def read(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= 128 * 1024 ** 2, 'Bounded regular JSON input')
    chunks, total, state = ([], 0, hashlib.sha256())
    with path.open('rb') as stream:
        while (chunk := stream.read(1024 * 1024)):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK and total <= before[2], 'Bounded JSON reads')
            chunks.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, 'Stable JSON bytes')
    expected = _FROZEN.get(path.relative_to(ROOT).as_posix()) if path.is_relative_to(ROOT) else _EXTERNAL.get(str(path))
    observed = state.hexdigest()
    require(expected is not None and observed == expected, 'JSON belongs to exact admitted SHA')
    require(path not in _OBSERVED or _OBSERVED[path] == observed, 'Stable observed JSON SHA')
    _OBSERVED[path] = observed
    _HASH_CACHE[path] = (before, observed)
    budget()
    result = json.loads(b''.join(chunks))
    guard_serialization_integers(result)
    budget()
    return result

def inventory(directory):
    found, total = (set(), 0)
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(canonical(candidate).is_relative_to(directory), 'No owned directory escape')
            require(not candidate.is_symlink(), 'No owned directory link')
        for name in names:
            actual = canonical(Path(root) / name)
            require(actual.is_relative_to(directory) and actual not in found, 'Unique owned path')
            require(actual.is_file(), 'Regular actual owned entry')
            found.add(actual)
            total += actual.stat().st_size
            require(len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, 'Finite owned inventory')
    return found

def guard_serialization_integers(value):
    """A bounded representation guard; it neither rounds nor changes a value."""
    budget()
    require(sys.get_int_max_str_digits() == INTEGER_DECIMAL_DIGITS, 'Fixed finite decimal policy unchanged')
    pending, count, maximum_bits = ([value], 0, 0)
    while pending:
        budget()
        item = pending.pop()
        count += 1
        require(count <= MAX_SERIALIZATION_VALUES, 'Evidence-value traversal bounded by128MiB')
        if type(item) is int:
            bits = item.bit_length()
            require(bits <= INTEGER_SERIALIZATION_BITS, 'Each serialized integer at most65536 bits')
            maximum_bits = max(maximum_bits, bits)
        elif isinstance(item, dict):
            for key, member in item.items():
                budget()
                pending.append(key)
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, 'Bounded serializer frontier')
        elif isinstance(item, (list, tuple)):
            for member in item:
                budget()
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, 'Bounded serializer frontier')
    budget()
    return {'visited_values': count, 'maximum_integer_bits': maximum_bits}

def exact_key(key):
    require(type(key) is str and key and (not Path(key).is_absolute()) and (not Path(key).drive) and ('\\' not in key) and all((part not in ('', '.', '..') for part in key.split('/'))) and (Path(key).as_posix() == key), 'Exact original ROOT-relative spelling')
    return ROOT / key

def object_sha(value):
    budget()
    data = json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    require(len(data) <= MAX_OWN_BYTES, 'Bounded literal metadata object')
    return hashlib.sha256(data).hexdigest()

def invocation_check():
    require(sys.version_info[:3] == (3, 12, 4) and sys.flags.isolated == 1 and (sys.flags.no_site == 1) and sys.dont_write_bytecode and (sys.flags.optimize == 0) and ('PYTHONOPTIMIZE' not in os.environ), 'Pinned Python3.12.4 isolated -I -S -B direct-script invocation')
    require(canonical(Path.cwd(), fresh=True) == ROOT, 'Exact original workspace cwd')
    require(canonical(sys.executable, fresh=True) == LAUNCHER and canonical(sys.base_prefix, fresh=True) == BASE and (canonical(sys.prefix, fresh=True) == BASE), 'No-site exact launcher/base/prefix')
    require(sys.path == [str(BASE / 'python312.zip'), str(BASE / 'DLLs'), str(BASE / 'Lib'), str(BASE)], 'Exact isolated stdlib search path')
    absent_zip = BASE / 'python312.zip'
    require(not absent_zip.exists() and (not absent_zip.is_symlink()), 'Exact absent standard zip')
    _ABSENT_RUNTIME.add(absent_zip)
    require(not any((name == 'site' or name.startswith('research.') for name in sys.modules)), 'No site or scientific module loaded')
    bind(LAUNCHER, LAUNCHER_SHA)
    bind(BASE / 'python.exe', BASE_SHA)

def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual, fresh=True) == expected, 'Full fresh original expected bytes')
    return actual

def standard_runtime_members():
    members = {LAUNCHER, BASE / 'python.exe'}
    for path in BASE.iterdir():
        budget()
        if path.is_file():
            members.add(canonical(path))
    for tree in (BASE / 'Lib', BASE / 'DLLs'):
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            parent = Path(root)
            require(canonical(parent, fresh=True) == parent, 'Exact current runtime directory')
            dirs[:] = [name for name in dirs if name.lower() != 'site-packages']
            for name in dirs:
                path = parent / name
                require(not path.is_symlink() and canonical(path, fresh=True) == path, 'No runtime alias silently skipped')
            for name in names:
                members.add(canonical(parent / name))
                require(len(members) <= MAX_RUNTIME_FILES, 'Current isolated runtime count cap')
    return members

def code_cache_policy(ready):
    paths = {exact_key('research/limitation_program_20261001/__pycache__/' + AUTHOR.stem + '.cpython-312' + suffix + '.pyc') for suffix in ('', '.opt-1', '.opt-2')}
    expected = ready['existing_new_code_cache_SHA256']
    absent = ready['absent_new_code_cache_paths']
    present = {path for path in paths if path.exists()}
    require(type(expected) is dict and type(absent) is list and (len(absent) == len(set(absent))) and ({exact_key(key) for key in expected} == present) and ({exact_key(key) for key in absent} == paths - present), 'Exact externally declared normal/opt1/opt2 current author cache partition')
    for key, pin in expected.items():
        path = bind(exact_key(key), pin)
        _CODE_CACHE_EXPECTED[path] = pin
    for key in absent:
        path = exact_key(key)
        require(not path.exists() and (not path.is_symlink()), 'Exact declared absent author cache')
        _ABSENT_RUNTIME.add(path)

def historical_code_cache_partition(source, partition):
    paths = {exact_key('research/limitation_program_20261001/__pycache__/' + source.stem + '.cpython-312' + suffix + '.pyc') for suffix in ('', '.opt-1', '.opt-2')}
    expected, absent = (partition['existing_expected_SHA256'], partition['absent_paths'])
    present = {path for path in paths if path.exists()}
    require(type(expected) is dict and type(absent) is list and (len(absent) == len(set(absent))) and ({exact_key(key) for key in expected} == present) and ({exact_key(key) for key in absent} == paths - present), 'Original externally fixed historical three-variant cache partition')
    for key, pin in expected.items():
        path = bind(exact_key(key), pin)
        _CODE_CACHE_EXPECTED[path] = pin
    for key in absent:
        path = exact_key(key)
        require(not path.exists() and (not path.is_symlink()) and (path.resolve(strict=False) == path), 'Original absent cache has no physical alias')
        _ABSENT_RUNTIME.add(path)

def serialization_runtime_admission():
    contract = SERIALIZATION_RUNTIME
    source = Path(contract['source_path'])
    require(str(source) in _EXTERNAL and _EXTERNAL[str(source)] == contract['source_SHA256'], 'Serializer module has original admitted complete-runtime expected SHA')
    require(canonical(_pylong.__file__, fresh=True) == source and digest(source, fresh=True) == contract['source_SHA256'], 'Upfront standard serializer origin freshly equals original expected SHA')
    require(contract['existing_cache_expected_SHA256'] == {}, 'Externally declared serializer cache partition')
    for key in contract['absent_three_variant_cache_paths']:
        path = Path(key)
        require(not path.exists() and (not path.is_symlink()), 'Every externally declared serializer cache variant absent before admission')
        _ABSENT_RUNTIME.add(path)

def retain_failed_e11_v1():
    history = FAILED_E11_V1_HISTORY
    freeze = read(bind(ROOT / history['ROOT_freeze_path'], history['ROOT_freeze_SHA256']))
    original_ready = read(bind(ROOT / history['ROOT_READY_path'], history['ROOT_READY_SHA256']))
    require(freeze['certified_scalar_result'] is False and freeze['manifest_absent'] is True and (freeze['own_complete_inventory'] == history['complete_failed_owned_inventory']), 'Failed V1 is immutable opaque history, never a certificate')
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
        require(not path.exists() and (not path.is_symlink()), 'Failed packet never acquires a completion seal')
        _ABSENT_RUNTIME.add(path)

def strict_loaded_origins():
    forbidden = {'numpy', 'scipy', 'mpmath', 'sympy', 'numba', 'pytest', 'pandas', 'gmpy', 'gmpy2'}
    require(not any((name.split('.', 1)[0] in forbidden or name.startswith('research.') for name in sys.modules)), 'No numerical or old scientific module import')
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ('__file__', '__cached__'):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(not any((lexical.is_relative_to(s) or lexical.resolve(strict=False).is_relative_to(s) for s in _EXCLUDED_SCOPE)), 'Excluded origin remains rejected')
            if lexical.is_file():
                actual = canonical(lexical, fresh=True)
                key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                require(key in mapping and digest(actual, fresh=True) == mapping[key], 'Every present loaded source/cache already has original expected SHA')
            else:
                require(attribute == '__cached__' and (not lexical.exists()) and (not lexical.is_symlink()) and (lexical.resolve(strict=False) == lexical), 'Only an immediate exact absent hypothetical cache; never missing source')
                source = getattr(module, '__file__', None)
                require(source is not None and str(source).endswith('.py') and (Path(cache_from_source(str(source), optimization='')) == lexical), 'Missing cache belongs exactly to its known loaded Python source')
                require(lexical in _ABSENT_RUNTIME or lexical.is_relative_to(BASE / 'Lib'), 'No unknown author/cache route; absent stdlib cache is not promoted to dependency')

def known_runtime_admission(original_e11_manifest):
    """Retain original full expected stdlib pins before strict bootstrap origins."""
    global _STANDARD_RUNTIME_MEMBERS
    expected = original_e11_manifest['external_runtime_inputs']
    require(type(expected) is dict and len(expected) == 2842, 'Exact original E11 external runtime map')
    for key, pin in expected.items():
        require(Path(key).is_absolute(), 'Original external runtime spelling')
        bind(Path(key), pin)
    members = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = members
    required = {Path(key) for key in expected} | {LAUNCHER}
    require(members == required, 'Complete original isolated runtime membership, no observed expectations')
    size = 0
    for path in sorted(members):
        budget()
        size += path.stat().st_size
    require(len(members) <= MAX_RUNTIME_FILES and size <= MAX_RUNTIME_BYTES, 'Original finite stdlib runtime budgets')
    return {'files': len(members), 'bytes': size, 'original_full_expected_SHA_before_origins': True, 'isolated_no_site': True, 'numerical_packages_loaded': False}

def full_active_owner(name, snapshot, archive_routes):
    """Retain every original field, key and owner; bind explicit role union only."""
    manifest = read(bind(ROOT / snapshot['manifest_path'], snapshot['literal_expected_manifest_SHA256']))
    for field, row in snapshot['complete_original_declared_maps_with_field_presence'].items():
        require(row['original_field_present'] == (field in manifest) and row['complete_original_map'] == manifest.get(field), 'Original map field presence and bytes')
    legacy = snapshot['complete_original_legacy_bare_owned_file_map']
    require(legacy is None or (name == 'A10_coefficient_run001' and legacy == manifest), 'Original bare A10 layout, never fabricated files/frozen/runtime fields')
    directory = canonical((ROOT / snapshot['manifest_path']).parent)
    aliases = {(r['original_owner'], r['original_map'], r['original_key']): r for r in archive_routes}
    for field, row in snapshot['complete_original_declared_maps_with_field_presence'].items():
        if not row['original_field_present']:
            continue
        for key, pin in row['complete_original_map'].items():
            budget()
            alias = aliases.get((name, field, key))
            if alias is not None:
                require(alias['expected_sha256'] == pin and alias['expected_hash_waived'] is False and (alias['current_original_path_integrity_asserted'] is False), 'Scoped equal-SHA archive does not assert current original integrity')
                path = ROOT / alias['verified_archived_path']
            elif field == 'external_runtime_inputs':
                require(Path(key).is_absolute(), 'Original external map exact absolute key')
                path = Path(key)
            elif field == 'files' and snapshot['original_files_key_layout'] == 'RECEIPT_RELATIVE':
                path = directory / Path(key)
            else:
                path = ROOT / key
            bind(path, pin)
    if legacy is not None:
        for key, pin in legacy.items():
            budget()
            require(not Path(key).is_absolute() and '..' not in Path(key).parts, 'Exact original A10 receipt-relative backslash keys')
            bind(directory / Path(key), pin)
    members = set()
    for row in snapshot['complete_physical_receipt_inventory_expected_hashes_and_stat_only']:
        budget()
        path = bind(ROOT / row['path'], row['expected_SHA256'])
        require(path.is_relative_to(directory) and path.stat().st_size == row['bytes_metadata_only'], 'Complete physical original receipt member, including manifest')
        members.add(path)
    require(inventory(directory) == members, 'Complete original owned physical inventory')
    _OWN_INVENTORIES[directory] = members
    for row in snapshot['original_declared_external_owned_artifacts']:
        require(row['exists_metadata_only'] is True, 'Original external-owned document remains explicit')
        bind(ROOT / row['path'], row['expected_SHA256'])
    return {'manifest_expected_SHA256': snapshot['literal_expected_manifest_SHA256'], 'original_map_counts': snapshot['original_map_counts'], 'original_files_key_layout': snapshot['original_files_key_layout'], 'original_field_presence': {k: r['original_field_present'] for k, r in snapshot['complete_original_declared_maps_with_field_presence'].items()}, 'full_original_snapshot': snapshot, 'no_recursive_nested_owner_success_or_runtime_promotion': True}

def checked_ratio(pair):
    budget()
    require(type(pair) is list and len(pair) == 2 and all((type(v) is int for v in pair)) and (pair[1] > 0) and (max((abs(v).bit_length() for v in pair)) <= INTEGER_SERIALIZATION_BITS), 'Bounded exact saved rational pair, no floats or implicit parameter replacement')
    value = Fraction(pair[0], pair[1])
    return rational_guard(value)

def rational_guard(value):
    budget()
    require(type(value) is Fraction and max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_REDUCED_RATIONAL_BITS, 'Fixed reduced-rational cap')
    return value

def plus(a, b):
    budget()
    require(max(abs(a.numerator).bit_length() + b.denominator.bit_length(), abs(b.numerator).bit_length() + a.denominator.bit_length()) + 1 <= MAX_ANALYTIC_TEMP_BITS and a.denominator.bit_length() + b.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS, 'Finite numerator sum temporary cap before operation')
    return rational_guard(a + b)

def times(a, b):
    budget()
    require(abs(a.numerator).bit_length() + abs(b.numerator).bit_length() <= MAX_ANALYTIC_TEMP_BITS and a.denominator.bit_length() + b.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS, 'Finite product temporary caps before operation')
    return rational_guard(a * b)

def pair_literal(value):
    rational_guard(value)
    require(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= INTEGER_SERIALIZATION_BITS, 'Every saved exact rational within original serialization bit cap')
    return [value.numerator, value.denominator]

class E11RadialProofReject(ValueError):
    pass

def admit_current_metadata_and_startup(ready_sha):
    global _CURRENT_AST_MAP
    require('PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and ('int_max_str_digits' not in sys._xoptions) and (sys.get_int_max_str_digits() == 4300), 'No decimal policy override or transition')
    ready = bootstrap_json(READY, ready_sha)
    require(set(ready) == set(READY_KEYS) and ready['schema'] == READY_SCHEMA and (ready['ready'] is True) and (ready['root_and_independent_static_reviews_passed'] is True) and (ready['radial_ideal_midpoint_rational_assembly_authorized'] is True), 'Own separate radial READY')
    require(sys.orig_argv[1:] == COMMON_EXPECTATIONS['runtime_invocation'][:-1] + [ready_sha], 'Exact current absolute SOURCE and externally supplied READY token')
    authors = ready['author_method_SHA256']
    require(type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, 'Own exact trio')
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = bootstrap_json(PREFLIGHT, authors[PREFLIGHT.name])
    require(set(policy) == set(POLICY_KEYS) and policy['schema'] == POLICY_SCHEMA and (policy['author_SHA256'] == authors[AUTHOR.name]) and (policy['method_SHA256'] == authors[METHOD_DOC.name]) and (policy['ROOT_READY'] == READY.relative_to(ROOT).as_posix()) and (policy['ROOT_READY_schema'] == READY_SCHEMA) and (policy['radial_ideal_midpoint_rational_assembly_authorized'] is False), 'Dormant policy is not SCI grant')
    require(all((policy[key] == ready[key] == value for key, value in COMMON_EXPECTATIONS.items())), 'All forty-nine fixed shared fields, only prior five authority fills')
    _CURRENT_AST_MAP = policy['current_definition_AST_SHA256']
    current_review_admission(ready, authors)
    code_cache_policy(ready)
    bind(ROOT / '.context/frontier_t0_env/pyvenv.cfg', NATIVE_CFG_SHA)
    invocation_check()
    source_code_guard()
    return (ready, policy)

def bootstrap_json(path, expected):
    global _HASH_WORK
    require(sys.get_int_max_str_digits() == 4300, 'Default4300, no setter')
    actual = bind(path, expected)
    before = fingerprint(actual)
    require(0 <= before[2] <= MAX_OWN_BYTES, 'Pre-read bootstrap bound')
    with actual.open('rb') as stream:
        raw = stream.read(before[2] + 1)
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2] and (fingerprint(actual) == before) and (hashlib.sha256(raw).hexdigest() == expected), 'Bounded stable external bootstrap bytes')
    value = json.loads(raw)
    guard_serialization_integers(value)
    return value

def complete_manifest(value, owned, nonmanifest_bytes):
    owned_output_guard()
    require(set(owned) == set(PLANNED_FILES) - {'manifest.json'} and len(owned) == 28, 'Exactly twenty-eight preseal files')
    require(not any(((OUTPUT / n).exists() for n in ('failure.json', 'FAILED_UNSEALED.json'))), 'No failure marker before seal')
    value['manifest_inclusive_owned_file_count'] = 29
    value['owned_nonmanifest_bytes'] = nonmanifest_bytes
    value['manifest_inclusive_retention_checked_before_sealing'] = True
    guard_serialization_integers(value)
    size = 1
    for part in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(value):
        budget()
        size += len(part.encode('utf-8'))
        require(nonmanifest_bytes + size <= MAX_OWN_BYTES, 'Prospective manifest byte cap')
    save('manifest.json', value)
    actual = inventory(OUTPUT)
    require({p.name for p in actual} == set(PLANNED_FILES) and len(actual) == 29 and ((OUTPUT / 'manifest.json').stat().st_size == size) and (sum((p.stat().st_size for p in actual)) == nonmanifest_bytes + size <= MAX_OWN_BYTES), 'Complete manifest-inclusive inventory and bytes')
    require(not any(((OUTPUT / n).exists() for n in ('failure.json', 'FAILED_UNSEALED.json'))), 'No failure marker after seal; ROOT still requires external terminal zero')
    owned_output_guard()

def copy(path, name):
    owned_output_guard()
    require(name in COPY_ROUTES and ROOT / COPY_ROUTES[name] == path, 'Exact planned copied source')
    source = canonical(path)
    expected = _FROZEN[source.relative_to(ROOT).as_posix()]
    require(digest(source, fresh=True) == expected, 'Prior externally expected copied input')
    before = fingerprint(source)
    target = OUTPUT / name
    members = inventory(OUTPUT)
    require(target.parent == OUTPUT and (not target.exists()) and (not target.is_symlink()) and (len(members) + 2 <= MAX_OWN_FILES) and (sum((p.stat().st_size for p in members)) + before[2] <= MAX_OWN_BYTES), 'Copied retention reserve')
    total, state = (0, hashlib.sha256())
    owned_output_guard()
    with source.open('rb') as incoming, target.open('xb') as outgoing:
        while (block := incoming.read(65536)):
            budget()
            total += len(block)
            state.update(block)
            require(total <= before[2], 'No growing copied input')
            owned_output_guard()
            require(outgoing.write(block) == len(block), 'No short copied write')
            owned_output_guard()
    require(total == before[2] and fingerprint(source) == before and (state.hexdigest() == expected) and (digest(target, fresh=True) == expected), 'Complete byte-exact copy is output, never input authority')
    owned_output_guard()

def current_review_admission(ready, authors):
    reviews = ready['static_review_expected_SHA256']
    require(type(reviews) is dict and set(reviews) == set(CURRENT_REVIEW_PATHS), 'Exactly own current three reviews')
    for key in CURRENT_REVIEW_PATHS:
        review = bootstrap_json(ROOT / key, reviews[key])
        require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers'] == [] and (review['author_method_SHA256'] == authors), 'Current full scientific and lifecycle flags before runtime or origins')
        bind(ROOT / key, reviews[key])

def five_radial_proof_controls():
    radial_scope_validator(CURRENT_POSITIVE_SCOPE)
    results = []
    for row in CURRENT_CONTROL_SPECS:
        variants = []
        for mutation in row['fixed_bad_metadata_variants']:
            bad = dict(CURRENT_POSITIVE_SCOPE)
            bad.update(mutation)
            try:
                radial_scope_validator(bad)
            except E11RadialProofReject as error:
                require(type(error) is E11RadialProofReject and str(error) == row['dedicated_tag'], 'Exact dedicated control rejection')
                variants.append({'mutation': mutation, 'rejected': True, 'dedicated_tag': str(error)})
            else:
                raise AssertionError('A fixed radial control was not rejected')
        results.append({'category': row['category'], 'variants': variants})
    require(len(results) == 5 and sum((len(r['variants']) for r in results)) == 13, 'Exactly five categories and thirteen controls')
    return {'passed': True, 'positive_validated_first': True, 'categories': results, 'fixed_categories_variants': [5, 13]}

def flags():
    return {key: COMMON_EXPECTATIONS[key] for key in RADIAL_FLAG_KEYS}

def fresh_radial_union():
    require(_FULL_ADMISSION is True, 'Whole admission precedes either union')
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical, fresh=True) == actual, 'Fresh confinement of every cached input')
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(not path.is_relative_to(OUTPUT) and (path not in union or union[path] == pin), 'Expected role union excludes this output and conflicting pins')
            union[path] = pin
    for path, pin in tuple(_OBSERVED.items()):
        budget()
        if path.is_relative_to(OUTPUT):
            continue
        require(path in union and union[path] == pin, 'Observation must already have an externally expected equal pin')
    require(len(union) <= MAX_REFERENCES, 'Finite complete expected union')
    size = 0
    for path, pin in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES and digest(actual, fresh=True, already_resolved=True) == pin, 'Fresh full expected bytes, no observed synthesis')
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, 'Complete original and opaque failed inventories unchanged')
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS and (not any((p.exists() or p.is_symlink() for p in _ABSENT_RUNTIME))), 'Exact runtime and all historical/current absences')
    for path, pin in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == pin, 'Externally expected existing cache unchanged')
    strict_loaded_origins()
    source_code_guard()
    return {'unique_paths': len(union), 'unique_bytes': size, 'full_fresh_physical_resolve_and_SHA': True, 'observed_expected_pin_synthesis': False, 'current_output_observations_excluded': True, 'active_owners': ACTIVE_OWNERS, 'native12_transitive_only': True, 'absent_runtime_paths': sorted((str(p) for p in _ABSENT_RUNTIME)), 'original_owner_inventories': {str(p): sorted((str(q) for q in members)) for p, members in _OWN_INVENTORIES.items()}}

def independent_radial_cell_bound(inputs):
    row = inputs['independent130']
    lower, upper = (row['lower'], row['upper'])
    require(lower > 0 and max(lower.denominator.bit_length(), abs(lower.numerator).bit_length()) <= MAX_ANALYTIC_TEMP_BITS, 'Independent reciprocal guard before construction')
    inverse = rational_guard(Fraction(lower.denominator, lower.numerator))
    delta = checked_ratio([1, 4294967296])
    delta2 = times(delta, delta)
    series = checked_ratio([0, 1])
    terms = []
    for j in range(1, 32):
        budget()
        require(1 <= j <= 31 and 5 <= 36 - j <= 35, 'Fixed independent shift/index before operation')
        term = checked_ratio([1, j * (1 << 36 - j)])
        series = plus(series, term)
        terms.append(pair_literal(term))
    remainder = plus(checked_ratio([1, 1]), times(checked_ratio([-1, 1]), delta))
    require(remainder > 0 and max(remainder.numerator.bit_length(), remainder.denominator.bit_length()) <= MAX_ANALYTIC_TEMP_BITS, 'Independent last-cell reciprocal guard')
    inv_remainder = rational_guard(Fraction(remainder.denominator, remainder.numerator))
    raw = plus(times(times(delta, inverse), plus(checked_ratio([1, 32]), series)), times(delta2, plus(times(checked_ratio([31, 4]), upper), times(checked_ratio([1, 2]), inv_remainder))))
    ideal = plus(times(times(delta, inverse), plus(checked_ratio([1, 16]), times(checked_ratio([2, 1]), series))), times(delta2, plus(plus(times(checked_ratio([31, 2]), upper), inv_remainder), checked_ratio([1936, 49]))))
    return {'profile': 'independent130', 'raw_radial_squared_L2_upper': pair_literal(raw), 'coordinate_radial_contribution': pair_literal(times(checked_ratio([2, 1]), raw)), 'ideal_midpoint_coordinate_squared_L2_upper': pair_literal(ideal), 'independent_reversed_sum_terms': terms, 'terms_executed': 31, 'primary_evaluator_called': False, 'native_coordinate_recertified': False}

def main():
    global _STARTED, _OWNS_OUTPUT, _OWNED_OUTPUT_ID
    try:
        _STARTED = process_started()
        runtime_scopes()
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--ready-sha256', required=True)
        args = parser.parse_args()
        require(canonical(__file__) == AUTHOR and (not OUTPUT.exists()) and (not OUTPUT.is_symlink()), 'Own exclusive new output')
        ready, policy, finite, proposal, witness, runtime = radial_admission(args.ready_sha256)
        first = fresh_radial_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        row = OUTPUT.stat()
        _OWNED_OUTPUT_ID = tuple((getattr(row, key, None) for key in ('st_dev', 'st_ino', 'st_ctime_ns', 'st_mode', 'st_file_attributes', 'st_reparse_tag')))
        _OWNS_OUTPUT = True
        for name, source in COPY_ROUTES.items():
            copy(ROOT / source, name)
        save('run_started.json', {'created_UTC': time.time_ns(), 'PID': os.getpid(), 'limits_CPU_admission_wall': [CPU, ADMISSION, WALL], **flags()})
        save('interpreter.json', runtime)
        save('loaded_module_origins.json', {'strict_known_only_present_origins': True, 'serializer': SERIALIZATION_RUNTIME, 'current_cache_partition': {'present': ready['existing_new_code_cache_SHA256'], 'absent': ready['absent_new_code_cache_paths']}})
        save('original2_and_transitive12_scope.json', witness)
        save('protocol.json', policy)
        inputs, adapters = radial_source_literal_inputs(finite)
        save('source_and_own_profile_adapters.json', {'own_profiles': adapters, 'theorem': radial_theorem_record(proposal)})
        controls = five_radial_proof_controls()
        save('five_radial_proof_controls.json', controls)
        primary = primary_radial_cell_bound(inputs)
        independent = independent_radial_cell_bound(inputs)
        save('primary_radial_and_ideal_midpoint_bound.json', primary)
        save('independent_radial_and_ideal_midpoint_bound.json', independent)
        pc = same_profile_saved_comparison('primary90', primary, inputs)
        ic = same_profile_saved_comparison('independent130', independent, inputs)
        save('primary_same_profile_saved_comparison.json', pc)
        save('independent_same_profile_saved_comparison.json', ic)
        save('fresh_full_input_union_before_radial.json', first)
        qualification = {'radial_and_ideal_midpoint_bounds_only': True, 'new_native_or_downstream_certificate': False, 'only_original_two_current_owners': True, 'ROOT_external_terminal0_and_absent_failure_markers_required': True, **flags()}
        save('qualification_and_remaining_gaps.json', qualification)
        second = fresh_radial_union()
        save('fresh_full_input_union_after_radial.json', second)
        summary = {'schema': 'e11-radial-cell-coupling-summary-v1', 'passed': True, 'completed': True, 'exact_own_profile_assemblies': 2, 'exact_same_profile_saved_comparisons': 2, 'controls': controls, 'primary': primary, 'independent': independent, 'same_profile_comparisons': [pc, ic], 'both_complete_fresh_input_unions': [first, second], 'planned_manifest_inclusive_owned_files': 29, 'limits_CPU_admission_wall': [CPU, ADMISSION, WALL], 'current_runtime': runtime, 'preseal_budget_observation': {'process_CPU_seconds': time.process_time(), 'wall_seconds': time.monotonic() - _STARTED}, 'budget_censored': False, **flags()}
        save('summary.json', summary)
        save('completion_outcome.json', {**summary, 'failed': False})
        members = inventory(OUTPUT)
        require({p.name for p in members} == set(PLANNED_FILES) - {'manifest.json'}, 'Exact preseal ledger')
        files, size = ({}, 0)
        for path in sorted(members):
            budget()
            size += path.stat().st_size
            files[path.name] = digest(path, fresh=True)
        complete_manifest({'schema': 'e11-radial-cell-coupling-manifest-v1', 'files': files, 'frozen_inputs': _FROZEN, 'external_runtime_inputs': _EXTERNAL, 'manifest_self_hash_excluded': True, 'completed': True, 'passed': True, 'budget_censored': False, 'both_complete_fresh_input_unions': [first, second], **flags()}, files, size)
        budget()
        print(json.dumps({'passed': True, 'manifest_SHA256': digest(OUTPUT / 'manifest.json', fresh=True), **flags()}), flush=True)
    except BaseException as error:
        retain_failure(error)
        raise

def original2_and_transitive12_witness(finite, proposal):
    snapshots = proposal['complete_two_original_scientific_owner_snapshots']
    require(set(snapshots) == set(ACTIVE_OWNERS), 'Only original two current owners')
    owners = {name: full_active_owner(name, snapshots[name], []) for name in ACTIVE_OWNERS}
    citation = finite['native12_transitive_citation_authority']
    gap = read(ROOT / citation['path'])
    nested = gap
    for key in citation['field']:
        nested = nested[key]
    require(set(nested) == set(citation['exact_original_owner_names']) and {key: object_sha(row) for key, row in nested.items()} == citation['each_full_snapshot_canonical_JSON_SHA256'], 'Complete original twelve snapshots are transitive metadata, not new owners')
    require(finite['original_native12_classifications']['new_current_owner_admission'] is False, 'No recursive SUCCESS or external runtime expansion')
    return {'two_original_current_owner_witnesses': owners, 'native12_transitive_citation': citation, 'active_archive_counts': [8, 4], 'native12_new_success_owners': False}

def original3_history_cache_admission(finite):
    for name, row in finite['original3_actual_history_cache_roles'].items():
        ready = read(bind(ROOT / row['original_READY_path'], row['original_READY_expected_SHA256']))
        require(ready['author_method_SHA256'] == row['original_author_method_SHA256'] and ready['static_review_expected_SHA256'] == row['original_static_review_expected_SHA256'] and (ready['output'] == row['original_output']), 'Original raw history declarations retained')
        for qualified in row['original_author_bare_key_to_declared_physical_path_roles'].values():
            bind(Path(qualified['original_declared_path']), qualified['original_expected_SHA256'])
        for key, pin in row['original_static_review_expected_SHA256'].items():
            bind(ROOT / key, pin)
        partition = {'existing_expected_SHA256': ready['existing_new_code_cache_SHA256'], 'absent_paths': ready['absent_new_code_cache_paths']}
        require(partition == row['actual_original_cache_partition'], 'Actual historical cache partition authority')
        source = next((key for key in ready['author_method_SHA256'] if key.endswith('.py')))
        historical_code_cache_partition(RESEARCH / source, partition)
    retain_failed_e11_v1()

def owned_output_guard():
    budget()
    require(_OWNS_OUTPUT is True and OUTPUT.is_dir() and (not OUTPUT.is_symlink()) and (OUTPUT.resolve(strict=True) == OUTPUT), 'This run owns the exact output directory')
    row = OUTPUT.stat()
    identity = tuple((getattr(row, key, None) for key in ('st_dev', 'st_ino', 'st_ctime_ns', 'st_mode', 'st_file_attributes', 'st_reparse_tag')))
    require(identity == _OWNED_OUTPUT_ID, 'Immutable directory identity; allocation size is not identity')

def primary_radial_cell_bound(inputs):
    row = inputs['primary90']
    lower, upper = (row['lower'], row['upper'])
    require(lower > 0 and max(lower.denominator.bit_length(), abs(lower.numerator).bit_length()) <= MAX_ANALYTIC_TEMP_BITS, 'Primary reciprocal guard before construction')
    inverse = rational_guard(Fraction(lower.denominator, lower.numerator))
    delta = checked_ratio([1, 4294967296])
    delta2 = times(delta, delta)
    first = times(times(delta, checked_ratio([1, 32])), inverse)
    band = checked_ratio([0, 1])
    terms = []
    for k in range(31):
        budget()
        require(0 <= k <= 30 and 5 <= k + 5 <= 35, 'Fixed primary shift/index before operation')
        coefficient = checked_ratio([1, (1 << k + 5) * (31 - k)])
        term = times(times(delta, inverse), coefficient)
        band = plus(band, term)
        terms.append(pair_literal(term))
    upper_band = times(times(checked_ratio([31, 4]), delta2), upper)
    remainder = plus(checked_ratio([1, 1]), times(checked_ratio([-1, 1]), delta))
    require(remainder > 0 and max(remainder.numerator.bit_length(), remainder.denominator.bit_length()) <= MAX_ANALYTIC_TEMP_BITS, 'Primary last-cell reciprocal guard')
    last = times(times(delta2, checked_ratio([1, 2])), rational_guard(Fraction(remainder.denominator, remainder.numerator)))
    raw = plus(plus(plus(first, band), upper_band), last)
    coordinate = times(checked_ratio([2, 1]), raw)
    angular = times(times(checked_ratio([4, 1]), times(checked_ratio([22, 7]), checked_ratio([22, 7]))), delta2)
    ideal = plus(coordinate, angular)
    return {'profile': 'primary90', 'raw_radial_squared_L2_upper': pair_literal(raw), 'coordinate_radial_contribution': pair_literal(coordinate), 'ideal_midpoint_coordinate_squared_L2_upper': pair_literal(ideal), 'angular_contribution': pair_literal(angular), 'four_raw_stages': [pair_literal(first), pair_literal(band), pair_literal(upper_band), pair_literal(last)], 'lower_band_terms': terms, 'terms_executed': 31, 'native_coordinate_recertified': False}

def radial_admission(ready_sha):
    global _FULL_ADMISSION
    ready, policy = admit_current_metadata_and_startup(ready_sha)
    finite, proposal = radial_method_roles()
    original3_history_cache_admission(finite)
    witness = original2_and_transitive12_witness(finite, proposal)
    native = read(ROOT / proposal['complete_two_original_scientific_owner_snapshots'][NATIVE_OWNER]['manifest_path'])
    runtime = known_runtime_admission(native)
    serialization_runtime_admission()
    strict_loaded_origins()
    source_code_guard()
    require(_FULL_ADMISSION is False, 'Sole whole-admission transition')
    _FULL_ADMISSION = True
    return (ready, policy, finite, proposal, witness, runtime)

def radial_method_roles():
    for key, pin in AUTHOR_INPUTS.items():
        bind(ROOT / key, pin)
    finite = read(ROOT / FINITE_METHOD)
    proposal = read(ROOT / SYMBOLIC_METHOD)
    grant = read(ROOT / AUTHORGRANT)
    require(grant['passed'] is grant['science_static_passed'] is grant['lifecycle_static_passed'] is True and grant['blockers'] == [] and (grant['controller_authoring_authorized'] is True) and (grant['SOURCE_authoring_only'] is True) and (grant['READY_or_SCI_execution_authorized'] is False), 'Separate authoring grant has no scientific execution permission')
    require(grant['reviewed_METHOD_path'] == FINITE_METHOD and grant['reviewed_METHOD_SHA256'] == AUTHOR_INPUTS[FINITE_METHOD] and (grant['future_current_SOURCE_MD_policy_QA_graph_delta_routes']['SOURCE'] == AUTHOR.relative_to(ROOT).as_posix()), 'Exact current authoring routes')
    expected = dict(finite['full_READY_policy_field_role_graph']['fixed_shared_values'])
    require(expected['accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256'] == {key: None for key in FINITE_PINS} and expected['current_authoring_acceptance_SHA256'] is None, 'Only five prior authority leaves')
    expected['accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256'] = FINITE_PINS
    expected['current_authoring_acceptance_SHA256'] = AUTHOR_INPUTS[AUTHORGRANT]
    require(expected == COMMON_EXPECTATIONS and grant['accepted_finite_METHOD_MD_independent_ROOT_expected_SHA256'] == FINITE_PINS, 'Full finite field graph unchanged except exact five accepted pins')
    require(finite['accepted_symbolic_METHOD_MD_independent_ROOT_expected_SHA256'] == SYMBOLIC_PINS and grant['accepted_symbolic_METHOD_MD_independent_ROOT_expected_SHA256'] == SYMBOLIC_PINS, 'Exact independent symbolic and finite authority')
    for group, path in ((SYMBOLIC_PINS, SYMBOLIC_METHOD), (FINITE_PINS, FINITE_METHOD)):
        for key, pin in group.items():
            if key.endswith('.json') and key != path:
                review = read(ROOT / key)
                require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers'] == [] and (review['reviewed_METHOD_path'] == path) and (review['reviewed_METHOD_SHA256'] == group[path]), 'Exact accepted METHOD reviews')
    require(object_sha(proposal['complete_two_original_scientific_owner_snapshots']) == ORIGINAL2_SHA, 'Complete two-owner snapshot object commitment')
    return (finite, proposal)

def radial_scope_validator(value):
    if type(value) is not dict or set(value) != set(CURRENT_POSITIVE_SCOPE):
        raise E11RadialProofReject('RADIAL_UNITS_SCOPE')
    for tag, row in VALIDATOR_PREDICATES.items():
        for key, expected in row['positive_expected_values'].items():
            if type(value[key]) is not type(expected) or value[key] != expected:
                raise E11RadialProofReject(tag)

def radial_source_literal_inputs(finite):
    radial_scope_validator(CURRENT_POSITIVE_SCOPE)
    inputs, records = ({}, {})
    for profile, row in finite['own_profile_endpoints_and_comparison_pointers'].items():
        ledger = read(ROOT / row['original_ln2_ledger_path'])
        component = read(ROOT / row['original_component_path'])
        old = read(ROOT / row['old_coordinate_path'])
        endpoint = ledger['endpoints'][2]
        require(endpoint['argument_exact'] == [2, 1] and endpoint['terms_executed'] == endpoint['fixed_terms'] == row['original_ln2_fixed_terms_history_only'], 'Own saved ln2 endpoint role and unchanged series history')
        pair = endpoint['window_exact']
        require(pair[0] == component['exact_component_allowances']['ln2_lower'] and pair[1] == component['exact_component_allowances']['ln2_upper'], 'Own literal ledger/component endpoint equality')
        lower, upper = (checked_ratio(pair[0]), checked_ratio(pair[1]))
        require(checked_ratio([1, 2]) <= lower <= upper <= checked_ratio([1, 1]), 'Positive own ln2 guards before any reciprocal')
        inputs[profile] = {'lower': lower, 'upper': upper, 'old': old, 'roles': row}
        records[profile] = {'roles': row, 'ln2_endpoint_exact_pairs': pair, 'positive_own_ln2_guard_passed': True, 'new_series_executed': False, 'native_arrays_replayed': False}
    require(set(inputs) == {'primary90', 'independent130'}, 'Exactly two own profiles')
    return (inputs, records)

def radial_theorem_record(proposal):
    require(proposal['primary_recipe_unevaluated'] == PRIMARY_RECIPE and proposal['independent_recipe_unevaluated'] == INDEPENDENT_RECIPE, 'Accepted two own recipes')
    return {'accepted_symbolic_expected_SHA256': SYMBOLIC_PINS, 'complete_symbolic_proposal_object_SHA256': object_sha(proposal), 'first_and_last_cells_paid': True, 'all_aligned_lower_bands_paid': True, 'native_or_stock_arrays_or_bounds_recertified': False, 'digital_pair_independence': False}

def retain_failure(error):
    if _OWNS_OUTPUT is not True:
        return
    try:
        owned_output_guard()
        save('failure.json', {'passed': False, 'completed': False, 'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(), **flags()})
        owned_output_guard()
    except BaseException:
        pass
    try:
        owned_output_guard()
        with (OUTPUT / 'FAILED_UNSEALED.json').open('xb') as stream:
            marker = b'{"passed":false,"completed":false,"failed":true}\n'
            require(stream.write(marker) == len(marker), 'Complete failure marker')
        owned_output_guard()
    except BaseException:
        pass

def same_profile_saved_comparison(profile, result, inputs):
    row = inputs[profile]
    old = row['old']
    roles = row['roles']
    require(read(ROOT / roles['old_coordinate_path']) == old and result['profile'] == profile, 'Same own profile source')
    new_ideal = checked_ratio(result['ideal_midpoint_coordinate_squared_L2_upper'])
    old_ideal = checked_ratio(old[roles['old_ideal_midpoint_field']])
    arithmetic = checked_ratio(old[roles['old_arithmetic_field']])
    rational_guard(new_ideal)
    rational_guard(old_ideal)
    require(abs(new_ideal.numerator).bit_length() + old_ideal.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS and abs(old_ideal.numerator).bit_length() + new_ideal.denominator.bit_length() <= MAX_ANALYTIC_TEMP_BITS, 'Cross-product temporary guards before exact saved comparison')
    improved = new_ideal.numerator * old_ideal.denominator <= old_ideal.numerator * new_ideal.denominator
    return {'profile': profile, 'new_ideal_midpoint_upper': pair_literal(new_ideal), 'old_same_profile_ideal_midpoint_upper': pair_literal(old_ideal), 'new_upper_not_greater_than_old_upper': improved, 'original_native_arithmetic_allowance_unchanged': pair_literal(arithmetic), 'raw_radial_compared_to_old_factor2_stage': False, 'new_native_or_financial_certificate': False}

def save(name, value):
    owned_output_guard()
    require(name in PLANNED_FILES or name == 'failure.json', 'Registered metadata filename')
    target = OUTPUT / name
    require(target.parent == OUTPUT and (not target.exists()) and (not target.is_symlink()), 'Exclusive metadata file')
    guard_serialization_integers(value)
    pieces, size = ([], 0)
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(value):
        budget()
        part = fragment.encode('utf-8')
        size += len(part)
        require(size < MAX_OWN_BYTES, 'Prospective encoding cap including newline')
        pieces.append(part)
    pieces.append(b'\n')
    size += 1
    members = inventory(OUTPUT)
    require(len(members) + 1 + (name != 'manifest.json') <= MAX_OWN_FILES and sum((p.stat().st_size for p in members)) + size <= MAX_OWN_BYTES, 'Manifest-inclusive retention cap')
    owned_output_guard()
    with target.open('xb') as stream:
        buffer = bytearray()
        for part in pieces:
            budget()
            offset = 0
            while offset < len(part):
                budget()
                count = min(65536 - len(buffer), len(part) - offset)
                require(count > 0, 'Positive fixed-size fitting slice')
                buffer.extend(part[offset:offset + count])
                offset += count
                if len(buffer) == 65536:
                    owned_output_guard()
                    require(stream.write(buffer) == len(buffer), 'No short physical write')
                    owned_output_guard()
                    buffer.clear()
        if buffer:
            owned_output_guard()
            require(stream.write(buffer) == len(buffer), 'No short final physical write')
            owned_output_guard()
    require(target.stat().st_size == size, 'Byte-exact original JSON encoding with newline')
    owned_output_guard()

def source_code_guard():
    global _HASH_WORK
    actual = canonical(AUTHOR, fresh=True)
    before = fingerprint(actual)
    require(before[2] <= 8 << 20, 'Finite SOURCE byte cap before read')
    with actual.open('rb') as stream:
        raw = stream.read(before[2] + 1)
    _HASH_WORK += len(raw)
    require(_HASH_WORK <= MAX_HASH_WORK and len(raw) == before[2] and (fingerprint(actual) == before) and (hashlib.sha256(raw).hexdigest() == _FROZEN[actual.relative_to(ROOT).as_posix()]), 'Exact externally bound SOURCE bytes')
    tree = ast.parse(raw)
    definitions = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    require(len(definitions) == 52 and {k: hashlib.sha256(ast.dump(n, include_attributes=False).encode()).hexdigest() for k, n in definitions.items()} == _CURRENT_AST_MAP, 'Complete current51 functions and Class AST map')
    compiled = compile(raw, str(AUTHOR), 'exec', dont_inherit=True, optimize=0)
    codes = {c.co_name: c for c in compiled.co_consts if isinstance(c, types.CodeType) and c.co_name in definitions}
    require(set(codes) == set(definitions), 'Every whole definition compiled without execution')
    namespace = globals()
    for name, node in definitions.items():
        budget()
        loaded = namespace[name]
        if isinstance(node, ast.ClassDef):
            require(name == 'E11RadialProofReject' and node.decorator_list == [] and (node.keywords == []) and (len(node.body) == 1) and isinstance(node.body[0], ast.Pass) and (len(node.bases) == 1) and isinstance(node.bases[0], ast.Name) and (node.bases[0].id == 'ValueError') and isinstance(loaded, type) and (loaded.__bases__ == (ValueError,)) and (loaded.__name__ == name) and (loaded.__qualname__ == name) and (loaded.__module__ == __name__) and (set(loaded.__dict__) <= {'__module__', '__doc__', '__dict__', '__weakref__'}), 'Exact plain dedicated rejection Class')
        else:
            require(type(loaded) is types.FunctionType and loaded.__globals__ is namespace and (loaded.__code__ == codes[name]), 'Loaded whole function/nested code equals frozen SOURCE')
            require(node.decorator_list == [] and loaded.__defaults__ == (tuple((ast.literal_eval(v) for v in node.args.defaults)) or None) and (loaded.__kwdefaults__ == ({a.arg: ast.literal_eval(v) for a, v in zip(node.args.kwonlyargs, node.args.kw_defaults) if v is not None} or None)) and (loaded.__annotations__ == {**{a.arg: ast.unparse(a.annotation) for a in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs] if a.annotation is not None}, **({'return': ast.unparse(node.returns)} if node.returns is not None else {})}) and (loaded.__doc__ == ast.get_docstring(node, clean=False)), 'Exact decorators/defaults/annotations/docstrings')
    modules = {'argparse': argparse, 'ast': ast, 'ctypes': ctypes, 'hashlib': hashlib, 'json': json, 'os': os, 'sys': sys, 'time': time, 'traceback': traceback, 'types': types, '_pylong': _pylong}
    for name, module in modules.items():
        require(module is sys.modules[name] and namespace[name] is module, 'Exact imported standard module identity')
    require(Path is sys.modules['pathlib'].Path and Fraction is sys.modules['fractions'].Fraction and (cache_from_source is sys.modules['importlib.util'].cache_from_source) and (wintypes is ctypes.wintypes), 'Exact imported constructors and cache helper')
    expected = {}

    def literal(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return expected[node.id]
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            values = [literal(n) for n in node.elts]
            return tuple(values) if isinstance(node, ast.Tuple) else set(values) if isinstance(node, ast.Set) else values
        if isinstance(node, ast.Dict):
            return {literal(k): literal(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'Path') and (len(node.args) == 1):
            return Path(literal(node.args[0]))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'set') and (not node.args):
            return set()
        if isinstance(node, ast.BinOp):
            a, b = (literal(node.left), literal(node.right))
            if isinstance(node.op, ast.Div):
                return a / b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Pow):
                return a ** b
            if isinstance(node.op, ast.Add):
                return a + b
        raise AssertionError('Undeclared module initializer form')
    mutable = {'_FROZEN': dict, '_EXTERNAL': dict, '_OBSERVED': dict, '_PATH_CACHE': dict, '_HASH_CACHE': dict, '_OWN_INVENTORIES': dict, '_ABSENT_RUNTIME': set, '_STANDARD_RUNTIME_MEMBERS': set, '_CODE_CACHE_EXPECTED': dict, '_BASE_SCOPE': object, '_EXCLUDED_SCOPE': object, '_HASH_WORK': int, '_REFERENCES': int, '_STARTED': object, '_FULL_ADMISSION': bool, '_OWNS_OUTPUT': bool, '_OWNED_OUTPUT_ID': object, '_CURRENT_AST_MAP': dict}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            require(len(node.targets) == 1, 'One module assignment target')
            target = node.targets[0]
            value = literal(node.value)
            names = [target.id] if isinstance(target, ast.Name) else [n.id for n in target.elts]
            values = [value] if isinstance(target, ast.Name) else list(value)
            require(len(names) == len(values), 'Exact packed module initializer ABI')
            for name, value in zip(names, values):
                expected[name] = value
                if name in mutable:
                    kind = mutable[name]
                    require(kind is object or type(namespace[name]) is kind, 'Tracked lifecycle mutable global type')
                else:
                    require(type(namespace[name]) is type(value) and namespace[name] == value, 'Every immutable module initializer unchanged')
    import_names = {a.asname or a.name.split('.')[0] for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
    allowed_namespace = set(definitions) | set(expected) | import_names | {'__name__', '__doc__', '__package__', '__loader__', '__spec__', '__builtins__', '__file__', '__cached__', '__annotations__'}
    require(set(namespace) <= allowed_namespace and __doc__ == ast.get_docstring(tree, clean=False), 'Complete module namespace/import/docstring closure; no undeclared builtin shadow')
    require(type(_FULL_ADMISSION) is type(_OWNS_OUTPUT) is bool and 0 <= _REFERENCES <= MAX_REFERENCES and (0 <= _HASH_WORK <= MAX_HASH_WORK) and (INTEGER_DECIMAL_DIGITS == 4300), 'Tracked mutable state is finite; no setter or observed authority')
    require(len({id(_FROZEN), id(_EXTERNAL), id(_OBSERVED), id(_PATH_CACHE), id(_HASH_CACHE), id(_OWN_INVENTORIES), id(_CODE_CACHE_EXPECTED)}) == 7 and len({id(_ABSENT_RUNTIME), id(_STANDARD_RUNTIME_MEMBERS)}) == 2, 'Tracked mutable namespaces have no undeclared aliases')
    for mapping in (_FROZEN, _EXTERNAL):
        require(all((type(k) is str and type(v) is str and (len(v) == 64) and all((c in '0123456789abcdef' for c in v)) for k, v in mapping.items())), 'Tracked expected maps retain only literal hash authority')
    for path, pin in _OBSERVED.items():
        expected_pin = _FROZEN.get(path.relative_to(ROOT).as_posix()) if path.is_relative_to(ROOT) else _EXTERNAL.get(str(path))
        require(path.is_relative_to(OUTPUT) or expected_pin == pin, 'Tracked observations never become expected authority')
    require(_BASE_SCOPE == BASE and _EXCLUDED_SCOPE == (BASE / 'Lib/site-packages', (BASE / 'Lib/site-packages').resolve(strict=False)), 'Tracked runtime scopes retain original exclusion')
    ready = read(READY)
    expected_absences = {BASE / 'python312.zip'} | {ROOT / key for key in ready['absent_new_code_cache_paths']}
    expected_caches = {ROOT / key: pin for key, pin in ready['existing_new_code_cache_SHA256'].items()}
    if FINITE_METHOD in _FROZEN and SYMBOLIC_METHOD in _FROZEN:
        finite = read(ROOT / FINITE_METHOD)
        proposal = read(ROOT / SYMBOLIC_METHOD)
        for row in finite['original3_actual_history_cache_roles'].values():
            expected_absences.update((ROOT / key for key in row['actual_original_cache_partition']['absent_paths']))
            expected_caches.update({ROOT / key: pin for key, pin in row['actual_original_cache_partition']['existing_expected_SHA256'].items()})
        expected_absences.update((Path(key) for key in SERIALIZATION_RUNTIME['absent_three_variant_cache_paths']))
        failed_decl = finite['original_failed_scalar19_opaque_history']
        expected_absences.update((ROOT / failed_decl['output'] / name for name in failed_decl['manifest_and_summary_and_second_union_absent']))
        expected_inventories = {(ROOT / row['manifest_path']).parent: {ROOT / entry['path'] for entry in row['complete_physical_receipt_inventory_expected_hashes_and_stat_only']} for row in proposal['complete_two_original_scientific_owner_snapshots'].values()}
        failed = finite['original_failed_scalar19_opaque_history']
        expected_inventories[ROOT / failed['output']] = {ROOT / failed['output'] / name for name in failed['complete_failed_owned_inventory']}
        require(_OWN_INVENTORIES == expected_inventories, 'Tracked two owners plus failed19 match original literal inventories')
        require(_STANDARD_RUNTIME_MEMBERS == {Path(k) for k in finite['runtime_contract']['original_external2842_expected_map']} | {LAUNCHER}, 'Tracked runtime set equals original native2842 plus launcher')
    else:
        require(_OWN_INVENTORIES == {} and _STANDARD_RUNTIME_MEMBERS == set(), 'No premature owned/runtime population')
    require(_ABSENT_RUNTIME == expected_absences and _CODE_CACHE_EXPECTED == expected_caches, 'Tracked absent/present cache sets equal exact phase declarations, no ignored populated sets')
    if _OWNS_OUTPUT:
        owned_output_guard()
    else:
        require(_OWNED_OUTPUT_ID is None, 'Unowned output has no fabricated identity')
if __name__ == '__main__':
    main()
