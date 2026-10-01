import numpy as np
import pytest

from research.frontier_classical_20261001.basis import canonical_factor, rotated_factor


def covariance(na, nt, sigma, rho, maturity):
    t = maturity * np.arange(1, nt + 1) / nt
    asset = sigma**2 * (rho * np.ones((na, na)) + (1 - rho) * np.eye(na))
    return np.kron(asset, np.minimum.outer(t, t))


@pytest.mark.parametrize("na,nt", [(4, 12), (8, 52), (16, 52), (16, 12)])
def test_factor_reproduces_covariance_with_positive_first_column(na, nt):
    L, groups = canonical_factor(na, nt, 0.3, 0.4, 1.0)
    cov = covariance(na, nt, 0.3, 0.4, 1.0)
    assert np.abs(L @ L.T - cov).max() <= 1e-12 * np.abs(cov).max()
    assert (L[:, 0] > 0).all()
    assert np.all(np.diff(np.linalg.norm(L, axis=0) ** 2) <= 1e-15)
    assert len(groups) == nt and all(len(g) == na - 1 for g in groups)


def test_factor_is_bit_identical_across_calls():
    a, _ = canonical_factor(8, 52, 0.3, 0.4, 1.0)
    b, _ = canonical_factor(8, 52, 0.3, 0.4, 1.0)
    assert np.array_equal(a, b)


def test_rotation_preserves_covariance_and_first_column():
    L, groups = canonical_factor(8, 52, 0.3, 0.4, 1.0)
    R = rotated_factor(L, groups, [2026100101, 1, 1])
    assert np.abs(R @ R.T - L @ L.T).max() <= 1e-12 * np.abs(L @ L.T).max()
    assert np.array_equal(R[:, 0], L[:, 0])
    assert not np.allclose(R, L)


def test_canonical_order_and_helmert_are_pinned():
    import scipy.linalg

    from research.frontier_classical_20261001.basis import asset_basis
    L, groups = canonical_factor(4, 12, 0.3, 0.4, 1.0)
    vecs, _ = asset_basis(4, 0.3, 0.4)
    assert np.array_equal(vecs[:, 1:].T, scipy.linalg.helmert(4, full=False))
    assert groups[:2] == [[1, 2, 3], [6, 7, 8]]
    # (asset mode, time mode) of the first columns, eigenvalue descending (spec section 0.1)
    expected = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (1, 1), (2, 1), (3, 1), (0, 3)]
    tv = np.sin(np.outer(np.arange(1, 13), 2 * np.arange(1, 13) - 1) * np.pi / 25)
    tv /= np.linalg.norm(tv, axis=0)
    for col, (a, m) in enumerate(expected):
        direction = np.kron(vecs[:, a], tv[:, m])
        assert abs(abs(L[:, col] @ direction) - np.linalg.norm(L[:, col])) < 1e-12, col


def test_factor_does_not_depend_on_blas_threads():
    import os
    import subprocess
    import sys
    code = "; ".join([
        "import hashlib",
        "from research.frontier_classical_20261001.basis import canonical_factor",
        "L = canonical_factor(8, 52, .3, .4, 1.)[0]",
        "print(hashlib.sha256(L.tobytes()).hexdigest())",
    ])
    hashes = set()
    for threads in ("1", "22"):
        env = dict(os.environ, OPENBLAS_NUM_THREADS=threads, MKL_NUM_THREADS=threads,
                   OMP_NUM_THREADS=threads)
        hashes.add(subprocess.run([sys.executable, "-c", code], env=env, capture_output=True,
                                  text=True, check=True).stdout.strip())
    assert len(hashes) == 1


def test_canonical_factor_hashes_are_pinned():
    import hashlib
    expected = {(4, 12): "4bfc6ae908e20ca1eac43933209176574479e4ba6e9b28a6785bb3db1a233a39",
                (8, 52): "57a0d32056dd6a278eeac16969baaed8cff3b3562385ab39ed4f15ecd28606f6"}
    for (na, nt), digest in expected.items():
        L, _ = canonical_factor(na, nt, 0.3, 0.4, 1.0)
        assert hashlib.sha256(L.tobytes()).hexdigest() == digest
