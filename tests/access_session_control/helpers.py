from __future__ import annotations

from time import sleep
from urllib.parse import urljoin

from config import BASE_URL, USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent


MODULE = "Access & Session Control"


def protected_url(path: str) -> str:
    return urljoin(BASE_URL, path.lstrip("/"))


def login_standard(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", USERS["standard_user"])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def logout(driver) -> None:
    MenuComponent(driver).open().logout()
    LoginPage(driver).visible(LoginPage.LOGIN)


def assert_protected_access_blocked(driver, path: str) -> str:
    driver.get(protected_url(path))
    login = LoginPage(driver)
    login_visible = login.is_visible(LoginPage.LOGIN)
    error = login.error_text() if login.error_visible() else ""
    assert login_visible
    assert error or "saucedemo.com" in driver.current_url
    return error


def bounded_idle_probe(driver, seconds: int = 2) -> bool:
    sleep(seconds)
    driver.refresh()
    return InventoryPage(driver).is_visible(InventoryPage.TITLE)
