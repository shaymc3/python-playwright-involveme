from playwright.sync_api import Page, expect

from .base_page import BasePage


class ConfigurePage(BasePage):

    def __init__(self,page: Page):
        super().__init__(page)
        self.FUNNEL_PUBLISH_BTN = self.page.get_by_test_id("project-settings-publish").locator("span")
        self.FUNNEL_PUBLISH_NOW_BTN = self.page.get_by_role(role="button",name="Publish now")
        self.FUNNEL_NAME_INPUT_FIELD = self.page.get_by_role(role="textbox",name="Funnel Name")
        self.FUNNEL_URL_INPUT_FIELD = self.page.get_by_label("Funnel URL")
        self.url_availability = self.page.locator("[for='project-url']").locator("span")
        self.LANGUAGE_DROPDOWN = self.page.get_by_label("Default Language")
        self.UPDATE_SETTINGS_BTN = self.page.get_by_test_id("update-general-settings-button")
        self.FUNNEL_NAME_TITLE = self.page.locator(".space-x-1.flex div")
        self.SAVED_MSG = self.page.get_by_text("Saved successfully")

    def publish_funnel(self):
        self.click(self.FUNNEL_PUBLISH_BTN)
        self.click(self.FUNNEL_PUBLISH_NOW_BTN)

    def set_funnel_name(self, new_name: str):
        self.fill(self.FUNNEL_NAME_INPUT_FIELD,new_name)

    def set_url(self,new_url):
        url = self.FUNNEL_URL_INPUT_FIELD
        self.fill(url,new_url)

    def select_language(self,language):
        lng_dropdown = self.LANGUAGE_DROPDOWN
        self.select_option(lng_dropdown,language)

    def click_update_settings(self):
        self.click(self.UPDATE_SETTINGS_BTN)
        self.page.wait_for_load_state("networkidle")

    def get_url_availability(self):
        expect(self.url_availability).not_to_have_text("checking...", timeout=5000)
        return self.url_availability.inner_text()

