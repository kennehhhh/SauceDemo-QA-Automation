from __future__ import annotations

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent
from testdata.products import PRODUCT_A
from tests.access_session_control.helpers import (
    MODULE,
    assert_protected_access_blocked,
    bounded_idle_probe,
    login_standard,
    logout,
    protected_url,
)


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_unauthenticated_inventory_access_is_blocked(driver, record_actual_result):
    error = assert_protected_access_blocked(driver, "/inventory.html")
    record_actual_result(f"Unauthenticated /inventory.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_unauthenticated_cart_access_is_blocked(driver, record_actual_result):
    error = assert_protected_access_blocked(driver, "/cart.html")
    record_actual_result(f"Unauthenticated /cart.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_unauthenticated_checkout_information_access_is_blocked(driver, record_actual_result):
    error = assert_protected_access_blocked(driver, "/checkout-step-one.html")
    record_actual_result(f"Unauthenticated /checkout-step-one.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_unauthenticated_checkout_overview_access_is_blocked(driver, record_actual_result):
    error = assert_protected_access_blocked(driver, "/checkout-step-two.html")
    record_actual_result(f"Unauthenticated /checkout-step-two.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_unauthenticated_checkout_complete_access_is_blocked(driver, record_actual_result):
    error = assert_protected_access_blocked(driver, "/checkout-complete.html")
    record_actual_result(f"Unauthenticated /checkout-complete.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_post_logout_inventory_access_is_blocked(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    error = assert_protected_access_blocked(driver, "/inventory.html")
    record_actual_result(f"Post-logout /inventory.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("N/A")
def test_post_logout_cart_access_is_blocked(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    error = assert_protected_access_blocked(driver, "/cart.html")
    record_actual_result(f"Post-logout /cart.html access was blocked with message: {error or '<none>'}.")


@pytest.mark.access_session_control
@pytest.mark.integration
@pytest.mark.case_id("AC-0008")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_authenticated_refresh_preserves_valid_session(driver, record_actual_result):
    login_standard(driver)
    driver.refresh()
    InventoryPage(driver).assert_loaded()
    record_actual_result("Authenticated inventory refresh preserved the active session.")


@pytest.mark.access_session_control
@pytest.mark.integration
@pytest.mark.case_id("AC-0009")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_second_tab_follows_same_session_policy_consistently(driver, record_actual_result):
    login_standard(driver)
    driver.execute_script("window.open(arguments[0], '_blank');", protected_url("/inventory.html"))
    driver.switch_to.window(driver.window_handles[-1])
    InventoryPage(driver).assert_loaded()
    record_actual_result("Protected inventory opened in a second tab using the same authenticated browser session.")


@pytest.mark.access_session_control
@pytest.mark.integration
@pytest.mark.case_id("AC-0010")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_logout_invalidates_current_session_state(driver, record_actual_result):
    inventory = login_standard(driver)
    inventory.add_product(PRODUCT_A)
    MenuComponent(driver).open().logout()
    driver.get(protected_url("/inventory.html"))
    login = LoginPage(driver)
    blocked = login.is_visible(LoginPage.LOGIN)
    record_actual_result("After logout, direct reuse of /inventory.html returned to login." if blocked else "After logout, /inventory.html remained usable.")
    assert blocked


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0011")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_idle_session_timeout_is_enforced(driver, record_actual_result):
    login_standard(driver)
    remained_authenticated = bounded_idle_probe(driver)
    record_actual_result(
        "After a bounded idle probe and refresh, inventory remained authenticated."
        if remained_authenticated
        else "After a bounded idle probe and refresh, session required re-login."
    )
    assert not remained_authenticated


@pytest.mark.access_session_control
@pytest.mark.system
@pytest.mark.case_id("AC-0012")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_sensitive_pages_discourage_browser_caching_after_logout(driver, record_actual_result):
    login_standard(driver)
    logout(driver)
    driver.back()
    inventory_visible = InventoryPage(driver).is_visible(InventoryPage.TITLE)
    record_actual_result(
        "Browser back after logout exposed the inventory page."
        if inventory_visible
        else "Browser back after logout did not expose a usable authenticated inventory page."
    )
    assert not inventory_visible
