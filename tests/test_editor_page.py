
from typing import List

import allure
import pytest
from playwright.sync_api import expect

from pages.editor_page import EditorPage
from pages.project_page import ProjectPage
from pages.ui_types.types import Elements, QuestionTypes


class TestEditorPage:

    @pytest.fixture()
    def create_new_funnel(self, project_page: ProjectPage, editor_page:EditorPage,request):
        ws_name = "Editor Tests"
        if ws_name not in project_page.get_all_workspace_titles():
            project_page.create_new_workspace(ws_name)

        project_page.go_to_workspace(ws_name)
        project_page.get_funnel_count_from_ws_list(ws_name)

        # funnel_name = f"funnel-{funnel_counter:02d}".
        funnel_name = request.node.name[:-10]
        if funnel_name not in project_page.get_all_funnel_titles():
            project_page.create_new_funnel_from_scratch(funnel_name, "Thank You page")
        else:
            project_page.funnel_dropdown_menu_option(funnel_name,"Edit")



        # self.funnel_name = funnel_name
        yield

    @allure.title("Editor Page: Assert Page Title")
    @allure.description("This test verifies that the editor page has the correct title.")
    @allure.epic("Project Editor")
    @allure.feature("Page Loading")
    @allure.story("Verify Page Title")
    @pytest.mark.ui
    def test_assert_page_title(self,editor_page:EditorPage,create_new_funnel):
        expect(editor_page.page).to_have_title("Editor | involve.me")

    @allure.title("Editor Page: Add Single Element")
    @allure.description("This test verifies that a single element can be added to the editor and the element count increases.")
    @allure.epic("Project Editor")
    @allure.feature("Element Manipulation")
    @allure.story("Add Element")
    @pytest.mark.ui
    def test_add_one_element(self, editor_page: EditorPage, create_new_funnel):
        before_count = editor_page.get_all_added_elements_count()
        editor_page.add_element_and_close("Single Choice")

        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(before_count+1)
        assert editor_page.single_choice.get_element_title() == editor_page.single_choice.DEFAULT_QUESTION_TEXT

    @allure.title("Editor Page: Add and Delete Two Elements")
    @allure.description("This test verifies adding two elements and then deleting one, checking the element count at each step.")
    @allure.epic("Project Editor")
    @allure.feature("Element Manipulation")
    @allure.story("Add and Delete Elements")
    @pytest.mark.ui
    def test_add_and_delete_2_elements(self, editor_page: EditorPage, create_new_funnel):
        editor_page.add_element_and_close("Yes/No")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(1)

        editor_page.add_element_and_close("Slider")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(3)

        before_count = editor_page.get_all_added_elements_count()
        editor_page.delete_element(1)
        editor_page.delete_element(0)
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(before_count - 2)

    @allure.title("Editor Page: Add and Delete Multiple Elements")
    @allure.description("This test verifies adding multiple different elements and then deleting all of them.")
    @allure.epic("Project Editor")
    @allure.feature("Element Manipulation")
    @allure.story("Bulk Add and Delete Elements")
    @pytest.mark.ui
    def test_add_and_remove_batch_elements(self, editor_page: EditorPage, create_new_funnel):
        expect(editor_page.ELEMENT_BTN_LIST.nth(5)).to_be_visible()
        elements: List[Elements] = ["Yes/No","Slider","Rating","Heading","Image + Text","Dropdown","Single Image Choice"]
        editor_page.add_elements(elements)
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(len(elements)+1)

        editor_page.delete_all_elements()
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(0)

    @allure.title("Editor Page: Change Question Type")
    @allure.description("This test verifies that the question type of an element can be changed.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Change Element Type")
    @pytest.mark.ui
    def test_change_question_type(self, editor_page:EditorPage, create_new_funnel):
        question_type: QuestionTypes = "Text Choice"
        new_question_type: QuestionTypes = "Image Choice"

        editor_page.add_element_and_edit("Single Choice")
        expect(editor_page.ELEMENT_TYPE_NAME).to_contain_text(question_type)
        assert editor_page.single_choice.get_element_title() == editor_page.single_choice.DEFAULT_QUESTION_TEXT

        editor_page.single_choice.change_question_type(new_question_type)
        expect(editor_page.ELEMENT_TYPE_NAME).to_contain_text(new_question_type)

        assert editor_page.get_element_type() == new_question_type

    @allure.title("Editor Page: Edit Text Block of a 'Single_choice' Element")
    @allure.description("This test navigates to a specific funnel and edits the text block of a 'Single Choice' element.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Edit Element Content")
    @pytest.mark.ui
    def test_single_choice_edit_question_text(self, editor_page:EditorPage, create_new_funnel):
        editor_page.add_element_and_edit("Single Choice")
        text = "What is your dream?"
        editor_page.single_choice.edit_text_block("Question Text",text)

        assert text in editor_page.single_choice.ELEMENT_QUESTION_TXT.all_inner_texts()

    @allure.title("Editor Page: Edit 'Single Choice' Description")
    @allure.description("This test verifies that the description text of a 'Single Choice' element can be edited.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Edit Element Content")
    @pytest.mark.ui
    def test_single_choice_edit_description_test(self, editor_page:EditorPage, create_new_funnel):
        editor_page.add_element_and_edit("Single Choice")
        text = "What is your dream?"
        editor_page.single_choice.edit_text_block("Description Text", text)

        expect(editor_page.single_choice.ELEMENT_DESCRIPTION_TXT.first).to_contain_text(text)

    @allure.title("Editor Page: Edit 'Single Choice' Hint Text")
    @allure.description("This test verifies that the hint/help text of a 'Single Choice' element can be edited.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Edit Element Content")
    @pytest.mark.ui
    def test_single_choice_edit_hint_text(self, editor_page:EditorPage, create_new_funnel):
        editor_page.add_element_and_edit("Single Choice")
        text = "What is your dream?"
        editor_page.single_choice.edit_text_block("Hint / Help Text", text)
        expect(editor_page.single_choice.ELEMENT_HINT_TXT).to_contain_text(text)


    @allure.title("Editor Page: Hide 'Single Choice' Question Text")
    @allure.description("This test verifies that the question text of a 'Single Choice' element can be hidden.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Toggle Element Visibility")
    @pytest.mark.ui
    def test_single_choice_hide_question_text(self, editor_page:EditorPage, create_new_funnel):
        editor_page.add_element_and_edit("Single Choice")
        editor_page.single_choice.toggle_option("Hide question text for participants","on")

        assert editor_page.single_choice.DEFAULT_QUESTION_TEXT not in editor_page.single_choice.ELEMENT_QUESTION_TXT.all_inner_texts()

    @allure.title("Editor Page: Change 'Single Choice' Answer Layout")
    @allure.description("This test verifies that the answer layout of a 'Single Choice' element can be changed.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Change Element Layout")
    @pytest.mark.ui
    def test_change_single_choice_layout(self, editor_page:EditorPage, create_new_funnel):
        editor_page.add_element_and_edit("Single Choice")
        editor_page.single_choice.answer_layout_option(3)
        expect(editor_page.single_choice.LAYOUT_TXT).to_contain_text("3")

        a = editor_page.single_choice.get_layout_from_element()
        b =editor_page.single_choice.get_layout_from_options()
        assert a == b

    @allure.title("Editor Page: Use 'Short Answer' Question as Placeholder")
    @allure.description("This test verifies that the question of a 'Short Answer' element can be used as a placeholder.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Change Element Display")
    @pytest.mark.ui
    def test_short_answer_question_as_placeholder(self, editor_page:EditorPage, create_new_funnel):
        question = "What are you doing here?"
        editor_page.add_element_and_edit("Short Answer")
        editor_page.short_answer.edit_text_block("Question Text",question)
        editor_page.short_answer.toggle_option("Use question as placeholder","on")

        assert editor_page.short_answer.get_by_placeholder(question)

    @allure.title("Editor Page: Change 'Slider' Element Range")
    @allure.description("This test verifies that the min, max, and start values of a 'Slider' element can be changed.")
    @allure.epic("Project Editor")
    @allure.feature("Element Properties")
    @allure.story("Edit Element Range")
    @pytest.mark.ui
    def test_slider_range_change(self, editor_page:EditorPage, create_new_funnel):
        min_range = -373
        max_range = 435
        start = 120

        editor_page.add_element_and_edit("Slider")
        editor_page.slider.input_option("Min Value",str(min_range))
        editor_page.slider.input_option("Max Value", str(max_range))
        editor_page.slider.input_option("Start Value", str(start))

        assert  editor_page.slider.get_start() == start
        assert  editor_page.slider.get_max() == max_range
        assert  editor_page.slider.get_min() == min_range

    @allure.title("Editor Page: Drag and Drop Element")
    @allure.description("This test verifies that an element can be added to the canvas via drag and drop.")
    @allure.epic("Project Editor")
    @allure.feature("Element Manipulation")
    @allure.story("Add Element via Drag and Drop")
    @pytest.mark.ui
    def test_drag_and_drop_element(self, editor_page:EditorPage, create_new_funnel):
        count_before = editor_page.get_all_added_elements_count()
        editor_page.drag_element_to("Slider",-1)
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(count_before + 2)

        assert editor_page.slider.get_element_title(-1) == editor_page.slider.DEFAULT_QUESTION_TEXT

    @allure.title("Editor Page: Add Funnel Page")
    @allure.description("This test verifies that a new page can be added to a funnel.")
    @allure.epic("Project Editor")
    @allure.feature("Funnel Pages")
    @allure.story("Add Page")
    @pytest.mark.ui
    def test_add_funnel_page(self, editor_page: EditorPage, create_new_funnel):
        initial_pages_count = editor_page.get_funnel_pages_count()
        editor_page.add_funnel_page()
        expect(editor_page.PAGE_LIST).to_have_count(initial_pages_count + 1)

    @allure.title("Editor Page: Delete Funnel Page")
    @allure.description("This test verifies that a page can be deleted from a funnel.")
    @allure.epic("Project Editor")
    @allure.feature("Funnel Pages")
    @allure.story("Delete Page")
    @pytest.mark.ui
    def test_delete_funnel_page(self, editor_page: EditorPage, create_new_funnel):
        initial_pages_count = editor_page.get_funnel_pages_count()
        editor_page.add_funnel_page()
        expect(editor_page.PAGE_LIST).to_have_count(initial_pages_count + 1)

        editor_page.delete_funnel_page(2) 
        expect(editor_page.PAGE_LIST).to_have_count(initial_pages_count)

    @allure.title("Editor Page: Edit Funnel Page Name")
    @allure.description("This test verifies that the name of a funnel page can be edited.")
    @allure.epic("Project Editor")
    @allure.feature("Funnel Pages")
    @allure.story("Edit Page Name")
    @pytest.mark.ui
    def test_edit_funnel_page_name(self, editor_page: EditorPage, create_new_funnel):
        new_name = "My Awesome New Page Name"
        editor_page.edit_funnel_page_name(1, new_name)
        
        page_name = editor_page.get_funnel_page_name(1)
        assert page_name == new_name
