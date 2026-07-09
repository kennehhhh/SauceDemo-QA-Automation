from __future__ import annotations

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


MODULE = "Product Listing"


def login_inventory(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page
