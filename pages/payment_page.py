import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class PaymentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = page.locator('[data-qa="name-on-card"]')
        self.card_number_input = page.locator('[data-qa="card-number"]')
        self.cvc_input = page.locator('[data-qa="cvc"]')
        self.expiry_month_input = page.locator('[data-qa="expiry-month"]')
        self.expiry_year_input = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        self.order_success_message = page.get_by_text(
            "Congratulations! Your order has been confirmed!", exact=True)

    @allure.step("Enter payment details")
    def fill_payment_details(self, payment_data: dict):
        self.name_input.fill(payment_data["name"])
        self.card_number_input.fill(payment_data["card_number"])
        self.cvc_input.fill(payment_data["cvc"])
        self.expiry_month_input.fill(payment_data["expiry_month"])
        self.expiry_year_input.fill(payment_data["expiry_year"])

    @allure.step("Pay and confirm order")
    def pay_and_confirm_order(self):
        self.click_with_retry_on_overload(self.pay_button)
