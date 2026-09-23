import allure
import re
from playwright.sync_api import Page
from pages.base_page import BasePage


class SignupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.signup_heading = page.get_by_role(
            "heading", 
            name=re.compile(r"^enter account information$", re.I)
        )

        # Account Information Form Locators
        self.title_group = page.locator(".clearfix", has=page.locator('[data-qa="title"]'))
        self.title_radio_buttons = self.title_group.locator('input[type="radio"]')
        self.name_input = page.locator('input#name')
        self.email_input = page.locator('input#email')
        self.password_input = page.locator('input#password')
        self.day_select = page.locator('select#days')
        self.month_select = page.locator('select#months')
        self.year_select = page.locator('select#years')

        self.newsletter_checkbox = page.locator('input#newsletter')
        self.offers_checkbox = page.locator('input#optin')

        # Address Information Form Locators
        self.first_name_input = page.locator('input#first_name')
        self.last_name_input = page.locator('input#last_name')
        self.company_input = page.locator('input#company')
        self.address1_input = page.locator('input#address1')
        self.address2_input = page.locator('input#address2')
        self.country_select = page.locator('select#country')
        self.state_input = page.locator('input#state')
        self.city_input = page.locator('input#city')
        self.zipcode_input = page.locator('input#zipcode')
        self.mobile_number_input = page.locator('input#mobile_number')

        self.create_account_button = page.locator('button[data-qa="create-account"]')

        self.account_created_heading = page.get_by_role(
            "heading",
            name=re.compile(r"account created!", re.I)
        )
        self.continue_button = page.locator('a[data-qa="continue-button"]')

    @allure.step("Fill Account Information Form on Signup Page")
    def fill_account_form(self, data: dict):
        title = data.get("title", "").lower()
        if title == "mr":
            self.title_radio_buttons.nth(0).check()
        elif title == "mrs":
            self.title_radio_buttons.nth(1).check()

        self.name_input.fill(data["name"])
        self.password_input.fill(data["password"])
        self.day_select.select_option(str(data["day"]))
        self.month_select.select_option(str(data["month"]))
        self.year_select.select_option(str(data["year"]))

    @allure.step("Click Newsletter Checkbox")
    def click_newsletter_checkbox(self):
        self.newsletter_checkbox.check()

    @allure.step("Click Offers Checkbox")
    def click_offers_checkbox(self):
        self.offers_checkbox.check()

    @allure.step("Fill Address Information Form on Signup Page")
    def fill_address_form(self, address_data: dict):
        self.first_name_input.fill(address_data["first_name"])
        self.last_name_input.fill(address_data["last_name"])
        self.company_input.fill(address_data["company"])
        self.address1_input.fill(address_data["address1"])
        self.address2_input.fill(address_data["address2"])
        self.country_select.select_option(address_data["country"])
        self.state_input.fill(address_data["state"])
        self.city_input.fill(address_data["city"])
        self.zipcode_input.fill(address_data["zipcode"])
        self.mobile_number_input.fill(address_data["mobile_number"])

    @allure.step("Click Create Account Button")
    def click_create_account_button(self):
        self.click_with_retry_on_overload(self.create_account_button)

    @allure.step("Click Continue Button")
    def click_continue_button(self):
        self.click_with_retry_on_overload(self.continue_button)