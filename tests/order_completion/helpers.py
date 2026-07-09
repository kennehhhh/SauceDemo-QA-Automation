from __future__ import annotations

from pages.checkout_page import CheckoutCompletePage
from testdata.products import PRODUCT_A
from tests.checkout_overview.helpers import open_checkout_overview


MODULE = "Order Completion"


def complete_order(driver, *product_names: str) -> CheckoutCompletePage:
    overview = open_checkout_overview(driver, *(product_names or (PRODUCT_A,)))
    overview.finish()
    page = CheckoutCompletePage(driver)
    page.assert_complete()
    return page
