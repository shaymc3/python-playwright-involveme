from typing import Iterable

import config
from .base_page import BasePage
from .editor_elements.text_choice import TextChoice, SingleChoice, MultipleChoice

from .ui_types.types import Elements, PageMenuOption


class EditorPage(BasePage):

    def __init__(self,page):
        super().__init__(page)
        # Elements
        self.single_choice: SingleChoice = SingleChoice(page)
        self.multiple_choice: MultipleChoice = MultipleChoice(page)

        self.EDITOR_HEADER = self.page.get_by_test_id("project-navigation-top")
        self.FUNNEL_NAME_TITLE = self.page.locator(".space-x-1.flex div")
        self.FUNNEL_PUBLISH_BTN = self.page.get_by_test_id("publish-button")
        self.WORKSPACE_TITLE = self.page.locator(".space-x-1.flex a")
        self.ELEMENT_BTN_LIST = self.page.get_by_test_id("editor-content-elements").locator(".text-left")
        self.ELEMENT_CLOSE_BTN = self.page.locator("[data-icon='xmark']")
        self.ADDED_ELEMENTS_LIST = self.page.locator("[data-index]")
        self.DELETE_BTN = self.page.locator(".fa-trash")
        self.SAVE_BTN = self.page.get_by_role(role="button",name="Save")
        self.DELETE_CONFIRM_BTN = self.page.locator("[data-danger='true']")
        self.ELEMENT_TYPE_NAME = self.page.locator(".sticky.top-0 >.py-2")
        self.PAGE_LIST = self.page.get_by_test_id("editor-page-navigation-input-pages").locator("div:nth-child(1)")
        self.ADD_PAGE_BTN = self.page.get_by_role("button", name="Add page")


    def goto_funnel_edit_page(self, funnel):
        self.page.add_locator_handler(self.page.locator(".popup-container"),
                                      lambda: self.page.locator(".popup-container .fa-xmark").click())
        self.page.goto(f"{config.EDITOR_PAGE}/{funnel}")

    def add_element_and_close(self,element:Elements):
        el = self.filter(self.ELEMENT_BTN_LIST, element)
        self.click(el)
        self.click(self.ELEMENT_CLOSE_BTN)

    def add_element_and_edit(self,element:Elements):
        el = self.filter(self.ELEMENT_BTN_LIST, element)
        self.click(el)

    def click_on_element(self,index):
        el = self.page.locator(f"[data-index='{index}']")
        self.click(el)

    def add_elements(self,elements: Iterable[Elements]):
        for el in elements:
            self.add_element_and_close(el)

    def get_all_added_elements_count(self) -> int:
        self.page.wait_for_load_state("networkidle")
        elements = self.ADDED_ELEMENTS_LIST
        return elements.count()

    def search_element(self,element):
        pass

    def publish_funnel(self):
        self.click(self.FUNNEL_PUBLISH_BTN)

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
        el_count = self.get_all_added_elements_count()
        el_type_list = []
        for i in range(el_count):
            self.click_on_element(i)
            el_typ = self.ELEMENT_TYPE_NAME.inner_text()
            el_type_list.append(el_typ)

    def add_funnel_page(self,after_page=1):
        page_num = after_page - 1
        add_after = self.PAGE_LIST.nth(page_num)
        add_after.hover()
        self.click(self.ADD_PAGE_BTN.nth(page_num))

    def funnel_page_dropdown_menu_option_choose(self,page_number,option:PageMenuOption):
        page_num = page_number - 1
        page_to_delete = self.PAGE_LIST.nth(page_num)
        page_to_delete.hover()
        self.click(page_to_delete.locator("+div > button").nth(0))
        chosen_option = self.page.get_by_role("button", name=option)
        self.click(chosen_option)

    def delete_funnel_page(self,page_number):
        page_num = page_number - 1
        self.PAGE_LIST.nth(page_num).wait_for(state="visible")
        self.funnel_page_dropdown_menu_option_choose(page_number,"Delete")
        self.click(self.DELETE_CONFIRM_BTN)

    def get_funnel_pages_count(self)-> int:
        page_list = self.PAGE_LIST.count()
        return int(page_list)

    def get_funnel_page_name(self,page_number)-> str:
        page_num = page_number - 1
        page_names = self.PAGE_LIST.nth(page_num).inner_text()
        return page_names[3:].strip()

    def edit_funnel_page_name(self,page_number,new_name):
        self.funnel_page_dropdown_menu_option_choose(page_number, "Edit")
        self.fill(self.page.get_by_role(role="textbox",name="Page Title"),new_name)
        self.click(self.SAVE_BTN)






