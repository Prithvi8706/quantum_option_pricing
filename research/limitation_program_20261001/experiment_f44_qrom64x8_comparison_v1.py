"""Unexecuted standalone F44 QROM64x8 comparison; external ROOT release required.

Exact retained StageC003 table, identical1301-wire clean dirty-XOR wrappers,
original minterm scan versus AST-derived shared-prefix traversal. No refit,
financial execution, gate credit, whole-caller cost transfer or source adoption.
"""

from __future__ import annotations
import argparse
from array import array
import ast
import ctypes
from ctypes import wintypes
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/limitation_program_20261001"
AUTHOR = HERE / "experiment_f44_qrom64x8_comparison_v1.py"
METHOD_MD = HERE / "F44_QROM64X8_COMPARISON_PREFLIGHT_V1.md"
METHOD_JSON = HERE / "f44_qrom64x8_comparison_preflight_v1.json"
READY = ROOT / ".context/F44_QROM64X8_COMPARISON_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/F44_QROM64X8_comparison_run001"
PRIMARY = ROOT / "results/limitation_program_20261001/A14_taylor_f44_stage_C_run003"
PRIMARY_MANIFEST = PRIMARY / "manifest.json"
PRIMARY_MANIFEST_SHA = "7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa"
PRIMARY_READY_KEY = ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json"
PRIMARY_READY_SHA = "b781c1c80bc2ee381c9e35b3b83f9c4cadd0fc141c2e88ab214b73f5de2c67c0"
BUILDER_KEY = "research/limitation_program_20261001/f44_cosine_stage_c_source.py"
BUILDER_SHA = "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"
SHARED_KEY = "research/controlled_source_completion/exact_lookup.py"
SHARED_SHA = "a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c"
SHARED_AST_SHA = "eaa7e9a6a9670be002eb5600b7a646d9308e287c5f886b89bb5a14e5c083dd45"
GATE_FRAGMENT_KEY = ".context/f44_stage_c_independent_gate_audit_author_fragment_v1.py"
GATE_FRAGMENT_SHA = "55851031aeb748ca8e802caf8c51d8f113b0ed3846bf8bd66deca75e705f34b1"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
CPU_LIMIT, WORK_LIMIT, WALL_LIMIT = 180, 150, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 4096, 512 << 20
MAX_FROZEN_FILES, MAX_FROZEN_BYTES = 16, 8 << 20
MAX_OWNED_FILES, MAX_OWNED_BYTES = 16, 16 << 20
MAX_SINGLE_BYTES, MAX_OWNED_SINGLE_BYTES = 128 << 20, 64 << 20
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 << 30, 24 << 30
MAX_LOOKUP_ROWS, LOOKUP_QUBITS, LOOKUP_BITS = 65536, 1301, 6
_ABSENT_CACHES, _CACHE_PRESENT = set(), {}
_ATTEMPT_ROUTE_OWNED = False
_PRIMARY_RUNTIME_EXPECTED, _PRIMARY_FROZEN_EXPECTED = {}, {}
_HASH_WORK = _REFERENCES = 0
_STARTED = None
SHA = re.compile("[0-9a-f]{64}\\Z")
_SCOPE = {
    "standalone_lookup_component_only": True,
    "immutable_table_no_refit": True,
    "standalone_lookup_native_emission_only": True,
    "program_fixture_credit": 0,
    "credited_gate_replays": 0,
    "financial_samples": 0,
    "financial_gate_emission": False,
    "financial_execution": False,
    "financial_adoption": False,
    "source_adoption": False,
    "G2_transfer": False,
    "whole_caller_cost_transfer": False,
    "quantum_advantage": False,
    "StageC_resource_REJECTED_unchanged": True,
}
PRIMARY_OWNED = {
    "actual_prototype_resources.json": "a06f70704e17a9068040b4ad432a9f5297ccdb86a6b8e82586cd4365f4957c52",
    "actual_structural_certificate.json": "7888c3d3336aef49365c38dc5c09a4b1a698a84693262b2531036dd103c5a0e6",
    "all64_native_certificate.json": "521555202d90879c1e70b8fae5a3ddb0c7f87e51394f1b37fb8b5c70187d59db",
    "completion_outcome.json": "e3b119ef5a3b14ee83fd1e28bb624749a6d2c9e5cad8727ce519e3300fff656d",
    "cosine.gates.bin": "a9145d3650a1dd5cb4682837e96f058af088e87c09e6a66c63c36ac728a6485a",
    "executed_A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b",
    "executed_A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json": "b781c1c80bc2ee381c9e35b3b83f9c4cadd0fc141c2e88ab214b73f5de2c67c0",
    "executed_A14_TAYLOR_F44_PROSPECTUS_V1.md": "e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04",
    "executed_F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141",
    "executed_a14_f44_cosine_stage_c_implementation_preflight_v3.json": "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41",
    "executed_a14_taylor_f44_prospectus_v1.json": "526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3",
    "executed_experiment_f44_cosine_stage_c_v3.py": "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6",
    "executed_f44_cosine_stage_c_source.py": "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74",
    "fixed_frontier_row.json": "22db25c5422e291ccfba6700ba965cc746d61a4e95811bb5a2835c58f2ba11a1",
    "fixed_native_diagnostics.json": "3c3185930f20ebd018231bf5fdfdc8513a9969eecae55488b7a8b205366358c2",
    "native_gate_array.json": "fe2b946766955b8e8c75d71d44a94f011d086c0e9f86f32fde37dcdd2544947b",
    "original_source_binding.json": "604d8c5682001d46047979f7b71c26c1614c385d983acc38b234edc752db9bfd",
    "primary90_literals.json": "9bfbeb64c13efe5268e610f9d6aac91f3a925bd3ab4d3a52522e9c75687fef04",
    "prior_A14_F44_COSINE_STAGE_C_ROOT_READY_run001.json": "2a6806788c576085aafd2ff3fed1a03908e33fcddffef8c1d5d2b1c866b047de",
    "prior_A14_F44_STAGE_C_FAILED_OWNED_FROZEN_run001.json": "60b2d2aa068169f19f72052738227588ea5ad2837498fbe0009db1d4a5c17c75",
    "prior_a14_f44_stage_c_run001.log": "da9d69f12a2cd1a8cef93ce0e112bf79410b659fad6289d8ae7b75bac14ada69",
    "prior_failed_owned_expected_map.json": "c7bf35ff427f10fd671d15eef680954c75d41d5402aeab10c60e255704d7cfab",
    "prior_prefit_A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V2.md": "f1cc8f98add202206d30cd082d75a2672039551124af4170d98402d47be9a1c0",
    "prior_prefit_A14_F44_COSINE_STAGE_C_ROOT_READY_run002.json": "b53f15f958c9da2b966c965a58bbbe0f4839a61c92ff4452b5ed759a608ee2bc",
    "prior_prefit_A14_F44_STAGE_C_V2_PREFIT_FAILURE_WITNESS_run002.json": "1de19d91d1359ffce383ffd917bc20f803c466d1b35a731c271f18a3b33b5be6",
    "prior_prefit_a14_f44_cosine_stage_c_implementation_preflight_v2.json": "40cd6de37e0aa811a8078be12f701d3df317a24732e2ef1ca276aa53beb14ecb",
    "prior_prefit_a14_f44_stage_c_run002.log": "a893e7feec700c44f5a686199dfd6ae3ad42687c29e7e11173bcd65e3821bad7",
    "prior_prefit_experiment_f44_cosine_stage_c_v2.py": "0a8e72bfa675b07ecaf948024d51ae5fb91381fd67fc0e9ec8d565635bcfff1c",
    "prototype_descriptor.json": "3b2bd96bf04650b9520c5f1f46c659bb84863221c60d2c62c0e0990da4c2e480",
    "run_started.json": "1b7ad7d5e0f24b953903640e375d02d924a986f114ffb7f5db41be85710fb41c",
    "serialization_edge_diagnostics.json": "b9311338ddcdccc419dcc6fe9b5a6ef19bc6bc636215b2dd238f89fd789e6360",
    "summary.json": "f0eae77f71203dda9cc2a4bc0db7e1e0b783e1c3c22cea9fc0eb9d978561fb0d",
    "uniform_certificate.json": "faf527954bb8c477e0c9078ac22543f2fe59845ecd70054137ce346615a736cc",
    "whole_source_resource_comparison.json": "c74e039293d6415a1c86f52bd8b3349b3f2d97fb0e062c11a6fb5a2bd46c7882",
}
POLICY_EXPECTED = {
    "schema": "f44-qrom64x8-comparison-preflight-v1",
    "author_status": "AUTHOR_ONLY_UNEXECUTED",
    "new_controller": "research/limitation_program_20261001/experiment_f44_qrom64x8_comparison_v1.py",
    "new_method": "research/limitation_program_20261001/F44_QROM64X8_COMPARISON_PREFLIGHT_V1.md",
    "new_policy": "research/limitation_program_20261001/f44_qrom64x8_comparison_preflight_v1.json",
    "new_output": "results/limitation_program_20261001/F44_QROM64X8_comparison_run001",
    "new_ROOT_READY": ".context/F44_QROM64X8_COMPARISON_ROOT_READY_run001.json",
    "primary_manifest_SHA256": "7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa",
    "primary_expected_counts": [34, 851, 2842],
    "primary_inclusive_owned_count": 35,
    "primary_owned_map": {
        "actual_prototype_resources.json": "a06f70704e17a9068040b4ad432a9f5297ccdb86a6b8e82586cd4365f4957c52",
        "actual_structural_certificate.json": "7888c3d3336aef49365c38dc5c09a4b1a698a84693262b2531036dd103c5a0e6",
        "all64_native_certificate.json": "521555202d90879c1e70b8fae5a3ddb0c7f87e51394f1b37fb8b5c70187d59db",
        "completion_outcome.json": "e3b119ef5a3b14ee83fd1e28bb624749a6d2c9e5cad8727ce519e3300fff656d",
        "cosine.gates.bin": "a9145d3650a1dd5cb4682837e96f058af088e87c09e6a66c63c36ac728a6485a",
        "executed_A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b",
        "executed_A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json": "b781c1c80bc2ee381c9e35b3b83f9c4cadd0fc141c2e88ab214b73f5de2c67c0",
        "executed_A14_TAYLOR_F44_PROSPECTUS_V1.md": "e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04",
        "executed_F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141",
        "executed_a14_f44_cosine_stage_c_implementation_preflight_v3.json": "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41",
        "executed_a14_taylor_f44_prospectus_v1.json": "526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3",
        "executed_experiment_f44_cosine_stage_c_v3.py": "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6",
        "executed_f44_cosine_stage_c_source.py": "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74",
        "fixed_frontier_row.json": "22db25c5422e291ccfba6700ba965cc746d61a4e95811bb5a2835c58f2ba11a1",
        "fixed_native_diagnostics.json": "3c3185930f20ebd018231bf5fdfdc8513a9969eecae55488b7a8b205366358c2",
        "native_gate_array.json": "fe2b946766955b8e8c75d71d44a94f011d086c0e9f86f32fde37dcdd2544947b",
        "original_source_binding.json": "604d8c5682001d46047979f7b71c26c1614c385d983acc38b234edc752db9bfd",
        "primary90_literals.json": "9bfbeb64c13efe5268e610f9d6aac91f3a925bd3ab4d3a52522e9c75687fef04",
        "prior_A14_F44_COSINE_STAGE_C_ROOT_READY_run001.json": "2a6806788c576085aafd2ff3fed1a03908e33fcddffef8c1d5d2b1c866b047de",
        "prior_A14_F44_STAGE_C_FAILED_OWNED_FROZEN_run001.json": "60b2d2aa068169f19f72052738227588ea5ad2837498fbe0009db1d4a5c17c75",
        "prior_a14_f44_stage_c_run001.log": "da9d69f12a2cd1a8cef93ce0e112bf79410b659fad6289d8ae7b75bac14ada69",
        "prior_failed_owned_expected_map.json": "c7bf35ff427f10fd671d15eef680954c75d41d5402aeab10c60e255704d7cfab",
        "prior_prefit_A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V2.md": "f1cc8f98add202206d30cd082d75a2672039551124af4170d98402d47be9a1c0",
        "prior_prefit_A14_F44_COSINE_STAGE_C_ROOT_READY_run002.json": "b53f15f958c9da2b966c965a58bbbe0f4839a61c92ff4452b5ed759a608ee2bc",
        "prior_prefit_A14_F44_STAGE_C_V2_PREFIT_FAILURE_WITNESS_run002.json": "1de19d91d1359ffce383ffd917bc20f803c466d1b35a731c271f18a3b33b5be6",
        "prior_prefit_a14_f44_cosine_stage_c_implementation_preflight_v2.json": "40cd6de37e0aa811a8078be12f701d3df317a24732e2ef1ca276aa53beb14ecb",
        "prior_prefit_a14_f44_stage_c_run002.log": "a893e7feec700c44f5a686199dfd6ae3ad42687c29e7e11173bcd65e3821bad7",
        "prior_prefit_experiment_f44_cosine_stage_c_v2.py": "0a8e72bfa675b07ecaf948024d51ae5fb91381fd67fc0e9ec8d565635bcfff1c",
        "prototype_descriptor.json": "3b2bd96bf04650b9520c5f1f46c659bb84863221c60d2c62c0e0990da4c2e480",
        "run_started.json": "1b7ad7d5e0f24b953903640e375d02d924a986f114ffb7f5db41be85710fb41c",
        "serialization_edge_diagnostics.json": "b9311338ddcdccc419dcc6fe9b5a6ef19bc6bc636215b2dd238f89fd789e6360",
        "summary.json": "f0eae77f71203dda9cc2a4bc0db7e1e0b783e1c3c22cea9fc0eb9d978561fb0d",
        "uniform_certificate.json": "faf527954bb8c477e0c9078ac22543f2fe59845ecd70054137ce346615a736cc",
        "whole_source_resource_comparison.json": "c74e039293d6415a1c86f52bd8b3349b3f2d97fb0e062c11a6fb5a2bd46c7882",
    },
    "source_pins": {
        "research/limitation_program_20261001/f44_cosine_stage_c_source.py": "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74",
        "research/controlled_source_completion/exact_lookup.py": "a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c",
        ".context/f44_stage_c_independent_gate_audit_author_fragment_v1.py": "55851031aeb748ca8e802caf8c51d8f113b0ed3846bf8bd66deca75e705f34b1",
    },
    "shared_AST_SHA256_pinned_Python3124": "eaa7e9a6a9670be002eb5600b7a646d9308e287c5f886b89bb5a14e5c083dd45",
    "limits_CPU_admission_wall": [180, 150, 600],
    "current_runtime_caps_files_bytes": [4096, 536870912],
    "new_release_caps_files_bytes": [16, 8388608],
    "owned_caps_files_bytes": [16, 16777216],
    "inherited_input_single_file_bytes": 134217728,
    "prospective_owned_single_file_bytes": 67108864,
    "inherited_caps_references_unique_bytes_hash_work": [100000, 8589934592, 25769803776],
    "fixed_algorithms": ["naive", "shared"],
    "retained_table_shape": [64, 8, 72],
    "retained_primary_digits": 90,
    "fixed_full_wire_count": 1301,
    "clean_private_address_output_count": 648,
    "clean_prefix_ancilla_count": 5,
    "algorithm_native_rows_cap": 65536,
    "replay_guard_rows": 128,
    "regular_cases_per_algorithm": 128,
    "high_address_cases_per_algorithm": 4,
    "high_address_witness_low6": [0, 63],
    "high_address_witness_bits": [6, 71],
    "high_address_witness_dirty_all8_words": "allones72",
    "logical_total_forward_inverse_calls": 528,
    "physical_total_bit_cohort_sweeps": 8,
    "physical_cohort_lanes": [128, 4],
    "prospective_complete_owned_count": 15,
    "prepare_scientific_emission_or_replay": False,
    "proof_scope": "Universal mod64 clean dirty-XOR standalone lookup identity; exact native absolute phase; no historical A15 proof transfer",
    "old_StageC_resource_status": "REJECTED",
    "scope": {
        "standalone_lookup_component_only": True,
        "immutable_table_no_refit": True,
        "standalone_lookup_native_emission_only": True,
        "program_fixture_credit": 0,
        "credited_gate_replays": 0,
        "financial_samples": 0,
        "financial_gate_emission": False,
        "financial_execution": False,
        "financial_adoption": False,
        "source_adoption": False,
        "G2_transfer": False,
        "whole_caller_cost_transfer": False,
        "quantum_advantage": False,
        "StageC_resource_REJECTED_unchanged": True,
    },
}


