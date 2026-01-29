import pytest
from playwright.sync_api import expect

from pages import ProjectPage


@pytest.mark.cleanup
def test_cleanup(project_page: ProjectPage):
    project_page.delete_all_workspace()
    expect(project_page.WORKSPACE_NAME_LIST).to_have_count(1)
    print("All clean")