import os
import sys
from typing import List

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel
from pydantic import Field

from ansys.aedt.toolkits.common.ui.models import UIProperties
from ansys.aedt.toolkits.common.ui.models import general_settings


class ExampleProperties(BaseModel):
    """Store toolkit properties."""
    primitives_created: List[str] = Field(default_factory=list)


class FrontendProperties(BaseModel):
    """Store toolkit properties."""
    example: ExampleProperties


class Properties(FrontendProperties, UIProperties, validate_assignment=True):
    """Store all properties."""


frontend_properties = {}
if "PYAEDT_TOOLKIT_CONFIG_DIR" in os.environ:
    local_dir = os.path.abspath(os.environ["PYAEDT_TOOLKIT_CONFIG_DIR"])
    frontend_config = os.path.join(local_dir, "frontend_properties.toml")
    if os.path.isfile(frontend_config):
        with open(frontend_config, mode="rb") as file_handler:
            frontend_properties = tomllib.load(file_handler)

if not frontend_properties and os.path.isfile(os.path.join(os.path.dirname(__file__), "frontend_properties.toml")):
    with open(os.path.join(os.path.dirname(__file__), "frontend_properties.toml"), mode="rb") as file_handler:
        frontend_properties = tomllib.load(file_handler)

toolkit_property = {}
if frontend_properties:
    for frontend_key in frontend_properties:
        if frontend_key == "defaults":
            for toolkit_key in frontend_properties["defaults"]:
                if hasattr(general_settings, toolkit_key):
                    setattr(general_settings, toolkit_key, frontend_properties["defaults"][toolkit_key])
        else:
            toolkit_property[frontend_key] = frontend_properties[frontend_key]

new_common_properties = {}
for common_key in general_settings:
    new_common_properties[common_key[0]] = common_key[1]

properties = Properties(**toolkit_property, **new_common_properties)
