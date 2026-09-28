import re

import allure
from playwright.sync_api import Page, expect

from pages.main_page import MainPage
from pages.testcases_page import TestCasesPage


@allure.feature("Test Cases")
class TestTestCases:

    @allure.story("TC-07: Verify Test Cases Page")
    def test_test_cases_page(
        self,
        main_page: MainPage,
        testcases_page: TestCasesPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_test_cases_button()
        expect(page).to_have_url(re.compile(r".*/test_cases(?:#.*)?$"))
        expect(testcases_page.heading).to_be_visible()