def budget():
    return guard(_STARTED, admission=True)


def merge_root_expected(target, source, started):
    for key in source:
        exact_relative_key(key)
    merge_expected(target, source, started)


def primary_inventory(started):
    require(PRIMARY.resolve(strict=True) == PRIMARY, "Exact immutable StageC003 receipt route")
    expected = {PRIMARY / name for name in PRIMARY_OWNED} | {PRIMARY_MANIFEST}
    actual = set(PRIMARY.iterdir())
    require(
        actual == expected and len(actual) == 35,
        "All and only35 complete original StageC owned members",
    )
    total = 0
    for path in actual:
        guard(started)
        require(
            path.is_file() and path.resolve(strict=True) == path,
            "Original owner is confined regular inventory",
        )
        total += path.stat().st_size
    require(total <= 128 << 20, "Original StageC inclusive128MiB retained cap")
    return total


def primary_packet(started):
    global _PRIMARY_RUNTIME_EXPECTED, _PRIMARY_FROZEN_EXPECTED
    manifest = json.loads(checked_read(PRIMARY_MANIFEST, PRIMARY_MANIFEST_SHA, started))
    require(
        manifest["schema"] == "a14-f44-stage-c-primary90-manifest-v3"
        and manifest["passed"] is True
        and manifest["completed"] is True
        and manifest["budget_censored"] is False
        and manifest["manifest_self_hash_excluded"] is True
        and manifest["manifest_inclusive_owned_file_count"] == 35
        and manifest["manifest_inclusive_retention_checked_before_sealing"] is True
        and manifest["row_status"] == "REJECTED"
        and all(
            manifest[k] is False
            for k in (
                "adoption",
                "cost_transfer",
                "full_G2",
                "quantum_advantage",
                "global_financial_gate_emission_authorized",
            )
        )
        and manifest["new_test_credit"]
        == manifest["new_price_samples"]
        == manifest["new_credited_gate_replays"]
        == 0,
        "Original completed scientific component retains resource rejection and zero transferred credit",
    )
    owned, frozen, external = (
        manifest[k] for k in ("files", "frozen_inputs", "external_runtime_inputs")
    )
    historical_map(owned, 34, started)
    historical_map(frozen, 851, started)
    historical_map(external, 2842, started, absolute_keys=True)
    require(owned == PRIMARY_OWNED, "Entire externally pinned original34-owned map")
    require(
        frozen[BUILDER_KEY] == BUILDER_SHA and frozen[PRIMARY_READY_KEY] == PRIMARY_READY_SHA,
        "Original frozen builder and ROOT READY remain exact",
    )
    _PRIMARY_FROZEN_EXPECTED = dict(frozen)
    root_map = {}
    merge_root_expected(root_map, frozen, started)
    merge_root_expected(
        root_map, {relative(PRIMARY / name): value for name, value in owned.items()}, started
    )
    merge_root_expected(root_map, {relative(PRIMARY_MANIFEST): PRIMARY_MANIFEST_SHA}, started)
    for key in external:
        path = Path(key)
        require(
            path.is_absolute()
            and str(path) == key
            and path.resolve(strict=True) == path
            and path.is_relative_to(BASE)
            and not path.is_relative_to(BASE / "Lib/site-packages"),
            "Literal full primary external map admits only base runtime, never a historical runtime expansion",
        )
    _PRIMARY_RUNTIME_EXPECTED = dict(external)
    _PRIMARY_RUNTIME_EXPECTED[str(LAUNCHER)] = LAUNCHER_SHA
    require(
        frozen[relative(LAUNCHER)] == LAUNCHER_SHA
        and external[str(BASE / "python.exe")] == BASE_SHA,
        "Both isolated launcher and base are original externally expected bytes",
    )
    merge_root_expected(
        root_map, {SHARED_KEY: SHARED_SHA, GATE_FRAGMENT_KEY: GATE_FRAGMENT_SHA}, started
    )
    primary_inventory(started)
    total = sum(
        len(checked_read(PRIMARY / name, expected, started)) for name, expected in owned.items()
    )
    require(total == manifest["owned_nonmanifest_bytes"], "Exact original34-owned byte total")
    return root_map


