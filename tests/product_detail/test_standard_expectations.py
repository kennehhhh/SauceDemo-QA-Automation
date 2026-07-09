from __future__ import annotations

import pytest

from testdata.products import PRODUCT_A
from tests.product_detail.helpers import MODULE, open_detail


@pytest.mark.product_detail
@pytest.mark.system
@pytest.mark.case_id("PD-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_detail_page_exposes_product_quantity_selection_when_expected(driver, record_actual_result):
    page = open_detail(driver, PRODUCT_A)
    exists = page.quantity_control_exists()
    record_actual_result(
        "Product detail quantity control was present."
        if exists
        else "No product quantity control was present on the detail page."
    )
    assert exists
