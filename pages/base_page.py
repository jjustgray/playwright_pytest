import time
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def remove_ad_overlays(self):
        self.page.evaluate("""
            () => {
                document.querySelectorAll('ins.adsbygoogle, iframe[id^="aswift_"], #click-protector').forEach(el => el.remove());
            }
        """)

    def click_with_retry_on_overload(self, locator: Locator, max_retries: int = 3):
        for attempt in range(max_retries):
            locator.click()
            if "This website is under heavy load (queue full)" in self.page.content().lower():
                if attempt < max_retries - 1:
                    time.sleep(2)
                    self.page.reload()
                else:
                    raise Exception(
                        "The website is under heavy load and did not recover after several attempts.")
            else:
                break
