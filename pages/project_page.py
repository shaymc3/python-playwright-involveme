from time import sleep
from typing import Iterable, List

from playwright.sync_api import expect

import config

from .publish_page import PublishPage
from .base_page import BasePage
from pages.components import Header
from .ui_types.types import FunnelTypes, FunnelMenuOption, SortTypes, SortOrder, FunnelStatus


class ProjectPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        # Components
        self.header = Header(self.page)
        # Locators
        # self.__ADD_NEW_WORKSPACE_BTN = self.page.locator("[data-intercom-target='project-overview-workspaces-new']")
        self.ADD_NEW_WORKSPACE_BTN = self.page.get_by_test_id("project-overview-workspaces-new")
        self.WORKSPACE_LIST = self.page.locator(".mt-6 > a")
        self.WORKSPACE_NAME_LIST = self.page.locator(".mt-6 > a > span:nth-child(1)")
        self.WORKSPACE_NAME_INPUT_FIELD = self.page.get_by_placeholder("Workspace name")
        self.WORKSPACE_CONFIRM_BTN = self.page.locator("#confirm-create-button")
        self.WORKSPACE_OPTIONS_BTN = self.page.get_by_test_id("project-overview-workspace-options")
        self.WORKSPACE_RENAME_BTN = self.page.get_by_test_id("project-overview-workspace-options").locator("li:nth-child(1)")
        self.WORKSPACE_DELETE_BTN = self.page.get_by_test_id("project-overview-workspace-options").locator("li:nth-child(2)")

        self.CREATE_NEW_FUNNEL_MENU_BTN = self.page.get_by_test_id("project-overview-new-project-btn")
        self.CREATE_NEW_FUNNEL_AI_BTN = self.page.get_by_test_id("new-project-from-ai-button")
        self.CREATE_NEW_FUNNEL_TEMPLATE_BTN = self.page.get_by_test_id("new-project-from-template-button")
        self.CREATE_NEW_FUNNEL_SCRATCH_BTN = self.page.get_by_test_id("new-project-from-scratch-button")
        self.FUNNEL_BLOCK_LIST = self.page.locator(".grid > div")
        self.FUNNEL_LIST_DROPDOWN_BTN = self.page.locator("[class*='dropdown']")
        self.FUNNEL_DROPDOWN_LIST = self.page.locator("ul > li")
        self.FUNNEL_SORT_MENU = self.page.get_by_role("combobox")
        self.FUNNEL_SEARCH_BAR = self.page.get_by_test_id("project-search-input")
        self.FUNNEL_TITLES_LIST = self.page.locator(".grid > div h1")
        self.FUNNEL_SUBMISSIONS_LIST = self.page.locator("[aria-labelledby='completed-submission'] + div")
        self.FUNNEL_CONFIRM_DELETE_BTN = self.page.locator("#confirm-delete-button")
        self.FUNNEL_CANCEL_DELETE_BTN = self.page.get_by_role(role="button",name="Cancel")
        self.FUNNEL_NAME_INPUT_FIELD = self.page.get_by_label("Funnel Name")
        self.FUNNEL_TYPE_BTN_LIST = self.page.locator(".gap-4")
        self.START_EDITING_BTN = self.page.get_by_role(role="button", name="START EDITING")
        self.FUNNEL_STATUS_MENU = self.page.locator(".flex.overflow-x-auto a")
        self.FUNNEL_MOVE_TO_DROPDOWN = self.page.get_by_role("combobox").filter(has_text="Select workspace")
        self.MOVE_FUNNEL_BTN = self.page.get_by_role("button", name="Move funnel")

        self.FUNNEL_AI_DESCRIPTION_INPUT_FIELD = self.page.locator(".resize-none")
        self.FUNNEL_AI_CONTINUE_BTN = self.page.get_by_role(role="button",name="Continue")
        self.FUNNEL_AI_GENERATE_BTN = self.page.get_by_role(role="button",name="Generate")
        self.FUNNEL_AI_EDIT_BTN = self.page.get_by_role(role="link",name="Edit this funnel")

    def goto_project_page(self):
        self.page.wait_for_load_state("networkidle")
        self.page.goto(config.PROJECTS_URL)

    def create_new_workspace(self,workspace_name):
        ws_list = self.WORKSPACE_LIST
        self.click(self.ADD_NEW_WORKSPACE_BTN)
        self.fill(self.WORKSPACE_NAME_INPUT_FIELD, workspace_name)
        self.click(self.WORKSPACE_CONFIRM_BTN)
        ws_list.nth(ws_list.count()).wait_for(state="visible")

    def create_funnels(self,workspace,funnel_list: List[str]):
        for fnl in funnel_list:
            self.go_to_workspace(workspace)
            self.create_new_funnel_from_scratch(fnl, "Answer-based Outcomes")
            self.goto_project_page()

    def go_to_workspace(self,workspace_name):
        workspace = self.filter(self.WORKSPACE_LIST, workspace_name)
        self.click(workspace.first)

    def rename_workspace(self,old_name,new_name):
        self.go_to_workspace(old_name)
        self.click(self.WORKSPACE_OPTIONS_BTN)
        self.click(self.WORKSPACE_RENAME_BTN)
        self.fill(self.page.get_by_placeholder(f"{old_name}"), new_name)
        self.click(self.WORKSPACE_CONFIRM_BTN)

    def get_workspace_locator(self,name):
        locator = self.filter(self.WORKSPACE_LIST,name)
        return locator

    def delete_workspace_by_name(self,name):
        ws_list = self.WORKSPACE_LIST
        before_count = ws_list.count() - 1
        self.go_to_workspace(name)
        self.click(self.WORKSPACE_OPTIONS_BTN)
        self.click(self.WORKSPACE_DELETE_BTN)
        self.fill(self.page.get_by_placeholder(f"{name}"), name)
        self.click(self.WORKSPACE_CONFIRM_BTN)
        # ws_list.nth(ws_list.count()-1).wait_for(state="detached")
        expect(ws_list).to_have_count(before_count)

    def delete_all_workspace(self):
        while len(self.get_all_workspace_titles()) > 1:
            ws = self.get_all_workspace_titles()
            self.delete_workspace_by_name(ws[0])

    def get_workspace_count(self)-> int:
        workspace_count = self.WORKSPACE_LIST.count()
        return workspace_count

    def get_funnel_count_from_ws_list(self,workspace_name):
        workspace = self.filter(self.WORKSPACE_NAME_LIST, workspace_name)
        count = self.get_inner_text(workspace.locator("+ span"))
        return int(count)

    def funnel_move_to_workspace(self,workspace):
        dropdown = self.FUNNEL_MOVE_TO_DROPDOWN
        self.click(dropdown)
        dropdown.select_option(value=workspace)
        self.click(self.MOVE_FUNNEL_BTN)

    def create_new_funnel_from_scratch(self,name,funnel_type:FunnelTypes):
        if self.is_visible(self.CREATE_NEW_FUNNEL_MENU_BTN):
            self.click(self.CREATE_NEW_FUNNEL_MENU_BTN)
        self.click(self.CREATE_NEW_FUNNEL_SCRATCH_BTN)
        self.fill(self.FUNNEL_NAME_INPUT_FIELD, name)
        fnl_type = self.filter(self.FUNNEL_TYPE_BTN_LIST, funnel_type)
        self.click(fnl_type)
        self.click(self.START_EDITING_BTN)

    def create_new_funnel_with_ai(self,description):
        if self.is_visible(self.CREATE_NEW_FUNNEL_MENU_BTN):
            self.click(self.CREATE_NEW_FUNNEL_MENU_BTN)
        self.click(self.CREATE_NEW_FUNNEL_AI_BTN)
        self.fill(self.FUNNEL_AI_DESCRIPTION_INPUT_FIELD,description)
        self.click(self.FUNNEL_AI_CONTINUE_BTN)
        self.click(self.FUNNEL_AI_GENERATE_BTN)
        self.click(self.FUNNEL_AI_EDIT_BTN)

    def create_new_funnel_with_template(self):
        if self.is_visible(self.CREATE_NEW_FUNNEL_MENU_BTN):
            self.click(self.CREATE_NEW_FUNNEL_MENU_BTN)
        self.click(self.CREATE_NEW_FUNNEL_TEMPLATE_BTN)

    def open_publish_new_page(self,funnel_name) -> PublishPage:
        with self.page.context.expect_page() as new_tab_info:
            self.funnel_dropdown_menu_option(funnel_name, "View")

        new_page = new_tab_info.value
        return PublishPage(new_page)

    def funnel_dropdown_menu_option(self,funnel_name: str, option: FunnelMenuOption):
        funnel = self.filter(self.FUNNEL_BLOCK_LIST, funnel_name).first
        funnel_dropdown_btn = funnel.locator(self.FUNNEL_LIST_DROPDOWN_BTN)
        self.click(funnel_dropdown_btn)
        dropdown_menu = funnel_dropdown_btn.locator(self.FUNNEL_DROPDOWN_LIST)
        opt = self.filter(dropdown_menu,option)
        self.click(opt)

    def funnel_sort_by(self, option:SortTypes):
        self.select_option(self.FUNNEL_SORT_MENU, option)

    def search_funnel(self,name):
        self.fill(self.FUNNEL_SEARCH_BAR, name)

    def get_all_funnel_titles(self):
        return self.get_all_inner_text(self.FUNNEL_TITLES_LIST)

    def get_all_workspace_titles(self):
        return self.get_all_inner_text(self.WORKSPACE_NAME_LIST)

    def get_all_funnel_submissions(self):
        return self.get_all_inner_text(self.FUNNEL_SUBMISSIONS_LIST)

    def is_funnel_sorted_by(self, values: Iterable[str], order:SortOrder = "asc") -> bool:
        normalized = [v.strip().lower() for v in values]
        expected = sorted(normalized,reverse=(order == "desc"),)
        return normalized == expected

    def delete_funnel(self,funnel_name):
        fnl_list = self.FUNNEL_TITLES_LIST
        before_count = fnl_list.count() - 1
        self.funnel_dropdown_menu_option(funnel_name,"Delete funnel")
        self.click(self.FUNNEL_CONFIRM_DELETE_BTN)
        expect(fnl_list).to_have_count(before_count)

    def goto_funnel_status(self,status:FunnelStatus):
        sts = self.filter(self.FUNNEL_STATUS_MENU,status)
        self.click(sts)

    def delete_all_funnels(self):
        for fnl in self.get_all_funnel_titles():
            self.delete_funnel(fnl)


