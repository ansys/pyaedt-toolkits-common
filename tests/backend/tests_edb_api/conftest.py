"""
API Test Configuration Module
-----------------------------

Description
===========
This module contains the configuration and fixture for the pytest-based tests for the API.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.2"
}

You can enable the API log file in the backend_properties.json.

"""

import pytest

from ansys.aedt.toolkits.common.backend.api import EDBCommon
from ansys.aedt.toolkits.common.backend.models import Properties
from tests.backend.conftest import read_local_config, setup_aedt_settings, DEFAULT_CONFIG

# Setup config
config = DEFAULT_CONFIG.copy()
local_cfg = read_local_config()
config.update(local_cfg)

# Update AEDT settings
setup_aedt_settings(config)


@pytest.fixture(scope="session")
def edb_common(logger):
    """Initialize toolkit with common EDB API."""
    logger.info("EDBCommon API initialization")

    properties = Properties()
    properties.aedt_version = config["desktop_version"]
    properties.non_graphical = config["non_graphical"]
    properties.use_grpc = config["use_grpc"]
    properties.debug = config["debug"]

    edb_common = EDBCommon(properties)

    yield edb_common
