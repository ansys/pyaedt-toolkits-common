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
import pytest


@pytest.mark.tests_aedt_api
class TestAEDT:
    """AEDTCommon unit tests."""

    def test_00_connect_aedt(self, aedt_common):
        """Connect AEDT."""

        assert aedt_common.connect_aedt()
        assert aedt_common.connect_aedt()
        assert aedt_common.release_aedt()

    def test_01_connect_design(self, aedt_common):
        """Connect design."""

        assert aedt_common.connect_design()
        assert aedt_common.connect_design()
        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Maxwell3D")
        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Tesla")

    def test_02_open_project(self, aedt_common, common_temp_dir):
        """Open AEDT project."""

        opened_project = os.path.join(common_temp_dir, "input_data", "Test.aedt")
        assert not aedt_common.open_project(opened_project)

    def test_03_save_project(self, aedt_common, common_temp_dir):
        """Save AEDT project."""

        assert aedt_common.save_project()
        new_project = os.path.join(common_temp_dir, "input_data", "New.aedt")
        assert aedt_common.save_project(new_project)

    def test_04_get_design_names(self, aedt_common):
        """Get design names."""

        design_names = aedt_common.get_design_names()
        number_designs = len(design_names)
        assert isinstance(design_names, list)
        aedt_common.properties.active_project = aedt_common.properties.project_list[0]
        active_project_name = aedt_common.get_project_name(aedt_common.properties.active_project)
        aedt_common.properties.active_design = aedt_common.properties.design_list[active_project_name][0]
        design_names = aedt_common.get_design_names()
        assert len(design_names) == 3
