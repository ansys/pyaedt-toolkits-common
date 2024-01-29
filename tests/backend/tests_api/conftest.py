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

You can enable the API log file in the backend_properties.json.

"""

import json
import logging
import os
import pathlib
import shutil
import tempfile

from pyaedt import settings
from pyaedt.generic.filesystem import Scratch
import pytest
from tests_api.models import properties

# Constants
PROJECT_NAME = "Test"

config = {
    "desktop_version": properties.aedt_version,
    "non_graphical": properties.non_graphical,
    "use_grpc": properties.use_grpc,
}

# Check for the local config file, override defaults if found
local_path = os.path.dirname(os.path.realpath(__file__))
local_config_file = os.path.join(local_path, "local_config.json")
if os.path.exists(local_config_file):
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

properties.use_grpc = config.get("use_grpc", True)
properties.non_graphical = config["non_graphical"]
properties.aedt_version = config["desktop_version"]

com_non_graphical = False
if not properties.use_grpc and properties.non_graphical:
    com_non_graphical = True

# The import should be here to have the updated properties
from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.api import Common
from ansys.aedt.toolkits.common.backend.api import EDBCommon

settings.enable_error_handler = False
settings.enable_desktop_logs = False
settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["non_graphical"]

scratch_path = tempfile.gettempdir()
local_scratch = Scratch(scratch_path)

input_data_dir = pathlib.Path(__file__).parent.parent.parent
aedt_project = os.path.join(input_data_dir, "input_data", "Test.aedt")
aedt_scratch = shutil.copy(aedt_project, local_scratch.path)

edb_scratch = shutil.copytree(
    os.path.join(input_data_dir, "input_data", "edb_test.aedb"), os.path.join(local_scratch.path, "edb_test.aedb")
)

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
    logger.info("Common API initialization")
    common_api = Common(properties)
    yield common_api
    # Check if any test has failed
    if request.session.testsfailed == 0:
        cleanup_process()


@pytest.fixture(scope="session")
def aedt_common(request):
    logger.info("AEDTCommon API initialization")
    aedt_common = AEDTCommon(properties)
    if com_non_graphical:
        logger.error("COM in non graphical not allowed")
        yield aedt_common
    else:
        aedt_common.launch_thread(aedt_common.launch_aedt)
        is_aedt_launched = aedt_common.wait_to_be_idle()
        if is_aedt_launched:
            yield aedt_common
            aedt_common.release_aedt(True, True)
        else:
            logger.error("AEDT is not launched")

    # Check if any test has failed
    if request.session.testsfailed == 0:
        cleanup_process()


@pytest.fixture(scope="session")
def edb_common(request):
    logger.info("EDBCommon API initialization")
    edb_common = EDBCommon(properties)
    yield edb_common
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


@pytest.fixture(scope="session")
def aedt_example():
    return aedt_scratch


@pytest.fixture(scope="session")
def edb_example():
    return edb_scratch


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
