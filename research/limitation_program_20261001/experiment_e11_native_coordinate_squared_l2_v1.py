"""Dormant E11 original-native Gaussian coordinate squared-L2 rational-only assembly.
Independent frozen controller peer and ROOT READY are mandatory before execution.
No old scientific helper/evaluator, numerical package, native gate array, fitting or sampling.
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
AUTHOR = RESEARCH / "experiment_e11_native_coordinate_squared_l2_v1.py"
METHOD_DOC = RESEARCH / "E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "e11_native_coordinate_squared_l2_preflight_v1.json"
READY = ROOT / ".context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/E11_native_coordinate_squared_L2_run001"
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
AUTHOR_INPUTS = {'.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_PROSPECTUS_run001.md': 'acc20e9a0441c6c1fbadb0e6bb6242fb806b7cbef1ff1e6fa33df269f4d882dc', '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_PROSPECTUS_run001.json': '301a97276c10e6a4a23a663bffb0e4224ab83f5f37aeec377c71f20e2fef509c', '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_AUTHOR_METADATA_QA_run001.json': 'cf4006e5b109961f8547d5918f222c9422451aa10a06fab9a72124e6a8256281', '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_GAP_MAP_INDEPENDENT_METHOD_REVIEW_next_run001.json': '9605eb108a704d215f64a977e9f67d9bc231d70727dc113d86ba003f477a2f7f', '.context/E11_NEXT_NATIVE_SAME_LAW_L2_BRIDGE_ROOT_PROSPECTIVE_METHOD_REVIEW_run001.json': '53f2107f8d6fdd7597ce892c26956d2ea9ee879099158fa7be5d6ebff88ab0b1', '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_PREPARATION_run001.md': 'af3a74d8be55f825070e9128268c7dc29579625da6a067c250f0b48651b6a594', '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_PREPARATION_run001.json': '09cb3e5debb6977c98e96e7487f9cc479f9d025db73e597946d706be2a1bdfae', '.context/E11_NATIVE_COORDINATE_BRIDGE_FUTURE_PROVENANCE_RETENTION_METADATA_QA_run001.json': '81726c245500a1b8a879a7500b5ca90839ff2684ee738eef10286dce6e84f72b', '.context/E11_NATIVE_COORDINATE_BRIDGE_PREPARATION_ROOT_METADATA_REVIEW_run001.json': '82762cc1752cbe7685d9c109b8cee3d3f732a27ff685eba019e14cef1903a7ba', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_METHOD_SUPPLEMENT_run001.md': '95390f58c23c9b51e51fbf4aa10f4ed41602e7ce636d61b93956b5d724517b32', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_METHOD_SUPPLEMENT_run001.json': '28c0c9280eb77755b88119000023ba344191c85dbc20ec253c98c89f1e7070e2', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_METHOD_SUPPLEMENT_METADATA_QA_run001.json': 'a2befdc7b0d24562ce12e56908dc856b227cd9c3b58f67b27462a2712bf1b4ec', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_ROOT_SYMBOLIC_REVIEW_run001.json': '4b841bd78a7827cf3b09ea5ec32da63a9c419ceb461f193e317ed9d1c213b06a', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_INDEPENDENT_STATIC_METHOD_PEER_run001.json': '7a6ec840faa1c1760ed80617f92c3faa66af1698600141bbf339fc208d69efac', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ACTUAL_RESULT_ROOT_VERIFICATION_run003.json': '91bcea31e3aba493d89ed7d617f9cda0ef306e57188e5835cac919e6e2b9f50f', '.context/E11_scalar_midpoint_L2_actual_ROOT_result_review_run003.py': 'bb06b0f3316fc1987b5a5defc7f19f479a995cb6e306f670b31355fc50b47fe1', '.context/E11_SCALAR_MIDPOINT_L2_ROOT_CHECKER003_INDEPENDENT_STATIC_DELTA_SUPPLEMENT_next_run001.json': '05012ca7493daf8f2a6aeb40c523cc4210dd5a9ba5c072e2583f869f5d1388da', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_FAILED_UNSEALED_ROOT_FREEZE_run001.json': 'c50342018999b1338a9ecc8ab5e6128a110b8d1076c5ce3021a6dac93e60dea6', '.context/E11_SCALAR_MIDPOINT_L2_NUMERICAL_ROOT_READY_run002.json': '9a9d00407a8a6f763e9142d95d97e06dcadde3f2d0a73dfa9fcf167ced6f2c65'}
COMMON_EXPECTATIONS = {'finite_protocol': {'numerical_envelope_assemblies': 2, 'primary_profile': 'primary90log/primary90cos/saved256ln2', 'independent_profile': 'independently_audited_log/independent130cos/saved1024ln2', 'proof_check': 'identity checks on existing primary records within second profile; no third envelope', 'primary_epsilon_l_strict_guard_comparisons': 1, 'new_series_or_precision_passes': 0, 'fixed_negative_controls': 4, 'numeric_fixtures': 0}, 'scientific_scope': {'source_law': 'original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'native_components': ['original_log_table_literal_and_native_Horner_floors', 'original_fixed_ln2_literal_and_all33_exponents', 'original_unclipped_minus2_nooverflow_and_unsigned46bit_isqrt_domain', 'original_sqrt_floor', 'all512_original_cosine_literals_and_native_Horner_floors', 'original_signed144product_stored72_and_product_floor'], 'quantity': 'squared_L2_Gaussian_coordinate', 'units': 'dimensionless_Gaussian_coordinate_squared', 'digital_pair_independence': False}, 'original_budget_caps': {'CPU_admission_creation_wall': [180, 150, 600], 'current_stdlib_runtime_files_bytes': [4096, 536870912], 'owned_files_bytes': [64, 134217728], 'references_unique_bytes_hash_work': [100000, 8589934592, 25769803776], 'serialized_integer_reduced_rational_analytic_temporary_bits': [65536, 131072, 524288]}, 'initial_decimal_digits': 4300, 'post_guard_decimal_digits': 20000, 'planned_manifest_inclusive_owned_file_count': 47, 'planned_manifest_inclusive_owned_file_ledger': ['executed_experiment_e11_native_coordinate_squared_l2_v1.py', 'executed_E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md', 'executed_e11_native_coordinate_squared_l2_preflight_v1.json', 'executed_E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json', 'reviewed_gap_map_method.md', 'reviewed_gap_map_method.json', 'reviewed_provenance_retention_preparation.md', 'reviewed_provenance_retention_preparation.json', 'reviewed_independent_method_peer.json', 'reviewed_ROOT_prospective_method.json', 'reviewed_preparation_metadata_QA.json', 'E11_completed_ROOT_saved_record_review003.json', 'E11_checker003_independent_delta.json', 'E11_failed_V1_ROOT_freeze.json', 'history_roles_and_nonpromotion.json', 'protocol.json', 'run_started.json', 'interpreter.json', 'loaded_module_origins.json', 'admission_scope_graph.json', 'active_owner_full_map_bindings_and_inventories.json', 'equal_SHA_archived_source_routes.json', 'selected_artifact_literal_adapters.json', 'B4_original_sampler_binding.json', 'B8_original_sampler_binding.json', 'upstream_ideal_gaussian_coordinate_authority.json', 'primary_native_arithmetic_components.json', 'independent_native_arithmetic_components.json', 'primary_native_coordinate_squared_L2_bound.json', 'independent_native_coordinate_squared_L2_bound.json', 'independent_primary_bound_proof_check.json', 'shared_pair_scope_without_independence.json', 'four_precise_negative_diagnostic_controls.json', 'qualification_and_remaining_gaps.json', 'fresh_full_input_union_before_assembly.json', 'fresh_full_input_union_after_assembly.json', 'summary.json', 'completion_outcome.json', 'manifest.json', 'original_manifest_A01_run011.json', 'original_manifest_A02_BM_native_financial_bridge_audit_run002.json', 'original_manifest_A02_BM_native_financial_bridge_root_verification_run001.json', 'original_manifest_A02_BM_native_financial_bridge_run002.json', 'original_manifest_A10_coefficient_run001.json', 'original_manifest_C06_pair_audit_run001.json', 'original_manifest_C06_pair_run001.json', 'original_manifest_E11_scalar_midpoint_L2_numerical_run002.json'], 'active_owner_names': ['A01_run011', 'A02_BM_native_financial_bridge_audit_run002', 'A02_BM_native_financial_bridge_root_verification_run001', 'A02_BM_native_financial_bridge_run002', 'A10_coefficient_run001', 'C06_pair_audit_run001', 'C06_pair_run001', 'E11_scalar_midpoint_L2_numerical_run002'], 'archive_only_citation_names': ['A01_run014', 'A02_quantile_financial_audit_run001', 'A02_quantile_law_audit_run001', 'E10_continuous_moment_only_run002'], 'owner_role_graph': {'A01_run011': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A01_run011', 'literal_expected_manifest_SHA256': '6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03', 'manifest_path': 'results/limitation_program_20261001/A01_run011/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [13, 623, None], 'role': 'active exact universal isqrt algebraic induction and archived native root structure only; no cost/fixture credit'}, 'A01_run014': {'active_proof_or_integrity_owner': False, 'archive_citation_only': True, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A01_run014', 'literal_expected_manifest_SHA256': '155bbe0b161c8ddf0da3550d834ed430dfe4c37f5275ddb192fda78f175759f8', 'manifest_path': 'results/limitation_program_20261001/A01_run014/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [16, 1221, None], 'role': 'archival cost/source-history citation only; not active approximation theorem or resource baseline'}, 'A02_BM_native_financial_bridge_audit_run002': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A02_BM_native_financial_bridge_audit_run002', 'literal_expected_manifest_SHA256': '62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0', 'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': True, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'RECEIPT_RELATIVE', 'original_map_counts': [23, 399, 2842], 'role': 'active independent130 all512 cosine literal/floor envelope and original-source audit; financial transport is not strong same-coupling L1'}, 'A02_BM_native_financial_bridge_root_verification_run001': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A02_BM_native_financial_bridge_root_verification_run001', 'literal_expected_manifest_SHA256': 'eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab', 'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_root_verification_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': True, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [2, 421, 2842], 'role': 'active saved original BM producer/auditor integrity authority; original missing terminal/header conventions retained'}, 'A02_BM_native_financial_bridge_run002': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A02_BM_native_financial_bridge_run002', 'literal_expected_manifest_SHA256': '78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162', 'manifest_path': 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': True, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'RECEIPT_RELATIVE', 'original_map_counts': [28, 375, 2842], 'role': 'active original-source binding/root provenance and primary90 all512 cosine literal/floor envelope; financial expectation bias is not a strong L2 premise'}, 'A02_quantile_financial_audit_run001': {'active_proof_or_integrity_owner': False, 'archive_citation_only': True, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A02_quantile_financial_audit_run001', 'literal_expected_manifest_SHA256': 'ca943429f62d6b1587e9210a8f5ad449b44720e760ec9b63aa94d21a60472323', 'manifest_path': 'results/limitation_program_20261001/A02_quantile_financial_audit_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [8, 2730, None], 'role': 'archival alternative-law price citation only; excluded same-U,V native coordinate proof'}, 'A02_quantile_law_audit_run001': {'active_proof_or_integrity_owner': False, 'archive_citation_only': True, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A02_quantile_law_audit_run001', 'literal_expected_manifest_SHA256': '7414ec32f4dc3ff9f98085c473f1c4dc1b045053f03c6b568336c3a46e95f572', 'manifest_path': 'results/limitation_program_20261001/A02_quantile_law_audit_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [7, 962, None], 'role': 'archival alternative finite-law citation only; excluded original BoxMuller numeric premises'}, 'A10_coefficient_run001': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/A10_coefficient_run001', 'literal_expected_manifest_SHA256': '0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40', 'manifest_path': 'results/limitation_program_20261001/A10_coefficient_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': False, 'frozen_inputs': False}, 'original_files_key_layout': 'RECEIPT_RELATIVE', 'original_map_counts': [None, None, None], 'role': 'active original B4/B8 target/descriptor/source snapshots and equal-SHA root source archives; legacy bare owned map retained; coefficient cost/real-function error not inferred'}, 'C06_pair_audit_run001': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/C06_pair_audit_run001', 'literal_expected_manifest_SHA256': '6207944e9d61bd27eaf8b7f1dfb05fbbe7223f38c997e613462314a86b9c6e14', 'manifest_path': 'results/limitation_program_20261001/C06_pair_audit_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [10, 111, None], 'role': 'active independently audited complete log literal/floor envelope, all-word no-overflow and actual pair source scopes'}, 'C06_pair_run001': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/C06_pair_run001', 'literal_expected_manifest_SHA256': 'edd1005612121fa739124ec24165aa2012afdec645dca63c13990012e4091a4a', 'manifest_path': 'results/limitation_program_20261001/C06_pair_run001/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': False, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'ROOT_RELATIVE', 'original_map_counts': [10, 24, None], 'role': 'active primary90 log table and exact original Q32/F40 paired sampler; old C06 cosine/cutoff combined coordinate error excluded'}, 'E10_continuous_moment_only_run002': {'active_proof_or_integrity_owner': False, 'archive_citation_only': True, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/E10_continuous_moment_only_run002', 'literal_expected_manifest_SHA256': '16a9c2e805839d423622ac2e21d9cd48c33d881281112220bc4a6aa19e2e7668', 'manifest_path': 'results/limitation_program_20261001/E10_continuous_moment_only_run002/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': True, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'RECEIPT_RELATIVE', 'original_map_counts': [17, 109, 2842], 'role': 'archival original E11 history only; C4/H8 moment result neither B4/B8 source/output nor a numeric native coordinate premise'}, 'E11_scalar_midpoint_L2_numerical_run002': {'active_proof_or_integrity_owner': True, 'archive_citation_only': False, 'complete_maps_owned_inventory_and_external_owned_docs_retained_in_immutable_GAP_JSON': True, 'complete_snapshot_exact_JSON_pointer': '/cited_complete_original_packet_snapshots/E11_scalar_midpoint_L2_numerical_run002', 'literal_expected_manifest_SHA256': '129ae9a650ac5c216b4f5221174dbcb5847b30100e493445171750fcd5a24170', 'manifest_path': 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/manifest.json', 'not_recursive_original_runtime_success_admission': True, 'original_field_presence': {'external_runtime_inputs': True, 'files': True, 'frozen_inputs': True}, 'original_files_key_layout': 'RECEIPT_RELATIVE', 'original_map_counts': [19, 174, 2842], 'role': 'active upstream ideal Gaussian coordinate coupling theorem and saved primary/independent ln2 windows only; f surrogate and old E10 moments not native financial proof'}}, 'archive_map_snapshots_only_in_fixed_gap_JSON': True, 'three_equal_SHA_archived_source_routes': [{'current_original_path_integrity_asserted': False, 'expected_hash_waived': False, 'expected_sha256': '69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6', 'original_key': 'research/controlled_source_completion/nonrestoring_sqrt.py', 'original_map': 'frozen_inputs', 'original_owner': 'A01_run011', 'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/nonrestoring_sqrt.py'}, {'current_original_path_integrity_asserted': False, 'expected_hash_waived': False, 'expected_sha256': '52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b', 'original_key': 'research/journal_sprint/reversible_fixed_point.py', 'original_map': 'frozen_inputs', 'original_owner': 'A01_run011', 'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible_fixed_point.py'}, {'current_original_path_integrity_asserted': False, 'expected_hash_waived': False, 'expected_sha256': '5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a', 'original_key': 'research/antithetic_feasibility/reversible.py', 'original_map': 'frozen_inputs', 'original_owner': 'A01_run011', 'verified_archived_path': 'results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py'}], 'completed_E11_V2_historical_cache_partition': {'existing_expected_SHA256': {}, 'absent_paths': ['research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-1.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.opt-2.pyc', 'research/limitation_program_20261001/__pycache__/experiment_e11_scalar_midpoint_l2_v2.cpython-312.pyc']}, 'current_required_review_paths': ['.context/E11_NATIVE_COORDINATE_SQUARED_L2_INDEPENDENT_STATIC_PEER_next_run001.json', '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json'], 'radicand_supplement_review_expected_SHA256': {'.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_ROOT_SYMBOLIC_REVIEW_run001.json': '4b841bd78a7827cf3b09ea5ec32da63a9c419ceb461f193e317ed9d1c213b06a', '.context/E11_NATIVE_COORDINATE_ORIGINAL_RADICAND_POSITIVITY_INDEPENDENT_STATIC_METHOD_PEER_run001.json': '7a6ec840faa1c1760ed80617f92c3faa66af1698600141bbf339fc208d69efac'}, 'fixed_original_source_expected_SHA256': {'docs/limitation_audit_20261001/implementation_plan/roadmap.json': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a', 'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md': 'b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637', 'research/advantage_frontier_20260923/barrier_oracle_depth.py': '1e0e225131c668f133ef05a5de3f78fbad4fb5307a2fc8c452d99d14c8dda929', 'research/controlled_source_completion/finance.py': '75f107e041a2b7fa7e1a6dfce471369549af96a18ae7852d212ca0e2b442f77b', 'research/controlled_source_completion/ir.py': '3a4af54bd2e439ef060b747ea8f26a0897ce9e4a119509b57fb018d936d5d223', 'results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384', 'results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/target.json': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'}, 'selected_original_artifact_expected_SHA256': {'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent130_cosine_envelope.json': '6bda8f5b03c3992d141d40c1fdbf7bace1fb714b1259ddf63c6418c306ee50d0', 'results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002/independent_transport_derivation.json': 'c23124e8a0e3c946172bb2879106f4c98a650784e2af72d625ef8367d2cb0ed2', 'results/limitation_program_20261001/A02_BM_native_financial_bridge_root_verification_run001/summary.json': '2f2ba5650a9255c38304969405962ce5babe4bb09a9882b68be0f26d531ed816', 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/complete_financial_bounds.json': '1ed44ea428e5bdc92d83cab57f51ea0d102f680344335fafb95ff5cdc01e350f', 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/cosine_envelope.json': 'a0e52ba6051ce9af1dbde6f387eefde0932c00bf34f6240491016c322f85cd27', 'results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/native_source_binding.json': 'f6f10f434d1408fae49419ae1503f3bda2588eb47b9179ea292eb25949846a41', 'results/limitation_program_20261001/C06_pair_audit_run001/actual_pair_scope_audit.json': '281b9bc40e78427b86e036aeb72382da767d39629747300c4d7e88099ef7d1e7', 'results/limitation_program_20261001/C06_pair_audit_run001/all_Q32_native_nooverflow_audit.json': '01e146b99fd6578331d50c9622ed1e70474941f706b9c66ce9abc8aa32a66cd7', 'results/limitation_program_20261001/C06_pair_audit_run001/independent_table_audit.json': '41a1ad7a86a07000314933f0bf6fe2174cc51d14fccf7b5c48762138209a5b32', 'results/limitation_program_20261001/C06_pair_run001/certificate.json': '8f027631a4b6abc6f601da2d7bbde3438c95557ebad7bf8fbb7b583aadca844c', 'results/limitation_program_20261001/E11_scalar_midpoint_L2_numerical_run002/exact_real_analytic_proof_and_scope.json': '229b26f1c68d6ba9e6bdb917c31fef3ed096a5861103b6029d9fe8539d5959ac'}, 'new_results': {'primary_native_arithmetic_components': None, 'independent_native_arithmetic_components': None, 'primary_coordinate_squared_L2_bound': None, 'independent_coordinate_squared_L2_bound': None, 'sole_primary_epsilon_l_guard_result': None, 'independent_primary_record_proof_check': None, 'diagnostic_control_results': None, 'runtime_resources_and_feasibility': None, 'financial_price_policy_path_G2_join': None}, 'historical_ownership_permission_separation': 'active8 exact original maps/inventories; archive4 citations, old READY/cache/failure roles only', 'root_original_domain_guards_separate_from_positivity': True, 'no_repair_refresh_or_expected_hash_waiver': True}
ACTIVE_OWNERS = ['A01_run011', 'A02_BM_native_financial_bridge_audit_run002', 'A02_BM_native_financial_bridge_root_verification_run001', 'A02_BM_native_financial_bridge_run002', 'A10_coefficient_run001', 'C06_pair_audit_run001', 'C06_pair_run001', 'E11_scalar_midpoint_L2_numerical_run002']
ARCHIVE_CITATIONS = ['A01_run014', 'A02_quantile_financial_audit_run001', 'A02_quantile_law_audit_run001', 'E10_continuous_moment_only_run002']
PLANNED_FILES = ['executed_experiment_e11_native_coordinate_squared_l2_v1.py', 'executed_E11_NATIVE_COORDINATE_SQUARED_L2_PREFLIGHT_V1.md', 'executed_e11_native_coordinate_squared_l2_preflight_v1.json', 'executed_E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_READY_run001.json', 'reviewed_gap_map_method.md', 'reviewed_gap_map_method.json', 'reviewed_provenance_retention_preparation.md', 'reviewed_provenance_retention_preparation.json', 'reviewed_independent_method_peer.json', 'reviewed_ROOT_prospective_method.json', 'reviewed_preparation_metadata_QA.json', 'E11_completed_ROOT_saved_record_review003.json', 'E11_checker003_independent_delta.json', 'E11_failed_V1_ROOT_freeze.json', 'history_roles_and_nonpromotion.json', 'protocol.json', 'run_started.json', 'interpreter.json', 'loaded_module_origins.json', 'admission_scope_graph.json', 'active_owner_full_map_bindings_and_inventories.json', 'equal_SHA_archived_source_routes.json', 'selected_artifact_literal_adapters.json', 'B4_original_sampler_binding.json', 'B8_original_sampler_binding.json', 'upstream_ideal_gaussian_coordinate_authority.json', 'primary_native_arithmetic_components.json', 'independent_native_arithmetic_components.json', 'primary_native_coordinate_squared_L2_bound.json', 'independent_native_coordinate_squared_L2_bound.json', 'independent_primary_bound_proof_check.json', 'shared_pair_scope_without_independence.json', 'four_precise_negative_diagnostic_controls.json', 'qualification_and_remaining_gaps.json', 'fresh_full_input_union_before_assembly.json', 'fresh_full_input_union_after_assembly.json', 'summary.json', 'completion_outcome.json', 'manifest.json', 'original_manifest_A01_run011.json', 'original_manifest_A02_BM_native_financial_bridge_audit_run002.json', 'original_manifest_A02_BM_native_financial_bridge_root_verification_run001.json', 'original_manifest_A02_BM_native_financial_bridge_run002.json', 'original_manifest_A10_coefficient_run001.json', 'original_manifest_C06_pair_audit_run001.json', 'original_manifest_C06_pair_run001.json', 'original_manifest_E11_scalar_midpoint_L2_numerical_run002.json']
REQUIRED_COMPONENTS = ['original_log_table_literal_and_native_Horner_floors', 'original_fixed_ln2_literal_and_all33_exponents', 'original_unclipped_minus2_nooverflow_and_unsigned46bit_isqrt_domain', 'original_sqrt_floor', 'all512_original_cosine_literals_and_native_Horner_floors', 'original_signed144product_stored72_and_product_floor']
SCIENTIFIC_SCOPE = {'source_law': 'original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'native_components': ['original_log_table_literal_and_native_Horner_floors', 'original_fixed_ln2_literal_and_all33_exponents', 'original_unclipped_minus2_nooverflow_and_unsigned46bit_isqrt_domain', 'original_sqrt_floor', 'all512_original_cosine_literals_and_native_Horner_floors', 'original_signed144product_stored72_and_product_floor'], 'quantity': 'squared_L2_Gaussian_coordinate', 'units': 'dimensionless_Gaussian_coordinate_squared', 'digital_pair_independence': False}
CURRENT_REVIEW_PATHS = ['.context/E11_NATIVE_COORDINATE_SQUARED_L2_INDEPENDENT_STATIC_PEER_next_run001.json', '.context/E11_NATIVE_COORDINATE_SQUARED_L2_ROOT_STATIC_REVIEW_run001.json']
AUTHOR_QA_KEY = '.context/E11_NATIVE_COORDINATE_SQUARED_L2_AUTHOR_STATIC_QA_run001.json'
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


def new_native_admission(ready_sha):
    global _FULL_ADMISSION
    require(sys.get_int_max_str_digits() == 4300 and "PYTHONINTMAXSTRDIGITS" not in os.environ
            and "int_max_str_digits" not in sys._xoptions, "Original startup decimal policy unchanged")
    ready = bootstrap_json(READY, ready_sha)
    require(ready["schema"] == "root-e11-native-coordinate-squared-L2-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True
            and ready["native_coordinate_rational_assembly_authorized"] is True
            and ready["output"] == OUTPUT.relative_to(ROOT).as_posix(), "One separate native-coordinate-only release")
    require(sys.orig_argv[1:] == ["-I", "-S", "-B", str(AUTHOR), "--ready-sha256", ready_sha],
            "Exact original isolated direct-script invocation and declared current source")
    authors = ready["author_method_SHA256"]
    require(type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
            "Exactly three current frozen authors")
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = bootstrap_json(PREFLIGHT, authors[PREFLIGHT.name])
    require(policy["schema"] == "e11-native-coordinate-squared-L2-preflight-v1"
            and policy["author_SHA256"] == authors[AUTHOR.name]
            and policy["method_SHA256"] == authors[METHOD_DOC.name]
            and all(policy[k] == ready[k] == value for k, value in COMMON_EXPECTATIONS.items()),
            "Complete current scope/cap/method/role graph exact, no old READY permission clone")
    for key, value in flags().items():
        require(policy[key] == ready[key] == value, "Only current native-coordinate flags govern current release")
    code_cache_policy(ready)
    original_e11 = bootstrap_json(ROOT / E11_MANIFEST_KEY, E11_MANIFEST_SHA)
    runtime = known_runtime_admission(original_e11)
    serialization_runtime_admission()
    source_code_guard()
    strict_loaded_origins()
    fixed_integer_policy()
    for key, pin in AUTHOR_INPUTS.items():
        bind(ROOT / key, pin)
    for key, pin in ready["static_review_expected_SHA256"].items():
        require(key.startswith(".context/") and ".." not in Path(key).parts, "Separate current reviews only")
        review = read(bind(ROOT / key, pin))
        require(review["passed"] is True and review.get("blockers", []) == []
                and review["author_method_SHA256"] == authors, "Every externally frozen current review passed for exact current trio")
    require(type(ready["static_review_expected_SHA256"]) is dict
            and set(ready["static_review_expected_SHA256"]) == set(CURRENT_REVIEW_PATHS), "Exactly separate current peer and ROOT reviews")
    require(ready["author_static_QA_path"] == AUTHOR_QA_KEY, "Fixed separate current author QA path")
    author_qa = read(bind(ROOT / AUTHOR_QA_KEY, ready["author_static_QA_SHA256"]))
    require(author_qa["passed"] is True and author_qa["author_method_SHA256"] == authors
            and author_qa["target_imported_or_executed"] is False
            and author_qa["scientific_evaluation_performed"] is False,
            "Exact author-only static QA, no scientific approval transfer")
    supplemental_reviews = ready["radicand_supplement_review_expected_SHA256"]
    require(supplemental_reviews == RADICAND_REVIEW_PINS,
            "Distinct ROOT and independent frozen symbolic supplemental reviews")
    for key, pin in supplemental_reviews.items():
        require(key.startswith(".context/") and ".." not in Path(key).parts, "Supplement reviewers are local fixed authority")
        review = read(bind(ROOT / key, pin))
        require(review["passed"] is True and review.get("blockers", []) == [], "Original-radicand symbolic reviews passed")
    gap, preparation = read(ROOT / GAP_KEY), read(ROOT / PREPARATION_KEY)
    require(preparation["active_owner_names"] == ACTIVE_OWNERS and preparation["archive_only_names"] == ARCHIVE_CITATIONS
            and preparation["prospective_exact_manifest_inclusive_output_ledger"] == PLANNED_FILES,
            "Frozen active8/archive4 and47 ledger, no scope expansion")
    require(preparation["three_original_archived_equal_SHA_routes_unchanged"]
            == gap["native_premises_scoped"]["native_root_realization_scope"]["prior_proof_source_archived_equal_SHA_routes"],
            "All three immutable archive identities retain original owner/key/pin")
    active = {}
    for name in ACTIVE_OWNERS:
        active[name] = full_active_owner(name, gap["cited_complete_original_packet_snapshots"][name],
                                        preparation["three_original_archived_equal_SHA_routes_unchanged"])
    original_completed_ready = read(bind(ROOT / COMPLETED_E11_READY_KEY, COMPLETED_E11_READY_SHA))
    completed_partition = {"existing_expected_SHA256": original_completed_ready["existing_new_code_cache_SHA256"],
                           "absent_paths": original_completed_ready["absent_new_code_cache_paths"]}
    require(completed_partition == COMPLETED_E11_CACHE_PARTITION
            == ready["completed_E11_V2_historical_cache_partition"], "Completed E11V2 original archive-only cache authority")
    historical_code_cache_partition(RESEARCH / "experiment_e11_scalar_midpoint_l2_v2.py", completed_partition)
    retain_failed_e11_v1()
    strict_loaded_origins()
    _FULL_ADMISSION = True
    return ready, policy, gap, preparation, active, runtime


def fresh_native_union():
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical, fresh=True) == actual, "Every lexical input remains freshly confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == pin, "Whole role union uses equal original expected SHA")
            union[path] = pin
    for path, pin in _OBSERVED.items():
        require(path not in union or union[path] == pin, "Observation never replaces expected authority")
        union[path] = pin
    require(len(union) <= MAX_REFERENCES, "Finite complete role union")
    size = 0
    for path, pin in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES and digest(actual, fresh=True, already_resolved=True) == pin,
                "Complete uncached physical/full-SHA union")
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, "Every admitted original owned inventory remains complete")
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS, "Complete original current stdlib membership unchanged")
    require(not any(p.exists() or p.is_symlink() for p in _ABSENT_RUNTIME), "All explicitly declared absences retained")
    for path, pin in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == pin, "Every externally declared present cache unchanged")
    strict_loaded_origins()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_physical_resolve_and_SHA": True,
            "active_owners": ACTIVE_OWNERS, "archive_only_citations_not_owner_success_closure": ARCHIVE_CITATIONS,
            "absent_runtime_paths": sorted(str(p) for p in _ABSENT_RUNTIME),
            "original_owner_inventories": {str(p): sorted(str(q) for q in members) for p, members in _OWN_INVENTORIES.items()}}


class E11NativeBridgeReject(ValueError):
    pass


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


def native_scope_validator(scope):
    if scope["source_law"] != "original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72":
        raise E11NativeBridgeReject("ORIGINAL_Q32_PAIRED_BM_SOURCE_REQUIRED")
    if set(scope["native_components"]) != set(REQUIRED_COMPONENTS):
        raise E11NativeBridgeReject("NATIVE_ARITHMETIC_LEDGER_REQUIRED")
    if scope["quantity"] != "squared_L2_Gaussian_coordinate" or scope["units"] != "dimensionless_Gaussian_coordinate_squared":
        raise E11NativeBridgeReject("SQUARED_GAUSSIAN_COORDINATE_L2_SCOPE_REQUIRED")
    if scope["digital_pair_independence"] is not False:
        raise E11NativeBridgeReject("DIGITAL_PAIR_INDEPENDENCE_UNPROVED")
    return True


def literal_numeric_inputs(preparation, gap):
    adapters = preparation["literal_envelope_and_ln2_adapters_uncombined"]
    fresh = {}
    for name, adapter in adapters.items():
        budget()
        raw = read(bind(ROOT / adapter["path"], adapter["literal_expected_SHA256"]))
        value = raw
        for key in adapter["JSON_pointer_components"]:
            value = value[key]
        require(value == adapter["saved_literal_uncombined"], "Exact saved literal adapter value, no observed refresh")
        fresh[name] = value
        if name in ("primary_ln2_window", "independent_ln2_window"):
            terms = 256 if name == "primary_ln2_window" else 1024
            require(raw["endpoints"][2]["argument_exact"] == [2, 1]
                    and raw["endpoints"][2]["fixed_terms"] == terms
                    and raw["endpoints"][2]["terms_executed"] == terms
                    and raw["endpoints"][2]["precision_passed"] is True,
                    "Original ln2 endpoint identity and fixed saved terms; no new series")
    nooverflow = read(bind(ROOT / NOOVERFLOW_KEY, NOOVERFLOW_SHA))
    require(nooverflow["passed"] is True and nooverflow["all_2pow32_midpoints_covered_analytically"] is True
            and nooverflow["negative_signed_integer_ln2_products_exact"] is True
            and nooverflow["all_table_centers_and_addresses_exact"] is True
            and nooverflow["quarter_turn_and_wrap_exact"] is True, "All-word original exact fixed arithmetic safety")
    primary_cos = read(ROOT / adapters["primary90_cosine_total"]["path"])
    require(primary_cos["all_product144_and_stored72_guards_passed"] is True
            and primary_cos["all_actual_coefficients_paid_without_half_ULP_assumption"] is True,
            "Original actual cosine literals and product144/stored72 guards")
    root = gap["native_premises_scoped"]["native_root_realization_scope"]
    require(root["prior_universal_induction"]["passed"] is True
            and root["prior_actual_gate_structure"]["passed"] is True
            and root["source_array_identity_not_fixture_inference"] is True,
            "Original unsigned isqrt guard/descriptor/universal semantics, no new array replay")
    for row in root["actual_descriptors"].values():
        descriptor = read(bind(ROOT / row["path"], ROOT_DESCRIPTOR_SHA))
        require(descriptor["spec"] == row["spec"] and row["spec"]["active_input_bits"] == 46
                and row["spec"]["width"] == 72 and row["spec"]["fraction_bits"] == 40
                and row["spec"]["input_contract"]["unsigned_input_bits"] == 46,
                "Exact original46-bit unsigned domain descriptor, separate from radicand positivity")
    upstream = read(bind(ROOT / UPSTREAM_COORDINATE_KEY, UPSTREAM_COORDINATE_SHA))
    require(upstream["all_continuous_bins_and_integrable_first_tail_included"] is True
            and upstream["formula"]["production_midpoint_bits"] == 32
            and upstream["formula"]["source_variables"] == "Independent U,V uniform on open(0,1); own floor-cell midpoints under same coupling"
            and upstream["financial_L2_source_transfer"] is False
            and upstream["compiled_native_same_law_policy_or_financial_bridge_claimed"] is False,
            "Upstream direct radial/angular ideal Gaussian lemma only; no inverse f or old native/financial join")
    return fresh


def original_sampler_bindings(gap):
    actual = read(bind(ROOT / SOURCE_BINDING_KEY, SOURCE_BINDING_SHA))
    require(actual["native_root_prior"] == gap["native_premises_scoped"]["native_root_realization_scope"],
            "Exact frozen original root provenance adapter")
    bindings = {}
    for name, expected_pairs, target_key, target_pin in ORIGINAL_CASES:
        target = read(bind(ROOT / target_key, target_pin))
        case = actual["cases"][name]
        require(case == gap["original_source_sampler_roles_and_all_pairs"][name],
                "Complete original saved source-case/raw-uniform/cosine/normal/root metadata, never new emission")
        scopes = case["joint_pair_scopes"]
        require(len(scopes) == expected_pairs
                and all(s["original_shared_pair_preserved"] is True and len(s["normal_values"]) == 2
                        and len(s["raw_uniform_values"]) == 2 and len(s["cosines"]) == 2 for s in scopes),
                "Every original pair and both original argument slots bound, no independence claim")
        bindings[name] = {"original_target_expected_SHA256": target_pin, "original_target_path": target_key,
                          "complete_original_saved_source_case": case,
                          "all_original_joint_pair_scopes": scopes, "pair_count": expected_pairs,
                          "normal_argument_slots": 2 * expected_pairs, "original_source_call_count": case["source_call_count"],
                          "original_actual_root_descriptor": case["actual_root_descriptor"],
                          "same_U_V_original_source_scope": True, "digital_pair_independence": False,
                          "native_path_policy_financial_output_join": False,
                          "target_read_as_original_raw_JSON_no_evaluation_or_emission": True}
    return bindings


def primary_arithmetic_components(inputs):
    """Primary exact rational assembly; no transcendental calls or new series."""
    log_error = checked_ratio(inputs["primary90_log_total"])
    cos_error = checked_ratio(inputs["primary90_cosine_total"])
    lo, hi = (checked_ratio(p) for p in inputs["primary_ln2_window"])
    require(0 < lo <= hi and log_error >= 0 and cos_error >= 0, "Certified positive ordered primary inputs")
    native_ln2 = Fraction(762123384786, 1 << 40)
    literal_error = max(abs(plus(native_ln2, -lo)), abs(plus(native_ln2, -hi)))
    logarithm = plus(log_error, times(Fraction(33), rational_guard(literal_error)))
    tau, delta = Fraction(1, 1 << 40), Fraction(1, 1 << 32)
    root_squared = plus(times(Fraction(4), logarithm), times(Fraction(2), times(tau, tau)))
    return {"log_table": log_error, "cosine_table": cos_error, "ln2_lower": lo, "ln2_upper": hi,
            "native_ln2": native_ln2, "native_ln2_literal_error": rational_guard(literal_error),
            "epsilon_l": logarithm, "radius_squared_error": root_squared, "tau": tau, "delta": delta}


def original_radicand_guard_once(primary):
    """One exact comparison of the already assembled primary allowance."""
    half_delta = Fraction(1, 1 << 33)
    require(primary["epsilon_l"] < half_delta,
            "Original native ell_d<0 guard failed: stop, no new clipping or precision adaptation")
    return {"epsilon_l_exact": pair_literal(primary["epsilon_l"]), "delta_half_exact": pair_literal(half_delta),
            "strict_guard_passed": True, "guard_comparisons_executed": 1,
            "proof": "-ln(U_M)>=1-U_M>=delta/2; ell_d<=ln(U_M)+epsilon_l<0",
            "native_source_clipping_inserted": False,
            "original_exact_minus2_and_unsigned_root_storage_guards_required_separately": True}


def primary_coordinate_bound(c):
    tau_squared = times(c["tau"], c["tau"])
    one_plus_cos = plus(Fraction(1), c["cosine_table"])
    first = times(times(one_plus_cos, one_plus_cos), c["radius_squared_error"])
    second = times(Fraction(2), times(c["cosine_table"], c["cosine_table"]))
    arithmetic = times(Fraction(3), plus(plus(first, second), tau_squared))
    midpoint_radial = times(times(Fraction(4 * 33), c["delta"]), c["ln2_upper"])
    midpoint_angular = times(times(Fraction(4), times(Fraction(22, 7), Fraction(22, 7))), times(c["delta"], c["delta"]))
    midpoint = plus(midpoint_radial, midpoint_angular)
    coordinate = times(Fraction(2), plus(midpoint, arithmetic))
    return {"existing_primary_stage_ledger": {"first_radius_term": pair_literal(first), "second_cosine_term": pair_literal(second),
            "native_floor_squared": pair_literal(tau_squared), "midpoint_radial": pair_literal(midpoint_radial),
            "midpoint_angular": pair_literal(midpoint_angular)},
            "arithmetic_squared_L2_upper": pair_literal(arithmetic), "ideal_midpoint_coordinate_squared_L2_upper": pair_literal(midpoint),
            "continuous_to_original_native_coordinate_squared_L2_upper": pair_literal(coordinate),
            "shared_pair_Euclidean_squared_L2_upper_without_independence": pair_literal(times(Fraction(2), coordinate)),
            "units": "dimensionless_Gaussian_coordinate_squared", "norm_squared_not_norm_twice": True}


def independent_arithmetic_components(inputs):
    """Own audited saved inputs, own expression order; no primary function call."""
    ell_table = checked_ratio(inputs["independently_audited_log_total"])
    ec = checked_ratio(inputs["independent130_cosine_total"])
    bounds = [checked_ratio(p) for p in inputs["independent_ln2_window"]]
    require(bounds[0] > 0 and bounds[1] >= bounds[0] and ell_table >= 0 and ec >= 0,
            "Independent certified rational input ordering")
    native = Fraction(762123384786, 1099511627776)
    distances = [rational_guard(abs(plus(bounds[0], -native))), rational_guard(abs(plus(bounds[1], -native)))]
    literal_distance = max(distances)
    ell = plus(times(literal_distance, Fraction(33)), ell_table)
    unit = Fraction(1, 1099511627776)
    radius = plus(times(times(unit, unit), Fraction(2)), times(ell, Fraction(4)))
    return {"log_table": ell_table, "cosine_table": ec, "ln2_lower": bounds[0], "ln2_upper": bounds[1],
            "native_ln2": native, "native_ln2_literal_error": literal_distance, "epsilon_l": ell,
            "radius_squared_error": radius, "tau": unit, "delta": Fraction(1, 4294967296)}


def independent_coordinate_bound(c):
    """Algebraically expanded equivalent ledger; no primary evaluator call."""
    ec = c["cosine_table"]
    ec2 = times(ec, ec)
    one_plus_squared = plus(plus(Fraction(1), times(Fraction(2), ec)), ec2)
    radius_term = times(times(Fraction(3), one_plus_squared), c["radius_squared_error"])
    cosine_term = times(Fraction(6), ec2)
    floor_term = times(Fraction(3), times(c["tau"], c["tau"]))
    arithmetic = plus(plus(radius_term, cosine_term), floor_term)
    radial = times(times(c["ln2_upper"], c["delta"]), Fraction(132))
    angular = times(times(c["delta"], c["delta"]), Fraction(1936, 49))
    ideal = plus(radial, angular)
    bound = plus(times(Fraction(2), ideal), times(Fraction(2), arithmetic))
    return {"arithmetic_squared_L2_upper": pair_literal(arithmetic), "ideal_midpoint_coordinate_squared_L2_upper": pair_literal(ideal),
            "continuous_to_original_native_coordinate_squared_L2_upper": pair_literal(bound),
            "shared_pair_Euclidean_squared_L2_upper_without_independence": pair_literal(plus(bound, bound)),
            "units": "dimensionless_Gaussian_coordinate_squared", "norm_squared_not_norm_twice": True}


def encoded_components(c, guard=None):
    return {"exact_component_allowances": {k: pair_literal(v) for k, v in c.items()},
            "original_native_radicand_domain_guard": guard,
            "root_Holder_and_native_floor_charged": True, "all_low_native_product_floor_charged": True,
            "original_unsigned_isqrt_storage_and_product144_nooverflow_required": True,
            "no_new_transcendental_series_or_native_evaluation": True}


def independently_reconcile_primary(inputs, primary_components, primary_result, guard):
    """Identity checks on existing records within profile2; no third envelope/precision/guard comparison."""
    c, result = primary_components, primary_result
    lower, upper = [checked_ratio(p) for p in inputs["primary_ln2_window"]]
    require(c["log_table"] == checked_ratio(inputs["primary90_log_total"])
            and c["cosine_table"] == checked_ratio(inputs["primary90_cosine_total"])
            and c["ln2_lower"] == lower and c["ln2_upper"] == upper
            and c["native_ln2"] == Fraction(762123384786, 1099511627776)
            and c["tau"] == Fraction(1, 1099511627776) and c["delta"] == Fraction(1, 4294967296),
            "Existing primary component identities equal original raw literal adapters")
    distance = max(rational_guard(abs(plus(lower, -c["native_ln2"]))), rational_guard(abs(plus(upper, -c["native_ln2"]))))
    require(c["native_ln2_literal_error"] == distance
            and c["epsilon_l"] == plus(times(distance, Fraction(33)), c["log_table"])
            and c["radius_squared_error"] == plus(times(times(c["tau"], c["tau"]), Fraction(2)), times(c["epsilon_l"], Fraction(4))),
            "Existing primary ln2/log/root ledger identities checked, no new bound candidate")
    stages = {k: checked_ratio(v) for k, v in result["existing_primary_stage_ledger"].items()}
    ec_squared = times(c["cosine_table"], c["cosine_table"])
    require(stages["first_radius_term"] == times(plus(plus(Fraction(1), times(c["cosine_table"], Fraction(2))), ec_squared), c["radius_squared_error"])
            and stages["second_cosine_term"] == times(ec_squared, Fraction(2))
            and stages["native_floor_squared"] == times(c["tau"], c["tau"])
            and stages["midpoint_radial"] == times(times(c["ln2_upper"], c["delta"]), Fraction(132))
            and stages["midpoint_angular"] == times(times(c["delta"], c["delta"]), Fraction(1936, 49)),
            "Existing primary terms equal distinct expanded algebra identities")
    claimed_arithmetic = checked_ratio(result["arithmetic_squared_L2_upper"])
    claimed_midpoint = checked_ratio(result["ideal_midpoint_coordinate_squared_L2_upper"])
    claimed_coordinate = checked_ratio(result["continuous_to_original_native_coordinate_squared_L2_upper"])
    require(claimed_arithmetic == plus(plus(times(stages["first_radius_term"], Fraction(3)), times(stages["second_cosine_term"], Fraction(3))), times(stages["native_floor_squared"], Fraction(3)))
            and claimed_midpoint == plus(stages["midpoint_angular"], stages["midpoint_radial"])
            and claimed_coordinate == plus(times(claimed_arithmetic, Fraction(2)), times(claimed_midpoint, Fraction(2)))
            and checked_ratio(result["shared_pair_Euclidean_squared_L2_upper_without_independence"]) == plus(claimed_coordinate, claimed_coordinate),
            "Existing primary sum/factor identities verified; no returned third bound")
    require(guard["strict_guard_passed"] is True and guard["guard_comparisons_executed"] == 1
            and guard["epsilon_l_exact"] == pair_literal(primary_components["epsilon_l"])
            and guard["delta_half_exact"] == [1, 1 << 33]
            and guard["native_source_clipping_inserted"] is False,
            "Reconcile the sole already performed exact native-domain guard, without another comparison")
    return {"passed": True, "primary_exact_expression_reconstructed_by_distinct_expanded_method": True,
            "exact_numerical_envelope_assemblies": 2, "new_envelope_or_candidate_returned": False,
            "different_outward_primary_independent_envelopes_not_required_equal_or_nested": True,
            "original_positive_native_domain_established_by_one_primary_comparison": guard,
            "own_independent130_components_and_bound_saved_separately": True,
            "continuous_and_all_Q32_source_proofs_are_external_byte_pinned_prerequisites": True}


def four_exact_diagnostic_controls():
    records = []
    changes = [("source_law", "alternate_quantile_loader", "ORIGINAL_Q32_PAIRED_BM_SOURCE_REQUIRED"),
               ("native_components", REQUIRED_COMPONENTS[1:], "NATIVE_ARITHMETIC_LEDGER_REQUIRED"),
               ("quantity", "price_L1", "SQUARED_GAUSSIAN_COORDINATE_L2_SCOPE_REQUIRED"),
               ("digital_pair_independence", True, "DIGITAL_PAIR_INDEPENDENCE_UNPROVED")]
    for key, bad_value, code in changes:
        budget()
        corrupted = dict(SCIENTIFIC_SCOPE)
        corrupted[key] = bad_value
        try:
            native_scope_validator(corrupted)
        except E11NativeBridgeReject as error:
            require(str(error) == code, "Only exact dedicated scope rejection earns control pass")
            records.append({"mutated_field": key, "dedicated_rejection": code, "expected_rejected": True})
        else:
            raise ValueError("Fixed malformed scope unexpectedly accepted")
    require(len(records) == 4, "Exactly four fixed scope diagnostics, zero new fixtures")
    return {"passed": True, "controls": records, "numeric_fixtures": 0, "fixture_credit": 0}


def theorem_record():
    return {"scope": SCIENTIFIC_SCOPE, "original_U_V_uniform_cell_coupling": True,
            "upstream_Z_radial_angular_all_tail_proof_not_inverse_f_Lipschitz": True,
            "continuous_first_bin_integrable_tail_included": True,
            "shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound": True,
            "E_R_midpoint_squared_upper": [2, 1], "Jensen_convex_negative_log_midpoint_to_cell_integral": True,
            "native_radius_squared_error_formula": "4epsilon_l+2tau^2; Holder plus exact unsigned sqrt floor",
            "native_product_error_split": "(r_d-R_M)c_d+R_M(c_d-c)+signed_product_floor",
            "arithmetic_squared_bound": "3[(1+ec)^2(4el+2tau^2)+2ec^2+tau^2]",
            "midpoint_coordinate_squared_bound": "4delta*33ln2+4(22/7)^2delta^2",
            "coordinate_total_squared_bound": "2*(midpoint_squared+native_arithmetic_squared)",
            "two_coordinate_Euclidean_squared_bound_by_sum_not_independence": True,
            "native_positive_radicand_guard_is_required_before_any_bridge_certificate": True,
            "no_financial_path_policy_or_C4_H8_output_join": True}


def flags():
    return {"item": "E11", "native_Gaussian_coordinate_squared_L2_only": True,
            "full_E11_completed": False, "native_financial_path_or_policy_L2_verified": False,
            "full_price_certificate": False, "G2_transfer": False, "adoption": False,
            "cost_comparison": False, "quantum_advantage": False, "physical_certificate": False,
            "estimator_schedule_emitted": False, "source_emission": False, "gate_emission": False,
            "prices_or_paths_sampled": False, "fits_or_pilots": False, "new_transcendental_series": False,
            "native_arrays_generated_or_replayed": False, "old_numerical_helpers_or_evaluators_called": False,
            "digital_pair_independence": False, "native_source_clipping_inserted": False,
            "fixture_credit": 0, "new_global_fixture_credit": 0, "local_only": True}


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    invocation_check()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists() and not OUTPUT.is_symlink(),
            "One exclusive new native-coordinate output route")
    try:
        ready, policy, gap, preparation, owners, runtime = new_native_admission(args.ready_sha256)
        first = fresh_native_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        copies = {
            "executed_" + AUTHOR.name: AUTHOR, "executed_" + METHOD_DOC.name: METHOD_DOC,
            "executed_" + PREFLIGHT.name: PREFLIGHT, "executed_" + READY.name: READY,
            "reviewed_gap_map_method.md": ROOT / GAP_MD_KEY, "reviewed_gap_map_method.json": ROOT / GAP_KEY,
            "reviewed_provenance_retention_preparation.md": ROOT / PREPARATION_MD_KEY,
            "reviewed_provenance_retention_preparation.json": ROOT / PREPARATION_KEY,
            "reviewed_independent_method_peer.json": ROOT / METHOD_PEER_KEY,
            "reviewed_ROOT_prospective_method.json": ROOT / METHOD_ROOT_KEY,
            "reviewed_preparation_metadata_QA.json": ROOT / PREPARATION_QA_KEY,
            "E11_completed_ROOT_saved_record_review003.json": ROOT / E11_ROOT003_KEY,
            "E11_checker003_independent_delta.json": ROOT / E11_CHECKER003_PEER_KEY,
            "E11_failed_V1_ROOT_freeze.json": ROOT / FAILED_E11_V1_HISTORY["ROOT_freeze_path"],
        }
        for name in ACTIVE_OWNERS:
            copies["original_manifest_" + name + ".json"] = ROOT / gap["cited_complete_original_packet_snapshots"][name]["manifest_path"]
        for name, path in copies.items():
            copy(path, name)
        save("history_roles_and_nonpromotion.json", {"active8": ACTIVE_OWNERS, "archive4": ARCHIVE_CITATIONS,
            "failed_E11_V1_opaque_history": FAILED_E11_V1_HISTORY, "E11_checker003_saved_record_only_no_SCI_rerun": True,
            "all12_full_original_snapshot_authority": {"path": GAP_KEY, "SHA256": AUTHOR_INPUTS[GAP_KEY]},
            "completed_E11_V2_original_cache_partition": COMPLETED_E11_CACHE_PARTITION,
            "radicand_method_supplement_external_input_pins": RADICAND_REVIEW_PINS,
            "old_checker002_metadata_failure_is_not_a_completed_receipt": True,
            "citation_history_not_native_numeric_or_recursive_runtime_success": True})
        save("protocol.json", policy)
        save("run_started.json", {"created_UTC": time.time_ns(), "PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        save("interpreter.json", runtime)
        save("loaded_module_origins.json", {"fresh_known_only_present_origins": True, "upfront_serializer": SERIALIZATION_RUNTIME,
            "current_author_external_cache_partition": {"present": ready["existing_new_code_cache_SHA256"], "absent": ready["absent_new_code_cache_paths"]}})
        save("admission_scope_graph.json", preparation["owner_role_graph"])
        save("active_owner_full_map_bindings_and_inventories.json", owners)
        save("equal_SHA_archived_source_routes.json", preparation["three_original_archived_equal_SHA_routes_unchanged"])
        save("selected_artifact_literal_adapters.json", preparation["literal_envelope_and_ln2_adapters_uncombined"])
        save("fresh_full_input_union_before_assembly.json", first)
        inputs = literal_numeric_inputs(preparation, gap)
        binding = original_sampler_bindings(gap)
        save("B4_original_sampler_binding.json", binding["B4x12"])
        save("B8_original_sampler_binding.json", binding["B8x52"])
        native_scope_validator(SCIENTIFIC_SCOPE)
        save("upstream_ideal_gaussian_coordinate_authority.json", theorem_record())
        primary = primary_arithmetic_components(inputs)
        guard = original_radicand_guard_once(primary)
        primary_bound = primary_coordinate_bound(primary)
        save("primary_native_arithmetic_components.json", encoded_components(primary, guard))
        save("primary_native_coordinate_squared_L2_bound.json", primary_bound)
        independent = independent_arithmetic_components(inputs)
        independent_bound = independent_coordinate_bound(independent)
        save("independent_native_arithmetic_components.json", encoded_components(independent))
        save("independent_native_coordinate_squared_L2_bound.json", independent_bound)
        comparison = independently_reconcile_primary(inputs, primary, primary_bound, guard)
        save("independent_primary_bound_proof_check.json", comparison)
        save("shared_pair_scope_without_independence.json", {"all_shared_pairs": 264, "all_argument_slots": 528,
            "primary_pair_squared_bound": primary_bound["shared_pair_Euclidean_squared_L2_upper_without_independence"],
            "independent_pair_squared_bound": independent_bound["shared_pair_Euclidean_squared_L2_upper_without_independence"],
            "pair_bound_is_sum_of_coordinate_squared_errors": True, "digital_pair_independence": False})
        controls = four_exact_diagnostic_controls()
        save("four_precise_negative_diagnostic_controls.json", controls)
        qualification = {"original_native_Gaussian_coordinate_same_law_bound_assembled": True,
            "original_native_radicand_guard": guard, "independent_arithmetic_proof_check_passed": comparison["passed"],
            "native_path_policy_payoff_residual_second_moment_and_G2_still_open": True,
            "E10_C4_H8_source_model_policy_join_still_open": True,
            "financial_expectation_bias_is_not_strong_same_UV_L1_or_L2": True, **flags()}
        save("qualification_and_remaining_gaps.json", qualification)
        second = fresh_native_union()
        save("fresh_full_input_union_after_assembly.json", second)
        summary = {"schema": "e11-native-coordinate-squared-L2-summary-v1", "passed": True, "completed": True,
            "exact_numerical_envelope_assemblies": 2, "primary_guard_comparisons": 1,
            "budget_censored": False, "primary_bound": primary_bound, "independent_bound": independent_bound,
            "primary_native_radicand_guard": guard, "independent_primary_expression_reconciled": comparison["passed"],
            "exact_four_diagnostic_controls": controls, "all_original_pairs_arguments_bound": [264, 528],
            "both_complete_fresh_input_unions": [first, second], "planned_manifest_inclusive_owned_files": 47,
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], "current_runtime": runtime,
            "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        members = inventory(OUTPUT)
        require({p.name for p in members} == set(PLANNED_FILES) - {"manifest.json"}, "Exactly fixed47 output ledger before seal")
        files, total = {}, 0
        for path in sorted(members):
            budget()
            total += path.stat().st_size
            require(total <= MAX_OWN_BYTES and len(files) < MAX_OWN_FILES - 1, "Manifest-inclusive retention reserve")
            files[path.name] = digest(path, fresh=True)
        complete_manifest({"schema": "e11-native-coordinate-squared-L2-manifest-v1", "files": files,
            "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL, "manifest_self_hash_excluded": True,
            "completed": True, "passed": True, "budget_censored": False, "both_complete_fresh_input_unions": [first, second],
            "terminal_budget_observation": {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}, **flags()}, files, total)
        budget()
        print(json.dumps({"passed": True, "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True), **flags()}), flush=True)
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
