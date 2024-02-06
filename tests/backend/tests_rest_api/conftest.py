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

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.2",
  "non_graphical": false,
  "use_grpc": true
}

You can enable the API log file in the backend_properties.json.

"""

import json
import logging
import pathlib
import shutil

from pyaedt import settings
import pytest

# Load properties from backend_properties.json
from tests.backend.tests_rest_api.models import properties
from tests.conftest import common_temp_dir

config = {
    "desktop_version": properties.aedt_version,
    "non_graphical": properties.non_graphical,
    "use_grpc": properties.use_grpc,
    "debug": False,
}

# Check for the local config file, override defaults if found
local_path = pathlib.Path(__file__).resolve().parent
local_config_file = pathlib.Path(local_path, "local_config.json")
if local_config_file.exists():
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

settings.enable_error_handler = False
settings.enable_desktop_logs = False
settings.use_grpc_api = config["use_grpc"]
settings.non_graphical = config["non_graphical"]

failed_tests = set()


def create_logger(temp_dir, name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    log_file = pathlib.Path(temp_dir, name)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def release_logger(logger):
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


from ansys.aedt.toolkits.common.backend.rest_api import app


@pytest.fixture(scope="session")
def client(common_temp_dir):
    logger = create_logger(common_temp_dir, "pytest_rest_api.log")

    logger.info("Client initialization")
    with app.test_client() as client:
        new_properties = {
            "aedt_version": config["desktop_version"],
            "non_graphical": config["non_graphical"],
            "use_grpc": config["use_grpc"],
            "debug": config["debug"],
        }
        client.put("/properties", json=new_properties)

        client.post("/launch_aedt")
        response = client.get("/wait_thread", json=60)
        if response.status_code == 200:
            aedt_project = pathlib.Path(common_temp_dir, "input_data", "Test.aedt")
            open_project_response = client.post("/open_project", json=str(aedt_project))
            if open_project_response.status_code == 200:
                yield client
            else:
                logger.error("Open project failed")
            close_properties = {"close_projects": True, "close_on_exit": True}
            client.post("/close_aedt", json=close_properties)
        else:
            logger.error("Launch AEDT failed")

        # Check if any test has failed
        if not failed_tests:
            logger.info(f"All tests passed successfully")
            release_logger(logger)
            shutil.rmtree(pathlib.Path(common_temp_dir.parent), ignore_errors=True)
        else:
            for failed_test in failed_tests:
                logger.error(f"FAILED: {failed_test.name}")
            release_logger(logger)


def pytest_runtest_makereport(item, call):
    if call.excinfo is not None and call.excinfo.typename == "AssertionError":
        failed_tests.add(item)
