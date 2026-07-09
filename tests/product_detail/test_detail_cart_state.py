from __future__ import annotations

import pytest

from testdata.products import PRODUCT_A
from tests.product_detail.helpers import MODULE, open_detail


@pytest.mark.product_detail
@pytest.mark.system
@pytest.mark.case_id("PD-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_add_product_from_detail_updates_cart_badge(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    page.add_to_cart()
    record_actual_result(f"Adding {PRODUCT_A} from detail changed action to Remove and cart badge to {page.cart_count()}.")
    assert page.is_remove_state()
    assert page.cart_count() == 1


@pytest.mark.product_detail
@pytest.mark.system
@pytest.mark.case_id("PD-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_remove_product_from_detail_updates_cart_badge(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    page.add_to_cart()
    page.remove_from_cart()
    record_actual_result(f"Removing {PRODUCT_A} from detail changed action to Add to cart and cart badge to {page.cart_count()}.")
    assert page.is_add_state()
    assert page.cart_count() == 0
