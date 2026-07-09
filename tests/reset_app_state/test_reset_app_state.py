from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_A, PRODUCT_B
from tests.reset_app_state.helpers import (
    MODULE,
    inventory_with_two_items,
    login_inventory,
    open_cart_after_reset,
    reset_from_inventory,
)


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_app_state_option_is_visible(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    visible = menu.has_reset_app_state()
    record_actual_result("Reset App State option was visible." if visible else "Reset App State option was not visible.")
    assert visible


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_clears_cart_badge(driver, record_actual_result):
    inventory = reset_from_inventory(driver)
    count = inventory.cart_count()
    record_actual_result(f"Cart badge count after Reset App State was {count}.")
    assert count == 0


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_clears_cart_contents(driver, record_actual_result):
    cart = open_cart_after_reset(driver)
    names = cart.item_names()
    record_actual_result(f"Cart contents after Reset App State were: {', '.join(names) or '<none>'}.")
    assert names == []


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_changes_remove_buttons_back_to_add_to_cart(driver, record_actual_result):
    inventory = reset_from_inventory(driver)
    states = {PRODUCT_A: inventory.button_state_for(PRODUCT_A), PRODUCT_B: inventory.button_state_for(PRODUCT_B)}
    record_actual_result(f"Product controls after reset were: {states}.")
    assert states == {PRODUCT_A: "Add to cart", PRODUCT_B: "Add to cart"}


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_can_be_invoked_repeatedly_without_error(driver, record_actual_result):
    inventory = inventory_with_two_items(driver)
    menu = MenuComponent(driver).open()
    menu.reset_app_state()
    menu.reset_app_state()
    count = inventory.cart_count()
    record_actual_result(f"After invoking Reset App State twice, cart badge count was {count}.")
    assert count == 0
    assert inventory.button_state_for(PRODUCT_A) == "Add to cart"


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_does_not_log_user_out(driver, record_actual_result):
    inventory = reset_from_inventory(driver)
    InventoryPage(driver).assert_loaded()
    record_actual_result(f"After Reset App State, current URL remained authenticated: {driver.current_url}.")
    assert "inventory.html" in driver.current_url
    assert inventory.is_visible(InventoryPage.TITLE)


@pytest.mark.reset_app_state
@pytest.mark.system
@pytest.mark.case_id("RS-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_effect_persists_across_navigation(driver, record_actual_result):
    cart = open_cart_after_reset(driver)
    cart.continue_shopping()
    inventory = InventoryPage(driver)
    inventory.assert_loaded()
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    names = cart.item_names()
    record_actual_result(f"After reset and navigation Products -> Cart, cart contents were: {', '.join(names) or '<none>'}.")
    assert names == []
