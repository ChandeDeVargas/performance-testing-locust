# Performance Testing with Locust

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Locust](https://img.shields.io/badge/Locust-00B140?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

> Advanced load testing framework with multi-endpoint coverage, SLA assertions, and interactive analytics dashboard

---

## 🎯 Project Overview

This project demonstrates **professional performance testing** using Locust to analyze API behavior under load. It includes automated test execution, SLA validation, custom metrics tracking, and visual analytics.

**API Under Test:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) - REST API for testing and prototyping

**Key Features:**

- ✅ 10 endpoint coverage (GET, POST, PUT operations)
- ✅ 3 load scenarios (10, 50, 100 concurrent users)
- ✅ SLA assertions with real-time violation tracking
- ✅ Automated analysis with visual dashboard
- ✅ Event hooks for lifecycle management
- ✅ Zero-failure stability testing

---

## 📊 Quick Results

| Metric                | 10 Users | 50 Users | 100 Users | Status       |
| --------------------- | -------- | -------- | --------- | ------------ |
| **Total Requests**    | 267      | 998      | 905       | ⚠️ Decreased |
| **Avg Response Time** | 93ms     | 267ms    | 1,122ms   | 🔴 +1,107%   |
| **RPS**               | 4.63     | 16.89    | 15.38     | 🔴 Collapsed |
| **Failures**          | 0        | 0        | 0         | ✅ Stable    |

**Critical Finding:** System degrades severely at 100 users but maintains zero failure rate (graceful degradation).

📈 [View Full Analysis](ANALYSIS.md) | 📊 [Endpoint Comparison](reports/COMPARISON.md) | 🎨 [Interactive Dashboard](reports/dashboard.html)

---

## 🗂️ Project Structure

```
performance-testing-locust/
├── locustfile.py              # Main test scenarios (10 endpoints)
├── config.py                  # SLA thresholds and configuration
├── run_tests.bat              # Automated test suite (Windows)
├── run_tests.sh               # Automated test suite (Linux/Mac)
├── analyze_results.py         # CSV analysis and comparison generator
├── generate_charts.py         # Interactive dashboard generator
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── ANALYSIS.md                # Deep-dive performance analysis
├── RESULTS.md                 # Detailed test results
├── METRICS.md                 # Custom metrics documentation
└── reports/                   # Generated test reports
    ├── dashboard.html         # Interactive visual dashboard
    ├── COMPARISON.md          # Endpoint-by-endpoint comparison
    ├── report_*_*.html        # Locust HTML reports (timestamped)
    └── results_*_*.csv        # Raw test data (timestamped)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/ChandeDeVargas/performance-testing-locust.git
cd performance-testing-locust

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running Tests

### Option 1: Automated Test Suite (Recommended)

Run all 3 load scenarios with a single command:

```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

**What it does:**

- ✅ Auto-detects virtual environment (no manual activation needed)
- ✅ Executes 3 scenarios: 10, 50, 100 concurrent users
- ✅ Generates timestamped HTML and CSV reports
- ✅ Validates SLA compliance in real-time
- ✅ Logs slow requests and violations

**Duration:** ~3-4 minutes total (60s per scenario + processing)

---

### Option 2: Manual Execution

#### Baseline Test (10 users - Normal Load)

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --stop-timeout 10 \
  --html reports/baseline.html --csv reports/baseline
```

#### Medium Load Test (50 users - Moderate Stress)

```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 60s --stop-timeout 10 \
  --html reports/medium.html --csv reports/medium
```

#### Stress Test (100 users - High Load)

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --stop-timeout 10 \
  --html reports/stress.html --csv reports/stress
```

---

### Option 3: Interactive Web UI

For real-time monitoring and manual control:

```bash
locust -f locustfile.py
```

Then open: **http://localhost:8089**

Configure users, spawn rate, and duration in the browser interface.

---

## 📈 Analysis & Visualization

### Generate Reports

After running tests, generate comprehensive analysis:

```bash
# 1. Generate endpoint comparison (Markdown report)
python analyze_results.py

# 2. Generate interactive visual dashboard (HTML charts)
python generate_charts.py
```

