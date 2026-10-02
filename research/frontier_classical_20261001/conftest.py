"""Stage C tests need numba (the pinned T0 environment). Where numba is missing, the test
modules are not collected and the pytest header says so, rather than failing at import:
  .context/frontier_t0_env/Scripts/python.exe -m pytest research/frontier_classical_20261001
"""

import importlib.util

NUMBA = importlib.util.find_spec("numba") is not None
collect_ignore_glob = [] if NUMBA else ["test_*.py"]


def pytest_report_header():
    if not NUMBA:
        return ("research/frontier_classical_20261001: tests skipped, numba unavailable; "
                "run them with the T0 environment (.context/frontier_t0_env)")
