import pytest

pytestmark = [pytest.mark.aedt]


class TestCommon:
    """Common unit tests."""

    def test_00_get_properties(self, common_instance):
        """Get properties."""

        api_properties = common_instance.get_properties()
        assert api_properties
