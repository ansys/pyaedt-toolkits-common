import json
import os
from typing import List

from pydantic import BaseModel
from pydantic import Field

from ansys.aedt.toolkits.common.ui.models import UIProperties
from ansys.aedt.toolkits.common.ui.models import general_settings


class FrontendProperties(BaseModel):
    """Store toolkit properties."""

    primitives_created: List[str] = Field(default_factory=list)


class Properties(FrontendProperties, UIProperties, validate_assignment=True):
    """Store all properties."""


backend_properties = {}
if os.path.exists(os.path.join(os.path.dirname(__file__), "frontend_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "frontend_properties.json")) as file_handler:
        backend_properties = json.load(file_handler)

toolkit_property = {}
if backend_properties:
    for backend_key in backend_properties:
        if hasattr(general_settings, backend_key):
            setattr(general_settings, backend_key, backend_properties[backend_key])
        else:
            toolkit_property[backend_key] = backend_properties[backend_key]

new_common_properties = {}
for common_key in general_settings:
    new_common_properties[common_key[0]] = common_key[1]

properties = Properties(**toolkit_property, **new_common_properties)
