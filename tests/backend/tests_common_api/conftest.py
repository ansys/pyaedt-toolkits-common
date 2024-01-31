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
import os
import shutil
import tempfile

from pyaedt.generic.filesystem import Scratch
import pytest
from tests_common_api.models import properties

scratch_path = tempfile.gettempdir()
local_scratch = Scratch(scratch_path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = os.path.join(local_scratch.path, "pytest_api.log")
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@pytest.fixture(scope="session")
def common(request):
    from ansys.aedt.toolkits.common.backend.api import Common

    logger.info("Common API initialization")
    common_api = Common(properties)
    yield common_api
    # Check if any test has failed
    if request.session.testsfailed == 0:
        cleanup_process()


failed_tests = set()


def pytest_runtest_makereport(item, call):
    if call.excinfo is not None and call.excinfo.typename == "AssertionError":
        failed_tests.add(item)


@pytest.fixture(scope="session")
def assert_handler(request):
    def finalizer():
        # Code to run after the test
        logger.info("Test Teardown")
        # Check if any test has failed during the session
        if request.session.testsfailed != 0:
            # Additional code to run when an assert fails
            for failed_test in failed_tests:
                logger.error(f"FAILED: {failed_test.name}")

    request.addfinalizer(finalizer)

    return assert_handler


def skip_test(skip=False):
    skip_flag = False
    if com_non_graphical or skip:
        skip_flag = True
    return skip_flag


def cleanup_process():
    """Cleanup process after the test is completed."""
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
    shutil.rmtree(local_scratch.path, ignore_errors=True)
