import os
import pytest

from tests.backend.conftest import PROJECT_NAME

pytestmark = [pytest.mark.aedt_common_api]

class TestAEDTCommon:
    """Class defining a workflow to test AEDTCommon."""

    def test_00_connect_aedt(self, aedt_common):
        """Connect AEDT."""

        if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
            pytest.skip("Unauthorized configuration (COM and non graphical)")
        
        assert aedt_common.connect_aedt()
        assert aedt_common.connect_aedt()
        assert aedt_common.release_aedt()

    def test_01_connect_design(self, aedt_common):
        """Connect design."""

        if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
            pytest.skip("Unauthorized configuration (COM and non graphical)")

        assert aedt_common.connect_design()
        assert aedt_common.connect_design()

        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Maxwell3D")

        aedt_common.properties.active_design = "No Design"
        assert aedt_common.connect_design("Tesla")

    def test_02_open_project(self, aedt_common, common_temp_dir):
        """Open AEDT project."""

        if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
            pytest.skip("Unauthorized configuration (COM and non graphical)")

        aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedt")
        aedt_common.open_project(aedt_file)
        assert not aedt_common.open_project(aedt_file)

    def test_03_save_project(self, aedt_common, common_temp_dir):
        """Save AEDT project."""

        if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
            pytest.skip("Unauthorized configuration (COM and non graphical)")

        assert aedt_common.save_project()
        new_aedt_file = os.path.join(common_temp_dir, "input_data", "New.aedt")
        assert aedt_common.save_project(new_aedt_file)

    def test_04_get_design_names(self, aedt_common):
        """Get design names."""

        if not aedt_common.properties.use_grpc and aedt_common.properties.non_graphical:
            pytest.skip("Unauthorized configuration (COM and non graphical)")

        design_names = aedt_common.get_design_names()
        assert isinstance(design_names, list)
        aedt_common.properties.active_project = aedt_common.properties.project_list[0]
        active_project_name = aedt_common.get_project_name(aedt_common.properties.active_project)
        aedt_common.properties.active_design = aedt_common.properties.design_list[active_project_name][0]
        design_names = aedt_common.get_design_names()
        assert len(design_names) == 3
