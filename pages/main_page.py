import allure
import re
from playwright.sync_api import Page
from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.slider_section = page.locator("section#slider")
        self.signup_login_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Signup / Login")

        self.ad_position_box = page.locator("div.ad_position_box")
        self.ad_mys_wrapper = self.ad_position_box.locator("div#mys_wrapper")
        self.ad_close_button = self.ad_position_box.locator(
            "div.close-button")

        self.logged_in_as_text = page.locator(
            "ul.navbar-nav a", has_text="Logged in as")
        self.delete_account_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Delete Account")
        self.deleted_account_heading = page.get_by_role(
            "heading",
            name=re.compile(r"account deleted!", re.I)
        )
        self.logout_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Logout")
        self.contactus_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name=" Contact us")
        self.home_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name=" Home")
        self.test_cases_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Test Cases")
        self.products_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Products")
        self.cart_button = page.locator(
            "ul.navbar-nav").get_by_role("link", name="Cart")

        self.subscription_heading = page.locator("#footer").get_by_role(
            "heading", name="Subscription", exact=True)
        self.subscription_email_input = page.locator(
            "#footer #susbscribe_email")
        self.subscribe_button = page.locator("#footer #subscribe")
        self.subscription_success_message = page.locator(
            "#footer #success-subscribe")

    @allure.step("Click on Signup / Login button")
    def click_signup_login_button(self):
        self.click_with_retry_on_overload(self.signup_login_button)

    @allure.step("Close Ad Position Box if visible")
    def close_ad_position_box(self):
        if self.ad_position_box.is_visible():
            self.click_with_retry_on_overload(self.ad_close_button)

    @allure.step("Click on Delete Account button")
    def click_delete_account_button(self):
        self.click_with_retry_on_overload(self.delete_account_button)

    @allure.step("Click Logout button")
    def click_logout_button(self):
        self.click_with_retry_on_overload(self.logout_button)

    @allure.step("Click Contact Us button")
    def click_contactus_button(self):
        self.click_with_retry_on_overload(self.contactus_button)

    @allure.step("Click Home button")
    def click_home_button(self):
        self.click_with_retry_on_overload(self.home_button)

    @allure.step("Click on Test Cases button")
    def click_test_cases_button(self):
        self.click_with_retry_on_overload(self.test_cases_button)

    @allure.step("Click on Products button")
    def click_products_button(self):
        self.click_with_retry_on_overload(self.products_button)

    @allure.step("Click on Cart button")
    def click_cart_button(self):
        self.click_with_retry_on_overload(self.cart_button)

    @allure.step("Scroll to subscription in footer")
    def scroll_to_subscription(self):
        self.subscription_heading.scroll_into_view_if_needed()

    @allure.step("Subscribe to newsletter")
    def subscribe_to_newsletter(self, email: str):
        self.subscription_email_input.fill(email)
        self.click_with_retry_on_overload(self.subscribe_button)
