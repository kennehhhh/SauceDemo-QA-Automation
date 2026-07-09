from __future__ import annotations

import pytest

from tests.product_listing.helpers import MODULE, login_inventory
from workbook.expectation_policy import ExpectationBlocked


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0021")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_product_search_control_is_available(driver, record_actual_result):
    page = login_inventory(driver)
    exists = page.search_exists()
    record_actual_result(
        "Product search control was present on the product listing page."
        if exists
        else "No product search control was present on the product listing page."
    )
    assert exists


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0022")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_search_returns_matching_products(driver, record_actual_result):
    page = login_inventory(driver)
    if not page.search_exists():
        raise ExpectationBlocked(
            "PL-0022",
            "PL-0021",
            "Search filtering behavior could not be executed because no product search control was present.",
        )
    page.search("Backpack")
    names = page.product_names()
    record_actual_result(f"Searching for Backpack returned products: {', '.join(names)}")
    assert names == ["Sauce Labs Backpack"]


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0023")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_no_result_search_state_is_clear(driver, record_actual_result):
    page = login_inventory(driver)
    if not page.search_exists():
        raise ExpectationBlocked(
            "PL-0023",
            "PL-0021",
            "No-result search behavior could not be executed because no product search control was present.",
        )
    page.search("not-a-real-product-name")
    names = page.product_names()
    record_actual_result(f"No-result search returned {len(names)} products.")
    assert not names
