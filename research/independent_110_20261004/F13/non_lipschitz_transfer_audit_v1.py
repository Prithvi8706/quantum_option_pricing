"""Bounded primary-theorem transfer audit for S4. No paths or timing runs."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import time
from fractions import Fraction as Q
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/independent_110_20261004/F13/run001"
DOC = ROOT / "docs/independent_110_20261004/F13"
AUTHOR = Path(__file__).resolve()
CORPUS = ["research/antithetic_feasibility/classical.py",
          "docs/antithetic_feasibility/RESULTS.md",
          "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
          "research/independent_110_20261004/F13/primary_sources/Pang_Wang_2305_12992v2.html"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class ReadMath(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag == "math":
            self.parts.append(dict(attrs).get("alttext", "")); self.skip += 1
    def handle_endtag(self, tag):
        if tag == "math": self.skip -= 1
    def handle_data(self, data):
        if self.skip == 0: self.parts.append(data)


def prepare():
    if OUT.exists(): raise ValueError("Fresh F13 run required.")
    OUT.mkdir(parents=True)
    dump(OUT / "protocol.json", {"schema": "f13-primary-theorem-transfer-preflight-v1",
        "author_sha256": sha(AUTHOR), "corpus": {p: sha(ROOT / p) for p in CORPUS},
        "theorem": "Pang and Wang arXiv2305.12992v2, Assumptions3.1-3.3 and Theorem5.1/Section5 payoff condition",
        "model": "Existing S4: kappa2, theta.04, xi.5, v0.04, leverage-.7; no model change.",
        "assumptions": ["The variance equation is CIR: drift kappa(theta-v), diffusion xi*sqrt(v) on v>=0.", "Lamperti Ito algebra is asserted only on v>0; no boundary extension is assumed.", "Exact counterexample sequences are analytic proof witnesses, not finite-difference derivative proofs."],
        "acceptance": ["Bind S4 parameters to frozen source AST and primary hypothesis locators.", "Classify each required hypothesis proved, failed or unresolved for the original state/payoff.", "Prove a failed coupled monotonicity condition for every finite C, p1>1 and xi>0.", "Check one optional Lamperti transform without claiming a boundary repair.", "Keep actual scheme admissibility, boundary behavior and population variance exponent unresolved where not proved."],
        "diagnostic_menu": {"C_values": [0, 1, 2, 10, 100, 10000], "p1_values": [[3, 2], [2, 1], [3, 1]], "Lamperti_y": [[1, 1], [1, 2], [1, 4], [1, 8], [1, 16], [1, 32]]},
        "budgets": {"cpu_seconds": 30, "wall_seconds": 60, "output_bytes": 4 * 1024 * 1024},
        "stop_rule": "One theorem assumption map and one optional transform; stop direct transfer on a failed necessary condition. No path simulation, fitting, payoff smoothing, compilation or additional theorem search.",
        "finance_draws": 0, "new_global_fixture_credit": 0})
    print("F13 S4/one-theorem/one-transform protocol frozen.")


PROOF = """F13: S4 DOES NOT SATISFY THE NOMINATED NON-GLOBALLY-LIPSCHITZ THEOREM

Primary evidence: Pang and Wang arXiv2305.12992v2 (11September2024),
Assumptions3.1-3.3, equations3.1-3.5, Section5 and Theorem5.1:
https://arxiv.org/html/2305.12992v2
Their required domain is R^d; drift is C1, diffusion columns are C2,
coefficient derivatives obey polynomial local growth bounds, and a coupled
monotonicity inequality holds. The modified scheme has additional admissibility
conditions. The variance result also uses its specified smooth payoff class.
These are precise requirements, not a claim that every non-Lipschitz SDE is covered.

Current frozen S4 variance: dv=kappa(theta-v)dt+xi*sqrt(v)dW,
kappa=2, theta=1/25, xi=1/2, v0=1/25. Its algebraic Feller ratio
2*kappa*theta/xi^2=16/25 is recorded only as a parameter fact here; no
boundary-hitting or convergence theorem is inferred from it.

Necessary-condition counterexample
The scalar variance component already defeats equation3.2. Set w=0,v=h>0,
and keep other state coordinates equal. The scalar contribution to the
required left side divided by h^2 is
 -2*kappa + (2*p1-1)*xi^2/h.
Additional price diffusion differences cannot reduce this contribution.
For every finite C>=0 and p1>1, let c=(2*p1-1)*xi^2>0 and
 h=c/[2*(C+2*kappa+1)]. The ratio becomes2*C+2*kappa+2>C.
