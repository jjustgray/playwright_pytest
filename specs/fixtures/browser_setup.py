import logging
import re
import time

import allure
import pytest
from playwright.sync_api import Page


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
        "accept_downloads": True,
        "locale": "en-US",
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
        },
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed and report.when in ("setup", "call"):
        page: Page = item.funcargs.get("page")
        if page and not page.is_closed():
            try:
                screenshot = page.screenshot(full_page=True, timeout=5000)
                allure.attach(
                    screenshot,
                    name=f"failure_screenshot_{report.when}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as error:
                logging.warning(f"Failed to capture failure screenshot: {error}")


@pytest.fixture(autouse=True)
def block_ads(page: Page):
    page.route(
        re.compile(
            r".*(googleads|pagead2|doubleclick|googlesyndication|adservice|adsystem).*"
        ),
        lambda route: route.abort(),
    )

    page.add_init_script("""
        const style = document.createElement('style');
        style.innerHTML = `
            iframe[id^="aswift_"],
            iframe[src*="googleads"],
            div[id^="google_ads"],
            .adsbygoogle,
            #dismiss-button,
            .grippy-host,
            [aria-label="Advertisement"],
            #google_esf {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
                width: 0px !important;
                height: 0px !important;
            }
        `;
        document.head.appendChild(style);

        setInterval(() => {
            const vignettes = document.querySelectorAll('iframe[src*="googleads"], #dismiss-button');
            vignettes.forEach(el => el.remove());
        }, 500);
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
