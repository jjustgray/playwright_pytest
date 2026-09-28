import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.delivery_address = page.locator("#address_delivery")
        self.invoice_address = page.locator("#address_invoice")
        self.order_review = page.get_by_role(
            "heading", name="Review Your Order", exact=True)
        self.comment_input = page.locator("#ordermsg textarea")
        self.place_order_button = page.locator("a.check_out[href='/payment']")

    @allure.step("Enter order comment")
    def enter_comment(self, comment: str):
        self.comment_input.fill(comment)

    @allure.step("Place order")
    def place_order(self):
        self.click_with_retry_on_overload(self.place_order_button)
