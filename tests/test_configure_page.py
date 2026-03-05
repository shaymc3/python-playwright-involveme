import allure
import pytest
from playwright.sync_api import expect

from pages.configure_page import ConfigurePage
from pages.editor_page import EditorPage
from pages.project_page import ProjectPage
from utils.data_handler_csv import DataReader


@pytest.mark.ui
@allure.epic("Configuration")
@allure.feature("Funnel Settings")
class TestConfigure:

    url_data = DataReader("configure_data/url_data").get_data()
    language_data = DataReader("configure_data/language_data").get_data()
    name_data = DataReader("configure_data/name_data").get_data()

    @pytest.fixture()
    def create_new_funnel(self, project_page: ProjectPage, editor_page:EditorPage):
        ws_name = "Configure Tests"
        if ws_name not in project_page.get_all_workspace_titles():
            project_page.create_new_workspace(ws_name)

        project_page.go_to_workspace(ws_name)
        funnel_counter = project_page.get_funnel_count_from_ws_list(ws_name)

        funnel_name = f"funnel-{funnel_counter:02d}"
        project_page.create_new_funnel_from_scratch(funnel_name, "Answer-based Outcomes")
        expect(editor_page.ELEMENT_BTN_LIST.nth(5)).to_be_visible()
        editor_page.click_on_header_menu_option("Settings")

        self.funnel_name = funnel_name
        yield

    @allure.description("Verify that the user can successfully change the name of the funnel.")
    @allure.story("General Settings")
    @pytest.mark.parametrize("data", name_data)
    def test_change_funnel_name(self, configure_page: ConfigurePage, data, create_new_funnel):
        allure.dynamic.title(f"Change funnel name to '{data['funnel_name']}'")
        new_name = data["funnel_name"]
        configure_page.set_funnel_name(new_name)
        configure_page.click_update_settings()
        configure_page.page.reload()
        expect(configure_page.FUNNEL_NAME_TITLE).to_contain_text(new_name)

    @allure.description("Verify that the user can change the URL of the funnel.")
    @allure.story("General Settings")
    @pytest.mark.parametrize("data", url_data)
    def test_change_url(self, configure_page: ConfigurePage, data,create_new_funnel):
        allure.dynamic.title(f"Change funnel URL to '{data['funnel_url']}'")
        new_url = data["funnel_url"]
        configure_page.set_url(new_url)
        assert configure_page.get_url_availability() in data["expected_msg"]


    @allure.description("Verify that the user can change the default language of the funnel.")
    @allure.story("General Settings")
    @pytest.mark.parametrize("data", language_data)
    def test_change_language(self, configure_page: ConfigurePage, data,create_new_funnel):
        allure.dynamic.title(f"Change funnel language to '{data['language']}'")
        language = data["language"]
        configure_page.select_language(language)
        configure_page.click_update_settings()
        expect(configure_page.LANGUAGE_DROPDOWN).to_have_value(data["value"])