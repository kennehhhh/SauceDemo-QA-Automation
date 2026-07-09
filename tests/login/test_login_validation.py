from __future__ import annotations

import pytest

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


LOGIN_MODULE = "Login & Session"


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.parametrize(
    "username,password,expected_error,actual_result",
    [
        pytest.param(
            "",
            "",
            "Username is required",
            "Login was rejected and the username-required error message was displayed for empty credentials.",
            marks=[
                pytest.mark.case_id("LG-0009"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0009",
        ),
        pytest.param(
            "",
            USERS["standard_user"],
            "Username is required",
            "Login was rejected and the username-required error message was displayed when password was populated.",
            marks=[
                pytest.mark.case_id("LG-0010"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0010",
        ),
        pytest.param(
            "standard_user",
            "",
            "Password is required",
            "Login was rejected and the password-required error message was displayed when username was populated.",
            marks=[
                pytest.mark.case_id("LG-0011"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0011",
        ),
        pytest.param(
            "not_a_user",
            USERS["standard_user"],
            "Username and password do not match any user in this service",
            "Login was rejected with invalid-credentials feedback for an unknown username.",
            marks=[
                pytest.mark.case_id("LG-0012"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0012",
        ),
        pytest.param(
            "standard_user",
            "wrong_password",
            "Username and password do not match any user in this service",
            "Login was rejected with invalid-credentials feedback for a wrong password.",
            marks=[
                pytest.mark.case_id("LG-0013"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0013",
        ),
        pytest.param(
            "bad_user",
            "bad_pass",
            "Username and password do not match any user in this service",
            "Login was rejected with invalid-credentials feedback for invalid username and password.",
            marks=[
                pytest.mark.case_id("LG-0014"),
                pytest.mark.module(LOGIN_MODULE),
                pytest.mark.test_user("N/A"),
            ],
            id="LG-0014",
        ),
    ],
)
def test_login_rejects_invalid_credentials(
    driver,
    record_actual_result,
    username: str,
    password: str,
    expected_error: str,
    actual_result: str,
):
    page = LoginPage(driver).open()
    page.login(username, password)

    observed_error = page.error_text()
    assert expected_error in observed_error
    assert "saucedemo.com" in driver.current_url
    record_actual_result(f"{actual_result} Observed message: {observed_error}")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0015")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_standard_user_credentials_are_accepted(driver, record_actual_result):
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    InventoryPage(driver).assert_loaded()
    record_actual_result("standard_user logged in successfully and was redirected to the Products inventory.")


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0023")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("locked_out_user")
def test_locked_out_user_is_rejected(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.login("locked_out_user", USERS["locked_out_user"])

    observed_error = page.error_text()
    assert "Sorry, this user has been locked out" in observed_error
    record_actual_result(f"locked_out_user was rejected with the locked-out account message: {observed_error}")
