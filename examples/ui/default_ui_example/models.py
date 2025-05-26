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


class Properties(UIProperties, validate_assignment=True):
    """Store all properties."""


new_common_properties = {}
for common_key in general_settings:
    new_common_properties[common_key[0]] = common_key[1]

properties = Properties(**new_common_properties)
