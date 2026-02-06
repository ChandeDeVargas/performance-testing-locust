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

### Option 1: Web UI (Interactive)

```bash
locust -f locustfile.py
```

Open: http://localhost:8089

Configure:

- Users: 10-100
- Spawn rate: 1-10 users/sec
- Duration: 60s-300s

---

### Option 2: CLI (Headless)

```bash
# 10 users, 1 user/sec spawn, 60 seconds
locust -f locustfile.py --headless -u 10 -r 1 -t 60s --html reports/report.html
```

---

### Option 3

## 📊 Viewing Reports

### After Running Tests

```bash
# Navigate to reports folder
cd reports

# Open report in browser
start report.html  # Windows
open report.html   # Mac
xdg-open report.html  # Linux
```

The HTML report will open in your default browser showing:

- ✅ Request statistics (RPS, response times, failures)
- ✅ Charts (response time percentiles, requests per second)
- ✅ Failure details (if any)

---

### Alternative: Python HTTP Server

```bash
# From project root
cd reports
python -m http.server 8000

# Then open: http://localhost:8000/report.html
```

⚠️ **Note:** Do NOT use Live Server (VSCode extension) - it won't render correctly.

## 📊 Test Scenarios

| Endpoint   | Method | Weight | Purpose            |
| ---------- | ------ | ------ | ------------------ |
| `/posts`   | GET    | 3x     | Browse all posts   |
| `/posts/1` | GET    | 2x     | View specific post |
| `/posts`   | POST   | 1x     | Create new post    |

**Weight:** Higher weight = more frequent requests (realistic behavior)

---

## 📈 Example Results

```
Type    Name            # reqs  Avg (ms)  Min   Max   RPS
GET     /posts          180     245       120   450   3.0
GET     /posts/1        120     180       90    320   2.0
POST    /posts          60      420       250   780   1.0
```

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
