from __future__ import annotations

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.menu_navigation.helpers import login_inventory


MODULE = "Reset App State"


def inventory_with_two_items(driver) -> InventoryPage:
    inventory = login_inventory(driver)
    inventory.add_product(PRODUCT_A)
    inventory.add_product(PRODUCT_B)
    assert inventory.cart_count() == 2
    return inventory


def reset_from_inventory(driver) -> InventoryPage:
    inventory = inventory_with_two_items(driver)
    MenuComponent(driver).open().reset_app_state()
    return inventory


def open_cart_after_reset(driver) -> CartPage:
    inventory = reset_from_inventory(driver)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    return cart
