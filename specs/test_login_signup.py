import re
import time
import allure
from playwright.sync_api import expect, Page
import pytest

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.signup_page import SignupPage


@pytest.mark.usefixtures("start_login_signup_flow")
@allure.feature("Login / Signup")
class TestLoginSignup:

    # @pytest.mark.skip(reason="Skipping this test for now")
    @allure.story("TC-01: Register User")
    def test_register_user(
        self,
        main_page: MainPage,
        login_page: LoginPage,
        signup_page: SignupPage,
    ):
        username = "Jimmy"
        user_email = f"jimmy_{int(time.time())}@example.com"

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
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {username}")
        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()

    # @pytest.mark.skip(reason="Skipping this test for now")
    @allure.story("TC-02: Login User with correct email and password")
    def test_login_user(
        self,
        main_page: MainPage,
        login_page: LoginPage,
        registered_user: dict,
    ):
        expect(login_page.login_heading).to_be_visible()
        login_page.fill_login_form(
            registered_user["email"], registered_user["password"])
        login_page.click_login_button()
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {registered_user['name']}")
        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()

    # @pytest.mark.skip(reason="Skipping this test for now")
    @allure.story("TC-03: Login User with incorrect email and password")
    def test_login_user_negative(
        self,
        login_page: LoginPage,
    ):
        expect(login_page.login_heading).to_be_visible()
        login_page.fill_login_form(
            "incorrect@example.com", "wrongpassword")
        login_page.click_login_button()
        expect(login_page.login_error_message).to_be_visible()

    # @pytest.mark.skip(reason="Skipping this test for now")
    @allure.story("TC-04: Logout User")
    def test_logout_user(
        self,
        main_page: MainPage,
        login_page: LoginPage,
        registered_user: dict,
        page: Page
    ):
        expect(login_page.login_heading).to_be_visible()
        login_page.fill_login_form(
            registered_user["email"], registered_user["password"])
        login_page.click_login_button()
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {registered_user['name']}")
        main_page.click_logout_button()
        expect(page).to_have_url(re.compile(r".*/login$"))

    @allure.story("TC-05: Register User with existing email")
    def test_register_with_exist_email(
        self,
        login_page: LoginPage,
        registered_user: dict,
        page: Page
    ):
        expect(login_page.signup_heading).to_be_visible()
        login_page.fill_signup_form(
            'Frodo', registered_user["email"]
        )
        login_page.click_signup_button()
        expect(login_page.signup_error_message).to_be_visible()
