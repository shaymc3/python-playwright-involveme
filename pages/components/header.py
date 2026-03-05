from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.ui_types.types import MainNavOption, UserMenuOption


class Header(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.__NAV_BAR = self.page.get_by_test_id("dashboard-navigation-top")
        self.NAV_BAR_MENU = self.__NAV_BAR.locator("a div")
        self.LOGO = self.__NAV_BAR.locator(".mr-4")
        self.USER_MENU = self.__NAV_BAR.locator("#nav-dropdown")
        self.USER_MENU_LIST = self.__NAV_BAR.locator("#nav-dropdown + ul > li")

    def click_on_logo(self):
        self.click(self.LOGO)

    def go_to_page(self,page:MainNavOption):
        page = self.filter(self.NAV_BAR_MENU,page)
        self.click(page)

    def click_on_user_menu(self):
        self.click(self.USER_MENU)

    def click_on_user_menu_option(self,option:UserMenuOption):
        option = self.filter(self.USER_MENU_LIST,option)
        self.click(option)

