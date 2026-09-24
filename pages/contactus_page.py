import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class ContactUsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.getintouch_heading = page.get_by_role(
            "heading", name="Get In Touch", exact=True)
        self.name_input = page.locator(
            'form[action="/contact_us"]').get_by_role("textbox", name="name")
        self.email_input = page.locator(
            'form[action="/contact_us"]').get_by_role("textbox", name="email")
        self.subject_input = page.locator(
            'form[action="/contact_us"]').get_by_role("textbox", name="subject")
        self.message_input = page.locator(
            'form[action="/contact_us"]').get_by_role("textbox", name="message")
        self.file_upload_input = page.locator('input[name="upload_file"]')
        self.submit_button = page.get_by_role('button', name="submit")
        self.success_message = page.locator(
            "#contact-page").get_by_text("Success! Your details have")

    @allure.step("Fill Get In Touch form")
    def fill_form(self, user_data: dict):
        self.name_input.fill(user_data["name"])
        self.email_input.fill(user_data["email"])
        self.subject_input.fill(user_data["subject"])
        self.message_input.fill(user_data["message"])

    @allure.step("Upload file to form")
    def upload_file(self, file_path: str):
        self.file_upload_input.set_input_files(file_path)

    @allure.step("Click Submit Button")
    def click_submit_button(self):
        def handle_dialog(dialog):
            with allure.step("Click OK button in modal window"):
                if dialog.message == "Press OK to proceed!":
                    dialog.accept()
                else:
                    dialog.dismiss()
                    raise ValueError(
                        f"Unexpected dialog message: {dialog.message}")

        self.page.once("dialog", handle_dialog)
        self.click_with_retry_on_overload(self.submit_button)
