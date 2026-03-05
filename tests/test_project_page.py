
import allure
import pytest
from playwright.sync_api import expect

from pages.editor_page import EditorPage
from pages.project_page import ProjectPage
from pages.templates_page import TemplatesPage


@pytest.fixture
def new_workspace(project_page:ProjectPage,request):
    ws_count = project_page.get_workspace_count()
    # ws_name = f"Test Workspace {ws_count + 1}"
    ws_name = request.node.name[:-10]
    project_page.create_new_workspace(ws_name)
    expect(project_page.WORKSPACE_NAME_LIST).to_have_count(ws_count + 1)
    assert ws_name in project_page.get_all_workspace_titles()

    yield ws_name

class TestProjectPage:

    @allure.title("Project Dashboard: Assert Page Title")
    @allure.description("This test verifies that the project dashboard page has the correct title.")
    @allure.epic("Project Dashboard")
    @allure.feature("Dashboard Loading")
    @allure.story("Verify Page Title")
    @pytest.mark.ui
    def test_assert_page_title(self,project_page:ProjectPage):
        expect(project_page.page).to_have_title("Funnels | involve.me")

    @allure.title("Project Dashboard: Sort Funnels by Name (Descending)")
    @allure.description("This test verifies that funnels on the dashboard can be sorted by name in descending order.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Sort Funnels")
    @pytest.mark.ui
    def test_sort_funnel_by_name_desc(self, project_page:ProjectPage,new_workspace):

        fnl_name_list = ["BBB","CCC","AAA"]

        project_page.create_funnels(new_workspace,fnl_name_list)
        project_page.go_to_workspace(new_workspace)
        project_page.funnel_sort_by("name-asc")
        funnel_title_list = project_page.get_all_funnel_titles()

        assert project_page.is_funnel_sorted_by(funnel_title_list, "asc")

    @allure.title("Project Dashboard: Create New Workspace")
    @allure.description("This test verifies that a new workspace can be created successfully.")
    @allure.epic("Project Dashboard")
    @allure.feature("Workspace Management")
    @allure.story("Create Workspace")
    @pytest.mark.ui
    def test_create_new_workspace(self, project_page,new_workspace):
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(0)

        assert new_workspace in project_page.get_all_workspace_titles()

    @allure.title("Project Dashboard: Change Workspace Name")
    @allure.description("This test verifies that a workspace can be renamed.")
    @allure.epic("Project Dashboard")
    @allure.feature("Workspace Management")
    @allure.story("Rename Workspace")
    @pytest.mark.ui
    def test_change_workspace_name(self, project_page:ProjectPage,new_workspace):
        new_ws_name = "Test Workspace rename"
        project_page.rename_workspace(new_workspace,new_ws_name)
        expect(project_page.page.get_by_text(new_workspace).last).not_to_be_visible()
        print(project_page.get_all_workspace_titles())
        assert new_ws_name in project_page.get_all_workspace_titles()

    @allure.title("Project Dashboard: Delete Workspace")
    @allure.description("This test verifies that a workspace can be deleted.")
    @allure.epic("Project Dashboard")
    @allure.feature("Workspace Management")
    @allure.story("Delete Workspace")
    @pytest.mark.ui
    def test_delete_workspace(self,project_page:ProjectPage,new_workspace):

        project_page.delete_workspace_by_name(new_workspace)

        assert new_workspace not in project_page.get_all_workspace_titles()

    @allure.title("Project Dashboard: Search for a Funnel")
    @allure.description("This test verifies the search functionality for funnels on the dashboard.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Search Funnel")
    @pytest.mark.ui
    def test_search_funnel(self,project_page:ProjectPage,new_workspace):
        fnl_name = "Funnel 1"
        fnl2_name = "Funnel 2"
        project_page.create_new_funnel_from_scratch(fnl_name,"Score-based Outcomes")
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        project_page.create_new_funnel_from_scratch(fnl2_name, "Score-based Outcomes")
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(2)

        project_page.search_funnel(fnl_name)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl_name in project_page.get_all_funnel_titles()

        project_page.search_funnel(fnl2_name)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl2_name in project_page.get_all_funnel_titles()

    @allure.title("Project Dashboard: Duplicate a Funnel")
    @allure.description("This test verifies that a funnel can be duplicated and that the copy appears on the dashboard.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Duplicate Funnel")
    @pytest.mark.ui
    def test_duplicate_funnel(self,project_page:ProjectPage,editor_page:EditorPage,new_workspace):
        fnl_name = "Funnel 1"
        project_page.create_new_funnel_from_scratch(fnl_name,"Score-based Outcomes")

        editor_page.add_element_and_close("Single Choice")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(1)

        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        project_page.funnel_dropdown_menu_option(fnl_name,"Duplicate funnel")
        expect(editor_page.ADDED_ELEMENTS_LIST).to_have_count(1)

        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(2)

        assert fnl_name in project_page.get_all_funnel_titles()
        assert f"{fnl_name} (copy)" in project_page.get_all_funnel_titles()

    @allure.title("Project Dashboard: Move Funnel to Another Workspace")
    @allure.description("This test verifies that a funnel can be moved from one workspace to another.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Move Funnel")
    @pytest.mark.ui
    def test_move_funnel_to_workspace(self,project_page:ProjectPage,editor_page,new_workspace):
        fnl_name = "Funnel 1"
        new_workspace2 = "test_move_funnel_to_workspace 2"

        project_page.create_new_funnel_from_scratch(fnl_name,"Thank You page")
        editor_page.wait_for_page_load()
        project_page.goto_project_page()
        project_page.create_new_workspace(new_workspace2)

        project_page.go_to_workspace(new_workspace)
        project_page.funnel_dropdown_menu_option(fnl_name,"Move to workspace")
        project_page.move_funnel_workspace_to(new_workspace2)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(0)

        project_page.go_to_workspace(new_workspace2)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl_name in project_page.get_all_funnel_titles()

    @allure.title("Project Dashboard: Create New Funnel from Scratch")
    @allure.description("This test verifies that a new funnel can be created from scratch in a workspace.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Creation")
    @allure.story("Create from Scratch")
    @pytest.mark.ui
    def test_create_new_funnel_from_scratch(self, project_page:ProjectPage, new_workspace, editor_page:EditorPage):
        fnl_name = "Test New Funnel"
        project_page.create_new_funnel_from_scratch(fnl_name,"Thank You page")
        expect(editor_page.WORKSPACE_TITLE).to_contain_text(new_workspace[:5])
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)

        expect(project_page.FUNNEL_TITLES_LIST).to_contain_text([fnl_name])

    @allure.title("Project Dashboard: Create New Funnel with AI")
    @allure.description("This test verifies that a new funnel can be created using the AI assistant.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Creation")
    @allure.story("Create with AI")
    @pytest.mark.ui
    def test_create_new_funnel_with_ai(self, project_page: ProjectPage,editor_page:EditorPage,new_workspace):
        project_page.create_new_funnel_with_ai("Create an appointment funnel designed")
        expect(editor_page.WORKSPACE_TITLE).to_contain_text(new_workspace[:5])
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)


    @allure.title("Project Dashboard: Create New Funnel from Template")
    @allure.description("This test verifies that a new funnel can be created from a pre-existing template.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Creation")
    @allure.story("Create from Template")
    @pytest.mark.ui
    def test_create_new_funnel_with_template(self, project_page:ProjectPage, templates_page: TemplatesPage,new_workspace):
        template_name = "Market Research Survey"

        project_page.create_new_funnel_with_template()

        templates_page.search_template(template_name)
        templates_page.choose_template(template_name)

        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)

        expect(project_page.FUNNEL_TITLES_LIST).to_contain_text([template_name])


    @allure.title("Project Dashboard: Delete All Funnels in a Workspace")
    @allure.description("This test verifies that all funnels within a workspace can be deleted.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Delete All Funnels")
    @pytest.mark.ui
    def test_delete_funnels(self,project_page:ProjectPage,new_workspace):
        fnl1_name = "Test Funnel 1"
        fnl2_name = "Test Funnel 2"
        project_page.create_new_funnel_from_scratch(fnl1_name,"Thank You page")
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        project_page.create_new_funnel_from_scratch(fnl2_name, "Answer-based Outcomes")
        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(2)

        project_page.delete_all_funnels()
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(0)

        assert project_page.get_funnel_count_from_ws_list(new_workspace) == 0

    @allure.title("Project Dashboard: Publish a Funnel")
    @allure.description("This test verifies the full workflow of publishing a funnel and checking its status on the dashboard.")
    @allure.epic("Project Dashboard")
    @allure.feature("Funnel Management")
    @allure.story("Publish Funnel")
    @pytest.mark.ui
    def test_publish_funnel(self,project_page:ProjectPage,editor_page:EditorPage,new_workspace):
        fnl_name = "published funnel"
        project_page.create_new_funnel_from_scratch(fnl_name,"Score-based Outcomes")

        editor_page.add_elements(["Button","Heading"])

        editor_page.wait_for_page_load()
        editor_page.publish_funnel()

        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        project_page.goto_funnel_status("Published")
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl_name in project_page.get_all_funnel_titles()