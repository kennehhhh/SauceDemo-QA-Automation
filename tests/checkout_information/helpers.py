from __future__ import annotations

from config import USERS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata.products import PRODUCT_A


MODULE = "Checkout Information"
VALID_FIRST = "John"
VALID_LAST = "Doe"
VALID_POSTAL = "1000"


def login_inventory(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def open_checkout_information(driver, product_name: str = PRODUCT_A) -> CheckoutInfoPage:
    inventory = login_inventory(driver)
    inventory.add_product(product_name)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    cart.checkout()
    page = CheckoutInfoPage(driver)
    page.assert_loaded()
    return page


def submit_information(driver, first: str, last: str, postal: str) -> CheckoutInfoPage:
    page = open_checkout_information(driver)
    page.fill(first=first, last=last, postal=postal)
    page.continue_checkout()
    return page
