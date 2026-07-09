from __future__ import annotations

import pytest

from config import USERS
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage


PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


def login_standard(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def complete_checkout(driver) -> None:
    info = CheckoutInfoPage(driver)
    info.fill()
    info.continue_checkout()
    overview = CheckoutOverviewPage(driver)
    overview.finish()
    CheckoutCompletePage(driver).assert_complete()


@pytest.mark.core
@pytest.mark.system
def test_CW_0001_successful_standard_purchase_flow(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    assert inventory.cart_count() == 1
    inventory.open_cart()

    cart = CartPage(driver)
    assert cart.item_names() == [PRODUCT_A]
    cart.checkout()
    complete_checkout(driver)


@pytest.mark.core
@pytest.mark.system
def test_CW_0002_multi_item_purchase_flow(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.add_product(PRODUCT_B)
    assert inventory.cart_count() == 2
    inventory.open_cart()

    cart = CartPage(driver)
    assert set(cart.item_names()) == {PRODUCT_A, PRODUCT_B}
    cart.checkout()

    info = CheckoutInfoPage(driver)
    info.fill()
    info.continue_checkout()

    overview = CheckoutOverviewPage(driver)
    assert set(overview.item_names()) == {PRODUCT_A, PRODUCT_B}
    overview.finish()
    CheckoutCompletePage(driver).assert_complete()


@pytest.mark.core
@pytest.mark.system
def test_CW_0003_add_then_remove_before_checkout(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.add_product(PRODUCT_B)
    inventory.open_cart()

    cart = CartPage(driver)
    cart.remove_product(PRODUCT_B)
    assert cart.item_names() == [PRODUCT_A]
    cart.checkout()
    complete_checkout(driver)


@pytest.mark.core
@pytest.mark.system
def test_CW_0004_product_detail_to_cart_to_checkout(driver):
    inventory = login_standard(driver)
    inventory.open_product(PRODUCT_A)

    product = ProductPage(driver)
    product.assert_product(PRODUCT_A)
    product.add_to_cart()
    product.open_cart()

    cart = CartPage(driver)
    assert cart.item_names() == [PRODUCT_A]
    cart.checkout()
    complete_checkout(driver)


@pytest.mark.core
@pytest.mark.system
def test_CW_0005_cancel_checkout_information_and_continue_shopping(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()

    cart = CartPage(driver)
    cart.checkout()

    info = CheckoutInfoPage(driver)
    info.cancel()

    # SauceDemo returns from checkout information to the cart.
    assert "/cart.html" in driver.current_url
    CartPage(driver).continue_shopping()
    InventoryPage(driver).assert_loaded()


@pytest.mark.core
@pytest.mark.system
def test_CW_0006_cancel_checkout_overview_then_return_to_cart(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    CartPage(driver).checkout()

    info = CheckoutInfoPage(driver)
    info.fill()
    info.continue_checkout()

    CheckoutOverviewPage(driver).cancel()

    # Current SauceDemo behavior returns to Products after cancelling overview.
    InventoryPage(driver).assert_loaded()
    InventoryPage(driver).open_cart()
    assert CartPage(driver).item_names() == [PRODUCT_A]


@pytest.mark.core
@pytest.mark.system
def test_CW_0007_sort_then_add_cheapest_product(driver):
    inventory = login_standard(driver)
    inventory.sort_by_value("lohi")

    prices = inventory.product_prices()
    assert prices == sorted(prices)

    sorted_names = inventory.product_names()
    cheapest_name = sorted_names[0]
    inventory.add_product(cheapest_name)
    inventory.open_cart()

    assert CartPage(driver).item_names() == [cheapest_name]
