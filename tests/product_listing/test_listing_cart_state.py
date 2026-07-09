from __future__ import annotations

import pytest

from testdata.products import PRODUCT_A, PRODUCT_B
from tests.product_listing.helpers import MODULE, login_inventory


@pytest.mark.product_listing
@pytest.mark.unit
@pytest.mark.case_id("PL-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_each_product_card_shows_add_to_cart_action_when_not_selected(driver, record_actual_result):
    page = login_inventory(driver)
    states = {card["name"]: card["button"] for card in page.product_cards()}
    record_actual_result("Every unselected product card showed an Add to cart action.")
    assert all(state == "Add to cart" for state in states.values())


@pytest.mark.product_listing
@pytest.mark.integration
@pytest.mark.case_id("PL-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_add_backpack_from_listing_updates_control_and_badge(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    state = page.button_state_for(PRODUCT_A)
    badge = page.cart_count()
    record_actual_result(f"Adding {PRODUCT_A} changed its control to {state} and cart badge to {badge}.")
    assert state == "Remove"
    assert badge == 1


@pytest.mark.product_listing
@pytest.mark.integration
@pytest.mark.case_id("PL-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_remove_backpack_from_listing_updates_control_and_badge(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    page.remove_product(PRODUCT_A)
    state = page.button_state_for(PRODUCT_A)
    badge = page.cart_count()
    record_actual_result(f"Removing {PRODUCT_A} changed its control to {state} and cleared cart badge to {badge}.")
    assert state == "Add to cart"
    assert badge == 0


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0016")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_badge_reflects_number_of_distinct_added_products(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    page.add_product(PRODUCT_B)
    badge = page.cart_count()
    record_actual_result(f"Cart badge reflected two distinct added products with value {badge}.")
    assert badge == 2


@pytest.mark.product_listing
@pytest.mark.system
@pytest.mark.case_id("PL-0017")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_badge_disappears_when_cart_becomes_empty(driver, record_actual_result):
    page = login_inventory(driver)
    page.add_product(PRODUCT_A)
    page.remove_product(PRODUCT_A)
    badge = page.cart_count()
    record_actual_result(f"Cart badge disappeared after cart became empty; observed count helper returned {badge}.")
    assert badge == 0
