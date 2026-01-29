from .base_page import BasePage

class TemplatesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.SEARCH_BAR = self.page.get_by_placeholder("Search templates")
        self.CATEGORY_LIST = self.page.locator(".categories-list a")
        self.TEMPLATE_CARDS = self.page.locator(".template-card")
        self.TEMPLATE_PREVIEW_BTN = self.page.get_by_role("link", name="Preview")
        self.USE_TEMPLATE_BTN = self.page.get_by_role("button", name="Choose")

    def search_template(self, query):
        self.fill(self.SEARCH_BAR, query)
        self.page.wait_for_load_state("networkidle")

    def select_category(self, category_name):
        self.click(self.page.get_by_role("link", name=category_name, exact=True))

    def get_template_count(self):
        return self.TEMPLATE_CARDS.count()

    def choose_first_template(self):
        # Hover over the first card to reveal buttons if necessary, or just click if always visible
        # Assuming we need to click "Choose" on the first visible template
        self.TEMPLATE_CARDS.first.hover()
        self.click(self.USE_TEMPLATE_BTN.first)

    def confirm_template_name(self, name):
        # Assuming a modal appears with a specific name input
        # Reusing the likely locator or defining one specific to this modal
        name_input = self.page.get_by_label("Project Name") # Or Funnel Name
        if self.is_visible(name_input):
             self.fill(name_input, name)
             self.click(self.page.get_by_role("button", name="Start Editing"))
        else:
            # Maybe it uses the project page one?
            pass