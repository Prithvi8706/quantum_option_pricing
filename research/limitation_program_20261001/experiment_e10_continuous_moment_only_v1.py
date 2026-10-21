"""E10 continuous C4/H8 moment certificate only. Separate ROOT release required.
Authoring must not import or execute this module. No schedule, pilot, price,
fitting, sampling, source emission, finite-law bridge or performance winner.
"""
import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "experiment_e10_continuous_moment_only_v1.py"
METHOD_DOC = RESEARCH / "E10_CONTINUOUS_MOMENT_ONLY_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "e10_continuous_moment_only_preflight_v1.json"
READY = ROOT / ".context/E10_CONTINUOUS_MOMENT_ONLY_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "E10_continuous_moment_only_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
FOREIGN_ADMISSION = ROOT / ".context/INDEPENDENT_110_TERMINAL_HANDOFF_ROOT_SCOPED_ADMISSION_run001.json"
FOREIGN_ADMISSION_SHA = "284cece7e500025dfe9cddcc28860ec7f57e97973deda7c934d5ae9ed4e294c6"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 4096, 512 * 1024**2
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
MAX_REDUCED_RATIONAL_BITS = 131072
MAX_EXP_ENDPOINTS = 4096
MAX_TERM_REFERENCES = 12000
FAILURE_NAMES = ("FAILED_UNSEALED.json", "failed_unsealed.json", "failure.json", "run_failure.json", "prepare_failure.json")
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_FULL_ADMISSION = False
FIXED_EVALUATIONS = (("C4", 80, 128), ("C4", 160, 256), ("H8", 160, 256))
FIXED_CONTROLS = ("constant_price_exact_zero", "single_lognormal_shared_exponent_exact_zero",
                  "two_independent_lognormals_identity", "reject_elapsed_future_dates",
                  "reject_missing_clipped_policy")
MODEL_SOURCE_KEY = "research/compound_feasibility/model.py"
MODEL_SOURCE_SHA = "ebf32b30aaf9424e38cc03d3afacdc89aea352215e2b4e418b8a039983d2d3d9"
DERIVATION_KEY = "docs/controlled_residual_feasibility/DERIVATION.md"
DERIVATION_SHA = "dd2e7fd510572c7451110356d996bf41ddf62b63f1b936a1a30e86d6a7666822"
SOURCE_TOKENS = {
 "C4": {"assets": "4", "dates": "12", "sigma": ".2", "rho": ".2", "maturity": "1.",
        "strike": "100.", "spot": "100.", "rate": ".03"},
 "H8": {"assets": "8", "dates": "24", "sigma": ".4", "rho": ".2", "maturity": "3.",
        "strike": "100.", "spot": "100.", "rate": ".03"},
}
POLICY_PREMISES = {
 "conditional_clipping": "L<=V<=U", "continuation_interval": "g<=L<=C<=U<=c0",
 "geometric_control": "g=q*E[(G-k)+|X]", "forward_plus_put": "c0=F+Pg",
 "residual": "Y=1(V>Kc)*(h-R)", "shift": "h=c0-V",
 "complement": "R=q*((k-G)+-(k-A)+)",
 "Kc_dollars_exact": [6, 1], "inner_strike_dollars_exact": [100, 1],
 "accrued_average_nonnegative": True, "future_average_equal_weights": True,
 "proof_conditional_on_premises_not_policy_code_validation": True,
}
SEMANTIC_SCOPE = {
 "law": "Continuous GBM mathematical Gaussian laws with common rho/sigma/r and ordered contractual future-date family",
 "parameter_values": "Outward hull of exact intended decimals and exact legacy binary64 source-literal dyadics",
 "date_values": "Hull of exact k*T/dates and legacy binary64 integer-times-maturity/division date values",
 "covariance_hull": "Entrywise interval enclosure of that legitimate common-parameter family, not assertion arbitrary entries are Gaussian covariances",
 "excluded": ["Intermediate legacy floating evaluation", "finite Box-Muller/input law", "guarded/clipped digital source Y_d",
              "L2 bridge", "policy regression or finite policy rounding", "full financial price", "estimator schedule", "performance winner"],
}

