from __future__ import annotations

import pytest

from pages.checkout_page import CheckoutInfoPage
from tests.checkout_information.helpers import (
    MODULE,
    VALID_FIRST,
    VALID_LAST,
    VALID_POSTAL,
    open_checkout_information,
)


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_first_name_field_is_visible(driver, record_actual_result):
    page = open_checkout_information(driver)
    visible = page.is_visible(CheckoutInfoPage.FIRST)
    record_actual_result("First Name field was visible." if visible else "First Name field was not visible.")
    assert visible


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_first_name_field_accepts_input(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.type(CheckoutInfoPage.FIRST, VALID_FIRST)
    record_actual_result(f"First Name field value was {page.first_value()!r}.")
    assert page.first_value() == VALID_FIRST


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_missing_first_name_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.fill(first="", last=VALID_LAST, postal=VALID_POSTAL)
    page.continue_checkout()
    error = page.error_text()
    record_actual_result(f"Observed checkout information validation message: {error or '<none>'}.")
    assert page.has_error_containing("First Name")
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_last_name_field_is_visible(driver, record_actual_result):
    page = open_checkout_information(driver)
    visible = page.is_visible(CheckoutInfoPage.LAST)
    record_actual_result("Last Name field was visible." if visible else "Last Name field was not visible.")
    assert visible


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_last_name_field_accepts_input(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.type(CheckoutInfoPage.LAST, VALID_LAST)
    record_actual_result(f"Last Name field value was {page.last_value()!r}.")
    assert page.last_value() == VALID_LAST


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_missing_last_name_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.fill(first=VALID_FIRST, last="", postal=VALID_POSTAL)
    page.continue_checkout()
    error = page.error_text()
    record_actual_result(f"Observed checkout information validation message: {error or '<none>'}.")
    assert page.has_error_containing("Last Name")
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_field_is_visible(driver, record_actual_result):
    page = open_checkout_information(driver)
    visible = page.is_visible(CheckoutInfoPage.POSTAL)
    record_actual_result("Postal Code field was visible." if visible else "Postal Code field was not visible.")
    assert visible


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_field_accepts_input(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.type(CheckoutInfoPage.POSTAL, VALID_POSTAL)
    record_actual_result(f"Postal Code field value was {page.postal_value()!r}.")
    assert page.postal_value() == VALID_POSTAL


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_missing_postal_code_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.fill(first=VALID_FIRST, last=VALID_LAST, postal="")
    page.continue_checkout()
    error = page.error_text()
    record_actual_result(f"Observed checkout information validation message: {error or '<none>'}.")
    assert page.has_error_containing("Postal Code")
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_continue_button_is_visible(driver, record_actual_result):
    page = open_checkout_information(driver)
    visible = page.is_visible(CheckoutInfoPage.CONTINUE)
    record_actual_result("Continue action was visible." if visible else "Continue action was not visible.")
    assert visible


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cancel_button_is_visible(driver, record_actual_result):
    page = open_checkout_information(driver)
    visible = page.is_visible(CheckoutInfoPage.CANCEL)
    record_actual_result("Cancel action was visible." if visible else "Cancel action was not visible.")
    assert visible
