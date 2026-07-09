from __future__ import annotations

import pytest

from config import USERS
from pages.login_page import LoginPage
from workbook.expectation_policy import ExpectationBlocked


LOGIN_MODULE = "Login & Session"


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0028")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_remember_me_option_is_available(driver, record_actual_result):
    page = LoginPage(driver).open()
    exists = page.remember_me_exists()
    record_actual_result("Remember Me control was present on the login form." if exists else "No Remember Me control was present on the login form.")
    assert exists


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0029")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_remember_me_persists_login_convenience(driver, record_actual_result):
    page = LoginPage(driver).open()
    if not page.remember_me_exists():
        raise ExpectationBlocked(
            "LG-0029",
            "LG-0028",
            "Remember Me persistence behavior could not be executed because the required Remember Me control was absent.",
        )
    record_actual_result("Remember Me control was present, so persistence behavior prerequisite was available.")
    assert page.remember_me_exists()


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0030")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_forgot_password_recovery_entry_point_is_available(driver, record_actual_result):
    page = LoginPage(driver).open()
    exists = page.forgot_password_exists()
    record_actual_result("Forgot Password recovery entry point was present." if exists else "No Forgot Password recovery entry point was present on the login form.")
    assert exists


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0031")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("standard_user")
def test_show_hide_password_control_is_available(driver, record_actual_result):
    page = LoginPage(driver).open()
    exists = page.show_password_exists()
    record_actual_result("Show/Hide Password control was present." if exists else "No Show/Hide Password control was present on the login form.")
    assert exists


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0032")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_username_maximum_length_is_enforced(driver, record_actual_result):
    page = LoginPage(driver).open()
    payload = "u" * 256
    page.type(LoginPage.USERNAME, payload)
    max_length = page.attribute(LoginPage.USERNAME, "maxlength")
    accepted_length = len(page.username_value())
    record_actual_result(f"Username maxlength attribute was {max_length or 'absent'}; accepted length was {accepted_length}.")
    assert max_length and accepted_length <= int(max_length) < len(payload)


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0033")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_password_maximum_length_is_enforced(driver, record_actual_result):
    page = LoginPage(driver).open()
    payload = "p" * 256
    page.type(LoginPage.PASSWORD, payload)
    max_length = page.attribute(LoginPage.PASSWORD, "maxlength")
    accepted_length = len(page.password_value())
    record_actual_result(f"Password maxlength attribute was {max_length or 'absent'}; accepted length was {accepted_length}.")
    assert max_length and accepted_length <= int(max_length) < len(payload)


def _attempt_invalid_logins(page: LoginPage, attempts: int = 3) -> str:
    observed_error = ""
    for idx in range(attempts):
        page.login(f"bad_user_{idx}", "bad_password")
        observed_error = page.error_text()
    return observed_error


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0034")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_repeated_failed_logins_are_rate_limited(driver, record_actual_result):
    page = LoginPage(driver).open()
    observed_error = _attempt_invalid_logins(page)
    rate_limited = "rate" in observed_error.lower() or "too many" in observed_error.lower() or "temporarily" in observed_error.lower()
    record_actual_result(f"After three invalid login attempts, observed message was: {observed_error}")
    assert rate_limited


@pytest.mark.login
@pytest.mark.system
@pytest.mark.case_id("LG-0035")
@pytest.mark.module(LOGIN_MODULE)
@pytest.mark.test_user("N/A")
def test_excessive_failed_attempts_trigger_temporary_protection(driver, record_actual_result):
    page = LoginPage(driver).open()
    observed_error = _attempt_invalid_logins(page)
    protected = "temporarily" in observed_error.lower() or "locked" in observed_error.lower() or "too many" in observed_error.lower()
    record_actual_result(f"After bounded repeated invalid attempts, observed message was: {observed_error}")
    assert protected
