"""Q4: payoff validation of the Stage A integer IR against an independent float64 reference
(ANALYSIS_SPEC_STAGE_C.md, Q4).

The reference is written from the IR's input law, without importing its builder: uniforms
u = (raw + 1/2)/2^32; normals in pairs (2j, 2j+1) = r cos 2 pi v, r sin 2 pi v with
r = sqrt(-2 ln u); per date j, normal j(na+1) is the common factor (sigma sqrt(rho dt)) and
normal j(na+1)+1+i the idiosyncratic factor of asset i (sigma sqrt((1-rho) dt)); drift
(r - sigma^2/2) dt; log spots prefix-summed. The IR clips each log spot to
[ln 2^-16, ln 4096] before exponentiating; the reference does not, and counts clip events.
  python -m research.frontier_classical_20261001.q4_payoff --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import subprocess
from pathlib import Path

import numba
import numpy as np
from scipy.stats import beta

from research.controlled_source_completion.ir import evaluate

ROOT_Q4 = 2026100191
STAGE_A = sc.ROOT / "results/frontier_completion_20260927/stage_a"
N_IID, N_NEAR, N_KO, N_ITM_DEAD, N_EXTREME = 5000, 5000, 50, 50, 2000
LAW_PATHS, WORKERS, BATCH = 10 ** 7, 16, 2 ** 15
CLIP_LO, CLIP_HI = math.log(2.0 ** -16), math.log(4096.0)
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))


@numba.njit(cache=True)
def reference(u, na, nt, sigma, rho, rate, maturity, spot, strike, barrier, clip):
    """Rows of uniforms u in (0, 1) -> (payoff, max date basket, average, clipped). With
    clip=True the log spots are clipped before exp, as in the IR."""
    n = u.shape[0]
    out = np.empty((n, 4))
    dt = maturity / nt
    drift = (rate - sigma * sigma / 2) * dt
    vc = sigma * math.sqrt(rho * dt)
    vi = sigma * math.sqrt((1 - rho) * dt)
    count = nt * (na + 1)
    z = np.empty(count + 1)
    logs = np.empty(na)
    for p in range(n):
        for j in range((count + 1) // 2):
            r = math.sqrt(-2.0 * math.log(u[p, 2 * j]))
            ang = 2.0 * math.pi * u[p, 2 * j + 1]
            z[2 * j] = r * math.cos(ang)
            z[2 * j + 1] = r * math.sin(ang)
        for i in range(na):
            logs[i] = math.log(spot)
        total, maxb, clipped = 0.0, -1.0, 0.0
        for j in range(nt):
            basket = 0.0
            for i in range(na):
                logs[i] += drift + vc * z[j * (na + 1)] + vi * z[j * (na + 1) + 1 + i]
                x = logs[i]
                if x < CLIP_LO or x > CLIP_HI:
                    clipped = 1.0
                    if clip:
                        x = min(max(x, CLIP_LO), CLIP_HI)
                s = math.exp(x)
                basket += s
                total += s
            basket /= na
            maxb = max(maxb, basket)
        avg = total / (na * nt)
        alive = maxb < barrier
        out[p, 0] = math.exp(-rate * maturity) * max(avg - strike, 0.0) if alive else 0.0
        out[p, 1], out[p, 2], out[p, 3] = maxb, avg, clipped
    return out


def midpoint(raw):
    return (raw.astype(np.float64) + 0.5) / 2.0 ** 32


def ref_raw(case, raw):
    return reference(midpoint(raw), case.na, case.nt, case.sigma, case.rho, case.rate,
                     case.maturity, case.spot, case.strike, case.barrier, False)


def load_target(case):
    name = f"B{case.na}x{case.nt}"
    path = STAGE_A / name / "target.json"
    expected = json.loads((STAGE_A / "artifact_hashes.json").read_text())[f"{name}/target.json"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"{path} hash mismatch")
    data = json.loads(path.read_text())
    producer = {o: n for n in data["nodes"] for o in n["out"]}
    h = round(case.barrier * 2 ** data["fraction_bits"])
    lts = [n for n in data["nodes"] if n["op"] == "lt" and producer[n["args"][1]]["op"] == "const"
           and producer[n["args"][1]]["params"]["value"] == h]
    assert len(lts) == 1, "barrier comparison node not unique"
    return data, lts[0]["args"][0], actual


def ir_task(args):
    case, raw = args
    data, max_arg, _ = load_target(case)
    w, f = data["width"], data["fraction_bits"]
    count = sum(1 for n in data["nodes"] if n["op"] == "input")
    out, vals = evaluate(data, {f"uniform_{k}": int(raw[k]) for k in range(count)}, trace=True)
    m = vals[max_arg]
    return out["Y"], (m - 2 ** w if m & 2 ** (w - 1) else m) / 2 ** f


def draws(case, n_uniform):
    """iid, near-barrier, and edge raw draws (each a row of n_uniform 32-bit integers)."""
    def gen(stratum):
        return np.random.default_rng([ROOT_Q4, case.case_index, 6, stratum, 0])
    iid = gen(0).integers(0, 2 ** 32, size=(N_IID, n_uniform), dtype=np.uint64)
    rng, near = gen(1), []
    while sum(len(x) for x in near) < N_NEAR:
        cand = rng.integers(0, 2 ** 32, size=(BATCH, n_uniform), dtype=np.uint64)
        maxb = ref_raw(case, cand)[:, 1]
        near.append(cand[np.abs(maxb - case.barrier) <= 0.01 * case.barrier])
    near = np.concatenate(near)[:N_NEAR]
    rng = gen(2)
    pool = rng.integers(0, 2 ** 32, size=(BATCH, n_uniform), dtype=np.uint64)
    r = ref_raw(case, pool)
    knocked = pool[r[:, 1] >= case.barrier][:N_KO]
    itm_dead = pool[(r[:, 1] < case.barrier) & (r[:, 2] < case.strike)][:N_ITM_DEAD]
    fixed = [np.zeros(n_uniform, np.uint64), np.full(n_uniform, 2 ** 32 - 1, np.uint64),
             np.where(np.arange(n_uniform) % 2, 2 ** 32 - 1, 0).astype(np.uint64)]
    for angle in (0, 2 ** 30, 2 ** 31, 3 * 2 ** 30):
        row = np.zeros(n_uniform, np.uint64)
        row[1::2] = angle
        fixed.append(row)
    ext = np.zeros((N_EXTREME, n_uniform), np.uint64)
    ext[:, 1::2] = rng.choice(np.array([0, 2 ** 30, 2 ** 31, 3 * 2 ** 30], np.uint64),
                              size=(N_EXTREME, n_uniform // 2))
    clipped = ext[ref_raw(case, ext)[:, 3] > 0][:20]
    edge = np.concatenate([knocked, itm_dead, np.array(fixed), clipped])
    return dict(iid=iid, near=near, edge=edge), int(len(clipped))


def law_task(args):
    """CRN law error and barrier-band counts on one worker's 10^7/16 continuous paths."""
    case, worker, delta = args
    rng_law = np.random.default_rng([ROOT_Q4, case.case_index, 8, 0, worker])
    rng_flip = np.random.default_rng([ROOT_Q4, case.case_index, 8, 1, worker])
    n_uniform = 2 * ((case.nt * (case.na + 1) + 1) // 2)
    params = (case.na, case.nt, case.sigma, case.rho, case.rate, case.maturity, case.spot,
              case.strike, case.barrier)
    diffs, band, total = [], 0, 0
    todo = LAW_PATHS // WORKERS
    while total < todo:
        size = min(BATCH, todo - total)
        u = rng_law.random((size, n_uniform))
        u[u == 0.0] = 2.0 ** -60
        cont = reference(u, *params, False)[:, 0]
        disc = reference(midpoint(np.floor(u * 2.0 ** 32)), *params, True)[:, 0]
        diffs.append(float((disc - cont).sum()))
        diffs.append(float(((disc - cont) ** 2).sum()))
        v = rng_flip.random((size, n_uniform))
        v[v == 0.0] = 2.0 ** -60
        band += int((np.abs(reference(v, *params, False)[:, 1] - case.barrier) <= delta).sum())
        total += size
    return total, math.fsum(diffs[0::2]), math.fsum(diffs[1::2]), band


def validate(case, pool):
    data, _, digest = load_target(case)
    n_uniform = sum(1 for n in data["nodes"] if n["op"] == "input")
    sets, clip_found = draws(case, n_uniform)
    result = dict(target_sha256=digest, clip_draws_found=clip_found, strata={})
    worst, delta_fp, flips_b, flips_k = 0.0, 0.0, 0, 0
    for name, raw in sets.items():
        ir = pool.map(ir_task, [(case, row) for row in raw], chunksize=8)
        ref = ref_raw(case, raw)
        y_ir = np.array([x[0] for x in ir])
        m_ir = np.array([x[1] for x in ir])
        b_flip = (m_ir < case.barrier) != (ref[:, 1] < case.barrier)
        k_flip = ~b_flip & ((y_ir > 0) != (ref[:, 0] > 0))
        ok = ~b_flip & ~k_flip & (ref[:, 3] == 0)
        err = float(np.abs(y_ir - ref[:, 0])[ok].max()) if ok.any() else 0.0
        worst, delta_fp = max(worst, err), max(delta_fp, float(np.abs(m_ir - ref[:, 1]).max()))
        flips_b, flips_k = flips_b + int(b_flip.sum()), flips_k + int(k_flip.sum())
        result["strata"][name] = dict(draws=len(raw), barrier_flips=int(b_flip.sum()),
                                      strike_flips=int(k_flip.sum()),
                                      clip_events=int((ref[:, 3] > 0).sum()),
                                      max_abs_error_unflipped=err)
    delta = 10 * delta_fp
    rows = pool.map(law_task, [(case, w, delta) for w in range(WORKERS)], chunksize=1)
    n = sum(r[0] for r in rows)
    mean = sum(r[1] for r in rows) / n
    se = math.sqrt(max(sum(r[2] for r in rows) / n - mean * mean, 0.0) / n)
    band = sum(r[3] for r in rows)
    p_u = float(beta.ppf(0.99, band + 1, n - band)) if band < n else 1.0
    jump = math.exp(-case.rate * case.maturity) * (case.barrier - case.strike + delta)
    law = abs(mean) + 2.5758293035489004 * se
    total = law + jump * p_u + worst
    result.update(draws_total=sum(len(r) for r in sets.values()), barrier_flips=flips_b,
                  strike_flips=flips_k, delta_fp=delta_fp, delta=delta,
                  law=dict(paths=n, mean_diff=mean, se=se, bound=law),
                  flip=dict(paths=n, band_count=band, p_upper99=p_u, bound=jump * p_u,
                            plug_in=jump * band / n),
                  arithmetic_max_unflipped=worst, total=total, allowance=1e-4,
                  passed=total <= 1e-4,
                  e_q_if_failed=None if total <= 1e-4 else max(0.0, 0.45e-3 - (total - 1e-4)))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out_dir = Path(ap.parse_args().out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    result = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT,
                                        capture_output=True, text=True).stdout.strip(), cases={})
    with mp.Pool(WORKERS) as pool:
        for case in DEV:
            result["cases"][f"B{case.na}x{case.nt}"] = validate(case, pool)
            (out_dir / "q4.json").write_text(json.dumps(result, indent=1))
            print(json.dumps(result["cases"][f"B{case.na}x{case.nt}"])[:600], flush=True)


if __name__ == "__main__":
    main()
