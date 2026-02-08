@echo off
echo ========================================
echo   LOCUST PERFORMANCE TEST SUITE
echo   JSONPlaceholder API Load Testing
echo ========================================
echo.

REM Create reports directory if it doesn't exist
if not exist reports mkdir reports

REM Get current date/time for report naming
set DATETIME=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATETIME=%DATETIME: =0%

echo [1/3] Running BASELINE test (10 users)...
echo ----------------------------------------
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --stop-timeout 10 ^
  --html reports/report_10users_%DATETIME%.html ^
  --csv reports/results_10users_%DATETIME%

echo.
echo [2/3] Running MEDIUM LOAD test (50 users)...
echo ----------------------------------------
locust -f locustfile.py --headless -u 50 -r 5 -t 60s --stop-timeout 10 ^
  --html reports/report_50users_%DATETIME%.html ^
  --csv reports/results_50users_%DATETIME%

echo.
echo [3/3] Running STRESS test (100 users)...
echo ----------------------------------------
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --stop-timeout 10 ^
  --html reports/report_100users_%DATETIME%.html ^
  --csv reports/results_100users_%DATETIME%

echo.
echo ========================================
echo   TESTS COMPLETED!
echo ========================================
echo.
echo Reports generated in: reports/
echo.
echo View reports:
echo   cd reports
echo   start report_10users_%DATETIME%.html
echo   start report_50users_%DATETIME%.html
echo   start report_100users_%DATETIME%.html
echo.
pause