from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MenuComponent(BasePage):
    OPEN = (By.ID, "react-burger-menu-btn")
    CLOSE = (By.ID, "react-burger-cross-btn")
    ALL_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-sidebar-link"]')
    ABOUT = (By.CSS_SELECTOR, '[data-test="about-sidebar-link"]')
    LOGOUT = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')
    RESET_APP_STATE = (By.CSS_SELECTOR, '[data-test="reset-sidebar-link"]')
    MENU_WRAP = (By.CSS_SELECTOR, ".bm-menu-wrap")

    def open(self) -> "MenuComponent":
        self.click(self.OPEN)
        self.visible(self.CLOSE)
        return self

    def close(self) -> None:
        self.click(self.CLOSE)
        self.wait_absent(self.CLOSE)

    def all_items(self) -> None:
        self.click(self.ALL_ITEMS)

    def about(self) -> None:
        self.click(self.ABOUT)

    def logout(self) -> None:
        self.click(self.LOGOUT)

    def reset_app_state(self) -> None:
        self.click(self.RESET_APP_STATE)

    def is_open(self) -> bool:
        return self.is_visible(self.CLOSE)

    def has_all_items(self) -> bool:
        return self.is_visible(self.ALL_ITEMS)

    def has_about(self) -> bool:
        return self.is_visible(self.ABOUT)

    def has_logout(self) -> bool:
        return self.is_visible(self.LOGOUT)

    def has_reset_app_state(self) -> bool:
        return self.is_visible(self.RESET_APP_STATE)
