from __future__ import annotations

import pytest

from config import USERS
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_RED_SHIRT
from tests.access_session_control.helpers import protected_url


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
@pytest.mark.case_id("CW-0001")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("A standard user completed a one-item purchase and reached the checkout confirmation page.")
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
@pytest.mark.case_id("CW-0002")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("A standard user completed checkout with three selected products.")
def test_CW_0002_multi_item_purchase_flow(driver):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.add_product(PRODUCT_B)
    inventory.add_product(PRODUCT_RED_SHIRT)
    assert inventory.cart_count() == 3
    inventory.open_cart()

    cart = CartPage(driver)
    assert set(cart.item_names()) == {PRODUCT_A, PRODUCT_B, PRODUCT_RED_SHIRT}
    cart.checkout()

    info = CheckoutInfoPage(driver)
    info.fill()
    info.continue_checkout()

    overview = CheckoutOverviewPage(driver)
    assert set(overview.item_names()) == {PRODUCT_A, PRODUCT_B, PRODUCT_RED_SHIRT}
    overview.finish()
    CheckoutCompletePage(driver).assert_complete()


@pytest.mark.core
@pytest.mark.system
@pytest.mark.case_id("CW-0003")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("After removing one selected item before checkout, only the remaining item was purchased.")
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
@pytest.mark.case_id("CW-0004")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("A product was opened from detail view, added to cart, and completed through checkout.")
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
@pytest.mark.case_id("CW-0005")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("Cancel on checkout information returned to the cart, and Continue Shopping returned to Products.")
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
@pytest.mark.case_id("CW-0006")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("Cancel on checkout overview returned to Products while preserving the selected cart item.")
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
@pytest.mark.case_id("CW-0007")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
@pytest.mark.actual_result("Products sorted from low to high price, and the cheapest displayed product was added to cart.")
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


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0008")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0008_login_success_loads_product_listing(driver, record_actual_result):
    login_standard(driver)
    record_actual_result("Successful login loaded the Product Listing inventory module.")


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0009")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0009_add_from_listing_updates_cart_module(driver, record_actual_result):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    names = CartPage(driver).item_names()
    record_actual_result(f"Cart module displayed listing-selected items: {', '.join(names)}.")
    assert names == [PRODUCT_A]


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0010")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0010_cart_checkout_passes_item_state_to_checkout_info(driver, record_actual_result):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    cart = CartPage(driver)
    assert cart.item_names() == [PRODUCT_A]
    cart.checkout()
    CheckoutInfoPage(driver).assert_loaded()
    CheckoutInfoPage(driver).cancel()
    preserved = CartPage(driver).item_names()
    record_actual_result(f"Checkout Information opened and returning to cart preserved items: {', '.join(preserved)}.")
    assert preserved == [PRODUCT_A]


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0011")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0011_checkout_info_passes_item_state_to_overview(driver, record_actual_result):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    CartPage(driver).checkout()
    info = CheckoutInfoPage(driver)
    info.fill(first="John", last="Doe", postal="1000")
    info.continue_checkout()
    names = CheckoutOverviewPage(driver).item_names()
    record_actual_result(f"Checkout Overview included items passed from Checkout Information: {', '.join(names)}.")
    assert names == [PRODUCT_A]


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0012")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0012_overview_finish_passes_to_completion(driver, record_actual_result):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    CartPage(driver).checkout()
    info = CheckoutInfoPage(driver)
    info.fill(first="John", last="Doe", postal="1000")
    info.continue_checkout()
    CheckoutOverviewPage(driver).finish()
    CheckoutCompletePage(driver).assert_complete()
    record_actual_result("Checkout Overview Finish opened the Order Completion page.")


@pytest.mark.core
@pytest.mark.integration
@pytest.mark.case_id("CW-0013")
@pytest.mark.module("Core Workflows")
@pytest.mark.test_user("standard_user")
def test_CW_0013_menu_logout_invalidates_protected_navigation(driver, record_actual_result):
    login_standard(driver)
    MenuComponent(driver).open().logout()
    driver.get(protected_url("/inventory.html"))
    blocked = LoginPage(driver).is_visible(LoginPage.LOGIN)
    record_actual_result("After menu logout, direct protected navigation returned to login." if blocked else "After menu logout, protected navigation remained usable.")
    assert blocked
