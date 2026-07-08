# POS System - End-to-End Test Automation Framework

Automated E2E testing framework for [Odoo POS](https://github.com/odoo/odoo) (Point of Sale) system, featuring self-healing locators, CI/CD integration, and graphical reporting dashboards.

## Architecture

```
┌────────────────────────────────────────────────────────  ─┐
│                    Test Layer (Tests)                     │
│  ┌────────────── ┐ ┌──────────┐ ┌────────────────── ─┐    │
│  │  Functional   │ │ Negative │ │   Performance      │    │
│  │    Tests      │ │  Tests   │ │  Tests (skipped)   │    │
│  └──────┬─────── ┘ └────┬─────┘ └─────────┬───────── ┘    │
├─────────┼────────── ────┼──────── ────────┼───────────────┤
│         │   Keywords Layer (Shared Business Ops)          │
│  ┌──────┴──────┐ ┌────┴───── ┐ ┌────┴────┐ ┌───────┐      │
│  │ AuthKeywords│ │PosKeywords│ │ProdKwyrd│ │Payment│      │
│  └──────┬──────┘ └─── ─┬─────┘ └────┬────┘ └───┬───┘      │
├─────────┼──────────────┼────────────┼──────────┼───────  ─┤
│         │      Page Object Model (POM)                    │
│  ┌──────┴──────┐ ┌── ──┴─────┐ ┌────┴────┐ ┌────┴───┐     │
│  │  LoginPage  │ │  POSPage  │ │ ProdPage│ │ CustPg │     │
│  └──────┬──────┘ └── ──┬─────┘ └────┬────┘ └────┬───┘     │
├─────────┼──────────────┼────────────┼──────────┼──────  ──┤
│         │         Core Framework                          │
│  ┌──────┴────────────────────────────────────────  ──┐    │
│  │    Self-Healing Layer (LocatorManager + Retry)    │    │
│  ├───────────────────────────────────────────────── ─┤    │
│  │         Browser Manager (Playwright)              │    │
│  ├───────────────────────────────────────────── ─────┤    │
│  │              Config + Fixtures                    │    │
│  └──────────────────────────────────────────────── ──┘    │
├──────────────────────────────────────────────────────  ───┤
│     Docker (Odoo 17.0 + PostgreSQL 16)                    │
│     CI/CD (GitHub Actions + Allure Report)                │
└───────────────────────────────────────────────────────  ──┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Test Runner** | Pytest | Test execution, fixtures, parallelization |
| **Browser Automation** | Playwright | Fast, reliable browser control with auto-waiting |
| **Self-Healing** | Custom LocatorManager | Multi-strategy locator fallback chain |
| **Reporting** | Allure Framework | Interactive HTML dashboard with graphs |
| **Load Testing** | k6 (Grafana) | High-performance API load testing (currently skipped) |
| **CI/CD** | GitHub Actions | Automated pipeline with matrix builds |
| **Containerization** | Docker + Docker Compose | Isolated Odoo + PostgreSQL environment |
| **Data Generation** | Faker + Custom | Randomized test data creation |

## Project Structure

```
pos-test-e2e/
├── docker/
│   ├── docker-compose.yml        # Local dev environment
│   ├── docker-compose.ci.yml     # CI-optimized environment
│   └── entrypoint.sh             # Odoo init with POS module
├── src/
│   ├── core/
│   │   ├── config.py             # Centralized configuration
│   │   ├── browser_manager.py    # Playwright lifecycle management
│   │   ├── fixtures.py           # Shared pytest fixtures
│   │   └── self_healing/
│   │       ├── locator_manager.py # Multi-strategy locator resolution
│   │       └── retry_handler.py  # Exponential backoff retry logic
│   ├── pages/
│   │   ├── base_page.py          # Base page with self-healing helpers
│   │   ├── pos/
│   │   │   ├── login_page.py
│   │   │   ├── dashboard_page.py
│   │   │   ├── pos_interface_page.py
│   │   │   ├── products_page.py
│   │   │   ├── orders_page.py
│   │   │   └── customers_page.py
│   │   └── shared/
│   │       ├── navbar_component.py
│   │       └── modal_component.py
│   ├── keywords/
│   │   ├── auth_keywords.py      # Login, logout, session management
│   │   ├── pos_keywords.py       # POS sale workflows
│   │   ├── product_keywords.py   # Product CRUD operations
│   │   ├── payment_keywords.py   # Payment processing
│   │   └── customer_keywords.py  # Customer management
│   ├── tests/
│   │   ├── conftest.py           # Fixture wiring
│   │   ├── functional/           # Functional test cases
│   │   │   ├── test_auth.py
│   │   │   ├── test_pos_full_workflow.py
│   │   │   └── test_product_management.py
│   │   ├── negative/             # Negative test cases
│   │   │   ├── test_invalid_login.py
│   │   │   ├── test_payment_failures.py
│   │   │   └── test_data_validation.py
│   │   └── performance/          # Performance test cases (skipped)
│   │       ├── test_pos_load.py
│   │       └── k6/
│   │           └── pos_browse_test.js
│   └── utils/
│       └── data_generator.py     # Test data generation
├── .github/workflows/
│   └── test.yml                  # GitHub Actions pipeline
├── reports/                      # Test output directory
├── screenshots/                  # Failure screenshots
├── Makefile                      # Command shortcuts
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
└── README.md
```

## Quick Start (Beginner Guide)

This guide walks you through setting up and running the POS test framework from scratch. No prior knowledge of Odoo, Docker, or Playwright is required — follow each step in order.

---

### Prerequisites

You need these tools installed on your machine before starting:

| Tool | Version | Purpose | Installation Guide |
|------|---------|---------|-------------------|
| **Docker Desktop** | Latest | Runs Odoo and PostgreSQL in isolated containers | [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| **Python** | 3.11+ | Runs the test framework | [Download Python](https://www.python.org/downloads/) |
| **Node.js** | 18+ | Required for k6 performance tests (optional; currently not needed) | [Download Node.js](https://nodejs.org/) |
| **Git** | Latest | Clone the repository | [Download Git](https://git-scm.com/downloads) |

> **Windows users**: Run all commands in PowerShell or Git Bash. Replace `python3` with `python` and use `.venv\Scripts\activate` to activate the virtual environment.

---

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone <repo-url> pos-test-e2e
cd pos-test-e2e
```

This downloads the project and moves you into the project folder.

---

### Step 2: Set Up Python Virtual Environment

A virtual environment isolates the project's Python dependencies so they don't conflict with other projects.

```bash
# Create a virtual environment named '.venv' inside the project folder
python3 -m venv .venv

# Activate it (your terminal prompt should change to show '(.venv)')
source .venv/bin/activate
```

> **Windows**: Use `.venv\Scripts\activate`
>
> **macOS/Linux**: Use `source .venv/bin/activate`

Verify it worked:
```bash
which python3
# Should show a path INSIDE your project folder, like:
# /Users/you/pos-test-e2e/.venv/bin/python3
```

---

### Step 3: Install Python Dependencies

```bash
# Option A: Using the Makefile (recommended)
make setup

# Option B: Manual install (if make is not available)
pip install -r requirements.txt
playwright install chromium
```

This installs:
- **pytest** and plugins (test runner, timeout, parallel execution, HTML reports)
- **playwright** (browser automation — controls Chrome/Firefox/Safari)
- **allure-pytest** (generates beautiful HTML test reports)
- **faker** (generates random test data like names, emails, barcodes)
- **k6** Python wrapper (for load testing; currently skipped)

The `playwright install chromium` command downloads the Chromium browser binary (headless) that Playwright uses to run tests. This is **not** your regular Chrome browser — it's a dedicated browser for testing.

---

### Step 4: Start Odoo 17 with Docker

Odoo is the POS system we're testing. Docker lets us run it without installing it directly on your machine.

```bash
# Start Odoo + PostgreSQL database + Adminer (database admin UI)
make docker-up
```

**What happens behind the scenes:**
1. Docker downloads the `odoo:17.0` and `postgres:16-alpine` images (first run only — takes 2-5 min)
2. PostgreSQL starts and waits to accept connections
3. Odoo's entrypoint script (`docker/entrypoint.sh`) runs:
   - Creates a database named `pos_test`
   - Installs the `point_of_sale` module with demo data
   - Starts the Odoo web server on port 8069
4. Adminer (database admin tool) starts on port 8080

**Verify Odoo is running:**

```bash
# Wait for Odoo to finish initializing (takes 30-60 seconds)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8069/web/login

# If this returns '200', Odoo is ready!
```

If you get `000` or nothing, wait 10 more seconds and try again:
```bash
# Check Odoo logs to see what's happening
docker compose -f docker/docker-compose.yml logs --tail=20 odoo
```

**What to expect in the logs:**
- Near the end, you should see lines like:
  ```
  pos-odoo  | Modules loaded.
  pos-odoo  | Starting Odoo HTTP service...
  ```
- If you see errors about database not existing, the entrypoint script is still creating it — just wait.

**Access the Odoo web interface:**
- Open your browser to **http://localhost:8069**
- You should see the Odoo login page
- Login with:
  - **Username**: `admin`
  - **Password**: `admin`

> **Note**: The first Docker startup creates a fresh database with POS demo data. This data includes products like "Corner Desk Left Sit", "Large Desk", etc., and a POS configuration named "Shop".

---

### Step 5: Understand the Odoo 17 POS Flow

Odoo 17 changed how POS sessions work compared to earlier versions. The key flow is:

1. **Login** to Odoo with admin credentials
2. The dashboard loads (defaults to the Discuss app)
3. Click the **apps menu** (grid icon in top-left corner)
4. Click **Point of Sale** — this takes you to the POS **Configuration** backend page
5. Click **Open Session** or **New Session** on the "Shop" card
6. The **POS Interface** loads at `http://localhost:8069/pos/ui?config_id=1`
7. If **Opening Control** is enabled, a popup asks for opening cash — enter `100` and click **Open session**
8. You're now in the POS and can add products, take payments, etc.

The test framework automates all of this, but you should understand the flow to debug issues.

---

### Step 6: Run the Tests

Now that Odoo is running, you can execute the test suite.

#### Run a Quick Smoke Test (recommended first step)

```bash
make test-smoke
```

This runs a small set of fast tests (~10 seconds) to verify everything is set up correctly:
- Login page loads
- Admin can log in
- Logout works

#### Run the Full Test Suite

```bash
make test
```

This runs all available tests. Depending on the number of tests, this can take 2-10 minutes.

#### Run Specific Test Categories

```bash
# Authentication tests (login, logout, page elements) — ~5 seconds
python3 -m pytest src/tests/functional/test_auth.py -v --timeout=20

# POS workflow tests (add products, payments, receipts) — ~30 seconds
python3 -m pytest src/tests/functional/test_receipt_verification.py src/tests/functional/test_multi_payment.py -v --timeout=30

# All new BrowserStack-guide tests — ~2 minutes
python3 -m pytest src/tests/functional/test_receipt_verification.py src/tests/functional/test_multi_payment.py src/tests/functional/test_stock_alerts.py src/tests/network/test_offline_resilience.py src/tests/compatibility/test_multi_currency.py -v --timeout=30

# Usability tests — ~7 seconds
python3 -m pytest src/tests/usability/ -v --timeout=20

# All passing tests — ~2.5 minutes
python3 -m pytest src/tests/functional/test_auth.py src/tests/functional/test_receipt_verification.py src/tests/functional/test_multi_payment.py src/tests/functional/test_stock_alerts.py src/tests/network/test_offline_resilience.py src/tests/compatibility/test_multi_currency.py src/tests/usability/ -v --timeout=30
```

#### Run a Single Test

```bash
python3 -m pytest "src/tests/functional/test_auth.py::TestAuthentication::test_admin_login_success" -v --timeout=20 --no-header
```

#### Understanding Test Output

Each test line shows:
```
PASSED/FAILED [percentage]
```

At the end, you'll see a summary:
```
======= 30 passed, 1 failed in 138.82s (0:02:18) =======
```

If a test fails, look for the **AssertionError** message — it tells you exactly what condition wasn't met. The framework also captures:
- A screenshot (`screenshots/FAILED_<test_name>.png`)
- A Playwright trace (`reports/traces/<test_name>.zip`)

---

### Step 7: View the Allure Report

The framework generates an interactive HTML dashboard with test results, graphs, and failure details.

```bash
# Generate the report from test results
make allure-report

# Serve it locally (opens a web server)
make allure-serve

# Open in your browser:
open http://localhost:8081   # macOS
# OR manually navigate to http://localhost:8081
```

**What the Allure dashboard shows:**
- **Overview**: Pass/fail counts, duration, severity breakdown
- **Categories**: Tests grouped by feature, story, severity
- **Timeline**: When each test ran and how long it took
- **Graphs**: Pie charts for pass/fail, bar charts for duration
- **Behaviors**: Feature → Story → Test hierarchy
- **Defects**: Failed/flaky tests with full logs and screenshots

> If `make allure-serve` fails, ensure Allure CLI is installed:
> ```bash
> brew install allure   # macOS
> npm install -g allure-commandline   # Any OS with Node.js
> ```

---

### Step 8: Stop the Docker Environment

When you're done testing, stop the Odoo containers:

```bash
make docker-down
```

This stops all containers but **preserves the database** in a Docker volume. Next time you run `make docker-up`, your test data and POS sessions will still be there.

To **completely reset** (fresh database with demo data):

```bash
# Stop and remove containers AND volumes (deletes all data)
docker compose -f docker/docker-compose.yml down -v

# Start fresh
make docker-up
```

---

## Test Categories (BrowserStack Guide Coverage)

Based on the BrowserStack POS testing guide, the framework covers these categories:

| Category | Test File | Tests | Status |
|----------|-----------|-------|--------|
| **Barcode Scanning** | `test_barcode_scanning.py` | 5 | ⏸️ Skipped (timeout) |
| **Receipt Verification** | `test_receipt_verification.py` | 5 | ✅ Passing |
| **Multi-Payment** | `test_multi_payment.py` | 5 | ✅ Passing |
| **Stock Alerts** | `test_stock_alerts.py` | 2 | ✅ Passing |
| **Offline Resilience** | `test_offline_resilience.py` | 2 | ✅ Passing |
| **Multi-Currency** | `test_multi_currency.py` | 2 | ✅ Passing |
| **Usability** | `test_ui_consistency.py`, `test_accessibility.py` | 10 | ✅ Passing |
| **Auth/Security** | `test_auth.py` | 5 | ✅ 4/5 Passing |

All markers are registered in `pytest.ini`:
```
barcode, payment_methods, receipt, stock_alerts, offline, multi_currency
```

Run tests by marker:
```bash
python3 -m pytest -m "receipt" -v --timeout=30
python3 -m pytest -m "payment_methods" -v --timeout=30
python3 -m pytest -m "offline or stock_alerts or multi_currency" -v --timeout=30
```

## Self-Healing Framework

The framework implements a multi-layered self-healing strategy to handle dynamic web elements and flaky tests.

### Locator Strategy Chain

When locating elements, the framework tries strategies in priority order:

```python
# For a data-testid="login-button", the resolution chain is:
1. [data-testid="login-button"]       # Priority 10 - Best practice
2. [data-oe-id="login-button"]        # Priority 20 - Odoo attribute
3. #login-button                       # Priority 30 - ID fallback
4. [name="login-button"]               # Priority 40 - Name fallback
5. .login-button                       # Priority 50 - CSS class
6. //*[@*[contains(., "login-button")]] # Priority 100 - XPath fallback
```

### Locator Types Available

```python
# In any Page Object or test:
page.get_by_testid("element-id")       # Best for test-specific attributes
page.get_by_role("button", "Submit")   # ARIA role-based
page.get_by_text("Add Product")        # Text content
page.get_by_placeholder("Search...")   # Placeholder text
page.get_by_label("Email")             # Label association
page.get_by_css(".product-list")       # CSS selector
page.get_by_xpath("//div[@class='x']") # XPath (last resort)
```

### Retry Mechanism

Failed operations automatically retry with exponential backoff:
- Attempt 1: immediate
- Attempt 2: after 1s
- Attempt 3: after 2s
- Attempt 4: after 4s
- Max attempts: 3 (configurable via `RETRY_MAX_ATTEMPTS`)

```python
from src.core.self_healing import retry_on_failure

@retry_on_failure(max_attempts=5, base_delay=0.5)
def click_critical_element(self):
    self.page.locator("#critical-btn").click()
```

### Failure Recovery

On test failure, the framework automatically captures:
- Full-page screenshot (`screenshots/FAILED_<test_name>.png`)
- Playwright trace (`reports/traces/<test_name>.zip`)
- Browser console logs
- Video recording (optional, via `VIDEO_ON_FAILURE=true`)

These artifacts are attached to the Allure report for debugging.

## Test Coverage

### Functional Tests (35+ scenarios)

| Category | Scenarios |
|----------|-----------|
| **Authentication** | Admin login, demo user login, logout, login page elements, database selection |
| **POS Workflow** | Single product sale, multi-product sale, bank/card payment, customer assignment, discount application, multiple sequential orders, refund processing, custom quantity, product search |
| **Product Management** | Create product, edit product, delete product, bulk creation, search, barcode assignment |
| **Customer Management** | Create customer, edit customer, delete customer, multi-customer creation |

### Negative Tests (15+ scenarios)

| Category | Scenarios |
|----------|-----------|
| **Invalid Login** | Empty credentials, empty password, non-existent user, wrong password, SQL injection, XSS injection, special characters |
| **Payment Failures** | Cancel payment, zero quantity, empty order payment, invalid split payment, refund on empty order |
| **Data Validation** | Empty product name, negative price, extremely long name, zero price, invalid email, empty customer name, delete non-existent product |

### Performance Tests (6+ scenarios — currently skipped)

| Test | Measurement |
|------|-------------|
| Login page load | LCP, CLS, FID, Page Load Time |
| POS module load | LCP, Page Load Time |
| Order processing | End-to-end order time |
| Throughput | 5 orders avg/max/min time |
| Product search | Search response time |
| Concurrent operations | Add product, discount, customer, quantity, payment timing |
| k6 load test | Ramp up to 50 concurrent users |

## CI/CD Pipeline

### GitHub Actions Workflow

The pipeline (`test.yml`) runs on:
- Push to `main`, `develop`, `feature/*`
- Pull requests to `main`
- Daily schedule (06:00 UTC)
- Manual trigger with environment selection

### Pipeline Stages

```
┌─────────┐    ┌─────────── ┐    ┌────────┐
│   Lint  │ => │  E2E Tests │ => │ Report │
│ (ruff + │    │ (Playwright│    │(Allure)│
│  mypy)  │    │  + Odoo)   │    │        │
└─────────┘    └─────────── ┘    └────────┘
```

### Test Matrix

| Suite | Markers | Duration (est.) |
|-------|---------|-----------------|
| smoke | `smoke` | ~3 min |
| functional | `functional` | ~15 min |
| negative | `negative` | ~8 min |
| performance | `performance` | ~10 min (currently skipped) |
| full | (all) | ~30 min |

### Artifacts

- Allure test results (retained 30 days)
- Failure screenshots (retained 14 days)
- Playwright traces (retained 14 days)
- JUnit XML reports (retained 30 days)
- k6 performance results (retained 30 days; currently skipped)

## Dashboard & Reporting

### Allure Dashboard

The Allure report provides:

- **Overview Page**: Test pass/fail rates, duration, severity breakdown
- **Categories**: Grouped by feature, story, severity
- **Timeline**: Test execution timeline with threading info
- **Graphs**: Pie charts, bar charts, trend lines
- **Behaviors**: BDD-style feature/story hierarchy
- **Defects**: Flaky tests, broken tests, known issues

To view the dashboard:

```bash
make allure-serve
# Opens http://localhost:8081
```

### k6 Performance Dashboard (currently skipped)

k6 outputs JSON results that can be visualized in:
- Grafana (with InfluxDB)
- k6 Cloud
- Custom dashboards

### CI Dashboard

The GitHub Actions pipeline page shows:
- Test pass/fail status per job
- Execution time trends
- Failure rate tracking
- Artifact download links

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `http://localhost:8069` | Odoo server URL |
| `ADMIN_USER` | `admin` | Admin username |
| `ADMIN_PASSWORD` | `admin` | Admin password |
| `DB_NAME` | `pos_test` | Odoo database name |
| `BROWSER` | `chromium` | Browser to use |
| `HEADLESS` | `true` | Run in headless mode |
| `TIMEOUT` | `30000` | Default timeout (ms) |
| `RETRY_MAX_ATTEMPTS` | `3` | Self-healing retry count |
| `SCREENSHOT_ON_FAILURE` | `true` | Capture screenshot on failure |
| `TRACE_ON_FAILURE` | `true` | Capture Playwright trace |
| `ALLURE_REPORT_DIR` | `reports/allure-results` | Allure output directory |

## Extending the Framework

### Adding a New Page Object

```python
# src/pages/pos/new_feature_page.py
from src.pages.base_page import BasePage

class NewFeaturePage(BasePage):
    SELECTORS = {
        "main_element": ".main-class",
        "submit_button": 'button:has-text("Submit")',
    }

    def do_something(self):
        self.click(self.SELECTORS["submit_button"])
        self.wait_for_page_load()
        return self
```

### Adding a New Keyword

```python
# src/keywords/new_keywords.py
import allure
from src.pages.pos.new_feature_page import NewFeaturePage

class NewFeatureKeywords:
    def __init__(self, page: NewFeaturePage):
        self.page = page

    @allure.step("Execute business workflow")
    def business_workflow(self, param: str):
        self.page.do_something()
        return self.page
```

### Adding a New Test

```python
# src/tests/functional/test_new_feature.py
import allure

@allure.feature("New Feature")
@allure.story("Core Workflow")
class TestNewFeature:
    @allure.title("New feature works correctly")
    def test_basic_flow(self, logged_in_admin, new_feature_keywords):
        result = new_feature_keywords.business_workflow("test")
        assert result is not None
```

## Docker Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `db` | postgres:16-alpine | 5432 | Database |
| `odoo` | odoo:17.0 | 8069 | Odoo POS |
| `adminer` | adminer:latest | 8080 | DB admin UI |

```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d

# Access Odoo: http://localhost:8069
# Access Adminer: http://localhost:8080
#   System: PostgreSQL
#   Server: db
#   Username: odoo
#   Password: odoo17
#   Database: pos_test
```

## Troubleshooting

### Odoo fails to start

```bash
# Check Odoo logs
docker logs pos-odoo

# Check PostgreSQL logs
docker logs pos-postgres

# Ensure entrypoint script is executable
chmod +x docker/entrypoint.sh

# Restart with fresh data
make docker-down && make docker-up
```

### Tests fail with element not found

The self-healing framework tries multiple strategies automatically. If tests still fail:
1. Check the failure screenshot in `screenshots/`
2. Review the Playwright trace in `reports/traces/`
3. Verify the Odoo page has loaded correctly
4. Update selectors in the page object if needed

### Port conflicts

If ports 8069 or 5432 are in use, update `docker-compose.yml` port mappings and set `BASE_URL` accordingly.

### Allure report not generating

```bash
# Ensure allure CLI is installed
brew install allure  # macOS
# OR
npm install -g allure-commandline

# Verify results exist
ls reports/allure-results/
```

