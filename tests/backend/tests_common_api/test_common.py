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

import pytest

pytestmark = [pytest.mark.common_api]


class TestCommon:
    """Class defining a workflow to test Common."""

    def test_00_get_properties(self, common):
        """Get properties."""

        api_properties = common.get_properties()
        assert api_properties

    def test_00_get_default_properties(self, common_default):
        """Get properties."""

        api_properties = common_default.get_properties()
        assert api_properties

    def test_01_set_properties(self, common):
        """Set properties."""

        new_properties = {}
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated

        new_properties = {
            "use_grpc": True,
            "is_toolkit_busy": False,
            "new_main_property": "hola",
            "new_main_property_in_section": "adios",
        }
        is_updated, _ = common.set_properties(new_properties)
        assert is_updated
        assert common.properties.use_grpc == new_properties["use_grpc"]
        assert (common.properties.test.section.new_main_property_in_section ==
                new_properties["new_main_property_in_section"])
        assert common.properties.test.new_main_property == new_properties["new_main_property"]

        common.properties.use_grpc = False
        api_properties = common.get_properties()
        assert not api_properties["use_grpc"]

        new_properties = {
            "is_toolkit_busy": False,
            "new_main_property": 20,
        }
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated

        new_properties = {"new_use_grpc": 10}
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated

    def test_02_installed_aedt_version(self, common):
        """Installed AEDT version."""
        installed_versions = common.installed_aedt_version()
        assert isinstance(installed_versions, list)