OWNER_EXPECTATIONS = {'C12': {'complete_literal_maps': {'files': {'RUN_STARTED.json': 'c3bf45c68c5e695e57d88b4674f6db90757259076b993a84afa021c138274d82',
                                             'completion_outcome.json': '8bb545c033c77bbd14f263ad9786e0f8d7add0127ca085bc3b2d8129395eb930',
                                             'evidence_families.json': 'a88f07c529f6fd5ea04c80cc582733df32aef34075747d96f9c3504784492c6a',
                                             'existing_evidence_accounting.json': '025b2ab9c68c9200741b32126a9ce03a10ddd120dfb2dd6d3b0cce8c18db5b7a',
                                             'negative_inventory_controls.json': 'bb3650af7e053fbe65ff0fc3ef46e3d34108d6f3448fa1c4ad8419240f6316cf',
                                             'protocol.json': 'c8a3257aae08231eee1d4a765d8e3ee91dcfd041bda781868768f7587a6ba10e',
                                             'shared_module_graph.json': 'a4c9d84839beb0a1dd3920dba5a477d67e80974a1dbac204329c498740689d36',
                                             'summary.json': '8bb545c033c77bbd14f263ad9786e0f8d7add0127ca085bc3b2d8129395eb930'},
                                   'frozen_corpus_sha256': {'docs/antithetic_feasibility/RESULTS.md': {'bytes': 28027,
                                                                                                       'sha256': 'fd7dedf1586e4e5a23cbe136e701021a860085f28058f87948741d90d0232cfb'},
                                                            'docs/compound_feasibility/RESULTS.md': {'bytes': 22734,
                                                                                                     'sha256': 'c97e3d9137bc1dbae4b5df167e93d2fa4afe65068b2dfe7d10a2a766b5a2dce5'},
                                                            'docs/controlled_priority_completion/RESULTS.md': {'bytes': 7944,
                                                                                                               'sha256': '16d2d836797ebba08accb5c6ddaee3671a831a76213e4ccc3650d4263743a22e'},
                                                            'docs/controlled_residual_feasibility/RESULTS.md': {'bytes': 16179,
                                                                                                                'sha256': '20e2afe6e97acc0f9d85d6f6d5c0ab53273b51dd239ee7b4a058ca024e097ace'},
                                                            'docs/controlled_source_completion/RESULTS.md': {'bytes': 15149,
                                                                                                             'sha256': '5241de46734c18e37c566b2897a224e0a2da6a79c20990b23bc84250c2cf4980'},
                                                            'docs/independent_110_20261004/C12/peer_run001/ARITHMETIC_EVIDENCE_STATIC_REVIEW.md': {'bytes': 13775,
                                                                                                                                                   'sha256': '58e677c21fb87477631df1df0e8ab66955894d83c7bd23fc28f502a36ad1329e'},
                                                            'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt': {'bytes': 11398,
                                                                                                                             'sha256': 'faa8e4776a6b1c6487803dd61894fc67b419cb48474a8e1879b370561adc3ad2'},
                                                            'docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md': {'bytes': 10738,
                                                                                                                        'sha256': '3adbab8fdf17cce1e0c9ba88b04bb8d47aa1a0ff79b402e754d0907ff77957d6'},
                                                            'docs/limitation_audit_20261001/implementation_plan/CONTRACT.md': {'bytes': 21086,
                                                                                                                               'sha256': 'c90588139c60a1cf820c26c4051c16661309d714e2947a3257a5773c3e8e2ce2'},
                                                            'docs/limitation_audit_20261001/implementation_plan/roadmap.json': {'bytes': 399383,
                                                                                                                                'sha256': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a'},
                                                            'docs/research_investigation/2026-09-23/ERRATA.md': {'bytes': 8051,
                                                                                                                 'sha256': 'e234166de9eed1b437bf12cac08d916a919fff4c65084f6ae16b48af8abea879'},
                                                            'docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md': {'bytes': 8495,
                                                                                                                               'sha256': '5063d89a864115233c1a9ae57a8b599b58c077b5bc7fb170452b47dbb1022e6e'},
                                                            'manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md': {'bytes': 8862,
                                                                                                                            'sha256': '263ba1f8babdd735287b28807c6bbcb676b603bbc4c0a7d00d904c5a25fc1c4c'},
                                                            'manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md': {'bytes': 36916,
                                                                                                                             'sha256': 'b3798f7c44a5bbc6c95d710ba38d5e713d6614294581543bbcaf18a2dfdf0637'},
                                                            'research/advantage_frontier_20260923/barrier_oracle_depth.py': {'bytes': 6262,
                                                                                                                             'sha256': '1e0e225131c668f133ef05a5de3f78fbad4fb5307a2fc8c452d99d14c8dda929'},
                                                            'research/antithetic_feasibility/compile_blocks.py': {'bytes': 3829,
                                                                                                                  'sha256': '3d38bb0d30305a79b399a7eb75e2f7cbaff0827de1b11ac7cf6e46e309ab30d6'},
                                                            'research/antithetic_feasibility/estimator.py': {'bytes': 4226,
                                                                                                             'sha256': 'bb30174c51ef125766fe86906c66f1e2a2d61fb77fde2946825f865e31f7a10a'},
                                                            'research/antithetic_feasibility/reversible.py': {'bytes': 6150,
                                                                                                              'sha256': '5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a'},
                                                            'research/compound_feasibility/compile.py': {'bytes': 1676,
                                                                                                         'sha256': '7ed1e838347930d6bd5c8baefdf4bebb727bed2c4b6965579496d78989b04439'},
                                                            'research/compound_feasibility/model.py': {'bytes': 5865,
                                                                                                       'sha256': 'ebf32b30aaf9424e38cc03d3afacdc89aea352215e2b4e418b8a039983d2d3d9'},
                                                            'research/compound_feasibility/reversible.py': {'bytes': 1400,
                                                                                                            'sha256': 'ad052ac4cfc560bb127110f6c13d5edf99e4c9ab794f4207769225893a1a44bf'},
                                                            'research/controlled_completion_followup/test_truncated_multiplier.py': {'bytes': 1494,
                                                                                                                                     'sha256': '251a6e0e0997f826edb7e0436a0f6b5292e98f6eb738bf70fdc24889b701cf42'},
                                                            'research/controlled_completion_followup/truncated_multiplier.py': {'bytes': 3772,
                                                                                                                                'sha256': 'ef4c219118dbf4ad431444c61d970193f7265e0d5a82e93c086a3768e58e59f6'},
                                                            'research/controlled_priority_completion/ranged_multiplier.py': {'bytes': 4095,
                                                                                                                             'sha256': '660e8fb899d09901db663616c4d30e2e278575bbb1589e6f56ba26eff7e27d33'},
                                                            'research/controlled_priority_completion/ranged_run.py': {'bytes': 4556,
                                                                                                                      'sha256': 'a5884411c2ddb75cbc24a3194c48694e46a0d76bf2fd19badf2b8d9dd0e9a78e'},
                                                            'research/controlled_residual_feasibility/bounds.py': {'bytes': 4637,
                                                                                                                   'sha256': 'b314bed79b330f47acf231e0e358fd3bc04fa1de2ccea8f7ec5674a4d52273ee'},
                                                            'research/controlled_residual_feasibility/cost.py': {'bytes': 6573,
                                                                                                                 'sha256': '428b94de94ceef60c6b1957e4861ca3f97e61345dd8b2186b9c764712d68905a'},
                                                            'research/controlled_source_completion/carry_save_multiplier.py': {'bytes': 2764,
                                                                                                                               'sha256': 'e006efe9b1a72e282dad43e29998425dc1722b20d9d3d22c796f809414e3b23d'},
                                                            'research/controlled_source_completion/compiler.py': {'bytes': 12549,
                                                                                                                  'sha256': '1c5aa68dceab3cee9b7e89f4144b2bd6138bf4ed0d2f6b06603a520f706949c9'},
                                                            'research/controlled_source_completion/constant_multiplier.py': {'bytes': 5696,
                                                                                                                             'sha256': '625619ede05d6470b877c30f6081d358a5a437cd98454f9e29a444b7c142eaab'},
                                                            'research/controlled_source_completion/exact_lookup.py': {'bytes': 2807,
                                                                                                                      'sha256': 'a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c'},
                                                            'research/controlled_source_completion/finance.py': {'bytes': 8297,
                                                                                                                 'sha256': '75f107e041a2b7fa7e1a6dfce471369549af96a18ae7852d212ca0e2b442f77b'},
                                                            'research/controlled_source_completion/ir.py': {'bytes': 7121,
                                                                                                            'sha256': '3a4af54bd2e439ef060b747ea8f26a0897ce9e4a119509b57fb018d936d5d223'},
                                                            'research/controlled_source_completion/primitives.py': {'bytes': 10504,
                                                                                                                    'sha256': '02b983af3f5afb538f5448aad372e214f6a3740a0c19fb017d633e302a278daf'},
                                                            'research/controlled_source_completion/run.py': {'bytes': 3952,
                                                                                                             'sha256': '8857a1904d6c910b01f256547d5359d2b42f0152ed792365744138c806c9e6f7'},
                                                            'research/independent_110_20261004/C12/audit_evidence_family_v1.py': {'bytes': 24608,
                                                                                                                                  'sha256': '48cd6159b8d575ca6b0e060572c53f8f891a1a829ef522ce928775519c0ef751'},
                                                            'research/independent_110_20261004/C12/audit_evidence_family_v2.py': {'bytes': 26487,
                                                                                                                                  'sha256': '75d8a04d4222c075b53f4611bc7dc82c15d2f6f19b1d814fb7e92178d870d0f5'},
                                                            'research/independent_110_20261004/C12/evidence_family_data_v1.json': {'bytes': 12215,
                                                                                                                                   'sha256': '4670e53d559a58841d4a3ffe264bbe85e72caa68966de2cc798ceaaededfa624'},
                                                            'research/independent_110_20261004/C12/peer_run001/selected_evidence.json': {'bytes': 7655,
                                                                                                                                         'sha256': 'fa93e600b4a11b3d363ccb7065d9d3cdd4571713825d3199498a0c12483e2f7c'},
                                                            'research/journal_sprint/reversible_fixed_point.py': {'bytes': 11610,
                                                                                                                  'sha256': '52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b'},
                                                            'research/limitation_audit_20261001/experiment_constant_multiplier.py': {'bytes': 10719,
                                                                                                                                     'sha256': 'aa5f505c2fffc09d03b8bb8315d2057493b4d6f73a635b9936b2bb848f501e01'},
                                                            'research/limitation_audit_20261001/experiment_lookup.py': {'bytes': 7709,
                                                                                                                        'sha256': '10d9a7dee3998647e008349735fe417426c6d41e33682297b19601c88ef0a2c7'},
                                                            'research/limitation_audit_20261001/experiment_mcx_cleanup.py': {'bytes': 5384,
                                                                                                                             'sha256': 'f04557b714c30a24063b9830e6bb8f6b4c4cc76392dbe941a71d1339cf3566ae'},
                                                            'research/limitation_audit_20261001/experiment_multiplier.py': {'bytes': 6152,
                                                                                                                            'sha256': 'b3f9552f1b91ac86c95c0e0d2ccdba1d9c631bae888016435aa2dba3717582d2'},
                                                            'research/limitation_audit_20261001/test_carry_save_multiplier.py': {'bytes': 1685,
                                                                                                                                 'sha256': '9a5f51417cc2a6ede8ab58a52bb02e43b3d407a4c82c4d5bc87cf7f5835b92ec'},
                                                            'research/limitation_audit_20261001/test_constant_multiplier.py': {'bytes': 7654,
                                                                                                                               'sha256': '854ee475bb8102955f494c31e373de0d1a69874a0a6863fa6de8b280df191127'},
                                                            'research/limitation_audit_20261001/test_lookup.py': {'bytes': 6282,
                                                                                                                  'sha256': '5151759869d1774008fd29f78e1a908db0afca489ce32763248b872000cc24a4'},
                                                            'research/stronger_arithmetic/circuits.py': {'bytes': 9296,
                                                                                                         'sha256': 'd9fbeb606e8a3b0ad928cd9b63f4b4b8aeddef245511f695b83993e7193706f2'},
                                                            'results/frontier_completion_20260927/stage_a/B4x12/target.json': {'bytes': 321011,
                                                                                                                               'sha256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'},
                                                            'results/frontier_completion_20260927/stage_a/B8x52/target.json': {'bytes': 2671579,
                                                                                                                               'sha256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'},
                                                            'results/independent_110_20261004/C12/audit_run001/STATIC_REJECTED_BEFORE_CHECKS.json': {'bytes': 622,
                                                                                                                                                     'sha256': '224e54a663910a0c4578aba914c6935115d9a080b1a3fb9876132d70afb5d035'},
                                                            'results/independent_110_20261004/C12/audit_run001/protocol.json': {'bytes': 13816,
                                                                                                                                'sha256': 'bbd9bee8f5dd19f42f8dbe888b1bc13e0c9a675d7b75223bdc5b5a232dca1aff'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/B4x12/signed-digit-carry-save/target.json': {'bytes': 321011,
                                                                                                                                                                   'sha256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/B8x52/signed-digit-carry-save/target.json': {'bytes': 2671579,
                                                                                                                                                                   'sha256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/executed_experiment_constant_multiplier.py': {'bytes': 10637,
                                                                                                                                                                    'sha256': '2a0aeaa2d0d440ea0113869fdbe93a40b16bdb181f047859202a18841ca79c44'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/protocol.json': {'bytes': 913,
                                                                                                                                       'sha256': '92e532c4f2afc93b3bc9cf3e83400585e31d6cdaf056c1870bb6363a95a97c49'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/summary.json': {'bytes': 42067,
                                                                                                                                      'sha256': '214bdc3513ffab4a6c2135f4749b8584407c52b6c9739ada0a03c350f1eff12d'},
                                                            'results/limitation_audit_20261001/constant_multiplier_v1/verification.json': {'bytes': 4240,
                                                                                                                                           'sha256': '2b1c5437ca62fc8689879f82ea24606b80cda75fdbfad17a06a657e496cf61d0'},
                                                            'results/limitation_audit_20261001/lookup_v2/B4x12/target.json': {'bytes': 321011,
                                                                                                                              'sha256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'},
                                                            'results/limitation_audit_20261001/lookup_v2/B8x52/target.json': {'bytes': 2671579,
                                                                                                                              'sha256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'},
                                                            'results/limitation_audit_20261001/lookup_v2/protocol.json': {'bytes': 500,
                                                                                                                          'sha256': 'c1988368deb4561e4f35395215e85cb9e0aa64576320d30a54bd42a636d03a72'},
                                                            'results/limitation_audit_20261001/lookup_v2/summary.json': {'bytes': 43685,
                                                                                                                         'sha256': 'b3485bf1789c1cea2228407045864a578cbd66c00042ea523baa2abd5c962131'},
                                                            'results/limitation_audit_20261001/mcx_cleanup_v1/mcx5.qasm': {'bytes': 385,
                                                                                                                           'sha256': '6d92d17f84539ccb357d0c2a052f95d984560a06b634436c82f9b8e6e5ddf698'},
                                                            'results/limitation_audit_20261001/mcx_cleanup_v1/result.json': {'bytes': 1168,
                                                                                                                             'sha256': '2c97bf54e160324a8c68942b708b64f60effdd7ef216fe5e08162e38a1f2f46e'},
                                                            'results/limitation_audit_20261001/multiplier_v2/B4x12/target.json': {'bytes': 321011,
                                                                                                                                  'sha256': 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'},
                                                            'results/limitation_audit_20261001/multiplier_v2/B8x52/target.json': {'bytes': 2671579,
                                                                                                                                  'sha256': '267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b'},
                                                            'results/limitation_audit_20261001/multiplier_v2/protocol.json': {'bytes': 584,
                                                                                                                              'sha256': '556a8a11ddc087da70ab57a3dec71510acae85f31582170078f7dc9d18b470a7'},
                                                            'results/limitation_audit_20261001/multiplier_v2/summary.json': {'bytes': 48932,
                                                                                                                             'sha256': '039636700146db298583b1650aad144cc7affab97851d9123b19775a3e3a41e4'}}},
         'complete_map_counts': {'files': 8, 'frozen_corpus_sha256': 68},
         'complete_map_object_SHA256': {'files': 'a05a627ce7abdb0e05e2bab1a8f93f999a2b45249f3d32c692d9629b975e2f88',
                                        'frozen_corpus_sha256': '9efe0b1468b8fccba5b8fe7bc261a417a7aaee854c748298b9c952b8fd00b0f4'},
         'directory': 'results/independent_110_20261004/C12/audit_run002',
         'files_key_scope': 'RECEIPT_RELATIVE',
         'history_scope': 'Only original explicit failed C12 references; no recursive runtime promotion',
         'inclusive_owned_count': 9,
         'manifest_SHA256': 'b9006f673150825f10954ac896e7048c24ed260db7d6455db002b10a3d7bf866',
         'map_fields': ['files', 'frozen_corpus_sha256']},
 'E16': {'complete_literal_maps': {'files': {'results/independent_110_20261004/E16/scalar_run001/certificate.json': '151bac1e5bb6802f6fb2cb6ce3e1bd5dad1f1070d44f932dd7a60af575da4bb6',
                                             'results/independent_110_20261004/E16/scalar_run001/comparison.json': '484ec0ed08b1ed7165e30fc259b066615792873593199418fcf82755c75f52c8',
                                             'results/independent_110_20261004/E16/scalar_run001/protocol.json': '7a674d5385a6888ebc421fd736725dca10217ac12fe3430808eb7f5af9198ece',
                                             'results/independent_110_20261004/E16/scalar_run001/run_started.json': 'da5ab96a4fff62e85d6b5820f4557fb9b19d19828fe727cab6d323719969475b',
                                             'results/independent_110_20261004/E16/scalar_run001/scalar_accounting.json': '51c5c8d70438a4441a1bb960a592266f7acff23c8bb2b4a8350058e662da5a32'},
                                   'frozen_inputs': {'docs/controlled_residual_feasibility/DERIVATION.md': {'bytes': 6956,
                                                                                                            'sha256': 'dd2e7fd510572c7451110356d996bf41ddf62b63f1b936a1a30e86d6a7666822'},
                                                     'docs/independent_110_20261004/E09/primary_sources/BHMT_quant_ph_0005055v1.pdf': {'bytes': 295305,
                                                                                                                                       'sha256': 'badedce80b0fe53e6cd93f915ce79c9680e375bb6565f83d2f572bc4114b0278'},
                                                     'docs/independent_110_20261004/E16/PROTOCOL.json': {'bytes': 3223,
                                                                                                         'sha256': 'a29e8302d88c3a19b210acfd6daedde1ae8d04682c0df298eb3a7e1da0ccb63f'},
                                                     'docs/independent_110_20261004/E16/SCALAR_PROOF.md': {'bytes': 5220,
                                                                                                           'sha256': '78da7c37484aa06bcad4b8ec2cb6d97418b9f86019a021d13b482d34e2110215'},
                                                     'docs/independent_110_20261004/E16/primary_sources/Hamoudi_2108_12172v1.pdf': {'bytes': 678072,
                                                                                                                                    'sha256': '7c9cb639136939d9152bef88e5aa828e00ae8570fed88edd894a17ad0443728b'},
                                                     'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt': {'bytes': 11398,
                                                                                                                      'sha256': 'faa8e4776a6b1c6487803dd61894fc67b419cb48474a8e1879b370561adc3ad2'},
                                                     'docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md': {'bytes': 35051,
                                                                                                                        'sha256': 'e5189e840fc88fa1a1f73b08659c76257aa84c916b6873a8730ec9f7c53c6fad'},
                                                     'docs/limitation_audit_20261001/implementation_plan/roadmap.json': {'bytes': 399383,
                                                                                                                         'sha256': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a'},
                                                     'research/compound_feasibility/model.py': {'bytes': 5865,
                                                                                                'sha256': 'ebf32b30aaf9424e38cc03d3afacdc89aea352215e2b4e418b8a039983d2d3d9'},
                                                     'research/controlled_source_completion/finance.py': {'bytes': 8297,
                                                                                                          'sha256': '75f107e041a2b7fa7e1a6dfce471369549af96a18ae7852d212ca0e2b442f77b'},
                                                     'research/independent_110_20261004/E16/author_helper.py': {'bytes': 901,
                                                                                                                'sha256': '029aceaf9cbef62789657ba674c3782475ad3ba7e88cf5494abf99139f9a0221'},
                                                     'research/independent_110_20261004/E16/interval_helper.py': {'bytes': 1955,
                                                                                                                  'sha256': 'b1b74f199087e5cf8ebc3a0ba1a1b6a0224fb923cb4d964d717fa58624b8fb53'},
                                                     'research/independent_110_20261004/E16/scalar_screen.py': {'bytes': 11002,
                                                                                                                'sha256': '7cf18926d8ff3ab6742d6bfe555ccd33ff0ed8434f33c527811a213f5a3555f9'},
                                                     'research/independent_110_20261004/F23/screen_covariance_compression.py': {'bytes': 15602,
                                                                                                                                'sha256': '716dbae4a01bb8f89fe49cd63fe68f7980a251d3356aae239d73998249a7bd50'}},
                                   'selected_runtime': {'C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python.exe': {'bytes': 103704,
                                                                                                                                      'sha256': 'fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b'},
                                                        'C:\\Users\\prith\\quantum_option_pricing\\.context\\frontier_t0_env\\Scripts\\python.exe': {'bytes': 270104,
                                                                                                                                                     'sha256': '41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5'}}},
         'complete_map_counts': {'files': 5, 'frozen_inputs': 14, 'selected_runtime': 2},
         'complete_map_object_SHA256': {'files': '1d8d5f4d064b7ba6c073627a94878f0d659fad605549c21f02a81e22564c060b',
                                        'frozen_inputs': '732280705e6502104ce70acc7a34b94f385de3c93b12c1605dfb37f50a68a76c',
                                        'selected_runtime': '84fd76c6080417e5731050ecb8fceeaa3774676b1afd341ae11598deb4715bd1'},
         'directory': 'results/independent_110_20261004/E16/scalar_run001',
         'files_key_scope': 'ROOT_RELATIVE',
         'history_scope': 'Only original explicit failed C12 references; no recursive runtime promotion',
         'inclusive_owned_count': 6,
         'manifest_SHA256': 'bc20052e68f0fe3a67d6830d832a1fcb01d61b3c4ec885bd21237291b3badaf0',
         'map_fields': ['files', 'frozen_inputs', 'selected_runtime']}}

SCIENTIFIC_CAPS = {'absolute_exp_argument_cap': 8,
 'each_fixed_endpoint_exp_width_at_most': '10^-requested_digits',
 'fixed_Taylor_terms': {'160': 256, '80': 128},
 'max_distinct_exp_endpoints_per_evaluation': 4096,
 'max_reduced_rational_numerator_or_denominator_bits': 131072,
 'max_term_references_per_evaluation': 12000,
 'no_adaptive_extra_terms_or_precision': True,
 'saved_exp_dyadic_bits_recipe': '4*requested_digits+32',
 'semantic_hull_width_not_subject_to_numerical_precision_threshold': True,
 'serialized_integer_bit_cap': 65536,
 'unreduced_fraction_operation_temporary_bit_bound': 524288}

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

def own_runtime():
    global _STANDARD_RUNTIME_MEMBERS
    invocation_check()
    members = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = members
    size = 0
    for path in sorted(members):
        budget()
        size += path.stat().st_size
        require(len(members) <= MAX_RUNTIME_FILES and size <= MAX_RUNTIME_BYTES,
                "Complete isolated4096-file/512MiB runtime")
        add(path, digest(path, fresh=True))
    return {"files": len(members), "bytes": size, "site_startup_disabled": True}

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


def flags():
    return dict(local_only=True, item="E10", continuous_moment_certificate_only=True,
                full_E10_completed=False, digital_moment_transfer=False, L2_bridge=False,
                estimator_schedule_emitted=False, source_emission=False, prices_or_paths_sampled=0,
                fits_or_pilots=0, cost_comparison=False, performance_winner=None,
                fixture_credit=0, new_global_fixture_credit=0, G2_transfer=False,
                full_price_certificate=False, physical_certificate=False, quantum_advantage=False)


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


def loaded_origins():
    forbidden = {"numpy", "scipy", "mpmath", "sympy", "numba", "pytest", "pandas"}
    require(not any(name.split(".", 1)[0] in forbidden or name.startswith("research.")
                    for name in sys.modules), "No scientific or historical module import")
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            path = Path(os.path.abspath(str(origin)))
            if not path.is_file():
                require(attribute == "__cached__" and not path.exists() and not path.is_symlink(),
                        "Only absent cache, never a missing source origin")
                if _FULL_ADMISSION:
                    require(path in _ABSENT_RUNTIME, "No postadmission cache-absence discovery")
                else:
                    require(path in _ABSENT_RUNTIME or
                            (path.is_relative_to(BASE / "Lib") and not path.is_relative_to(BASE / "Lib/site-packages")),
                            "Initial missing cache only in declared author or isolated stdlib scope")
                    _ABSENT_RUNTIME.add(path)
                continue
            actual = canonical(path, fresh=True)
            key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
            mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
            require(key in mapping, "Every loaded source/present cache has prior expected SHA")
            require(digest(actual, fresh=True, already_resolved=True) == mapping[key],
                    "Every loaded origin freshly equals its original admitted SHA")


def original_owner(name, expectation):
    directory = exact_key(expectation["directory"])
    manifest_path = directory / "manifest.json"
    packet = read(bind(manifest_path, expectation["manifest_SHA256"]))
    fields = [key for key in ("files", "frozen_corpus_sha256", "frozen_inputs", "selected_runtime") if key in packet]
    require(fields == expectation["map_fields"] and packet["completed"] is True and packet["passed"] is True,
            "Exact completed original scoped owner and map presence")
    owned = {manifest_path}
    for field in fields:
        mapping = packet[field]
        require(type(mapping) is dict and mapping == expectation["complete_literal_maps"][field]
                and len(mapping) == expectation["complete_map_counts"][field]
                and object_sha(mapping) == expectation["complete_map_object_SHA256"][field],
                "Entire original declared map, literal pins and counts unchanged")
        for key, record in mapping.items():
            budget(admission=True)
            if field == "files" and expectation["files_key_scope"] == "RECEIPT_RELATIVE":
                path = directory / key
                require(not Path(key).is_absolute() and ".." not in Path(key).parts, "Receipt-owned exact relative key")
            else:
                path = exact_key(key) if not Path(key).is_absolute() else Path(key)
            pin = record if type(record) is str else record["sha256"]
            actual = bind(path, pin)
            if type(record) is dict:
                require(actual.stat().st_size == record["bytes"], "Original declared byte count")
            if field == "files":
                require(actual.is_relative_to(directory) and actual not in owned, "Original owned inventory confined")
                owned.add(actual)
    require(len(owned) == expectation["inclusive_owned_count"] and inventory(directory) == owned,
            "Original complete physical owned inventory")
    require(not any((directory / marker).exists() for marker in FAILURE_NAMES), "No authoritative failure on completed owner")
    _OWN_INVENTORIES[directory] = owned
    return packet


def fresh_union():
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        require(canonical(lexical, fresh=True) == actual, "Every lexical input freshly remains physically confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = ROOT / key if not Path(key).is_absolute() else Path(key)
            require(path not in union or union[path] == pin, "Equal original expected-SHA union")
            union[path] = pin
    for path, pin in _OBSERVED.items():
        require(path not in union or union[path] == pin, "Observed never replaces original expected SHA")
        union[path] = pin
    require(len(union) <= MAX_REFERENCES, "Finite complete input union")
    size = 0
    for path, pin in sorted(union.items()):
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES and digest(actual, fresh=True, already_resolved=True) == pin,
                "Complete full fresh input bytes and expected SHA")
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, "Every complete historical inventory unchanged")
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS, "Complete isolated runtime membership unchanged")
    require(not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME), "Every declared absent cache/zip remains absent")
    for path, pin in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == pin, "Externally declared present author cache unchanged")
    loaded_origins()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_physical_resolve_and_SHA": True,
            "absent_runtime_paths": sorted(str(path) for path in _ABSENT_RUNTIME),
            "prior_original_owned_inventories": {str(path): sorted(str(member) for member in members)
                                                 for path, members in _OWN_INVENTORIES.items()}}


