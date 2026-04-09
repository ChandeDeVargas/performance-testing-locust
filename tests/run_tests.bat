@echo off
REM Wrapper to call the Python unified runner
set "PYTHON_CMD=python"

REM Navigate to the root directory
cd /d "%~dp0\.."

if exist "venv\Scripts\python.exe" (
    set "PYTHON_CMD=venv\Scripts\python.exe"
)

%PYTHON_CMD% tests\run_tests.py
pause