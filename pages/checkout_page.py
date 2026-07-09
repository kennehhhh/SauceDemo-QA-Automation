from __future__ import annotations

import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue"]')
    CANCEL = (By.CSS_SELECTOR, '[data-test="cancel"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')

    def assert_loaded(self) -> None:
        assert self.text(self.TITLE) == "Checkout: Your Information"
        self.visible(self.FIRST)
        self.visible(self.LAST)
        self.visible(self.POSTAL)

    def fill(self, first: str = "Test", last: str = "User", postal: str = "1000") -> None:
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.POSTAL, postal)

    def continue_checkout(self) -> None:
        self.click(self.CONTINUE)

    def cancel(self) -> None:
        self.click(self.CANCEL)

    def field_value(self, locator) -> str:
        return self.attribute(locator, "value")

    def first_value(self) -> str:
        return self.field_value(self.FIRST)

    def last_value(self) -> str:
        return self.field_value(self.LAST)

    def postal_value(self) -> str:
        return self.field_value(self.POSTAL)

    def error_text(self) -> str:
        return self.text(self.ERROR) if self.exists(self.ERROR) else ""

    def has_error_containing(self, expected: str) -> bool:
        return expected.lower() in self.error_text().lower()


class CheckoutOverviewPage(BasePage):
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PAYMENT_INFO = (By.CSS_SELECTOR, '[data-test="payment-info-label"], [data-test="payment-info-value"]')
    SHIPPING_INFO = (By.CSS_SELECTOR, '[data-test="shipping-info-label"], [data-test="shipping-info-value"]')
    PRICE_TOTAL = (By.CSS_SELECTOR, '[data-test="total-info-label"], [data-test="subtotal-label"], [data-test="total-label"]')
    SUBTOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    TAX = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')
    CANCEL = (By.CSS_SELECTOR, '[data-test="cancel"]')

    def assert_loaded(self) -> None:
        assert self.text(self.TITLE) == "Checkout: Overview"
        self.visible(self.CART_ITEM)

    def item_names(self) -> list[str]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
        return [e.text.strip() for e in elems]

    def items(self) -> list[dict[str, str]]:
        records = []
        for item in self.elements(self.CART_ITEM):
            records.append(
                {
                    "quantity": item.find_element(By.CSS_SELECTOR, '[data-test="item-quantity"]').text.strip(),
                    "name": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text.strip(),
                    "description": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-desc"]').text.strip(),
                    "price": item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-price"]').text.strip(),
                }
            )
        return records

    def item_prices(self) -> list[float]:
        return [self._money(item["price"]) for item in self.items()]

    def subtotal(self) -> float:
        return self._money(self.text(self.SUBTOTAL))

    def tax(self) -> float:
        return self._money(self.text(self.TAX))

    def total(self) -> float:
        return self._money(self.text(self.TOTAL))

    def payment_info_visible(self) -> bool:
        return self.is_visible(self.PAYMENT_INFO)

    def shipping_info_visible(self) -> bool:
        return self.is_visible(self.SHIPPING_INFO)

    def price_total_visible(self) -> bool:
        return self.is_visible(self.PRICE_TOTAL)

    @staticmethod
    def _money(text: str) -> float:
        match = re.search(r"\$?([0-9]+(?:\.[0-9]{2})?)", text)
        if not match:
            raise AssertionError(f"No money amount found in text: {text!r}")
        return float(match.group(1))

    def finish(self) -> None:
        self.click(self.FINISH)

    def cancel(self) -> None:
        self.click(self.CANCEL)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')
    COMPLETE_TEXT = (By.CSS_SELECTOR, '[data-test="complete-text"]')
    BACK_HOME = (By.CSS_SELECTOR, '[data-test="back-to-products"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')

    def assert_complete(self) -> None:
        assert self.text(self.TITLE) == "Checkout: Complete!"
        text = self.text(self.COMPLETE_HEADER).lower()
        assert "thank you" in text

    def success_message(self) -> str:
        header = self.text(self.COMPLETE_HEADER)
        detail = self.text(self.COMPLETE_TEXT) if self.exists(self.COMPLETE_TEXT) else ""
        return " ".join(part for part in (header, detail) if part)

    def back_home(self) -> None:
        self.click(self.BACK_HOME)

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def cart_count(self) -> int:
        elems = self.driver.find_elements(*self.CART_BADGE)
        return int(elems[0].text) if elems else 0
