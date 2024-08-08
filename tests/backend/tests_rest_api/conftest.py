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

"""
API Test Configuration Module
-----------------------------

Description
===========
This module contains the configuration and fixture for the pytest-based tests for the API.

The default configuration can be changed by placing a file called local_config.json.
An example of the contents of local_config.json:

{
  "desktop_version": "2024.2",
  "non_graphical": false,
  "use_grpc": true
}

You can enable the API log file in the backend_properties.json.

"""

import os
import pytest

from tests.backend.conftest import read_local_config, setup_aedt_settings, DEFAULT_CONFIG, PROJECT_NAME
from ansys.aedt.toolkits.common.backend.rest_api import app

# Setup config
config = DEFAULT_CONFIG.copy()
local_cfg = read_local_config()
config.update(local_cfg)

# Update AEDT settings
setup_aedt_settings(config)


@pytest.fixture(scope="session")
def client(logger, common_temp_dir):
    """Create a test client."""
    logger.info("Client initialization")
    app.testing = True

    with app.test_client() as client:
        properties = {
            "aedt_version": config["desktop_version"],
            "non_graphical": config["non_graphical"],
            "use_grpc": config["use_grpc"],
            "debug": config["debug"],
        }
        client.put("/properties", json=properties)
        client.post("/launch_aedt")
        timeout = 60
        client.get("/wait_thread", json=timeout)
        aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedt")
        response = client.post("/open_project", data=aedt_file)
        assert response.status_code == 200

        yield client

        close_properties = {"close_projects": True, "close_on_exit": True}
        client.post("/close_aedt", json=close_properties)
