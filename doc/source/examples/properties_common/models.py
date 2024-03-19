import json
import os
from typing import List

from pydantic import BaseModel
from pydantic import Field

from ansys.aedt.toolkits.common.backend.models import CommonProperties
from ansys.aedt.toolkits.common.backend.models import common_properties


class BackendProperties(BaseModel):
    """Store toolkit properties."""

    invented_property: List[int] = Field(default_factory=list)
    test: str = "hola"


class Properties(BackendProperties, CommonProperties, validate_assignment=True):
    """Store all properties."""


backend_properties = {}
if os.path.isfile(os.path.join(os.path.dirname(__file__), "backend_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "backend_properties.json")) as file_handler:
        backend_properties = json.load(file_handler)

toolkit_property = {}
if backend_properties:
    for backend_key in backend_properties:
        if hasattr(common_properties, backend_key):
            setattr(common_properties, backend_key, backend_properties[backend_key])
        else:
            toolkit_property[backend_key] = backend_properties[backend_key]

new_common_properties = {}
for common_key in common_properties:
    new_common_properties[common_key[0]] = common_key[1]

properties = Properties(**toolkit_property, **new_common_properties)
