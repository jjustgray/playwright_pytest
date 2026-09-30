import allure
import pytest
from playwright.sync_api import expect

from pages.main_page import MainPage


@allure.feature("Page Scrolling")
class TestPageScrolling:

    @pytest.mark.regression
    @allure.story("TC-25: Scroll Up Using Arrow")
    def test_scroll_up_using_arrow(self, main_page: MainPage):
        expect(main_page.slider_section).to_be_visible()
        main_page.scroll_to_page_bottom()
        expect(main_page.subscription_heading).to_be_visible()

        main_page.click_scroll_up_button()
        expect(main_page.homepage_heading).to_be_in_viewport()

    @pytest.mark.regression
    @allure.story("TC-26: Scroll Up Without Arrow")
    def test_scroll_up_without_arrow(self, main_page: MainPage):
        expect(main_page.slider_section).to_be_visible()
        main_page.scroll_to_page_bottom()
        expect(main_page.subscription_heading).to_be_visible()

        main_page.scroll_to_page_top()
        expect(main_page.homepage_heading).to_be_in_viewport()
