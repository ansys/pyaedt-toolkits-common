# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import pytest

from ansys.aedt.toolkits.common.utils import ToolkitThreadStatus

pytestmark = [pytest.mark.rest_api]


class TestRESTAPI:
    """Class defining a workflow to test the Flask application REST API."""

    def test_00_get_status(self, client):
        response = client.get("/status")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert data == ToolkitThreadStatus.IDLE.value

    def test_01_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_02_get_properties(self, client):
        response = client.get("/properties")
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data.get("log_file")

    def test_03_set_properties(self, client):
        new_properties = {
            "port": "5002",
        }
        response = client.put("/properties", json=new_properties)
        assert response.status_code == 200
        response = client.get("/properties")
        data = json.loads(response.data.decode("utf-8"))
        assert data.get("port") == 5002
        new_properties = {
            "port": True,
        }
        response = client.put("/properties", json={})
        assert response.status_code == 500

    def test_04_installed_versions(self, client):
        response = client.get("/installed_versions")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, list)

    def test_05_aedt_sessions(self, client):
        response = client.get("/aedt_sessions")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, dict)

    def test_06_connect_design(self, client):
        response = client.post("/connect_design", json={"aedtapp": "Icepak"})
        assert response.status_code == 200

        response = client.post("/connect_design", json={})
        assert response.status_code == 500

    def test_07_save_project(self, client, common_temp_dir):
        new_project = os.path.join(common_temp_dir, "New.aedt")
        response = client.post("/save_project", json=new_project)
        assert response.status_code == 200
        assert os.path.exists(new_project)
        response = client.post("/save_project", json={})
        assert response.status_code == 500

    def test_08_get_design_names(self, client):
        response = client.get("/design_names")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert isinstance(data, list)

    def test_09_wait_thread(self, client):
        response = client.get("/wait_thread", data={})
        assert response.status_code == 500

    def test_10_open_project(self, client):
        response = client.post("/open_project", data={})
        assert response.status_code == 500

    def test_11_close_aedt(self, client):
        response = client.post("/close_aedt", json={})
        assert response.status_code == 500
        response = client.post("/close_aedt", json=[True])
        assert response.status_code == 500

    def test_12_get_aedt_model(self, client):
        response = client.get("/get_aedt_model", json={})
        assert response.status_code == 500
