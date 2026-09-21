import allure
from playwright.sync_api import Page, expect

class TestCasesPage:
    def __init__(self, page: Page):
        self.page = page
        self.test_cases_headings = page.locator(".panel-group .panel-title")

    @allure.step("Открыть страницу Test Cases: {url}")
    def navigate(self, url: str = "https://www.automationexercise.com/test_cases"):
        self.page.goto(url)

    @allure.step("Проверить видимость заголовочного блока")
    def verify_page_loaded(self):
        expect(self.page.get_by_role("heading", name="Test Cases")).to_be_visible()

    @allure.step("Получить количество всех тест-кейсов на странице")
    def get_test_cases_count(self) -> int:
        return self.test_cases_headings.count()

    @allure.step("Раскрыть и проверить тест-кейс №{index}: {title_text}")
    def expand_test_case(self, index: int, title_text: str):
        target = self.test_cases_headings.nth(index)
        expect(target).to_contain_text(title_text)
        target.click()