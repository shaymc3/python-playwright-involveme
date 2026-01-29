import pytest
from playwright.sync_api import expect
from pages import ProjectPage, EditorPage, ConfigurePage

@pytest.fixture
def new_workspace(project_page:ProjectPage):
    ws_count = project_page.get_workspace_count()
    ws_name = f"Test Workspace {ws_count + 1}"
    project_page.create_new_workspace(ws_name)

    assert ws_name in project_page.get_all_workspace_titles(), \
        f"Workspace '{ws_name}' was not created"

    yield ws_name

class TestProjectDash:

    def test_assert_page_title(self,project_page:ProjectPage):
        expect(project_page.page).to_have_title("Funnels | involve.me")

    def test_sort_funnel_by_name_desc(self, project_page:ProjectPage,new_workspace):

        fnl_name_list = ["AAA","BBB","CCC"]

        project_page.create_funnels(new_workspace,fnl_name_list)
        project_page.go_to_workspace(new_workspace)
        project_page.funnel_sort_by("name-asc")
        funnel_title_list = project_page.get_all_funnel_titles()

        assert project_page.is_funnel_sorted_by(funnel_title_list, "asc")

    def test_create_new_workspace(self, project_page,new_workspace):
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(0)

        assert new_workspace in project_page.get_all_workspace_titles()

    def test_change_workspace_name(self, project_page:ProjectPage,new_workspace):
        new_ws_name = "Test Workspace rename"
        project_page.rename_workspace(new_workspace,new_ws_name)
        expect(project_page.page.get_by_text(new_workspace).last).not_to_be_visible()

        assert new_ws_name in project_page.get_all_workspace_titles()

    def test_delete_workspace(self,project_page:ProjectPage,new_workspace):
        project_page.delete_workspace_by_name(new_workspace)

        assert new_workspace not in project_page.get_all_workspace_titles()

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

    def test_move_funnel_to_workspace(self,project_page:ProjectPage,new_workspace):
        fnl_name = "Funnel 1"
        new_ws = "Move To Workspace"
        project_page.create_new_funnel_from_scratch(fnl_name,"Thank You page")
        project_page.goto_project_page()
        project_page.create_new_workspace(new_ws)
        project_page.go_to_workspace(new_workspace)
        project_page.funnel_dropdown_menu_option(fnl_name,"Move to workspace")
        project_page.funnel_move_to_workspace(new_ws)
        project_page.go_to_workspace(new_ws)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl_name in project_page.get_all_funnel_titles()

    def test_create_new_funnel_from_scratch(self, project_page:ProjectPage):
        ws_name = "Test Workspace 05"
        fnl_name = "Test Funnel 05"
        project_page.create_new_workspace(ws_name)
        project_page.create_new_funnel_from_scratch(fnl_name,"Thank You page")
        project_page.goto_project_page()
        project_page.go_to_workspace(ws_name)

        assert fnl_name in project_page.get_all_funnel_titles()

    def test_create_new_funnel_with_ai(self, project_page: ProjectPage,editor_page:EditorPage):
        ws_name = "Test Workspace 06"
        project_page.create_new_workspace(ws_name)
        project_page.create_new_funnel_with_ai("Create an appointment funnel designed")
        expect(editor_page.WORKSPACE_TITLE).to_contain_text(ws_name[:5])

        project_page.goto_project_page()
        project_page.go_to_workspace(ws_name)
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)
        assert project_page.get_funnel_count_from_ws_list(ws_name) == 1

    def test_delete_all_funnels(self,project_page:ProjectPage,new_workspace):
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

    def test_publish_funnel(self,project_page:ProjectPage,editor_page:EditorPage,configure_page:ConfigurePage,new_workspace):
        fnl_name = "Test Funnel"
        fnl_new_name = "published funnel"
        project_page.create_new_funnel_from_scratch(fnl_name,"Score-based Outcomes")

        editor_page.add_element_and_close("Button")
        editor_page.publish_funnel()

        configure_page.change_funnel_name(fnl_new_name)
        configure_page.publish_funnel()

        project_page.goto_project_page()
        project_page.go_to_workspace(new_workspace)
        project_page.goto_funnel_status("Published")
        expect(project_page.FUNNEL_BLOCK_LIST).to_have_count(1)

        assert fnl_new_name in project_page.get_all_funnel_titles()



