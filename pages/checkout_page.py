from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue"]')
    CANCEL = (By.CSS_SELECTOR, '[data-test="cancel"]')

    def fill(self, first: str = "Test", last: str = "User", postal: str = "1000") -> None:
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.POSTAL, postal)

    def continue_checkout(self) -> None:
        self.click(self.CONTINUE)

    def cancel(self) -> None:
        self.click(self.CANCEL)


class CheckoutOverviewPage(BasePage):
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')
    CANCEL = (By.CSS_SELECTOR, '[data-test="cancel"]')

    def item_names(self) -> list[str]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
        return [e.text.strip() for e in elems]

    def finish(self) -> None:
        self.click(self.FINISH)

    def cancel(self) -> None:
        self.click(self.CANCEL)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def assert_complete(self) -> None:
        text = self.text(self.COMPLETE_HEADER).lower()
        assert "thank you" in text
