from __future__ import annotations

from time import perf_counter

from config import USERS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_A, PRODUCT_RED_SHIRT


MODULE = "Interface / Responsive"
MOBILE = (375, 812)
DESKTOP = (1440, 1000)


def no_horizontal_overflow(driver) -> bool:
    return bool(
        driver.execute_script(
            "return document.documentElement.scrollWidth <= window.innerWidth + 1 "
            "&& document.body.scrollWidth <= window.innerWidth + 1;"
        )
    )


def login_as(driver, username: str = "standard_user") -> InventoryPage:
    LoginPage(driver).open().login(username, USERS[username])
    page = InventoryPage(driver)
    page.assert_loaded()
    return page


def open_mobile_cart(driver) -> CartPage:
    driver.set_window_size(*MOBILE)
    inventory = login_as(driver)
    inventory.add_product(PRODUCT_A)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.assert_loaded()
    return cart


def open_mobile_checkout_info(driver) -> CheckoutInfoPage:
    cart = open_mobile_cart(driver)
    cart.checkout()
    page = CheckoutInfoPage(driver)
    page.assert_loaded()
    return page


def open_mobile_checkout_overview(driver) -> CheckoutOverviewPage:
    info = open_mobile_checkout_info(driver)
    info.fill(first="John", last="Doe", postal="1000")
    info.continue_checkout()
    page = CheckoutOverviewPage(driver)
    page.assert_loaded()
    return page


def login_performance_user(driver) -> float:
    start = perf_counter()
    LoginPage(driver).open().login("performance_glitch_user", USERS["performance_glitch_user"])
    InventoryPage(driver).assert_loaded()
    return perf_counter() - start


def red_shirt_name_and_button_rects(driver):
    item = driver.find_element(
        "xpath",
        f'//div[@data-test="inventory-item" and .//div[@data-test="inventory-item-name" and normalize-space()="{PRODUCT_RED_SHIRT}"]]',
    )
    name = item.find_element("css selector", '[data-test="inventory-item-name"]')
    button = item.find_element("css selector", "button")
    return name.rect, button.rect


def rects_overlap(a: dict, b: dict) -> bool:
    return not (
        a["x"] + a["width"] <= b["x"]
        or b["x"] + b["width"] <= a["x"]
        or a["y"] + a["height"] <= b["y"]
        or b["y"] + b["height"] <= a["y"]
    )


def accessible_name(locator_element) -> str:
    pieces = [
        locator_element.get_attribute("aria-label") or "",
        locator_element.get_attribute("name") or "",
        locator_element.get_attribute("placeholder") or "",
        locator_element.get_attribute("data-test") or "",
        locator_element.get_attribute("id") or "",
    ]
    return " ".join(piece for piece in pieces if piece).strip()
