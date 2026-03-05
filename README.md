# Playwright Python Automation Framework for involve.me

This repository contains an automated testing framework for the [involve.me](https://app.involve.me) application, built using **Playwright with Python**. It utilizes the **Page Object Model (POM)** design pattern for maintainability and scalability, and **Allure** for comprehensive reporting.

## 🚀 Features

*   **Framework:** Pytest + Playwright
*   **Design Pattern:** Page Object Model (POM)
*   **Reporting:** Allure Reports (integrated with GitHub Pages)
*   **CI/CD:** Docker & GitHub Actions
*   **Cross-Browser Testing:** Supports Chromium, Firefox, and WebKit (configured via Playwright)
*   **Visual Feedback:** Custom overlay during test execution to show test status.

## 📂 Project Structure

```
python-playwright-involveme/
├── .github/workflows/   # GitHub Actions CI/CD configuration
├── data/                # Data-driven test files (CSV)
├── pages/               # Page Object Model (POM) classes
│   ├── components/      # Shared UI components (Header, etc.)
│   ├── editor_elements/ # Specific editor element classes
│   └── ui_types/        # Type definitions for UI elements
├── playwright/          # Playwright specific configurations (auth, etc.)
├── tests/               # Test cases
│   ├── test_00_cleanup.py # Cleanup script (runs first)
│   └── ...              # Other test files
├── utils/               # Utility functions (visual effects, data handlers)
├── config.py            # Global configuration settings
├── conftest.py          # Pytest fixtures and hooks
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker image definition
├── pytest.ini           # Pytest configuration
└── requirements.txt     # Python dependencies
```

## 🛠️ Prerequisites

*   Python 3.8+
*   Pip (Python Package Manager)
*   Docker & Docker Compose (optional, for containerized execution)

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/python-playwright-involveme.git
    cd python-playwright-involveme
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

5.  **Environment Setup:**
    Copy the example environment file and update it with your credentials:
    ```bash
    cp .env.example .env
    ```

## 🏃‍♂️ Running Tests

### Local Execution

To run all tests:
```bash
pytest
```

To run a specific test file:
```bash
pytest tests/test_project_page.py
```

To view Allure reports (the results are automatically generated as configured in `pytest.ini`):
```bash
allure serve allure-results
```

### Docker Execution

To run tests inside a Docker container using Docker Compose:

```bash
docker compose up --build
```
**It is recommended to first run `pytest --headed` outside of Docker until login is complete, because sometimes manual verification is required (e.g., CAPTCHA or email code).**

*This command runs the cleanup test first, followed by all other tests, and maps the `allure-results` to your local machine.*

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for Continuous Integration.
*   **Workflow File:** `.github/workflows/main.yml`
*   **Trigger:** Pushes to the `main` branch.
*   **Steps:**
    1.  Checkout code.
    2.  Build Docker image.
    3.  Run tests via Docker Compose.
    4.  Generate Allure Report.
    5.  Deploy report to GitHub Pages.

**Note:** Ensure you add `USER_EMAIL` and `USER_PASSWORD` to your GitHub Repository Secrets for the pipeline to work correctly.

## 🧪 Key Test Scenarios

*   **Cleanup:** `test_00_cleanup.py` ensures a clean state by deleting old workspaces before the test suite runs.
*   **Project Management:** Create, rename, delete, and search workspaces/funnels.
*   **Editor:** Add/remove elements, change element properties, drag & drop.
*   **Preview:** Validate the published funnel behavior (slider, dropdowns, etc.).

## 📝 Code Standards

*   **Type Hinting:** Used extensively for better code analysis and auto-completion.
*   **Fixtures:** Pytest fixtures are used for setup/teardown (e.g., login, creating workspaces).
*   **Dynamic Waits:** Playwright's auto-waiting and explicit `wait_for` are used instead of hard sleeps where possible.

## 📧 Contact

For any questions or suggestions, please feel free to reach out.
