import pytest

pytestmark = [pytest.mark.common_api]

class TestCommon:
    """Class defining a workflow to test Common."""

    def test_00_get_properties(self, common):
        """Get properties."""

        api_properties = common.get_properties()
        assert api_properties

    def test_01_set_properties(self, common):
        """Set properties."""

        new_properties = {}
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated

        new_properties = {
            "use_grpc": True,
            "is_toolkit_busy": False,
        }
        is_updated, _ = common.set_properties(new_properties)
        assert is_updated
        assert common.properties.use_grpc == new_properties["use_grpc"]

        common.properties.use_grpc = False
        api_properties = common.get_properties()
        assert not api_properties["use_grpc"]

        new_properties = {
            "use_grpc": 10,
            "is_toolkit_busy": False,
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
