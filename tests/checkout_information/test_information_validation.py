from __future__ import annotations

import pytest

from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage
from tests.checkout_information.helpers import (
    MODULE,
    VALID_FIRST,
    VALID_LAST,
    VALID_POSTAL,
    open_checkout_information,
)


LONG_FIRST = "A" * 256
LONG_POSTAL = "9" * 256


def _submit(page: CheckoutInfoPage, first: str, last: str, postal: str) -> str:
    page.fill(first=first, last=last, postal=postal)
    page.continue_checkout()
    return page.error_text()


def _assert_rejected_at_information(driver, page: CheckoutInfoPage, expected_field: str) -> str:
    error = page.error_text()
    assert expected_field.lower() in error.lower()
    assert "checkout-step-one.html" in driver.current_url
    return error


def _record_validation_probe(record_actual_result, driver, page: CheckoutInfoPage, label: str) -> None:
    error = page.error_text()
    location = "overview" if "checkout-step-two.html" in driver.current_url else "checkout information"
    record_actual_result(f"{label}: current page was {location}; validation message was {error or '<none>'}.")


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_all_information_fields_empty_are_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first="", last="", postal="")
    error = _assert_rejected_at_information(driver, page, "First Name")
    record_actual_result(f"All empty fields were blocked with validation message: {error}.")


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_empty_with_names_filled_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal="")
    error = _assert_rejected_at_information(driver, page, "Postal Code")
    record_actual_result(f"Missing Postal Code was blocked with validation message: {error}.")


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_last_name_empty_with_first_and_postal_filled_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last="", postal=VALID_POSTAL)
    error = _assert_rejected_at_information(driver, page, "Last Name")
    record_actual_result(f"Missing Last Name was blocked with validation message: {error}.")


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_first_name_empty_with_last_and_postal_filled_is_rejected(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first="", last=VALID_LAST, postal=VALID_POSTAL)
    error = _assert_rejected_at_information(driver, page, "First Name")
    record_actual_result(f"Missing First Name was blocked with validation message: {error}.")


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0016")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_all_information_fields_valid_advance_to_overview(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal=VALID_POSTAL)
    CheckoutOverviewPage(driver).assert_loaded()
    record_actual_result("Valid checkout information advanced to Checkout Overview.")


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0017")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_first_name_whitespace_only_is_rejected_by_policy(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first="   ", last=VALID_LAST, postal=VALID_POSTAL)
    _record_validation_probe(record_actual_result, driver, page, "First Name whitespace-only probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0018")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_first_name_very_long_input_is_rejected_by_policy(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=LONG_FIRST, last=VALID_LAST, postal=VALID_POSTAL)
    _record_validation_probe(record_actual_result, driver, page, "First Name very-long-input probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0019")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_last_name_apostrophe_input_is_handled(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last="O'Neil", postal=VALID_POSTAL)
    record_actual_result(
        "Apostrophe last name advanced to Checkout Overview."
        if "checkout-step-two.html" in driver.current_url
        else f"Apostrophe last name remained on checkout information with message: {page.error_text() or '<none>'}."
    )
    assert "checkout-step-two.html" in driver.current_url or page.error_text()


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0020")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_whitespace_only_is_rejected_by_policy(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal="   ")
    _record_validation_probe(record_actual_result, driver, page, "Postal Code whitespace-only probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0021")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_alphabetic_input_is_rejected_by_policy(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal="ABC")
    _record_validation_probe(record_actual_result, driver, page, "Postal Code alphabetic-input probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.unit
@pytest.mark.case_id("CI-0022")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_very_long_input_is_rejected_by_policy(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal=LONG_POSTAL)
    _record_validation_probe(record_actual_result, driver, page, "Postal Code very-long-input probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0023")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_maximum_length_is_enforced(driver, record_actual_result):
    page = open_checkout_information(driver)
    page.type(CheckoutInfoPage.POSTAL, LONG_POSTAL)
    max_length = page.attribute(CheckoutInfoPage.POSTAL, "maxlength")
    accepted_length = len(page.postal_value())
    page.fill(first=VALID_FIRST, last=VALID_LAST, postal=page.postal_value())
    page.continue_checkout()
    record_actual_result(
        f"Postal Code maxlength attribute was {max_length or 'absent'}; accepted length was {accepted_length}; "
        f"validation message was {page.error_text() or '<none>'}."
    )
    assert max_length and accepted_length <= int(max_length) < len(LONG_POSTAL)


@pytest.mark.checkout_information
@pytest.mark.system
@pytest.mark.case_id("CI-0024")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_postal_code_format_validation_is_enforced(driver, record_actual_result):
    page = open_checkout_information(driver)
    _submit(page, first=VALID_FIRST, last=VALID_LAST, postal="ABC")
    _record_validation_probe(record_actual_result, driver, page, "Postal Code format-validation probe")
    assert page.error_text()
    assert "checkout-step-one.html" in driver.current_url
