
import allure
import pytest
from playwright.sync_api import expect

from pages.editor_page import EditorPage
from pages.project_page import ProjectPage


@pytest.mark.ui
@allure.epic("Preview")
@allure.feature("Content Elements")
@allure.story("Interactive Elements")
class TestPreviewPage:

    @pytest.fixture(autouse=True)
    def create_new_funnel(self, project_page: ProjectPage, editor_page: EditorPage, request):
        ws_name = "Preview Tests"
        if ws_name not in project_page.get_all_workspace_titles():
            project_page.create_new_workspace(ws_name)

        project_page.go_to_workspace(ws_name)

        # Use test name as funnel name
        funnel_name = request.node.name[:-10]

        self.ws_name = ws_name
        self.funnel_name = funnel_name
        if funnel_name not in project_page.get_all_funnel_titles():
            project_page.create_new_funnel_from_scratch(funnel_name, "Answer-based Outcomes")
        else:
            project_page.funnel_dropdown_menu_option(funnel_name, "Edit")
        yield

    @allure.title("Preview: Slider and Yes/No elements")
    @allure.description("Verify that Slider and Yes/No elements work correctly in the preview mode.")
    def test_preview_slider_and_yes_no(self, editor_page: EditorPage, project_page: ProjectPage):
        editor_page.delete_all_elements()
        editor_page.add_elements(["Slider", "Yes/No"])
        project_page.goto_project_page()
        project_page.go_to_workspace(self.ws_name)
        preview_page = project_page.open_publish_new_page(self.funnel_name)

        preview_page.set_slider_to(11)
        preview_page.click_on("No")
        preview_page.click_on("Next")

        expect(preview_page.THANKS_MSG).to_be_attached()
        assert preview_page.get_total_page_number() == preview_page.get_current_page_number()

    @allure.title("Preview: Yes/No element")
    @allure.description("Verify that a Yes/No element works correctly in the preview mode.")
    def test_preview_yes_no(self, editor_page: EditorPage, project_page: ProjectPage):
        editor_page.delete_all_elements()
        editor_page.add_element_and_close("Yes/No")
        project_page.goto_project_page()
        project_page.go_to_workspace(self.ws_name)
        preview_page = project_page.open_publish_new_page(self.funnel_name)

        preview_page.click_on("Yes")
        expect(preview_page.THANKS_MSG).to_be_visible()
        assert preview_page.get_total_page_number() == preview_page.get_current_page_number()

    @allure.title("Preview: Dropdown and Short Answer elements")
    @allure.description("Verify that Dropdown and Short Answer elements work correctly in the preview mode.")
    def test_preview_dropdown_and_short_answer(self, editor_page: EditorPage, project_page: ProjectPage):
        editor_page.delete_all_elements()
        editor_page.add_elements(["Dropdown", "Short Answer"])
        project_page.goto_project_page()
        project_page.go_to_workspace(self.ws_name)
        preview_page = project_page.open_publish_new_page(self.funnel_name)

        preview_page.select_option_from_dropdown("Growing steadily")
        preview_page.fill_text("Sample Answer")

        preview_page.click_on("Next")
        expect(preview_page.THANKS_MSG).to_be_visible()
        assert preview_page.get_total_page_number() == preview_page.get_current_page_number()

    @allure.title("Preview: Multiple Image Choice and Rating elements")
    @allure.description("Verify that Multiple Image Choice and Rating elements work correctly in the preview mode.")
    def test_preview_multiple_image_choice_and_rating(self, editor_page: EditorPage, project_page: ProjectPage):
        editor_page.delete_all_elements()
        editor_page.add_elements(["Multiple Image Choice", "Rating"])
        project_page.goto_project_page()
        project_page.go_to_workspace(self.ws_name)
        preview_page = project_page.open_publish_new_page(self.funnel_name)

        preview_page.click_on("Instagram")

        preview_page.click_on("Next")
        expect(preview_page.THANKS_MSG).to_be_visible()
        assert preview_page.get_total_page_number() == preview_page.get_current_page_number()
