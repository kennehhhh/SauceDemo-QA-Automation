from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    IMAGE = (By.CSS_SELECTOR, '[data-test="item-sauce-labs-backpack-img"], .inventory_details_img')
    ADD = (By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]')
    REMOVE = (By.CSS_SELECTOR, 'button[data-test^="remove"]')
    BACK = (By.CSS_SELECTOR, '[data-test="back-to-products"]')
    CART = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    QUANTITY = (
        By.XPATH,
        '//*[self::input or self::button or self::select][contains(translate(@data-test, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity") '
        'or contains(translate(@name, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity") '
        'or contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity")]',
    )

    def assert_product(self, expected_name: str) -> None:
        assert self.text(self.NAME) == expected_name

    def add_to_cart(self) -> None:
        self.click(self.ADD)

    def remove_from_cart(self) -> None:
        self.click(self.REMOVE)

    def open_cart(self) -> None:
        self.click(self.CART)

    def back_to_products(self) -> None:
        self.click(self.BACK)

    def snapshot(self) -> dict[str, str]:
        return {
            "name": self.text(self.NAME),
            "description": self.text(self.DESCRIPTION),
            "price": self.text(self.PRICE),
            "image": self.attribute(self.IMAGE, "src"),
        }

    def is_add_state(self) -> bool:
        return self.exists(self.ADD)

    def is_remove_state(self) -> bool:
        return self.exists(self.REMOVE)

    def cart_count(self) -> int:
        elems = self.driver.find_elements(*self.CART_BADGE)
        return int(elems[0].text) if elems else 0

    def quantity_control_exists(self) -> bool:
        return self.exists(self.QUANTITY)
