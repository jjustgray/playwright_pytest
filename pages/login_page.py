import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # signup form elements
        self.signup_heading = page.get_by_role(
            "heading", name=" New User Signup!", exact=True)
        self.name_input = page.locator(
            'form[action="/signup"]').get_by_role("textbox", name="Name")
        self.email_input = page.locator(
            'form[action="/signup"]').get_by_role("textbox", name="Email Address")
        self.signup_button = page.locator(
            'form[action="/signup"]').get_by_role("button", name="Signup")
        self.signup_form_heading = page.get_by_role(
            "heading", name="ENTER ACCOUNT INFORMATION", exact=True)
        self.signup_error_message = page.get_by_text(
            "Email Address already exist!"
        )

        # login form elements
        self.login_heading = page.get_by_role(
            "heading", name="Login to your account", exact=True)
        self.login_email_input = page.locator(
            'form[action="/login"]').get_by_role("textbox", name="Email Address")
        self.login_password_input = page.locator(
            'form[action="/login"]').get_by_role("textbox", name="Password")
        self.login_error_message = page.get_by_text(
            "Your email or password is incorrect!")
        self.login_button = page.locator(
            'form[action="/login"]').get_by_role("button", name="Login")

    @allure.step("Fill Signup Form on Login Page")
    def fill_signup_form(self, name: str, email: str):
        self.name_input.fill(name)
        self.email_input.fill(email)

    @allure.step("Fill Login Form on Login Page")
    def fill_login_form(self, email: str, password: str):
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)

    @allure.step("Click Signup Button")
    def click_signup_button(self):
        self.click_with_retry_on_overload(self.signup_button)

    @allure.step("Click Login Button")
    def click_login_button(self):
        self.click_with_retry_on_overload(self.login_button)
