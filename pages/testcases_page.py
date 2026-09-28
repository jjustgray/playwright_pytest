import re

from playwright.sync_api import Page
from pages.base_page import BasePage


class TestCasesPage(BasePage):
    __test__ = False

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name=re.compile(r"^Test Cases$", re.I))
