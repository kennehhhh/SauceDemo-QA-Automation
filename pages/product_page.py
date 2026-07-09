from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ADD = (By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]')
    CART = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    def assert_product(self, expected_name: str) -> None:
        assert self.text(self.NAME) == expected_name

    def add_to_cart(self) -> None:
        self.click(self.ADD)

    def open_cart(self) -> None:
        self.click(self.CART)
