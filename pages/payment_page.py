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
        self.download_invoice_button = page.get_by_role(
            "link", name="Download Invoice", exact=True)
        self.continue_button = page.locator(
            'a[data-qa="continue-button"]')

    @allure.step("Enter payment details")
    def fill_payment_details(self, payment_data: dict):
        self.name_input.fill(payment_data["name"])
        self.card_number_input.fill(payment_data["card_number"])
        self.cvc_input.fill(payment_data["cvc"])
        self.expiry_month_input.fill(payment_data["expiry_month"])
        self.expiry_year_input.fill(payment_data["expiry_year"])
        self.attach_step_screenshot("payment: details entered")

    @allure.step("Pay and confirm order")
    def pay_and_confirm_order(self):
        self.pay_button.click()
        self.attach_step_screenshot("payment: pay and confirm clicked")

    @allure.step("Download invoice")
    def download_invoice(self, timeout: float = 5000):
        href = self.download_invoice_button.get_attribute("href")

        try:
            with self.page.expect_download(timeout=timeout) as download_info:
                self.click_with_retry_on_overload(self.download_invoice_button)
            self.attach_step_screenshot(
                "payment: invoice downloaded via browser")
            return download_info.value
        except Exception:
            if href:
                response = self.page.request.get(href)
                if response.ok:
                    self.attach_step_screenshot(
                        "payment: invoice fetched via API fallback")
                    return response.body()
            raise RuntimeError(
                f"Failed to download or fetch invoice from href: {href}")

    @allure.step("Continue after order completion")
    def click_continue_button(self):
        self.click_with_retry_on_overload(self.continue_button)
