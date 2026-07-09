from __future__ import annotations

from config import USERS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata.products import PRODUCT_A


MODULE = "Checkout Overview"


def login_inventory(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def open_cart_for_products(driver, *product_names: str) -> CartPage:
    inventory = login_inventory(driver)
    for product_name in product_names or (PRODUCT_A,):
        inventory.add_product(product_name)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    return cart


def open_checkout_overview(driver, *product_names: str) -> CheckoutOverviewPage:
    cart = open_cart_for_products(driver, *(product_names or (PRODUCT_A,)))
    cart.checkout()
    info = CheckoutInfoPage(driver)
    info.assert_loaded()
    info.fill(first="John", last="Doe", postal="1000")
    info.continue_checkout()
    page = CheckoutOverviewPage(driver)
    page.assert_loaded()
    return page
