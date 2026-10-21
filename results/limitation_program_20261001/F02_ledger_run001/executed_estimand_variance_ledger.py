"""Bind the finite active estimand menu to distinct variance interfaces.

Only frozen C09 snapshots and prior source/support certificates are read. No
financial draws, bootstrap, gate replay, timing or new coherent transform is
executed. Classical path-sigma pilots, independent-scramble estimator variance,
native payoff support and selector Bernoulli variance remain different objects.
"""

from __future__ import annotations

# Receipt explanations stay readable.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
INVENTORY = PROGRAM / "C09_audit_run001"
CLASSICAL = ROOT / "results/frontier_classical_20261001"
RESEARCH = ROOT / "research/frontier_classical_20261001"
METHODS = (
    "plain-rqmc",
    "preintegration",
    "time-ordered-oss",
    "oss-bb",
    "iid-reference",
    "native-quantum-payoff",
)
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def encoded(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen dependency changed", name)


def close(actual, expected, name):
    assert math.isfinite(actual) and math.isfinite(expected)
    assert math.isclose(actual, expected, rel_tol=2e-11, abs_tol=2e-12), (name, actual, expected)


class FrozenInventory:
    def __init__(self):
        protocol = read(INVENTORY / "protocol.json")
        self.files = {record["original"]: record for record in protocol["files"]}
        assert read(INVENTORY / "summary.json")["passed"]
        for record in self.files.values():
            assert sha(ROOT / record["snapshot"]) == record["sha256"]

    def path(self, original):
        return ROOT / self.files[relative(original)]["snapshot"]

    def json(self, original):
        return read(self.path(original))

    def array(self, original):
        array = np.load(self.path(original), allow_pickle=False)
        assert np.isfinite(array).all()
        return array

    def binding(self, original):
        record = self.files[relative(original)]
        return dict(
            original=relative(original),
            immutable_C09_snapshot=record["snapshot"],
            sha256=record["sha256"],
        )

    def transform_bindings(self, names):
        return [self.binding(RESEARCH / name) for name in names]


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    manifest = read(INVENTORY / "manifest.json")
    frozen = dict(manifest["files"])
    frozen[relative(INVENTORY / "manifest.json")] = sha(INVENTORY / "manifest.json")
    extras = [
        Path(__file__).resolve(),
        PROGRAM / "E02_financial_audit_run001/summary.json",
        PROGRAM / "E02_financial_audit_run001/manifest.json",
    ]
    for case in CASES:
        extras.extend(
            PROGRAM / "E02_financial_run002" / case / name
            for name in ("estimator_ledger.json", "iterate.json")
        )
        extras.extend(
            PROGRAM / "A10_coefficient_run001" / case / "min-depth" / name
            for name in ("source.json", "schedule_capped.json")
        )
        extras.extend(
            (
                PROGRAM / "E03_support_run001" / (case + "_certificate.json"),
                PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"),
            )
        )
    extras.extend(
        PROGRAM / name / "manifest.json"
        for name in ("E02_financial_run002", "E03_support_run001", "E03_support_audit_run002")
    )
    frozen.update({relative(path): sha(path) for path in extras})
    verify(frozen)
    output.mkdir()
    shutil.copy2(Path(__file__).resolve(), output / "executed_estimand_variance_ledger.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_ledger_calculations=True,
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            numpy=np.__version__,
            finite_menu=[dict(case=case, method=method) for case in CASES for method in METHODS],
            active_menu_rows=12,
            source_inventory=relative(INVENTORY),
            classical_numerical_inputs="Only already frozen C09 snapshots",
            additional_inputs="Previously audited native support, actual source binding and current finite estimator invocation ledger; no acquisition",
            calculations=[
                "independent-scramble mean sample variance from C1/C5/RefA prefixarrays",
                "separate averaged-scramble variance using actual replicate count",
                "recorded continuous one-path sigma pilots with provenance limits",
                "iid worker-aggregate path variance and variance of its independent mean",
                "native finite-payoff support Popoviciu bound and exact46-bit/64dollar selector normalization",
                "unavailable smoothing, residual and scramble variance credits for unchanged native quantum payoff",
            ],
            new_financial_draws=0,
            new_financial_replays=0,
            new_bootstraps=0,
            new_timing_runs=0,
            new_coherent_transforms=0,
            stop_rule="Audit this fixed menu once; unsupported benefits remain unavailable and prior valid accounting retained",
            complete_price_or_quantum_advantage_claim=False,
            C09_reference_coverage_provenance_blockers_preserved=True,
            preserve_failures=True,
        ),
    )
    print("F02 active estimand/variance menu frozen:12 rows,no new finance", flush=True)