def caches_for(sources, present, absent, frozen, started):
    paths = {
        relative(Path(cache_from_source(str(source)))): Path(cache_from_source(str(source)))
        for source in sources
    }
    actual_present = {key for key, path in paths.items() if path.exists()}
    require(
        type(present) is dict
        and set(present) == actual_present
        and type(absent) is list
        and absent == sorted(set(paths) - actual_present),
        "Complete external cache presence/absence declaration without new aliases",
    )
    for key in actual_present:
        require(
            key in frozen and frozen[key] == present[key],
            "Declared present cache is an externally expected input",
        )
        checked_read(paths[key], present[key], started)
        _CACHE_PRESENT[paths[key]] = present[key]
    for key in absent:
        path = paths[key]
        require(
            not path.exists() and not path.is_symlink() and path.resolve(strict=False) == path,
            "Every declared absent code cache remains physically absent",
        )
        _ABSENT_CACHES.add(path)


def inherited_cache_contracts(frozen, started):
    failure_key = ".context/A14_F44_STAGE_C_FAILED_OWNED_FROZEN_run001.json"
    require(
        frozen[failure_key] == "60b2d2aa068169f19f72052738227588ea5ad2837498fbe0009db1d4a5c17c75",
        "Original failed-owned external freeze remains exact",
    )
    failed = json.loads(checked_read(ROOT / failure_key, frozen[failure_key], started))
    require(
        failed["passed"] is False
        and failed["metadata_freeze_only"] is True
        and failed["original_failure_is_authoritative"] is True
        and failed["Stage_C_release_authorized"] is False
        and failed["new_test_credit"] == failed["all_expected_SHA_waivers"] == 0,
        "Prior partial scientific files remain unapproved opaque historical bytes",
    )
    failed_map = failed["observed_owned_files"]
    historical_map(failed_map, 13, started)
    require(
        all(frozen[key] == sha for key, sha in failed_map.items()),
        "All original failed-owned hashes already in direct full primary map",
    )
    failed_route = ROOT / failed["failure_route"]
    require(
        failed["failure_route"]
        == "results/limitation_program_20261001/A14_taylor_f44_stage_C_run001"
        and failed_route.resolve(strict=True) == failed_route
        and set(failed_route.iterdir()) == {ROOT / key for key in failed_map}
        and all(
            path.is_file() and path.resolve(strict=True) == path for path in failed_route.iterdir()
        )
        and sum(path.stat().st_size for path in failed_route.iterdir())
        == failed["owned_bytes"]
        == 11426616,
        "Original13-member failed-owned inventory remains exact, with no old manifest or partial reuse",
    )
    prefit_key = ".context/A14_F44_STAGE_C_V2_PREFIT_FAILURE_WITNESS_run002.json"
    require(
        frozen[prefit_key] == "1de19d91d1359ffce383ffd917bc20f803c466d1b35a731c271f18a3b33b5be6",
        "Original prefit failure witness remains exact",
    )
    prefit = json.loads(checked_read(ROOT / prefit_key, frozen[prefit_key], started))
    absent_route = ROOT / "results/limitation_program_20261001/A14_taylor_f44_stage_C_run002"
    require(
        prefit["passed"] is False
        and prefit["metadata_only"] is True
        and prefit["actual_V2_failed_before_output_mkdir"] is True
        and prefit["scientific_execution_started"] is False
        and prefit["output_route"] == relative(absent_route)
        and prefit["new_fixture_credit"] == 0
        and not absent_route.exists()
        and not absent_route.is_symlink(),
        "Original prefit output route remains absent",
    )
    declarations = (
        (
            ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run001.json",
            ("experiment_f44_cosine_stage_c_v1.py", "f44_cosine_stage_c_source.py"),
        ),
        (
            ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run002.json",
            ("experiment_f44_cosine_stage_c_v2.py", "f44_cosine_stage_c_source.py"),
        ),
        (
            PRIMARY_READY_KEY,
            ("experiment_f44_cosine_stage_c_v3.py", "f44_cosine_stage_c_source.py"),
        ),
        (
            ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json",
            ("experiment_taylor_f44_stage_k.py", "taylor_f44_stage_k_source.py"),
        ),
        (
            ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json",
            ("audit_taylor_f44_stage_k.py",),
        ),
        (
            ".context/A14_TAYLOR_F44_STAGE_K_INTEGRITY_ROOT_READY_run001.json",
            ("verify_taylor_f44_stage_k_root_v1.py",),
        ),
    )
    for key, names in declarations:
        require(
            key in _PRIMARY_FROZEN_EXPECTED,
            "Historical direct cache metadata already in full primary map",
        )
        record = json.loads(checked_read(ROOT / key, frozen[key], started))
        caches_for(
            [HERE / name for name in names],
            record["existing_new_code_cache_SHA256"],
            record["absent_new_code_cache_paths"],
            frozen,
            started,
        )
    keys = (
        "results/limitation_program_20261001/A14_cosine_feasibility_run001/interpreter.json",
        "results/limitation_program_20261001/A14_cosine_feasibility_audit_run003/protocol.json",
    )
    for key in keys:
        record = json.loads(checked_read(ROOT / key, frozen[key], started))
        record = record["interpreter"] if key.endswith("protocol.json") else record
        for spelling in record["absent_standard_runtime_paths"]:
            path = Path(spelling)
            require(
                path.is_absolute()
                and str(path) == spelling
                and path.resolve(strict=False) == path
                and not path.exists()
                and not path.is_symlink(),
                "All original explicitly absent runtime paths unchanged",
            )
            _ABSENT_CACHES.add(path)