### View Results

**Interactive Dashboard:**

```bash
cd reports
python -m http.server 8000
```

Open in browser: **http://localhost:8000/dashboard.html**

**Features:**

- 📊 Bar chart: Response time by load level
- 📈 Line chart: Performance degradation trends
- 📋 Summary statistics cards
- 🎨 Beautiful gradient design

**Static Reports:**

- `reports/COMPARISON.md` - Detailed endpoint comparison
- `ANALYSIS.md` - Comprehensive performance analysis
- `RESULTS.md` - Test results with insights
- `METRICS.md` - Custom metrics documentation

---

## 🎯 Test Coverage

### Endpoints Tested (10 Total)

**Posts Resource:**

- `GET /posts` - Browse all posts (SLA: <500ms)
- `GET /posts/1` - View single post (SLA: <300ms)
- `GET /posts?userId=1` - Filtered posts (SLA: <600ms)
- `POST /posts` - Create new post (SLA: <1000ms)
- `PUT /posts/1` - Update post (SLA: <800ms)

**Users Resource:**

- `GET /users` - Browse all users (SLA: <500ms)
- `GET /users/1` - View single user (SLA: <300ms)

**Other Resources:**

- `GET /comments` - Browse comments (SLA: <400ms)
- `GET /albums` - Browse albums (SLA: <500ms)

### Load Scenarios

| Scenario     | Users | Spawn Rate | Duration | Purpose                  |
| ------------ | ----- | ---------- | -------- | ------------------------ |
| **Baseline** | 10    | 2/sec      | 60s      | Normal user behavior     |
| **Medium**   | 50    | 5/sec      | 60s      | Moderate traffic spike   |
| **Stress**   | 100   | 10/sec     | 60s      | Peak load / Black Friday |

---

## 🔬 Advanced Features

### 1. SLA Assertions ✅

Every request is validated against response time limits defined in `config.py`:

```python
SLA_THRESHOLDS = {
    "GET": {
        "/posts": 500,      # Max 500ms
        "/posts/1": 300,    # Max 300ms
        # ... more endpoints
    }
}
```

**Real-time Validation:**

- SLA violations logged immediately
- Total violations reported at test end
- Enables performance regression detection

---

### 2. Custom Metrics 📊

**Tracked Automatically:**

- ⚠️ Slow requests (>2 seconds)
- 🔴 SLA violations per endpoint
- 📈 Response time percentiles (p50, p95, p99)
- 🎯 Request distribution by endpoint

**Event Hooks:**

```python
on_test_start()  → Initialize logging, display config
on_request()     → Validate SLA, track slow requests
on_test_stop()   → Summary statistics, top 5 slowest
```

---

### 3. Multi-Layer Validation ✅

Each request goes through:

1. **Status Code Check** - Expected vs actual (200, 201, etc.)
2. **Response Structure** - Required fields present
3. **Response Content** - Non-empty, valid JSON
4. **SLA Compliance** - Response time within limits

---

### 4. Automated Analysis 🤖

**CSV Parser (`analyze_results.py`):**

- Finds latest test results automatically
- Parses all endpoint statistics
- Calculates performance degradation
- Generates comparison tables

**Chart Generator (`generate_charts.py`):**

- Creates interactive Chart.js visualizations
- Bar charts for response time comparison
- Line charts for degradation trends
- Summary statistics cards

---

## 📚 Documentation

### Analysis Documents

| File                                           | Description                                                                |
| ---------------------------------------------- | -------------------------------------------------------------------------- |
| [ANALYSIS.md](ANALYSIS.md)                     | Deep-dive performance analysis, bottleneck identification, recommendations |
| [RESULTS.md](RESULTS.md)                       | Detailed test results with metrics tables                                  |
| [METRICS.md](METRICS.md)                       | Custom metrics implementation and SLA definitions                          |
| [reports/COMPARISON.md](reports/COMPARISON.md) | Auto-generated endpoint comparison                                         |

### Key Findings

**Performance Degradation:**

