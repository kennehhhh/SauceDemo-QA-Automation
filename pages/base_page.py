from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator) -> None:
        self.clickable(locator).click()

    def safe_click(self, locator) -> None:
        try:
            self.clickable(locator).click()
        except ElementClickInterceptedException:
            self.scroll_into_view(locator)
            self.clickable(locator).click()

    def type(self, locator, value: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator) -> str:
        return self.visible(locator).text.strip()

    def exists(self, locator) -> bool:
        return bool(self.driver.find_elements(*locator))

    def is_visible(self, locator) -> bool:
        try:
            return self.visible(locator).is_displayed()
        except TimeoutException:
            return False

    def is_enabled(self, locator) -> bool:
        try:
            return self.visible(locator).is_enabled()
        except TimeoutException:
            return False

    def attribute(self, locator, name: str) -> str:
        value = self.visible(locator).get_attribute(name)
        return "" if value is None else value

    def elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_url_contains(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

    def wait_absent(self, locator) -> None:
        self.wait.until(EC.invisibility_of_element_located(locator))

    def scroll_into_view(self, locator) -> None:
        element = self.present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def set_viewport(self, width: int, height: int) -> None:
        self.driver.set_window_size(width, height)

    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)
