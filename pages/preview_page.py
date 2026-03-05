
import config

from .base_page import BasePage


class PreviewPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.REQUIRED_MSG = "Fill in all required fields"
        self.ELEMENTS_LIST = self.page.locator("[data-index]")
        self.PROGRESS_BAR = self.page.locator(".progress-tooltip")
        self.ERROR_MSG = self.page.locator(".validation-error-message")
        self.NUMBER_INPUT = self.page.get_by_role("spinbutton")
        self.TEXTBOX_INPUT = self.page.get_by_role("textbox")
        self.THANKS_MSG = self.page.get_by_role(role="heading", name="Thanks for your submission!")

    def goto_preview_page(self,preview_page):
        self.page.goto(f"{config.BASE_URL}/{preview_page}")

    def click_on(self,name,nth = 0):
        element = self.page.get_by_role(role="button",name=f"{name}").nth(nth)
        self.click(element)

    def select_option_from_dropdown(self ,option ,nth = 0):
        dropdown_trigger = self.page.locator(".vue-select .control").nth(nth)
        dropdown_trigger.click()

        self.page.get_by_role("option", name=option).click()

    def set_slider_to(self,number,nth = 0):
        slider = self.page.get_by_role(role="slider").nth(nth)
        slider.fill(str(number))

    def fill_text(self, text, nth: int = 1):
        text_box = self.TEXTBOX_INPUT.nth(nth)

        self.fill(text_box, text)


    def set_number_input(self,num,nth = 0):
        num_input = self.NUMBER_INPUT.nth(nth)
        self.fill(num_input,num)

    def get_number_input_max(self,nth: int = 0):
        num_input = self.NUMBER_INPUT.nth(nth)
        max_num = num_input.get_attribute("max")
        return max_num

    def get_number_input_min(self,nth: int = 0):
        num_input = self.NUMBER_INPUT.nth(nth)
        min_num = num_input.get_attribute("min")
        return min_num

    def get_error_msg(self):
        return self.ERROR_MSG.first.inner_text()

    def get_current_page_number(self):
        progress = self.PROGRESS_BAR.inner_text()
        current_page = int(progress[:2].replace("/", ""))
        return current_page

    def get_total_page_number(self):
        progress = self.PROGRESS_BAR.inner_text()
        last_page = int(progress[2:].replace("/", "").strip())
        return last_page

    def is_error_msg_visible(self):
        return self.ERROR_MSG.first.is_visible()

    def test(self):
        print(self.page.locator("body").inner_text())