- Worst endpoint: `GET /users/1` (+1,796% at 100 users)
- Best endpoint: `GET /users` (+515% at 100 users)
- Average degradation: +1,107% across all endpoints

**Bottleneck Analysis:**

- 🔴 Database connection pool exhaustion
- 🔴 Single-threaded request processing
- 🔴 No HTTP keep-alive / connection pooling
- 🔴 Lack of caching layer

**Recommendations:**

1. Set production limit: 50 concurrent users max
2. Implement Redis caching layer
3. Increase database connection pool
4. Enable async request processing

See [ANALYSIS.md](ANALYSIS.md) for full details.

---

## 🛠️ Configuration

### SLA Thresholds (`config.py`)

Customize response time limits per endpoint:

```python
SLA_THRESHOLDS = {
    "GET": {
        "/posts": 500,      # Milliseconds
        "/users": 500,
        # ... customize as needed
    }
}
```

### Feature Flags

Enable/disable features:

```python
ENABLE_ASSERTIONS = True        # Fail tests on SLA violations
ENABLE_DETAILED_LOGGING = True  # Log each request details
ENABLE_PERCENTILE_TRACKING = True
```

---

## 🎓 What This Project Demonstrates

### Performance Testing Skills:

- ✅ Load test design with realistic user behavior
- ✅ Metrics analysis (RPS, response times, percentiles)
- ✅ Bottleneck identification and root cause analysis
- ✅ SLA definition and compliance tracking
- ✅ Report generation and data visualization

### Technical Skills:

- ✅ Locust framework (Python)
- ✅ HTTP/REST API testing
- ✅ CLI automation (headless mode)
- ✅ Event-driven architecture (hooks)
- ✅ Data parsing and analysis (CSV)
- ✅ Interactive visualizations (Chart.js)
- ✅ Shell scripting (Bash, Batch)
- ✅ Git version control

### Professional Practices:

- ✅ Modular code organization
- ✅ Configuration management
- ✅ Automated testing pipelines
- ✅ Comprehensive documentation
- ✅ Reproducible results

---

## 🔍 Viewing Reports

### HTML Reports (Locust Native)

```bash
# From reports directory
cd reports
python -m http.server 8000
```

Open: `http://localhost:8000/report_10users_YYYYMMDD_HHMMSS.html`

**Tabs:**

- **Statistics:** Request counts, failures, response times, RPS
- **Charts:** Response time percentiles, RPS over time
- **Failures:** Error details (if any)
- **Exceptions:** Stack traces (if any)

### Dashboard (Custom Visualizations)

```bash
cd reports
python -m http.server 8000
```

Open: `http://localhost:8000/dashboard.html`

**Features:**

- Interactive bar charts (response time by load)
- Performance trend lines
- Summary statistics cards
- Responsive design

⚠️ **Note:** Do NOT use Live Server (VSCode extension) - use Python HTTP server for correct rendering.

---

## 📦 Dependencies

```txt
locust==2.32.4
```

**Additional Requirements:**

- Python 3.8+
- Modern web browser (for dashboard viewing)

---

## 🚦 CI/CD Integration (Future)

Example GitHub Actions workflow:

```yaml
name: Performance Tests

on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run performance tests
        run: |
          ./run_tests.sh
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: performance-reports
          path: reports/
```

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project as a template for your own performance testing needs.

---

## 👤 Author

**Chande De Vargas**

- GitHub: [@ChandeDeVargas](https://github.com/ChandeDeVargas)
- LinkedIn: [Chande De Vargas](https://www.linkedin.com/in/chande-de-vargas-b8a51838a/)
- Portfolio: Performance Testing Specialist

---

## 📚 Resources & References

- [Locust Documentation](https://docs.locust.io/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
- [Performance Testing Best Practices](https://martinfowler.com/articles/practical-test-pyramid.html)
- [HTTP Load Testing](https://www.w3.org/Protocols/rfc2616/rfc2616.html)

---

## 🙏 Acknowledgments

- Locust.io team for the excellent load testing framework
- JSONPlaceholder for providing a reliable test API
- Chart.js for beautiful visualizations

---

**⭐ If you found this project helpful, please consider giving it a star!**
