from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    ERROR_CLOSE = (By.CSS_SELECTOR, '[data-test="error-button"]')

    def open(self) -> "LoginPage":
        self.driver.get(BASE_URL)
        self.visible(self.USERNAME)
        return self

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN)

    def submit_with_enter(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        password_field = self.visible(self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)

    def error_text(self) -> str:
        return self.text(self.ERROR)

    def username_input_type(self) -> str:
        return self.visible(self.USERNAME).get_attribute("type")

    def password_input_type(self) -> str:
        return self.visible(self.PASSWORD).get_attribute("type")

    def is_username_enabled(self) -> bool:
        return self.visible(self.USERNAME).is_enabled()

    def is_password_enabled(self) -> bool:
        return self.visible(self.PASSWORD).is_enabled()

    def is_login_button_enabled(self) -> bool:
        return self.visible(self.LOGIN).is_enabled()
