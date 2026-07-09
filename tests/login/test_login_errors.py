from __future__ import annotations

import pytest

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


LOGIN_MODULE = "Login & Session"
INVALID_CREDENTIALS_ERROR = "Username and password do not match any user in this service"


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0020")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_login_error_message_displays_after_invalid_credentials(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.login("not_a_user", USERS["standard_user"])
    observed_error = page.error_text()
    record_actual_result(f"Invalid credentials displayed an error banner: {observed_error}")
    assert INVALID_CREDENTIALS_ERROR in observed_error
    assert page.error_visible()


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0021")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_error_close_control_dismisses_message(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.login("not_a_user", USERS["standard_user"])
    assert page.error_visible()
    page.dismiss_error()
    record_actual_result("The login error close control dismissed the error banner.")
    assert not page.error_visible()


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0022")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_successful_login_clears_prior_error_state(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.login("not_a_user", USERS["standard_user"])
    assert page.error_visible()
    page.login("standard_user", USERS["standard_user"])
    InventoryPage(driver).assert_loaded()
    record_actual_result("After a prior invalid login, valid credentials loaded Products and stale login error was gone.")
    assert "/inventory.html" in driver.current_url
