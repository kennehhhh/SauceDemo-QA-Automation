from __future__ import annotations

import re

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.cart.helpers import MODULE, open_cart_with_products, open_empty_cart


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_page_heading_is_displayed(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    heading = cart.text(CartPage.TITLE)
    record_actual_result(f"Cart page heading was displayed as: {heading}")
    assert heading == "Your Cart"


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_continue_shopping_action_is_visible(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    record_actual_result("Continue Shopping action was visible in cart.")
    assert cart.is_visible(CartPage.CONTINUE)


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_cart_item_shows_name(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    names = cart.item_names()
    record_actual_result(f"Cart item names displayed: {', '.join(names)}")
    assert names == [PRODUCT_A]


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_cart_item_shows_description(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    item = cart.item_by_name(PRODUCT_A)
    record_actual_result("Cart item displayed a non-empty product description.")
    assert item["description"]


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_cart_item_shows_price(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    price = cart.item_by_name(PRODUCT_A)["price"]
    record_actual_result(f"Cart item displayed valid price: {price}")
    assert re.match(r"^\$\d+\.\d{2}$", price)


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_empty_cart_page_opens(driver, record_actual_result):
    cart = open_empty_cart(driver)
    record_actual_result("Empty cart page opened without crash and showed no item rows.")
    assert cart.is_empty()
    assert "/cart.html" in driver.current_url


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_empty_cart_displays_controlled_empty_state(driver, record_actual_result):
    cart = open_empty_cart(driver)
    record_actual_result("Empty cart used an intentionally empty list state with no item rows.")
    assert cart.is_empty()
    assert cart.is_visible(CartPage.CART_LIST)


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_multiple_distinct_items_appear_once_each(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A, PRODUCT_B)
    names = cart.item_names()
    record_actual_result(f"Multiple selected products appeared once each: {', '.join(names)}")
    assert set(names) == {PRODUCT_A, PRODUCT_B}
    assert len(names) == len(set(names))


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_continue_shopping_returns_to_products_page(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    cart.continue_shopping()
    InventoryPage(driver).assert_loaded()
    record_actual_result("Continue Shopping returned from cart to the Products inventory page.")
    assert "/inventory.html" in driver.current_url


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0017")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_removing_one_of_several_items_preserves_others(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A, PRODUCT_B)
    cart.remove_product(PRODUCT_B)
    names = cart.item_names()
    record_actual_result(f"After removing {PRODUCT_B}, remaining cart items were: {', '.join(names)}")
    assert names == [PRODUCT_A]
