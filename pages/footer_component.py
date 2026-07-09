from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FooterComponent(BasePage):
    FOOTER = (By.CSS_SELECTOR, "footer, .footer")
    TWITTER = (By.CSS_SELECTOR, '[data-test="social-twitter"], a[href*="twitter.com"], a[href*="x.com"]')
    FACEBOOK = (By.CSS_SELECTOR, '[data-test="social-facebook"], a[href*="facebook.com"]')
    LINKEDIN = (By.CSS_SELECTOR, '[data-test="social-linkedin"], a[href*="linkedin.com"]')
    COPYRIGHT = (By.CSS_SELECTOR, '[data-test="footer-copy"], .footer_copy, footer')

    def footer_visible(self) -> bool:
        return self.is_visible(self.FOOTER)

    def twitter_visible(self) -> bool:
        return self.is_visible(self.TWITTER)

    def facebook_visible(self) -> bool:
        return self.is_visible(self.FACEBOOK)

    def linkedin_visible(self) -> bool:
        return self.is_visible(self.LINKEDIN)

    def copyright_text(self) -> str:
        return self.text(self.COPYRIGHT)

    def click_twitter(self) -> None:
        self.click(self.TWITTER)

    def click_facebook(self) -> None:
        self.click(self.FACEBOOK)

    def click_linkedin(self) -> None:
        self.click(self.LINKEDIN)