def release(ready_sha):
    global _FULL_ADMISSION
    ready = read(bind(READY, ready_sha))
    require(ready["schema"] == "root-e10-continuous-moment-only-READY-v1" and ready["ready"] is True
            and ready["root_and_independent_static_reviews_passed"] is True
            and ready["continuous_moment_only_execution_authorized"] is True
            and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
            and ready["owner_expectations"] == OWNER_EXPECTATIONS
            and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL],
            "Separate exact ROOT/peer release before any output or moment computation")
    authors = ready["author_method_SHA256"]
    require(set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, "Exactly three externally frozen author files")
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(policy["schema"] == "e10-continuous-moment-only-preflight-v1"
            and policy["author_SHA256"] == authors[AUTHOR.name] and policy["method_SHA256"] == authors[METHOD_DOC.name]
            and policy["owner_expectations"] == OWNER_EXPECTATIONS
            and policy["fixed_evaluations"] == [list(row) for row in FIXED_EVALUATIONS]
            and policy["fixed_controls"] == list(FIXED_CONTROLS)
            and policy["semantic_scope"] == SEMANTIC_SCOPE and policy["policy_premises"] == POLICY_PREMISES
            and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
            and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
            and policy["reference_unique_hash_work_caps"] == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
            and policy["finite_scientific_caps"] == SCIENTIFIC_CAPS,
            "Exact fixed scope, evaluation/control identities and every declared guard")
    code_cache_policy(ready)
    for key, pin in ready["static_review_expected_SHA256"].items():
        require(key.startswith(".context/"), "ROOT-local independent/ROOT static review")
        bind(exact_key(key), pin)
    admission = read(bind(FOREIGN_ADMISSION, FOREIGN_ADMISSION_SHA))
    require(admission["declared_hash_maps_and_inventory_passed"] is True
            and admission["complete_runtime_closure_claimed"] is False,
            "Original foreign admission remains scoped metadata evidence")
    for name, expected in OWNER_EXPECTATIONS.items():
        joined = [row for row in admission["per_item_reconciliation_proposal"] if row["item"] == name]
        require(len(joined) == 1 and joined[0]["literal_expected_receipt_sha256"] == expected["manifest_SHA256"],
                "Two owner manifest pins joined to original ROOT foreign admission")
    loaded_origins()
    _FULL_ADMISSION = True
    return ready, policy



