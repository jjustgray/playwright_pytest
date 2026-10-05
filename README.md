# Playwright + Pytest Automation Testing Framework

Automation testing framework for the [Automation Exercise](https://www.automationexercise.com/test_cases) website, built with **Python**, **Playwright**, **Pytest**, and **Allure Reporter**.

## 🚀 Framework Features
* **Page Object Model (POM)**: Modular and maintainable page architecture.
* **Parallel Execution**: Running tests in multiple threads via `pytest-xdist`.
* **Cross-Browser Support**: Support for Chromium, Firefox, and WebKit.
* **Allure Reports**: Detailed reports with screenshots for failed tests and step-by-step reporting (`@allure.step`).
* **CI/CD Pipeline**: Configured GitHub Actions workflow with automated report deployment to **GitHub Pages**.
* **Slack Notifications**: Automated test run status notifications sent to Slack with direct links to the Allure Report.

---

## 📋 Requirements
* **Python**: 3.10 or higher
* **Node.js**: 18.0 or higher (required for local `@allure/cli` dependency)
* **Java (JDK/JRE)**: 11 or higher (required by Allure CLI to generate reports)

---

## 👉 Quick Start (Local)

1. Clone the repository
```
git clone https://github.com/jjustgray/playwright_pytest.git
cd playwright_pytest
```

2. Set up virtual environment and install dependencies
post-create: 
```
python -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows (Git Bash):
source venv/Scripts/activate

# Install Python & Node.js packages 
pip install -r requirements.txt
npm install

# Install Playwright browsers
playwright install --with-deps
```

---

## 🧪 Project Execution (poethepoet usage)

| Command | Description |
| :--- | :--- |
|`poe test` | Run all tests in headless mode |
|`poe test-headed` | Run tests with browser UI enabled (Headed mode) |
|`poe test-file` | Run a specific test file (Usage: poe test-file specs/test_contactus.py) |
|`poe test-browser` | Run tests in a specific browser (Usage: poe test-browser --browser firefox) |
|`poe test-smoke` | Run critical-path smoke tests only |
|`poe test-regression` | Run regression tests only |
|`poe test-all-browsers` | Run tests parallel across all three supported browsers |
|`poe test-parallel` | Run tests parallel in 4 threads in one browser |
|`poe clean` | Clean up report directories, pytest cache, and Python bytecode files |

`smoke` tests are a small set of quick checks for critical user journeys. `regression` tests cover the remaining features, negative cases, and detailed behavior. All tests in this project are end-to-end browser tests; these markers select a run group, not a test level.

---

### 📁 Generate and open Allure report locally using npx

```
poe serve-report
```

---

## ⊔ CI/CD & Slack Notifications
* **GitHub Actions**: Automated test execution on every push / pull request.
* **GitHub Pages**: Automated Allure report deployment after each test run.
* **Slack**: Automated notifications containing execution status and direct link to GitHub Pages.