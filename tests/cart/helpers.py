from __future__ import annotations

from config import USERS
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


MODULE = "Cart"


def login_inventory(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def open_cart_with_products(driver, *product_names: str) -> CartPage:
    inventory = login_inventory(driver)
    for product_name in product_names:
        inventory.add_product(product_name)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    return cart


def open_empty_cart(driver) -> CartPage:
    inventory = login_inventory(driver)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    return cart
