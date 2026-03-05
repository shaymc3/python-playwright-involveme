import os
import warnings
import allure
import pytest
import config
from time import sleep
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, expect
from pages.configure_page import ConfigurePage
from pages.editor_page import EditorPage
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from pages.templates_page import TemplatesPage
from pages.all_pages import AllPages
from pages.preview_page import PreviewPage
from utils.effects import show_overlay

# Ensure the directory for auth file exists
AUTH_DIR = os.path.join("playwright", ".auth")
os.makedirs(AUTH_DIR, exist_ok=True)
AUTH_FILE = os.path.join(AUTH_DIR, "auth.json")

# Create auth file if it doesn't exist
if not os.path.exists(AUTH_FILE):
    with open(AUTH_FILE, "w") as f:
        f.write("{}")


@pytest.fixture(autouse=True)
def setup(page:Page,playwright):
    playwright.selectors.set_test_id_attribute("data-intercom-target")

    page.add_locator_handler(
        page.locator(".involveme_embed_popup-container").first,
        lambda: page.locator("#embed-popup-close").click()
    )

    page.goto(config.BASE_URL)
    if config.PROJECTS_URL in page.url:
        return
    else:
        show_overlay(page, "user is disconnected, starting login process", "RUNNING")

        login_page = LoginPage(page)
        login_page.login(config.USER_EMAIL, config.USER_PASSWORD)

        login_page.page.context.storage_state(path=AUTH_FILE)

        show_overlay(page, "setup success, starting tests", "PASS")
        sleep(2)

@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": AUTH_FILE,
        "viewport": {"width": 1920, "height": 1080}
    }



@pytest.fixture(scope="function")
def all_pages(page: Page,setup)-> AllPages:
    return AllPages(page)

@pytest.fixture(scope="function")
def project_page(page: Page,setup) -> ProjectPage:
    return ProjectPage(page)

@pytest.fixture(scope="function")
def configure_page(page: Page,setup) -> ConfigurePage:
    return ConfigurePage(page)

@pytest.fixture
def editor_page(page: Page):
    return EditorPage(page)

@pytest.fixture
def templates_page(page: Page):
    return TemplatesPage(page)

@pytest.fixture
def preview_page(page: Page):
    return PreviewPage(page)


@pytest.fixture(autouse=True)
def test_overlay_start(request, page):
    test_name = request.node.name
    show_overlay(page, test_name, "RUNNING")
    yield

@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call":
        page = item.funcargs.get("page")
        if page:
            if rep.passed:
                try:
                    show_overlay(page, item.name, "PASS")
                except PlaywrightError:
                    pass

            elif rep.failed:
                try:
                    allure.attach(
                        body=page.url,
                        name="URL",
                        attachment_type=allure.attachment_type.URI_LIST,
                    )
                    allure.attach(
                        body=page.screenshot(full_page=True),
                        name="Screen shot on failure",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as e:
                    print(f"Failed to attach screenshot: {e}")
                
                try:
                    show_overlay(page, item.name, "FAIL")
                except PlaywrightError:
                    pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    page = item.funcargs.get("page")
    console_errors = []

    if page:
        def on_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)
                print(f"[Console Error] {msg.text}")

        def on_page_error(exc):
            console_errors.append(f"Uncaught exception: {exc.message}")
            print(f"[Page Error] {exc.message}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

    yield

    if console_errors:
        joined = "\n".join(console_errors)

        allure.attach(
            joined,
            name="Browser Console Errors",
            attachment_type=allure.attachment_type.TEXT
        )

        warnings.warn(
            "Browser console errors detected (see attachment)",
            UserWarning
        )