def root_release(expected, started):
    raw = checked_read(READY, expected, started)
    ready = json.loads(raw)
    require(
        ready["schema"] == "root-f44-qrom64x8-comparison-READY-v1"
        and ready["passed"] is True
        and ready["static_review_only"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["standalone_lookup_emission_approved"] is True,
        "Separate ROOT-frozen standalone component release required",
    )
    require(
        ready["primary_manifest_SHA256"] == PRIMARY_MANIFEST_SHA
        and ready["output_route"] == relative(OUTPUT)
        and ready["CPU_admission_wall_seconds"] == [180, 150, 600]
        and ready["scope"] == _SCOPE,
        "Exact source, route, limits and no-credit component scope",
    )
    release = ready["frozen_inputs"]
    require(
        type(release) is dict
        and set(release) == {relative(AUTHOR), relative(METHOD_MD), relative(METHOD_JSON)},
        "Exactly three separately frozen new author files",
    )
    new_bytes = len(raw)
    for key, sha in release.items():
        exact_relative_key(key)
        new_bytes += len(checked_read(ROOT / key, sha, started))
    require(
        len(release) + 1 <= MAX_FROZEN_FILES and new_bytes <= MAX_FROZEN_BYTES,
        "Bounded new release",
    )
    method = json.loads(checked_read(METHOD_JSON, release[relative(METHOD_JSON)], started))
    require(method == POLICY_EXPECTED, "Entire prospective policy fixed before any emission")
    frozen = primary_packet(started)
    merge_root_expected(frozen, release, started)
    merge_root_expected(frozen, {relative(READY): expected}, started)
    merge_root_expected(frozen, ready["existing_new_code_cache_SHA256"], started)
    inherited_cache_contracts(frozen, started)
    caches_for(
        [AUTHOR, ROOT / SHARED_KEY],
        ready["existing_new_code_cache_SHA256"],
        ready["absent_new_code_cache_paths"],
        frozen,
        started,
    )
    return frozen


def fresh_union(frozen, runtime, started, protocol_expected=None):
    invocation_check(started)
    current, _ = runtime_packet(started)
    require(
        current == runtime == _PRIMARY_RUNTIME_EXPECTED,
        "Entire externally expected current runtime membership and SHA exact",
    )
    primary_inventory(started)
    inherited_cache_contracts(frozen, started)
    union = {}
    for key, sha in frozen.items():
        path = ROOT / key
        require(path not in union or union[path] == sha, "Equal-SHA direct full-map union")
        union[path] = sha
    for key, sha in runtime.items():
        path = Path(key)
        require(path not in union or union[path] == sha, "Equal-SHA actual runtime union")
        union[path] = sha
    if protocol_expected is not None:
        union[OUTPUT / "protocol.json"] = protocol_expected
    require(len(union) <= MAX_REFERENCES, "Complete inherited unique-path cap")
    total = 0
    for path, sha in sorted(union.items(), key=lambda item: str(item[0])):
        total += len(checked_read(path, sha, started))
        require(total <= MAX_UNIQUE_BYTES, "Complete inherited8GiB uncached union bound")
    primary_inventory(started)
    for path, sha in _CACHE_PRESENT.items():
        checked_read(path, sha, started)
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_CACHES),
        "All declared absent caches/runtime remain absent",
    )
    return {
        "full_fresh_resolve_and_SHA": True,
        "unique_paths": len(union),
        "unique_bytes": total,
        "sha_mismatches": 0,
        "expected_hash_waivers": 0,
        "primary_complete_counts": [34, 851, 2842],
        "original35_owned_inventory_exact": True,
        "loaded_runtime_origins": loaded_runtime_check(runtime, started),
        "historical_recursive_runtime_promotion": False,
    }


def protocol_value(frozen, runtime, runtime_bytes):
    return {
        "schema": "f44-qrom64x8-comparison-protocol-v1",
        "local_only": True,
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "external_runtime_bytes": runtime_bytes,
        "primary_manifest_SHA256": PRIMARY_MANIFEST_SHA,
        "scope": dict(_SCOPE),
        "policy": POLICY_EXPECTED,
        "runtime_layout": {
            "isolated": True,
            "no_site": True,
            "bytecode_writes": False,
            "absent_loaded_cache_paths": sorted(str(p) for p in _ABSENT_CACHES),
        },
        "prepare_scientific_emission_or_replay": False,
    }


def prepare(args, started):
    global _ATTEMPT_ROUTE_OWNED
    invocation_check(started)
    require(
        not OUTPUT.exists() and not OUTPUT.is_symlink(), "Never reuse a standalone comparison route"
    )
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(
        runtime == _PRIMARY_RUNTIME_EXPECTED,
        "New isolated runtime matches all original external expected bytes",
    )
    loaded_runtime_check(runtime, started)
    fresh_union(frozen, runtime, started)
    guard(started, admission=True)
    OUTPUT.mkdir(parents=False, exist_ok=False)
    _ATTEMPT_ROUTE_OWNED = True
    write_json(OUTPUT / "protocol.json", protocol_value(frozen, runtime, runtime_bytes), started)
    protocol_sha = hashlib.sha256(stable_read(OUTPUT / "protocol.json", started)).hexdigest()
    terminal = fresh_union(frozen, runtime, started, protocol_sha)
    guard(started)
    print(
        json.dumps(
            {
                "prepare_passed": True,
                "scientific_execution": False,
                "protocol_SHA256": protocol_sha,
                "protocol": relative(OUTPUT / "protocol.json"),
                "terminal_full_union": terminal,
            }
        ),
        flush=True,
    )


class LookupArray:
    def __init__(self):
        budget()
        require(
            sys.byteorder == "little" and array("i").itemsize == 4,
            "Fixed native little-endian int32 rows",
        )
        self.words, self.scratch_used = array("i"), False
        self.checkpoint = budget

    @property
    def rows(self):
        return len(self.words) // 4

    def register(self, width):
        budget()
        require(
            type(width) is int and width == 5 and not self.scratch_used,
            "Only one exact reusable five-wire stack",
        )
        self.scratch_used = True
        return list(range(1296, 1301))

    def gate(self, *operands):
        if self.rows % 128 == 0:
            budget()
        require(
            1 <= len(operands) <= 3
            and len(set(operands)) == len(operands)
            and all(type(wire) is int and 0 <= wire < LOOKUP_QUBITS for wire in operands)
            and self.rows < MAX_LOOKUP_ROWS,
            "Canonical finite prospective native row",
        )
        self.words.extend((len(operands), *operands, *([0] * (3 - len(operands)))))


def lookup_wrapper(algorithm, table):
    budget()
    p = LookupArray()
    address = list(range(72))
    outs = [list(range(72 + 72 * column, 144 + 72 * column)) for column in range(8)]
    private_address = list(range(648, 720))
    private_outs = [list(range(720 + 72 * column, 792 + 72 * column)) for column in range(8)]
    for source, target in zip(address, private_address, strict=True):
        p.gate(source, target)
    begin = p.rows
    function = lookup_naive if algorithm == "naive" else lookup_shared
    require(algorithm in ("naive", "shared"), "Only two prospectively fixed algorithms")
    function(p, private_address, private_outs, table, 6)
    end = p.rows
    require(p.scratch_used, "Exactly five physical prefix ancillas allocated")
    for source, target in zip(private_outs, outs, strict=True):
        for a, b in zip(source, target, strict=True):
            p.gate(a, b)
    inverse_begin = p.rows
    for index in range(end - 1, begin - 1, -1):
        kind, operands = c130_native_row(p.words, index, LOOKUP_QUBITS)
        p.gate(*operands)
    inverse_end = p.rows
    for source, target in zip(address, private_address, strict=True):
        p.gate(source, target)
    budget()
    return p.words, {
        "algorithm": algorithm,
        "qubits": LOOKUP_QUBITS,
        "rows": p.rows,
        "args": [address],
        "outs": outs,
        "private_address": private_address,
        "private_outs": private_outs,
        "clean_prefix_ancillas": list(range(1296, 1301)),
        "argument_copy_rows": [0, begin],
        "body_rows": [begin, end],
        "output_XOR_rows": [end, inverse_begin],
        "literal_body_inverse_rows": [inverse_begin, inverse_end],
        "argument_uncopy_rows": [inverse_end, p.rows],
        "input_preserved": True,
        "dirty_output_XOR": True,
        "private648_and_prefix5_zero_entry_exit": True,
    }


def retained_table(frozen, started):
    """Unused giant exact-oracle integers remain decimal strings, never evaluated."""
    name = "primary90_literals.json"
    raw = checked_read(PRIMARY / name, PRIMARY_OWNED[name], started)
    original = json.loads(raw, parse_int=str)
    require(
        original["schema"] == "a14-f44-stage-c-primary90-literals-v1"
        and original["row_id"] == "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38"
        and original["primary_digits"] == "90"
        and original["table_literal_count"] == "512"
        and original["coefficient_count"] == "448"
        and original["center_count"] == "64",
        "Exact immutable primary90 object and full retained literal count",
    )
    require(
        type(original["table"]) is list and len(original["table"]) == 64,
        "All original64 table rows",
    )
    table = []
    for index, row in enumerate(original["table"]):
        budget()
        require(
            type(row) is list
            and len(row) == 8
            and all(
                type(word) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)", word) and len(word) <= 23
                for word in row
            ),
            "All512 bounded canonical raw decimal words",
        )
        converted = [int(word) for word in row]
        require(
            all(-(1 << 71) <= word < (1 << 71) for word in converted)
            and converted[0] == (2 * index + 1) << 37,
            "Every exact signed72 literal and unchanged center",
        )
        table.append(converted)
    return table


