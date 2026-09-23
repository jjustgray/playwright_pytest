import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.signup_heading = page.get_by_role("heading", name=" New User Signup!", exact=True)
        self.name_input = page.locator('form[action="/signup"]').get_by_role("textbox", name="Name")
        self.email_input = page.locator('form[action="/signup"]').get_by_role("textbox", name="Email Address")
        self.signup_button = page.locator('form[action="/signup"]').get_by_role("button", name="Signup")
        self.signup_form_heading = page.get_by_role("heading", name="ENTER ACCOUNT INFORMATION", exact=True)

    @allure.step("Fill Signup Form on Login Page")
    def fill_signup_form(self, name: str, email: str):
        self.name_input.fill(name)
        self.email_input.fill(email)

    @allure.step("Click Signup Button")
    def click_signup_button(self):
        self.click_with_retry_on_overload(self.signup_button)