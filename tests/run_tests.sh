#!/bin/bash

echo "========================================"
echo "  LOCUST PERFORMANCE TEST SUITE"
echo "  JSONPlaceholder API Load Testing"
echo "========================================"
echo ""

# Create reports directory if it doesn't exist
mkdir -p reports

# Get current timestamp for report naming
DATETIME=$(date +%Y%m%d_%H%M%S)

echo "[1/3] Running BASELINE test (10 users)..."
echo "----------------------------------------"
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --stop-timeout 10 \
  --html "reports/report_10users_${DATETIME}.html" \
  --csv "reports/results_10users_${DATETIME}"

echo ""
echo "[2/3] Running MEDIUM LOAD test (50 users)..."
echo "----------------------------------------"
locust -f locustfile.py --headless -u 50 -r 5 -t 60s --stop-timeout 10 \
  --html "reports/report_50users_${DATETIME}.html" \
  --csv "reports/results_50users_${DATETIME}"

echo ""
echo "[3/3] Running STRESS test (100 users)..."
echo "----------------------------------------"
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --stop-timeout 10 \
  --html "reports/report_100users_${DATETIME}.html" \
  --csv "reports/results_100users_${DATETIME}"

echo ""
echo "========================================"
echo "  TESTS COMPLETED!"
echo "========================================"
echo ""
echo "Reports generated in: reports/"
echo ""
echo "View reports:"
echo "  cd reports"
echo "  open report_10users_${DATETIME}.html"
echo "  open report_50users_${DATETIME}.html"
echo "  open report_100users_${DATETIME}.html"
echo ""