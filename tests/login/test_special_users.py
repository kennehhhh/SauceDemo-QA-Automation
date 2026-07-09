from __future__ import annotations

import pytest

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


LOGIN_MODULE = "Login & Session"


@pytest.mark.login
@pytest.mark.system
@pytest.mark.parametrize(
    "username,case_id,expected_access",
    [
        pytest.param("locked_out_user", "LG-0023", False, marks=[pytest.mark.case_id("LG-0023"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("locked_out_user")], id="LG-0023"),
        pytest.param("problem_user", "LG-0024", True, marks=[pytest.mark.case_id("LG-0024"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("problem_user")], id="LG-0024"),
        pytest.param("performance_glitch_user", "LG-0025", True, marks=[pytest.mark.case_id("LG-0025"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("performance_glitch_user")], id="LG-0025"),
        pytest.param("error_user", "LG-0026", True, marks=[pytest.mark.case_id("LG-0026"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("error_user")], id="LG-0026"),
        pytest.param("visual_user", "LG-0027", True, marks=[pytest.mark.case_id("LG-0027"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("visual_user")], id="LG-0027"),
    ],
)
def test_special_user_authentication_behavior(driver, record_actual_result, username: str, case_id: str, expected_access: bool):
    page = LoginPage(driver).open()
    page.login(username, USERS[username])

    if expected_access:
        InventoryPage(driver).assert_loaded()
        record_actual_result(f"{username} authenticated successfully and reached the Products inventory.")
        assert "/inventory.html" in driver.current_url
    else:
        observed_error = page.error_text()
        record_actual_result(f"{username} was blocked with message: {observed_error}")
        assert "Sorry, this user has been locked out" in observed_error
