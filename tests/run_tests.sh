#!/bin/bash
# Wrapper to call the Python unified runner
PYTHON_CMD="python3"

# Navigate to the root directory
cd "$(dirname "$0")/.." || exit

if [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
fi

$PYTHON_CMD tests/run_tests.py