import pytest


@pytest.mark.common
class TestCommon:
    """Common unit tests."""

    def test_00_get_properties(self, common, assert_handler, request):
        """Get properties."""

        api_properties = common.get_properties()
        assert api_properties

    def test_01_set_properties(self, common, assert_handler, request):
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

        new_properties = {
            "use_grpc": 10,
            "is_toolkit_busy": False,
        }
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated

        new_properties = {"new_use_grpc": 10}
        is_updated, _ = common.set_properties(new_properties)
        assert not is_updated
        request.node.get_closest_marker(name="common")
