#!/usr/bin/env bash
ROOT=/c/Users/prith/quantum_option_pricing
H=$ROOT/.context/health_9d734ff5; M=$ROOT/.context/health_main
V=$ROOT/venv/Scripts; T0=$ROOT/.context/frontier_t0_env/Scripts/python.exe
cd "$H"
echo "== HEAD $(git rev-parse --short HEAD) vs main $(cd $M && git rev-parse --short HEAD)"
echo "== [1] project pytest (pyproject testpaths, fast loop excludes slow)"; "$V/pytest.exe" -q -m "not slow" -p no:cacheprovider 2>&1 | tail -6; echo "rc=$?"
echo "== [2] mypy src/ app/ tests/"; "$V/python.exe" -m mypy src/ app/ tests/ 2>&1 | tail -4
echo "== [3] ruff whole repo: branch vs main"
echo "branch: $("$V/ruff.exe" check . --no-cache --statistics 2>/dev/null | awk '{s+=$1} END {print s}') errors"
echo "main:   $(cd $M && "$V/ruff.exe" check . --no-cache --statistics 2>/dev/null | awk '{s+=$1} END {print s}') errors"
echo "== [4] ruff on Python files changed in this branch"
FILES=$(git diff --name-only --diff-filter=AM origin/main...HEAD -- '*.py'); echo "$FILES" | wc -l; "$V/ruff.exe" check --no-cache $FILES 2>&1 | tail -15
echo "== [5] Stage B/C tests in T0 env"; OPENBLAS_NUM_THREADS=1 "$T0" -m pytest -q -p no:cacheprovider research/frontier_classical_20261001 research/frontier_replay_20261001 2>&1 | tail -4
echo "== [6] Stage A tests and verifier (T0 env, which has numba)"; OPENBLAS_NUM_THREADS=1 "$T0" -m pytest -q -p no:cacheprovider research/frontier_completion_20260927/test_stage_a.py 2>&1 | tail -3; "$T0" -m research.frontier_completion_20260927.verify_stage_a > /tmp/verify.out 2>&1; echo "verify rc=$?"; tail -4 /tmp/verify.out
echo "== [7] whitespace"; git diff --check origin/main...HEAD -- . ':(exclude)*.json' ':(exclude)*.jsonl' | head -10; echo "check done"
echo "== [8] mypy (anaconda mypy; project venv has none): branch vs main"
echo "branch: $(/c/Users/prith/anaconda3/python.exe -m mypy src/ app/ tests/ 2>&1 | tail -1)"; echo "main: $(cd $M && /c/Users/prith/anaconda3/python.exe -m mypy src/ app/ tests/ 2>&1 | tail -1)"; echo "check2 done"