Hence no finite C satisfies the required inequality even on the closed
physical half-space. This is an analytic forall-C proof, not a sampled claim.
Independently, sqrt(v) has derivative1/(2sqrt(v)) on v>0 and no finite
right derivative at0; the diffusion is not C2 across the zero boundary.
An arbitrary extension to negative v cannot repair its right derivative at0
while preserving the original square-root coefficient for all v>=0.

The log-price/variance drift is affine, so its differentiability is not the
obstruction. On the physical half-space its coercivity growth can be bounded
by Young inequalities: |x*v|<=(x^2+v^2)/2, and all remaining drift/diffusion
terms have at most quadratic growth. That restricted inequality does not
remove the full-domain, diffusion smoothness or coupled-monotonicity failures.
Deterministic initial state has every finite moment. High scheme/trajectory
moments and Assumption3.3's exact modification bounds are unverified; they
are not set to satisfied merely because selected numerical paths are positive.
The original positive-part payoff has a kink at strike; the left derivative
is0 and right derivative1. It therefore does not meet a C2 payoff premise
without a separately certified smoothing/boundary argument.

One optional Lamperti transform
For Y=2sqrt(v)/xi and while v>0, Ito's rule gives
 dY=[a/Y-kappa*Y/2]dt+dW, a=2*kappa*theta/xi^2-1/2=7/50.
Although diffusion is now constant, the drift derivative is
 -a/Y^2-kappa/2, and its derivative grows as2*a/Y^3 near0. These
singularities on a bounded neighborhood cannot meet the specified polynomial
derivative bounds on all R^d. The transform is undefined at the same boundary;
the Ito identity before hitting it is not a global boundary-preserving process
construction. No transformed boundary extension or complete antithetic
scheme is supplied, and no numerical simulation is used to infer one.