def rational_guard(value):
    budget()
    require(type(value) is Fraction and value.numerator.bit_length() <= MAX_REDUCED_RATIONAL_BITS
            and value.denominator.bit_length() <= MAX_REDUCED_RATIONAL_BITS,
            "Fixed reduced-rational numerator/denominator bit cap")
    return value


def interval(lo, hi=None):
    lo = rational_guard(Fraction(lo))
    hi = lo if hi is None else rational_guard(Fraction(hi))
    require(lo <= hi, "Ordered exact rational interval")
    return lo, hi


def plus(a, b):
    return interval(a[0] + b[0], a[1] + b[1])


def minus(a, b):
    return interval(a[0] - b[1], a[1] - b[0])


def times(a, b):
    products = [rational_guard(x * y) for x in a for y in b]
    return interval(min(products), max(products))


def scale(a, coefficient):
    coefficient = rational_guard(Fraction(coefficient))
    return times(a, interval(coefficient))


def average(values):
    require(values, "Nonempty finite average")
    answer = interval(0)
    for value in values:
        answer = plus(answer, value)
    return scale(answer, Fraction(1, len(values)))


def pair(value):
    rational_guard(value)
    return [value.numerator, value.denominator]


def interval_pair(value):
    return [pair(value[0]), pair(value[1])]


