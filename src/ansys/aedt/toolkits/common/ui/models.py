# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class UIProperties(BaseModel):
    """Store common UI properties."""

    toolkit_name: str = "common"
    backend_url: str = "127.0.0.1"
    backend_port: int = 5001
    debug: bool = True
    log_file: str = "common_frontend.log"
    app_name: str = "toolkit Wizard"
    main_title: str = "toolkit Template Wizard"
    welcome_message: str = "Welcome to the toolkit"
    version: str = "v0.0.1"
    copyright: str = "By: x"
    year: int = 2024
    logo: str = ""
    icon: str = ""
    startup_size: List[int] = Field(default_factory=list)
    minimum_size: List[int] = Field(default_factory=list)
    left_menu_size: Dict[str, int] = Field(default_factory=dict)
    left_menu_content_margins: int = 3
    left_column_size: Dict[str, int] = Field(default_factory=dict)
    right_column_size: Dict[str, int] = Field(default_factory=dict)
    progress_size: Dict[str, int] = Field(default_factory=dict)
    font: Dict[str, Any] = Field(default_factory=dict)
    high_resolution: bool = False
    theme: str = "ansys_dark.json"
    images: str = ""
    add_left_menus: List[Dict] = Field(default_factory=list)
    add_title_bar_menus: List[Dict] = Field(default_factory=list)
    block_settings_after_load: bool = True


class Properties(UIProperties, validate_assignment=True):
    """Store all properties."""


common_kwargs = {}
if os.path.isfile(os.path.join(os.path.dirname(__file__), "common_properties.toml")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.toml"), mode="rb") as file_handler:
        common_kwargs = tomllib.load(file_handler)

general_settings = Properties(**common_kwargs)
