import allure
from playwright.sync_api import Page

class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.slider_section = page.locator("section#slider")
        self.signup_login_button = page.locator("ul.navbar-nav").get_by_role("link", name=" Signup / Login", exact=True)

    @allure.step("Click on Signup / Login button")
    def click_signup_login_button(self):
        self.signup_login_button.click()