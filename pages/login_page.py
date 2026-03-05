from playwright.sync_api import Page

import config
from pages.base_page import BasePage
from utils.effects import show_overlay
import time

seconds = 10

for i in range(seconds, 0, -1):
    print(i)

class LoginPage(BasePage):
    def __init__(self,page: Page):
        super().__init__(page)
        self.__EMAIL_INPUT_FIELD = self.page.get_by_test_id("login-email-input")
        self.__PASSWORD_INPUT_FIELD = self.page.get_by_test_id("login-password-input")
        self.__SIGN_IN_BTN = self.page.get_by_test_id("login-form-button")
        # self.__SIGN_IN_WITH_GOOGLE_BTN = self.page.locator("#container-div")

    def login(self, email: str, password: str):
        self.fill(self.__EMAIL_INPUT_FIELD,email)
        self.fill(self.__PASSWORD_INPUT_FIELD,password)
        self.click(self.__SIGN_IN_BTN)
        self.page.wait_for_url(config.PROJECTS_URL, timeout=120000)