def prefix_variance(array, powers, saved=None):
    assert array.ndim == 2 and array.shape[0] >= 2 and array.shape[1] == len(powers)
    count = array.shape[0]
    values = []
    for j, power in enumerate(powers):
        sigma_mean = float(array[:, j].std(ddof=1))
        variance_mean = sigma_mean**2
        if saved is not None:
            close(saved["sd_one_scramble"][j], sigma_mean, "saved scramble-mean deviation")
        values.append(
            dict(
                points_per_scramble=1 << power,
                independent_scrambles_observed=count,
                sample_variance_of_one_scramble_mean_dollars_squared=variance_mean,
                sample_sd_of_one_scramble_mean_dollars=sigma_mean,
                estimated_variance_of_average_of_observed_scrambles_dollars_squared=variance_mean
                / count,
                estimated_variance_of_average_of_16_fresh_scrambles_dollars_squared=variance_mean
                / 16,
                covariance_between_dependent_points_within_scramble_not_discarded=True,
                one_path_variance_not_inferred_by_multiplying_by_n=True,
                population_variance_confidence_certificate=None,
            )
        )
    if saved is not None:
        close(saved["price"], float(array[:, -1].mean()), "saved final price")
        close(
            saved["std_error"],
            math.sqrt(
                values[-1]["estimated_variance_of_average_of_observed_scrambles_dollars_squared"]
            ),
            "saved final SE",
        )
    return values


def path_sigma_measurement(pilot, method, binding, code_binding):
    sigma = pilot["sigma_q" if method == "plain-rqmc" else "sigma_preint"]
    assert sigma > 0 and pilot["paths"] == 1 << 20
    result = dict(
        measurement_kind="one_path_sample_standard_deviation_of_discounted_continuous_model_integrand",
        sample_sd_dollars=sigma,
        sample_variance_dollars_squared=sigma**2,
        iid_normal_draws=pilot["paths"],
        ddof=1,
        pilot_receipt_binding=binding,
        pilot_transform_source_binding=code_binding,
        source_family="canonicalPCA Gaussian normal pilot",
        raw_one_path_values_archived_in_frozen_inventory=False,
        full_code_spec_environment_hashes_in_pilot=False,
        measured_value_not_a_certified_population_upper_bound=True,
        finite_quantum_law_bound_transfer_certified=False,
        sigma_over_epsilon_cost_substituted_for_measured_RQMC_variance=False,
    )
    if method == "plain-rqmc":
        result["recorded_bootstrap_ci95_dollars"] = pilot["sigma_q_ci95"]
        assert (
            len(pilot["sigma_q_ci95"]) == 2
            and pilot["sigma_q_ci95"][0] <= sigma <= pilot["sigma_q_ci95"][1]
        )
        result["bootstrap_ci_is_not_a_99percent_population_bound"] = True
    else:
        result["recorded_bootstrap_ci95_dollars"] = None
        result["conditioning_interpretation"] = (
            "Ideal exact preintegration is a conditional expectation; law of total variance supportsnonincrease butthisreported sd is a numericalpilot,not a currentcoherentquantumsource."
        )
    return result


