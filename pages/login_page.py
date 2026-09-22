import allure
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading_signup = page.get_by_role("heading", name="New User Signup!", exact=True)