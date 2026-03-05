import allure
import pytest
from playwright.sync_api import expect

from pages.project_page import ProjectPage


@allure.title("Cleanup: Delete All Workspaces")
@allure.description("This test deletes all existing workspaces to ensure a clean test environment for subsequent runs.")
@allure.epic("Maintenance")
@allure.feature("Environment Setup/Teardown")
@allure.story("Clean Workspace Environment")
@pytest.mark.cleanup
@pytest.mark.order(1)
def test_cleanup(project_page: ProjectPage):
    project_page.delete_all_workspace()
    expect(project_page.WORKSPACE_NAME_LIST).to_have_count(1)
    print("All clean")