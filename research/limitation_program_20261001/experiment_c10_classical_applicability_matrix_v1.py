"""C10 first applicability census only; external ROOT release required.
No pricing, sampling, solver, fit, rate, confidence-oracle or target module imports.
"""
import argparse
import ctypes
from ctypes import wintypes
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
AUTHOR = RESEARCH / "experiment_c10_classical_applicability_matrix_v1.py"
METHOD_DOC = RESEARCH / "C10_CLASSICAL_APPLICABILITY_MATRIX_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "c10_classical_applicability_matrix_preflight_v1.json"
READY = ROOT / ".context/C10_CLASSICAL_APPLICABILITY_MATRIX_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "C10_classical_applicability_matrix_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 4096, 512 * 1024**2
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
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

OWNER_EXPECTATIONS = {'G0_run003': {'manifest_SHA256': '8ecd597b05a3ea0a8995aeaf29196280d9017f2789eadca503ec78468329b94c',
               'map_fields': ['files', 'frozen_inputs'],
               'complete_map_counts': {'files': 10, 'frozen_inputs': 141},
               'complete_map_object_SHA256': {'files': 'f7291c7e84165c561ecc0dfa6448e816d6e0540d61901719817f4c06efe152ed',
                                              'frozen_inputs': 'aba4578a71fc96ac4c881fb4f84c7accae63dbd25cf455a1b1966301d8510efa'},
               'inclusive_owned_count': 11,
               'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C09_audit_run001': {'manifest_SHA256': 'f8a51247f8126f4a2b043060cec5a1a0f5b929286f721ff4296dcafb6ecb6e53',
                      'map_fields': ['files'],
                      'complete_map_counts': {'files': 188},
                      'complete_map_object_SHA256': {'files': '7dffdd472676fcf5ee0f7309aa2255ec22d810f577f7576078337ab71219ad8d'},
                      'inclusive_owned_count': 189,
                      'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C04_frontier_run002': {'manifest_SHA256': '3135cf7b08ece58dff32b4070f2702593d026c802fb8e383414807c0e677f409',
                         'map_fields': ['files', 'frozen_inputs'],
                         'complete_map_counts': {'files': 4, 'frozen_inputs': 15},
                         'complete_map_object_SHA256': {'files': '336b5b6de7db3be87b3dba0d6dda89516f98038183b9befea75a64803c95a1e3',
                                                        'frozen_inputs': '63f12f13c73656fee5d8633f36c4c24bd8acf42d4b9498f9fe71b886d30d5364'},
                         'inclusive_owned_count': 5,
                         'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C04_frontier_audit_run001': {'manifest_SHA256': '2b424ab6b7f16299ebc9a15c07c1394fa8b0af1aecd753b50a176f71f336fa6b',
                               'map_fields': ['files', 'frozen_inputs'],
                               'complete_map_counts': {'files': 3, 'frozen_inputs': 18},
                               'complete_map_object_SHA256': {'files': '0c3b84d9943bd65d56eb52f8bdb7122568c75ec48f1fae5a7eee2c726569b4f0',
                                                              'frozen_inputs': '857ebffa873b72a893bce5b606a0f584ef215e775c9388bbd608f5f055bc0f3a'},
                               'inclusive_owned_count': 4,
                               'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C09_stagec_timing_update_run001': {'manifest_SHA256': '1baf82a5d8a66ecd80fe6e489385215c4c3020692012a9f063118f8c57742fe2',
                                     'map_fields': ['files', 'frozen_inputs'],
                                     'complete_map_counts': {'files': 135,
                                                             'frozen_inputs': 249},
                                     'complete_map_object_SHA256': {'files': '9d8cf087786320a0419d7bf510cb7bda5a7acab745d732ca3fb5374b6cea20b3',
                                                                    'frozen_inputs': 'f211fd8467cf36c54bfa06e1fb5708439a8bdc0380551dcb6b5f16e8c30b47bf'},
                                     'inclusive_owned_count': 136,
                                     'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C09_conservative_coverage_run001': {'manifest_SHA256': 'a83b2d503c37a003fab7e67ccea0918fc7b0458cc64b72ed260e9c3562b32d40',
                                      'map_fields': ['files', 'frozen_inputs'],
                                      'complete_map_counts': {'files': 8,
                                                              'frozen_inputs': 1548},
                                      'complete_map_object_SHA256': {'files': '289e9a94261c0e782a599930a1f831ae0a1e4a897a383a154df0f13c6ab63894',
                                                                     'frozen_inputs': '428e0eae0ce1b9404836f00b4a6a46729451743a98ca7b66f5d1001f142cbc32'},
                                      'inclusive_owned_count': 9,
                                      'scope': 'COMPLETE_DECLARED_MAPS_LIVE_FULL_SHA'},
 'C8_execution_run003': {'manifest_SHA256': '4ddc581a0a6da72c1394e20914a53bb8dec058bc218b1dc032800ae6c0285812',
                         'map_fields': ['files', 'frozen_inputs', 'external_runtime_inputs'],
                         'complete_map_counts': {'files': 30,
                                                 'frozen_inputs': 18233,
                                                 'external_runtime_inputs': 0},
                         'complete_map_object_SHA256': {'files': '6f0dee9c16d2f4f26c0e0cc1bff797330484849afb15933e680f86fab7be746f',
                                                        'frozen_inputs': '0b67e16ef6c2a0211c89b241fe87edbf43a8a9242c9e88cd037c22075344408f',
                                                        'external_runtime_inputs': '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'},
                         'inclusive_owned_count': 31,
                         'scope': 'FAILED_HISTORY_MAPS_OPAQUE_OWNED_FULLY_VERIFIED'}}
STARTUP_REFERENCE_EXPECTATIONS = {'.context/frontier_t0_env/Lib/site-packages/__pycache__/_cuda_bindings_redirector.cpython-312.pyc': {'SHA256': 'd8536aedd91ba3763b64147357c5e8c0a270b6a8031a59130c10d10351ce879e',
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
DOCUMENT_EXPECTATIONS = {'docs/limitation_audit_20261001/IMPLEMENTATION_PLAN.md': '482b5306d9120c6385f0fce99e5c4e1f639cd750ad940525c4923d0c3347c80e',
 'docs/limitation_audit_20261001/implementation_plan/CONTRACT.md': 'c90588139c60a1cf820c26c4051c16661309d714e2947a3257a5773c3e8e2ce2',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json': '59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a',
 'docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md': '3adbab8fdf17cce1e0c9ba88b04bb8d47aa1a0ff79b402e754d0907ff77957d6',
 'research/limitation_program_20261001/experiment_f44_cosine_caller_grid_axis_v2.py': '1575a24cdb54efc53dd33120ca17da6727d66e35abea4f79fc9ffc3e1b62f102',
 '.context/F44_GRID_AXIS_V2_STARTUP_EXPECTED_JOIN_STATIC_DIAGNOSIS_next_run001.json': '258b5d54dd1826b2e52de593f41e924094c3679e4eabd075d7ef52b75d8bc683'}
TASK_EXPECTED = {'annual_rate': 0.03,
 'annual_volatility_each_asset': 0.3,
 'assets': 4,
 'barrier_dollars': 140.0,
 'barrier_equality': 'basket >= H is knocked out; alive uses strict < H',
 'continuous_sampling': 'Independent common/idiosyncratic standard normals give exact GBM '
                        'log increments at each contractual date before numerical '
                        'representation.',
 'dates': 12,
 'digital_source': {'exponential': 'ln(2) range reduction and degree-12 Taylor polynomial '
                                   'evaluated by Estrin',
                    'fraction_bits': 40,
                    'guard_semantics': 'Each accumulated log spot is clipped before its '
                                       "Estrin exponential; the digital guard's "
                                       'continuous-price bias remains unproved.',
                    'integer_semantics': 'Signed two-complement fixed-point; flags and '
                                         'indexes are unscaled integers; all output '
                                         'arithmetic is modulo 2^width.',
                    'law': 'Independent uniform 32-bit integers, paired Box-Muller with '
                           'existing log/cos polynomial tables and integer square root',
                    'normal_count': 60,
                    'output': {'Y': 5697},
                    'output_dollar_conversion': 'Interpret output Y as signed '
                                                "two's-complement integer divided by 2^40; "
                                                'discount is already applied.',
                    'spot_guard': [1.52587890625e-05, 4096.0],
                    'uniform_bits_each': 32,
                    'uniform_midpoint': 'u=(integer+1/2)/2^32',
                    'word_width': 72},
 'discount': 0.9704455335485082,
 'equicorrelation': 0.4,
 'equity_covariance_matrix': [[1.0, 0.4, 0.4, 0.4],
                              [0.4, 1.0, 0.4, 0.4],
                              [0.4, 0.4, 1.0, 0.4],
                              [0.4, 0.4, 0.4, 1.0]],
 'maturity_years': 1.0,
 'model': 'correlated geometric Brownian motion at contractual dates',
 'notional_semantics': {'initial_equal_weight_basket_dollars': 100.0,
                        'interpretation': 'One unit of the equal-weight basket/Asian call. '
                                          'Initial basket is $100; payoff is already in '
                                          'dollars. No extra factor of 100 or 0.01 is '
                                          'introduced.',
                        'participation': 1,
                        'recovered_from': 'barrier_oracle_depth.build constants, 1/assets '
                                          'and 1/(assets*dates) averages, strike and '
                                          'discount; matches Stage A original_target and '
                                          'optimized target',
                        'separate_notional_multiplier': None},
 'observation_times': [0.08333333333333333,
                       0.16666666666666666,
                       0.25,
                       0.3333333333333333,
                       0.4166666666666667,
                       0.5,
                       0.5833333333333334,
                       0.6666666666666666,
                       0.75,
                       0.8333333333333334,
                       0.9166666666666666,
                       1.0],
 'output_contract': {'absolute_error_dollars': [0.1, 0.03, 0.01, 0.001],
                     'complete_advantage': 'T_Q <= fastest eligible complete measured T_C / '
                                           '10',
                     'delivered_output': 'one classical discounted dollar price',
                     'final_strict_target_scope': '0.001 is the historical B4/B8 knock-out '
                                                  'final test, not silently extended to '
                                                  'every source family',
                     'per_price_success_probability_at_least': 0.99,
                     'statistical_share_reference': 'e=0.45*epsilon retained as a '
                                                    'historical/planning allocation, not an '
                                                    'implemented estimator'},
 'payoff': 'exp(-r*T) * max(mean over all asset/date spots - K, 0) * indicator(max over '
           'monitored dates of equal-weight spot basket < H)',
 'spot_each_asset_dollars': 100.0,
 'strike_dollars': 100.0}
FAMILIES = [{'id': 'conditioning_rqmc',
  'family': 'Conditioning/preintegration with randomized quasi-Monte Carlo',
  'task_applicability': 'EXISTING_TARGETED_CLASSICAL_IMPLEMENTATION_WITH_OPEN_DELIVERY_PROOFS',
  'same_task_required': 'Conditional expectation integrates the ORIGINAL12-date '
                        'arithmetic-Asian basket payoff including alive iff every monitored '
                        'basket<140; unchanged discounted scalar.',
  'law_required': 'Original full-rank correlated GBM date law; conditional likelihood/weight '
                  'and numerical inverse-normal, clipping and root errors must be accounted '
                  'for.',
  'monitoring_required': 'Contractual12 monitoring dates; basket>=H kills, including '
                         'equality. No continuous monitoring or selected barrier-date '
                         'substitution.',
  'confidence_required': 'Sound99% true-price delivery including reference/numerical bias, '
                         'replicate dependence and any stopping/selection; nominal scramble '
                         'intervals alone are insufficient.',
  'setup_required': 'Same complete cold/setup/warm conventions; include '
                    'conditioning/root/transform/factorization/training if used, uniform '
                    'draws and all payoff work.',
  'existing_evidence': ['C09_audit_run001',
                        'C04_frontier_run002',
                        'C04_frontier_audit_run001',
                        'C09_stagec_timing_update_run001',
                        'C09_conservative_coverage_run001'],
  'named_holds': ['F01 applicability/performance-optimality dependency remains unresolved',
                  'Full true-price99% and numerical bias qualification is not supplied by '
                  'saved nominal intervals',
                  'Any new conditioning directions need separate exact-conditional/payoff '
                  'proof and pilot',
                  'Complete cold/setup and held-out acquisition must use separately '
                  'preregistered accounting'],
  'variant_incompatibility': 'Replacing min over ALL12 contractual basket-barrier tests by '
                             'one chosen date changes the payoff; it is not a same-task '
                             'challenger.',
  'next_small_step': 'Specify one candidate transformation and its exact conditional '
                     'expectation/weight, monetary bias and confidence/setup premises before '
                     'any pilot.',
  'performance_rank': None,
  'challenger_implementation_released': False,
  'delivery_eligible': False},
 {'id': 'mlmc_fixed_target',
  'family': 'Multilevel Monte Carlo with exact final monitored-date target',
  'task_applicability': 'CONDITIONAL_HOLD_UNSUPPLIED_HIERARCHY_AND_COUPLING',
  'same_task_required': 'Preregister levels and telescope, whose FINAL level equals the '
                        'original12-date payoff expectation, with separately bounded '
                        'residual/bias and sampling error.',
  'law_required': 'Every required level marginal and fine/coarse Gaussian covariance '
                  'coupling is exact or bias-paid; common/idiosyncratic sharing at original '
                  'dates is retained.',
  'monitoring_required': 'Final target retains all12 original dates, arithmetic averaging '
                         'and equality killing. Coarse intermediate estimands are permitted '
                         'ONLY through a proved final-target telescope.',
  'confidence_required': 'Joint allocation over base, all corrections and any '
                         'residual/stopping/selection gives same99% scalar delivery; no '
                         'assumed IID or variance decay.',
  'setup_required': 'Charge coupling/base/corrections/pilot/allocation/reference and '
                    'complete setup; no free trained or analytic base.',
  'existing_evidence': ['G0_run003'],
  'named_holds': ['Explicit same-final-target hierarchy and telescoping identity not '
                  'supplied',
                  'Level marginal/covariance/date and arithmetic averaging coupling proof '
                  'not supplied',
                  'Correction variance/cost and bias rates not supplied for this fixed '
                  'payoff',
                  'Confidence/setup allocation and independent held-out target validation '
                  'not supplied',
                  'F01 comparator applicability dependency remains unresolved'],
  'variant_incompatibility': 'A standalone coarse-date price replacing original12 '
                             'monitoring/averaging dates fails the task. This does NOT '
                             'exclude coarse intermediate MLMC levels with a valid '
                             'telescope.',
  'next_small_step': 'Supply one finite hierarchy/coupling/telescope ending at exact '
                     'original12-date target; hold allocations and pilot until that identity '
                     'is reviewed.',
  'performance_rank': None,
  'challenger_implementation_released': False,
  'delivery_eligible': False},
 {'id': 'pde_discrete_average_state',
  'family': 'State-space PDE with discrete-date average update and killing',
  'task_applicability': 'CONDITIONAL_HOLD_UNSUPPLIED_DISCRETE_UPDATE_AND_NUMERICAL_ERROR_PROOF',
  'same_task_required': 'State holds four spot/log-spot coordinates plus accumulated '
                        'monitored equal-weight-basket sum; no scalar-basket Markov closure '
                        'assumed. Sum/12 gives original arithmetic average at maturity.',
  'law_required': 'Generator/covariance, initial state and discount represent unchanged '
                  'four-asset correlated GBM; any truncation/low-rank/reduction error is '
                  'paid in dollars.',
  'monitoring_required': 'At each ORIGINAL date update accumulated basket sum and kill iff '
                         'basket>=140. Between dates there is no continuously monitored '
                         'absorbing basket barrier substituted.',
  'confidence_required': 'Deterministic domain/discretization/solver/roundoff error<=same '
                         'dollar allowance; randomized components need same99% complete '
                         'allocation. A residual norm alone needs output-dollar conversion.',
  'setup_required': 'Charge domain, mesh, generator/matrix/boundary construction, '
                    'solve/preconditioner/storage and scalar output extraction; analytic or '
                    'trained bases are not free.',
  'existing_evidence': ['G0_run003'],
  'named_holds': ['Complete original-date jump/killing/terminal and scalar readout '
                  'formulation not supplied',
                  'Finite domain/tail, discretization, interpolation, solver and '
                  'floating-point dollar error bounds not supplied',
                  'Initial/terminal and covariance/state storage contracts not supplied as '
                  'executable solver inputs',
                  'Comparable complete setup/solve/readout pilot and validation not supplied',
                  'F01 comparator applicability dependency remains unresolved'],
  'variant_incompatibility': 'A continuous absorbing basket-barrier PDE changes discrete '
                             'monitoring; a basket-only state without proved closure changes '
                             'the model/average state. These variants do not exclude a valid '
                             'full-state discrete-update PDE.',
  'next_small_step': 'Write the full four-asset-plus-average-state backward problem with '
                     'ORIGINAL12 update/killing operators and dollar-error ledger before '
                     'choosing a mesh/solver.',
  'performance_rank': None,
  'challenger_implementation_released': False,
  'delivery_eligible': False}]

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



def flags():
    return dict(metadata_only=True, item="C10", first_matrix_substep_only=True,
                fixture_credit=0, new_prices_paths_scrambles_timings=0,
                new_scientific_tests=0, challenger_implementation_released=False,
                universal_fastest_claim=False, G4_closed=False, quantum_advantage=False,
                financial_adoption=False, source_adoption=False, G2_transfer=False,
                cost_transfer=False, F01_dependency_closed=False,
                untouched_foreign_F03_F31_F32_C15=True)


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


def loaded_origins():
    forbidden = {"numpy", "scipy", "mpmath", "sympy", "numba", "pytest", "pandas"}
    require(not any(name.split(".", 1)[0] in forbidden or name.startswith("research.")
                    for name in sys.modules), "No pricing/historical/numerical package import")
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            path = Path(os.path.abspath(str(origin)))
            if not path.is_file():
                require(attribute == "__cached__" and not path.exists() and not path.is_symlink(),
                        "Only an absent declared loaded cache, never a missing source origin")
                require(path in _ABSENT_RUNTIME
                        or (path.is_relative_to(BASE / "Lib")
                            and not path.is_relative_to(BASE / "Lib/site-packages")),
                        "Absent loaded cache is in declared author or isolated stdlib scope")
                _ABSENT_RUNTIME.add(path)
                continue
            actual = canonical(path, fresh=True)
            key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
            mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
            require(key in mapping, "Every loaded origin/cache has a prior admitted expectation")
            require(digest(actual, fresh=True, already_resolved=True) == mapping[key],
                    "Every actual loaded origin/cache equals frozen expected bytes")


def startup_reference_bindings():
    for key, record in STARTUP_REFERENCE_EXPECTATIONS.items():
        budget()
        actual = canonical(exact_key(key), fresh=True)
        add(actual, record["SHA256"])
        require(fingerprint(actual)[2] == record["bytes"]
                and digest(actual, fresh=True, already_resolved=True) == record["SHA256"],
                "Six ORIGINAL finite startup reference expectations before first origin check")


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


def original_owner(name, expectation):
    directory = PROGRAM / name
    manifest_path = directory / "manifest.json"
    packet = read(bind(manifest_path, expectation["manifest_SHA256"]))
    fields = [key for key in ("files", "frozen_inputs", "external_runtime_inputs") if key in packet]
    require(fields == expectation["map_fields"], "Exact original map presence, no invented maps")
    history = expectation["scope"] == "FAILED_HISTORY_MAPS_OPAQUE_OWNED_FULLY_VERIFIED"
    owned = {manifest_path}
    for field in fields:
        mapping = packet[field]
        require(type(mapping) is dict and len(mapping) == expectation["complete_map_counts"][field]
                and object_sha(mapping) == expectation["complete_map_object_SHA256"][field],
                "Full original literal map/count/pins retained")
        for key, pin in mapping.items():
            budget(admission=True)
            path = exact_key(key) if not Path(key).is_absolute() else Path(key)
            require(type(pin) is str and len(pin) == 64
                    and all(char in "0123456789abcdef" for char in pin), "Original literal expected SHA")
            if history and field != "files":
                continue
            actual = bind(path, pin)
            if field == "files":
                require(actual.is_relative_to(directory) and actual not in owned,
                        "Complete exact original owned inventory confinement")
                owned.add(actual)
    require(len(owned) == expectation["inclusive_owned_count"] and inventory(directory) == owned,
            "Complete original physical owned inventory")
    _OWN_INVENTORIES[directory] = owned
    if history:
        require(name == "C8_execution_run003" and packet["schema"] == "c8_local_terminal_manifest_v1"
                and packet["passed"] is False and packet["fixture_credit"] == 0,
                "Original C8 sealed failure remains failed, zero credit")
    else:
        require(not any((directory / marker).exists() for marker in FAILURE_NAMES),
                "No new authoritative failure on original scoped evidence owner")
    return packet


def fresh_union():
    invocation_check()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(canonical(lexical, fresh=True) == actual,
                "Every original lexical input alias remains freshly confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, expected in mapping.items():
            budget()
            path = ROOT / key if not Path(key).is_absolute() else Path(key)
            require(path not in union or union[path] == expected, "Equal original expected SHA union")
            union[path] = expected
    for path, pin in _OBSERVED.items():
        require(path not in union or union[path] == pin, "Observed never replaces expected")
        union[path] = pin
    require(len(union) <= MAX_REFERENCES, "Complete input reference cap")
    size = 0
    for path, expected in sorted(union.items()):
        actual = canonical(path, fresh=True)
        size += actual.stat().st_size
        require(size <= MAX_UNIQUE_BYTES, "Complete input unique byte cap")
        require(digest(actual, fresh=True, already_resolved=True) == expected,
                "Every full fresh actual input equals original expected SHA")
    for directory, expected in _OWN_INVENTORIES.items():
        require(inventory(directory) == expected, "All original full owned inventories unchanged")
    require(standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
            "Complete current isolated runtime membership unchanged")
    require(not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
            "All original/current loaded cache and standard zip absences unchanged")
    for path, expected in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == expected, "All declared existing code cache bytes unchanged")
    loaded_origins()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_physical_resolve_and_SHA": True}


def release(ready_sha):
    global _FULL_ADMISSION
    ready = read(bind(READY, ready_sha))
    require(ready["schema"] == "root-c10-classical-applicability-matrix-READY-v1"
            and ready["ready"] is True and ready["root_and_independent_static_reviews_passed"] is True
            and ready["metadata_matrix_only_execution_authorized"] is True
            and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
            and ready["owner_expected_manifest_and_map_scope"] == OWNER_EXPECTATIONS,
            "Separate ROOT release of this fixed metadata-only applicability census")
    authors = ready["author_method_SHA256"]
    require(set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
            "Exactly three externally frozen new author files")
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(policy["schema"] == "c10-classical-applicability-matrix-preflight-v1"
            and policy["owner_expected_manifest_and_map_scope"] == OWNER_EXPECTATIONS
            and policy["fixed_families"] == FAMILIES
            and policy["startup_reference_original_expectations"] == STARTUP_REFERENCE_EXPECTATIONS
            and policy["task_original_expected_record"] == TASK_EXPECTED
            and policy["author_SHA256"] == authors[AUTHOR.name]
            and policy["method_SHA256"] == authors[METHOD_DOC.name]
            and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
            and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
            and policy["reference_unique_hash_work_caps"]
            == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK],
            "Exact fixed row identities/task/limits before output or matrix generation")
    for key, expected in DOCUMENT_EXPECTATIONS.items():
        bind(exact_key(key), expected)
    code_cache_policy(ready)
    for key, pin in ready["static_review_expected_SHA256"].items():
        require(key.startswith(".context/"), "ROOT-local prior static review")
        bind(exact_key(key), pin)
    _FULL_ADMISSION = True
    loaded_origins()
    return ready, policy


def applicability_matrix():
    task = read(PROGRAM / "G0_run003/B4x12_task.json")
    require(task == TASK_EXPECTED and task["assets"] == 4 and task["dates"] == 12
            and task["barrier_equality"] == "basket >= H is knocked out; alive uses strict < H"
            and task["output_contract"]["absolute_error_dollars"] == [0.1, 0.03, 0.01, 0.001]
            and task["output_contract"]["per_price_success_probability_at_least"] == 0.99
            and task["notional_semantics"]["separate_notional_multiplier"] is None,
            "Original G0 task fixes dollar units, final0.001/99%, all dates and equality")
    comparison = read(PROGRAM / "C04_frontier_run002/comparison.json")
    audit = read(PROGRAM / "C04_frontier_audit_run001/summary.json")
    require(audit["passed"] is True and audit["independent_measured_rows_audited"] == 6
            and audit["actual_source_and_complete_runtime_and_ratios_null"] is True,
            "Carry C04 measured and conditional scope without new ratio evaluation")
    selected = [row for row in comparison["rows"] if row["case"] == "B4x12"
                and row["classical_accuracy_target_dollars_exact"] == [1, 1000]]
    require(len(selected) == 1 and selected[0]["classical_method"] == "preint"
            and selected[0]["classical_evidence_is_measured_confirmation"] is True
            and selected[0]["classical_full_coverage_qualification"] is False
            and selected[0]["actual_complete_speedup_ratio"] is None,
            "One actual saved B4 final-dollar timing record, with qualification still open")
    coverage = read(PROGRAM / "C09_conservative_coverage_run001/summary.json")
    timing = read(PROGRAM / "C09_stagec_timing_update_run001/summary.json")
    law = read(PROGRAM / "C09_audit_run001/source_estimand_law_ledger.json")
    failure = read(PROGRAM / "C8_execution_run003/summary.json")
    require(coverage["true_price_99_percent_delivery_proved"] is False
            and coverage["reference_true_price_confidence_premise_verified"] is False
            and coverage["conditional_IID_binomial_model_verified"] is False
            and timing["all_epsilon0p001_C5_C7_times_are_fitted_not20_run_confirmed"] is True
            and failure["passed"] is False and failure["fixture_credit"] == 0
            and failure["oracle_phase_executed"] is False,
            "Preserve exact existing confidence/fitted timing and failed C8 qualifications")
    require(law["classical_hard_payoff_and_preintegrated_estimands_differ_pointwise_but_target_same_continuous_expectation"] is True
            and law["identical_actual_finite_sampler_or_arithmetic"] is False,
            "Same continuous expectation is distinct from identical digital sampler/integrand")
    require(len(FAMILIES) == 3 and [row["id"] for row in FAMILIES]
            == ["conditioning_rqmc", "mlmc_fixed_target", "pde_discrete_average_state"],
            "Exactly three preregistered families without adaptive selection")
    return {"schema": "c10-three-family-applicability-census-v1", "case": "B4x12",
            "delivered_output": task["output_contract"]["delivered_output"],
            "task_SHA256": "c7ac83c1019b649e46a12469cf15df1cede810539b96f18e7de313660117537f",
            "price_law": "Original continuous correlated GBM at contractual12 dates",
            "absolute_error_dollars_exact": [1, 1000], "per_price_success_probability_exact": [99, 100],
            "notional_multiplier_added": False, "normalization_or_quantum0p01_budget_transfer": False,
            "original_contract": task, "rows": FAMILIES,
            "retained_measured_final_dollar_baseline_row": selected[0],
            "retained_C09_law_qualification_as_historical_record_only": law,
            "retained_confidence_status": coverage, "retained_C5_C7_status": timing,
            "retained_C8_failed_guard_and_no_numerical_phase": failure,
            "decision": "FIRST_APPLICABILITY_CENSUS_WITH_NAMED_HOLDS_NO_CHALLENGER_RELEASE",
            "global_current_original_G2_status_reassessed": False,
            "strongest_tested_baseline_changed": False, "universally_fastest_method_selected": None,
            "next_challenger_selected": None, "entire_C10_completed": False, **flags()}


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__, fresh=True) == AUTHOR and not OUTPUT.exists(), "One fresh C10 route")
    try:
        fixed_integer_policy()
        startup_reference_bindings()
        runtime = own_runtime()
        ready, policy = release(args.ready_sha256)
        packets = {name: original_owner(name, expected) for name, expected in OWNER_EXPECTATIONS.items()}
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save("run_started.json", {"PID": os.getpid(), "limits_CPU_admission_wall": [CPU, ADMISSION, WALL], **flags()})
        save("original_C8_failure_history_literal_maps.json", packets["C8_execution_run003"])
        result = applicability_matrix()
        save("applicability_matrix.json", result)
        second = fresh_union()
        summary = {"passed": True, "completed": True, "budget_censored": False,
                   "decision": result["decision"], "case": "B4x12", "families": 3,
                   "absolute_error_dollars_exact": [1, 1000], "success_probability_exact": [99, 100],
                   "both_full_fresh_input_unions": [first, second], "current_runtime": runtime,
                   "entire_C10_completed": False, "delivery_eligible_challengers": 0, **flags()}
        save("summary.json", summary)
        owned = inventory(OUTPUT)
        files = {path.relative_to(OUTPUT).as_posix(): digest(path, fresh=True) for path in sorted(owned)}
        manifest = {"schema": "c10-classical-applicability-matrix-manifest-v1",
                    "passed": True, "completed": True, "budget_censored": False,
                    "manifest_self_hash_excluded": True, "files": files,
                    "frozen_inputs": _FROZEN, "external_runtime_inputs": _EXTERNAL,
                    "owner_expected_manifest_and_map_scope": OWNER_EXPECTATIONS,
                    "both_full_fresh_input_unions": [first, second],
                    "ROOT_READY_SHA256": args.ready_sha256,
                    "terminal_budget_observation": {"CPU_seconds": time.process_time(),
                                                    "wall_seconds": time.monotonic() - _STARTED},
                    "entire_C10_completed": False, **flags()}
        complete_manifest(manifest, files, sum(path.stat().st_size for path in owned))
        budget()
        print(json.dumps(summary, sort_keys=True))
        return 0
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
