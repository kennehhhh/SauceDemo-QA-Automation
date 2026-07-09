from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage
from pages.inventory_page import InventoryPage
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.order_completion.helpers import MODULE, complete_order
from tests.checkout_overview.helpers import open_checkout_overview


@pytest.mark.order_completion
@pytest.mark.unit
@pytest.mark.case_id("OC-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_completion_heading_is_displayed(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A)
    heading = page.text(CheckoutCompletePage.TITLE)
    record_actual_result(f"Completion heading was visible as {heading!r}.")
    assert heading == "Checkout: Complete!"


@pytest.mark.order_completion
@pytest.mark.unit
@pytest.mark.case_id("OC-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_success_message_is_displayed(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A)
    message = page.success_message()
    record_actual_result(f"Completion success message was: {message}.")
    assert "thank you" in message.lower()
    assert "order" in message.lower()


@pytest.mark.order_completion
@pytest.mark.unit
@pytest.mark.case_id("OC-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_back_home_button_is_visible(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A)
    visible = page.is_visible(CheckoutCompletePage.BACK_HOME)
    record_actual_result("Back Home action was visible." if visible else "Back Home action was not visible.")
    assert visible


@pytest.mark.order_completion
@pytest.mark.system
@pytest.mark.case_id("OC-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_finish_navigates_to_completion_page(driver, record_actual_result):
    overview = open_checkout_overview(driver, PRODUCT_A)
    overview.finish()
    CheckoutCompletePage(driver).assert_complete()
    record_actual_result("Finish navigated from Checkout Overview to Order Completion.")


@pytest.mark.order_completion
@pytest.mark.system
@pytest.mark.case_id("OC-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_back_home_returns_to_products_page(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A)
    page.back_home()
    InventoryPage(driver).assert_loaded()
    record_actual_result("Back Home returned to the Products page.")


@pytest.mark.order_completion
@pytest.mark.system
@pytest.mark.case_id("OC-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_purchased_cart_badge_is_cleared_after_completion(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A, PRODUCT_B)
    count = page.cart_count()
    record_actual_result(f"Cart badge count after completion was {count}.")
    assert count == 0


@pytest.mark.order_completion
@pytest.mark.system
@pytest.mark.case_id("OC-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_purchased_items_are_not_left_in_cart_after_completion(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A, PRODUCT_B)
    page.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    names = cart.item_names()
    record_actual_result(f"Cart items after completion were: {', '.join(names) or '<none>'}.")
    assert names == []


@pytest.mark.order_completion
@pytest.mark.system
@pytest.mark.case_id("OC-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_refresh_completion_page_does_not_create_duplicate_order_side_effect(driver, record_actual_result):
    page = complete_order(driver, PRODUCT_A)
    driver.refresh()
    page = CheckoutCompletePage(driver)
    page.assert_complete()
    count = page.cart_count()
    record_actual_result(f"After refreshing completion page, completion remained visible and cart badge count was {count}.")
    assert count == 0
