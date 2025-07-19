# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

from unittest.mock import patch

import pytest

MOCK_PROPERTIES = {
    "version": "0.1",
    "active_project": "Dummy project",
    "project_list": ["Dummy project"],
    "design_list": {"Dummy project": "Dummy design"},
    "example": {},
}


@pytest.fixture
def patched_window_methods():
    with (patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.check_connection",
                return_value=True),
          patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.get_properties",
                return_value=MOCK_PROPERTIES),
          patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.installed_versions",
                return_value=["25.1"]),
          patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.SettingsMenu.process_id",
                return_value=12345),
          patch("ansys.aedt.toolkits.common.ui.actions_generic.FrontendGeneric.set_properties",
                return_value=None)):
        yield
