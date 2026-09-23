import time
import allure
from playwright.sync_api import expect, Page

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.signup_page import SignupPage


@allure.feature("Login / Signup")
class TestLoginSignup:

    @allure.story("TC-01: Register User")
    def test_register_user(
        self,
        main_page: MainPage,
        login_page: LoginPage,
        signup_page: SignupPage,
        page: Page
    ):
        username = "Jimmy"
        user_email = f"jimmy_{int(time.time())}@example.com"

        expect(main_page.slider_section).to_be_visible()
        main_page.click_signup_login_button()
        expect(login_page.signup_heading).to_be_visible()
        login_page.fill_signup_form(username, user_email)
        login_page.click_signup_button()
        expect(signup_page.signup_heading).to_be_visible()
        signup_page.fill_account_form({
            "title": "Mr",
            "name": username,
            "password": "password123",
            "day": "8",
            "month": "10",
            "year": "2006",
        })
        signup_page.click_newsletter_checkbox()
        signup_page.click_offers_checkbox()
        signup_page.fill_address_form({
            "first_name": "Jimmy",
            "last_name": "Smith",
            "company": "Example Inc.",
            "address1": "123 Main St",
            "address2": "Apt 4B",
            "country": "United States",
            "state": "California",
            "city": "Los Angeles",
            "zipcode": "90001",
            "mobile_number": "1234567890",
        })
        signup_page.click_create_account_button()
        expect(signup_page.account_created_heading).to_be_visible()
        signup_page.click_continue_button()
        expect(main_page.logged_in_as_text).to_contain_text(f"Logged in as {username}")
        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
