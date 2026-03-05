from playwright.sync_api import Locator, Page
from pages.editor_elements.base_element import BaseElement
from pages.ui_types.types import TextAnswerOptions


class TextAnswer(BaseElement[TextAnswerOptions]):

    def __init__(self, page: Page):
        super().__init__(page)
        self.QUESTION_TEXTBOX = self.page.get_by_role("textbox", name="Question Text")
        self.DESCRIPTION_TEXTBOX = self.page.get_by_role("textbox", name="Description Text")
        self.HINT_HELP_TEXTBOX = self.page.get_by_role("textbox", name="Hint / Help Text")
        self.CHANGE_QUESTION_TYPE_BTN = self.page.get_by_role(role="button", name="Change question type")

class ShortAnswer(TextAnswer):

    def __init__(self, page: Page):
     super().__init__(page)
     self.DEFAULT_QUESTION_TEXT = "Type your answer here"

    def get_by_placeholder(self,placeholder: str) -> Locator:
        return self.page.get_by_placeholder(placeholder)