import pytest
from playwright.sync_api import expect
from pages.all_pages import AllPages


class TestTemplatesPage:

    def test_search_and_filter_templates(self, all_pages: AllPages):
        """
        Test searching for a template and verifying results.
        """
        # Navigate to templates page (usually accessible from project page or direct URL)
        # Using project page to navigate
        all_pages.project_page.create_new_funnel_with_template()

        # Search for a specific topic
        search_term = "Quiz"
        all_pages.templates_page.search_template(search_term)

        # Verify results exist
        expect(all_pages.templates_page.TEMPLATE_CARDS.first).to_be_visible()
        count = all_pages.templates_page.get_template_count()
        assert count > 0, f"No templates found for '{search_term}'"

    def test_create_project_from_template(self, all_pages: AllPages):
        """
        Test creating a new project by selecting a template.
        """
        ws_name = "Template Workspace"
        all_pages.project_page.create_new_workspace(ws_name)
        all_pages.project_page.go_to_workspace(ws_name)

        all_pages.project_page.create_new_funnel_with_template()

        # Just pick the first available template
        all_pages.templates_page.choose_first_template()
        all_pages.templates_page.confirm_template_name(ws_name)

        # Checking if we are redirected to editor:
        expect(all_pages.editor_page.page).to_have_url(lambda url: "/editor/" in url)

        # Cleanup can happen in fixture or verify created
        all_pages.project_page.goto_project_page()
        all_pages.project_page.go_to_workspace(ws_name)
        assert all_pages.project_page.get_funnel_count_from_ws_list(ws_name) >= 1