def verify_scientific_text(frozen, started):
    original_shared = ast.parse(checked_read(ROOT / SHARED_KEY, SHARED_SHA, started))
    shared = next(
        n
        for n in original_shared.body
        if isinstance(n, ast.FunctionDef) and n.name == "lookup_shared"
    )
    require(
        hashlib.sha256(ast.dump(shared, include_attributes=False).encode()).hexdigest()
        == SHARED_AST_SHA,
        "Exact immutable shared-prefix AST identity, with no external source import",
    )
    author = ast.parse(checked_read(AUTHOR, frozen[relative(AUTHOR)], started))
    embedded = next(
        n for n in author.body if isinstance(n, ast.FunctionDef) and n.name == "lookup_shared"
    )
    require(
        ast.dump(embedded, include_attributes=False) == ast.dump(shared, include_attributes=False),
        "Owned shared-prefix function is exact text-derived admitted source AST",
    )
    original_builder = ast.parse(checked_read(ROOT / BUILDER_KEY, BUILDER_SHA, started))
    helper = next(
        n
        for n in original_builder.body
        if isinstance(n, ast.FunctionDef) and n.name == "helper_compute"
    )
    branch = next(
        n
        for n in ast.walk(helper)
        if isinstance(n, ast.If)
        and isinstance(n.test, ast.Compare)
        and isinstance(n.test.left, ast.Name)
        and n.test.left.id == "name"
        and len(n.test.comparators) == 1
        and isinstance(n.test.comparators[0], ast.Constant)
        and n.test.comparators[0].value == "QROM64x8"
    )
    naive = next(
        n for n in author.body if isinstance(n, ast.FunctionDef) and n.name == "lookup_naive"
    )
    require(
        [ast.dump(n, include_attributes=False) for n in naive.body[4:]]
        == [ast.dump(n, include_attributes=False) for n in branch.body],
        "Narrow owned naive function retains the exact original QROM branch AST after only fixed interface setup",
    )
    fragment = ast.parse(checked_read(ROOT / GATE_FRAGMENT_KEY, GATE_FRAGMENT_SHA, started))
    names = {
        "c130_native_row",
        "c130_schedule_interval",
        "c130_phase_shift",
        "c130_phase_add",
        "c130_ccx_absolute_phase",
    }
    expected = {
        n.name: ast.dump(n, include_attributes=False)
        for n in fragment.body
        if isinstance(n, ast.FunctionDef) and n.name in names
    }
    actual = {
        n.name: ast.dump(n, include_attributes=False)
        for n in author.body
        if isinstance(n, ast.FunctionDef) and n.name in names
    }
    require(
        actual == expected and set(expected) == names,
        "Exact pinned authored resource and phase definitions",
    )
    constants = lambda tree: [
        ast.dump(n, include_attributes=False)
        for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(x, ast.Name) and x.id == "C130_CCX_MACRO" for x in n.targets)
    ]
    require(
        constants(author) == constants(fragment),
        "Exact same actual7T macro for resource and absolute-phase proofs",
    )


def bind_actual_baseline(words, descriptor, table, frozen, started):
    original = json.loads(
        checked_read(
            PRIMARY / "prototype_descriptor.json",
            PRIMARY_OWNED["prototype_descriptor.json"],
            started,
        )
    )
    events = [event for event in original["trace"] if event["op"] == "QROM64x8"]
    require(len(events) == 1, "One actual saved primary QROM event")
    event = events[0]
    require(
        event["params"] == {"table": table}
        and event["full_private_bank_reused"] is True
        and event["inner_argument_copy_CX"] == 144
        and len(event["args"]) == 1
        and len(event["outs"]) == 8,
        "Exact immutable table and complete original copied wrapper",
    )
    mapping = (
        event["args"][0]
        + [wire for bank in event["outs"] for wire in bank]
        + original["shared_private_workspace"][:653]
    )
    require(
        len(mapping) == LOOKUP_QUBITS and len(set(mapping)) == LOOKUP_QUBITS,
        "Injective physical1301-wire normalization",
    )
    start, end = event["rows"]
    require(end - start == descriptor["rows"], "Every actual baseline helper-wrapper row retained")
    actual = array("i")
    actual.frombytes(
        checked_read(PRIMARY / "cosine.gates.bin", PRIMARY_OWNED["cosine.gates.bin"], started)
    )
    require(
        len(actual) == 4 * original["gate_rows"] and 0 <= start <= end <= original["gate_rows"],
        "Full original saved native payload",
    )
    for index in range(descriptor["rows"]):
        if index % 128 == 0:
            budget()
        opcode, operands = c130_native_row(words, index, LOOKUP_QUBITS)
        original_opcode, original_operands = c130_native_row(
            actual, start + index, original["qubits"]
        )
        require(
            opcode == original_opcode
            and tuple(mapping[wire] for wire in operands) == original_operands,
            "Every complete baseline row equals the normalized actual StageC003 saved row",
        )
    for field, own in (
        ("compute_rows", "body_rows"),
        ("copy_rows", "output_XOR_rows"),
        ("inverse_rows", "literal_body_inverse_rows"),
    ):
        require(
            event[field] == [start + value for value in descriptor[own]],
            "All original helper body/copy/inverse boundaries retained",
        )
    return {
        "passed": True,
        "original_manifest_SHA256": PRIMARY_MANIFEST_SHA,
        "original_table_SHA256": PRIMARY_OWNED["primary90_literals.json"],
        "original_descriptor_SHA256": PRIMARY_OWNED["prototype_descriptor.json"],
        "original_native_SHA256": PRIMARY_OWNED["cosine.gates.bin"],
        "actual_source_event_rows": [start, end],
        "standalone_used_wire_count": LOOKUP_QUBITS,
        "normalization_is_injective": True,
        "all_actual_event_rows_matched": True,
        "unused_original_caller_wires_removed_only_from_standalone_comparison": True,
        "whole_caller_qubits_or_depth_transferred": False,
        "original_resource_REJECTED_unchanged": True,
    }


