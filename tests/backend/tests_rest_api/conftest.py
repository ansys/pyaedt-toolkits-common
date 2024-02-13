"""
REST API Test Configuration Module
----------------------------------

Description
===========
This module contains the configuration and fixture for the pytest-based tests for the REST API.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.2",
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
        response = client.get("/wait_thread", json=timeout)
        aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedt")
        client.post("/open_project", json=aedt_file)
        assert response.status_code == 200

        yield client

        close_properties = {"close_projects": True, "close_on_exit": True}
        client.post("/close_aedt", json=close_properties)
