from __future__ import annotations

from selenium.webdriver.common.keys import Keys

import pytest

from config import USERS
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent
from tests.interface_responsive.helpers import (
    DESKTOP,
    MOBILE,
    MODULE,
    accessible_name,
    login_as,
    login_performance_user,
    no_horizontal_overflow,
    open_mobile_cart,
    open_mobile_checkout_info,
    open_mobile_checkout_overview,
    rects_overlap,
    red_shirt_name_and_button_rects,
)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_login_page_remains_usable_at_desktop_width(driver, record_actual_result):
    driver.set_window_size(*DESKTOP)
    page = LoginPage(driver).open()
    controls_visible = page.username_visible() and page.password_visible() and page.login_button_visible()
    record_actual_result("Login controls were visible at desktop width." if controls_visible else "Login controls were not all visible at desktop width.")
    assert controls_visible
    assert no_horizontal_overflow(driver)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_login_page_remains_usable_at_narrow_mobile_width(driver, record_actual_result):
    driver.set_window_size(*MOBILE)
    page = LoginPage(driver).open()
    controls_visible = page.username_visible() and page.password_visible() and page.login_button_visible()
    record_actual_result("Login inputs and button stayed visible within the mobile viewport." if controls_visible else "Login controls were not all visible on mobile.")
    assert controls_visible
    assert no_horizontal_overflow(driver)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_products_grid_reflows_without_horizontal_page_overflow(driver, record_actual_result):
    driver.set_window_size(*MOBILE)
    login_as(driver)
    ok = no_horizontal_overflow(driver)
    record_actual_result("Products page had no horizontal overflow at narrow viewport." if ok else "Products page had horizontal overflow at narrow viewport.")
    assert ok


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_product_card_long_text_stays_contained(driver, record_actual_result):
    driver.set_window_size(*MOBILE)
    login_as(driver)
    name_rect, button_rect = red_shirt_name_and_button_rects(driver)
    overlap = rects_overlap(name_rect, button_rect)
    record_actual_result(f"Long product name and action button overlap was {overlap}.")
    assert not overlap


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_cart_layout_remains_usable_on_mobile(driver, record_actual_result):
    cart = open_mobile_cart(driver)
    usable = cart.item_names() and cart.is_visible(cart.CHECKOUT) and cart.is_visible(cart.CONTINUE)
    record_actual_result("Cart items and actions were accessible on mobile." if usable else "Cart mobile layout was not fully usable.")
    assert usable
    assert no_horizontal_overflow(driver)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_checkout_information_form_remains_usable_on_mobile(driver, record_actual_result):
    page = open_mobile_checkout_info(driver)
    usable = all(page.is_visible(locator) for locator in (CheckoutInfoPage.FIRST, CheckoutInfoPage.LAST, CheckoutInfoPage.POSTAL, CheckoutInfoPage.CONTINUE))
    record_actual_result("Checkout information fields/buttons fit the mobile viewport." if usable else "Checkout information controls were not all visible on mobile.")
    assert usable
    assert no_horizontal_overflow(driver)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_checkout_overview_remains_readable_on_mobile(driver, record_actual_result):
    page = open_mobile_checkout_overview(driver)
    readable = page.item_names() and page.is_visible(CheckoutOverviewPage.TOTAL) and page.is_visible(CheckoutOverviewPage.FINISH)
    record_actual_result("Checkout overview items, total, and Finish remained readable on mobile." if readable else "Checkout overview mobile state was not readable.")
    assert readable
    assert no_horizontal_overflow(driver)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_side_menu_remains_operable_on_mobile(driver, record_actual_result):
    driver.set_window_size(*MOBILE)
    login_as(driver)
    menu = MenuComponent(driver).open()
    operable = menu.has_all_items() and menu.has_logout() and menu.has_reset_app_state()
    record_actual_result("Side menu items were reachable on mobile." if operable else "Side menu items were not all reachable on mobile.")
    assert operable


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_keyboard_focus_is_visible_on_interactive_controls(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.visible(LoginPage.USERNAME).send_keys(Keys.TAB)
    active_tag = driver.execute_script("return document.activeElement && document.activeElement.tagName;")
    focus_style = driver.execute_script(
        "const s = window.getComputedStyle(document.activeElement);"
        "return {outline: s.outlineStyle, outlineWidth: s.outlineWidth, boxShadow: s.boxShadow};"
    )
    has_indicator = focus_style["outline"] != "none" or focus_style["boxShadow"] != "none" or focus_style["outlineWidth"] != "0px"
    record_actual_result(f"Focused element tag was {active_tag}; computed focus style was {focus_style}.")
    assert active_tag in {"INPUT", "BUTTON"}
    assert has_indicator


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_buttons_do_not_overlap_at_200_percent_zoom(driver, record_actual_result):
    driver.set_window_size(768, 900)
    login_as(driver)
    driver.execute_script("document.body.style.zoom = '200%';")
    name_rect, button_rect = red_shirt_name_and_button_rects(driver)
    overlap = rects_overlap(name_rect, button_rect)
    record_actual_result(f"At 200 percent CSS zoom, long product name and action button overlap was {overlap}.")
    assert not overlap


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_page_supports_narrow_mobile_viewport(driver, record_actual_result):
    driver.set_window_size(*MOBILE)
    login_as(driver)
    ok = no_horizontal_overflow(driver)
    record_actual_result("Products page had no horizontal overflow at 375px viewport." if ok else "Products page overflowed horizontally at 375px viewport.")
    assert ok


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_error_messages_are_understandable(driver, record_actual_result):
    page = LoginPage(driver).open()
    page.login("bad_user", "bad_password")
    error = page.error_text()
    raw_terms = ("traceback", "exception", "stacktrace", "undefined", "null")
    record_actual_result(f"Invalid login error message was: {error}.")
    assert error
    assert not any(term in error.lower() for term in raw_terms)


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0013")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("performance_glitch_user")
def test_performance_glitch_user_loading_delay_gives_usable_feedback(driver, record_actual_result):
    elapsed = login_performance_user(driver)
    record_actual_result(f"performance_glitch_user reached Products after {elapsed:.2f} seconds.")
    assert elapsed < 12
    InventoryPage(driver).assert_loaded()


@pytest.mark.interface_responsive
@pytest.mark.system
@pytest.mark.case_id("UX-0014")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("visual_user")
def test_visual_user_discrepancies_are_captured_against_standard_user(driver, record_actual_result):
    standard = login_as(driver, "standard_user").product_image_srcs()
    MenuComponent(driver).open().logout()
    LoginPage(driver).login("visual_user", USERS["visual_user"])
    visual = InventoryPage(driver)
    visual.assert_loaded()
    visual_srcs = visual.product_image_srcs()
    differences = [idx for idx, (left, right) in enumerate(zip(standard, visual_srcs), start=1) if left != right]
    record_actual_result(f"visual_user image source differences versus standard_user were at positions: {differences or '<none>'}.")
    assert differences


@pytest.mark.interface_responsive
@pytest.mark.unit
@pytest.mark.case_id("UX-0015")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_login_inputs_have_accessible_names(driver, record_actual_result):
    page = LoginPage(driver).open()
    username_name = accessible_name(page.visible(LoginPage.USERNAME))
    password_name = accessible_name(page.visible(LoginPage.PASSWORD))
    record_actual_result(f"Username accessible-name sources: {username_name}; password accessible-name sources: {password_name}.")
    assert "user" in username_name.lower()
    assert "password" in password_name.lower()
