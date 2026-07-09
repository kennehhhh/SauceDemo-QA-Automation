from __future__ import annotations

import pytest

from pages.inventory_page import InventoryPage
from tests.product_sorting.helpers import MODULE, SORT_OPTIONS, login_inventory


@pytest.mark.product_sorting
@pytest.mark.unit
@pytest.mark.case_id("PS-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_sort_dropdown_is_visible(driver, record_actual_result):
    page = login_inventory(driver)
    record_actual_result("Sort dropdown was visible and enabled on the Products page.")
    assert page.is_visible(InventoryPage.SORT)
    assert page.is_enabled(InventoryPage.SORT)


@pytest.mark.product_sorting
@pytest.mark.unit
@pytest.mark.parametrize(
    "label,case_id",
    [
        pytest.param("Name (A to Z)", "PS-0002", marks=[pytest.mark.case_id("PS-0002"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0002"),
        pytest.param("Name (Z to A)", "PS-0004", marks=[pytest.mark.case_id("PS-0004"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0004"),
        pytest.param("Price (low to high)", "PS-0006", marks=[pytest.mark.case_id("PS-0006"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0006"),
        pytest.param("Price (high to low)", "PS-0008", marks=[pytest.mark.case_id("PS-0008"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0008"),
    ],
)
def test_sort_option_is_available(driver, record_actual_result, label: str, case_id: str):
    page = login_inventory(driver)
    options = page.sort_options()
    record_actual_result(f"Sort options displayed: {', '.join(options)}; requested option {label} was present.")
    assert label in options
    assert SORT_OPTIONS[label]
