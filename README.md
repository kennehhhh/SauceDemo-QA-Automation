# SauceDemo Selenium Core Workflow Automation

This project automates **only the System-category cases in the latest `Core Workflows - TC` sheet**
from `SauceDemo_Refactored_Committed_Test_Cases.xlsx`.

It intentionally does **not** automate all 239 workbook cases. The scope is the main end-to-end
user flow so the suite stays small, maintainable, and aligned with the workbook.

## Automated workbook cases

| Case ID | Scenario |
|---|---|
| CW-0001 | Successful standard purchase flow |
| CW-0002 | Multi-item purchase flow |
| CW-0003 | Add then remove before checkout |
| CW-0004 | Product detail to cart to checkout |
| CW-0005 | Cancel checkout information and continue shopping |
| CW-0006 | Cancel checkout overview then return to cart |
| CW-0007 | Sort then add cheapest product |

Total automated cases: **7**

## Project structure

```text
saucedemo_selenium_core/
├── case_mapping.csv
├── config.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── pages/
│   ├── base_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── inventory_page.py
│   ├── login_page.py
│   └── product_page.py
├── tests/
│   └── test_core_workflows.py
└── results/
```

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Modern Selenium uses Selenium Manager to resolve supported browser drivers automatically
when possible, so you normally do not need to manually download a driver.

## Run all core System workflows

```bash
pytest tests/test_core_workflows.py
```

Headless Chrome:

```bash
set HEADLESS=true
pytest tests/test_core_workflows.py
```

PowerShell:

```powershell
$env:HEADLESS="true"
pytest tests/test_core_workflows.py
```

## Choose browser

Chrome:

```bash
set BROWSER=chrome
pytest
```

Edge:

```bash
set BROWSER=edge
pytest
```

Firefox:

```bash
set BROWSER=firefox
pytest
```

The framework deliberately does not claim Opera automation support by default. Opera is
Chromium-based, but reliable execution depends on a compatible Opera/Chromium driver setup
and browser binary configuration. Add it only if your environment is explicitly prepared.

## Workbook-aligned result export

After a test session, the framework writes a CSV into `results/` with columns matching the
workbook `Test Execution Log`:

```text
Execution ID
Case ID
Module
Test User
Browser
Actual Result
Status
Related Defect ID
Tester
Execution Date
Remarks
```

You can copy/import those rows into the workbook's `Test Execution Log`.

## Important execution model

The automation project does not pre-create browser × user permutations.

Each pytest run is an actual execution session. For example:

```bash
set BROWSER=chrome
pytest
```

produces Chrome execution rows.

A later run:

```bash
set BROWSER=firefox
pytest
```

produces Firefox execution rows.

That preserves the workbook architecture:
one Case ID may have multiple actual executions, but only when those executions were genuinely run.
