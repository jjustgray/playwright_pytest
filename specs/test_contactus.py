import os
import allure
from playwright.sync_api import expect, Page

from pages.main_page import MainPage
from pages.contactus_page import ContactUsPage


@allure.feature("Contact Us")
class TestContactUs:

    @allure.story("TC-06: Contact Us Form")
    def test_contactus_form(
        self,
        main_page: MainPage,
        contactus_page: ContactUsPage,
        page: Page
    ):
        file_path = os.path.abspath("specs/fixtures/sample_file.txt")
        expect(main_page.slider_section).to_be_visible()
        main_page.click_contactus_button()
        expect(contactus_page.getintouch_heading).to_be_visible()
        contactus_page.fill_form({
            "name": "Temp User",
            "email": "tempuser@example.com",
            "subject": "Testing",
            "message": "I m testing Contact Us form"
        })
        contactus_page.upload_file(file_path=file_path)
        contactus_page.click_submit_button()
        expect(contactus_page.success_message).to_be_visible()
        main_page.click_home_button()
        expect(main_page.slider_section).to_be_visible()
