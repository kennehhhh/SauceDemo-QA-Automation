from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutOverviewPage
from testdata.products import PRODUCT_A
from tests.checkout_information.helpers import (
    MODULE,
    VALID_FIRST,
    VALID_LAST,
    VALID_POSTAL,
    open_checkout_information,
)


@pytest.mark.checkout_information
@pytest.mark.integration
@pytest.mark.case_id("CI-0025")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cancel_returns_to_cart_with_items_preserved(driver, record_actual_result):
    page = open_checkout_information(driver, PRODUCT_A)
    page.cancel()
    cart = CartPage(driver)
    cart.assert_loaded()
    names = cart.item_names()
    record_actual_result(f"Cancel returned to cart with items: {', '.join(names) or '<none>'}.")
    assert names == [PRODUCT_A]


@pytest.mark.checkout_information
@pytest.mark.integration
@pytest.mark.case_id("CI-0026")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_valid_information_advances_to_overview(driver, record_actual_result):
    page = open_checkout_information(driver, PRODUCT_A)
    page.fill(first=VALID_FIRST, last=VALID_LAST, postal=VALID_POSTAL)
    page.continue_checkout()
    overview = CheckoutOverviewPage(driver)
    overview.assert_loaded()
    record_actual_result("Valid checkout information opened Checkout Overview.")
