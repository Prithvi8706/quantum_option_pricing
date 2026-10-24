"""Stdlib helpers for the C11/U2 compile (22 Oct 2026).

Gate IR (as in research/controlled_source_completion/primitives.py and the E02 wrapper): int32 rows
(kind, a, b, c) with kind 1 X(a), 2 CX(a->b), 3 CCX(a,b->c), 4 H(a), 5 CZ(a,b), 6 Z(a).

Two depth conventions are computed here, without numpy or numba:
  * t_depth: an independent re-implementation of the repository's exact seven-T CCX ASAP schedule
    (primitives.gate_resources / native_payoff_estimator_v2._extended_depth);
  * toffoli_depth: the N1 floor's reaction convention (one reaction layer per Toffoli layer, Cliffords free;
    research/plan110_n1/headline/floor_sheet.py docstring).
"""
import ast
import hashlib
import json
import os
from array import array

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\", "/") + "/"

# Seven-T CCX expansion on (a, b, c): wire pairs per step; T/T-dagger steps marked (same table as the repo).
_CCX = ((2, 2), (1, 2), (2, 2), (0, 2), (2, 2), (1, 2), (2, 2), (0, 2), (1, 1), (2, 2), (2, 2), (0, 1), (0, 0), (1, 1), (0, 1))
_TSTEP = frozenset((2, 4, 6, 8, 9, 12, 13))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def read_npy_int32(path):
    """Minimal .npy v1/v2 reader for little-endian int32 C-order (n, 4) arrays."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:6] != b"\x93NUMPY":
        raise ValueError("not an npy file")
    major = raw[6]
    if major == 1:
        hlen = int.from_bytes(raw[8:10], "little")
        off = 10
    else:
        hlen = int.from_bytes(raw[8:12], "little")
        off = 12
    header = ast.literal_eval(raw[off:off + hlen].decode("latin1"))
    if header["descr"] != "<i4" or header["fortran_order"] or len(header["shape"]) != 2 or header["shape"][1] != 4:
        raise ValueError(f"unexpected npy header {header}")
    data = array("i")
    data.frombytes(raw[off + hlen:])
    n = header["shape"][0]
    if len(data) != 4 * n:
        raise ValueError("npy payload length mismatch")
    return [tuple(data[4 * i:4 * i + 4]) for i in range(n)]


def resources(gates, qubits, inverse=False):
    """Counts, seven-T T-depth, Clifford+T depth and Toffoli (reaction) depth of a gate list."""
    seq = gates[::-1] if inverse else gates
    lev = [0] * qubits   # T levels
    dep = [0] * qubits   # Clifford+T depth
    tof = [0] * qubits   # Toffoli layers, Cliffords free
    cnt = [0] * 7
    for kind, a, b, c in seq:
        cnt[kind] += 1
        if kind in (1, 4, 6):
            dep[a] += 1
        elif kind in (2, 5):
            t = max(lev[a], lev[b]); d = max(dep[a], dep[b]) + 1; r = max(tof[a], tof[b])
            lev[a] = lev[b] = t; dep[a] = dep[b] = d; tof[a] = tof[b] = r
        elif kind == 3:
            w = (a, b, c)
            for j in range(15):
                x, y = w[_CCX[j][0]], w[_CCX[j][1]]
                t = max(lev[x], lev[y]) + (1 if j in _TSTEP else 0)
                d = max(dep[x], dep[y]) + 1
                lev[x] = lev[y] = t; dep[x] = dep[y] = d
            r = max(tof[a], tof[b], tof[c]) + 1
            tof[a] = tof[b] = tof[c] = r
        else:
            raise ValueError("unknown gate kind")
    return dict(source_gates=len(gates), x=cnt[1], cx=cnt[2], ccx=cnt[3], h=cnt[4], cz=cnt[5], z=cnt[6],
                t_count=7 * cnt[3], clifford_cx=cnt[2] + 6 * cnt[3], clifford_h=cnt[4] + 2 * cnt[3], t_depth=max(lev, default=0), clifford_t_depth=max(dep, default=0),
                toffoli_depth=max(tof, default=0))


def run_gates(gates, state, inverse=False):
    """Classical basis-state simulation (X/CX/CCX only) on a Python int."""
    seq = gates[::-1] if inverse else gates
    for kind, a, b, c in seq:
        if kind == 1:
            state ^= 1 << a
        elif kind == 2:
            if (state >> a) & 1:
                state ^= 1 << b
        elif kind == 3:
            if (state >> a) & 1 and (state >> b) & 1:
                state ^= 1 << c
        else:
            raise ValueError("non-classical gate in basis simulation")
    return state


def write_new(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "x", encoding="utf-8") as f:  # exclusive create
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")


def progress(row):
    p = ROOT + "results/claim_debts_20261022/c11/progress.jsonl"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
