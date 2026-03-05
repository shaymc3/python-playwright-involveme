
from playwright.sync_api import Page
import config
from .base_page import BasePage
from .components.header import Header


class TemplatesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Components
        self.header = Header(self.page)
        # Locators
        self.SEARCH_BAR = self.page.get_by_placeholder("Filter templates by name or keywords")
        self.CATEGORY_LIST = self.page.locator(".divide-gray-200 div")
        self.TEMPLATE_CARDS = self.page.locator("[loading-page] > div")
        self.TEMPLATE_PREVIEW_BTN = self.page.get_by_role("link", name="Preview")
        self.CHOOSE_TEMPLATE_BTN = self.page.get_by_role(role="link", name="Choose")
        self.NEXT_BTN = self.page.get_by_role("link", name="Next")
        self.skeleton_selector = ".bg-gray-300"
        self.USE_TEMPLATE_BTN = self.page.get_by_role(role="button",name="Use this template")


    def goto_templates_page(self):
        self.page.goto(config.TEMPLATES_URL)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        self.page.wait_for_selector(self.skeleton_selector, state="detached", timeout=10000)

    def search_template(self, query: str):

        self.fill(self.SEARCH_BAR, query)
        self.wait_for_page_load()

    def select_category(self, category: str,sub_category: str):
        self.click(self.filter(self.CATEGORY_LIST,category).first)
        self.click(self.page.get_by_role("button", name=sub_category))

    def get_templates_count_from_the_list(self,category: str,sub_category: str) -> int:
        self.select_category(category,sub_category)
        count= self.page.get_by_role("button", name=sub_category).locator("div").nth(1).inner_text()
        return int(count)

    def choose_template(self, template_name: str) -> None:
        template = self.filter(self.TEMPLATE_CARDS, template_name).first
        template.hover()
        choose_btn = template.locator(self.CHOOSE_TEMPLATE_BTN)
        self.click(choose_btn)

    def preview_template(self,template_name: str) -> None:
        template = self.filter(self.TEMPLATE_CARDS, template_name).first
        template.hover()
        preview_btn = template.locator(self.TEMPLATE_PREVIEW_BTN)
        self.click(preview_btn)

    def get_template_titles(self):
        templates = self.TEMPLATE_CARDS.all_inner_texts()
        template_titles = [text.split("\n")[-1] for text in templates if text.strip()]
        return template_titles

    def get_templates_count(self) -> int:
        total: int = 0

        blank_template = self.filter(self.TEMPLATE_CARDS,"Blank Design")
        if blank_template:
            total = -1

        while True:
            self.wait_for_page_load()

            total += self.CHOOSE_TEMPLATE_BTN.count()
            if  not self.NEXT_BTN.is_visible() or ("cursor-not-allowed" in self.NEXT_BTN.get_attribute("class")):
                break

            self.click(self.NEXT_BTN)
        return int(total)