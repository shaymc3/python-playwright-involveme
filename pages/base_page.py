from typing import Iterable, List

from playwright.sync_api import Page, Locator

import config
from utils.effects import click_script, fill_script, show_overlay


class BasePage:
    def __init__(self, page: Page):
        self.page = page


    def click(self, locator):
        self.page.evaluate(click_script)
        locator.click()


    def fill(self, locator: Locator, text):
        element = locator
        element.evaluate(fill_script)
        element.fill(str(text))

    def select_option(self,locator,value):
        self.click(locator)
        locator.select_option(value=str(value))

    def is_visible(self,locator:Locator) -> bool:
        return locator.is_visible()

    def filter(self,locator,name)-> Locator | bool:
        get_locator = locator.filter(has_text=name).first
        # filtered = get_locator.first if get_locator.count() > 0 else False
        return get_locator

    def wait_for_element(self,locator: Locator):
        locator.wait_for(state="visible")
        locator.highlight()

    def get_page_title(self):
        return self.page.title()

    def get_all_inner_text(self,locator:Locator)-> list[str]:
        self.page.wait_for_load_state("networkidle")
        return locator.all_inner_texts()

    def get_inner_text(self,locator:Locator)-> str:
        locator.wait_for(state="visible")
        return locator.inner_text()

    # def check_for_broken_links(self)-> List[str]:
    #     links = self.page.locator("a[href]")
    #     hrefs = links.evaluate_all(
    #         """elements =>
    #         elements
    #             .map(el => el.getAttribute("href"))
    #             .filter(href => href && !href.startsWith("#"))
    #         """
    #     )
    #     if not hrefs:
    #         return []
    #
    #     broken_links = []
    #     for href in hrefs:
    #         if hrefs == 3:#for not getting blocked
    #             break
    #         if href.startswith("/"):
    #             href = config.BASE_URL + href
    #
    #         if not href.startswith("https:"):
    #             href = self.page.url + href
    #
    #         if href.startswith(("mailto:", "tel:", "javascript:")):
    #             continue
    #
    #         if href.startswith("billing/plans"):
    #             href = self.page.url + f"/{href}"
    #
    #         print(href)
    #         show_overlay(self.page,f"testing: {href}","RUNNING")
    #         response = self.page.request.head(href, timeout=10000)
    #
    #         if not response.ok:
    #             broken_links.append((href, response.status))
    #     return broken_links