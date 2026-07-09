from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.product_sorting.helpers import MODULE, login_inventory


@pytest.mark.product_sorting
@pytest.mark.system
@pytest.mark.parametrize(
    "case_id,sort_value,description",
    [
        pytest.param("PS-0003", "az", "alphabetically ascending", marks=[pytest.mark.case_id("PS-0003"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0003"),
        pytest.param("PS-0005", "za", "alphabetically descending", marks=[pytest.mark.case_id("PS-0005"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0005"),
    ],
)
def test_name_sorting(driver, record_actual_result, case_id: str, sort_value: str, description: str):
    page = login_inventory(driver)
    page.sort_by_value(sort_value)
    names = page.product_names()
    expected = sorted(names, reverse=sort_value == "za")
    record_actual_result(f"Products were ordered {description}: {', '.join(names)}")
    assert names == expected


@pytest.mark.product_sorting
@pytest.mark.system
@pytest.mark.parametrize(
    "case_id,sort_value,description",
    [
        pytest.param("PS-0007", "lohi", "ascending by price", marks=[pytest.mark.case_id("PS-0007"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0007"),
        pytest.param("PS-0009", "hilo", "descending by price", marks=[pytest.mark.case_id("PS-0009"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PS-0009"),
    ],
)
def test_price_sorting(driver, record_actual_result, case_id: str, sort_value: str, description: str):
    page = login_inventory(driver)
    page.sort_by_value(sort_value)
    prices = page.product_prices()
    expected = sorted(prices, reverse=sort_value == "hilo")
    record_actual_result(f"Products were ordered {description}: {prices}")
    assert prices == expected


@pytest.mark.product_sorting
@pytest.mark.integration
@pytest.mark.case_id("PS-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_default_sort_order_is_deterministic(driver, record_actual_result):
    first = login_inventory(driver).product_names()
    driver.get("https://www.saucedemo.com/inventory.html")
    second = login_inventory(driver).product_names()
    record_actual_result(f"Initial product order was consistent across repeated loads: {', '.join(first)}")
    assert first == second


@pytest.mark.product_sorting
@pytest.mark.integration
@pytest.mark.case_id("PS-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_changing_sort_does_not_alter_cart_contents(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    before_badge = page.cart_count()
    page.sort_by_value("hilo")
    page.open_cart()
    cart_names = CartPage(driver).item_names()
    record_actual_result(f"After changing sort, cart badge was {before_badge} and cart contained: {', '.join(cart_names)}")
    assert before_badge == 1
    assert cart_names == [PRODUCT_A]


@pytest.mark.product_sorting
@pytest.mark.integration
@pytest.mark.case_id("PS-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_sort_remains_usable_after_adding_items(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    page.add_product(PRODUCT_B)
    page.sort_by_value("lohi")
    prices = page.product_prices()
    record_actual_result(f"After adding items, sorting low to high still worked and cart badge stayed {page.cart_count()}.")
    assert prices == sorted(prices)
    assert page.cart_count() == 2
    assert page.button_state_for(PRODUCT_A) == "Remove"
    assert page.button_state_for(PRODUCT_B) == "Remove"


@pytest.mark.product_sorting
@pytest.mark.system
@pytest.mark.case_id("PS-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_sort_behavior_after_refresh_is_deterministic(driver, record_actual_result):
    page = login_inventory(driver)
    page.sort_by_value("za")
    before = page.product_names()
    driver.refresh()
    page.assert_loaded()
    after = page.product_names()
    is_za = after == sorted(after, reverse=True)
    is_default = after == sorted(after)
    record_actual_result(f"After refresh, product order was deterministic: {', '.join(after)}")
    assert before == sorted(before, reverse=True)
    assert is_za or is_default
