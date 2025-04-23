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

pytestmark = [pytest.mark.aedt_common_api]


class TestAEDTCommon:
    """Class defining a workflow to test AEDTCommon."""

    def test_00_connect_aedt(self, aedt_common):
        """Connect AEDT."""

        assert aedt_common.connect_aedt()
        assert aedt_common.connect_aedt()

    def test_01_open_project(self, aedt_common):
        """Open AEDT project."""

        assert aedt_common.open_project(aedt_common.properties.active_project)
        assert not aedt_common.open_project(aedt_common.properties.active_project)

    def test_02_connect_design(self, aedt_common):
        """Connect design."""

        assert aedt_common.connect_design()
        assert aedt_common.connect_design()

        aedt_common.properties.active_design = "Maxwell3D_Test"
        assert aedt_common.connect_design("Maxwell3D")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 2
        assert "Maxwell3D_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Layout_Test"
        assert aedt_common.connect_design("HFSS 3D Layout Design")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 3
        assert "Layout_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Icepak_Test"
        assert aedt_common.connect_design("Icepak")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 4
        assert "Icepak_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Circuit_Test"
        assert aedt_common.connect_design("Circuit Design")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 5
        assert "Circuit_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Maxwell2D_Test"
        assert aedt_common.connect_design("Maxwell 2D")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 6
        assert "Maxwell2D_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Maxwell_Circuit_Test"
        assert aedt_common.connect_design("Maxwell Circuit")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 7
        assert "Maxwell_Circuit_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Q2D_Test"
        assert aedt_common.connect_design("Q2D")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 8
        assert "Q2D_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Q3D_Test"
        assert aedt_common.connect_design("Q3D")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 9
        assert "Q3D_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "RMxprt_Test"
        assert aedt_common.connect_design("RMxprt")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 10
        assert "RMxprt_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "TwinBuilder_Test"
        assert aedt_common.connect_design("TwinBuilder")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 11
        assert "TwinBuilder_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "Mechanical_Test"
        assert aedt_common.connect_design("Mechanical")
        assert len(aedt_common.properties.design_list["Test_Common"]) == 12
        assert "Mechanical_Test" in aedt_common.properties.design_list["Test_Common"]

        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Tesla")

    def test_03_save_project(self, aedt_common, common_temp_dir):
        """Save AEDT project."""

        assert aedt_common.save_project()
        new_aedt_file = os.path.join(common_temp_dir, "input_data", "New.aedt")
        assert aedt_common.save_project(new_aedt_file)

    def test_04_get_design_names(self, aedt_common):
        """Get design names."""

        design_names = aedt_common.get_design_names()
        assert isinstance(design_names, list)

        aedt_common.properties.active_project = aedt_common.properties.project_list[0]
        active_project_name = aedt_common.get_project_name(aedt_common.properties.active_project)
        aedt_common.properties.active_design = aedt_common.properties.design_list[active_project_name][0]
        design_names = aedt_common.get_design_names()
        assert len(design_names) == 13

    def test_05_get_aedt_model(self, aedt_common, common_temp_dir):
        """Get aedt model."""

        aedt_common.properties.active_design = "Maxwell3D_Test"
        aedt_common.connect_design("Maxwell3D")
        assert aedt_common.aedtapp.modeler.create_box([0, 0, 0], [10, 20, 30])
        assert aedt_common.release_aedt()
        encoded_files = aedt_common.export_aedt_model(air_objects=True, encode=True, export_path=common_temp_dir)
        assert isinstance(encoded_files, dict)
        files = aedt_common.export_aedt_model(air_objects=True, encode=False, export_path=common_temp_dir)
        assert isinstance(files, list)