def common_row(case, method, bindings):
    assets, dates = CASES[case]
    return dict(
        case=case,
        method=method,
        original_contract=dict(
            assets=assets,
            monitored_dates=dates,
            spot_dollars_exact=[100, 1],
            strike_dollars_exact=[100, 1],
            strict_survival_basket_threshold_dollars_exact=[140, 1],
            sigma_exact=[3, 10],
            correlation_exact=[2, 5],
            rate_exact=[3, 100],
            maturity_years_exact=[1, 1],
            scalar_discounted_price=True,
            notional_rescaling=1,
        ),
        normalization=dict(
            output_units="already discounted dollars",
            output_contains_original_discount=True,
            second_discount_applied=False,
            native_fixed_point_fraction_bits=None,
            amplitude_normalization_span_dollars=None,
        ),
        transform_source_bindings=bindings,
        one_path_sigma=None,
        one_path_population_variance_upper_bound=None,
        independent_scramble_variance_measurements=[],
        iid_mean_variance_measurement=None,
        residual_range_dollars=None,
        residual_variance_upper_bound=None,
        residual_covariance_bound=None,
        residual_or_coherent_control_implemented=False,
        financial_full_price_certificate=False,
    )


def classical_rows(inventory, case, c1, c5, pilot, refa):
    rows = []
    data = c1["cases"][case]
    canonical_path = CLASSICAL / "c1" / (case + "_canonical.npy")
    canonical = inventory.array(canonical_path)
    assert canonical.shape == (32, 6, len(data["ms"]))
    for method, column, name in (
        ("plain-rqmc", 2, "knockout"),
        ("preintegration", 5, "knockout_pre"),
    ):
        bindings = inventory.transform_bindings(
            ("scrambles.py", "basis.py", "kernels.py", "timing.py")
        )
        row = common_row(case, method, bindings)
        row.update(
            law="ContinuousGBM covariance model evaluatednumerically by clippedinverse-normal scrambledSobol andfullrankPCA",
            integrand="discounted unsmoothed monitored knockoutpayoff"
            if method == "plain-rqmc"
            else "discounted firstprincipalGaussian direction conditional expectation ofmonitored knockoutpayoff",
            coordinates=CASES[case][0] * CASES[case][1],
            one_path_sigma=path_sigma_measurement(
                pilot[case],
                method,
                inventory.binding(CLASSICAL / "sigma_dev/sigma_dev.json"),
                inventory.binding(RESEARCH / "sigma_q.py"),
            ),
            expectation_identity="Original continuous Gaussian covariance model; changingPCAbasis preservesitsidealdistribution, butthisisnot anexact rotation identityfor pairedfiniteBoxMuller/nativewords",
            independent_scramble_variance_measurements=prefix_variance(
                canonical[:, column, :], data["ms"], data["summary"]["canonical"][name]
            ),
            raw_scramble_prefix_binding=inventory.binding(canonical_path),
            recorded_covariance_factor_sha256=data["factor_sha256"]["canonical"],
            quantum_smoothing_or_variance_credit_available=False,
            measured_error_cost_model="Use independent-scramble error versuspointcount andactualtimings;do not substituteonepathsigma/sqrtn orsigma/epsilon.",
        )
        row["one_path_population_variance_upper_bound"] = dict(
            upper_dollars_squared_exact=[400, 1],
            law="ideal original continuous monitored discountedpayoff"
            if method == "plain-rqmc"
            else "ideal exact conditionalexpectation transform",
            proof="BothYandidealE[Y|remainingcoordinates] liein[0,40];Popoviciu givesvariance<=40^2/4",
            actual_float64_transform_bias_bound_dollars=None,
            bound_not_a_complete_actual_float64_price_certificate=True,
        )
        rows.append(row)
    for method, label in (("time-ordered-oss", "oss"), ("oss-bb", "oss_bb")):
        key = case + "/" + label
        saved = c5[key]["summary"]
        array_path = CLASSICAL / "c5/rates" / (case + "_" + label + ".npy")
        array = inventory.array(array_path)
        assert array.shape == (32, 14)
        row = common_row(
            case,
            method,
            inventory.transform_bindings(("c5_smoothers.py", "oss.py", "basis.py", "timing.py")),
        )
        row.update(
            law="ContinuousGBM survival-conditioned Gaussianincrements withlikelihoodweight product; Brownianbridgeordering foridioPCs"
            if method == "oss-bb"
            else "ContinuousGBM time-ordered survival-conditioned Gaussianincrements withlikelihoodweight product",
            integrand="discounted survivorAsianpositivepayoff multipliedbyproductofconditional survivalprobabilities",
            coordinates=CASES[case][0] * CASES[case][1],
            independent_scramble_variance_measurements=prefix_variance(
                array, list(range(6, 20)), saved
            ),
            raw_scramble_prefix_binding=inventory.binding(array_path),
            one_path_sigma=None,
            one_path_sigma_unavailable_reason="No individual OSSpath outcomes or onepathvariance measurement inthisfrozenmenu;prefixmeans donotsupplyonepathvariance",
            expectation_identity="Ideal exact survivalconditioning andlikelihoodweights targettheoriginal continuousmonitored price; numericalCDF,quantile,rootandroundoff effectsstillneedfinancialcertification",
            quantum_smoothing_or_variance_credit_available=False,
            measured_error_cost_model="Independent-scramble meanvariancecurve for thisOSStransform;onepathsigma/e isnota replacement.",
        )
        row["one_path_population_variance_upper_bound"] = dict(
            upper_dollars_squared_exact=[400, 1],
            law="ideal exactly conditioned,correctly likelihoodweightedOSS integrand",
            proof="Conditional survivalweights arein[0,1] andsurvivingdiscounted payoffisin[0,40], henceintegrandisin[0,40]",
            actual_float64_transform_bias_bound_dollars=None,
            bound_not_a_complete_actual_float64_price_certificate=True,
        )
        if method == "time-ordered-oss":
            reference_path = CLASSICAL / "c3_refa" / (case + "_oss_prefix.npy")
            reference = inventory.array(reference_path)
            a = refa["cases"][case]
            assert reference.shape == (64, len(a["ms"])) and a["ms"][-1] == 22
            record = prefix_variance(reference, a["ms"])
            close(
                math.sqrt(
                    record[-1][
                        "estimated_variance_of_average_of_observed_scrambles_dollars_squared"
                    ]
                ),
                a["se"],
                "OSS RefA SE",
            )
            row["additional_64_scramble_reference_variance_measurements"] = record
            row["additional_reference_prefix_binding"] = inventory.binding(reference_path)
        rows.append(row)
    reference_path = CLASSICAL / "c3_refb" / case / "ref_b.json"
    reference = inventory.json(reference_path)
    workers = reference["workers"]
    assert len(workers) == 16
    n = sum(w["n"] for w in workers)
    mean = math.fsum(w["sum"] for w in workers) / n
    variance = (math.fsum(w["sumsq"] for w in workers) - n * mean**2) / (n - 1)
    close(math.sqrt(variance), reference["sd"], "iid actual onepath sd")
    close(math.sqrt(variance / n), reference["se"], "iid mean SE")
    row = common_row(
        case, "iid-reference", inventory.transform_bindings(("c3_refb.py", "scrambles.py"))
    )
    row.update(
        law="PCG64 independentnormal numericalgenerator,commonplusidio onefactor exactmonitored-date stepping",
        integrand="discounted unsmoothed plainmonitored knockoutpayoff",
        normal_coordinates=CASES[case][1] * (CASES[case][0] + 1),
        one_path_sigma=dict(
            sample_sd_dollars=math.sqrt(variance),
            sample_variance_dollars_squared=variance,
            actual_paths=n,
            ddof=1,
            raw_worker_aggregates_reconciled=True,
            receipt_binding=inventory.binding(reference_path),
            certified_population_upper_bound=False,
        ),
        iid_mean_variance_measurement=dict(
            estimated_variance_dollars_squared=variance / n,
            standard_error_dollars=reference["se"],
            actual_iid_paths=n,
            formula="Samplepathvariance/actualindependentpathcount; thisidentitydoesnotapplytoscrambledRQMC prefixpoints",
            normal_approximation_hw99_dollars=reference["hw99"],
            rigorous_population_error_certificate=None,
        ),
        independent_scramble_variance_measurements=[],
        quantum_smoothing_or_variance_credit_available=False,
        measured_error_cost_model="Thisrowis theexistingfixedbudgetreference,notanaccuracy-target time-to-delivery anchor.",
    )
    row["one_path_population_variance_upper_bound"] = dict(
        upper_dollars_squared_exact=[400, 1],
        law="ideal original continuous monitored discountedpayoff",
        proof="Originalsurvivalimpliespositivepayoffbelow40;Popoviciu",
        actual_float64_transform_bias_bound_dollars=None,
    )
    rows.append(row)
    return rows


