from playwright.sync_api import Page

from pages.configure_page import ConfigurePage
from pages.editor_page import EditorPage
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from pages.templates_page import TemplatesPage


class AllPages:

    def __init__(self,page: Page):
        self.login_page: LoginPage = LoginPage(page)
        self.project_page: ProjectPage = ProjectPage(page)
        self.templates_page: TemplatesPage = TemplatesPage(page)
        self.editor_page: EditorPage = EditorPage(page)
        self.configure_page: ConfigurePage = ConfigurePage(page)