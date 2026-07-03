# POS System - End-to-End Test Automation Framework

Automated E2E testing framework for [Odoo POS](https://github.com/odoo/odoo) (Point of Sale) system, featuring self-healing locators, CI/CD integration, and graphical reporting dashboards.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Test Layer (Tests)                     │
│  ┌──────────────┐ ┌──────────┐ ┌───────────────────┐    │
│  │  Functional   │ │ Negative │ │   Performance      │    │
│  │    Tests      │ │  Tests   │ │  Tests (k6 + PW)   │    │
│  └──────┬───────┘ └────┬─────┘ └─────────┬─────────┘    │
├─────────┼──────────────┼────────────────┼───────────────┤
│         │   Keywords Layer (Shared Business Ops)         │
│  ┌──────┴──────┐ ┌────┴─────┐ ┌────┴────┐ ┌───────┐    │
│  │ AuthKeywords│ │PosKeywords│ │ProdKwyrd│ │Payment│    │
│  └──────┬──────┘ └────┬─────┘ └────┬────┘ └───┬───┘    │
├─────────┼──────────────┼────────────┼──────────┼────────┤
│         │    Page Object Model (POM)                    │
│  ┌──────┴──────┐ ┌────┴─────┐ ┌────┴────┐ ┌────┴───┐  │
│  │  LoginPage  │ │  POSPage │ │ ProdPage│ │ CustPg │  │
│  └──────┬──────┘ └────┬─────┘ └────┬────┘ └────┬───┘  │
├─────────┼──────────────┼────────────┼──────────┼────────┤
│         │        Core Framework                          │
│  ┌──────┴──────────────────────────────────────────┐    │
│  │    Self-Healing Layer (LocatorManager + Retry)    │   │
│  ├──────────────────────────────────────────────────┤    │
│  │         Browser Manager (Playwright)              │   │
│  ├──────────────────────────────────────────────────┤    │
│  │              Config + Fixtures                    │   │
│  └──────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│     Docker (Odoo 17.0 + PostgreSQL 16)                   │
│     CI/CD (GitHub Actions + Allure Report)               │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Test Runner** | Pytest | Test execution, fixtures, parallelization |
| **Browser Automation** | Playwright | Fast, reliable browser control with auto-waiting |
| **Self-Healing** | Custom LocatorManager | Multi-strategy locator fallback chain |
| **Reporting** | Allure Framework | Interactive HTML dashboard with graphs |
| **Load Testing** | k6 (Grafana) | High-performance API load testing |
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
│   │   └── performance/          # Performance test cases
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

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+ (for k6 performance tests)

### 1. Setup

```bash
# Clone the repository
git clone <repo-url> pos-test-e2e
cd pos-test-e2e

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
make setup
```

### 2. Start Odoo Environment

```bash
# Start Odoo + PostgreSQL
make docker-up

# Verify Odoo is running
curl http://localhost:8069/web/login
```

### 3. Run Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-smoke       # Quick smoke tests
make test-func        # Functional tests only
make test-negative    # Negative tests only
make test-perf        # Performance tests only

# Run tests in parallel (4 workers)
make test-parallel

# Run load tests with k6
make k6-test
```

### 4. View Reports

```bash
# Generate Allure report
make allure-report

# Serve Allure report locally
make allure-serve
# Open http://localhost:8081 in your browser
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

### Performance Tests (6+ scenarios)

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
┌─────────┐    ┌───────────┐    ┌─────────────┐    ┌────────┐
│   Lint  │ => │  E2E Tests│ => │  k6 Load    │ => │ Report │
│ (ruff + │    │ (Playwright│   │  Test       │    │(Allure)│
│  mypy)  │    │  + Odoo)  │    │             │    │        │
└─────────┘    └───────────┘    └─────────────┘    └────────┘
```

### Test Matrix

| Suite | Markers | Duration (est.) |
|-------|---------|-----------------|
| smoke | `smoke` | ~3 min |
| functional | `functional` | ~15 min |
| negative | `negative` | ~8 min |
| performance | `performance` | ~10 min |
| full | (all) | ~30 min |

### Artifacts

- Allure test results (retained 30 days)
- Failure screenshots (retained 14 days)
- Playwright traces (retained 14 days)
- JUnit XML reports (retained 30 days)
- k6 performance results (retained 30 days)

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

### k6 Performance Dashboard

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

