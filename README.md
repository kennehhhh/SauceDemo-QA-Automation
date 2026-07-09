# SauceDemo Workbook-Aligned Selenium Automation

This repository is a SauceDemo execution engine for the current workbook-based QA project. The workbook remains the source of truth for test specifications and execution history; pytest/Selenium implements deterministic automated cases and writes actual execution results back to the workbook's `Test Execution Log`.

The suite is intentionally hybrid. It does not claim to automate all 239 workbook cases, all UAT judgment cases, or every user/browser permutation.

## Current Automated Scope

All 14 workbook modules are recognized by the workbook parser and coverage tooling. Only the deterministic proof set below has Selenium implementations right now.

Implemented automated Case IDs:

| Module | Case IDs |
|---|---|
| Login & Session | `LG-0009` through `LG-0015`, `LG-0023` |
| Core Workflows | `CW-0001` through `CW-0007` |

The login module is the proof-of-concept expansion from the workbook. The core workflow tests from the original prototype are preserved and now use explicit Case ID metadata.

## Workbook Module Roadmap

| Code | Workbook Module | Sheet | Automation status |
|---|---|---|---|
| LG | Login & Session | `Login & Session - TC` | Implemented proof set |
| PL | Product Listing | `Product Listing - TC` | Planned |
| PS | Product Sorting | `Product Sorting - TC` | Planned |
| PD | Product Detail | `Product Detail - TC` | Planned |
| CT | Cart | `Cart - TC` | Planned |
| CI | Checkout Information | `Checkout Information - TC` | Planned |
| CO | Checkout Overview | `Checkout Overview - TC` | Planned |
| OC | Order Completion | `Order Completion - TC` | Planned |
| MN | Menu Navigation | `Menu Navigation - TC` | Planned |
| RS | Reset App State | `Reset App State - TC` | Planned |
| AC | Access Session Control | `Access Session Control - TC` | Planned |
| FT | Footer External Links | `Footer External Links - TC` | Planned |
| UX | Interface Responsive | `Interface Responsive - TC` | Planned/manual-heavy |
| CW | Core Workflows | `Core Workflows - TC` | Implemented proof set |

## Project Structure

```text
saucedemo_selenium_core/
+-- artifacts/                  # failure screenshots/page source by run_id
+-- pages/                      # Selenium page objects
+-- results/                    # result models, collector, CSV exporter, run manifests
+-- scripts/
|   +-- coverage_report.py
|   +-- update_workbook.py
|   +-- validate_mappings.py
+-- tests/
|   +-- access_session_control/
|   +-- cart/
|   +-- checkout_information/
|   +-- checkout_overview/
|   +-- core/
|   +-- footer_external_links/
|   +-- interface_responsive/
|   +-- login/
|   +-- menu_navigation/
|   +-- order_completion/
|   +-- product_detail/
|   +-- product_listing/
|   +-- product_sorting/
|   +-- reset_app_state/
|   +-- unit/
|   +-- test_core_workflows.py
+-- workbook/                   # parser, module registry, Test Execution Log updater
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

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Modern Selenium uses Selenium Manager to resolve supported browser drivers automatically when possible.

## Supported Browsers

Directly supported:

- Chrome
- Edge
- Firefox

Opera is listed in the workbook as planning coverage, but this repository does not claim Opera support yet.

Choose a browser:

```powershell
$env:BROWSER="chrome"
pytest
```

Headless:

```powershell
$env:HEADLESS="true"
pytest
```

## Run Tests

Run the full automated suite:

```bash
pytest
```

Run one implemented module:

```bash
pytest tests/login
pytest tests/test_core_workflows.py
```

Run one Case ID:

```bash
pytest --case-id LG-0010
```

## Workbook Result Append

Pass the current workbook path to append the run's execution rows into a saved workbook copy:

```powershell
pytest --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

Optional explicit output path:

```powershell
pytest --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx" --workbook-output "D:\Downloads\SauceDemo-Spreadsheet-automated.xlsx"
```

By default, the updater:

- locates `Test Execution Log`
- appends only actual pytest executions
- preserves existing sheets and execution rows
- validates Case ID and Module against workbook module sheets
- continues existing `EXE-####` values
- writes a new workbook copy
- records `run_id` in Remarks
- prevents duplicate import of the same run through an import ledger

In-place workbook update is deliberately explicit and creates a backup first:

```powershell
pytest --workbook-path "D:\Downloads\SauceDemo-Spreadsheet.xlsx" --workbook-in-place
```

## CSV Fallback and Manifests

Every run writes a structured JSON manifest under `results/`. By default it also writes a workbook-compatible CSV fallback.

Disable CSV export:

```bash
pytest --no-csv
```

Append a previously saved manifest to a workbook copy:

```bash
python scripts/update_workbook.py --workbook "D:\Downloads\SauceDemo-Spreadsheet.xlsx" --manifest "results\execution_manifest_RUN-....json"
```

## Traceability Tools

Validate that implemented Case ID markers exist in the workbook:

```bash
python scripts/validate_mappings.py --workbook "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

Generate an automation coverage summary:

```bash
python scripts/coverage_report.py --workbook "D:\Downloads\SauceDemo-Spreadsheet.xlsx"
```

## Manual vs Automated Scope

Automate cases that are deterministic, observable, repeatable, and meaningful through Selenium.

Keep manual:

- UAT requiring representative-user judgment
- subjective visual quality
- nuanced responsive usability
- performance experience without an agreed threshold
- exploratory checks
- standard-expectation defect classification that needs instructor/project review

Failed automation writes execution evidence, but it does not automatically create confirmed defects.