def native_row(inventory, case):
    target_path = PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json"
    target = inventory.json(target_path)
    support_path = PROGRAM / "E03_support_run001" / (case + "_certificate.json")
    audit_path = PROGRAM / "E03_support_audit_run002" / (case + "_audit.json")
    support, audit = read(support_path), read(audit_path)
    assert audit["passed"] and support["payoff_raw_bounds"] == audit["payoff_raw_bounds"]
    assert support["target_output"] == target["outputs"]
    assert (
        support["width"] == target["width"] == 72
        and support["fraction_bits"] == target["fraction_bits"] == 40
    )
    native_binding = read(PROGRAM / "E02_financial_run002" / case / "estimator_ledger.json")
    binding = native_binding["binding"]
    assert (
        binding["case"] == case and binding["word_width"] == 72 and binding["fraction_bits"] == 40
    )
    assert binding["selector_bits"] == 46 and binding["dollar_span"] == 64
    assert binding["hashes"]["target.json"] == inventory.files[relative(target_path)]["sha256"]
    assert (
        binding["payoff_raw_bounds"] == support["payoff_raw_bounds"]
        and not binding["second_discount_applied"]
    )
    for name in ("source.json", "schedule_capped.json"):
        assert sha(binding["paths"][name]) == binding["hashes"][name]
    assert (
        native_binding["price_output_already_discounted"]
        and not native_binding["second_discount_applied"]
    )
    assert (
        native_binding["normalization_span_dollars"] == 64
        and native_binding["adaptive_quantum_rounds"] == 0
    )
    assert (
        native_binding["financial_forwards"]
        == native_binding["financial_literal_inverses"]
        == 983025
    )
    assert not native_binding["full_continuous_price_certificate"]
    for directory in (PROGRAM / "E03_support_run001", PROGRAM / "E03_support_audit_run002"):
        manifest = read(directory / "manifest.json")
        names = {
            name.replace("\\", "/"): digest for name, digest in manifest["frozen_inputs"].items()
        }
        assert names[relative(target_path)] == inventory.files[relative(target_path)]["sha256"]
    q = 1 << 40
    lower, upper = (Fraction(value, q) for value in support["payoff_raw_bounds"])
    assert 0 == lower <= upper < 40
    variance_upper = (upper - lower) ** 2 / 4
    y_node = next(node for node in target["nodes"] if target["outputs"]["Y"] in node["out"])
    assert y_node["op"] == "select"
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    discount_node = producers[y_node["args"][1]]
    assert (
        discount_node["op"] == "cmul"
        and discount_node["params"]["c"] == support["discount_coefficient"]
    )
    inputs = [node for node in target["nodes"] if node["op"] == "input"]
    words = 60 if case == "B4x12" else 468
    assert len(inputs) == words and all(n["params"]["bits"] == 32 for n in inputs)
    row = common_row(
        case,
        "native-quantum-payoff",
        [
            inventory.binding(target_path),
            dict(
                source=relative(Path(binding["paths"]["source.json"])),
                sha256=binding["hashes"]["source.json"],
            ),
            dict(
                estimator_ledger=relative(
                    PROGRAM / "E02_financial_run002" / case / "estimator_ledger.json"
                ),
                sha256=sha(PROGRAM / "E02_financial_run002" / case / "estimator_ledger.json"),
            ),
        ],
    )
    row["normalization"].update(
        native_fixed_point_fraction_bits=40,
        native_integer_to_dollars_scale_exact=[1, q],
        native_discount_literal_exact=encoded(Fraction(support["discount_coefficient"], q)),
        amplitude_normalization_span_dollars=64,
        selector_bits=46,
        probability_identity="p=E[Yraw]/2^46=E[alreadydiscountednativeYdollars]/64",
    )
    row.update(
        law="Uniformproduct32bitinputwords,exactf40midpoints,jointsharedinputBoxMuller,nativetableandEstrinarithmetic,clippedlogprefixes andstrictmonitoring",
        integrand="Unsmoothedoriginalnative discounted knockoutpayoffY,notaclassicalconditionalexpectation orsurvivalweightedtransform",
        random_uniform_words=words,
        joint_Box_Muller_pairs=words // 2,
        finite_outputs_claimed_independent_gaussian=False,
        one_path_sigma=None,
        one_path_population_variance_upper_bound=dict(
            upper_dollars_squared_exact=encoded(variance_upper),
            law="Actualacceptednativefinite source,allinputwords",
            proof="IndependentlyauditedactualYsupportplusPopoviciu",
            native_payoff_support_dollars_exact=[encoded(lower), encoded(upper)],
            native_payoff_support_raw=support["payoff_raw_bounds"],
            native_path_sigma_upper_dollars_exact=encoded((upper - lower) / 2),
            certificate=relative(support_path),
            certificate_sha256=sha(support_path),
            independent_audit=relative(audit_path),
            independent_audit_sha256=sha(audit_path),
        ),
        normalized_payoff_value_population_variance_upper_exact=encoded(variance_upper / 64**2),
        selector_marking_Bernoulli_population_variance_upper_exact=[1, 4],
        selector_variance_is_not_scaled_path_payoff_variance=True,
        independent_scramble_variance_measurements=[],
        iid_mean_variance_measurement=None,
        measured_native_path_sigma=None,
        classical_smoothed_path_sigma_credited=False,
        classical_scramble_mean_variance_credited=False,
        current_estimator_kind="Sourcecompatible boundedrangeQPE with64dollarspan; itdoesnotconsumea smoothedclassicalsigma",
        current_Grover_invocations=983025,
        current_fresh_preparations=native_binding["fresh_preparations"],
        extra_coherent_preintegration_or_OSS_source_implemented=False,
        rangebound_does_not_close_continuous_G2=True,
    )
    return row


