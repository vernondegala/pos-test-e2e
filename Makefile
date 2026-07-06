.PHONY: help setup dev test lint clean docker-up docker-down docker-ci allure-report perf-test

help:
	@echo "POS E2E Test Automation Framework"
	@echo "================================="
	@echo ""
	@echo "Development Commands:"
	@echo "  make setup           Install all dependencies"
	@echo "  make dev             Install dev dependencies (includes Playwright browsers)"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up       Start Odoo + PostgreSQL containers"
	@echo "  make docker-down     Stop and remove containers"
	@echo "  make docker-ci       Start CI-optimized containers"
	@echo "  make docker-logs     View container logs"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test            Run all tests"
	@echo "  make test-smoke      Run smoke tests only"
	@echo "  make test-func       Run functional tests only"
	@echo "  make test-negative   Run negative tests only"
	@echo "  make test-perf       Run performance tests only"
	@echo "  make test-parallel   Run tests in parallel (4 workers)"
	@echo ""
	@echo "Reporting:"
	@echo "  make allure-report   Generate Allure report from results"
	@echo "  make allure-serve    Serve Allure report locally"
	@echo ""
	@echo "Performance:"
	@echo "  make k6-test         Run k6 performance load test"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            Run ruff linter"
	@echo "  make typecheck       Run mypy type checker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove temporary files and reports"

setup:
	pip install --upgrade pip
	pip install -r requirements.txt
	playwright install chromium

dev: setup
	playwright install-deps chromium

docker-up:
	docker compose -f docker/docker-compose.yml up -d --build
	@echo "Waiting for Odoo to be ready..."
	@until curl -s http://localhost:8069/web/login > /dev/null 2>&1; do sleep 5; done
	@echo "Odoo is ready at http://localhost:8069"

docker-down:
	docker compose -f docker/docker-compose.yml down -v

docker-ci:
	docker compose -f docker/docker-compose.ci.yml up -d

docker-logs:
	docker compose -f docker/docker-compose.yml logs -f

test:
	pytest src/tests/functional/test_auth.py src/tests/functional/test_receipt_verification.py src/tests/functional/test_multi_payment.py src/tests/functional/test_stock_alerts.py src/tests/network/test_offline_resilience.py src/tests/compatibility/test_multi_currency.py src/tests/usability/ -v --timeout=30

test-smoke:
	pytest src/tests/functional/test_auth.py src/tests/usability/ -v --timeout=20

test-func:
	pytest src/tests/functional/ -v

test-negative:
	pytest src/tests/negative/ -v

test-perf:
	pytest src/tests/performance/ -v -k "not k6"

test-parallel:
	pytest src/tests/ -n 4 --dist loadscope -v

allure-report:
	JAVA_HOME="$$HOME/Library/Java/JavaVirtualMachines/jdk-17.0.12+7-jre/Contents/Home" PATH="$$JAVA_HOME/bin:$$HOME/.local/bin:$$PATH" allure generate reports/allure-results -o reports/allure-report --clean

allure-serve:
	JAVA_HOME="$$HOME/Library/Java/JavaVirtualMachines/jdk-17.0.12+7-jre/Contents/Home" PATH="$$JAVA_HOME/bin:$$HOME/.local/bin:$$PATH" allure serve reports/allure-results --port 8081

k6-test:
	k6 run src/tests/performance/k6/pos_browse_test.js

lint:
	ruff check src/ --fix

typecheck:
	mypy src/ --ignore-missing-imports || true

clean:
	rm -rf reports/allure-results reports/allure-report reports/junit reports/traces screenshots .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
