import allure
import pytest
from playwright.sync_api import expect
from pages.editor_page import EditorPage
from pages.templates_page import TemplatesPage
from utils.data_handler_csv import DataReader

class TestTemplatesPage:

    templates_data = DataReader("templates_data").get_data()
    categories_data = DataReader("categories_data").get_data()

    @allure.title("Templates Page: Search and Filter Templates")
    @allure.description("This test verifies the search and filtering functionality on the templates page.")
    @allure.epic("Templates")
    @allure.feature("Template Discovery")
    @allure.story("Search and Filter Templates")
    @pytest.mark.ui
    @pytest.mark.parametrize("data", templates_data)
    def test_search_and_filter_templates(self, templates_page:TemplatesPage,editor_page:EditorPage, data):
        allure.dynamic.title(f"Search and select template: '{data['template_name']}'")
        templates_page.goto_templates_page()

        search_term = data["template_name"]

        templates_page.search_template(search_term)
        templates_page.wait_for_page_load()

        titles = templates_page.get_template_titles()
        assert any(search_term in title for title in titles)

        templates_page.choose_template(search_term)
        templates_page.wait_for_page_load()

        assert search_term == editor_page.get_funnel_name_title()


    @allure.title("Template Category Count")
    @allure.description("This test verifies that the number of templates displayed matches the count in the category menu.")
    @allure.epic("Templates")
    @allure.feature("Template Discovery")
    @allure.story("Category Counts")
    @pytest.mark.ui
    @pytest.mark.parametrize("data", categories_data)
    def test_template_menu_count_matches_items(self, templates_page: TemplatesPage,data):
        allure.dynamic.title(f"Category '{data['category_name']}' -> '{data['sub_category_name']}' count matches items")
        category = data["category_name"]
        sub_category = data["sub_category_name"]

        templates_page.goto_templates_page()
        count_from_list = templates_page.get_templates_count_from_the_list(category, sub_category)
        count_on_page = templates_page.get_templates_count()
        assert count_from_list == count_on_page

    @allure.title("Template Preview")
    @allure.description("This test verifies that a template can be previewed correctly.")
    @allure.epic("Templates")
    @allure.feature("Template Discovery")
    @allure.story("Template Preview")
    @pytest.mark.parametrize("data", templates_data)
    def test_preview_template(self, templates_page: TemplatesPage,data):
        allure.dynamic.title(f"Preview template: '{data['template_name']}'")
        template_name = data["template_name"]

        templates_page.goto_templates_page()
        templates_page.preview_template(template_name)
        expect(templates_page.USE_TEMPLATE_BTN).to_be_visible()
        assert template_name in templates_page.get_page_title()

