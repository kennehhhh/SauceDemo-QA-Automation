from __future__ import annotations

from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN = (By.CSS_SELECTOR, '[data-test="login-button"]')

    def open(self) -> "LoginPage":
        self.driver.get(BASE_URL)
        self.visible(self.USERNAME)
        return self

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN)
