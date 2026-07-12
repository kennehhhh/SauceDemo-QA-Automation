# SauceDemo Workbook-Aligned Selenium Automation

This repository executes Case ID-mapped Selenium tests against the SauceDemo workbook. The attached `SauceDemo-Spreadsheet.xlsx` is the source of truth for scenarios, expected results, user applicability, browser planning, and execution logging.

A module is only implemented when executable pytest/Selenium tests exist for its required Case IDs.

## Implemented Executable Coverage

| Module | Executable Case IDs |
|---|---|
| Login & Session | `LG-0001` through `LG-0039` |
| Product Listing | `PL-0001` through `PL-0023` |
| Product Sorting | `PS-0001` through `PS-0013` |
| Product Detail | `PD-0001` through `PD-0015` |
| Cart | `CT-0001` through `CT-0020` |
| Core Workflows | `CW-0001` through `CW-0007` |

`LG-0040`, `PL-0024`, `PS-0014`, `PD-0016`, `CT-0021`, and `CT-0022` are UAT/manual and intentionally have no Selenium test. Other workbook modules are not implemented yet.

## Current Structure

```text
saucedemo_selenium_core/
+-- artifacts/                  # failure screenshots/page source by run_id
+-- pages/                      # Selenium page objects/components
+-- results/                    # result models, collector, CSV exporter, run manifests
+-- scripts/
|   +-- coverage_report.py
|   +-- update_workbook.py
|   +-- validate_mappings.py
+-- tests/
|   +-- login/                  # executable LG tests
|   +-- product_listing/        # executable PL tests
|   +-- unit/                   # framework/unit tests
|   +-- test_core_workflows.py  # executable CW proof set
+-- workbook/                   # parser, dispositions, module registry, updater
+-- config.py
+-- conftest.py
+-- pytest.ini
+-- requirements.txt
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

## Supported Browsers

Directly supported by the framework:

- Chrome
- Edge
- Firefox

Opera is not implemented.

## Run Tests

Run all currently implemented automated tests:

```bash
pytest
```

Run Login only:

```bash
pytest tests/login
```

Run one workbook Case ID:

```bash
pytest --case-id LG-0010
```

Run one workbook module code:

```bash
pytest --module-code LG
```

Run safe Standard Expectation preflight probes:

```bash
pytest --expectation-preflight --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

## Workbook Result Append

Append actual executions into a new workbook copy:

```powershell
$env:BROWSER="chrome"
$env:TESTER_NAME="Quisayang"
pytest --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

The updater validates Case ID/module mappings, finds the `Test Execution Log` header by content, continues `EXE-####`, preserves existing rows/sheets, and blocks duplicate run imports.

In-place update is opt-in and creates a backup:

```bash
pytest --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx" --workbook-in-place
```

## Mapping And Coverage

Validate implemented Case ID markers against the workbook:

```bash
python scripts/validate_mappings.py --workbook "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

Generate console, JSON, and CSV coverage reports:

```bash
python scripts/coverage_report.py --workbook "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

The generated report distinguishes `AUTO`, `HYBRID`, and `MANUAL` dispositions and does not count folders or README claims as implementation.
