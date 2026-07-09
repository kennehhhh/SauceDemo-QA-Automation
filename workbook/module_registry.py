from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkbookModule:
    code: str
    module: str
    sheet_name: str
    test_path: str


WORKBOOK_MODULES = [
    WorkbookModule("LG", "Login & Session", "Login & Session - TC", "tests/login"),
    WorkbookModule("PL", "Product Listing", "Product Listing - TC", "tests/product_listing"),
    WorkbookModule("PS", "Product Sorting", "Product Sorting - TC", "tests/product_sorting"),
    WorkbookModule("PD", "Product Detail", "Product Detail - TC", "tests/product_detail"),
    WorkbookModule("CT", "Cart", "Cart - TC", "tests/cart"),
    WorkbookModule("CI", "Checkout Information", "Checkout Information - TC", "tests/checkout_information"),
    WorkbookModule("CO", "Checkout Overview", "Checkout Overview - TC", "tests/checkout_overview"),
    WorkbookModule("OC", "Order Completion", "Order Completion - TC", "tests/order_completion"),
    WorkbookModule("MN", "Menu & Navigation", "Menu Navigation - TC", "tests/menu_navigation"),
    WorkbookModule("RS", "Reset App State", "Reset App State - TC", "tests/reset_app_state"),
    WorkbookModule("AC", "Access & Session Control", "Access Session Control - TC", "tests/access_session_control"),
    WorkbookModule("FT", "Footer & External Links", "Footer External Links - TC", "tests/footer_external_links"),
    WorkbookModule("UX", "Interface / Responsive", "Interface Responsive - TC", "tests/interface_responsive"),
    WorkbookModule("CW", "Core Workflows", "Core Workflows - TC", "tests/core"),
]


MODULES_BY_CODE = {module.code: module for module in WORKBOOK_MODULES}
MODULES_BY_NAME = {module.module: module for module in WORKBOOK_MODULES}
