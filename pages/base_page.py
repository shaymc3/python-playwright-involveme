from playwright.sync_api import Locator, Page

from utils.effects import click_script, fill_script


class BasePage:
    def __init__(self, page: Page):
        self.page = page


    def click(self, locator: Locator):
        # locator.wait_for(state="visible")
        self.page.evaluate(click_script)
        locator.click()


    def fill(self, locator: Locator, text: str):
        # locator.wait_for(state="visible")
        locator.evaluate(fill_script)
        locator.fill(str(text))

    def select_option(self,locator: Locator,value: str):
        self.click(locator)
        locator.select_option(value=str(value))

    def is_visible(self,locator:Locator) -> bool:
        return locator.is_visible()

    def filter(self,locator: Locator,text: str, exact: bool = False):
        if exact:
            return locator.filter(has_text=text).first
        return locator.filter(has_text=text)

    def get_page_title(self) -> str:
        return self.page.title()

    def get_all_inner_text(self,locator:Locator)-> list[str]:
        # locator.last.wait_for(state="visible")
        return locator.all_inner_texts()

    def get_inner_text(self,locator:Locator)-> str:
        locator.wait_for(state="visible")
        return locator.inner_text()

