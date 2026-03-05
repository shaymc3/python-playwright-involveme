from typing import Generic, Literal, TypeVar

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.ui_types.types import ElementTextBox

OptionT = TypeVar("OptionT", bound=str)

class BaseElement(Generic[OptionT],BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.ELEMENT_LIST = self.page.locator("[data-index]")
        self.OPTIONS_LIST = self.page.locator(".edit-block-section")
        self.ELEMENT_QUESTION_TXT = self.ELEMENT_LIST.locator("h1 > span")
        self.ELEMENT_DESCRIPTION_TXT = self.ELEMENT_LIST.locator("h2")
        self.ELEMENT_HINT_TXT = self.ELEMENT_LIST.locator(".break-words")

    def edit_text_block(self, block_name:ElementTextBox, text: str) -> None:
        locator = self.page.get_by_role("textbox", name=block_name)
        self.fill(locator,text)

    def toggle_option(self, option_label: OptionT, state:Literal["on", "off"]) -> None:
        toggle_button = self.OPTIONS_LIST.get_by_text(option_label)
        toggle_state_locator = self.page.get_by_label(option_label)
        toggle_state = toggle_state_locator.get_attribute("value")
        if (toggle_state == "true") != (state == "on"):
            self.click(toggle_button)

    def input_option(self,option_label: OptionT,text: str):
        option = self.OPTIONS_LIST.get_by_text(option_label)
        self.fill(option,text)

    #TODO: Add type hints
    def dropdown_options(self,dropdown_label: str, option: str):
        dropdown = self.OPTIONS_LIST.locator(f"label:has-text('{dropdown_label}')+ div").get_by_role(role="combobox")
        dropdown.click()
        opt = self.filter(self.OPTIONS_LIST.get_by_role(role="option"), option)
        self.click(opt)

    def get_element_title(self,index: int = -1):
        self.page.wait_for_load_state("networkidle")
        return self.ELEMENT_QUESTION_TXT.nth(index).inner_text()