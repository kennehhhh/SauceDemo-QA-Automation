from __future__ import annotations

import pytest

from pages.footer_component import FooterComponent
from pages.inventory_page import InventoryPage
from tests.footer_external_links.helpers import MODULE, click_external_link, open_products_footer


@pytest.mark.footer_external_links
@pytest.mark.unit
@pytest.mark.case_id("FT-0001")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_twitter_footer_link_visibility_is_recorded(driver, record_actual_result):
    footer = open_products_footer(driver)
    visible = footer.twitter_visible()
    record_actual_result("Twitter footer link was visible." if visible else "Twitter footer link was absent.")
    assert visible or footer.footer_visible()


@pytest.mark.footer_external_links
@pytest.mark.system
@pytest.mark.case_id("FT-0002")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_twitter_footer_link_opens_intended_destination(driver, record_actual_result):
    footer = open_products_footer(driver)
    assert footer.twitter_visible()
    opened_url = click_external_link(driver, footer.click_twitter)
    InventoryPage(driver).assert_loaded()
    record_actual_result(f"Twitter footer link opened {opened_url} and Products page remained usable.")
    assert "twitter.com" in opened_url.lower() or "x.com" in opened_url.lower()


@pytest.mark.footer_external_links
@pytest.mark.unit
@pytest.mark.case_id("FT-0003")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_facebook_footer_link_visibility_is_recorded(driver, record_actual_result):
    footer = open_products_footer(driver)
    visible = footer.facebook_visible()
    record_actual_result("Facebook footer link was visible." if visible else "Facebook footer link was absent.")
    assert visible or footer.footer_visible()


@pytest.mark.footer_external_links
@pytest.mark.system
@pytest.mark.case_id("FT-0004")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_facebook_footer_link_opens_intended_destination(driver, record_actual_result):
    footer = open_products_footer(driver)
    assert footer.facebook_visible()
    opened_url = click_external_link(driver, footer.click_facebook)
    InventoryPage(driver).assert_loaded()
    record_actual_result(f"Facebook footer link opened {opened_url} and Products page remained usable.")
    assert "facebook.com" in opened_url.lower()


@pytest.mark.footer_external_links
@pytest.mark.unit
@pytest.mark.case_id("FT-0005")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_linkedin_footer_link_visibility_is_recorded(driver, record_actual_result):
    footer = open_products_footer(driver)
    visible = footer.linkedin_visible()
    record_actual_result("LinkedIn footer link was visible." if visible else "LinkedIn footer link was absent.")
    assert visible or footer.footer_visible()


@pytest.mark.footer_external_links
@pytest.mark.system
@pytest.mark.case_id("FT-0006")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_linkedin_footer_link_opens_intended_destination(driver, record_actual_result):
    footer = open_products_footer(driver)
    assert footer.linkedin_visible()
    opened_url = click_external_link(driver, footer.click_linkedin)
    InventoryPage(driver).assert_loaded()
    record_actual_result(f"LinkedIn footer link opened {opened_url} and Products page remained usable.")
    assert "linkedin.com" in opened_url.lower()


@pytest.mark.footer_external_links
@pytest.mark.unit
@pytest.mark.case_id("FT-0007")
@pytest.mark.module(MODULE)
@pytest.mark.test_user("standard_user")
def test_footer_copyright_text_is_visible(driver, record_actual_result):
    footer = open_products_footer(driver)
    text = footer.copyright_text()
    record_actual_result(f"Footer copyright text was: {text}.")
    assert "sauce labs" in text.lower() or "rights reserved" in text.lower()
