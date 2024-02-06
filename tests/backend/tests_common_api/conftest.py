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

import logging
import pathlib
import shutil

from pyaedt import settings
import pytest

# Load properties from backend_properties.json
from tests.backend.tests_common_api.models import properties
from tests.conftest import common_temp_dir

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


@pytest.fixture(scope="session")
def common(common_temp_dir):
    from ansys.aedt.toolkits.common.backend.api import Common

    logger = create_logger(common_temp_dir, "pytest_common_api.log")

    logger.info("Common API initialization")
    common_api = Common(properties)
    yield common_api
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
