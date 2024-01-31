import json
import os

from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus


class TestRESTAPI:
    def test_00_get_status(self, client, assert_handler):
        response = client.get("/status")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert data == ToolkitThreadStatus.IDLE.value

    def test_01_health(self, client, assert_handler):
        response = client.get("/health")
        assert response.status_code == 200

    def test_02_get_properties(self, client, assert_handler):
        response = client.get("/properties")
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data.get("log_file")

    def test_03_set_properties(self, client, assert_handler):
        new_properties = {
            "port": "5002",
        }
        response = client.put("/properties", json=new_properties)
        assert response.status_code == 200
        response = client.get("/properties")
        data = json.loads(response.data.decode("utf-8"))
        assert data.get("port") == 5002

    def test_04_installed_versions(self, client, assert_handler):
        response = client.get("/installed_versions")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, list)

    def test_05_aedt_sessions(self, client, assert_handler):
        response = client.get("/aedt_sessions")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, dict)

    def test_06_connect_design(self, client, assert_handler):
        response = client.post("/connect_design", json={"aedtapp": "Icepak"})
        assert response.status_code == 200

    def test_07_save_project(self, client, assert_handler, aedt_example):
        new_project = os.path.join(os.path.dirname(aedt_example), "New.aedt")
        response = client.post("/save_project", json=new_project)
        assert response.status_code == 200
        assert os.path.exists(new_project)

    def test_08_get_design_names(self, client, assert_handler):
        response = client.get("/design_names")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, list)
