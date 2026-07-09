from __future__ import annotations

import pytest

from config import BASE_URL, USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent


LOGIN_MODULE = "Login & Session"


def login_standard(driver):
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    InventoryPage(driver).assert_loaded()


def logout(driver):
    MenuComponent(driver).open().logout()
    LoginPage(driver).visible(LoginPage.USERNAME)


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0036")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_logout_option_is_available_after_login(driver, record_actual_result):
    login_standard(driver)
    menu = MenuComponent(driver).open()
    record_actual_result("Logout option was visible in the menu after standard_user logged in.")
    assert menu.has_logout()


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0037")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_logout_returns_user_to_login_page(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    record_actual_result("Logout returned standard_user to the login page.")
    assert LoginPage(driver).username_visible()
    assert "saucedemo.com" in driver.current_url


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0038")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_browser_back_after_logout_does_not_restore_authenticated_state(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    driver.back()
    page = LoginPage(driver)
    if "/inventory.html" in driver.current_url:
        page.visible(LoginPage.ERROR)
    record_actual_result("Browser Back after logout did not restore a usable authenticated inventory session.")
    assert "/inventory.html" not in driver.current_url or page.error_visible()


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0039")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_direct_inventory_url_after_logout_is_blocked(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    driver.get(f"{BASE_URL.rstrip('/')}/inventory.html")
    page = LoginPage(driver)
    observed_error = page.error_text()
    record_actual_result(f"Direct /inventory.html access after logout was blocked with message: {observed_error}")
    assert "You can only access '/inventory.html' when you are logged in" in observed_error
