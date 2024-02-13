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

import pytest

from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.models import Properties
from tests.backend.conftest import read_local_config, setup_aedt_settings, DEFAULT_CONFIG, PROJECT_NAME

# Setup config
config = DEFAULT_CONFIG.copy()
local_cfg = read_local_config()
config.update(local_cfg)

# Update AEDT settings
setup_aedt_settings(config)

@pytest.fixture(scope="session")
def aedt_common(logger):
    """Initialize toolkit with common API."""
    logger.info("AEDTCommon API initialization")

    properties = Properties()
    properties.aedt_version = config["desktop_version"]
    properties.non_graphical = config["non_graphical"]
    properties.use_grpc = config["use_grpc"]
    properties.debug = config["debug"]

    aedt_common = AEDTCommon(properties)

    if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
        logger.error("COM in non graphical not allowed")
        yield aedt_common
    else:
        aedt_common.launch_thread(aedt_common.launch_aedt)
        is_aedt_launched = aedt_common.wait_to_be_idle()
        if is_aedt_launched:
            yield aedt_common
        else:
            logger.error("AEDT is not launched")

    aedt_common.release_aedt(True, True)
