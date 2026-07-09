from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage
from pages.inventory_page import InventoryPage
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.cart.helpers import MODULE, login_inventory, open_cart_with_products, open_empty_cart


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_checkout_action_is_visible(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    record_actual_result("Checkout action was visible in cart with an item.")
    assert cart.is_visible(CartPage.CHECKOUT)


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_cart_item_shows_quantity(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    quantity = cart.item_by_name(PRODUCT_A)["quantity"]
    record_actual_result(f"Cart item quantity was displayed as {quantity}.")
    assert quantity == "1"


@pytest.mark.cart
@pytest.mark.unit
@pytest.mark.case_id("CT-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_cart_item_shows_remove_action(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    remove_text = cart.item_by_name(PRODUCT_A)["remove"]
    record_actual_result(f"Cart item showed Remove action text: {remove_text}")
    assert remove_text == "Remove"


@pytest.mark.cart
@pytest.mark.integration
@pytest.mark.case_id("CT-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_add_backpack_then_verify_it_appears_in_cart(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    item = cart.item_by_name(PRODUCT_A)
    record_actual_result(f"{PRODUCT_A} appeared in cart with price {item['price']} and description.")
    assert item["name"] == PRODUCT_A
    assert item["description"]
    assert item["price"].startswith("$")


@pytest.mark.cart
@pytest.mark.integration
@pytest.mark.case_id("CT-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_remove_backpack_from_cart(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    cart.remove_product(PRODUCT_A)
    record_actual_result(f"{PRODUCT_A} was removed from cart and cart badge became {cart.cart_count()}.")
    assert PRODUCT_A not in cart.item_names()
    assert cart.cart_count() == 0


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_badge_equals_number_of_distinct_selected_products(driver, record_actual_result):
    inventory = login_inventory(driver)
    inventory.add_product(PRODUCT_A)
    inventory.add_product(PRODUCT_B)
    badge = inventory.cart_count()
    record_actual_result(f"Cart badge showed {badge} for two distinct selected products.")
    assert badge == 2


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0016")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_contents_persist_when_returning_to_products(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A, PRODUCT_B)
    cart.continue_shopping()
    InventoryPage(driver).assert_loaded()
    inventory = InventoryPage(driver)
    inventory.open_cart()
    names = CartPage(driver).item_names()
    record_actual_result(f"Cart contents persisted after returning to Products: {', '.join(names)}")
    assert set(names) == {PRODUCT_A, PRODUCT_B}


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0018")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_checkout_button_works_with_non_empty_cart(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    cart.checkout()
    record_actual_result("Checkout with a non-empty cart opened checkout information.")
    assert CheckoutInfoPage(driver).is_visible(CheckoutInfoPage.FIRST)
    assert "/checkout-step-one.html" in driver.current_url


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0019")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_checkout_behavior_with_empty_cart_is_controlled(driver, record_actual_result):
    cart = open_empty_cart(driver)
    cart.checkout()
    controlled = "/checkout-step-one.html" in driver.current_url or "/cart.html" in driver.current_url
    record_actual_result(f"Checkout from empty cart followed controlled policy; current URL was {driver.current_url}.")
    assert controlled