def lookup_sweep(words, state, lanes, inverse=False):
    budget()
    require(
        type(lanes) is int
        and 1 <= lanes <= 128
        and len(state) == LOOKUP_QUBITS
        and len(words) % 4 == 0
        and 0 < len(words) // 4 <= MAX_LOOKUP_ROWS,
        "Fixed complete bounded lookup replay",
    )
    mask = (1 << lanes) - 1
    require(
        all(type(value) is int and 0 <= value <= mask for value in state),
        "Exact finite bit-cohort wire planes",
    )
    indices = range(len(words) // 4 - 1, -1, -1) if inverse else range(len(words) // 4)
    for step, index in enumerate(indices):
        if step % 128 == 0:
            budget()
        opcode, wires = c130_native_row(words, index, LOOKUP_QUBITS)
        if opcode == 1:
            state[wires[0]] ^= mask
        elif opcode == 2:
            state[wires[1]] ^= state[wires[0]]
        else:
            state[wires[2]] ^= state[wires[0]] & state[wires[1]]
    budget()


def lookup_cohort(words, table, cases):
    initial = [0] * LOOKUP_QUBITS
    for lane, (address, dirty) in enumerate(cases):
        budget()
        require(
            0 <= address < (1 << 72) and dirty in (0, (1 << 72) - 1),
            "Fixed full72 raw address and per-bank dirty word",
        )
        for bit in range(72):
            initial[bit] |= ((address >> bit) & 1) << lane
            for column in range(8):
                initial[72 + 72 * column + bit] |= ((dirty >> bit) & 1) << lane
    expected = list(initial)
    for lane, (address, _) in enumerate(cases):
        row = table[address % 64]
        for column, value in enumerate(row):
            for bit in range(72):
                expected[72 + 72 * column + bit] ^= ((value >> bit) & 1) << lane
    current = list(initial)
    lookup_sweep(words, current, len(cases))
    for wire in range(LOOKUP_QUBITS):
        if wire % 128 == 0:
            budget()
        require(
            current[wire] == expected[wire],
            "Every full address/output/private/prefix wire matches independent retained-word XOR oracle",
        )
    lookup_sweep(words, current, len(cases), inverse=True)
    require(
        current == initial,
        "Every complete allocated state returns exactly through actual inverse rows",
    )
    return {
        "case_count": len(cases),
        "forward_calls": len(cases),
        "inverse_calls": len(cases),
        "physical_bit_cohort_sweeps": 2,
        "every1301_wire_checked": True,
        "all_private653_zero_checked": True,
    }


def fixed_lookup_diagnostics(words, table):
    dirty = (1 << 72) - 1
    regular = [(address, word) for address in range(64) for word in (0, dirty)]
    witnesses = [(address | (1 << high), dirty) for address in (0, 63) for high in (6, 71)]
    require(
        len(regular) == 128 and len(witnesses) == 4,
        "Exactly accepted frozen regular/high-bit case quantities",
    )
    return {
        "passed": True,
        "all64_low_addresses_two_dirty_outputs": lookup_cohort(words, table, regular),
        "unused_high_address_witnesses": lookup_cohort(words, table, witnesses),
        "unused_high_cases": [
            {"low6": address % 64, "raw_address": address, "dirty_all8_words": dirty}
            for address, _ in witnesses
        ],
        "logical_full_forward_calls": 132,
        "logical_full_inverse_calls": 132,
        "physical_bit_cohort_sweeps": 4,
        "fixture_credit": 0,
        "corpus_expansion_after_observation": False,
    }


def lookup_resources(words):
    full = c130_schedule_interval(words, LOOKUP_QUBITS, 0, len(words) // 4)
    result = {key: value for key, value in full.items() if key != "rows"}
    result.update(
        qubits=LOOKUP_QUBITS,
        clifford_cx=result["cx"] + 6 * result["ccx"],
        clifford_h=2 * result["ccx"],
        schedule="all-to-all ASAP entire standalone chronological exact7T expansion",
        all_argument_copies_output_copies_body_inverse_and_cleanup_included=True,
        whole_caller_cost_or_capped_depth_transfer=False,
    )
    return result


def write_binary(path, words, started):
    guard(started)
    require(
        path.parent == OUTPUT
        and OUTPUT.resolve(strict=True) == OUTPUT
        and not path.exists()
        and not path.is_symlink(),
        "Exclusive confined new native array",
    )
    prior = set(OUTPUT.iterdir())
    require(
        all(member.is_file() and member.resolve(strict=True) == member for member in prior),
        "Complete regular prior owned set",
    )
    prior_bytes = sum(member.stat().st_size for member in prior)
    size = 4 * len(words)
    require(
        len(prior) + 1 <= MAX_OWNED_FILES
        and size <= MAX_OWNED_SINGLE_BYTES
        and prior_bytes + size <= MAX_OWNED_BYTES,
        "Exact pre-admitted binary ownership including payload",
    )
    with path.open("xb") as stream:
        view = memoryview(words).cast("B")
        for begin in range(0, len(view), 1 << 20):
            guard(started)
            stream.write(view[begin : begin + (1 << 20)])
    require(
        path.stat().st_size == size and set(OUTPUT.iterdir()) == prior | {path},
        "All actual native bytes written and no new extra member",
    )
    guard(started)


def universal_lookup_proof():
    return {
        "schema": "f44-qrom64x8-universal-clean-XOR-proof-v1",
        "passed": True,
        "domain": "All full72 addresses, arbitrary576-bit dirty outputs, and zero private653 bits",
        "selection": "address mod64; all high66 address bits preserved and ignored by body",
        "naive_identity": "One-hot six-bit minterms; five clean AND-prefix wires computed/copied/uncomputed per row",
        "shared_identity": "base=row0; residual_i=row_i XOR base. A node clean flag goes P*x, P*(1-x), P*x,0 by CCX,CX,CX,CCX; children restore their own stack. Pruned all-zero residual subtrees emit no output change. High branch/address complement/low branch/address restoration partition every six-bit address exactly once",
        "signed_words": "Each word reduced modulo2^72 only at bit extraction; every signed72 retained integer unchanged",
        "wrapper_identity": "copy all72 address bits; compute private576 table bits; XOR-copy all576 into arbitrary dirty outputs; literal body inverse; uncopy address. All648 private address/output bits and all5 prefix bits restore zero",
        "coherent_absolute_phase": "Only exact X,CX,CCX permutations; exact7T CCX absolute+1 phase verified separately; basis identity extends linearly",
        "full_dirty_output_universality_from_affine_XOR_translation": True,
        "historical_A15_or_financial_proof_transferred": False,
        "whole_StageC_function_replaced_or_approved": False,
        "program_fixture_credit": 0,
    }


def seal(frozen, runtime, started, before, after, protocol_sha):
    expected_names = {
        "protocol.json",
        "run_started.json",
        "retained_table.json",
        "naive.gates.bin",
        "shared.gates.bin",
        "native_gate_arrays.json",
        "source_binding.json",
        "universal_lookup_proof.json",
        "exact_CCX_phase_proof.json",
        "naive_diagnostics.json",
        "shared_diagnostics.json",
        "resources.json",
        "summary.json",
        "verification.json",
    }
    require(
        {p.name for p in OUTPUT.iterdir()} == expected_names,
        "All and only complete14 nonmanifest comparison members",
    )
    owned, total = {}, 0
    for path in sorted(OUTPUT.iterdir(), key=str):
        data = stable_read(path, started)
        total += len(data)
        owned[relative(path)] = hashlib.sha256(data).hexdigest()
    require(
        owned[relative(OUTPUT / "protocol.json")] == protocol_sha,
        "Exact externally frozen prepared protocol unchanged",
    )
    value = {
        "schema": "f44-qrom64x8-comparison-manifest-v1",
        "passed": True,
        "completed": True,
        "budget_censored": False,
        "error": None,
        "owned_files": owned,
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "fresh_before": before,
        "fresh_after": after,
        "prepared_protocol_SHA256": protocol_sha,
        "primary_manifest_SHA256": PRIMARY_MANIFEST_SHA,
        "scope": dict(_SCOPE),
        "manifest_self_hash_excluded": True,
        "manifest_inclusive_owned_file_count": len(owned) + 1,
        "owned_nonmanifest_bytes": total,
        "manifest_inclusive_retention_checked_before_sealing": True,
    }
    encoded = len((json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode())
    require(
        len(owned) + 2 <= MAX_OWNED_FILES and total + encoded + 4096 <= MAX_OWNED_BYTES,
        "Inclusive manifest and one bounded post-seal failure marker admitted before seal",
    )
    write_json(OUTPUT / "manifest.json", value, started)
    actual = set(OUTPUT.iterdir())
    require(
        actual == {ROOT / name for name in owned} | {OUTPUT / "manifest.json"}
        and len(actual) == 15 <= MAX_OWNED_FILES
        and all(path.is_file() and path.resolve(strict=True) == path for path in actual)
        and sum(path.stat().st_size for path in actual) == total + encoded <= MAX_OWNED_BYTES,
        "Exact15-member complete inclusive final ownership and bytes",
    )
    guard(started)


def run(args, started):
    global _ATTEMPT_ROUTE_OWNED
    require(
        OUTPUT.is_dir()
        and OUTPUT.resolve(strict=True) == OUTPUT
        and {path.name for path in OUTPUT.iterdir()} == {"protocol.json"},
        "One exact new prepared comparison route",
    )
    _ATTEMPT_ROUTE_OWNED = True
    invocation_check(started)
    protocol = json.loads(checked_read(OUTPUT / "protocol.json", args.protocol_sha256, started))
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(
        runtime == _PRIMARY_RUNTIME_EXPECTED == protocol["external_runtime_inputs"],
        "Full externally expected runtime before emission",
    )
    loaded_runtime_check(runtime, started)
    require(
        protocol == protocol_value(frozen, runtime, runtime_bytes),
        "Entire separately externally frozen protocol exact",
    )
    before = fresh_union(frozen, runtime, started, args.protocol_sha256)
    guard(started, admission=True)
    write_json(
        OUTPUT / "run_started.json",
        {
            "PID": os.getpid(),
            "root_ready_expected_SHA256": args.root_ready_sha256,
            "protocol_expected_SHA256": args.protocol_sha256,
            "component_emission_started": False,
            "scope": dict(_SCOPE),
        },
        started,
    )
    verify_scientific_text(frozen, started)
    table = retained_table(frozen, started)
    write_json(
        OUTPUT / "retained_table.json",
        {
            "table": table,
            "literal_count": 512,
            "primary_literal_SHA256": PRIMARY_OWNED["primary90_literals.json"],
            "refit": False,
        },
        started,
    )
    words, descriptors, diagnostics, resources, array_records = {}, {}, {}, {}, {}
    for algorithm in ("naive", "shared"):
        words[algorithm], descriptors[algorithm] = lookup_wrapper(algorithm, table)
    binding = bind_actual_baseline(words["naive"], descriptors["naive"], table, frozen, started)
    write_json(OUTPUT / "source_binding.json", binding, started)
    phase = c130_ccx_absolute_phase()
    write_json(OUTPUT / "exact_CCX_phase_proof.json", phase, started)
    write_json(OUTPUT / "universal_lookup_proof.json", universal_lookup_proof(), started)
    for algorithm in ("naive", "shared"):
        name = algorithm + ".gates.bin"
        write_binary(OUTPUT / name, words[algorithm], started)
        sha = hashlib.sha256(stable_read(OUTPUT / name, started)).hexdigest()
        array_records[algorithm] = {
            "path": relative(OUTPUT / name),
            "sha256": sha,
            "bytes": 4 * len(words[algorithm]),
            "format": "raw little-endian int32 Nx4 X/CX/CCX rows",
            "descriptor": descriptors[algorithm],
        }
        diagnostics[algorithm] = fixed_lookup_diagnostics(words[algorithm], table)
        resources[algorithm] = lookup_resources(words[algorithm])
        write_json(OUTPUT / (algorithm + "_diagnostics.json"), diagnostics[algorithm], started)
    write_json(OUTPUT / "native_gate_arrays.json", array_records, started)
    original_resources = json.loads(
        checked_read(
            PRIMARY / "actual_prototype_resources.json",
            PRIMARY_OWNED["actual_prototype_resources.json"],
            started,
        )
    )
    original_qrom = [
        event
        for event in original_resources["matched_serial_event_chronology"]["forward_actual_events"]
        if event["op"] == "QROM64x8"
    ]
    require(
        len(original_qrom) == 1
        and all(
            original_qrom[0][key] == resources["naive"][key]
            for key in ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")
        ),
        "Standalone baseline reconstructs every recorded actual original QROM event count and depth",
    )
    fields = (
        "source_gates",
        "x",
        "cx",
        "ccx",
        "t_count",
        "t_depth",
        "clifford_t_depth",
        "clifford_cx",
        "clifford_h",
        "qubits",
    )
    comparison = {
        "naive": resources["naive"],
        "shared": resources["shared"],
        "shared_minus_naive": {
            key: resources["shared"][key] - resources["naive"][key] for key in fields
        },
        "numerical_cost_direction_is_observed_not_a_pass_requirement": True,
        "identical1301_wire_full_copies_cleanup": True,
        "actual_original_QROM_event_resources_reconstructed": True,
        "whole_caller_or_capped_depth_transfer": False,
    }
    write_json(OUTPUT / "resources.json", comparison, started)
    original_summary = json.loads(
        checked_read(PRIMARY / "summary.json", PRIMARY_OWNED["summary.json"], started)
    )
    require(
        original_summary["row"]["status"] == "REJECTED"
        and original_summary["row"]["resource_gate_passed"] is False,
        "Original wholeStageC rejection remains authoritative and unchanged",
    )
    write_json(
        OUTPUT / "summary.json",
        {
            "schema": "f44-qrom64x8-comparison-summary-v1",
            "passed": True,
            "standalone_lookup_comparison_complete": True,
            "immutable_retained_signed72_words": 512,
            "algorithms": ["naive", "shared"],
            "regular_cases_per_algorithm": 128,
            "high_address_witnesses_per_algorithm": 4,
            "logical_total_forward_inverse_calls": 528,
            "physical_total_bit_cohort_sweeps": 8,
            "coherent_full72_address_dirty576_output_clean653_map": True,
            "original_StageC_row_status": "REJECTED",
            "original_StageC_resource_gate_passed": False,
            "resource_comparison": comparison,
            "scope": dict(_SCOPE),
        },
        started,
    )
    after = fresh_union(frozen, runtime, started, args.protocol_sha256)
    write_json(
        OUTPUT / "verification.json",
        {
            "passed": True,
            "before": before,
            "after": after,
            "primary_or_shared_source_imported": False,
            "expected_hash_waivers": 0,
            "scope": dict(_SCOPE),
        },
        started,
    )
    seal(frozen, runtime, started, before, after, args.protocol_sha256)
    print(
        json.dumps(
            {
                "passed": True,
                "standalone_component_only": True,
                "manifest": relative(OUTPUT / "manifest.json"),
                "scope": dict(_SCOPE),
                "observed_CPU": time.process_time(),
                "observed_wall": time.monotonic() - started,
            }
        ),
        flush=True,
    )


def main():
    global _STARTED
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--root-ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    args = parser.parse_args()
    _STARTED = started_clock()
    require(
        args.mode == "prepare" or args.protocol_sha256 is not None,
        "Separate external protocol freeze required",
    )
    try:
        if args.mode == "prepare":
            require(
                args.protocol_sha256 is None, "Prepare starts without an old protocol expectation"
            )
            prepare(args, _STARTED)
        else:
            run(args, _STARTED)
    except BaseException as error:
        preserve_failure(error, _STARTED)
        raise


# Text-derived operational and lookup definitions follow; __main__ is appended last.


def require(value, message):
    if not value:
        raise ValueError(message)


def started_clock():
    require(sys.platform == "win32", "Frozen experiment requires Windows")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(x) for x in values)),
        "Actual process creation time",
    )
    ticks = values[0].dwHighDateTime << 32 | values[0].dwLowDateTime
    elapsed = (time.time_ns() - (ticks - 116444736000000000) * 100) / 1000000000
    require(elapsed >= 0, "Nonnegative process age")
    return time.monotonic() - elapsed


