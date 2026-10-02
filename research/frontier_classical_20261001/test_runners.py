import hashlib
import json
import math

import pytest

pytest.importorskip("numba")

from research.frontier_classical_20261001 import c2_timing  # noqa: E402
from research.frontier_classical_20261001.c4_coverage import references  # noqa: E402
from research.frontier_classical_20261001.c7_c8_cases import c8_cases  # noqa: E402
from research.frontier_classical_20261001.fit import SHARE, windows  # noqa: E402


def block(confirm=None):
    marks = [2 ** m for m in range(6, 20)]
    warm = [dict(all16={n: 0.5 + 1e-5 * max(n, 4096) for n in marks})] * 5
    fresh = dict(all16={n: 4.5 + 1e-5 * max(n, 4096) for n in marks})
    return dict(warm=warm, fresh=fresh, confirmation=confirm or {},
                fits=dict(all16=(0.5, 1e-5), per_scramble=(0.4, 1e-5), load_balanced=(0.6, 1e-5)))


def est(n):
    return dict(n_eps={"0.001": dict(point=n)}, fits=dict(primary=dict(r=0.6)))


def test_t_c_modelled_and_small_n_branches():
    big = c2_timing.t_c(block(), est(5e5), 0.001)
    assert big["convention"] == "modelled all-16" and math.isclose(big["primary"], 0.5 + 5.0)
    small = c2_timing.t_c(block(), est(100.0), 0.001)
    assert small["convention"] == "measured small-n mark" and small["mark"] == 128
    assert math.isclose(small["fresh_cached"] - small["primary"], 4.0)


def test_t_c_confirmation_scales_only_when_accuracy_is_missed():
    def confirm(sd):
        means = [3.5 + sd * ((-1) ** k) for k in range(16)]
        return {"0.001": dict(n_run=2 ** 17, runs=[dict(wall=2.0, hw99=0.0,
                                                         scramble_means=means)] * 20)}
    ok = c2_timing.t_c(block(confirm(1e-5)), est(1e5), 0.001)
    assert ok["convention"] == "measured confirmation" and ok["scale"] == 1.0
    miss = c2_timing.t_c(block(confirm(1e-2)), est(1e5), 0.001)
    hw16 = miss["pooled_hw16"]
    assert miss["scale"] > 1.0 and math.isclose(
        miss["primary"], 2.0 * (hw16 / (SHARE * 0.001)) ** (1 / 0.6))


def test_fit_windows_follow_the_spec():
    assert "w14" in windows(19) and "w14" in windows(18) and "w14" not in windows(17)
    assert windows(17)["primary"] == (10, 17)


def test_c8_generator_is_pinned():
    cases = [tuple(round(v, 12) if isinstance(v, float) else v for v in c.__dict__.values())
             for c in c8_cases()]
    digest = hashlib.sha256(json.dumps(cases).encode()).hexdigest()
    assert len(cases) == 24 and [c[0] for c in cases] == list(range(100, 124))
    assert digest == "c16634919ee906af008012b273c5c7ce8494118ac017ebc6240e0a76f6d56848"


def test_oracle_build_case_restores_module_constants():
    pytest.importorskip("qiskit")
    from research.frontier_classical_20261001 import oracle
    from research.frontier_classical_20261001.scrambles import Case
    before = {k: getattr(oracle.bod, k) for k in oracle.CONSTANTS}
    oracle.build_case(Case(9, 4, 12, barrier=150.0, sigma=0.2))
    with pytest.raises(Exception):
        oracle.build_case(Case(9, 0, 12))
    assert {k: getattr(oracle.bod, k) for k in oracle.CONSTANTS} == before


def test_references_pass_and_weight(tmp_path):
    (tmp_path / "c3_refa").mkdir()
    (tmp_path / "c3_refa" / "ref_a.json").write_text(json.dumps(dict(cases={
        n: dict(price=1.0, se=1e-4, hw99=2.6e-4) for n in ("B4x12", "B8x52")})))
    for n, price in (("B4x12", 1.0001), ("B8x52", 1.01)):
        (tmp_path / "c3_refb" / n).mkdir(parents=True)
        (tmp_path / "c3_refb" / n / "ref_b.json").write_text(json.dumps(
            dict(price=price, se=1e-4, hw99=2.6e-4)))
    r = references(tmp_path)
    assert r["B4x12"]["agreement_passed"] and math.isclose(r["B4x12"]["reference"], 1.00005)
    assert not r["B8x52"]["agreement_passed"] and r["B8x52"]["reference"] is None
