from .base_page import BasePage


class ConfigurePage(BasePage):

    def __init__(self,page):
        super().__init__(page)
        self.__FUNNEL_PUBLISH_BTN = self.page.get_by_test_id("project-settings-publish").locator("span")
        self.__FUNNEL_PUBLISH_NOW_BTN = self.page.get_by_role(role="button",name="Publish now")
        self.FUNNEL_NAME_INPUT_FIELD = self.page.get_by_role(role="textbox",name="Funnel Name")
        self.UPDATE_SETTINGS_BTN = self.page.get_by_test_id("update-general-settings-button")

    def publish_funnel(self):
        self.click(self.__FUNNEL_PUBLISH_BTN)
        self.click(self.__FUNNEL_PUBLISH_NOW_BTN)

    def change_funnel_name(self,new_name):
        self.fill(self.FUNNEL_NAME_INPUT_FIELD,new_name)
        self.click(self.UPDATE_SETTINGS_BTN)

