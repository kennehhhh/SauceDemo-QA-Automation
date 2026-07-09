from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkbookModule:
    code: str
    module: str
    sheet_name: str
    test_path: str
    status: str


WORKBOOK_MODULES = [
    WorkbookModule("LG", "Login & Session", "Login & Session - TC", "tests/login", "implemented proof"),
    WorkbookModule("PL", "Product Listing", "Product Listing - TC", "tests/product_listing", "planned"),
    WorkbookModule("PS", "Product Sorting", "Product Sorting - TC", "tests/product_sorting", "planned"),
    WorkbookModule("PD", "Product Detail", "Product Detail - TC", "tests/product_detail", "planned"),
    WorkbookModule("CT", "Cart", "Cart - TC", "tests/cart", "planned"),
    WorkbookModule("CI", "Checkout Information", "Checkout Information - TC", "tests/checkout_information", "planned"),
    WorkbookModule("CO", "Checkout Overview", "Checkout Overview - TC", "tests/checkout_overview", "planned"),
    WorkbookModule("OC", "Order Completion", "Order Completion - TC", "tests/order_completion", "planned"),
    WorkbookModule("MN", "Menu Navigation", "Menu Navigation - TC", "tests/menu_navigation", "planned"),
    WorkbookModule("RS", "Reset App State", "Reset App State - TC", "tests/reset_app_state", "planned"),
    WorkbookModule("AC", "Access Session Control", "Access Session Control - TC", "tests/access_session_control", "planned"),
    WorkbookModule("FT", "Footer External Links", "Footer External Links - TC", "tests/footer_external_links", "planned"),
    WorkbookModule("UX", "Interface Responsive", "Interface Responsive - TC", "tests/interface_responsive", "planned/manual-heavy"),
    WorkbookModule("CW", "Core Workflows", "Core Workflows - TC", "tests/core", "implemented proof"),
]


MODULES_BY_CODE = {module.code: module for module in WORKBOOK_MODULES}
MODULES_BY_NAME = {module.module: module for module in WORKBOOK_MODULES}
