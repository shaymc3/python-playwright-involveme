from typing import Literal
from playwright.sync_api import Page
from pages.editor_elements.base_element import BaseElement
from pages.ui_types.types import QuestionTypes, TextChoiceOptions


class TextChoice(BaseElement[TextChoiceOptions]):

    def __init__(self, page: Page):
        super().__init__(page)
        self.QUESTION_TEXTBOX = self.page.get_by_role("textbox", name="Question Text")
        self.DESCRIPTION_TEXTBOX = self.page.get_by_role("textbox", name="Description Text")
        self.HINT_HELP_TEXTBOX = self.page.get_by_role("textbox", name="Hint / Help Text")
        self.CHANGE_QUESTION_TYPE_BTN = self.page.get_by_role(role="button", name="Change question type")

    def change_question_type(self,option: QuestionTypes):
        self.dropdown_options("Change to",option)
        self.click(self.CHANGE_QUESTION_TYPE_BTN)

    def answer_layout_option(self, columns: Literal[1, 2, 3, 4]):
        slider = self.OPTIONS_LIST.get_by_role("slider")
        self.fill(slider, str(columns))

class SingleChoice(TextChoice):
    def __init__(self,page: Page):
        super().__init__(page)
        self.DEFAULT_QUESTION_TEXT = 'Where did you hear about us?'
        self.LAYOUT_TXT = self.OPTIONS_LIST.get_by_text("columns")
        self.ANSWER_TXT_INPUT = self.page.locator("componenttype='5'")

    def get_layout_from_options(self)-> int:
        return int(self.LAYOUT_TXT.inner_text()[:1])

    def get_layout_from_element(self):
        for i in range(1,5):
            layout = self.page.locator(f".v-grid-{i}")
            if layout.count() > 0:
                return i
        return None

class MultipleChoice(TextChoice):
    def __init__(self, page: Page):
        super().__init__(page)
        self.DEFAULT_QUESTION_TEXT = 'What are your two main lead generation goals?'