def guard(started, admission=False):
    cpu, wall = (time.process_time(), time.monotonic() - started)
    if cpu >= (WORK_LIMIT if admission else CPU_LIMIT) or wall >= WALL_LIMIT:
        raise RuntimeError(f"QROM fixed budget reached: CPU={cpu}, wall={wall}")
    return (cpu, wall)


def stable_read(path, started):
    global _HASH_WORK
    guard(started)
    require(
        path.is_absolute() and path.resolve(strict=True) == path, "Exact absolute path, no alias"
    )
    before = path.stat()
    require(path.is_file() and before.st_size <= MAX_SINGLE_BYTES, "Finite regular input")
    parts = []
    with path.open("rb") as stream:
        while True:
            guard(started)
            part = stream.read(1 << 20)
            if not part:
                break
            _HASH_WORK += len(part)
            require(_HASH_WORK <= MAX_HASH_WORK, "Inherited24GiB complete hashing/read-work cap")
            parts.append(part)
            require(sum(map(len, parts)) <= MAX_SINGLE_BYTES, "Bounded file read")
    data = b"".join(parts)
    after = path.stat()
    fields = (
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
        "st_mode",
        "st_file_attributes",
        "st_reparse_tag",
    )
    require(all((getattr(before, k) == getattr(after, k) for k in fields)), "Stable file identity")
    require(path.resolve(strict=True) == path, "Exact nonredirected input after complete read")
    require(len(data) == before.st_size, "Full observed byte count")
    guard(started)
    return data


def checked_read(path, expected, started):
    global _REFERENCES
    _REFERENCES += 1
    require(_REFERENCES <= MAX_REFERENCES, "Inherited100000 reference cap")
    require(isinstance(expected, str) and SHA.fullmatch(expected), "Exact expected SHA-256")
    data = stable_read(path, started)
    require(hashlib.sha256(data).hexdigest() == expected, "Fresh bytes equal frozen expected SHA")
    return data


def write_json(path, value, started):
    guard(started)
    require(
        path.parent == OUTPUT and OUTPUT.resolve(strict=True) == OUTPUT,
        "Exact confined owned output directory",
    )
    require(not path.exists() and (not path.is_symlink()), "New owned output only")
    prior = set(OUTPUT.iterdir())
    prior_bytes = 0
    for member in prior:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Existing owned members are confined regular files",
        )
        prior_bytes += member.stat().st_size
    require(
        len(prior) + 1 <= MAX_OWNED_FILES and prior_bytes < MAX_OWNED_BYTES,
        "Prospective exclusive write stays within owned capacities",
    )
    encoded_bytes = 1
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
            value
        ):
            guard(started)
            encoded_bytes += len(fragment.encode("utf-8"))
            require(encoded_bytes <= MAX_OWNED_SINGLE_BYTES, "Bounded exclusive JSON encoding")
            require(
                prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
                "Guarded encoded bytes stay within remaining owned capacity",
            )
            stream.write(fragment)
            guard(started)
        stream.write("\n")
    require(path.stat().st_size == encoded_bytes, "Exact actual UTF8 owned byte count")
    actual = set(OUTPUT.iterdir())
    require(
        actual == prior | {path} and len(actual) <= MAX_OWNED_FILES,
        "Exact guarded write ownership count",
    )
    actual_bytes = 0
    for member in actual:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Final written owned members retain exact routes",
        )
        actual_bytes += member.stat().st_size
    require(
        actual_bytes == prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
        "Actual complete guarded write ownership bytes",
    )
    guard(started)


def relative(path):
    return path.relative_to(ROOT).as_posix()


def invocation_check(started):
    require(Path.cwd().resolve(strict=True) == ROOT, "Exact workspace invocation cwd")
    require(sys.version_info[:3] == (3, 12, 4), "Pinned Python 3.12.4")
    require(sys.flags.isolated == 1 and sys.flags.no_site == 1, "Use -I -S")
    require(sys.dont_write_bytecode, "Use -B")
    require(Path(sys.executable).resolve(strict=True) == LAUNCHER, "Actual pinned launcher")
    require(Path(sys.base_prefix).resolve(strict=True) == BASE, "Actual pinned interpreter root")
    require(Path(sys.prefix).resolve(strict=True) == BASE, "No-site base interpreter prefix")
    expected_path = [str(BASE / "python312.zip"), str(BASE / "DLLs"), str(BASE / "Lib"), str(BASE)]
    require(sys.path == expected_path, "Exact isolated standard-library search path")
    require(not (BASE / "python312.zip").exists(), "Frozen absent runtime ZIP")
    require(not (BASE / "python312.zip").is_symlink(), "No dangling alias for absent runtime ZIP")
    require(
        not any((name == "site" or name.startswith("research.") for name in sys.modules)),
        "No site startup or scientific module admitted",
    )
    checked_read(LAUNCHER, LAUNCHER_SHA, started)
    checked_read(BASE / "python.exe", BASE_SHA, started)


