from __future__ import annotations

import pytest

from config import USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


LOGIN_MODULE = "Login & Session"
INVALID_CREDENTIALS_ERROR = "Username and password do not match any user in this service"


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0001")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_username_field_is_visible(driver, record_actual_result):
    page = LoginPage(driver).open()
    assert page.username_visible()
    record_actual_result("Username input was visible on the login form.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0002")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_password_field_is_visible(driver, record_actual_result):
    page = LoginPage(driver).open()
    assert page.password_visible()
    record_actual_result("Password input was visible on the login form.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0003")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_login_button_is_visible(driver, record_actual_result):
    page = LoginPage(driver).open()
    assert page.login_button_visible()
    record_actual_result("Login button was visible on the login form.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0004")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_username_field_is_enabled(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.type(LoginPage.USERNAME, "standard_user")
    assert page.is_username_enabled()
    assert page.username_value() == "standard_user"
    record_actual_result("Username input was enabled and accepted typed text.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0005")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_password_field_is_enabled(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.type(LoginPage.PASSWORD, USERS["standard_user"])
    assert page.is_password_enabled()
    assert page.password_value() == USERS["standard_user"]
    record_actual_result("Password input was enabled and accepted typed text.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0006")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_password_characters_are_masked(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.type(LoginPage.PASSWORD, USERS["standard_user"])
    assert page.password_input_type() == "password"
    record_actual_result("Password input used type=password after entering the test password.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0007")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_enter_key_submits_valid_credentials(driver, record_actual_result):
    LoginPage(driver).open().submit_with_enter("standard_user", USERS["standard_user"])
    InventoryPage(driver).assert_loaded()
    assert "/inventory.html" in driver.current_url
    record_actual_result("Pressing Enter from the password field submitted valid credentials and loaded Products.")


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0008")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_enter_key_with_empty_fields_triggers_validation(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.submit_with_enter("", "")
    observed_error = page.error_text()
    record_actual_result(f"Pressing Enter with empty fields produced message: {observed_error}")
    assert "Username is required" in observed_error
    assert "/inventory.html" not in driver.current_url


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.parametrize(
    "username,password,expected_error,actual_result",
    [
        pytest.param("", "", "Username is required", "Login was rejected for empty credentials.", marks=[pytest.mark.case_id("LG-0009"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0009"),
        pytest.param("", USERS["standard_user"], "Username is required", "Login was rejected when username was empty and password was populated.", marks=[pytest.mark.case_id("LG-0010"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0010"),
        pytest.param("standard_user", "", "Password is required", "Login was rejected when username was populated and password was empty.", marks=[pytest.mark.case_id("LG-0011"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0011"),
        pytest.param("not_a_user", USERS["standard_user"], INVALID_CREDENTIALS_ERROR, "Login was rejected for an unknown username.", marks=[pytest.mark.case_id("LG-0012"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0012"),
        pytest.param("standard_user", "wrong_password", INVALID_CREDENTIALS_ERROR, "Login was rejected for an invalid password.", marks=[pytest.mark.case_id("LG-0013"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0013"),
        pytest.param("bad_user", "bad_pass", INVALID_CREDENTIALS_ERROR, "Login was rejected for invalid username and password.", marks=[pytest.mark.case_id("LG-0014"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0014"),
        pytest.param("   ", USERS["standard_user"], INVALID_CREDENTIALS_ERROR, "Login was rejected for a whitespace-only username.", marks=[pytest.mark.case_id("LG-0016"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0016"),
        pytest.param("standard_user", "    ", INVALID_CREDENTIALS_ERROR, "Login was rejected for a whitespace-only password.", marks=[pytest.mark.case_id("LG-0017"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0017"),
        pytest.param("' OR '1'='1", USERS["standard_user"], INVALID_CREDENTIALS_ERROR, "Login safely rejected a SQL injection-like username.", marks=[pytest.mark.case_id("LG-0018"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0018"),
        pytest.param("<script>alert(1)</script>", USERS["standard_user"], INVALID_CREDENTIALS_ERROR, "Login safely rejected an XSS-like username.", marks=[pytest.mark.case_id("LG-0019"), pytest.mark.module(LOGIN_MODULE), pytest.mark.test_user("N/A")], id="LG-0019"),
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
    record_actual_result(f"{actual_result} Observed message: {observed_error}")
    assert expected_error in observed_error
    assert "/inventory.html" not in driver.current_url


@pytest.mark.login
@pytest.mark.unit
@pytest.mark.case_id("LG-0015")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_standard_user_credentials_are_accepted(driver, record_actual_result):
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    InventoryPage(driver).assert_loaded()
    assert "/inventory.html" in driver.current_url
    record_actual_result("standard_user logged in successfully and was redirected to /inventory.html Products.")
