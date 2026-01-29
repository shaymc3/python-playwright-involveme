from time import sleep

import pytest

from playwright.sync_api import Page, expect

import config
from pages import LoginPage, ProjectPage, EditorPage, ConfigurePage
from pages.all_pages import AllPages
from pages.publish_page import PublishPage
from utils.effects import show_overlay

AUTH_FILE = "playwright/.auth/auth.json"


@pytest.fixture(autouse=True)
def setup(page:Page,playwright):
    playwright.selectors.set_test_id_attribute("data-intercom-target")
    page.add_locator_handler(
        page.locator("#popup-container"),
        lambda: page.locator("#embed-popup-close").click()
    )
    page.goto(config.BASE_URL)
    if config.PROJECTS_URL in page.url:
        return
    else:
        show_overlay(page, "user is disconnected, starting login process", "RUNNING")

        login_page = LoginPage(page)
        login_page.login(config.USER_EMAIL, config.USER_PASSWORD)

        login_page.page.wait_for_url(config.PROJECTS_URL)
        expect(login_page.page).to_have_url(config.PROJECTS_URL)

        login_page.page.context.storage_state(path=AUTH_FILE)

        show_overlay(page, "setup success, starting tests", "PASS")
        sleep(2)

@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": AUTH_FILE,
        "no_viewport": True,
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
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

@pytest.fixture(scope="function")
def publish_page_temp(page: Page,setup):
    page.goto("https://shay30.involve.me/my-funnel-0e10")
    return PublishPage(page)

@pytest.fixture
def editor_page(page: Page):
    return EditorPage(page)

@pytest.fixture(autouse=True)
def test_overlay_start(request, page):
    test_name = request.node.name
    show_overlay(page, test_name, "RUNNING")
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        page = item.funcargs.get("page")
        if page:
            if rep.passed:
                show_overlay(page, item.name, "PASS")
            elif rep.failed:
                show_overlay(page, item.name, "FAIL")
            page.wait_for_timeout(2000)