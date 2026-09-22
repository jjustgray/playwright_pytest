import allure
import pytest
from playwright.sync_api import Page, expect

from pages.main_page import MainPage
from pages.login_page import LoginPage

@allure.feature("Login / Signup")
class LoginSignupTests:

    @pytest.fixture
    @allure.story("Before Each Test")
    def setup(self, page: Page):
        page.goto('/')
        yield
        page.close()

    @allure.story("TC-01: Register User")
    def test_register_user(self, page: Page, setup):
        main_page = MainPage(page)
        expect(main_page.slider_section).to_be_visible()
        main_page.click_signup_login_button()
        login_page = LoginPage(page)
        expect(login_page.heading_signup).to_be_visible()
        # 6. Enter name and email address