def runtime_packet(started):
    paths = {LAUNCHER, BASE / "python.exe"}
    require(BASE.resolve(strict=True) == BASE, "Exact base interpreter directory")
    for path in BASE.iterdir():
        guard(started)
        if path.is_file():
            paths.add(path)
    for tree in (BASE / "Lib", BASE / "DLLs"):
        for directory, names, files in os.walk(tree, followlinks=False):
            guard(started)
            parent = Path(directory)
            require(
                parent.resolve(strict=True) == parent, "Runtime inventory does not follow aliases"
            )
            names[:] = [name for name in names if name.casefold() != "site-packages"]
            for name in names:
                child = parent / name
                require(
                    not child.is_symlink() and child.resolve(strict=True) == child,
                    "No silently skipped runtime directory alias",
                )
            paths.update((parent / name for name in files))
            require(len(paths) <= MAX_RUNTIME_FILES, "Finite isolated runtime file count")
    mapping, total = ({}, 0)
    for path in sorted(paths, key=str):
        data = stable_read(path, started)
        total += len(data)
        require(total <= MAX_RUNTIME_BYTES, "Finite isolated runtime byte count")
        mapping[str(path)] = hashlib.sha256(data).hexdigest()
    return (mapping, total)


def loaded_runtime_check(runtime, started):
    origins = set()
    for module in tuple(sys.modules.values()):
        guard(started)
        spec = getattr(module, "__spec__", None)
        origin = getattr(spec, "origin", None)
        if origin in (None, "built-in", "frozen"):
            continue
        path = Path(origin)
        require(
            path.is_absolute() and path.resolve(strict=True) == path,
            "Loaded runtime origin has no lexical alias",
        )
        require(str(path) in runtime, "Every imported runtime module has a frozen input")
        origins.add(str(path))
        cache = getattr(spec, "cached", None)
        if cache:
            cache_path = Path(cache)
            require(cache_path.is_absolute(), "Declared loaded cache has an absolute route")
            if cache_path.exists():
                require(
                    cache_path.resolve(strict=True) == cache_path and str(cache_path) in runtime,
                    "Existing imported bytecode is exact and frozen",
                )
            else:
                require(not cache_path.is_symlink(), "No dangling alias for absent loaded cache")
                _ABSENT_CACHES.add(cache_path)
    require(
        not any((path.exists() or path.is_symlink() for path in _ABSENT_CACHES)),
        "Every declared absent loaded cache remains absent",
    )
    return len(origins)


def exact_relative_key(key):
    require(
        type(key) is str
        and key
        and not Path(key).is_absolute()
        and not Path(key).drive
        and "\\" not in key
        and all(part not in ("", ".", "..") for part in key.split("/"))
        and Path(key).as_posix() == key,
        "Exact slash-relative historical member spelling",
    )


def historical_map(mapping, count, started, row_objects=False, absolute_keys=False, legacy=False):
    """Validate archived literal maps only; never hash their unselected dependencies."""
    require(type(mapping) is dict and len(mapping) == count, "Complete retained historical map")
    for key, value in mapping.items():
        guard(started)
        require(type(key) is str and key, "Literal historical map key")
        if Path(key).is_absolute():
            require(absolute_keys, "Absolute spelling only in declared historical scope")
            require(".." not in Path(key).parts, "No historical absolute traversal")
        elif legacy:
            require(
                "/" not in key
                and not Path(key).drive
                and all(part not in ("", ".", "..") for part in key.split("\\")),
                "Only original ROOT-integrity Windows-relative literal keys",
            )
        else:
            exact_relative_key(key)
        if row_objects:
            require(
                type(value) is dict
                and set(value) == {"sha256", "bytes"}
                and type(value["bytes"]) is int
                and value["bytes"] >= 0,
                "Exact archived SHA/byte record shape",
            )
            value = value["sha256"]
        require(type(value) is str and SHA.fullmatch(value), "Original literal expected SHA")


def merge_expected(target, source, started):
    for key, expected in source.items():
        guard(started)
        require(type(expected) is str and SHA.fullmatch(expected), "Exact externally expected SHA")
        require(
            key not in target or target[key] == expected,
            "No conflicting or substituted expectation",
        )
        target[key] = expected


def preserve_failure(error, started):
    """Every owned incomplete attempt is authoritative; no failed packet is resealed."""
    if not _ATTEMPT_ROUTE_OWNED or not OUTPUT.is_dir():
        return
    try:
        guard(started)
        if not (OUTPUT / "failure.json").exists() and not (OUTPUT / "manifest.json").exists():
            write_json(
                OUTPUT / "failure.json",
                {
                    "failed": True,
                    "passed": False,
                    "completed": False,
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "observed_CPU": time.process_time(),
                    "observed_wall": time.monotonic() - started,
                    "no_partial_scientific_approval": True,
                    "original_expected_hashes_waived": False,
                    "fixture_credit": 0,
                    "finance_execution": False,
                },
                started,
            )
    except BaseException:
        pass
    try:
        require(OUTPUT.resolve(strict=True) == OUTPUT, "Confined failed attempt route")
        members = set(OUTPUT.iterdir())
        payload = b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"fixture_credit":0,"finance_execution":false}\n'
        require(
            all(path.is_file() and path.resolve(strict=True) == path for path in members)
            and len(members) + 1 <= MAX_OWNED_FILES
            and sum(path.stat().st_size for path in members) + len(payload) <= MAX_OWNED_BYTES,
            "Fixed failure marker remains inside inclusive owned limits",
        )
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(payload)
    except (OSError, ValueError):
        pass


def lookup_shared(p, address, outs, table, bits):
    """Apply out[j] ^= table[address mod 2**bits][j], modulo output widths.

    Unlisted rows are zero, matching the historical equality-scan circuit.
    A prefix P splits into P*x and P*(1-x) using one clean target, two
    Toffolis and two CNOTs for compute, sibling switch, and cleanup.
    """
    if type(bits) is not int or not 0 <= bits <= len(address):
        raise ValueError("lookup bits must fit the address register")
    if not outs or any(not out for out in outs):
        raise ValueError("lookup requires nonempty output registers")
    wires = list(address) + [wire for out in outs for wire in out]
    if len(set(wires)) != len(wires):
        raise ValueError("lookup address and outputs must be disjoint")
    if not table or len(table) > 1 << bits or any(len(row) != len(outs) for row in table):
        raise ValueError("lookup table shape does not match the interface")

    masks = [(1 << len(out)) - 1 for out in outs]
    rows = [tuple(int(value) & mask for value, mask in zip(row, masks)) for row in table]
    rows += [tuple(0 for _ in outs)] * ((1 << bits) - len(rows))
    base = rows[0]
    for out, value in zip(outs, base):
        for bit, wire in enumerate(out):
            if (value >> bit) & 1:
                p.gate(wire)
    residual = [tuple(a ^ b for a, b in zip(row, base)) for row in rows]
    if bits == 0 or not any(any(row) for row in residual):
        return

    # Allocate only a reusable stack, rather than one flag for each table row.
    scratch = p.register(bits - 1) if bits > 1 else ()

    def emit_row(index, control):
        for out, value in zip(outs, residual[index]):
            for bit, wire in enumerate(out):
                if (value >> bit) & 1:
                    p.gate(control, wire)

    def visit(level, prefix, start):
        if not any(any(row) for row in residual[start : start + (1 << (level + 1))]):
            return
        if level < 0:
            emit_row(start, prefix)
            return
        flag = scratch[level]
        bit = address[level]
        p.gate(prefix, bit, flag)
        visit(level - 1, flag, start + (1 << level))
        p.gate(prefix, flag)
        visit(level - 1, flag, start)
        p.gate(prefix, flag)
        p.gate(prefix, bit, flag)

    high = address[bits - 1]
    visit(bits - 2, high, 1 << (bits - 1))
    p.gate(high)
    visit(bits - 2, high, 0)
    p.gate(high)


def lookup_naive(p, address, outs, table, bits):
    require(type(bits) is int and bits == 6, "Exactly six selected address bits")
    args = [address]
    params = {"table": table}
    scratch = p.register(5)
    require(
        len(args) == 1 and len(outs) == 8 and (set(params) == {"table"}) and (len(scratch) >= 5),
        "One fixed full72-address eight-output QROM",
    )
    table, address, prefix = (params["table"], args[0], scratch[:5])
    require(
        type(table) is list
        and len(table) == 64
        and all((type(row) is list and len(row) == 8 for row in table)),
        "Complete512 literal table",
    )
    for index, row in enumerate(table):
        p.checkpoint()
        negative = [bit for bit in range(6) if not index >> bit & 1]
        for bit in negative:
            p.gate(address[bit])
        p.gate(address[0], address[1], prefix[0])
        for bit in range(2, 6):
            p.gate(prefix[bit - 2], address[bit], prefix[bit - 1])
        for word, bank in zip(row, outs, strict=True):
            require(type(word) is int and -(1 << 71) <= word < 1 << 71, "Full72 lookup literal")
            raw = word & (1 << 72) - 1
            for bit in range(72):
                p.checkpoint()
                if raw >> bit & 1:
                    p.gate(prefix[4], bank[bit])
        for bit in range(5, 1, -1):
            p.gate(prefix[bit - 2], address[bit], prefix[bit - 1])
        p.gate(address[0], address[1], prefix[0])
        for bit in reversed(negative):
            p.gate(address[bit])


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


if __name__ == "__main__":
    main()
