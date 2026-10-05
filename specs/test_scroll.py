import allure
import pytest
from playwright.sync_api import expect

from pages.main_page import MainPage


@allure.feature("Page Scrolling")
class TestPageScrolling:

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "scroll_up_method, story_title",
        [
            ("click_scroll_up_button", "TC-25: Scroll Up Using Arrow"),
            ("scroll_to_page_top", "TC-26: Scroll Up Without Arrow"),
        ],
        ids=["with_arrow", "without_arrow"],
    )
    def test_scroll_up(
        self,
        main_page: MainPage,
        scroll_up_method: str,
        story_title: str,
    ):
        allure.dynamic.story(story_title)

        expect(main_page.slider_section).to_be_visible()
        main_page.scroll_to_page_bottom()
        expect(main_page.subscription_heading).to_be_visible()

        # Call the scroll up method dynamically based on parameter
        getattr(main_page, scroll_up_method)()
        expect(main_page.homepage_heading).to_be_in_viewport()