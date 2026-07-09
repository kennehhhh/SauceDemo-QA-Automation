from __future__ import annotations

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


MODULE = "Product Detail"


def open_detail(driver, product_name: str) -> ProductPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    inventory = InventoryPage(driver)
    inventory.assert_loaded()
    inventory.open_product(product_name)
    return ProductPage(driver)


def listing_snapshot_for(driver, product_name: str) -> dict[str, str]:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    inventory = InventoryPage(driver)
    inventory.assert_loaded()
    for card in inventory.product_cards():
        if card["name"] == product_name:
            return card
    raise AssertionError(f"Product not found on listing: {product_name}")
