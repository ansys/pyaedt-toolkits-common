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

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib
else:
    import tomli as tomllib

from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class CommonProperties(BaseModel):
    """Stores common AEDT properties."""

    aedt_version: str = "2024.1"
    non_graphical: bool = False
    active_project: str = ""
    active_design: str = ""
    project_list: List[str] = Field(default_factory=list)
    design_list: Dict[str, List[str]] = Field(default_factory=dict)
    selected_process: int = 0
    use_grpc: bool = True
    is_toolkit_busy: bool = False
    url: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    toolkit_name: str = "common"
    log_file: str = "common_backend.log"


class Properties(CommonProperties, validate_assignment=True):
    """Stores all properties."""

    def __repr__(self):  # pragma: no cover
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Properties({attributes})"


common_kwargs = {}
if os.path.isfile(os.path.join(os.path.dirname(__file__), "common_properties.toml")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.toml"), mode="rb") as file_handler:
        common_kwargs = tomllib.load(file_handler)

common_properties = Properties(**common_kwargs)
