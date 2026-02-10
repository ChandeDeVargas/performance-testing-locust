#!/bin/bash

echo "========================================"
echo "  LOCUST PERFORMANCE TEST SUITE"
echo "  JSONPlaceholder API - Advanced Metrics"
echo "========================================"
echo ""
echo "Features:"
echo " - SLA Assertions (response time limits)"
echo " - Custom Metrics (p95, p99 tracking)"
echo " - Event Hooks (lifecycle logging)"
echo " - Slow Request Detection"
echo ""
echo "========================================"

# Detect Virtual Environment
LOCUST_CMD="locust"
PYTHON_CMD="python3"

if [ -f "venv/bin/locust" ]; then
    LOCUST_CMD="venv/bin/locust"
    PYTHON_CMD="venv/bin/python"
    echo "[INFO] Using virtual environment found in venv/"
else
    echo "[WARNING] Virtual environment not found. Using global commands."
fi

# Create reports directory
mkdir -p reports

# Get timestamp
DATETIME=$(date +%Y%m%d_%H%M%S)

echo ""
echo "[1/3] BASELINE TEST (10 users)"
echo "========================================"
echo "Expected: Low load, all SLAs pass"
echo "----------------------------------------"
$LOCUST_CMD -f locustfile.py --headless -u 10 -r 2 -t 60s --stop-timeout 10 \
  --html "reports/report_10users_${DATETIME}.html" \
  --csv "reports/results_10users_${DATETIME}" \
  --loglevel INFO

echo ""
echo "[2/3] MEDIUM LOAD TEST (50 users)"
echo "========================================"
echo "Expected: Moderate stress, some SLA violations possible"
echo "----------------------------------------"
$LOCUST_CMD -f locustfile.py --headless -u 50 -r 5 -t 60s --stop-timeout 10 \
  --html "reports/report_50users_${DATETIME}.html" \
  --csv "reports/results_50users_${DATETIME}" \
  --loglevel INFO

echo ""
echo "[3/3] STRESS TEST (100 users)"
echo "========================================"
echo "Expected: High load, SLA violations expected"
echo "----------------------------------------"
$LOCUST_CMD -f locustfile.py --headless -u 100 -r 10 -t 60s --stop-timeout 10 \
  --html "reports/report_100users_${DATETIME}.html" \
  --csv "reports/results_100users_${DATETIME}" \
  --loglevel INFO

echo ""
echo "========================================"
echo "  ALL TESTS COMPLETED"
echo "========================================"
echo ""
echo "Reports: reports/"
echo ""
echo "View results:"
echo "  cd reports"
echo "  $PYTHON_CMD -m http.server 8000"
echo "  Open: http://localhost:8000"
echo ""