def unsupported_credits():
    records = []
    for case in CASES:
        for benefit, reason in (
            (
                "classical preintegrated path sigma assigned to native quantum payoff",
                "AcceptednativeY isunsmoothed; no samecoherentconditionalexpectation sourceoritscleanup/errorcostexistsinthismenu",
            ),
            (
                "classical OSS or OSS-BB variance assigned to native quantum payoff",
                "Survivalconditioningchangesgeneratorandintegrandweights; thesametransformisnotimplementedintheacceptednative source",
            ),
            (
                "classical independent-scramble mean variance assigned to quantum path variance",
                "RQMCmeanvarianceincludescovarianceofpointswithin ascramble; itisnota onepathvarianceandthenativeestimatorisnotclassicalRQMC",
            ),
            (
                "continuous plain path sigma treated as certified native finite-law sigma",
                "Fullcontinuous/digital lawbridge remainsopen andpilotconfidence isnota99percentnativepopulationbound",
            ),
            (
                "iid sigma divided by epsilon substituted for measured classical RQMC cost",
                "RQMCerrorversuspointcount andcompleteactualtimingmustbefitted/measuredforthechosenclassicaltransform",
            ),
            (
                "residual variance reduction without covariance/range and implemented source",
                "Nocertifiedresidualorcoherentcontrolisimplementedinthefixedactive menu; missingboundremainsnull",
            ),
        ):
            records.append(
                dict(
                    case=case,
                    proposed_credit=benefit,
                    available=False,
                    reason=reason,
                    native_cost_or_statistical_budget_reduced=False,
                )
            )
    return records


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert (
        sha(sys.executable) == protocol["interpreter_sha256"]
        and np.__version__ == protocol["numpy"]
    )
    inventory = FrozenInventory()
    c1 = inventory.json(CLASSICAL / "c1/c1_summary.json")
    c5 = inventory.json(CLASSICAL / "c5/rates/c5_rates.json")
    pilot = inventory.json(CLASSICAL / "sigma_dev/sigma_dev.json")["cases"]
    refa = inventory.json(CLASSICAL / "c3_refa/ref_a.json")
    rows = []
    for case in CASES:
        case_rows = classical_rows(inventory, case, c1, c5, pilot, refa)
        case_rows.append(native_row(inventory, case))
        assert [row["method"] for row in case_rows] == list(METHODS)
        rows.extend(case_rows)
        print(case, "six exact estimand/variance interfaces reconciled", flush=True)
    assert [dict(case=row["case"], method=row["method"]) for row in rows] == protocol["finite_menu"]
    assert len(rows) == 12 and all(
        row["residual_range_dollars"]
        is row["residual_variance_upper_bound"]
        is row["residual_covariance_bound"]
        is None
        for row in rows
    )
    assert all(not row["residual_or_coherent_control_implemented"] for row in rows)
    save(output / "estimand_ledger.json", rows)
    unsupported = unsupported_credits()
    save(output / "unsupported_credits.json", unsupported)
    prior = read(INVENTORY / "summary.json")
    assert prior["passed"] and not prior["C09_complete"] and not prior["G4_closed"]
    blockers = dict(
        C09_summary_sha256=sha(INVENTORY / "summary.json"),
        common_full_price_law_bridge_certified=False,
        actual_reference_status=prior["actual_reference_status"],
        coverage_complete_and_scored=prior["coverage_complete_and_scored"],
        source_provenance=read(INVENTORY / "recorded_source_provenance_audit.json"),
        measured_and_modelled_timing_status=prior["candidate_timing_rows"],
        existing_jobs_untouched=True,
        original_reference_coverage_provenance_blockers_removed=False,
        finite_estimator_confidence_is_not_continuous_financial_confidence=True,
    )
    save(output / "preserved_classical_financial_blockers.json", blockers)
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            fixed_active_menu_rows=12,
            cases=list(CASES),
            methods=list(METHODS),
            classical_rows=10,
            native_quantum_rows=2,
            path_sigma_and_scramble_mean_variance_distinguished=True,
            within_scramble_dependence_preserved=True,
            actual_prefix_variance_reconciliations=sum(
                len(row["independent_scramble_variance_measurements"])
                + len(row.get("additional_64_scramble_reference_variance_measurements", []))
                for row in rows
            ),
            classical_smoothed_variance_assigned_to_native_quantum_source=False,
            native_population_variance_bounds_from_actual_support=True,
            selector_Bernoulli_and_payoff_value_variance_distinguished=True,
            coherent_variance_reduction_source_implemented=False,
            unsupported_credit_rows=len(unsupported),
            unsupported_variance_credits_removed_from_active_interfaces=True,
            current_range_based_estimator_cost_rows_unchanged=True,
            no_population99_confidence_awarded_to_bootstrap95_or_pilots=True,
            new_financial_draws=0,
            new_financial_gate_replays=0,
            new_bootstraps=0,
            new_timing_runs=0,
            C09_reference_coverage_provenance_blockers_preserved=True,
            C09_complete=False,
            full_G2_closed=False,
            G4_closed=False,
            complete_quantum_advantage_claim=False,
            physical_runtime_seconds=None,
        ),
    )
    verify(protocol["frozen_inputs"])
    finish_manifest(output)
    print("F02 estimand/variance ledger PASS; no unsupported smoothing credit", flush=True)


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    local_only=True,
                    new_financial_draws=0,
                    new_financial_gate_replays=0,
                    C09_complete=False,
                    full_G2_closed=False,
                    G4_closed=False,
                ),
            )
            finish_manifest(output)
            raise
