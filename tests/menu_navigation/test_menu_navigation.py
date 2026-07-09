from __future__ import annotations

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_A
from tests.menu_navigation.helpers import MODULE, login_inventory


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_burger_menu_button_is_visible(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver)
    visible = menu.is_visible(MenuComponent.OPEN)
    record_actual_result("Burger menu control was visible." if visible else "Burger menu control was not visible.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_burger_menu_opens(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    record_actual_result("Side menu opened." if menu.is_open() else "Side menu did not open.")
    assert menu.is_open()


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_close_menu_control_is_visible_when_menu_open(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    visible = menu.is_visible(MenuComponent.CLOSE)
    record_actual_result("Close menu action was visible." if visible else "Close menu action was not visible.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_close_menu_control_closes_menu(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    menu.close()
    record_actual_result("Side menu closed after clicking close.")
    assert not menu.is_open()


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_all_items_menu_item_is_available(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    visible = menu.has_all_items()
    record_actual_result("All Items menu option was visible." if visible else "All Items menu option was not visible.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.integration
@pytest.mark.case_id("MN-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_all_items_menu_action_works(driver, record_actual_result):
    inventory = login_inventory(driver)
    inventory.open_product(PRODUCT_A)
    MenuComponent(driver).open().all_items()
    InventoryPage(driver).assert_loaded()
    record_actual_result("All Items returned to the Products inventory page.")


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_about_menu_item_is_available(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    visible = menu.has_about()
    record_actual_result("About menu option was visible." if visible else "About menu option was not visible.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.integration
@pytest.mark.case_id("MN-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_about_menu_action_works(driver, record_actual_result):
    login_inventory(driver)
    MenuComponent(driver).open().about()
    record_actual_result(f"About menu navigated to URL: {driver.current_url}.")
    assert "saucelabs.com" in driver.current_url.lower()


@pytest.mark.menu_navigation
@pytest.mark.unit
@pytest.mark.case_id("MN-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_logout_menu_item_is_available(driver, record_actual_result):
    login_inventory(driver)
    menu = MenuComponent(driver).open()
    visible = menu.has_logout()
    record_actual_result("Logout menu option was visible." if visible else "Logout menu option was not visible.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.integration
@pytest.mark.case_id("MN-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_logout_menu_action_works(driver, record_actual_result):
    login_inventory(driver)
    MenuComponent(driver).open().logout()
    visible = LoginPage(driver).is_visible(LoginPage.LOGIN)
    record_actual_result("Logout returned to the login page." if visible else "Logout did not return to the login page.")
    assert visible


@pytest.mark.menu_navigation
@pytest.mark.integration
@pytest.mark.case_id("MN-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_reset_app_state_menu_action_works(driver, record_actual_result):
    inventory = login_inventory(driver)
    inventory.add_product(PRODUCT_A)
    assert inventory.cart_count() == 1
    MenuComponent(driver).open().reset_app_state()
    record_actual_result(
        f"After Reset App State, cart badge count was {inventory.cart_count()} and {PRODUCT_A!r} button text was "
        f"{inventory.button_state_for(PRODUCT_A)!r}."
    )
    assert inventory.cart_count() == 0
    assert inventory.button_state_for(PRODUCT_A).lower() == "add to cart"
