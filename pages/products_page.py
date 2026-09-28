import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.all_products_heading = page.get_by_role(
            "heading", name=re.compile(r"^ALL PRODUCTS$", re.I))
        self.searched_products_heading = page.get_by_role(
            "heading", name=re.compile(r"^SEARCHED PRODUCTS$", re.I))
        self.product_list = page.locator(".features_items")
        self.product_cards = self.product_list.locator(
            ".product-image-wrapper")
        self.first_view_product_button = self.product_cards.first.get_by_role(
            "link", name=re.compile(r"View Product", re.I))
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.quantity_input = page.locator("#quantity")
        self.detail_add_to_cart_button = page.locator(
            ".product-information button.cart")
        self.cart_modal = page.locator("#cartModal")
        self.continue_shopping_button = self.cart_modal.get_by_role(
            "button", name="Continue Shopping")
        self.view_cart_button = self.cart_modal.get_by_role(
            "link", name="View Cart")

        self.product_information = page.locator(".product-information")
        self.product_name = self.product_information.locator("h2")
        self.product_category = self.product_information.locator(
            "p").filter(has_text=re.compile(r"^Category:"))
        self.product_price = self.product_information.locator("span span")
        self.product_availability = self.product_information.locator(
            "p").filter(has_text=re.compile(r"^Availability:"))
        self.product_condition = self.product_information.locator(
            "p").filter(has_text=re.compile(r"^Condition:"))
        self.product_brand = self.product_information.locator(
            "p").filter(has_text=re.compile(r"^Brand:"))

    @allure.step("Click View Product for the first product")
    def click_first_view_product(self):
        self.click_with_retry_on_overload(self.first_view_product_button)

    @allure.step("Search for product: {product_name}")
    def search_product(self, product_name: str):
        self.search_input.fill(product_name)
        self.click_with_retry_on_overload(self.search_button)

    @allure.step("Add product {index} to cart")
    def add_product_to_cart(self, index: int):
        product_card = self.product_cards.nth(index)
        product_card.hover()
        self.click_with_retry_on_overload(
            product_card.locator("a.add-to-cart").last)

    @allure.step("Set product quantity to {quantity}")
    def set_quantity(self, quantity: int):
        self.quantity_input.fill(str(quantity))

    @allure.step("Add product details to cart")
    def add_product_details_to_cart(self):
        self.click_with_retry_on_overload(self.detail_add_to_cart_button)

    @allure.step("Continue shopping")
    def continue_shopping(self):
        self.click_with_retry_on_overload(self.continue_shopping_button)

    @allure.step("View cart from add-to-cart modal")
    def view_cart_from_modal(self):
        self.click_with_retry_on_overload(self.view_cart_button)
