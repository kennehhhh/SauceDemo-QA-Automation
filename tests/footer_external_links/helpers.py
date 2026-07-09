from __future__ import annotations

from selenium.webdriver.support.ui import WebDriverWait

from pages.footer_component import FooterComponent
from tests.menu_navigation.helpers import login_inventory


MODULE = "Footer & External Links"


def open_products_footer(driver) -> FooterComponent:
    login_inventory(driver)
    footer = FooterComponent(driver)
    footer.visible(FooterComponent.FOOTER)
    return footer


def click_external_link(driver, click_action) -> str:
    original = driver.current_window_handle
    existing_handles = set(driver.window_handles)
    click_action()
    WebDriverWait(driver, 8).until(lambda d: len(set(d.window_handles) - existing_handles) == 1)
    new_handle = (set(driver.window_handles) - existing_handles).pop()
    driver.switch_to.window(new_handle)
    WebDriverWait(driver, 8).until(lambda d: d.current_url and d.current_url != "about:blank")
    opened_url = driver.current_url
    driver.close()
    driver.switch_to.window(original)
    return opened_url
