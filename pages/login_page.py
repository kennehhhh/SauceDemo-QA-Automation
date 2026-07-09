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
    REMEMBER_ME = (
        By.XPATH,
        '//*[self::input or self::label or self::button][contains(translate(@data-test, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "remember") '
        'or contains(translate(@name, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "remember") '
        'or contains(translate(@id, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "remember") '
        'or contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "remember")]',
    )
    FORGOT_PASSWORD = (
        By.XPATH,
        '//*[self::a or self::button][contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "forgot")]',
    )
    SHOW_PASSWORD = (
        By.XPATH,
        '//*[self::button or self::input][contains(translate(@data-test, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "show") '
        'or contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "show") '
        'or contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "show")]',
    )

    def open(self) -> "LoginPage":
        self.driver.get(BASE_URL)
        self.visible(self.USERNAME)
        return self

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN)

    def submit_with_enter(self, username: str = "", password: str = "", from_field: str = "password") -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        if from_field == "username":
            self.visible(self.USERNAME).send_keys(Keys.ENTER)
        else:
            self.visible(self.PASSWORD).send_keys(Keys.ENTER)

    def error_text(self) -> str:
        return self.text(self.ERROR)

    def error_visible(self) -> bool:
        return self.is_visible(self.ERROR)

    def dismiss_error(self) -> None:
        self.click(self.ERROR_CLOSE)
        self.wait_absent(self.ERROR)

    def username_value(self) -> str:
        return self.attribute(self.USERNAME, "value")

    def password_value(self) -> str:
        return self.attribute(self.PASSWORD, "value")

    def clear_username(self) -> None:
        self.visible(self.USERNAME).clear()

    def clear_password(self) -> None:
        self.visible(self.PASSWORD).clear()

    def username_input_type(self) -> str:
        return self.attribute(self.USERNAME, "type")

    def password_input_type(self) -> str:
        return self.attribute(self.PASSWORD, "type")

    def is_username_enabled(self) -> bool:
        return self.visible(self.USERNAME).is_enabled()

    def is_password_enabled(self) -> bool:
        return self.visible(self.PASSWORD).is_enabled()

    def is_login_button_enabled(self) -> bool:
        return self.visible(self.LOGIN).is_enabled()

    def username_visible(self) -> bool:
        return self.is_visible(self.USERNAME)

    def password_visible(self) -> bool:
        return self.is_visible(self.PASSWORD)

    def login_button_visible(self) -> bool:
        return self.is_visible(self.LOGIN)

    def remember_me_exists(self) -> bool:
        return self.exists(self.REMEMBER_ME)

    def forgot_password_exists(self) -> bool:
        return self.exists(self.FORGOT_PASSWORD)

    def show_password_exists(self) -> bool:
        return self.exists(self.SHOW_PASSWORD)

    def click_show_password(self) -> None:
        self.click(self.SHOW_PASSWORD)
