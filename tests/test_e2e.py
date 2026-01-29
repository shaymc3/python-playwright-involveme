import pytest
from playwright.sync_api import expect
from pages.all_pages import AllPages


class TestE2E:

    @pytest.mark.e2e
    def test_00_workflow(self, all_pages: AllPages):
        ws_name = "Workspace1"
        ws_name2 = "Workspace2"
        ful_name = "My Funnel"

        all_pages.project_page.create_new_workspace(ws_name)
        all_pages.project_page.create_new_workspace(ws_name2)
        all_pages.project_page.go_to_workspace(ws_name)

        assert ws_name in all_pages.project_page.get_all_workspace_titles()

        all_pages.project_page.create_new_funnel_from_scratch(ful_name, "Answer-based Outcomes")

        expect(all_pages.editor_page.FUNNEL_NAME_TITLE).to_have_text(ful_name)
        expect(all_pages.editor_page.WORKSPACE_TITLE).to_have_text(ws_name)

        all_pages.editor_page.add_element_and_close("Single Choice")
        all_pages.editor_page.add_element_and_close("Yes/No")
        all_pages.editor_page.add_element_and_close("Dropdown")

        # After adding two elements, the editor automatically adds a "Next" button. so the count should be 4
        expect(all_pages.editor_page.ADDED_ELEMENTS_LIST).to_have_count(4)

        all_pages.editor_page.publish_funnel()
        all_pages.configue_page.publish_funnel()

        all_pages.project_page.goto_project_page()
        all_pages.project_page.go_to_workspace(ws_name)
        ws_list_count = all_pages.project_page.get_funnel_count_from_ws_list(ws_name)
        expect(all_pages.project_page.FUNNEL_TITLES_LIST).to_have_count(ws_list_count)

        all_pages.project_page.goto_funnel_status("Published")
        expect(all_pages.project_page.FUNNEL_TITLES_LIST).to_have_count(1)

        publish_page = all_pages.project_page.open_publish_new_page(ful_name)
        expect(publish_page.ELEMENTS_LIST).to_have_count(4)

        publish_page.page.close()

    @pytest.mark.e2e
    def test_funnel_page_manipulation_workflow(self, all_pages: AllPages):
        """
        Test a workflow involving adding, renaming, and deleting pages in the editor.
        """
        ws_name = "Workflow Workspace"
        funnel_name = "Multi-Page Funnel"

        # 1. Create Workspace
        all_pages.project_page.create_new_workspace(ws_name)
        all_pages.project_page.go_to_workspace(ws_name)

        # 2. Create Funnel from scratch
        all_pages.project_page.create_new_funnel_from_scratch(funnel_name, "Answer-based Outcomes")

        # Verify initial state
        # Depending on the funnel type, it might start with 1 page or more. "Answer-based Outcomes" usually has a start page?
        # Let's check count dynamically
        initial_count = all_pages.editor_page.get_funnel_pages_count()
        assert initial_count >= 1

        # 3. Add Pages
        # Add 2 new pages
        all_pages.editor_page.add_funnel_page(after_page=initial_count)
        all_pages.editor_page.add_funnel_page(after_page=initial_count + 1)

        expected_count = initial_count + 2
        assert all_pages.editor_page.get_funnel_pages_count() == expected_count

        # 4. Rename Pages
        # Rename the last added page
        new_page_name = "Renamed Page"
        last_page_index = expected_count
        all_pages.editor_page.edit_funnel_page_name(last_page_index, new_page_name)

        # Verify rename
        # get_funnel_page_name strips the "1. " prefix
        current_name = all_pages.editor_page.get_funnel_page_name(last_page_index)
        assert new_page_name in current_name

        # 5. Delete Page
        # Delete the page we just renamed
        all_pages.editor_page.delete_funnel_page(last_page_index)

        # Verify count decreased
        assert all_pages.editor_page.get_funnel_pages_count() == expected_count - 1

        # 6. Publish Funnel
        all_pages.editor_page.publish_funnel()
        all_pages.configue_page.publish_funnel()

        # 7. Cleanup / Verify in Dashboard
        all_pages.project_page.goto_project_page()
        all_pages.project_page.go_to_workspace(ws_name)

        assert funnel_name in all_pages.project_page.get_all_funnel_titles()
