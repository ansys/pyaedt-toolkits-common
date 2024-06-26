import os
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel

from ansys.aedt.toolkits.common.backend.models import CommonProperties
from ansys.aedt.toolkits.common.backend.models import common_properties


class ExampleProperties(BaseModel):
    """Store properties for the example"""
    multiplier: int = 1.0
    geometry: str = "Box"


class BackendProperties(BaseModel):
    """Store toolkit properties."""
    example: ExampleProperties


class Properties(BackendProperties, CommonProperties, validate_assignment=True):
    """Store all properties."""


backend_properties = {}
if os.path.isfile(os.path.join(os.path.dirname(__file__), "backend_properties.toml")):
    with open(os.path.join(os.path.dirname(__file__), "backend_properties.toml"), mode="rb") as file_handler:
        backend_properties = tomllib.load(file_handler)

toolkit_property = {}
if backend_properties:
    for backend_key in backend_properties:
        if backend_key == "defaults":
            for toolkit_key in backend_properties["defaults"]:
                if hasattr(common_properties, toolkit_key):
                    setattr(common_properties, toolkit_key, backend_properties["defaults"][toolkit_key])
        else:
            toolkit_property[backend_key] = backend_properties[backend_key]

new_common_properties = {}
for common_key in common_properties:
    new_common_properties[common_key[0]] = common_key[1]

properties = Properties(**toolkit_property, **new_common_properties)
