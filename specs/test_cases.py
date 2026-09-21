import allure
import pytest
from pages.test_cases_page import TestCasesPage

@allure.epic("Automation Exercise")
@allure.feature("Test Cases Page")
class TestCasesSuite:

    @allure.story("Проверка видимости списка всех тест-кейсов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_verify_test_cases_page_loaded(self, page):
        test_cases_page = TestCasesPage(page)
        
        test_cases_page.navigate()
        test_cases_page.verify_page_loaded()
        
        count = test_cases_page.get_test_cases_count()
        assert count > 0, "Список тест-кейсов пуст!"

    @pytest.mark.parametrize("case_index, expected_title", [
        (0, "Test Case 1: Register User"),
        (1, "Test Case 2: Login User with correct email and password"),
        (2, "Test Case 3: Login User with incorrect email and password"),
    ])
    @allure.story("Параметризованная проверка структуры тест-кейсов")
    def test_verify_individual_test_case(self, page, case_index, expected_title):
        test_cases_page = TestCasesPage(page)
        test_cases_page.navigate()
        test_cases_page.expand_test_case(case_index, expected_title)