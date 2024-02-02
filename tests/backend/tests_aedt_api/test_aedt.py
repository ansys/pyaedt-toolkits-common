import os

import pytest

from tests.backend.tests_aedt_api.conftest import skip_test


class TestAEDT:
    """AEDTCommon unit tests."""

    def test_00_connect_aedt(self, aedt_common, assert_handler):
        """Connect AEDT."""

        if skip_test():
            pytest.skip()

        assert aedt_common.connect_aedt()
        assert aedt_common.connect_aedt()
        assert aedt_common.release_aedt()

    def test_01_connect_design(self, aedt_common, assert_handler):
        """Connect design."""

        if skip_test():
            pytest.skip()

        assert aedt_common.connect_design()
        assert aedt_common.connect_design()
        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Maxwell3D")
        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Tesla")

    def test_02_open_project(self, aedt_common, assert_handler, aedt_example):
        """Open AEDT project."""

        if skip_test():
            pytest.skip()

        assert not aedt_common.open_project(aedt_example)

    def test_03_save_project(self, aedt_common, assert_handler, aedt_example):
        """Save AEDT project."""

        if skip_test():
            pytest.skip()

        assert aedt_common.save_project()
        new_project = os.path.join(os.path.dirname(aedt_example), "New.aedt")
        assert aedt_common.save_project(new_project)

    def test_04_get_design_names(self, aedt_common, assert_handler):
        """Get design names."""

        if skip_test():
            pytest.skip()

        design_names = aedt_common.get_design_names()
        assert isinstance(design_names, list)
        aedt_common.properties.active_project = aedt_common.properties.project_list[0]
        active_project_name = aedt_common.get_project_name(aedt_common.properties.active_project)
        aedt_common.properties.active_design = aedt_common.properties.design_list[active_project_name][0]
        design_names = aedt_common.get_design_names()
        assert len(design_names) == 3
