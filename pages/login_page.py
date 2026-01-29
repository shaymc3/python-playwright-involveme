import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.__EMAIL_INPUT_FIELD = self.page.get_by_test_id("login-email-input")
        self.__PASSWORD_INPUT_FIELD = self.page.get_by_test_id("login-password-input")
        self.__SIGN_IN_BTN = self.page.get_by_test_id("login-form-button")
        # self.__SIGN_IN_WITH_GOOGLE_BTN = self.page.locator("#container-div")

    def login(self, email, password):
        self.fill(self.__EMAIL_INPUT_FIELD,email)
        self.fill(self.__PASSWORD_INPUT_FIELD,password)
        self.click(self.__SIGN_IN_BTN)
        self.page.wait_for_url(config.PROJECTS_URL)