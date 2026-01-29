
from typing import List

import pytest
from playwright.sync_api import expect
from pages import EditorPage, ProjectPage
from pages.ui_types.types import Elements


class TestEditorPage:

    @pytest.fixture(autouse=False)
    def create_new_funnel_each_test(self,project_page: ProjectPage,editor_page:EditorPage):
        ws_name = "Editor Tests"
        if ws_name not in project_page.get_all_workspace_titles():
            project_page.create_new_workspace(ws_name)

        project_page.go_to_workspace(ws_name)
        funnel_counter = project_page.get_funnel_count_from_ws_list(ws_name)

        funnel_name = f"funnel-{funnel_counter:02d}"
        project_page.create_new_funnel_from_scratch(funnel_name, "Thank You page")
        expect(editor_page.ELEMENT_BTN_LIST.nth(5)).to_be_visible()


        self.funnel_name = funnel_name
        yield

    def test_assert_page_title(self,editor_page:EditorPage):
        expect(editor_page.page).to_have_title("Editor | involve.me")

    def test_add_one_element(self,editor_page: EditorPage):
        before_count = editor_page.get_all_added_elements_count()
        editor_page.add_element_and_close("Single Choice")

        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(before_count+1)
        assert editor_page.single_choice.get_element_title() == editor_page.single_choice.DEFAULT_NAME

    def test_add_and_delete_2_element(self,editor_page: EditorPage):
        editor_page.add_element_and_close("Yes/No")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(1)

        editor_page.add_element_and_close("Slider")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(3)

        before_count = editor_page.get_all_added_elements_count()
        editor_page.delete_element(0)
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(before_count - 1)

    def test_10_add_and_delete_elements(self, editor_page: EditorPage):
        expect(editor_page.ELEMENT_BTN_LIST.nth(5)).to_be_visible()
        elements: List[Elements] = ["Yes/No","Slider","Rating","Heading","Image + Text","Dropdown","Single Image Choice"]
        editor_page.add_elements(elements)
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(len(elements)+1)

        editor_page.delete_all_elements()
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(0)

    def test_edit_name(self,editor_page:EditorPage):
        editor_page.goto_funnel_edit_page("funnel-00")
        editor_page.add_element_and_edit("Single Choice")
        editor_page.single_choice.answer_layout_option(4)
        editor_page.single_choice.toggle_option("Individual Score & Calculation", "on")
        editor_page.single_choice.toggle_option("Randomize answers", "on")
        editor_page.single_choice.toggle_option("Hide question text for participants", "on")
        editor_page.single_choice.toggle_option("Answer is required","on")
        editor_page.single_choice.toggle_option("Always Hide for participants", "on")



