from pages import ProjectPage,TemplatesPage,LoginPage,EditorPage,ConfigurePage


class AllPages:

    def __init__(self,page):
        pages: AllPages
        self.login_page: LoginPage = LoginPage(page)
        self.project_page: ProjectPage = ProjectPage(page)
        self.templates_page: TemplatesPage = TemplatesPage(page)
        self.editor_page: EditorPage = EditorPage(page)
        self.configue_page: ConfigurePage = ConfigurePage(page)
