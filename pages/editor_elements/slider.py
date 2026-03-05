from playwright.sync_api import Page

from pages.editor_elements.base_element import BaseElement
from pages.ui_types.types import SliderOptions


class Slider(BaseElement[SliderOptions]):

    def __init__(self, page: Page):
        super().__init__(page)
        self.DEFAULT_QUESTION_TEXT = 'For how long will you run your campaign?'
        self.ELEMENTS = self.page.locator("[data-index]")
        self.OPTIONS = self.page.locator(".edit-block-section").nth(0)
        self.SLIDER_RANGE = self.page.get_by_role("slider")

    def get_min(self, index: int = -1) -> int:
        slider_mix = self.SLIDER_RANGE.nth(index).get_attribute("min")
        return int(slider_mix)

    def get_max(self, index: int = -1) -> int:
        slider_max = self.SLIDER_RANGE.nth(index).get_attribute("max")
        return int(slider_max)

    def get_start(self, index: int = -1) -> int:
        start = self.SLIDER_RANGE.nth(index).locator("+div").inner_text()
        return int(start.split()[0])