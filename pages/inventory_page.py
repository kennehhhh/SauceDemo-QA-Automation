from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    SORT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')

    def assert_loaded(self) -> None:
        assert self.text(self.TITLE) == "Products"

    @staticmethod
    def _slug(name: str) -> str:
        return (
            name.lower()
            .replace(".", "")
            .replace("()", "")
            .replace(" ", "-")
        )

    def add_product(self, product_name: str) -> None:
        slug = self._slug(product_name)
        self.click((By.CSS_SELECTOR, f'[data-test="add-to-cart-{slug}"]'))

    def remove_product(self, product_name: str) -> None:
        slug = self._slug(product_name)
        self.click((By.CSS_SELECTOR, f'[data-test="remove-{slug}"]'))

    def open_product(self, product_name: str) -> None:
        self.click((By.XPATH, f'//div[@data-test="inventory-item-name" and normalize-space()="{product_name}"]'))

    def cart_count(self) -> int:
        elems = self.driver.find_elements(*self.CART_BADGE)
        return int(elems[0].text) if elems else 0

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def sort_by_value(self, value: str) -> None:
        Select(self.visible(self.SORT)).select_by_value(value)

    def product_names(self) -> list[str]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
        return [e.text.strip() for e in elems]

    def product_prices(self) -> list[float]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
        return [float(e.text.replace("$", "").strip()) for e in elems]

    def logout(self) -> None:
        self.click(self.MENU)
        self.click(self.LOGOUT)
