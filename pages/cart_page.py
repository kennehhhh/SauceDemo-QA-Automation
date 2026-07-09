from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_LIST = (By.CSS_SELECTOR, '[data-test="cart-list"]')
    CART_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')
    QUANTITY_CONTROL = (
        By.XPATH,
        '//*[self::input or self::button or self::select][contains(translate(@data-test, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity") '
        'or contains(translate(@name, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity") '
        'or contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "quantity")]',
    )

    def assert_loaded(self) -> None:
        assert self.text(self.TITLE) == "Your Cart"

    def item_names(self) -> list[str]:
        cart_list = self.present(self.CART_LIST)
        elems = cart_list.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
        return [e.text.strip() for e in elems]

    def items(self) -> list[dict[str, str]]:
        records = []
        cart_list = self.present(self.CART_LIST)
        for item in cart_list.find_elements(*self.CART_ITEM):
            records.append(
                {
                    "quantity": item.find_element(By.CSS_SELECTOR, '[data-test="item-quantity"]').text.strip(),
                    "name": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text.strip(),
                    "description": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-desc"]').text.strip(),
                    "price": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-price"]').text.strip(),
                    "remove": item.find_element(By.CSS_SELECTOR, 'button[data-test^="remove"]').text.strip(),
                }
            )
        return records

    def item_by_name(self, product_name: str) -> dict[str, str]:
        for item in self.items():
            if item["name"] == product_name:
                return item
        raise AssertionError(f"Cart item not found: {product_name}")

    def remove_product(self, product_name: str) -> None:
        item = self.driver.find_element(
            By.XPATH,
            f'//div[@data-test="inventory-item" and .//div[@data-test="inventory-item-name" and normalize-space()="{product_name}"]]'
        )
        item.find_element(By.CSS_SELECTOR, 'button[data-test^="remove"]').click()

    def checkout(self) -> None:
        self.click(self.CHECKOUT)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE)

    def cart_count(self) -> int:
        elems = self.driver.find_elements(*self.CART_BADGE)
        return int(elems[0].text) if elems else 0

    def is_empty(self) -> bool:
        return not self.item_names()

    def quantity_control_exists(self) -> bool:
        return self.exists(self.QUANTITY_CONTROL)
