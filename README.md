# Performance Testing with Locust

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Locust](https://img.shields.io/badge/Locust-00B140?style=for-the-badge)

> Load testing for JSONPlaceholder API to identify performance bottlenecks

---

## 🎯 Project Purpose

This project demonstrates **performance testing** using Locust to:

- Simulate realistic user load on APIs
- Identify performance bottlenecks
- Measure response times under stress
- Detect breaking points

**API Under Test:** [JSONPlaceholder](https://jsonplaceholder.typicode.com)

---

## 🗂️ Project Structure

```
performance-testing-locust/
├── locustfile.py          # Load test scenarios
├── reports/               # HTML test reports
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone repo
git clone https://github.com/your-username/performance-testing-locust.git
cd performance-testing-locust

# Create venv
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running Tests

### Quick Start (Automated)

Run all test scenarios with a single command:

```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

This executes:

- ✅ Baseline (10 users, 60s)
- ✅ Medium Load (50 users, 60s)
- ✅ Stress Test (100 users, 60s)

Reports generated in `reports/` folder.

---

### Manual Execution

#### Baseline Test (10 users)

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html reports/baseline.html
```

#### Medium Load (50 users)

```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 60s --html reports/medium.html
```

#### Stress Test (100 users)

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --html reports/stress.html
```

---

### Interactive Web UI

```bash
locust -f locustfile.py
```

Open: http://localhost:8089

### Alternative: Python HTTP Server

```bash
# From project root
cd reports
python -m http.server 8000

# Then open: http://localhost:8000/report.html
```

⚠️ **Note:** Do NOT use Live Server (VSCode extension) - it won't render correctly.

## 📊 Test Scenarios (Updated)

| Endpoint             | Method | Weight | Purpose          | Expected Time |
| -------------------- | ------ | ------ | ---------------- | ------------- |
| `/posts`             | GET    | 3x     | Browse all posts | < 500ms       |
| `/posts/1`           | GET    | 2x     | View single post | < 300ms       |
| `/comments?postId=1` | GET    | 2x     | Read comments    | < 400ms       |
| `/posts`             | POST   | 1x     | Create new post  | < 1000ms      |
| `/posts/1`           | PUT    | 1x     | Update post      | < 800ms       |

**Weight:** Higher weight = more frequent requests (realistic user behavior)

---

## 📈 Load Test Scenarios

| Scenario     | Users | Spawn Rate | Duration | Purpose         |
| ------------ | ----- | ---------- | -------- | --------------- |
| **Baseline** | 10    | 2/sec      | 60s      | Normal load     |
| **Medium**   | 50    | 5/sec      | 60s      | Moderate stress |
| **Stress**   | 100   | 10/sec     | 60s      | High load       |

See [RESULTS.md](RESULTS.md) for detailed performance analysis.

## 📈 Load Test Scenarios

| Scenario     | Users | Spawn Rate | Duration | Purpose         |
| ------------ | ----- | ---------- | -------- | --------------- |
| **Baseline** | 10    | 2/sec      | 60s      | Normal load     |
| **Medium**   | 50    | 5/sec      | 60s      | Moderate stress |
| **Stress**   | 100   | 10/sec     | 60s      | High load       |

See [RESULTS.md](RESULTS.md) for detailed performance analysis.

---

**Key Metrics:**

- **RPS (Requests/sec):** Total throughput
- **Avg Response Time:** Average latency
- **Min/Max:** Best/worst case scenarios
- **Percentiles (p50, p95, p99):** Performance distribution

---

## 🎓 What This Project Demonstrates

### Performance Testing Skills:

- ✅ Load test design (realistic user behavior)
- ✅ Metrics analysis (RPS, response times, percentiles)
- ✅ Bottleneck identification
- ✅ Report generation

### Technical Skills:

- ✅ Locust framework (Python)
- ✅ HTTP testing
- ✅ CLI usage (headless mode)
- ✅ Web UI (interactive testing)

---

## 📚 Resources

- [Locust Documentation](https://docs.locust.io/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)

---

👤 Chande De Vargas
GitHub: https://github.com/ChandeDeVargas
LinkedIn: https://www.linkedin.com/in/chande-de-vargas-b8a51838a/

---

## 📄 License

MIT License

```

---
```
