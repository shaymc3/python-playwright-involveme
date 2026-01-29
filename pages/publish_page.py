from .base_page import BasePage


class PublishPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.ELEMENTS_LIST = self.page.locator("[data-index]")


    def click_on_element(self,name):
        element = self.page.get_by_role(role="button",name=f"{name}")
        self.click(element)

    def select_option_from_dropdown(self,option,nth=0):
        element = self.page.get_by_role(role="combobox").nth(nth)
        self.click(element)
        option = self.page.get_by_role("option", name=f"{option}")
        self.click(option)
