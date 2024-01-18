"""
AEDT Common Test Configuration Module
------------------------------------

Description
===========
This module contains the configuration and fixture for the pytest-based tests for AEDT.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.2",
  "non_graphical": false,
  "use_grpc": true
}

"""

import json
import logging
import os

from pyaedt import settings
import pytest

from ansys.aedt.toolkits.common.backend.api import Common

# from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus

# Constants
PROJECT_NAME = "Test"
AEDT_DEFAULT_VERSION = "2023.2"

config = {
    "desktop_version": AEDT_DEFAULT_VERSION,
    "non_graphical": True,
    "use_grpc": True,
}

# Check for the local config file, override defaults if found
local_path = os.path.dirname(os.path.realpath(__file__))
local_config_file = os.path.join(local_path, "local_config.json")
if os.path.exists(local_config_file):
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

settings.enable_error_handler = False
settings.enable_desktop_logs = False
settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["non_graphical"]


@pytest.fixture(scope="class")
def common_instance():
    """Initialize the Common object for testing."""
    common_api = Common()

    # Log the start of the test
    logging.info("Test Started")

    # Provide the Common instance to tests
    yield common_api

    # Log the end of the test
    logging.info("Test Completed")
