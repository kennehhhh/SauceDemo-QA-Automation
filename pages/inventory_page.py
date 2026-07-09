from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    INVENTORY_LIST = (By.CSS_SELECTOR, '[data-test="inventory-list"]')
    INVENTORY_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    SORT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_DESC = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    PRODUCT_IMAGE = (By.CSS_SELECTOR, '[data-test="inventory-item"] img')
    SEARCH = (
        By.XPATH,
        '//*[self::input or self::button][contains(translate(@data-test, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "search") '
        'or contains(translate(@placeholder, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "search") '
        'or contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "search") '
        'or contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "search")]',
    )
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')

    def assert_loaded(self) -> None:
        assert self.text(self.TITLE) == "Products"
        self.visible(self.INVENTORY_LIST)

    @staticmethod
    def _slug(name: str) -> str:
        return (
            name.lower()
            .replace(".", "")
            .replace("()", "")
            .replace(" ", "-")
        )

    def add_product(self, product_name: str) -> None:
        slug = self._slug(product_name)
        self.click((By.CSS_SELECTOR, f'[data-test="add-to-cart-{slug}"]'))

    def remove_product(self, product_name: str) -> None:
        slug = self._slug(product_name)
        self.click((By.CSS_SELECTOR, f'[data-test="remove-{slug}"]'))

    def open_product(self, product_name: str) -> None:
        self.click((By.XPATH, f'//div[@data-test="inventory-item-name" and normalize-space()="{product_name}"]'))

    def click_product_image(self, product_name: str) -> None:
        item = self._item_for(product_name)
        item.find_element(By.CSS_SELECTOR, "img").click()

    def _item_for(self, product_name: str):
        return self.driver.find_element(
            By.XPATH,
            f'//div[@data-test="inventory-item" and .//div[@data-test="inventory-item-name" and normalize-space()="{product_name}"]]',
        )

    def product_cards(self) -> list[dict[str, str]]:
        cards = []
        for item in self.elements(self.INVENTORY_ITEM):
            name = item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text.strip()
            desc = item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-desc"]').text.strip()
            price = item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-price"]').text.strip()
            image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src") or ""
            button = item.find_element(By.CSS_SELECTOR, "button").text.strip()
            cards.append({"name": name, "description": desc, "price": price, "image": image, "button": button})
        return cards

    def cart_count(self) -> int:
        elems = self.driver.find_elements(*self.CART_BADGE)
        return int(elems[0].text) if elems else 0

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def sort_by_value(self, value: str) -> None:
        Select(self.visible(self.SORT)).select_by_value(value)

    def product_names(self) -> list[str]:
        elems = self.driver.find_elements(*self.PRODUCT_NAME)
        return [e.text.strip() for e in elems]

    def product_descriptions(self) -> list[str]:
        elems = self.driver.find_elements(*self.PRODUCT_DESC)
        return [e.text.strip() for e in elems]

    def product_prices(self) -> list[float]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
        return [float(e.text.replace("$", "").strip()) for e in elems]

    def product_price_texts(self) -> list[str]:
        elems = self.driver.find_elements(*self.PRODUCT_PRICE)
        return [e.text.strip() for e in elems]

    def product_image_srcs(self) -> list[str]:
        elems = self.driver.find_elements(*self.PRODUCT_IMAGE)
        return [(e.get_attribute("src") or "").strip() for e in elems]

    def button_state_for(self, product_name: str) -> str:
        item = self._item_for(product_name)
        return item.find_element(By.CSS_SELECTOR, "button").text.strip()

    def sort_options(self) -> list[str]:
        select = Select(self.visible(self.SORT))
        return [option.text.strip() for option in select.options]

    def selected_sort_text(self) -> str:
        return Select(self.visible(self.SORT)).first_selected_option.text.strip()

    def search_exists(self) -> bool:
        return self.exists(self.SEARCH)

    def search(self, text: str) -> None:
        self.type(self.SEARCH, text)

    def logout(self) -> None:
        self.click(self.MENU)
        self.click(self.LOGOUT)
