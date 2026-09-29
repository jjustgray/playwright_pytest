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

        self.category_sidebar = page.locator(
            ".left-sidebar .category-products")
        self.women_category = self.category_sidebar.locator(
            'a[href="#Women"]')
        self.men_category = self.category_sidebar.locator(
            'a[href="#Men"]')
        self.women_subcategories = page.locator("#Women")
        self.men_subcategories = page.locator("#Men")
        self.brands_sidebar = page.locator(".left-sidebar .brands-name")
        self.brand_links = self.brands_sidebar.locator("li a")
        self.brand_products_heading = page.locator(
            ".features_items h2.title")
        self.review_form = page.locator("#review-form")
        self.review_heading = page.get_by_role(
            "link", name="Write Your Review", exact=True)
        self.review_name_input = self.review_form.locator("#name")
        self.review_email_input = self.review_form.locator("#email")
        self.review_text_input = self.review_form.locator("#review")
        self.review_submit_button = self.review_form.locator(
            "#button-review")
        self.review_success_message = page.get_by_text(
            "Thank you for your review.", exact=True)
        self.recommended_items = page.locator(".recommended_items")
        self.recommended_product_cards = page.locator(
            ".recommended_items .product-image-wrapper:visible")

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

    @allure.step("Expand Women category")
    def expand_women_category(self):
        self.click_with_retry_on_overload(self.women_category)

    @allure.step("Open Women subcategory: {subcategory}")
    def click_women_subcategory(self, subcategory: str):
        self.click_with_retry_on_overload(
            self.women_subcategories.get_by_role(
                "link", name=subcategory, exact=True))

    @allure.step("Expand Men category")
    def expand_men_category(self):
        self.click_with_retry_on_overload(self.men_category)

    @allure.step("Open Men subcategory: {subcategory}")
    def click_men_subcategory(self, subcategory: str):
        self.click_with_retry_on_overload(
            self.men_subcategories.get_by_role(
                "link", name=subcategory, exact=True))

    @allure.step("Open brand at index {index}")
    def click_brand(self, index: int):
        self.click_with_retry_on_overload(
            self.brand_links.nth(index))

    @allure.step("Fill product review form")
    def fill_review_form(self, name: str, email: str, review: str):
        self.review_name_input.fill(name)
        self.review_email_input.fill(email)
        self.review_text_input.fill(review)

    @allure.step("Submit product review")
    def submit_review(self):
        self.click_with_retry_on_overload(self.review_submit_button)

    @allure.step("Add recommended product {index} to cart")
    def add_recommended_product_to_cart(self, index: int = 0):
        product_card = self.recommended_product_cards.nth(index)
        product_card.scroll_into_view_if_needed()
        product_card.hover()
        self.click_with_retry_on_overload(
            product_card.locator("a.add-to-cart").last)
