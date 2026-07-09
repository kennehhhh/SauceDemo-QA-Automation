from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')

    def item_names(self) -> list[str]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
        return [e.text.strip() for e in elems]

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
