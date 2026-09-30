import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_heading = page.locator(".breadcrumb").get_by_text(
            "Shopping Cart", exact=True)
        self.product_rows = page.locator(
            "#cart_info_table tbody tr[id^='product-']")
        self.proceed_to_checkout_button = page.locator("a.check_out")
        self.empty_cart_message = page.locator("#empty_cart")
        self.checkout_prompt = page.locator(".modal-content").filter(
            has_text="Register / Login account to proceed on checkout.")
        self.register_login_button = self.checkout_prompt.get_by_role(
            "link", name="Register / Login")
        self.continue_on_cart_button = page.get_by_role(
            "button", name="Continue On Cart")

    def product_row(self, product_id: int) -> Locator:
        return self.page.locator(f"#product-{product_id}")

    @allure.step("Remove product {product_id} from cart")
    def remove_product(self, product_id: int):
        self.click_with_retry_on_overload(
            self.product_row(product_id).locator(".cart_quantity_delete"))
        self.attach_step_screenshot(f"cart: removed product {product_id}")

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        self.click_with_retry_on_overload(self.proceed_to_checkout_button)
        self.attach_step_screenshot("cart: proceed to checkout")

    @allure.step("Continue on cart after guest checkout prompt")
    def continue_on_cart(self):
        self.click_with_retry_on_overload(self.continue_on_cart_button)
        self.attach_step_screenshot("cart: continue on cart")

    @allure.step("Open registration and login from checkout prompt")
    def click_register_login(self):
        self.click_with_retry_on_overload(self.register_login_button)
        self.attach_step_screenshot(
            "cart: register/login from checkout prompt")
