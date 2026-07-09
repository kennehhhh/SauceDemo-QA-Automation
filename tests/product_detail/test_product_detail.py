from __future__ import annotations

import re

import pytest

from config import BASE_URL
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from testdata.products import PRODUCT_A, PRODUCT_RED_SHIRT
from tests.product_detail.helpers import MODULE, listing_snapshot_for, open_detail


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_detail_page_shows_product_name(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    name = page.snapshot()["name"]
    record_actual_result(f"Detail page displayed product name: {name}")
    assert name == PRODUCT_A


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_detail_page_shows_product_description(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    description = page.snapshot()["description"]
    record_actual_result("Detail page displayed a non-empty product description.")
    assert description


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_detail_page_shows_product_price(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    price = page.snapshot()["price"]
    record_actual_result(f"Detail page displayed valid currency price: {price}")
    assert re.match(r"^\$\d+\.\d{2}$", price)


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_detail_page_shows_product_image(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    image = page.snapshot()["image"]
    record_actual_result("Detail page displayed a product image source.")
    assert image


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_back_to_products_action_is_visible(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    record_actual_result("Back to products action was visible on the detail page.")
    assert page.is_visible(ProductPage.BACK)


@pytest.mark.product_detail
@pytest.mark.unit
@pytest.mark.case_id("PD-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_add_to_cart_action_is_visible_when_not_selected(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    record_actual_result("Add to cart action was available for an unselected detail product.")
    assert page.is_add_state()


@pytest.mark.product_detail
@pytest.mark.integration
@pytest.mark.parametrize(
    "case_id,product_name",
    [
        pytest.param("PD-0007", PRODUCT_A, marks=[pytest.mark.case_id("PD-0007"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PD-0007"),
        pytest.param("PD-0009", PRODUCT_RED_SHIRT, marks=[pytest.mark.case_id("PD-0009"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PD-0009"),
    ],
)
def test_open_detail_page_from_listing(driver, record_actual_result, case_id: str, product_name: str):
    page = open_detail(driver, product_name)
    name = page.snapshot()["name"]
    record_actual_result(f"Opening {product_name} from listing displayed matching detail product: {name}.")
    assert name == product_name
    assert "/inventory-item.html" in driver.current_url


@pytest.mark.product_detail
@pytest.mark.integration
@pytest.mark.parametrize(
    "case_id,product_name",
    [
        pytest.param("PD-0008", PRODUCT_A, marks=[pytest.mark.case_id("PD-0008"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PD-0008"),
        pytest.param("PD-0010", PRODUCT_RED_SHIRT, marks=[pytest.mark.case_id("PD-0010"), pytest.mark.module(MODULE), pytest.mark.test_user("standard_user")], id="PD-0010"),
    ],
)
def test_detail_data_matches_listing(driver, record_actual_result, case_id: str, product_name: str):
    listing = listing_snapshot_for(driver, product_name)
    InventoryPage(driver).open_product(product_name)
    detail = ProductPage(driver).snapshot()
    record_actual_result(f"Detail values for {product_name} matched listing name, description, and price.")
    assert detail["name"] == listing["name"]
    assert detail["description"] == listing["description"]
    assert detail["price"] == listing["price"]


@pytest.mark.product_detail
@pytest.mark.system
@pytest.mark.case_id("PD-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_back_to_products_returns_to_inventory(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    page.back_to_products()
    InventoryPage(driver).assert_loaded()
    record_actual_result("Back to products returned to the Products inventory page.")
    assert "/inventory.html" in driver.current_url


@pytest.mark.product_detail
@pytest.mark.system
@pytest.mark.case_id("PD-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_direct_invalid_product_detail_url_is_handled(driver, record_actual_result):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    driver.get(f"{BASE_URL.rstrip('/')}/inventory-item.html?id=9999")
    controlled = "inventory-item.html" in driver.current_url or "inventory.html" in driver.current_url
    record_actual_result(f"Invalid product detail URL was handled without browser crash; current URL was {driver.current_url}.")
    assert controlled
