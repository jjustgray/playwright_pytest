import re
import uuid

import allure
from playwright.sync_api import Page, expect

from pages.main_page import MainPage


@allure.feature("Subscription")
class TestSubscription:

    @allure.story("TC-10: Verify Subscription in Home Page")
    def test_subscription_on_home_page(self, main_page: MainPage):
        expect(main_page.slider_section).to_be_visible()
        main_page.scroll_to_subscription()
        expect(main_page.subscription_heading).to_be_visible()
        main_page.subscribe_to_newsletter(
            f"subscriber_{uuid.uuid4().hex}@example.com")
        expect(main_page.subscription_success_message).to_contain_text(
            "You have been successfully subscribed!")

    @allure.story("TC-11: Verify Subscription in Cart Page")
    def test_subscription_on_cart_page(
        self,
        main_page: MainPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_cart_button()
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        main_page.scroll_to_subscription()
        expect(main_page.subscription_heading).to_be_visible()
        main_page.subscribe_to_newsletter(
            f"subscriber_{uuid.uuid4().hex}@example.com")
        expect(main_page.subscription_success_message).to_be_visible()
        expect(main_page.subscription_success_message).to_contain_text(
            "You have been successfully subscribed!")
