from typing import Iterable
from playwright.sync_api import Page, Position, TimeoutError
import config
from .base_page import BasePage
from .editor_elements.slider import Slider
from .editor_elements.text_answer import ShortAnswer
from .editor_elements.text_choice import MultipleChoice, SingleChoice
from .ui_types.types import EditorHeaderOpt, Elements, PageMenuOption


class EditorPage(BasePage):

    def __init__(self,page: Page):
        super().__init__(page)

        # Elements
        self.single_choice: SingleChoice = SingleChoice(page)
        self.multiple_choice: MultipleChoice = MultipleChoice(page)
        self.short_answer: ShortAnswer = ShortAnswer(page)
        self.slider: Slider = Slider(page)
        # Locators
        self.EDITOR_HEADER = self.page.get_by_test_id("project-navigation-top")
        self.EDITOR_HEADER_MENU = self.EDITOR_HEADER.locator(":scope > div").nth(1).locator("a")
        self.PREVIEW_BTN = self.EDITOR_HEADER.locator(":scope > div > a").nth(1)
        self.ELEMENT_BTN_LIST = self.page.get_by_test_id("editor-content-elements").locator(".text-left")
        self.ELEMENT_CLOSE_BTN = self.page.locator("[data-icon='xmark']")
        self.ADDED_ELEMENTS_LIST = self.page.locator("[data-index]")
        self.DELETE_BTN = self.page.locator(".fa-trash")
        self.SAVE_BTN = self.page.get_by_role(role="button",name="Save")
        self.DELETE_CONFIRM_BTN = self.page.locator("[data-danger='true']")
        self.ELEMENT_TYPE_NAME = self.page.locator(".sticky.top-0 >.py-2")
        self.PAGE_LIST = self.page.get_by_test_id("editor-page-navigation-input-pages").locator("div:nth-child(1)")
        self.ADD_PAGE_BTN = self.page.get_by_role("button", name="Add page")
        self.FUNNEL_NAME_TITLE = self.page.locator(".space-x-1.flex div")
        self.FUNNEL_PUBLISH_BTN = self.page.get_by_test_id("publish-button")
        self.FUNNEL_PUBLISH_NOW_BTN = self.page.get_by_role(role="button",name="Publish now")
        self.WORKSPACE_TITLE = self.page.locator(".space-x-1.flex a")
        self.CONFIGURE_BTN = self.page.get_by_test_id("project-navigation-settings")
        self.MAIN_BOARD = self.page.locator(".webfontsloaded svg")
        self.OK_BTN = self.page.get_by_role(role="button", name="OK")

    def goto_funnel_edit_page(self, funnel: str):
        self.page.goto(f"{config.EDITOR_PAGE}/{funnel}")

    def wait_for_page_load(self):
        try:
            self.ADDED_ELEMENTS_LIST.last.wait_for(state="visible", timeout=1500)
            return
        except TimeoutError:
            self.MAIN_BOARD.last.wait_for(state="visible")

    def add_element_and_close(self,element:Elements):
        el = self.filter(self.ELEMENT_BTN_LIST, element).first
        self.click(el)
        self.click(self.ELEMENT_CLOSE_BTN.first)

    def add_element_and_edit(self,element:Elements):
        el = self.filter(self.ELEMENT_BTN_LIST, element).first
        self.click(el)

    def click_on_element(self,index: int):
        el = self.page.locator(f"[data-index='{index}']")
        self.click(el)

    def add_elements(self,elements: Iterable[Elements]):
        for el in elements:
            self.add_element_and_close(el)


    def get_all_added_elements_count(self) -> int:
        self.page.wait_for_load_state("domcontentloaded")
        elements = self.ADDED_ELEMENTS_LIST
        return elements.count()

    def search_element(self,element: str):
        pass

    def delete_element(self,index: int):
        self.click_on_element(index)
        self.click(self.DELETE_BTN)
        self.click(self.DELETE_CONFIRM_BTN)

    def delete_all_elements(self):
        element_count = self.get_all_added_elements_count()
        if element_count > 0:
            self.delete_element(element_count - 1)
            self.delete_all_elements()

    def get_element_type(self):
        el_typ = self.ELEMENT_TYPE_NAME.inner_text()
        return el_typ

    def add_funnel_page(self,after_page: int=1):
        page_num = after_page - 1
        add_after = self.PAGE_LIST.nth(page_num)
        add_after.hover()
        self.click(self.ADD_PAGE_BTN.nth(page_num))

    def funnel_page_dropdown_menu_option_choose(self,page_number: int,option:PageMenuOption):
        page_num = page_number - 1
        page_to_delete = self.PAGE_LIST.nth(page_num)
        page_to_delete.hover()
        self.click(page_to_delete.locator("+div > button").nth(0))
        chosen_option = self.page.get_by_role("button", name=option)
        self.click(chosen_option)

    def delete_funnel_page(self,page_number: int):
        page_num = page_number - 1
        self.PAGE_LIST.nth(page_num).wait_for(state="visible")
        self.funnel_page_dropdown_menu_option_choose(page_number,"Delete")
        self.click(self.DELETE_CONFIRM_BTN)

    def get_funnel_pages_count(self)-> int:
        page_list = self.PAGE_LIST.count()
        return int(page_list)

    def get_funnel_page_name(self,page_number: int)-> str:
        page_num = page_number - 1
        page_names = self.PAGE_LIST.nth(page_num).inner_text()
        return page_names[3:].strip()

    def edit_funnel_page_name(self,page_number: int,new_name: str):
        self.funnel_page_dropdown_menu_option_choose(page_number, "Edit")
        self.fill(self.page.get_by_role(role="textbox",name="Page Title"),new_name)
        self.click(self.SAVE_BTN)

    def drag_element_to(self,element:Elements,index: int = -1):
        el = self.filter(self.ELEMENT_BTN_LIST, element).first
        target = self.MAIN_BOARD
        if self.ADDED_ELEMENTS_LIST.count() > 0:
            target = self.ADDED_ELEMENTS_LIST.nth(index)

        target_box = target.bounding_box()
        if index == -1:
            pos: Position = {
                "x": target_box["width"] / 2,
                "y": target_box["height"] - 1,
            }
            el.drag_to(target, target_position=pos)
        else:
            el.drag_to(target)

    def publish_funnel(self):
        self.click(self.FUNNEL_PUBLISH_BTN)
        self.click(self.FUNNEL_PUBLISH_NOW_BTN)

    def get_funnel_name_title(self):
        el = self.FUNNEL_NAME_TITLE
        title = el.get_attribute("title")
        return title

    def click_on_header_menu_option(self,option:EditorHeaderOpt):
        opt = self.filter(self.EDITOR_HEADER_MENU, option)
        self.click(opt)


