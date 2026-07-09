from __future__ import annotations

import re

import pytest

from pages.inventory_page import InventoryPage
from testdata.products import BASELINE_PRODUCT_NAMES, PRODUCT_A, PRODUCT_RED_SHIRT
from tests.product_listing.helpers import MODULE, login_inventory


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_products_heading_is_displayed(driver, record_actual_result):
    page = login_inventory(driver)
    title = page.text(InventoryPage.TITLE)
    record_actual_result(f"Products heading was displayed as: {title}")
    assert title == "Products"


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_inventory_list_is_displayed(driver, record_actual_result):
    page = login_inventory(driver)
    count = len(page.product_cards())
    record_actual_result(f"Inventory list was displayed with {count} product cards.")
    assert page.is_visible(InventoryPage.INVENTORY_LIST)
    assert count == 6


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_product_card_shows_name(driver, record_actual_result):
    page = login_inventory(driver)
    names = page.product_names()
    record_actual_result(f"All product cards showed names: {', '.join(names)}")
    assert len(names) == 6
    assert all(names)


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_product_card_shows_description(driver, record_actual_result):
    page = login_inventory(driver)
    descriptions = page.product_descriptions()
    record_actual_result(f"All {len(descriptions)} product cards showed non-empty descriptions.")
    assert len(descriptions) == 6
    assert all(descriptions)


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_product_card_shows_price(driver, record_actual_result):
    page = login_inventory(driver)
    prices = page.product_price_texts()
    record_actual_result(f"All product cards showed prices: {', '.join(prices)}")
    assert len(prices) == 6
    assert all(prices)


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_product_card_shows_image(driver, record_actual_result):
    page = login_inventory(driver)
    images = page.product_image_srcs()
    record_actual_result(f"All {len(images)} product cards showed image sources.")
    assert len(images) == 6
    assert all(images)


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_product_names_are_clickable(driver, record_actual_result):
    page = login_inventory(driver)
    page.open_product(PRODUCT_A)
    record_actual_result(f"Clicking product name opened detail page for {PRODUCT_A}.")
    assert "/inventory-item.html" in driver.current_url


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_product_images_have_controlled_click_behavior(driver, record_actual_result):
    page = login_inventory(driver)
    before_url = driver.current_url
    page.click_product_image(PRODUCT_A)
    after_url = driver.current_url
    opened_detail = "/inventory-item.html" in after_url
    stayed_listing = after_url == before_url
    record_actual_result(
        f"Clicking the {PRODUCT_A} image resulted in URL {after_url}; "
        f"{'detail opened' if opened_detail else 'listing remained stable'}."
    )
    assert opened_detail or stayed_listing


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_icon_is_visible(driver, record_actual_result):
    page = login_inventory(driver)
    record_actual_result("Shopping cart icon/link was visible on the product listing page.")
    assert page.is_visible(InventoryPage.CART_LINK)


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.parametrize(
    "case_id,product_name",
    [
        pytest.param("PL-0011", PRODUCT_A, marks=[pytest.mark.case_id("PL-0011"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PL-0011"),
        pytest.param("PL-0012", PRODUCT_RED_SHIRT, marks=[pytest.mark.case_id("PL-0012"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PL-0012"),
    ],
)
def test_representative_products_are_displayed(driver, record_actual_result, case_id: str, product_name: str):
    page = login_inventory(driver)
    names = page.product_names()
    record_actual_result(f"Product listing displayed {product_name}.")
    assert product_name in names


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_inventory_remains_stable_after_browser_refresh(driver, record_actual_result):
    page = login_inventory(driver)
    before = page.product_cards()
    driver.refresh()
    page.assert_loaded()
    after = page.product_cards()
    record_actual_result("Inventory product cards remained stable after browser refresh.")
    assert after == before


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0018")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_adding_one_product_does_not_alter_unrelated_product_data(driver, record_actual_result):
    page = login_inventory(driver)
    before = {card["name"]: card for card in page.product_cards()}
    page.add_product(PRODUCT_A)
    after = {card["name"]: card for card in page.product_cards()}
    unrelated_before = {k: v for k, v in before.items() if k != PRODUCT_A}
    unrelated_after = {k: v for k, v in after.items() if k != PRODUCT_A}
    record_actual_result(f"Adding {PRODUCT_A} did not alter unrelated product name/description/price/image data.")
    assert unrelated_after == unrelated_before


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0019")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_product_prices_use_consistent_currency_format(driver, record_actual_result):
    page = login_inventory(driver)
    prices = page.product_price_texts()
    record_actual_result(f"Displayed product prices used currency format: {', '.join(prices)}")
    assert all(re.match(r"^\$\d+\.\d{2}$", price) for price in prices)


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0020")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_no_duplicate_product_cards_are_displayed(driver, record_actual_result):
    page = login_inventory(driver)
    names = page.product_names()
    record_actual_result(f"Product listing displayed {len(names)} unique product names.")
    assert len(names) == len(set(names))
    assert set(names) == set(BASELINE_PRODUCT_NAMES)
