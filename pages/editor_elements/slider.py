from typing import Literal

from pages.base_page import BasePage


class Slider(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.ELEMENTS = self.page.locator("[data-index]")
        self.OPTIONS = self.page.locator(".edit-block-section").nth(0)

    def toggle_option(self,option):
        toggle_button = self.OPTIONS.get_by_text(option)
        self.click(toggle_button)