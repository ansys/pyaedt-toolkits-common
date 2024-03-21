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

import os
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from typing import Any
from typing import Dict
from typing import List

from ansys.aedt.toolkits.common.backend.models import CommonProperties
from ansys.aedt.toolkits.common.backend.models import common_properties
from pydantic import BaseModel


class Section(BaseModel, validate_assignment=True):
    """Store section properties."""

    new_main_property_in_section: str = ""


class TestProperties(BaseModel, validate_assignment=True):
    """Store antenna properties."""

    new_main_property: str = ""
    section: Section = Section()


class BackendProperties(BaseModel):
    """Store toolkit properties."""

    test: TestProperties


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

properties = Properties(test=TestProperties(**toolkit_property), **new_common_properties)
