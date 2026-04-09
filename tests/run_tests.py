import sys
import os
import subprocess
from datetime import datetime

# Add parent directory to path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from config import SCENARIOS
except ImportError as e:
    print(f"Error importing config: {e}")
    sys.exit(1)

def run_tests():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    locust_file = os.path.join(root_dir, "locustfile.py")
    results_dir = os.path.join(root_dir, "reports")

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("========================================")
    print("  LOCUST PERFORMANCE TEST SUITE")
    print("  JSONPlaceholder API - Advanced Metrics")
    print("========================================\n")

    for scenario_name, params in SCENARIOS.items():
        users = params["users"]
        spawn_rate = params["spawn_rate"]
        duration = params["duration"]
        
        print(f"[{scenario_name.upper()} TEST] ({users} users)")
        print("========================================")
        print(f"Expected: Load test with {users} users, rate {spawn_rate}")
        print("----------------------------------------")
        
        csv_prefix = os.path.join(results_dir, f"results_{users}users_{timestamp}")
        html_report = os.path.join(results_dir, f"report_{users}users_{timestamp}.html")

        # Determine python/locust commands based on venv in root
        venv_locust = os.path.join(root_dir, "venv", "Scripts", "locust.exe") if os.name == 'nt' else os.path.join(root_dir, "venv", "bin", "locust")
        
        if os.path.exists(venv_locust):
            locust_cmd = venv_locust
        else:
            locust_cmd = "locust"

        cmd = [
            locust_cmd,
            "-f", locust_file,
            "--headless",
            "-u", str(users),
            "-r", str(spawn_rate),
            "--run-time", duration,
            "--csv", csv_prefix,
            "--html", html_report,
            "--loglevel", "INFO"
        ]
        
        try:
            subprocess.run(cmd, check=True, cwd=root_dir)
            print()
        except subprocess.CalledProcessError as e:
            print(f"[{scenario_name}] Test failed with error: {e}\n")

    print("========================================")
    print("  ALL TESTS COMPLETED")
    print("========================================")
    print(f"\nReports: {results_dir}\n")

if __name__ == "__main__":
    run_tests()
