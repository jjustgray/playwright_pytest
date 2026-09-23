import time
import allure
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.signup_page import SignupPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, browser_name):
    if browser_name == "chromium":
        return {
            **browser_type_launch_args,
            "args": [
                "--disable-features=Translate,TranslateUI",
                "--disable-translate",
                "--disable-extensions",
                "--lang=en-US",
            ],
        }
    return browser_type_launch_args

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "en-US",
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
        },
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture(autouse=True)
def block_ads(page: Page):
    ad_patterns = [
        "**/*googleads*",
        "**/*pagead*",
        "**/*doubleclick*",
        "**/*adservice*",
        "**/zrt_lookup_*",
        "**/*googlesyndication*",
    ]
    for pattern in ad_patterns:
        page.route(pattern, lambda route: route.abort())

    page.add_init_script("""
        const style = document.createElement('style');
        style.innerHTML = `
            ins.adsbygoogle, 
            iframe[id^="aswift_"], 
            [id^="google_ads"], 
            #click-protector,
            .grippy-host {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
                height: 0 !important;
                width: 0 !important;
            }
        `;
        document.head.appendChild(style);
    """)


@pytest.fixture(autouse=True)
def setup_page(page: Page):
    max_retries = 3
    retry_delay = 3

    page.goto("/")

    for attempt in range(max_retries):
        is_overloaded = (
            page.locator("body")
            .filter(has_text="This website is under heavy load (queue full)")
            .count()
            > 0
        )

        if is_overloaded:
            if attempt < max_retries - 1:
                print(
                    f"\n[WARNING] Website under heavy load. Attempt {attempt + 1}/{max_retries}. Waiting {retry_delay}s..."
                )
                time.sleep(retry_delay)
                page.reload(wait_until="domcontentloaded")
            else:
                pytest.fail(
                    "The website is under heavy load and did not recover after several attempts."
                )
        else:
            break

    yield


@pytest.fixture
def main_page(page: Page) -> MainPage:
    return MainPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def signup_page(page: Page) -> SignupPage:
    return SignupPage(page)