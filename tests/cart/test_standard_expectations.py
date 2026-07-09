from __future__ import annotations

import pytest

from testdata.products import PRODUCT_A
from tests.cart.helpers import MODULE, open_cart_with_products


@pytest.mark.cart
@pytest.mark.system
@pytest.mark.case_id("CT-0020")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_supports_quantity_increase_when_expected(driver, record_actual_result):
    cart = open_cart_with_products(driver, PRODUCT_A)
    exists = cart.quantity_control_exists()
    record_actual_result(
        "Cart quantity increase control was present."
        if exists
        else "No cart quantity increase control was present for the cart item."
    )
    assert exists
