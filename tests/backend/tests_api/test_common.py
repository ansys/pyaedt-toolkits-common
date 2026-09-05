import pytest


@pytest.mark.common
class TestCommon:
    """Common unit tests."""

    def test_00_get_properties(self, common, assert_handler):
        """Get properties."""

        api_properties = common.get_properties()
        assert api_properties
        assert common.properties.new_property == api_properties["new_property"]

    def test_01_set_properties(self, common, assert_handler):
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

    def test_02_installed_aedt_version(self, common, assert_handler):
        """Installed AEDT version."""