def exact_source_models():
    path = bind(exact_key(MODEL_SOURCE_KEY), MODEL_SOURCE_SHA)
    before = fingerprint(path)
    raw = path.read_bytes()
    require(fingerprint(path) == before and hashlib.sha256(raw).hexdigest() == MODEL_SOURCE_SHA,
            "Exact stable admitted model text, never imported or executed")
    tree = ast.parse(raw.decode("utf-8"))
    model = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Model")
    defaults = {node.target.id: node.value for node in model.body
                if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)}
    assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "MODELS" for target in node.targets))
    require(isinstance(assignment.value, ast.List) and len(assignment.value.elts) == 4,
            "Original four-model literal declaration")
    calls = assignment.value.elts
    require(isinstance(calls[0], ast.Call) and isinstance(calls[3], ast.Call)
            and isinstance(calls[0].func, ast.Name) and calls[0].func.id == "Model"
            and not calls[0].args and not calls[0].keywords and calls[3].func.id == "Model"
            and len(calls[3].args) == 6 and not calls[3].keywords
            and isinstance(calls[3].args[0], ast.Constant) and calls[3].args[0].value == "H8",
            "Exact C4 defaults and original H8 positional source model")
    output = {}
    for name in ("C4", "H8"):
        nodes = dict(defaults)
        if name == "H8":
            nodes.update(zip(("name", "assets", "dates", "sigma", "rho", "maturity"), calls[3].args))
        records, values = {}, {}
        for field, token in SOURCE_TOKENS[name].items():
            node = nodes[field]
            require(isinstance(node, ast.Constant) and type(node.value) in (int, float)
                    and ast.get_source_segment(raw.decode("utf-8"), node) == token,
                    "Exact original scalar source token and literal value kind")
            intended = Fraction(token)
            literal = Fraction(node.value) if type(node.value) is int else Fraction(*node.value.as_integer_ratio())
            values[field] = interval(min(intended, literal), max(intended, literal))
            records[field] = {"source_token": token, "intended_decimal_exact": pair(intended),
                              "legacy_literal_exact": pair(literal),
                              "legacy_literal_hex": None if type(node.value) is int else node.value.hex(),
                              "robust_parameter_hull": interval_pair(values[field])}
        require(values["assets"][0] == values["assets"][1] and values["dates"][0] == values["dates"][1]
                and values["maturity"][0] == values["maturity"][1]
                and values["spot"] == interval(100) and values["strike"] == interval(100),
                "Exact integer counts/maturity and common100-dollar spot/strike")
        require(interval(0)[0] <= values["rho"][0] <= values["rho"][1] <= interval(1)[0]
                and values["sigma"][0] >= 0, "Legitimate common equicorrelation/volatility family")
        output[name] = {"values": values, "records": records}
    return output


