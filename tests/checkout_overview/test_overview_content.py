from __future__ import annotations

import pytest

from pages.checkout_page import CheckoutOverviewPage
from testdata.products import PRODUCT_A
from tests.checkout_overview.helpers import MODULE, open_checkout_overview


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_overview_heading_is_displayed(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    heading = page.text(CheckoutOverviewPage.TITLE)
    record_actual_result(f"Overview heading was visible as {heading!r}.")
    assert heading == "Checkout: Overview"


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_selected_item_is_displayed(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    names = page.item_names()
    record_actual_result(f"Overview displayed selected items: {', '.join(names)}.")
    assert PRODUCT_A in names


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_selected_item_name_is_visible(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    item = page.items()[0]
    record_actual_result(f"Overview item name was {item['name']!r}.")
    assert item["name"] == PRODUCT_A


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_selected_item_description_is_visible(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    description = page.items()[0]["description"]
    record_actual_result(f"Overview item description was {description!r}.")
    assert description


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_selected_item_price_is_visible(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    price = page.items()[0]["price"]
    record_actual_result(f"Overview item price was {price!r}.")
    assert price.startswith("$")


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_payment_information_section_is_displayed(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    visible = page.payment_info_visible()
    record_actual_result("Payment Information section was visible." if visible else "Payment Information section was not visible.")
    assert visible


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_shipping_information_section_is_displayed(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    visible = page.shipping_info_visible()
    record_actual_result("Shipping Information section was visible." if visible else "Shipping Information section was not visible.")
    assert visible


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_price_total_section_is_displayed(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    visible = page.price_total_visible()
    record_actual_result("Price Total section was visible." if visible else "Price Total section was not visible.")
    assert visible


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_finish_button_is_visible(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    visible = page.is_visible(CheckoutOverviewPage.FINISH)
    record_actual_result("Finish action was visible." if visible else "Finish action was not visible.")
    assert visible


@pytest.mark.checkout_overview
@pytest.mark.unit
@pytest.mark.case_id("CO-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cancel_button_is_visible(driver, record_actual_result):
    page = open_checkout_overview(driver, PRODUCT_A)
    visible = page.is_visible(CheckoutOverviewPage.CANCEL)
    record_actual_result("Cancel action was visible." if visible else "Cancel action was not visible.")
    assert visible
