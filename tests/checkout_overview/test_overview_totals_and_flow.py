from __future__ import annotations

from collections import Counter

import pytest

from pages.checkout_page import CheckoutCompletePage, CheckoutInfoPage, CheckoutOverviewPage
from testdata.products import PRODUCT_A, PRODUCT_B, PRODUCT_RED_SHIRT
from tests.checkout_overview.helpers import MODULE, open_cart_for_products, open_checkout_overview


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_item_total_equals_sum_of_listed_item_prices(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A, PRODUCT_B)
    summed_prices = round(sum(page.item_prices()), 2)
    subtotal = page.subtotal()
    record_actual_result(f"Listed item prices summed to ${summed_prices:.2f}; displayed item total was ${subtotal:.2f}.")
    assert subtotal == summed_prices


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_displayed_total_is_mathematically_consistent(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A, PRODUCT_B)
    subtotal = page.subtotal()
    tax = page.tax()
    total = page.total()
    calculated_total = round(subtotal + tax, 2)
    record_actual_result(f"Subtotal ${subtotal:.2f} plus tax ${tax:.2f} equaled ${calculated_total:.2f}; displayed total was ${total:.2f}.")
    assert total == calculated_total


@pytest.mark.checkout_overview
@pytest.mark.system
@pytest.mark.case_id("CO-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_single_item_overview_matches_cart(driver, record_actual_result):
    cart = open_cart_for_products(driver, PRODUCT_A)
    cart_items = cart.items()
    cart.checkout()

    info = CheckoutInfoPage(driver)
    info.fill(first="John", last="Doe", postal="1000")
    info.continue_checkout()
    overview = CheckoutOverviewPage(driver)
    overview.assert_loaded()
    overview_items = overview.items()
    record_actual_result(f"Cart item and overview item were both {overview_items[0]['name']!r}.")
    assert overview_items == [
        {
            "quantity": cart_items[0]["quantity"],
            "name": cart_items[0]["name"],
            "description": cart_items[0]["description"],
            "price": cart_items[0]["price"],
        }
    ]


@pytest.mark.checkout_overview
@pytest.mark.system
@pytest.mark.case_id("CO-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_multiple_item_overview_matches_cart(driver, record_actual_result):
    products = (PRODUCT_A, PRODUCT_B, PRODUCT_RED_SHIRT)
    page = open_checkout_overview(driver, *products)
    names = page.item_names()
    record_actual_result(f"Overview displayed multiple items: {', '.join(names)}.")
    assert Counter(names) == Counter(products)


@pytest.mark.checkout_overview
@pytest.mark.system
@pytest.mark.case_id("CO-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_finish_completes_order(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    page.finish()
    CheckoutCompletePage(driver).assert_complete()
    record_actual_result("Finish opened the Order Completion page.")