def future_date_family(model, recipe="absolute-contractual-future-dates"):
    require(recipe == "absolute-contractual-future-dates", "Exact absolute future-date recipe")
    values = model["values"]
    dates, maturity = int(values["dates"][0]), values["maturity"][0]
    require(dates % 2 == 0 and maturity.denominator == 1, "Original even dates and exact integer maturity")
    hulls, records = [], []
    for k in range(dates // 2 + 1, dates + 1):
        exact = rational_guard(Fraction(k, dates) * maturity)
        # Here integer k*maturity is exactly representable. This explicitly records
        # the old array expression's binary64 division, not an interval exp shortcut.
        legacy = Fraction(*((float(k) * float(maturity)) / float(dates)).as_integer_ratio())
        value = interval(min(exact, legacy), max(exact, legacy))
        require(value[0] > maturity / 2 and (not hulls or hulls[-1][1] < value[0]),
                "Original ordered absolute dates strictly after exercise")
        hulls.append(value)
        records.append({"contractual_index": k, "exact_contractual_date": pair(exact),
                        "legacy_binary64_date_exact": pair(legacy), "robust_date_hull": interval_pair(value)})
    return hulls, records


class RationalExpLedger:
    def __init__(self, digits, terms):
        require((digits, terms) in ((80, 128), (160, 256)), "Fixed two precisions and Taylor term counts")
        self.digits, self.terms, self.bits = digits, terms, 4 * digits + 32
        self.endpoint_cache, self.hull_cache = {}, {}
        self.endpoints, self.hulls = [], []

    def endpoint(self, x):
        x = rational_guard(Fraction(x))
        if x in self.endpoint_cache:
            return self.endpoint_cache[x]
        require(len(self.endpoints) < MAX_EXP_ENDPOINTS and abs(x) <= 8, "Finite fixed exp endpoint/domain cap")
        y, term, total = abs(x), Fraction(1), Fraction(1)
        for k in range(1, self.terms + 1):
            budget()
            term = rational_guard(term * y / k)
            total = rational_guard(total + term)
        next_term = rational_guard(term * y / (self.terms + 1))
        ratio = rational_guard(y / (self.terms + 2))
        require(0 <= ratio < 1 and total > 0, "Positive Taylor geometric remainder premise")
        remainder = rational_guard(next_term / (1 - ratio))
        lower, upper = total, rational_guard(total + remainder)
        if x < 0:
            lower, upper = rational_guard(1 / upper), rational_guard(1 / lower)
        lattice = 1 << self.bits
        lo_int = (lower.numerator * lattice) // lower.denominator
        hi_int = -((-upper.numerator * lattice) // upper.denominator)
        value = interval(Fraction(lo_int, lattice), Fraction(hi_int, lattice))
        width = rational_guard(value[1] - value[0])
        require(width <= Fraction(1, 10**self.digits), "Fixed-endpoint exp numerical width at requested digits")
        index = len(self.endpoints)
        record = {"id": index, "argument_exact": pair(x), "positive_argument_exact": pair(y),
                  "Taylor_terms_in_sum_including_k0": self.terms + 1, "Taylor_max_degree": self.terms,
                  "remainder_recipe": "t_(N+1)/(1-|x|/(N+2)); t0=1, t_k=t_(k-1)*|x|/k",
                  "negative_argument_rule": "[1/(S_N+R),1/S_N]" if x < 0 else None,
                  "outward_dyadic_bits": self.bits, "enclosure_exact": interval_pair(value),
                  "numerical_width_exact": pair(width), "numerical_width_requirement_passed": True}
        self.endpoints.append(record)
        self.endpoint_cache[x] = (index, value)
        return index, value

    def hull(self, argument):
        require(argument[0] <= argument[1], "Ordered exp argument hull")
        if argument in self.hull_cache:
            return self.hull_cache[argument]
        lo_id, lo = self.endpoint(argument[0])
        hi_id, hi = self.endpoint(argument[1])
        result = interval(lo[0], hi[1])
        semantic_width = interval(0) if argument[0] == argument[1] else interval(hi[0] - lo[1], hi[1] - lo[0])
        index = len(self.hulls)
        self.hulls.append({"id": index, "argument_hull_exact": interval_pair(argument),
                           "lower_endpoint_id": lo_id, "upper_endpoint_id": hi_id,
                           "exp_hull_exact": interval_pair(result),
                           "total_robust_exp_hull_width_exact": pair(result[1] - result[0]),
                           "parameter_endpoint_exp_separation_enclosure_exact": interval_pair(semantic_width),
                           "numerical_endpoint_widths_exact": [pair(lo[1] - lo[0]), pair(hi[1] - hi[0])],
                           "semantic_width_not_required_to_vanish_with_precision": True})
        self.hull_cache[argument] = (index, result)
        return index, result


def moment_terms(values, time_hulls, ledger):
    assets = int(values["assets"][0])
    times_by_component = [(value, asset, date) for date, value in enumerate(time_hulls) for asset in range(assets)]
    count = len(times_by_component)
    require(count > 0 and count * count + count + 1 <= MAX_TERM_REFERENCES, "Finite complete moment term references")
    rate, sigma, rho, spot = (values[key] for key in ("rate", "sigma", "rho", "spot"))
    sigma2 = times(sigma, sigma)
    drift = minus(rate, scale(sigma2, Fraction(1, 2)))
    covariance = []
    for ti, ai, _ in times_by_component:
        row = []
        for tj, aj, _ in times_by_component:
            minimum_time = interval(min(ti[0], tj[0]), min(ti[1], tj[1]))
            row.append(times(times(sigma2, minimum_time), interval(1) if ai == aj else rho))
        covariance.append(row)
    mean_t = average([entry[0] for entry in times_by_component])
    var_g = average([entry for row in covariance for entry in row])
    row_means = [average(row) for row in covariance]
    spot2 = times(spot, spot)
    require(spot2[0] == spot2[1], "Exact common initial spot factor")
    components, refs, combined = {}, {"EA2": [], "EAG": [], "EG2": []}, {}

    def append(category, argument, weight, sign, indices):
        budget()
        exp_id, enclosed = ledger.hull(argument)
        refs[category].append({"indices": indices, "exp_hull_id": exp_id, "equal_weight_exact": pair(weight)})
        combined[exp_id] = rational_guard(combined.get(exp_id, Fraction(0)) + sign * weight * spot2[0])
        return scale(enclosed, weight * spot2[0])

    components["EA2"] = interval(0)
    for i, (ti, _, _) in enumerate(times_by_component):
        for j, (tj, _, _) in enumerate(times_by_component):
            argument = plus(times(rate, plus(ti, tj)), covariance[i][j])
            components["EA2"] = plus(components["EA2"], append("EA2", argument, Fraction(1, count * count), 1, [i, j]))
    components["EAG"] = interval(0)
    for i, (ti, _, _) in enumerate(times_by_component):
        argument = plus(plus(times(rate, ti), times(drift, mean_t)), plus(scale(var_g, Fraction(1, 2)), row_means[i]))
        components["EAG"] = plus(components["EAG"], append("EAG", argument, Fraction(1, count), -2, [i]))
    argument = plus(scale(times(drift, mean_t), 2), scale(var_g, 2))
    components["EG2"] = append("EG2", argument, Fraction(1), 1, [])
    separate = plus(minus(components["EA2"], scale(components["EAG"], 2)), components["EG2"])
    grouped = interval(0)
    for exp_id, coefficient in sorted(combined.items()):
        budget()
        if coefficient:
            hull = ledger.hulls[exp_id]["exp_hull_exact"]
            grouped = plus(grouped, scale((Fraction(*hull[0]), Fraction(*hull[1])), coefficient))
    # Shared exponent grouping is exact symbolic coefficient cancellation, not a
    # numeric max masking cancellation. Both interval evaluations are valid.
    spread = interval(max(separate[0], grouped[0]), min(separate[1], grouped[1]))
    require(spread[1] >= 0, "Squared random-variable moment has nonnegative upper enclosure")
    nonnegative = interval(0 if spread[0] < 0 else spread[0], spread[1])
    return {"components": components, "references": refs, "separate_cancellation": separate,
            "shared_exponent_cancellation": grouped, "spread": nonnegative,
            "shared_coefficients": [{"exp_hull_id": key, "coefficient_exact": pair(value)} for key, value in sorted(combined.items())],
            "count": count, "covariance": covariance, "mean_t": mean_t, "var_g": var_g,
            "nonnegative_intersection_authority": "E[(A-G)^2]>=0 for each legitimate declared Gaussian law"}


def validate_policy(premises):
    require(premises == POLICY_PREMISES and premises["conditional_clipping"] == "L<=V<=U"
            and premises["continuation_interval"] == "g<=L<=C<=U<=c0",
            "Exact conditional clipping including V>=g and V<=c0")


def uniform_theorem():
    validate_policy(POLICY_PREMISES)
    return {"premises": POLICY_PREMISES, "derivation_SHA256": DERIVATION_SHA,
            "steps": ["AM-GM: 0<=R<=q*(A-G)", "V>=g and put-call parity: 0<=h=c0-V<=q*E[A-G|X]",
                      "Nonnegative h,R: (h-R)^2<=h^2+R^2", "Conditional Jensen: h^2<=q^2*E[(A-G)^2|X]",
                      "R^2<=q^2*(A-G)^2; 1(V>Kc)<=1", "Tower: E[Y^2]<=2*q^2*E[(A-G)^2]"],
            "applies_uniformly_to_every_policy_satisfying_premises": True,
            "actual_policy_code_or_digital_law_verified": False}


def certificate(name, digits, terms, model):
    start_cpu, start_wall = time.process_time(), time.monotonic()
    dates, date_records = future_date_family(model)
    ledger = RationalExpLedger(digits, terms)
    result = moment_terms(model["values"], dates, ledger)
    factor_arg = scale(times(model["values"]["rate"], model["values"]["maturity"]), -1)
    factor_id, factor_exp = ledger.hull(factor_arg)
    factor = scale(factor_exp, Fraction(1, 2))
    upper_moment = times(factor, result["spread"])
    numerical_width = max(Fraction(*row["numerical_width_exact"]) for row in ledger.endpoints)
    spread_endpoint_rounding_slack = 4 * model["values"]["spot"][1]**2 * numerical_width
    moment_endpoint_rounding_slack = rational_guard(factor[1] * spread_endpoint_rounding_slack
                                                   + max(abs(endpoint) for endpoint in result["spread"]) * numerical_width / 2)
    record = {"schema": "e10-robust-continuous-moment-certificate-v1", "case": name,
              "requested_interval_digits": digits, "fixed_Taylor_max_degree": terms,
              "semantic_scope": SEMANTIC_SCOPE, "parameters": model["records"], "absolute_future_dates": date_records,
              "component_count": result["count"], "source_model_SHA256": MODEL_SOURCE_SHA,
              "theorem": uniform_theorem(), "E_A_squared_interval_dollars2_exact": interval_pair(result["components"]["EA2"]),
              "E_A_G_interval_dollars2_exact": interval_pair(result["components"]["EAG"]),
              "E_G_squared_interval_dollars2_exact": interval_pair(result["components"]["EG2"]),
              "separate_cancellation_interval_dollars2_exact": interval_pair(result["separate_cancellation"]),
              "shared_exponent_cancellation_interval_dollars2_exact": interval_pair(result["shared_exponent_cancellation"]),
              "E_spread_squared_interval_dollars2_exact": interval_pair(result["spread"]),
              "nonnegative_intersection_authority": result["nonnegative_intersection_authority"],
              "factor_2q2_exp_hull_id": factor_id, "factor_2q2_interval_exact": interval_pair(factor),
              "flat_policy_residual_second_moment_upper_dollars2_exact": pair(upper_moment[1]),
              "robust_global_fallback_interval_dollars2_exact": interval_pair(upper_moment),
              "total_robust_moment_hull_width_dollars2_exact": pair(upper_moment[1] - upper_moment[0]),
              "max_fixed_exp_endpoint_numerical_width_exact": pair(numerical_width),
              "one_sided_moment_endpoint_numerical_rounding_slack_upper_dollars2_exact": pair(moment_endpoint_rounding_slack),
              "semantic_hull_width_not_a_failed_precision_check": True,
              "terms": result["references"], "shared_exponent_coefficients": result["shared_coefficients"],
              "covariance_hull_exact": [[interval_pair(entry) for entry in row] for row in result["covariance"]],
              "mean_absolute_future_time_hull_exact": interval_pair(result["mean_t"]),
              "geometric_log_variance_hull_exact": interval_pair(result["var_g"]),
              "distinct_fixed_exp_endpoints": len(ledger.endpoints), "distinct_exp_argument_hulls": len(ledger.hulls),
              "numeric_exp_endpoint_precision_passed": True,
              "evaluation_CPU_seconds": time.process_time() - start_cpu,
              "evaluation_wall_seconds": time.monotonic() - start_wall, **flags()}
    exp_record = {"schema": "e10-rational-exp-enclosure-ledger-v1", "case": name, "digits": digits,
                  "fixed_max_degree": terms, "domain": [-8, 8], "saved_dyadic_bits": ledger.bits,
                  "proof": "Positive Taylor terms; successive omitted-term ratio<=|x|/(N+2)<1; geometric remainder; negative reciprocal; outward integer dyadic rounding",
                  "fixed_endpoints": ledger.endpoints, "argument_hulls": ledger.hulls}
    return record, exp_record


def controls():
    ledger = RationalExpLedger(80, 128)
    def values(assets, rate, sigma, rho, spot):
        return {key: interval(value) for key, value in (("assets", assets), ("rate", rate), ("sigma", sigma),
                                                       ("rho", rho), ("spot", spot))}
    first = moment_terms(values(2, 0, 0, 0, 100), [interval(Fraction(1, 2)), interval(1)], ledger)
    require(first["spread"] == interval(0), "Constant-price exact zero-spread control")
    second = moment_terms(values(1, Fraction(3, 100), Fraction(1, 5), Fraction(1, 5), 100),
                          [interval(Fraction(1, 2))], ledger)
    require(second["shared_exponent_cancellation"] == interval(0) and second["spread"] == interval(0),
            "One-component shared exponent exact cancellation")
    var = Fraction(1, 16)
    third = moment_terms(values(2, var / 2, Fraction(1, 4), 0, 1), [interval(1)], ledger)
    _, e2 = ledger.hull(interval(2 * var))
    _, e1 = ledger.hull(interval(var))
    _, eg = ledger.hull(interval(5 * var / 4))
    independent = plus(plus(scale(e2, Fraction(1, 2)), scale(e1, Fraction(3, 2))), scale(eg, -2))
    require(third["shared_exponent_cancellation"] == independent,
            "Independent two-lognormal identity: .5exp(2v)+1.5exp(v)-2exp(5v/4)")
    negative = []
    for identity, operation, expected in (
        ("reject_elapsed_future_dates", lambda: future_date_family({}, "elapsed-after-exercise"), "Exact absolute future-date recipe"),
        ("reject_missing_clipped_policy", lambda: validate_policy({**POLICY_PREMISES, "conditional_clipping": "0<=V<=c0"}),
         "Exact conditional clipping including V>=g and V<=c0"),
    ):
        try:
            operation()
        except ValueError as error:
            require(str(error) == expected, "Exact preregistered negative-control rejection, never a budget failure")
            negative.append({"id": identity, "expected_rejection": expected, "passed": True})
        else:
            raise ValueError("Negative control unexpectedly admitted")
    rows = [{"id": FIXED_CONTROLS[0], "spread_interval_exact": interval_pair(first["spread"]), "passed": True},
            {"id": FIXED_CONTROLS[1], "spread_interval_exact": interval_pair(second["spread"]), "passed": True},
            {"id": FIXED_CONTROLS[2], "general_interval_exact": interval_pair(third["shared_exponent_cancellation"]),
             "independent_closed_form_interval_exact": interval_pair(independent), "variance_exact": pair(var), "passed": True},
            *negative]
    require([row["id"] for row in rows] == list(FIXED_CONTROLS), "Exactly five fixed controls")
    return {"schema": "e10-five-fixed-controls-v1", "controls": rows, "fixed_endpoints": ledger.endpoints,
            "argument_hulls": ledger.hulls, "all_passed": True, "population_proof_not_replaced_by_controls": True}



def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__, fresh=True) == AUTHOR and not OUTPUT.exists(), "One fresh E10 route")
    try:
        fixed_integer_policy()
        runtime = own_runtime()
        ready, policy = release(args.ready_sha256)
        packets = {name: original_owner(name, expected) for name, expected in OWNER_EXPECTATIONS.items()}
        require(_FROZEN[MODEL_SOURCE_KEY] == MODEL_SOURCE_SHA and _FROZEN[DERIVATION_KEY] == DERIVATION_SHA,
                "Admitted full original owner maps contain exact mathematical premise source pins")
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save("run_started.json", {"PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        save("protocol.json", policy)
        save("original_owner_complete_maps_and_inventories.json", {
            "expectations": OWNER_EXPECTATIONS, "complete_original_manifests": packets,
            "foreign_admission_SHA256": FOREIGN_ADMISSION_SHA,
            "inventories": first["prior_original_owned_inventories"],
            "explicit_failed_C12_references_only_no_recursive_failed_runtime": True})
        save("fresh_input_union_before_science.json", first)
        science_cpu, science_wall = time.process_time(), time.monotonic()
        models = exact_source_models()
        save("five_fixed_controls.json", controls())
        outcomes = []
        for name, digits, terms in FIXED_EVALUATIONS:
            budget()
            result, exp_ledger = certificate(name, digits, terms, models[name])
            stem = name + "_digits" + str(digits)
            save(stem + "_certificate.json", result)
            save(stem + "_exp_ledger.json", exp_ledger)
            outcomes.append({"case": name, "digits": digits, "fixed_Taylor_max_degree": terms,
                             "moment_upper_dollars2_exact": result["flat_policy_residual_second_moment_upper_dollars2_exact"],
                             "component_count": result["component_count"],
                             "numeric_exp_endpoint_precision_passed": True})
        science_observation = {"CPU_seconds": time.process_time() - science_cpu,
                               "wall_seconds": time.monotonic() - science_wall,
                               "includes_model_parse_five_controls_three_evaluations_and_scientific_output_serialization": True}
        second = fresh_union()
        save("fresh_input_union_after_science.json", second)
        summary = {"schema": "e10-continuous-moment-only-summary-v1", "passed": True, "completed": True,
                   "budget_censored": False, "fixed_evaluations": outcomes, "fixed_controls_passed": 5,
                   "semantic_scope": SEMANTIC_SCOPE, "policy_premises": POLICY_PREMISES,
                   "both_full_fresh_input_unions": [first, second], "current_runtime": runtime,
                   "science_and_retention_acquisition_observation": science_observation,
                   "process_inclusive_acquisition_observation_before_seal": {
                       "CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED},
                   "cost_comparison_with_historical_pilot_or_support": None, **flags()}
        save("summary.json", summary)
        owned = inventory(OUTPUT)
        files = {path.relative_to(OUTPUT).as_posix(): digest(path, fresh=True) for path in sorted(owned)}
        manifest = {"schema": "e10-continuous-moment-only-manifest-v1", "passed": True, "completed": True,
                    "budget_censored": False, "manifest_self_hash_excluded": True, "files": files,
                    "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL,
                    "original_owner_expectations": OWNER_EXPECTATIONS, "ROOT_READY_SHA256": args.ready_sha256,
                    "both_full_fresh_input_unions": [first, second],
                    "terminal_budget_observation_before_seal": {"CPU_seconds": time.process_time(),
                                                               "wall_seconds": time.monotonic() - _STARTED}, **flags()}
        complete_manifest(manifest, files, sum(path.stat().st_size for path in owned))
        budget()
        print(json.dumps({"passed": True, "completed": True, "evaluations": outcomes,
                          "fixed_controls_passed": 5, "CPU_seconds": time.process_time(),
                          "wall_seconds": time.monotonic() - _STARTED, **flags()}, sort_keys=True))
        return 0
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
