import pytest


@pytest.mark.aedt
class TestAEDT:
    """AEDTCommon unit tests."""

    def test_00_aedt_connected(self, aedt_common, assert_handler):
        """Get properties."""

        connected, msg = aedt_common.is_aedt_connected()
        assert not connected
