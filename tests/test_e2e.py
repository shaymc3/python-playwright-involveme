import allure
import pytest
from playwright.sync_api import expect

from pages.editor_page import EditorPage
from pages.project_page import ProjectPage
from pages.all_pages import AllPages


class TestE2E:

    @allure.title("E2E Workflow: Create Workspace, Funnel, and Publish")
    @allure.description("This test covers the end-to-end workflow of creating a workspace, adding a funnel from scratch, adding elements to it, and publishing it.")
    @allure.epic("End-to-End Tests")
    @allure.feature("Core Funnel Workflow")
    @allure.story("Successful Funnel Creation and Publication")
    @pytest.mark.e2e
    def test_create_ws_funnel_and_publish_workflow(self, all_pages: AllPages, project_page: ProjectPage, editor_page:EditorPage):
        ws_name = "test_workflow_1"
        ful_name = "My Funnel"

        project_page.create_new_workspace(ws_name)
        project_page.wait_for_page_load()
        project_page.create_new_funnel_from_scratch(ful_name, "Answer-based Outcomes")

        expect(editor_page.FUNNEL_NAME_TITLE).to_have_text(ful_name)
        expect(editor_page.WORKSPACE_TITLE).to_have_text(ws_name)

        editor_page.add_element_and_close("Single Choice")
        editor_page.add_element_and_close("Dropdown")
        editor_page.add_element_and_close("Yes/No")

        # After adding two elements, the editor automatically adds a "Next" button. so the count should be 4
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(4)

        editor_page.publish_funnel()

        project_page.goto_project_page()
        project_page.go_to_workspace(ws_name)
        ws_list_count = project_page.get_funnel_count_from_ws_list(ws_name)
        expect(project_page.FUNNEL_TITLES_LIST).to_have_count(ws_list_count)

        project_page.goto_funnel_status("Published")
        expect(project_page.FUNNEL_TITLES_LIST).to_have_count(1)

        publish_page = project_page.open_publish_new_page(ful_name)
        expect(publish_page.ELEMENTS_LIST).to_have_count(4)

        publish_page.page.close()

    @allure.title("E2E Workflow: Funnel Page Manipulation")
    @allure.description("This test covers creating a funnel and manipulating its pages (add, rename).")
    @allure.epic("End-to-End Tests")
    @allure.feature("Funnel Page Management")
    @allure.story("Page Manipulation in Editor")
    @pytest.mark.e2e
    def test_funnel_page_manipulation_workflow(self, all_pages: AllPages):
        ws_name = "test_workflow_2"
        funnel_name = "Multi-Page Funnel"

        all_pages.project_page.create_new_workspace(ws_name)
        all_pages.project_page.go_to_workspace(ws_name)

        all_pages.project_page.create_new_funnel_from_scratch(funnel_name, "Answer-based Outcomes")
        expect(all_pages.editor_page.PAGE_LIST).to_have_count(1)

        initial_count = all_pages.editor_page.get_funnel_pages_count()
        all_pages.editor_page.add_funnel_page()
        all_pages.editor_page.add_funnel_page(after_page=initial_count + 1)

        expected_count = initial_count + 2
        expect(all_pages.editor_page.PAGE_LIST).to_have_count(expected_count)

        new_page_name = "Renamed Page"
        last_page_index = expected_count
        all_pages.editor_page.edit_funnel_page_name(last_page_index, new_page_name)

        expect(all_pages.editor_page.PAGE_LIST.nth(expected_count - 1)).to_contain_text(new_page_name)

        all_pages.project_page.goto_project_page()
        all_pages.project_page.go_to_workspace(ws_name)

        assert funnel_name in all_pages.project_page.get_all_funnel_titles()