Decision and completion scope
Completed the single F13 theorem-transfer audit and optional transform screen:
reject this direct application for unchanged S4. This does not refute the
paper, prove an S4 variance lower bound, or rule out another boundary-specific
theorem/scheme. Keep F12's empirical coupling question separate and preserve
all prior rates as observations. No existing workload, payoff, source,
confidence allocation or quantum-advantage claim changes.
"""


def run():
    tc, tw = time.process_time(), time.monotonic()
    p = json.loads((OUT / "protocol.json").read_text())
    if (OUT / "RUN_STARTED.json").exists(): raise ValueError("F13 one-attempt rule.")
    assert sha(AUTHOR) == p["author_sha256"]
    for path, expected in p["corpus"].items(): assert sha(ROOT / path) == expected
    dump(OUT / "RUN_STARTED.json", {"finance_draws": 0})
    tree = ast.parse((ROOT / CORPUS[0]).read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Model")
    defaults = {n.target.id: ast.literal_eval(n.value) for n in cls.body if isinstance(n, ast.AnnAssign)}
    ms = next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MODELS" for t in n.targets))
    call = next(c for c in ms.elts if any(k.arg == "name" and ast.literal_eval(k.value) == "S4" for k in c.keywords))
    model = dict(defaults); model.update({k.arg: ast.literal_eval(k.value) for k in call.keywords})
    kappa, theta, xi = [Q(str(model[k])) for k in ["kappa", "theta", "xi"]]
    assert (kappa, theta, xi, Q(str(model["v0"])), Q(str(model["leverage"]))) == (Q(2), Q(1, 25), Q(1, 2), Q(1, 25), Q(-7, 10))
    parser = ReadMath(); parser.feed((ROOT / CORPUS[-1]).read_text(encoding="utf-8"))
    text = " ".join(" ".join(parser.parts).split())
    for label in ["Assumption 3.1", "Assumption 3.2", "Assumption 3.3", "Theorem 5.1", "twice continuously differentiable"]:
        assert label in text
    witnesses = []
    for C in p["diagnostic_menu"]["C_values"]:
        for pair in p["diagnostic_menu"]["p1_values"]:
            p1 = Q(*pair); c = (2 * p1 - 1) * xi * xi
            h = c / (2 * (C + 2 * kappa + 1))
            left = -2 * kappa * h * h + c * h
            right = C * h * h
            assert h > 0 and left > right
            witnesses.append({"C": C, "p1": str(p1), "h": str(h), "left": str(left), "right": str(right), "required_inequality_fails": True})
    a = 2 * kappa * theta / (xi * xi) - Q(1, 2)
    assert a == Q(7, 50)
    transformed = []
    previous = Q()
    for pair in p["diagnostic_menu"]["Lamperti_y"]:
        y = Q(*pair); derivative = -a / (y * y) - kappa / 2
        assert abs(derivative) > previous
        previous = abs(derivative)
        # Ito substitution identity for the transform, before zero is reached.
        v = xi * xi * y * y / 4
        drift_chain = (kappa * (theta - v) / (xi * (xi * y / 2))) - Q(1, 4) * xi / (xi * y / 2)
        assert drift_chain == a / y - kappa * y / 2
        transformed.append({"y": str(y), "drift_derivative": str(derivative), "Ito_drift_identity": True})
    mapping = [
        {"hypothesis": "3.1 full R^d coercivity/domain", "status": "unresolved_full_domain; restricted physical-space growth bounded", "proof": "Young inequalities for affine log-price/variance drift; square-root diffusion lacks declared negative-v extension."},
        {"hypothesis": "3.2 drift C1", "status": "proved", "proof": "Affine drift in log-price/variance state."},
        {"hypothesis": "3.2 diffusion C2", "status": "failed", "proof": "Right derivative xi/(2sqrt(v)) diverges at0."},
        {"hypothesis": "3.2 equation3.2 coupled monotonicity", "status": "failed", "proof": "Universal C/p1 variance-component counterexample above."},
        {"hypothesis": "3.2 equations3.3-3.4 derivative growth", "status": "failed_for_diffusion; other directional products not needed after necessary failures", "proof": "Boundary derivatives diverge on bounded sets."},
        {"hypothesis": "3.2 equation3.5 initial finite moments", "status": "proved", "proof": "Fixed deterministic finite S4 initial state."},
        {"hypothesis": "3.3 modified scheme bounds", "status": "unresolved", "proof": "No identity with all prescribed modifications and finite bounds is certified."},
        {"hypothesis": "Section5 smooth payoff premise", "status": "failed_for_unchanged_positive_part", "proof": "At strike the one-sided derivatives are0 and1."},
        {"hypothesis": "Theorem5.1 required high scheme moments", "status": "unresolved", "proof": "No high-moment numerical-scheme certificate; simulation positivity is insufficient."},
        {"hypothesis": "Lamperti optional transform", "status": "failed_direct_transfer", "proof": "Constant diffusion but singular drift/derivatives and unresolved boundary extension."},
    ]
    dump(OUT / "assumption_map.json", {"model": model, "Feller_ratio_parameter_only": str(2*kappa*theta/(xi*xi)), "primary_html_sha256": p["corpus"][CORPUS[-1]], "mapping": mapping, "monotonicity_witnesses": witnesses, "Lamperti_checks": transformed})
    summary = {"passed": True, "completed": True, "decision": "direct_theorem_transfer_rejected",
        "scope": "One nominated F13 S4 primary-theorem map plus one Lamperti transform; no general theorem search or convergence rate claim.",
        "hypothesis_rows": len(mapping), "exact_monotonicity_counterchecks": len(witnesses), "exact_Ito_transform_checks": len(transformed),
        "analytic_universal_counterexample": True, "derivatives_proved_by_finite_differences": False,
        "finance_draws": 0, "new_global_fixture_credit": 0, "quantum_advantage": False,
        "remaining": ["A separately justified boundary-specific theorem/scheme.", "Original payoff/boundary smoothing error if a new transfer is proposed.", "Population antithetic correction variance/moment certificates for unchanged S4."]}
    dump(OUT / "summary.json", summary)
    DOC.mkdir(parents=True, exist_ok=True); proof = DOC / "THEOREM_TRANSFER.txt"
    if proof.exists(): raise ValueError("Fresh F13 proof required.")
    proof.write_text(PROOF, encoding="utf-8")
    for path, expected in p["corpus"].items(): assert sha(ROOT / path) == expected
    assert time.process_time()-tc <= p["budgets"]["cpu_seconds"] and time.monotonic()-tw <= p["budgets"]["wall_seconds"]
    files = list(OUT.iterdir())+[proof]
    assert sum(f.stat().st_size for f in files if f.is_file()) <= p["budgets"]["output_bytes"]
    dump(OUT / "manifest.json", {"files": {str(f.relative_to(ROOT)).replace('\\', '/'): {"sha256": sha(f), "bytes": f.stat().st_size} for f in sorted(files) if f.is_file()}, "author_sha256": p["author_sha256"], "input_pins": p["corpus"]})
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args(); prepare() if args.mode == "prepare" else run()
