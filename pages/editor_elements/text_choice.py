from typing import Literal

from pages.base_page import BasePage
from pages.ui_types.types import TextChoiceOptions


class TextChoice(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.ELEMENTS = self.page.locator("[data-index]")
        self.QUESTION_TEXTBOX = self.page.get_by_role("textbox", name="Question Text")
        self.DESCRIPTION_TEXTBOX = self.page.get_by_role("textbox", name="Description Text")
        self.HINT_HELP_TEXTBOX = self.page.get_by_role("textbox", name="Hint / Help Text")
        self.OPT_BTN = self.page.get_by_role(role="button",name="Options")
        self.BTN = self.page.get_by_label(text="Hide question text for participants")
        self.OPTIONS = self.page.locator(".edit-block-section")
        self.ELEMENT_TITLE = self.ELEMENTS.get_by_role(role="heading")

    def edit_question_text(self, text):
        self.fill(self.QUESTION_TEXTBOX, text)

    def edit_description_text(self, text):
        self.fill(self.DESCRIPTION_TEXTBOX, text)

    def edit_HINT_HELP_text(self, text):
        self.fill(self.HINT_HELP_TEXTBOX, text)

    def toggle_option(self,option:TextChoiceOptions,state:Literal["on","off"]):
        toggle_button = self.OPTIONS.get_by_text(option)
        toggle_state_locator = self.page.get_by_label(option)
        # return true or false
        toggle_state = toggle_state_locator.get_attribute("value")
        if (toggle_state == "true") != (state == "on"):
            self.click(toggle_button)

    def answer_layout_option(self,columns:Literal[1, 2, 3, 4]):
        slider = self.OPTIONS.get_by_role("slider")
        self.fill(slider,columns)

    def get_element_title(self,index: int = 1):
        index = index-1
        return self.ELEMENT_TITLE.nth(index).inner_text()

class SingleChoice(TextChoice):
    def __init__(self,page):
        super().__init__(page)
        self.DEFAULT_NAME = 'Where did you hear about us?'

class MultipleChoice(TextChoice):
    def __init__(self, page):
        super().__init__(page)
        self.DEFAULT_NAME = 'What are your two main lead generation goals?'
